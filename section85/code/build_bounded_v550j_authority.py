#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

R184_RELEASE = "P3-AUTHORITY-2026-08-02-R184"
SCOPE_ID = "BOUNDED_9_SOURCE_FAMILY_20_VARIABLE_CANARY"
PRODUCTION_CLAIM = "NO_PRODUCTION_COMPLETENESS_CLAIM"


@dataclass(frozen=True)
class ConfigurationSpec:
    source_family: str
    wave: str
    country_code: str
    scope_dir: str
    filter_file: str
    joint_configuration_id: str
    family_type: str
    family_label: str
    source_structure_id: str
    item_role: str
    var_codes: tuple[str, ...]
    minimum_items_answered: int
    signed_boundary_authority: bool = False
    existing_gss_family_id: str = ""


CONFIGURATIONS: tuple[ConfigurationSpec, ...] = (
    ConfigurationSpec("Afrobarometer", "R1", "LS", "Afrobarometer_R1_LS", "afrobarometer_r1.json", "JCFG-AFRO-R1-MIP-RANKED", "ranked_priority_configuration", "Afrobarometer ranked national-problem priorities", "afro_struct_338388735c9d7618", "ranked_priority_item", ("mip1", "mip2"), 2),
    ConfigurationSpec("Arab Barometer", "I", "YE", "Arab Barometer_I_YE", "arabbarometer_i.json", "JCFG-ARAB-I-POLITICAL-KNOWLEDGE", "parallel_knowledge_item_configuration", "Arab Barometer political-knowledge pair", "arab_structure_273db16a2c1ee16c2748", "knowledge_item", ("q2571", "q2572"), 2),
    ConfigurationSpec("Asian Barometer", "W1", "PH", "Asian Barometer_W1_PH", "asianbarometer_w1.json", "JCFG-ASIAN-W1-CHANGE-EVALUATION", "parallel_change_evaluation_configuration", "Asian Barometer change-evaluation pair", "asian_barometer_struct_run_634ba9e4e52393e941", "change_evaluation_item", ("q109", "q111"), 2),
    ConfigurationSpec("EVS", "1981", "BE", "EVS_1981_BE", "evs_1981.json", "JCFG-EVS-1981-MORAL-JUSTIFIABILITY", "moral_justifiability_battery", "EVS moral-justifiability canary battery", "evs_structure_ef2f7c70914e905b8adf", "justifiability_item", ("v471", "v472", "v514", "v517"), 3, True),
    ConfigurationSpec("GSS", "2010", "US", "GSS_2010_US", "gss_2010.json", "JCFG-GSS-ABORTION-CONDITIONS", "conditional_attitude_battery", "GSS abortion-condition control", "existing_registry_structure::gss_abortion_condition_family::2010", "condition_item", ("abdefect", "abhlth", "abrape", "abany", "absingle", "abnomore"), 3, True, "gss_abortion_condition_family"),
    ConfigurationSpec("Latinobarómetro", "1995", "BR", "Latinobarómetro_1995_BR", "latinobarometro_1995.json", "JCFG-LATINOBAROMETRO-1995-INSTITUTION-CONFIDENCE", "institution_confidence_battery", "Latinobarómetro institution-confidence canary battery", "latinobarometro_struct_a75ba74fad9b602c3d", "institution_target", ("p27e", "p27g", "p27m"), 2, True),
    ConfigurationSpec("LiTS", "2006", "BY", "LiTS_2006_BY", "lits_2006.json", "JCFG-LITS-2006-TRANSITION-EVALUATION", "transition_evaluation_battery", "LiTS transition-evaluation canary battery", "lits_struct_24bdd9b458c7689bbb", "evaluation_target", ("q301_1", "q301_8", "q301_11"), 2, True),
    ConfigurationSpec("South Asia", "W1", "IN", "South Asia_W1_IN", "southasia_w1.json", "JCFG-SOUTH-ASIA-W1-INSTITUTION-TRUST", "institution_trust_battery", "South Asia institution-trust canary battery", "south_asia_struct_ee2ce47eea6de1d296", "institution_target", ("c13f", "c13h"), 2, True),
    ConfigurationSpec("WVS", "W1", "SE", "WVS_W1_SE", "wvs_w1.json", "JCFG-WVS-W1-CHILD-QUALITIES", "multiselect_child_quality_configuration", "WVS important-child-qualities canary pair", "wvs_structure_c4f94fa98e17c785b1c4", "child_quality_item", ("V22", "V24"), 2),
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def stable_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str).fillna("")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def locate_response_audit(canary_root: Path, scope_dir: str) -> Path:
    matches = list(canary_root.glob(f"v550/shard_runs/*/{scope_dir}/bridge/response_semantics_audit.csv"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one response audit for {scope_dir}, found {len(matches)}")
    return matches[0]


def audit_summary(audit: pd.DataFrame, var_code: str) -> dict[str, Any]:
    rows = audit[audit["var_code"].str.lower() == var_code.lower()].copy()
    if rows.empty:
        raise RuntimeError(f"No response-semantics rows for {var_code}")
    def vals(column: str) -> list[str]:
        if column not in rows.columns:
            return []
        return sorted({v for v in rows[column].astype(str).str.strip() if v})
    option_pairs = sorted({(str(r.response_value_normalized), str(r.response_label)) for r in rows.itertuples()})
    return {
        "response_option_row_count": int(len(rows)),
        "response_topologies": vals("response_topology"),
        "response_families": vals("response_family"),
        "directionality_statuses": vals("directionality_status"),
        "directional_certification_statuses": vals("directional_certification_status"),
        "response_semantics_statuses": vals("response_semantics_status"),
        "response_semantics_contract_hashes": vals("response_semantics_contract_hash"),
        "response_values": sorted({x for x, _ in option_pairs}),
        "labeled_response_options": [{"value": x, "label": y} for x, y in option_pairs if y and y != x],
    }


def canonical_item_map(membership: pd.DataFrame, authority: pd.DataFrame) -> dict[str, dict[str, str]]:
    auth = authority.set_index("canonical_family_id")
    out: dict[str, dict[str, str]] = {}
    for row in membership.itertuples(index=False):
        fam = str(row.canonical_family_id)
        a = auth.loc[fam]
        out[str(row.member_object_id)] = {
            "p3_canonical_family_id": fam,
            "p3_current_family_revision_id": str(a.latest_family_revision_id),
            "p3_variant_revision_id": str(row.variant_revision_id),
            "p3_authority_release_id": R184_RELEASE,
            "p3_membership_status": "BOUND_TO_CURRENT_CANONICAL_FAMILY",
        }
    return out


def generic_family(spec: ConfigurationSpec, items: list[dict[str, Any]], decision: dict[str, Any]) -> dict[str, Any]:
    role_groups: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        role_groups.setdefault(str(item["item_role"]), []).append({k: v for k, v in item.items() if k != "item_role"})
    active_roles = list(role_groups)
    family: dict[str, Any] = {
        "family_id": spec.joint_configuration_id,
        "joint_configuration_id": spec.joint_configuration_id,
        "source_family": spec.source_family,
        "family_type": spec.family_type,
        "family_structure_type": spec.family_type,
        "expected_multi_target": True,
        "family_label": spec.family_label,
        "eligible_waves": [spec.wave],
        "minimum_items_answered": spec.minimum_items_answered,
        "authority_metadata": {
            "scope_id": SCOPE_ID,
            "production_completeness_claim": PRODUCTION_CLAIM,
            "p2_source_structure_id": spec.source_structure_id,
            "p2_authority_effect": "P2_DISCOVERY_EVIDENCE_ONLY_NOT_J_FAMILY_AUTHORITY",
            "joint_configuration_adjudication_id": decision["adjudication_id"],
            "joint_configuration_decision_status": decision["decision_status"],
            "joint_configuration_authority_release_id": decision["authority_release_id"],
            "authority_basis_status": "HUMAN_ADJUDICATED_FROM_EXACT_SOURCE_EVIDENCE",
            "p3_authority_release_id": R184_RELEASE,
            "p3_authority_effect": "QUESTION_PROPOSITION_IDENTITY_ONLY_WHERE_MEMBERSHIP_EXISTS",
            "response_portability_status": "NOT_AUTHORIZED_BY_P3",
            "configuration_authority_status": "GOVERNED_BOUNDED_CANARY_ONLY",
        },
        "item_role_groups": role_groups,
        "target_resolution_rules": [
            {
                "applies_to_roles": active_roles,
                "target_entity_template": f"{spec.joint_configuration_id.lower()}_{{condition_label}}",
                "target_domain": spec.family_type,
                "target_group_label_from": "condition_label",
                "target_resolution_grain": "condition_label",
                "target_resolution_status": "bounded_registry_resolved_item",
                "target_resolution_authority_source": "bounded_v550j_registry.item_role_groups",
                "target_resolution_basis_source": "P2 source structure plus exact source-wave variable binding",
            }
        ],
    }
    if bool(decision["signed_boundary_authority"]):
        family["boundary_rules"] = [
            {"boundary_pattern_type": "broad_support", "support_share_min": 0.75, "oppose_share_max": 0.25},
            {"boundary_pattern_type": "broad_opposition", "oppose_share_min": 0.75, "support_share_max": 0.25},
            {"boundary_pattern_type": "mixed_signed_configuration", "require_any": [
                *[{"role": role, "semantic_response_role": "support"} for role in active_roles],
                *[{"role": role, "semantic_response_role": "oppose"} for role in active_roles],
            ]},
        ]
    else:
        family["boundary_rules"] = []
    return family


def load_gss_control(template_path: Path, spec: ConfigurationSpec, item_metadata: dict[str, dict[str, Any]]) -> dict[str, Any]:
    payload = yaml.safe_load(template_path.read_text(encoding="utf-8"))
    family = next(x for x in payload["families"] if x["family_id"] == spec.existing_gss_family_id)
    allowed = {x.lower() for x in spec.var_codes}
    role_groups: dict[str, list[dict[str, Any]]] = {}
    for role, members in (family.get("item_role_groups") or {}).items():
        kept = []
        for item in members or []:
            code = str(item.get("var_code", ""))
            if code.lower() not in allowed:
                continue
            enriched = dict(item)
            enriched.update(item_metadata[code.lower()])
            kept.append(enriched)
        if kept:
            role_groups[role] = kept
    family = dict(family)
    family["family_id"] = spec.joint_configuration_id
    family["joint_configuration_id"] = spec.joint_configuration_id
    family["source_family"] = spec.source_family
    family["family_label"] = spec.family_label
    family["eligible_waves"] = [spec.wave]
    family["item_role_groups"] = role_groups
    family["authority_metadata"] = {
        "scope_id": SCOPE_ID,
        "production_completeness_claim": PRODUCTION_CLAIM,
        "p2_source_structure_id": spec.source_structure_id,
        "p3_authority_release_id": R184_RELEASE,
        "p3_authority_effect": "QUESTION_PROPOSITION_IDENTITY_ONLY_WHERE_MEMBERSHIP_EXISTS",
        "response_portability_status": "NOT_AUTHORIZED_BY_P3",
        "configuration_authority_status": "GOVERNED_BOUNDED_CANARY_ONLY",
        "inherited_registry_family_id": spec.existing_gss_family_id,
    }
    return family


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--canary-root", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--adjudications-path", type=Path, required=True)
    args = ap.parse_args()
    root, canary, out = args.repo_root, args.canary_root, args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    adjudication_payload = json.loads(args.adjudications_path.read_text(encoding="utf-8"))
    joint_authority_release_id = str(adjudication_payload.get("authority_release_id", "")).strip()
    if not joint_authority_release_id:
        raise RuntimeError("Bounded joint-configuration adjudications are missing authority_release_id")
    if adjudication_payload.get("authority_scope") != SCOPE_ID:
        raise RuntimeError("Bounded joint-configuration adjudication scope mismatch")
    if adjudication_payload.get("production_completeness_claim") != PRODUCTION_CLAIM:
        raise RuntimeError("Bounded joint-configuration adjudications must deny production completeness")
    if adjudication_payload.get("p3_parent_authority_release_id") != R184_RELEASE:
        raise RuntimeError("Bounded joint-configuration adjudications cite a stale P3 parent release")
    decisions = {row["joint_configuration_id"]: {**row, "authority_release_id": joint_authority_release_id} for row in adjudication_payload.get("decisions", [])}
    if len(decisions) != len(adjudication_payload.get("decisions", [])):
        raise RuntimeError("Duplicate bounded joint-configuration adjudication ID surface")

    p2 = root / "32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1"
    structure_registry = read_csv(p2 / "Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv")
    structure_membership = read_csv(p2 / "Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv")
    lineage_registry = read_csv(p2 / "Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv")
    lineage_lookup = lineage_registry.set_index("lineage_id")
    p3 = root / "84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION" / "authority"
    p3_authority = read_csv(p3 / "P3C_CANONICAL_FAMILY_AUTHORITY.csv")
    p3_membership = read_csv(p3 / "P3C_CANONICAL_FAMILY_MEMBERSHIP.csv")
    p3_map = canonical_item_map(p3_membership, p3_authority)

    crosswalk_rows: list[dict[str, Any]] = []
    config_rows: list[dict[str, Any]] = []
    families: list[dict[str, Any]] = []
    scope_rows: list[dict[str, Any]] = []

    for spec in CONFIGURATIONS:
        decision = decisions.get(spec.joint_configuration_id)
        if not decision:
            raise RuntimeError(f"{spec.joint_configuration_id}: missing bounded joint-configuration adjudication")
        if decision.get("decision_status") not in {"ACCEPTED_BOUNDED_SOURCE_NATIVE_CONFIGURATION", "ACCEPTED_EXISTING_GSS_EXECUTABLE_CONTROL"}:
            raise RuntimeError(f"{spec.joint_configuration_id}: adjudication is not accepted")
        exact_surface = {
            "source_family": spec.source_family,
            "wave": spec.wave,
            "source_structure_id": spec.source_structure_id,
        }
        for key, expected in exact_surface.items():
            if str(decision.get(key, "")) != expected:
                raise RuntimeError(f"{spec.joint_configuration_id}: adjudication {key} mismatch")
        if [str(x) for x in decision.get("member_var_codes", [])] != list(spec.var_codes):
            raise RuntimeError(f"{spec.joint_configuration_id}: adjudicated member order mismatch")
        role_map = {str(k).lower(): str(v) for k, v in (decision.get("item_roles") or {}).items()}
        if set(role_map) != {value.lower() for value in spec.var_codes}:
            raise RuntimeError(f"{spec.joint_configuration_id}: adjudicated item-role surface mismatch")
        if int(decision.get("minimum_items_answered", -1)) != spec.minimum_items_answered:
            raise RuntimeError(f"{spec.joint_configuration_id}: minimum-items adjudication mismatch")
        if bool(decision.get("signed_boundary_authority")) != spec.signed_boundary_authority:
            raise RuntimeError(f"{spec.joint_configuration_id}: signed-boundary adjudication mismatch")

        filter_payload = json.loads((canary / "filters" / spec.filter_file).read_text(encoding="utf-8"))
        selected = {str(x).lower() for x in (filter_payload.get("var_codes") or [])}
        missing_filter = [x for x in spec.var_codes if x.lower() not in selected]
        if missing_filter:
            raise RuntimeError(f"{spec.joint_configuration_id}: variables absent from exact 20-variable filter: {missing_filter}")

        sr = structure_registry[structure_registry["source_structure_id"] == spec.source_structure_id]
        if sr.empty:
            raise RuntimeError(f"Missing source structure {spec.source_structure_id}")
        struct = sr.iloc[0]
        sm = structure_membership[
            (structure_membership["source_structure_id"] == spec.source_structure_id)
            & (structure_membership["source_family"] == spec.source_family)
            & (structure_membership["wave"] == spec.wave)
        ].copy()
        audit_path = locate_response_audit(canary, spec.scope_dir)
        audit = read_csv(audit_path)
        item_records: list[dict[str, Any]] = []
        item_metadata: dict[str, dict[str, Any]] = {}

        for ordinal, var_code in enumerate(spec.var_codes, start=1):
            match = sm[sm["source_variable_code"].str.lower() == var_code.lower()]
            if len(match) != 1:
                raise RuntimeError(f"{spec.joint_configuration_id}/{var_code}: expected one exact P2 source-structure membership, found {len(match)}")
            m = match.iloc[0]
            lineage_id = str(m.lineage_id)
            lineage = lineage_lookup.loc[lineage_id]
            response = audit_summary(audit, var_code)
            p3_binding = p3_map.get(lineage_id, {
                "p3_canonical_family_id": "",
                "p3_current_family_revision_id": "",
                "p3_variant_revision_id": "",
                "p3_authority_release_id": R184_RELEASE,
                "p3_membership_status": "SOURCE_LOCAL_ONLY_NOT_ON_P3_CANONICAL_SURFACE",
            })
            condition_label = str(lineage.representative_text).strip() or var_code
            item = {
                "var_code": var_code,
                "condition_label": condition_label,
                "item_role": role_map[var_code.lower()],
                "joint_configuration_adjudication_id": decision["adjudication_id"],
                "joint_configuration_authority_release_id": joint_authority_release_id,
                "p2_lineage_id": lineage_id,
                "question_implementation_id": str(m.question_implementation_id),
                "p2_source_structure_id": spec.source_structure_id,
                **p3_binding,
                "response_portability_status": "NOT_AUTHORIZED_BY_P3",
            }
            item_records.append(item)
            item_metadata[var_code.lower()] = {k: v for k, v in item.items() if k not in {"var_code", "condition_label"}}
            crosswalk_rows.append({
                "scope_id": SCOPE_ID,
                "production_completeness_claim": PRODUCTION_CLAIM,
                "joint_configuration_id": spec.joint_configuration_id,
                "source_family": spec.source_family,
                "wave": spec.wave,
                "country_code": spec.country_code,
                "family_type": spec.family_type,
                "family_label": spec.family_label,
                "source_structure_id": spec.source_structure_id,
                "source_structure_type": str(struct.structure_type),
                "source_structure_authority_status": str(struct.source_authority_status),
                "source_structure_cross_source_use_status": str(struct.cross_source_use_status),
                "item_order": ordinal,
                "item_role": role_map[var_code.lower()],
                "joint_configuration_adjudication_id": decision["adjudication_id"],
                "joint_configuration_decision_status": decision["decision_status"],
                "joint_configuration_authority_release_id": joint_authority_release_id,
                "var_code": var_code,
                "question_implementation_id": str(m.question_implementation_id),
                "p2_lineage_id": lineage_id,
                "question_text": str(lineage.representative_text),
                "response_topologies": str(lineage.response_topologies_json),
                "response_semantics_summary": json.dumps(response, sort_keys=True, ensure_ascii=False),
                **p3_binding,
                "response_portability_status": "NOT_AUTHORIZED_BY_P3",
                "configuration_authority_status": "GOVERNED_BOUNDED_CANARY_ONLY",
            })

        family = load_gss_control(root / "02_CORE_REFERENCE" / "question_family_registry_GSS_FROZEN_SNAPSHOT.yaml", spec, item_metadata) if spec.existing_gss_family_id else generic_family(spec, item_records, decision)
        family.setdefault("authority_metadata", {}).update({
            "joint_configuration_adjudication_id": decision["adjudication_id"],
            "joint_configuration_decision_status": decision["decision_status"],
            "joint_configuration_authority_release_id": joint_authority_release_id,
            "authority_basis_status": "HUMAN_ADJUDICATED_FROM_EXACT_SOURCE_EVIDENCE",
            "p2_authority_effect": "P2_DISCOVERY_EVIDENCE_ONLY_NOT_J_FAMILY_AUTHORITY" if not spec.existing_gss_family_id else "EXISTING_GSS_IMPLEMENTATION_REFERENCE",
            "adjudication_rationale": decision["rationale"],
            "authorized_inference": decision["authorized_inference"],
            "forbidden_inferences": decision["forbidden_inferences"],
        })
        families.append(family)
        config_rows.append({
            "scope_id": SCOPE_ID,
            "joint_configuration_id": spec.joint_configuration_id,
            "source_family": spec.source_family,
            "wave": spec.wave,
            "country_code": spec.country_code,
            "family_type": spec.family_type,
            "family_label": spec.family_label,
            "source_structure_id": spec.source_structure_id,
            "joint_configuration_adjudication_id": decision["adjudication_id"],
            "joint_configuration_decision_status": decision["decision_status"],
            "joint_configuration_authority_release_id": joint_authority_release_id,
            "adjudication_rationale": decision["rationale"],
            "authorized_inference": decision["authorized_inference"],
            "forbidden_inferences_json": json.dumps(decision["forbidden_inferences"], sort_keys=True),
            "item_count": len(spec.var_codes),
            "minimum_items_answered": spec.minimum_items_answered,
            "signed_boundary_authority": str(spec.signed_boundary_authority).lower(),
            "p3_bound_item_count": sum(1 for x in item_records if x["p3_membership_status"] == "BOUND_TO_CURRENT_CANONICAL_FAMILY"),
            "source_local_only_item_count": sum(1 for x in item_records if x["p3_membership_status"] != "BOUND_TO_CURRENT_CANONICAL_FAMILY"),
            "configuration_authority_status": "GOVERNED_BOUNDED_CANARY_ONLY",
        })
        scope_rows.append({
            "scope_id": SCOPE_ID,
            "source_family": spec.source_family,
            "wave": spec.wave,
            "country_code": spec.country_code,
            "scope_dir": spec.scope_dir,
            "filter_file": spec.filter_file,
            "filter_sha256": sha256_file(canary / "filters" / spec.filter_file),
            "v550_response_semantics_audit": str(audit_path.relative_to(canary)),
            "v550_response_semantics_audit_sha256": sha256_file(audit_path),
            "joint_configuration_id": spec.joint_configuration_id,
        })

    registry = {
        "registry_version": "bounded-r184-v1",
        "source_family": "MULTI_SOURCE_BOUNDED_CANARY",
        "status": "governed",
        "scope_id": SCOPE_ID,
        "production_completeness_claim": PRODUCTION_CLAIM,
        "p3_authority_release_id": R184_RELEASE,
        "joint_configuration_authority_release_id": joint_authority_release_id,
        "joint_configuration_adjudication_set_hash": sha256_file(args.adjudications_path),
        "response_portability_status": "NOT_AUTHORIZED_BY_P3",
        "families": families,
    }
    registry_hash = stable_hash(registry)
    registry["registry_content_hash"] = registry_hash
    (out / "bounded_9source_v550j_registry.yaml").write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=True), encoding="utf-8")
    for family in families:
        single = dict(registry)
        single["source_family"] = family["source_family"]
        single["families"] = [family]
        single["registry_content_hash"] = stable_hash({k: v for k, v in single.items() if k != "registry_content_hash"})
        safe = family["source_family"].lower().replace(" ", "_").replace("ó", "o")
        (out / f"registry_{safe}.yaml").write_text(yaml.safe_dump(single, sort_keys=False, allow_unicode=True), encoding="utf-8")

    write_csv(out / "bounded_joint_configuration_authority.csv", config_rows)
    write_csv(out / "bounded_joint_configuration_item_crosswalk.csv", crosswalk_rows)
    write_csv(out / "bounded_nine_scope_manifest.csv", scope_rows)
    manifest = {
        "status": "PASS_BOUNDED_AUTHORITY_GENERATED",
        "scope_id": SCOPE_ID,
        "production_completeness_claim": PRODUCTION_CLAIM,
        "p3_authority_release_id": R184_RELEASE,
        "joint_configuration_authority_release_id": joint_authority_release_id,
        "joint_configuration_adjudication_set_hash": sha256_file(args.adjudications_path),
        "configuration_count": len(config_rows),
        "source_family_count": len({r["source_family"] for r in config_rows}),
        "item_count": len(crosswalk_rows),
        "p3_bound_item_count": sum(1 for r in crosswalk_rows if r["p3_membership_status"] == "BOUND_TO_CURRENT_CANONICAL_FAMILY"),
        "source_local_only_item_count": sum(1 for r in crosswalk_rows if r["p3_membership_status"] != "BOUND_TO_CURRENT_CANONICAL_FAMILY"),
        "registry_content_hash": registry_hash,
        "response_portability_status": "NOT_AUTHORIZED_BY_P3",
        "authority_effect": "BOUNDED_SOURCE_NATIVE_JOINT_CONFIGURATION_AUTHORITY_ONLY",
        "input_hashes": {
            "p2_structure_registry": sha256_file(p2 / "Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv"),
            "p2_structure_membership": sha256_file(p2 / "Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv"),
            "p2_lineage_registry": sha256_file(p2 / "Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv"),
            "p3_family_authority": sha256_file(p3 / "P3C_CANONICAL_FAMILY_AUTHORITY.csv"),
            "p3_family_membership": sha256_file(p3 / "P3C_CANONICAL_FAMILY_MEMBERSHIP.csv"),
            "bounded_joint_configuration_adjudications": sha256_file(args.adjudications_path),
        },
    }
    (out / "BOUNDED_V550J_AUTHORITY_RETURN.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
