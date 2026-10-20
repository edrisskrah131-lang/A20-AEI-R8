"""Software checks using generated fixtures; no DET2023 results are produced."""
import csv
import json
from pathlib import Path
import random
import tempfile
import unittest

from PIL import Image

import intake
import risk


class IntakeChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.images = self.root / "images"
        self.images.mkdir()
        rng = random.Random(20261020)
        self.data = {"images": [], "annotations": [],
                     "categories": [{"id": 1, "name": "fixture_defect"}]}
        for i in range(20):
            image = Image.new("RGB", (36, 32))
            image.putdata([tuple(rng.randrange(256) for _ in range(3)) for _ in range(36 * 32)])
            image.save(self.images / f"{i}.png")
            self.data["images"].append({"id": i, "file_name": f"{i}.png", "width": 36, "height": 32})
            self.data["annotations"].append(
                {"id": i, "image_id": i, "category_id": 1, "bbox": [2, 3, 4, 5]})
        self.annotation = self.root / "annotations.json"
        self.write_annotation()

    def tearDown(self):
        self.temp.cleanup()

    def write_annotation(self):
        self.annotation.write_text(json.dumps(self.data))

    def audited(self):
        return intake.audit([self.annotation], self.images, self.root / "audit")

    def grouping(self, data):
        path = self.root / "groups.csv"
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["uid", "group_id", "group_basis"])
            writer.writeheader()
            for i, row in enumerate(data["records"]):
                writer.writerow({"uid": row["uid"], "group_id": f"capture-{i}",
                                 "group_basis": "test-fixture identity"})
        return path

    def test_duplicate_formats_and_input_rejected(self):
        data = self.audited()
        self.assertEqual(data["labeled_records"], 20)
        with self.assertRaises(ValueError):
            intake.audit([self.annotation, self.annotation], self.images, self.root / "other")

    def test_path_escape_rejected(self):
        self.data["images"][0]["file_name"] = "../outside.png"
        self.write_annotation()
        with self.assertRaisesRegex(ValueError, "escapes"):
            self.audited()

    def test_invalid_target_rejected(self):
        self.data["annotations"][0]["bbox"] = [35, 1, 2, 2]
        self.write_annotation()
        with self.assertRaisesRegex(ValueError, "bounding box"):
            self.audited()

    def test_crowd_needs_policy(self):
        self.data["annotations"][0]["iscrowd"] = 1
        self.write_annotation()
        with self.assertRaisesRegex(ValueError, "Crowd"):
            self.audited()

    def test_duplicates_stay_together_and_splits_repeat(self):
        (self.images / "1.png").write_bytes((self.images / "0.png").read_bytes())
        data = self.audited()
        self.assertEqual(data["unique_pixel_arrays"], 19)
        groups = self.grouping(data)
        result = intake.make_split(self.root / "audit/audit.json", groups, self.root / "split.json")
        repeat = intake.make_split(self.root / "audit/audit.json", groups, self.root / "repeat.json")
        self.assertEqual(result, repeat)
        rows = {r["uid"]: r for r in result["rows"]}
        a, b = [r["uid"] for r in data["records"][:2]]
        self.assertEqual(rows[a]["split_group"], rows[b]["split_group"])
        memberships = {}
        for row in rows.values():
            memberships.setdefault(row["split_group"], set()).add(row["split"])
        self.assertTrue(all(len(value) == 1 for value in memberships.values()))
        self.assertFalse(result["independence_proven"])

    def test_empty_grouping_rejected(self):
        self.audited()
        with self.assertRaisesRegex(ValueError, "reviewed capture"):
            intake.make_split(self.root / "audit/audit.json",
                              self.root / "audit/groups_template.csv", self.root / "split.json")

    def test_changed_data_after_audit_rejected(self):
        data = self.audited()
        (self.images / "0.png").write_bytes((self.images / "1.png").read_bytes())
        with self.assertRaisesRegex(ValueError, "changed after audit"):
            intake.make_split(self.root / "audit/audit.json", self.grouping(data), self.root / "split.json")


class RiskChecks(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"uid": "a", "producer": "v1", "category": "fixture", "split": "calibration",
             "split_group": "g1", "true_positives": 2, "ground_truth": 2},
            {"uid": "b", "producer": "v1", "category": "fixture", "split": "calibration",
             "split_group": "g1", "true_positives": 0, "ground_truth": 1},
            {"uid": "c", "producer": "v1", "category": "fixture", "split": "calibration",
             "split_group": "g2", "true_positives": 0, "ground_truth": 0},
        ]
        self.units = [{"uid": r["uid"], "split": "calibration", "split_group": r["split_group"],
                       "ground_truth_by_category": {"fixture": r["ground_truth"]}} for r in self.rows]
        self.events = [{"id": "v1-fixture-complete", "producer": "v1", "category": "fixture",
                        "recall_floor": 1.0}]

    def test_independent_unit_is_group_not_box(self):
        events = risk.group_events(self.rows, .75)
        self.assertEqual(len(events), 1)
        self.assertAlmostEqual(events[0]["recall"], 2 / 3)
        self.assertTrue(events[0]["failure"])

    def test_cp_endpoints_and_zero_failure_formula(self):
        self.assertEqual(risk.upper_bound(0, 0, .05), 1)
        self.assertEqual(risk.upper_bound(4, 4, .05), 1)
        self.assertAlmostEqual(risk.upper_bound(0, 50, .05 / 4), 1 - (.05 / 4) ** (1 / 50), places=14)
        n = risk.required_zero_failure_groups(4, .10)
        self.assertLessEqual(risk.upper_bound(0, n, .05 / 4), .10)
        self.assertGreater(risk.upper_bound(0, n - 1, .05 / 4), .10)

    def test_no_dropping_failed_images(self):
        with self.assertRaisesRegex(ValueError, "Every calibration image"):
            risk.fixed_family_cards(self.events, self.rows[:1], self.units)

    def test_test_results_cannot_calibrate(self):
        self.rows[0]["split"] = "test"
        with self.assertRaisesRegex(ValueError, "calibration results only"):
            risk.fixed_family_cards(self.events, self.rows, self.units)

    def test_gt_manifest_controls_counts(self):
        self.rows[1]["ground_truth"] = 0
        with self.assertRaisesRegex(ValueError, "fixed calibration manifest"):
            risk.fixed_family_cards(self.events, self.rows, self.units)

    def test_rare_class_does_not_become_success(self):
        event = [{"id": "absent", "producer": "v1", "category": "absent", "recall_floor": 1.0}]
        rows = [{**r, "category": "absent", "true_positives": 0, "ground_truth": 0} for r in self.rows]
        card = risk.fixed_family_cards(event, rows, self.units)[0]
        self.assertEqual(card["groups"], 0)
        self.assertEqual(card["upper"], 1)


if __name__ == "__main__":
    unittest.main()
