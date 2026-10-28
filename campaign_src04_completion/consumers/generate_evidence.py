"""Generate lane-D consumer evidence from retained B0 and identity negatives."""
from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable

from rawlsing_next.pre553_empirical_objects import ExactRef

from .b0_native_fixture import B0_FIXTURE_SCOPE, load_b0_native_bundle
from .consumer import (
    ConsumerRefusal,
    b0_fixture_contract,
    consume_native_producer,
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


def _sensitivity_result(product: dict[str, Any]) -> dict[str, Any]:
    discovery = product.get("downstream_discovery") or {}
    return {
        "fact_ref": product["fact_ref"],
        "raw_numerator_support": product["raw_numerator_support"],
        "raw_denominator_support": product["raw_denominator_support"],
        "downstream_value_effect": product["downstream_value_effect"],
        "discovery_supported_candidate_count": discovery.get("supported_candidate_count", 0),
        "discovery_empirical_fact_refs": [
            ref["content_hash"] for ref in discovery.get("empirical_fact_refs", [])
        ],
    }


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

    # Exact native path on the retained B0 fixture.  This executes the fixed
    # consume_native_producer path, a real downstream discovery owner, and the
    # existing effective-N owner.  It is fixture-only engineering evidence.
    native_kwargs = {
        "expected_source_id": "SRC09",
        "requested_claim_ceiling": "SUPPORTED_COMPONENT_ONLY",
        "use_scope": "SUPPORTED_COMPONENT_ONLY",
        "allow_fixture_engineering": True,
    }
    native_original_base = consume_native_producer(
        load_b0_native_bundle(), **native_kwargs
    )
    native_mutated_base = consume_native_producer(
        load_b0_native_bundle(mutate_q101_2_to_1=True), **native_kwargs
    )
    native_restored_base = consume_native_producer(
        load_b0_native_bundle(), **native_kwargs
    )
    original_result = _sensitivity_result(native_original_base)
    mutated_result = _sensitivity_result(native_mutated_base)
    restored_result = _sensitivity_result(native_restored_base)
    changed = (
        original_result["fact_ref"] != mutated_result["fact_ref"]
        and original_result["raw_numerator_support"] != mutated_result["raw_numerator_support"]
        and original_result["raw_denominator_support"] != mutated_result["raw_denominator_support"]
        and original_result["discovery_empirical_fact_refs"]
        != mutated_result["discovery_empirical_fact_refs"]
    )
    restored = restored_result == original_result
    if not changed:
        raise RuntimeError("fixture value mutation did not change the consumed empirical result")
    if not restored:
        raise RuntimeError("fixture value restoration did not reproduce the original consumed result")
    sensitivity = {
        "schema": "PYAT_SRC04_LANE_D_VALUE_SENSITIVITY@1.0.0",
        "status": "MEASURED_FIXTURE_ONLY",
        "scope": "NONRESPONDENT_FIXTURE_ONLY",
        "fixture_scope": B0_FIXTURE_SCOPE,
        "measured": True,
        "changed": changed,
        "restored": restored,
        "upstream_change": (
            "B0 synthetic nonrespondent fixture q101 row-2 raw_value 2.0 -> 1.0; "
            "original fixture SHA "
            f"{native_original_base['source_sha256']} -> {native_mutated_base['source_sha256']}"
        ),
        "original": original_result,
        "mutated": mutated_result,
        "restored_result": restored_result,
        "consumer_owner": "campaign_src04_completion.consumers.consumer.consume_native_producer",
        "downstream_owner": native_original_base["downstream_value_consumer"],
        "actual_api_calls": [
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.pre553_native_workload_binding.build_projection_catalog",
            "rawlsing_next.pre553_empirical_query.execute_empirical_query",
            "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery",
            "rawlsing_next.pre553_effective_n.compute_effective_n",
            "rawlsing_next.objective_consumer_bounded_evidence.evaluate_oc01_pre553_source_local",
        ],
        "fixture_only": True,
        "source_local_claim": False,
        "respondent_cells_emitted": False,
    }
    native_original = consume_native_producer(
        load_b0_native_bundle(),
        **native_kwargs,
        value_sensitivity_evidence=sensitivity,
        value_sensitivity_case="original",
    )
    native_mutated = consume_native_producer(
        load_b0_native_bundle(mutate_q101_2_to_1=True),
        **native_kwargs,
        value_sensitivity_evidence=sensitivity,
        value_sensitivity_case="mutated",
    )
    native_restored = consume_native_producer(
        load_b0_native_bundle(),
        **native_kwargs,
        value_sensitivity_evidence=sensitivity,
        value_sensitivity_case="restored",
    )
    native_original_path = write("B0_NATIVE_ORIGINAL_PRODUCT.json", native_original)
    native_mutated_path = write("B0_NATIVE_MUTATED_PRODUCT.json", native_mutated)
    native_restored_path = write("B0_NATIVE_RESTORED_PRODUCT.json", native_restored)
    sensitivity_path = write("VALUE_SENSITIVITY.json", sensitivity)

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
    negatives["NEGATIVE_NATIVE_FIXTURE_LABEL"] = negative(
        "native_fixture_requires_engineering_label",
        lambda: consume_native_producer(
            load_b0_native_bundle(),
            expected_source_id="SRC09",
            requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
            use_scope="SUPPORTED_COMPONENT_ONLY",
            allow_fixture_engineering=False,
        ),
        identity={"fixture_only": True, "allow_fixture_engineering": False},
    )
    negatives["NEGATIVE_NATIVE_FIXTURE_PROMOTION"] = negative(
        "native_fixture_cannot_claim_source_local",
        lambda: consume_native_producer(
            load_b0_native_bundle(),
            expected_source_id="SRC09",
            requested_claim_ceiling="SOURCE_LOCAL_STATISTIC",
            use_scope="SUPPORTED_COMPONENT_ONLY",
            allow_fixture_engineering=True,
        ),
        identity={
            "fixture_only": True,
            "fixture_claim_ceiling": "SUPPORTED_COMPONENT_ONLY",
            "requested_claim_ceiling": "SOURCE_LOCAL_STATISTIC",
        },
    )
    negatives["NEGATIVE_NATIVE_DOWNSTREAM_MISSING"] = negative(
        "native_fixture_without_value_consumer_is_refused",
        lambda: consume_native_producer(
            replace(load_b0_native_bundle(), discovery=None),
            expected_source_id="SRC09",
            requested_claim_ceiling="SUPPORTED_COMPONENT_ONLY",
            use_scope="SUPPORTED_COMPONENT_ONLY",
            allow_fixture_engineering=True,
        ),
        identity={"fixture_only": True, "downstream_discovery": None},
    )
    for name, document in negatives.items():
        write(f"{name}.json", document)

    prior_blocker = EV / "LANE_D_BLOCKER.json"
    blocker = {
        "schema": "PYAT_SRC04_LANE_D_BLOCKER@1.1.0",
        "status": "BLOCKED_PENDING_FULL_SRC04_SOURCE_PRODUCER",
        "blocker": "FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED",
        "requires": [
            "real original-bound C11LogicalRelease for the full SRC04 source product",
            "exact EmpiricalQuerySpec@1.0.0 and EmpiricalPredicate@1.0.0",
            "exact EmpiricalFact@1.0.0 fact ref from the existing empirical executor",
            "exact source-local ALLOW authority refs and purpose/use scope",
            "a direct value-consuming downstream owner input: exact discovery authority/catalog, "
            "or exact weighted effective-N inputs; a raw ref-only bundle is refused",
            "producer module implementing module:function returning ProducerBundle",
        ],
        "downstream_value_consumer_contract": {
            "accepted_owner_1": "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery",
            "accepted_owner_2": "rawlsing_next.pre553_effective_n.compute_effective_n (SUPPORTED weighted state only)",
            "ref_only_bundle_result": "DOWNSTREAM_VALUE_CONSUMER_REQUIRED",
            "policy_only_result_is_insufficient": True,
        },
        "producer_contract": str(CONTRACT.relative_to(ROOT)),
        "producer_contract_sha256": sha(CONTRACT) if CONTRACT.is_file() else None,
        "prior_blocker": {
            "path": str(prior_blocker.relative_to(ROOT)),
            "sha256": sha(prior_blocker) if prior_blocker.is_file() else None,
        },
        "source_read_performed": False,
        "original_workload_issued": False,
        "no_original_source_access": True,
    }
    blocker_path = write("LANE_D_BLOCKER_V2.json", blocker)

    summary = {
        "schema": "PYAT_SRC04_LANE_D_PRIMARY_CONSUMER_RUN@1.1.0",
        "lane": "D",
        "status": "NATIVE_FIXTURE_VALUE_CONSUMING_POSITIVE__SOURCE_LOCAL_PENDING",
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
        "retained_receipt_product": {
            "path": str(positive_path.relative_to(ROOT)),
            "sha256": sha(positive_path),
            "status": positive["status"],
            "oc01_state": positive["oc01_receipt"]["state"],
            "oc01_claim_ceiling": positive["oc01_receipt"]["requested_claim_ceiling"],
            "fact_ref": positive["fact_ref"],
            "raw_numerator_support": positive["raw_numerator_support"],
            "raw_denominator_support": positive["raw_denominator_support"],
            "source_value_sensitive": False,
            "fixture_only": True,
        },
        "native_fixture_value_consuming_product": {
            "path": str(native_original_path.relative_to(ROOT)),
            "sha256": sha(native_original_path),
            "status": native_original["status"],
            "oc01_state": native_original["oc01_receipt"]["state"],
            "oc01_claim_ceiling": native_original["oc01_receipt"]["requested_claim_ceiling"],
            "fact_ref": native_original["fact_ref"],
            "release_ref": native_original["release_ref"],
            "query_ref": native_original["query_ref"],
            "predicate_ref": native_original["predicate_ref"],
            "raw_numerator_support": native_original["raw_numerator_support"],
            "raw_denominator_support": native_original["raw_denominator_support"],
            "downstream_value_consumer": native_original["downstream_value_consumer"],
            "downstream_value_effect": native_original["downstream_value_effect"],
            "downstream_discovery_state": native_original["downstream_discovery"]["status"],
            "downstream_discovery_supported_candidates": native_original["downstream_discovery"]["supported_candidate_count"],
            "effective_n_state": native_original["effective_n_product"]["typed_state"],
            "source_value_sensitive": native_original["source_value_sensitive"],
            "fixture_value_sensitive": native_original["fixture_value_sensitive"],
            "fixture_only": True,
            "source_local_claim": False,
        },
        "value_sensitivity": {
            "path": str(sensitivity_path.relative_to(ROOT)),
            "sha256": sha(sensitivity_path),
            "status": sensitivity["status"],
            "measured": sensitivity["measured"],
            "changed": sensitivity["changed"],
            "restored": sensitivity["restored"],
            "mutated_product_path": str(native_mutated_path.relative_to(ROOT)),
            "mutated_product_sha256": sha(native_mutated_path),
            "restored_product_path": str(native_restored_path.relative_to(ROOT)),
            "restored_product_sha256": sha(native_restored_path),
            "source_local_claim": False,
        },
        "source_local_blocker": {
            "path": str(blocker_path.relative_to(ROOT)),
            "sha256": sha(blocker_path),
            **blocker,
        },
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
            "rawlsing_next.pre553_empirical_query.execute_empirical_query",
            "rawlsing_next.pre553_empirical_query.replay_empirical_query",
            "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery",
            "rawlsing_next.pre553_effective_n.compute_effective_n",
            "rawlsing_next.objective_consumer_bounded_evidence.evaluate_oc01_pre553_source_local",
        ],
        "source_read_performed": False,
        "original_workload_issued": False,
        "no_original_source_access": True,
        "no_d1_tally_conversion": True,
        "no_ff_v553_adoption": True,
        "limits": [
            "Native product is a nonrespondent/test-only B0 SRC09 fixture; it is not original SRC04 and not source-local proof.",
            "The fixture value mutation is an engineering probe, not a scientific edit or a population claim.",
            "Source-local value-sensitivity proof remains pending the full SRC04 producer and its downstream owner inputs.",
            "No original SRC04 file was stat'ed, hashed, opened or decoded by this lane.",
            "No D1 tally was converted into EmpiricalFact and no FF/V553 semantic adoption was performed.",
        ],
    }
    write("PRIMARY_CONSUMER_RUN_V2.json", summary)
    print(json.dumps({
        "status": summary["status"],
        "native_fixture_product": str(native_original_path),
        "oc01_state": native_original["oc01_receipt"]["state"],
        "downstream_effect": native_original["downstream_value_effect"],
        "fixture_value_sensitive": native_original["fixture_value_sensitive"],
        "source_local_positive": False,
        "blocker": blocker["blocker"],
        "negatives": {k: v["status"] for k, v in negatives.items()},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
