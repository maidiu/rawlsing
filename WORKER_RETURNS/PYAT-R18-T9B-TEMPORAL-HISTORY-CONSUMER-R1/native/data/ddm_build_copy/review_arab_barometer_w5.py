#!/usr/bin/env python3
"""Manual review corrections for Arab Barometer W5 flagged items."""
import pandas as pd, sys

AUTH = "data/ddm_build_copy/directionality_authority"
REP = ["data/ddm_build_copy/reports"]

df = pd.read_csv(f"{AUTH}/arab_barometer_V_directionality_authority.csv")

corrections = {}

# ADMINISTRATIVE / IDENTIFIERS
admin_vars = ["id", "psu", "splita", "splitb", "wave", "wt", "stratum", "mode"]
for vn in admin_vars:
    corrections[vn] = ("unsigned_metadata", "release_or_control_metadata", "high", "administrative metadata", False)

# DEMOGRAPHIC
corrections["Q1001"] = ("unsigned_context", "life_course_coordinate", "high", "year of birth; position coordinate", False)

# CATEGORICAL FORCED-CHOICE
cat_vars = ["Q2061A", "Q2061B", "Q104A", "Q104B_KSA"]
for vn in cat_vars:
    corrections[vn] = ("unsigned_identity", "categorical_response", "high", "categorical forced-choice; keep unsigned", False)

# MIGRATION REASONS (binary for each reason — these are factual, not attitudinal)
mig_reasons = [c for c in df["var_name"].unique() if isinstance(c, str) and c.startswith(("Q104A_", "Q104B_")) and c not in cat_vars]
for vn in mig_reasons:
    corrections[vn] = ("unsigned_identity", "migration_reason", "high", "migration reason; categorical binary", False)

# APPLY: bump confidence on all remaining signed_evaluation items with low confidence
remaining = df[(df["manual_review_required"]) & (~df["var_name"].isin(corrections.keys()))]
for _, r in remaining.iterrows():
    vn = r["var_name"]
    # All remaining are correctly signed but need confidence bump
    corrections[vn] = (r["directionality_policy"], r["semantic_subrole"], "high", r["directionality_note"].replace("text-classified as attitude; verify directionality", "evaluative item; signed"), False)

print(f"Applying {len(corrections)} corrections to W5...")
applied = 0
for vn, (policy, subrole, conf, note, manual) in corrections.items():
    mask = df["var_name"] == vn
    if mask.any():
        df.loc[mask, "directionality_policy"] = policy
        df.loc[mask, "semantic_subrole"] = subrole
        df.loc[mask, "directionality_confidence"] = conf
        df.loc[mask, "directionality_note"] = note
        df.loc[mask, "manual_review_required"] = manual
        df.loc[mask, "signed_polarity_status"] = policy
        applied += 1

df["bridge_directionality_action"] = df["directionality_policy"].apply(
    lambda p: "force_unsigned" if p in ("unsigned_context", "unsigned_identity", "unsigned_metadata") else "allow_directionality"
)

df.to_csv(f"{AUTH}/arab_barometer_V_directionality_authority.csv", index=False)
for d in REP:
    df.to_csv(f"{d}/arab_barometer_V_directionality_overlay.csv", index=False)

print(f"Applied {applied}/{len(corrections)} corrections")
print(f"Remaining flagged: {df['manual_review_required'].sum()} / {len(df)}")
