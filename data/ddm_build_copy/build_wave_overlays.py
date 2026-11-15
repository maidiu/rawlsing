#!/usr/bin/env python3
"""Build wave-specific overlay files for any survey family.

Generates review-candidate first-pass, semantic, position, and directionality
overlays from the question structure register. Heuristic inference is never
written as certified authority.

Output files are written only to
data/ddm_build_copy/reports/{source}_{wave}_*.csv.

Usage:
  python3 data/ddm_build_copy/build_wave_overlays.py \
    --source "Arab Barometer" --wave I --canonical-wave I
"""
import argparse, sys, json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_question_use import (
    infer_semantic_detail, infer_semantic_role,
    build_question_use_contract,
)
from data.ddm_build_copy.ddm_v550_family_overlay import load_family_overlay

REPORTS = ROOT / "data" / "ddm_build_copy" / "reports"
MANIFESTS = ROOT / "data" / "ddm_build_copy" / "manifests"

SOURCE_STRUCTURE_AUDIT_DIR = REPORTS / "source_structure_audits"


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"  Wrote {path} ({len(df)} rows)")


def build_overlays(source: str, wave: str, canonical_wave: str, output_dir: Path | None = None):
    print(f"=== Building overlays for {source} / {wave} ===")

    # ── 1. Load question structure register ──
    qsr_path = MANIFESTS / "question_structure_register.csv"
    print(f"\nLoading question_structure_register from {qsr_path}...")
    qsr = pd.read_csv(qsr_path, low_memory=False)
    qsr_wave = qsr[(qsr["source"].str.strip() == source) & (qsr["wave"].str.strip() == wave)]
    print(f"  Found {len(qsr_wave)} rows for {source}/{wave}")

    if len(qsr_wave) == 0:
        print(f"  WARNING: No rows found. Available waves: {qsr[qsr['source'].str.strip() == source]['wave'].unique()}")
        return

    # ── 2. Build first_pass_authority_table ──
    print(f"\n--- First-pass authority table ---")
    fp_cols = [
        "source", "wave", "canonical_wave", "var_name", "var_code",
        "question_id", "question_text", "module_guess", "semantic_lane",
        "semantic_role", "evidence_lane",
        "allowed_as_branch_position_signature", "allowed_as_branch_relation_cosignature",
        "allowed_as_attitude_cloud_anchor", "allowed_as_attitude_cloud_feature",
        "allowed_as_v551_relation_evidence", "allowed_as_association_feature",
        "is_substantive", "not_direct_evidence",
        "manual_designation_required", "designation_confidence", "rationale",
    ]
    fp_rows = []
    for _, r in qsr_wave.iterrows():
        row = {k: r.get(k, "") for k in fp_cols if k in qsr.columns}
        row["source"] = source
        row["wave"] = canonical_wave
        row["canonical_wave"] = canonical_wave
        # Fill missing cols
        for k in fp_cols:
            row.setdefault(k, "")
        # Infer semantic role if missing
        if not row.get("semantic_role"):
            try:
                row["semantic_role"] = infer_semantic_role(dict(r))
            except Exception:
                row["semantic_role"] = "unknown"
        for permission in (
            "allowed_as_branch_position_signature",
            "allowed_as_branch_relation_cosignature",
            "allowed_as_attitude_cloud_anchor",
            "allowed_as_attitude_cloud_feature",
            "allowed_as_v551_relation_evidence",
            "allowed_as_association_feature",
        ):
            row[permission] = False
        row["semantic_role_authority_status"] = "HEURISTIC_REVIEW_ONLY"
        row["runtime_authority_status"] = "NOT_CERTIFIED"
        row["manual_designation_required"] = True
        row["designation_confidence"] = "review_only"
        row["rationale"] = (
            str(row.get("rationale") or "").strip()
            or "heuristic candidate; independent authority review required"
        )
        fp_rows.append(row)
    fp_df = pd.DataFrame(fp_rows)

    # Save
    slug = source.lower().replace(" ", "_").replace("-", "_")
    first_pass_path = output_dir or REPORTS
    fp_name = f"{slug}_{canonical_wave}_first_pass_authority_table.csv"
    write_csv(fp_df, first_pass_path / fp_name)

    # ── 3. Build semantic_authority_overlay ──
    print(f"\n--- Semantic authority overlay ---")
    sa_rows = []
    for _, r in qsr_wave.iterrows():
        record = r.to_dict()
        try:
            detail = infer_semantic_detail(record)
        except Exception as e:
            print(f"  ERROR: {r.get('var_name', '?')}: {e}")
            detail = {"semantic_subrole": "unknown", "semantic_tags": "", "directionality_policy": "unsigned_context", "semantic_confidence": "low", "semantic_note": "inference_error"}
        role = str(record.get("semantic_role", "")).strip()
        if not role:
            try:
                role = infer_semantic_role(record)
            except Exception:
                role = "UNKNOWN"
        sa_rows.append({
            "source": source,
            "wave": canonical_wave,
            "canonical_wave": canonical_wave,
            "var_name": str(record.get("var_name", "")),
            "question_text": str(record.get("question_text", "")),
            "semantic_lane": str(record.get("semantic_lane", "")),
            "semantic_role": role,
            "evidence_lane": str(record.get("evidence_lane", "")),
            "semantic_subrole": detail.get("semantic_subrole", ""),
            "semantic_tags": detail.get("semantic_tags", ""),
            "directionality_policy": detail.get("directionality_policy", ""),
            "semantic_confidence": detail.get("semantic_confidence", "low"),
            "semantic_note": detail.get("semantic_note", ""),
            "semantic_role_authority_status": "HEURISTIC_REVIEW_ONLY",
            "semantic_detail_authority_status": "HEURISTIC_REVIEW_ONLY",
            "manual_review_required": True,
        })
    sa_df = pd.DataFrame(sa_rows)
    sa_name = f"{slug}_{canonical_wave}_semantic_authority_overlay.csv"
    write_csv(sa_df, REPORTS / sa_name)

    # ── 4. Build position_conditioning_overlay ──
    print(f"\n--- Position conditioning overlay ---")
    pc_rows = []
    for _, r in qsr_wave.iterrows():
        record = r.to_dict()
        try:
            detail = infer_semantic_detail(record)
        except Exception:
            detail = {"semantic_subrole": "unknown", "semantic_tags": "", "directionality_policy": "unsigned_context", "semantic_confidence": "low", "semantic_note": ""}
        role = str(record.get("semantic_role", "")).strip()
        if not role:
            try:
                role = infer_semantic_role(record)
            except Exception:
                role = "UNKNOWN"
        pc_rows.append({
            "source": source,
            "wave": canonical_wave,
            "canonical_wave": canonical_wave,
            "var_name": str(record.get("var_name", "")),
            "question_text": str(record.get("question_text", "")),
            "semantic_lane": str(record.get("semantic_lane", "")),
            "semantic_role": role,
            "evidence_lane": str(record.get("evidence_lane", "")),
            "semantic_subrole": detail.get("semantic_subrole", ""),
            "semantic_tags": detail.get("semantic_tags", ""),
            "directionality_policy": detail.get("directionality_policy", ""),
            "semantic_confidence": detail.get("semantic_confidence", "low"),
            "semantic_note": detail.get("semantic_note", ""),
            "position_conditioning": str(record.get("position_conditioning", "")),
            "position_modifiers": str(record.get("position_modifiers", "")),
            "structural_mapping_authority_status": "HEURISTIC_REVIEW_ONLY",
            "manual_review_required": True,
        })
    pc_df = pd.DataFrame(pc_rows)
    pc_name = f"{slug}_{canonical_wave}_position_conditioning_overlay.csv"
    write_csv(pc_df, REPORTS / pc_name)

    # ── 5. Build directionality_overlay ──
    print(f"\n--- Directionality overlay ---")
    # For this we need the response option map to get anchor labels
    rom_path = REPORTS / "V550_response_option_map.csv"
    rom = None
    if rom_path.exists():
        print(f"  Loading response option map from {rom_path}...")
        try:
            rom = pd.read_csv(rom_path, low_memory=False, nrows=500000)
        except Exception as e:
            print(f"  WARNING: Could not load response option map: {e}")

    di_rows = []
    for _, r in qsr_wave.iterrows():
        record = r.to_dict()
        try:
            detail = infer_semantic_detail(record)
        except Exception:
            detail = {"semantic_subrole": "unknown", "semantic_tags": "", "directionality_policy": "unsigned_context", "semantic_confidence": "low", "semantic_note": ""}

        var_name = str(record.get("var_name", ""))
        policy = detail.get("directionality_policy", "")
        pol_status = policy
        resp_family = "ordinal_scale"
        pos_anchor = ""
        neg_anchor = ""
        neutral = "neutral / ambivalent"
        suggested_bridge_action = "force_unsigned" if policy in ("unsigned_identity", "unsigned_context", "unsigned_metadata") else "allow_directionality"
        confidence = detail.get("semantic_confidence", "low")
        note = detail.get("semantic_note", "")

        # Try to get anchor labels from response option map
        if rom is not None and var_name:
            rom_vars = rom[rom["var_name"].astype(str).str.strip() == var_name]
            if len(rom_vars) > 0:
                # Get the first row's response family
                resp_families = rom_vars["response_family"].dropna().unique()
                if len(resp_families) > 0:
                    resp_family = resp_families[0]
                if "signed" in policy:
                    suggested_bridge_action = "allow_directionality"
                    if "evaluat" in policy or "frequency" in policy:
                        pos_anchor = "more positive" if "evaluat" in policy else "more frequent"
                        neg_anchor = "more negative" if "evaluat" in policy else "less frequent"
                    elif "attitude" in policy:
                        pos_anchor = "more endorsing"
                        neg_anchor = "more rejecting"
                    elif "policy" in policy:
                        pos_anchor = "more approving"
                        neg_anchor = "more disapproving"
                    elif "coordinate" in policy:
                        pos_anchor = "more positive"
                        neg_anchor = "more negative"
                        suggested_bridge_action = "force_unsigned"

        di_rows.append({
            "source": source,
            "wave": canonical_wave,
            "canonical_wave": canonical_wave,
            "var_name": var_name,
            "question_text": str(record.get("question_text", "")),
            "semantic_role": str(record.get("semantic_role", "")).strip() or "UNKNOWN",
            "semantic_subrole": detail.get("semantic_subrole", ""),
            "directionality_policy": policy,
            "signed_polarity_status": pol_status,
            "response_family_expectation": resp_family,
            "positive_anchor_label": pos_anchor,
            "negative_anchor_label": neg_anchor,
            "neutral_anchor_label": neutral,
            "bridge_directionality_action": "force_unsigned",
            "suggested_bridge_directionality_action": suggested_bridge_action,
            "directionality_confidence": confidence,
            "directionality_note": note,
            "directionality_authority_status": "HEURISTIC_REVIEW_ONLY",
            "directional_certification_status": "NOT_CERTIFIED",
            "current_directional_atom_eligible": False,
            "manual_review_required": True,
        })
    di_df = pd.DataFrame(di_rows)
    di_name = f"{slug}_{canonical_wave}_directionality_overlay.csv"
    write_csv(di_df, REPORTS / di_name)

    # ── Summary ──
    print(f"\n=== Summary for {source}/{wave} ===")
    print(f"  first_pass_authority_table:  {len(fp_df)} rows")
    print(f"  semantic_authority_overlay:   {len(sa_df)} rows")
    print(f"  position_conditioning_overlay: {len(pc_df)} rows")
    print(f"  directionality_overlay:      {len(di_df)} rows")
    print(f"  Output: {REPORTS}/")
    print(f"\n  Directionality policy distribution:")
    print(f"    {di_df['directionality_policy'].value_counts().to_string()}")


def main():
    parser = argparse.ArgumentParser(description="Build wave-specific overlay files for any survey family")
    parser.add_argument("--source", required=True, help="Survey family name (e.g., 'Arab Barometer')")
    parser.add_argument("--wave", required=True, help="Wave identifier (e.g., 'I', '1972', 'W1')")
    parser.add_argument("--canonical-wave", default=None, help="Canonical wave (defaults to --wave)")
    parser.add_argument("--output-dir", default=None, help="Override output directory")
    args = parser.parse_args()

    build_overlays(
        source=args.source,
        wave=args.wave,
        canonical_wave=args.canonical_wave or args.wave,
        output_dir=Path(args.output_dir) if args.output_dir else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
