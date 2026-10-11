"""HQ280 F8F — independent injected owner-level hostiles (reviewer-authored).

Every test below invokes a real accepted owner or the candidate owner with an
ADVERSARIALLY MUTATED input and records the actual typed outcome. Static
inspections are deliberately NOT placed here.
"""
from dataclasses import replace

import pytest

from rawlsing_next import pre553_c1_immutable_release_binding as CAND
from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests import c1_at08_at13_fixture as FX
from rawlsing_next.tests import (
    test_pre553_ee14_c1_owner_authenticated_ingress_hq262 as G1,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _query_authority, _registry,
)


@pytest.fixture(scope="module")
def actual():
    source = FX.xor_fixture()
    qauth = _query_authority("c1-at09-xor")
    registry = _registry(source, qauth)
    plans = G1._plans(source)
    out = {}
    for cell in ("q1", "q2"):
        plan = plans[cell]
        composition, consumer_query = G1._compose(
            source=source, qauth=qauth, registry=registry,
            conditions=plan.conditions, target_question=plan.target_question,
            tag=plan.tag,
        )
        out[cell] = (composition, plan.model_rule)
    return source, out


def build(actual, cell="q1", **overrides):
    source, products = actual
    composition, model_rule = products[cell]
    args = {"cell": cell, "composition": composition, "model_rule": model_rule,
            "source_release_ref": source["release_ref"]}
    args.update(overrides)
    return CAND.build_source_free_c1_release(**args)


# ---------------------------------------------------------------- K1 order invariance
def test_k1_affected_set_is_order_invariant(actual):
    view = build(actual)
    model = actual[1]["q1"][1]
    refs = [model.model_authority_ref, model.walkback_authority_ref]
    a = {r.key for r in view.analytical_graph.affected(refs)}
    b = {r.key for r in view.analytical_graph.affected(list(reversed(refs)))}
    assert a == b, "affected() must be order invariant"
    assert view.subject.ref.key in a


# ---------------------------------------------------------- K2 subset mutation of graph
def test_k2_subset_mutation_changes_affected_set_exactly(actual):
    view = build(actual)
    model = actual[1]["q1"][1]
    full = {r.key for r in view.analytical_graph.affected([model.model_authority_ref])}
    assert view.subject.ref.key in full
    # subset mutation: a graph built WITHOUT the model authority edge
    reg = view.analytical_registration
    omit = [(model.model_authority_ref, reg.product_ref)]
    mutated = view.analytical_registry.build_graph(omit_authority_edges=omit)
    mutated_affected = {r.key for r in mutated.affected([model.model_authority_ref])}
    assert reg.product_ref.key not in mutated_affected or mutated_affected != full, \
        "omitting the authority edge must change propagation"
    # the unrelated-authority negative control
    unrelated = replace(model.model_authority_ref, authority_id="urn:reviewer:unrelated")
    assert view.subject.ref.key not in {
        r.key for r in view.analytical_graph.affected([unrelated])}


# ------------------------------------------------- K3 graph edge completeness / no extras
def test_k3_every_determinant_is_an_edge_and_no_unsupported_edge(actual):
    view = build(actual)
    dets = {r.key for r in view.analytical_registration.determinant_exact_refs}
    parents = {p.key for p, _ in view.analytical_graph.dependency_edges}
    children = {c.key for _, c in view.analytical_graph.dependency_edges}
    assert dets <= parents, "every determinant must be an edge parent"
    assert children == {view.analytical_registration.product_ref.key}, \
        "every dependency edge must terminate at this product (no unsupported edge)"
    assert len(view.analytical_graph.dependency_edges) >= len(dets)


# --------------------------------------------------- K4 B5 caller-supplied trust boundary
def test_k4_b5_caller_supplied_spoofed_replay_state(actual):
    """Adversarial: a caller-built subject claiming REPLAY_COMPLETE.

    Records the ACTUAL owner outcome rather than asserting a refusal.
    """
    view = build(actual)
    ea = ExactRef("EventAuthority", "urn:reviewer:ea", semantic_hash({"ea": 1}))
    er = ExactRef("EventRule", "urn:reviewer:er", semantic_hash({"er": 1}))
    spoofed = replace(view.lifecycle_subject, replay_state="REPLAY_COMPLETE")
    ex = B5.LearnedProductLifecycleExecutor()
    ex.stage_release(spoofed)
    ex.register_product(spoofed.release_ref, event_authority_ref=ea, event_rule_ref=er)
    outcome = {}
    try:
        ex.publish_product(spoofed.release_ref, event_authority_ref=ea, event_rule_ref=er)
        outcome["published"] = True
    except Exception as exc:  # noqa: BLE001
        outcome["published"] = False
        outcome["exception"] = type(exc).__name__
        outcome["message"] = str(exc)[:160]
    # record truth: B5 trusts the caller-supplied replay_state
    assert outcome["published"] is True, outcome
    assert spoofed.replay_state == "REPLAY_COMPLETE"


# --------------------------------------------- K5 permission ceiling is never validated
def _publish_outcome(subject):
    ea = ExactRef("EventAuthority", "urn:reviewer:ea", semantic_hash({"ea": 1}))
    er = ExactRef("EventRule", "urn:reviewer:er", semantic_hash({"er": 1}))
    ex = B5.LearnedProductLifecycleExecutor()
    ex.stage_release(subject)
    ex.register_product(subject.release_ref, event_authority_ref=ea, event_rule_ref=er)
    try:
        ex.publish_product(subject.release_ref, event_authority_ref=ea, event_rule_ref=er)
        return {"published": True, "exception": None, "message": None,
                "stored_ceiling": ex._subject(subject.release_ref).producer_permission_ceiling_ref.key}
    except Exception as exc:  # noqa: BLE001
        return {"published": False, "exception": type(exc).__name__, "message": str(exc)[:160]}


def test_k5a_honest_replay_state_plus_fake_production_ceiling(actual):
    """Control: with the honest (non-complete) replay_state the publish is refused,
    and the refusal reason is the replay closure — NOT the permission ceiling."""
    view = build(actual)
    fake = ExactRef("ProducerPermissionCeiling",
                    "urn:reviewer:PRODUCTION_GRANT", semantic_hash({"prod": True}))
    out = _publish_outcome(replace(view.lifecycle_subject,
                                   producer_permission_ceiling_ref=fake))
    assert out["published"] is False
    assert out["exception"] == "LearnedProductLifecycleError"
    assert "REPLAY" in out["message"], out


def test_k5b_spoofed_replay_state_with_fake_production_ceiling_is_published(actual):
    """Adversarial: forge replay_state AND a production-looking permission ceiling.
    If B5 published, it never validated the ceiling (the caller-supplied boundary)."""
    view = build(actual)
    fake = ExactRef("ProducerPermissionCeiling",
                    "urn:reviewer:PRODUCTION_GRANT", semantic_hash({"prod": True}))
    subject = replace(view.lifecycle_subject, replay_state="REPLAY_COMPLETE",
                      producer_permission_ceiling_ref=fake)
    out = _publish_outcome(subject)
    assert out["published"] is True, out
    assert out["stored_ceiling"] == fake.key


def test_k5c_fake_closure_receipt_refs_are_accepted(actual):
    """Adversarial: replace every build/release receipt + replay root with fake refs."""
    view = build(actual)
    fake_receipt = ExactRef("BuildReceipt", "urn:reviewer:fake-receipt",
                            semantic_hash({"fake": 1}))
    fake_root = ExactRef("ReplayRoot", "urn:reviewer:fake-root", semantic_hash({"fake": 2}))
    subject = replace(view.lifecycle_subject, replay_state="REPLAY_COMPLETE",
                      build_or_release_receipt_refs=(fake_receipt,),
                      replay_root_ref=fake_root)
    out = _publish_outcome(subject)
    assert out["published"] is True, out


# ------------------------------------------------ K6 alien predicate, same denominator
def test_k6_alien_predicate_same_shape_is_refused(actual):
    """Recompute q1 from a DIFFERENT condition set: same arity, same denominator."""
    source, products = actual
    qauth = _query_authority("c1-at09-xor")
    registry = _registry(source, qauth)
    plans = G1._plans(source)
    honest_plan = plans["q1"]
    other = plans["q2"]
    alien, _ = G1._compose(source=source, qauth=qauth, registry=registry,
                           conditions=other.conditions,
                           target_question=other.target_question, tag=other.tag)
    with pytest.raises(Exception) as ei:  # noqa: BLE001
        CAND.build_source_free_c1_release(
            cell="q1", composition=alien, model_rule=other.model_rule,
            source_release_ref=source["release_ref"])
    assert "MISMATCH" in str(ei.value) or "IDENTITY" in str(ei.value), str(ei.value)[:200]


# ------------------------------------------------- K7 native nonpositive mints no M2
def test_k7_native_nonpositive_mints_no_product(actual):
    """Force a nonpositive native state and require a candidate refusal."""
    source, products = actual
    comp, rule = products["q1"]
    mutated = replace(comp, analytical_state="UNSUPPORTED")
    with pytest.raises(Exception) as ei:  # noqa: BLE001
        CAND.build_source_free_c1_release(
            cell="q1", composition=mutated, model_rule=rule,
            source_release_ref=source["release_ref"])
    assert "NONPOSITIVE" in str(ei.value), str(ei.value)[:200]


# ------------------------------------------------- K8 replay grade overclaim refused
def test_k8_fresh_process_replay_overclaim_refused(actual):
    with pytest.raises(Exception) as ei:  # noqa: BLE001
        build(actual, requested_replay_grade="FRESH_PROCESS_REPLAY")
    assert "OVERCLAIM" in str(ei.value), str(ei.value)[:200]
