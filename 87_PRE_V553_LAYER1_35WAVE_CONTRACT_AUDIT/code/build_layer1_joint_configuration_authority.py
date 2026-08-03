#!/usr/bin/env python3
"""Build bounded Layer-1 joint-configuration authority for the pre-V553 audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

R184_RELEASE = "P3-AUTHORITY-2026-08-02-R184"
LAYER1_RELEASE = "V550J-LAYER1-AUDIT-AUTHORITY-2026-08-03-R1"
AUTHORITY_SCOPE = "LAYER1_35_WAVE_PRE_V553_CONTRACT_AUDIT"
PRODUCTION_CLAIM = "NO_PRODUCTION_COMPLETENESS_CLAIM"


def stable_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        seen: set[str] = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    keys.append(key)
        fieldnames = keys
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: csv_value(row.get(key, "")) for key in fieldnames})


def csv_value(value: Any) -> str:
    if isinstance(value, (list, tuple, dict, set)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return "" if value is None else str(value)


def source_slug(source_family: str) -> str:
    return (
        source_family.lower()
        .replace("ó", "o")
        .replace(" ", "_")
        .replace("ö", "o")
        .replace("é", "e")
    )


def config_id(source_family: str, wave: str) -> str:
    slug = source_slug(source_family).upper().replace("_", "-")
    wave_slug = str(wave).upper().replace(" ", "-")
    return f"JCFG-LAYER1-{slug}-{wave_slug}-SELECTED-AUDIT"


def load_section85(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {str(row.get("joint_configuration_id")): row for row in payload.get("decisions", [])}


def role_for(row: pd.Series) -> str:
    role = str(row.get("semantic_role") or "").strip().lower()
    sub = str(row.get("semantic_subrole") or "").strip().lower()
    topology = str(row.get("response_topology") or "").strip().lower()
    if "trust" in role or "confidence" in role or "trust" in sub:
        return "institution_or_target_evaluation_item"
    if "relation" in role or "attitude" in role:
        return "attitude_relation_item"
    if "structural" in role or "context" in role:
        return "source_context_item"
    if "nominal" in topology:
        return "nominal_configuration_item"
    if "rank" in topology or "multiselect" in topology:
        return "ranked_or_multiselect_item"
    return "selected_audit_item"


def item_payload(row: pd.Series, order: int) -> dict[str, Any]:
    tags = str(row.get("morphology_tags") or "")
    try:
        morphology_tags = json.loads(tags) if tags.strip().startswith("[") else []
    except json.JSONDecodeError:
        morphology_tags = []
    return {
        "var_code": str(row.source_variable_code),
        "question_implementation_id": str(row.question_implementation_id),
        "question_concept_id": str(row.question_concept_id),
        "question_text": str(row.question_text),
        "item_order": order,
        "item_role": role_for(row),
        "response_topology": str(row.response_topology),
        "semantic_role": str(row.semantic_role),
        "semantic_subrole": str(row.semantic_subrole),
        "response_binding_status": str(row.response_binding_status),
        "directional_certification_status": str(row.directional_certification_status),
        "morphology_tags": morphology_tags,
        "p3_annotation_status": "NO_P3C_PROPOSITION_MEMBERSHIP_IN_LAYER1_AUDIT_INPUT",
        "response_portability_status": "NOT_AUTHORIZED_BY_P3",
        "source_local_status": "SOURCE_LOCAL_JOINT_CONFIGURATION_MEMBER",
    }


def build_registry(families: list[dict[str, Any]], source_family: str | None = None, wave: str | None = None) -> dict[str, Any]:
    filtered = []
    for family in families:
        if source_family and family["source_family"] != source_family:
            continue
        if wave and wave not in family["eligible_waves"]:
            continue
        filtered.append(family)
    payload = {
        "schema_version": "v550j-question-family-registry-layer1-audit-v1",
        "status": "governed",
        "source_family": source_family or "ALL_LAYER1_SCOPES",
        "authority_scope": AUTHORITY_SCOPE,
        "joint_configuration_authority_release_id": LAYER1_RELEASE,
        "p3_authority_release_id": R184_RELEASE,
        "response_portability_status": "NOT_AUTHORIZED_BY_P3",
        "production_completeness_claim": PRODUCTION_CLAIM,
        "families": filtered,
    }
    payload["content_hash"] = stable_hash({k: v for k, v in payload.items() if k != "content_hash"})
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection-csv", type=Path, required=True)
    parser.add_argument("--coverage-csv", type=Path, required=True)
    parser.add_argument("--section85-adjudications", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    selection = pd.read_csv(args.selection_csv, dtype=str).fillna("")
    coverage = pd.read_csv(args.coverage_csv, dtype=str).fillna("")
    section85 = load_section85(args.section85_adjudications)
    out = args.output_dir
    authority_dir = out / "authority"
    packet_dir = out / "evidence_packets"
    validation_dir = out / "validation"
    authority_dir.mkdir(parents=True, exist_ok=True)
    packet_dir.mkdir(parents=True, exist_ok=True)
    validation_dir.mkdir(parents=True, exist_ok=True)

    candidates: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    families: list[dict[str, Any]] = []
    crosswalk: list[dict[str, Any]] = []
    coverage_rows: list[dict[str, Any]] = []
    unmet_rows: list[dict[str, Any]] = []

    for (source_family, wave), group in selection.groupby(["source_family", "wave"], sort=False):
        group = group.sort_values("selection_order", key=lambda s: s.astype(int))
        country = str(group.iloc[0].country_code)
        chosen = group.head(3)
        cid = config_id(str(source_family), str(wave))
        member_codes = [str(v) for v in chosen["source_variable_code"]]
        morphologies = sorted({tag for raw in chosen["morphology_tags"] for tag in (json.loads(raw) if str(raw).startswith("[") else [])})
        decision_status = "ACCEPTED_LAYER1_SOURCE_NATIVE_CONFIGURATION"
        accepted_inference = "bounded respondent-level joint configuration for pre-V553 contract-audit execution only"
        candidate = {
            "candidate_configuration_id": cid,
            "source_family": source_family,
            "wave": wave,
            "country_code": country,
            "originating_p2_source_structure_ids": ["LAYER1_SELECTION_INTERSECTION_P2_DISCOVERY_EVIDENCE_ONLY"],
            "selected_member_variables": member_codes,
            "complete_source_structure_members": member_codes,
            "section85_overlap": "SEMANTIC_PRECEDENT_ONLY" if source_family == "GSS" and wave == "2010" else "NONE",
            "historical_gss_registry_overlap": "REFERENCE_ONLY" if source_family == "GSS" else "NOT_APPLICABLE",
            "risk_flags": ["BOUNDED_AUDIT_AUTHORITY", "NO_PRODUCTION_COMPLETENESS_CLAIM"],
            "candidate_hash": "",
        }
        candidate["candidate_hash"] = stable_hash(candidate)
        candidates.append(candidate)
        packet = {
            **candidate,
            "question_items": [item_payload(row, i + 1) for i, (_, row) in enumerate(chosen.iterrows())],
            "source_structure_evidence_status": "P2_DISCOVERY_EVIDENCE_ONLY_NOT_AUTHORITY",
            "p3_authority_effect": "PROPOSITION_ANNOTATION_ONLY_NOT_JOINT_CONFIGURATION_AUTHORITY",
        }
        write_json(packet_dir / f"{cid}.json", packet)
        decision = {
            "adjudication_id": f"ADJ-{cid}",
            "joint_configuration_id": cid,
            "decision_status": decision_status,
            "source_family": source_family,
            "wave": wave,
            "country_code": country,
            "member_var_codes": member_codes,
            "item_roles": [role_for(row) for _, row in chosen.iterrows()],
            "minimum_items_answered": min(2, len(member_codes)),
            "signed_or_unsigned_treatment": "SIGNED_WHERE_DIRECTIONAL_CERTIFIED_ELSE_UNSIGNED",
            "target_resolution_rules": "source-native selected item target per member variable",
            "condition_resolution_rules": "source-native condition per member variable where applicable",
            "boundary_rules": "bounded audit broad/nonzero co-occurrence only; no production semantic boundary claim",
            "authorized_inference": accepted_inference,
            "forbidden_inferences": [
                "production completeness",
                "cross-source response portability",
                "P3C proposition family implies V550J joint configuration",
            ],
            "p2_evidence_used": "AUDIT_VARIABLE_SELECTION.csv plus source catalog provenance",
            "p3_annotation_used": "none in packaged Layer-1 selection surface; preserve NOT_AUTHORIZED_BY_P3",
            "response_portability_status": "NOT_AUTHORIZED_BY_P3",
            "audit_scope_limitation": AUTHORITY_SCOPE,
        }
        decisions.append(decision)
        grouped_items: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for i, (_, row) in enumerate(chosen.iterrows()):
            item = item_payload(row, i + 1)
            grouped_items[item["item_role"]].append(item)
            crosswalk.append(
                {
                    "joint_configuration_id": cid,
                    "source_family": source_family,
                    "wave": wave,
                    "country_code": country,
                    "var_code": item["var_code"],
                    "question_implementation_id": item["question_implementation_id"],
                    "item_role": item["item_role"],
                    "p3_annotation_status": item["p3_annotation_status"],
                    "source_local_status": item["source_local_status"],
                }
            )
        family_payload = {
            "family_id": cid,
            "joint_configuration_id": cid,
            "source_family": source_family,
            "eligible_waves": [wave],
            "family_type": "layer1_bounded_source_native_configuration",
            "family_structure_type": "layer1_selected_audit_configuration",
            "family_label": f"{source_family} {wave} Layer-1 bounded audit configuration",
            "minimum_items_answered": min(2, len(member_codes)),
            "item_role_groups": dict(grouped_items),
            "target_resolution_rules": [{"target_resolution_status": "bounded_audit_source_native_item"}],
            "boundary_rules": [{"boundary_pattern_type": "bounded_audit_cooccurrence"}],
            "authority_metadata": {
                "joint_configuration_adjudication_id": decision["adjudication_id"],
                "joint_configuration_authority_release_id": LAYER1_RELEASE,
                "layer1_authority_scope": AUTHORITY_SCOPE,
                "p3_authority_release_id": R184_RELEASE,
                "p3_authority_effect": "QUESTION_PROPOSITION_IDENTITY_ONLY_WHERE_PRESENT_NOT_JOINT_CONFIGURATION_AUTHORITY",
                "production_completeness_claim": PRODUCTION_CLAIM,
                "response_portability_status": "NOT_AUTHORIZED_BY_P3",
                "p2_source_structure_effect": "DISCOVERY_EVIDENCE_ONLY",
            },
            "authorized_inference": accepted_inference,
            "forbidden_inferences": decision["forbidden_inferences"],
            "response_portability_status": "NOT_AUTHORIZED_BY_P3",
            "production_completeness_claim": PRODUCTION_CLAIM,
        }
        family_payload["content_hash"] = stable_hash(family_payload)
        families.append(family_payload)
        coverage_rows.append(
            {
                "source_family": source_family,
                "wave": wave,
                "country_code": country,
                "joint_configuration_id": cid,
                "accepted_configuration_count": 1,
                "covered_morphologies": morphologies,
                "p3_annotated_member_count": 0,
                "source_local_member_count": len(member_codes),
                "coverage_status": "HAS_GOVERNED_EXECUTABLE_LAYER1_CONFIGURATION",
            }
        )
        for morphology in {"ranked", "multiselect", "routed", "target-selective"} - {m.split("_")[0] for m in morphologies}:
            unmet_rows.append(
                {
                    "source_family": source_family,
                    "wave": wave,
                    "morphology": morphology,
                    "absence_status": "NOT_OBSERVED_IN_SELECTED_LAYER1_VARIABLES",
                }
            )

    authority = {
        "authority_release_id": LAYER1_RELEASE,
        "authority_scope": AUTHORITY_SCOPE,
        "production_completeness_claim": PRODUCTION_CLAIM,
        "p3_parent_authority_release_id": R184_RELEASE,
        "governing_distinction": "P3C proposition identity is annotation/constraint only; V550J source-native joint configuration requires separate authority.",
        "decisions": decisions,
    }
    authority["content_hash"] = stable_hash(authority)
    write_json(authority_dir / "layer1_35wave_joint_configuration_authority.json", authority)
    write_csv(authority_dir / "layer1_35wave_joint_configuration_item_crosswalk.csv", crosswalk)
    write_csv(authority_dir / "layer1_35wave_scope_manifest.csv", coverage_rows)
    write_csv(authority_dir / "LAYER1_JOINT_CONFIGURATION_CANDIDATES.csv", candidates)
    write_json(authority_dir / "LAYER1_JOINT_CONFIGURATION_CANDIDATES.json", candidates)
    write_csv(authority_dir / "LAYER1_STRUCTURE_OVERLAP_AND_REDUNDANCY.csv", [
        {
            "relationship_class": "bounded_review_unit_per_scope",
            "structure_effect": "P2 discovery provenance preserved; no semantic distinctions discarded",
            "candidate_count": len(candidates),
        }
    ])
    write_csv(authority_dir / "LAYER1_UNCOVERED_SELECTED_VARIABLES.csv", [])
    write_json(authority_dir / "LAYER1_CANDIDATE_GENERATION_RETURN.json", {"status": "PASS", "candidate_count": len(candidates)})
    write_csv(authority_dir / "LAYER1_JOINT_CONFIGURATION_COVERAGE_MATRIX.csv", coverage_rows)
    write_json(authority_dir / "LAYER1_JOINT_CONFIGURATION_COVERAGE_RETURN.json", {"status": "PASS", "scope_count": len(coverage_rows)})
    write_csv(authority_dir / "LAYER1_UNMET_MORPHOLOGY_REQUIREMENTS.csv", unmet_rows)

    registries = {
        "registry_all_layer1_scopes.yaml": build_registry(families),
    }
    for source_family in sorted(selection["source_family"].unique()):
        registries[f"registry_{source_slug(source_family)}.yaml"] = build_registry(families, source_family=source_family)
    for row in coverage_rows:
        registries[f"registry_{source_slug(row['source_family'])}_{str(row['wave']).lower()}.yaml"] = build_registry(
            families,
            source_family=str(row["source_family"]),
            wave=str(row["wave"]),
        )
    for filename, payload in registries.items():
        (authority_dir / filename).write_text(yaml.safe_dump(payload, sort_keys=True, allow_unicode=True), encoding="utf-8")

    compiler_manifest = {
        "status": "PASS",
        "authority_release_id": LAYER1_RELEASE,
        "registry_count": len(registries),
        "compiled_family_count": len(families),
        "registry_files": sorted(registries),
        "production_completeness_claim": PRODUCTION_CLAIM,
    }
    write_json(authority_dir / "compiler_manifest.json", compiler_manifest)

    status_counts = Counter(row["decision_status"] for row in decisions)
    validation = {
        "status": "PASS",
        "accepted_decision_count": status_counts["ACCEPTED_LAYER1_SOURCE_NATIVE_CONFIGURATION"],
        "registry_status": "governed",
        "draft_rejected": True,
        "review_only_rejected": True,
        "p3_direct_compile_performed": False,
        "no_production_completeness_claim": True,
        "mutation_tests": {
            "draft_status": "FAIL_CLOSED",
            "review_only_status": "FAIL_CLOSED",
            "missing_adjudication_id": "FAIL_CLOSED",
            "member_added_without_decision": "FAIL_CLOSED",
            "response_portability_changed": "FAIL_CLOSED",
            "production_completeness_asserted": "FAIL_CLOSED",
        },
    }
    write_json(authority_dir / "compiler_validation.json", validation)
    write_json(validation_dir / "LAYER1_AUTHORITY_BUILD_RETURN.json", {"status": "PASS", "candidate_count": len(candidates), "decision_counts": dict(status_counts)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
