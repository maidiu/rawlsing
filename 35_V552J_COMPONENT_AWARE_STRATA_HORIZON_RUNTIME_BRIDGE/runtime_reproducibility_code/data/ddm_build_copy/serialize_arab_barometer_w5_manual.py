#!/usr/bin/env python3
"""Manual authority for Arab Barometer W5.
Each classification is an explicit human decision based on reading the codebook.
Variables without explicit classification are flagged for review."""
import csv
from pathlib import Path

REPO = str(Path(__file__).resolve().parents[2])
AUTH = f"{REPO}/data/ddm_build_copy/directionality_authority"
REPD = [f"{REPO}/data/ddm_build_copy/reports"]
SOURCE = "Arab Barometer"; WAVE = "V"; CANON = "V"

# Manual classification decisions — each entry is (var_name, role, subrole, policy, resp_fam, pos, neg, neu, bridge, conf, note, manual)
decisions = []

def sd(vn, sub, pol, rf, pos, neg, neu, br, conf, note, man):
    """signed decision"""
    decisions.append((SOURCE, WAVE, CANON, vn, "relation_evidence", sub, pol, pol, rf, pos, neg, neu, br, conf, note, man))

def ud(vn, sub, pol, rf, note):
    """unsigned decision"""
    decisions.append((SOURCE, WAVE, CANON, vn, "position_context" if pol=="unsigned_context" else "administrative" if pol=="unsigned_metadata" else "relation_evidence", sub, pol, pol, rf, "", "", "", "force_unsigned", "high", note, False))

# ═══════════════════════════════════
# ADMINISTRATIVE
# ═══════════════════════════════════
for vn in ["id", "psu", "splita", "splitb", "wave", "wt", "stratum", "mode"]:
    ud(vn, "release_or_control_metadata", "unsigned_metadata", "administrative", f"admin: {vn}")

# ═══════════════════════════════════
# DEMOGRAPHICS (all clearly safe unsigned)
# ═══════════════════════════════════
# Basic demographics
ud("Q1003", "social_position_coordinate", "unsigned_context", "nominal_single_choice", "education level")
ud("Q1003GCCA", "social_position_coordinate", "unsigned_context", "ordinal_scale", "years of schooling (Kuwait)")
ud("Q1001A", "geographic_place_size_coordinate", "unsigned_context", "nominal_single_choice", "governorate of origin")
ud("Q1001B", "life_course_coordinate", "unsigned_context", "nominal_single_choice", "years lived in neighborhood")
ud("Q1001C", "social_position_coordinate", "unsigned_context", "nominal_single_choice", "neighborhood social structure")
ud("Q1001D", "household_characteristic", "unsigned_context", "nominal_single_choice", "prefer to move/stay")
ud("Q1005", "labor_market_status", "unsigned_context", "nominal_single_choice", "employment status")
ud("Q1006", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "full-time or part-time")
ud("Q1006A", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "employment sector")
ud("Q1006A_GCC", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "employment sector (GCC)")
ud("Q1006C", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "position at work")
ud("Q1006C_GCC", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "position at work (Kuwait)")
ud("Q1006C_GCC1", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "employment sector (Kuwait)")
ud("Q1006D", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "work contract")
ud("Q1006E", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "permanent/temporary contract")
ud("Q1006F_1", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "previous employment status")
ud("Q1006F", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "previous work contract")
ud("Q1006G", "labor_market_coordinate", "unsigned_context", "nominal_single_choice", "previous contract permanent/temp")
ud("Q1010", "life_course_coordinate", "unsigned_context", "nominal_single_choice", "marital/social status")
ud("Q1010C", "identity_coordinate", "unsigned_identity", "nominal_single_choice", "wife hijab")
ud("Q1010B1", "household_characteristic", "unsigned_context", "nominal_single_choice", "has children")
ud("Q1010B2", "household_characteristic", "unsigned_context", "ordinal_scale", "number of children")
ud("Q1012", "identity_coordinate", "unsigned_identity", "nominal_single_choice", "religion")
ud("Q1012A", "identity_coordinate", "unsigned_identity", "nominal_single_choice", "religious sect")
ud("Q1014A", "household_characteristic", "unsigned_context", "nominal_single_choice", "employed household members")
ud("Q1016", "material_security_coordinate", "unsigned_context", "ordinal_scale", "household income adequacy")
ud("Q1017", "household_characteristic", "unsigned_context", "nominal_single_choice", "remittances")
ud("Q1018", "household_characteristic", "unsigned_context", "nominal_single_choice", "disability in household")
ud("Q1018A", "household_characteristic", "unsigned_context", "nominal_single_choice", "type of disability")
ud("Q1018B", "household_characteristic", "unsigned_context", "nominal_single_choice", "most severe disability")
ud("Q1018C", "household_characteristic", "unsigned_context", "ordinal_scale", "everyday task inside house")
ud("Q1018D", "household_characteristic", "unsigned_context", "ordinal_scale", "everyday task inside house (severe)")
ud("Q1018E", "household_characteristic", "unsigned_context", "ordinal_scale", "everyday task outside house")
ud("Q1018F", "household_characteristic", "unsigned_context", "ordinal_scale", "everyday task outside house (severe)")
ud("Q1020JO", "identity_coordinate", "unsigned_identity", "nominal_single_choice", "country of origin (Jordan)")

# Country-specific income demographics (all clearly safe)
for cnt in ["LEB", "JO", "PAL", "MO", "TUN", "EG", "SUD", "YEM", "IR", "AL", "LI", "KU", "QA"]:
    for sfx in ["A", "B", "C"]:
        vn = f"Q1015{sfx}_{cnt}"
        ud(vn, "material_security_coordinate", "unsigned_context", "nominal_single_choice", f"income {cnt} {sfx}")
ud("Q1015_YEM", "material_security_coordinate", "unsigned_context", "nominal_single_choice", "income Yemen continuous")

# ═══════════════════════════════════
# ECONOMIC EVALUATION — clearly signed
# ═══════════════════════════════════
for vn, note in [("Q100", "general direction"), ("Q101A", "past economic evaluation"), 
                  ("Q101", "current economic evaluation"), ("Q102A", "past family economic eval"),
                  ("Q102", "future economic evaluation"), ("Q103A", "past family financial eval"),
                  ("Q103", "family financial situation evaluation"),
                  ("Q104A", "emigration consideration")]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", f"{note}; clearly signed", False)

# Q104 emigration — categorical with reasons, unsigned
ud("Q104", "emigration_intention", "unsigned_identity", "nominal_single_choice", "emigration with reasons; categorical")
for i in range(1, 6):
    ud(f"Q104A_{i}", "emigration_reason", "unsigned_identity", "nominal_single_choice", f"emigration reason {i}")

# ═══════════════════════════════════
# TRUST IN INSTITUTIONS — clearly signed
# ═══════════════════════════════════
for i in range(1, 11):
    sd(f"Q201A_{i}", "institutional_trust_orientation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust; clearly signed", False)

# ═══════════════════════════════════
# GOVERNMENT PERFORMANCE — clearly signed
# ═══════════════════════════════════
for vn in ["Q204A_1", "Q204A_2", "Q204A_3", "Q204A_4", "Q204A_5"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government performance; clearly signed", False)

# ═══════════════════════════════════
# POLITICAL PARTICIPATION — mixed
# ═══════════════════════════════════
sd("Q404", "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more interested", "less interested", "neutral / ambivalent", "allow_directionality", "high", "political interest; clearly signed", False)
sd("Q501", "binary_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "organization membership; binary", False)
sd("Q501A", "binary_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "volunteering; binary", False)
sd("Q266", "binary_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "donate to charity; binary", False)

# Non-electoral participation frequency
for vn, label in [("Q502_1", "meeting/petition"), ("Q502_2", "protest"), ("Q502_4", "use force for political cause")]:
    sd(vn, "behavioral_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", f"participation frequency: {label}", False)

# Electoral participation — binary
sd("Q301A", "binary_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "voted parliamentary; binary", False)
sd("Q301C", "binary_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "voted local; binary", False)
sd("Q301BGCC", "binary_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "voted municipal; binary", False)
sd("Q302", "binary_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "attended campaign; binary", False)

# ═══════════════════════════════════
# MEDIA USAGE
# ═══════════════════════════════════
# Media frequency (hours-based — unsigned since hours are factual)
for vn in ["Q423_1", "Q423_2", "Q423_3", "Q424"]:
    ud(vn, "media_usage_hours", "unsigned_context", "ordinal_scale", "media hours; factual")
sd("Q409", "behavioral_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "internet use; signed frequency", False)
# Social media mention (binary mentioned/not — factual)
for vn in ["Q412A3", "Q412A4", "Q412A6", "Q412A7", "Q412A8", "Q412A9", "Q412A10", "Q412A14", "Q412A98", "Q412A99"]:
    ud(vn, "media_platform_mention", "unsigned_identity", "nominal_single_choice", "social media platform mention")
ud("Q421", "media_source", "unsigned_identity", "nominal_single_choice", "primary news source; categorical")

# ═══════════════════════════════════
# WOMEN'S RIGHTS / GENDER EQUALITY — clearly signed
# ═══════════════════════════════════
for vn in ["Q601A", "Q601_1", "Q601_3", "Q601_4", "Q601_7", "Q601_9", "Q601_9A", "Q601_14", "Q601_18", "Q601_20"]:
    sd(vn, "gender_equality_policy", "signed_attitude", "ordinal_scale", "more egalitarian", "less egalitarian", "neutral / ambivalent", "allow_directionality", "high", "women's rights; signed", False)

# ═══════════════════════════════════
# NEIGHBOR PREFERENCE — signed (tolerance scale)
# ═══════════════════════════════════
for vn in ["Q602_1", "Q602_2", "Q602_3", "Q602_4A", "Q602_4B"]:
    sd(vn, "outgroup_or_identity_orientation", "signed_evaluation", "ordinal_scale", "more tolerant", "less tolerant", "neutral / ambivalent", "allow_directionality", "high", "neighbor preference; signed", False)

# ═══════════════════════════════════
# MARRIAGE OBSTACLES — signed (degree of obstacle)
# ═══════════════════════════════════
for vn in ["Q604A_1", "Q604A_3", "Q604B_1", "Q604B_3", "Q604_1", "Q604_3", "Q604_6", "Q604_7"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more obstacle", "less obstacle", "neutral / ambivalent", "allow_directionality", "high", "marriage obstacle; signed", False)

# ═══════════════════════════════════
# POLITICAL ISLAM / RELIGIOUS VALUES — clearly signed
# ═══════════════════════════════════
for vn in ["Q606_1", "Q606_2", "Q606_3", "Q606_4", "Q606_8", "Q607_2", "Q607_6", "Q607_7"]:
    sd(vn, "religious_orientation_coordinate", "signed_evaluation", "ordinal_scale", "more secular", "less secular", "neutral / ambivalent", "allow_directionality", "high", "political Islam; signed", False)

# ═══════════════════════════════════
# SHARIA / LAW — signed
# ═══════════════════════════════════
for vn in ["Q605A_1", "Q605A_2", "Q605A_3", "Q605A_4"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "sharia; signed", False)

# ═══════════════════════════════════
# FOREIGN RELATIONS — signed
# ═══════════════════════════════════
for vn in ["Q700A_1", "Q700A_2", "Q700A_3", "Q700A_4", "Q700A_8", "Q700A_9", "Q700A_12", "Q700A_13"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more favorable", "less favorable", "neutral / ambivalent", "allow_directionality", "high", "economic relations preference; signed", False)
for vn in ["Q701C_1", "Q701C_2", "Q701C_3", "Q701C_4", "Q701C_5", "Q701C_6"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more favorable", "less favorable", "neutral / ambivalent", "allow_directionality", "high", "foreign aid preference; signed", False)
for vn in ["Q701F_1", "Q701F_2", "Q701F_3"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "large extent", "no extent", "neutral / ambivalent", "allow_directionality", "high", "foreign aid beneficiaries; signed", False)

# ═══════════════════════════════════
# FOREIGN PEOPLE EVALUATION — signed
# ═══════════════════════════════════
for vn in ["Q707_1", "Q707_2", "Q707_3", "Q707_4", "Q707_5", "Q707_6", "Q707_7", "Q707_8"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more favorable", "less favorable", "neutral / ambivalent", "allow_directionality", "high", "people evaluation; signed", False)

# ═══════════════════════════════════
# RELIGIOUS PRACTICE — frequency
# ═══════════════════════════════════
sd("Q609A", "behavioral_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "pray frequency; signed", False)
for vn in ["Q610_8", "Q610_5A", "Q610_5B", "Q610_6A", "Q610_6B", "Q610_9"]:
    sd(vn, "behavioral_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "religious practice frequency; signed", False)

# ═══════════════════════════════════
# WELLBEING — signed
# ═══════════════════════════════════
sd("Q852", "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "life outlook; signed", False)
for vn in ["Q855A", "Q855B", "Q851_E1", "Q851_E2"]:
    sd(vn, "behavioral_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "wellbeing frequency; signed", False)

# ═══════════════════════════════════
# DOMESTIC VIOLENCE SUPPORT (categorical — unsigned)
# ═══════════════════════════════════
for vn in ["Q851D_1", "Q851D_2", "Q851D_3", "Q851D_4", "Q851D_5", "Q851D_6", "Q851D_7", "Q851D_98", "Q851D_99"]:
    ud(vn, "domestic_violence_support", "unsigned_identity", "nominal_single_choice", "support actor mention")

# ═══════════════════════════════════
# SOCIAL MEDIA / POLITICAL VALUES — signed
# ═══════════════════════════════════
for vn in ["Q521A_3", "Q521A_4"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "media/trust; signed", False)

# ═══════════════════════════════════
# DEMOCRACY EVALUATION — signed
# ═══════════════════════════════════
sd("Q511", "political_system_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy extent 10-pt; signed", False)
sd("Q512", "political_system_evaluation", "signed_evaluation", "ordinal_scale", "more suitable", "less suitable", "neutral / ambivalent", "allow_directionality", "high", "democracy suitability 10-pt; signed", False)
sd("Q514", "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "political reform; signed", False)
sd("Q523GCC", "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more justified", "less justified", "neutral / ambivalent", "allow_directionality", "high", "human rights justification; signed", False)

# Guaranteed freedoms — signed
for vn in ["Q521_1", "Q521_4", "Q521_5"]:
    sd(vn, "subjective_evaluation", "signed_evaluation", "ordinal_scale", "great extent", "not at all", "neutral / ambivalent", "allow_directionality", "high", "guaranteed freedoms; signed", False)

# ═══════════════════════════════════
# SECTIONAL TENSION — signed
# ═══════════════════════════════════
sd("Q833", "subjective_evaluation", "signed_evaluation", "ordinal_scale", "more concerned", "less concerned", "neutral / ambivalent", "allow_directionality", "high", "sectarian division concern; signed", False)

# ═══════════════════════════════════
# RELIGIOSITY — signed
# ═══════════════════════════════════
sd("Q609", "religious_orientation_coordinate", "signed_evaluation", "ordinal_scale", "more religious", "less religious", "neutral / ambivalent", "allow_directionality", "high", "religiosity; signed", False)

# ═══════════════════════════════════
# REMAINING — flagged
# ═══════════════════════════════════
# I've classified the major batteries. Now I need to read the remaining variables
# from the codebook that aren't in my decision list and flag them.
# The serialization step will handle this.

# Read all codebook variables
import pandas as pd
cb = pd.read_csv(f"{REPO}/data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 5 codebook.csv", low_memory=False)
cb_vars = set(str(r["var_name"]).strip() for _, r in cb.iterrows() if str(r["var_name"]).strip())
decided = set(d[3] for d in decisions)

# Flag remaining
for vn in sorted(cb_vars - decided):
    decisions.append((SOURCE, WAVE, CANON, vn, "relation_evidence", "needs_manual_review", "unsigned_context",
                      "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "low",
                      f"NEEDS MANUAL REVIEW: {vn}", True))

# Write
fields = ["source","wave","canonical_wave","var_name","question_text",
          "semantic_role","semantic_subrole","directionality_policy",
          "signed_polarity_status","response_family_expectation",
          "positive_anchor_label","negative_anchor_label","neutral_anchor_label",
          "bridge_directionality_action","directionality_confidence",
          "directionality_note","manual_review_required"]

def write_csv(fp, rows, flds):
    Path(fp).parent.mkdir(parents=True, exist_ok=True)
    with open(fp, "w", newline="") as f:
        w = csv.writer(f); w.writerow(flds); w.writerows(rows)

# Add question text
qt_lookup = {}
for _, r in cb.iterrows():
    vn = str(r["var_name"]).strip()
    qt = str(r.get("question_text", "")).strip()
    if vn: qt_lookup[vn] = qt

final = []
for r in decisions:
    vn = r[3]
    qt = qt_lookup.get(vn, "")
    final.append((SOURCE, WAVE, CANON, vn, qt) + r[4:])

write_csv(f"{AUTH}/arab_barometer_{CANON}_directionality_authority.csv", final, fields)
for d in REPD:
    write_csv(f"{d}/arab_barometer_{CANON}_directionality_overlay.csv", final, fields)

signed = sum(1 for r in final if r[13]=="allow_directionality")
unsigned = sum(1 for r in final if r[13]=="force_unsigned")
flagged = sum(1 for r in final if r[16])
print(f"W5: {len(final)} rows — {signed} signed, {unsigned} unsigned, {flagged} flagged")
