#!/usr/bin/env python3
"""Check structural completeness of a proposed Pyat HQ accession dossier.

NOT a scientific, source-use, persona-quality, or independent-review verifier.
By default the template FAILS. This script never grants HQ legitimacy.
Usage: python PYAT_CONTROL_ROOM/verify_incoming_hq_grok_r1.py path/to/accession.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_FUNCTIONS = {
    "crosswave_atlas_semantic_mapping",
    "driver_facet_scale_semantic_authority",
    "source_population_conditioning_weights",
    "cross_source_statistical_synthesis_proxies",
    "recursive_empirical_discovery_higher_order",
    "temporal_wave_harmonization",
    "temporal_structural_pressure_and_age_cohort",
    "selected_world_to_v3_development_to_v2",
}
REQUIRED_PROOFS = {
    "live_control_and_handoff",
    "original_persona_and_terminal_demand",
    "pre_main_pyat_full_machine",
    "dva_trii_chetiri",
    "long_memory_current_succession",
    "crosswave_semantic_driver_facet",
    "empirical_inference_and_synthesis",
    "historical_temporal_and_current_successor",
    "objective_selected_world_and_v3_v2",
    "fresh_methods_comparison_and_improvement",
    "end_product_test_and_sensitivity",
    "scientific_scope_35wave_and_authority",
    "resource_privacy_and_worktree",
}
VALID_DECISIONS = {
    "REUSE_AS_IS",
    "INTEGRATE_OR_ADAPT",
    "IMPROVE_OR_COMPLETE",
    "REPLACE_AFTER_COMPARATIVE_PROOF",
    "NO_DECISION__NEEDS_EVIDENCE",
}
VALID_FUNCTIONAL_STATES = {
    "CURRENT_ADOPTED",
    "IMPLEMENTED_UNADOPTED",
    "HISTORICAL_FUNCTIONAL_CANDIDATE",
    "STRANDED",
    "SUPERSEDED_PROVED",
    "UNKNOWN_NEEDS_CHECK",
    "REAL_FUNCTIONAL_GAP",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")

def meaningful(x):
    return isinstance(x, str) and bool(x.strip()) and x.strip() not in {
        "UNKNOWN", "NONE", "TBD", "NOT_PROVED", "NOT_YET_VERIFIED", "UNVERIFIED",
    }

def check(record):
    errors = []
    if record.get("schema") != "PYAT_INCOMING_HQ_GROK_ATTESTATION_R1":
        errors.append("wrong schema")
    if record.get("template") is not False:
        errors.append("template is not an accession: set template=false in a distinct new dossier")
    identity = record.get("candidate") or {}
    for key in ("session_or_accession_id", "branch", "proposed_hq_label",
                "prior_sealed_handoff_sha", "current_remote_control_sha"):
        val = identity.get(key)
        if not meaningful(val):
            errors.append(f"candidate.{key}: missing")
    for k in ("prior_sealed_handoff_sha", "current_remote_control_sha"):
        if meaningful(identity.get(k)) and not HEX40.fullmatch(identity[k]):
            errors.append(f"candidate.{k}: not a full 40-character SHA")

    proofs = record.get("proof_sections") or {}
    for cat in sorted(REQUIRED_PROOFS):
        p = proofs.get(cat) or {}
        if p.get("status") != "PASS":
            errors.append(f"proof {cat}: not PASS")
        if not meaningful(p.get("substantive_conclusion")):
            errors.append(f"proof {cat}: no substantive conclusion")
        e = p.get("evidence")
        if not isinstance(e, list) or not e:
            errors.append(f"proof {cat}: no cited evidence")
        else:
            for i, row in enumerate(e):
                if not isinstance(row, dict) or any(not meaningful(row.get(k)) for k in
                                                    ("repository_path_or_source", "source_commit_or_sha",
                                                     "verified_fact", "currentness")):
                    errors.append(f"proof {cat}[{i}]: lacks exact source/evidence/currentness")

    got = set()
    for row in record.get("function_adjudications") or []:
        if not isinstance(row, dict):
            errors.append("function_adjudication: non-object row")
            continue
        name = row.get("function")
        if name in got:
            errors.append(f"duplicate function: {name}")
        got.add(name)
        if name not in REQUIRED_FUNCTIONS:
            continue
        for key in ("historical_ref", "current_owner_ref", "current_proof",
                    "alternatives_comparison", "persona_consumer",
                    "first_missing_edge", "positive_test"):
            if not meaningful(row.get(key)):
                errors.append(f"function {name}: missing {key} (use precise negative evidence if genuinely absent)")
        if row.get("functional_status") not in VALID_FUNCTIONAL_STATES:
            errors.append(f"function {name}: invalid functional state")
        if row.get("decision") not in VALID_DECISIONS or row.get("decision") == "NO_DECISION__NEEDS_EVIDENCE":
            errors.append(f"function {name}: no supported improvement/reuse adjudication")
    for absent in sorted(REQUIRED_FUNCTIONS - got):
        errors.append(f"missing required function: {absent}")

    e = record.get("end_product_evaluation") or {}
    for key in ("target_persona_scenario", "actual_source_inputs_and_claim_grades",
                "actual_accepted_or_pending_production_route", "actual_v3_v2_consumer",
                "observable_output_or_scoped_interface_test", "normal_control",
                "historical_or_material_counterfactual",
                "uncertainty_and_approximation_analysis",
                "required_approvals_and_missing_edges"):
        if not meaningful(e.get(key)):
            errors.append(f"end_product_evaluation.{key}: missing")

    review = record.get("independent_acceptance") or {}
    if review.get("status") != "ACCEPTED":
        errors.append("independent acceptance not recorded")
    if review.get("reviewer_type") not in {"USER", "AUTHORIZED_INDEPENDENT_REVIEWER"}:
        errors.append("independent acceptance: reviewer type invalid")
    for key in ("reviewer_identity_or_user_ack", "review_artifact_ref",
                "review_sha", "reviewed_candidate_sha"):
        if not meaningful(review.get(key)):
            errors.append(f"independent acceptance: missing {key}")
    if record.get("final_readiness") != "ACCESSION_REVIEW_ACCEPTED__OPERATIVE_CONTROL_STILL_SUBJECT_TO_EXISTING_HQD":
        errors.append("final readiness did not preserve original authority hierarchy")
    return errors

def main(argv):
    if len(argv) != 2:
        print("usage: verify_incoming_hq_grok_r1.py accession.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        errors = check(data)
    except (OSError, ValueError, TypeError) as exc:
        print(f"HQ_GROK_STRUCTURAL_CHECK_FAIL: {exc}", file=sys.stderr)
        return 2
    if errors:
        print(f"HQ_GROK_STRUCTURAL_CHECK_FAIL ({len(errors)} findings)")
        for e in errors[:150]:
            print(f"- {e}")
        return 1
    print("HQ_GROK_DOSSIER_STRUCTURALLY_COMPLETE")
    print("NOT AN HQ AUTHORIZATION. Verify source truth, reviewer consent, and governing HQD independently.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
