"""Individual correspondence and reachable target mass on the public 2010 GSS.

python3 reference_target.py /path/to/2010_stata.zip
Draws complete empirical response cells internally. Exports aggregate results and
the one reference hour used by the bounded native construction.
The threshold family is an upper bound on one reading, not a person generator.
"""
import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
from random import Random

import pandas as pd

from conditioning import SHA256, WEIGHT, design_se, ratio_influence

SUBJECTS = ("ath", "rac", "com", "mil", "homo", "mslm")
VENUES = ("spk", "col", "lib")
BATTERY = tuple(venue + subject for subject in SUBJECTS for venue in VENUES)
OTHER = ("pray", "attend", "partteam", "wkdecide", "hrs1", "richwork")
ITEMS = BATTERY + OTHER
ORDERS = tuple(permutations(range(3)))


@dataclass(frozen=True)
class ReferenceTarget:
    ballot: int
    form: int
    values: tuple

    def read_constraint(self, item):
        return self.values[ITEMS.index(item)]

    def compare_emissions(self, observed):
        return {
            "matched": [k for k in ITEMS if k in observed and observed[k] == self.read_constraint(k)],
            "mismatched": [k for k in ITEMS if k in observed and observed[k] != self.read_constraint(k)],
            "unimplemented": [k for k in ITEMS if k not in observed],
        }


def permissions(values):
    """Normalize only for the capacity comparison. Targets retain raw codes."""
    rows = []
    for i, subject in enumerate(SUBJECTS):
        speak, college, library = values[3 * i:3 * i + 3]
        if speak not in (1, 2) or college not in (4, 5) or library not in (1, 2):
            raise ValueError("Unqualified substantive code")
        rows.append((speak == 1, college == (5 if subject == "com" else 4), library == 2))
    return rows


def nested(row, order):
    return all(row[i] >= row[j] for i, j in zip(order, order[1:]))


def compatible_orders(rows, separate_firing):
    # An arbitrary personal venue ranking, arbitrary personal subject scores.
    # The firing question can instead have its own threshold: one cell cannot
    # order that threshold against the three others, so only compare its two
    # ordinary venues. A suitable fourth threshold always exists for that cell.
    def compatible(i, order):
        if separate_firing and SUBJECTS[i] == "com":
            order = tuple(j for j in order if VENUES[j] != "col")
        return nested(rows[i], order)
    return [o for o in ORDERS if all(compatible(i, o) for i in range(len(rows)))]


def crossing(rows):
    for a, b in combinations(range(len(rows)), 2):
        for j, k in combinations(range(3), 2):
            if rows[a][j] != rows[a][k] and (rows[a][j], rows[a][k]) == (rows[b][k], rows[b][j]):
                return [BATTERY[i * 3 + v] for i in (a, b) for v in (j, k)]
    return None


def analyze(data, profile, seed):
    eligible = data.loc[profile]
    offered = eligible.loc[eligible.ballot.isin([1, 3])]
    answered = offered.dropna(subset=list(ITEMS))
    failures, wording_failures = [], []
    cells = Counter()
    for row in answered.itertuples(index=False):
        target = tuple(int(getattr(row, key)) for key in ITEMS)
        rows = permissions(target)
        failed = not compatible_orders(rows, False)
        assert failed == bool(crossing(rows))
        relaxed_failed = not compatible_orders(rows, True)
        assert not relaxed_failed or failed
        failures.append(failed)
        wording_failures.append(relaxed_failed)
        cells[(int(row.ballot), int(row.form), target)] += getattr(row, WEIGHT)

    weighted = answered[WEIGHT]
    fail = pd.Series(failures, index=answered.index)
    relaxed = pd.Series(wording_failures, index=answered.index)
    result = {}
    for name, indicator in (("common_venues", fail), ("separate_firing", relaxed)):
        result[name] = {"infeasible_n": int(indicator.sum()),
                        "infeasible_weighted_share": float(weighted @ indicator / weighted.sum()),
                        "design_se": design_se(data, ratio_influence(answered, 1., indicator))}

    ordered_cells = sorted(cells)
    ballot, form, target = Random(seed).choices(ordered_cells, weights=[cells[c] for c in ordered_cells])[0]
    result.update(profile_n=len(eligible), offered_n=len(offered), complete_n=len(answered),
                  distinct_reference_cells=len(cells), sampled_item_count=len(target),
                  sampled_hrs1=target[ITEMS.index("hrs1")])
    return result, ReferenceTarget(ballot, form, target)


def run(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Source edition mismatch")
    cols = ["age", "sex", "degree", "wrkstat", "ballot", "form", WEIGHT, "vstrat", "vpsu"] + list(ITEMS)
    data = pd.read_stata(path, columns=cols, convert_categoricals=False)
    eligible = data.age.between(25, 44) & (data.degree <= 2) & data.wrkstat.isin([1, 2])
    # Two illustrative candidate pools, before a maternal-path/partner join.
    summaries = {"archive_sha256": SHA256, "sampling_seeds": [201011, 201012]}
    draws = {}
    for name, code, seed in (("female_profile", 2, 201011), ("male_profile", 1, 201012)):
        summaries[name], draws[name] = analyze(data, eligible & (data.sex == code), seed)
    return summaries, draws


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    print(json.dumps(run(parser.parse_args().archive)[0], indent=2, allow_nan=False))
