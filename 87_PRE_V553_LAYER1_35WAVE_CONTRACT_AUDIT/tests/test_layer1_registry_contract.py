from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE" / "runtime_reproducibility_code"
SCRIPT = ROOT / "data" / "ddm_build_copy" / "ddm_v550j_registry_contract.py"
spec = importlib.util.spec_from_file_location("registry_contract", SCRIPT)
assert spec and spec.loader
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


def test_draft_registry_rejected():
    assert contract.registry_status_is_executable("draft") is False


def test_review_only_registry_rejected():
    assert contract.registry_status_is_executable("review_only") is False


def test_governed_registry_accepted():
    assert contract.registry_status_is_executable("governed") is True


def test_runner_and_consumer_share_same_status_set():
    assert contract.EXECUTABLE_JOINT_REGISTRY_STATUSES == frozenset({"active", "approved", "certified", "governed"})


def test_layer1_authority_release_is_accepted_for_bounded_audit():
    assert (
        contract.require_joint_configuration_authority_release("V550J-LAYER1-AUDIT-AUTHORITY-2026-08-03-R1")
        == "V550J-LAYER1-AUDIT-AUTHORITY-2026-08-03-R1"
    )
