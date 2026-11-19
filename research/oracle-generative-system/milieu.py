"""Conditional context for an observed four-answer pattern, using the NORC 2010 zip.

Run with the original public Stata zip. Returns aggregate joint counts only.
The March-2026 SAV in the supplied extraction is a different release.
"""
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from conditioning import SHA256, WEIGHT, design_se, ratio_influence

ITEMS = ["spkath", "libath", "spkcom", "libcom"]
QUARTET = (1260, 1951, 1055, 1401)


def summarize(data, domain):
    offered = data.loc[domain & data.ballot.isin([1, 3])]
    valid = offered.dropna(subset=[*ITEMS, WEIGHT])
    pattern = valid[ITEMS].eq(1).all(axis=1)
    weights = valid[WEIGHT]
    outside = ~valid.id.isin(QUARTET)
    return {
        "in_domain": int(domain.sum()), "on_ballots": len(offered),
        "joint_complete": len(valid), "pattern_n": int(pattern.sum()),
        "weighted_share": float(weights @ pattern / weights.sum()),
        "linearized_design_se": design_se(data, ratio_influence(valid, 1., pattern)),
        "weight_only_effective_n": float(weights.sum() ** 2 / (weights @ weights)),
        "outside_quartet_complete": int(outside.sum()),
        "outside_quartet_pattern_n": int((outside & pattern).sum()),
    }


def run(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Different NORC archive")
    columns = ["age", "educ", "region", "marital", "sex", "wrkstat", "id",
               "vstrat", "vpsu", "ballot", WEIGHT, *ITEMS]
    d = pd.read_stata(path, columns=columns, convert_categoricals=False)
    # Women retiring, income, and parenting are not treated as causes of opinion.
    near = d.age.between(55, 75) & (d.region == 3) & (d.educ == 12) & (d.marital == 1)
    women = near & (d.sex == 2)
    return {label: summarize(d, domain) for label, domain in (
        ("US", pd.Series(True, index=d.index)), ("married_south_age55_75_educ12", near),
        ("also_female", women), ("also_retired", women & (d.wrkstat == 5)))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    print(json.dumps(run(parser.parse_args().archive), indent=2))
