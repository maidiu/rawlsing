"""Independent WG0I sourcefree candidate court. EXACT WG0P code blob is imported.

Owner modules are isolated EXPLICIT TEST STUBS, NOT accepted PRE553 modules.
This court verifies candidate enumeration, grant predicates, identities,
fallback computations and construction boundary. It does not qualify WG0P's
14 claimed accepted-owner tests or invoke original C11/I03/I05.
"""
from __future__ import annotations
import sys, types, hashlib
from pathlib import Path
from dataclasses import dataclass, replace
from fractions import Fraction
from collections import Counter

import pytest

# Test-only import closure. It deliberately does not pretend to implement
# BatchExecutionRunner or any original PRE553 authority; executing it raises.
root = types.ModuleType('rawlsing_next'); root.__path__ = []
objects = types.ModuleType('rawlsing_next.pre553_empirical_objects')
@dataclass(frozen=True)
class ExactRef:
    kind: str
    object_id: str
    content_hash: str
    @property
    def key(self): return f'{self.kind}|{self.object_id}|{self.content_hash}'
objects.ExactRef = ExactRef
batch = types.ModuleType('rawlsing_next.pre553_batch_runner')
class BatchIntegrityError(ValueError): pass
@dataclass(frozen=True)
class BatchUnitSpec:
    job_kind: str
    job_ref: ExactRef
    release_refs: tuple
    semantic_input_refs: tuple
    @property
    def unit_ref(self):
        return ExactRef('UNIT', self.job_ref.object_id, self.job_ref.content_hash)
@dataclass
class BatchManifest:
    units: tuple
@dataclass
class ExecutionOutcome:
    result_refs: tuple
    provenance_refs: tuple
@dataclass
class ExecutorBinding:
    ref: ExactRef
    executor: object
class BatchExecutionRunner:
    def __init__(self,*a,**k): raise RuntimeError('NOT_QUALIFIED_ACCEPTED_OWNER_RUNTIME')
for k in ('BatchIntegrityError','BatchUnitSpec','BatchManifest','ExecutionOutcome','ExecutorBinding','BatchExecutionRunner'):
    setattr(batch,k,globals()[k])
repo = types.ModuleType('rawlsing_next.pre553_c11_repository')
class C11Repository:
    def __init__(self): self._by_ref={}
repo.C11Repository = C11Repository
sys.modules.update({'rawlsing_next':root,'rawlsing_next.pre553_empirical_objects':objects,
                    'rawlsing_next.pre553_batch_runner':batch,'rawlsing_next.pre553_c11_repository':repo})
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wg0p_executable_workload as w


def builder(items=None):
    b=w.WorkloadBuilder()
    for item in (w.independent_oracle_items() if items is None else items):
        assert b.add_item(item)=='OK'
    return b


def operations():
    b=builder(); b.freeze(); return b.enumerate()


def make_same_respondent_items():
    a=w.independent_oracle_items()[0]
    b=replace(a,item_id='OTHER-RESPONDENT-FORM',form_id='Q-OTHER',options=('N','Y'))
    return a,b


def execute_direct(op=None, values=None):
    if op is None: op=next(o for o in operations() if o.disposition==w.Disposition.PRODUCED)
    plan=w.build_executable_plan([op])
    unit=plan.units_by_op[op.op_id]
    return w.make_executor({} if values is None else values)(unit)


def test_control_exact_candidate_file_and_frozen_inventory():
    assert w.__file__ == str(Path(__file__).parent / 'wg0p_executable_workload.py')
    assert len(w.independent_oracle_items()) == 5
    ops=operations(); counts=Counter((o.op_class,o.disposition.value) for o in ops)
    assert counts == {('MARGINAL','PRODUCED'):3,('MARGINAL','HELD'):2,('CONDITIONAL','INADMISSIBLE'):10}
    assert len(ops)==15


def test_control_manifest_exactly_three_marginals_and_injected_c11_occupant():
    plan=w.build_executable_plan(operations())
    assert len(plan.manifest.units)==3
    assert all(u.job_kind=='QUERY' for u in plan.manifest.units)
    assert len(plan.repository._by_ref)==1
    assert type(next(iter(plan.repository._by_ref.values()))) is object


def test_control_fallback_is_exact_half_but_unqualified():
    out=execute_direct()
    assert out.result_refs[0].object_id.endswith(':1/2')
    assert out.provenance_refs[0].kind=='EXECUTION_TRACE'


def test_control_synthetic_zero_and_minority():
    op=next(o for o in operations() if o.disposition==w.Disposition.PRODUCED)
    for n,d,expect in [(0,16,'0/1'),(1,16,'1/16')]:
        out=execute_direct(op,{op.op_id:{'numerator':n,'denominator':d}})
        assert expect in out.result_refs[0].object_id


def test_control_frozen_builder_rejects_new_item():
    b=builder();b.freeze()
    assert b.add_item(replace(w.independent_oracle_items()[0],form_id='NEW'))=='FRONTIER_FROZEN'


# Deliberately failing acceptance guards: each records a scientifically
# required refusal/retention that exact WG0P source lacks.

def test_red_missing_operation_payload_must_fail_closed():
    with pytest.raises((KeyError,ValueError,LookupError)):
        execute_direct(values={})


def test_red_invalid_negative_observation_must_fail_closed():
    op=next(o for o in operations() if o.disposition==w.Disposition.PRODUCED)
    with pytest.raises((ValueError,TypeError)):
        execute_direct(op,{op.op_id:{'numerator':-1,'denominator':16}})


def test_red_no_c11_release_without_validated_c11logicalrelease():
    plan=w.build_executable_plan(operations())
    assert all(type(x).__name__=='C11LogicalRelease' for x in plan.repository._by_ref.values())


def test_red_no_condition_without_joined_respondent_risk_set():
    a,b=make_same_respondent_items()
    ops=builder([a,b]).enumerate()
    assert not [o for o in ops if o.op_class=='CONDITIONAL' and o.disposition==w.Disposition.PRODUCED]


def test_red_unknown_source_rights_must_hold():
    orig=w.independent_oracle_items()[0]
    it=replace(orig,grant='WITHHELD')
    op=next(o for o in builder([it]).enumerate() if o.op_class=='MARGINAL')
    assert op.disposition==w.Disposition.HELD


def test_red_arbitrary_grant_token_must_not_be_permission():
    it=replace(w.independent_oracle_items()[0],grant='NO_SOURCE_ISSUER_OR_LICENSE')
    assert builder([it]).enumerate()[0].disposition==w.Disposition.HELD


def test_red_freeze_must_bind_original_native_options():
    it=w.independent_oracle_items()[0]
    before=builder([it]).freeze()
    changed=builder([replace(it,options=('changed-native-category',))]).freeze()
    assert before!=changed


def test_red_freeze_must_bind_source_permission_status():
    it=w.independent_oracle_items()[0]
    before=builder([it]).freeze()
    changed=builder([replace(it,grant='WITHDRAWN')]).freeze()
    assert before!=changed


def test_red_withdrawn_conditioning_pair_must_retained_as_held():
    items=w.independent_oracle_items()
    ops=builder(items).enumerate()
    wanted='OP-WG0P-ORD-01-GIVEN-WG0P-ORD-04'
    found=[o for o in ops if o.op_id==wanted]
    assert found and found[0].disposition==w.Disposition.HELD


def test_red_routed_unknown_pair_must_retain_as_held():
    items=w.independent_oracle_items()
    ops=builder(items).enumerate()
    wanted='OP-WG0P-ORD-01-GIVEN-WG0P-ROUTED-03'
    found=[o for o in ops if o.op_id==wanted]
    assert found and found[0].disposition==w.Disposition.HELD


def test_red_conflicting_source_same_canonical_identity_not_silently_dropped():
    a=w.independent_oracle_items()[0]
    b=replace(a,item_id='OTHER_CARRIER',unit='household',options=('N','Y'))
    bl=w.WorkloadBuilder();assert bl.add_item(a)=='OK'
    assert bl.add_item(b)=='CONFLICTING_NATIVE_ITEM_IDENTITY'


def test_red_duplicate_op_id_with_conflicting_semantics_refused():
    ops=operations(); o=next(x for x in ops if x.disposition==w.Disposition.PRODUCED)
    conflicting=replace(o,item_ids=('ANOTHER-ORIGINAL-ITEM',),target='ANOTHER-ORIGINAL-ITEM')
    with pytest.raises((ValueError,KeyError,RuntimeError)):
        w.build_executable_plan([o,conflicting])


def test_red_no_drop_full_frontier_in_execution_plan():
    ops=operations();plan=w.build_executable_plan(ops)
    assert hasattr(plan, 'frontier_receipts')  # A frozen no-drop ledger for held/inadmissible items is absent from the returned plan.


def test_red_original_native_category_mutation_propagates_source_value():
    a=w.independent_oracle_items()[0]
    orig_ops=builder([a]).enumerate()
    mut_ops=builder([replace(a,options=('changed','meaning'))]).enumerate()
    p1=w.build_executable_plan(orig_ops)
    p2=w.build_executable_plan(mut_ops)
    assert p1.manifest.units[0].unit_ref != p2.manifest.units[0].unit_ref


def test_red_original_publisher_custody_hold_must_block_result():
    op=next(x for x in operations() if x.disposition==w.Disposition.PRODUCED)
    plan=w.build_executable_plan([op])
    assert hasattr(plan, 'source_issuer_grant')  # No positive authority provenance travels with this executable plan.
