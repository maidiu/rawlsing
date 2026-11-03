"""Read-only comparison of accepted GAP007 P1 family entries to R03."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile

CANDIDATE = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007')
P1_DIR = CANDIDATE / 'WORKER_RETURNS/PDEV01-GAP007/p1'
HERE = Path(__file__).resolve().parent

# Load the exact candidate P1 constructor and its test input without editing it.
spec = importlib.util.spec_from_file_location('cmp.p1', P1_DIR / 'programma_pyat_original35_constructor.py')
p1 = importlib.util.module_from_spec(spec)
sys.modules['cmp.p1'] = p1
sys.modules['rawlsing_next.programma_pyat_original35_constructor'] = p1
spec.loader.exec_module(p1)
tspec = importlib.util.spec_from_file_location('cmp.p1test', P1_DIR / 'test_programma_pyat_original35_constructor.py')
pt = importlib.util.module_from_spec(tspec)
tspec.loader.exec_module(pt)

from rawlsing_next.tests.test_universal_workload import (  # noqa: E402
    AS_OF, HOST, PURPOSE, _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.pre553_universal_workload import (  # noqa: E402
    compile_governed_frontier, execute_governed_frontier,
)


def key_material(ref):
    if ref is None:
        return None
    return ref.as_dict() if hasattr(ref, 'as_dict') else ref


def p1_sample(plan, kind, input_waves):
    operations = [op for op in plan.operations if op.operation_kind == kind]
    op = operations[0]
    item = None
    for wave in input_waves:
        for candidate in wave.items:
            if candidate.item_ref == op.item_ref:
                item = candidate
                break
    return operations, op, item


def r03_sample(op, record):
    return {
        'claim_class': op.claim_class,
        'targets': [key.material() for key in op.targets],
        'target_roles': list(op.target_roles),
        'conditions': [
            {'occurrence': key.material(), 'value': value}
            for key, value in op.conditions
        ],
        'conditioner_roles': list(op.conditioner_roles),
        'condition_mode': op.condition_mode,
        'unit': op.unit,
        'topology': op.topology,
        'state_variant': op.state_variant,
        'measure_id': op.measure_id,
        'measure_kind': op.measure_kind,
        'risk_set_ref': op.risk_set_ref,
        'risk_set_refs': list(op.risk_set_refs),
        'direction_ref': op.direction_ref,
        'form_scope': list(op.form_scope),
        'scope': op.scope,
        'branch_depth': op.branch_depth,
        'recursion_depth': op.recursion_depth,
        'baseline_ref': op.baseline_ref,
        'source_inventory': op.source_inventory,
        'source_id': op.source_id,
        'dataset_id': op.dataset_id,
        'wave': op.wave,
        'edition': op.edition,
        'source_sha256': op.source_sha256,
        'policy_id': op.policy_id,
        'policy_hash': op.policy_hash,
        'policy_grade': op.policy_grade,
        'estimand': op.estimand,
        'weight_ref': op.weight_ref,
        'design_ref': op.design_ref,
        'administration_states': list(op.administration_states),
        'lowering': {
            'status': record.status,
            'reason': record.reason,
            'family': record.family,
            'form': record.form,
            'rule_id': record.rule_id,
            'rule': record.rule,
            'predicate_refs': list(record.predicate_refs),
            'query_refs': list(record.query_refs),
        },
    }


def main():
    input_value = pt._input()
    plan = p1.construct_original35_epre(input_value)
    cond_ops, cond, cond_item = p1_sample(plan, p1.OPERATION_CONDITIONAL, input_value.waves)
    joint_ops, joint, joint_item = p1_sample(plan, p1.OPERATION_JOINT, input_value.waves)

    with tempfile.TemporaryDirectory(prefix='p1-r03-compare-') as directory:
        bundle, _ = _frontier_bundle(Path(directory) / 'r03.sav')
        inventory, policy, frontier = _frontier_fixture(bundle)
        cond_r03 = next(op for op in frontier.eligible() if op.claim_class == 'CONDITIONAL')
        joint_r03 = next(op for op in frontier.eligible() if op.claim_class == 'JOINT')
        compilation = compile_governed_frontier(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of=AS_OF, host=HOST, purpose=PURPOSE,
        )
        result = execute_governed_frontier(
            compilation=compilation,
            source_factory=lambda _ref: bundle.physical_stream,
        )
        records = {record.operation_id: record for record in compilation.plan.records}
        cond_record = records[cond_r03.op_id]
        joint_record = records[joint_r03.op_id]
        r03 = {
            'inventory_hash': inventory.content_hash,
            'policy_id': policy.policy_id,
            'policy_hash': policy.content_hash,
            'frontier_eligible_counts': {
                k: sum(1 for op in frontier.eligible() if op.claim_class == k)
                for k in ('DIST', 'CONDITIONAL', 'JOINT', 'CO_TRAVEL', 'INTERACTION', 'FORK')
            },
            'compilation_hash': compilation.content_hash,
            'execution': {
                'anti_join_no_drop_ok': result.anti_join.get('no_drop_ok'),
                'operation_no_drop_ok': result.operation_anti_join.get('no_drop_ok'),
                'receipt_refs': len(result.receipt_refs),
                'fact_refs': len(result.fact_refs),
                'native_receipts': len(result.native_execution.receipts),
                'native_result_receipts': len(result.native_execution.native_result.receipts),
            },
            'conditional': r03_sample(cond_r03, cond_record),
            'joint': r03_sample(joint_r03, joint_record),
        }

    p1_ops = {
        'conditional': {
            'count': len(cond_ops),
            'operation': cond.material(),
            'item': cond_item.material() if cond_item else None,
        },
        'joint': {
            'count': len(joint_ops),
            'operation': joint.material(),
            'item': joint_item.material() if joint_item else None,
        },
    }
    required = {
        'conditional': {
            'exact_operand_refs': [
                'R03 OccurrenceKey for target (item_id/option_id/form_id/repeat_id)',
                'R03 OccurrenceKey for each conditioner plus typed condition value',
                'R03 source_inventory and GrammarPolicy identity',
                'R03 risk_set_ref and risk_set_refs (eligibility/denominator handoff)',
                'R03 direction_ref / form_scope / scope / administration states',
                'current NativeCatalog baseline predicate and condition predicate refs',
                'current EmpiricalQuerySpec and EmpiricalPredicate refs for I03',
            ],
            'first_missing': 'exact R03 OccurrenceKey for target and conditioner; P1 supplies only SourceItem refs and source_variable_code strings',
        },
        'joint': {
            'exact_operand_refs': [
                'R03 OccurrenceKey for both targets',
                'R03 source_inventory and GrammarPolicy identity',
                'R03 risk_set_ref and risk_set_refs (eligibility/denominator handoff)',
                'R03 direction_ref / form_scope / scope / administration states',
                'current NativeCatalog joint and marginal query refs',
                'current EmpiricalQuerySpec and predicate refs for I03',
            ],
            'first_missing': 'exact R03 OccurrenceKey for both targets; P1 supplies only SourceItem refs/source codes, and no joint/marginal query refs',
        },
    }
    doc = {
        'schema': 'PDEV01_P1_R03_FAMILY_COMPARISON@1.0.0',
        'candidate_commit': 'd3d6e48791623478fd1d838c7e95a72b77b5cd74',
        'review_head': 'cb5d9b0ddefc10b42a25b168d3fea0e2c09c54ce',
        'p1_plan': {
            'plan_ref': plan.plan_ref,
            'operation_count': len(plan.operations),
            'conditional_count': len(cond_ops),
            'joint_count': len(joint_ops),
            'batch_units': len(plan.batch_units),
            'source_qualification': plan.source_qualification,
        },
        'p1': p1_ops,
        'r03': r03,
        'required': required,
        'comparison': {
            'alias': 'NO: P1 SourceItem refs and source_variable_code strings do not equal R03 OccurrenceKey identities; P1 has no option/form/repeat occurrence identity.',
            'missing_handoff': 'YES: P1 conditional/joint records lack R03 OccurrenceKey, inventory/policy, risk-set/eligibility/denominator, direction/form/scope/administration and current I03 query/predicate/joint/marginal refs.',
            'unissued_scientific_intent': 'YES: P1 conditional/joint are TEST_ONLY prospective operation classes; they have no current issued I03/I05 binding and no sourced scientific result.',
            'first_missing_input': 'exact R03 OccurrenceKey for P1 target/conditioner operands (then R03 inventory/policy/risk_set and current NativeCatalog query/predicate refs).',
        },
        'disposition': 'HOLD_MISSING_EXACT_P1_HANDOFF',
        'execution': 'R03 existing sourcefree receiver executed with its own exact inventory/frontier; P1 conditional/joint cannot be executed because the exact R03/I03 inputs above are not supplied. No predicates invented.',
        'scope': {
            'sourcefree': True, 'test_only': True, 'original_data': False,
            'production_edit': False, 'merge': False, 'ci': False, 'adoption': False,
        },
    }
    out = HERE / 'evidence' / 'COMPARISON.json'
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({
        'disposition': doc['disposition'],
        'p1_conditional': len(cond_ops), 'p1_joint': len(joint_ops),
        'r03_conditional': r03['conditional']['lowering']['status'],
        'r03_joint': r03['joint']['lowering']['status'],
        'r03_execution': r03['execution'],
        'first_missing': doc['comparison']['first_missing_input'],
        'out': str(out),
    }, indent=2))


if __name__ == '__main__':
    main()
