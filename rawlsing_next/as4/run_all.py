"""Sequential fresh-process HB04 A/B/C runner.

Order is frozen A -> B -> C.  Children never overlap and no comparative
performance or winner-selection logic is permitted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any, Mapping

from rawlsing_next.as4.loader import HB04FreezeError, load_hb04_manifest, reject_ungoverned_directive


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_all(
    *,
    workdir: Path,
    bounded_fixture: bool = False,
    freeze_path: Path | None = None,
    directives: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    reject_ungoverned_directive(directives)
    manifest = load_hb04_manifest(freeze_path=freeze_path)
    if not bounded_fixture:
        raise HB04FreezeError(
            "production source preparation is separately gated; B21 run_all may "
            "execute only the explicit governed bounded fixture"
        )
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    children = []
    previous_finish = None
    for index, candidate in enumerate(manifest.candidate_order, 1):
        child_dir = workdir / f"{index}_{candidate}"
        output = workdir / f"{index}_{candidate}_receipt.json"
        if child_dir.exists():
            shutil.rmtree(child_dir)
        cmd = [
            sys.executable,
            "-m",
            "rawlsing_next.as4.run_candidate",
            "--candidate",
            candidate,
            "--workdir",
            str(child_dir),
            "--output",
            str(output),
            "--bounded-fixture",
        ]
        if freeze_path is not None:
            cmd.extend(["--freeze", str(freeze_path)])
        started = time.monotonic_ns()
        if previous_finish is not None and started < previous_finish:
            raise HB04FreezeError("sequential runner monotonic ordering failed")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pid = proc.pid
        stdout, stderr = proc.communicate()
        finished = time.monotonic_ns()
        if proc.returncode != 0:
            raise HB04FreezeError(
                f"HB04 candidate {candidate} child failed with {proc.returncode}: {stderr}"
            )
        if not output.is_file():
            raise HB04FreezeError(f"HB04 candidate {candidate} emitted no receipt")
        receipt = json.loads(output.read_text(encoding="utf-8"))
        if receipt.get("candidate") != candidate or receipt.get("status") != "PASS":
            raise HB04FreezeError(f"HB04 candidate {candidate} receipt mismatch")
        if receipt.get("process_id") != pid:
            raise HB04FreezeError(f"HB04 candidate {candidate} process identity mismatch")
        cleanup = receipt.get("cleanup", {})
        if cleanup.get("status") != "PASS_CLOSED_AND_SCRATCH_REMOVED":
            raise HB04FreezeError(f"HB04 candidate {candidate} cleanup receipt failed")
        children.append(
            {
                "candidate": candidate,
                "ordinal": index,
                "process_id": pid,
                "started_monotonic_ns": started,
                "finished_monotonic_ns": finished,
                "receipt_path": str(output),
                "receipt_sha256": _file_sha(output),
                "semantic_identity_sha256": receipt["semantic_identity_sha256"],
                "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
                "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
                "exit_code": proc.returncode,
                "session_closed": receipt["session_closed"],
                "cleanup": cleanup,
            }
        )
        previous_finish = finished
        if child_dir.exists():
            shutil.rmtree(child_dir)

    pids = [row["process_id"] for row in children]
    if len(set(pids)) != 3:
        raise HB04FreezeError("run_all did not use three distinct child processes")
    if [row["candidate"] for row in children] != ["A", "B", "C"]:
        raise HB04FreezeError("run_all candidate order changed")
    for left, right in zip(children, children[1:]):
        if right["started_monotonic_ns"] < left["finished_monotonic_ns"]:
            raise HB04FreezeError("candidate child processes overlapped")

    return {
        "schema": "HB04_RUN_ALL_RECEIPT@1.0.0",
        "status": "PASS",
        "order": ["A", "B", "C"],
        "process_count": 3,
        "distinct_process_count": 3,
        "sequential_no_overlap": True,
        "intake_freeze_sha256": manifest.intake_sha256,
        "children": children,
        "all_sessions_closed": all(row["session_closed"] for row in children),
        "all_cleanup_passed": all(
            row["cleanup"]["status"] == "PASS_CLOSED_AND_SCRATCH_REMOVED"
            for row in children
        ),
        "ranking_logic_count": 0,
        "selection_logic_count": 0,
        "comparative_early_stop_count": 0,
        "real_lits1_open_count": 0,
        "real_wvs7_open_count": 0,
        "c09_execution_count": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--freeze")
    parser.add_argument("--bounded-fixture", action="store_true")
    parser.add_argument("--directive-json")
    parser.add_argument("--extra-accelerator")
    args = parser.parse_args(argv)
    directives: dict[str, Any] = {}
    if args.directive_json:
        value = json.loads(args.directive_json)
        if not isinstance(value, dict):
            raise HB04FreezeError("directive JSON must be one object")
        directives.update(value)
    if args.extra_accelerator:
        directives["extra_accelerator"] = args.extra_accelerator
    reject_ungoverned_directive(directives)
    receipt = run_all(
        workdir=Path(args.workdir),
        bounded_fixture=args.bounded_fixture,
        freeze_path=Path(args.freeze) if args.freeze else None,
        directives=directives,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_canonical(receipt) + "\n", encoding="utf-8")
    print(_canonical(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
