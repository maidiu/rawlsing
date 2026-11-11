#!/usr/bin/env python3
"""Exact F07 second-canary PRE-V3 admission instantiation and M1/V554 replay.

Claim-specific only.  This module consumes the frozen E10 authority and the
D09 evidence/state records already committed in this repository.  It does not
widen GT2, create publication authority, call M3, or create person/actor state.
"""
from __future__ import annotations

from dataclasses import asdict
import copy
import hashlib
import json
from pathlib import Path
import unicodedata
from typing import Any, Mapping

from rawlsing_next.m1_admitted_field_forge_relation_v554_ingress import (
    RELATION_ADMISSION_REF_KIND,
    RELATION_ADMISSION_SCHEMA,
    RELATION_BASIS_KIND,
    RELATION_INFORMATION_LOSS,
    RELATION_M1_CONTRACT_ID,
    RELATION_TEMPORAL_DISPOSITION,
    RelationBasisPreparation,
    RelationPreparationState,
    evaluate_m1_admitted_field_forge_relation_v554,
    make_nonpositive_relation_basis_preparation,
    prepare_admitted_field_forge_relation_basis,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1DecisionState,
    TARGET_USE,
    semantic_hash,
)

F07_RUNTIME_SCHEMA = "PREV3_F07_SECOND_CANARY_ADMISSION_INSTANTIATION@1.0.0"
F07_SNAPSHOT_SCHEMA = "PREV3_F07_SECOND_CANARY_SOURCE_SNAPSHOT@1.0.0"
CLAIM_ID = "FFR2_R5_Q73A_Q86A_EXACT_JOINT_CONDITIONED_DIRECTIONAL_HETEROGENEITY_CANARY@1"
RELATION_FAMILY = "FFR2_R5_Q73A_Q86A_EXACT_REALIZED_SAMPLE_CONDITIONED_DIRECTIONAL_HETEROGENEITY_RELATION@1.0.0"
RELATION_IDENTITY_SHA256 = "1a3b1d28cecdb5b06c7b8ac927848249693324da733d1ee9649a94e50d4322ee"
AUTHORITY_ID = "PREV3_SECOND_CANARY_RELATION_ADMISSION_AUTHORITY"
AUTHORITY_VERSION = "1.0.0"
AUTHORITY_SHA256 = "33c6f8b2e33758ef91d57d3eb3fa8bab7c65dfb7a6498495fb08d5261dc3a5fd"
REPLAY_KEY_SHA256 = "0615a8668d87c5641c8a7bba4b144011d297c653a5369d6db2bd979e824fd19d"
ADMISSION_OWNER = "PREV3_FIELD_FORGE_RELATION_ADMISSION_OWNER"
RELATION_OWNER = "FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER"
ADMISSION_OPERATION = "ADMIT_EXACT_FFR2_R5_Q73A_Q86A_SECOND_CANARY_RELATION_FOR_STRUCTURAL_MEDIATION_INPUT"
SOURCE_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
RISK_SET_ID = "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1"
RISK_SET_ROWS = 19210
RISK_SET_MEMBER_SET_SHA256 = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
PROPOSITION_SHA256 = "13f4c1be9e29f4b26df286d863c5cb07a7e6713e315850f748a1fe33f4c313b0"
COMMON_SEMANTIC_INPUT_SHA256 = "026dcc5a69a546188ea9ea207be50fa46d8be8091369a149dee9465f16c1b254"
SUPPORT_SHA256 = "97200c2dd2a1b8b857e1256210a466a5a3a5b507dfe7d16a7476fa659e37aaaa"
CITC_SHA256 = "7b5156b53818d97add3a1316ab97184d6f10993e0e008bd022ef87320f10529b"
COMPARISON_SHA256 = "3b01550178424191b7f31df672e57ca968629e1e455bd3db9b208ab9d523c437"
ROSTER_ARTIFACT_SHA256 = "1cc810979eb80d52d1e5efcd1a916e309be1b60e8d5cc4eed1575bce30f38814"
BROAD_DELTA = "1308605/25287342"

EXPECTED_TYPED_STATE = {
    "observed_joint_states": 812,
    "support_admitted": 441,
    "zero_denominator_abstentions": 371,
    "directional_persistence": 185,
    "directional_reversal": 130,
    "exact_zero_difference": 126,
}
E10_AUTHORITY_REF = {
    "authority_id": AUTHORITY_ID,
    "authority_version": AUTHORITY_VERSION,
    "authority_content_hash": AUTHORITY_SHA256,
}
E10_RELATION_REF = {
    "kind": "FIELD_FORGE_CLAIM_SPECIFIC_RELATION",
    "object_id": CLAIM_ID,
    "content_hash": RELATION_IDENTITY_SHA256,
}
# M1 receives the exact E10-authorized operation as its bounded rule identity;
# F07 does not mint a second general relation rule.
V554_RULE_REF = {"id": ADMISSION_OPERATION, "version": AUTHORITY_VERSION, "hash": AUTHORITY_SHA256}
FOCAL_PROPOSITION_REF = f"sha256:{PROPOSITION_SHA256}"
GOVERNED_USE_ID = f"{CLAIM_ID}::STRUCTURAL_MEDIATION_INPUT"

SOURCE_RECORD_BLOBS = {
    "e10_authority": "48168c4ed96ab34c906db74cf96054e765f57d7a",
    "e10_replay_ledger": "69719830dbff2f752a373ab961bf6e05d05edd2d",
    "d09_execution_register": "00c458bd60688f7fb46fe11f3f8f7c65e8ef37af",
    "d09_evidence_receipt": "354b849202e0e2350e5ae775b8d87760c0a04092",
    "d09_typed_state_court": "8440e50f70789dc6b50470ca1fc9cf93450eaf7f",
}
_REPO_ROOT = Path(__file__).resolve().parents[1]
_ASTRA = _REPO_ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1"
_E10 = _ASTRA / "HQ_SECOND_WAVE_FANIN_AND_THIRD_WAVE_DISPATCH_R1/THIRD_WAVE_WORKER_RETURNS/E10"
_D09 = _ASTRA / "HQ_FIRST_WAVE_FANIN_AND_SECOND_WAVE_DISPATCH_R1/SECOND_WAVE_WORKER_RETURNS/W2-D09"
SOURCE_RECORD_PATHS = {
    "e10_authority": _E10 / "01_SECOND_CANARY_RELATION_ADMISSION_AUTHORITY.json",
    "e10_replay_ledger": _E10 / "02_PERMISSION_NEGATIVE_STATE_REPLAY_LEDGER.json",
    "d09_execution_register": _D09 / "01_REAL_STRUCTURAL_RELATION_EXECUTION_REGISTER.json",
    "d09_evidence_receipt": _D09 / "02_SELECTED_CANDIDATE_EVIDENCE_RECEIPT.json",
    "d09_typed_state_court": _D09 / "03_TYPED_NEGATIVE_AND_ADMISSION_BLOCKER_COURT.json",
}


class SecondCanaryIntegrity(ValueError):
    pass


def _require(ok: bool, message: str) -> None:
    if not ok:
        raise SecondCanaryIntegrity(message)


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    _require(isinstance(value, dict), f"{path.name} must contain an object")
    return value


def load_current_governed_inputs() -> dict[str, dict[str, Any]]:
    return {name: _load(path) for name, path in SOURCE_RECORD_PATHS.items()}


def _e10_hash(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(unicodedata.normalize("NFC", text).encode("utf-8")).hexdigest()


def _typed_state(ledger: Mapping[str, Any]) -> dict[str, int]:
    typed = ledger["typed_state_preservation"]
    return {
        "observed_joint_states": typed["observed_joint_states"],
        "support_admitted": typed["support_admitted"],
        "zero_denominator_abstentions": typed["zero_denominator_abstentions"]["count"],
        "directional_persistence": typed["directional_persistence"]["count"],
        "directional_reversal": typed["directional_reversal"]["count"],
        "exact_zero_difference": typed["exact_zero_difference"]["count"],
    }


def validate_governed_inputs(inputs: Mapping[str, Mapping[str, Any]]) -> None:
    _require(set(inputs) == set(SOURCE_RECORD_PATHS), "governed input set mismatch")
    authority = inputs["e10_authority"]
    ledger = inputs["e10_replay_ledger"]
    execution = inputs["d09_execution_register"]
    evidence = inputs["d09_evidence_receipt"]
    state = inputs["d09_typed_state_court"]

    _require(authority.get("schema_id") == "PREV3_SECOND_CANARY_RELATION_ADMISSION_AUTHORITY_OBJECT@1.0.0", "E10 authority schema mismatch")
    _require(authority.get("status") == "CURRENT_CLAIM_SPECIFIC_AUTHORITY__ALLOW_EXACT_SECOND_CANARY_TO_STRUCTURAL_MEDIATION_INPUT", "E10 authority not current ALLOW")
    _require(_e10_hash(authority.get("relation_identity_key")) == authority.get("relation_identity_sha256") == RELATION_IDENTITY_SHA256, "E10 relation identity mismatch")
    _require(_e10_hash(authority.get("authority_key")) == authority.get("authority_key_sha256") == AUTHORITY_SHA256, "E10 authority identity mismatch")
    _require(authority.get("relation_ref") == E10_RELATION_REF, "E10 relation ref mismatch")
    _require(authority.get("authority_ref") == E10_AUTHORITY_REF, "E10 authority ref mismatch")

    relation = authority["relation_identity_key"]
    auth = authority["authority_key"]
    _require(relation.get("relation_family") == RELATION_FAMILY, "relation family mismatch")
    _require(relation.get("claim_id") == CLAIM_ID, "claim mismatch")
    _require(relation.get("relation_semantic_owner") == RELATION_OWNER, "relation owner mismatch")
    _require(relation.get("source_sha256") == SOURCE_SHA256, "source hash mismatch")
    _require(relation.get("risk_set") == {"id": RISK_SET_ID, "rows": RISK_SET_ROWS, "member_set_sha256": RISK_SET_MEMBER_SET_SHA256}, "risk-set mismatch")
    participants = relation.get("participants")
    _require(isinstance(participants, list) and len(participants) == 5, "five operands required")
    _require([x.get("ordinal") for x in participants] == [0, 1, 2, 3, 4], "operand order mismatch")
    _require([x.get("source_variable") for x in participants] == ["Q73A", "Q86A", "Q70B", "Q70C", "Q84"], "operand coordinates mismatch")
    _require(relation.get("z_order") == ["Q70B", "Q70C", "Q84"], "Z order mismatch")
    _require(relation.get("frozen_hashes") == {"common_semantic_input": COMMON_SEMANTIC_INPUT_SHA256, "proposition": PROPOSITION_SHA256, "support_uncertainty": SUPPORT_SHA256, "citc": CITC_SHA256, "comparison_claim": COMPARISON_SHA256}, "support identity mismatch")
    _require(relation.get("information_loss") == "NONE__REFERENCE_PRESERVING", "information-loss declaration mismatch")
    _require(auth.get("owner") == ADMISSION_OWNER and auth.get("decision_state") == "ALLOW", "admission owner/decision mismatch")
    _require(auth.get("operation") == ADMISSION_OPERATION, "admission operation mismatch")
    _require(auth.get("relation_ref") == E10_RELATION_REF, "authority relation binding mismatch")
    _require(auth.get("target_use") == TARGET_USE and auth.get("downstream_contract") == RELATION_M1_CONTRACT_ID, "M1 target binding mismatch")
    _require(auth.get("allowed_permission_subset") == [TARGET_USE], "permission ceiling widened")
    condition = auth.get("positive_admission_condition", {})
    _require(condition.get("roster_conservation_required") == "812 == 441 + 371", "roster conservation law mismatch")
    _require(condition.get("admitted_state_partition_required") == "441 == 185 + 130 + 126", "admitted-state partition law mismatch")
    _require(condition.get("no_state_deletion") is True, "no-state-deletion law missing")

    _require(ledger.get("schema_id") == "PREV3_E10_PERMISSION_NEGATIVE_STATE_REPLAY_LEDGER@1.0.0", "E10 replay ledger schema mismatch")
    _require(ledger.get("authority_ref") == E10_AUTHORITY_REF and ledger.get("relation_ref") == E10_RELATION_REF, "E10 replay ledger binding mismatch")
    _require(ledger.get("permission") == {"decision": "ALLOW", "allowed": [TARGET_USE], "downstream_contract": RELATION_M1_CONTRACT_ID, "scope": "EXACT_CURRENT_SECOND_CANARY_INSTANCE_ONLY", "not_generic": True}, "singleton permission mismatch")
    _require(_typed_state(ledger) == EXPECTED_TYPED_STATE, "E10 typed-state roster mismatch")
    _require(ledger["typed_state_preservation"].get("partition_checks") == {"812_eq_441_plus_371": True, "441_eq_185_plus_130_plus_126": True}, "typed-state partition check mismatch")
    _require(_e10_hash(ledger.get("replay_key")) == ledger.get("replay_key_sha256") == REPLAY_KEY_SHA256, "E10 replay identity mismatch")
    replay_terminal = ledger["replay_key"]["replay_proof"]["required_terminal_result"]
    _require(replay_terminal.get("broad_delta") == BROAD_DELTA and replay_terminal.get("broad_sign") == 1, "replay broad result mismatch")
    _require(ledger["replay_key"]["source_execution_artifacts"].get("03_JOINT_STATE_ROSTER_SUPPORT.tsv.gz") == ROSTER_ARTIFACT_SHA256, "full roster artifact mismatch")

    selected = execution.get("selected_candidate", {})
    _require(execution.get("schema_id") == "PREV3_W2_D09_REAL_STRUCTURAL_RELATION_EXECUTION_REGISTER@1.0.0" and selected.get("claim_id") == CLAIM_ID, "D09 execution identity mismatch")
    _require(selected.get("source_sha256") == SOURCE_SHA256 and selected.get("risk_set_member_set_sha256") == RISK_SET_MEMBER_SET_SHA256, "D09 execution source/risk mismatch")
    j = selected.get("joint_roster", {})
    _require({"observed_joint_states": j.get("observed_states"), "support_admitted": j.get("support_admitted"), "zero_denominator_abstentions": j.get("zero_denominator_abstentions"), "directional_persistence": j.get("positive_states"), "directional_reversal": j.get("reversal_states"), "exact_zero_difference": j.get("exact_zero_difference_states")} == EXPECTED_TYPED_STATE, "D09 execution roster mismatch")
    _require(selected.get("broad", {}).get("delta_canonical") == BROAD_DELTA, "D09 broad result mismatch")

    _require(evidence.get("schema_id") == "PREV3_W2_D09_SELECTED_CANDIDATE_EVIDENCE_RECEIPT@1.0.0" and evidence.get("candidate_claim_id") == CLAIM_ID, "D09 evidence identity mismatch")
    _require(evidence.get("source", {}).get("sha256") == SOURCE_SHA256, "D09 evidence source mismatch")
    _require(evidence.get("artifact_sha256", {}).get("03_JOINT_STATE_ROSTER_SUPPORT.tsv.gz") == ROSTER_ARTIFACT_SHA256, "D09 roster evidence mismatch")
    for name, digest in ledger["replay_key"]["source_execution_artifacts"].items():
        _require(evidence.get("artifact_sha256", {}).get(name) == digest, f"D09/E10 artifact mismatch: {name}")

    negatives = state.get("typed_negative_evidence", {})
    _require(state.get("schema_id") == "PREV3_W2_D09_TYPED_NEGATIVE_AND_ADMISSION_BLOCKER_COURT@1.0.0" and state.get("candidate") == CLAIM_ID, "D09 typed-state identity mismatch")
    _require({"observed_joint_states": negatives.get("observed_joint_states"), "support_admitted": negatives.get("support_admitted"), "zero_denominator_abstentions": negatives.get("ABSTAIN__ZERO_DENOMINATOR__DO_NOT_FABRICATE"), "directional_persistence": negatives.get("EXACT_DIRECTIONAL_PERSISTENCE"), "directional_reversal": negatives.get("EXACT_DIRECTIONAL_REVERSAL"), "exact_zero_difference": negatives.get("EXACT_ZERO_DIFFERENCE_IN_REALIZED_SAMPLE")} == EXPECTED_TYPED_STATE, "D09 typed-state roster mismatch")


def build_source_snapshot(inputs: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    validate_governed_inputs(inputs)
    value = {"schema_id": F07_SNAPSHOT_SCHEMA, "source_record_git_blobs": dict(SOURCE_RECORD_BLOBS), "records": {name: copy.deepcopy(inputs[name]) for name in sorted(inputs)}}
    value["snapshot_sha256"] = semantic_hash(value)
    return value


def _receipt_material(inputs: Mapping[str, Mapping[str, Any]], snapshot_sha256: str) -> dict[str, Any]:
    authority = inputs["e10_authority"]
    ledger = inputs["e10_replay_ledger"]
    relation = authority["relation_identity_key"]
    auth = authority["authority_key"]
    current = auth["current_selection"]
    return {
        "schema_id": RELATION_ADMISSION_SCHEMA,
        "field_forge_relation_ref": copy.deepcopy(E10_RELATION_REF),
        "relation_owner_ref_or_id": RELATION_OWNER,
        "relation_rule_ref": {"id": RELATION_FAMILY, "version": "1.0.0", "hash": RELATION_IDENTITY_SHA256},
        "relation_typed_state": "ADMITTED__COMPLETE_812_STATE_ROSTER_PRESERVED",
        "admission_authority_ref": copy.deepcopy(E10_AUTHORITY_REF),
        "admission_rule_ref": copy.deepcopy(E10_AUTHORITY_REF),
        "admission_decision_state": "ADMITTED",
        "target_use_ref": TARGET_USE,
        "requested_downstream_owner_or_contract_family": RELATION_M1_CONTRACT_ID,
        "relation_semantic_identity_refs": [f"relation_family:{RELATION_FAMILY}", f"claim_id:{CLAIM_ID}", f"event_family:{relation['event_family']}", f"relation_identity_sha256:{RELATION_IDENTITY_SHA256}", f"replay_key_sha256:{REPLAY_KEY_SHA256}"],
        "native_scope_identity_refs": [{"source_sha256": SOURCE_SHA256, "risk_set_id": RISK_SET_ID, "risk_set_rows": RISK_SET_ROWS, "risk_set_member_set_sha256": RISK_SET_MEMBER_SET_SHA256}, {"z_order": copy.deepcopy(relation["z_order"])}],
        "source_universe_refs": [{"family": "Afrobarometer", "wave": "R5", "source_path": "Data/Afro Barometer Round 5.sav", "source_sha256": SOURCE_SHA256, "rows": 51587}],
        "risk_set_refs": [{"id": RISK_SET_ID, "rows": RISK_SET_ROWS, "member_set_sha256": RISK_SET_MEMBER_SET_SHA256}],
        "relation_participant_role_order_cardinality_refs": copy.deepcopy(relation["participants"]),
        "target_use_permission_refs": [f"permission:{TARGET_USE}"],
        "effective_time_or_interval_refs_required_by_target_use": [],
        "estimand_refs": [f"estimand:{relation['estimand']}"],
        "measure_and_weight_authority_refs": ["measure:UNWEIGHTED_EXACT_REALIZED_SAMPLE", "weight:NOT_AUTHORIZED"],
        "source_relation_comparability_authority_refs_where_required": [{"source_variable": "Q84", "state_identity_ceiling": "COUNTRY_ALPHA3_QUALIFIED_NATIVE_CATEGORY__NO_CROSS_COUNTRY_EQUIVALENCE"}],
        "applicable_negative_denial_noncomparability_refs": [{"typed_state_preservation": copy.deepcopy(ledger["typed_state_preservation"]), "full_roster_artifact": {"name": "03_JOINT_STATE_ROSTER_SUPPORT.tsv.gz", "sha256": ROSTER_ARTIFACT_SHA256, "observed_states": 812}}],
        "interpretation_critical_authority_refs": [copy.deepcopy(E10_AUTHORITY_REF), {"forbidden_permission_promotions": copy.deepcopy(auth["forbidden_permission_promotions"])}],
        "producer_replay_locator_or_reference_root": {"schema_id": "PREV3_SECOND_CANARY_RELATION_ADMISSION_REPLAY_KEY@1.0.0", "replay_key_sha256": REPLAY_KEY_SHA256, "source_execution_artifacts": copy.deepcopy(ledger["replay_key"]["source_execution_artifacts"]), "proof": copy.deepcopy(ledger["replay_key"]["replay_proof"])},
        "authority_current_selection_dependency_provenance_refs": [f"hq_fanin_commit:{current['hq_fanin_commit']}", f"e10_commission_commit:{current['e10_commission_commit']}", f"d09_return_commit:{current['d09_return_commit']}", f"e10_authority_sha256:{AUTHORITY_SHA256}", f"e10_relation_sha256:{RELATION_IDENTITY_SHA256}", f"e10_replay_key_sha256:{REPLAY_KEY_SHA256}", f"f07_source_snapshot_sha256:{snapshot_sha256}"] + [f"source_record_blob:{name}:{SOURCE_RECORD_BLOBS[name]}" for name in sorted(SOURCE_RECORD_BLOBS)],
        "relation_information_loss_declaration": RELATION_INFORMATION_LOSS,
        "f07_instantiation": {"schema_id": F07_RUNTIME_SCHEMA, "authority_key_sha256": AUTHORITY_SHA256, "relation_identity_sha256": RELATION_IDENTITY_SHA256, "replay_key_sha256": REPLAY_KEY_SHA256, "source_snapshot_sha256": snapshot_sha256, "typed_state_summary": dict(EXPECTED_TYPED_STATE), "permission_ceiling": [TARGET_USE], "publication_authority": "NONE", "m3_promotion": "DENIED", "person_state_promotion": "DENIED", "gt2_rule_reuse": "DENIED"},
    }


def instantiate_second_canary_admission(inputs: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    validate_governed_inputs(inputs)
    snapshot = build_source_snapshot(inputs)
    material = _receipt_material(inputs, snapshot["snapshot_sha256"])
    digest = semantic_hash(material)
    return {**material, "field_forge_relation_admission_id": f"urn:rawlsing:prev3:f07:second-canary-admission:sha256:{digest}", "field_forge_relation_admission_content_hash": digest}


def validate_instantiated_receipt(receipt: Mapping[str, Any], inputs: Mapping[str, Mapping[str, Any]]) -> None:
    expected = instantiate_second_canary_admission(inputs)
    _require(dict(receipt) == expected, "admission receipt differs from exact authorized instance")
    _require(receipt.get("target_use_permission_refs") == [f"permission:{TARGET_USE}"], "receipt permission ceiling widened")
    _require(receipt.get("f07_instantiation", {}).get("typed_state_summary") == EXPECTED_TYPED_STATE, "receipt typed-state roster mismatch")


def _projection(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "relation_admission_ref": {"kind": RELATION_ADMISSION_REF_KIND, "object_id": receipt["field_forge_relation_admission_id"], "content_hash": receipt["field_forge_relation_admission_content_hash"]},
        "relation_admission_authority_ref": copy.deepcopy(receipt["admission_authority_ref"]),
        "relation_admission_rule_ref": copy.deepcopy(receipt["admission_rule_ref"]),
        "relation_admission_decision_state": "ADMITTED",
        "field_forge_relation_ref": copy.deepcopy(receipt["field_forge_relation_ref"]),
        "relation_semantic_identity_refs": copy.deepcopy(receipt["relation_semantic_identity_refs"]),
        "relation_participant_role_order_cardinality_refs": copy.deepcopy(receipt["relation_participant_role_order_cardinality_refs"]),
        "focal_structural_proposition_ref": FOCAL_PROPOSITION_REF,
        "native_scope_identity_refs": copy.deepcopy(receipt["native_scope_identity_refs"]),
        "source_universe_refs": copy.deepcopy(receipt["source_universe_refs"]),
        "risk_set_refs": copy.deepcopy(receipt["risk_set_refs"]),
        "target_use_ref": TARGET_USE,
        "requested_downstream_owner_or_contract_family": RELATION_M1_CONTRACT_ID,
        "target_use_permission_refs": copy.deepcopy(receipt["target_use_permission_refs"]),
        "effective_time_or_interval_refs_required_by_target_use": [],
        "estimand_refs": copy.deepcopy(receipt["estimand_refs"]),
        "measure_and_weight_authority_refs": copy.deepcopy(receipt["measure_and_weight_authority_refs"]),
        "source_relation_comparability_authority_refs_where_required": copy.deepcopy(receipt["source_relation_comparability_authority_refs_where_required"]),
        "applicable_negative_denial_noncomparability_refs": copy.deepcopy(receipt["applicable_negative_denial_noncomparability_refs"]),
        "interpretation_critical_authority_refs": copy.deepcopy(receipt["interpretation_critical_authority_refs"]),
        "producer_replay_locator_or_reference_root": copy.deepcopy(receipt["producer_replay_locator_or_reference_root"]),
        "authority_current_selection_dependency_provenance_refs": copy.deepcopy(receipt["authority_current_selection_dependency_provenance_refs"]),
        "information_loss_declaration": RELATION_INFORMATION_LOSS,
        "temporal_semantic_disposition": RELATION_TEMPORAL_DISPOSITION,
    }


def _equivalence_key(projection: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "focal_structural_proposition_ref": FOCAL_PROPOSITION_REF,
        "target_use": TARGET_USE,
        "v554_rule_id": V554_RULE_REF["id"],
        "v554_rule_version": V554_RULE_REF["version"],
        "v554_rule_hash": V554_RULE_REF["hash"],
        "basis_semantic_class": RELATION_BASIS_KIND,
        "rule_relevant_structural_semantic_identity_fingerprint": semantic_hash(list(projection["relation_semantic_identity_refs"])),
        "relation_participant_role_order_cardinality_fingerprint": semantic_hash(list(projection["relation_participant_role_order_cardinality_refs"])),
        "native_scope_identity_fingerprint": semantic_hash(list(projection["native_scope_identity_refs"])),
        "rule_relevant_effective_time_semantics_fingerprint": semantic_hash({"disposition": RELATION_TEMPORAL_DISPOSITION, "refs": list(projection["effective_time_or_interval_refs_required_by_target_use"])}),
        "originating_admitted_relation_lineage_fingerprint": semantic_hash(projection["relation_admission_ref"]),
        "source_universe_fingerprint": semantic_hash(list(projection["source_universe_refs"])),
        "estimand_fingerprint": semantic_hash(list(projection["estimand_refs"])),
        "measure_and_weight_authority_fingerprint": semantic_hash(list(projection["measure_and_weight_authority_refs"])),
        "rule_relevant_source_relation_comparability_authority_fingerprint": semantic_hash(list(projection["source_relation_comparability_authority_refs_where_required"])),
        "interpretation_critical_semantic_authority_fingerprint": semantic_hash(list(projection["interpretation_critical_authority_refs"])),
    }


def build_m1_preparation_payload(receipt: Mapping[str, Any], inputs: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    validate_instantiated_receipt(receipt, inputs)
    projection = _projection(receipt)
    semantics = {
        "relation_family": RELATION_FAMILY,
        "claim_id": CLAIM_ID,
        "relation_identity_sha256": RELATION_IDENTITY_SHA256,
        "authority_sha256": AUTHORITY_SHA256,
        "replay_key_sha256": REPLAY_KEY_SHA256,
        "participants": copy.deepcopy(inputs["e10_authority"]["relation_identity_key"]["participants"]),
        "z_order": ["Q70B", "Q70C", "Q84"],
        "event_family": "F01__EXACT_NATIVE_SINGLE_STATE_EVENT_CONTRAST",
        "typed_state_preservation": copy.deepcopy(inputs["e10_replay_ledger"]["typed_state_preservation"]),
        "permission_ceiling": [TARGET_USE],
        "broad_delta": BROAD_DELTA,
        "full_roster_artifact_sha256": ROSTER_ARTIFACT_SHA256,
        "information_loss": RELATION_INFORMATION_LOSS,
    }
    return {
        "relation_admission": dict(receipt),
        "basis_ref": {"kind": RELATION_BASIS_KIND, "object_id": receipt["field_forge_relation_admission_id"], "content_hash": receipt["field_forge_relation_admission_content_hash"]},
        "projection": projection,
        "projection_hash": semantic_hash(projection),
        "equivalence_key": _equivalence_key(projection),
        "selected_rule_relevant_basis_semantics": semantics,
        "focal_structural_proposition_ref": FOCAL_PROPOSITION_REF,
    }


def prepare_second_canary_m1(receipt: Mapping[str, Any], inputs: Mapping[str, Mapping[str, Any]]) -> RelationBasisPreparation:
    try:
        payload = build_m1_preparation_payload(receipt, inputs)
    except (SecondCanaryIntegrity, KeyError, TypeError, ValueError) as exc:
        return make_nonpositive_relation_basis_preparation(RelationPreparationState.INTEGRITY_FAILURE, str(exc) or "invalid exact second-canary admission")
    return prepare_admitted_field_forge_relation_basis(payload)


def _authority_bundle(inputs: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    snapshot = build_source_snapshot(inputs)
    return {"f07_runtime_schema": F07_RUNTIME_SCHEMA, "relation_admission_contract": RELATION_ADMISSION_SCHEMA, "m1_contract": RELATION_M1_CONTRACT_ID, "e10_authority_ref": copy.deepcopy(E10_AUTHORITY_REF), "e10_relation_ref": copy.deepcopy(E10_RELATION_REF), "e10_replay_key_sha256": REPLAY_KEY_SHA256, "source_snapshot_sha256": snapshot["snapshot_sha256"], "typed_state_summary": dict(EXPECTED_TYPED_STATE), "full_roster_artifact_sha256": ROSTER_ARTIFACT_SHA256, "permission_ceiling": [TARGET_USE], "publication_authority": None}


def execute_second_canary_m1(receipt: Mapping[str, Any], inputs: Mapping[str, Mapping[str, Any]]):
    preparation = prepare_second_canary_m1(receipt, inputs)
    spine = semantic_hash({"relation_ref": E10_RELATION_REF, "authority_ref": E10_AUTHORITY_REF, "replay_key_sha256": REPLAY_KEY_SHA256, "source_record_git_blobs": SOURCE_RECORD_BLOBS})
    return evaluate_m1_admitted_field_forge_relation_v554(
        governed_use_id=GOVERNED_USE_ID,
        v554_rule_ref=V554_RULE_REF,
        focal_structural_proposition_ref=FOCAL_PROPOSITION_REF,
        preparations=[preparation],
        required_authority_snapshot_refs=[f"authority:{AUTHORITY_SHA256}", f"relation:{RELATION_IDENTITY_SHA256}", f"replay:{REPLAY_KEY_SHA256}", f"roster:{ROSTER_ARTIFACT_SHA256}"],
        authority_bundle_material=_authority_bundle(inputs),
        producer_reference_spine_fingerprint=spine,
        publication_authority=None,
    )


def evaluation_material(value: Any) -> dict[str, Any]:
    material = asdict(value)
    state = material.get("decision_state")
    if hasattr(state, "value"):
        material["decision_state"] = state.value
    return material


def execute_current_second_canary() -> dict[str, Any]:
    inputs = load_current_governed_inputs()
    receipt = instantiate_second_canary_admission(inputs)
    first = execute_second_canary_m1(receipt, inputs)
    second = execute_second_canary_m1(receipt, inputs)
    first_material = evaluation_material(first)
    second_material = evaluation_material(second)
    _require(first_material == second_material, "same-input M1/V554 replay changed output")
    _require(first.decision_state is M1DecisionState.ELIGIBLE, f"M1/V554 ingress not eligible: {first.decision_state}")
    return {"source_snapshot": build_source_snapshot(inputs), "admission_receipt": receipt, "m1_evaluation": first_material, "m1_replay_sha256": semantic_hash(first_material)}
