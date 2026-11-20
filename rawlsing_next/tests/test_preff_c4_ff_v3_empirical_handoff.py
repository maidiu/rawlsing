"""C4: ACTUAL one-I03 -> S04/DHIKR -> FF01 -> PRE-V3 sourcefree consumer.

Sourcefree replay/negative court. The other owner remains responsible for
original source, structural relation, actor and independent G5 admission.
"""
from __future__ import annotations

from dataclasses import replace
from json import loads

import pytest

from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash
from rawlsing_next.pre553_s04_cold_custody import SOURCEFREE_ASSERTION
from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest
from rawlsing_next.pre553_s04_field_forge_v3_bridge import (
    EmpiricalSeamError,
    V3SeamEnvelope,
    build_empirical_field_forge_v3_handoff,
    consume_v3_empirical_case_offer,
    write_sourcefree_v3_handoff_private,
    read_sourcefree_v3_handoff_private,
)
from rawlsing_next.tests.test_pre553_s04_observed_research import _real


def _build(tag="PYAT-C4-GENUINE-FF-V3"):
    _, _, _, query, execution = _real(tag=tag)
    return build_empirical_field_forge_v3_handoff(
        query=query,
        execution=execution,
        comparison_request=DHIKRComparisonRequest(
            target_axis=2,
            predictor_axes=(0, 1),
            min_branch_n=2,
            max_depth=2,
            max_nodes=9,
            max_interaction_order=2,
            bootstrap_replicates=24,
        ),
        conditioner_index=0,
        sourcefree_origin_assertion=SOURCEFREE_ASSERTION,
    )


def test_one_real_i03_to_s04_dhikr_to_ff01_to_prev3_whole_joint():
    result = _build()
    bridge = result.envelope.material()
    assert bridge["grade"].startswith("SOURCEFREE_RAW")
    assert bridge["sourcefree_assertion"] == SOURCEFREE_ASSERTION
    assert bridge["ff01_ref"] == result.first_consumer.ff01.ref.as_dict()
    assert bridge["s04_ref"] == result.first_consumer.knowledge.ref.as_dict()
    assert bridge["dhikr_ref"] == result.comparison.ref.as_dict()
    assert bridge["one_pass_ref"] == result.first_consumer.receipt.ref.as_dict()
    assert bridge["execution_count"] == "ONE_ALREADY_EXECUTED_I03__NO_REQUERY"
    assert len(bridge["source_observed_contexts"]) >= 3
    assert bridge["source_observed_contexts"][0]["raw_same_case_n"] == 4
    assert all("observed_research_ref" in item for item in bridge["source_observed_contexts"])
    assert "V3_OR_SOROK_PERSON_OR_RECRUITMENT_AUTHORITY" in bridge["not_issued"]
    offer = consume_v3_empirical_case_offer(
        envelope=result.envelope,
        external_pin=result.external_pin,
        conditions={0: "0"}, seed=12,
    )
    value = offer.material()
    assert value["state"] == "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
    assert value["raw_conditioned_complete_case_n"] == 2
    assert len(value["selected_complete_joint_cell"]) == 3
    assert value["selected_cell_support_raw"] == 1
    chosen = {item["source_dimension"]: item["candidate_state"]
              for item in value["selected_complete_joint_cell"]}
    assert chosen[0] == "0"
    assert int(chosen[2]) == int(chosen[0]) ^ int(chosen[1])
    assert value["sampled_unit"] == "ANONYMOUS_COMPLETE_JOINT_CONFIGURATION_NOT_RESPONDENT"
    assert value["sorok_v3_actor_mutation"] is None
    assert value["structural_relation_admission"] is None
    assert value["source_target_distribution_ref"] is not None
    assert (consume_v3_empirical_case_offer(
        envelope=result.envelope,
        external_pin=result.external_pin,
        conditions={0: "0"}, seed=12,
    ).ref == offer.ref)


def test_cold_replay_requires_independent_pin_and_recovers_same_source_case():
    result = _build("PYAT-C4-COLD")
    cold = V3SeamEnvelope(result.envelope.payload_json, result.envelope.content_hash)
    offer = consume_v3_empirical_case_offer(
        envelope=cold, external_pin=result.external_pin,
        conditions={}, seed=4,
    )
    assert offer.material()["raw_conditioned_complete_case_n"] == 4
    assert len(offer.material()["selected_complete_joint_cell"]) == 3
    with pytest.raises(EmpiricalSeamError, match="separately held source pin"):
        consume_v3_empirical_case_offer(
            envelope=cold, external_pin=None, conditions={}, seed=4,
        )
    with pytest.raises(EmpiricalSeamError, match="external/ff01_ref"):
        consume_v3_empirical_case_offer(
            envelope=cold,
            external_pin=replace(
                result.external_pin, ff01_ref=result.external_pin.query_ref,
            ),
            conditions={}, seed=4,
        )


def test_not_outside_source_domain_and_no_independent_marginal_fabrication():
    result = _build("PYAT-C4-DOMAIN")
    with pytest.raises(EmpiricalSeamError, match="outside source-issued domain"):
        consume_v3_empirical_case_offer(
            envelope=result.envelope, external_pin=result.external_pin,
            conditions={0: "NOT_A_VALUE"}, seed=1,
        )
    offer = consume_v3_empirical_case_offer(
        envelope=result.envelope, external_pin=result.external_pin,
        conditions={0: "0", 1: "1"}, seed=7,
    )
    # This source-observed exact combination has n=1. It must NOT
    # expose the complete cell as a hypothetical-person candidate.
    assert offer.material()["raw_conditioned_complete_case_n"] == 1
    # Exact sample support of one case is not a person-generating license.
    # The default min context n=2 forces abstention: no selected source cell.
    assert offer.material()["state"] == "LOW_CONTEXT_SUPPORT__ABSTAIN"
    assert offer.material()["selected_complete_joint_cell"] == []
    assert offer.material()["source_target_distribution_ref"] is None


def test_zero_context_and_minimum_support_are_holds_not_impossible_states():
    result = _build("PYAT-C4-LOW-N")
    offer = consume_v3_empirical_case_offer(
        envelope=result.envelope, external_pin=result.external_pin,
        conditions={0: "1"}, seed=6, min_context_n=3,
    )
    assert offer.material()["state"] == "LOW_CONTEXT_SUPPORT__ABSTAIN"
    assert offer.material()["raw_conditioned_complete_case_n"] == 2
    assert offer.material()["selected_complete_joint_cell"] == []
    zero = consume_v3_empirical_case_offer(
        envelope=result.envelope, external_pin=result.external_pin,
        conditions={0: "0", 1: "0", 2: "1"}, seed=7,
    )
    assert zero.material()["state"] == "ZERO_OBSERVED_CONTEXT__NOT_IMPOSSIBILITY"
    assert zero.material()["raw_conditioned_complete_case_n"] == 0
    assert zero.material()["selected_complete_joint_cell"] == []
    assert zero.material()["source_target_distribution_ref"] is None


def test_rehashed_ff01_body_cannot_pass_exact_external_consumer_pin():
    result = _build("PYAT-C4-FORGED")
    material = result.envelope.material()
    raw = loads(material["ff01_projection_json"])
    raw["complete_cells"][0]["raw_support"] += 1
    material["ff01_projection_json"] = canonical_json(raw)
    forged = V3SeamEnvelope(canonical_json(material), semantic_hash(material))
    with pytest.raises(EmpiricalSeamError):
        consume_v3_empirical_case_offer(
            envelope=forged, external_pin=result.external_pin,
            conditions={}, seed=5,
        )


def test_rehashed_dhikr_context_does_not_survive_actual_ff01_research_crossread():
    result = _build("PYAT-C4-CONTEXT-ATTACK")
    material = result.envelope.material()
    material["source_observed_contexts"][0]["raw_same_case_n"] = 900
    forged = V3SeamEnvelope(canonical_json(material), semantic_hash(material))
    with pytest.raises(EmpiricalSeamError, match="context-observed-n"):
        consume_v3_empirical_case_offer(
            envelope=forged, external_pin=result.external_pin,
            conditions={}, seed=1,
        )


def test_original_source_permission_cannot_be_claimed_from_caller_string():
    _, _, _, query, execution = _real(tag="PYAT-C4-ORIGINAL-DENY")
    with pytest.raises(EmpiricalSeamError, match="ORIGINAL_SOURCE_SEAM_RIGHTS_NOT_ISSUED"):
        build_empirical_field_forge_v3_handoff(
            query=query, execution=execution,
            comparison_request=DHIKRComparisonRequest(
                target_axis=2, predictor_axes=(0, 1),
            ),
            conditioner_index=0,
            sourcefree_origin_assertion="ORIGINAL_SOURCE_AUTHORIZED_BY_ME",
        )


def test_persisted_cold_field_forge_prev3_first_consumer_no_source_requery(
    tmp_path,
):
    result = _build("PYAT-C4-REAL-COLD")
    private = tmp_path / "seam-private"
    private.mkdir(mode=0o700)
    file = write_sourcefree_v3_handoff_private(private, result.envelope)
    assert file.is_file()
    restored = read_sourcefree_v3_handoff_private(
        file, external_pin=result.external_pin,
    )
    assert restored.ref == result.envelope.ref
    assert (consume_v3_empirical_case_offer(
        envelope=restored, external_pin=result.external_pin,
        conditions={1: "1"}, seed=41,
    ).material()["raw_conditioned_complete_case_n"] == 2)
    with pytest.raises(EmpiricalSeamError, match="exists"):
        write_sourcefree_v3_handoff_private(private, result.envelope)
    with pytest.raises(EmpiricalSeamError, match="external source/consumer"):
        read_sourcefree_v3_handoff_private(file, external_pin=None)
    altered = bytearray(file.read_bytes())
    altered[-3] = 33
    file.write_bytes(altered)
    with pytest.raises(EmpiricalSeamError):
        read_sourcefree_v3_handoff_private(
            file, external_pin=result.external_pin,
        )


def test_held_low_n_context_never_publishes_target_research_reference():
    result = _build("REMONT-C4-LOW-N-REF")
    one = consume_v3_empirical_case_offer(
        envelope=result.envelope, external_pin=result.external_pin,
        conditions={0: "0", 1: "0"}, seed=11,
    ).material()
    assert one["raw_conditioned_complete_case_n"] == 1
    assert one["state"] == "LOW_CONTEXT_SUPPORT__ABSTAIN"
    assert one["source_target_distribution_ref"] is None
    assert one["selected_complete_joint_cell"] == []
    valid = consume_v3_empirical_case_offer(
        envelope=result.envelope, external_pin=result.external_pin,
        conditions={0: "0"}, seed=11,
    ).material()
    assert valid["state"] == "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
    assert valid["source_target_distribution_ref"] is not None
