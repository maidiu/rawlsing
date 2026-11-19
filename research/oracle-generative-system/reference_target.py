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


def work_context(answered, target, seed):
    # Bound the error of every deterministic reader given exactly these keys.
    # This is an empirical support calculation over the fitted finite release.
    context = ["hrs1", "wkdecide", "partteam"]
    mass = answered.groupby(context + ["ballot", "form", "richwork"])[WEIGHT].sum()
    by_answer = mass.unstack(fill_value=0).reindex(columns=[1, 2], fill_value=0)
    minority = by_answer.min(axis=1)
    peers = answered
    for item in context:
        peers = peers.loc[peers[item] == target.read_constraint(item)]
    alternate = peers.loc[peers.richwork != target.read_constraint("richwork")]
    summary = {"inputs": context + ["ballot", "form"], "distinct_inputs": len(by_answer),
               "mixed_cells": int((minority > 0).sum()),
               "minimum_in_sample_weighted_error": float(minority.sum() / by_answer.sum().sum()),
               "same_work_context_before_form_n": len(peers),
               "different_report_in_same_work_context_n": len(alternate)}
    if alternate.empty:
        return summary, None
    cells = alternate.groupby(["ballot", "form", *ITEMS])[WEIGHT].sum()
    cell = Random(seed).choices(list(cells.index), weights=list(cells), k=1)[0]
    ballot, form, *values = map(int, cell)
    return summary, ReferenceTarget(ballot, form, tuple(values))


def analyze(data, profile, seed, contrasts=None):
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
    reference = ReferenceTarget(ballot, form, target)
    if contrasts is not None:
        result["work_context"], alternative = work_context(answered, reference, seed)
        if alternative is not None:
            contrasts.append(alternative)
    return result, reference


def run(path, *, include_work_contrasts=False):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Source edition mismatch")
    cols = ["age", "sex", "degree", "wrkstat", "ballot", "form", WEIGHT, "vstrat", "vpsu"] + list(ITEMS)
    data = pd.read_stata(path, columns=cols, convert_categoricals=False)
    eligible = data.age.between(25, 44) & (data.degree <= 2) & data.wrkstat.isin([1, 2])
    # Two illustrative candidate pools, before a maternal-path/partner join.
    summaries = {"archive_sha256": SHA256, "sampling_seeds": [201011, 201012]}
    draws = {}
    for name, code, seed in (("female_profile", 2, 201011), ("male_profile", 1, 201012)):
        contrasts = [] if include_work_contrasts else None
        summaries[name], draws[name] = analyze(data, eligible & (data.sex == code), seed, contrasts)
        if contrasts:
            draws[name + "_work_contrast"] = contrasts[0]
    return summaries, draws


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    print(json.dumps(run(parser.parse_args().archive)[0], indent=2, allow_nan=False))
