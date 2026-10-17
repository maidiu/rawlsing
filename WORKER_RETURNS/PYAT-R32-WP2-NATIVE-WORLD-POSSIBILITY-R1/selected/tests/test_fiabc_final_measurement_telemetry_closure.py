from __future__ import annotations

import tempfile
import types
import unittest
from pathlib import Path

from rawlsing_next import ee_p2x_darwin_stage_backend as backend
from rawlsing_next import fiabc_live_accounting_binding as live
from rawlsing_next.fiabc_telemetry_semantics import (
    CellIdentity,
    CostClass,
    LifecycleActionReceipt,
    METRIC_DEFINITIONS,
    MetricState,
    ObservationContext,
    ProcessEnvelopeReceipt,
    TelemetryContractError,
    TelemetryLedger,
)


SHA = "a" * 64


def cell(candidate="A"):
    return CellIdentity(
        source_id="LITS_I",
        source_sha256=SHA,
        candidate_id=candidate,
        workload_id="WORKLOAD",
        authority_set_id="AUTHORITY",
    )


def ctx(*, candidate="A", phase="S10_SOURCE_RELEASE_INVALIDATION",
        process="A-main", action=None, cost=CostClass.C2):
    return ObservationContext(
        source_id="LITS_I",
        source_sha256=SHA,
        candidate_id=candidate,
        phase_id=phase,
        process_token=process,
        cost_class=cost,
        lifecycle_action_id=action,
        evidence_ref="qualification",
    )


def main_process():
    return ProcessEnvelopeReceipt(
        cell=cell(),
        phase_id="__CANDIDATE_ENVELOPE__",
        process_token="A-main",
        pid=100,
        role="MAIN",
        parent_process_token=None,
        cpu_scope="PROCESS_SELF_ONLY",
        rss_scope="CANDIDATE_PROCESS_LOCAL",
        cpu_user_start_ns=10,
        cpu_user_stop_ns=110,
        cpu_system_start_ns=20,
        cpu_system_stop_ns=50,
        wall_start_ns=1_000,
        wall_stop_ns=2_000,
        peak_rss_bytes=400,
        evidence_ref="main",
    )


class FinalMeasurementTelemetryClosureTests(unittest.TestCase):
    def test_exact_35_metric_registry_has_producer_or_frozen_applicability(self):
        production = live.metric_production_manifest()
        self.assertEqual(len(METRIC_DEFINITIONS), 35)
        self.assertEqual(set(production), set(METRIC_DEFINITIONS))
        self.assertEqual(set(backend.METRICS), set(METRIC_DEFINITIONS))
        for row in production.values():
            self.assertTrue(row["producer"])
            self.assertTrue(row["applicability"])
        self.assertEqual(
            production["delete_rebuild_wall_ns"]["applicability"],
            "B_C_MEASURED__A_FROZEN_NOT_APPLICABLE",
        )

    def test_io_seal_requires_complete_bridge_coverage(self):
        complete = [
            {"observations": {"io_coverage_complete": True}},
            {"observations": {"io_coverage_complete": True}},
        ]
        live._require_complete_stage_coverage(
            complete, "io_coverage_complete", "canonical I/O metrics"
        )
        with self.assertRaises(live.LiveAccountingError):
            live._require_complete_stage_coverage(
                complete + [{"observations": {}}],
                "io_coverage_complete",
                "canonical I/O metrics",
            )

    def test_scratch_seal_requires_complete_bridge_coverage(self):
        with self.assertRaises(live.LiveAccountingError):
            live._require_complete_stage_coverage(
                [{"observations": {"scratch_coverage_complete": False}}],
                "scratch_coverage_complete",
                "scratch high-water metrics",
            )

    def test_scratch_peak_is_event_high_water_not_endpoint_size(self):
        ledger = TelemetryLedger(cell())
        c = ctx(phase="S01_CANDIDATE_PREPARATION_BUILD")
        ledger.observe_empty_scratch_baseline(c)
        ledger.observe_scratch_size(c, object_id="tmp-a", current_size_bytes=100)
        ledger.observe_scratch_size(c, object_id="tmp-b", current_size_bytes=30)
        ledger.observe_scratch_remove(c, object_id="tmp-a")
        ledger.observe_scratch_size(c, object_id="tmp-b", current_size_bytes=40)
        ledger.seal_scratch_accounting(c)
        receipt = ledger.receipt(candidate_semantic_state="PASS")
        self.assertEqual(receipt["metrics"]["peak_scratch_bytes"]["value"], 130)
        self.assertEqual(receipt["metrics"]["peak_scratch_file_count"]["value"], 2)

    def test_invalidation_wall_and_rewrite_are_bound_to_exact_action(self):
        ledger = TelemetryLedger(cell())
        ledger.bind_lifecycle_receipt(LifecycleActionReceipt(
            cell=cell(),
            action_id="s10",
            action_type="SOURCE_INVALIDATION",
            phase_id="S10_SOURCE_RELEASE_INVALIDATION",
            process_token="A-main",
            outcome="EXECUTED_NOW",
            evidence_ref="s10-action",
        ))
        ledger.bind_lifecycle_receipt(LifecycleActionReceipt(
            cell=cell(),
            action_id="s11",
            action_type="AUTHORITY_SEMANTIC_INVALIDATION",
            phase_id="S11_SEMANTIC_AUTHORITY_INVALIDATION",
            process_token="A-main",
            outcome="EXECUTED_NOW",
            evidence_ref="s11-action",
        ))
        s10 = ctx(action="s10")
        s11 = ctx(phase="S11_SEMANTIC_AUTHORITY_INVALIDATION", action="s11")
        ledger.record_duration(
            "source_release_invalidation_wall_ns",
            s10,
            monotonic_start_ns=100,
            monotonic_stop_ns=145,
            state_predicate_ref="EXECUTED_SOURCE_INVALIDATION",
        )
        ledger.observe_io(
            s10, operation="WRITE", byte_count=7,
            object_id="state-a", rewrite_of="state-a",
        )
        ledger.observe_io(
            s11, operation="WRITE", byte_count=11,
            object_id="state-b", rewrite_of="state-b",
        )
        ledger.seal_lifecycle_rewrite_bytes(
            "source_release_invalidation_bytes_rewritten", s10
        )
        seal = ctx(phase="__IO_EVENT_LEDGER__", action=None)
        ledger.seal_io_accounting(seal)
        receipt = ledger.receipt(candidate_semantic_state="PASS")
        self.assertEqual(
            receipt["metrics"]["source_release_invalidation_wall_ns"][0]["value"], 45
        )
        self.assertEqual(
            receipt["metrics"]["source_release_invalidation_bytes_rewritten"][0]["value"], 7
        )
        self.assertEqual(receipt["metrics"]["bytes_rewritten"]["value"], 18)

    def test_fresh_replay_cpu_uses_exact_child_and_is_not_double_counted(self):
        ledger = TelemetryLedger(cell())
        ledger.record_process_envelope(main_process())
        child = ProcessEnvelopeReceipt(
            cell=cell(),
            phase_id="S15_FRESH_PROCESS_REPLAY",
            process_token="fresh-child",
            pid=101,
            role="CHILD",
            parent_process_token="A-main",
            cpu_scope="PROCESS_SELF_ONLY",
            rss_scope="CANDIDATE_PROCESS_LOCAL",
            cpu_user_start_ns=0,
            cpu_user_stop_ns=30,
            cpu_system_start_ns=0,
            cpu_system_stop_ns=12,
            wall_start_ns=1_200,
            wall_stop_ns=1_400,
            peak_rss_bytes=500,
            evidence_ref="fresh-child",
        )
        ledger.record_process_envelope(child)
        ledger.bind_lifecycle_receipt(LifecycleActionReceipt(
            cell=cell(),
            action_id="fresh",
            action_type="FRESH_PROCESS_REPLAY",
            phase_id="S15_FRESH_PROCESS_REPLAY",
            process_token="A-main",
            outcome="EXECUTED_NOW",
            evidence_ref="fresh-action",
        ))
        child_ctx = ctx(
            phase="S15_FRESH_PROCESS_REPLAY",
            process="fresh-child",
            action="fresh",
            cost=CostClass.C3,
        )
        ledger.seal_fresh_process_replay_cpu(
            process_token="fresh-child", ctx=child_ctx
        )
        ledger.seal_process_metrics(evidence_ref="all-processes")
        receipt = ledger.receipt(candidate_semantic_state="PASS")
        self.assertEqual(
            receipt["metrics"]["fresh_process_replay_cpu_ns"][0]["value"], 42
        )
        self.assertEqual(receipt["metrics"]["cpu_user_ns"]["value"], 130)
        self.assertEqual(receipt["metrics"]["cpu_system_ns"]["value"], 42)
        with self.assertRaises(TelemetryContractError):
            ledger.record_process_envelope(child)

    def test_durable_state_size_classification_is_exact_and_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            durable = root / "durable"
            durable.mkdir()
            (durable / "lits_a_r5").mkdir()
            (durable / "lits_a_r5" / "root.json").write_bytes(b"12345")
            (durable / "lits_a_r5.parentage.json").write_bytes(b"1234567")
            (durable / "ee_p2x_backend_state.json").write_bytes(b"ignored")
            fake = types.SimpleNamespace(
                roots=types.SimpleNamespace(durable=durable)
            )
            first = backend._durable_state_sizes(fake)
            second = backend._durable_state_sizes(fake)
            self.assertEqual(first, second)
            self.assertEqual(first[0], 7)
            self.assertEqual(first[1], 5)
            (durable / "unclassified.bin").write_bytes(b"x")
            with self.assertRaises(backend.BackendStop):
                backend._durable_state_sizes(fake)

    def test_retained_state_size_is_deterministic_and_cycle_safe(self):
        value = {"a": [1, 2, 3]}
        value["cycle"] = value
        first = backend._deep_size_bytes(value)
        second = backend._deep_size_bytes(value)
        self.assertEqual(first, second)
        self.assertGreater(first, 0)

    def test_state_size_and_moving_parts_records_remain_cell_bound(self):
        ledger = TelemetryLedger(cell("A"))
        a = ctx(candidate="A", phase="S16_TERMINAL_METRIC_VECTOR_COMPLETENESS")
        ledger.record_observed_value(
            "durable_authoritative_bytes", a, 17,
            evidence_kind="EXACT_CLASSIFIED_DURABLE_STATE",
        )
        ledger.record_observed_value(
            "implementation_moving_parts_count", a, 4,
            evidence_kind="EXACT_RUNTIME_PART_MANIFEST",
        )
        with self.assertRaises(TelemetryContractError):
            ledger.record_observed_value(
                "durable_transformed_regenerable_bytes",
                ctx(candidate="B", phase="S16_TERMINAL_METRIC_VECTOR_COMPLETENESS"),
                1,
                evidence_kind="WRONG_CELL",
            )

    def test_frozen_not_applicable_is_typed_null_not_zero(self):
        ledger = TelemetryLedger(cell())
        c = ctx(phase="S09_DELETION_REGEN_OR_A_PERSISTENCE")
        ledger.mark_lifecycle_not_applicable(
            "delete_rebuild_wall_ns",
            c,
            reason="CANDIDATE_A_S09_FROZEN_PERSISTENCE_AUDIT",
        )
        row = ledger.receipt(candidate_semantic_state="PASS")["metrics"]["delete_rebuild_wall_ns"][0]
        self.assertEqual(row["state"], MetricState.NOT_APPLICABLE_BY_FROZEN_COURT.value)
        self.assertIsNone(row["value"])

    def test_io_and_scratch_seals_are_write_once(self):
        ledger = TelemetryLedger(cell())
        c = ctx(phase="S16_TERMINAL_METRIC_VECTOR_COMPLETENESS")
        ledger.observe_io(c, operation="READ", byte_count=3, object_id="x")
        ledger.seal_io_accounting(c)
        with self.assertRaises(TelemetryContractError):
            ledger.seal_io_accounting(c)
        other = TelemetryLedger(cell())
        other.observe_empty_scratch_baseline(c)
        other.seal_scratch_accounting(c)
        with self.assertRaises(TelemetryContractError):
            other.seal_scratch_accounting(c)


if __name__ == "__main__":
    unittest.main()
