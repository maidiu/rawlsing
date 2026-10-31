#!/usr/bin/env python3
"""Generate the historical-function-to-current-consumer contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

CANDIDATE = Path(__file__).resolve().parent.parent
RETURN = CANDIDATE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    inventory = json.loads((RETURN / "04_ROLLBACK_SOURCE_HASHES_AND_PROVENANCE.json").read_text())
    historical = inventory["historical_source_files"]
    adapters = inventory["adapter_source_files"]
    probe = json.loads((CANDIDATE / "evidence" / "first_consumer_probe.json").read_text())
    court = json.loads((CANDIDATE / "evidence" / "court_results.json").read_text())

    def hsource(path: str) -> str:
        return historical.get(path, {}).get("sha256", "")

    def hadapter(path: str) -> str:
        return adapters.get(path, "")

    payload = {
        "schema": "SOROK_V3CORE_R1_HISTORICAL_FUNCTION_TO_CURRENT_CONSUMER_CONTRACT@1",
        "contract_version": "1",
        "repository": inventory["repository"],
        "base_commit": inventory["base_commit"],
        "branch": inventory["branch"],
        "inputs": inventory["inputs"],
        "clock_domains": {
            "CURRENT_C12_ACTOR_WORLD": "Actual I1/BP4 C12 world clock. Accepted only through an explicit M25 annual binding.",
            "SOROK_NEO_N11_EVENT_RECURSION": "Neo N11 event recursion. Refused as an M25 year event.",
            "PYAT_N11_OBJECTIVE_WORLD_ACCEPTANCE": "Pyat objective-world N11 acceptance. Refused as an M25 year event.",
            "V3_M25_ANNUAL_SCHEDULE": "Historical 19-step annual scheduler. Never treated as an event multiplier.",
        },
        "source_record_contract": {
            "event": "ActorWorldEvent(event_id, actor_id, world_id, kind, location, source_clock_domain, source_clock, body, provenance, owner_receipt_hash, source_owned)",
            "access": "ActorAccess(event_id, actor_id, channel, perceived, source_clock_domain, source_clock, provenance)",
            "response": "ActorResponse(event_id, actor_id, kind, performed, body, source_clock_domain, source_clock, provenance)",
            "annual_binding": "AnnualBinding(event_id, schedule_clock_domain=V3_M25_ANNUAL, annual_year, bound_by, provenance)",
            "separation": [
                "source facts: ledger.source_events/accesses/responses and BackboneState.events_this_year",
                "durable actor state: BackboneState material fields only",
                "derived computation: PublishedDerived plus a diagnostic-only compute_all_derived result",
                "readable expression: BackboneState.rendered_output only",
            ],
        },
        "reference_sources_outside_candidate": inventory.get("reference_sources_outside_candidate", {}),
        "historical_function_map": [
            {
                "id": "M01/M26",
                "historical_function": "BackboneState stored state and clamp",
                "source_path": "vendor/v3/core/state.py",
                "source_sha256": hsource("vendor/v3/core/state.py"),
                "adapter_unit": "quarantine.build_projection_state / ledger.HistoricalProjection",
                "adapter_path": "v3core_adapter/quarantine.py",
                "adapter_sha256": hadapter("v3core_adapter/quarantine.py"),
                "fit": "REUSED_EXACT_DATACLASS_WITH_EXPLICIT_UNSET_ZEROING",
                "notes": "All defaulted psychological fields are emptied; only source-grounded material capacity is populated.",
            },
            {
                "id": "M01/M26",
                "historical_function": "compute_all_derived",
                "source_path": "vendor/v3/core/derived.py",
                "source_sha256": hsource("vendor/v3/core/derived.py"),
                "adapter_unit": "derived_scope.derive_scoped",
                "adapter_path": "v3core_adapter/derived_scope.py",
                "adapter_sha256": hadapter("v3core_adapter/derived_scope.py"),
                "fit": "REUSED_EXACT_ON_COPY_ONLY",
                "notes": "Executed on a deep copy for diagnostics and scoped publication; live state is never given metabolic_style/registers.",
            },
            {
                "id": "M25",
                "historical_function": "immutable 19-step yearly step order",
                "source_path": "vendor/v3/v3_yearly_step_order.yaml",
                "source_sha256": hsource("vendor/v3/v3_yearly_step_order.yaml"),
                "adapter_unit": "scheduler.validate_step_order / scheduler.load_plan",
                "adapter_path": "v3core_adapter/scheduler.py",
                "adapter_sha256": hadapter("v3core_adapter/scheduler.py"),
                "fit": "REUSED_EXACT_CONFIG_WITH_STRICT_SUBSEQUENCE_CHECK",
                "notes": "Core 19 ids, append-only extensions, and derived schedule equality are enforced; mutation court fails.",
            },
            {
                "id": "M25",
                "historical_function": "run_one_year",
                "source_path": "vendor/v3/engine/yearly_step.py",
                "source_sha256": hsource("vendor/v3/engine/yearly_step.py"),
                "adapter_unit": "scheduler.run_year",
                "adapter_path": "v3core_adapter/scheduler.py",
                "adapter_sha256": hadapter("v3core_adapter/scheduler.py"),
                "fit": "ADAPTED_RESTRICTED_REGISTRY",
                "notes": "Only event_sampling (actual ingress), capacity_update (material accounting) and render_layer are admitted. The other 16 steps are typed HELD with no mutation.",
            },
            {
                "id": "M38",
                "historical_function": "derived schedule fail-fast",
                "source_path": "vendor/v3/engine/yearly_step.py",
                "source_sha256": hsource("vendor/v3/engine/yearly_step.py"),
                "adapter_unit": "scheduler.validate_step_order / run_year derived schedule check",
                "adapter_path": "v3core_adapter/scheduler.py",
                "adapter_sha256": hadapter("v3core_adapter/scheduler.py"),
                "fit": "REUSED_EXACT_INVARIANT",
                "notes": "Declared derived_compute and schedule compute_after_step must match exactly or SchedulerRefusal is raised.",
            },
            {
                "id": "M21",
                "historical_function": "run_pressure_flow_cycle",
                "source_path": "vendor/v3/psyche/flow.py",
                "source_sha256": hsource("vendor/v3/psyche/flow.py"),
                "adapter_unit": "flow_quarantine.run_conserved_charge_flow_probe / memory.update_material_memory",
                "adapter_path": "v3core_adapter/flow_quarantine.py",
                "adapter_sha256": hadapter("v3core_adapter/flow_quarantine.py"),
                "fit": "QUARANTINED_TEST_ONLY_ON_COPY",
                "notes": "Conserved-charge routing is not assumed. The probe is opt-in, runs on a copy and never mutates live state. Material memory tracks recorded deltas, not charge.",
            },
            {
                "id": "M29/M30",
                "historical_function": "render_year",
                "source_path": "vendor/v3/render/phenomenology.py",
                "source_sha256": hsource("vendor/v3/render/phenomenology.py"),
                "adapter_unit": "render.render_readonly",
                "adapter_path": "v3core_adapter/render.py",
                "adapter_sha256": hadapter("v3core_adapter/render.py"),
                "fit": "REUSED_EXACT_WITH_NONMUTATION_COURT",
                "notes": "The exact renderer is used without an LLM callback; any backbone mutation is rolled back as HELD_RENDERER_MUTATION.",
            },
            {
                "id": "M40",
                "historical_function": "GenerationIntegrityAccumulator and readiness",
                "source_path": "vendor/v3/core/generation_integrity.py",
                "source_sha256": hsource("vendor/v3/core/generation_integrity.py"),
                "adapter_unit": "readiness.HistoricalReadiness",
                "adapter_path": "v3core_adapter/readiness.py",
                "adapter_sha256": hadapter("v3core_adapter/readiness.py"),
                "fit": "REUSED_EXACT_ACCUMULATOR",
                "notes": "clean/degraded/blocked semantics are preserved; readiness is labeled TEST_ONLY and is not native or science authority.",
            },
            {
                "id": "M02",
                "historical_function": "YearRecord snapshot persistence",
                "source_path": "vendor/v3/core/year_record.py",
                "source_sha256": hsource("vendor/v3/core/year_record.py"),
                "adapter_unit": "contracts.YearRecord / ledger.HistoricalProjection",
                "adapter_path": "v3core_adapter/contracts.py",
                "adapter_sha256": hadapter("v3core_adapter/contracts.py"),
                "fit": "ADAPTED_TYPED_RECORD",
                "notes": "The archive helper normalizes YearRecord dicts; the runtime year dict is produced by server/generation/simulation.py. The typed record mirrors state/derived hashes, event ledger, micro-trace, integrity and readiness.",
            },
            {
                "id": "M37/M38",
                "historical_function": "stored/derived separation and derived field prohibition",
                "source_path": "vendor/v3/core/invariants.py",
                "source_sha256": hsource("vendor/v3/core/invariants.py"),
                "adapter_unit": "tests/test_render_and_derived.py / derived_scope",
                "adapter_path": "v3core_adapter/derived_scope.py",
                "adapter_sha256": hadapter("v3core_adapter/derived_scope.py"),
                "fit": "REUSED_EXACT_ASSERTION",
                "notes": "assert_no_derived_fields_in_backbone passes; PublishedDerived is frozen and diagnostic output is not stored in BackboneState.",
            },
        ],
        "quarantine": {
            "manifest_path": "v3core_adapter/quarantine.py",
            "manifest_sha256": hadapter("v3core_adapter/quarantine.py"),
            "mechanisms": [
                "M08 identity-seeded wound",
                "M15/M36 missing-parent 50/50/50 and hopeful defaults",
                "M31 Enneagram/type determinism",
                "M34 synthetic fallback practice / first-candidate fallback",
                "M35 placeholder cracks/frameworks",
                "M39 random age-band rupture",
            ],
            "enforcement": [
                "fresh projection state zeroes every ungrounded field and records QUARANTINED_UNSET",
                "forbidden_default_reasons blocks the year before commit",
                "module-level import scan forbids active adapter imports of the quarantined mechanisms",
            ],
        },
        "current_consumer": {
            "consumer": "I1 GuardedJoinedProduct -> v3core_adapter.i1_consumer.project_actual_market_event",
            "i1_commit": inventory["inputs"]["I1"]["commit"],
            "actual_event_id": probe["event_id"],
            "observed_world_hash": probe.get("observed_world_hash", ""),
            "source_clock": probe["source_clock"],
            "source_clock_domain": probe["source_clock_domain"],
            "cash_before": probe["cash_before"],
            "cash_after": probe["cash_after"],
            "completed_units_before": probe["completed_units_before"],
            "completed_units_after": probe["completed_units_after"],
            "position_before": probe["position_before"],
            "position_after": probe["position_after"],
            "material_index_before": probe["material_index_before"],
            "material_index_after": probe["material_index_after"],
            "material_index_delta": probe["material_index_delta"],
            "state_hash_before": probe["state_hash_before"],
            "state_hash_after": probe["state_hash_after"],
            "projection_ledger_sha256": probe["projection_ledger_sha256"],
            "projection_cold_equal": probe["projection_cold_equal"],
            "c12_counts_before": probe["c12_counts_before"],
            "c12_counts_after": probe["c12_counts_after"],
            "c12_authenticity": probe["c12_authenticity"],
            "canonical_c9_claimed": probe["canonical_c9_claimed"],
            "rival_store_created": probe["rival_store_created"],
            "real_difference": "material_capacity_index 11.3 -> 11.6 (+0.3) and durable cash 54 -> 56 from the actual I1 OFFSCREEN_REPAIR event",
            "not_a_trait": "no class, identity, ethnicity, religion, Enneagram or typographic value is read or written",
        },
        "courts": {
            "unchanged_v3_source_tests": court["courts"][0]["summary"],
            "adapter_tests": court["courts"][1]["summary"],
            "i1_unchanged_tests": court["courts"][2]["summary"],
            "mutated_19_step_order": court["courts"][3]["summary"],
        },
        "authority": {
            "science_issued": False,
            "native_person_claimed": False,
            "original_author_claimed": False,
            "canonical_c9_claimed": False,
            "rival_store_created": False,
            "self_reviewed": False,
            "merge_or_premain_mutated": False,
        },
        "not_run": [
            "full historical V3/V2 suite (TD-R05 80-test aggregate)",
            "native source/respondent data and any CAN/ADP/SCI05 issuance",
            "I1 durable C9 handoff, external C12 anchor and native A5 person",
            "Pyat N11/N12 native world acceptance",
            "production or PRE-MAIN integration",
        ],
    }
    output = RETURN / "01_HISTORICAL_FUNCTION_TO_CURRENT_CONSUMER_CONTRACT.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
