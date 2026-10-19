"""Native all35 scheduling controls. Every executed source is a literal fixture.

The independent original roster is used only to test nonsemantic custody; these
fixtures issue no original source, U/E_pre or scientific acceptance rights.
"""
from dataclasses import replace
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from rawlsing_next import pre553_issued_workload as w
from test_issued_workload import fixture,ref
from execute_permitted import execute_current_permitted

R=Path(__file__).resolve().parents[1]


class TestEstateResolver:
    __test__=False
    def __init__(self,frontier,records):
        self.frontier=frontier
        self.records=records
    def resolve_estate_frontier(self):
        return self.frontier
    def resolve_current(self,exact):
        return self.records[exact.key]


def estate_fixture():
    waves=json.loads((R/"original35_wave_execution_manifest.json").read_text())
    roster=w.original35_roster(waves)
    source_calls=[];persisted=[];sources={};records={}

    def packet(label,wave,**args):
        fx,p,resolver=fixture(**args)
        p=replace(p,decision_ref=ref("estate-decision-"+label),
            source_factory_ref=ref("estate-factory-"+label),original_wave_identity=wave)
        record=replace(resolver.record,decision_ref=p.decision_ref,
            envelope_sha256=w.semantic_hash(p.envelope()),original_wave_identity=wave,
            native_universe_refs=tuple(u.ref for u in p.projection.universes))
        sources[p.source_factory_ref.key]=fx["stream"]
        records[p.decision_ref.key]=record
        return p

    # Three independent named declarations precede candidate mapping/submissions.
    first=packet("first",roster[0])
    same_wave_shard=packet("same-wave-shard",roster[0],missing_weight=True)
    second_wave=packet("second-wave",roster[1],valid_empty=True)
    declarations=(first,same_wave_shard,second_wave)
    bindings=tuple(w.ExpectedWorkloadBinding(p.original_wave_identity,p.decision_ref,
        records[p.decision_ref.key].envelope_sha256) for p in declarations)
    frontier=w.IssuedEstateFrontier(ref("estate-expected"),"TEST_HOST","TEST_SOURCEFREE",
        w.semantic_hash(w.material(roster)),bindings,"CURRENT","TEST_ONLY_SOURCEFREE")
    resolver=TestEstateResolver(frontier,records)

    def factory(exact):
        source_calls.append(exact.key)
        return sources[exact.key]

    runtime=SimpleNamespace(host="TEST_HOST",purpose="TEST_SOURCEFREE",resolver=resolver,
        workloads={roster[0].atlas_id:(first,same_wave_shard),roster[1].atlas_id:second_wave},
        source_factory=factory,persist_native_result=lambda atlas,result:persisted.append((atlas,result)))
    return waves,runtime,declarations,source_calls,persisted


def test_native_estate_consumer_preserves_complete_current_packet_set():
    waves,runtime,declarations,source_calls,persisted=estate_fixture()
    result=execute_current_permitted(waves,runtime,allow_test_only=True)
    assert len(result["waves"])==35 and result["expected_permitted_packet_count"]==3
    bywave={r["atlas_id"]:r for r in result["waves"]}
    assert bywave["SRC01"]["state"]=="NATIVE_COMPLETED"
    assert bywave["SRC02"]["state"]=="NATIVE_COMPLETED"
    assert len(bywave["SRC01"]["native_packets"])==2
    expected={p.decision_ref.key for p in declarations}
    actual={w.ExactRef(**p["decision_ref"]).key for row in result["waves"] for p in row.get("native_packets",())}
    assert actual==expected
    assert len(source_calls)==len(persisted)==3
    assert all(len(native.receipts)==3 for atlas,native in persisted)
    assert all(native.original_wave_identity.atlas_id==atlas for atlas,native in persisted)
    assert all(native.route_results and native.native_outputs for atlas,native in persisted)
    assert result["original_measured_wave_count"]==0 and not result["is_scientific_completion"]
    assert result["runtime_issuance_status"]=="TEST_ONLY_SOURCEFREE_RUNTIME"
    assert result["all_supplied_wave_runs_completed"]
    assert sum(row["state"]=="NOT_YET_ISSUED" for row in result["waves"])==33


@pytest.mark.parametrize("attack",["drop_packet","duplicate_packet","equal_count_replace","drop_wave","move_wave","change_wave","change_dataset","change_family"])
def test_independent_packet_or_wave_fault_refuses_before_source_open(attack):
    waves,runtime,declarations,calls,persisted=estate_fixture()
    first,shard,second=declarations
    if attack=="drop_packet":runtime.workloads["SRC01"]=(first,)
    elif attack=="duplicate_packet":runtime.workloads["SRC01"]=(first,shard,shard)
    elif attack=="equal_count_replace":runtime.workloads["SRC01"]=(first,first)
    elif attack=="drop_wave":del runtime.workloads["SRC02"]
    elif attack=="move_wave":runtime.workloads["SRC01"],runtime.workloads["SRC02"]=(second,),(first,shard)
    else:
        field={"change_wave":"wave","change_dataset":"dataset_id","change_family":"source_family"}[attack]
        changed=replace(first.original_wave_identity,**{field:"FOREIGN"})
        runtime.workloads["SRC01"]=(replace(first,original_wave_identity=changed),shard)
    with pytest.raises(w.WorkloadAdmissionError):
        execute_current_permitted(waves,runtime,allow_test_only=True)
    assert not calls and not persisted


def test_estate_fixture_cannot_enter_original_execution():
    waves,runtime,declarations,calls,persisted=estate_fixture()
    with pytest.raises(w.WorkloadAdmissionError,match="CURRENT_ESTATE"):
        execute_current_permitted(waves,runtime)
    assert not calls


@pytest.mark.parametrize("attack",["wrong_universe","issuer_wave","revoked_one","roster_root","stale_frontier","unprovided_frontier"])
def test_current_issuer_custody_remains_separate_from_candidate_mapping(attack):
    waves,runtime,declarations,calls,persisted=estate_fixture()
    first=declarations[0]
    if attack in {"wrong_universe","issuer_wave","revoked_one"}:
        old=runtime.resolver.records[first.decision_ref.key]
        changes={"wrong_universe":{"native_universe_refs":(ref("FOREIGN_UNIVERSE"),)},
            "issuer_wave":{"original_wave_identity":declarations[-1].original_wave_identity},
            "revoked_one":{"currentness":"WITHDRAWN"}}[attack]
        runtime.resolver.records[first.decision_ref.key]=replace(old,**changes)
        result=execute_current_permitted(waves,runtime,allow_test_only=True)
        row=next(row for row in result["waves"] if row["atlas_id"]=="SRC01")
        assert row["state"]=="HOLD__NAMED_OWNER_DECISION"
        assert len(calls)==len(persisted)==2
        assert first.source_factory_ref.key not in calls
        assert result["original_measured_wave_count"]==0
        assert not result["all_supplied_wave_runs_completed"]
    else:
        frontier=runtime.resolver.frontier
        if attack=="roster_root":runtime.resolver.frontier=replace(frontier,roster_identity="0"*64)
        elif attack=="stale_frontier":runtime.resolver.frontier=replace(frontier,currentness="WITHDRAWN")
        else:runtime.resolver=SimpleNamespace(resolve_current=runtime.resolver.resolve_current)
        with pytest.raises(w.WorkloadAdmissionError):
            execute_current_permitted(waves,runtime,allow_test_only=True)
        assert not calls


def test_no_runtime_preserves_original35_unissued_denominator():
    waves=json.loads((R/"original35_wave_execution_manifest.json").read_text())
    result=execute_current_permitted(waves)
    assert len(result["waves"])==35 and result["original_measured_wave_count"]==0
    assert result["expected_permitted_packet_count"] is None and result["U_E_pre_count"] is None
    assert all(row["state"]=="NOT_YET_ISSUED" for row in result["waves"])
