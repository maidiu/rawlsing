"""CLI for the exact SRC04 observed-response native workload builder.

Modes:
  plan             construct the finite plan from SCOPE_LEDGER_V2 + pending contract
  fixture-evidence execute the production builder against the labelled nonrespondent fixture
  execute          refuse original execution until full release + exact authority exist

No original source file is opened by any mode.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from campaign_src04_completion.empirical.native_workload import (
    NativeWorkloadRefusal,
    WorkloadPolicy,
    plan_from_scope,
)
from rawlsing_next.pre553_empirical_objects import canonicalize
from rawlsing_next.pre553_observed_response import ObservedResponseContract

ROOT = Path(__file__).resolve().parents[2]
EMPIRICAL = ROOT / "campaign_src04_completion/empirical"
DEFAULT_SCOPE = EMPIRICAL / "SCOPE_LEDGER_V2.json"
DEFAULT_CONTRACT = EMPIRICAL / "CONTRACT_APPROVAL_READY_V2.json"
PLAN_PATH = EMPIRICAL / "NATIVE_WORKLOAD_PLAN_V2.json"
REFUSAL_PATH = EMPIRICAL / "NATIVE_WORKLOAD_REFUSAL.json"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, value) -> None:
    path.write_text(json.dumps(canonicalize(value), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _contract(path: Path) -> ObservedResponseContract:
    raw = _load(path)
    material = raw.get("contract", raw)
    return ObservedResponseContract.from_mapping(material)


def run_plan(scope_path: Path, contract_path: Path) -> int:
    scope = _load(scope_path)
    contract = _contract(contract_path)
    if scope.get("contract_ref") != contract.ref.as_dict():
        raise NativeWorkloadRefusal("SCOPE_CONTRACT_REF_MISMATCH")
    policy = WorkloadPolicy.from_mapping(scope.get("workload_policy", {}))
    plan = plan_from_scope(scope=scope, contract=contract, policy=policy)
    plan.update({
        "scope_path": str(scope_path.relative_to(ROOT)),
        "scope_sha256": _sha(scope_path),
        "contract_path": str(contract_path.relative_to(ROOT)),
        "contract_sha256": _sha(contract_path),
        "contract_ref": contract.ref.as_dict(),
        "contract_state": contract.contract_state,
        "original_execution": {
            "issued": 0,
            "executed": 0,
            "status": "REFUSED_UNTIL_FULL_RELEASE_AND_EXACT_AUTHORITY",
            "reason": "pending operation authority + full SRC04 C11 release; no original source I/O in Lane C",
        },
    })
    _write(PLAN_PATH, plan)
    print(json.dumps({
        "status": "PLAN_COMPLETE",
        "plan": str(PLAN_PATH.relative_to(ROOT)),
        "available": plan["scope"]["available_response_fields"],
        "held": plan["scope"]["held_response_fields"],
        "unary": plan["operations"]["unary_operations"],
        "joint": plan["operations"]["joint_pair_operations"],
        "conditional_pairs": plan["operations"]["conditional_target_pairs_awaiting_release_values"],
        "higher_order_not_authorized": plan["operations"]["higher_order_requested_not_authorized"],
    }, indent=2))
    return 0


def run_fixture() -> int:
    from campaign_src04_completion.empirical.fixture_native_workload_evidence import main as fixture_main
    fixture_main()
    return 0


def run_execute() -> int:
    refusal = {
        "schema": "PYAT_SRC04_NATIVE_WORKLOAD_REFUSAL@2.0.0",
        "status": "REFUSED",
        "actual_code": "ORIGINAL_EXECUTION_REQUIRES_FULL_RELEASE_AND_EXACT_AUTHORITY",
        "source_read_performed": False,
        "original_workload_issued": False,
        "reason": "Lane C has no full SRC04 release or positive observed-response operation/topology authority; source-free execution cannot be claimed.",
        "allowed_modes": ["plan", "fixture-evidence"],
    }
    _write(REFUSAL_PATH, refusal)
    print(json.dumps(refusal, indent=2))
    return 2


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("plan", "fixture-evidence", "execute"), default="plan")
    parser.add_argument("--scope", default=str(DEFAULT_SCOPE))
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    args = parser.parse_args(argv)
    try:
        if args.mode == "plan":
            return run_plan(Path(args.scope), Path(args.contract))
        if args.mode == "fixture-evidence":
            return run_fixture()
        return run_execute()
    except NativeWorkloadRefusal as exc:
        print(json.dumps({"status": "REFUSED", "actual_code": exc.code, "detail": exc.detail}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
