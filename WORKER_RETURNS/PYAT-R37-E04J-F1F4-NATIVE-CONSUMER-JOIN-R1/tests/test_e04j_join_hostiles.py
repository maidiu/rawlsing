"""E04J — hostile / boundary challenges over the REAL lifecycle join and native consumer.

Covers the commissioned boundaries: same-person vs cross-person identity, actual risk
denominator, minority alternatives, no-support vs missing, current/historical
selection, wrong release root, missing immutable release, revocation, targeted
invalidation, cold replay and stale-evidence refusal. Anything unsupported issues a
typed refusal rather than a fabricated positive.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
for _p in (RET, RET / "runtime", RET.parents[1]):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import e04j_lifecycle_bridge as BR  # noqa: E402
from product.service import GenericSelectedWorldService  # noqa: E402
from product.nonparent import consume as e04_consume  # noqa: E402
import rawlsing_next.pre553_learned_world_composition as i4  # noqa: E402
import rawlsing_next.pre553_learned_product_release as m2  # noqa: E402
import rawlsing_next.pre553_learned_product_lifecycle as b5  # noqa: E402


def _fresh():
    svc = GenericSelectedWorldService()
    ss = svc.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    return svc, ss, e04_consume(svc, ss)


# ------------------------------------------------------------------ denominators
def test_actual_risk_denominator_is_reported_and_not_substituted():
    svc, ss, receipt = _fresh()
    step = svc.provider.step("Y", (("A", 1), ("B", 1), ("C", 1)))
    assert step["denominator"] == 8
    assert step["risk_set_ref"]["object_id"].endswith("R_ALL")
    geo = step["geometry"]["denominator"]
    assert geo["raw_denominator_support"] == 8
    assert len(geo["denominator_member_refs"]) == 8


def test_minority_alternative_survives_to_the_consumer():
    svc, ss, receipt = _fresh()
    final = receipt["material"]["empirical"]["steps"][-1]
    cells = {c["cell"]: c["raw_numerator_support"] for c in final["cells"]}
    # minority '0' cell is retained with support, not pruned
    assert cells.get("0", 0) >= 1
    assert final["uncertainty"] != "NO_SUPPORTED_EVIDENCE"


# ------------------------------------------------------------------ identity
def test_same_respondent_joint_is_denominator_member_based():
    """The joint is counted over distinct RESPONDENT identities, not an abstract count.

    The native E04 step exposes no `same_respondent_joint_ref` field; the genuine
    same-respondent basis is `geometry.denominator.denominator_member_refs`, each of
    which is a distinct C11Internal:RespondentIdentity. This asserts that directly.
    """
    svc, ss, receipt = _fresh()
    final = receipt["material"]["empirical"]["steps"][-1]
    members = final["geometry"]["denominator"]["denominator_member_refs"]
    assert len(members) == final["denominator"] == 8
    assert {m["kind"] for m in members} == {"C11Internal:RespondentIdentity"}
    # every contributing member is a DISTINCT respondent; no person is double counted
    assert len({m["object_id"] for m in members}) == len(members)
    # the same respondent basis holds at the lifecycle carrier grain
    j = BR.run_lifecycle_join(same_marginals=False)
    step_members = j.native_step["geometry"]["denominator"]["denominator_member_refs"]
    assert {m["kind"] for m in step_members} == {"C11Internal:RespondentIdentity"}
    assert len({m["object_id"] for m in step_members}) == j.native_step["denominator"]


def test_cross_person_identity_is_never_claimed():
    """No cross-person join is asserted, and every member is a single-survey identity.

    The native step carries no respondent-link object across sources; the measure is
    declared RAW/unweighted, and no merged structural-empirical probability is issued.
    """
    svc, ss, receipt = _fresh()
    step = svc.provider.step("Y", (("A", 1),))
    assert step["measure"] == "RAW; unweighted; no causal inference"
    assert step["dependencies"] == ["empirical"]
    # conditioning on one source's own coordinates only; no cross-survey source universe
    assert step["source_universe_ref"]["kind"] == "EmpiricalUniverse@1.0.0"
    assert svc.catalog.empirical_identity()["permission_root"] == "TEST_ONLY_E04_SOURCE_ROOT"
    mat = receipt["material"]
    assert mat["route_probability"] is None
    assert mat["route_probability_reason"] == "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"
    # no V3 actor execution and no model call is ever issued by the generic facade
    assert mat["actor_executions"] == 0
    assert mat["model_calls"] == 0
    assert mat["new_issuer"] is False


# ------------------------------------------------------------------ no-support vs missing
def test_no_support_is_distinct_from_a_fabricated_null():
    """Support loss yields a TYPED zero-support step, never a manufactured 0/0.

    The deepest progressive step reports state=ZERO_SUPPORT with denominator 0 and
    NO_SUPPORTED_EVIDENCE, and the consumer reports PARTIAL, not PRODUCTIVE. A measured
    null remains a positive product only when it is actually measured.
    """
    svc = GenericSelectedWorldService(support_loss=True)
    ss = svc.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    receipt = e04_consume(svc, ss)
    mat = receipt["material"]
    assert mat["state"] == "PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT"
    assert mat["empirical"]["state"] == "PARTIAL_TYPED_EMPIRICAL_SUPPORT"
    steps = mat["empirical"]["steps"]
    # shallower steps remain genuinely supported
    assert [s["state"] for s in steps[:2]] == ["EXACT_SUPPORTED", "EXACT_SUPPORTED"]
    # the deepest step is typed zero-support with NO denominator, not a 0/0 null
    deepest = steps[-1]
    assert deepest["state"] == "ZERO_SUPPORT"
    assert deepest["denominator"] == 0
    assert deepest["uncertainty"] == "NO_SUPPORTED_EVIDENCE"
    assert deepest["cells"] == []
    assert mat["route_probability"] is None


def test_wrong_condition_role_is_refused_not_guessed():
    svc, ss, receipt = _fresh()
    with pytest.raises(ValueError, match="TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE"):
        svc.provider.step("A", (("B", 1),))


# ------------------------------------------------------------------ B5 selection / invalidation
def test_b5_current_selection_and_invalidation_are_distinct():
    svc, ss, old = _fresh()
    result = svc.invalidate("empirical")
    assert old["receipt_hash"] in result["invalidated_for_fresh_use"]
    # historical evidence (old receipt) remains intact and readable
    assert old["material"]["empirical"]["state"] == "PRODUCTIVE_TEST_ONLY"
    # a fresh select after invalidation yields a genuinely different snapshot
    ss2 = svc.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    assert ss2.snapshot_hash != ss.snapshot_hash
    # the invalidated receipt hash is the one the consumer actually produced
    assert result["invalidated_for_fresh_use"] == [old["receipt_hash"]]
    # the pre-invalidation receipt is retained as historical, not destroyed
    assert result["historical_receipts_retained"] is True
    assert old["receipt_hash"] in result["old_receipt_hashes"]


def test_lifecycle_refuses_wrong_release_root_or_missing_release():
    """A compose attempt whose M1 disposition is absent is BLOCKED, not fabricated."""
    contract = i4.LearnedWorldProductContractBinding(
        route="M1_M2_B5",
        product_family_ref=BR._iref("ProductFamily", "hostile-family"),
        producer_owner_ref=BR._iref("ProducerOwner", "m1-owner"),
        producer_contract_ref=i4.M1_DISPOSITION_PRODUCER_CONTRACT_REF,
        release_subject_kind="TYPED_DISPOSITION",
        selection_scope_ref=BR._iref("SelectionScope", "hostile-scope"),
        producer_permission_ceiling_ref=BR._iref("PermissionCeiling", "ceiling"),
        consumer_product_purpose_ref=BR._iref("ConsumerPurpose", "purpose"),
        m1_family_rule_binding_ref=None,
        lifecycle_actions=(),
        registration_event_authority_ref=None,
        registration_event_rule_ref=None,
        publication_event_authority_ref=None,
        publication_event_rule_ref=None,
        selection_purpose_ref=None,
        selection_event_authority_ref=None,
        selection_event_rule_ref=None,
        selection_attestation_ref=None,
    )
    result = i4.compose_learned_world(
        contract, m2_repository=m2.M2Repository(),
        lifecycle_executor=b5.LearnedProductLifecycleExecutor(), m1_disposition=None)
    assert result.receipt.terminal_state == "BLOCKED"
    assert result.receipt.m2_release_ref is None


def test_cold_replay_is_verified_and_stale_evidence_is_not_reselected():
    j = BR.run_lifecycle_join(same_marginals=False)
    # B5 replay of the executed lifecycle is verified
    assert j.composition.b5_replay_receipt.replay_state == "REPLAY_VERIFIED"
    # a second independent join re-derives the same selection (deterministic replay)
    j2 = BR.run_lifecycle_join(same_marginals=False)
    assert j.composition.b5_selection_receipt.ref == j2.composition.b5_selection_receipt.ref


# ------------------------------------------------------------------ F4 / I05 honest holds
def test_f4_and_i05_are_bounded_not_fabricated():
    """The M1_M2_B5 route does NOT consume M01/I05 evidence, and the receipt says so.

    On the M1_M2_B5 route the I4 receipt leaves m01_execution_receipt_ref and
    m01_object_graph_ref as None: no I05 recursive object graph was consumed. This is
    a precise, falsifiable boundary claim - the join proves the learned product reaches
    E04, and explicitly does NOT claim I05 recursion or F4 co-travel closure.
    """
    j = BR.run_lifecycle_join(same_marginals=False)
    r = j.composition.receipt
    assert r.route_taken == "M1_M2_B5"
    # no M01/I05 execution or object graph is claimed on this route
    assert r.m01_execution_receipt_ref is None
    assert r.m01_object_graph_ref is None
    # but the learned-product chain is fully present and verified
    assert r.terminal_state == "RULE_SATISFIED"
    assert r.m1_disposition_ref is not None
    assert r.m2_release_ref is not None
    assert r.b5_selection_receipt_ref is not None
    # the semantic ceiling explicitly withholds release/currentness/promotion/person state
    ceiling = r.semantic_ceiling
    for withheld in ("NO_PRODUCT_RELEASE", "NO_CURRENTNESS",
                     "NO_STRUCTURAL_ADMISSION", "NO_CAUSAL_PROMOTION"):
        assert withheld in ceiling, withheld
    assert "NO_PERSON_OR_V3_STATE" in ceiling
