"""Generate lane-D consumer evidence from retained B0 and identity negatives."""
from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from rawlsing_next.pre553_empirical_objects import ExactRef

from .consumer import (
    ConsumerRefusal,
    b0_fixture_contract,
    consume_retained_b0_fixture,
    consume_retained_receipt,
    refuse_d1_tally,
    validate_contract,
)

ROOT = Path(__file__).resolve().parents[2]
LANE = Path(__file__).resolve().parent
EV = LANE / "evidence"
B0 = EV / "B0_FIXTURE_POSITIVE.json"
D1_REF = EV / "D1_TALLY_REF.json"
CONTRACT = LANE / "PRODUCER_CONTRACT.json"


def write(name: str, document: Any) -> Path:
    path = EV / name
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def negative(label: str, fn: Callable[[], Any], *, identity: dict[str, Any]) -> dict[str, Any]:
    try:
        fn()
    except ConsumerRefusal as exc:
        return {
            "schema": "PYAT_SRC04_LANE_D_NEGATIVE@1.0.0",
            "negative_id": label,
            "status": "REFUSED",
            "error_type": type(exc).__name__,
            "error_code": exc.code,
            "detail": exc.detail,
            **identity,
            "source_read_performed": False,
            "original_workload_issued": False,
            "consumer_success_claimed": False,
        }
    except Exception as exc:  # noqa: BLE001 - record actual unexpected error
        return {
            "schema": "PYAT_SRC04_LANE_D_NEGATIVE@1.0.0",
            "negative_id": label,
            "status": "FAIL_UNEXPECTED_EXCEPTION",
            "error_type": type(exc).__name__,
            "detail": str(exc),
            **identity,
            "source_read_performed": False,
            "original_workload_issued": False,
            "consumer_success_claimed": False,
        }
    return {
        "schema": "PYAT_SRC04_LANE_D_NEGATIVE@1.0.0",
        "negative_id": label,
        "status": "FAIL_UNEXPECTED_SUCCESS",
        **identity,
        "source_read_performed": False,
        "original_workload_issued": False,
        "consumer_success_claimed": False,
    }


def main() -> int:
    receipt = json.loads(B0.read_text(encoding="utf-8"))
    contract = b0_fixture_contract(receipt)

    positive = consume_retained_b0_fixture(B0)
    positive_path = write("B0_FIXTURE_CONSUMER_PRODUCT.json", positive)

    negatives = {}
    negatives["NEGATIVE_WRONG_SOURCE"] = negative(
        "wrong_source",
        lambda: consume_retained_b0_fixture(B0, expected_source_id="SRC04"),
        identity={"expected_source_id": "SRC09", "supplied_source_id": "SRC04"},
    )
    wrong_release = replace(
        contract,
        release_ref=ExactRef("C11LogicalRelease", contract.release_ref.object_id, "0" * 64),
    )
    negatives["NEGATIVE_WRONG_RELEASE"] = negative(
        "wrong_release",
        lambda: consume_retained_receipt(receipt, wrong_release),
        identity={"expected_release": contract.release_ref.as_dict(), "supplied_release": wrong_release.release_ref.as_dict()},
    )
    wrong_fact = replace(
        contract,
        fact_ref=ExactRef("EmpiricalFact@1.0.0", contract.fact_ref.object_id, "1" * 64),
    )
    negatives["NEGATIVE_WRONG_FACT"] = negative(
        "wrong_fact",
        lambda: consume_retained_receipt(receipt, wrong_fact),
        identity={"expected_fact": contract.fact_ref.as_dict(), "supplied_fact": wrong_fact.fact_ref.as_dict()},
    )
    negatives["NEGATIVE_WRONG_USE"] = negative(
        "wrong_use_scope",
        lambda: consume_retained_b0_fixture(B0, use_scope="SOURCE_LOCAL_STATISTIC"),
        identity={"allowed_use_scope": "SUPPORTED_COMPONENT_ONLY", "supplied_use_scope": "SOURCE_LOCAL_STATISTIC"},
    )
    missing_authority = replace(contract, policy_authority_refs=())
    negatives["NEGATIVE_MISSING_AUTHORITY"] = negative(
        "missing_authority",
        lambda: consume_retained_receipt(receipt, missing_authority),
        identity={"authority_refs": []},
    )
    negatives["NEGATIVE_CLAIM_CEILING"] = negative(
        "fixture_cannot_claim_source_local",
        lambda: consume_retained_b0_fixture(B0, requested_claim_ceiling="SOURCE_LOCAL_STATISTIC"),
        identity={"fixture_evidence_tier": "PARTIAL_AUTHORITY", "requested_claim_ceiling": "SOURCE_LOCAL_STATISTIC"},
    )
    fixture_as_source = replace(
        contract,
        fixture_only=False,
        evidence_tier="SOURCE_LOCAL_CERTIFIED",
        claim_ceiling="SOURCE_LOCAL_STATISTIC",
        use_scopes=("SOURCE_LOCAL_STATISTIC",),
    )
    negatives["NEGATIVE_FIXTURE_AS_SOURCE_LOCAL"] = negative(
        "fixture_contract_cannot_become_source_local",
        lambda: validate_contract(
            fixture_as_source,
            expected_source_id="SRC09",
            requested_claim_ceiling="SOURCE_LOCAL_STATISTIC",
            use_scope="SOURCE_LOCAL_STATISTIC",
        ),
        identity={"fixture_only": True, "attempted_evidence_tier": "SOURCE_LOCAL_CERTIFIED"},
    )
    negatives["NEGATIVE_D1_TALLY"] = refuse_d1_tally(D1_REF)
    for name, document in negatives.items():
        write(f"{name}.json", document)

    blocker = {
        "schema": "PYAT_SRC04_LANE_D_BLOCKER@1.0.0",
        "status": "BLOCKED_PENDING_FULL_SRC04_SOURCE_PRODUCER",
        "blocker": "FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED",
        "requires": [
            "real original-bound C11LogicalRelease for the full SRC04 source product",
            "exact EmpiricalQuerySpec@1.0.0 and EmpiricalPredicate@1.0.0",
            "exact EmpiricalFact@1.0.0 fact ref from the existing empirical executor",
            "exact source-local ALLOW authority refs and purpose/use scope",
            "producer module implementing module:function returning ProducerBundle",
        ],
        "producer_contract": str(CONTRACT.relative_to(ROOT)),
        "producer_contract_sha256": sha(CONTRACT) if CONTRACT.is_file() else None,
        "source_read_performed": False,
        "original_workload_issued": False,
        "no_original_source_access": True,
    }
    write("LANE_D_BLOCKER.json", blocker)

    summary = {
        "schema": "PYAT_SRC04_LANE_D_PRIMARY_CONSUMER_RUN@1.0.0",
        "lane": "D",
        "status": "CONSUMER_CODE_EXECUTED__FIXTURE_ONLY_POSITIVE__SOURCE_LOCAL_PENDING",
        "source_local_positive": False,
        "fixture_only_positive": True,
        "b0_negative_evidence": "RETAINED_B0_ENGINEERING_ONLY",
        "b0_receipt": {
            "path": str(B0.relative_to(ROOT)),
            "sha256": sha(B0),
            "scope": receipt.get("scope"),
            "product_positive": receipt.get("product_positive"),
            "test_only_query_authority_used": receipt.get("test_only_query_authority_used"),
            "original_source_or_release_read": receipt.get("original_source_or_release_read"),
        },
        "b0_consumer_product": {
            "path": str(positive_path.relative_to(ROOT)),
            "sha256": sha(positive_path),
            "status": positive["status"],
            "oc01_state": positive["oc01_receipt"]["state"],
            "oc01_claim_ceiling": positive["oc01_receipt"]["requested_claim_ceiling"],
            "fact_ref": positive["fact_ref"],
            "release_ref": positive["release_ref"],
            "query_ref": positive["query_ref"],
            "predicate_ref": positive["predicate_ref"],
            "numerator": positive["raw_numerator_support"],
            "denominator": positive["raw_denominator_support"],
            "source_value_sensitive": False,
            "fixture_only": True,
        },
        "source_local_blocker": blocker,
        "negative_results": {
            name: {
                "status": document["status"],
                "error_code": document.get("error_code"),
                "path": str((EV / f"{name}.json").relative_to(ROOT)),
                "sha256": sha(EV / f"{name}.json"),
            }
            for name, document in negatives.items()
        },
        "actual_existing_api_calls_in_b0_evidence": receipt.get("actual_existing_api_calls"),
        "lane_actual_api_calls": [
            "rawlsing_next.objective_consumer_bounded_evidence.evaluate_oc01_pre553_source_local",
        ],
        "source_read_performed": False,
        "original_workload_issued": False,
        "no_original_source_access": True,
        "no_d1_tally_conversion": True,
        "no_ff_v553_adoption": True,
        "limits": [
            "B0 fixture consumer positive is nonrespondent/test-only engineering evidence; it is not an SRC04 source-local product.",
            "Source-value-sensitive original consumer proof remains pending the full SRC04 producer contract.",
            "No original SRC04 file was stat'ed, hashed, opened or decoded by this lane.",
            "No D1 tally was converted into EmpiricalFact and no FF/V553 semantic adoption was performed.",
        ],
    }
    write("PRIMARY_CONSUMER_RUN.json", summary)
    print(json.dumps({
        "status": summary["status"],
        "b0_product": str(positive_path),
        "oc01_state": positive["oc01_receipt"]["state"],
        "source_local_positive": False,
        "blocker": blocker["blocker"],
        "negatives": {k: v["status"] for k, v in negatives.items()},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
