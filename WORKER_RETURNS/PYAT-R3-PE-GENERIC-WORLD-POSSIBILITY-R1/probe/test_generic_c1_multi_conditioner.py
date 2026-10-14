"""P-E stronger C1 multi-condition test-only proof candidates; NOT_EXECUTED.

Uses accepted AT09 source-free four-person XOR ground truth.  No marginal
multiplication or household inference. World known/unknown predicates determine
which independently computed, EXACT same-respondent conditional is consumed.
"""
from dataclasses import replace
import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests import c1_at08_at13_fixture as cfx
from rawlsing_next.tests.test_pre553_empirical_query import (
    _query_authority, _registry,
)
from generic_progressive_possibility import (
    EmpiricalOption, GenericRequest, GenericPossibilityRefusal,
    WorldCondition, WorldFact, WorldSnapshot,
    evaluate_generic_progressive, verify_generic_replay,
)


def ref(name):
    obj = {"fixture": "PE_XOR", "name": name}
    return ExactRef("PE_XOR_TEST_REF", "urn:test:pe:xor:" + name, semantic_hash(obj))


SUBJECT = ref("subject")
GEO = ref("geography")
A_P = ref("A-condition")
B_P = ref("B-condition")
A0 = ref("A0")
B1 = ref("B1")
B_UNKNOWN = ref("B-not-yet-supplied")
A_FACT = ref("A0-world-criterion")
B1_FACT = ref("B1-world-criterion")
B_UNKNOWN_FACT = ref("B-unknown-world-criterion")


def c1_pair():
    source = cfx.xor_fixture(tag="pe-c1-xor")
    qauth = _query_authority("pe-c1-xor")
    registry = _registry(source, qauth)
    single, sq, _, _, _ = cfx.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "A", 0)],
        target_question="C", target_domain=["0", "1"], tag="pe-xor-a0",
    )
    joint, jq, _, _, _ = cfx.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "A", 0), ("RESPONSE", "B", 1)],
        target_question="C", target_domain=["0", "1"], tag="pe-xor-a0b1",
    )
    assert sq.target_ref == jq.target_ref
    assert sq.source_universe_ref == jq.source_universe_ref
    assert sq.release_ref == jq.release_ref
    return (single, sq), (joint, jq)


def opts():
    (single, sq), (joint, jq) = c1_pair()
    primary = WorldCondition("A0-criterion", A_P, A0, A_FACT)
    return (
        EmpiricalOption(
            option_id="A0_SINGLE_CONDITION",
            consumer_query=sq, computed_provider=None,
            computed_c1=single,
            world_conditions=(
                primary,
                WorldCondition("B-status", B_P, B_UNKNOWN, B_UNKNOWN_FACT),
            ),
        ),
        EmpiricalOption(
            option_id="A0_AND_B1",
            consumer_query=jq, computed_provider=None,
            computed_c1=joint,
            world_conditions=(
                primary,
                WorldCondition("B-status", B_P, B1, B1_FACT),
            ),
        ),
    )


def world(known):
    return WorldSnapshot(
        snapshot_ref=ref("world-knows-B1" if known else "world-B-unknown"),
        subject_ref=SUBJECT, geography_ref=GEO,
        as_of_year=2008, publication_year=2007, selection_year=2008,
        currentness_state="CURRENT_AT_SELECTED_AS_OF",
        facts=(
            WorldFact(A_FACT, A_P, A0, 2000, 2015),
            WorldFact(B1_FACT if known else B_UNKNOWN_FACT, B_P,
                      B1 if known else B_UNKNOWN, 2000, 2015),
        ),
    )


def request(known, *, consumer="NONPARENT_SOCIAL_POSSIBILITY"):
    return GenericRequest(
        request_id="PE_XOR_PROGRESSIVE",
        consumer_id=consumer, subject_ref=SUBJECT,
        world=world(known), options=opts(), expected_as_of_year=2008,
    )


@pytest.mark.parametrize("consumer", [
    "CONCEPTION_SCENARIO_CONSUMER__NO_PARENT_INFERENCE",
    "NONPARENT_SOCIAL_OUTREACH_CONSUMER",
])
def test_world_known_second_criterion_changes_actual_c1_denominator(consumer):
    initial = evaluate_generic_progressive(request(False, consumer=consumer))
    later = evaluate_generic_progressive(request(True, consumer=consumer))
    assert initial["status"] == later["status"] == "SELECTED"
    assert initial["selected_option_id"] == "A0_SINGLE_CONDITION"
    assert later["selected_option_id"] == "A0_AND_B1"
    assert initial["selected_computed_empirical_evidence"]["raw_support"] == 2
    assert later["selected_computed_empirical_evidence"]["raw_support"] == 1
    assert initial["selected_computed_empirical_evidence"]["target_ref"] == (
        later["selected_computed_empirical_evidence"]["target_ref"]
    )
    assert len(initial["selected_computed_empirical_evidence"]["conditioner_ids"]) == 1
    assert len(later["selected_computed_empirical_evidence"]["conditioner_ids"]) == 2
    assert initial["progressive_steps"][1]["possible_option_ids"] == [
        "A0_AND_B1", "A0_SINGLE_CONDITION"
    ]
    assert later["progressive_steps"][1]["possible_option_ids"] == [
        "A0_AND_B1", "A0_SINGLE_CONDITION"
    ]
    assert initial["progressive_steps"][2]["possible_option_ids"] == [
        "A0_SINGLE_CONDITION"
    ]
    assert later["progressive_steps"][2]["possible_option_ids"] == [
        "A0_AND_B1"
    ]
    assert initial["all_computed_empirical_evidence"] == later["all_computed_empirical_evidence"]
    assert later["actor_generations"] == 0
    assert verify_generic_replay(later, request(True, consumer=consumer)) == later


def test_xor_conditionals_not_multiplication_of_unary_marginals():
    a = evaluate_generic_progressive(request(False))
    b = evaluate_generic_progressive(request(True))
    a_cells = a["selected_computed_empirical_evidence"]["geometry"]["cells"]
    b_cells = b["selected_computed_empirical_evidence"]["geometry"]["cells"]
    a_counts = {x["cell"]: x["raw_numerator_support"] for x in a_cells}
    b_counts = {x["cell"]: x["raw_numerator_support"] for x in b_cells}
    assert a_counts == {"0": 1, "1": 1}
    assert b_counts == {"0": 0, "1": 1}
    # Frozen XOR original 4 rows: P(C=1|A=0)=1/2 versus
    # P(C=1|A=0,B=1)=1 on exact observed same-respondent fixture.
    assert a["selected_computed_empirical_evidence"]["geometry"]["denominator"][
        "raw_denominator_support"
    ] == 2
    assert b["selected_computed_empirical_evidence"]["geometry"]["denominator"][
        "raw_denominator_support"
    ] == 1


def test_c1_multi_conditional_replay_invalidates_when_world_changes():
    before = evaluate_generic_progressive(request(False))
    with pytest.raises(GenericPossibilityRefusal, match="PROGRESSIVE_REPLAY_MISMATCH"):
        verify_generic_replay(before, request(True))


def test_no_source_or_claim_issuer_created_by_c1_fixture():
    got = evaluate_generic_progressive(request(True))
    assert got["grade"].startswith("TEST_ONLY")
    assert got["selected_computed_empirical_evidence"]["provider_receipt_ref"] is None
    assert got["selected_computed_empirical_evidence"]["producer_route"] == (
        "DIRECT_I03_TO_POSITIONED_SUBJECT"
    )
    assert got["real_world_promotion"] is False
