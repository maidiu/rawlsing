"""Fail-closed FIABC terminal telemetry completeness law.

This module validates evidence completeness only.  It never compares candidate
values, ranks candidates, emits a preferred candidate, or changes semantic
qualification.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.fiabc_telemetry_semantics import (
    CONTRACT_ID as TELEMETRY_CONTRACT_ID,
    METRIC_DEFINITION_HASH,
    METRIC_DEFINITIONS,
    MetricGrain,
    MetricState,
    metric_definition_manifest,
)

COMPLETENESS_SCHEMA = "RAWLSING_FIABC_TERMINAL_TELEMETRY_COMPLETENESS@1.0.0"

# Exact numeric fields frozen by CHETIRI Lock-1, expressed in the canonical T4
# telemetry names.  candidate_total_wall_ns is additionally mandatory because
# the final accounting contract requires a sealed wall/CPU/RSS process envelope.
FROZEN_DISPOSITIVE_METRICS = (
    "source_open_count",
    "source_decode_count",
    "source_reread_count",
    "bytes_read",
    "bytes_written",
    "bytes_rewritten",
    "build_or_open_wall_ns",
    "candidate_total_wall_ns",
    "cpu_user_ns",
    "cpu_system_ns",
    "peak_rss_bytes",
    "peak_scratch_bytes",
    "peak_scratch_file_count",
    "durable_authoritative_bytes",
    "durable_transformed_regenerable_bytes",
    "cold_i03_latency_ns",
    "warm_i03_latency_ns",
    "i05_learned_production_wall_ns",
    "i05_learned_production_throughput_per_s",
    "repeated_research_source_open_count",
    "repeated_research_source_redecode_count",
    "repeated_research_source_reread_count",
    "warm_retained_state_bytes",
    "delete_rebuild_wall_ns",
    "source_release_invalidation_recomputation_units",
    "source_release_invalidation_wall_ns",
    "source_release_invalidation_bytes_rewritten",
    "semantic_authority_invalidation_recomputation_units",
    "semantic_authority_invalidation_wall_ns",
    "semantic_authority_invalidation_bytes_rewritten",
    "fresh_process_replay_wall_ns",
    "fresh_process_replay_cpu_ns",
    "audit_wall_ns",
    "persistent_bytes_removable_with_zero_information_loss",
    "implementation_moving_parts_count",
)

if set(FROZEN_DISPOSITIVE_METRICS) != set(METRIC_DEFINITIONS):
    raise RuntimeError(
        "FIABC terminal completeness metric constitution drift: "
        "FROZEN_DISPOSITIVE_METRICS must be definition-identical to METRIC_DEFINITIONS"
    )
assert set(FROZEN_DISPOSITIVE_METRICS) == set(METRIC_DEFINITIONS)

# Stage-local origin for dispositive metrics.  __CELL__ means the metric is a
# whole-cell accounting seal rather than one stage's lifecycle product.
METRIC_STAGE = {
    "build_or_open_wall_ns": "S01_CANDIDATE_PREPARATION_BUILD",
    "i05_learned_production_wall_ns": "S05_I05_LEARNED_PRODUCTION",
    "i05_learned_production_throughput_per_s": "S05_I05_LEARNED_PRODUCTION",
    "audit_wall_ns": "S06_PROVENANCE_AUDIT",
    "cold_i03_latency_ns": "S07_COLD_RESEARCH",
    "warm_i03_latency_ns": "S08_WARM_REPEATED_RESEARCH",
    "repeated_research_source_open_count": "S08_WARM_REPEATED_RESEARCH",
    "repeated_research_source_redecode_count": "S08_WARM_REPEATED_RESEARCH",
    "repeated_research_source_reread_count": "S08_WARM_REPEATED_RESEARCH",
    "warm_retained_state_bytes": "S08_WARM_REPEATED_RESEARCH",
    "delete_rebuild_wall_ns": "S09_DELETION_REGEN_OR_A_PERSISTENCE",
    "source_release_invalidation_recomputation_units": "S10_SOURCE_RELEASE_INVALIDATION",
    "source_release_invalidation_wall_ns": "S10_SOURCE_RELEASE_INVALIDATION",
    "source_release_invalidation_bytes_rewritten": "S10_SOURCE_RELEASE_INVALIDATION",
    "semantic_authority_invalidation_recomputation_units": "S11_SEMANTIC_AUTHORITY_INVALIDATION",
    "semantic_authority_invalidation_wall_ns": "S11_SEMANTIC_AUTHORITY_INVALIDATION",
    "semantic_authority_invalidation_bytes_rewritten": "S11_SEMANTIC_AUTHORITY_INVALIDATION",
    "fresh_process_replay_wall_ns": "S15_FRESH_PROCESS_REPLAY",
    "fresh_process_replay_cpu_ns": "S15_FRESH_PROCESS_REPLAY",
    "persistent_bytes_removable_with_zero_information_loss": "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
    "implementation_moving_parts_count": "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
}

EXPECTED_LIFECYCLE_ACTION = {
    "S01_CANDIDATE_PREPARATION_BUILD": "COLD_FIRST_REALIZATION",
    "S06_PROVENANCE_AUDIT": "AUDIT_REVALIDATION",
    "S08_WARM_REPEATED_RESEARCH": "WARM_RETAINED_STATE_USE",
    "S09_DELETION_REGEN_OR_A_PERSISTENCE": "DELETION_REGENERATION",
    "S10_SOURCE_RELEASE_INVALIDATION": "SOURCE_INVALIDATION",
    "S11_SEMANTIC_AUTHORITY_INVALIDATION": "AUTHORITY_SEMANTIC_INVALIDATION",
    "S12_STALE_CACHE_OR_PERSISTENT_STATE": "STALE_STATE_RECOVERY",
    "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE": "CORRUPT_STATE_RECOVERY",
    "S14_INTERRUPTION_RECOVERY": "INTERRUPTION_RECOVERY",
    "S15_FRESH_PROCESS_REPLAY": "FRESH_PROCESS_REPLAY",
}

AUTHORIZED_STOP_DISPOSITIONS = frozenset({
    "CANDIDATE_LOCAL_FAILURE",
    "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
    "BLOCKED_BY_COMMON_COURT_AUTHORITY",
})
PRESERVED_NO_NUMERIC = "PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY"


class TerminalCompletenessError(RuntimeError):
    pass


def _fail(code: str, detail: str) -> None:
    raise TerminalCompletenessError(f"{code}: {detail}")


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def _hash(value: Any) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _cell_contract(
    current_manifest: Mapping[str, Any], source: str, candidate: str
) -> Mapping[str, Any]:
    cells = current_manifest.get("cells")
    if not isinstance(cells, Sequence) or isinstance(cells, (str, bytes)):
        _fail("TC_MANIFEST_CELL_SET_INVALID", "current execution manifest cells are absent")
    matches = [
        row for row in cells
        if isinstance(row, Mapping)
        and row.get("source") == source
        and row.get("candidate") == candidate
    ]
    if len(matches) != 1:
        _fail("TC_MANIFEST_CELL_IDENTITY_INVALID", f"expected exactly one {source}/{candidate} cell")
    stages = matches[0].get("stages")
    if not isinstance(stages, Mapping):
        _fail("TC_MANIFEST_STAGE_SET_INVALID", f"{source}/{candidate} stage law is absent")
    return matches[0]


def _stage_tuple(cell: Mapping[str, Any], stage_id: str) -> Sequence[Any]:
    raw = cell.get("stages", {}).get(stage_id)
    if (
        not isinstance(raw, Sequence)
        or isinstance(raw, (str, bytes))
        or len(raw) != 5
        or not isinstance(raw[0], str)
    ):
        _fail("TC_STAGE_LAW_INVALID", f"malformed stage law for {stage_id}")
    return raw


def _stage_disposition(cell: Mapping[str, Any], stage_id: str) -> str:
    return str(_stage_tuple(cell, stage_id)[0])


def _stage_law_ref(cell: Mapping[str, Any], stage_id: str) -> str | None:
    raw = _stage_tuple(cell, stage_id)[1]
    return raw if isinstance(raw, str) else None


def _metric_rows(telemetry: Mapping[str, Any], name: str) -> list[Mapping[str, Any]]:
    metrics = telemetry.get("metrics")
    if not isinstance(metrics, Mapping) or name not in metrics:
        _fail("TC_REQUIRED_METRIC_ABSENT", f"canonical telemetry slot {name} is absent")
    raw = metrics[name]
    definition = METRIC_DEFINITIONS[name]
    rows = raw if definition.grain != MetricGrain.CANDIDATE else [raw]
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)) or not rows:
        _fail("TC_METRIC_ROW_INVALID", f"{name} has no canonical metric row")
    if any(not isinstance(row, Mapping) for row in rows):
        _fail("TC_METRIC_ROW_INVALID", f"{name} contains a malformed metric row")
    return list(rows)


def _validate_metric_row_shape(
    row: Mapping[str, Any],
    *,
    name: str,
    source: str,
    source_sha256: str,
    candidate: str,
) -> None:
    definition = METRIC_DEFINITIONS[name]
    if row.get("name") != name or row.get("unit") != definition.unit:
        _fail("TC_METRIC_DEFINITION_DRIFT", f"{name} row name/unit differs from frozen definition")
    if (
        row.get("source_id") != source
        or row.get("source_sha256") != source_sha256
        or row.get("candidate_id") != candidate
    ):
        _fail("TC_METRIC_CELL_DRIFT", f"{name} is attributed to another source/candidate/root")
    state = row.get("state")
    allowed = {item.value for item in MetricState}
    if state not in allowed:
        _fail("TC_METRIC_STATE_INVALID", f"{name} uses unknown state {state!r}")
    value = row.get("value")
    if state == MetricState.MEASURED.value:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            _fail("TC_MEASURED_VALUE_INVALID", f"{name} MEASURED row lacks a non-negative numeric value")
    elif value is not None:
        _fail("TC_TYPED_NULL_HAS_VALUE", f"{name} non-measured row must carry value:null")


def _stop_index(
    *,
    current_manifest: Mapping[str, Any],
    cell: Mapping[str, Any],
    stage_receipts: Mapping[str, Mapping[str, Any]],
) -> int | None:
    catalog = list(current_manifest.get("stage_catalog", ()))
    for index, stage_id in enumerate(catalog):
        receipt = stage_receipts.get(stage_id)
        if not isinstance(receipt, Mapping):
            continue
        disposition = receipt.get("terminal_disposition")
        if disposition not in AUTHORIZED_STOP_DISPOSITIONS:
            continue
        # A stop is lawful only at a stage the frozen current cell actually
        # admits as executable.  A fabricated stop on a frozen skip/preserve
        # stage cannot legalize downstream missing telemetry.
        if _stage_disposition(cell, stage_id) != "READY__RUN_LOCALLY":
            _fail("TC_UNAUTHORIZED_STOP", f"stop claimed at non-executable stage {stage_id}")
        return index
    return None


def _preserved_authority(
    stage_receipts: Mapping[str, Mapping[str, Any]], stage_id: str
) -> Mapping[str, Any]:
    receipt = stage_receipts.get(stage_id)
    if not isinstance(receipt, Mapping):
        _fail("TC_PRESERVED_RECEIPT_ABSENT", f"preserved stage receipt absent for {stage_id}")
    adjudication = receipt.get("t4_preserved_work_adjudication")
    if not isinstance(adjudication, Mapping):
        _fail("TC_PRESERVED_ADJUDICATION_ABSENT", f"T4 preserved-work adjudication absent for {stage_id}")
    if (
        adjudication.get("disposition") != PRESERVED_NO_NUMERIC
        or adjudication.get("numeric_credit_allowed") is not False
        or adjudication.get("missing_numeric_is_zero") is not False
    ):
        _fail(
            "TC_PRESERVED_DISPOSITION_INVALID",
            f"{stage_id} does not prove the exact no-numeric-credit preserved-work disposition",
        )
    return adjudication


def _skip_authority(
    *,
    current_manifest: Mapping[str, Any],
    cell: Mapping[str, Any],
    stage_receipts: Mapping[str, Mapping[str, Any]],
    stage_id: str,
) -> None:
    receipt = stage_receipts.get(stage_id)
    if not isinstance(receipt, Mapping):
        _fail("TC_NA_RECEIPT_ABSENT", f"frozen N/A stage receipt absent for {stage_id}")
    law_ref = _stage_law_ref(cell, stage_id)
    law = current_manifest.get("stop_laws", {}).get(law_ref)
    if (
        not law_ref
        or not isinstance(law, str)
        or receipt.get("stop_law_ref") != law_ref
        or receipt.get("stop_law") != law
    ):
        _fail("TC_NA_LAW_DRIFT", f"{stage_id} N/A claim is not bound to its exact frozen stop law")


def _metric_expectation(
    *,
    name: str,
    candidate: str,
    current_manifest: Mapping[str, Any],
    cell: Mapping[str, Any],
    stage_receipts: Mapping[str, Mapping[str, Any]],
    stop_at: int | None,
) -> str:
    stage_id = METRIC_STAGE.get(name)

    # S09 is explicitly DELETION_REGEN_OR_A_PERSISTENCE.  For A, the frozen
    # operation is persistence characterization, not delete/rebuild timing.
    if name == "delete_rebuild_wall_ns" and candidate == "A":
        return MetricState.NOT_APPLICABLE_BY_FROZEN_COURT.value

    if stage_id is None:
        return MetricState.MEASURED.value

    catalog = list(current_manifest.get("stage_catalog", ()))
    if stage_id not in catalog:
        _fail("TC_STAGE_CATALOG_DRIFT", f"metric {name} binds unknown stage {stage_id}")
    stage_index = catalog.index(stage_id)
    if stop_at is not None and stage_index > stop_at:
        return MetricState.NOT_REACHED_AUTHORIZED_STOP.value

    disposition = _stage_disposition(cell, stage_id)
    if disposition == "READY__RUN_LOCALLY":
        return MetricState.MEASURED.value
    if disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
        _skip_authority(
            current_manifest=current_manifest,
            cell=cell,
            stage_receipts=stage_receipts,
            stage_id=stage_id,
        )
        return MetricState.NOT_APPLICABLE_BY_FROZEN_COURT.value
    if disposition == "DONE__PRESERVE":
        _preserved_authority(stage_receipts, stage_id)
        return PRESERVED_NO_NUMERIC
    _fail("TC_METRIC_STAGE_DISPOSITION_INVALID", f"{name} binds unsupported disposition {disposition}")
    raise AssertionError("unreachable")


def _expected_lifecycle_actions(
    *,
    source: str,
    candidate: str,
    current_manifest: Mapping[str, Any],
    cell: Mapping[str, Any],
    stage_receipts: Mapping[str, Mapping[str, Any]],
    stop_at: int | None,
) -> Mapping[str, str]:
    del source
    expected: dict[str, str] = {}
    catalog = list(current_manifest.get("stage_catalog", ()))
    for stage_id, default_action in EXPECTED_LIFECYCLE_ACTION.items():
        if stage_id not in catalog:
            continue
        index = catalog.index(stage_id)
        if stop_at is not None and index > stop_at:
            continue
        disposition = _stage_disposition(cell, stage_id)
        if disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
            _skip_authority(
                current_manifest=current_manifest,
                cell=cell,
                stage_receipts=stage_receipts,
                stage_id=stage_id,
            )
            continue
        if disposition == "DONE__PRESERVE":
            continue
        if disposition != "READY__RUN_LOCALLY":
            _fail("TC_LIFECYCLE_STAGE_INVALID", f"{stage_id} has unsupported lifecycle disposition")
        action = (
            "AUDIT_REVALIDATION"
            if stage_id == "S09_DELETION_REGEN_OR_A_PERSISTENCE" and candidate == "A"
            else "DELETION_REGENERATION"
            if stage_id == "S09_DELETION_REGEN_OR_A_PERSISTENCE"
            else default_action
        )
        expected[stage_id] = action
    return expected


def validate_terminal_telemetry_completeness(
    *,
    telemetry: Mapping[str, Any],
    source: str,
    candidate: str,
    current_manifest: Mapping[str, Any],
    stage_receipts: Mapping[str, Mapping[str, Any]] | None = None,
    completed_qualifying_cell: bool,
) -> Mapping[str, Any]:
    """Return an immutable PASS receipt or raise TerminalCompletenessError.

    The function is intentionally selection-neutral: it checks whether the
    frozen evidence vector is complete for one cell and never compares values
    across candidates.
    """
    stage_receipts = dict(stage_receipts or {})
    cell = _cell_contract(current_manifest, source, candidate)

    if telemetry.get("schema") != TELEMETRY_CONTRACT_ID:
        _fail("TC_TELEMETRY_SCHEMA_DRIFT", "canonical T4 telemetry schema mismatch")
    if telemetry.get("metric_definition_hash") != METRIC_DEFINITION_HASH:
        _fail("TC_METRIC_DEFINITION_HASH_DRIFT", "metric-definition hash differs from frozen T4 definitions")
    if telemetry.get("metric_definitions") != metric_definition_manifest():
        _fail("TC_METRIC_DEFINITION_MANIFEST_DRIFT", "metric-definition manifest differs from frozen T4 definitions")
    if telemetry.get("semantic_state_was_modified_by_telemetry") is not False:
        _fail("TC_SEMANTIC_INTERFERENCE", "telemetry claims semantic modification")

    source_sha = current_manifest.get("sources", {}).get(source, {}).get("sha256")
    telemetry_cell = telemetry.get("cell")
    if not isinstance(telemetry_cell, Mapping):
        _fail("TC_TELEMETRY_CELL_ABSENT", "telemetry cell identity is absent")
    if (
        telemetry_cell.get("source_id") != source
        or telemetry_cell.get("candidate_id") != candidate
        or telemetry_cell.get("source_sha256") != source_sha
    ):
        _fail("TC_TELEMETRY_CELL_DRIFT", "telemetry cell does not match current source/candidate/root")

    metrics = telemetry.get("metrics")
    if not isinstance(metrics, Mapping):
        _fail("TC_METRIC_SET_ABSENT", "canonical telemetry metric set is absent")
    if set(metrics) != set(METRIC_DEFINITIONS):
        _fail(
            "TC_METRIC_SET_DRIFT",
            "canonical telemetry metric keys do not exactly equal the frozen T4 definition set",
        )
    for name in sorted(METRIC_DEFINITIONS):
        for metric_row in _metric_rows(telemetry, name):
            _validate_metric_row_shape(
                metric_row,
                name=name,
                source=source,
                source_sha256=str(source_sha),
                candidate=candidate,
            )

    stop_at = _stop_index(
        current_manifest=current_manifest,
        cell=cell,
        stage_receipts=stage_receipts,
    )
    if completed_qualifying_cell and stop_at is not None:
        _fail("TC_COMPLETED_CELL_HAS_STOP", "a completed qualifying cell cannot also claim an authorized early stop")

    obligations: dict[str, str] = {}
    for name in FROZEN_DISPOSITIVE_METRICS:
        if name not in METRIC_DEFINITIONS:
            _fail("TC_FROZEN_METRIC_UNKNOWN", f"frozen metric {name} is absent from T4 definitions")
        expectation = _metric_expectation(
            name=name,
            candidate=candidate,
            current_manifest=current_manifest,
            cell=cell,
            stage_receipts=stage_receipts,
            stop_at=stop_at,
        )
        rows = _metric_rows(telemetry, name)
        observed_states = {str(row.get("state")) for row in rows}

        if expectation == PRESERVED_NO_NUMERIC:
            if observed_states != {MetricState.MEASUREMENT_NOT_CAPTURED.value}:
                _fail(
                    "TC_PRESERVED_NUMERIC_CREDIT_FORBIDDEN",
                    f"{name} may not acquire numeric credit for exact preserved/no-telemetry work",
                )
            obligations[name] = PRESERVED_NO_NUMERIC
            continue

        if observed_states != {expectation}:
            code = (
                "TC_REQUIRED_METRIC_NOT_MEASURED"
                if expectation == MetricState.MEASURED.value
                else "TC_METRIC_DISPOSITION_INVALID"
            )
            _fail(code, f"{name} expected {expectation} but observed {sorted(observed_states)}")
        obligations[name] = expectation

    summary = telemetry.get("telemetry_summary")
    if not isinstance(summary, Mapping):
        _fail("TC_TELEMETRY_SUMMARY_ABSENT", "telemetry completeness flags are absent")
    if completed_qualifying_cell:
        if summary.get("process_metrics_sealed") is not True:
            _fail("TC_PROCESS_SEAL_INCOMPLETE", "completed cell lacks sealed CPU/RSS/wall process accounting")
        if summary.get("io_event_stream_sealed") is not True:
            _fail("TC_IO_SEAL_INCOMPLETE", "completed cell lacks complete event-level I/O accounting")
        if summary.get("scratch_high_water_sealed") is not True:
            _fail("TC_SCRATCH_SEAL_INCOMPLETE", "completed cell lacks complete scratch high-water accounting")

    process_envelopes = telemetry.get("process_envelopes")
    if completed_qualifying_cell:
        if not isinstance(process_envelopes, Sequence) or isinstance(process_envelopes, (str, bytes)):
            _fail("TC_PROCESS_ENVELOPE_ABSENT", "completed cell lacks process-envelope evidence")
        mains = [
            row for row in process_envelopes
            if isinstance(row, Mapping) and row.get("role") == "MAIN"
        ]
        if len(mains) != 1:
            _fail("TC_PROCESS_MAIN_CARDINALITY", "completed cell must bind exactly one MAIN process envelope")

    expected_actions = _expected_lifecycle_actions(
        source=source,
        candidate=candidate,
        current_manifest=current_manifest,
        cell=cell,
        stage_receipts=stage_receipts,
        stop_at=stop_at,
    )
    lifecycle = telemetry.get("lifecycle_action_receipts")
    if not isinstance(lifecycle, Sequence) or isinstance(lifecycle, (str, bytes)):
        _fail("TC_LIFECYCLE_RECEIPTS_ABSENT", "telemetry lifecycle receipt set is absent")
    observed_actions: dict[str, set[str]] = {}
    for row in lifecycle:
        if not isinstance(row, Mapping):
            _fail("TC_LIFECYCLE_RECEIPT_INVALID", "malformed lifecycle receipt")
        phase = row.get("phase_id")
        action = row.get("action_type")
        if isinstance(phase, str) and isinstance(action, str):
            observed_actions.setdefault(phase, set()).add(action)
    for stage_id, action in expected_actions.items():
        if observed_actions.get(stage_id) != {action}:
            _fail(
                "TC_REQUIRED_LIFECYCLE_EVIDENCE_MISSING",
                f"{stage_id} requires exactly lifecycle action {action}",
            )

    core = {
        "schema": COMPLETENESS_SCHEMA,
        "status": "PASS",
        "source": source,
        "candidate": candidate,
        "source_sha256": source_sha,
        "metric_definition_hash": METRIC_DEFINITION_HASH,
        "completed_qualifying_cell": bool(completed_qualifying_cell),
        "authorized_stop_stage_index": stop_at,
        "frozen_metric_obligations": dict(sorted(obligations.items())),
        "required_lifecycle_actions": dict(sorted(expected_actions.items())),
        "selection_neutral": True,
        "ranking_or_selection": False,
        "candidate_comparison_performed": False,
    }
    core["receipt_identity"] = _hash(core)
    return core


__all__ = [
    "COMPLETENESS_SCHEMA",
    "FROZEN_DISPOSITIVE_METRICS",
    "TerminalCompletenessError",
    "validate_terminal_telemetry_completeness",
]
