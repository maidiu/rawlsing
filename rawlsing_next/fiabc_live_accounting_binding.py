"""FIABC-T4 live telemetry/lifecycle binding.

This module is the narrow T4 seam between the already-governing T3 process
envelope and the accepted I06B/I06C accounting contracts.  It does not decide
semantic disposition, oracle truth, candidate capability, or terminal parity.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from typing import Any, Mapping

from rawlsing_next.ee_p2x_candidate_process_envelope import load_frozen_upstream_receipt
from rawlsing_next.fiabc_telemetry_semantics import (
    CANDIDATE_ENVELOPE_PHASE,
    CellIdentity,
    CostClass,
    LifecycleActionReceipt as TelemetryLifecycleReceipt,
    METRIC_DEFINITIONS,
    MetricState as TelemetryMetricState,
    ObservationContext,
    ProcessEnvelopeReceipt as TelemetryProcessReceipt,
    TelemetryLedger,
)
from rawlsing_next.fiabc_lifecycle_accounting import (
    ActionObservation,
    AccountingDisposition,
    CallableLifecycleActionAdapter,
    CallableTelemetryAdapter,
    EvidenceKind,
    LifecycleAction,
    LifecycleActionRequest,
    LifecycleBinding,
    MetricState as LifecycleMetricState,
    ProcessIsolationReceipt,
    TelemetryMetric,
    execute_lifecycle_action,
    receipt_as_dict,
)

LIVE_CONTRACT = "FIABC_T4_LIVE_ACCOUNTING_BINDING@1.0.0"
JOURNAL_SCHEMA = "FIABC_T4_LIVE_ACCOUNTING_JOURNAL@1.0.0"
PARENTAGE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"
PRESERVED_SCHEMA = "FIABC_T4_PRESERVED_WORK_LIVE_ADJUDICATION@1.0.0"


FROZEN_METRIC_PRODUCTION = {
    "source_open_count": ("SOURCE_EVENT_LEDGER", "ALL_COMPLETED_CELLS"),
    "source_decode_count": ("SOURCE_EVENT_LEDGER", "ALL_COMPLETED_CELLS"),
    "source_reread_count": ("SOURCE_EVENT_LEDGER", "ALL_COMPLETED_CELLS"),
    "bytes_read": ("COMPLETE_IO_EVENT_LEDGER", "ALL_COMPLETED_CELLS"),
    "bytes_written": ("COMPLETE_IO_EVENT_LEDGER", "ALL_COMPLETED_CELLS"),
    "bytes_rewritten": ("COMPLETE_IO_EVENT_LEDGER", "ALL_COMPLETED_CELLS"),
    "candidate_total_wall_ns": ("T3_MAIN_PROCESS_ENVELOPE", "ALL_COMPLETED_CELLS"),
    "build_or_open_wall_ns": ("S01_MONOTONIC_TIMER", "ALL_COMPLETED_CELLS"),
    "cpu_user_ns": ("NONOVERLAPPING_PROCESS_SELF_ENVELOPES", "ALL_COMPLETED_CELLS"),
    "cpu_system_ns": ("NONOVERLAPPING_PROCESS_SELF_ENVELOPES", "ALL_COMPLETED_CELLS"),
    "peak_rss_bytes": ("MAX_PROCESS_LOCAL_RSS", "ALL_COMPLETED_CELLS"),
    "peak_scratch_bytes": ("SCRATCH_MUTATION_HIGH_WATER", "ALL_COMPLETED_CELLS"),
    "peak_scratch_file_count": ("SCRATCH_MUTATION_HIGH_WATER", "ALL_COMPLETED_CELLS"),
    "durable_authoritative_bytes": ("S16_CLASSIFIED_DURABLE_INVENTORY", "ALL_COMPLETED_CELLS"),
    "durable_transformed_regenerable_bytes": ("S16_CLASSIFIED_DURABLE_INVENTORY", "ALL_COMPLETED_CELLS"),
    "warm_retained_state_bytes": ("S08_RETAINED_SESSION_OBJECT_GRAPH", "ALL_COMPLETED_CELLS"),
    "cold_i03_latency_ns": ("S07_MONOTONIC_TIMER", "ALL_COMPLETED_CELLS"),
    "warm_i03_latency_ns": ("S08_MONOTONIC_TIMER", "ALL_COMPLETED_CELLS"),
    "i05_learned_production_wall_ns": ("S05_MONOTONIC_TIMER", "ALL_COMPLETED_CELLS"),
    "i05_learned_production_throughput_per_s": ("S05_OBSERVED_COUNT_OVER_OBSERVED_WALL", "ALL_COMPLETED_CELLS"),
    "repeated_research_source_open_count": ("S08_SOURCE_EVENT_DELTA", "ALL_COMPLETED_CELLS"),
    "repeated_research_source_redecode_count": ("S08_SOURCE_EVENT_DELTA", "ALL_COMPLETED_CELLS"),
    "repeated_research_source_reread_count": ("S08_SOURCE_EVENT_DELTA", "ALL_COMPLETED_CELLS"),
    "delete_rebuild_wall_ns": ("S09_DELETION_REGEN_MONOTONIC_TIMER", "B_C_MEASURED__A_FROZEN_NOT_APPLICABLE"),
    "source_release_invalidation_recomputation_units": ("S10_EXECUTED_RECOMPUTATION_LINEAGE", "ALL_COMPLETED_CELLS"),
    "source_release_invalidation_wall_ns": ("S10_MONOTONIC_ACTION_TIMER", "ALL_COMPLETED_CELLS"),
    "source_release_invalidation_bytes_rewritten": ("S10_ACTION_TAGGED_WRITE_SUBSET", "ALL_COMPLETED_CELLS"),
    "semantic_authority_invalidation_recomputation_units": ("S11_EXECUTED_RECOMPUTATION_LINEAGE", "ALL_COMPLETED_CELLS"),
    "semantic_authority_invalidation_wall_ns": ("S11_MONOTONIC_ACTION_TIMER", "ALL_COMPLETED_CELLS"),
    "semantic_authority_invalidation_bytes_rewritten": ("S11_ACTION_TAGGED_WRITE_SUBSET", "ALL_COMPLETED_CELLS"),
    "fresh_process_replay_wall_ns": ("S15_MONOTONIC_TIMER", "ALL_COMPLETED_CELLS"),
    "fresh_process_replay_cpu_ns": ("S15_EXACT_CHILD_PROCESS_SELF_ENVELOPE", "ALL_COMPLETED_CELLS"),
    "audit_wall_ns": ("S06_MONOTONIC_TIMER", "ALL_COMPLETED_CELLS"),
    "persistent_bytes_removable_with_zero_information_loss": ("S09_EXACT_REGENERABLE_STATE_INVENTORY", "ALL_COMPLETED_CELLS"),
    "implementation_moving_parts_count": ("S16_EXACT_RUNTIME_PART_MANIFEST", "ALL_COMPLETED_CELLS"),
}


def metric_production_manifest() -> Mapping[str, Mapping[str, str]]:
    if set(FROZEN_METRIC_PRODUCTION) != set(METRIC_DEFINITIONS):
        raise LiveAccountingError("frozen metric production manifest does not cover exact telemetry registry")
    return {
        name: {"producer": producer, "applicability": applicability}
        for name, (producer, applicability) in sorted(FROZEN_METRIC_PRODUCTION.items())
    }


class LiveAccountingError(RuntimeError):
    pass


@dataclass(frozen=True)
class DerivativeParentage:
    derivative_identity: Any
    governed_producer_identity: str
    governed_operation_identity: str
    governed_config_identity: str
    canonical_source_sha256: str
    evidence_refs: tuple[str, ...]

    @property
    def identity(self) -> str:
        return _hash({
            "derivative_identity": self.derivative_identity,
            "governed_producer_identity": self.governed_producer_identity,
            "governed_operation_identity": self.governed_operation_identity,
            "governed_config_identity": self.governed_config_identity,
            "canonical_source_sha256": self.canonical_source_sha256,
            "evidence_refs": list(self.evidence_refs),
        })


def _canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")


def _hash(value: Any) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False,default=str)+"\n",encoding="utf-8")
    os.replace(tmp,path)


def _cost(value: str) -> CostClass:
    try:
        return {
            "C0": CostClass.C0, "C1": CostClass.C1, "C2": CostClass.C2,
            "C3": CostClass.C3, "C4": CostClass.C4,
        }[value]
    except KeyError as exc:
        raise LiveAccountingError(f"unknown cost class {value!r}") from exc


def require_derivative_parentage(
    path: Path,
    *,
    derivative_identity: Any,
    canonical_source_sha256: str,
    expected_binding: Mapping[str, Any] | None = None,
) -> DerivativeParentage:
    """Compatibility seam: T4 no longer owns a derivative-parentage law.

    Exact live consumers must provide the complete R35-I02 expected binding.
    This adapter delegates all admission to fiabc_derivative_parentage and
    exposes only a T4 accounting summary after the generic bundle verifies.
    """
    if expected_binding is None:
        raise LiveAccountingError(
            "generic R35 derivative parentage requires the exact expected consumer binding"
        )
    p=Path(path)
    if not p.is_file():
        raise LiveAccountingError("derivative parentage bundle is absent")
    try:
        doc=json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise LiveAccountingError("derivative parentage bundle is malformed") from exc
    try:
        from rawlsing_next.fiabc_derivative_parentage import (
            BUNDLE_SCHEMA,
            ParentageError,
            canonical_digest,
            verify_parentage_bundle,
        )
        if doc.get("schema") != BUNDLE_SCHEMA or BUNDLE_SCHEMA != PARENTAGE_SCHEMA:
            raise ParentageError("generic derivative parentage bundle schema drift")
        binding=dict(expected_binding)
        expected_identity=binding.get("expected_derivative_identity")
        if derivative_identity != expected_identity:
            raise ParentageError("consumed derivative identity differs from exact R35 expected binding")
        if binding.get("expected_source_sha256") not in (None, canonical_source_sha256):
            raise ParentageError("T4/R35 canonical source SHA binding drift")
        binding.pop("expected_source_sha256",None)
        verified=verify_parentage_bundle(
            doc,
            expected_source_sha256=canonical_source_sha256,
            **binding,
        )
        source_receipt=verified["source_receipt"]
        derivative_receipt=verified["derivative_receipt"]
        producer=derivative_receipt["producer"]
        reader_config=derivative_receipt["reader_config"]
        return DerivativeParentage(
            derivative_identity=derivative_identity,
            governed_producer_identity=str(producer["identity"]),
            governed_operation_identity=str(derivative_receipt["derivation_operation"]),
            governed_config_identity=canonical_digest(reader_config),
            canonical_source_sha256=canonical_source_sha256,
            evidence_refs=(
                str(verified["bundle_identity"]),
                str(source_receipt["receipt_identity"]),
                str(derivative_receipt["receipt_identity"]),
            ),
        )
    except (ParentageError, KeyError, TypeError) as exc:
        raise LiveAccountingError("generic R35 derivative parentage failed closed") from exc


def _freeze() -> tuple[Mapping[str, Any], str]:
    raw=os.environ.get("RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT")
    if not raw:
        raise LiveAccountingError("T4 requires the T3 frozen-upstream receipt")
    return load_frozen_upstream_receipt(Path(raw))


def _cell(source: str, source_sha256: str, candidate: str, freeze: Mapping[str, Any]) -> CellIdentity:
    workloads=freeze.get("workload_identities",{})
    authorities=freeze.get("authority_identities",{})
    if source not in workloads or source not in authorities:
        raise LiveAccountingError("frozen workload/authority identity missing for accounting cell")
    return CellIdentity(
        source_id=source, source_sha256=source_sha256, candidate_id=candidate,
        workload_id=_hash(workloads[source]), authority_set_id=_hash(authorities[source]),
    )


def _process_token(envelope: Mapping[str, Any]) -> str:
    proc=envelope.get("process",{})
    pid=proc.get("pid")
    cell=envelope.get("cell_key")
    if not isinstance(pid,int) or pid <= 0 or not isinstance(cell,str) or not cell:
        raise LiveAccountingError("T3 process envelope lacks exact process identity")
    return f"{cell}::pid={pid}"


def _runtime_identity(envelope: Mapping[str, Any], repo_head: str) -> str:
    return _hash({
        "repo_head": repo_head,
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "system": platform.system(),
        "machine": platform.machine(),
        "process_environment_attribution": envelope.get("process",{}).get("environment_attribution"),
        "freeze_receipt_sha256": envelope.get("candidate_neutral_freeze",{}).get("receipt_sha256"),
    })


def _state_scope(roots: Any) -> str:
    return _hash({
        "root": str(Path(roots.root).resolve()),
        "scratch": str(Path(roots.scratch).resolve()),
        "durable": str(Path(roots.durable).resolve()),
        "receipts": str(Path(roots.receipts).resolve()),
    })


def _isolation(source: str, candidate: str, envelope: Mapping[str, Any], roots: Any) -> ProcessIsolationReceipt:
    proc=envelope.get("process",{})
    if proc.get("session_registry_empty_at_start") is not True:
        raise LiveAccountingError("T3 isolation receipt does not prove empty candidate session registry")
    return ProcessIsolationReceipt(
        source_id=source,candidate_id=candidate,process_token=_process_token(envelope),
        candidate_root_identity=_state_scope(roots),fresh_process_for_cell=True,
        cross_candidate_state_reachable=False,
        isolation_contract_identity=_hash({
            "schema":envelope.get("schema"),"cell_key":envelope.get("cell_key"),
            "freeze":envelope.get("candidate_neutral_freeze"),
            "environment":proc.get("environment_attribution"),
        }),
    )


def _life_binding(*, source: str, source_sha256: str, candidate: str,
                  candidate_owner_identity: str, envelope: Mapping[str, Any],
                  roots: Any, freeze: Mapping[str, Any], repo_head: str,
                  expected_terminal_identity: str) -> LifecycleBinding:
    cell=_cell(source,source_sha256,candidate,freeze)
    return LifecycleBinding(
        source_id=source,source_sha256=source_sha256,candidate_id=candidate,
        candidate_owner_identity=candidate_owner_identity,
        workload_id=cell.workload_id,authority_set_identity=cell.authority_set_id,
        runtime_binding_identity=_runtime_identity(envelope,repo_head),
        state_scope_identity=_state_scope(roots),
        expected_terminal_identity=expected_terminal_identity,
        isolation=_isolation(source,candidate,envelope,roots),
    )


def _action_observation(event: Mapping[str, Any], binding: LifecycleBinding) -> ActionObservation:
    try: action=LifecycleAction(event["action"])
    except Exception as exc: raise LiveAccountingError("unknown lifecycle action") from exc
    kw={
        "action":action,"binding_id":binding.binding_id,"source_id":binding.source_id,
        "candidate_id":binding.candidate_id,"performed":True,
        "evidence_kind":EvidenceKind.EXECUTED_CANDIDATE_ACTION,
        "action_id":event["action_id"],"state_before_id":event["state_before_id"],
        "state_after_id":event["state_after_id"],"terminal_identity":event["terminal_identity"],
    }
    optional=(
        "candidate_state_object_ids_before","candidate_state_object_ids_after",
        "deleted_object_ids","regenerated_object_ids","regeneration_lineage",
        "retained_state_id","retained_state_candidate_id","cold_state_proven_absent",
        "invalidation_trigger_identity","invalidated_unit_ids","recomputed_unit_ids",
        "stale_determinant_before","stale_determinant_after","stale_detected",
        "corrupt_target_id","corruption_injected","corrupt_detected",
        "interrupted_operation_id","interrupted_candidate_state_id","interruption_injected",
        "recovered_operation_id","parent_process_token","replay_process_token",
        "audit_primitive_identity","recovery_performed","evidence_refs",
    )
    for name in optional:
        if name in event:
            val=event[name]
            if name in {"candidate_state_object_ids_before","candidate_state_object_ids_after",
                        "deleted_object_ids","regenerated_object_ids","invalidated_unit_ids",
                        "recomputed_unit_ids","evidence_refs"}:
                val=tuple(val)
            elif name=="regeneration_lineage":
                val=tuple(tuple(x) for x in val)
            kw[name]=val
    return ActionObservation(**kw)


def _metric_map(observations: Mapping[str, Any], action_id: str) -> dict[str, Mapping[str, Any]]:
    return {m["name"]:m for m in observations.get("metric_events",[]) if m.get("lifecycle_action_id")==action_id}


def _validate_lifecycle(*, event: Mapping[str, Any], observations: Mapping[str, Any],
                        source: str, source_sha256: str, candidate: str,
                        candidate_owner_identity: str, envelope: Mapping[str, Any],
                        roots: Any, freeze: Mapping[str, Any], repo_head: str):
    binding=_life_binding(
        source=source,source_sha256=source_sha256,candidate=candidate,
        candidate_owner_identity=candidate_owner_identity,envelope=envelope,roots=roots,
        freeze=freeze,repo_head=repo_head,
        expected_terminal_identity=str(event["expected_terminal_identity"]),
    )
    action=LifecycleAction(event["action"])
    if action is LifecycleAction.COLD_FIRST_REALIZATION:
        cold=envelope.get("cold_state_observation",{})
        if (
            cold.get("candidate_owned_warm_state_present") is not False
            or cold.get("scratch_files_before_start") not in ([], ())
            or cold.get("durable_files_before_start") not in ([], ())
        ):
            raise LiveAccountingError(
                "cold first realization is not backed by the governing T3/I06A absent-state receipt"
            )
        if event.get("cold_state_proven_absent") is not True:
            raise LiveAccountingError(
                "backend cold claim does not agree with T3/I06A absent-state boundary"
            )
    request=LifecycleActionRequest(
        binding=binding,action=action,
        governed_operation_id=str(event["governed_operation_id"]),
        expected_metric_names=tuple(event.get("metric_names",())),
    )
    observation=_action_observation(event,binding)
    by_name=_metric_map(observations,event["action_id"])
    def action_cb(_request): return observation
    def telemetry_cb(_request,_observation):
        rows=[]
        for name in request.expected_metric_names:
            m=by_name.get(name)
            if m is None: raise LiveAccountingError(f"lifecycle metric {name} was not observed after action")
            if m.get("kind")=="DURATION":
                value=int(m["stop_ns"])-int(m["start_ns"]); unit="ns"
            else:
                value=m.get("value"); unit=m.get("unit") or ""
            rows.append(TelemetryMetric(
                name=name,state=LifecycleMetricState.MEASURED,value=value,unit=unit,
                action_id=observation.action_id,binding_id=binding.binding_id,
            ))
        return tuple(rows)
    return execute_lifecycle_action(
        request,CallableLifecycleActionAdapter(action_cb),CallableTelemetryAdapter(telemetry_cb)
    )


def _journal_path(roots: Any) -> Path:
    return Path(roots.receipts)/"fiabc_t4_live_accounting_journal.json"


def _load_journal(roots: Any, *, source: str, source_sha256: str, candidate: str) -> dict[str, Any]:
    p=_journal_path(roots)
    if not p.exists():
        return {"schema":JOURNAL_SCHEMA,"source":source,"source_sha256":source_sha256,
                "candidate":candidate,"stages":{}}
    doc=json.loads(p.read_text(encoding="utf-8"))
    if doc.get("schema")!=JOURNAL_SCHEMA or doc.get("source")!=source or doc.get("source_sha256")!=source_sha256 or doc.get("candidate")!=candidate:
        raise LiveAccountingError("T4 accounting journal cell identity drift")
    return doc


def _phase_rows(journal: Mapping[str, Any]):
    return [journal["stages"][k] for k in sorted(journal["stages"], key=lambda x: journal["stages"][x]["ordinal"])]


def _require_complete_stage_coverage(rows, field: str, label: str) -> None:
    if not rows or not all(row.get("observations",{}).get(field) is True for row in rows):
        raise LiveAccountingError(f"{label} cannot seal before complete event coverage")


def _materialize_telemetry(*, journal: Mapping[str, Any], roots: Any, source: str,
                           source_sha256: str, candidate: str, freeze: Mapping[str, Any],
                           semantic_state: str) -> Mapping[str, Any]:
    cell=_cell(source,source_sha256,candidate,freeze)
    ledger=TelemetryLedger(cell)
    rows=_phase_rows(journal)
    if not rows:
        raise LiveAccountingError("cannot finalize telemetry without stage observations")
    first=rows[0]; final=rows[-1]
    first_env=first["process_envelope"]; final_env=final["process_envelope"]
    if first_env.get("cell_key")!=final_env.get("cell_key"):
        raise LiveAccountingError("cross-cell process envelope leak")
    token=_process_token(first_env)
    proc=first_env["process"]; stop=final_env.get("stop")
    if not isinstance(stop,Mapping):
        raise LiveAccountingError("S16 telemetry finalization requires a stopped T3 candidate process")
    start_res=proc.get("pre_backend_import_resource",{})
    stop_res=stop.get("resource_at_stop",{})
    rss_samples=[int(proc.get("pre_backend_import_resource",{}).get("peak_rss_bytes",0))]
    for row in rows:
        rss_samples.append(int(row["process_envelope"].get("resource_after_stage",{}).get("peak_rss_bytes",0)))
    rss_samples.append(int(stop_res.get("peak_rss_bytes",0)))
    ledger.record_process_envelope(TelemetryProcessReceipt(
        cell=cell,phase_id=CANDIDATE_ENVELOPE_PHASE,process_token=token,pid=int(proc["pid"]),
        role="MAIN",parent_process_token=None,cpu_scope="PROCESS_SELF_ONLY",
        rss_scope="CANDIDATE_PROCESS_LOCAL",
        cpu_user_start_ns=int(start_res.get("cpu_user_ns",0)),
        cpu_user_stop_ns=int(stop_res.get("cpu_user_ns",0)),
        cpu_system_start_ns=int(start_res.get("cpu_system_ns",0)),
        cpu_system_stop_ns=int(stop_res.get("cpu_system_ns",0)),
        wall_start_ns=int(first_env["candidate_local_boundary"]["parent_envelope_start_monotonic_ns"]),
        wall_stop_ns=int(stop["parent_envelope_stop_monotonic_ns"]),
        peak_rss_bytes=max(rss_samples),evidence_ref="T3_PROCESS_ENVELOPE",
    ))

    seen_child_tokens=set()
    child_tokens={}
    for row in rows:
        for child in row.get("observations",{}).get("child_process_envelopes",[]):
            child_token=str(child["process_token"])
            if child_token in seen_child_tokens:
                raise LiveAccountingError("child process accounting attempted to charge one child twice")
            seen_child_tokens.add(child_token)
            label=str(child.get("label") or "")
            key=(row["stage_id"],label)
            if label and key in child_tokens:
                raise LiveAccountingError("stage emitted duplicate child role label")
            if label:
                child_tokens[key]=child_token
            ledger.record_process_envelope(TelemetryProcessReceipt(
                cell=cell,phase_id=str(child["phase_id"]),process_token=child_token,
                pid=int(child["pid"]),role="CHILD",parent_process_token=token,
                cpu_scope="PROCESS_SELF_ONLY",rss_scope="CANDIDATE_PROCESS_LOCAL",
                cpu_user_start_ns=int(child["cpu_user_start_ns"]),
                cpu_user_stop_ns=int(child["cpu_user_stop_ns"]),
                cpu_system_start_ns=int(child["cpu_system_start_ns"]),
                cpu_system_stop_ns=int(child["cpu_system_stop_ns"]),
                wall_start_ns=int(child["wall_start_ns"]),wall_stop_ns=int(child["wall_stop_ns"]),
                peak_rss_bytes=int(child["peak_rss_bytes"]),evidence_ref=str(child["evidence_ref"]),
            ))

    previous=proc.get("post_backend_import_resource",{})
    for row in rows:
        env=row["process_envelope"]; current=env.get("resource_after_stage",{})
        ctx=ObservationContext(
            source_id=source,source_sha256=source_sha256,candidate_id=candidate,
            phase_id=row["stage_id"],process_token=token,cost_class=CostClass.C3,
            evidence_ref=row["stage_address"],
        )
        ledger.observe_phase_cpu_counters(
            ctx,user_start_ns=int(previous.get("cpu_user_ns",0)),user_stop_ns=int(current.get("cpu_user_ns",0)),
            system_start_ns=int(previous.get("cpu_system_ns",0)),system_stop_ns=int(current.get("cpu_system_ns",0)),
            evidence_ref=row["stage_address"],
        )
        previous=current
    ledger.seal_process_metrics(evidence_ref="T3_CELL_PROCESS_STOP")

    lifecycle_ids={}
    scratch_event_count=0
    for row in rows:
        lr=row.get("lifecycle_receipt")
        if lr and lr.get("action_id"):
            lifecycle_ids[row["stage_id"]]=lr["action_id"]
            ledger.bind_lifecycle_receipt(TelemetryLifecycleReceipt(
                cell=cell,action_id=lr["action_id"],action_type=lr["action"],
                phase_id=row["stage_id"],process_token=token,outcome=lr["disposition"],
                evidence_ref=row["stage_address"],
            ))
        observations=row.get("observations",{})
        for m in observations.get("metric_events",[]):
            ctx=ObservationContext(
                source_id=source,source_sha256=source_sha256,candidate_id=candidate,
                phase_id=row["stage_id"],process_token=str(m.get("process_token") or token),
                cost_class=_cost(m.get("cost_class","C2")),
                lifecycle_action_id=m.get("lifecycle_action_id"),evidence_ref=m.get("evidence_ref"),
            )
            if m.get("kind")=="DURATION":
                ledger.record_duration(
                    m["name"],ctx,monotonic_start_ns=int(m["start_ns"]),
                    monotonic_stop_ns=int(m["stop_ns"]),
                    state_predicate_ref=m.get("evidence_ref") or row["stage_address"],
                )
            else:
                ledger.record_observed_value(
                    m["name"],ctx,float(m["value"]),evidence_kind="OBSERVED_BACKEND_EVENT"
                )
        for unavailable in observations.get("metric_unavailable",[]):
            state_name=str(unavailable.get("state"))
            try:
                metric_state=TelemetryMetricState(state_name)
            except Exception as exc:
                raise LiveAccountingError("backend emitted unknown typed metric state") from exc
            ctx=ObservationContext(
                source_id=source,source_sha256=source_sha256,candidate_id=candidate,
                phase_id=row["stage_id"],process_token=token,cost_class=_cost(unavailable.get("cost_class","C2")),
                lifecycle_action_id=unavailable.get("lifecycle_action_id"),
                evidence_ref=unavailable.get("evidence_ref") or row["stage_address"],
            )
            if metric_state is TelemetryMetricState.NOT_APPLICABLE_BY_FROZEN_COURT and ctx.lifecycle_action_id is None:
                ledger.mark_lifecycle_not_applicable(
                    unavailable["name"],ctx,reason=str(unavailable["reason"])
                )
            else:
                ledger.mark_unavailable(
                    unavailable["name"],ctx,state=metric_state,reason=str(unavailable["reason"])
                )
        for event in observations.get("source_events",[]):
            ctx=ObservationContext(
                source_id=source,source_sha256=source_sha256,candidate_id=candidate,
                phase_id=row["stage_id"],process_token=token,cost_class=CostClass.C1,
                evidence_ref=row["stage_address"],
            )
            ledger.observe_source_event(ctx,event=event)
        for io_event in observations.get("io_events",[]):
            io_token=str(io_event.get("process_token") or token)
            ctx=ObservationContext(
                source_id=source,source_sha256=source_sha256,candidate_id=candidate,
                phase_id=row["stage_id"],process_token=io_token,cost_class=_cost(io_event.get("cost_class","C1")),
                lifecycle_action_id=io_event.get("lifecycle_action_id"),
                evidence_ref=io_event.get("evidence_ref"),
            )
            ledger.observe_io(
                ctx,operation=io_event["operation"],byte_count=int(io_event["byte_count"]),
                object_id=io_event["object_id"],rewrite_of=io_event.get("rewrite_of"),
            )
        for scratch in observations.get("scratch_events",[]):
            scratch_event_count += 1
            scratch_token=str(scratch.get("process_token") or token)
            ctx=ObservationContext(
                source_id=source,source_sha256=source_sha256,candidate_id=candidate,
                phase_id=row["stage_id"],process_token=scratch_token,
                cost_class=_cost(scratch.get("cost_class","C2")),
                lifecycle_action_id=scratch.get("lifecycle_action_id"),
                evidence_ref=scratch.get("evidence_ref") or row["stage_address"],
            )
            operation=scratch.get("operation")
            if operation=="SIZE":
                ledger.observe_scratch_size(
                    ctx,object_id=scratch["object_id"],
                    current_size_bytes=int(scratch["current_size_bytes"]),
                )
            elif operation=="REMOVE":
                ledger.observe_scratch_remove(ctx,object_id=scratch["object_id"])
            elif operation=="EMPTY_BASELINE":
                ledger.observe_empty_scratch_baseline(ctx)
            else:
                raise LiveAccountingError("unknown scratch observation operation")

    source_ctx=ObservationContext(
        source_id=source,source_sha256=source_sha256,candidate_id=candidate,
        phase_id="__SOURCE_EVENT_LEDGER__",process_token=token,cost_class=CostClass.C1,
        evidence_ref="T4_OBSERVED_SOURCE_EVENTS",
    )
    ledger.seal_source_event_counters(source_ctx)

    _require_complete_stage_coverage(rows,"io_coverage_complete","canonical I/O metrics")
    io_ctx=ObservationContext(
        source_id=source,source_sha256=source_sha256,candidate_id=candidate,
        phase_id="__IO_EVENT_LEDGER__",process_token=token,cost_class=CostClass.C2,
        evidence_ref="T4_COMPLETE_CANDIDATE_LOCAL_IO_EVENT_STREAM",
    )
    ledger.seal_io_accounting(io_ctx)

    _require_complete_stage_coverage(rows,"scratch_coverage_complete","scratch high-water metrics")
    scratch_ctx=ObservationContext(
        source_id=source,source_sha256=source_sha256,candidate_id=candidate,
        phase_id="__SCRATCH_HIGH_WATER_LEDGER__",process_token=token,cost_class=CostClass.C2,
        evidence_ref="T4_COMPLETE_SCRATCH_MUTATION_EVENT_STREAM",
    )
    if scratch_event_count==0:
        ledger.observe_empty_scratch_baseline(scratch_ctx)
    ledger.seal_scratch_accounting(scratch_ctx)

    for stage_id,metric_name in (
        ("S10_SOURCE_RELEASE_INVALIDATION","source_release_invalidation_bytes_rewritten"),
        ("S11_SEMANTIC_AUTHORITY_INVALIDATION","semantic_authority_invalidation_bytes_rewritten"),
    ):
        action_id=lifecycle_ids.get(stage_id)
        if action_id is None:
            raise LiveAccountingError(f"{stage_id} lacks lifecycle action required for rewrite accounting")
        ctx=ObservationContext(
            source_id=source,source_sha256=source_sha256,candidate_id=candidate,
            phase_id=stage_id,process_token=token,cost_class=CostClass.C2,
            lifecycle_action_id=action_id,evidence_ref=stage_id+"::EXACT_REWRITE_EVENT_SUBSET",
        )
        ledger.seal_lifecycle_rewrite_bytes(metric_name,ctx)

    fresh_action=lifecycle_ids.get("S15_FRESH_PROCESS_REPLAY")
    fresh_child=child_tokens.get(("S15_FRESH_PROCESS_REPLAY","FRESH_PROCESS_REPLAY"))
    if fresh_action is None or fresh_child is None:
        raise LiveAccountingError("fresh-process replay CPU lacks exact lifecycle-bound child envelope")
    fresh_ctx=ObservationContext(
        source_id=source,source_sha256=source_sha256,candidate_id=candidate,
        phase_id="S15_FRESH_PROCESS_REPLAY",process_token=fresh_child,cost_class=CostClass.C3,
        lifecycle_action_id=fresh_action,evidence_ref="S15::EXACT_FRESH_REPLAY_CHILD_CPU",
    )
    ledger.seal_fresh_process_replay_cpu(process_token=fresh_child,ctx=fresh_ctx)

    receipt=ledger.receipt(candidate_semantic_state=semantic_state)
    missing=[]
    for name,value in receipt["metrics"].items():
        values=value if isinstance(value,list) else [value]
        if any(row["state"]==TelemetryMetricState.MEASUREMENT_NOT_CAPTURED.value for row in values):
            missing.append(name)
    if missing:
        raise LiveAccountingError(
            "terminal metric vector still contains instrumentation-absent fields: "+",".join(sorted(missing))
        )
    return receipt

def admit_live_stage_accounting(*, stage: Any, roots: Any, source_sha256: str,
                                candidate_owner_identity: str, repo_head: str,
                                backend_receipt: Mapping[str, Any],
                                terminal_disposition: str) -> Mapping[str, Any]:
    if stage.source=="COURT":
        return {"schema":LIVE_CONTRACT,"classification":"C4_COURT_ADMINISTRATION",
                "candidate_numeric_cost":"NOT_APPLICABLE","semantic_state_modified":False}
    envelope=backend_receipt.get("process_envelope")
    if not isinstance(envelope,Mapping):
        raise LiveAccountingError("T4 requires the exact T3 process envelope")
    if envelope.get("source")!=stage.source or envelope.get("candidate")!=stage.candidate:
        raise LiveAccountingError("T3 process envelope cross-candidate/source leak")
    freeze,freeze_sha=_freeze()
    if envelope.get("candidate_neutral_freeze",{}).get("receipt_sha256")!=freeze_sha:
        raise LiveAccountingError("T3 process envelope freeze identity drift")
    payload=backend_receipt.get("stage_payload",{})
    observations=payload.get("t4_accounting_observations",{})
    if not isinstance(observations,Mapping):
        observations={}
    lifecycle=None
    event=observations.get("lifecycle_event")
    if event is not None:
        lifecycle=_validate_lifecycle(
            event=event,observations=observations,source=stage.source,
            source_sha256=source_sha256,candidate=stage.candidate,
            candidate_owner_identity=candidate_owner_identity,envelope=envelope,roots=roots,
            freeze=freeze,repo_head=repo_head,
        )
    journal=_load_journal(roots,source=stage.source,source_sha256=source_sha256,candidate=stage.candidate)
    row={
        "stage_address":stage.address,"stage_id":stage.stage_id,
        "ordinal":len(journal["stages"])+1,"terminal_disposition":terminal_disposition,
        "process_envelope":dict(envelope),"observations":dict(observations),
        "lifecycle_receipt":receipt_as_dict(lifecycle) if lifecycle is not None else None,
    }
    old=journal["stages"].get(stage.address)
    if old is not None:
        if _hash({k:v for k,v in old.items() if k!="ordinal"}) != _hash({k:v for k,v in row.items() if k!="ordinal"}):
            raise LiveAccountingError("write-once stage accounting observation changed on resume")
        row=old
    else:
        journal["stages"][stage.address]=row
        _atomic_json(_journal_path(roots),journal)
    out={
        "schema":LIVE_CONTRACT,"stage":stage.address,"source":stage.source,
        "candidate":stage.candidate,"journal_sha256":_sha(_journal_path(roots)),
        "lifecycle_receipt":row.get("lifecycle_receipt"),
        "semantic_state_modified":False,
        "candidate_neutral_c0_excluded":True,
    }
    if stage.stage_id=="S16_TERMINAL_METRIC_VECTOR_COMPLETENESS":
        telemetry=_materialize_telemetry(
            journal=journal,roots=roots,source=stage.source,source_sha256=source_sha256,
            candidate=stage.candidate,freeze=freeze,
            semantic_state=str(payload.get("semantic_state_identity") or terminal_disposition),
        )
        tpath=Path(roots.receipts)/"fiabc_t4_telemetry_receipt.json"
        if tpath.exists() and _hash(json.loads(tpath.read_text(encoding="utf-8"))) != _hash(telemetry):
            raise LiveAccountingError("write-once canonical telemetry receipt overwrite attempted")
        if not tpath.exists(): _atomic_json(tpath,telemetry)
        out["telemetry_receipt_path"]=str(tpath)
        out["telemetry_receipt_sha256"]=_sha(tpath)
        out["metric_definition_hash"]=telemetry["metric_definition_hash"]
    return out


def preserved_stage_adjudication(*, stage: Any, source_sha256: str,
                                 evidence_ref: str | None) -> Mapping[str, Any]:
    disposition=AccountingDisposition.NOT_APPLICABLE
    reason="preserved stage is not a candidate numeric production obligation"
    numeric_credit_allowed=False
    if stage.source=="LITS_I" and stage.candidate=="A" and stage.stage_id=="S01_CANDIDATE_PREPARATION_BUILD":
        parentage=os.environ.get("RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT")
        parentage_identity=os.environ.get("RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT_IDENTITY")
        disposition=AccountingDisposition.PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY
        if parentage and parentage_identity:
            reason="LiTS-A generic R35 parentage is externally bound; numeric credit still requires exact field-by-field T4 compatibility proof"
        else:
            reason="LiTS-A generic R35 parentage path/identity is incomplete; no preserved numeric credit may be admitted"
    elif stage.source=="LITS_I" and stage.candidate=="B" and stage.stage_id in {
        "S01_CANDIDATE_PREPARATION_BUILD","S02_C11_REACHABILITY"
    }:
        disposition=AccountingDisposition.PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY
        reason="LiTS-B accepted cacheless C11 telemetry was not captured; numeric fields remain null"
    return {
        "schema":PRESERVED_SCHEMA,"stage":stage.address,"source_sha256":source_sha256,
        "evidence_ref":evidence_ref,"disposition":disposition.value,
        "numeric_credit_allowed":numeric_credit_allowed,"reason":reason,
        "missing_numeric_is_zero":False,
    }


def authorized_same_cell_transitions(stage_catalog) -> tuple[str, ...]:
    stages=tuple(stage_catalog)
    return tuple(f"{a}>{b}" for a,b in zip(stages,stages[1:]))


__all__=[
    "LIVE_CONTRACT","PARENTAGE_SCHEMA","LiveAccountingError","DerivativeParentage",
    "require_derivative_parentage","admit_live_stage_accounting",
    "preserved_stage_adjudication","authorized_same_cell_transitions",
    "metric_production_manifest",
]
