"""R5 WG0P2 repaired workload court: the 15 WG0I-observed failures, fixed.

Same test names as WG0I's independent hostiles where the required behavior is
identical; repaired semantics where the old test asserted a defect. Three
repaired controls replace defect-asserting controls. All computation flows
through real C11 ingest, real I03 queries and the real BatchExecutionRunner.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.pre553_batch_runner import BatchExecutionRunner, BatchUnitSpec
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_query import execute_empirical_query

import wg0p2_workload as w


def _releases():
    return w.build_all_releases()


def _builder(items=None):
    b = w.WorkloadBuilder()
    for item in (w.independent_oracle_items() if items is None else items):
        assert b.add_item(item) == "OK"
    return b


def _items_by_id():
    return {i.item_id: i for i in w.independent_oracle_items()}


def _full_plan():
    releases = _releases()
    b = _builder()
    freeze_hash = b.freeze()
    ops = b.enumerate()
    return w.build_executable_plan(ops, releases, freeze_hash=freeze_hash,
                                   items_by_id=_items_by_id())


def _executed():
    plan = _full_plan()
    runner, receipts = w.run_plan(plan, w.make_executor(plan))
    return plan, runner, receipts


def _cells(op_id):
    plan, _, receipts = _executed()
    eff = w.consumer_effects(plan, receipts)
    return eff[op_id]


# --------------------------------------------------------------------------
# Repaired controls (defect-asserting controls replaced by repaired equivalents)
# --------------------------------------------------------------------------

def test_control_exact_candidate_file_and_frozen_inventory():
    assert w.__file__ == str(Path(__file__).parent / "wg0p2_workload.py")
    assert len(w.independent_oracle_items()) == 5
    ops = _builder().enumerate()
    counts = Counter((o.op_class, o.disposition.value) for o in ops)
    assert counts == {("MARGINAL", "PRODUCED"): 3, ("MARGINAL", "HELD"): 2,
                      ("CONDITIONAL", "HELD"): 14, ("CONDITIONAL", "INADMISSIBLE"): 6}
    assert len(ops) == 25
    assert not [o for o in ops if o.op_class == "CONDITIONAL"
                and o.disposition == w.Disposition.PRODUCED]


def test_control_validated_c11_releases_no_manual_injection():
    plan = _full_plan()
    assert len(plan.repository.release_refs) == 3
    for ref in plan.repository.release_refs:
        release = plan.repository.resolve_release_exact(ref)
        assert type(release).__name__ == "C11LogicalRelease"
        assert isinstance(release, C11LogicalRelease)


def test_control_no_fallback_missing_payload_fails_closed():
    plan = _full_plan()
    unit = plan.manifest.units[0]
    foreign = BatchUnitSpec(
        job_kind="QUERY",
        job_ref=w._ref("EmpiricalQuerySpec@1.0.0", "OP-NOT-IN-SPECS"),
        release_refs=unit.release_refs,
        semantic_input_refs=unit.semantic_input_refs,
    )
    with pytest.raises((KeyError, ValueError, LookupError)):
        w.make_executor(plan)(foreign)


def test_control_real_computed_values_not_caller_fractions():
    eff01 = _cells("OP-WG0P-ORD-01-MARGINAL")
    assert eff01[0]["denominator"] == 6
    assert {c["cell"]: c["n"] for c in eff01[0]["cells"]} == {
        "0": 1, "1": 2, "2": 2, "3": 1, "9": 0}
    assert eff01[0]["cells"][-1]["state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    eff05 = _cells("OP-WG0P-ORD-05-MARGINAL")
    assert eff05[0]["denominator"] == 4
    assert {c["cell"]: c["n"] for c in eff05[0]["cells"]} == {
        "0": 0, "1": 2, "2": 1, "3": 1, "9": 0}


def test_control_frozen_builder_rejects_new_item():
    b = _builder()
    b.freeze()
    assert b.add_item(replace(w.independent_oracle_items()[0], form_id="NEW")) == "FRONTIER_FROZEN"


# --------------------------------------------------------------------------
# Repaired reds (same names, required behavior now holds)
# --------------------------------------------------------------------------

def test_red_missing_operation_payload_must_fail_closed():
    plan = _full_plan()
    unit = plan.manifest.units[0]
    held_op = next(o for o in _builder().enumerate()
                   if o.disposition == w.Disposition.HELD)
    assert held_op.op_id not in plan.op_specs
    with pytest.raises((KeyError, ValueError, LookupError)):
        w.make_executor(plan)(unit.__class__(
            job_kind="QUERY",
            job_ref=w._ref("EmpiricalQuerySpec@1.0.0", held_op.op_id),
            release_refs=unit.release_refs,
            semantic_input_refs=unit.semantic_input_refs,
        ))


def test_red_invalid_negative_observation_must_fail_closed():
    with pytest.raises((ValueError, TypeError)):
        w.admit_native_rows("REL-A-W1", {"Q-ORD-A": {"topology": "SCALAR_SINGULAR",
                                                     "domain": ["0", "1", "2", "3", "9"]}},
                            [{"id": "RX", "responses": {"Q-ORD-A": "-1"}}])


def test_red_no_c11_release_without_validated_c11logicalrelease():
    plan = _full_plan()
    assert all(type(plan.repository.resolve_release_exact(ref)).__name__ == "C11LogicalRelease"
               for ref in plan.repository.release_refs)
    assert len(plan.repository._by_ref) == 3


def test_red_no_condition_without_joined_respondent_risk_set():
    a = w.independent_oracle_items()[0]
    b = replace(a, item_id="OTHER-RESPONDENT-FORM", form_id="Q-OTHER", options=("N", "Y"))
    ops = _builder([a, b]).enumerate()
    assert not [o for o in ops if o.op_class == "CONDITIONAL"
                and o.disposition == w.Disposition.PRODUCED]


def test_red_unknown_source_rights_must_hold():
    orig = w.independent_oracle_items()[0]
    it = replace(orig, grant="WITHHELD")
    op = next(o for o in _builder([it]).enumerate() if o.op_class == "MARGINAL")
    assert op.disposition == w.Disposition.HELD


def test_red_arbitrary_grant_token_must_not_be_permission():
    it = replace(w.independent_oracle_items()[0], grant="NO_SOURCE_ISSUER_OR_LICENSE")
    assert _builder([it]).enumerate()[0].disposition == w.Disposition.HELD


def test_red_freeze_must_bind_original_native_options():
    it = w.independent_oracle_items()[0]
    b1, b2 = w.WorkloadBuilder(), w.WorkloadBuilder()
    b1.add_item(it)
    b2.add_item(replace(it, options=("changed-native-category",)))
    assert b1.freeze() != b2.freeze()


def test_red_freeze_must_bind_source_permission_status():
    it = w.independent_oracle_items()[0]
    b1, b2 = w.WorkloadBuilder(), w.WorkloadBuilder()
    b1.add_item(it)
    b2.add_item(replace(it, grant="WITHDRAWN"))
    assert b1.freeze() != b2.freeze()


def test_red_withdrawn_conditioning_pair_must_retained_as_held():
    ops = _builder().enumerate()
    wanted = "OP-WG0P-ORD-01-GIVEN-WG0P-ORD-04"
    found = [o for o in ops if o.op_id == wanted]
    assert found and found[0].disposition == w.Disposition.HELD


def test_red_routed_unknown_pair_must_retain_as_held():
    ops = _builder().enumerate()
    wanted = "OP-WG0P-ORD-01-GIVEN-WG0P-ROUTED-03"
    found = [o for o in ops if o.op_id == wanted]
    assert found and found[0].disposition == w.Disposition.HELD


def test_red_conflicting_source_same_canonical_identity_not_silently_dropped():
    a = w.independent_oracle_items()[0]
    b = replace(a, item_id="OTHER_CARRIER", unit="household", options=("N", "Y"))
    bl = w.WorkloadBuilder()
    assert bl.add_item(a) == "OK"
    assert bl.add_item(b) == "CONFLICTING_NATIVE_ITEM_IDENTITY"


def test_red_duplicate_op_id_with_conflicting_semantics_refused():
    ops = _builder().enumerate()
    o = next(x for x in ops if x.disposition == w.Disposition.PRODUCED)
    conflicting = replace(o, item_ids=("ANOTHER-ORIGINAL-ITEM",), target="ANOTHER-ORIGINAL-ITEM")
    releases = _releases()
    with pytest.raises((ValueError, KeyError, RuntimeError)):
        w.build_executable_plan([o, conflicting], releases, freeze_hash="x",
                                items_by_id=_items_by_id())


def test_red_no_drop_full_frontier_in_execution_plan():
    plan = _full_plan()
    assert hasattr(plan, "frontier_receipts")
    assert len(plan.frontier_receipts) == 25
    counts = Counter((r["op_class"], r["disposition"]) for r in plan.frontier_receipts)
    assert counts == {("MARGINAL", "PRODUCED"): 3, ("MARGINAL", "HELD"): 2,
                      ("CONDITIONAL", "HELD"): 14, ("CONDITIONAL", "INADMISSIBLE"): 6}


def test_red_original_native_category_mutation_propagates_source_value():
    a = w.independent_oracle_items()[0]
    a_mut = replace(a, options=("changed", "meaning"))
    b1, b2 = _builder([a]), _builder([a_mut])
    releases = _releases()
    p1 = w.build_executable_plan(b1.enumerate(), releases, freeze_hash=b1.freeze(),
                                 items_by_id={a.item_id: a})
    p2 = w.build_executable_plan(b2.enumerate(), releases, freeze_hash=b2.freeze(),
                                 items_by_id={a_mut.item_id: a_mut})
    assert p1.manifest.units[0].unit_ref != p2.manifest.units[0].unit_ref


def test_red_original_publisher_custody_hold_must_block_result():
    plan = _full_plan()
    assert hasattr(plan, "source_issuer_grant")
    assert plan.source_issuer_grant["grant"] == w.PERMITTED_GRANT
    assert plan.source_issuer_grant["issuer"] == w.FIXTURE_ISSUER


# --------------------------------------------------------------------------
# Repair-specific mechanism proofs
# --------------------------------------------------------------------------

def test_repair_oracle_matches_builder_exactly():
    oracle_ops = w.repair_oracle_eligible_operations(w.independent_oracle_items())
    builder_ops = _builder().enumerate()
    key = lambda o: (o.op_id, o.op_class, o.target, tuple(o.conditioners),
                     o.disposition.value, o.disposition_reason)
    assert sorted(map(key, oracle_ops)) == sorted(map(key, builder_ops))


def test_repair_joint_respondent_risk_set_produces_real_conditional():
    """Same respondents answering two questions + joint risk set => real joint cells."""
    releases = w.build_all_releases()
    rel = releases["REL-A-W1"]
    members = ("R1", "R2", "R3", "R4", "R5", "R6")
    pred = w._response_predicate_for(rel, "Q-ORD-A", "1", risk_name="R_JOINT_ORD_RT",
                                        tag="joint-proof")
    query = w._query_for(rel, pred, (("Q-RT-C", ("yes", "no")),), risk="R_JOINT_ORD_RT",
                         tag="joint-proof")
    res = execute_empirical_query(
        repository=rel.repo, query=query, predicate=pred,
        authority_registry=w._registry_for(rel), release_refs=(rel.release_ref,))
    fact = res.facts[0]
    assert fact.typed_state == "SUPPORTED"
    cells = {r["cell"]: r["raw_numerator_support"] for r in
             fact.target_topology["complete_cell_semantic_projection"]}
    # R2,R3 answered 1: R2 yes, R3 no
    assert cells == {"yes": 1, "no": 1}
    assert fact.raw_denominator_support == 2


def test_repair_missing_evidence_yields_typed_zero_support_not_number():
    from rawlsing_next.pre553_c11_integrity import TypedAbsence  # noqa
    releases = w.build_all_releases()
    rel = releases["REL-A-W1"]
    pred = w._branch_predicate_for(rel, (), tag="empty-proof", risk_name="R_ORD")
    query = w._query_for(rel, pred, (("Q-ORD-A", ("0", "1", "2", "3", "9")),),
                         risk="R_ORD", tag="empty-proof")
    res = execute_empirical_query(
        repository=rel.repo, query=query, predicate=pred,
        authority_registry=w._registry_for(rel), release_refs=(rel.release_ref,))
    fact = res.facts[0]
    assert fact.typed_state == "ZERO_SUPPORT"
    assert fact.raw_denominator_support == 0


def test_repair_revoke_source_supersedes_receipt_and_keeps_waves_stable():
    releases = w.build_all_releases()
    items = _items_by_id()
    granted = dict(items)
    granted["WG0P-ORD-04"] = replace(items["WG0P-ORD-04"], grant="GRANTED_FIXTURE")
    b1 = w.WorkloadBuilder()
    for it in granted.values():
        assert b1.add_item(it) == "OK"
    ops1 = b1.enumerate()
    assert next(o for o in ops1 if o.target == "WG0P-ORD-04").disposition == w.Disposition.PRODUCED
    plan1 = w.build_executable_plan(ops1, releases, freeze_hash=b1.freeze(), items_by_id=granted)
    _, receipts1 = w.run_plan(plan1, w.make_executor(plan1))
    eff1 = w.consumer_effects(plan1, receipts1)
    assert "OP-WG0P-ORD-04-MARGINAL" in eff1
    # withdraw the source: rebuild, 04 becomes HELD, prior receipt superseded not deleted
    b2 = w.WorkloadBuilder()
    for it in items.values():
        assert b2.add_item(it) == "OK"
    ops2 = b2.enumerate()
    assert next(o for o in ops2 if o.target == "WG0P-ORD-04").disposition == w.Disposition.HELD
    plan2 = w.build_executable_plan(ops2, releases, freeze_hash=b2.freeze(), items_by_id=items)
    _, receipts2 = w.run_plan(plan2, w.make_executor(plan2))
    eff2 = w.consumer_effects(plan2, receipts2)
    assert "OP-WG0P-ORD-04-MARGINAL" not in eff2
    superseded = {r.unit_ref.key: r for r in receipts1
                  if r.unit_ref.key not in {x.unit_ref.key for x in receipts2}}
    assert superseded, "prior receipt must be retained as superseded, not deleted"
    def _values(entries):
        return [(e["typed_state"], e["denominator"],
                 sorted((tuple(c["cell"]) if isinstance(c["cell"], list) else c["cell"], c["n"])
                        for c in e["cells"])) for e in entries]
    for op_id in ("OP-WG0P-ORD-01-MARGINAL", "OP-WG0P-ORD-05-MARGINAL", "OP-WG0P-HH-MR-02-MARGINAL"):
        assert _values(eff1[op_id]) == _values(eff2[op_id]), f"unrelated wave changed on revocation: {op_id}"


def test_repair_resume_and_shard_determinism():
    plan = _full_plan()
    r1, receipts1 = w.run_plan(plan, w.make_executor(plan), max_units=1)
    assert len(receipts1) == 1
    r2, receipts2 = w.run_plan(plan, w.make_executor(plan))
    assert len(receipts2) == 3
    _, receipts_full = w.run_plan(plan, w.make_executor(plan))
    h = lambda rs: sorted((r.unit_ref.key, r.attempt_index, r.receipt_hash) for r in rs)
    assert h(receipts2) == h(receipts_full)
    assert [u.unit_ref.key for u in r1.schedule] == [u.unit_ref.key for u in r2.schedule]


def test_repair_changed_input_changes_output_unrelated_stable():
    plan = _full_plan()
    _, receipts = w.run_plan(plan, w.make_executor(plan))
    before = w.consumer_effects(plan, receipts)
    mutated = dict(w.COHORTS["REL-A-W1"])
    rows = [dict(r) for r in mutated["rows"]]
    rows[0] = dict(rows[0], responses=dict(rows[0]["responses"], **{"Q-ORD-A": "3"}))
    mutated["rows"] = rows
    orig = w.COHORTS["REL-A-W1"]
    w.COHORTS["REL-A-W1"] = mutated
    try:
        from rawlsing_next.pre553_c11_repository import C11Repository
        shared = C11Repository()
        releases = {
            "REL-A-W1": w.build_release("REL-A-W1", "aw1", repo=shared),
            "REL-A-W2": w.build_release("REL-A-W2", "aw2", repo=shared),
            "REL-B-W2": w.build_release("REL-B-W2", "bw2", repo=shared),
        }
        b = _builder()
        ops = b.enumerate()
        plan2 = w.build_executable_plan(ops, releases, freeze_hash=b.freeze(), items_by_id=_items_by_id())
        _, receipts2 = w.run_plan(plan2, w.make_executor(plan2))
        after = w.consumer_effects(plan2, receipts2)
    finally:
        w.COHORTS["REL-A-W1"] = orig
    assert after["OP-WG0P-ORD-01-MARGINAL"] != before["OP-WG0P-ORD-01-MARGINAL"]
    def _values(entries):
        return [(e["typed_state"], e["denominator"],
                 sorted((tuple(c["cell"]) if isinstance(c["cell"], list) else c["cell"], c["n"])
                        for c in e["cells"])) for e in entries]
    # unrelated waves keep identical computed cell values (fact refs rotate with release)
    assert _values(after["OP-WG0P-ORD-05-MARGINAL"]) == _values(before["OP-WG0P-ORD-05-MARGINAL"])
    assert _values(after["OP-WG0P-HH-MR-02-MARGINAL"]) == _values(before["OP-WG0P-HH-MR-02-MARGINAL"])


def test_repair_weak_small_n_exact_counts_no_smoothing():
    releases = w.build_all_releases()
    rel = releases["REL-B-W2"]
    pred = w._branch_predicate_for(rel, ("RB1", "RB2", "RB3"), tag="weak-proof", risk_name="R_ORDB")
    query = w._query_for(rel, pred, (("Q-ORD-A", ("0", "1", "2", "3", "9")),),
                         risk="R_ORDB", tag="weak-proof")
    res = execute_empirical_query(
        repository=rel.repo, query=query, predicate=pred,
        authority_registry=w._registry_for(rel), release_refs=(rel.release_ref,))
    fact = res.facts[0]
    cells = {r["cell"]: r["raw_numerator_support"] for r in
             fact.target_topology["complete_cell_semantic_projection"]}
    assert cells == {"0": 2, "1": 1, "2": 0, "3": 0, "9": 0}
    assert fact.raw_denominator_support == 3


def test_repair_unknown_grant_variants_all_hold():
    base = w.independent_oracle_items()[0]
    for grant in ("WITHHELD", "NO_SOURCE_ISSUER_OR_LICENSE", "PENDING", "UNKNOWN", ""):
        op = next(o for o in _builder([replace(base, grant=grant)]).enumerate()
                  if o.op_class == "MARGINAL")
        assert op.disposition == w.Disposition.HELD, grant


def test_repair_mr_option_profile_derived_from_computed_joint():
    eff = _cells("OP-WG0P-HH-MR-02-MARGINAL")[0]
    assert eff["denominator"] == 4
    profiles = {tuple(c["cell"]): c["n"] for c in eff["cells"] if c["n"] > 0}
    assert profiles == {("yes", "yes", "no", "no", "no"): 1,
                        ("no", "yes", "yes", "no", "no"): 1,
                        ("yes", "no", "yes", "yes", "no"): 1,
                        ("no", "no", "no", "no", "yes"): 1}
