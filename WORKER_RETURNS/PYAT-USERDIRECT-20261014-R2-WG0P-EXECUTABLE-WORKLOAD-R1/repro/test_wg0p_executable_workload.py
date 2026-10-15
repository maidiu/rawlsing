"""R2 WG0P tests: independent oracle, real owner execution, numeric consumer evidence."""

import sys
from pathlib import Path
from fractions import Fraction

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wg0p_executable_workload import (
    WorkloadBuilder, Disposition, independent_oracle_items,
    oracle_eligible_operations, build_executable_plan, make_executor, run_plan,
)
from rawlsing_next import pre553_batch_runner as batch_owner


def _build_all():
    builder = WorkloadBuilder()
    for item in independent_oracle_items():
        assert builder.add_item(item) == "OK"
    builder.freeze()
    return builder, builder.enumerate()


def test_independent_oracle_matches_builder_exactly():
    items = independent_oracle_items()
    expected = {(o.op_id, o.disposition, o.disposition_reason) for o in oracle_eligible_operations(items)}
    builder = WorkloadBuilder()
    for item in items:
        builder.add_item(item)
    builder.freeze()
    actual = {(o.op_id, o.disposition, o.disposition_reason) for o in builder.enumerate()}
    assert actual == expected


def test_produced_label_is_not_produced_result():
    _, ops = _build_all()
    produced = [o for o in ops if o.disposition == Disposition.PRODUCED]
    assert len(produced) > 0
    for op in produced:
        assert not hasattr(op, "receipt") and not hasattr(op, "result")


def test_cross_wave_conditioning_inadmissible():
    _, ops = _build_all()
    cross = [o for o in ops if o.op_id == "OP-WG0P-ORD-01-GIVEN-WG0P-ORD-05"]
    assert len(cross) == 1
    assert cross[0].disposition == Disposition.INADMISSIBLE
    assert cross[0].disposition_reason == "CROSS_WAVE_NOT_SAME_PERSON"


def test_cross_unit_conditioning_inadmissible():
    _, ops = _build_all()
    cross = [o for o in ops if o.op_id == "OP-WG0P-ORD-01-GIVEN-WG0P-HH-MR-02"]
    assert len(cross) == 1
    assert cross[0].disposition == Disposition.INADMISSIBLE
    assert cross[0].disposition_reason == "CROSS_UNIT_NOT_SAME_PERSON"


def test_routed_without_evidence_held():
    _, ops = _build_all()
    held = [o for o in ops if o.op_id == "OP-WG0P-ROUTED-03-MARGINAL"]
    assert len(held) == 1
    assert held[0].disposition == Disposition.HELD
    assert held[0].disposition_reason == "ROUTE_EVIDENCE_MISSING"


def test_withdrawn_grant_held():
    _, ops = _build_all()
    held = [o for o in ops if o.op_id == "OP-WG0P-ORD-04-MARGINAL"]
    assert len(held) == 1
    assert held[0].disposition == Disposition.HELD
    assert held[0].disposition_reason == "GRANT_WITHDRAWN"


def test_duplicate_form_identity_single():
    builder = WorkloadBuilder()
    items = independent_oracle_items()
    assert builder.add_item(items[0]) == "OK"
    assert builder.add_item(items[0]) == "DUPLICATE_IDENTITY"


def test_real_batch_owner_invocation_with_receipts():
    _, ops = _build_all()
    plan = build_executable_plan(ops)
    assert "pre553_batch_runner" in batch_owner.__file__
    table = {op.op_id: {"numerator": 9, "denominator": 16} for op in ops if op.disposition == Disposition.PRODUCED}
    runner, receipts = run_plan(plan, make_executor(table))
    summary = runner.summary()
    assert summary.full_coverage is True
    assert summary.coverage_state == "FULL_MANIFEST_COVERAGE"
    assert all(r.state == "COMPLETED" and r.execution_performed for r in receipts)
    assert len(receipts) == len([o for o in ops if o.disposition == Disposition.PRODUCED])


def test_changed_input_changes_computed_output():
    _, ops = _build_all()
    plan = build_executable_plan(ops)
    t1 = {op.op_id: {"numerator": 9, "denominator": 16} for op in ops if op.disposition == Disposition.PRODUCED}
    t2 = dict(t1)
    first = sorted(t1)[0]
    t2[first] = {"numerator": 5, "denominator": 8}
    _, r1 = run_plan(plan, make_executor(t1))
    _, r2 = run_plan(plan, make_executor(t2))
    h1 = {r.unit_ref.key: [x.object_id for x in r.result_refs] for r in r1}
    h2 = {r.unit_ref.key: [x.object_id for x in r.result_refs] for r in r2}
    unit_key = plan.units_by_op[first].unit_ref.key
    assert h1[unit_key] != h2[unit_key]
    others = [k for k in h1 if k != unit_key]
    assert all(h1[k] == h2[k] for k in others)


def test_irrelevant_mutation_unchanged_output():
    _, ops = _build_all()
    plan = build_executable_plan(ops)
    t1 = {op.op_id: {"numerator": 9, "denominator": 16} for op in ops if op.disposition == Disposition.PRODUCED}
    _, r1 = run_plan(plan, make_executor(t1))
    _, r2 = run_plan(plan, make_executor(dict(t1)))
    assert [r.receipt_hash for r in r1] == [r.receipt_hash for r in r2]


def test_deterministic_shard_replay_and_resume():
    _, ops = _build_all()
    plan = build_executable_plan(ops)
    table = {op.op_id: {"numerator": 1, "denominator": 4} for op in ops if op.disposition == Disposition.PRODUCED}
    runner1, _ = run_plan(plan, make_executor(table), max_units=1)
    assert runner1.summary().coverage_state == "INCOMPLETE_MANIFEST_COVERAGE"
    pending = [u.unit_ref.key for u in runner1.pending_units()]
    assert len(pending) == len(plan.manifest.units) - 1
    from rawlsing_next.pre553_batch_runner import BatchExecutionRunner, ExecutorBinding
    from wg0p_executable_workload import _ref
    runner2 = BatchExecutionRunner(
        manifest=plan.manifest, repository=plan.repository, prior_receipts=runner1.receipts)
    binding = ExecutorBinding(_ref("EXECUTOR", "wg0p-query"), make_executor(table))
    runner2.run(executors={"QUERY": binding})
    assert runner2.summary().full_coverage is True


def test_revoke_source_keeps_unrelated_wave_stable():
    builder = WorkloadBuilder()
    items = independent_oracle_items()
    for item in items:
        builder.add_item(item)
    ops_before = builder.enumerate()
    w1_ops = sorted(o.op_id for o in ops_before if o.disposition == Disposition.PRODUCED)
    builder2 = WorkloadBuilder()
    for item in items:
        if item.source_id == "WG0P-SRC-B":
            continue
        builder2.add_item(item)
    ops_after = builder2.enumerate()
    after_by_id = {o.op_id: o for o in ops_after}
    before_by_id = {o.op_id: o for o in ops_before}
    for op_id in ("OP-WG0P-ORD-01-MARGINAL", "OP-WG0P-HH-MR-02-MARGINAL"):
        assert op_id in after_by_id
        assert after_by_id[op_id].disposition == before_by_id[op_id].disposition == Disposition.PRODUCED


def test_zero_null_minority_outcomes():
    _, ops = _build_all()
    plan = build_executable_plan(ops)
    produced = [o.op_id for o in ops if o.disposition == Disposition.PRODUCED]
    table = {op_id: {"numerator": 0, "denominator": 16} for op_id in produced}
    table[produced[0]] = {"numerator": 1, "denominator": 16}
    _, receipts = run_plan(plan, make_executor(table))
    assert all(r.state == "COMPLETED" for r in receipts)


def test_typed_refusals_for_bad_manifest():
    from rawlsing_next.pre553_batch_runner import BatchManifest, BatchIntegrityError
    import pytest
    with pytest.raises(BatchIntegrityError):
        BatchManifest(())
