#!/usr/bin/env python3
"""Batch build review-only directionality candidates for survey families.

Heuristics in this file do not certify semantic role or directionality. Machine
source/wave identity is delegated to the shared governed UID kernel; the
historical table below supplies only DB/codebook locator provenance.
Run: python3 data/ddm_build_copy/build_all_survey_overlays.py
"""
import argparse, os, re, sys
from pathlib import Path

import pandas as pd
import psycopg2

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    validate_source_wave_identity_coherence,
)
from data.ddm_build_copy.ddm_source_wave_identity import (
    ProductionMembershipError,
    SourceWaveIdentityError,
    resolve_source_family_identity,
    resolve_source_wave_identity,
)
from data.ddm_build_copy.ddm_v550_family_overlay import (
    enforce_review_only_overlay_frame,
    resolve_overlay_identity,
)

CB_DIR = REPO / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"
AUTH_DIR = REPO / "data" / "ddm_build_copy" / "directionality_authority"
REPORTS = REPO / "data" / "ddm_build_copy" / "reports"
DSN = os.environ.get("DATABASE_URL", "").strip()

# Historical DB/QSM/codebook locator metadata. These spellings are provenance,
# not machine identity or production authorization.
ALL_SURVEYS = [
    # (survey_name, db_wave, qsm_wave, canonical_wave, codebook_filename, codebook_has_svl)
    ("Afrobarometer", "R1", "R1", "R1", "Afrobarometer Round 1 codebook.csv", False),
    ("Afrobarometer", "R5", "R5", "R5", "Afrobarometer Round 5 codebook.csv", True),
    ("Afrobarometer", "R9", "R9", "R9", "Afrobarometer Round 9 codebook.csv", False),
    ("Arab Barometer", "I", "W1", "I", "Arab Barometer Wave 1 codebook.csv", True),
    ("Arab Barometer", "II", "W2", "II", "Arab Barometer Wave 2 codebook.csv", False),
    ("Arab Barometer", "V", "W5", "V", "Arab Barometer Wave 5 codebook.csv", True),
    ("Arab Barometer", "VIII", "W8", "VIII", "Arab Barometer Wave 8 codebook.csv", True),
    ("Asian Barometer", "W1", "W1", "W1", "Asian Barometer Wave 1 codebook.csv", False),
    ("Asian Barometer", "W4", "W4", "W4", "Asian Barometer Wave 4 codebook.csv", True),
    ("Asian Barometer", "W5", "W5", "W5", "Asian Barometer Wave 5 codebook.csv", True),
    ("Asian Barometer", "W6", "W6", "W6", "Asian Barometer Wave 6 codebook.csv", False),
    ("EVS", "1981", "W1", "1981", "EVS Wave 1 codebook 1981.csv", True),
    ("EVS", "1990", "1990", "1990", "EVS Wave 2 codebook 1990.csv", True),
    ("EVS", "1999", "W3", "1999", "EVS Wave 3 codebook 1999.csv", True),
    ("EVS", "2008", "2008", "2008", "EVS Wave 4 codebook 2008.csv", True),
    ("EVS", "2017", "2017", "2017", "EVS Wave 5 codebook 2017.csv", True),
    ("Latinobarómetro", "1995", "1995", "1995", "Latinobarometro 1995 codebook.csv", False),
    ("Latinobarómetro", "2011", "2011", "2011", "Latinobarometro 2011 codebook.csv", True),
    ("Latinobarómetro", "2024", "2024", "2024", "Latinobarometro 2024 codebook.csv", False),
    ("LiTS", "2006", "2006", "I", "LiTS-I-codebook.csv", False),
    ("LiTS", "II", "II", "II", "LiTS-II-codebook.csv", False),
    ("LiTS", "III", "III", "III", "LiTS-III-codebook.csv", False),
    ("LiTS", "IV", "IV", "IV", "LiTS-IV-codebook.csv", False),
    ("South Asia", "W1", "W1", "W1", "South Asia Wave 1 codebook.csv", True),
    ("South Asia", "W2", "W2", "W2", "South Asia Wave 2 codebook.csv", True),
    ("WVS", "W1", "W1", "W1", "World Values Survey Wave 1 codebook.csv", True),
    ("WVS", "W4", "W4", "W4", "World Values Survey Wave 4 codebook.csv", True),
    ("WVS", "W7", "W7", "W7", "World Values Survey Wave 7 codebook.csv", True),
]


def connect():
    if not DSN:
        raise RuntimeError("DATABASE_URL is required")
    return psycopg2.connect(DSN)


def slugify(s):
    return re.sub(r"[^a-zA-Z0-9]", "_", s).strip("_").lower()


def detect_ordinal_parts(svl):
    """Count ordinal positions if value labels look ordered."""
    parts = [p.strip() for p in svl.split("|") if p.strip()]
    codes = []
    for p in parts:
        m = re.match(r"\s*(\d+)\s*=", p)
        if m:
            codes.append(int(m.group(1)))
    if codes and codes == list(range(1, len(codes) + 1)):
        return len(codes), True
    return len(parts), False


def classify_from_labels(var_name, question_text, svl):
    """Classify a variable from its substantive_value_labels."""
    if not svl or svl == "nan" or pd.isna(svl):
        return None
    svl_lower = svl.lower()
    parts = [p.strip() for p in svl.split("|") if p.strip()]

    if re.search(r"\b1\s*=\s*(?:yes|favor|approve|agree|male)\b", svl_lower) and re.search(r"\b2\s*=\s*(?:no|oppose|disapprove|disagree|female)\b", svl_lower):
        codes = set()
        for p in parts:
            m = re.match(r"\s*(\d+)", p)
            if m:
                codes.add(int(m.group(1)))
        if codes in ({1, 2}, {1, 2, 3}):
            return {
                "semantic_role": "relation_evidence",
                "semantic_subrole": "binary_attitude",
                "directionality_policy": "signed_attitude",
                "signed_polarity_status": "signed_attitude",
                "response_family_expectation": "yes_no",
                "positive_anchor_label": "more endorsing",
                "negative_anchor_label": "more rejecting",
                "neutral_anchor_label": "neutral / ambivalent",
                "bridge_directionality_action": "allow_directionality",
                "directionality_confidence": "high",
                "directionality_note": "binary item; sign reflects endorsement vs rejection",
                "manual_review_required": False,
            }

    ordinal4_pos = ["very good", "good", "very satisfied", "satisfied", "very safe", "safe",
                    "very interested", "interested", "strongly agree", "agree", "a great deal"]
    ordinal4_neg = ["bad", "very bad", "dissatisfied", "unsafe", "not interested", "disagree", "strongly disagree",
                    "no trust"]
    if len(parts) == 4:
        codes = []
        labels = []
        for p in parts:
            m = re.match(r"\s*(\d+)\s*=\s*(.+)", p)
            if m:
                codes.append(int(m.group(1)))
                labels.append(m.group(2).strip().lower())
        if codes == [1, 2, 3, 4]:
            has_pos = any(any(pos in lbl for pos in ordinal4_pos) for lbl in labels[:2])
            has_neg = any(any(neg in lbl for neg in ordinal4_neg) for lbl in labels[2:])
            if has_pos and has_neg:
                return {
                    "semantic_role": "relation_evidence",
                    "semantic_subrole": "subjective_evaluation",
                    "directionality_policy": "signed_evaluation",
                    "signed_polarity_status": "signed_evaluation",
                    "response_family_expectation": "ordinal_scale",
                    "positive_anchor_label": "more positive",
                    "negative_anchor_label": "more negative",
                    "neutral_anchor_label": "neutral / ambivalent",
                    "bridge_directionality_action": "allow_directionality",
                    "directionality_confidence": "high",
                    "directionality_note": "evaluative ordered item; sign from unfavorable to favorable",
                    "manual_review_required": False,
                }
            if "trust" in svl_lower:
                return {
                    "semantic_role": "relation_evidence",
                    "semantic_subrole": "trust_evaluation",
                    "directionality_policy": "signed_evaluation",
                    "signed_polarity_status": "signed_evaluation",
                    "response_family_expectation": "ordinal_scale",
                    "positive_anchor_label": "more trusting",
                    "negative_anchor_label": "less trusting",
                    "neutral_anchor_label": "neutral / ambivalent",
                    "bridge_directionality_action": "allow_directionality",
                    "directionality_confidence": "high",
                    "directionality_note": "trust ordered item; sign from less to more trusting",
                    "manual_review_required": False,
                }

    if any(w in svl_lower for w in ["strongly agree", "agree", "disagree", "somewhat agree"]):
        clean_parts = [p for p in parts if re.match(r"\s*([0-9]|10)\s*=", p)]
        if len(clean_parts) >= 3:
            codes = [int(re.match(r"\s*(\d+)", p).group(1)) for p in clean_parts if re.match(r"\s*(\d+)", p)]
            if codes and len(set(codes)) == len(codes) and max(codes) - min(codes) <= len(codes):
                return {
                    "semantic_role": "relation_evidence",
                    "semantic_subrole": "subjective_evaluation",
                    "directionality_policy": "signed_evaluation",
                    "signed_polarity_status": "signed_evaluation",
                    "response_family_expectation": "ordinal_scale",
                    "positive_anchor_label": "more positive",
                    "negative_anchor_label": "more negative",
                    "neutral_anchor_label": "neutral / ambivalent",
                    "bridge_directionality_action": "allow_directionality",
                    "directionality_confidence": "high",
                    "directionality_note": "evaluative ordered item",
                    "manual_review_required": False,
                }

    if any(w in svl_lower for w in ["daily", "often", "frequently", "always", "never"]):
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "behavioral_frequency",
            "directionality_policy": "signed_frequency",
            "signed_polarity_status": "signed_frequency",
            "response_family_expectation": "frequency_scale",
            "positive_anchor_label": "more frequent",
            "negative_anchor_label": "less frequent",
            "neutral_anchor_label": "neutral / ambivalent",
            "bridge_directionality_action": "allow_directionality",
            "directionality_confidence": "high",
            "directionality_note": "frequency-ordered item",
            "manual_review_required": False,
        }

    if re.search(r"10.point|dictatorship.*democracy|1.*complete.*10", svl_lower):
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "subjective_evaluation",
            "directionality_policy": "signed_evaluation",
            "signed_polarity_status": "signed_evaluation",
            "response_family_expectation": "ordinal_scale",
            "positive_anchor_label": "more positive",
            "negative_anchor_label": "more negative",
            "neutral_anchor_label": "neutral / ambivalent",
            "bridge_directionality_action": "allow_directionality",
            "directionality_confidence": "high",
            "directionality_note": "10-point scale item",
            "manual_review_required": False,
        }

    if any(kw in svl_lower for kw in ["television", "newspaper", "radio", "internet"]):
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "informational_channel",
            "directionality_policy": "unsigned_identity",
            "signed_polarity_status": "unsigned_identity",
            "response_family_expectation": "nominal_single_choice",
            "positive_anchor_label": "", "negative_anchor_label": "", "neutral_anchor_label": "",
            "bridge_directionality_action": "force_unsigned",
            "directionality_confidence": "high",
            "directionality_note": "nominal categorical choice; keep unsigned",
            "manual_review_required": False,
        }

    demo_label_markers = [
        r"\d+\s*-\s*\d+\s*(?:years|dh|shekel|dinar)", r"(?:less than|more than)\s*\d+",
        r"\b(?:illiterate|elementary|primary|secondary|college|university|postgraduate)\b",
        r"\b(?:muslim|christian|shiite|sunni|druze|jewish)\b",
        r"\b(?:public sector|private sector|ngo|government)\b",
        r"\b(?:housewife|student|retired|unemployed)\b",
        r"\b(?:married|single|divorced|widowed)\b",
        r"\b(?:dh\b|dinar|shekel|pound)\b",
    ]
    demo_matches = sum(1 for p in demo_label_markers if re.search(p, svl_lower))
    has_attitude = any(w in svl_lower for w in ["agree", "disagree", "satisfied", "approve", "trust"])
    if demo_matches >= 2 and not has_attitude:
        return None

    return None


def _validate_locator_representations(identity, survey, db_wave, qsm_wave, canonical_wave):
    """All populated historical representations must resolve to one UID pair."""
    try:
        return validate_source_wave_identity_coherence(
            {
                "source": survey,
                "raw_wave": db_wave,
                "wave": qsm_wave,
                "canonical_wave": canonical_wave,
            },
            expected_source_family_uid=identity.source_family_uid,
            expected_wave_uid=identity.wave_uid,
            require_complete=True,
        )
    except BoundaryContractError as exc:
        raise RuntimeError(f"OVERLAY_LOCATOR_IDENTITY_CONTRADICTION:{exc}") from exc


def build_for_survey(
    survey,
    db_wave,
    qsm_wave,
    canonical_wave,
    codebook_file,
    has_svl,
    *,
    historical_nonproduction=False,
):
    identity = resolve_overlay_identity(
        survey,
        canonical_wave,
        historical_nonproduction=historical_nonproduction,
    )
    _validate_locator_representations(identity, survey, db_wave, qsm_wave, canonical_wave)

    source = identity.canonical_display_source
    canonical_wave = identity.canonical_display_wave
    slug = slugify(source)
    cb_path = CB_DIR / codebook_file
    print(f"\n{'='*60}")
    print(
        f"{source} / raw_db={db_wave} / display={canonical_wave} "
        f"[{identity.source_family_uid}|{identity.wave_uid}]"
    )
    print(f"  Codebook: {codebook_file}")

    codebook = None
    if cb_path.exists():
        try:
            codebook = pd.read_csv(cb_path, low_memory=False)
            print(f"  Loaded codebook: {len(codebook)} rows")
        except Exception as e:
            print(f"  WARNING: Could not load codebook: {e}")

    # QSM scope is machine identity; raw DB/QSM spellings remain provenance.
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT var_code, question_id, driver_id, driver_facet_id, relation_axis_id, "
        "target_entity_id, structural_domain_id, display_text "
        "FROM question_structural_mapping WHERE source_family_uid=%s AND wave_uid=%s "
        "ORDER BY var_code",
        (identity.source_family_uid, identity.wave_uid),
    )
    qsm_vars = cur.fetchall()
    conn.close()
    print(f"  QSM variables: {len(qsm_vars)}")

    if len(qsm_vars) == 0:
        print(f"  SKIP: No question_structural_mapping for {identity.uid_key}")
        return 0

    rows = []
    for vrow in qsm_vars:
        vn = str(vrow[0]).strip() if vrow[0] else ""
        qi = str(vrow[1]).strip() if vrow[1] else ""
        di = str(vrow[2]).strip() if vrow[2] else ""
        dfi = str(vrow[3]).strip() if vrow[3] else ""
        rai = str(vrow[4]).strip() if vrow[4] else ""
        tei = str(vrow[5]).strip() if vrow[5] else ""
        sdi = str(vrow[6]).strip() if vrow[6] else ""
        dt = str(vrow[7]).strip() if vrow[7] else ""

        qt = dt
        svl = ""
        if codebook is not None and vn:
            cb_cols = set(codebook.columns)
            if "var_name" in cb_cols:
                cb_row = codebook[codebook["var_name"].astype(str).str.strip() == vn]
                if len(cb_row) > 0:
                    qt = str(cb_row.iloc[0].get("question_text", dt))
                    if has_svl:
                        svl = str(cb_row.iloc[0].get("substantive_value_labels", ""))
                    elif "response_options_substantive" in cb_cols:
                        svl = str(cb_row.iloc[0].get("response_options_substantive", ""))
            elif "name" in cb_cols:
                cb_row = codebook[codebook["name"].astype(str).str.strip() == vn]
                if len(cb_row) > 0:
                    qt = str(cb_row.iloc[0].get("label", dt))
            elif "question_id" in cb_cols:
                cb_row = codebook[codebook["question_id"].astype(str).str.strip() == vn]
                if len(cb_row) > 0:
                    qt = str(cb_row.iloc[0].get("question_text", dt))
                    if has_svl:
                        svl = str(cb_row.iloc[0].get("substantive_value_labels", ""))

        cls = classify_from_labels(vn, qt, svl) if svl else None

        if cls:
            role = cls["semantic_role"]
            subrole = cls["semantic_subrole"]
            policy = cls["directionality_policy"]
            pol_status = cls["signed_polarity_status"]
            resp_fam = cls["response_family_expectation"]
            pos = cls["positive_anchor_label"]
            neg = cls["negative_anchor_label"]
            neu = cls["neutral_anchor_label"]
            bridge = cls["bridge_directionality_action"]
            conf = cls["directionality_confidence"]
            note = cls["directionality_note"]
        else:
            has_driver = bool(di)
            has_axis = bool(rai)
            di_lower = di.lower() if di else ""
            is_metadata_driver = any(di_lower.startswith(p) for p in ["metadata::", "context::", "admin::"])
            is_demo_driver = any(kw in di_lower for kw in ["demo_", "demo_age", "demo_sex", "demo_educ",
                                                              "demo_income", "demo_region", "demo_relig",
                                                              "demo_employ", "demo_occup", "sector",
                                                              "urban", "rural", "ethnic", "language",
                                                              "hhsize", "hhtype", "num_child", "marital",
                                                              "birthyr", "age", "gender", "weight"])
            if is_metadata_driver or is_demo_driver:
                role = "position_context"
                subrole = "demographic_status"
                policy = "unsigned_context"
                pol_status = "unsigned_context"
                resp_fam = "nominal_single_choice"
                pos = ""; neg = ""; neu = ""
                bridge = "force_unsigned"
                conf = "high"
                note = "demographic / context item; keep unsigned"
            elif has_driver and has_axis:
                role = "relation_evidence"
                subrole = "qsm_structured"
                policy = "signed_evaluation"
                pol_status = "signed_evaluation"
                resp_fam = "ordinal_scale"
                pos = "more positive"
                neg = "more negative"
                neu = "neutral / ambivalent"
                bridge = "allow_directionality"
                conf = "medium"
                note = "classified from QSM driver/axis presence; verify directionality"
            elif has_driver:
                role = "relation_evidence"
                subrole = "qsm_partial"
                policy = "signed_evaluation"
                pol_status = "signed_evaluation"
                resp_fam = "ordinal_scale"
                pos = "more positive"
                neg = "more negative"
                neu = "neutral / ambivalent"
                bridge = "allow_directionality"
                conf = "low"
                note = "has driver_id but no relation_axis_id; weak directionality"
            else:
                role = "position_context"
                subrole = "context_coordinate"
                policy = "unsigned_context"
                pol_status = "unsigned_context"
                resp_fam = "nominal_single_choice"
                pos = ""; neg = ""; neu = ""
                bridge = "force_unsigned"
                conf = "high"
                note = "no driver mapping; context/coordinate item"

        rows.append({
            "raw_source": survey,
            "raw_db_wave": db_wave,
            "qsm_wave_provenance": qsm_wave,
            "canonical_display_source": identity.canonical_display_source,
            "canonical_display_wave": identity.canonical_display_wave,
            "source_family_uid": identity.source_family_uid,
            "wave_uid": identity.wave_uid,
            "governance_state": identity.governance_state,
            "closed_35_member": identity.closed_35_member,
            "source": source,
            "wave": canonical_wave,
            "canonical_wave": canonical_wave,
            "var_name": vn,
            "question_id": qi,
            "driver_id": di,
            "driver_facet_id": dfi,
            "relation_axis_id": rai,
            "target_entity_id": tei,
            "structural_domain_id": sdi,
            "question_text": qt,
            "semantic_role": role,
            "semantic_subrole": subrole,
            "directionality_policy": policy,
            "signed_polarity_status": pol_status,
            "response_family_expectation": resp_fam,
            "positive_anchor_label": pos,
            "negative_anchor_label": neg,
            "neutral_anchor_label": neu,
            "bridge_directionality_action": "force_unsigned",
            "suggested_bridge_directionality_action": bridge,
            "directionality_confidence": conf,
            "directionality_note": note,
            "semantic_role_authority_status": "HEURISTIC_REVIEW_ONLY",
            "directionality_authority_status": "HEURISTIC_REVIEW_ONLY",
            "directional_certification_status": "NOT_CERTIFIED",
            "current_directional_atom_eligible": False,
            "manual_review_required": True,
        })

    df = enforce_review_only_overlay_frame(pd.DataFrame(rows))
    print(f"  Generated: {len(df)} directionality rows")

    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    auth_name = f"{slug}_{canonical_wave}_directionality_authority.csv"
    df.to_csv(AUTH_DIR / auth_name, index=False)
    print(f"  Wrote: {auth_name}")

    REPORTS.mkdir(parents=True, exist_ok=True)
    ol_name = f"{slug}_{canonical_wave}_directionality_overlay.csv"
    df.to_csv(REPORTS / ol_name, index=False)
    print(f"  Wrote: {ol_name}")

    return len(df)


def update_index():
    """Rebuild the review-only directionality index from row identity, not filenames."""
    index_rows = []
    for path in sorted(AUTH_DIR.glob("*_directionality_authority.csv")):
        try:
            df = pd.read_csv(path, low_memory=False)
            cnt = len(df)
        except Exception as exc:
            index_rows.append({
                "source": "", "wave": "", "source_family_uid": "", "wave_uid": "",
                "file_name": path.name, "row_count": 0,
                "status": "review_only_unreadable", "notes": str(exc),
            })
            continue

        if df.empty:
            index_rows.append({
                "source": "", "wave": "", "source_family_uid": "", "wave_uid": "",
                "file_name": path.name, "row_count": 0,
                "status": "review_only_empty", "notes": "",
            })
            continue

        if not {"source_family_uid", "wave_uid"}.issubset(df.columns):
            index_rows.append({
                "source": "", "wave": "", "source_family_uid": "", "wave_uid": "",
                "file_name": path.name, "row_count": cnt,
                "status": "legacy_unresolved_review_only",
                "notes": "identity not inferred from filename; regenerate through UID-aware builder",
            })
            continue

        source_uids = {str(v).strip() for v in df["source_family_uid"].dropna() if str(v).strip()}
        wave_uids = {str(v).strip() for v in df["wave_uid"].dropna() if str(v).strip()}
        if len(source_uids) != 1 or len(wave_uids) != 1:
            raise RuntimeError(f"REVIEW_OVERLAY_INDEX_MIXED_UID_SCOPE:{path}")
        source_uid = next(iter(source_uids))
        wave_uid = next(iter(wave_uids))
        identity = resolve_source_wave_identity(
            str(df.iloc[0].get("canonical_display_source") or df.iloc[0].get("source") or ""),
            str(df.iloc[0].get("canonical_display_wave") or df.iloc[0].get("wave") or ""),
        )
        if identity.source_family_uid != source_uid or identity.wave_uid != wave_uid:
            raise RuntimeError(f"REVIEW_OVERLAY_INDEX_UID_CONTRADICTION:{path}")
        index_rows.append({
            "source": identity.canonical_display_source,
            "wave": identity.canonical_display_wave,
            "source_family_uid": source_uid,
            "wave_uid": wave_uid,
            "file_name": path.name,
            "row_count": cnt,
            "status": "review_only_not_certified",
            "notes": "HEURISTIC_REVIEW_ONLY; NOT_CERTIFIED",
        })

    idx_df = pd.DataFrame(index_rows)
    idx_path = AUTH_DIR / "directionality_authority_index.csv"
    idx_df.to_csv(idx_path, index=False)
    print(f"\nUpdated review-only index: {idx_path} ({len(index_rows)} entries)")


def _selected_source_uids(values):
    if not values:
        return None
    return {resolve_source_family_identity(value).source_family_uid for value in values}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--surveys", nargs="*", default=None,
                        help="Specific survey families to build (aliases resolve by governed source UID)")
    parser.add_argument(
        "--historical-nonproduction",
        action="store_true",
        help="Explicitly include recognized excluded/historical review identities such as Asian Barometer W6",
    )
    args = parser.parse_args()

    selected_uids = _selected_source_uids(args.surveys)
    total = 0
    for s, dw, qw, cw, cb, svl in ALL_SURVEYS:
        family_uid = resolve_source_family_identity(s).source_family_uid
        if selected_uids is not None and family_uid not in selected_uids:
            continue
        try:
            identity = resolve_overlay_identity(
                s,
                cw,
                historical_nonproduction=args.historical_nonproduction,
            )
        except ProductionMembershipError as exc:
            print(f"SKIP NONPRODUCTION: {s}/{cw}: {exc}")
            continue
        cnt = build_for_survey(
            s, dw, qw, cw, cb, svl,
            historical_nonproduction=args.historical_nonproduction,
        )
        total += cnt

    update_index()

    print(f"\n{'='*60}")
    print(f"Total review-only directionality rows generated: {total}")
    print("Done.")


if __name__ == "__main__":
    main()
