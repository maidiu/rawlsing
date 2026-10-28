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

from campaign_src04_completion.empirical.authorized_execution import (
    AuthorizedExecutionRefusal,
    GRANT_SHA256,
    SOURCE_SHA256,
    authenticate_grant,
    execute_issued,
    issue_authorized_execution,
    load_parquet_release,
    preflight,
)
from campaign_src04_completion.empirical.consumer_bridge import consume_with_lane_d
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
GRANT_PATH = EMPIRICAL / "USER_EMPIRICAL_GRANT.json"
EXECUTION_PATH = EMPIRICAL / "NATIVE_WORKLOAD_EXECUTION.json"
PREFLIGHT_PATH = EMPIRICAL / "NATIVE_WORKLOAD_PREFLIGHT.json"


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


def run_execute(
    *,
    grant_path: Path,
    grant_sha256: str,
    scope_path: Path,
    contract_path: Path,
    parquet_root: Path | None,
    release_id: str | None,
    semantic_hash_value: str | None,
    source_sha256: str,
    start_after_operation_id: str | None,
    run_consumer: bool,
) -> int:
    grant = authenticate_grant(grant_path, grant_sha256)
    scope = _load(scope_path)
    pending = _contract(contract_path)
    if scope.get("contract_ref") != pending.ref.as_dict():
        raise NativeWorkloadRefusal("SCOPE_CONTRACT_REF_MISMATCH")
    policy = WorkloadPolicy.from_mapping(scope.get("workload_policy", {}))
    if parquet_root is None or release_id is None or semantic_hash_value is None:
        pending_record = preflight(grant=grant, pending_contract=pending, scope=scope)
        pending_record["required_command"] = (
            "PYTHONPATH=. python3 campaign_src04_completion/empirical/run_native_workload.py "
            "--mode execute --parquet-root <exact-parquet-root> --release-id <exact-release-id> "
            "--semantic-hash <exact-semantic-hash> --source-sha "
            "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18 "
            "--consumer"
        )
        pending_record["consumer_path"] = {
            "owner": "campaign_src04_completion.consumers.consumer.consume_native_producer",
            "status": "READ_ONLY_EXTERNAL_DEPENDENCY_NOT_JOINED",
            "dependency": "accepted Lane D consumer module",
            "discovery_or_effective_n_required": True,
        }
        _write(PREFLIGHT_PATH, pending_record)
        print(json.dumps({
            "status": pending_record["status"],
            "grant_sha256": grant.sha256,
            "preflight": str(PREFLIGHT_PATH.relative_to(ROOT)),
            "required_input": pending_record["release_input_required"],
        }, indent=2))
        return 0
    if source_sha256 != SOURCE_SHA256:
        raise NativeWorkloadRefusal("SOURCE_SHA_MISMATCH", source_sha256)
    release = load_parquet_release(
        root=parquet_root,
        source_sha256=source_sha256,
        release_id=release_id,
        semantic_hash_value=semantic_hash_value,
    )
    issued = issue_authorized_execution(
        grant=grant, release=release, pending_contract=pending, policy=policy)
    workload = execute_issued(
        issued, start_after_operation_id=start_after_operation_id)
    record = {
        "schema": "PYAT_SRC04_AUTHORIZED_NATIVE_EXECUTION@1.0.0",
        "status": "AUTHORIZED_NATIVE_EXECUTION_COMPLETE",
        "grant": {"path": str(grant.path.relative_to(ROOT)) if grant.path.is_relative_to(ROOT) else str(grant.path), "sha256": grant.sha256, "ref": grant.ref.as_dict()},
        "release_ref": release.release_ref.as_dict(),
        "source_artifact_ref": release.source_artifact_ref.as_dict(),
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "contract_ref": issued.contract.ref.as_dict(),
        "authority_refs": {
            "source_literal": issued.source_literal_authority_ref.as_dict(),
            "target_use": issued.target_use_authority_ref.as_dict(),
            "topology_count": len(issued.topology_authority_refs),
        },
        "held_targets": list(issued.held_targets),
        "workload": workload.receipt(),
        "original_workload_issued": True,
        "source_read_performed": False,
        "raw_respondent_rows_committed": False,
        "consumer_path": {
            "owner": "campaign_src04_completion.consumers.consumer.consume_native_producer",
            "required_dependency": "accepted Lane D consumer module joined as read-only dependency",
            "command": "PYTHONPATH=. python3 campaign_src04_completion/empirical/run_native_workload.py --mode execute ... --consumer",
            "discovery_or_effective_n_required": True,
        },
    }
    if run_consumer:
        bridge = consume_with_lane_d(grant=grant, issued=issued, workload=workload)
        record["consumer"] = {
            "status": bridge.status,
            "detail": bridge.detail,
            "product": canonicalize(bridge.product) if bridge.product is not None else None,
        }
    _write(EXECUTION_PATH, record)
    print(json.dumps({
        "status": record["status"],
        "execution": str(EXECUTION_PATH.relative_to(ROOT)),
        "contract_ref": record["contract_ref"],
        "executed": workload.accounting.get("executed_operations"),
        "refused": workload.accounting.get("refused_operations"),
        "held_targets": len(issued.held_targets),
    }, indent=2))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("plan", "fixture-evidence", "execute"), default="plan")
    parser.add_argument("--scope", default=str(DEFAULT_SCOPE))
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    parser.add_argument("--grant", default=str(GRANT_PATH))
    parser.add_argument("--grant-sha256", default=GRANT_SHA256)
    parser.add_argument("--parquet-root", default=None)
    parser.add_argument("--release-id", default=None)
    parser.add_argument("--semantic-hash", default=None)
    parser.add_argument("--source-sha", default=SOURCE_SHA256)
    parser.add_argument("--start-after", default=None)
    parser.add_argument("--consumer", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.mode == "plan":
            return run_plan(Path(args.scope), Path(args.contract))
        if args.mode == "fixture-evidence":
            return run_fixture()
        return run_execute(
            grant_path=Path(args.grant),
            grant_sha256=args.grant_sha256,
            scope_path=Path(args.scope),
            contract_path=Path(args.contract),
            parquet_root=Path(args.parquet_root) if args.parquet_root else None,
            release_id=args.release_id,
            semantic_hash_value=args.semantic_hash,
            source_sha256=args.source_sha,
            start_after_operation_id=args.start_after,
            run_consumer=args.consumer,
        )
    except (NativeWorkloadRefusal, AuthorizedExecutionRefusal) as exc:
        print(json.dumps({"status": "REFUSED", "actual_code": exc.code, "detail": exc.detail}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
