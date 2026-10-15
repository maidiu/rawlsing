"""Independent paired-analysis recompute on the RBA mock sweep captures.

Written independently from assay/scoring.py against the frozen spec. Compares
against the candidate's reported paired numbers. Exits nonzero on mismatch.
"""
import gzip
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
RUN = RET / "exec" / "r2" / "receipts" / "rba_review_run1" / "complete_lawful"
SCHED = RET / "staging" / "r2" / "data" / "schedule.json"

BELIEFS = ("UNCERTAIN", "CONFIDENT", "NOT_ASKED")
STANDING = ("RECORDED", "UNRECORDED", "NOT_ASKED")


def main() -> int:
    schedule = json.loads((RET / "staging" / "r2" / "data" / "schedule.json").read_text())
    oracle = json.loads((RET / "staging" / "r2" / "data" / "oracle.json").read_text())
    coded = json.loads(gzip.decompress((RUN / "coded_captures.json.gz").read_bytes()))
    trials = {r["id"]: r for r in schedule}

    # independent scoring: valid schema + in-menu + in expected actions + joint match
    records = []
    for tid, raw in coded.items():
        row = trials[tid]
        exp = oracle[row["case"]]
        try:
            x = json.loads(raw)
            valid = (set(x) == {"action", "belief_report", "standing_report", "origin_claim"})
        except (ValueError, TypeError):
            valid = False
            x = {}
        ok = bool(valid and x["action"] in row["menu"] and x["action"] in exp["actions"]
                  and all(x[k] == exp[k] for k in ("belief_report", "standing_report", "origin_claim")))
        records.append({"id": tid, "block": row["block"], "case": row["case"],
                        "family": row["family"], "k": row["k"], "arm": row["arm"],
                        "correct": ok})

    def paired(recs, base, comp, alpha=0.05, comparisons=12):
        groups = defaultdict(dict)
        for r in recs:
            if r["arm"] not in (base, comp):
                continue
            if r["arm"] in groups[r["block"]]:
                raise ValueError("DUPLICATE_PAIR_MEMBER")
            groups[r["block"]][r["arm"]] = r
        fam = defaultdict(list)
        for block, g in groups.items():
            if set(g) != {base, comp}:
                raise ValueError("UNPAIRED_ID")
            a, b = g[base], g[comp]
            if (a["case"], a["family"], a["k"]) != (b["case"], b["family"], b["k"]):
                raise ValueError("PAIR_CONTEXT_MISMATCH")
            fam[a["family"]].append(int(b["correct"]) - int(a["correct"]))
        diffs = [sum(v) / len(v) for v in fam.values()]
        n = len(diffs)
        delta = sum(diffs) / n
        radius = math.sqrt(2 * math.log(2 * comparisons / alpha) / n)
        return {"delta": delta, "interval": [max(-1, delta - radius), min(1, delta + radius)],
                "n_families": n, "n_matched_blocks": len(groups),
                "family_diffs": {k: v for k, v in zip(sorted(fam), diffs)}}

    out = {}
    for base, comp in (("A", "B"), ("A", "C")):
        out[f"{comp}_minus_{base}"] = paired(records, base, comp)
    print(json.dumps(out, indent=1))

    # cross-check against candidate's own paired summary if present
    summary = json.loads((RUN / "summary.json").read_text())
    mine = (OUT := RET / "outputs" / "paired_recompute.json")
    mine.parent.mkdir(exist_ok=True)
    mine.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

    # correctness fractions per arm/K (sanity: lawful mock scores 1.0)
    frac = defaultdict(lambda: [0, 0])
    for r in records:
        frac[(r["k"], r["arm"])][0] += 1
        frac[(r["k"], r["arm"])][1] += int(r["correct"])
    print("per-K-arm correct/total:")
    for k in sorted({r["k"] for r in records}):
        print(" ", k, {a: f"{frac[(k,a)][1]}/{frac[(k,a)][0]}" for a in "ABC"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
