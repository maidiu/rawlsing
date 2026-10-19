"""Sourcefree admission/transport, never a surrogate original35 qualification."""
import copy
from dataclasses import replace
import json
import sys

import pytest

from rawlsing_next import pre553_issued_workload as w
from rawlsing_next.tests.test_pre553_route_b_production import _fixture
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest


def ref(label):
    return ExactRef("TEST_ONLY", "urn:test:u43:"+label, semantic_hash(label))


class TestOnlyResolver:
    __test__ = False
    def __init__(self, record):
        self.record = record
    def resolve_current(self, exact):
        if exact != self.record.decision_ref:
            raise w.WorkloadAdmissionError("UNKNOWN_TEST_ONLY_ISSUANCE")
        return self.record


def fixture(**args):
    fx = _fixture(**args)
    p = fx["projection"]
    desc = dict(source_edition=p.instrument_release_id,
        native_item_ids=[q.native_question_ref.as_dict() for q in p.questions],
        release_tag=p.release_id, routing_and_risk=w.material(p.routing),
        carrier=w.material(p.row_bindings),
        country_and_population=[u.semantic_projection() for u in p.universes],
        weight_design_estimand=w.material(p.weight_slots),
        missing_and_occurrence_policy=w.material(p.response_slots),
        target_conditioner_roles=[fx["raw_query"].semantic_projection(),fx["weighted_query"].semantic_projection()])
    requests = tuple(I03ExecutionRequest(q.ref, fx["all_p"].ref) for q in (fx["raw_query"], fx["weighted_query"]))
    # Independent named fixture declarations, not enumeration of emitted requests.
    jobs = tuple(sorted([
        ("QUERY", fx["raw_query"].ref.key, fx["all_p"].ref.key),
        ("QUERY", fx["weighted_query"].ref.key, fx["all_p"].ref.key),
        ("DISCOVERY", fx["discovery_authority"].ref.key, ""),
    ]))
    workload = w.NativeWorkload(ref("decision"),ref("source-factory"),w.canonical(desc),p,fx["catalog"],
        requests,(fx["discovery_authority"].ref,),semantic_hash(desc["native_item_ids"]),semantic_hash(jobs))
    record = w.IssuedWorkloadRecord(workload.decision_ref,ref("source-permission"),(ref("science-permission"),),
        "TEST_HOST", "TEST_SOURCEFREE",fx["stream"].source_sha256,semantic_hash(workload.envelope()),
        workload.original_u_root,workload.expected_frontier_root,jobs,"CURRENT_GRANTED","TEST_ONLY_SOURCEFREE")
    return fx,workload,TestOnlyResolver(record)


def execute(workload,resolver,fx,**args):
    return w.execute_issued_workload(workload,resolver,source_factory=lambda exact:fx["stream"],
        host="TEST_HOST",purpose="TEST_SOURCEFREE",allow_test_only=True,**args)


@pytest.mark.parametrize("missing_weight,valid_empty",[(False,False),(True,False),(False,True)])
def test_real_native_route_batch_receipts_and_complete_expected_set(missing_weight,valid_empty):
    fx,p,resolver=fixture(missing_weight=missing_weight,valid_empty=valid_empty)
    calls=[]
    def trace(frame,event,arg):
        if event=="call" and frame.f_code.co_name in {"execute_route_b_production","execute_empirical_query","execute_exact_bounded_discovery","run"}:
            calls.append((frame.f_code.co_filename,frame.f_code.co_name))
    sys.setprofile(trace)
    try: result=execute(p,resolver,fx)
    finally: sys.setprofile(None)
    assert len(result.manifest.units)==len(result.receipts)==3
    assert all(r.state=="COMPLETED" for r in result.receipts)
    assert result.scope=="TEST_ONLY_SOURCEFREE"
    assert {"execute_route_b_production","execute_empirical_query","execute_exact_bounded_discovery","run"} <= {n for f,n in calls}
    assert result.route_results[0].i03_results
    assert all(p.decision_ref in r.provenance_refs for r in result.receipts)
    facts=[f for out in result.route_results[0].i03_results for f in out.facts]
    if missing_weight: assert any(f.typed_state=="UNAVAILABLE" for f in facts)


@pytest.mark.parametrize("field",sorted(w.DESCRIPTOR_FIELDS))
def test_each_complete_descriptor_field_refused_before_source_or_native_call(field):
    fx,p,resolver=fixture();desc=json.loads(p.descriptor);desc[field]="CALLER_FORGED"
    forged=replace(p,descriptor=w.canonical(desc));source_calls=[]
    # Caller may calculate any new digest, but the resolver retains the issued record.
    assert semantic_hash(forged.envelope()) != resolver.record.envelope_sha256
    with pytest.raises(w.WorkloadAdmissionError,match="ISSUED_ENVELOPE"):
        w.execute_issued_workload(forged,resolver,source_factory=lambda ref:source_calls.append(ref),
            host="TEST_HOST",purpose="TEST_SOURCEFREE",allow_test_only=True)
    assert not source_calls


@pytest.mark.parametrize("attack",["omit","equal_count_swap","duplicate","root","permission","host","purpose","authority_snapshot","population","missing","carrier","weight"])
def test_source_native_closure_or_scope_fault_refuses_early(attack):
    fx,p,resolver=fixture()
    if attack=="omit": p=replace(p,requests=p.requests[:-1])
    elif attack=="equal_count_swap": p=replace(p,requests=(p.requests[0],I03ExecutionRequest(p.requests[0].query_ref,p.requests[0].predicate_ref)))
    elif attack=="duplicate": p=replace(p,requests=(*p.requests,p.requests[0]))
    elif attack=="root": p=replace(p,expected_frontier_root="0"*64)
    elif attack=="permission":resolver.record=replace(resolver.record,currentness="WITHDRAWN")
    elif attack=="host":resolver.record=replace(resolver.record,host="FOREIGN")
    elif attack=="purpose":resolver.record=replace(resolver.record,purpose="FOREIGN")
    elif attack=="authority_snapshot":
        a=p.catalog.authorities[0];p=replace(p,catalog=replace(p.catalog,authorities=p.catalog.authorities[1:]))
    elif attack=="population":
        u=p.projection.universes[0];fields=w.material(u.semantic_fields);fields["target_population_and_sample_frame"]="FOREIGN_POPULATION"
        changed=type(u)(typed_state=u.typed_state,authority_snapshot_refs=u.authority_snapshot_refs,
            dependency_refs=u.dependency_refs,producer_replay_locator_or_reference_root=u.producer_replay_locator_or_reference_root,**fields)
        p=replace(p,projection=replace(p.projection,universes=(changed,)))
    elif attack=="missing":
        rule=p.projection.response_slots[0]
        p=replace(p,projection=replace(p.projection,response_slots=(replace(rule,values=()),*p.projection.response_slots[1:])))
    elif attack=="carrier":
        row=p.projection.row_bindings[0]
        p=replace(p,projection=replace(p.projection,row_bindings=(replace(row,row_ordinal=99),*p.projection.row_bindings[1:])))
    elif attack=="weight":p=replace(p,projection=replace(p.projection,weight_slots=()))
    source_calls=[]
    with pytest.raises(w.WorkloadAdmissionError):
        w.execute_issued_workload(p,resolver,source_factory=lambda ref:source_calls.append(ref),host="TEST_HOST",purpose="TEST_SOURCEFREE",allow_test_only=True)
    assert not source_calls


def test_fixture_cannot_enter_original_source_default():
    fx,p,resolver=fixture()
    with pytest.raises(w.WorkloadAdmissionError,match="COMPETENT_SOURCE"):
        w.admit(p,resolver,host="TEST_HOST",purpose="TEST_SOURCEFREE")


def test_wrong_physical_source_factory_hash_refuses():
    fx,p,resolver=fixture()
    fx["stream"]=replace(fx["stream"],source_sha256="f"*64)
    with pytest.raises(w.WorkloadAdmissionError,match="WRONG_EDITION"):
        execute(p,resolver,fx)


def test_native_partial_preserves_maximal_manifest():
    fx,p,resolver=fixture();result=execute(p,resolver,fx,max_units=1)
    assert len(result.manifest.units)==3 and len(result.receipts)==1


def test_currentness_rechecked_after_source_factory():
    fx,p,resolver=fixture()
    def revoked_factory(ref):
        resolver.record=replace(resolver.record,currentness="WITHDRAWN")
        return fx["stream"]
    with pytest.raises(w.WorkloadAdmissionError,match="COMPETENT_SOURCE"):
        w.execute_issued_workload(p,resolver,source_factory=revoked_factory,
            host="TEST_HOST",purpose="TEST_SOURCEFREE",allow_test_only=True)


def test_consumer_cannot_execute_copied_issued_descriptor():
    fx,p,resolver=fixture()
    original=execute(p,resolver,fx)
    assert len(original.receipts)==3
    desc=json.loads(p.descriptor);desc["source_edition"]="FORGED_CALLER_EDITION"
    altered=replace(p,descriptor=w.canonical(desc));calls=[];error=None
    def factory(ref):
        calls.append(ref)
        return fx["stream"]
    try:
        w.execute_issued_workload(altered,resolver,source_factory=factory,
            host="TEST_HOST",purpose="TEST_SOURCEFREE",allow_test_only=True)
    except w.WorkloadAdmissionError as exc:error=exc
    assert isinstance(error,w.WorkloadAdmissionError), "Copied unissued descriptor reached the native consumer"
    assert not calls


def test_query_only_scope_returns_native_fact_preimages():
    fx,p,resolver=fixture()
    expected=tuple(sorted([
        ("QUERY",fx["raw_query"].ref.key,fx["all_p"].ref.key),
        ("QUERY",fx["weighted_query"].ref.key,fx["all_p"].ref.key),
    ]))
    p=replace(p,discoveries=(),expected_frontier_root=semantic_hash(expected))
    # Explicit test-only issuer fixture, before execution; never original authority.
    resolver.record=replace(resolver.record,expected_jobs=expected,
        expected_frontier_root=p.expected_frontier_root,envelope_sha256=semantic_hash(p.envelope()))
    result=execute(p,resolver,fx)
    assert len(result.manifest.units)==len(result.native_outputs)==2
    facts=[f for output in result.native_outputs for f in output.facts]
    assert facts and {f.ref for f in facts}==set(result.output_refs)
