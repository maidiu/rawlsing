"""Build Lane C approval/operation evidence from accepted preparation metadata.

No original SAV is statted, opened, decoded or hashed here.  The script reads only
the committed SRC04 source configuration and emits exact contract/ledger material.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, authority_ref, exact_ref, semantic_hash
from rawlsing_next.pre553_observed_response import (
    ObservedResponseContract,
    ObservedResponseTopologyBinding,
)

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.json"
OUT = ROOT / "campaign_src04_completion/empirical"
ORIGINAL_SHA = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
HELD_FIELDS = (
    "q217", "q235", "q236", "q237", "q238", "q239", "q240", "q241", "q242",
    "q243", "q244", "q715withoutmorocco", "q716withoutmorocco",
    "q715incomedeciles", "q716incomedeciles",
)
OPERATION = "PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0"


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_json(value) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_refs(config):
    identity = config["identity"]
    universe_ref = exact_ref(config["questions"][0]["empirical_universe_ref"], "universe_ref")
    source_artifact_ref = ExactRef(
        "SOURCE_ARTIFACT", identity["source_artifact_id"], identity["expected_source_sha256"]
    )
    source_snapshot_ref = exact_ref(
        identity["source_snapshot_retention_ref"], "source_snapshot_ref"
    )
    canonical_sha = sha_json(config)
    source_config_ref = ExactRef(
        "SOURCE_CONFIGURATION",
        "urn:rawlsing:r157:source-configuration:SRC04",
        canonical_sha,
    )
    return universe_ref, source_artifact_ref, source_snapshot_ref, source_config_ref, canonical_sha


def topology_binding(question, response_slot):
    occurrence = response_slot["values"][0]["occurrences"][0]
    return ObservedResponseTopologyBinding(
        target_ref=exact_ref(question["native_question_ref"], "native_question_ref"),
        source_native_topology_ref=exact_ref(occurrence["topology_ref"], "topology_ref"),
        source_native_kind=occurrence["multiplicity_order_rank_fields"]["kind"],
        i03_topology="SCALAR_SINGULAR",
        topology_operation="R157_PREPARE_SOURCE_TOPOLOGY",
        topology_authority_ref=authority_ref(
            question["topology_authority_ref"], "topology_authority_ref"
        ),
        response_semantic_authority_refs=(
            authority_ref(question["semantic_authority_ref"], "semantic_authority_ref"),
        ),
    )


def main() -> None:
    config_bytes = CONFIG_PATH.read_bytes()
    config = json.loads(config_bytes)
    universe_ref, source_artifact_ref, source_snapshot_ref, source_config_ref, canonical_sha = source_refs(config)
    questions = {q["question_id"]: q for q in config["questions"]}
    response_slots = {r["question_id"]: r for r in config["response_slots"]}
    if set(questions) != set(response_slots):
        raise SystemExit("question/response slot identity mismatch")
    if len(questions) != 178 or len(config["coordinate_slots"]) != 3:
        raise SystemExit("unexpected SRC04 configured scope")
    missing_held = set(HELD_FIELDS) - set(questions)
    if missing_held:
        raise SystemExit(f"held fields absent from configuration: {sorted(missing_held)}")
    available_fields = tuple(sorted(set(questions) - set(HELD_FIELDS)))
    if len(available_fields) != 163:
        raise SystemExit("expected 163 available response fields")

    field_ledger = []
    for question_id in sorted(questions):
        question = questions[question_id]
        slot = response_slots[question_id]
        occurrence = slot["values"][0]["occurrences"][0]
        held = question_id in HELD_FIELDS
        field_ledger.append({
            "question_id": question_id,
            "response_slot_ordinal": slot["slot"]["ordinal"],
            "native_question_ref": question["native_question_ref"],
            "source_native_topology_kind": occurrence["multiplicity_order_rank_fields"]["kind"],
            "source_native_topology_ref": occurrence["topology_ref"],
            "status": "HELD_PENDING_BINDING_REPAIR" if held else "AVAILABLE_FOR_OBSERVED_RESPONSE",
            "held_reason": (
                "observed-value binding incomplete per directive section 3; pending Lane B repair"
                if held else None
            ),
            "canonical_values_authorized": False,
            "canonicalization_state": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
        })
    field_status = Counter(item["status"] for item in field_ledger)
    if field_status["AVAILABLE_FOR_OBSERVED_RESPONSE"] != 163 or \
            field_status["HELD_PENDING_BINDING_REPAIR"] != 15:
        raise SystemExit("field ledger status count mismatch")

    coordinate_ledger = []
    for coordinate in config["coordinate_slots"]:
        name = coordinate["slot"]["name"]
        held = name == "q701"
        coordinate_ledger.append({
            "name": name,
            "ordinal": coordinate["slot"]["ordinal"],
            "native_coordinate_ref": coordinate["native_coordinate_ref"],
            "status": (
                "HELD_PENDING_CONTINUOUS_COORDINATE_REPAIR"
                if held else "AVAILABLE_AS_CONDITION_POSITION"
            ),
            "reason": (
                "continuous age coordinate binding incomplete per directive section 3"
                if held else "observed coordinate available for exact condition position"
            ),
        })
    coordinate_status = Counter(item["status"] for item in coordinate_ledger)

    target_refs = tuple(sorted(
        (exact_ref(questions[q]["native_question_ref"], "native_question_ref") for q in available_fields),
        key=lambda ref: ref.key,
    ))
    bindings = tuple(sorted(
        (topology_binding(questions[q], response_slots[q]) for q in available_fields),
        key=lambda binding: binding.target_ref.key,
    ))
    risk_policy = {
        "source_id": "SRC04",
        "operation": OPERATION,
        "target_refs": [ref.as_dict() for ref in target_refs],
        "observed_states": ["DK", "SOURCE_SPECIFIC_SPECIAL", "SUBSTANTIVE_RESPONSE"],
        "missing_states": ["MISSING"],
        "denominator_policies": ["CO_OBSERVED_TARGETS", "PER_TARGET_OBSERVED"],
        "routing_state": "ROUTING_UNKNOWN_NOT_USED",
        "not_eligible_population_estimate": True,
    }
    risk_set_ref = ExactRef(
        "RISK_SET",
        "urn:rawlsing:pre553:observed-response:SRC04:co-observed-cohort",
        sha_json(risk_policy),
    )
    contract = ObservedResponseContract(
        contract_id="PRE553-SRC04-OBSERVED-RESPONSE-APPROVAL-READY",
        contract_version="1.0.0",
        contract_state="APPROVAL_PENDING",
        authority_grade="ORIGINAL_SCIENTIFIC",
        source_id="SRC04",
        source_sha256=ORIGINAL_SHA,
        source_snapshot_ref=source_snapshot_ref,
        source_artifact_ref=source_artifact_ref,
        source_release_manifest_hash=None,
        release_ref=None,
        universe_ref=universe_ref,
        source_config_ref=source_config_ref,
        operation=OPERATION,
        operation_authority_ref=None,
        risk_set_ref=risk_set_ref,
        target_refs=target_refs,
        observed_states=("DK", "SOURCE_SPECIFIC_SPECIAL", "SUBSTANTIVE_RESPONSE"),
        missing_states=("MISSING",),
        denominator_policies=("CO_OBSERVED_TARGETS", "PER_TARGET_OBSERVED"),
        condition_observation_policy="ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
        topology_bindings=bindings,
    )

    n = len(available_fields)
    unordered_pairs = n * (n - 1) // 2
    ordered_pairs = n * (n - 1)
    triples = math.comb(n, 3)
    planned_total = n + ordered_pairs + unordered_pairs + triples
    operation_families = [
        {
            "family": "UNARY_OBSERVED_DISTRIBUTION",
            "operation": "per response field, exact observed-state cell distribution",
            "available_targets": n,
            "held_targets": len(HELD_FIELDS),
            "planned_operations": n,
            "status": "NOT_ISSUED_AUTHORITY_PENDING",
            "denominator_policy": "PER_TARGET_OBSERVED",
            "missingness": "MISSING excluded and counted; DK/special retained as observed typed response states",
        },
        {
            "family": "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
            "operation": "for every ordered pair (target, condition) among available response fields",
            "available_targets": n,
            "ordered_pairs": ordered_pairs,
            "planned_operations": ordered_pairs,
            "status": "NOT_ISSUED_AUTHORITY_PENDING",
            "denominator_policy": "PER_TARGET_OBSERVED_WITH_ALL_CONDITION_VARIABLES_CO_OBSERVED",
            "missingness": "target or any referenced condition variable missing => excluded and counted",
        },
        {
            "family": "SAME_RESPONDENT_JOINT_DISTRIBUTION",
            "operation": "for every unordered pair of available response fields",
            "available_targets": n,
            "unordered_pairs": unordered_pairs,
            "planned_operations": unordered_pairs,
            "status": "NOT_ISSUED_AUTHORITY_PENDING",
            "denominator_policy": "CO_OBSERVED_TARGETS",
            "missingness": "any target missing => excluded from denominator and counted",
        },
        {
            "family": "HIGHER_ORDER_CO_OBSERVED_JOINT",
            "operation": "same-respondent target sets of exact arity 3 over available response fields",
            "max_arity": 3,
            "planned_operations": triples,
            "status": "NOT_ISSUED_AUTHORITY_PENDING",
            "denominator_policy": "CO_OBSERVED_TARGETS",
            "missingness": "any target missing => excluded and counted",
        },
        {
            "family": "MINORITY_ZERO_AND_SPARSE_CELLS",
            "operation": "derived cell states from every issued distribution/joint; no separate query family",
            "observed_zero_policy": "raw numerator == 0 and raw denominator > 0",
            "sparse_policy": "0 < raw numerator <= issuer-approved exact threshold",
            "sparse_threshold": None,
            "status": "DERIVED_AFTER_AUTHORIZED_EXECUTION",
        },
        {
            "family": "RECURSIVE_HIGHER_ORDER_BRANCHING",
            "operation": "recursive target-set growth over the co-observed finite grammar, bounded at arity 3 for this contract",
            "max_arity": 3,
            "base_operations": unordered_pairs,
            "branch_growth_rule": "extend only by exact available field refs not already in target set; no numeric-value crossproduct",
            "status": "NOT_ISSUED_AUTHORITY_PENDING",
        },
    ]
    operation_ledger = {
        "schema": "PYAT_SRC04_OBSERVED_RESPONSE_OPERATION_LEDGER@1.0.0",
        "source_scope": {
            "source_id": "SRC04",
            "source_sha256": ORIGINAL_SHA,
            "source_file_bytes": config["identity"]["source_bytes"],
            "records": config["identity"]["source_row_count"],
            "physical_slots": 181,
            "response_slots": 178,
            "coordinate_slots": 3,
            "available_response_fields": n,
            "held_response_fields": len(HELD_FIELDS),
            "available_condition_coordinates": coordinate_status["AVAILABLE_AS_CONDITION_POSITION"],
            "held_coordinates": coordinate_status["HELD_PENDING_CONTINUOUS_COORDINATE_REPAIR"],
            "field_record_positions": 178 * config["identity"]["source_row_count"],
            "available_response_field_positions": n * config["identity"]["source_row_count"],
            "coordinate_positions": 3 * config["identity"]["source_row_count"],
            "unaccounted_positions": 0,
        },
        "source_config": {
            "path": "rawlsing_next/source_configuration/data/SRC04/source.config.json",
            "file_sha256": sha_bytes(config_bytes),
            "canonical_sha256": canonical_sha,
            "config_id": config["config_id"],
            "config_revision": config["config_revision"],
            "source_snapshot_ref": source_snapshot_ref.as_dict(),
            "source_artifact_ref": source_artifact_ref.as_dict(),
            "universe_ref": universe_ref.as_dict(),
        },
        "field_ledger": field_ledger,
        "available_field_ids": list(available_fields),
        "held_fields": [q for q in HELD_FIELDS],
        "coordinate_ledger": coordinate_ledger,
        "operation_families": operation_families,
        "operation_accounting": {
            "planned_total": planned_total,
            "issued": 0,
            "executed": 0,
            "not_issued_authority_pending": planned_total,
            "held_field_bindings": len(HELD_FIELDS),
            "held_coordinate_bindings": coordinate_status["HELD_PENDING_CONTINUOUS_COORDINATE_REPAIR"],
            "unsupported": 0,
            "inapplicable": 0,
            "unexplained_drops": 0,
            "status": "AUTHORITY_PENDING_NO_ORIGINAL_WORKLOAD_ISSUED",
        },
        "cell_domain_policy": {
            "unary": "exact target domain from the field's source-native observed value/state universe",
            "joint": "exact declared target domains only; no all-numeric-value crossproduct",
            "conditional": "target domain plus exact condition leaves; all referenced response variables co-observed",
            "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
        },
        "routing_policy": {
            "routing_state": "ROUTING_UNKNOWN",
            "used_for_membership": False,
            "eligible_risk_claim": False,
            "population_estimate": False,
        },
        "repair_integration": {
            "current_contract_version": "1.0.0",
            "future_contract_version_on_repair": "2.0.0",
            "held_response_fields": list(HELD_FIELDS),
            "held_coordinate": "q701",
            "rule": "add each repaired field only after its exact source-native observed-value binding and topology decision are accepted",
        },
        "limits": [
            "No operation has been issued or executed against original respondents.",
            "The 42-field D1 aggregate is not an I03 query and is not used as original observed-response issuance.",
            "No canonical values, weights, population/eligibility estimates, structural claims, or actor/V3/V2 state are produced.",
            "The fixture test proves the engineering seam only; it is not an original SRC04 result.",
        ],
    }

    approval = {
        "schema": "PYAT_SRC04_OBSERVED_RESPONSE_APPROVAL_PACKAGE@1.0.0",
        "status": "APPROVAL_READY_EXTERNAL_AUTHORITY_PENDING",
        "contract": contract.as_dict(),
        "contract_ref": contract.ref.as_dict(),
        "contract_material_sha256": contract.content_hash,
        "operation_ledger": "campaign_src04_completion/empirical/OPERATION_LEDGER.json",
        "issuer_boundary": {
            "issuer": "competent external scientific/operation authority under the standing program",
            "lane_c_is_issuer": False,
            "fixture_authority_may_be_used": False,
            "new_authority_created_here": False,
        },
        "required_issuer_fields": [
            "operation_authority_ref: exact ALLOW PREDICATE_GRAMMAR snapshot governing the adopted operation token, source universe, risk-set identity and EmpiricalPredicate/EmpiricalQuerySpec/EmpiricalFact families",
            "release_ref: exact full SRC04 C11LogicalRelease ref from Lane A",
            "source_release_manifest_hash: exact full C11 source release manifest hash",
            "topology_bindings[].topology_authority_ref: exact positive SOURCE_SEMANTICS_TOPOLOGY authority for the source-native-to-I03 topology binding",
            "target_use_ref/target_use_authority_ref/target_use_operation: exact positive TARGET_USE_PERMISSION if an EmpiricalFact is consumed downstream",
        ],
        "minimal_semantic_decision": [
            "Adopt or replace operation token PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0.",
            "Adopt the exact observed states DK, SOURCE_SPECIFIC_SPECIAL, SUBSTANTIVE_RESPONSE and missing state MISSING.",
            "Adopt or replace the proposed source-native SCALAR/ORDINAL_CONTEXT/NOMINAL_CHOICE/BINARY_FACTUAL/BINARY_CONTRAST/RANKED_CHOICE -> SCALAR_SINGULAR topology profile after exact native review.",
            "Adopt PER_TARGET_OBSERVED and CO_OBSERVED_TARGETS denominator policies with all referenced condition variables co-observed.",
            "Approve sparse-cell threshold if a minority/sparse cell claim is required; observed zero itself is exact and needs no threshold.",
        ],
        "release_binding": {
            "status": "REQUIRED_FROM_LANE_A_FULL_RELEASE",
            "accepted_42_field_release_ref": "fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec",
            "accepted_42_field_release_is_sufficient": False,
            "required_release_ref": None,
            "required_source_release_manifest_hash": None,
        },
        "existing_authority_state": {
            "operation_authority": "ABSENT_NOT_FABRICATED",
            "topology_authority": "EXISTING_SRC04_PREPARATION_SNAPSHOT_IS_DEFER",
            "item_semantic_authority": "EXISTING_SRC04_PREPARATION_SNAPSHOT_IS_DEFER",
            "routing_authority": "DEFER_AND_NOT_USED",
            "canonical_mapping_authority": "DEFER_AND_NOT_USED",
        },
        "execution_contract": {
            "public_query_spec": "EmpiricalQuerySpec@1.0.0",
            "public_predicate": "EmpiricalPredicate@1.0.0",
            "public_fact": "EmpiricalFact@1.0.0",
            "risk_set_types": ["OBSERVED_RESPONSE_RISK_SET", "CO_OBSERVED_RESPONSE_RISK_SET"],
            "grain_fields": [
                "query_operation",
                "observed_response_contract_ref",
                "observed_response_contract",
            ],
            "output_family": "EmpiricalFact with target_topology.observed_response ledger",
            "replay": "existing exact query replay; contract ref is in query dependency closure and replay material",
        },
        "negative_boundaries": [
            "fixture-only operation authority cannot authorize ORIGINAL_SCIENTIFIC contract",
            "missing, deferred or mismatched operation authority refuses",
            "release, universe, source artifact or manifest mismatch refuses",
            "routing/applicability condition leaf refuses",
            "weighted observed-response profile refuses",
            "unresolved routing remains refused by existing _risk_membership when eligible-risk profile is used",
        ],
        "limits": [
            "This package does not execute original SRC04 workload.",
            "This package does not read/stat/hash/open/decode the original SAV.",
            "This package does not issue I03 facts or I05 products.",
            "The fixture tests are nonrespondent engineering discrimination only.",
        ],
    }

    write(OUT / "OPERATION_LEDGER.json", operation_ledger)
    write(OUT / "CONTRACT_APPROVAL_READY.json", approval)
    print(json.dumps({
        "contract_ref": contract.ref.as_dict(),
        "targets": len(target_refs),
        "bindings": len(bindings),
        "planned_operations": planned_total,
        "available_fields": n,
        "held_fields": len(HELD_FIELDS),
    }, indent=2))


if __name__ == "__main__":
    main()
