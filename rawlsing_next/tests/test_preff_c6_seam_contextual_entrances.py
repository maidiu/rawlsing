"""C6: actual PYAT I03->S04/DHIKR->FF01->C4->C5->V3/SEAM-input court.

This is sourcefree historical possibility, not a new V3 actor or survey
partner model. Tests execute real native I03 fixtures via inherited C4/C5.
"""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash
from rawlsing_next.pre553_s04_field_forge_v3_bridge import EmpiricalSeamError
from rawlsing_next.pre553_ff_prev3_possibility_navigation import (
    V3ContextNavigationError, V3ContextPath,
    plan_v3_sourcefree_context_branches,
)
from rawlsing_next.pre553_world_conditioned_progressive_service import (
    consume_world_conditioned_prefixes,
)
from rawlsing_next.pre553_c6_seam_contextual_entrances import (
    ENTRY_PARENT, ENTRY_NADIA, HELD_WORLD_STATE,
    C6SeamError, C6ContextualEntrance, C6IndependentParents,
    assemble_c6_contextual_entrance,
    replay_c6_contextual_entrance,
    assemble_two_sourcefree_parent_entrances,
    as_nonissuing_world_conditioned_prefix,
)
from rawlsing_next.tests.test_preff_c5_continuing_contextual_prev3 import (
    _c4, _path,
)


def _context(tag="PYAT-C6-REPLAY", *, steps=((0, "0"),), seed=19,
             entrance=ENTRY_PARENT, slot="adult-alpha", initial=None, min_cell=2):
    build = _c4(tag)
    path = _path(build, steps, initial=initial, seed=seed)
    packet = assemble_c6_contextual_entrance(
        envelope=build.envelope, external_pin=build.external_pin,
        path=path, entrance=entrance, slot=slot,
        min_disclosure_cell_n=min_cell,
    )
    return build, path, packet


def test_actual_c4_c5_enters_c6_without_second_i03_or_fabricated_actor():
    c4, path, result = _context()
    m = result.material()
    assert m["source_c4_handoff_ref"] == c4.envelope.ref.as_dict()
    assert m["source_c5_path_ref"] == path.ref.as_dict()
    assert m["source_dhikr_ref"] == c4.comparison.ref.as_dict()
    assert m["source_ff01_ref"] == c4.first_consumer.ff01.ref.as_dict()
    assert m["no_additional_i03_queries"] is True
    assert m["no_independent_marginal_sampling"] is True
    assert m["no_partner_coupling_inference"] is True
    assert m["actor_state_transition"] is None
    assert m["world_or_actor_issuer"] is None
    assert "V3_SEAM_ACTOR_STATE_TRANSITION" in m["not_issued"]
    assert len(m["source_observed_future_branches"]) == 2
    assert result.ref == replay_c6_contextual_entrance(
        receipt=result, envelope=c4.envelope,
        external_pin=c4.external_pin, path=path,
    ).ref


def test_singleton_whole_joint_cell_is_not_laundered_from_eligible_context():
    _, path, packet = _context("PYAT-C6-SINGLETON")
    assert path.material()["status"] == "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
    assert path.material()["final_raw_complete_case_n"] == 2
    assert path.material()["final_case_offer_payload"]["selected_cell_support_raw"] == 1
    m = packet.material()
    assert m["whole_case_state"] == "WHOLE_CELL_WITHHELD_OR_NO_SUPPORTED_CONTEXT"
    assert m["hypothetical_joint_configuration"] == []
    assert m["original_selected_cell_n_if_disclosable"] is None
    assert m["conditioned_raw_n_if_disclosable"] == 2
    for axis in m["source_observed_future_branches"]:
        assert all(option["qualified_raw_n"] is None for option in axis["options"])
        assert all(option["person_trait_or_motive"] is None for option in axis["options"])
        assert all(option["population_probability"] is None for option in axis["options"])


def test_low_zero_and_sourcefree_not_issued_are_conserved():
    _, _, low = _context("PYAT-C6-LOW", steps=((0, "0"), (1, "0")))
    lm = low.material()
    assert lm["conditioned_sample_status"] == "LOW_CONTEXT_SUPPORT__ABSTAIN"
    assert lm["hypothetical_joint_configuration"] == []
    assert lm["conditioned_raw_n_if_disclosable"] is None
    _, _, zero = _context("PYAT-C6-ZERO", steps=((2, "1"),),
                          initial={0: "0", 1: "0"})
    zm = zero.material()
    assert zm["conditioned_sample_status"] == "ZERO_OBSERVED_CONTEXT__NOT_IMPOSSIBILITY"
    assert zm["hypothetical_joint_configuration"] == []
    assert zm["conditioned_raw_n_if_disclosable"] is None


def test_nadia_entrance_is_contextual_not_an_adult_determined_at_birth():
    c4, path, packet = _context(
        "PYAT-C6-NADIA", steps=(), initial={1: "1"},
        entrance=ENTRY_NADIA, slot="child-lived-context-t03",
    )
    m = packet.material()
    assert m["entrance"] == ENTRY_NADIA
    assert m["source_states_conditioning"] == path.material()["final_context"]
    assert m["scenario_slot_not_actor_id"] == "child-lived-context-t03"
    assert m["actor_state_transition"] is None
    assert m["world_or_actor_issuer"] is None
    assert replay_c6_contextual_entrance(
        receipt=packet, envelope=c4.envelope,
        external_pin=c4.external_pin, path=path,
    ).ref == packet.ref


def test_two_historical_parent_entrances_never_claim_partner_selection():
    c4 = _c4("PYAT-C6-TWO-PARENTS")
    a_path = _path(c4, [(0, "0")], seed=11)
    b_path = _path(c4, [(1, "1")], seed=13)
    def make(path, slot):
        return assemble_c6_contextual_entrance(
            envelope=c4.envelope, external_pin=c4.external_pin,
            path=path, entrance=ENTRY_PARENT, slot=slot,
        )
    first, second = make(a_path, "adult-one"), make(b_path, "adult-two")
    triplet_a=(c4.envelope,c4.external_pin,a_path)
    triplet_b=(c4.envelope,c4.external_pin,b_path)
    pair = assemble_two_sourcefree_parent_entrances(
        first=first, second=second,
        first_source=triplet_a, second_source=triplet_b,
    )
    m = pair.material()
    assert pair.ref != first.ref and pair.ref != second.ref
    assert m["first_parent_proposal_ref"] == first.ref.as_dict()
    assert m["second_parent_proposal_ref"] == second.ref.as_dict()
    assert m["pairing_state"].endswith("RELATIONSHIP_UNISSUED")
    assert m["partner_selection_evidence"] is None
    assert m["inferred_parental_relationship"] is None
    assert m["no_fabricated_cross_person_correlation"] is True
    assert m["actor_state_transition"] is None
    assert assemble_two_sourcefree_parent_entrances(
        first=first, second=second,
        first_source=triplet_a, second_source=triplet_b,
    ).ref == pair.ref
    with pytest.raises(C6SeamError, match="PARTNER_SELECTION_NOT_ESTABLISHED"):
        assemble_two_sourcefree_parent_entrances(
            first=first, second=second,
            first_source=triplet_a, second_source=triplet_b,
            partner_selection_claim={"statistic": "within-person co-travel"},
        )
    with pytest.raises(C6SeamError, match="slots must differ"):
        assemble_two_sourcefree_parent_entrances(
            first=first, second=first,
            first_source=triplet_a, second_source=triplet_a,
        )


def test_fake_parent_as_nadia_or_person_authority_cannot_be_emitted():
    c4, path, child = _context(
        "PYAT-C6-NO-PAIR-FROM-CHILD", entrance=ENTRY_NADIA,
    )
    with pytest.raises(C6SeamError, match="adult backfill"):
        assemble_two_sourcefree_parent_entrances(
            first=child, second=child,
            first_source=(c4.envelope,c4.external_pin,path),
            second_source=(c4.envelope,c4.external_pin,path),
        )
    with pytest.raises(C6SeamError, match="historical entrance"):
        assemble_c6_contextual_entrance(
            envelope=c4.envelope, external_pin=c4.external_pin, path=path,
            entrance="SOROK_AUTHORIZED_PARENT", slot="nope",
        )
    with pytest.raises(C6SeamError, match="private cell support minimum"):
        assemble_c6_contextual_entrance(
            envelope=c4.envelope, external_pin=c4.external_pin, path=path,
            entrance=ENTRY_PARENT, slot="nope", min_disclosure_cell_n=True,
        )


def test_rehashed_c5_and_c6_forgeries_fail_pinned_replay_and_world():
    c4, path, packet = _context("PYAT-C6-HOSTILE")
    altered = path.material()
    altered["seed"] += 1
    forged_path = V3ContextPath(canonical_json(altered), semantic_hash(altered))
    with pytest.raises(V3ContextNavigationError, match="failed independently pinned replay"):
        assemble_c6_contextual_entrance(
            envelope=c4.envelope, external_pin=c4.external_pin,
            path=forged_path, entrance=ENTRY_PARENT, slot="forged",
        )
    fake = packet.material()
    fake["scenario_slot_not_actor_id"] = "substituted-child"
    forged_packet = C6ContextualEntrance(canonical_json(fake), semantic_hash(fake))
    with pytest.raises(C6SeamError, match="cold source replay failed"):
        replay_c6_contextual_entrance(
            receipt=forged_packet, envelope=c4.envelope,
            external_pin=c4.external_pin, path=path,
        )
    with pytest.raises(C6SeamError, match="cold source replay failed"):
        as_nonissuing_world_conditioned_prefix(
            receipt=forged_packet, envelope=c4.envelope,
            external_pin=c4.external_pin, path=path,
        )
    wrong_pin = replace(c4.external_pin, ff01_ref=c4.external_pin.query_ref)
    with pytest.raises(EmpiricalSeamError, match="external/ff01_ref"):
        as_nonissuing_world_conditioned_prefix(
            receipt=packet, envelope=c4.envelope,
            external_pin=wrong_pin, path=path,
        )


def test_existing_world_first_consumer_gets_held_not_fake_n10e_issuance():
    c4, path, packet = _context("PYAT-C6-WORLD-FIRST")
    prefix = as_nonissuing_world_conditioned_prefix(
        receipt=packet, envelope=c4.envelope,
        external_pin=c4.external_pin, path=path,
    )
    assert prefix.step["state"] == HELD_WORLD_STATE
    assert prefix.step["cells"] == []
    assert prefix.step["denominator"] is None
    assert "WORLD_CAUSAL_RELATION_OR_N10W" in prefix.step["not_issued"]

    class ExistingCatalog:
        def read(self, snapshot, key):
            assert key == "empirical"
            return {"state": "SUPPORTED_TEST_ONLY"}
    actual = consume_world_conditioned_prefixes(
        snapshot=SimpleNamespace(snapshot_hash="C6-TEST-WORLD-SNAPSHOT"),
        catalog=ExistingCatalog(), prefixes=(prefix,),
    )[0]
    native = actual.material()["native_material"]
    assert native["state"] == HELD_WORLD_STATE
    assert native["route_probability"] is None
    assert native["structural_routes"] == {}
    assert actual.native_receipt_hash == ""


def test_native_source_change_prevents_cross_entrance_replay():
    a, path, packet = _context("PYAT-C6-ORIGINAL")
    b = _c4("PYAT-C6-CHANGED-SOURCE")
    assert a.envelope.ref != b.envelope.ref
    with pytest.raises((V3ContextNavigationError, EmpiricalSeamError)):
        replay_c6_contextual_entrance(
            receipt=packet, envelope=b.envelope,
            external_pin=b.external_pin, path=path,
        )


def test_c5_axes_unhashable_input_yields_typed_failure_not_builtin_typeerror():
    c4 = _c4("PYAT-C6-MALFORMED-AXES")
    with pytest.raises(V3ContextNavigationError, match="axis"):
        plan_v3_sourcefree_context_branches(
            envelope=c4.envelope, external_pin=c4.external_pin,
            conditions={}, candidate_axes=([1],),
        )


def test_actual_eight_respondent_full_joint_can_seed_non_singular_v3_proposal():
    """A positive C6 on genuine native I03 facts, not only a safe HOLD demo."""
    from itertools import product
    from rawlsing_next.tests import test_pre553_empirical_query as native
    from rawlsing_next.pre553_s04_cold_custody import SOURCEFREE_ASSERTION
    from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest
    from rawlsing_next.pre553_s04_field_forge_v3_bridge import (
        build_empirical_field_forge_v3_handoff,
    )
    from rawlsing_next.pre553_ff_prev3_possibility_navigation import (
        run_v3_sourcefree_context_path,
    )
    tag = "PYAT-C6-NATIVE-EIGHT-ROW-POSITIVE"
    rows = [
        {"id": f"R{x}{y}{rep}", "responses": {"X": x, "Y": y, "Z": x ^ y}}
        for x, y, rep in product((0, 1), (0, 1), (0, 1))
    ]
    source = native._build_source(
        tag, rows, question_namespace="S04-RESEARCH-QUESTIONS"
    )
    qa = native._query_authority(tag)
    predicate = native._branch_predicate(source, qa, tag="all")
    query = native._query(source, qa, predicate, ("X", "Y", "Z"), tag="query")
    actual = native._run(source, qa, predicate, query)
    assert actual.facts[0].typed_state == "SUPPORTED"
    c4 = build_empirical_field_forge_v3_handoff(
        query=query, execution=actual,
        comparison_request=DHIKRComparisonRequest(
            target_axis=2, predictor_axes=(0, 1),
            min_branch_n=2, max_depth=2, max_nodes=9,
            max_interaction_order=2, bootstrap_replicates=0,
        ),
        conditioner_index=0,
        sourcefree_origin_assertion=SOURCEFREE_ASSERTION,
    )
    path = run_v3_sourcefree_context_path(
        envelope=c4.envelope, external_pin=c4.external_pin,
        starting_conditions={0: "0"}, steps=((1, "1"),), seed=121,
    )
    assert path.material()["final_raw_complete_case_n"] == 2
    packet = assemble_c6_contextual_entrance(
        envelope=c4.envelope, external_pin=c4.external_pin,
        path=path, entrance=ENTRY_PARENT, slot="qualified-sample-parent",
        min_disclosure_cell_n=2,
    )
    m = packet.material()
    assert m["whole_case_state"] == "SOURCEFREE_CELL_PROPOSAL_ONLY__NO_PERSON"
    assert m["original_selected_cell_n_if_disclosable"] == 2
    chosen = {
        x["source_dimension"]: x["candidate_state"]
        for x in m["hypothetical_joint_configuration"]
    }
    assert len(chosen) == 3
    assert chosen == {0: "0", 1: "1", 2: "1"}
    assert packet.ref == replay_c6_contextual_entrance(
        receipt=packet, envelope=c4.envelope,
        external_pin=c4.external_pin, path=path,
    ).ref
    # Even a positive whole joint candidate is not N10W or actor approval.
    prefix = as_nonissuing_world_conditioned_prefix(
        receipt=packet, envelope=c4.envelope,
        external_pin=c4.external_pin, path=path,
    )
    assert prefix.step["state"] == HELD_WORLD_STATE
    assert prefix.step["cells"] == []
