#!/usr/bin/env python3
"""Build directionality authority for Arab Barometer Wave I.
Mirrors the GSS pattern from build_directionality_authority.py."""
import argparse, pandas as pd, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CODEBOOK = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS" / "Arab Barometer Wave 1 codebook.csv"
DEFAULT_OUTPUT = ROOT / "data" / "ddm_build_copy" / "directionality_authority"
INDEX_PATH = DEFAULT_OUTPUT / "directionality_authority_index.csv"

SOURCE = "Arab Barometer"
WAVE = "I"
CANONICAL_WAVE = "I"

# Variables that are demographic/administrative — excluded from directionality authority
DEMOGRAPHIC_VARS = {
    "country", "ser", "q701", "q701agecategories", "q703", "q704", "q707", "q708",
    "q710", "q711", "q715withoutmorocco", "q716withoutmorocco",
    "V715onlymorocco", "V716onlymorocco",
    "q715incomedeciles", "q716incomedeciles",
}

# Variables whose value labels are demographic ranges (not attitudinal)
DEMOGRAPHIC_LABEL_KEYWORDS = [
    "years old", "age", "income", "salary", "education",
    "elementary", "secondary", "university", "postgraduate",
    "religious", "muslim", "christian", "druze",
    "public sector", "private sector", "government", "ngo",
    "housewife", "student", "retired", "unemployed",
    "married", "single", "divorced", "widowed",
    "shekel", "dinar", "pound", "lira",
]


def is_demographic(var_name: str, question_text: str, substantive_labels: str) -> bool:
    vn = var_name.strip().lower()
    # Exact var-name matches — these are always demographic
    if vn in DEMOGRAPHIC_VARS:
        return True
    # Var names that CONTAIN these patterns are demographic
    demo_var_patterns = [r"\bage\b", r"\bincome\b", r"\beducation\b", r"\bemployment\b",
                         r"\boccupation\b", r"\bsector\b", r"\bdecile",
                         r"\bliteracy\b", r"\bmarital\b", r"\bsex\b"]
    for pat in demo_var_patterns:
        if re.search(pat, vn):
            return True
    # q7xx variables are demographics (age, income, education, sex, religion, etc.)
    # except specific attitudinal ones
    q7_attitudinal = {"q712", "q713", "q714", "q714a"}
    if re.match(r"^q?7\d", vn) and vn not in q7_attitudinal:
        return True

    svl = (substantive_labels or "").lower()
    # Check value labels for demographic content patterns
    # Demographic variables have labels like: age ranges, income bands, education levels, religious affiliations
    demo_label_markers = [
        r"\d+\s*-\s*\d+\s*(?:years|dh|shekel|dinar)",  # age/income ranges
        r"(?:less than|more than)\s*\d+\s*(?:years|dh|shekel|dinar)",  # income bands
        r"\b(?:illiterate|elementary|primary|secondary|college|university|postgraduate)\b",  # education
        r"\b(?:muslim|christian|shiite|sunni|druze|jewish)\b",  # religion affiliations
        r"\b(?:public sector|private sector|ngo|government|military)\b",  # employment sector
        r"\b(?:housewife|student|retired|unemployed|self.?employed)\b",  # employment status
        r"\b(?:employer|manager|professional|executive|clerical|sales|service|skilled|semi.?skilled)\b",  # occupation
        r"\b(?:married|single|divorced|widowed|separated)\b",  # marital status
        r"\b(?:dh\b|dinar|shekel|pound|lira)\b",  # currency in labels
        r"\bfirst decile\b",  # income deciles
        r"\bno revenue\b",  # income
        r"\b(?:less than 1|\d{4,})\s*(?:dh|dinar|shekel)\b",  # specific currency amounts
    ]
    demo_matches = sum(1 for pat in demo_label_markers if re.search(pat, svl))
    # If value labels look demographic (3+ markers or 1+ strong marker with no attitude keywords)
    attitude_keywords = [r"\bagree\b", r"\bstrongly\b", r"\bdisagree\b", r"\bsafe\b",
                         r"\btrust\b", r"\bfair\b", r"\bsatisfied\b", r"\bendors",
                         r"\bapprove\b", r"\bopinion\b"]
    has_attitude = any(re.search(kw, svl) for kw in attitude_keywords)
    if demo_matches >= 2 and not has_attitude:
        return True
    if demo_matches >= 1 and re.search(r"\b(?:age|income|education|religion|employ)", vn):
        return True
    return False


def classify_directionality(var_name: str, question_text: str, substantive_labels: str) -> dict | None:
    """Given a variable name, question text, and substantive value labels,
    determine the directionality policy and anchor labels."""

    q = (question_text or "").lower()
    svl = (substantive_labels or "").lower()

    # --- Detect binary yes/no ---
    yes_no_patterns = [
        r"^\s*1\s*=\s*(?:yes|favor|approve|agree)\b",
        r"\|\s*2\s*=\s*(?:no|oppose|disapprove|disfavor)\b",
    ]
    if all(re.search(p, svl) for p in yes_no_patterns):
        # Check if it's a simple yes/no or has additional categories
        parts = [p.strip() for p in svl.split("|")]
        codes = set()
        for part in parts:
            m = re.match(r"\s*(\d+)", part)
            if m:
                codes.add(int(m.group(1)))
        if codes == {1, 2}:
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
                "directionality_note": f"binary yes/no; sign reflects endorsement vs rejection",
                "manual_review_required": False,
            }
        # Check for yes/no with third category (e.g. "not illegible")
        if codes == {1, 2, 3}:
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
                "directionality_note": f"binary yes/no with third option; sign reflects endorsement vs rejection",
                "manual_review_required": False,
            }

    # --- Detect 4-point ordinal evaluation (good/bad, agree/disagree) ---
    # Pattern: 1=very good | 2=good | 3=bad | 4=very bad
    # Pattern: 1=strongly agree | 2=agree | 3=disagree | 4=strongly disagree
    # Pattern: 1=very safe | 2=safe | 3=unsafe | 4=very unsafe
    ordinal4_eval_keywords = ["good", "bad", "agree", "disagree", "safe", "unsafe", "satisfied", "unsatisfied",
                               "easy", "difficult", "interested", "interested", "suitable", "unsuitable",
                               "justified", "justified", "free", "fair"]
    # Check for 1=positive | 2=positive | 3=negative | 4=negative pattern
    parts = [p.strip() for p in svl.split("|")]
    if len(parts) == 4:
        codes = []
        labels = []
        for p in parts:
            m = re.match(r"\s*(\d+)\s*=\s*(.+)", p)
            if m:
                codes.append(int(m.group(1)))
                labels.append(m.group(2).strip())
        if codes == [1, 2, 3, 4]:
            # Check if it's a positive-to-negative scale
            positive_words = ["good", "agree", "safe", "satisfied", "easy", "suitable", "free", "fair", "justified", "interested"]
            negative_words = ["bad", "disagree", "unsafe", "unsatisfied", "difficult", "unsuitable", "not free", "unfair", "unjustified", "uninterested"]
            first_pos = sum(1 for w in positive_words if w in labels[0].lower() or w in labels[1].lower())
            first_neg = sum(1 for w in negative_words if w in labels[2].lower() or w in labels[3].lower())
            if first_pos > 0 and first_neg > 0:
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
                    "directionality_note": f"evaluative ordered item; sign from unfavorable to favorable",
                    "manual_review_required": False,
                }

    # --- Detect ordinal trust scale ---
    # 1=a great deal of trust | 2=quite a lot of trust | 3=not very much trust | 4=no trust at all
    if "trust" in svl and any(w in svl for w in ["great deal", "quite a lot", "not very much", "no trust"]):
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
            "directionality_note": f"trust ordered item; sign from less to more trusting",
            "manual_review_required": False,
        }

    # --- Detect 5-point ordinal (very easy to very difficult / never tried) ---
    # Pattern: 1=very easy | 2=easy | 3=difficult | 4=very difficult | 5=never tried
    if len(parts) == 5:
        codes = [re.match(r"\s*(\d+)", p) for p in parts]
        codes = [int(m.group(1)) for m in codes if m]
        if codes == [1, 2, 3, 4, 5]:
            if "easy" in svl and "difficult" in svl:
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
                    "directionality_note": f"evaluative ordered item with never-tried option; sign from unfavorable to favorable",
                    "manual_review_required": False,
                }
            if "very often" in svl and "never" in svl:
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
                    "directionality_note": f"frequency-ordered item; sign from less to more frequent",
                    "manual_review_required": False,
                }

    # --- Detect frequency scales ---
    # Pattern: 1=daily ... | 2=weekly ... | 3=monthly ... | 4=never
    if any(w in svl for w in ["daily", "often", "frequently", "always", "never"]):
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
            "directionality_note": f"frequency-ordered item; sign from less to more frequent",
            "manual_review_required": False,
        }

    # --- Detect 10-point democracy/dictatorship scales ---
    # 1 = complete dictatorship, 10 = complete democracy
    if re.search(r"10.point|1.*dictatorship|10.*democracy", q) or re.search(r"10.point|1.*dictatorship|10.*democracy", svl):
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "political_system_evaluation",
            "directionality_policy": "signed_evaluation",
            "signed_polarity_status": "signed_evaluation",
            "response_family_expectation": "ordinal_scale",
            "positive_anchor_label": "more democratic",
            "negative_anchor_label": "less democratic",
            "neutral_anchor_label": "neutral / ambivalent",
            "bridge_directionality_action": "allow_directionality",
            "directionality_confidence": "high",
            "directionality_note": f"10-point democracy scale; sign from less to more democratic",
            "manual_review_required": False,
        }

    # --- Detect 10-point satisfaction ---
    if re.search(r"10.point.*satisf", q) or re.search(r"10.point.*satisf", svl):
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "satisfaction_evaluation",
            "directionality_policy": "signed_evaluation",
            "signed_polarity_status": "signed_evaluation",
            "response_family_expectation": "ordinal_scale",
            "positive_anchor_label": "more satisfied",
            "negative_anchor_label": "less satisfied",
            "neutral_anchor_label": "neutral / ambivalent",
            "bridge_directionality_action": "allow_directionality",
            "directionality_confidence": "high",
            "directionality_note": f"10-point satisfaction scale; sign from less to more satisfied",
            "manual_review_required": False,
        }

    # --- Detect 3-point ordinal (once | more than once | never) ---
    if len(parts) == 3:
        codes = [re.match(r"\s*(\d+)", p) for p in parts]
        codes = [int(m.group(1)) for m in codes if m]
        if codes == [1, 2, 3] and "never" in svl:
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
                "directionality_note": f"frequency-ordered item; sign from less to more frequent",
                "manual_review_required": False,
            }

    # --- Detect ordinal justification (completely justified ... not justified at all) ---
    if "justified" in svl:
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "moral_evaluation",
            "directionality_policy": "signed_evaluation",
            "signed_polarity_status": "signed_evaluation",
            "response_family_expectation": "ordinal_scale",
            "positive_anchor_label": "more justified",
            "negative_anchor_label": "less justified",
            "neutral_anchor_label": "neutral / ambivalent",
            "bridge_directionality_action": "allow_directionality",
            "directionality_confidence": "high",
            "directionality_note": f"justification ordered item; sign from less to more justified",
            "manual_review_required": False,
        }

    # --- Detect impact scale ---
    if "impact" in svl or "positive impact" in svl:
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
            "directionality_note": f"evaluative ordered item; sign from unfavorable to favorable",
            "manual_review_required": False,
        }

    # --- Detect nominal (non-ordered) items ---
    # These are things like "what is your most important source of information" with TV/radio/newspaper
    if "television" in svl or "newspaper" in svl or "radio" in svl or "internet" in svl:
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "informational_channel",
            "directionality_policy": "unsigned_identity",
            "signed_polarity_status": "unsigned_identity",
            "response_family_expectation": "nominal_single_choice",
            "positive_anchor_label": "",
            "negative_anchor_label": "",
            "neutral_anchor_label": "",
            "bridge_directionality_action": "force_unsigned",
            "directionality_confidence": "high",
            "directionality_note": f"nominal categorical choice; keep unsigned",
            "manual_review_required": False,
        }

    # --- Detect political system type items (nominal) ---
    if "characteristics of democracy" in q or "important for democracy" in q or "define democracy" in q:
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "democratic_definition",
            "directionality_policy": "unsigned_identity",
            "signed_polarity_status": "unsigned_identity",
            "response_family_expectation": "nominal_single_choice",
            "positive_anchor_label": "",
            "negative_anchor_label": "",
            "neutral_anchor_label": "",
            "bridge_directionality_action": "force_unsigned",
            "directionality_confidence": "high",
            "directionality_note": f"nominal categorical choice; keep unsigned",
            "manual_review_required": False,
        }

    # --- Nominal wasta type ---
    if "wasta" in q and ("government" in svl or "parliament" in svl):
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "wasta_channel",
            "directionality_policy": "unsigned_identity",
            "signed_polarity_status": "unsigned_identity",
            "response_family_expectation": "nominal_single_choice",
            "positive_anchor_label": "",
            "negative_anchor_label": "",
            "neutral_anchor_label": "",
            "bridge_directionality_action": "force_unsigned",
            "directionality_confidence": "high",
            "directionality_note": f"nominal categorical choice; keep unsigned",
            "manual_review_required": False,
        }

    # --- Agree/disagree with extra codes (like 100 = not provided) ---
    if any("strongly agree" in svl for kw in ["strongly agree", "agree", "disagree"]):
        # Filter out non-ordinal extra codes (values > 10)
        clean_parts = [p for p in parts if re.match(r"\s*([0-9]|10)\s*=", p)]
        if len(clean_parts) >= 3:
            clean_codes = []
            for p in clean_parts:
                m = re.match(r"\s*(\d+)", p)
                if m:
                    clean_codes.append(int(m.group(1)))
            if clean_codes == list(range(clean_codes[0], clean_codes[0] + len(clean_codes))):
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
                    "directionality_note": f"evaluative ordered item; sign from unfavorable to favorable",
                    "manual_review_required": False,
                }

    # --- Detect forced-choice (nominal) items with no ordinal direction ---
    # e.g. 1=internal factors | 2=external factors | 3=both equally important
    if any(w in svl for w in ["factors", "both are equally"]) and len(parts) <= 4:
        return {
            "semantic_role": "relation_evidence",
            "semantic_subrole": "causal_attribution",
            "directionality_policy": "unsigned_identity",
            "signed_polarity_status": "unsigned_identity",
            "response_family_expectation": "nominal_single_choice",
            "positive_anchor_label": "",
            "negative_anchor_label": "",
            "neutral_anchor_label": "",
            "bridge_directionality_action": "force_unsigned",
            "directionality_confidence": "high",
            "directionality_note": f"nominal categorical forced-choice; keep unsigned",
            "manual_review_required": False,
        }

    # --- Fallback: try ordinal detection by counting codes ---
    if parts and len(parts) >= 3 and len(parts) <= 5:
        codes = []
        for p in parts:
            m = re.match(r"\s*(\d+)", p)
            if m:
                codes.append(int(m.group(1)))
        if codes and codes == list(range(1, len(codes) + 1)):
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
                "directionality_confidence": "medium",
                "directionality_note": f"ordered item; directionality inferred from ordinal structure",
                "manual_review_required": True,
            }

    # --- Last resort: nominal ---
    return {
        "semantic_role": "relation_evidence",
        "semantic_subrole": "categorical_response",
        "directionality_policy": "unsigned_identity",
        "signed_polarity_status": "unsigned_identity",
        "response_family_expectation": "nominal_single_choice",
        "positive_anchor_label": "",
        "negative_anchor_label": "",
        "neutral_anchor_label": "",
        "bridge_directionality_action": "force_unsigned",
        "directionality_confidence": "low",
        "directionality_note": f"non-ordered or unclassified; default unsigned",
        "manual_review_required": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codebook", default=str(DEFAULT_CODEBOOK))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    codebook = pd.read_csv(args.codebook, low_memory=False)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process all variables with substantive value labels (note field is unreliable)
    candidates = codebook[codebook["substantive_value_labels"].notna() & (codebook["substantive_value_labels"] != "")].copy()
    print(f"Total codebook rows: {len(codebook)}")
    print(f"With substantive value labels: {len(candidates)}")

    rows = []
    for _, r in candidates.iterrows():
        var_name = str(r["var_name"]).strip()
        question_text = str(r.get("question_text", "")).strip()
        substantive_labels = str(r.get("substantive_value_labels", "")).strip()

        # Check if demographic/context item
        is_demo = is_demographic(var_name, question_text, substantive_labels)
        is_admin = var_name in ("ser", "country", "serial", "id")

        if is_admin:
            d = {
                "semantic_role": "administrative",
                "semantic_subrole": "metadata_identifier",
                "directionality_policy": "unsigned_metadata",
                "signed_polarity_status": "unsigned_metadata",
                "response_family_expectation": "administrative",
                "positive_anchor_label": "",
                "negative_anchor_label": "",
                "neutral_anchor_label": "",
                "bridge_directionality_action": "force_unsigned",
                "directionality_confidence": "high",
                "directionality_note": "administrative / metadata; keep unsigned",
                "manual_review_required": False,
            }
        elif is_demo:
            d = {
                "semantic_role": "context_coordinate",
                "semantic_subrole": "demographic_status",
                "directionality_policy": "unsigned_context",
                "signed_polarity_status": "unsigned_context",
                "response_family_expectation": "nominal_single_choice",
                "positive_anchor_label": "",
                "negative_anchor_label": "",
                "neutral_anchor_label": "",
                "bridge_directionality_action": "force_unsigned",
                "directionality_confidence": "high",
                "directionality_note": "position / context item; preserve routing but do not sign",
                "manual_review_required": False,
            }
        else:
            d = classify_directionality(var_name, question_text, substantive_labels)
            if d is None:
                continue

        rows.append({
            "source": SOURCE,
            "wave": WAVE,
            "canonical_wave": CANONICAL_WAVE,
            "var_name": var_name,
            "question_text": question_text,
            "semantic_role": d["semantic_role"],
            "semantic_subrole": d["semantic_subrole"],
            "directionality_policy": d["directionality_policy"],
            "signed_polarity_status": d["signed_polarity_status"],
            "response_family_expectation": d["response_family_expectation"],
            "positive_anchor_label": d["positive_anchor_label"],
            "negative_anchor_label": d["negative_anchor_label"],
            "neutral_anchor_label": d["neutral_anchor_label"],
            "bridge_directionality_action": d["bridge_directionality_action"],
            "directionality_confidence": d["directionality_confidence"],
            "directionality_note": d["directionality_note"],
            "manual_review_required": d["manual_review_required"],
        })

    authority = pd.DataFrame(rows)
    out_path = output_dir / f"arab_barometer_I_directionality_authority.csv"
    authority.to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({len(authority)} rows)")

    # Update index
    index_path = output_dir / "directionality_authority_index.csv"
    if index_path.exists():
        index = pd.read_csv(index_path)
    else:
        index = pd.DataFrame(columns=["source", "wave", "file_name", "row_count", "status", "notes"])
    # Remove existing entry for this source/wave if present
    index = index[~((index["source"] == SOURCE) & (index["wave"] == WAVE))]
    new_entry = pd.DataFrame([{
        "source": SOURCE,
        "wave": WAVE,
        "file_name": out_path.name,
        "row_count": len(authority),
        "status": "active",
        "notes": "seeded from codebook value labels via automated classification",
    }])
    index = pd.concat([index, new_entry], ignore_index=True)
    index.to_csv(index_path, index=False)
    print(f"Updated {index_path}")

    # Summary
    print(f"\n=== Summary ===")
    for policy in sorted(authority["directionality_policy"].unique()):
        cnt = len(authority[authority["directionality_policy"] == policy])
        print(f"  {policy}: {cnt} variables")
    print(f"\nManual review required: {authority['manual_review_required'].sum()}")
    print(f"\nVariables with manual_review_required=True:")
    for _, r in authority[authority["manual_review_required"]].iterrows():
        print(f"  {r['var_name']}: {r['question_text'][:60]} (confidence={r['directionality_confidence']})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
