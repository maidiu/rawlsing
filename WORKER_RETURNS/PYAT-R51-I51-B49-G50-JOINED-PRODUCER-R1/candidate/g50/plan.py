"""NativeConstructionPlan@candidate1: refs into the existing native owners only."""
from __future__ import annotations

from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import semantic_hash

from .types import PLAN_SCHEMA, ScientificFrontier


def native_construction_plan(frontier: ScientificFrontier, native_run) -> dict[str, Any]:
    """Describe the exact existing-owner refs; no new Batch/U43/C11 writer."""

    unsupported = sorted({
        op.claim_class for op in frontier.eligible()
        if op.native_support == "POLICY_ONLY"
    })
    plan = {
        "schema": PLAN_SCHEMA,
        "frontier_hash": frontier.content_hash,
        "bundle_id": frontier.bundle_id,
        "policy_id": frontier.policy_id,
        "owners": {
            "grammar": "rawlsing_next.pre553_discovery_exact._compile_frontier (existing)",
            "executor": "rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery",
            "query": "rawlsing_next.pre553_empirical_query.execute_empirical_query",
            "c11": "existing C11 repository (not rebuilt by G50)",
            "batch": "existing U43/Batch boundary (not rebuilt by G50)",
        },
        "grammar_hash": native_run.grammar_hash,
        "coverage": "EXACT_DECLARED_FRONTIER",
        "native_rule_counts": dict(native_run.candidate_rule_counts),
        "candidate_count": native_run.candidate_count,
        "frontier_ref_hash": native_run.frontier_ref_hash,
        "replay_ref_hash": native_run.replay_ref_hash,
        "unsupported_classes": unsupported,
        "unsupported_disposition": "SPEC_ONLY_NATIVE_UNSUPPORTED_OR_POLICY_ONLY",
        "no_new_batch_writer": True,
        "no_new_c11_engine": True,
        "no_original_source_grant": True,
    }
    plan["plan_hash"] = semantic_hash(plan)
    return plan


__all__ = ["native_construction_plan"]
