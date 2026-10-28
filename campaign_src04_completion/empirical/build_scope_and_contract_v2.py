"""Build the Lane C V2 scope ledger and pending approval contract from the
read-only B repaired configuration.  This is metadata construction only; it
performs no original-source I/O and creates no authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, authority_ref, exact_ref
from rawlsing_next.pre553_observed_response import (
    ObservedResponseContract,
    ObservedResponseTopologyBinding,
)
from rawlsing_next.source_configuration.schema import canonical_config_hash

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "campaign_src04_completion/empirical"
SOURCE_SHA = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
B_CONFIG_FILE = "5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5"
B_CONFIG_CANONICAL = "28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d"
B_COMMIT = "da23c65d1e211cb7e8ce416e98757f321b78d25e"
A_COMMIT = "0f731cbda9fb0bc778c015eac50189e868a6d5f1"
INITIAL_HELD = (
    "q217", "q235", "q236", "q237", "q238", "q239", "q240", "q241", "q242",
    "q243", "q244", "q715withoutmorocco", "q716withoutmorocco",
    "q715incomedeciles", "q716incomedeciles",
)
RESIDUAL_HELD = ("q217", "q715withoutmorocco", "q716withoutmorocco")
B_REPAIRED_RESPONSE = tuple(f"q{n}" for n in range(235, 245)) + (
    "q715incomedeciles", "q716incomedeciles",
)
OPERATION = "PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0"


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_json(value) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ref_from_authority(value) -> AuthorityRef:
    return authority_ref(value, "authority_ref")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    path = Path(args.config)
    raw = path.read_bytes()
    config = json.loads(raw)
    if sha_bytes(raw) != B_CONFIG_FILE:
        raise SystemExit(f"B config file SHA mismatch: {sha_bytes(raw)}")
    canonical = canonical_config_hash(config)
    if canonical != B_CONFIG_CANONICAL:
        raise SystemExit(f"B config canonical SHA mismatch: {canonical}")
    questions = {q["question_id"]: q for q in config["questions"]}
    responses = {r["question_id"]: r for r in config["response_slots"]}
    if len(questions) != 178 or len(responses) != 178 or len(config["coordinate_slots"]) != 3:
        raise SystemExit("unexpected B config scope")
    for field in INITIAL_HELD:
        if field not in questions:
            raise SystemExit(f"missing initial held field {field}")
    if set(RESIDUAL_HELD) - set(questions):
        raise SystemExit("residual field absent from B config")

    field_ledger = []
    for qid in sorted(questions):
        q = questions[qid]
        slot = responses[qid]
        if qid in RESIDUAL_HELD:
            status = "HELD_RESIDUAL"
            reason = "B remaining residual; not source-qualified for this contract"
        elif qid in INITIAL_HELD:
            status = "AVAILABLE_B_REPAIRED"
            reason = "B repaired exact field/binding; contract-eligible after full release"
        else:
            status = "AVAILABLE_INITIAL"
            reason = "initial source-qualified field"
        occurrence = slot["values"][0]["occurrences"][0]
        topology_ref = exact_ref(occurrence["topology_ref"], "topology_ref")
        topology_kind = occurrence["multiplicity_order_rank_fields"]["kind"]
        field_ledger.append({
            "question_id": qid,
            "ordinal": slot["slot"]["ordinal"],
            "native_question_ref": q["native_question_ref"],
            "source_native_topology_ref": topology_ref.as_dict(),
            "source_native_topology_kind": topology_kind,
            "i03_topology": "SCALAR_SINGULAR",
            "status": status,
            "reason": reason,
            "analytical_target_eligible": status != "HELD_RESIDUAL",
        })
    available = tuple(item["question_id"] for item in field_ledger if item["analytical_target_eligible"])
    held = tuple(item["question_id"] for item in field_ledger if not item["analytical_target_eligible"])
    if len(available) != 175 or len(held) != 3:
        raise SystemExit(f"unexpected available/held counts {len(available)}/{len(held)}")
    if tuple(sorted(held)) != tuple(sorted(RESIDUAL_HELD)):
        raise SystemExit("held set differs from B residuals")

    coordinate_roles = {
        "country": {
            "status": "SOURCE_CONTEXT_HELD_ROLE",
            "analytical_eligible": False,
            "reason": "coordinate presence does not adopt a demographic/social-position role",
        },
        "ser": {
            "status": "IDENTITY_ONLY",
            "analytical_eligible": False,
            "reason": "respondent serial identity, never an analytical condition",
        },
        "q701": {
            "status": "COORDINATE_REPAIRED_ROLE_NOT_ADOPTED",
            "analytical_eligible": False,
            "reason": "B repaired the coordinate binding, but exact native role/units/contract are not adopted",
        },
    }
    coordinate_ledger = []
    for c in config["coordinate_slots"]:
        name = c["slot"]["name"]
        role = coordinate_roles[name]
        coordinate_ledger.append({
            "name": name,
            "ordinal": c["slot"]["ordinal"],
            "native_coordinate_ref": c["native_coordinate_ref"],
            **role,
        })
    if sum(1 for c in coordinate_ledger if c["analytical_eligible"]) != 0:
        raise SystemExit("coordinate role adoption was fabricated")

    universe_ref = exact_ref(questions[available[0]]["empirical_universe_ref"], "universe_ref")
    identity = config["identity"]
    source_artifact_ref = ExactRef(
        "SOURCE_ARTIFACT", identity["source_artifact_id"], identity["expected_source_sha256"])
    source_snapshot_ref = exact_ref(identity["source_snapshot_retention_ref"], "source_snapshot_ref")
    source_config_ref = ExactRef(
        "SOURCE_CONFIGURATION",
        "urn:rawlsing:r157:source-configuration:SRC04:repaired-v2",
        B_CONFIG_CANONICAL,
    )
    target_refs = tuple(sorted(
        (exact_ref(questions[q]["native_question_ref"], "native_question_ref") for q in available),
        key=lambda ref: ref.key,
    ))
    bindings = []
    for qid in available:
        q = questions[qid]
        slot = responses[qid]
        occurrence = slot["values"][0]["occurrences"][0]
        bindings.append(ObservedResponseTopologyBinding(
            target_ref=exact_ref(q["native_question_ref"], "native_question_ref"),
            source_native_topology_ref=exact_ref(occurrence["topology_ref"], "topology_ref"),
            source_native_kind=occurrence["multiplicity_order_rank_fields"]["kind"],
            i03_topology="SCALAR_SINGULAR",
            topology_operation="R157_PREPARE_SOURCE_TOPOLOGY",
            topology_authority_ref=ref_from_authority(q["topology_authority_ref"]),
            response_semantic_authority_refs=(
                ref_from_authority(q["semantic_authority_ref"]),
            ),
        ))
    bindings = tuple(sorted(bindings, key=lambda item: item.target_ref.key))
    risk_policy = {
        "source_id": "SRC04",
        "operation": OPERATION,
        "target_refs": [ref.as_dict() for ref in target_refs],
        "observed_states": ["DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL", "SUBSTANTIVE_RESPONSE"],
        "missing_states": ["MISSING"],
        "denominator_policies": ["CO_OBSERVED_TARGETS", "PER_TARGET_OBSERVED"],
        "routing_state": "ROUTING_UNKNOWN_NOT_USED",
        "not_eligible_population_estimate": True,
    }
    risk_set_ref = ExactRef(
        "RISK_SET",
        "urn:rawlsing:pre553:observed-response:SRC04:co-observed-cohort:v2",
        sha_json(risk_policy),
    )
    contract = ObservedResponseContract(
        contract_id="PRE553-SRC04-OBSERVED-RESPONSE-APPROVAL-READY-V2",
        contract_version="2.0.0",
        contract_state="APPROVAL_PENDING",
        authority_grade="ORIGINAL_SCIENTIFIC",
        source_id="SRC04",
        source_sha256=SOURCE_SHA,
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
        observed_states=("DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL", "SUBSTANTIVE_RESPONSE"),
        missing_states=("MISSING",),
        denominator_policies=("CO_OBSERVED_TARGETS", "PER_TARGET_OBSERVED"),
        condition_observation_policy="ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
        topology_bindings=bindings,
    )
    policy = {
        "schema": "PYAT_SRC04_NATIVE_WORKLOAD_POLICY@2.0.0",
        "policy_id": "SRC04-OBSERVED-RESPONSE-FINITE-FRONTIER-V2",
        "target_scope": "ALL_175_CURRENTLY_QUALIFIED_B_REPAIRED_RESPONSE_FIELDS",
        "operation_families": ["UNARY_OBSERVED_DISTRIBUTION", "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION", "SAME_RESPONDENT_JOINT_DISTRIBUTION"],
        "max_arity": 2,
        "higher_order_status": "NOT_AUTHORIZED_BY_THIS_CONTRACT",
        "conditional_value_scope": "ALL_OBSERVED_DISTINCT_STATES_VALUES_IN_QUALIFIED_RELEASE",
        "execution_requires_authorized_contract": True,
        "routing_conditions": "NOT_USED_ROUTING_UNKNOWN_PRESERVED",
        "sparse_threshold": None,
    }
    planned_unary = len(available)
    planned_joint = len(available) * (len(available) - 1) // 2
    requested_triples = len(available) * (len(available) - 1) * (len(available) - 2) // 6
    scope = {
        "schema": "PYAT_SRC04_OBSERVED_RESPONSE_SCOPE_LEDGER@2.0.0",
        "source_id": "SRC04",
        "source_sha256": SOURCE_SHA,
        "source_config": {
            "path": "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json",
            "file_sha256": B_CONFIG_FILE,
            "canonical_sha256": B_CONFIG_CANONICAL,
            "pinned_commit": B_COMMIT,
            "a_join_commit": A_COMMIT,
            "read_only_git_input": True,
            "path_present_in_this_branch": False,
            "source_read_performed": False,
        },
        "physical_accounting": {
            "physical_slots": 181,
            "response_slots": 178,
            "coordinate_slots": 3,
            "available_response_fields": len(available),
            "held_response_fields": len(held),
            "b_repaired_response_fields": len(B_REPAIRED_RESPONSE),
            "initial_available_response_fields": len(available) - len(B_REPAIRED_RESPONSE),
            "available_analytical_coordinates": 0,
            "identity_only_coordinates": 1,
            "held_coordinate_roles": 2,
            "all_181_slots_accounted": True,
            "unaccounted_slots": 0,
        },
        "field_ledger": field_ledger,
        "available_field_ids": list(available),
        "held_field_ids": list(held),
        "coordinate_ledger": coordinate_ledger,
        "selection_rule": "all 163 initial qualified fields plus 12 B repaired response fields; 3 B residuals held; no arbitrary 163 ceiling",
        "native_target_refs": [ref.as_dict() for ref in target_refs],
        "contract_ref": contract.ref.as_dict(),
        "contract_material_sha256": contract.content_hash,
        "workload_policy": policy,
        "planning_accounting": {
            "unary_operations": planned_unary,
            "joint_pair_operations": planned_joint,
            "requested_higher_order_triples_not_authorized": requested_triples,
            "conditional_operations": "NOT_COUNTED_UNTIL_QUALIFIED_RELEASE_DISTINCT_VALUES_ARE_CONSTRUCTED",
            "issued": 0,
            "executed": 0,
            "residuals_not_zero": [
                "q217_UNRESOLVED_EXACT_UNLABELED_CODES",
                "q715withoutmorocco_PENDING_OBSERVED_DOMAIN",
                "q716withoutmorocco_PENDING_OBSERVED_DOMAIN",
                "q701_COORDINATE_ROLE_NOT_ADOPTED",
                "country_SOURCE_CONTEXT_ROLE_NOT_ADOPTED",
                "ser_IDENTITY_ONLY",
            ],
        },
    }
    approval = {
        "schema": "PYAT_SRC04_OBSERVED_RESPONSE_APPROVAL_PACKAGE@2.0.0",
        "status": "APPROVAL_READY_EXTERNAL_AUTHORITY_PENDING",
        "contract": contract.as_dict(),
        "contract_ref": contract.ref.as_dict(),
        "scope_ledger": "campaign_src04_completion/empirical/SCOPE_LEDGER_V2.json",
        "workload_policy": policy,
        "issuer_proposition": {
            "method_adopted": "raw observed-response and same-respondent co-observed responses; no eligible-risk or weighted-population interpretation",
            "response_states_included": ["SUBSTANTIVE_RESPONSE", "DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL"],
            "response_states_excluded": ["MISSING"],
            "denominators": ["PER_TARGET_OBSERVED", "CO_OBSERVED_TARGETS"],
            "condition_policy": "ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
            "permitted_source_local_use": "software/source-local observed-response operations over the exact SRC04 release; no cross-source pooling, canonical direction, weight, population, structural or actor claim",
            "new_topology_premise": "one-event source-native SCALAR/ORDINAL_CONTEXT/NOMINAL_CHOICE/BINARY_FACTUAL/BINARY_CONTRAST/RANKED_CHOICE carriers map to existing I03 SCALAR_SINGULAR for this contract; issuer must adopt or correct exact bindings",
            "not_requested_from_human": "individual hashes, 163-equivalent approvals, or per-field equivalent bindings",
        },
        "required_issuer_fields": [
            "exact ALLOW PREDICATE_GRAMMAR operation authority for the adopted operation token, source universe, risk-set ref and EmpiricalPredicate/EmpiricalQuerySpec/EmpiricalFact families",
            "exact full SRC04 C11LogicalRelease ref and source release manifest hash from Lane A",
            "positive SOURCE_SEMANTICS_TOPOLOGY authority for the exact source-native topology bindings",
            "TARGET_USE_PERMISSION only if an EmpiricalFact is consumed downstream",
        ],
        "release_binding": {
            "status": "REQUIRED_FROM_LANE_A_FULL_RELEASE",
            "accepted_42_field_release_ref": "fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec",
            "accepted_42_field_release_is_sufficient": False,
        },
        "authority_state": {
            "operation_authority": "ABSENT_NOT_FABRICATED",
            "topology_authority": "EXISTING_SRC04_PREPARATION_SNAPSHOT_IS_DEFER",
            "item_semantic_authority": "EXISTING_SRC04_PREPARATION_SNAPSHOT_IS_DEFER",
            "canonical_mapping": "DEFER",
            "routing": "ROUTING_UNKNOWN_NOT_USED",
            "weight": "NOT_DECLARED",
        },
        "limits": [
            "Approval package only; no original workload issuance or execution.",
            "No original SAV stat/hash/open/decode/read.",
            "No I03/I05, canonical, weight, population/eligibility, structural or actor claim.",
            "The 3 residual response fields and 3 coordinate roles are not silently converted into analytical features.",
        ],
    }
    write(OUT / "SCOPE_LEDGER_V2.json", scope)
    write(OUT / "CONTRACT_APPROVAL_READY_V2.json", approval)
    print(json.dumps({
        "available": len(available), "held": len(held),
        "contract_ref": contract.ref.as_dict(),
        "unary": planned_unary, "joint": planned_joint,
        "requested_triples_not_authorized": requested_triples,
    }, indent=2))


if __name__ == "__main__":
    main()
