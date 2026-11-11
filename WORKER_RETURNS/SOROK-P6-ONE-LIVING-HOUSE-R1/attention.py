"""Exposure-conditioned selection. No world or actor input is produced here."""

from collections import Counter


def select(objects, history):
    # Favor repeated directed conduct. A choice following a presented detail
    # remains evidence, with less weight than independently choosing an affordance.
    weights = Counter()
    for row in history[-12:]:
        weights[row["target"]] += 1 if row["shown"] else 2
    return max(objects, key=lambda ref: weights[ref], default=None)


def register(profile, frame, target, turn):
    if any(row["turn"] == turn for row in profile["history"]):
        return
    prior = profile["exposure"]
    profile["history"].append({
        "target": target, "turn": turn,
        "shown": prior.get("detail") == target and prior.get("room") == frame["room"],
        "available": sorted(frame["objects"]),
    })
