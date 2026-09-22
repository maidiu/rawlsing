from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from rawlsing_next.fiabc_live_accounting_binding import (
    LiveAccountingError,
    PARENTAGE_SCHEMA,
    require_derivative_parentage,
)
from rawlsing_next.fiabc_telemetry_semantics import (
    CellIdentity, CostClass, MetricState, ObservationContext, TelemetryContractError, TelemetryLedger
)
from rawlsing_next.fiabc_lifecycle_accounting import (
    ActionObservation, AccountingContractError, CallableLifecycleActionAdapter,
    CallableTelemetryAdapter, EvidenceKind, LifecycleAction, LifecycleActionRequest,
    LifecycleBinding, ProcessIsolationReceipt, TelemetryMetric, MetricState as LifeMetricState,
    execute_lifecycle_action,
)

SHA="a"*64

def cell(candidate="A"):
    return CellIdentity("LITS_I",SHA,candidate,"workload","authority")

def ctx(candidate="A", phase="S04", token="proc-A"):
    return ObservationContext("LITS_I",SHA,candidate,phase,token,CostClass.C2)

def test_cross_candidate_metrics_cannot_leak():
    ledger=TelemetryLedger(cell("A"))
    with pytest.raises(TelemetryContractError):
        ledger.record_observed_value("audit_wall_ns",ctx("B"),1,evidence_kind="OBSERVED")

def test_metric_overwrite_fails():
    ledger=TelemetryLedger(cell())
    ledger.record_observed_value("audit_wall_ns",ctx(),1,evidence_kind="OBSERVED")
    with pytest.raises(TelemetryContractError):
        ledger.record_observed_value("audit_wall_ns",ctx(),2,evidence_kind="OBSERVED")

def test_missing_metric_is_typed_null_not_zero():
    rec=TelemetryLedger(cell()).receipt(candidate_semantic_state="UNCHANGED")
    m=rec["metrics"]["bytes_read"]
    assert m["state"]==MetricState.MEASUREMENT_NOT_CAPTURED.value
    assert m["value"] is None

def test_endpoint_size_is_not_observed_io():
    ledger=TelemetryLedger(cell())
    c=ctx()
    ledger.observe_io(c,operation="READ",byte_count=7,object_id="source")
    # Endpoint size 9000 is irrelevant; without a complete event stream bytes_read stays null.
    rec=ledger.receipt(candidate_semantic_state="UNCHANGED")
    assert rec["metrics"]["bytes_read"]["value"] is None

def test_scratch_endpoint_is_not_peak():
    ledger=TelemetryLedger(cell())
    c=ctx()
    ledger.observe_scratch_size(c,object_id="a",current_size_bytes=100)
    ledger.observe_scratch_size(c,object_id="a",current_size_bytes=10)
    ledger.seal_scratch_accounting(c)
    assert ledger.receipt(candidate_semantic_state="UNCHANGED")["metrics"]["peak_scratch_bytes"]["value"]==100

def life_binding():
    iso=ProcessIsolationReceipt("LITS_I","A","proc-A","root-A",True,False,"i06a")
    return LifecycleBinding("LITS_I",SHA,"A","owner","workload","authority","runtime","state","terminal",iso)

def execute_bad(kind):
    b=life_binding()
    r=LifecycleActionRequest(b,LifecycleAction.STALE_STATE_RECOVERY,"stale-op",())
    o=ActionObservation(
        action=r.action,binding_id=b.binding_id,source_id="LITS_I",candidate_id="A",
        performed=True,evidence_kind=kind,action_id="action",state_before_id="before",
        state_after_id="after",terminal_identity="terminal",
        stale_determinant_before="d1",stale_determinant_after="d2",
        stale_detected=True,recovery_performed=True,
    )
    with pytest.raises(AccountingContractError):
        execute_lifecycle_action(r,CallableLifecycleActionAdapter(lambda _:o),
                                 CallableTelemetryAdapter(lambda *_:()))

def test_formula_estimated_rebuild_or_lifecycle_does_not_count_as_executed():
    execute_bad(EvidenceKind.FORMULA_DERIVED)

def test_law_hash_is_not_stale_or_corrupt_exercise():
    execute_bad(EvidenceKind.LAW_HASH_ONLY)

def test_temp_file_trick_is_not_interruption_recovery():
    b=life_binding()
    r=LifecycleActionRequest(b,LifecycleAction.INTERRUPTION_RECOVERY,"real-op",())
    o=ActionObservation(
        action=r.action,binding_id=b.binding_id,source_id="LITS_I",candidate_id="A",
        performed=True,evidence_kind=EvidenceKind.GENERIC_TEMP_FILE,action_id="action",
        state_before_id="before",state_after_id="after",terminal_identity="terminal",
        candidate_state_object_ids_before=("state",),candidate_state_object_ids_after=("state",),
        interrupted_operation_id="real-op",interrupted_candidate_state_id="state",
        interruption_injected=True,recovered_operation_id="real-op",recovery_performed=True,
    )
    with pytest.raises(AccountingContractError):
        execute_lifecycle_action(r,CallableLifecycleActionAdapter(lambda _:o),
                                 CallableTelemetryAdapter(lambda *_:()))

def test_invalid_warm_state_reuse_fails():
    b=life_binding()
    r=LifecycleActionRequest(b,LifecycleAction.WARM_RETAINED_STATE_USE,"warm",())
    o=ActionObservation(
        action=r.action,binding_id=b.binding_id,source_id="LITS_I",candidate_id="A",
        performed=True,evidence_kind=EvidenceKind.EXECUTED_CANDIDATE_ACTION,action_id="action",
        state_before_id="before",state_after_id="after",terminal_identity="terminal",
        candidate_state_object_ids_before=(),candidate_state_object_ids_after=(),
        retained_state_id="foreign",retained_state_candidate_id="A",
    )
    with pytest.raises(AccountingContractError):
        execute_lifecycle_action(r,CallableLifecycleActionAdapter(lambda _:o),
                                 CallableTelemetryAdapter(lambda *_:()))

def test_wrong_terminal_identity_after_replay_fails():
    b=life_binding()
    r=LifecycleActionRequest(b,LifecycleAction.FRESH_PROCESS_REPLAY,"replay",())
    o=ActionObservation(
        action=r.action,binding_id=b.binding_id,source_id="LITS_I",candidate_id="A",
        performed=True,evidence_kind=EvidenceKind.EXECUTED_CANDIDATE_ACTION,action_id="action",
        state_before_id="before",state_after_id="after",terminal_identity="WRONG",
        parent_process_token="p",replay_process_token="q",
    )
    with pytest.raises(AccountingContractError):
        execute_lifecycle_action(r,CallableLifecycleActionAdapter(lambda _:o),
                                 CallableTelemetryAdapter(lambda *_:()))

def test_derivative_without_sufficient_parentage_cannot_receive_credit(tmp_path):
    derivative={"kind":"R5","release":"x"}
    with pytest.raises(LiveAccountingError):
        require_derivative_parentage(tmp_path/"missing.json",derivative_identity=derivative,canonical_source_sha256=SHA)
    p=tmp_path/"bad.json"
    p.write_text(json.dumps({
        "schema":PARENTAGE_SCHEMA,"derivative_identity":derivative,
        "canonical_source_sha256":SHA,
        "governed_producer_identity":"producer",
        "governed_operation_identity":"",
        "governed_config_identity":"config",
        "evidence_refs":["evidence"],
    }))
    with pytest.raises(LiveAccountingError):
        require_derivative_parentage(p,derivative_identity=derivative,canonical_source_sha256=SHA)


def test_child_process_cpu_charged_once_and_rss_uses_max():
    from rawlsing_next.fiabc_telemetry_semantics import ProcessEnvelopeReceipt
    c=cell()
    ledger=TelemetryLedger(c)
    ledger.record_process_envelope(ProcessEnvelopeReceipt(
        c,"__CANDIDATE_ENVELOPE__","main",101,"MAIN",None,
        "PROCESS_SELF_ONLY","CANDIDATE_PROCESS_LOCAL",
        10,30,20,50,100,300,1000,"main"
    ))
    ledger.record_process_envelope(ProcessEnvelopeReceipt(
        c,"S15","child",202,"CHILD","main",
        "PROCESS_SELF_ONLY","CANDIDATE_PROCESS_LOCAL",
        0,7,0,11,150,250,4000,"child"
    ))
    ledger.seal_process_metrics(evidence_ref="seal")
    receipt=ledger.receipt(candidate_semantic_state="UNCHANGED")
    assert receipt["metrics"]["cpu_user_ns"]["value"] == 27
    assert receipt["metrics"]["cpu_system_ns"]["value"] == 41
    assert receipt["metrics"]["peak_rss_bytes"]["value"] == 4000
    with pytest.raises(TelemetryContractError):
        ledger.record_process_envelope(ProcessEnvelopeReceipt(
            c,"S15","child",202,"CHILD","main",
            "PROCESS_SELF_ONLY","CANDIDATE_PROCESS_LOCAL",
            0,7,0,11,150,250,4000,"child"
        ))
