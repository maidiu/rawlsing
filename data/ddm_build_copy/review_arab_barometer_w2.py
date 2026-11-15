#!/usr/bin/env python3
"""Manual review corrections for Arab Barometer W2 flagged items."""
import pandas as pd
from pathlib import Path

REPO = str(Path(__file__).resolve().parents[2])
AUTH = f"{REPO}/data/ddm_build_copy/directionality_authority"
REP = f"{REPO}/data/ddm_build_copy/reports"
REP2 = f"{REPO}/data/ddm_build_copy/reports"

# W2 corrections — review each flagged item
# (var_name, new_policy, new_subrole, new_confidence, new_note, new_manual)
corrections_w2 = {
    # DEMOGRAPHIC / ADMIN — should be unsigned
    "v13": ("unsigned_context", "geographic_place_size_coordinate", "high", "name of place; position coordinate", False),
    "q1005": ("unsigned_context", "demographic_status", "high", "respondent status; position coordinate", False),
    "sa1012": ("unsigned_identity", "identity_coordinate", "high", "religious denomination; identity coordinate", False),
    "q1013": ("unsigned_context", "household_characteristic", "high", "housing type; position coordinate", False),
    "q1017": ("unsigned_context", "household_characteristic", "high", "remittances; household characteristic", False),
    
    # CATEGORICAL FORCED-CHOICE — should be unsigned_identity
    "q104": ("unsigned_identity", "emigration_intention", "high", "emigration consideration; categorical with reason split", False),
    "q2062": ("unsigned_identity", "civic_priority", "high", "second most important challenge; categorical", False),
    "eg305": ("unsigned_identity", "civic_priority", "high", "most important factor; categorical", False),
    "sa305": ("unsigned_identity", "civic_priority", "high", "most important factor; categorical", False),
    "t305": ("unsigned_identity", "civic_priority", "high", "most important factor; categorical", False),
    "eg801": ("unsigned_identity", "protest_position", "high", "position during protests; categorical", False),
    "eg807": ("unsigned_identity", "media_source", "high", "source of information; categorical", False),
    "eg808": ("unsigned_identity", "media_source", "high", "identify source; open-ended categorical", False),
    "eg814": ("unsigned_identity", "political_system_preference", "high", "preferred political system; categorical", False),
    "eg815": ("unsigned_identity", "state_preference", "high", "preferred state; categorical", False),
    "t901": ("unsigned_identity", "protest_position", "high", "position during protests; categorical", False),
    "t907": ("unsigned_identity", "media_source", "high", "source of information; categorical", False),
    "t908": ("unsigned_identity", "media_source", "high", "identify source; open-ended categorical", False),
    "t916": ("unsigned_identity", "political_system_preference", "high", "preferred political system; categorical", False),
    "t917": ("unsigned_identity", "state_preference", "high", "preferred state; categorical", False),
    "q408": ("unsigned_identity", "media_source", "high", "identify source; open-ended categorical", False),
    "eg308": ("unsigned_identity", "political_identity_coordinate", "high", "which party; categorical", False),
    
    # FACTUAL KNOWLEDGE — should be unsigned_identity
    "q5221": ("unsigned_identity", "political_knowledge", "high", "name foreign minister; factual recall", False),
    "q5222": ("unsigned_identity", "political_knowledge", "high", "name speaker of house; factual recall", False),
    "sa5222": ("unsigned_identity", "political_knowledge", "high", "name speaker of shura; factual recall", False),
    "q5223": ("unsigned_identity", "political_knowledge", "high", "name minister of interior; factual recall", False),
    "q5224": ("unsigned_identity", "political_knowledge", "high", "name mayor/governor; factual recall", False),
    "ir5225": ("unsigned_identity", "political_knowledge", "high", "name governor; factual recall", False),
    "t913ot": ("unsigned_identity", "political_knowledge", "high", "name of protest; open-ended", False),
    
    # BINARY PARTICIPATION — should be signed_attitude (was signed_evaluation)
    "eg302": ("signed_attitude", "binary_attitude", "high", "will you vote; binary participation", False),
    "eg307": ("signed_attitude", "binary_attitude", "high", "would vote tomorrow; voting intention", False),
    "eg311": ("signed_attitude", "binary_attitude", "high", "would vote in presidential; voting intention", False),
    "t302": ("signed_attitude", "binary_attitude", "high", "will you participate in elections; binary", False),
    "t307": ("signed_attitude", "binary_attitude", "high", "would vote tomorrow; voting intention", False),
    "te501d": ("signed_attitude", "binary_attitude", "high", "plan on joining party; binary", False),
    "eg804": ("signed_attitude", "binary_attitude", "high", "offered assistance to protests; binary", False),
    "eg805": ("signed_attitude", "binary_attitude", "high", "supported protests via internet; binary", False),
    "eg806": ("signed_attitude", "binary_attitude", "high", "friends participated; binary", False),
    "t904": ("signed_attitude", "binary_attitude", "high", "supported protests via internet; binary", False),
    "t905": ("signed_attitude", "binary_attitude", "high", "friends participated; binary", False),
    "t906": ("signed_attitude", "binary_attitude", "high", "joined protection committees; binary", False),
    "t914": ("signed_attitude", "binary_attitude", "high", "offered assistance; binary", False),
    "q6101": ("signed_attitude", "binary_attitude", "high", "pray daily; binary practice", False),
    "q6105": ("signed_attitude", "binary_attitude", "high", "attend Friday prayer; binary practice", False),
    "q6106": ("signed_attitude", "binary_attitude", "high", "read Quran/Bible; binary practice", False),
    "t6101": ("signed_attitude", "binary_attitude", "high", "pray daily; binary practice", False),
    "t6105": ("signed_attitude", "binary_attitude", "high", "attend Friday prayer; binary practice", False),
    "t6106": ("signed_attitude", "binary_attitude", "high", "read Quran/Bible; binary practice", False),
    "q603": ("signed_evaluation", "subjective_evaluation", "high", "lottery willingness; evaluative", False),
    
    # ORDINAL EVALUATION — correctly signed, bump confidence to high
    "te105": ("signed_evaluation", "subjective_evaluation", "high", "safety vs last year; evaluative comparison", False),
    "eg301": ("signed_evaluation", "subjective_evaluation", "high", "ready for elections; attitude", False),
    "eg306": ("signed_evaluation", "subjective_evaluation", "high", "will elections be free; attitude", False),
    "eg309": ("signed_evaluation", "subjective_evaluation", "high", "will any party win majority; attitude", False),
    "eg310": ("signed_evaluation", "subjective_evaluation", "high", "ready for presidential elections; attitude", False),
    "q504": ("signed_evaluation", "subjective_evaluation", "high", "evaluate democracy and human rights; evaluative", False),
    "q512": ("signed_evaluation", "subjective_evaluation", "high", "democracy suitability scale; evaluative", False),
    "q5171": ("signed_evaluation", "subjective_evaluation", "high", "political system evaluation", False),
    "q5172": ("signed_evaluation", "subjective_evaluation", "high", "political system evaluation", False),
    "q5173": ("signed_evaluation", "subjective_evaluation", "high", "political system evaluation", False),
    "eg810": ("signed_evaluation", "subjective_evaluation", "high", "feelings of victory/loss; evaluative", False),
    "eg8111": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve democracy; attitude", False),
    "eg8113": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve economy; attitude", False),
    "eg8114": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve human rights; attitude", False),
    "eg8115": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve rule of law; attitude", False),
    "eg8116": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve social justice; attitude", False),
    "eg8117": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve role for Egypt; attitude", False),
    "t910": ("signed_evaluation", "subjective_evaluation", "high", "feelings of victory/loss; evaluative", False),
    "t9111": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve democracy; attitude", False),
    "t9113": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve economy; attitude", False),
    "t9114": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve human rights; attitude", False),
    "t9115": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve rule of law; attitude", False),
    "t9116": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve social justice; attitude", False),
    "t9117": ("signed_evaluation", "subjective_evaluation", "high", "will revolution achieve role for Tunisia; attitude", False),
    "q7001": ("signed_evaluation", "subjective_evaluation", "high", "prefer relations with US; evaluative", False),
    "q7002": ("signed_evaluation", "subjective_evaluation", "high", "prefer relations with Saudi; evaluative", False),
    "q7003": ("signed_evaluation", "subjective_evaluation", "high", "prefer relations with Iran; evaluative", False),
    "q7004": ("signed_evaluation", "subjective_evaluation", "high", "prefer relations with Turkey; evaluative", False),
    "q7005": ("signed_evaluation", "subjective_evaluation", "high", "prefer relations with France; evaluative", False),
    "q7006": ("signed_evaluation", "subjective_evaluation", "high", "prefer relations with Israel; evaluative", False),
    "q7011": ("signed_evaluation", "subjective_evaluation", "high", "influence on democracy; evaluative", False),
    "q7012": ("signed_evaluation", "subjective_evaluation", "high", "influence on democracy; evaluative", False),
    "q7013": ("signed_evaluation", "subjective_evaluation", "high", "influence on democracy; evaluative", False),
    "p713": ("signed_evaluation", "subjective_evaluation", "high", "new elections attitude; evaluative", False),
    "eg708a": ("signed_evaluation", "subjective_evaluation", "high", "do you...; attitude", False),
    
    # IMPORTANCE RANKING — correctly signed, bump confidence
    "q5201": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    "q5202": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    "q5204": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    "q5206": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    "q5207": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    "q5208": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    "ir52011": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    "t52012": ("signed_evaluation", "subjective_evaluation", "high", "characteristics importance ranking; evaluative", False),
    
    # LEFT AS LOW-CONFIDENCE (need more info): 
    # sa503 "which intellectual movement" — categorical, should be unsigned_identity
    "sa503": ("unsigned_identity", "political_identity_coordinate", "high", "intellectual movement preference; categorical", False),
}

for wave, canonical, corrections in [("II", "II", corrections_w2)]:
    path = f"{AUTH}/arab_barometer_{canonical}_directionality_authority.csv"
    df = pd.read_csv(path)
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
        else:
            print(f"  WARNING: {vn} not found in W{canonical}")
    
    # Sync bridge action from policy
    df["bridge_directionality_action"] = df["directionality_policy"].apply(
        lambda p: "force_unsigned" if p in ("unsigned_context", "unsigned_identity", "unsigned_metadata") else "allow_directionality"
    )
    
    df.to_csv(path, index=False)
    print(f"W{canonical}: {applied}/{len(corrections)} corrections applied")
    
    # Also update overlay and authority files
    from shutil import copy2
    for d in [REP, REP2]:
        opath = f"{d}/arab_barometer_{canonical}_directionality_overlay.csv"
        df.to_csv(opath, index=False)
    
    remaining = df["manual_review_required"].sum()
    print(f"  Remaining flagged: {remaining} / {len(df)}")
