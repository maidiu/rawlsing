#!/usr/bin/env python3
"""Manual directionality authority for Arab Barometer Wave I (W1).
Human-authored classification of all 181 codebook variables.
Script serializes decisions only — does not infer semantics."""
import csv, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AUTH = REPO / "data" / "ddm_build_copy" / "directionality_authority"
REP = REPO / "data" / "ddm_build_copy" / "reports"

SOURCE = "Arab Barometer"
WAVE = "I"
CANON = "I"

# (var_name, semantic_role, semantic_subrole, directionality_policy,
#  signed_polarity_status, response_family_expectation,
#  positive_anchor_label, negative_anchor_label, neutral_anchor_label,
#  bridge_directionality_action, directionality_confidence, directionality_note, manual_review)

ADMIN = [
    ("ser", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "survey number; administrative metadata", False),
    ("country", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "country identifier; administrative metadata", False),
]

DEMO = [
    ("q701", "position_context", "life_course_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "exact age; position coordinate", False),
    ("q701agecategories", "position_context", "life_course_coordinate", "unsigned_context", "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "high", "age categories; position coordinate", False),
    ("q702", "position_context", "identity_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "sex; position coordinate", False),
    ("q703", "position_context", "social_position_coordinate", "unsigned_context", "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "high", "education level; position coordinate", False),
    ("q703dichotomous", "position_context", "social_position_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "literacy; position coordinate", False),
    ("q704", "position_context", "labor_market_status", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "employment status; position coordinate", False),
    ("q705", "position_context", "labor_market_status", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "retired/housewife/student; position coordinate", False),
    ("q706", "position_context", "labor_market_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "full-time or part-time; position coordinate", False),
    ("q707", "position_context", "labor_market_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "occupation; position coordinate", False),
    ("q708", "position_context", "labor_market_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "employment sector; position coordinate", False),
    ("q709", "position_context", "life_course_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "marital status; position coordinate", False),
    ("q710", "position_context", "labor_market_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "spouse occupation; position coordinate", False),
    ("q711", "position_context", "identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "religion; identity coordinate", False),
    ("q715withoutmorocco", "position_context", "material_security_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "individual income; position coordinate", False),
    ("q716withoutmorocco", "position_context", "material_security_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "family income; position coordinate", False),
    ("V715onlymorocco", "position_context", "material_security_coordinate", "unsigned_context", "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "high", "Morocco individual income; position coordinate", False),
    ("V716onlymorocco", "position_context", "material_security_coordinate", "unsigned_context", "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "high", "Morocco family income; position coordinate", False),
    ("q715incomedeciles", "position_context", "material_security_coordinate", "unsigned_context", "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "high", "income deciles; position coordinate", False),
    ("q716incomedeciles", "position_context", "material_security_coordinate", "unsigned_context", "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "high", "income deciles family; position coordinate", False),
    ("q717", "position_context", "identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "country of origin; identity coordinate", False),
]

NOMINAL = [
    ("q217", "relation_evidence", "media_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "source of information; categorical only", False),
    ("q227", "relation_evidence", "wasta_channel", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "type of wasta; categorical only", False),
    ("q2311", "relation_evidence", "democratic_definition", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "essential characteristic of democracy forced-choice; categorical", False),
    ("q2312", "relation_evidence", "democratic_definition", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "second essential characteristic; categorical", False),
    ("q248withoutpalestine", "relation_evidence", "civic_priority", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "most important problem; categorical", False),
    ("q248donlypalestine", "relation_evidence", "civic_priority", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "most important problem Palestine version; categorical", False),
    ("q249withoutpalestine", "relation_evidence", "civic_priority", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "second most important problem; categorical", False),
    ("q249onlypalestine", "relation_evidence", "civic_priority", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "second most important problem Palestine; categorical", False),
    ("q301", "relation_evidence", "political_identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "identity primacy; categorical forced-choice", False),
    ("q3021", "relation_evidence", "political_identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "most important identity group; categorical", False),
    ("q3022", "relation_evidence", "political_identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "second most important identity; categorical", False),
    ("q305", "relation_evidence", "emigration_intention", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "emigration consideration with reason split; categorical", False),
    ("q503", "relation_evidence", "spouse_preference", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "most important spouse characteristic; categorical", False),
    ("q601", "relation_evidence", "causal_attribution", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "reasons arab world lags; categorical forced-choice", False),
    ("q612", "relation_evidence", "causal_attribution", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "why government fails to provide; categorical", False),
    ("q714", "relation_evidence", "religious_practice_location", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "prayer location; categorical", False),
]

SIGNED = [
    # Economic evaluation — ordinal
    ("q101", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "current economic condition; evaluative", False),
    ("q102", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "future economic condition; evaluative", False),
    ("q103", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "family economic situation; evaluative", False),

    # Institutional trust
    ("q2011", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust in institutions; evaluative", False),
    ("q2012", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust in institutions; evaluative", False),
    ("q2013", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust in institutions; evaluative", False),
    ("q2014", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust in institutions; evaluative", False),
    ("q2015", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust in institutions; evaluative", False),

    # Binary attitude
    ("q202", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "organization membership; binary", False),

    # Binary interpersonal trust
    ("q204", "relation_evidence", "social_trust_orientation", "signed_attitude", "signed_attitude", "yes_no", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "interpersonal trust; binary attitude", False),

    # Safety evaluation — ordinal
    ("q205", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "safety perception; evaluative", False),
    ("q206", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "safety vs past; evaluative comparison", True),

    # Political participation binary
    ("q207", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "participated in elections; binary with not eligible option", False),
    ("q210", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "attended campaign; binary", False),

    # Election fairness — ordinal
    ("q211", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "election freeness/fairness; evaluative", False),

    # Binary
    ("q212", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "platform differences; binary", False),

    # Ease of access — ordinal
    ("q2131", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "ease obtaining service; evaluative with never-tried", False),
    ("q2132", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "ease obtaining service; evaluative", False),
    ("q2133", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "ease obtaining service; evaluative", False),
    ("q2134", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "ease obtaining service; evaluative", False),
    ("q2135", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "ease obtaining service; evaluative", False),

    # Political/economy evaluation — ordinal
    ("q214", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political situation; evaluative", False),
    ("q215", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political interest; evaluative", False),

    # Frequency
    ("q216", "relation_evidence", "media_orientation", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "news frequency; frequency", False),

    # Government impact — ordinal
    ("q219", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government policy impact; evaluative", False),

    # Agree/disagree — ordinal
    ("q221", "relation_evidence", "gender_equality_policy", "signed_attitude", "signed_attitude", "ordinal_scale", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "gender equality; agree/disagree", False),

    # Frequency
    ("q222", "relation_evidence", "media_orientation", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "internet use; frequency", False),

    # Duration
    ("q224", "relation_evidence", "life_course_coordinate", "signed_frequency", "signed_frequency", "frequency_scale", "more time", "less time", "neutral / ambivalent", "allow_directionality", "high", "time abroad; duration", False),

    # Agree/disagree democracy
    ("q2251", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "competition good for democracy; agree/disagree", False),
    ("q2252", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "politicians should compete; agree/disagree", False),

    # Binary
    ("q226", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "used wasta; binary", False),
    ("q228", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "court dispute resolution; binary", False),

    # Political action frequency
    ("q2301", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "political action frequency; frequency", False),
    ("q2302", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "political action frequency; frequency", False),

    # Agree/disagree equality
    ("q2321", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "income inequality; agree/disagree", False),
    ("q2322", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "democracy preference; agree/disagree", False),
    ("q2323", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "elected government; agree/disagree", False),
    ("q2324", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "economic equality; agree/disagree", False),

    # Human rights justification — ordinal
    ("q234", "relation_evidence", "moral_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more justified", "less justified", "neutral / ambivalent", "allow_directionality", "high", "human rights violation justification; evaluative", False),

    # 10-point democracy scales
    ("q235", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale current; evaluative", False),
    ("q236", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale; evaluative", False),
    ("q237", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale; evaluative", False),
    ("q238", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale; evaluative", False),
    ("q239", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale; evaluative", False),
    ("q240", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale; evaluative", False),
    ("q241", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale; evaluative", False),
    ("q242", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more democratic", "less democratic", "neutral / ambivalent", "allow_directionality", "high", "democracy scale; evaluative", False),
    ("q243", "relation_evidence", "political_system_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more suitable", "less suitable", "neutral / ambivalent", "allow_directionality", "high", "democracy suitability; 10-point evaluative", False),
    ("q244", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more satisfied", "less satisfied", "neutral / ambivalent", "allow_directionality", "high", "democracy satisfaction; 10-point evaluative", False),

    # Political system approval — ordinal
    ("q2451", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system; evaluative", False),
    ("q2452", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system; evaluative", False),
    ("q2453", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system; evaluative", False),
    ("q2454", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system; evaluative", False),

    # Suitability — ordinal
    ("q2461", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system suitability; evaluative", False),
    ("q2462", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system suitability; evaluative", False),
    ("q2463", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system suitability; evaluative", False),
    ("q2464", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "political system suitability; evaluative", False),

    # Government performance — ordinal
    ("q2471", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government performance; evaluative with NA option", False),
    ("q2472", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government performance; evaluative", False),
    ("q2473", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government performance; evaluative", False),
    ("q2474", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government performance; evaluative", False),
    ("q2475", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government performance; evaluative", False),
    ("q2476", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government performance; evaluative", False),

    # Likelihood — ordinal
    ("q2501", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more likely", "less likely", "neutral / ambivalent", "allow_directionality", "high", "government will solve problems; likelihood", False),
    ("q2502", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more likely", "less likely", "neutral / ambivalent", "allow_directionality", "high", "government will solve; likelihood", False),

    # Agree/disagree statements
    ("q2511", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "agree/disagree statement; evaluative", False),
    ("q2512", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "agree/disagree statement; evaluative", False),
    ("q2513", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "agree/disagree statement; evaluative", False),
    ("q2514", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "agree/disagree statement; evaluative", False),

    # Power/perception — ordinal
    ("q252", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "legislature power; evaluative", False),
    ("q253", "relation_evidence", "corruption_perception", "signed_evaluation", "signed_evaluation", "ordinal_scale", "less corruption", "more corruption", "neutral / ambivalent", "allow_directionality", "high", "corruption prevalence; evaluative", False),
    ("q254", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government anti-corruption; evaluative", False),

    # Importance — ordinal
    ("q2551", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "qualification importance; evaluative", False),
    ("q2552", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "qualification importance; evaluative", False),
    ("q2553", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "qualification importance; evaluative", False),
    ("q2554", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "qualification importance; evaluative", False),
    ("q2561", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "voting factor importance; evaluative", False),
    ("q2562", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "voting factor importance; evaluative", False),
    ("q2563", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "voting factor importance; evaluative", False),
    ("q2564", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "voting factor importance; evaluative", False),
    ("q2565", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "voting factor importance; evaluative", False),

    # Knowledge (factual recall) — unsigned
    ("q2571", "relation_evidence", "political_knowledge", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "name foreign minister; factual recall", False),
    ("q2572", "relation_evidence", "political_knowledge", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "name speaker of parliament; factual recall", False),

    # Neighbor preference — binary attitude
    ("q3031", "relation_evidence", "outgroup_or_identity_orientation", "signed_attitude", "signed_attitude", "yes_no", "more accepting", "less accepting", "neutral / ambivalent", "allow_directionality", "high", "neighbor preference; binary acceptance", False),
    ("q3032", "relation_evidence", "outgroup_or_identity_orientation", "signed_attitude", "signed_attitude", "yes_no", "more accepting", "less accepting", "neutral / ambivalent", "allow_directionality", "high", "neighbor preference different religion; binary", False),
    ("q3033", "relation_evidence", "outgroup_or_identity_orientation", "signed_attitude", "signed_attitude", "yes_no", "more accepting", "less accepting", "neutral / ambivalent", "allow_directionality", "high", "neighbor preference immigrants; binary", False),

    # Equality — agree/disagree ordinal
    ("q304", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "religion race gender obstacle; agree/disagree", False),

    # National pride — ordinal
    ("q306", "relation_evidence", "national_identity_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more proud", "less proud", "neutral / ambivalent", "allow_directionality", "high", "national pride; evaluative", False),

    # Values — agree/disagree ordinal
    ("q4011", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "values; agree/disagree", False),
    ("q4012", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "values; agree/disagree", False),
    ("q4013", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "values; agree/disagree", False),
    ("q4014", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "values; agree/disagree", False),
    ("q4021", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "principles importance; agree/disagree", False),
    ("q4022", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "principles importance; agree/disagree", False),
    ("q4023", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "principles importance; agree/disagree", False),

    # Lottery willingness — ordinal
    ("q501", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more willing", "less willing", "neutral / ambivalent", "allow_directionality", "high", "lottery willingness; evaluative", False),

    # Spouse criteria — importance ordinal
    ("q5021", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "spouse criteria importance; evaluative", False),
    ("q5022", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "spouse criteria importance; evaluative", False),
    ("q5023", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "spouse criteria importance; evaluative", False),
    ("q5024", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "spouse criteria importance; evaluative with other", False),
    ("q5025", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "spouse criteria importance; evaluative", False),
    ("q5026", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more important", "less important", "neutral / ambivalent", "allow_directionality", "high", "spouse criteria importance; evaluative", False),

    # Religious/values — agree/disagree ordinal
    ("q5041", "relation_evidence", "religious_orientation_coordinate", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "religious interpretation; agree/disagree", False),
    ("q5042", "relation_evidence", "religious_orientation_coordinate", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "religious interpretation; agree/disagree", False),
    ("q5043", "relation_evidence", "religious_orientation_coordinate", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "religious interpretation; agree/disagree", False),
    ("q5044", "relation_evidence", "religious_orientation_coordinate", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "religious interpretation; agree/disagree", False),
    ("q5045", "relation_evidence", "religious_orientation_coordinate", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "religious interpretation; agree/disagree", False),
    ("q5046", "relation_evidence", "religious_orientation_coordinate", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "religious interpretation; agree/disagree", False),

    # Principles — agree/disagree ordinal
    ("q5051", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "principles; agree/disagree", False),
    ("q5052", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "principles; agree/disagree", False),
    ("q5053", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "principles; agree/disagree", False),
    ("q5054", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "principles; agree/disagree", False),
    ("q5055", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "principles; agree/disagree", False),
    ("q5056", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "principles; agree/disagree", False),
    ("q5057", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "principles; agree/disagree", False),

    # Qualifications comparison — ordinal
    ("q5061", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "qualifications vs experience; evaluative", False),
    ("q5062", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "qualifications vs experience; evaluative", False),
    ("q5063", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "qualifications vs experience; evaluative", False),

    # Government/leadership — agree/disagree ordinal
    ("q5071", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "government officials; agree/disagree", False),
    ("q5072", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "political leaders; agree/disagree", False),
    ("q5073", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "government officials; agree/disagree", False),
    ("q5074", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "government creates fear; agree/disagree", False),
    ("q5075", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "politics and government; agree/disagree", False),

    # Arab League — ordinal
    ("q602", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more successful", "less successful", "neutral / ambivalent", "allow_directionality", "high", "Arab League effectiveness; evaluative", False),

    # Terrorist classification — binary attitude
    ("q6031", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more attributing", "less attributing", "neutral / ambivalent", "allow_directionality", "high", "classify as terrorist; ternary with heard-of option", False),
    ("q6032", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more attributing", "less attributing", "neutral / ambivalent", "allow_directionality", "high", "classify as terrorist; ternary", False),
    ("q6033", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more attributing", "less attributing", "neutral / ambivalent", "allow_directionality", "high", "classify as terrorist; ternary", False),
    ("q6034", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more attributing", "less attributing", "neutral / ambivalent", "allow_directionality", "high", "classify as terrorist; ternary", False),
    ("q6035", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more attributing", "less attributing", "neutral / ambivalent", "allow_directionality", "high", "classify as terrorist; ternary", False),

    # Regional politics — ordinal agree/disagree
    ("q604", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "US involvement justified; agree/disagree", False),
    ("q605", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "armed groups justified attacking civilians; agree/disagree", False),
    ("q606", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "US democracy promotion; agree/disagree", False),

    # Binary agree/disagree
    ("q607", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "US policy despite negative; binary agree/disagree", False),
    ("q608", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "Western culture agree/disagree; binary", False),

    # Ordinal agree/disagree
    ("q609", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "exposure to Western culture; agree/disagree", False),

    # Israel acceptance — binary attitude (forced-choice but attitudinal)
    ("q610", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "Israel acceptance; binary forced-choice", False),

    # Government does all it can — ordinal
    ("q611", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more agree", "more disagree", "neutral / ambivalent", "allow_directionality", "high", "government does all it can; agree/disagree", False),

    # Parliament role — ordinal
    ("q6131", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "parliament role; evaluative", False),
    ("q6132", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "parliament role; evaluative", False),
    ("q6133", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "parliament role; evaluative", False),

    # Quran reading — frequency
    ("q712", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "quran reading; frequency", False),

    # Prayer binary
    ("q713", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "do you pray; binary with other", False),

    # Religiosity — ordinal
    ("q714a", "relation_evidence", "religious_orientation_coordinate", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more religious", "less religious", "neutral / ambivalent", "allow_directionality", "high", "religiosity self-assessment; evaluative with other", False),
]

ALL = ADMIN + DEMO + NOMINAL + SIGNED

# Serialize
fields = ["source","wave","canonical_wave","var_name","question_text",
          "semantic_role","semantic_subrole","directionality_policy",
          "signed_polarity_status","response_family_expectation",
          "positive_anchor_label","negative_anchor_label","neutral_anchor_label",
          "bridge_directionality_action","directionality_confidence",
          "directionality_note","manual_review_required"]

import pandas as pd
cb = pd.read_csv(REPO / "data"/"FINAL CODEBOOKS"/"FINAL FINAL CODEBOOKS"/"Arab Barometer Wave 1 codebook.csv", low_memory=False)

def write_csv(path, rows, flds):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(flds)
        for r in rows:
            vn = r[0]
            qt = ""
            m = cb[cb["var_name"]==vn]
            if len(m):
                qt = str(m.iloc[0].get("question_text",""))
            w.writerow([SOURCE, WAVE, CANON, vn, qt] + list(r[1:]))

# Directionality authority
write_csv(AUTH/f"arab_barometer_{CANON}_directionality_authority.csv", ALL, fields)
print(f"Authority: {len(ALL)} rows")

# Directionality overlay
for d in [REP]:
    write_csv(d/f"arab_barometer_{CANON}_directionality_overlay.csv", ALL, fields)
print(f"Overlay: {len(ALL)} rows")

# Semantic authority overlay
sa_f = ["source","wave","canonical_wave","var_name","question_text","semantic_lane","semantic_role","evidence_lane","semantic_subrole","semantic_tags","directionality_policy","semantic_confidence","semantic_note"]
for d in [REP]:
    sa_rows = []
    for r in ALL:
        vn=r[0]; sr=r[1]; ss=r[2]; dp=r[3]; conf=r[10]; note=r[11]
        qt = ""
        m = cb[cb["var_name"]==vn]
        if len(m): qt = str(m.iloc[0].get("question_text",""))
        lane = "direct" if sr=="relation_evidence" else ("context" if sr=="position_context" else "admin")
        ev = "direct_relation_response" if lane=="direct" else ("position_context" if lane=="context" else "administrative")
        sa_rows.append([SOURCE,WAVE,CANON,vn,qt,lane,sr,ev,ss,"",dp,conf,note])
    with open(d/f"arab_barometer_{CANON}_semantic_authority_overlay.csv","w",newline="") as f:
        w = csv.writer(f); w.writerow(sa_f); w.writerows(sa_rows)
    print(f"Semantic overlay: {len(sa_rows)} rows")

# First-pass authority
fp_f = ["source","wave","canonical_wave","var_name","var_code","question_id","question_text","module_guess","semantic_lane","semantic_role","evidence_lane","allowed_as_branch_position_signature","allowed_as_branch_relation_cosignature","allowed_as_attitude_cloud_anchor","allowed_as_attitude_cloud_feature","allowed_as_v551_relation_evidence","allowed_as_association_feature","is_substantive","not_direct_evidence","manual_designation_required","designation_confidence","rationale"]
for d in [REP]:
    fp_rows = []
    for r in ALL:
        vn=r[0]; sr=r[1]; note=r[11]
        qt = ""
        m = cb[cb["var_name"]==vn]
        if len(m): qt = str(m.iloc[0].get("question_text",""))
        sub = "TRUE" if sr=="relation_evidence" else "FALSE"
        lane = "direct_relation" if sub=="TRUE" else "context"
        ev = "direct_response" if sub=="TRUE" else "context"
        fp_rows.append([SOURCE,WAVE,CANON,vn,vn,vn,qt,"substantive" if sub=="TRUE" else "context",lane,sr,ev,"FALSE","FALSE","TRUE" if sub=="TRUE" else "FALSE","FALSE","TRUE" if sub=="TRUE" else "FALSE","FALSE",sub,"FALSE","FALSE","high",note])
    with open(d/f"arab_barometer_{CANON}_first_pass_authority_table.csv","w",newline="") as f:
        w = csv.writer(f); w.writerow(fp_f); w.writerows(fp_rows)
    print(f"First-pass: {len(fp_rows)} rows")

# Position conditioning overlay (minimal — no position routing for these items)
pc_f = ["source","wave","canonical_wave","var_name","question_text","semantic_lane","semantic_role","evidence_lane","semantic_subrole","semantic_tags","directionality_policy","semantic_confidence","semantic_note","position_conditioning","position_modifiers"]
for d in [REP]:
    pc_rows = []
    for r in ALL:
        vn=r[0]; sr=r[1]; ss=r[2]; dp=r[3]; conf=r[10]; note=r[11]
        qt = ""
        m = cb[cb["var_name"]==vn]
        if len(m): qt = str(m.iloc[0].get("question_text",""))
        lane = "direct" if sr=="relation_evidence" else ("context" if sr=="position_context" else "admin")
        ev = "direct_relation_response" if lane=="direct" else ("position_context" if lane=="context" else "administrative")
        pc_rows.append([SOURCE,WAVE,CANON,vn,qt,lane,sr,ev,ss,"",dp,conf,note,"",""])
    with open(d/f"arab_barometer_{CANON}_position_conditioning_overlay.csv","w",newline="") as f:
        w = csv.writer(f); w.writerow(pc_f); w.writerows(pc_rows)
    print(f"Position conditioning: {len(pc_rows)} rows")

# Update index
idx_path = AUTH / "directionality_authority_index.csv"
idx_rows = []
if idx_path.exists():
    with open(idx_path) as f:
        for row in csv.DictReader(f):
            idx_rows.append(row)
idx_rows = [r for r in idx_rows if not (r.get("source")==SOURCE and r.get("wave")==WAVE)]
idx_rows.append({"source":SOURCE,"wave":WAVE,"file_name":f"arab_barometer_{CANON}_directionality_authority.csv","row_count":str(len(ALL)),"status":"active","notes":"manually authored from codebook by Codex; 1 manual_review"})
with open(idx_path,"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["source","wave","file_name","row_count","status","notes"])
    w.writeheader(); w.writerows(idx_rows)
print(f"Index updated")

signed = sum(1 for r in ALL if r[9]=="allow_directionality")
unsigned = sum(1 for r in ALL if r[9]=="force_unsigned")
print(f"\n=== Summary ===")
print(f"Total: {len(ALL)}")
print(f"Signed: {signed} ({signed/len(ALL)*100:.0f}%)")
print(f"Unsigned: {unsigned} ({unsigned/len(ALL)*100:.0f}%)")
print(f"Manual review: {sum(1 for r in ALL if r[12])}")
print(f"Done.")
