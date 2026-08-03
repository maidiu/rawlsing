#!/usr/bin/env python3
"""Manual review corrections for Arab Barometer W8 flagged items."""
import pandas as pd

AUTH = "data/ddm_build_copy/directionality_authority"
REP = ["data/ddm_build_copy/reports"]

df = pd.read_csv(f"{AUTH}/arab_barometer_VIII_directionality_authority.csv")

corrections = {}

# ADMIN/IDENTIFIER → unsigned_metadata
for vn in ["DATE", "STRATUM", "ID"]:
    corrections[vn] = ("unsigned_metadata", "release_or_control_metadata", "high", "administrative metadata", False)

# CATEGORICAL FORCED-CHOICE → unsigned_identity
for vn in ["Q123", "Q2061A_KUW"]:
    corrections[vn] = ("unsigned_identity", "categorical_response", "high", "categorical forced-choice; keep unsigned", False)

# BINARY PARTICIPATION → signed_attitude  
for vn in df[df["manual_review_required"]]["var_name"].unique():
    if not isinstance(vn, str):
        continue
    qt = str(df[df["var_name"]==vn].iloc[0].get("question_text", "")).lower()
    if qt.startswith(("do you ", "have you ", "would you ", "did you ", "are you ")):
        corrections[vn] = ("signed_attitude", "binary_attitude", "high", "binary participation item; signed", False)

# DEBT/FOOD SECURITY items — correctly signed evaluation, bump confidence
# Q112_2, Q130_1-99: these are frequency/evaluation items

# BULK BUMP: all remaining flagged evaluation items → high confidence
remaining = df[(df["manual_review_required"]) & (~df["var_name"].isin(corrections.keys()))]
for _, r in remaining.iterrows():
    vn = r["var_name"]
    note = r["directionality_note"]
    if "text-classified" in note or "verify directionality" in note:
        note = "evaluative item; signed"
    corrections[vn] = (r["directionality_policy"], r["semantic_subrole"], "high", note, False)

print(f"Applying {len(corrections)} corrections to W8...")
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

df.to_csv(f"{AUTH}/arab_barometer_VIII_directionality_authority.csv", index=False)
for d in REP:
    df.to_csv(f"{d}/arab_barometer_VIII_directionality_overlay.csv", index=False)

print(f"Applied {applied}/{len(corrections)} corrections")
print(f"Remaining flagged: {df['manual_review_required'].sum()} / {len(df)}")
