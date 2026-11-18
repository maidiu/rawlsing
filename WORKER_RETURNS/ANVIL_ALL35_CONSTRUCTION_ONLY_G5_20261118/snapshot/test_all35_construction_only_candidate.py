"""Focused candidate test: construction-only entry with native child proof."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_r157_projection_adapter import SourceReadAdmissionRefusal
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_construction_only
from rawlsing_next.tests.test_pyat960_s1e_support import (
    DenyResolver, source_fixture,
)

CHILD = Path(__file__).with_name("all35_construction_only_child.py")
SCRATCH_ROOT = Path(__file__).resolve().parents[2]


def _run_child(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = {
        **os.environ,
        "PYTHONPATH": str(SCRATCH_ROOT),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    return subprocess.run(
        [sys.executable, "-B", str(CHILD), str(root), *args],
        cwd=str(SCRATCH_ROOT), env=env, text=True, capture_output=True,
    )


def _pid_alive(pid: int) -> bool:
    probe = subprocess.run(
        ["ps", "-p", str(pid), "-o", "pid="],
        capture_output=True, text=True,
    )
    return bool(probe.stdout.strip())


def test_native_child_construction_then_fresh_full_payload_reopen(tmp_path):
    root = tmp_path / "native"
    root.mkdir()
    produced = _run_child(root, "producer")
    assert produced.returncode == 0, produced.stdout + produced.stderr
    build = json.loads((root / "build.json").read_text())
    assert _pid_alive(build["producer_pid"]) is False
    assert build["sourcefree_test_only"] is True
    assert build["original_source_bodies_read"] is False
    assert build["joined_q2"] is False
    assert build["authorized_executable_q2"] is False
    assert build["issued_workload"] is False
    assert build["has_operation_fates"] is False
    assert build["has_census_audit"] is False
    assert build["unresolved_states"]["operation_eligibility"] == "UNRESOLVED_NOT_EVALUATED"
    assert build["unresolved_states"]["analytical_issuance"] == "NOT_ISSUED"
    assert build["source_metadata"]["source_id"]
    assert set(build["payload_digests"]) == set(build["family_counts"])
    assert build["body_transport"]["complete"] is True

    for mode in ("positive", "wrong_current", "revoked", "wrong_root"):
        result = _run_child(root, "reopen", mode)
        assert result.returncode == 0, (
            mode + "\n" + result.stdout + result.stderr
        )
    positive = json.loads((root / "reopen_positive.json").read_text())
    assert positive["producer_exited_before_reader"] is True
    assert positive["roots_equal_build"] is True
    assert positive["family_counts"] == build["family_counts"]
    assert positive["payload_digests"] == build["payload_digests"]
    assert positive["identity_payload_equivalent"] is True
    assert positive["routing_payload_equivalent"] is True
    for mode in ("wrong_current", "revoked", "wrong_root"):
        refusal = json.loads((root / f"refusal_{mode}.json").read_text())
        assert refusal["refused"] is True
        assert refusal["before_estate_open"] is True
        assert refusal["error_type"] == "DirectEstateError"


def test_original_missing_resolver_refuses_before_source_bytes(tmp_path, monkeypatch):
    fixture = source_fixture(tmp_path / "src-original", original=True)
    dest = tmp_path / "denied.sqlite"
    import rawlsing_next.pre553_source_i02_handoff as handoff_mod

    calls = []

    def forbidden(*args, **kwargs):
        calls.append(1)
        raise AssertionError("source bytes were decoded")

    monkeypatch.setattr(handoff_mod, "decode_sav", forbidden)
    monkeypatch.setattr(handoff_mod, "decode_dta", forbidden)
    with pytest.raises(SourceReadAdmissionRefusal, match="SOURCE_READ_NOT_CURRENT"):
        build_source_i02_construction_only(
            config=fixture["config"], source_path=fixture["path"],
            destination=dest, resolver=DenyResolver(), host="h", purpose="p",
            consumer_use="c", semantic_use_scope=("S1E_SOURCEFREE",),
        )
    assert calls == []
    assert not dest.exists()
