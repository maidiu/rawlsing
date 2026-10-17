import copy
import unittest

from rawlsing_next.fiabc_telemetry_semantics import (
    METRIC_DEFINITION_HASH,
    METRIC_DEFINITIONS,
    MetricGrain,
    MetricState,
    metric_definition_manifest,
)
from rawlsing_next.fiabc_terminal_completeness import (
    FROZEN_DISPOSITIVE_METRICS,
    METRIC_STAGE as COMPLETENESS_METRIC_STAGE,
    TerminalCompletenessError,
    validate_terminal_telemetry_completeness,
)


SHA = "a" * 64
STAGES = [
    "S00_SOURCE_PREFLIGHT_IDENTITY",
    "S01_CANDIDATE_PREPARATION_BUILD",
    "S02_C11_REACHABILITY",
    "S03_PARITY_ORACLE_GATE",
    "S04_I03_EXECUTION",
    "S05_I05_LEARNED_PRODUCTION",
    "S06_PROVENANCE_AUDIT",
    "S07_COLD_RESEARCH",
    "S08_WARM_REPEATED_RESEARCH",
    "S09_DELETION_REGEN_OR_A_PERSISTENCE",
    "S10_SOURCE_RELEASE_INVALIDATION",
    "S11_SEMANTIC_AUTHORITY_INVALIDATION",
    "S12_STALE_CACHE_OR_PERSISTENT_STATE",
    "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE",
    "S14_INTERRUPTION_RECOVERY",
    "S15_FRESH_PROCESS_REPLAY",
    "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
]

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

ACTION_BY_STAGE = {
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


def manifest(source="LITS_I", candidate="A"):
    stages = {}
    for index, stage in enumerate(STAGES):
        nxt = STAGES[index + 1] if index + 1 < len(STAGES) else "COURT/S17"
        stages[stage] = ["READY__RUN_LOCALLY", None, False, True, nxt]
    return {
        "sources": {source: {"sha256": SHA}},
        "stage_catalog": list(STAGES),
        "stop_laws": {
            "PURE_B_NO_CACHE": "Candidate B has no optional cache.",
            "C_ZERO_ACCELERATOR_NO_CACHE": "WVS7/C has zero authorized accelerators.",
        },
        "cells": [{
            "source": source,
            "candidate": candidate,
            "stages": stages,
        }],
    }


def row(name, source, candidate, state, value=None, phase=None):
    d = METRIC_DEFINITIONS[name]
    return {
        "name": name,
        "state": state,
        "value": value,
        "unit": d.unit,
        "source_id": source,
        "source_sha256": SHA,
        "candidate_id": candidate,
        "phase_id": phase or METRIC_STAGE.get(name) or "__CELL__",
        "process_token": "p-main",
        "cost_class": "C2",
        "lifecycle_action_id": None,
        "evidence_kind": "TEST",
        "evidence_ref": "synthetic-hostile-test",
    }


def telemetry(source="LITS_I", candidate="A", *, skipped=(), stop_after=None):
    metrics = {}
    for name, definition in METRIC_DEFINITIONS.items():
        state = MetricState.MEASUREMENT_NOT_CAPTURED.value
        value = None
        if name in FROZEN_DISPOSITIVE_METRICS:
            state = MetricState.MEASURED.value
            value = 1
        if name == "delete_rebuild_wall_ns" and candidate == "A":
            state = MetricState.NOT_APPLICABLE_BY_FROZEN_COURT.value
            value = None
        if stop_after is not None and name in FROZEN_DISPOSITIVE_METRICS:
            stage = METRIC_STAGE.get(name)
            if stage is not None and STAGES.index(stage) > STAGES.index(stop_after):
                state = MetricState.NOT_REACHED_AUTHORIZED_STOP.value
                value = None
        rec = row(name, source, candidate, state, value)
        metrics[name] = [rec] if definition.grain != MetricGrain.CANDIDATE else rec

    lifecycle = []
    for stage, action in ACTION_BY_STAGE.items():
        if stage in skipped:
            continue
        if stop_after is not None and STAGES.index(stage) > STAGES.index(stop_after):
            continue
        if stage == "S09_DELETION_REGEN_OR_A_PERSISTENCE" and candidate == "A":
            action = "AUDIT_REVALIDATION"
        lifecycle.append({
            "action_id": "a-" + stage,
            "action_type": action,
            "phase_id": stage,
            "process_token": "p-main",
            "outcome": "EXECUTED_NOW",
            "evidence_ref": "synthetic-hostile-test",
        })

    return {
        "schema": "FIABC_W3_I06B_TELEMETRY_SEMANTICS@1.0.0",
        "metric_definition_hash": METRIC_DEFINITION_HASH,
        "metric_definitions": metric_definition_manifest(),
        "cell": {
            "source_id": source,
            "source_sha256": SHA,
            "candidate_id": candidate,
            "workload_id": "workload",
            "authority_set_id": "authority",
        },
        "candidate_semantic_state": "PASS",
        "semantic_state_was_modified_by_telemetry": False,
        "telemetry_summary": {
            "measured_records": 1,
            "measurement_not_captured_records": 0,
            "io_event_stream_sealed": True,
            "scratch_high_water_sealed": True,
            "process_metrics_sealed": True,
        },
        "metrics": metrics,
        "phase_cpu": [],
        "process_envelopes": [{"role": "MAIN", "process_token": "p-main"}],
        "lifecycle_action_receipts": lifecycle,
        "io_events": [],
    }


def set_metric_state(doc, name, state, value=None):
    raw = doc["metrics"][name]
    rows = raw if isinstance(raw, list) else [raw]
    for rec in rows:
        rec["state"] = state
        rec["value"] = value


class TerminalCompletenessHostileTests(unittest.TestCase):
    def test_frozen_dispositive_metric_set_is_definition_identical_35_of_35(self):
        self.assertEqual(len(METRIC_DEFINITIONS), 35)
        self.assertEqual(len(FROZEN_DISPOSITIVE_METRICS), 35)
        self.assertEqual(set(FROZEN_DISPOSITIVE_METRICS), set(METRIC_DEFINITIONS))

    def test_all_lifecycle_grain_metrics_bind_exact_governed_stages(self):
        lifecycle_names = {
            name for name, definition in METRIC_DEFINITIONS.items()
            if definition.grain == MetricGrain.LIFECYCLE
        }
        self.assertEqual(
            {name: COMPLETENESS_METRIC_STAGE.get(name) for name in lifecycle_names},
            {
                "delete_rebuild_wall_ns": "S09_DELETION_REGEN_OR_A_PERSISTENCE",
                "source_release_invalidation_recomputation_units": "S10_SOURCE_RELEASE_INVALIDATION",
                "source_release_invalidation_wall_ns": "S10_SOURCE_RELEASE_INVALIDATION",
                "source_release_invalidation_bytes_rewritten": "S10_SOURCE_RELEASE_INVALIDATION",
                "semantic_authority_invalidation_recomputation_units": "S11_SEMANTIC_AUTHORITY_INVALIDATION",
                "semantic_authority_invalidation_wall_ns": "S11_SEMANTIC_AUTHORITY_INVALIDATION",
                "semantic_authority_invalidation_bytes_rewritten": "S11_SEMANTIC_AUTHORITY_INVALIDATION",
                "fresh_process_replay_wall_ns": "S15_FRESH_PROCESS_REPLAY",
                "fresh_process_replay_cpu_ns": "S15_FRESH_PROCESS_REPLAY",
            },
        )

    def test_one_missing_required_metric_blocks(self):
        m = manifest()
        t = telemetry()
        del t["metrics"]["bytes_read"]
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_METRIC_SET_DRIFT"):
            validate_terminal_telemetry_completeness(
                telemetry=t, source="LITS_I", candidate="A",
                current_manifest=m, stage_receipts={},
                completed_qualifying_cell=True,
            )

    def test_measurement_not_captured_required_metric_blocks(self):
        m = manifest()
        t = telemetry()
        set_metric_state(t, "bytes_read", MetricState.MEASUREMENT_NOT_CAPTURED.value)
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_REQUIRED_METRIC_NOT_MEASURED"):
            validate_terminal_telemetry_completeness(
                telemetry=t, source="LITS_I", candidate="A",
                current_manifest=m, stage_receipts={},
                completed_qualifying_cell=True,
            )

    def test_legitimate_candidate_a_delete_rebuild_na_passes(self):
        result = validate_terminal_telemetry_completeness(
            telemetry=telemetry(), source="LITS_I", candidate="A",
            current_manifest=manifest(), stage_receipts={},
            completed_qualifying_cell=True,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["frozen_metric_obligations"]["delete_rebuild_wall_ns"],
            MetricState.NOT_APPLICABLE_BY_FROZEN_COURT.value,
        )

    def test_wrong_na_on_reachable_metric_blocks(self):
        m = manifest()
        t = telemetry()
        set_metric_state(t, "bytes_read", MetricState.NOT_APPLICABLE_BY_FROZEN_COURT.value)
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_REQUIRED_METRIC_NOT_MEASURED"):
            validate_terminal_telemetry_completeness(
                telemetry=t, source="LITS_I", candidate="A",
                current_manifest=m, stage_receipts={},
                completed_qualifying_cell=True,
            )

    def test_authorized_stop_allows_only_downstream_stop_state(self):
        m = manifest(candidate="B")
        stop = "S10_SOURCE_RELEASE_INVALIDATION"
        t = telemetry(candidate="B", stop_after=stop)
        stage_receipts = {stop: {"terminal_disposition": "CANDIDATE_LOCAL_FAILURE"}}
        result = validate_terminal_telemetry_completeness(
            telemetry=t, source="LITS_I", candidate="B",
            current_manifest=m, stage_receipts=stage_receipts,
            completed_qualifying_cell=False,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertIsNotNone(result["authorized_stop_stage_index"])

        forged = copy.deepcopy(t)
        set_metric_state(
            forged,
            "bytes_read",
            MetricState.NOT_REACHED_AUTHORIZED_STOP.value,
        )
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_REQUIRED_METRIC_NOT_MEASURED"):
            validate_terminal_telemetry_completeness(
                telemetry=forged, source="LITS_I", candidate="B",
                current_manifest=m, stage_receipts=stage_receipts,
                completed_qualifying_cell=False,
            )

    def test_wrong_metric_definition_hash_blocks(self):
        t = telemetry()
        t["metric_definition_hash"] = "0" * 64
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_METRIC_DEFINITION_HASH_DRIFT"):
            validate_terminal_telemetry_completeness(
                telemetry=t, source="LITS_I", candidate="A",
                current_manifest=manifest(), stage_receipts={},
                completed_qualifying_cell=True,
            )

    def test_missing_process_seal_blocks(self):
        t = telemetry()
        t["telemetry_summary"]["process_metrics_sealed"] = False
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_PROCESS_SEAL_INCOMPLETE"):
            validate_terminal_telemetry_completeness(
                telemetry=t, source="LITS_I", candidate="A",
                current_manifest=manifest(), stage_receipts={},
                completed_qualifying_cell=True,
            )

    def test_incomplete_io_seal_blocks(self):
        t = telemetry()
        t["telemetry_summary"]["io_event_stream_sealed"] = False
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_IO_SEAL_INCOMPLETE"):
            validate_terminal_telemetry_completeness(
                telemetry=t, source="LITS_I", candidate="A",
                current_manifest=manifest(), stage_receipts={},
                completed_qualifying_cell=True,
            )

    def test_incomplete_scratch_seal_blocks(self):
        t = telemetry()
        t["telemetry_summary"]["scratch_high_water_sealed"] = False
        with self.assertRaisesRegex(TerminalCompletenessError, "TC_SCRATCH_SEAL_INCOMPLETE"):
            validate_terminal_telemetry_completeness(
                telemetry=t, source="LITS_I", candidate="A",
                current_manifest=manifest(), stage_receipts={},
                completed_qualifying_cell=True,
            )

    def test_candidate_b_no_cache_skips_remain_lawful(self):
        m = manifest(candidate="B")
        for stage in ("S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"):
            m["cells"][0]["stages"][stage][0] = "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW"
            m["cells"][0]["stages"][stage][1] = "PURE_B_NO_CACHE"
        receipts = {
            stage: {
                "stop_law_ref": "PURE_B_NO_CACHE",
                "stop_law": m["stop_laws"]["PURE_B_NO_CACHE"],
            }
            for stage in ("S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE")
        }
        result = validate_terminal_telemetry_completeness(
            telemetry=telemetry(candidate="B", skipped=receipts),
            source="LITS_I", candidate="B", current_manifest=m,
            stage_receipts=receipts, completed_qualifying_cell=True,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertNotIn("S12_STALE_CACHE_OR_PERSISTENT_STATE", result["required_lifecycle_actions"])
        self.assertNotIn("S13_CORRUPT_CACHE_OR_PERSISTENT_STATE", result["required_lifecycle_actions"])

    def test_wvs_c_zero_accelerator_skip_creates_no_fake_cache_obligation(self):
        m = manifest(source="WVS7", candidate="C")
        for stage in ("S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"):
            m["cells"][0]["stages"][stage][0] = "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW"
            m["cells"][0]["stages"][stage][1] = "C_ZERO_ACCELERATOR_NO_CACHE"
        receipts = {
            stage: {
                "stop_law_ref": "C_ZERO_ACCELERATOR_NO_CACHE",
                "stop_law": m["stop_laws"]["C_ZERO_ACCELERATOR_NO_CACHE"],
            }
            for stage in ("S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE")
        }
        result = validate_terminal_telemetry_completeness(
            telemetry=telemetry(source="WVS7", candidate="C", skipped=receipts),
            source="WVS7", candidate="C", current_manifest=m,
            stage_receipts=receipts, completed_qualifying_cell=True,
        )
        self.assertEqual(result["status"], "PASS")

    def test_exact_preserved_no_numeric_disposition_allows_typed_missing(self):
        m = manifest(candidate="B")
        m["cells"][0]["stages"]["S01_CANDIDATE_PREPARATION_BUILD"][0] = "DONE__PRESERVE"
        t = telemetry(candidate="B", skipped={"S01_CANDIDATE_PREPARATION_BUILD"})
        set_metric_state(
            t,
            "build_or_open_wall_ns",
            MetricState.MEASUREMENT_NOT_CAPTURED.value,
        )
        receipts = {
            "S01_CANDIDATE_PREPARATION_BUILD": {
                "t4_preserved_work_adjudication": {
                    "disposition": "PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY",
                    "numeric_credit_allowed": False,
                    "missing_numeric_is_zero": False,
                }
            }
        }
        result = validate_terminal_telemetry_completeness(
            telemetry=t, source="LITS_I", candidate="B",
            current_manifest=m, stage_receipts=receipts,
            completed_qualifying_cell=True,
        )
        self.assertEqual(
            result["frozen_metric_obligations"]["build_or_open_wall_ns"],
            "PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY",
        )

    def test_completeness_receipt_cannot_rank_or_select(self):
        result = validate_terminal_telemetry_completeness(
            telemetry=telemetry(), source="LITS_I", candidate="A",
            current_manifest=manifest(), stage_receipts={},
            completed_qualifying_cell=True,
        )
        self.assertTrue(result["selection_neutral"])
        self.assertFalse(result["ranking_or_selection"])
        self.assertFalse(result["candidate_comparison_performed"])
        forbidden = {"winner", "selected_candidate", "rank", "score", "ranking"}
        self.assertTrue(forbidden.isdisjoint(result))


if __name__ == "__main__":
    unittest.main()
