"""PYAT HQ280 PV3 A04 - source-free authorized workload binder CANDIDATE tests.

Development-only.  Every positive case runs the REAL accepted owners
(``bind_governed_c11_projection`` -> ``execute_route_b_production`` ->
C11/I03/I05 -> ``BatchExecutionRunner``) over an honest SYNTHETIC source-free
fixture reused from the accepted Route B test corpus.  No raw SAV/DTA, no
original source, no all-35 claim, no model permission, no canonical adoption.

The expected universe is declared DOCUMENTARILY, before and apart from any
produced manifest, and is never derived from a generated workload.
"""

from __future__ import annotations

import random

import pytest

import rawlsing_next.pre553_original_workload_binder_candidate as binder
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_source_backed_c11_facade import GovernedC11Projection
from rawlsing_next.tests.test_pre553_empirical_query import (
    _predicate,
    _query,
    _response_leaf,
)
from rawlsing_next.tests.test_pre553_route_b_production import _fixture


SOURCE = "SYNTHETIC-SOURCEFREE-A04"
WAVE = "W1"
CONSUMER_C1 = "C1_ANALYTICAL_COMPOSITION"
CONSUMER_FF = "FIELD_FORGE_CONDITIONAL_SUPPORT"
CONSUMER_LEARNED = "LEARNED_EMPIRICAL_ADJUDICATION"


# --------------------------------------------------------------------------
# Honest source-free fixture (real accepted construction, reused unchanged)
# --------------------------------------------------------------------------
def _conditioned_predicate(stub, qauth, tag):
    """A real conditioned predicate: X==1 AND the whole-question cohort."""
    ast = {
        "op": "AND",
        "children": [
            _response_leaf(stub, qauth, "X", 1),
            {
                "op": "LEAF",
                "leaf_type": "DERIVED_BRANCH_COHORT",
                "branch_definition_id": f"BRANCH-{tag}",
                "resolved_predicate_hash_or_exact_membership_ref": ExactRef(
                    "BRANCH_MEMBERSHIP", f"urn:test:a04:{tag}",
                    stub["universe"].ref.content_hash,
                ),
                "parent_ancestry_ref": ExactRef(
                    "BRANCH_PARENT", f"urn:test:a04:{tag}-parent",
                    stub["universe"].ref.content_hash,
                ),
                "branch_algorithm_authority_ref": qauth.authority_ref,
                "branch_membership_replay_ref": ExactRef(
                    "BRANCH_REPLAY", f"urn:test:a04:{tag}-replay",
                    stub["universe"].ref.content_hash,
                ),
                "branch_source_scope_ref": stub["universe"].ref,
                "exact_member_respondent_refs": tuple(
                    sorted(
                        (m.ref for m in stub["respondents"].values()),
                        key=lambda r: r.key,
                    )
                ),
            },
        ],
    }
    return _predicate(stub, qauth, ast, tag=tag)


from rawlsing_next.pre553_empirical_objects import ExactRef  # noqa: E402


def _scope(tag: str = "a04"):
    """Real source-free substrate plus a caller-issued RuntimeObjectCatalog."""
    fx = _fixture()
    projection = fx["projection"]
    assert isinstance(projection, GovernedC11Projection)
    source_auth = next(
        a for a in projection.authority_snapshots
        if a.authority_kind == "SOURCE_SEMANTICS_TOPOLOGY"
    )
    stub = {
        "universe": projection.universes[0],
        "respondents": {r.respondent_key: r for r in projection.respondents},
        "qrefs": fx["qrefs"],
        "risk_refs": {"R": fx["risk"]},
        "source_auth": source_auth,
    }
    qauth, dauth, all_p = fx["qauth"], fx["dauth"], fx["all_p"]
    cond_x1 = _conditioned_predicate(stub, qauth, f"{tag}-cond-x1")

    queries = {
        # the fixture's own queries are RETAINED because the issued I05
        # discovery grammar's query templates reference them exactly.
        "y": fx["raw_query"],
        "y_weighted": fx["weighted_query"],
        "x": _query(stub, qauth, all_p, ("X",), measure="RAW", tag=f"{tag}-x"),
        "xy": _query(stub, qauth, all_p, ("X", "Y"), measure="RAW", tag=f"{tag}-xy"),
        "yx": _query(stub, qauth, all_p, ("Y", "X"), measure="RAW", tag=f"{tag}-yx"),
        # a candidate own-derivative topic used as a joint target
        "x_dk": _query(stub, qauth, all_p, ("X", "X"), measure="RAW",
                       tag=f"{tag}-x-dk"),
        "y_given_x1": _query(
            stub, qauth, cond_x1, ("Y",), measure="RAW", tag=f"{tag}-y-given-x1"
        ),
    }
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*projection.authority_snapshots, qauth, dauth)),
        predicates=(all_p, fx["x1"], fx["empty"], cond_x1),
        queries=tuple(queries[name] for name in sorted(queries)),
        discovery_authorities=(fx["discovery_authority"],),
    )
    projection_fields = {
        name: getattr(projection, name)
        for name in projection.__dataclass_fields__
    }
    return {
        "fx": fx, "projection": projection,
        "projection_fields": projection_fields, "catalog": catalog,
        "stream": fx["stream"], "source_sha": fx["stream"].source_sha256,
        "qauth": qauth, "dauth": dauth, "all_p": all_p,
        "discovery_ref": fx["discovery_authority"].ref, "queries": queries,
    }


# --------------------------------------------------------------------------
# INDEPENDENT expected universe, declared DOCUMENTARILY (never from output)
# --------------------------------------------------------------------------
def owner_order(query):
    """The issued owner's exact semantic target order tokens."""
    return tuple(
        component["target_ref"]["object_id"]
        for component in query.target_arity_and_topology["components"]
    )


def _d(scope, **kwargs):
    base = dict(
        source=SOURCE, wave=WAVE, source_identity=scope["source_sha"],
        authority_ref=scope["qauth"].authority_ref.key, measure_kind="RAW",
    )
    base.update(kwargs)
    return binder.ExpectedWorkDeclaration(**base)


def runnable_universe(scope):
    """Six independently declared RUNNABLE expected operations."""
    q = scope["queries"]
    return [
        _d(scope, item="A", form="F1", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="X",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR_SINGULAR", required_consumer=CONSUMER_C1,
           query_ref=q["x"].ref, predicate_ref=scope["all_p"].ref),
        _d(scope, item="B", form="F1", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="Y",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR_SINGULAR", required_consumer=CONSUMER_C1,
           query_ref=q["y"].ref, predicate_ref=scope["all_p"].ref),
        _d(scope, item="B", form="F1", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="Y",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR_SINGULAR", measure_kind="GOVERNED_WEIGHTED",
           required_consumer=CONSUMER_C1,
           query_ref=q["y_weighted"].ref, predicate_ref=scope["all_p"].ref),
        _d(scope, item="B", form="F1", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY",
           roles=("CONDITIONER", "TARGET"), target="Y",
           condition_order=("X",), risk_identity="RISK-R-COND",
           topology_identity="SCALAR_SINGULAR", required_consumer=CONSUMER_C1,
           query_ref=q["y_given_x1"].ref,
           predicate_ref=q["y_given_x1"].dependency_refs[0]),
        _d(scope, item="B", form="F1", slot="S2",
           op_class="I03_UNARY_OR_JOINT_QUERY",
           roles=("CONDITIONER", "TARGET"), target="J2",
           # the exact semantic target order the issued owner itself declares
           condition_order=owner_order(q["xy"]), risk_identity="RISK-R-COMMON",
           topology_identity="SCALAR_2X2_JOINT", required_consumer=CONSUMER_FF,
           query_ref=q["xy"].ref, predicate_ref=scope["all_p"].ref),
        _d(scope, item="B", form="F1", slot="S2",
           op_class="I05_BOUNDED_DISCOVERY", roles=("BASE",), target="D1",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR_2X2", required_consumer=CONSUMER_LEARNED,
           discovery_authority_ref=scope["discovery_ref"]),
    ]


def held_universe(scope):
    """Four declared obligations that must stay visible and never runnable."""
    return [
        _d(scope, item="O", form="F1", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="O",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="ORDERED_SEQUENCE", required_consumer=CONSUMER_C1,
           state="HELD",
           hold_reason="ORDERED_SEQUENCE_COLLAPSE_NOT_YET_AUTHORIZED"),
        _d(scope, item="R", form="F1", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="R",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="REPEATED_EVENT", required_consumer=CONSUMER_C1,
           state="HELD",
           hold_reason="REPEATED_EVENT_JOIN_NOT_YET_AUTHORIZED"),
        _d(scope, item="V", form="F2", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="V",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR_SINGULAR", required_consumer=CONSUMER_C1,
           state="DENIED", hold_reason="EXPLICIT_FAIL_CLOSED_SOURCE_GAP"),
        _d(scope, item="U", form="F2", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="U",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR_SINGULAR", required_consumer=CONSUMER_C1,
           state="SOURCE_NONAPPLICABLE",
           hold_reason="NO_COADMINISTERED_TARGET_IN_THIS_SLICE"),
    ]


def frozen_universe(scope):
    """THE independently frozen expectation. Never derived from any output."""
    return runnable_universe(scope) + held_universe(scope)


def submitted(scope, *, omit_items=(), omit_targets=(), include_held=True):
    """A producer's submission, possibly dropping expected work.

    The I05 discovery operation is always retained: Route B requires exactly
    one discovery authority, so hostiles target the I03 expectation set.
    """
    kept = [
        d for d in runnable_universe(scope)
        if (
            d.op_class == "I05_BOUNDED_DISCOVERY"
            or (d.item not in omit_items and d.target not in omit_targets)
        )
    ]
    return kept + (held_universe(scope) if include_held else [])


def bind(scope, declarations):
    return binder.bind_expected_work(
        declarations=declarations,
        projection_fields=scope["projection_fields"],
        runtime_catalog=scope["catalog"],
    )


def run(scope, bound):
    return binder.execute_bound_workload(bound, source=scope["stream"])


def consumers_for(declarations, executed):
    """Consumer receipts built from REAL produced result refs."""
    receipts = []
    by_query = {
        d.query_ref.key: d for d in declarations
        if d.is_runnable and d.op_class == "I03_UNARY_OR_JOINT_QUERY"
    }
    for item in executed.production_result.i03_results:
        d = by_query.get(item.query_ref.key)
        if d is None:
            continue
        for fact in item.facts:
            receipts.append({
                "expected_work_key": d.expected_work_key,
                "consumer": d.required_consumer,
                "consumed_output_identity": binder.output_identity(
                    expected_work_key_value=d.expected_work_key,
                    result_type="EMPIRICAL_FACT",
                    value=fact.ref.as_dict(),
                ),
            })
    discovery = next(
        (d for d in declarations
         if d.is_runnable and d.op_class == "I05_BOUNDED_DISCOVERY"),
        None,
    )
    if discovery is not None:
        for receipt in executed.production_result.i05_result.receipts:
            receipts.append({
                "expected_work_key": discovery.expected_work_key,
                "consumer": discovery.required_consumer,
                "consumed_output_identity": binder.output_identity(
                    expected_work_key_value=discovery.expected_work_key,
                    result_type="DISCOVERY_RECEIPT",
                    value=receipt.ref.as_dict(),
                ),
            })
    return receipts


def court(scope, submission, *, frozen=None, receipts="auto"):
    """Bind + execute a SUBMISSION, then reconcile against the FROZEN universe."""
    frozen = frozen_universe(scope) if frozen is None else frozen
    bound = bind(scope, submission)
    executed = run(scope, bound)
    use = consumers_for(frozen, executed) if receipts == "auto" else receipts
    return executed, binder.reconcile(
        declarations=frozen, executed=executed, consumer_receipts=use
    )


def clone(declaration, **overrides):
    """Faithful copy of a declaration with selected identity fields changed."""
    fields = dict(
        source=declaration.source, wave=declaration.wave, item=declaration.item,
        form=declaration.form, slot=declaration.slot, op_class=declaration.op_class,
        roles=declaration.roles, target=declaration.target,
        condition_order=declaration.condition_order,
        measure_kind=declaration.measure_kind,
        source_identity=declaration.source_identity,
        authority_ref=declaration.authority_ref,
        risk_identity=declaration.risk_identity,
        topology_identity=declaration.topology_identity,
        required_consumer=declaration.required_consumer,
        state=declaration.state, hold_reason=declaration.hold_reason,
        multiplicity=declaration.multiplicity,
        query_ref=declaration.query_ref, predicate_ref=declaration.predicate_ref,
        discovery_authority_ref=declaration.discovery_authority_ref,
    )
    fields.update(overrides)
    return binder.ExpectedWorkDeclaration(**fields)


def swap(declarations, original, replacement):
    return [replacement if d is original else d for d in declarations]


# ==========================================================================
# POSITIVE
# ==========================================================================
def test_positive_source_free_run_through_real_owners():
    scope = _scope()
    declared = frozen_universe(scope)
    executed, verdict = court(scope, declared)

    # real Route B / C11 / I03 / I05 effects actually happened
    assert executed.production_result.c11_release.release_ref is not None
    assert len(executed.production_result.i03_results) == 5
    assert executed.production_result.i05_result.evaluated_frontier_ref is not None
    assert executed.batch_summary.batch_state == "COMPLETED"
    assert executed.batch_summary.full_coverage is True
    assert executed.batch_summary.total_units == 6

    assert verdict.omitted == ()
    assert verdict.extra == ()
    assert verdict.work_reconciled is True
    assert verdict.ok is True, verdict.failure_codes()
    assert all(
        cls in binder.MEASURED_RESULT_CLASSES
        for cls in verdict.result_classes.values()
    )
    assert len(verdict.visible_non_runnable) == 4
    assert all(row["runnable"] is False for row in executed.bound.held_frontier)


def test_binder_emits_zero_semantic_or_promotion_effects():
    scope = _scope()
    bound = bind(scope, frozen_universe(scope))
    assert dict(bound.effects) == {
        "source_meaning_inference": False,
        "authority_creation": False,
        "candidate_frontier_invention": False,
        "structural_truth_effect": False,
        "causal_truth_effect": False,
        "model_permission_effect": False,
        "learned_product_publication_effect": False,
        "actor_v3_effect": False,
    }
    executed = run(scope, bound)
    assert executed.production_result.replay_receipt["effects"] == {
        "learned_empirical_adjudication_effect": False,
        "learned_product_publication_effect": False,
        "learned_product_current_selection_effect": False,
        "structural_truth_effect": False,
        "causal_truth_effect": False,
        "actor_v3_effect": False,
    }


def test_expected_work_is_frozen_before_any_owner_runs():
    scope = _scope()
    declared = frozen_universe(scope)
    before = binder.expected_frontier_digest(declared)
    bound = bind(scope, declared)
    assert bound.expected_frontier_hash == before
    executed = run(scope, bound)
    assert binder.expected_frontier_digest(declared) == before
    assert bound.expected_frontier_hash != binder.expected_frontier_digest([])


def test_stable_reorder_yields_identical_jobs_manifest_and_results():
    scope = _scope()
    declared = frozen_universe(scope)
    first = run(scope, bind(scope, declared))

    shuffled = list(declared)
    random.Random(20261011).shuffle(shuffled)
    reversed_catalog = RuntimeObjectCatalog(
        authorities=tuple(reversed(scope["catalog"].authorities)),
        predicates=tuple(reversed(scope["catalog"].predicates)),
        queries=tuple(reversed(scope["catalog"].queries)),
        discovery_authorities=tuple(reversed(scope["catalog"].discovery_authorities)),
    )
    second = run(scope, binder.bind_expected_work(
        declarations=shuffled,
        projection_fields=scope["projection_fields"],
        runtime_catalog=reversed_catalog,
    ))

    assert first.bound.expected_frontier_hash == second.bound.expected_frontier_hash
    assert first.batch_manifest.manifest_hash == second.batch_manifest.manifest_hash
    assert tuple(u.unit_ref for u in first.batch_manifest.units) == tuple(
        u.unit_ref for u in second.batch_manifest.units
    )
    for field in ("dependency_root", "receipt_identity"):
        assert (
            first.production_result.replay_receipt[field]
            == second.production_result.replay_receipt[field]
        )
    assert first.batch_summary.receipt_set_hash == second.batch_summary.receipt_set_hash


def test_restart_identity_resume_does_not_duplicate_semantic_work():
    scope = _scope()
    first = run(scope, bind(scope, frozen_universe(scope)))
    resumed = BatchExecutionRunner(
        manifest=first.batch_manifest,
        repository=first.production_result.repository_binding.executor.repository,
        prior_receipts=first.batch_receipts,
    )
    assert resumed.pending_units() == ()
    assert len(resumed.receipts) == len(first.batch_receipts)
    assert resumed.summary().batch_state == "COMPLETED"
    assert resumed.summary().receipt_set_hash == first.batch_summary.receipt_set_hash


def test_distinct_identity_kinds_are_never_conflated():
    scope = _scope()
    runnable = runnable_universe(scope)
    d = next(x for x in runnable if x.item == "A")
    other = next(x for x in runnable if x.target == "J2")

    assert d.item_key != other.item_key                       # documentary item
    assert d.operation_key_value != other.operation_key_value  # operation
    assert d.expected_work_key != other.expected_work_key      # expected work
    assert binder.execution_attempt_key(
        expected_work_key_value=d.expected_work_key, attempt_index=1
    ) != binder.execution_attempt_key(
        expected_work_key_value=d.expected_work_key, attempt_index=2
    )
    assert binder.output_identity(
        expected_work_key_value=d.expected_work_key,
        result_type="EMPIRICAL_FACT", value={"x": 1},
    ) != binder.output_identity(
        expected_work_key_value=d.expected_work_key,
        result_type="DISCOVERY_RECEIPT", value={"x": 1},
    )


def test_raw_and_weighted_are_distinct_operations_not_one_key():
    """A genuine defect found while binding: measure kind is identity-bearing."""
    scope = _scope()
    raw = next(d for d in runnable_universe(scope)
               if d.measure_kind == "RAW" and d.target == "Y")
    weighted = next(d for d in runnable_universe(scope)
                    if d.measure_kind == "GOVERNED_WEIGHTED")
    assert raw.item_key == weighted.item_key  # same administered item
    assert raw.operation_key_value != weighted.operation_key_value
    assert raw.expected_work_key != weighted.expected_work_key

    executed, verdict = court(scope, frozen_universe(scope))
    assert len(verdict.result_classes) == 6


# ==========================================================================
# HOSTILES
# ==========================================================================
def test_a_only_submission_while_a_and_b_are_independently_expected():
    """A+B expected; the submitted manifest carries only A's operation."""
    scope = _scope()
    a_only = submitted(scope, omit_items={"B"})
    executed, verdict = court(scope, a_only)
    assert verdict.ok is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict.failure_codes()
    # four B operations are dropped (the I05 discovery op is retained because
    # Route B requires exactly one discovery authority)
    assert len(verdict.omitted) == 4
    assert set(verdict.omitted) == {
        d.expected_work_key for d in runnable_universe(scope)
        if d.item == "B" and d.op_class == "I03_UNARY_OR_JOINT_QUERY"
    }


def test_missing_b_witness():
    scope = _scope()
    without_b = submitted(scope, omit_items={"B"})
    _, verdict = court(scope, without_b)
    assert verdict.ok is False
    assert len(verdict.omitted) == 4
    assert verdict.work_reconciled is False


def test_missing_j2_joint_witness():
    scope = _scope()
    frozen = frozen_universe(scope)
    joint = next(d for d in frozen if d.target == "J2")
    without_j2 = [d for d in frozen if d is not joint]
    _, verdict = court(scope, without_j2)
    assert verdict.ok is False
    assert "EXPECTED_OPERATION_OMITTED" in verdict.failure_codes()
    assert joint.expected_work_key in verdict.omitted
    assert verdict.extra == ()


def test_missing_b_and_missing_j2_together():
    scope = _scope()
    frozen = frozen_universe(scope)
    joint = next(d for d in frozen if d.target == "J2")
    trimmed = submitted(scope, omit_items={"B"}, omit_targets={"J2"})
    _, verdict = court(scope, trimmed)
    assert verdict.ok is False
    assert joint.expected_work_key in verdict.omitted
    assert len(verdict.omitted) == 4


def test_unauthorized_extra_work_is_caught():
    scope = _scope()
    # an I03 declaration whose query was NEVER declared expected
    rogue = _d(scope, item="Z", form="F1", slot="S9",
               op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="R",
               condition_order=owner_order(scope["queries"]["yx"]),
               risk_identity="RISK-R-ALL",
               topology_identity="SCALAR_2X2_JOINT", required_consumer=CONSUMER_C1,
               query_ref=scope["queries"]["yx"].ref,
               predicate_ref=scope["all_p"].ref)
    _, verdict = court(scope, frozen_universe(scope) + [rogue])
    assert verdict.ok is False
    assert "UNAUTHORIZED_EXTRA_JOB" in verdict.failure_codes()
    assert len(verdict.extra) == 1


def test_same_count_different_keys_fails():
    """Equal totals, different identities: the classic false PASS."""
    scope = _scope()
    frozen = frozen_universe(scope)
    a_decl = next(d for d in frozen if d.item == "A")
    # same job, renamed documentary item -> same count, wrong expected key
    renamed = clone(a_decl, item="A-PRIME")
    assert renamed.expected_work_key != a_decl.expected_work_key
    _, verdict = court(scope, swap(frozen, a_decl, renamed))
    assert verdict.ok is False
    codes = verdict.failure_codes()
    assert "EXPECTED_OPERATION_OMITTED" in codes
    assert "UNAUTHORIZED_EXTRA_JOB" in codes
    assert len(verdict.job_keys) == len(verdict.expected_keys)


def test_condition_order_substitution_changes_the_operation_key():
    """q(C|A) vs q(C|A,B) denominator substitution."""
    scope = _scope()
    frozen = frozen_universe(scope)
    xy = next(d for d in frozen if d.target == "J2")
    yx = scope["queries"]["yx"]
    assert owner_order(yx) != owner_order(xy.query_ref and scope["queries"]["xy"])
    reordered = clone(xy, query_ref=yx.ref, condition_order=owner_order(yx))
    assert reordered.operation_key_value != xy.operation_key_value
    _, verdict = court(scope, swap(frozen, xy, reordered))
    assert verdict.ok is False
    assert xy.expected_work_key in verdict.omitted
    assert reordered.expected_work_key in verdict.extra


def test_candidate_own_dk_cotopic_fake_joint_is_rejected():
    scope = _scope()
    frozen = frozen_universe(scope)
    xy = next(d for d in frozen if d.target == "J2")
    # A shared topic used as a joint warrant: the conditioner and the target
    # are the SAME item, one of them a candidate own-_dk derivative.
    fake = clone(
        xy, target="J2_DK",
        condition_order=owner_order(scope["queries"]["x_dk"]),
        query_ref=scope["queries"]["x_dk"].ref,
    )
    _, verdict = court(scope, swap(frozen, xy, fake))
    assert verdict.ok is False
    assert "CANDIDATE_OWN_DK_JOINT" in verdict.failure_codes()


def test_altered_document_version_changes_item_identity_and_is_caught():
    scope = _scope()
    frozen = frozen_universe(scope)
    a_decl = next(d for d in frozen if d.item == "A")
    wrong_form = clone(a_decl, form="F2")
    assert a_decl.item_key != wrong_form.item_key
    _, verdict = court(scope, swap(frozen, a_decl, wrong_form))
    assert verdict.ok is False
    assert a_decl.expected_work_key in verdict.omitted


def test_source_identity_mismatch_is_caught():
    scope = _scope()
    frozen = frozen_universe(scope)
    a_decl = next(d for d in frozen if d.item == "A")
    # every OTHER declaration still names the true source; only this one lies
    wrong = clone(a_decl, source_identity="0" * 64, item="A")
    assert wrong.expected_work_key != a_decl.expected_work_key
    _, verdict = court(scope, swap(frozen, a_decl, wrong))
    assert verdict.ok is False
    codes = verdict.failure_codes()
    assert "SOURCE_IDENTITY_MISMATCH" in codes
    assert a_decl.expected_work_key in verdict.omitted


def test_post_result_expected_work_laundering_is_caught():
    """A manifest cannot certify itself as the independent expectation."""
    scope = _scope()
    frozen = frozen_universe(scope)

    # laundered "expectation" == exactly what the producer emitted
    truncated = submitted(scope, omit_items={"B"})
    executed = run(scope, bind(scope, truncated))
    produced = [plan.expected_work_key for plan in executed.bound.job_plans]
    laundered = [d for d in frozen if d.expected_work_key in set(produced)]

    self_verdict = binder.reconcile(
        declarations=laundered, executed=executed,
        consumer_receipts=consumers_for(laundered, executed),
    )
    # against ITSELF the truncated submission self-certifies: every job it
    # emitted matches its own reduced "expectation".  This is exactly why
    # self-certification is NOT sufficient evidence of no-drop.
    assert {d.expected_work_key for d in laundered} == set(produced)
    assert len(laundered) < len([d for d in frozen if d.is_runnable])
    assert self_verdict.omitted == ()

    # against the independently frozen universe it must fail hard
    frozen_verdict = binder.reconcile(
        declarations=frozen, executed=executed,
        consumer_receipts=consumers_for(frozen, executed),
    )
    assert frozen_verdict.ok is False
    assert "EXPECTED_OPERATION_OMITTED" in frozen_verdict.failure_codes()
    assert len(frozen_verdict.omitted) == 4

    # and the structural guard: the bound frontier is the TRUNCATED one
    assert executed.bound.expected_frontier_hash == (
        binder.expected_frontier_digest(truncated)
    )
    assert executed.bound.expected_frontier_hash != (
        binder.expected_frontier_digest(frozen)
    )
    # the two verdicts see DIFFERENT frontiers even for one execution: the
    # self-certified one hides 4 omitted expected operations
    assert self_verdict.declared_frontier_hash != frozen_verdict.declared_frontier_hash
    assert frozen_verdict.declared_frontier_hash == binder.expected_frontier_digest(frozen)
    assert self_verdict.declared_frontier_hash == executed.bound.expected_frontier_hash


def test_expected_set_output_derived_is_detected_directly():
    """Reconciliation rejects an expectation that was recomputed from output."""
    scope = _scope()
    truncated = submitted(scope, omit_items={"B"})
    executed = run(scope, bind(scope, truncated))
    frozen = frozen_universe(scope)
    verdict = binder.reconcile(
        declarations=frozen, executed=executed,
        consumer_receipts=consumers_for(frozen, executed),
    )
    assert "EXPECTED_SET_OUTPUT_DERIVED" in verdict.failure_codes()


def test_required_consumer_omission_fails_even_with_every_job_present():
    scope = _scope()
    declared = frozen_universe(scope)
    executed = run(scope, bind(scope, declared))
    partial = consumers_for(declared, executed)[:-1]
    verdict = binder.reconcile(
        declarations=declared, executed=executed, consumer_receipts=partial
    )
    assert verdict.work_reconciled is True
    assert verdict.ok is False
    assert "REQUIRED_CONSUMER_OMITTED" in verdict.failure_codes()
    assert len(verdict.unsatisfied_consumers) == 1


def test_duplicate_semantic_job_is_refused():
    scope = _scope()
    frozen = frozen_universe(scope)
    a_decl = next(d for d in frozen if d.item == "A")
    with pytest.raises(binder.BinderCandidateError, match="collapsed onto one semantic"):
        bind(scope, frozen + [clone(a_decl, item="A-TWIN")])


def test_multiplicity_requires_explicit_justification():
    scope = _scope()
    frozen = frozen_universe(scope)
    a_decl = next(d for d in frozen if d.item == "A")
    with pytest.raises(binder.BinderCandidateError, match="collapsed onto one semantic"):
        bind(scope, frozen + [clone(a_decl, item="A-MULTI", multiplicity=2)])


def test_held_denied_and_na_obligations_can_never_carry_executable_refs():
    scope = _scope()
    for d in held_universe(scope):
        with pytest.raises(binder.BinderCandidateError, match="must not carry executable"):
            clone(d, query_ref=scope["queries"]["y"].ref,
                  predicate_ref=scope["all_p"].ref)


def test_held_denied_and_na_stay_visible_and_never_runnable():
    scope = _scope()
    executed, verdict = court(scope, frozen_universe(scope))
    assert verdict.ok is True, verdict.failure_codes()
    states = {row["state"] for row in executed.bound.held_frontier}
    assert states == {"HELD", "DENIED", "SOURCE_NONAPPLICABLE"}
    assert all(row["runnable"] is False for row in executed.bound.held_frontier)
    assert len(verdict.visible_non_runnable) == 4
    assert set(verdict.visible_non_runnable) == {
        d.expected_work_key for d in held_universe(scope)
    }


def test_held_obligations_removed_entirely_are_detected():
    scope = _scope()
    _, verdict = court(scope, submitted(scope, include_held=False))
    assert verdict.ok is False
    assert "HELD_OR_DENIED_WORK_NOT_VISIBLE" in verdict.failure_codes()


def test_non_runnable_reason_is_mandatory():
    with pytest.raises(binder.BinderCandidateError, match="hold/denial reason"):
        binder.ExpectedWorkDeclaration(
            source=SOURCE, wave=WAVE, item="A", form="F1", slot="S1",
            op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="X",
            condition_order=(), measure_kind="RAW", source_identity="0" * 64,
            authority_ref="AUTH", risk_identity="RISK",
            topology_identity="SCALAR", required_consumer=CONSUMER_C1,
            state="HELD",
        )


def test_undeclared_authority_is_refused():
    scope = _scope()
    frozen = frozen_universe(scope)
    a_decl = next(d for d in frozen if d.item == "A")
    rogue = clone(a_decl, authority_ref="NOT-IN-CATALOG|1.0.0|" + "f" * 64)
    with pytest.raises(binder.BinderCandidateError, match="issued RuntimeObjectCatalog"):
        bind(scope, swap(frozen, a_decl, rogue))


def test_missing_i05_expected_work_is_refused():
    scope = _scope()
    without = [d for d in frozen_universe(scope)
               if d.op_class != "I05_BOUNDED_DISCOVERY"]
    with pytest.raises(binder.BinderCandidateError, match="exactly one I05"):
        bind(scope, without)


def test_runnable_without_owner_refs_is_refused():
    scope = _scope()
    with pytest.raises(binder.BinderCandidateError, match="requires exact query_ref"):
        _d(scope, item="A", form="F1", slot="S1",
           op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="X",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR_SINGULAR", required_consumer=CONSUMER_C1)
    with pytest.raises(binder.BinderCandidateError, match="requires exact discovery"):
        _d(scope, item="A", form="F1", slot="S1",
           op_class="I05_BOUNDED_DISCOVERY", roles=("BASE",), target="D1",
           condition_order=(), risk_identity="RISK-R-ALL",
           topology_identity="SCALAR", required_consumer=CONSUMER_LEARNED)


def test_unexecuted_work_is_never_an_admissible_null():
    """Absence of execution is a typed failure, never a measured null."""
    assert binder.ADMISSIBLE_NULL_CLASS not in binder.FORBIDDEN_NULL_SOURCES
    assert binder.ADMISSIBLE_NULL_CLASS not in binder.NEVER_SUCCESS_CLASSES
    klass = binder._classify_result(
        expected_work_key_value="k", declared_measure_kind="RAW",
        produced_fact=None, executed=False, batch_state="DEFERRED",
        expected_multiplicity=1, observed_multiplicity=0,
    )
    assert klass == "UNEXECUTED"
    assert klass != binder.ADMISSIBLE_NULL_CLASS
    assert klass not in binder.MEASURED_RESULT_CLASSES
    assert "UNEXECUTED" in binder.FORBIDDEN_NULL_SOURCES
    for never in ("UNVISITED", "PARTIAL", "ADAPTIVE_PARTIAL", "UNAVAILABLE"):
        assert never in binder.NEVER_SUCCESS_CLASSES


def test_multiplicity_mismatch_is_a_typed_failure():
    assert binder._classify_result(
        expected_work_key_value="k", declared_measure_kind="RAW",
        produced_fact=object(), executed=True, batch_state="COMPLETED",
        expected_multiplicity=2, observed_multiplicity=1,
    ) == "MULTIPLICITY_MISMATCH"


def test_unrecognized_owner_state_is_never_promoted_to_measured():
    class _Odd:
        typed_state = "SOMETHING_NEW"

    klass = binder._classify_result(
        expected_work_key_value="k", declared_measure_kind="RAW",
        produced_fact=_Odd(), executed=True, batch_state="COMPLETED",
        expected_multiplicity=1, observed_multiplicity=1,
    )
    assert klass == "OWNER_TYPED_SOMETHING_NEW"
    assert klass not in binder.MEASURED_RESULT_CLASSES


def test_missing_weighted_result_is_not_reported_as_an_empirical_null():
    """An UNAVAILABLE governed-weighted fact may not launder into MEASURED_NULL."""
    scope = _scope()
    frozen = frozen_universe(scope)
    weighted = next(d for d in frozen if d.measure_kind == "GOVERNED_WEIGHTED")

    class _Unavailable:
        typed_state = "UNAVAILABLE"

    executed = run(scope, bind(scope, frozen))
    # the governed-weighted expectation really executed against the real owner
    weighted_executions = [
        item for item in executed.production_result.i03_results
        if item.query_ref == scope["queries"]["y_weighted"].ref
    ]
    assert len(weighted_executions) == 1
    assert weighted_executions[0].facts[0].measure_kind == "GOVERNED_WEIGHTED"
    assert weighted_executions[0].facts[0].weighted_denominator_support_if_authorized
    klass = binder._classify_result(
        expected_work_key_value=weighted.expected_work_key,
        declared_measure_kind="GOVERNED_WEIGHTED",
        produced_fact=_Unavailable(), executed=True, batch_state="COMPLETED",
        expected_multiplicity=1, observed_multiplicity=1,
    )
    assert klass == "OWNER_TYPED_UNAVAILABLE"
    assert klass not in binder.MEASURED_RESULT_CLASSES
    assert klass != binder.ADMISSIBLE_NULL_CLASS


def test_consumer_obligations_are_declared_per_operation_not_per_product():
    scope = _scope()
    declared = frozen_universe(scope)
    executed = run(scope, bind(scope, declared))
    verdict = binder.reconcile(
        declarations=declared, executed=executed,
        consumer_receipts=consumers_for(declared, executed),
    )
    obligations = verdict.consumer_obligations
    assert len(obligations) == len([d for d in declared if d.is_runnable])
    assert len({o["expected_work_key"] for o in obligations}) == len(obligations)
    shared = [o for o in obligations if o["consumer"] == CONSUMER_C1]
    assert len(shared) >= 4
    assert len({o["expected_work_key"] for o in shared}) == len(shared)


def test_threshold_truncation_before_reconciliation_cannot_hide_work():
    scope = _scope()
    executed, verdict = court(scope, frozen_universe(scope))
    filtered = dict(verdict.result_classes)
    filtered.pop(next(iter(filtered)))
    # truncating the RESULT VIEW does not change the frozen frontier
    assert verdict.frontier_hash == executed.bound.expected_frontier_hash
    assert len(verdict.expected_keys) == 6
    assert len(filtered) == 5


def test_five_identity_kinds_have_distinct_domains():
    a = binder.documentary_item_key(
        source=SOURCE, wave=WAVE, item="A", form="F1", slot="S1"
    )
    o = binder.operation_key(
        op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="X"
    )
    e = binder.expected_work_key(
        item_key=a, operation_key_value=o, source_identity="s",
        authority_ref="auth", risk_identity="r", topology_identity="t",
        consumer="c",
    )
    assert len({a, o, e}) == 3
    # an explicit version participates in the key
    assert binder.documentary_item_key(
        source=SOURCE, wave=WAVE, item="A", form="F1", slot="S1",
        version="OTHER@2.0.0",
    ) != a


def test_every_declaration_has_a_distinct_complete_preimage():
    scope = _scope()
    declared = frozen_universe(scope)
    keys = [d.expected_work_key for d in declared]
    assert len(set(keys)) == len(keys)
    preimages = {
        binder.canonical_preimage_json(dict(d.preimage())) for d in declared
    }
    assert len(preimages) == len(declared)


def test_binder_uses_only_existing_accepted_owners():
    import inspect

    source = inspect.getsource(binder)
    import_surface = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    for token in (
        "pre553_route_b_production", "pre553_carrier_execution",
        "pre553_batch_runner", "pre553_empirical_objects",
        "pre553_source_backed_c11_facade",
    ):
        assert token in import_surface
    # no invented replacement scheduler/engine
    for forbidden in (
        "class Scheduler", "class Engine", "class WorkloadPlanner",
        "class SchedulerReplacement",
    ):
        assert forbidden not in source


def test_binder_does_not_import_or_depend_on_the_a05_oracle():
    import inspect

    source = inspect.getsource(binder)
    assert "a05_oracle" not in source
    assert "a05_hostiles" not in source
    import_surface = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    assert "a05" not in import_surface


def test_a05_public_contract_compatibility_is_declarative_only():
    assert binder.A05_COMPATIBLE_SCHEMA_VERSION == "HQ280_PV3_A05_EXPECTED_WORK@1.0.0"
    assert binder.EXPECTED_WORK_SCHEMA_VERSION == "HQ280_PV3_A04_EXPECTED_WORK@1.0.0"
    # the same public failure vocabulary A05 published
    scope = _scope()
    _, verdict = court(scope, submitted(scope, omit_items={"B"}))
    assert set(verdict.failure_codes()) <= {
        "EXPECTED_OPERATION_OMITTED", "UNAUTHORIZED_EXTRA_JOB",
        "EXPECTED_MULTIPLICITY_MISMATCH", "MISSING_TYPED_RESULT",
        "FALSE_EMPIRICAL_NULL", "PARTIAL_OR_UNAVAILABLE_REPORTED_AS_SUCCESS",
        "ZERO_DENOMINATOR_NOT_TYPED", "PRODUCT_ABSENT",
        "REQUIRED_CONSUMER_OMITTED", "HELD_OR_DENIED_WORK_EXECUTED",
        "HELD_OR_DENIED_WORK_NOT_VISIBLE", "CANDIDATE_OWN_DK_JOINT",
        "EXPECTED_SET_OUTPUT_DERIVED", "SOURCE_IDENTITY_MISMATCH",
    }


def test_source_free_only_no_original_source_claim():
    """The candidate declares its own development-only ceiling."""
    import inspect

    doc = inspect.getdoc(binder)
    assert "source-free development only" in doc
    assert "no original-source" in doc.lower() or "original-source" in doc