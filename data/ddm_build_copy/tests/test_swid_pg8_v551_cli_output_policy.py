from __future__ import annotations

import sys
from pathlib import Path

from data.ddm_build_copy import compile_v551_relation_evidence_atoms as compiler


def test_governed_runner_output_flags_are_accepted_and_forwarded(monkeypatch, tmp_path: Path):
    bridge_path = tmp_path / "bridge.parquet"
    output_root = tmp_path / "out"
    sentinel_bridge = object()
    observed = {}

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "compile_v551_relation_evidence_atoms.py",
            "--run-id",
            "runtime-canary",
            "--bridge-path",
            str(bridge_path),
            "--output-root",
            str(output_root),
            "--v551-compile-mode",
            "canonical",
            "--write-parquet",
            "--no-write-csv",
        ],
    )
    monkeypatch.setattr(compiler, "_read", lambda path: sentinel_bridge)

    def fake_compile(bridge, **kwargs):
        observed["bridge"] = bridge
        observed.update(kwargs)
        return {"run_integrity_status": "PASS"}

    monkeypatch.setattr(compiler, "compile_v551_run", fake_compile)

    assert compiler.main() == 0
    assert observed == {
        "bridge": sentinel_bridge,
        "run_id": "runtime-canary",
        "bridge_path": bridge_path,
        "output_root": str(output_root),
        "write_parquet": True,
        "write_csv": False,
    }


def test_cli_exposes_fail_closed_no_parquet_state(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "compile_v551_relation_evidence_atoms.py",
            "--run-id",
            "runtime-canary",
            "--bridge-path",
            "bridge.parquet",
            "--no-write-parquet",
            "--write-csv",
        ],
    )

    args = compiler.parse_args()

    assert args.write_parquet is False
    assert args.write_csv is True
