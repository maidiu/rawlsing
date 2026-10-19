#!/usr/bin/env python3
"""A41 CLI: ingest -> assess -> emit the three N11 candidate artifacts.

Usage (from the A41 return root):
    python3 -m a41.cli assemble [--repo REPO_ROOT] [--out-dir DIR]
    python3 -m a41.cli replay   [--repo REPO_ROOT]
"""
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

from a41.gitpreimage import GitPreimage  # noqa: E402
from a41 import receipt_bank, estate_assessor, n11_artifacts  # noqa: E402


def _load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def assemble(repo: Path, out_dir: Path) -> dict:
    scope = _load_json(RETURN_ROOT / "evidence" / "expected_scope_frozen.json")
    bank = _load_json(RETURN_ROOT / "evidence" / "receipt_bank_frozen.json")
    gp = GitPreimage(repo)
    ingested = receipt_bank.ingest_bank(bank, gp, expected_scope=scope)
    accounting = estate_assessor.assess(scope, ingested)
    gm = n11_artifacts.gate_maturity(gp, scope["startup_commit"])

    artifacts = {
        "f1_f8_acceptance_matrix.json": json.dumps(
            n11_artifacts.f1_f8_matrix(accounting, scope, gm), indent=2, sort_keys=True) + "\n",
        "estate_acceptance_manifest.json": json.dumps(
            n11_artifacts.estate_manifest(accounting, scope), indent=2, sort_keys=True) + "\n",
        "final_maturity_adjudication.md": n11_artifacts.final_maturity_md(accounting, scope),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    digests = {}
    for name, payload in artifacts.items():
        (out_dir / name).write_text(payload, encoding="utf-8")
        digests[name] = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return {
        "n11_state": accounting["verdict"]["n11_state"],
        "expected_cells": accounting["verdict"]["total_cells"],
        "original_measured_occupied_cells": accounting["verdict"]["original_measured_occupied_cells"],
        "missing_expected_cells": accounting["verdict"]["missing_expected_cells"],
        "finite_blocker_count": accounting["verdict"]["finite_blocker_count"],
        "ingested_receipts": ingested["ingested_count"],
        "artifact_sha256": digests,
        "blended_digest": hashlib.sha256(
            json.dumps(digests, sort_keys=True).encode("utf-8")).hexdigest(),
    }


def replay(repo: Path) -> dict:
    """Cold replay: assemble twice and require identical artifact digests."""
    import tempfile
    runs = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as d:
            runs.append(assemble(repo, Path(d)))
    stable = runs[0]["artifact_sha256"] == runs[1]["artifact_sha256"]
    return {"cold_replay_stable": stable, "blended_digest": runs[0]["blended_digest"],
            "runs": [r["artifact_sha256"] for r in runs]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("assemble", "replay"))
    ap.add_argument("--repo", type=Path, default=RETURN_ROOT.parents[1])
    ap.add_argument("--out-dir", type=Path, default=RETURN_ROOT)
    args = ap.parse_args()
    if args.command == "assemble":
        print(json.dumps(assemble(args.repo, args.out_dir), indent=2, sort_keys=True))
    else:
        print(json.dumps(replay(args.repo), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
