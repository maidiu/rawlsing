from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rawlsing_next import fiabc_lits_astra_substantive_parity as parity
from rawlsing_next.fiabc_lits_cross_schema_candidate_identity import (
    LOGICAL_CONTRACT,
    current_pre553_logical_candidate_bindings,
)


ROOT = Path(__file__).resolve().parents[2]
WORKER_BASE = "b5737718cc2d3fd4eb5d3737c99fa7de0341e651"
WORKER_IMPLEMENTATION = "1882662f861e93e33bb956e015b984458074e9bc"
WORKER_RETURN_TIP = "fddb356c69d2bcaf64351869aecbb9cec66dd36f"
RETURN = ROOT / "WORKER_RETURNS/PREMAIN-FIABC-LITS-CROSS-SCHEMA-CANDIDATE-NORMALIZATION-R1/RETURN.json"

EXPECTED_IMPLEMENTATION_FILES = {
    "rawlsing_next/ee_p2x_darwin_stage_backend.py",
    "rawlsing_next/fiabc_final_oracle_freeze_producers.py",
    "rawlsing_next/fiabc_lits_astra_substantive_parity.py",
    "rawlsing_next/fiabc_lits_cross_schema_candidate_identity.py",
    "rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py",
}


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def _ensure_history() -> None:
    subprocess.run(
        ["git", "fetch", "--no-tags", "origin", WORKER_BASE, WORKER_IMPLEMENTATION, WORKER_RETURN_TIP],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def test_worker_return_is_exactly_bound_to_qualified_semantic_head():
    ret = json.loads(RETURN.read_text(encoding="utf-8"))
    assert ret["audit_base"] == WORKER_BASE
    assert ret["semantic_implementation_head"] == WORKER_IMPLEMENTATION
    assert ret["qualification"]["run_id"] == 35889692534
    assert ret["qualification"]["job_id"] == 107278727156
    assert ret["qualification"]["governed_tests"] == "100 passed"
    assert ret["status"] == "PASS__SOURCE_FREE_QUALIFIED__INDEPENDENT_ACCEPTANCE_REQUIRED"


def test_worker_history_is_descended_from_exact_blocking_audit_base():
    _ensure_history()
    assert _git("merge-base", WORKER_BASE, WORKER_IMPLEMENTATION) == WORKER_BASE
    assert _git("merge-base", WORKER_IMPLEMENTATION, WORKER_RETURN_TIP) == WORKER_IMPLEMENTATION


def test_implementation_diff_contains_only_expected_production_files_plus_governance_tests():
    _ensure_history()
    names = set(_git("diff", "--name-only", f"{WORKER_BASE}..{WORKER_IMPLEMENTATION}").splitlines())
    production = {n for n in names if n.startswith("rawlsing_next/") and "/tests/" not in n}
    # Commission/court-spec/test changes are governance evidence; only these five production files may change.
    assert production == EXPECTED_IMPLEMENTATION_FILES
    forbidden_suffixes = (".sav", ".dta", ".zip")
    assert not any(n.lower().endswith(forbidden_suffixes) for n in names)


def test_parity_comparison_domain_is_logical_not_native_hash_equality():
    assert "logical_candidate_identity" in parity.PARITY_SECTIONS
    assert "native_candidate_provenance" not in parity.PARITY_SECTIONS
    source = Path(parity.__file__).read_text(encoding="utf-8")
    assert '"native_candidate_hash_equality_required": False' in source
    assert '"historical_native_candidate_hash_domain": "G02_EXECUTION_CANDIDATE_HASH"' in source
    assert '"current_native_candidate_hash_domain": "PRE553_I05_CANDIDATE_HASH"' in source
    assert LOGICAL_CONTRACT == "FIABC_LITS_CROSS_SCHEMA_LOGICAL_CANDIDATE@1.0.0"


def test_return_preserves_bank_checkpoint_as_downstream_evidence_only():
    ret = json.loads(RETURN.read_text(encoding="utf-8"))
    assert ret["banked_lits_downstream_evidence"]["checkpoint_identity"] == (
        "8593814c51456015e5167cbe6f05037de7dbeadcc36ab857c72192b9087f9062"
    )
    assert ret["banked_lits_downstream_evidence"]["oracle_identity"] == (
        "eca0ce0ad4bf6299e3705899099c21a0d635e1828f7b4c7e2cee0be4e9f05db0"
    )
    assert ret["prohibited_activity"]["banked_lits_checkpoint_consumed"] is False
    assert ret["prohibited_activity"]["banked_lits_oracle_altered"] is False


def test_return_preserves_exact_wvs7_frozen_truth():
    ret = json.loads(RETURN.read_text(encoding="utf-8"))
    wvs = ret["wvs7_conservation"]
    assert wvs["terminal_counts"] == {"COVERAGE_LIMITED": 46}
    assert wvs["successor_lock2"] == "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
    assert wvs["discovery_authority"] == "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"
    assert wvs["oracle_identity"] == "3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800"
    assert wvs["truth_identity"] == "eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405"
    assert wvs["candidate_processes_started"] == 0
    assert wvs["candidate_outputs_seen"] == 0
