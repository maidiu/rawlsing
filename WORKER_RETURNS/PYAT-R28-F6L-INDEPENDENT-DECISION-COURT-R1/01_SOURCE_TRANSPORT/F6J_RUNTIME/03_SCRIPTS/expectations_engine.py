"""F6J independent expectation engine.

Written from the published standardization definition, using fractions.Fraction
only. It does NOT import the native producer and does NOT call it. The native
producer is executed only afterwards and only compared against these values.

ROLE: new distinct independent F6 scientific reviewer (F6J), not the F6C author
(9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f), not the incomplete F6I reviewer
(6d99650bed01eed8365ec38bd888741a88888a45).
"""
from __future__ import annotations

from fractions import Fraction as F


def expected_standardization(target_strata, tables, weights, min_raw_support):
    """Independent reimplementation of target joint standardization.

    tables: {sid: {z: {"masses": {cellkey: Fraction}, "raw_n": int}}}
    Returns exact-rational joint / lower / upper / uncovered.
    """
    keys = sorted({k for s in tables.values() for z in s.values()
                   for k in z["masses"]})
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
            t = tables[sid].get(z)
            if (t is not None and t["raw_n"] >= min_raw_support
                    and sum(t["masses"].values(), F(0)) > 0):
                eligible.append(sid)
        denom = sum((F(weights[s]) for s in eligible), F(0))
        coverage[z] = {"target_share": str(share), "eligible": list(eligible),
                       "excluded": [s for s in sorted(tables) if s not in eligible]}
        if not denom:
            uncovered += share
            for k in keys:
                upper[k] += share
            continue
        ps = []
        for sid in eligible:
            alpha = F(weights[sid]) / denom
            masses = tables[sid][z]["masses"]
            mass = sum(masses.values(), F(0))
            p = {k: (masses.get(k, F(0)) / mass if mass else F(0)) for k in keys}
            ps.append(p)
            for k in keys:
                joint[k] += share * alpha * p[k]
        for k in keys:
            lower[k] += share * min(p[k] for p in ps)
            upper[k] += share * max(p[k] for p in ps)
    return {"joint": joint, "lower": lower, "upper": upper,
            "uncovered": uncovered, "coverage": coverage, "keys": keys}


def expected_sensitivity(lower, upper, radius):
    radius = F(radius)
    return {"lower": {k: max(F(0), lower[k] - radius) for k in lower},
            "upper": {k: min(F(1), upper[k] + radius) for k in upper},
            "radius": radius}


def expected_conditional(joint, keys, axes, conditions, outcome):
    """Independent reimplementation of the cumulative-predicate conditional."""
    oi = axes.index(outcome)
    sel = [k for k in keys
           if all(k[axes.index(a)] == v for a, v in conditions.items())]
    denom = sum((joint[k] for k in sel), F(0))
    table = {}
    for k in sel:
        v = k[oi]
        table[v] = table.get(v, F(0)) + joint[k]
    probs = {v: (p / denom) for v, p in sorted(table.items())} if denom else {}
    return {"denominator": denom, "probabilities": probs, "selected": list(sel)}


def expected_frechet(p, q):
    p, q = F(p), F(q)
    return {"lower": max(F(0), p + q - 1), "upper": min(p, q),
            "independence_scenario": p * q}


def l1(a, b):
    return sum((abs(a[k] - b[k]) for k in a), F(0))


def s(q):
    """Canonical exact-rational string."""
    return str(F(q))
