#!/usr/bin/env python3
"""A42 CLI: verify frozen A41 + R41 bank, assess, emit v2 N11 candidate artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
if str(RETURN_ROOT) not in sys.path:
    sys.path.insert(0, str(RETURN_ROOT))

from a42 import core  # noqa: E402
from frozen_a41.a41.gitpreimage import GitPreimage  # noqa: E402

REPO = RETURN_ROOT.parents[1]


def _load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def assemble(out_dir: Path):
    gp = GitPreimage(REPO)
    scope = core.load_scope(gp)
    a41 = core.a41_receipts_v2(gp)
    bank = _load(RETURN_ROOT / "evidence" / "r41_receipt_bank_v2.json")
    r41 = core.ingest_r41_bank(bank, gp, scope)
    receipts = a41 + r41
    w41reg = core.load_w41_register(gp)
    old_manifest = json.loads(gp.blob_at(
        core.A41_COMMIT, core.A41_DIR + "/estate_acceptance_manifest.json"))
    acc = core.assess_v2(scope, receipts, w41reg, old_manifest)
    meta = [{"receipt_id": r["receipt_id"], "grade": r["grade"],
             "origin_commit": r["origin_commit"],
             "claim_id": r["claim_id"], "source_return": r.get("source_return")}
            for r in r41]
    f1f8, manifest, md, intake, wake, j42 = core.artifacts(acc, scope, old_manifest, meta)
    out_dir.mkdir(parents=True, exist_ok=True)
    payloads = {
        "f1_f8_acceptance_matrix.json": json.dumps(f1f8, indent=2, sort_keys=True) + "\n",
        "estate_acceptance_manifest.json": json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        "final_maturity_adjudication.md": md,
        "n11_r41_return_intake_and_delta.json": json.dumps(intake, indent=2, sort_keys=True) + "\n",
        "original35_source_positive_execution_wake_packet.json": json.dumps(wake, indent=2, sort_keys=True) + "\n",
        "j42_addon_endpoint.json": json.dumps(j42, indent=2, sort_keys=True) + "\n",
    }
    digests = {}
    for name, text in payloads.items():
        (out_dir / name).write_text(text, encoding="utf-8")
        digests[name] = hashlib.sha256(text.encode()).hexdigest()
    return {"n11_state": acc["verdict"]["n11_state"],
            "original_measured": acc["verdict"]["original_measured_occupied_cells"],
            "missing": acc["verdict"]["missing_expected_cells"],
            "sourcefree_integrated": acc["verdict"]["sourcefree_integrated_cells"],
            "independently_accepted_sourcefree": acc["verdict"]["independently_accepted_sourcefree_cells"],
            "historical_or_retained": acc["verdict"]["historical_or_retained_cells"],
            "unmatched_unresolved": acc["verdict"]["unmatched_still_unresolved"],
            "receipts": len(receipts), "artifact_sha256": digests,
            "blended": hashlib.sha256(json.dumps(digests, sort_keys=True).encode()).hexdigest()}


def replay(out_dir: Path):
    import tempfile
    runs = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as d:
            runs.append(assemble(Path(d)))
    return {"cold_replay_stable": runs[0]["artifact_sha256"] == runs[1]["artifact_sha256"],
            "blended": runs[0]["blended"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("assemble", "replay"))
    ap.add_argument("--out-dir", type=Path, default=RETURN_ROOT)
    a = ap.parse_args()
    print(json.dumps(assemble(a.out_dir) if a.command == "assemble" else replay(a.out_dir),
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
