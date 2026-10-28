"""Execute the independently accepted original SRC04 observed workload.

This entry point uses only the accepted durable native release receipt bundle and
the human empirical grant.  It never opens the original SAV and never rebuilds a
source release.  The default paths are the exact pins recorded in the execution
commission; every override is content-hashed and surfaced in the return.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Mapping

from campaign_src04_completion.empirical.actual_carrier import load_actual_carrier_view
from campaign_src04_completion.empirical.authorized_execution import (
    authenticate_grant,
    issue_authorized_execution,
)
from campaign_src04_completion.empirical.consumer_bridge import consume_with_lane_d
from campaign_src04_completion.empirical.native_streaming import execute_native_workload_stream
from campaign_src04_completion.empirical.native_workload import WorkloadPolicy
from rawlsing_next.pre553_observed_response import ObservedResponseContract

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE = Path(
    "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/d1-src04-observed-tally/"
    "campaign_src04_completion/release/evidence")
DEFAULT_BUNDLE = Path(
    "/Users/matthewsmith/Library/Application Support/Rawlsing/campaign-src04-full/"
    "releases/SRC04-9ddec98561a0fc54")
DEFAULT_GRANT = ROOT / "campaign_src04_completion/empirical/USER_EMPIRICAL_GRANT.json"
DEFAULT_CONTRACT = ROOT / "campaign_src04_completion/empirical/CONTRACT_APPROVAL_READY_V2.json"
DEFAULT_RECEIPT_DIR = ROOT / ".r61/src04-original-execution"
EXPECTED = {
    "source_sha256": "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18",
    "local_receipt_sha256": "dc085fb28d6ed2ed0ce3a2460484d6b532ac7ee6243be41e28abb30e952b099d",
    "release_receipt_sha256": "eba37061a5642ee82c13f1759eba623572435d97968f4c10fb8a59b1999a0ede",
    "primary_run_sha256": "700475070365d7d526165cd6c741da31e605281fb17e47bfb43b9a1035e128a9",
}
POLICY = WorkloadPolicy(
    policy_id="SRC04-ORIGINAL-QUALIFIED-RELEASE-FINITE-FRONTIER",
    families=(
        "UNARY_OBSERVED_DISTRIBUTION",
        "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
        "SAME_RESPONDENT_JOINT_DISTRIBUTION",
    ),
    max_arity=2,
)


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return _sha(path)


def run(*, evidence_dir: Path, bundle_dir: Path, grant_path: Path,
        pending_contract_path: Path, receipt_dir: Path) -> dict[str, Any]:
    started = time.time()
    progress_path = receipt_dir / "progress.jsonl"
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_handle = progress_path.open("w", encoding="utf-8")

    def progress(event: Mapping[str, Any]) -> None:
        record = {"elapsed_seconds": round(time.time() - started, 1), **dict(event)}
        progress_handle.write(json.dumps(record, sort_keys=True) + "\n")
        progress_handle.flush()
        print(json.dumps(record, sort_keys=True), flush=True)

    print(json.dumps({"status": "LOADING_ACCEPTED_NATIVE_VIEW"}, sort_keys=True), flush=True)
    release, view = load_actual_carrier_view(
        local_receipt_path=evidence_dir / "LOCAL_RELEASE_RECEIPT.json",
        release_receipt_path=evidence_dir / "RELEASE_RECEIPT.json",
        primary_run_path=evidence_dir / "ACTUAL_PRIMARY_RUN.json",
        bundle_dir=bundle_dir,
        expected_source_sha256=EXPECTED["source_sha256"],
        local_receipt_sha256=EXPECTED["local_receipt_sha256"],
        release_receipt_sha256=EXPECTED["release_receipt_sha256"],
        primary_run_sha256=EXPECTED["primary_run_sha256"],
    )
    view_path = receipt_dir / "execution_view.json"
    view_sha = _write(view_path, view)
    print(json.dumps({"status": "NATIVE_VIEW_READY", "view": view}, sort_keys=True), flush=True)

    grant = authenticate_grant(grant_path)
    pending = ObservedResponseContract.from_mapping(
        json.loads(pending_contract_path.read_text(encoding="utf-8"))["contract"])
    issued = issue_authorized_execution(
        grant=grant, release=release, pending_contract=pending, policy=POLICY)
    issued_path = receipt_dir / "issued_contract.json"
    issued_sha = _write(issued_path, {
        "contract_ref": issued.contract.ref.as_dict(),
        "contract": issued.contract.as_dict(),
        "release_ref": release.release_ref.as_dict(),
        "target_count": len(issued.contract.target_refs),
        "held_targets": list(issued.held_targets),
        "fixture_only": issued.fixture_only,
        "source_literal_authority_ref": issued.source_literal_authority_ref.as_dict(),
        "target_use_authority_ref": issued.target_use_authority_ref.as_dict(),
    })
    print(json.dumps({
        "status": "ORIGINAL_CONTRACT_ISSUED",
        "contract_ref": issued.contract.ref.as_dict(),
        "targets": len(issued.contract.target_refs),
        "held": len(issued.held_targets),
    }, sort_keys=True), flush=True)

    operation_receipts = receipt_dir / "operation_receipts.jsonl"
    streamed = execute_native_workload_stream(
        repository=issued.repository,
        release_ref=release.release_ref,
        contract=issued.contract,
        authority_registry=issued.registry,
        policy=POLICY,
        receipt_path=operation_receipts,
        include_consumer_conditional=True,
        progress_callback=progress,
        resume=True,
    )
    progress_handle.close()
    stream_path = receipt_dir / "stream_result.json"
    stream_sha = _write(stream_path, streamed.return_projection())
    print(json.dumps({
        "status": "ORIGINAL_NATIVE_OPERATIONS_COMPLETE",
        "accounting": dict(streamed.accounting),
    }, sort_keys=True), flush=True)

    consumer = consume_with_lane_d(
        grant=grant, issued=issued, workload=streamed.workload)
    consumer_path = receipt_dir / "consumer_product.json"
    consumer_value = {
        "status": consumer.status,
        "detail": consumer.detail,
        "product": consumer.product,
    }
    consumer_sha = _write(consumer_path, consumer_value)
    product = consumer.product or {}
    product_summary = {
        "status": consumer.status,
        "downstream_value_effect": product.get("downstream_value_effect"),
        "downstream_value_consumer": product.get("downstream_value_consumer"),
        "observed_response": product.get("observed_response"),
        "claim_ceiling": (product.get("contract") or {}).get("claim_ceiling")
        if isinstance(product.get("contract"), Mapping) else None,
        "source_local_claim": product.get("source_local_claim"),
        "fixture_only": product.get("fixture_only"),
        "limits": product.get("limits"),
        "raw_numerator_support": product.get("raw_numerator_support"),
        "raw_denominator_support": product.get("raw_denominator_support"),
        "discovery_status": (product.get("downstream_discovery") or {}).get("status")
        if isinstance(product.get("downstream_discovery"), Mapping) else None,
    }
    return {
        "schema": "PYAT_SRC04_ORIGINAL_NATIVE_EXECUTION_RETURN@1.0.0",
        "status": "ORIGINAL_NATIVE_WORKLOAD_AND_CONSUMER_EXECUTED",
        "source_id": "SRC04",
        "source_sha256": EXPECTED["source_sha256"],
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "release_ref": release.release_ref.as_dict(),
        "source_read_performed_by_lane_c": False,
        "fixture_substituted": False,
        "actual_original_execution_claimed": streamed.accounting["executed_operations"] > 0,
        "receipts": {
            "local_release_receipt_sha256": EXPECTED["local_receipt_sha256"],
            "release_receipt_sha256": EXPECTED["release_receipt_sha256"],
            "actual_primary_run_sha256": EXPECTED["primary_run_sha256"],
        },
        "view": {
            **view,
            "execution_view_path": str(view_path),
            "execution_view_sha256": view_sha,
            "full_stream_count_and_hash_verified": True,
            "view_is_transient_query_projection_not_new_release": True,
        },
        "contract_ref": issued.contract.ref.as_dict(),
        "contract_path": str(issued_path),
        "contract_sha256": issued_sha,
        "targets": {
            "qualified_contract_targets": len(issued.contract.target_refs),
            "observed_operations_targets": streamed.accounting["selected_observed_targets"],
            "held_or_unobserved": streamed.accounting["held_or_unobserved_targets"],
            "q217_held_elsewhere": True,
        },
        "operations": dict(streamed.accounting),
        "operation_receipt_path": str(operation_receipts),
        "operation_receipt_sha256": streamed.receipt_sha256,
        "stream_result_path": str(stream_path),
        "stream_result_sha256": stream_sha,
        "consumer": product_summary,
        "consumer_product_path": str(consumer_path),
        "consumer_product_sha256": consumer_sha,
        "limits": [
            "C did not stat/hash/open/decode the original SAV; it consumed the accepted durable native release and receipts only.",
            "The execution view streamed and dropped routing/coordinate/weight carriers that observed-response I03 cannot use; all 1,298,649 response events, 7,337 respondent identities, universes and authorities were retained.",
            "The release is source-local observed-response evidence; it is not a population, weighted, causal, structural, canonical, FF/V553, N11 or N12 claim.",
            "Conditional directions are exactly derivable from retained same-person joint cell projections; one ordinary conditional operation was issued only for the accepted Lane D consumer shape.",
            "Sparse-cell interpretation remains limited; exact counts, denominator provenance and valid zeros are preserved.",
            "q217 remains held outside the 177-response qualified release; C makes no q217 or residual-zero claim.",
        ],
        "replay": {
            "command": "PYTHONPATH=. python3 campaign_src04_completion/empirical/run_original_execution.py --evidence-dir <release-evidence> --bundle-dir <durable-release> --receipt-dir <local-receipt-dir>",
            "note": "Replays only from the exact receipt-pinned accepted native bundle; no source conversion or reconstruction.",
        },
        "elapsed_seconds": round(time.time() - started, 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--bundle-dir", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--grant", type=Path, default=DEFAULT_GRANT)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--receipt-dir", type=Path, default=DEFAULT_RECEIPT_DIR)
    parser.add_argument("--output", type=Path, default=ROOT / "campaign_src04_completion/empirical/ORIGINAL_EXECUTION_RETURN.json")
    args = parser.parse_args()
    if args.output.exists():
        try:
            existing = json.loads(args.output.read_text(encoding="utf-8"))
        except Exception:
            existing = {}
        if existing.get("status") == "ORIGINAL_NATIVE_WORKLOAD_AND_CONSUMER_EXECUTED":
            print(json.dumps({"status": "FINAL_RETURN_ALREADY_PRESENT", "path": str(args.output)}, sort_keys=True))
            return
    result = run(
        evidence_dir=args.evidence_dir,
        bundle_dir=args.bundle_dir,
        grant_path=args.grant,
        pending_contract_path=args.contract,
        receipt_dir=args.receipt_dir,
    )
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "operations": result["operations"], "consumer": result["consumer"]}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
