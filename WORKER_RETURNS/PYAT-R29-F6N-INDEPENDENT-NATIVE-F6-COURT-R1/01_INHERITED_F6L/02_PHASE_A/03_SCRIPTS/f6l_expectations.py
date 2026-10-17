"""F6L independent exact-rational expectation engine.

Written from the published target-joint standardization definition using only
fractions.Fraction.  It does NOT import the native producer and never calls it.
The native producer is executed only afterwards, by the probe/test harness, and
compared against these exact values.

Role: independent F6J scientific reviewer continuation (F6L), not F6K author.
"""
from __future__ import annotations

from fractions import Fraction as F


def q(value):
    return F(value)


def s(value):
    return str(F(value))


def standardize(target_strata, tables, weights, min_raw_support):
    """Independent reimplementation of target-joint standardization.

    target_strata: {z: share}
    tables: {sid: {z: {"masses": {cell: Fraction}, "raw_n": int}}}
    weights: {sid: weight}
    """
    keys = sorted({k for per_source in tables.values()
                   for table in per_source.values() for k in table["masses"]})
    joint = {k: F(0) for k in keys}
    lower = {k: F(0) for k in keys}
    upper = {k: F(0) for k in keys}
    uncovered = F(0)
    coverage = {}
    for z in sorted(target_strata):
        share = F(target_strata[z])
        if not share:
            continue
        eligible = []
        for sid in sorted(tables):
            table = tables[sid].get(z)
            if (table is not None
                    and table["raw_n"] >= min_raw_support
                    and sum(table["masses"].values(), F(0)) > 0):
                eligible.append(sid)
        denom = sum((F(weights[sid]) for sid in eligible), F(0))
        coverage[z] = {"target_share": s(share), "eligible": eligible,
                       "excluded": [sid for sid in sorted(tables) if sid not in eligible]}
        if not denom:
            uncovered += share
            for k in keys:
                upper[k] += share
            continue
        per_source = []
        for sid in eligible:
            alpha = F(weights[sid]) / denom
            masses = tables[sid][z]["masses"]
            mass = sum(masses.values(), F(0))
            p = {k: masses.get(k, F(0)) / mass for k in keys}
            per_source.append(p)
            for k in keys:
                joint[k] += share * alpha * p[k]
        for k in keys:
            lower[k] += share * min(p[k] for p in per_source)
            upper[k] += share * max(p[k] for p in per_source)
    return {"keys": keys, "joint": joint, "lower": lower, "upper": upper,
            "uncovered": uncovered, "coverage": coverage}


def sensitivity(lower, upper, radii):
    radius = sum((F(r) for r in radii), F(0))
    return {"radius": radius,
            "lower": {k: max(F(0), lower[k] - radius) for k in lower},
            "upper": {k: min(F(1), upper[k] + radius) for k in upper}}


def conditional(joint, axes, conditions, outcome):
    oi = axes.index(outcome)
    selected = [k for k in joint
                if all(k[axes.index(a)] == v for a, v in conditions.items())]
    denom = sum((joint[k] for k in selected), F(0))
    table = {}
    for k in selected:
        v = k[oi]
        table[v] = table.get(v, F(0)) + joint[k]
    probs = {v: table[v] / denom for v in sorted(table)} if denom else {}
    return {"denominator": denom, "probabilities": probs, "selected": selected}


def frechet(p, q):
    p, q = F(p), F(q)
    return {"lower": max(F(0), p + q - 1), "upper": min(p, q),
            "independence_scenario": p * q}


def cells_to_map(cells):
    return {tuple(c["categories"]): F(c["probability"]) for c in cells}


def map_to_cells(mapping):
    return {str(k): s(v) for k, v in sorted(mapping.items())}
