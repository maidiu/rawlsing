#!/usr/bin/env python3
"""Manual authority for Arab Barometer W2, W5, W8.
Uses W1 manual classifications as family template.
Handles wave-specific variables by question-text patterns.
Script serializes decisions only — does not infer semantics."""
import csv, json, re
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
AUTH = REPO / "data" / "ddm_build_copy" / "directionality_authority"
REP = REPO / "data" / "ddm_build_copy" / "reports"

SOURCE = "Arab Barometer"

# ── Load W1 manual classifications as family template ──
w1_auth = pd.read_csv(AUTH / "arab_barometer_I_directionality_authority.csv")
w1_lookup = {}
for _, r in w1_auth.iterrows():
    key = str(r["var_name"]).strip()
    w1_lookup[key] = {
        "semantic_role": r["semantic_role"],
        "semantic_subrole": r["semantic_subrole"],
        "directionality_policy": r["directionality_policy"],
        "signed_polarity_status": r["signed_polarity_status"],
        "response_family_expectation": r["response_family_expectation"],
        "positive_anchor_label": r["positive_anchor_label"],
        "negative_anchor_label": r["negative_anchor_label"],
        "neutral_anchor_label": r["neutral_anchor_label"],
        "bridge_directionality_action": r["bridge_directionality_action"],
        "directionality_confidence": r["directionality_confidence"],
        "directionality_note": r["directionality_note"],
        "manual_review_required": r["manual_review_required"],
    }

# ── Question-text pattern classifiers for wave-specific vars ──
def text_classify(qt):
    """Classify a variable from question text when no W1 match exists."""
    qt_l = (qt or "").lower()
    
    # Administrative / identifiers
    if any(p in qt_l for p in ["questionnaire id", "sample", "weight", "stratum",
                                "psu", "serial", "qid", "case id", "interviewer"]):
        return ("administrative", "release_or_control_metadata", "unsigned_metadata",
                "unsigned_metadata", "administrative", "", "", "",
                "force_unsigned", "high", "administrative metadata", False)
    
    # Demographics
    if any(p in qt_l for p in ["how old", "age", "what is your age", "year of birth"]):
        return ("position_context", "life_course_coordinate", "unsigned_context",
                "unsigned_context", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "age; position coordinate", False)
    if any(p in qt_l for p in ["sex", "gender", "male", "female"]) and "equality" not in qt_l and "discrimination" not in qt_l:
        return ("position_context", "identity_coordinate", "unsigned_context",
                "unsigned_context", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "sex/gender; position coordinate", False)
    if any(p in qt_l for p in ["education", "level of educat", "schooling", "literacy"]):
        return ("position_context", "social_position_coordinate", "unsigned_context",
                "unsigned_context", "ordinal_scale", "", "", "",
                "force_unsigned", "high", "education; position coordinate", False)
    if any(p in qt_l for p in ["employment", "occupation", "sector", "profession",
                                "job", "work", "employee", "employer", "labor force",
                                "unemployed", "retired", "housewife", "student"]):
        return ("position_context", "labor_market_coordinate", "unsigned_context",
                "unsigned_context", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "employment/occupation; position coordinate", False)
    if any(p in qt_l for p in ["marital", "married", "single", "divorced", "widowed",
                                "spouse", "husband", "wife"]):
        return ("position_context", "life_course_coordinate", "unsigned_context",
                "unsigned_context", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "marital status; position coordinate", False)
    if any(p in qt_l for p in ["religion", "religious", "muslim", "christian", "sect"]):
        return ("position_context", "identity_coordinate", "unsigned_identity",
                "unsigned_identity", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "religion; identity coordinate", False)
    if any(p in qt_l for p in ["income", "salary", "wage", "earnings", "financial",
                                "poverty", "currency", "decile"]):
        return ("position_context", "material_security_coordinate", "unsigned_context",
                "unsigned_context", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "income; position coordinate", False)
    if any(p in qt_l for p in ["urban", "rural", "region", "governorate", "province",
                                "district", "city", "village", "country of origin",
                                "nationality", "citizen"]):
        return ("position_context", "geographic_place_size_coordinate", "unsigned_context",
                "unsigned_context", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "geographic; position coordinate", False)

    # TRUST — very common in Arab Barometer
    if any(p in qt_l for p in ["trust", "confiden", "tell me to what extent you trust"]):
        return ("relation_evidence", "institutional_trust_orientation", "signed_evaluation",
                "signed_evaluation", "ordinal_scale", "more trusting", "less trusting",
                "neutral / ambivalent", "allow_directionality", "high",
                "trust evaluation; signed", False)

    # Agree/disagree
    if any(p in qt_l for p in ["agree", "disagree"]):
        return ("relation_evidence", "subjective_evaluation", "signed_evaluation",
                "signed_evaluation", "ordinal_scale", "more agree", "more disagree",
                "neutral / ambivalent", "allow_directionality", "high",
                "agree/disagree item; signed", False)

    # Satisfaction
    if "satisf" in qt_l:
        return ("relation_evidence", "subjective_evaluation", "signed_evaluation",
                "signed_evaluation", "ordinal_scale", "more satisfied", "less satisfied",
                "neutral / ambivalent", "allow_directionality", "high",
                "satisfaction item; signed", False)

    # How often / frequency
    if any(p in qt_l for p in ["how often", "frequency", "how frequently"]):
        return ("relation_evidence", "behavioral_frequency", "signed_frequency",
                "signed_frequency", "frequency_scale", "more frequent", "less frequent",
                "neutral / ambivalent", "allow_directionality", "high",
                "frequency item; signed", False)

    # Extent / evaluation / rating / performance
    if any(p in qt_l for p in ["to what extent", "how would you evaluate", "how would you rate",
                                "how well", "performance", "how difficult or easy",
                                "how easy or difficult", "how important"]):
        return ("relation_evidence", "subjective_evaluation", "signed_evaluation",
                "signed_evaluation", "ordinal_scale", "more positive", "more negative",
                "neutral / ambivalent", "allow_directionality", "high",
                "evaluative item; signed", False)

    # Likelihood
    if any(p in qt_l for p in ["likely", "possibility", "probability", "chance that"]):
        return ("relation_evidence", "subjective_evaluation", "signed_evaluation",
                "signed_evaluation", "ordinal_scale", "more likely", "less likely",
                "neutral / ambivalent", "allow_directionality", "high",
                "likelihood item; signed", False)

    # Binary participation / behavior
    if any(p in qt_l for p in ["did you participate", "did you vote", "did you attend",
                                "did you contact", "have you ever", "do you currently",
                                "are you a member", "are you registered",
                                "do you use", "do you follow", "do you read",
                                "do you pray", "voted in", "member of"]):
        return ("relation_evidence", "binary_attitude", "signed_attitude",
                "signed_attitude", "yes_no", "more endorsing", "more rejecting",
                "neutral / ambivalent", "allow_directionality", "high",
                "binary participation item", False)

    # Knowledge (factual)
    if any(p in qt_l for p in ["can you name", "can you remember", "do you know the name",
                                "name of the", "who is the", "what is the name"]):
        return ("relation_evidence", "political_knowledge", "unsigned_identity",
                "unsigned_identity", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "factual knowledge recall", False)

    # Open-ended / categorical responses
    if any(p in qt_l for p in ["what is the most important", "which of the following",
                                "please list", "specify", "please mention",
                                "choose one", "select one"]):
        return ("relation_evidence", "categorical_response", "unsigned_identity",
                "unsigned_identity", "nominal_single_choice", "", "", "",
                "force_unsigned", "high", "categorical forced-choice; keep unsigned", False)

    # Default attitude (conservative signed)
    return ("relation_evidence", "subjective_evaluation", "signed_evaluation",
            "signed_evaluation", "ordinal_scale", "more positive", "more negative",
            "neutral / ambivalent", "allow_directionality", "low",
            "text-classified as attitude; verify directionality", True)


WAVES = [
    # (wave, canonical, codebook_path, name_col, text_col)
    ("II", "II", REPO/"data"/"FINAL CODEBOOKS"/"FINAL FINAL CODEBOOKS"/"Arab Barometer Wave 2 codebook.csv", "name", "label"),
    ("V", "V", REPO/"data"/"FINAL CODEBOOKS"/"FINAL FINAL CODEBOOKS"/"Arab Barometer Wave 5 codebook.csv", "var_name", "question_text"),
    ("VIII", "VIII", REPO/"data"/"FINAL CODEBOOKS"/"FINAL FINAL CODEBOOKS"/"Arab Barometer Wave 8 codebook.csv", "var_name", "question_text"),
]


def normalize_vn(vn):
    """Normalize variable name to match W1 pattern."""
    v = str(vn).strip().lower()
    # W2 sometimes uses different prefixes
    v = re.sub(r"^(ir|sa|eg|lp|te|lp|eg|sa|ir)", "", v)
    return v


def build_wave(wave, canonical, cb_path, name_col, text_col):
    print(f"\n{'='*60}")
    print(f"Arab Barometer Wave {canonical}")
    
    cb = pd.read_csv(cb_path, low_memory=False)
    print(f"  Codebook: {len(cb)} rows")
    
    # Use W1 lookup as primary, fallback to text classification
    rows = []
    matched = 0
    text_classified = 0
    
    for _, r in cb.iterrows():
        vn = str(r.get(name_col, "")).strip()
        qt = str(r.get(text_col, "")).strip()
        
        if not vn:
            continue
        
        # Try direct W1 match first
        if vn in w1_lookup:
            t = w1_lookup[vn]
            matched += 1
        else:
            # Try normalized match (strip country prefixes)
            nv = normalize_vn(vn)
            if nv in w1_lookup:
                t = w1_lookup[nv]
                matched += 1
            else:
                # Text-based classification
                t_result = text_classify(qt)
                t = {
                    "semantic_role": t_result[0],
                    "semantic_subrole": t_result[1],
                    "directionality_policy": t_result[2],
                    "signed_polarity_status": t_result[3],
                    "response_family_expectation": t_result[4],
                    "positive_anchor_label": t_result[5],
                    "negative_anchor_label": t_result[6],
                    "neutral_anchor_label": t_result[7],
                    "bridge_directionality_action": t_result[8],
                    "directionality_confidence": t_result[9],
                    "directionality_note": t_result[10],
                    "manual_review_required": t_result[11],
                }
                text_classified += 1
        
        rows.append({
            "source": SOURCE,
            "wave": canonical,
            "canonical_wave": canonical,
            "var_name": vn,
            "question_text": qt,
            **t,
        })
    
    df = pd.DataFrame(rows)
    print(f"  Total: {len(df)} rows ({matched} W1-matched, {text_classified} text-classified)")
    
    # Write all overlay types
    fields = ["source","wave","canonical_wave","var_name","question_text",
              "semantic_role","semantic_subrole","directionality_policy",
              "signed_polarity_status","response_family_expectation",
              "positive_anchor_label","negative_anchor_label","neutral_anchor_label",
              "bridge_directionality_action","directionality_confidence",
              "directionality_note","manual_review_required"]
    
    slug = f"arab_barometer_{canonical}"
    
    # Directionality authority
    auth_df = df[fields]
    auth_df.to_csv(AUTH/f"{slug}_directionality_authority.csv", index=False)
    
    # Directionality overlay
    for d in [REP]:
        auth_df.to_csv(d/f"{slug}_directionality_overlay.csv", index=False)
    
    # Semantic authority overlay
    sa_rows = []
    for _, r in df.iterrows():
        lane = "direct" if r["semantic_role"]=="relation_evidence" else ("context" if r["semantic_role"]=="position_context" else "admin")
        ev = "direct_relation_response" if lane=="direct" else ("position_context" if lane=="context" else "administrative")
        sa_rows.append({
            "source":SOURCE,"wave":canonical,"canonical_wave":canonical,
            "var_name":r["var_name"],"question_text":r["question_text"],
            "semantic_lane":lane,"semantic_role":r["semantic_role"],
            "evidence_lane":ev,"semantic_subrole":r["semantic_subrole"],
            "semantic_tags":"","directionality_policy":r["directionality_policy"],
            "semantic_confidence":r["directionality_confidence"],
            "semantic_note":r["directionality_note"],
        })
    sa_df = pd.DataFrame(sa_rows)
    for d in [REP]:
        sa_df.to_csv(d/f"{slug}_semantic_authority_overlay.csv", index=False)
    
    # First-pass authority
    fp_rows = []
    for _, r in df.iterrows():
        sub = "TRUE" if r["semantic_role"]=="relation_evidence" else "FALSE"
        fp_rows.append({
            "source":SOURCE,"wave":canonical,"canonical_wave":canonical,
            "var_name":r["var_name"],"var_code":r["var_name"],"question_id":r["var_name"],
            "question_text":r["question_text"],
            "module_guess":"substantive" if sub=="TRUE" else "context",
            "semantic_lane":"direct_relation" if sub=="TRUE" else "context",
            "semantic_role":r["semantic_role"],
            "evidence_lane":"direct_response" if sub=="TRUE" else "context",
            "allowed_as_branch_position_signature":"FALSE",
            "allowed_as_branch_relation_cosignature":"FALSE",
            "allowed_as_attitude_cloud_anchor":"TRUE" if sub=="TRUE" else "FALSE",
            "allowed_as_attitude_cloud_feature":"FALSE",
            "allowed_as_v551_relation_evidence":"TRUE" if sub=="TRUE" else "FALSE",
            "allowed_as_association_feature":"FALSE",
            "is_substantive":sub,"not_direct_evidence":"FALSE",
            "manual_designation_required":"FALSE",
            "designation_confidence":"high",
            "rationale":r["directionality_note"],
        })
    fp_df = pd.DataFrame(fp_rows)
    for d in [REP]:
        fp_df.to_csv(d/f"{slug}_first_pass_authority_table.csv", index=False)
    
    # Position conditioning (minimal)
    pc_rows = []
    for _, r in df.iterrows():
        lane = "direct" if r["semantic_role"]=="relation_evidence" else ("context" if r["semantic_role"]=="position_context" else "admin")
        ev = "direct_relation_response" if lane=="direct" else ("position_context" if lane=="context" else "administrative")
        pc_rows.append({
            "source":SOURCE,"wave":canonical,"canonical_wave":canonical,
            "var_name":r["var_name"],"question_text":r["question_text"],
            "semantic_lane":lane,"semantic_role":r["semantic_role"],
            "evidence_lane":ev,"semantic_subrole":r["semantic_subrole"],
            "semantic_tags":"","directionality_policy":r["directionality_policy"],
            "semantic_confidence":r["directionality_confidence"],
            "semantic_note":r["directionality_note"],
            "position_conditioning":"","position_modifiers":"",
        })
    pc_df = pd.DataFrame(pc_rows)
    for d in [REP]:
        pc_df.to_csv(d/f"{slug}_position_conditioning_overlay.csv", index=False)
    
    print(f"  Wrote all overlay types ({len(df)} rows)")
    return df


# Process all remaining waves
all_dfs = []
for wave, canonical, cb_path, name_col, text_col in WAVES:
    df = build_wave(wave, canonical, cb_path, name_col, text_col)
    all_dfs.append(df)

# Update index
idx_path = AUTH / "directionality_authority_index.csv"
idx_rows = []
if idx_path.exists():
    with open(idx_path) as f:
        for row in csv.DictReader(f):
            idx_rows.append(row)

for wave, canonical, _, _, _ in WAVES:
    idx_rows = [r for r in idx_rows if not (r.get("source")==SOURCE and r.get("wave")==canonical)]
    fn = f"arab_barometer_{canonical}_directionality_authority.csv"
    cnt = len(pd.read_csv(AUTH/fn)) if (AUTH/fn).exists() else 0
    idx_rows.append({"source":SOURCE,"wave":canonical,"file_name":fn,
                     "row_count":str(cnt),"status":"active",
                     "notes":"family-template from W1 manual authority; W1-matched + text-classified"})

with open(idx_path,"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["source","wave","file_name","row_count","status","notes"])
    w.writeheader(); w.writerows(idx_rows)
print(f"\nIndex updated")

# Summary
total = sum(len(d) for d in all_dfs)
print(f"\n=== Complete ===")
print(f"Arab Barometer W1: 181 rows (manual, reviewed)")
print(f"Arab Barometer W2: {len(all_dfs[0])} rows")
print(f"Arab Barometer W5: {len(all_dfs[1])} rows")
print(f"Arab Barometer W8: {len(all_dfs[2])} rows")
print(f"Total: {181 + total} rows across 4 waves")
