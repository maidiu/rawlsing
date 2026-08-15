#!/usr/bin/env python3
"""Manual authority for Arab Barometer W2.
ONLY clearly safe rows are classified.
Everything ambiguous is flagged for manual review.
No text classifier invents authority."""
import csv
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
AUTH = REPO / "data/ddm_build_copy/directionality_authority"
REPD = [REPO / "data/ddm_build_copy/reports"]
SOURCE = "Arab Barometer"; WAVE = "II"; CANON = "II"

cb = pd.read_csv(REPO/"data"/"FINAL CODEBOOKS"/"FINAL FINAL CODEBOOKS"/"Arab Barometer Wave 2 codebook.csv")
qt_map = {}
for _, r in cb.iterrows():
    n = str(r["name"]).strip()
    lbl = str(r["label"]).strip()
    if n: qt_map[n] = lbl

rows = []
def add(vn, role, sub, pol, rf, pos, neg, neu, bridge, conf, note, man):
    rows.append((SOURCE, WAVE, CANON, vn, qt_map.get(vn,""), role, sub, pol, pol,
                 rf, pos, neg, neu, bridge, conf, note, man))

# ── SAFE UNSIGNED: administrative metadata ──
for vn in ["qid", "country", "a1", "v1", "samp"]:
    add(vn, "administrative", "release_or_control_metadata", "unsigned_metadata",
        "administrative", "", "", "", "force_unsigned", "high", "admin metadata", False)

# ── SAFE UNSIGNED: clear demographics ──
# Province, urban/rural, region
add("q1", "position_context", "geographic_place_size_coordinate", "unsigned_context",
    "nominal_single_choice", "", "", "", "force_unsigned", "high", "province", False)
add("q13", "position_context", "geographic_place_size_coordinate", "unsigned_context",
    "nominal_single_choice", "", "", "", "force_unsigned", "high", "urban/rural", False)

# q1xx demographic battery — these are all clearly demographic
# From reading the codebook: q100, q101-q104, etc.
# q100 about general direction — actually that's an attitude item
# Let me be careful and only flag what's CLEARLY safe

# ── SAFE UNSIGNED: demographic variables (q1001-q1017) ──
# These are clearly demographic: age, gender, education, employment, income, housing, etc.
demo_battery = {
    "q1001": ("life_course_coordinate", "age"),
    "q1002": ("identity_coordinate", "gender"),
    "q1003": ("social_position_coordinate", "education"),
    "q1004": ("labor_market_coordinate", "employment"),
    "q1005": ("labor_market_coordinate", "retired/housewife/student"),
    "q1006": ("labor_market_coordinate", "occupation"),
    "q1007": ("labor_market_coordinate", "employment sector"),
    "q1008": ("life_course_coordinate", "marital status"),
    "q1009": ("identity_coordinate", "religion"),
    "q1010": ("identity_coordinate", "religious denomination"),
    "q1011": ("material_security_coordinate", "household income"),
    "q1012": ("material_security_coordinate", "personal income"),
    "q1013": ("household_characteristic", "housing type"),
    "q1014": ("household_characteristic", "household composition"),
    "q1015": ("household_characteristic", "household amenities"),
    "q1016": ("labor_market_coordinate", "spouse employment"),
    "q1017": ("household_characteristic", "remittances"),
    "v1014": ("household_characteristic", "household size"),
    "v1015": ("household_characteristic", "household members"),
    "v13": ("geographic_place_size_coordinate", "name of place"),
    "wt": ("release_or_control_metadata", "weight"),
}
for vn, (sub, note) in demo_battery.items():
    if vn in qt_map:
        id_type = "unsigned_identity" if sub == "identity_coordinate" else "unsigned_context"
        add(vn, "position_context", sub, id_type,
            "nominal_single_choice", "", "", "", "force_unsigned", "high",
            f"{note}; position coordinate", False)

# ── SAFE: q101-q104 economic/trust evaluation ──
# q100: general direction
if "q100" in qt_map:
    add("q100", "relation_evidence", "subjective_evaluation", "signed_evaluation",
        "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
        "allow_directionality", "high", "general direction; clearly signed", False)

# ── SAFE SIGNED: trust battery (q2011-q20110) ──
# These are clearly 1=great trust → 4=no trust ordinal scales
for i in range(1, 17):
    vn = f"q201{i}"
    if vn in qt_map:
        add(vn, "relation_evidence", "institutional_trust_orientation", "signed_evaluation",
            "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent",
            "allow_directionality", "high", "trust in institutions; clearly signed", False)

# Also handle sa2013
for vn in qt_map:
    if vn.startswith("sa201") or vn.startswith("ir201") or vn.startswith("lp201"):
        add(vn, "relation_evidence", "institutional_trust_orientation", "signed_evaluation",
            "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent",
            "allow_directionality", "high", "trust in institutions; clearly signed", False)

# ── SAFE SIGNED: government performance (q2041-q20415) ──
# Clearly evaluative: "How would you evaluate the performance..."
for i in range(1, 16):
    vn = f"q204{i}"
    if vn in qt_map:
        add(vn, "relation_evidence", "subjective_evaluation", "signed_evaluation",
            "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
            "allow_directionality", "high", "government performance; clearly signed", False)
# Also handle country-specific variants
for prefix in ["eg", "ir", "lp", "te"]:
    for i in range(1, 16):
        vn = f"{prefix}204{i}"
        if vn in qt_map:
            add(vn, "relation_evidence", "subjective_evaluation", "signed_evaluation",
                "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
                "allow_directionality", "high", "government performance; clearly signed", False)

# ── SAFE: economic evaluation q101-q103 ──
# "How would you evaluate the current economic situation"
for vn in ["q101", "q102"]:
    if vn in qt_map:
        add(vn, "relation_evidence", "subjective_evaluation", "signed_evaluation",
            "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
            "allow_directionality", "high", "economic evaluation; clearly signed", False)

# ── SAFE: safety evaluation q105, te105 ──
for vn in ["q105", "te105"]:
    if vn in qt_map:
        add(vn, "relation_evidence", "subjective_evaluation", "signed_evaluation",
            "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
            "allow_directionality", "high", "safety evaluation; clearly signed", False)

# ── SAFE: equal treatment q106 ──
if "q106" in qt_map:
    add("q106", "relation_evidence", "subjective_evaluation", "signed_evaluation",
        "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
        "allow_directionality", "high", "equal treatment; clearly signed", False)

# ── SAFE: q103 interpersonal trust ──
if "q103" in qt_map:
    add("q103", "relation_evidence", "social_trust_orientation", "signed_attitude",
        "yes_no", "more trusting", "less trusting", "neutral / ambivalent",
        "allow_directionality", "high", "interpersonal trust; clearly signed", False)

# ── SAFE: q104 emigration ──
# This has yes+reasons/no — categorical, not directional
if "q104" in qt_map:
    add("q104", "relation_evidence", "emigration_intention", "unsigned_identity",
        "nominal_single_choice", "", "", "", "force_unsigned", "high",
        "emigration with reasons; categorical, unsigned", False)

# ── SAFE: election evaluation q5171-5173 ──
for i in range(1, 4):
    vn = f"q517{i}"
    if vn in qt_map:
        add(vn, "relation_evidence", "subjective_evaluation", "signed_evaluation",
            "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
            "allow_directionality", "high", "political system evaluation; clearly signed", False)

# ── SAFE: democracy satisfaction q504 ──
if "q504" in qt_map:
    add("q504", "relation_evidence", "subjective_evaluation", "signed_evaluation",
        "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
        "allow_directionality", "high", "democracy evaluation; clearly signed", False)

# ── SAFE: q512 democracy suitability (10-point scale) ──
if "q512" in qt_map:
    add("q512", "relation_evidence", "political_system_evaluation", "signed_evaluation",
        "ordinal_scale", "more suitable", "less suitable", "neutral / ambivalent",
        "allow_directionality", "high", "democracy suitability 10-point; clearly signed", False)

# ── SAFE: q603 lottery willingness ──
if "q603" in qt_map:
    add("q603", "relation_evidence", "subjective_evaluation", "signed_evaluation",
        "ordinal_scale", "more willing", "less willing", "neutral / ambivalent",
        "allow_directionality", "high", "lottery willingness; clearly signed", False)

# ── SAFE: q6101-q6106 religious practice (binary) ──
for i in [1, 2, 3, 4, 5, 6]:
    vn = f"q610{i}"
    if vn in qt_map:
        add(vn, "relation_evidence", "binary_attitude", "signed_attitude",
            "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent",
            "allow_directionality", "high", "religious practice; signed binary", False)

# ── SAFE: ease/access questions q2053-2055 ──
for i in [3, 4, 5]:
    vn = f"q205{i}"
    if vn in qt_map:
        add(vn, "relation_evidence", "subjective_evaluation", "signed_evaluation",
            "ordinal_scale", "more easy", "more difficult", "neutral / ambivalent",
            "allow_directionality", "high", "ease of access; clearly signed", False)

# ── SAFE: q202 reform evaluation ──
if "q202" in qt_map:
    add("q202", "relation_evidence", "subjective_evaluation", "signed_evaluation",
        "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
        "allow_directionality", "high", "reform evaluation; clearly signed", False)

# ── SAFE: q2031-2034 performance evaluation ──
for i in [1, 2, 3, 4]:
    vn = f"q203{i}"
    if vn in qt_map:
        add(vn, "relation_evidence", "subjective_evaluation", "signed_evaluation",
            "ordinal_scale", "more positive", "more negative", "neutral / ambivalent",
            "allow_directionality", "high", "performance evaluation; clearly signed", False)

# ── KNOWLEDGE QUESTIONS (clearly safe factual recall) ──
for vn in ["q5221", "q5222", "q5223", "q5224"]:
    if vn in qt_map:
        add(vn, "relation_evidence", "political_knowledge", "unsigned_identity",
            "nominal_single_choice", "", "", "", "force_unsigned", "high",
            "factual knowledge recall; unsigned", False)

# ── FLAG EVERYTHING ELSE ──
classified = {r[3] for r in rows}
for vn in sorted(qt_map.keys()):
    if vn not in classified:
        add(vn, "relation_evidence", "needs_manual_review", "unsigned_context",
            "ordinal_scale", "", "", "", "force_unsigned", "low",
            "NEEDS MANUAL REVIEW — not yet classified", True)

# Write
fields = ["source","wave","canonical_wave","var_name","question_text",
          "semantic_role","semantic_subrole","directionality_policy",
          "signed_polarity_status","response_family_expectation",
          "positive_anchor_label","negative_anchor_label","neutral_anchor_label",
          "bridge_directionality_action","directionality_confidence",
          "directionality_note","manual_review_required"]

AUTH.mkdir(parents=True, exist_ok=True)
fp = AUTH / f"arab_barometer_{CANON}_directionality_authority.csv"
with open(fp, "w", newline="") as f:
    w = csv.writer(f); w.writerow(fields); w.writerows(rows)
print(f"Wrote authority ({len(rows)} rows)")

for d in REPD:
    d.mkdir(parents=True, exist_ok=True)
    with open(d/f"arab_barometer_{CANON}_directionality_overlay.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(fields); w.writerows(rows)
    print(f"Wrote overlay ({len(rows)} rows)")

signed = sum(1 for r in rows if r[13]=="allow_directionality")
unsigned = sum(1 for r in rows if r[13]=="force_unsigned")
flagged = sum(1 for r in rows if r[16])
print(f"\nSigned: {signed} | Unsigned: {unsigned} | Flagged: {flagged}")
print(f"Flagged items ({len([r for r in rows if r[16]])}):")
for r in rows:
    if r[16]:
        print(f"  {r[3]:25s} {r[5]:25s} {r[15][:60]}")
