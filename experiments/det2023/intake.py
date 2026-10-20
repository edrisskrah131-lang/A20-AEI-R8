"""Audit the labeled COCO population and create a reviewed, grouped split."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import random

from PIL import Image


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def contained(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Image escapes the supplied image directory: {path}")
    return path


def fingerprint(path):
    with Image.open(path) as image:
        image = image.convert("RGB")
        width, height = image.size
        digest = hashlib.sha256(f"RGB:{width}:{height}:".encode() + image.tobytes())
        small = image.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
        pixels = small.tobytes()
        bits = 0
        for row in range(8):
            for col in range(8):
                bits = (bits << 1) | (pixels[row * 9 + col] > pixels[row * 9 + col + 1])
        return width, height, digest.hexdigest(), f"{bits:016x}"


def audit(annotations, images_root, output):
    images_root, output = Path(images_root).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    records, sources, category_names = [], {}, set()
    seen_annotation_files = set()
    for annotation in annotations:
        annotation = Path(annotation).resolve()
        if annotation in seen_annotation_files:
            raise ValueError("The same annotation file was supplied twice")
        seen_annotation_files.add(annotation)
        data = json.loads(annotation.read_text())
        source_id = sha(annotation)
        if source_id in sources:
            raise ValueError("Identical annotation files must not be counted twice")
        sources[source_id] = str(annotation)
        categories = {int(c["id"]): str(c["name"]) for c in data["categories"]}
        if len(categories) != len(data["categories"]) or len(set(categories.values())) != len(categories):
            raise ValueError("Duplicate category identifiers or category names")
        category_names.update(categories.values())
        images = {int(i["id"]): i for i in data["images"]}
        if len(images) != len(data["images"]):
            raise ValueError("Duplicate COCO image IDs within one annotation file")
        targets = {key: [] for key in images}
        annotation_ids = set()
        for target in data["annotations"]:
            if target["id"] in annotation_ids:
                raise ValueError("Duplicate COCO annotation IDs")
            annotation_ids.add(target["id"])
            image_id, category_id = int(target["image_id"]), int(target["category_id"])
            if image_id not in images or category_id not in categories:
                raise ValueError("Annotation references an unknown image or category")
            x, y, width, height = map(float, target["bbox"])
            image = images[image_id]
            if not all(math.isfinite(v) for v in [x, y, width, height]):
                raise ValueError("Nonfinite bounding box")
            if (x < 0 or y < 0 or width <= 0 or height <= 0
                    or x + width > image["width"] + 1e-6
                    or y + height > image["height"] + 1e-6):
                raise ValueError(f"Invalid bounding box in image {image_id}")
            if target.get("iscrowd", 0) or target.get("ignore", 0):
                raise ValueError("Crowd/ignore targets require an explicit scoring policy")
            targets[image_id].append({
                "category": categories[category_id], "bbox": [x, y, width, height],
                "annotation_id": target["id"],
            })
        for image_id, image in sorted(images.items()):
            path = contained(images_root, images_root / image["file_name"])
            if not path.is_file():
                raise FileNotFoundError(f"COCO image is missing: {path}")
            width, height, pixel_hash, dhash = fingerprint(path)
            if (width, height) != (image["width"], image["height"]):
                raise ValueError(f"COCO dimensions differ from image bytes: {path}")
            records.append({
                "uid": f"{source_id[:16]}:{image_id}", "coco_image_id": image_id,
                "annotation_sha256": source_id, "file_name": image["file_name"],
                "image_sha256": sha(path), "pixel_sha256": pixel_hash, "dhash": dhash,
                "width": width, "height": height, "targets": targets[image_id],
                "group_hints": {key: image[key] for key in
                               ["aircraft_id", "region_id", "session_id", "sequence_id"]
                               if key in image},
            })
    # Similarity proposes review candidates; it does not establish independence.
    pairs = []
    for index, left in enumerate(records):
        for right in records[index + 1:]:
            same_pixels = left["pixel_sha256"] == right["pixel_sha256"]
            distance = (int(left["dhash"], 16) ^ int(right["dhash"], 16)).bit_count()
            if same_pixels or distance <= 4:
                pairs.append({"uid_a": left["uid"], "uid_b": right["uid"],
                              "same_pixels": same_pixels, "dhash_distance": distance})
    result = {
        "schema": "a20-det2023-intake-v1", "images_root": str(images_root),
        "annotation_sources": sources, "labeled_records": len(records),
        "unique_image_files": len({r["image_sha256"] for r in records}),
        "unique_pixel_arrays": len({r["pixel_sha256"] for r in records}),
        "categories": sorted(category_names), "records": records,
        "duplicate_candidates": pairs, "independence_verified": False,
        "unlabeled_images_used_as_negative_examples": False,
        "formats_counted": ["COCO"],
    }
    save(output / "audit.json", result)
    with (output / "groups_template.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["uid", "file_name", "group_id", "group_basis"])
        writer.writeheader()
        for record in records:
            writer.writerow({"uid": record["uid"], "file_name": record["file_name"],
                             "group_id": "", "group_basis": ""})
    save(output / "duplicate_candidates.json", pairs)
    return result


def make_split(audit_path, groups_path, output, seed=20261020):
    audit_path, groups_path = Path(audit_path), Path(groups_path)
    data = json.loads(audit_path.read_text())
    records = {r["uid"]: r for r in data["records"]}
    root = Path(data["images_root"])
    for digest, annotation in data["annotation_sources"].items():
        if sha(annotation) != digest:
            raise ValueError("Annotations changed after audit")
    for record in records.values():
        if sha(contained(root, root / record["file_name"])) != record["image_sha256"]:
            raise ValueError("An image changed after audit")
    with groups_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    groups = {}
    for row in rows:
        uid = row["uid"]
        if uid not in records or uid in groups:
            raise ValueError("Unknown or duplicated UID in grouping manifest")
        if not row.get("group_id", "").strip() or not row.get("group_basis", "").strip():
            raise ValueError("Every image needs a reviewed capture group and its provenance")
        groups[uid] = row["group_id"].strip()
    if set(groups) != set(records):
        raise ValueError("Grouping manifest must cover every audited image")
    # Coarsen supplied capture groups when pixel similarity connects them.
    # Neither this merge nor a user-provided group label proves independence.
    parent = {group: group for group in groups.values()}

    def find(group):
        while parent[group] != group:
            parent[group] = parent[parent[group]]
            group = parent[group]
        return group

    for pair in data["duplicate_candidates"]:
        a, b = find(groups[pair["uid_a"]]), find(groups[pair["uid_b"]])
        if a != b:
            parent[max(a, b)] = min(a, b)
    components = sorted({find(group) for group in groups.values()})
    if len(components) < 8:
        raise ValueError("Fewer than eight retained groups; do not manufacture image-level independence")
    random.Random(seed).shuffle(components)
    count = len(components)
    ends = [int(.55 * count), int(.55 * count) + max(1, int(.15 * count))]
    ends += [ends[-1] + max(1, int(.15 * count)), count]
    labels = ["train", "development", "calibration", "test"]
    assignments, start = {}, 0
    for name, end in zip(labels, ends):
        if end <= start:
            raise ValueError("A split has no groups")
        assignments.update({group: name for group in components[start:end]})
        start = end
    split_rows = [{"uid": uid, "capture_group": groups[uid], "split_group": find(groups[uid]),
                   "split": assignments[find(groups[uid])]} for uid in records]
    statistics = {}
    for name in labels:
        selected = [row for row in split_rows if row["split"] == name]
        statistics[name] = {
            "images": len(selected), "groups": len({r["split_group"] for r in selected}),
            "positive_groups_by_category": {
                category: len({r["split_group"] for r in selected
                               if any(t["category"] == category for t in records[r["uid"]]["targets"])})
                for category in data["categories"]},
        }
    result = {"schema": "a20-det2023-grouped-split-v1", "seed": seed,
              "audit_sha256": sha(audit_path), "group_manifest_sha256": sha(groups_path),
              "grouping_basis": "user-supplied capture provenance, coarsened by duplicate candidates",
              "independence_proven": False, "rows": split_rows, "statistics": statistics}
    save(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("audit")
    p.add_argument("--annotations", type=Path, nargs="+", required=True)
    p.add_argument("--images-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("split")
    p.add_argument("--audit", type=Path, required=True)
    p.add_argument("--groups", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--seed", type=int, default=20261020)
    args = parser.parse_args()
    if args.command == "audit":
        result = audit(args.annotations, args.images_root, args.output)
        print(json.dumps({k: result[k] for k in ["labeled_records", "unique_pixel_arrays", "categories"]},
                         ensure_ascii=False))
    else:
        result = make_split(args.audit, args.groups, args.output, args.seed)
        print(json.dumps(result["statistics"], ensure_ascii=False))


if __name__ == "__main__":
    main()
