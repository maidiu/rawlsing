from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]

HISTORICAL = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_OBL053_055_SUBJECT_PREDECESSOR_CONSTRUCTION_WAVE_R1/"
    "S1_ONE_OBJECT_SUBJECT_ENTITY_SEMANTIC_AUTHORITY_R1/"
    "01_ONE_OBJECT_SUBJECT_ENTITY_SEMANTIC_AUTHORITY_CANDIDATE.json"
)

REPAIRED = ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_WAVE_R1/"
    "V1_OBL053_HASH_GRAPH_INTEGRITY_REPAIR_R1/"
    "01_REPAIRED_HASH_GRAPH_CANDIDATE.json"
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _sha256_projection(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _replace_exact(value: Any, old: str, new: str) -> Any:
    if isinstance(value, list):
        return [_replace_exact(item, old, new) for item in value]
    if isinstance(value, dict):
        return {
            key: _replace_exact(item, old, new)
            for key, item in value.items()
        }
    return new if value == old else value


def _diff_paths(left: Any, right: Any, prefix: tuple[Any, ...] = ()) -> set[tuple[Any, ...]]:
    if type(left) is not type(right):
        return {prefix}
    if isinstance(left, dict):
        if set(left) != set(right):
            return {prefix + ("<keys>",)}
        out: set[tuple[Any, ...]] = set()
        for key in left:
            out |= _diff_paths(left[key], right[key], prefix + (key,))
        return out
    if isinstance(left, list):
        if len(left) != len(right):
            return {prefix + ("<length>",)}
        out: set[tuple[Any, ...]] = set()
        for index, (a, b) in enumerate(zip(left, right)):
            out |= _diff_paths(a, b, prefix + (index,))
        return out
    return set() if left == right else {prefix}


def _set_path(value: Any, path: Iterable[Any], replacement: Any) -> Any:
    out = deepcopy(value)
    cursor = out
    parts = list(path)
    for part in parts[:-1]:
        cursor = cursor[part]
    cursor[parts[-1]] = replacement
    return out


def _derive_repaired_graph(
    historical: dict[str, Any],
) -> tuple[str, dict[str, Any], str, str, dict[str, Any], str]:
    old_authority_hash = historical["candidate_authority"]["authority_content_hash"]
    old_object_hash = historical["prospective_semantic_object"]["semantic_object_content_hash"]
    old_object_id = historical["prospective_semantic_object"]["semantic_object_id"]

    authority_projection = historical["candidate_authority"]["semantic_projection"]
    corrected_authority_hash = _sha256_projection(authority_projection)

    corrected_object_projection = _replace_exact(
        historical["prospective_semantic_object"]["semantic_projection"],
        old_authority_hash,
        corrected_authority_hash,
    )
    corrected_object_hash = _sha256_projection(corrected_object_projection)
    corrected_object_id = (
        "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:"
        + corrected_object_hash
    )

    corrected_receipt_projection = _replace_exact(
        historical["objective_evidence_receipt"]["semantic_projection"],
        old_authority_hash,
        corrected_authority_hash,
    )
    corrected_receipt_projection = _replace_exact(
        corrected_receipt_projection,
        old_object_hash,
        corrected_object_hash,
    )
    corrected_receipt_projection = _replace_exact(
        corrected_receipt_projection,
        old_object_id,
        corrected_object_id,
    )
    corrected_receipt_hash = _sha256_projection(corrected_receipt_projection)

    return (
        corrected_authority_hash,
        corrected_object_projection,
        corrected_object_hash,
        corrected_object_id,
        corrected_receipt_projection,
        corrected_receipt_hash,
    )


def test_historical_mismatch_state_is_independently_reproduced() -> None:
    historical = _load(HISTORICAL)

    seed = historical["generation_seed"]
    authority = historical["candidate_authority"]
    obj = historical["prospective_semantic_object"]
    receipt = historical["objective_evidence_receipt"]

    assert _sha256_projection(seed["semantic_projection"]) == seed["seed_content_hash"]
    assert (
        _sha256_projection(authority["semantic_projection"])
        != authority["authority_content_hash"]
    )
    assert (
        _sha256_projection(obj["semantic_projection"])
        != obj["semantic_object_content_hash"]
    )
    assert (
        _sha256_projection(receipt["semantic_projection"])
        != receipt["receipt_content_hash"]
    )


def test_independent_derivation_matches_v1_candidate_exactly() -> None:
    historical = _load(HISTORICAL)
    repaired = _load(REPAIRED)

    (
        authority_hash,
        object_projection,
        object_hash,
        object_id,
        receipt_projection,
        receipt_hash,
    ) = _derive_repaired_graph(historical)

    assert repaired["candidate_authority"]["authority_content_hash"] == authority_hash
    assert repaired["prospective_semantic_object"]["semantic_projection"] == object_projection
    assert repaired["prospective_semantic_object"]["semantic_object_content_hash"] == object_hash
    assert repaired["prospective_semantic_object"]["semantic_object_id"] == object_id
    assert repaired["objective_evidence_receipt"]["semantic_projection"] == receipt_projection
    assert repaired["objective_evidence_receipt"]["receipt_content_hash"] == receipt_hash


def test_only_exact_transitive_identity_paths_changed_in_semantic_projections() -> None:
    historical = _load(HISTORICAL)
    repaired = _load(REPAIRED)

    assert (
        repaired["generation_seed"]["semantic_projection"]
        == historical["generation_seed"]["semantic_projection"]
    )
    assert (
        repaired["candidate_authority"]["semantic_projection"]
        == historical["candidate_authority"]["semantic_projection"]
    )

    object_diffs = _diff_paths(
        historical["prospective_semantic_object"]["semantic_projection"],
        repaired["prospective_semantic_object"]["semantic_projection"],
    )
    assert object_diffs == {
        ("semantic_owner_authority", "authority_content_hash"),
        ("provenance_refs", 1, "content_hash"),
    }

    receipt_diffs = _diff_paths(
        historical["objective_evidence_receipt"]["semantic_projection"],
        repaired["objective_evidence_receipt"]["semantic_projection"],
    )
    assert receipt_diffs == {
        ("semantic_object_id",),
        ("semantic_object_content_hash",),
        ("semantic_owner_authority", "authority_content_hash"),
    }


def test_objective_facts_and_semantic_ceilings_are_unchanged() -> None:
    historical = _load(HISTORICAL)
    repaired = _load(REPAIRED)

    old_object = historical["prospective_semantic_object"]["semantic_projection"]
    new_object = repaired["prospective_semantic_object"]["semantic_projection"]

    assert new_object["objective_entity_facts"] == old_object["objective_entity_facts"]
    assert new_object["semantic_ceiling"] == old_object["semantic_ceiling"]
    assert repaired["authority_ceiling"] == historical["authority_ceiling"]

    old_receipt = historical["objective_evidence_receipt"]["semantic_projection"]
    new_receipt = repaired["objective_evidence_receipt"]["semantic_projection"]
    assert new_receipt["objective_entity_facts"] == old_receipt["objective_entity_facts"]
    assert (
        new_receipt["evidence_sufficiency_ceiling"]
        == old_receipt["evidence_sufficiency_ceiling"]
    )


def test_semantic_seed_mutation_cannot_retain_repaired_graph() -> None:
    historical = _load(HISTORICAL)
    repaired = _load(REPAIRED)

    mutated_seed = deepcopy(historical["generation_seed"]["semantic_projection"])
    mutated_seed["objective_entity_fact_seed"]["facility_form"] = "HOSPITAL"
    mutated_seed_hash = _sha256_projection(mutated_seed)

    admitted_seed_hash = repaired["generation_seed"]["seed_content_hash"]
    assert mutated_seed_hash != admitted_seed_hash

    mutated_authority = deepcopy(historical["candidate_authority"]["semantic_projection"])
    mutated_authority["jurisdiction"]["admitted_seed_content_hash"] = mutated_seed_hash
    mutated_authority_hash = _sha256_projection(mutated_authority)
    assert mutated_authority_hash != repaired["candidate_authority"]["authority_content_hash"]

    mutated_object = deepcopy(repaired["prospective_semantic_object"]["semantic_projection"])
    mutated_object["semantic_owner_authority"]["authority_content_hash"] = mutated_authority_hash
    mutated_object["generation_seed"]["seed_content_hash"] = mutated_seed_hash
    mutated_object["provenance_refs"][0]["content_hash"] = mutated_seed_hash
    mutated_object["provenance_refs"][1]["content_hash"] = mutated_authority_hash
    mutated_object["objective_entity_facts"]["facility_form"] = "HOSPITAL"
    assert (
        _sha256_projection(mutated_object)
        != repaired["prospective_semantic_object"]["semantic_object_content_hash"]
    )


def test_each_historical_authority_reversion_breaks_repaired_object_identity() -> None:
    historical = _load(HISTORICAL)
    repaired = _load(REPAIRED)
    old_authority_hash = historical["candidate_authority"]["authority_content_hash"]
    repaired_projection = repaired["prospective_semantic_object"]["semantic_projection"]
    declared_hash = repaired["prospective_semantic_object"]["semantic_object_content_hash"]

    for path in (
        ("semantic_owner_authority", "authority_content_hash"),
        ("provenance_refs", 1, "content_hash"),
    ):
        reverted = _set_path(repaired_projection, path, old_authority_hash)
        assert _sha256_projection(reverted) != declared_hash


def test_each_historical_reversion_breaks_repaired_receipt_identity() -> None:
    historical = _load(HISTORICAL)
    repaired = _load(REPAIRED)

    old_authority_hash = historical["candidate_authority"]["authority_content_hash"]
    old_object_hash = historical["prospective_semantic_object"]["semantic_object_content_hash"]
    old_object_id = historical["prospective_semantic_object"]["semantic_object_id"]

    repaired_projection = repaired["objective_evidence_receipt"]["semantic_projection"]
    declared_hash = repaired["objective_evidence_receipt"]["receipt_content_hash"]

    attacks = (
        (("semantic_owner_authority", "authority_content_hash"), old_authority_hash),
        (("semantic_object_content_hash",), old_object_hash),
        (("semantic_object_id",), old_object_id),
    )
    for path, old_value in attacks:
        reverted = _set_path(repaired_projection, path, old_value)
        assert _sha256_projection(reverted) != declared_hash


def test_one_object_and_nonownership_ceiling_survives_repair() -> None:
    historical = _load(HISTORICAL)
    repaired = _load(REPAIRED)

    # The entire authority semantic projection is unchanged. This is the strongest
    # proof that no new jurisdiction was smuggled in by the identity repair.
    authority = repaired["candidate_authority"]["semantic_projection"]
    assert authority == historical["candidate_authority"]["semantic_projection"]

    jurisdiction = authority["jurisdiction"]
    assert jurisdiction["object_cardinality"] == 1
    assert jurisdiction["additional_seed_hashes"] == "FORBIDDEN"
    assert jurisdiction["additional_objects"] == "FORBIDDEN"
    assert jurisdiction["general_world_object_creation"] == "FORBIDDEN"
    assert jurisdiction["general_facility_ontology"] == "FORBIDDEN"

    semantic_output = authority["semantic_output"]
    assert semantic_output["classifier_proposition_is_not_emitted_by_this_authority"] is True
    assert semantic_output["subject_ref_materialization_is_not_emitted_by_this_authority"] is True

    forbidden = set(authority["forbidden_inference_and_nonownership"])
    assert "NO_ACTOR_CONTACT_USE_ENCOUNTER_EXPOSURE" in forbidden
    assert "NO_COMPARATOR_PSEPF_METABOLISM_CAN008_V2_OR_POSITIVE_V3_AUTHORITY" in forbidden

    assert repaired["prospective_semantic_object"]["current_subject_ref"].startswith("NONE__")


def test_repaired_artifact_is_still_candidate_not_adopted() -> None:
    repaired = _load(REPAIRED)
    assert repaired["status"].startswith("CANDIDATE_NOT_ADOPTED")
    assert "FRESH_HQ_ADOPTION_REQUIRED" in " ".join(repaired["required_next_steps"])
