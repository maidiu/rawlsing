"""Descriptive GSS 2010 inverse problem. Input is the public NORC single-year zip.

python3 conditioning.py /path/to/2010_stata.zip   (numpy, pandas)
No respondent identities, fitted people, or individual survey rows are exported.
"""
import argparse
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

SHA256 = "df10cad3986178c044b41d782c5984d039c649d9065fde96b063fdebf20f9355"
ITEMS = ["pray", "attend", "spkath", "libath"]
PAST = ["relig16", "mawrkgrw"]
WEIGHT = "ballotformwtnr"
EXPRESSION = ITEMS + ["relig", "reliten", "partyid", "polviews", "spkrac", "librac", "class"]
WORK = ["wrkstat", "wrkslf", "chngtme"]
CODES = np.array(list(product(range(2), repeat=4)))
# Analytical contrast, chosen for its content. Iterate every cell in the fit.
TIP = 15


def ratio_influence(rows, mask, outcome):
    weighted = rows[WEIGHT] * mask
    return weighted * (outcome - weighted @ outcome / weighted.sum()) / weighted.sum()


def design_se(frame, influence):
    # Keep zero-influence PSUs outside the analysis domain.
    full = influence.reindex(frame.index, fill_value=0.)
    psus = full.groupby([frame.vstrat, frame.vpsu]).sum().unstack()
    assert psus.shape[1] == 2 and psus.notna().all().all()
    return float(np.linalg.norm(psus.iloc[:, 0] - psus.iloc[:, 1]))


def summarize(frame, sex):
    profile = ((frame.sex == sex) & frame.age.between(30, 64)
               & (frame.childs >= 1) & (frame.degree <= 2))
    offered = profile & frame.ballot.isin([1, 3])
    complete = offered & frame[ITEMS + PAST].notna().all(axis=1)
    d = frame.loc[complete].copy()
    bits = np.column_stack((d.pray <= 2, d.attend >= 7, d.spkath == 1, d.libath == 1))
    y = bits @ np.array([8, 4, 2, 1])
    x_labels = sorted(set(zip(d.relig16.astype(int), d.mawrkgrw.astype(int))))
    x = np.array([x_labels.index(pair) for pair in zip(d.relig16, d.mawrkgrw)])
    w = d[WEIGHT].to_numpy()
    assert np.all(np.isfinite(w) & (w > 0))

    def counts(mask):
        table = np.zeros((len(x_labels), len(CODES)))
        np.add.at(table, (x[mask], y[mask]), w[mask])
        return table

    table = counts(np.ones(len(d), dtype=bool))
    joint = table / table.sum()
    py = joint.sum(axis=0)
    px = joint.sum(axis=1)
    # This data set has full *coarsened adult* support in the two selected domains.
    assert np.all(py > 0)
    reverse = joint / py
    emit = joint / px[:, None]
    forward_again = reverse.T @ emit
    assert np.allclose(py @ forward_again, py)
    prob_bits = py @ CODES
    independent = np.prod(np.where(CODES, prob_bits, 1 - prob_bits), axis=1)
    # Preserve P(reported past | adult tip), change only the adult joint to marginals.
    independent_past = reverse @ independent
    work = np.array([job == 1 for _, job in x_labels])
    # A prospective propensity conditioned only on x must be bounded by the
    # smallest/largest row. Even a perfect ex ante selector cannot exceed this hull.
    supported = table.sum(axis=1) > 0
    # Out-of-sample comparison. Hold out complete variance strata, both PSUs.
    # Shrink each training conditional law by 8 mean-weight pseudo-observations
    # toward the training-domain law, with one uniformly spread count for positivity.
    score = np.zeros(3)
    for fold in range(5):
        holdout = d.vstrat.to_numpy().astype(int) % 5 == fold
        train = ~holdout
        t = counts(train) / w[train].mean()
        baseline = (t.sum(axis=0) + 1 / 16) / (t.sum() + 1)
        fitted = (t + 8 * baseline) / (t.sum(axis=1)[:, None] + 8)
        marg = baseline @ CODES
        independent_fit = np.prod(np.where(CODES, marg, 1 - marg), axis=1)
        for i, p in enumerate((independent_fit[y[holdout]], baseline[y[holdout]],
                               fitted[x[holdout], y[holdout]])):
            score[i] -= w[holdout] @ np.log(p)

    tip_n = int(np.sum(y == TIP))
    raw_count = np.bincount(y, minlength=16)
    # Display finite conditional possibilities for this one tip. No private biography.
    tip_prior = reverse[:, TIP]
    tv = lambda a, b: float(abs(a - b).sum() / 2)
    worked_at_tip = float(work @ tip_prior)
    return {
        "n_profile": int(profile.sum()), "n_on_ballots_A_C": int(offered.sum()),
        "n_answered_four": int((offered & frame[ITEMS].notna().all(axis=1)).sum()),
        "n_complete_six": len(d), "tip_n": tip_n,
        "distinct_original_four_item_patterns": d[ITEMS].drop_duplicates().shape[0],
        "cells_binary_order_0000_to_1111": raw_count.tolist(), "weighted_joint": py.tolist(),
        "marginal_product_tv": tv(py, independent),
        "tip_rate": py[TIP], "tip_design_se": design_se(frame, ratio_influence(d, 1., y == TIP)),
        "tip_marginal_product": independent[TIP],
        "reported_past_tv_under_marginal_product": tv(px, independent_past),
        "reported_past_tv_at_tip_vs_profile": tv(tip_prior, px),
        "work_report_profile": float(work @ px), "work_report_tip": worked_at_tip,
        "work_report_tip_design_se": design_se(frame, ratio_influence(d, y == TIP, work[x])),
        "roundtrip_same_tip_given_tip": forward_again[TIP, TIP],
        "roundtrip_mean_tv_from_profile": float(py @ (abs(forward_again - py).sum(axis=1) / 2)),
        "roundtrip_ensemble_tv": tv(py @ forward_again, py),
        "max_tip_rate_over_observed_past_cells_in_sample": float(emit[supported, TIP].max()),
        "stratum_holdout_log_losses_independent_joint_joint_given_past": (score / w.sum()).tolist(),
        "conditional_past_for_tip": [
            {"relig16": religion, "mawrkgrw": job, "probability": p}
            for (religion, job), p in zip(x_labels, tip_prior) if p > 0],
    }


def compare_input_readers(rows, outcome):
    """Hold out all respondents from a variance stratum together.

    Each proposed predictor is shrunk toward its shorter prefix. If a field is
    missing, stop at its last usable prefix; no match draws exactly the parent.
    These empirical conditional means predict one report, not a private state.
    """
    chains = {
        "profile": [],
        "expression": [ITEMS, EXPRESSION],
        "work": [WORK],
        "work_and_expression": [WORK, WORK + ITEMS, WORK + EXPRESSION],
    }
    results = {}
    folds = rows.vstrat.astype(int) % 5
    for name, chain in chains.items():
        loss = 0.
        finest_support = 0
        for fold in range(5):
            fit, test = rows.loc[folds != fold], rows.loc[folds == fold]
            weights = fit[WEIGHT] / fit[WEIGHT].mean()
            mass = pd.DataFrame({"n": weights, "positive": weights * outcome.loc[fit.index]})
            base = (mass.positive.sum() + .5) / (mass.n.sum() + 1)
            tables = [fit[block].join(mass).groupby(block)[["n", "positive"]].sum().T.to_dict()
                      for block in chain]
            for index, row in test.iterrows():
                probability = base
                for depth, (block, table) in enumerate(zip(chain, tables)):
                    key = tuple(row[k] for k in block)
                    if any(pd.isna(k) for k in key) or key not in table:
                        break
                    found = table[key]
                    probability = (found["positive"] + 8 * probability) / (found["n"] + 8)
                    if depth + 1 == len(chain):
                        finest_support += 1
                assigned = probability if outcome.at[index] else 1-probability
                loss -= row[WEIGHT] * np.log(assigned)
        results[name] = {"heldout_log_loss": loss / rows[WEIGHT].sum(),
                         "observations_with_finest_training_match": finest_support if chain else len(rows)}
    return results


def working_domain(frame, sex):
    """Additional joint at the employed-parent domain with its own risk set."""
    domain = (frame.age.between(30, 64) & (frame.sex == sex) & (frame.childs >= 1)
              & (frame.degree <= 2) & frame.wrkstat.isin([1, 2]))
    offered = domain & frame.ballot.isin([1, 3])
    d = frame.loc[offered].dropna(subset=ITEMS + ["partteam", "wkdecide"])
    bits = np.column_stack((d.pray <= 2, d.attend >= 7, d.spkath == 1, d.libath == 1))
    cell = bits @ np.array([8, 4, 2, 1])
    team_often = (d.partteam == 1) & (d.wkdecide == 1)
    settings = {}
    for key, mask in [("profile_only", np.ones(len(d), dtype=bool)),
                      ("1111", cell == TIP), ("1010", cell == 10)]:
        w = d.loc[mask, WEIGHT]
        rated = mask & team_often & d.wkfreedm.notna()
        low = d.loc[rated, "wkfreedm"].isin([3, 4])
        rated_weight = d.loc[rated, WEIGHT]
        settings[key] = {"n": int(mask.sum()),
                         "team_often_with_freedom_answer_n": int(rated.sum()),
                         "low_freedom_n": int(low.sum()),
                         "low_freedom_share_within_team_often": (
                             float(rated_weight @ low / rated_weight.sum()) if rated.any() else None),
                         "team_often": float(w @ team_often[mask] / w.sum())}
    # The full profile includes the tip. Their estimates are correlated.
    tip = cell == TIP
    difference_se = design_se(frame, ratio_influence(d, tip, team_often)
                              - ratio_influence(d, 1., team_often))
    all_tips = {}
    for n, p in enumerate(CODES):
        in_cell = cell == n
        if not in_cell.any():
            continue
        weights = d.loc[in_cell, WEIGHT]
        all_tips["".join(map(str, p))] = {
            "mass": float(weights.sum() / d[WEIGHT].sum()),
            "team_often": float(weights @ team_often[in_cell] / weights.sum()),
            "n": int(in_cell.sum())}
    return {"formative_report_predictions": compare_input_readers(d, team_often),
            "weighted_observed_support": all_tips, "tip_profile_difference_se": difference_se,
            "profile_n": int(domain.sum()), "ballots_a_c_n": int(offered.sum()),
            "conditionals": settings}


def run(path):
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256:
        raise ValueError("Expected the specified NORC release. Re-adjudicate changed editions.")
    cols = ["age", "sex", "childs", "degree", "vstrat", "vpsu", "ballot", "form", WEIGHT]
    columns = cols + PAST + EXPRESSION + WORK + ["partteam", "wkdecide", "wkfreedm"]
    d = pd.read_stata(path, columns=columns, convert_categoricals=False)
    tagged = pd.read_stata(path, columns=columns, convert_missing=True, convert_categoricals=False)
    missing = {k: tagged[k][d[k].isna()].map(str).value_counts().to_dict()
               for k in PAST + ITEMS}
    assert (tagged.loc[d.ballot == 2, ["libath", "spkath"]].map(str) == ".i").all().all()
    return {"sha256": SHA256, "release_n": len(d), "source_missing_codes": missing,
            "female": summarize(d, 2), "male": summarize(d, 1),
            "employed_female": working_domain(d, 2), "employed_male": working_domain(d, 1)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    print(json.dumps(run(parser.parse_args().archive), indent=2, allow_nan=False))
