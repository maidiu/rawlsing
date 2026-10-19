#!/usr/bin/env python3
"""B43 CLI: freeze frontier, prove feeder/admission, re-run A42 with B43 receipt."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
if str(RETURN_ROOT) not in sys.path:
    sys.path.insert(0, str(RETURN_ROOT))

from frozen_a42.a42 import core as a42core  # noqa: E402
from frozen_a42.frozen_a41.a41.gitpreimage import GitPreimage  # noqa: E402
from b43 import frontier as b43frontier  # noqa: E402
from b43 import feeder  # noqa: E402

REPO = RETURN_ROOT.parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def _dump(name, obj):
    p = RETURN_ROOT / name
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return hashlib.sha256(p.read_bytes()).hexdigest()


def assemble():
    gp = GitPreimage(REPO)
    fr = b43frontier.load_frontier(gp)
    docket = b43frontier.decision_docket(fr)
    owner = feeder.owner_call_contract()

    # A42 base run (frozen A41 + R41 banks), then with the B43 pending receipt.
    scope = a42core.load_scope(gp)
    a41 = a42core.a41_receipts_v2(gp)
    bank = json.loads((RETURN_ROOT / "frozen_a42" / "evidence" / "r41_receipt_bank_v2.json").read_text())
    r41 = a42core.ingest_r41_bank(bank, gp, scope)
    receipts = a41 + r41
    w41reg = a42core.load_w41_register(gp)
    old_manifest = json.loads(gp.blob_at(
        a42core.A41_COMMIT, a42core.A41_DIR + "/estate_acceptance_manifest.json"))
    base = a42core.assess_v2(scope, receipts, w41reg, old_manifest)
    b43r = feeder.b43_a42_receipt(fr, docket)
    after = a42core.assess_v2(scope, receipts + [b43r], w41reg, old_manifest)
    f1f8, manifest, md, intake, wake, j42 = a42core.artifacts(
        after, scope, old_manifest,
        [{"receipt_id": r["receipt_id"], "grade": r["grade"],
          "origin_commit": r["origin_commit"], "claim_id": r["claim_id"],
          "source_return": "E41/W41/P41/A41"} for r in r41])

    digests = {}
    digests["b43_source_frontier.json"] = _dump("b43_source_frontier.json", fr)
    digests["b43_source_owner_decision_docket.json"] = _dump(
        "b43_source_owner_decision_docket.json", docket)
    digests["b43_a42_v2_f1_f8_acceptance_matrix.json"] = _dump(
        "b43_a42_v2_f1_f8_acceptance_matrix.json", f1f8)
    digests["b43_a42_v2_estate_acceptance_manifest.json"] = _dump(
        "b43_a42_v2_estate_acceptance_manifest.json", manifest)
    (RETURN_ROOT / "b43_a42_v2_final_maturity_adjudication.md").write_text(md, encoding="utf-8")
    digests["b43_a42_v2_final_maturity_adjudication.md"] = hashlib.sha256(
        (RETURN_ROOT / "b43_a42_v2_final_maturity_adjudication.md").read_bytes()).hexdigest()
    delta = {
        "schema": "B43_A42_SOURCE_GRADE_DELTA@1",
        "a42_return": "843175b0587b54db3df1f461ad9f7f1314894372",
        "b43_receipt": "B43-SELECTED-B-SOURCE-FEEDER",
        "base_a42": {"original_measured_occupied_cells": base["verdict"]["original_measured_occupied_cells"],
                     "historical_or_retained_cells": base["verdict"]["historical_or_retained_cells"],
                     "missing_expected_cells": base["verdict"]["missing_expected_cells"],
                     "functional_evidence_gates": base["verdict"].get("functional_evidence_gates")},
        "after_b43": {"original_measured_occupied_cells": after["verdict"]["original_measured_occupied_cells"],
                      "historical_or_retained_cells": after["verdict"]["historical_or_retained_cells"],
                      "missing_expected_cells": after["verdict"]["missing_expected_cells"],
                      "functional_evidence_gates": after["verdict"].get("functional_evidence_gates")},
        "new_original_measured_cells": (after["verdict"]["original_measured_occupied_cells"]
                                        - base["verdict"]["original_measured_occupied_cells"]),
        "truthful_original_measured_occupancy": after["verdict"]["original_measured_occupied_cells"],
        "source_grant_present": False,
        "source_positive_state": "SOURCE_EXECUTION_PENDING_OWNER",
        "feeder_owner": owner,
        "note": ("B43 adds the executable feeder and WG0L provenance repairs; it adds no measured "
                 "original occupancy without a competent grant."),
    }
    digests["b43_a42_source_grade_delta.json"] = _dump("b43_a42_source_grade_delta.json", delta)
    return {"n11_state": after["verdict"]["n11_state"],
            "original_measured_occupied_cells": after["verdict"]["original_measured_occupied_cells"],
            "functional_evidence_gates": after["verdict"].get("functional_evidence_gates"),
            "wave_count": fr["wave_count"], "executed_original_operations": 0,
            "owner": owner["owner"],
            "artifact_sha256": digests,
            "blended": hashlib.sha256(json.dumps(digests, sort_keys=True).encode()).hexdigest()}


def replay():
    import tempfile
    a = assemble()
    b = assemble()
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
