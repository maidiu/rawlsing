"""One-candidate HB04 runner.  No ranking or cross-candidate logic lives here."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping

from rawlsing_next.as4.loader import (
    HB04FreezeError,
    load_hb04_manifest,
    reject_ungoverned_directive,
)
from rawlsing_next.as4.protocol import prepare, result_identity_receipt


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def run_candidate(
    *,
    candidate: str,
    workdir: Path,
    bounded_fixture: bool = False,
    freeze_path: Path | None = None,
    expected_source_sha256: str | None = None,
    directives: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    if candidate not in {"A", "B", "C"}:
        raise HB04FreezeError("candidate must be exactly A, B, or C")
    reject_ungoverned_directive(directives)
    manifest = load_hb04_manifest(freeze_path=freeze_path)
    if not bounded_fixture:
        raise HB04FreezeError(
            "production source preparation is separately gated; B21 may execute only "
            "the explicit governed bounded fixture"
        )

    from rawlsing_next.as4.bounded_fixture import build_bounded_source

    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    source = build_bounded_source(candidate, workdir)
    if expected_source_sha256 is not None and source.source_sha256 != expected_source_sha256:
        raise HB04FreezeError("source SHA mismatch before semantic execution")

    session = None
    cleanup = None
    try:
        session = prepare(
            candidate,
            source,
            manifest,
            workdir,
            allow_bounded_fixture=True,
        )
        i03 = session.run_i03()
        i05 = session.run_i05()
        identity = result_identity_receipt(candidate, i03, i05)
        measurements = session.measurements
    finally:
        if session is not None:
            cleanup = session.close()
        else:
            # Source preparation may have created bounded scratch before prepare.
            for path in source.cleanup_paths:
                try:
                    import shutil
                    shutil.rmtree(path)
                except OSError:
                    pass

    if cleanup is None or cleanup.get("status") != "PASS_CLOSED_AND_SCRATCH_REMOVED":
        raise HB04FreezeError("candidate cleanup did not close exactly")
    semantic_digest = _sha(identity)
    return {
        "schema": "HB04_RUN_CANDIDATE_RECEIPT@1.0.0",
        "status": "PASS",
        "candidate": candidate,
        "process_id": os.getpid(),
        "intake_freeze_sha256": manifest.intake_sha256,
        "successor_package": manifest.successor_identity_receipt,
        "source": dict(source.source_identity_receipt),
        "semantic_identity": identity,
        "semantic_identity_sha256": semantic_digest,
        "resource_observation": measurements,
        "cleanup": cleanup,
        "session_closed": True,
        "fresh_process_required_by_run_all": True,
        "ranking_logic_count": 0,
        "selection_logic_count": 0,
        "real_lits1_open_count": 0,
        "real_wvs7_open_count": 0,
        "c09_execution_count": 0,
        "hb05_hb06_hb07_execution_count": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, choices=("A", "B", "C"))
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--freeze")
    parser.add_argument("--expected-source-sha256")
    parser.add_argument("--bounded-fixture", action="store_true")
    parser.add_argument("--directive-json")
    parser.add_argument("--extra-accelerator")
    args = parser.parse_args(argv)

    directives: dict[str, Any] = {}
    if args.directive_json:
        value = json.loads(args.directive_json)
        if not isinstance(value, dict):
            raise HB04FreezeError("directive JSON must be an object")
        directives.update(value)
    if args.extra_accelerator:
        directives["extra_accelerator"] = args.extra_accelerator
    reject_ungoverned_directive(directives)

    receipt = run_candidate(
        candidate=args.candidate,
        workdir=Path(args.workdir),
        bounded_fixture=args.bounded_fixture,
        freeze_path=Path(args.freeze) if args.freeze else None,
        expected_source_sha256=args.expected_source_sha256,
        directives=directives,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_canonical(receipt) + "\n", encoding="utf-8")
    print(_canonical(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
