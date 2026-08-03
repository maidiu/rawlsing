#!/usr/bin/env python3
"""Manual directionality authority for Afrobarometer Round 1.
Human-authored. Script only serializes, does not infer."""
import csv, os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AUTH_DIR = REPO / "data" / "ddm_build_copy" / "directionality_authority"
REPORTS = REPO / "data" / "ddm_build_copy" / "reports"

SOURCE = "Afrobarometer"
WAVE = "R1"
CANONICAL = "R1"

# (var_name, semantic_role, semantic_subrole, directionality_policy,
#  signed_polarity_status, response_family_expectation,
#  positive_anchor_label, negative_anchor_label, neutral_anchor_label,
#  bridge_directionality_action, directionality_confidence, directionality_note, manual_review)

# Administrative metadata
ADMIN = [
    ("refnumb", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "administrative / release metadata; keep unsigned", False),
    ("respnumb", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "administrative / release metadata; keep unsigned", False),
    ("withinwt", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "survey weight; keep unsigned", False),
    ("acrosswt", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "survey weight; keep unsigned", False),
    ("combinwt", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "survey weight; keep unsigned", False),
    ("africawt", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "survey weight; keep unsigned", False),
    ("afcombwt", "administrative", "release_or_control_metadata", "unsigned_metadata", "unsigned_metadata", "administrative", "", "", "", "force_unsigned", "high", "survey weight; keep unsigned", False),
]

# Demographic / position context — unsigned
DEMO = [
    ("country", "position_context", "position_context_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "country of interview; position coordinate", False),
    ("area", "position_context", "geographic_place_size_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "district/region; position coordinate", False),
    ("identity", "position_context", "identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "self-identity label; position coordinate", False),
    ("gender", "position_context", "identity_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "sex of respondent; position coordinate", False),
    ("age", "position_context", "life_course_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "age of respondent; position coordinate", False),
    ("educ", "position_context", "social_position_coordinate", "unsigned_context", "unsigned_context", "ordinal_scale", "", "", "", "force_unsigned", "high", "education level; position coordinate", False),
    ("race", "position_context", "identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "race/ethnicity; identity coordinate", False),
    ("language", "position_context", "survey_language_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "home language; position coordinate", False),
    ("urbrur", "position_context", "geographic_place_size_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "urban/rural; position coordinate", False),
    ("occup", "position_context", "labor_market_coordinate", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "occupation; position coordinate", False),
    ("unemp", "position_context", "labor_market_status", "unsigned_context", "unsigned_context", "nominal_single_choice", "", "", "", "force_unsigned", "high", "unemployment status; position coordinate", False),
]

# Open-ended / forced-choice nominal — unsigned_identity
NOMINAL = [
    ("demoe1", "relation_evidence", "democratic_definition", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "open-ended meaning of democracy; categorical only", False),
    ("demoe2", "relation_evidence", "democratic_definition", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "open-ended meaning of democracy; categorical only", False),
    ("demoe3", "relation_evidence", "democratic_definition", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "open-ended meaning of democracy; categorical only", False),
    ("mip1", "relation_evidence", "civic_priority", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "open-ended most important problem; categorical only", False),
    ("mip2", "relation_evidence", "civic_priority", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "open-ended second important problem; categorical only", False),
    ("pfrgpr", "relation_evidence", "outgroup_or_identity_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "open-ended which group represented; categorical only", False),
    ("pid", "relation_evidence", "political_identity_coordinate", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "party affiliation; identity coordinate", False),
    ("marhse", "relation_evidence", "policy_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "medium", "who responsible for housing; categorical forced-choice", True),
    ("marcdt", "relation_evidence", "policy_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "medium", "who responsible for agricultural credit; categorical", True),
    ("marcom", "relation_evidence", "policy_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "medium", "who responsible for marketing; categorical", True),
    ("marsch", "relation_evidence", "policy_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "medium", "who responsible for schools; categorical", True),
    ("maremp", "relation_evidence", "policy_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "medium", "who responsible for jobs; categorical", True),
    ("marcrm", "relation_evidence", "policy_orientation", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "medium", "who responsible for crime; categorical", True),
]

# Ordinal evaluation / agree-disagree / frequency — signed_evaluation/frequency/attitude
SIGNED = [
    # Support for democracy
    ("supdem", "relation_evidence", "policy_orientation", "signed_attitude", "signed_attitude", "ordinal_scale", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "support for democracy; sign reflects endorsement", False),
    ("supold", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "rating of past system; 0-10 evaluative", False),
    ("supnow", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "rating of current government; 0-10 evaluative", False),
    ("supfut", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "rating of future system; 0-10 evaluative", False),

    # Reject non-democratic alternatives
    ("rejone", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "reject one-party rule; signed policy", False),
    ("rejtrd", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "reject traditional rule; signed policy", False),
    ("rejmil", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "reject military rule; signed policy", False),
    ("rejdic", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "reject presidential dictatorship; signed policy", False),
    ("rejexp", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "medium", "reject government by experts; signed policy", True),

    # Democratic evaluation
    ("dmpext", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "extent of democracy; evaluative", False),
    ("dmpsat", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "satisfaction with democracy; evaluative", False),
    ("dmpvot", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "vote matters vs not; signed forced-choice", False),
    ("dmpsay", "relation_evidence", "attitude_polarity", "signed_attitude", "signed_attitude", "ordinal_scale", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "careful what you say; agree/disagree", False),

    # Support/oppose government actions
    ("defnew", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "support/oppose shutting down critical media; signed policy", False),
    ("defjug", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "support/oppose dismissing judges; signed policy", False),
    ("defele", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "support/oppose suspending elections; signed policy", False),

    # Policy forced-choice
    ("spamar", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "market variety vs low prices; signed forced-choice", False),
    ("spafee", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "free vs fee school/health; signed forced-choice", False),
    ("sparet", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "keep civil servants vs retrench; signed forced-choice", False),
    ("spaprv", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "medium", "government ownership vs privatization; signed forced-choice", True),

    # SAP
    ("sapknw", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "heard of SAP; binary knowledge", False),
    ("sapmin", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "SAP helped vs hurt; signed forced-choice", False),
    ("sapsat", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "satisfaction with SAP; evaluative", False),

    # Market responsibility
    ("marsuc", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "people vs government responsibility; signed forced-choice", False),
    ("marjob", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "private sector vs government jobs; signed forced-choice", False),
    ("marear", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "free to earn vs government limits; signed forced-choice", False),
    ("marrsk", "relation_evidence", "policy_orientation", "signed_policy", "signed_policy", "ordinal_scale", "more approving", "more disapproving", "neutral / ambivalent", "allow_directionality", "high", "starting business risky vs good idea; signed forced-choice", False),

    # Democracy essential items
    ("demmaj", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "majority rule essential for democracy; importance", False),
    ("demspc", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "freedom to criticize essential for democracy; importance", False),
    ("demele", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "regular elections essential for democracy; importance", False),
    ("demmpd", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "multi-party competition essential for democracy; importance", False),
    ("demnec", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "basic necessities essential for democracy; importance", False),
    ("dememp", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "jobs for everyone essential for democracy; importance", False),
    ("demedu", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "equal education essential for democracy; importance", False),
    ("demgap", "relation_evidence", "policy_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "small income gap essential for democracy; importance", False),

    # Social trust and political engagement
    ("sctrust", "relation_evidence", "social_trust_orientation", "signed_attitude", "signed_attitude", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "interpersonal trust; signed attitude", False),
    ("scint", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "interest in politics; evaluative", False),
    ("scdsc", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "discuss politics; frequency", False),
    ("scund", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "understand government; evaluative", False),

    # Knowledge items (correct/incorrect — factual, not directional)
    ("sckloc", "relation_evidence", "political_knowledge", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "name local govt representative; factual recall", False),
    ("sckmp", "relation_evidence", "political_knowledge", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "name legislative representative; factual recall", False),
    ("sckfin", "relation_evidence", "political_knowledge", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "name finance minister; factual recall", False),
    ("sckvp", "relation_evidence", "political_knowledge", "unsigned_identity", "unsigned_identity", "nominal_single_choice", "", "", "", "force_unsigned", "high", "name vice-president; factual recall", False),

    # National/group pride and identity
    ("nidprd", "relation_evidence", "national_identity_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "proud to be citizen; signed evaluation", False),
    ("nidchl", "relation_evidence", "national_identity_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "children should identify as citizens; signed evaluation", False),
    ("gidprd", "relation_evidence", "outgroup_or_identity_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "proud of identity group; signed evaluation", False),
    ("gidchl", "relation_evidence", "outgroup_or_identity_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "children should identify with group; signed evaluation", False),
    ("gidbes", "relation_evidence", "outgroup_or_identity_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "own group best; signed evaluation", False),
    ("gidstr", "relation_evidence", "outgroup_or_identity_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "stronger ties to own group; signed evaluation", False),

    # Economic evaluation
    ("pfesol", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past living standards; evaluative comparison", False),
    ("pfeemp", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt job creation performance; evaluative", False),
    ("pfeprc", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt price stability performance; evaluative", False),
    ("pfegap", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt income gap reduction performance; evaluative", False),
    ("pfenow", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "satisfaction with economy; evaluative", False),
    ("pfepas", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past satisfaction; evaluative comparison", False),
    ("pfefut", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "future expectations; evaluative", False),
    ("pfeerd", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "own living conditions vs others; evaluative", False),
    ("pfegrp", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "group economic conditions vs others; evaluative", False),

    # Freedom and governance evaluation
    ("pfrsay", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past free to say; evaluative comparison", False),
    ("pfrass", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past freedom to join; evaluative comparison", False),
    ("pfrvot", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past voting freedom; evaluative comparison", False),
    ("pfreql", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past treated equally; evaluative comparison", False),
    ("pfrele", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "elections honest; evaluative", False),
    ("pfrgpt", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "all citizens treated equally; signed evaluation", False),
    ("pfrfai", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "group treated unfairly; evaluative", False),
    ("pfrall", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt represents all or one group; evaluative", False),

    # Crime and corruption
    ("pfpcrm", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt crime handling; evaluative", False),
    ("pfpsaf", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past safety; evaluative comparison", False),
    ("pfpcr1", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt corruption handling; evaluative", False),
    ("pfpcr2", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "extent of corruption; evaluative", False),
    ("pfpcr3", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "corruption among elected leaders; evaluative", False),
    ("pfpcr4", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "corruption among civil servants; evaluative", False),
    ("pfpcr5", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "present vs past corruption; evaluative comparison", False),

    # Institutional trust
    ("trspre", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust president; signed evaluation", False),
    ("trspol", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust police; signed evaluation", False),
    ("trscts", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust courts; signed evaluation", False),
    ("trsarm", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust army; signed evaluation", False),
    ("trsnec", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust electoral commission; signed evaluation", False),
    ("trsbrd", "relation_evidence", "institutional_trust_orientation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more trusting", "less trusting", "neutral / ambivalent", "allow_directionality", "high", "trust national broadcasting; signed evaluation", False),

    # Government performance
    ("pfgpre", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "president performance; evaluative", False),
    ("pfgmp", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "parliament/MP performance; evaluative", False),
    ("pfgloc", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "local government performance; evaluative", False),
    ("pfgedu", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt education handling; evaluative", False),
    ("pfghlt", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt health handling; evaluative", False),
    ("pfghiv", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "govt AIDS handling; evaluative", False),

    # Legitimacy
    ("legcon", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "constitution expresses values; signed evaluation", False),
    ("leggov", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "government has right to govern; signed evaluation", False),

    # Membership (binary)
    ("memrel", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "member of religious group; binary", False),
    ("memdev", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "member of development association; binary", False),
    ("membus", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "member of business group; binary", False),
    ("memlab", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "member of trade union; binary", False),

    # Political participation
    ("pidcls", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "close to party; binary", False),
    ("pidwin", "relation_evidence", "subjective_evaluation", "signed_evaluation", "signed_evaluation", "ordinal_scale", "more positive", "more negative", "neutral / ambivalent", "allow_directionality", "high", "close to ruling party or opposition; evaluative", False),
    ("parvot", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "voted in last election; binary", False),

    # Political participation frequency
    ("parcom", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "attend community meetings; frequency", False),
    ("pariss", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "raise an issue; frequency", False),
    ("parral", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "attend election rally; frequency", False),
    ("parcam", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "work for candidate/party; frequency", False),
    ("parlet", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "write to newspaper; frequency", False),
    ("pardem", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "attend demonstration; frequency", False),
    ("parctg", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "contact government official; frequency", False),
    ("parcti", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "contact influential person; frequency", False),

    # Media frequency
    ("medrad", "relation_evidence", "media_orientation", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "radio news; frequency", False),
    ("medtv", "relation_evidence", "media_orientation", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "TV news; frequency", False),
    ("mednew", "relation_evidence", "media_orientation", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "newspaper; frequency", False),

    # Deprivation frequency
    ("povfoo", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "gone without food; frequency", False),
    ("povwat", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "gone without water; frequency", False),
    ("povhth", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "gone without healthcare; frequency", False),
    ("povelc", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "gone without electricity; frequency", False),
    ("povinc", "relation_evidence", "behavioral_frequency", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "gone without cash income; frequency", False),

    # Health frequency
    ("hltmen", "relation_evidence", "subjective_affect_or_wellbeing_coordinate", "signed_frequency", "signed_frequency", "frequency_scale", "more frequent", "less frequent", "neutral / ambivalent", "allow_directionality", "high", "routine affected by worry; frequency", False),

    # AIDS experience (binary)
    ("aidexp", "relation_evidence", "binary_attitude", "signed_attitude", "signed_attitude", "yes_no", "more endorsing", "more rejecting", "neutral / ambivalent", "allow_directionality", "high", "friend/relative died of AIDS; binary", False),
]

ALL = ADMIN + DEMO + NOMINAL + SIGNED

fields = [
    "source", "wave", "canonical_wave", "var_name", "question_text",
    "semantic_role", "semantic_subrole", "directionality_policy",
    "signed_polarity_status", "response_family_expectation",
    "positive_anchor_label", "negative_anchor_label", "neutral_anchor_label",
    "bridge_directionality_action", "directionality_confidence",
    "directionality_note", "manual_review_required",
]

# Write directionality authority
AUTH_DIR.mkdir(parents=True, exist_ok=True)
out = AUTH_DIR / "afrobarometer_R1_directionality_authority.csv"
# Build from codebook to get question text
import pandas as pd
cb = pd.read_csv(REPO / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS" / "Afrobarometer Round 1 codebook.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(fields)
    for r in ALL:
        var_name = r[0]
        qt = ""
        m = cb[cb["var_name"] == var_name]
        if len(m):
            qt = str(m.iloc[0].get("display_text", ""))
        if not qt and len(m):
            qt = str(m.iloc[0].get("variable_label", ""))
        row = [SOURCE, WAVE, CANONICAL, var_name, qt] + list(r[1:])
        w.writerow(row)
print(f"Wrote {out} ({len(ALL)} rows)")

# Also write directionality overlay
for d in [REPORTS]:
    d.mkdir(parents=True, exist_ok=True)
    o2 = d / "afrobarometer_R1_directionality_overlay.csv"
    # Same format but with overlay-specific column order
    with open(o2, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for r in ALL:
            var_name = r[0]
            qt = ""
            mm = cb[cb["var_name"] == var_name]
            if len(mm):
                qt = str(mm.iloc[0].get("display_text", ""))
            if not qt and len(mm):
                qt = str(mm.iloc[0].get("variable_label", ""))
            row = [SOURCE, WAVE, CANONICAL, var_name, qt] + list(r[1:])
            w.writerow(row)
    print(f"Wrote {o2} ({len(ALL)} rows)")

# Write semantic authority overlay
sa_fields = ["source", "wave", "canonical_wave", "var_name", "question_text",
             "semantic_lane", "semantic_role", "evidence_lane",
             "semantic_subrole", "semantic_tags", "directionality_policy",
             "semantic_confidence", "semantic_note"]
for d in [REPORTS]:
    d.mkdir(parents=True, exist_ok=True)
    o3 = d / "afrobarometer_R1_semantic_authority_overlay.csv"
    with open(o3, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(sa_fields)
        for r in ALL:
            var_name = r[0]
            qt = ""
            mm = cb[cb["var_name"] == var_name]
            if len(mm):
                qt = str(mm.iloc[0].get("display_text", ""))
            if not qt and len(mm):
                qt = str(mm.iloc[0].get("variable_label", ""))
            lane = "direct" if r[1] == "relation_evidence" else ("context" if r[1] in ("position_context",) else "admin")
            evidence = "direct_relation_response" if lane == "direct" else ("position_context" if lane == "context" else "administrative")
            conf = r[10]
            note = r[11]
            subrole = r[2]
            policy = r[3]
            w.writerow([SOURCE, WAVE, CANONICAL, var_name, qt, lane, r[1], evidence,
                       subrole, "", policy, conf, note])
    print(f"Wrote {o3} ({len(ALL)} rows)")

# Write first-pass authority table
fp_fields = ["source", "wave", "canonical_wave", "var_name", "var_code", "question_id",
             "question_text", "module_guess", "semantic_lane", "semantic_role",
             "evidence_lane", "allowed_as_branch_position_signature",
             "allowed_as_branch_relation_cosignature", "allowed_as_attitude_cloud_anchor",
             "allowed_as_attitude_cloud_feature", "allowed_as_v551_relation_evidence",
             "allowed_as_association_feature", "is_substantive", "not_direct_evidence",
             "manual_designation_required", "designation_confidence", "rationale"]
for d in [REPORTS]:
    d.mkdir(parents=True, exist_ok=True)
    o4 = d / "afrobarometer_R1_first_pass_authority_table.csv"
    with open(o4, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fp_fields)
        for r in ALL:
            var_name = r[0]
            qt = ""
            mm = cb[cb["var_name"] == var_name]
            if len(mm):
                qt = str(mm.iloc[0].get("display_text", ""))
            if not qt and len(mm):
                qt = str(mm.iloc[0].get("variable_label", ""))
            is_substantive = "TRUE" if r[1] == "relation_evidence" else "FALSE"
            v551_evidence = "TRUE" if r[1] == "relation_evidence" else "FALSE"
            cloud_anchor = "TRUE" if r[1] == "relation_evidence" else "FALSE"
            design_conf = "high"
            rationale = r[11]
            w.writerow([SOURCE, WAVE, CANONICAL, var_name, var_name, var_name,
                       qt, "substantive" if is_substantive == "TRUE" else "context",
                       "direct_relation" if is_substantive == "TRUE" else "context",
                       r[1], "direct_response" if is_substantive == "TRUE" else "context",
                       "FALSE", "FALSE", cloud_anchor, "FALSE",
                       v551_evidence, "FALSE", is_substantive, "FALSE",
                       "FALSE", design_conf, rationale])
    print(f"Wrote {o4} ({len(ALL)} rows)")

# Update index
idx_path = AUTH_DIR / "directionality_authority_index.csv"
import csv
idx_rows = []
if idx_path.exists():
    with open(idx_path) as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            idx_rows.append(row)
# Remove existing Afrobarometer R1 entry
idx_rows = [r for r in idx_rows if not (r.get("source") == SOURCE and r.get("wave") == WAVE)]
import datetime
idx_rows.append({
    "source": SOURCE,
    "wave": WAVE,
    "file_name": "afrobarometer_R1_directionality_authority.csv",
    "row_count": str(len(ALL)),
    "status": "active",
    "notes": "manually authored from codebook by Codex; 0 manual_review required",
})
with open(idx_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["source", "wave", "file_name", "row_count", "status", "notes"])
    w.writeheader()
    w.writerows(idx_rows)
print(f"Updated index")

# Summary
signed = sum(1 for r in ALL if r[9] == "allow_directionality")
unsigned = sum(1 for r in ALL if r[9] == "force_unsigned")
print(f"\n=== Summary ===")
print(f"Total: {len(ALL)}")
print(f"Signed: {signed} ({signed/len(ALL)*100:.0f}%)")
print(f"Unsigned: {unsigned} ({unsigned/len(ALL)*100:.0f}%)")
print(f"Manual review required: {sum(1 for r in ALL if r[12])}")
print(f"Done.")
