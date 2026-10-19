#!/usr/bin/env python3
"""S44 CLI: historical positive -> deployable handoff -> A42 v4 source-grade fan-in."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
REPO = RETURN_ROOT.parents[1]
for p in (RETURN_ROOT, REPO):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from frozen_a42.a42 import core as a42core  # noqa: E402
from frozen_a42.frozen_a41.a41.gitpreimage import GitPreimage  # noqa: E402
from s44 import historical, handoff, a42_fanin  # noqa: E402


def _dump(name, obj):
    p = RETURN_ROOT / name
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return hashlib.sha256(p.read_bytes()).hexdigest()


def assemble():
    gp = GitPreimage(REPO)
    hist = historical.verify_historical(gp)
    ho = handoff.handoff(gp, hist)
    scope, hist2, new, base, after, delta = a42_fanin.run(gp)
    old_manifest = json.loads(gp.blob_at(
        a42core.A41_COMMIT, a42core.A41_DIR + "/estate_acceptance_manifest.json"))
    f1f8, manifest, md, intake, wake, j42 = a42core.artifacts(
        after, scope, old_manifest,
        [{"receipt_id": r["receipt_id"], "grade": r["grade"],
          "origin_commit": r["origin_commit"], "claim_id": r["claim_id"],
          "source_return": r["receipt_id"].split("-")[0]} for r in new])

    d = {}
    d["s44_historical_source_positives.json"] = _dump(
        "s44_historical_source_positives.json", hist)
    d["s44_source_runtime_handoff.json"] = _dump("s44_source_runtime_handoff.json", ho)
    d["s44_all35_deferred_ledger.json"] = _dump(
        "s44_all35_deferred_ledger.json", ho["deferred_ledger"])
    d["s44_single_owner_decision.json"] = _dump(
        "s44_single_owner_decision.json", ho["single_decision"])
    d["s44_a42_v4_estate_acceptance_manifest.json"] = _dump(
        "s44_a42_v4_estate_acceptance_manifest.json", manifest)
    d["s44_a42_v4_f1_f8_acceptance_matrix.json"] = _dump(
        "s44_a42_v4_f1_f8_acceptance_matrix.json", f1f8)
    (RETURN_ROOT / "s44_a42_v4_final_maturity_adjudication.md").write_text(md, encoding="utf-8")
    d["s44_a42_v4_final_maturity_adjudication.md"] = hashlib.sha256(
        (RETURN_ROOT / "s44_a42_v4_final_maturity_adjudication.md").read_bytes()).hexdigest()
    d["s44_a42_source_grade_delta.json"] = _dump("s44_a42_source_grade_delta.json", delta)
    return {"grade": "FIRST_ORIGINAL_CURRENT_B_MEASURED_NOT_YET_EARNED",
            "n11_state": after["verdict"]["n11_state"],
            "original_measured": after["verdict"]["original_measured_occupied_cells"],
            "historical_or_retained": after["verdict"]["historical_or_retained_cells"],
            "missing": after["verdict"]["missing_expected_cells"],
            "functional_evidence_gates": after["verdict"].get("functional_evidence_gates"),
            "historical_as2b_supported_fact": hist["as2b"]["supported_fact"],
            "handoff_grade": ho["grade"], "deferred_waves": ho["deferred_ledger"]["wave_count"],
            "selected_decision_wave": ho["single_decision"]["selected_wave"],
            "artifact_sha256": d,
            "blended": hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()}


def replay():
    a = assemble(); b = assemble()
    return {"cold_replay_stable": a["artifact_sha256"] == b["artifact_sha256"],
            "blended": a["blended"]}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("assemble", "replay"))
    a = ap.parse_args()
    print(json.dumps(assemble() if a.command == "assemble" else replay(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
