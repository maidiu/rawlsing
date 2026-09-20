import unittest

from rawlsing_next.fiabc_telemetry_semantics import (
    CellIdentity,
    CostClass,
    LifecycleActionReceipt,
    MetricState,
    ObservationContext,
    ProcessEnvelopeReceipt,
    TelemetryContractError,
    TelemetryLedger,
)


SHA = "a" * 64


def cell(candidate="A", source="LITS_I"):
    return CellIdentity(
        source_id=source,
        source_sha256=SHA,
        candidate_id=candidate,
        workload_id="LOCK2_WORKLOAD",
        authority_set_id="FROZEN_AUTHORITY_SET",
    )


def ctx(candidate="A", source="LITS_I", phase="S04_I03", cost=CostClass.C3, process="p-main"):
    return ObservationContext(
        source_id=source,
        source_sha256=SHA,
        candidate_id=candidate,
        phase_id=phase,
        process_token=process,
        cost_class=cost,
        evidence_ref="test-evidence",
    )


def main_receipt(candidate="A", source="LITS_I", rss_scope="CANDIDATE_PROCESS_LOCAL"):
    return ProcessEnvelopeReceipt(
        cell=cell(candidate, source),
        phase_id="__CANDIDATE_ENVELOPE__",
        process_token=f"{candidate}-main",
        pid=100 + ord(candidate),
        role="MAIN",
        parent_process_token=None,
        cpu_scope="PROCESS_SELF_ONLY",
        rss_scope=rss_scope,
        cpu_user_start_ns=1_000,
        cpu_user_stop_ns=1_100,
        cpu_system_start_ns=2_000,
        cpu_system_stop_ns=2_020,
        wall_start_ns=10_000,
        wall_stop_ns=20_000,
        peak_rss_bytes=500,
        evidence_ref="i06a-main",
    )


class TelemetrySemanticsHostileTests(unittest.TestCase):
    def test_same_immutable_metric_twice_is_rejected(self):
        t = TelemetryLedger(cell())
        c = ctx(phase="S04_I03")
        t.record_duration(
            "cold_i03_latency_ns", c,
            monotonic_start_ns=10, monotonic_stop_ns=20,
            state_predicate_ref="COLD_STATE_1",
        )
        with self.assertRaises(TelemetryContractError):
            t.record_duration(
                "cold_i03_latency_ns", c,
                monotonic_start_ns=30, monotonic_stop_ns=40,
                state_predicate_ref="COLD_STATE_1",
            )

    def test_later_cold_work_cannot_overwrite_earlier_cold_metric(self):
        t = TelemetryLedger(cell())
        t.record_duration(
            "cold_i03_latency_ns", ctx(phase="S04_I03"),
            monotonic_start_ns=10, monotonic_stop_ns=20,
            state_predicate_ref="CANONICAL_COLD",
        )
        with self.assertRaises(TelemetryContractError):
            t.record_duration(
                "cold_i03_latency_ns", ctx(phase="S07_COLD_RESEARCH"),
                monotonic_start_ns=50, monotonic_stop_ns=90,
                state_predicate_ref="LATER_COLD_LIKE_WORK",
            )

    def test_missing_telemetry_is_typed_null_never_zero(self):
        t = TelemetryLedger(cell())
        r = t.receipt(candidate_semantic_state="PASS")
        missing = r["metrics"]["cold_i03_latency_ns"]
        self.assertEqual(missing["state"], MetricState.MEASUREMENT_NOT_CAPTURED.value)
        self.assertIsNone(missing["value"])
        self.assertNotEqual(missing["value"], 0)

    def test_cumulative_cpu_counter_is_converted_to_phase_delta(self):
        t = TelemetryLedger(cell())
        rec = t.observe_phase_cpu_counters(
            ctx(phase="S05_I05"),
            user_start_ns=1_000,
            user_stop_ns=1_250,
            system_start_ns=2_000,
            system_stop_ns=2_075,
            evidence_ref="phase-counters",
        )
        self.assertEqual(rec.user_cpu_ns, 250)
        self.assertEqual(rec.system_cpu_ns, 75)
        self.assertNotEqual(rec.user_cpu_ns, 1_250)

    def test_nested_phase_cpu_cannot_double_count_candidate_total(self):
        t = TelemetryLedger(cell())
        t.record_process_envelope(main_receipt())
        t.observe_phase_cpu_counters(
            ctx(phase="OUTER", process="A-main"),
            user_start_ns=0, user_stop_ns=100,
            system_start_ns=0, system_stop_ns=20,
            evidence_ref="outer",
        )
        t.observe_phase_cpu_counters(
            ctx(phase="INNER", process="A-main"),
            user_start_ns=20, user_stop_ns=60,
            system_start_ns=5, system_stop_ns=10,
            parent_phase_id="OUTER",
            evidence_ref="inner",
        )
        t.seal_process_metrics(evidence_ref="i06a-envelope")
        r = t.receipt(candidate_semantic_state="PASS")
        self.assertEqual(r["metrics"]["cpu_user_ns"]["value"], 100)
        self.assertEqual(r["metrics"]["cpu_system_ns"]["value"], 20)
        phase_user = sum(x["user_cpu_ns"] for x in r["phase_cpu"])
        self.assertEqual(phase_user, 140)
        self.assertNotEqual(r["metrics"]["cpu_user_ns"]["value"], phase_user)

    def test_process_global_rss_is_rejected(self):
        t = TelemetryLedger(cell())
        with self.assertRaises(TelemetryContractError):
            t.record_process_envelope(
                main_receipt(rss_scope="COURT_PROCESS_GLOBAL_HISTORY")
            )

    def test_endpoint_directory_size_cannot_masquerade_as_bytes_written(self):
        t = TelemetryLedger(cell())
        c = ctx(phase="S16", cost=CostClass.C2)
        t.record_observed_value(
            "durable_transformed_regenerable_bytes", c, 500,
            evidence_kind="CLASSIFIED_ENDPOINT_INVENTORY",
        )
        with self.assertRaises(TelemetryContractError):
            t.record_observed_value(
                "bytes_written", c, 500,
                evidence_kind="ENDPOINT_DIRECTORY_SIZE",
            )
        r = t.receipt(candidate_semantic_state="PASS")
        self.assertIsNone(r["metrics"]["bytes_written"]["value"])

    def test_hardcoded_zero_rewrite_cannot_satisfy_observed_accounting(self):
        t = TelemetryLedger(cell())
        c = ctx(phase="S09", cost=CostClass.C2)
        with self.assertRaises(TelemetryContractError):
            t.record_observed_value(
                "bytes_rewritten", c, 0,
                evidence_kind="HARDCODED_CONSTANT",
            )
        t.observe_io(c, operation="WRITE", byte_count=9, object_id="new", rewrite_of="old")
        t.seal_io_accounting(c)
        r = t.receipt(candidate_semantic_state="PASS")
        self.assertEqual(r["metrics"]["bytes_rewritten"]["value"], 9)

    def test_scratch_endpoint_cannot_masquerade_as_peak(self):
        t = TelemetryLedger(cell())
        c = ctx(phase="S01", cost=CostClass.C2)
        with self.assertRaises(TelemetryContractError):
            t.record_observed_value(
                "peak_scratch_bytes", c, 40,
                evidence_kind="ENDPOINT_DIRECTORY_SIZE",
            )
        t.observe_scratch_size(c, object_id="a", current_size_bytes=100)
        t.observe_scratch_size(c, object_id="b", current_size_bytes=40)
        t.observe_scratch_remove(c, object_id="a")
        t.seal_scratch_accounting(c)
        r = t.receipt(candidate_semantic_state="PASS")
        self.assertEqual(r["metrics"]["peak_scratch_bytes"]["value"], 140)
        self.assertEqual(r["metrics"]["peak_scratch_file_count"]["value"], 2)

    def test_candidate_a_metric_cannot_be_attributed_to_b(self):
        t = TelemetryLedger(cell("A"))
        with self.assertRaises(TelemetryContractError):
            t.record_duration(
                "cold_i03_latency_ns", ctx(candidate="B"),
                monotonic_start_ns=1, monotonic_stop_ns=2,
                state_predicate_ref="COLD",
            )

    def test_metric_without_exact_phase_identity_fails_closed(self):
        with self.assertRaises(TelemetryContractError):
            ObservationContext(
                source_id="LITS_I",
                source_sha256=SHA,
                candidate_id="A",
                phase_id="",
                process_token="p",
                cost_class=CostClass.C2,
            )

    def test_candidate_neutral_production_excluded_but_candidate_access_counted(self):
        t = TelemetryLedger(cell())
        c0 = ctx(phase="COMMON_PREP", cost=CostClass.C0, process="common-prep")
        c1 = ctx(phase="S01", cost=CostClass.C1, process="A-main")
        seal = ctx(phase="__CANDIDATE_ENVELOPE__", cost=CostClass.C2, process="A-main")
        t.observe_io(c0, operation="READ", byte_count=100, object_id="frozen-authority")
        t.observe_io(c1, operation="READ", byte_count=25, object_id="frozen-authority")
        t.seal_io_accounting(seal)
        r = t.receipt(candidate_semantic_state="PASS")
        self.assertEqual(r["metrics"]["bytes_read"]["value"], 25)
        self.assertFalse(r["io_events"][0]["charged_to_candidate"])
        self.assertTrue(r["io_events"][1]["charged_to_candidate"])

    def test_metric_definition_hash_is_identical_for_a_b_c(self):
        hashes = {
            TelemetryLedger(cell(candidate)).receipt(candidate_semantic_state="PASS")[
                "metric_definition_hash"
            ]
            for candidate in ("A", "B", "C")
        }
        self.assertEqual(len(hashes), 1)

    def test_child_cpu_is_added_once_and_rss_uses_max_not_sum(self):
        t = TelemetryLedger(cell())
        main = main_receipt()
        t.record_process_envelope(main)
        child = ProcessEnvelopeReceipt(
            cell=cell(),
            phase_id="S15_FRESH_REPLAY",
            process_token="A-child",
            pid=999,
            role="CHILD",
            parent_process_token="A-main",
            cpu_scope="PROCESS_SELF_ONLY",
            rss_scope="CANDIDATE_PROCESS_LOCAL",
            cpu_user_start_ns=0,
            cpu_user_stop_ns=30,
            cpu_system_start_ns=0,
            cpu_system_stop_ns=10,
            wall_start_ns=12_000,
            wall_stop_ns=13_000,
            peak_rss_bytes=900,
            evidence_ref="i06a-child",
        )
        t.record_process_envelope(child)
        t.seal_process_metrics(evidence_ref="i06a-envelopes")
        r = t.receipt(candidate_semantic_state="PASS")
        self.assertEqual(r["metrics"]["cpu_user_ns"]["value"], 130)
        self.assertEqual(r["metrics"]["cpu_system_ns"]["value"], 30)
        self.assertEqual(r["metrics"]["peak_rss_bytes"]["value"], 900)

    def test_fresh_replay_child_cpu_binds_exact_lifecycle_action(self):
        t = TelemetryLedger(cell())
        t.record_process_envelope(main_receipt())
        child = ProcessEnvelopeReceipt(
            cell=cell(),
            phase_id="S15_FRESH_REPLAY",
            process_token="A-child",
            pid=999,
            role="CHILD",
            parent_process_token="A-main",
            cpu_scope="PROCESS_SELF_ONLY",
            rss_scope="CANDIDATE_PROCESS_LOCAL",
            cpu_user_start_ns=0,
            cpu_user_stop_ns=30,
            cpu_system_start_ns=0,
            cpu_system_stop_ns=10,
            wall_start_ns=12_000,
            wall_stop_ns=13_000,
            peak_rss_bytes=900,
            evidence_ref="i06a-child",
        )
        t.record_process_envelope(child)
        t.bind_lifecycle_receipt(LifecycleActionReceipt(
            cell=cell(),
            action_id="fresh-replay-1",
            action_type="FRESH_PROCESS_REPLAY",
            phase_id="S15_FRESH_REPLAY",
            process_token="A-child",
            outcome="COMPLETED",
            evidence_ref="i06c-action",
        ))
        replay_ctx = ObservationContext(
            source_id="LITS_I",
            source_sha256=SHA,
            candidate_id="A",
            phase_id="S15_FRESH_REPLAY",
            process_token="A-child",
            cost_class=CostClass.C3,
            lifecycle_action_id="fresh-replay-1",
            evidence_ref="i06a-child",
        )
        t.seal_fresh_process_replay_cpu(process_token="A-child", ctx=replay_ctx)
        r = t.receipt(candidate_semantic_state="PASS")
        rows = r["metrics"]["fresh_process_replay_cpu_ns"]
        self.assertEqual(rows[0]["value"], 40)

    def test_cpu_scope_with_children_already_included_is_rejected(self):
        bad = ProcessEnvelopeReceipt(
            cell=cell(),
            phase_id="__CANDIDATE_ENVELOPE__",
            process_token="bad-main",
            pid=123,
            role="MAIN",
            parent_process_token=None,
            cpu_scope="SELF_PLUS_CHILDREN",
            rss_scope="CANDIDATE_PROCESS_LOCAL",
            cpu_user_start_ns=0,
            cpu_user_stop_ns=100,
            cpu_system_start_ns=0,
            cpu_system_stop_ns=10,
            wall_start_ns=0,
            wall_stop_ns=1000,
            peak_rss_bytes=100,
            evidence_ref="bad-scope",
        )
        with self.assertRaises(TelemetryContractError):
            TelemetryLedger(cell()).record_process_envelope(bad)

    def test_cold_and_warm_are_distinct_immutable_fields(self):
        t = TelemetryLedger(cell())
        t.record_duration(
            "cold_i03_latency_ns", ctx(phase="S04"),
            monotonic_start_ns=0, monotonic_stop_ns=100,
            state_predicate_ref="COLD_STATE",
        )
        t.record_duration(
            "warm_i03_latency_ns", ctx(phase="S08"),
            monotonic_start_ns=200, monotonic_stop_ns=230,
            state_predicate_ref="WARM_STATE",
        )
        r = t.receipt(candidate_semantic_state="PASS")
        self.assertEqual(r["metrics"]["cold_i03_latency_ns"]["value"], 100)
        self.assertEqual(r["metrics"]["warm_i03_latency_ns"]["value"], 30)

    def test_telemetry_does_not_upgrade_semantic_failure(self):
        t = TelemetryLedger(cell())
        r = t.receipt(candidate_semantic_state="SEMANTIC_FAIL")
        self.assertEqual(r["candidate_semantic_state"], "SEMANTIC_FAIL")
        self.assertFalse(r["semantic_state_was_modified_by_telemetry"])


if __name__ == "__main__":
    unittest.main()
