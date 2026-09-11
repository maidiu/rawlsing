# COMMISSION — SDTF R4 R1 RULE AUTHORITY BINDING

BRANCH: `agent/rabochii-hq-sdtf-r4-r1-rule-authority-binding-r1`

LAUNCH BASE: `315ec8ba942cbf356bf1ef57471441299ae1a875`

AUTHORIZED GRAIN:
`SDTF_R4_MECHANISM_RULE_ADMISSION_CURRENTNESS_AND_EVIDENCE_AUTHORITY_BINDING_R1_ONLY`

AUTHORITY:
- HQ-adopted R4 seam constitution + reviewed companion;
- gap-audit return `84dfab0dc88b06261dc495cc30796b2154419621`;
- HQ gap-audit adoption File 06.

MISSION:
Implement the smallest generalized authority/current-selection envelope for concrete future R4 mechanism rules, combining G1 + generic G6 evidence-authority binding. Reuse project-current authority patterns; do not create a second parallel authority stack.

REUSE, DO NOT REPLACE:
- `rawlsing_next/pre553_empirical_authority.py` blob `c824bcf17257c0318e86497fc12ee31101bb6daf`
- `rawlsing_next/pre553_empirical_objects.py` blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`
- `rawlsing_next/gt34_d08_empirical_predicate_grammar_authority.py` blob `4b162386c3c473b4ae0a4bf61de21e7cd62672ed`
- `rawlsing_next/gt12_permission_translation_authority.py` blob `2eb1441e0ee5be3eef2567f8ffb57819fc47f0d6`
- `rawlsing_next/bounded_empirical_runtime.py` blob `5677751c36a8cd15daa7679232126a4ab69bdd89`
- `rawlsing_next/pre553_source_local_universe_admission.py` blob `b968fa16c6620cd06b191ebdb5da7da86f524393`

REQUIRED SEMANTICS:
- constitution currentness != rule currentness;
- exact rule id/version/content identity + P1-P5 class/composition identity;
- source/claim/evidence-status/normalized-mechanism trace refs;
- measurement/estimand/identification/portability/currentness ceilings where applicable;
- competent causal-use authority ref;
- calibration authority required for numeric rules; explicit N/A for nonnumeric rules;
- fail closed on missing/ambiguous owner, version, causal-use, or required calibration authority.

PROHIBITED:
- no concrete mechanism rules;
- no coefficients/probabilities/thresholds;
- no actor facts;
- no calibration choices;
- no OBL063 defaults as authority;
- no OBL062 closure;
- no main/HQ mutation.

Tests may be added/updated only as required for this bounded implementation.

PASS:
`SDTF_R4_R1_MECHANISM_RULE_AUTHORITY_BINDING_IMPLEMENTED__READY_FOR_INTEGRATION_QUALIFICATION`

BLOCKER:
`SDTF_R4_R1_MECHANISM_RULE_AUTHORITY_BINDING__EXACT_IMPLEMENTATION_OR_AUTHORITY_BLOCKER_PROVED`

Commit the governed return with exact changed-file identities, tests, and remaining boundaries.