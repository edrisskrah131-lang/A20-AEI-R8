"""One-sided CP bounds on group events, with an explicitly fixed event family."""
import math

from scipy.stats import beta


def upper_bound(failures, groups, alpha):
    if not isinstance(groups, int) or not isinstance(failures, int):
        raise ValueError("Counts must be integers")
    if not 0 <= failures <= groups or not 0 < alpha < 1:
        raise ValueError("Invalid binomial inputs")
    return 1.0 if groups == 0 or failures == groups else float(beta.isf(alpha, failures + 1, groups - failures))


def required_zero_failure_groups(family_size, allowance, confidence_error=.05):
    if family_size < 1 or not isinstance(family_size, int):
        raise ValueError("Family size must be a positive integer")
    if not 0 < allowance < 1 or not 0 < confidence_error < 1:
        raise ValueError("Invalid risk/confidence allowance")
    return math.ceil(math.log(confidence_error / family_size) / math.log1p(-allowance))


def group_events(rows, recall_floor):
    """Aggregate image counts before thresholding; absent classes are not successes.

    Rows belong to one fixed producer, one category, and one split. A complete
    capture group is the sampling unit; annotated instances are not independent
    calibration trials. The result concerns a positive-class group population.
    """
    if not 0 < recall_floor <= 1:
        raise ValueError("Recall floor must lie in (0, 1]")
    grouped, seen = {}, set()
    contexts = {(r["producer"], r["category"], r["split"]) for r in rows}
    if len(contexts) != 1:
        raise ValueError("Use one producer/category/split per event")
    for row in rows:
        if row["uid"] in seen:
            raise ValueError("Duplicate image result")
        seen.add(row["uid"])
        tp, gt = row["true_positives"], row["ground_truth"]
        if not isinstance(tp, int) or not isinstance(gt, int) or not 0 <= tp <= gt:
            raise ValueError("Invalid detection counts")
        group = grouped.setdefault(row["split_group"], [0, 0])
        group[0] += tp
        group[1] += gt
    return [{"group": name, "true_positives": tp, "ground_truth": gt,
             "recall": tp / gt, "failure": tp / gt < recall_floor}
            for name, (tp, gt) in sorted(grouped.items()) if gt > 0]


def fixed_family_cards(event_specs, scored_rows, calibration_units, confidence_error=.05):
    """Every fixed event consumes its allocation, including zero-support events.

    event_specs must be fixed before reading calibration outcomes. This helper
    receives that family; it cannot establish its precommitment or independence.
    """
    if not event_specs or len({e["id"] for e in event_specs}) != len(event_specs):
        raise ValueError("Supply a nonempty fixed family with distinct IDs")
    signatures = {(e["producer"], e["category"], e["recall_floor"]) for e in event_specs}
    if len(signatures) != len(event_specs):
        raise ValueError("Duplicate events must not inflate the fixed family")
    if any(not 0 < e["recall_floor"] <= 1 for e in event_specs):
        raise ValueError("Invalid group recall threshold")
    if any(r["split"] != "calibration" for r in scored_rows):
        raise ValueError("Evidence cards may use calibration results only")
    units = {u["uid"]: u for u in calibration_units}
    if len(units) != len(calibration_units):
        raise ValueError("Duplicate calibration units")
    if any(u["split"] != "calibration" for u in units.values()):
        raise ValueError("Calibration manifest contains another split")
    contexts = {(e["producer"], e["category"]) for e in event_specs}
    if any((r["producer"], r["category"]) not in contexts for r in scored_rows):
        raise ValueError("Result belongs to an undeclared producer/category")
    for producer, category in contexts:
        rows = [r for r in scored_rows if r["producer"] == producer and r["category"] == category]
        if len(rows) != len(units) or {r["uid"] for r in rows} != set(units):
            raise ValueError("Every calibration image needs an explicit result, including failed inference")
        for row in rows:
            unit = units[row["uid"]]
            if (row["split_group"] != unit["split_group"]
                    or row["ground_truth"] != unit["ground_truth_by_category"].get(category, 0)):
                raise ValueError("Scoring rows disagree with the fixed calibration manifest")
    alpha = confidence_error / len(event_specs)
    cards = []
    for event in event_specs:
        rows = [r for r in scored_rows if r["producer"] == event["producer"]
                and r["category"] == event["category"]]
        outcomes = group_events(rows, event["recall_floor"]) if rows else []
        k, n = sum(r["failure"] for r in outcomes), len(outcomes)
        cards.append({**event, "failures": k, "groups": n, "alpha": alpha,
                      "upper": upper_bound(k, n, alpha),
                      "risk_unit": "positive-category capture group"})
    return cards
