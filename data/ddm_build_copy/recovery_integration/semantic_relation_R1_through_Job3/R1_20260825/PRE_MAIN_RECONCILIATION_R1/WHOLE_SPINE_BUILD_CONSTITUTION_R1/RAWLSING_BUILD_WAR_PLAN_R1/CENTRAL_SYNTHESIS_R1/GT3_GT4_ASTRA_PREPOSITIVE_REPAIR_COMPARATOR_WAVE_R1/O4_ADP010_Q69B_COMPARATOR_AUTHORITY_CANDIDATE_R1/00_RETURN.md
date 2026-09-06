# GT3/GT4 O4 — ADP-010 <-> Q69B FIELD-SPECIFIC COMPARATOR AUTHORITY CANDIDATE R1

## Terminal

PASS__GT34_O4_ADP010_Q69B_FIELD_SPECIFIC_COMPARATOR_AUTHORITY_CANDIDATE_DEFINED__NO_ADOPTION

## Execution boundary

- repository: maidiu/rawlsing
- branch: agent/rabochii-gt34-o4-adp010-q69b-comparator-authority-candidate-r1
- exact working-ancestry start: 3aaf6759f270c9b730db5d09bb6a87f92ec34345
- immutable instruction ref, evidence only: 15f1a470843ffe322c054a115c0685cb8a4e26e8
- instruction blob: 9fbafb5fbae85bda28c1c577a9fd0bf85e868dd5
- worker: O4 — ADP-010 <-> Q69B FIELD-SPECIFIC COMPARATOR AUTHORITY CANDIDATE R1
- production implementation: NONE
- adoption: NONE
- PSEPF: NONE
- metabolism authority: NONE
- CAN-008 authority: NONE
- positive actor mutation: NONE

The worker branch was verified identical to the mandated starting SHA before this work began.

No concurrent O1/O2/O3 result is consumed. This candidate is explicitly conditional on later HQ adoption of the exact Q69B authority/release identities already banked at the common start.

---

## 1. Holding

The first exact OBL031 field-specific comparator authority can now be defined at one field only:

accepted ADP-010 V3OEERealizationRecord
with
realization_state = ENCOUNTER
and
event_effect_kind = OEE_ENCOUNTER_OCCURRED
and
an exact independently-owned subject semantic proof of public-clinic-or-hospital contact/use
and
an exact actor event time

->
respondent-specific temporal comparison under the exact Q69B DATEINTR-anchored source-native PAST_12_MONTHS rule

->
exact D08 EmpiricalPredicate selecting the canonical Q69B value PUBLIC_CLINIC_EXPERIENCE_PRESENT, scoped only to the exact respondents whose Q69B DATEINTR window unambiguously contains the actor encounter time

plus

COMPARATOR_PROVENANCE_RECEIPT.

This is not a generic actor<->survey comparator framework.

The mapping is exactly one-directional and one-field:

ADP010_PUBLIC_CLINIC_OR_HOSPITAL_ENCOUNTER_IN_RESPONDENT_DATEINTR_WINDOW
->
Q69B_PUBLIC_CLINIC_EXPERIENCE_PRESENT.

The named Q69B medicine/supplies problem is not transferred into actor history.

Exposure is not required.

No actor-side ABSENT comparator is defined.

Silence in actor history is not negative evidence.

---

## 2. Frozen accepted/banked evidence

### Actor owner

Accepted owner:

V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0

Accepted authority artifact blob:

0eac41d081b112255dcfc6dd42a6afab15a2928b

Accepted record family:

V3OEERealizationRecord

Exact positive state:

ENCOUNTER

Exact event effect:

OEE_ENCOUNTER_OCCURRED

ADP-010 itself states ENCOUNTER means an admitted contact occurrence under opportunity and does not imply exposure or downstream psyche/history.

### L1A relation proof

GT34_L1A_Q69B_TO_ADP010_ENCOUNTER_RELATION_PROOF@1.0.0

hash:

7eaa5197a26c3e5ddc65b631453007f2a5ed9ba9310da6c9c233eaef6fb12aa9

That predecessor proof already freezes:
- exact ADP-010 ENCOUNTER;
- OEE_ENCOUNTER_OCCURRED;
- independently-owned public-clinic-or-hospital subject semantics;
- exact temporal alignment;
- no medicine/supplies-problem promotion;
- no survey->actor direction;
- no actor silence->empirical ABSENT inference.

### Q69B source/release

Source snapshot:

Data/Afro Barometer Round 5.sav

SHA-256:

c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651

Rows:

51,587

Empirical universe hash:

4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1

Candidate release ID:

R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1

Frozen handoff/source-release-manifest hash:

15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4

N2 final release semantic hash:

2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec

N2 replay manifest hash:

8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539

### Q69B coordinate

Coordinate:

Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS

hash:

7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937

Repaired coordinate authority:

R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY@1.0.0

hash:

cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c

Crosswalk:

R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_STATUS_CROSSWALK@1.0.0

hash:

fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095

Time authority:

R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR@1.0.0

hash:

4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2

Raw conditioner measure basis:

R5_Q69B_RAW_CONDITIONER_MEMBERSHIP_BASIS@1.0.0

hash:

f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3

Currentness hash:

467a98d69e49a715527c79f35dbfe65dc95bfbfee7ae455053465b8b438c3a08

Native codes:
- 0/1/2/3 -> PUBLIC_CLINIC_EXPERIENCE_PRESENT
- 7 -> PUBLIC_CLINIC_EXPERIENCE_ABSENT
- 9 -> UNKNOWN
- 998 -> REFUSAL_NOT_LAWFULLY_CONDITIONABLE
- -1 -> MISSING

The 0/1/2/3 frequency order is not used by this comparator.

### D08 / PRE553 grammar evidence

Accepted D08 empirical-fact-algebra evidence blob:

c766f4b0d6ade72a56e921e6d03aa3dc20fba68c

Current EmpiricalPredicate schema blob:

91974c52ce8c0acafa939be0d7d83f4a5c8085b7

Current predicate evaluator blob:

902b179817f02a46fc0844971f268113123347f4

D08 owns the typed empirical predicate grammar, including EMPIRICAL_POSITION_COORDINATE leaves. O4 does not become predicate-grammar authority.

At positive resolution, the produced EmpiricalPredicate must carry an exact accepted-current AuthorityRef whose authority kind is PREDICATE_GRAMMAR, whose governed family includes EmpiricalPredicate@1.0.0, and whose exact scope permits this D08 EMPIRICAL_POSITION_COORDINATE EQ predicate.

No default/latest/fuzzy/nearest or scope-incompatible grammar authority is permitted.

Because O4 performs no positive execution, no runtime predicate instance and therefore no runtime grammar AuthorityRef instance is emitted in this worker. The exact accepted grammar ref is a mandatory positive invocation binding and must be persisted in the comparator receipt.

---

# 3. Content-addressing law

Every O4 semantic object below uses:

- SHA-256;
- UTF-8;
- lexicographically ascending mapping keys;
- compact comma/colon JSON separators;
- exact sequence order for semantically ordered sequences;
- set-like normalization only where the schema explicitly marks a field set-like;
- exclusion only of the object's own derived content-hash field from its own semantic projection.

No caller-selected projection is permitted.

---

# 4. Subject semantic requirement

Object:

GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.0.0

semantic hash:

78a7418047dd6ac0b9685d2466eb9ec9892ba9279b2470c768493954c22f1374

Exact semantic projection:

{
  "actor_record_field": "subject_ref",
  "content_addressing_law": {
    "algorithm": "SHA-256",
    "derived_hash_field_rule": "EXCLUDE_ONLY_THE_OBJECTS_OWN_DERIVED_CONTENT_HASH_FROM_ITS_SEMANTIC_PROJECTION",
    "encoding": "UTF-8",
    "mapping_key_order": "LEXICOGRAPHIC_ASCENDING",
    "ordered_sequences": "PRESERVE_EXACT_ORDER",
    "separators": "COMPACT_COMMA_COLON",
    "set_like_collections": "SORT_BY_CANONICAL_JSON_AND_DEDUPLICATE_ONLY_WHERE_SCHEMA_MARKS_SET_LIKE"
  },
  "does_not_assert": [
    "MEDICINE_OR_SUPPLIES_PROBLEM",
    "EXPOSURE",
    "AWARENESS",
    "BELIEF",
    "MEMORY",
    "RESPONSE"
  ],
  "failure": "NONCOMPARABLE_SUBJECT",
  "owner_law": [
    "SUBJECT_REF_MUST_BE_EXACT_CONTENT_ADDRESSED",
    "SUBJECT_REF_MUST_RESOLVE_UNDER_ITS_OWN_SEPARATELY_ACCEPTED_CURRENT_SEMANTIC_OWNER",
    "THE_SUBJECT_OWNER_NOT_ADP010_AND_NOT_THIS_COMPARATOR_MUST_AUTHORIZE_THE_EXACT_PUBLIC_CLINIC_OR_HOSPITAL_CONTACT_OR_USE_PROPOSITION",
    "LEXICAL_LABEL_SIMILARITY_CATEGORY_SIMILARITY_COLOCATION_OR_INSTITUTION_CLASS_ALONE_IS_INSUFFICIENT",
    "THE_EXACT_SUBJECT_REF_OWNER_AUTHORITY_REF_AND_PROPOSITION_PROOF_HASH_MUST_ENTER_THE_COMPARATOR_RECEIPT"
  ],
  "positive_relation_ceiling": "CONTACT_OR_USE_OF_PUBLIC_CLINIC_OR_HOSPITAL_ONLY",
  "required_subject_proposition": "PUBLIC_CLINIC_OR_HOSPITAL_CONTACT_OR_USE",
  "schema": "GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.0.0"
}

This does not invent an institution taxonomy.

It requires the input record's own independently accepted subject semantic owner to prove the proposition exactly.

If that proof cannot be resolved, the comparator returns NONCOMPARABLE_SUBJECT and emits no predicate.

Therefore the handoff's subject-semantics blocker is avoided without semantic laundering.

---

# 5. Temporal comparability rule

Object:

GT34_ADP010_Q69B_DATEINTR_TEMPORAL_COMPARABILITY_RULE@1.0.0

semantic hash:

2a67c53125bd4892fa562306edd89cc2a69324958eea3364657b6aa776f86fa2

Exact semantic projection:

{
  "accepted_time_authority_ref": {
    "authority_content_hash": "4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2",
    "authority_id": "R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR",
    "authority_version": "1.0.0"
  },
  "actor_time_source": {
    "evidence_query_proxy_time_substitution": "FORBIDDEN",
    "field": "effective_from",
    "record_family": "V3OEERealizationRecord",
    "required_event_effect_kind": "OEE_ENCOUNTER_OCCURRED"
  },
  "content_addressing_law": {
    "algorithm": "SHA-256",
    "derived_hash_field_rule": "EXCLUDE_ONLY_THE_OBJECTS_OWN_DERIVED_CONTENT_HASH_FROM_ITS_SEMANTIC_PROJECTION",
    "encoding": "UTF-8",
    "mapping_key_order": "LEXICOGRAPHIC_ASCENDING",
    "ordered_sequences": "PRESERVE_EXACT_ORDER",
    "separators": "COMPACT_COMMA_COLON",
    "set_like_collections": "SORT_BY_CANONICAL_JSON_AND_DEDUPLICATE_ONLY_WHERE_SCHEMA_MARKS_SET_LIKE"
  },
  "empirical_time_source": {
    "field": "effective_or_reference_time",
    "physical_anchor": "DATEINTR",
    "record_family": "EmpiricalCoordinateFact@1.0.0",
    "source_native_interval": "PAST_12_MONTHS"
  },
  "membership_law": [
    "FOR_EACH_EXACT_Q69B_COORDINATE_USE_THAT_COORDINATES_OWN_DATEINTR_ANCHOR",
    "INCLUDE_RESPONDENT_IN_TEMPORALLY_COMPARABLE_SCOPE_ONLY_IF_THE_ACCEPTED_Q69B_TIME_RULE_PROVES_ACTOR_ENCOUNTER_TIME_IN_WINDOW_UNAMBIGUOUS",
    "DO_NOT_INVENT_SOURCE_NATIVE_LOWER_EDGE_INCLUSION",
    "ANY_CASE_DEPENDING_ON_DISPUTED_EDGE_INCLUSION_OR_INSUFFICIENT_TIME_GRANULARITY_IS_NONCOMPARABLE_NOT_MATCH_OR_NO_MATCH",
    "QUERY_TIME_WALL_CLOCK_AND_ACTOR_CURRENT_TIME_SUBSTITUTION_ARE_FORBIDDEN",
    "TEMPORAL_SCOPE_MEMBER_SET_IS_CONTENT_ADDRESSED_AND_SORTED_BY_EXACT_RESPONDENT_REF"
  ],
  "per_respondent_relation_states": [
    "IN_WINDOW_UNAMBIGUOUS",
    "OUTSIDE_WINDOW_UNAMBIGUOUS",
    "NONCOMPARABLE_BOUNDARY_OR_GRANULARITY",
    "UNRESOLVED_TIME_AUTHORITY_OR_INTEGRITY"
  ],
  "positive_scope_law": "AT_LEAST_ONE_IN_WINDOW_UNAMBIGUOUS_RESPONDENT_REQUIRED_FOR_PREDICATE_PRODUCTION",
  "schema": "GT34_ADP010_Q69B_DATEINTR_TEMPORAL_COMPARABILITY_RULE@1.0.0",
  "zero_positive_scope_outcome": "NONCOMPARABLE_TIME"
}

The important noncollapse is respondent-specific time.

N2 materialized every Q69B coordinate with its own respondent DATEINTR as effective_or_reference_time.

O4 therefore does not pretend all R5 respondents share one anchor date.

The actor event time is compared to each respondent coordinate's own source-native twelve-month window.

Cases whose inclusion depends on an unspecified source-native lower-edge convention are not guessed; they are typed NONCOMPARABLE.

The resulting exact temporally-comparable respondent member set becomes a content-addressed scope ref on the predicate.

No new temporal predicate leaf is invented.

---

# 6. Exact D08 predicate construction

Object:

GT34_ADP010_Q69B_PRESENT_D08_PREDICATE_CONSTRUCTION@1.0.0

semantic hash:

042bb34c596ccdf86803e08a6d58c52bb0bec044df0e809afc7b65fef7e06dbe

Fixed predicate AST hash:

d11f3d42cddb2f1eccf58f2f5d7727371a8af0573a0d105c70476cd137f3b7cb

Exact operator ref:

D08:EMPIRICAL_POSITION_COORDINATE:EQ

operator-ref hash:

23245d3a8ab3545707768eb85df600c8507366736f7f2b32a8c0ca7be7151708

Exact canonical PRESENT value ref:

Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_PRESENT

value-ref hash:

f2317b8c2ab4a3238e030a1ecdd995e6496b1c306703e654864cfd581325ded7

Typed-state policy ref:

R5_Q69B_PRESENT_CONDITIONER_POLICY@1.0.0

policy-ref hash:

dfbe0f6f0119badc64e25acad89da76076b8f9a9a1d9dd862792612e279384a2

Exact fixed predicate AST:

{
  "comparison_operator_ref": {
    "content_hash": "23245d3a8ab3545707768eb85df600c8507366736f7f2b32a8c0ca7be7151708",
    "kind": "COMPARISON_OPERATOR",
    "object_id": "D08:EMPIRICAL_POSITION_COORDINATE:EQ"
  },
  "coordinate_authority_ref": {
    "authority_content_hash": "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c",
    "authority_id": "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY",
    "authority_version": "1.0.0"
  },
  "coordinate_semantic_ref": {
    "content_hash": "7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937",
    "kind": "COORDINATE_NATIVE",
    "object_id": "Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS"
  },
  "empirical_universe_ref": {
    "content_hash": "4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1",
    "kind": "EmpiricalUniverse@1.0.0",
    "object_id": "urn:rawlsing:pre553:EmpiricalUniverse:sha256:4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1"
  },
  "exact_values": [
    "PUBLIC_CLINIC_EXPERIENCE_PRESENT"
  ],
  "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
  "op": "LEAF",
  "operator": "EQ",
  "typed_state_policy_ref": {
    "content_hash": "dfbe0f6f0119badc64e25acad89da76076b8f9a9a1d9dd862792612e279384a2",
    "kind": "TYPED_STATE_POLICY",
    "object_id": "R5_Q69B_PRESENT_CONDITIONER_POLICY@1.0.0"
  },
  "value_or_value_set_ref": {
    "content_hash": "f2317b8c2ab4a3238e030a1ecdd995e6496b1c306703e654864cfd581325ded7",
    "kind": "EMPIRICAL_COORDINATE_VALUE",
    "object_id": "Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_PRESENT"
  }
}

The complete runtime EmpiricalPredicate additionally must bind:
- an exact accepted-current PREDICATE_GRAMMAR AuthorityRef;
- the exact Q69B coordinate/value/operator refs above;
- the exact empirical universe;
- the Q69B candidate/adopted release;
- the exact content-addressed temporally-comparable respondent scope produced from the actor event and respondent DATEINTR anchors;
- same-respondent semantics tying the Q69B coordinate to that temporal scope;
- no weights.

The full runtime predicate object gets its own content hash over all of those fields.

The AST hash remains the fixed hash above.

This keeps temporal comparability in exact predicate scope while leaving the D08 coordinate grammar itself unchanged.

No native 0/1/2/3 ordering appears in the predicate.

---

# 7. Comparator rule

Rule:

GT34_ADP010_PUBLIC_CLINIC_ENCOUNTER_TO_R5_Q69B_PRESENT_D08_COMPARATOR_RULE@1.0.0

semantic hash:

7aef68630e4f87fca9c2826ab3b71f61a20c8f5a1e70f3698dae813cbafaed5a

Exact actor input:
- V3OEERealizationRecord;
- owner V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0;
- accepted authority artifact blob 0eac41d081b112255dcfc6dd42a6afab15a2928b;
- realization_state ENCOUNTER;
- event_effect_kind OEE_ENCOUNTER_OCCURRED;
- exact actor_id;
- exact record_id/hash;
- exact subject_ref;
- exact effective_from/time_granularity;
- exact rule id/version;
- exact event id;
- exact prior ledger anchor;
- exact replay/provenance.

Exposure is not required.

Exact subject rule:
GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.0.0
78a7418047dd6ac0b9685d2466eb9ec9892ba9279b2470c768493954c22f1374

Exact temporal rule:
GT34_ADP010_Q69B_DATEINTR_TEMPORAL_COMPARABILITY_RULE@1.0.0
2a67c53125bd4892fa562306edd89cc2a69324958eea3364657b6aa776f86fa2

Exact empirical binding:
- source c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651;
- release manifest 15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4;
- release semantic 2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec;
- universe 4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1;
- coordinate 7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937;
- coordinate authority cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c;
- crosswalk fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095;
- time authority 4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2;
- measure f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3;
- N2 replay 8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539;
- currentness 467a98d69e49a715527c79f35dbfe65dc95bfbfee7ae455053465b8b438c3a08;
- portability NONE;
- pooling NONE;
- weights NOT_APPLICABLE;
- frequency order false.

Exact relation:

ADP010_PUBLIC_CLINIC_OR_HOSPITAL_ENCOUNTER_IN_RESPONDENT_DATEINTR_WINDOW
->
Q69B_PUBLIC_CLINIC_EXPERIENCE_PRESENT

Relation kind:

SOURCE_SPECIFIC_SEMANTIC_EQUIVALENCE_PLUS_TEMPORALLY_CONDITIONAL_EQUIVALENCE

Direction:

ACTOR_FACT_TO_EMPIRICAL_CONDITIONER_PREDICATE_ONLY

The relation does not mean:
- actor encountered medicine/supplies problem;
- actor was exposed;
- survey response is actor history;
- actor probability is survey prevalence.

Positive outcome:

MATCH_PREDICATE_PRODUCED

Exact nonpositive outcomes:

- INELIGIBLE_ACTOR_FACT_NOT_EXACT_ADP010_ENCOUNTER
- NONCOMPARABLE_SUBJECT
- NONCOMPARABLE_TIME
- UNRESOLVED_ACTOR_FACT_AUTHORITY
- UNRESOLVED_SUBJECT_SEMANTIC_AUTHORITY
- UNRESOLVED_EMPIRICAL_AUTHORITY
- UNRESOLVED_D08_PREDICATE_GRAMMAR_AUTHORITY
- STALE
- NO_AUTHORIZED_NEGATIVE_COMPARATOR
- INTEGRITY_FAILURE

There is deliberately no generic NO_MATCH state.

---

# 8. Negative actor law

This comparator has no actor->Q69B ABSENT branch.

Exact law:

1. no ADP-010 encounter record is not evidence of no clinic/hospital encounter;
2. ADP-010 silence is not an empirical conditioner;
3. an ADP-010 NONOCCURRENCE decision is not silently widened into a separately authoritative subject-specific full-window nonoccurrence biography fact;
4. Q69B PUBLIC_CLINIC_EXPERIENCE_ABSENT may be targeted only by a separately accepted full-window actor nonoccurrence fact plus a separate comparator rule;
5. this O4 authority grants neither.

Therefore absence/silence yields no negative empirical predicate.

Where the caller attempts to use this rule as a negative comparator, the exact outcome is:

NO_AUTHORIZED_NEGATIVE_COMPARATOR.

---

# 9. Comparator provenance receipt

Receipt schema:

GT34_ADP010_Q69B_COMPARATOR_PROVENANCE_RECEIPT@1.0.0

Projection:

GT34_ADP010_Q69B_COMPARATOR_PROVENANCE_RECEIPT_SEMANTIC_PROJECTION@1.0.0

projection hash:

3ce38e06f24872a44a26a5b0c8236e60b0d1b0fece7468018d02a441c2187ef7

The receipt semantic projection binds exactly:

- receipt_schema
- decision_state
- actor_id
- actor_fact_ref
- actor_fact_record_hash
- actor_owner_authority_id
- actor_owner_authority_version
- actor_owner_authority_artifact_blob
- actor_rule_id_version
- actor_event_id
- actor_event_effect_kind
- actor_effective_time
- actor_time_granularity
- actor_prior_ledger_anchor_ref
- actor_replay_and_provenance_refs
- subject_ref
- subject_semantic_authority_ref
- subject_semantic_authority_content_hash
- subject_semantic_proposition_proof_hash
- comparator_authority_ref
- comparator_rule_ref
- comparator_rule_content_hash
- source_ref
- release_manifest_ref
- release_semantic_ref
- empirical_universe_ref
- q69b_coordinate_ref
- q69b_coordinate_authority_ref
- q69b_crosswalk_authority_ref
- q69b_time_authority_ref
- q69b_measure_basis_ref
- q69b_currentness_ref
- q69b_replay_manifest_hash
- d08_normative_owner_evidence_blob
- d08_predicate_grammar_authority_ref
- temporal_rule_ref
- temporal_scope_ref
- temporal_scope_member_set_hash
- temporal_scope_member_count
- temporal_relation_decision_receipt_hash
- predicate_construction_ref
- predicate_ast_hash
- resolved_predicate_ref
- resolved_predicate_content_hash
- negative_or_noncomparability_refs
- integrity_state

Set-like:
- actor_replay_and_provenance_refs
- negative_or_noncomparability_refs

Derived field excluded only from its own projection:

receipt_content_hash

Hash formula:

SHA256(UTF8(CANONICAL_JSON(EXACT_REQUIRED_SEMANTIC_FIELDS_EXCEPT_RECEIPT_CONTENT_HASH)))

Positive receipt requirements:
- decision_state = MATCH_PREDICATE_PRODUCED;
- exact actor record and ADP-010 owner verify;
- exact independently-owned subject semantics verify;
- temporal scope has at least one unambiguous in-window respondent;
- exact HQ-adopted/current Q69B identities verify;
- exact accepted-current D08/PRE553 PREDICATE_GRAMMAR authority verifies;
- resolved predicate AST hash equals d11f3d42cddb2f1eccf58f2f5d7727371a8af0573a0d105c70476cd137f3b7cb;
- resolved predicate scope binds the exact temporal scope.

All negative receipts use the same content-addressing projection.

---

# 10. Comparator authority candidate

Authority:

GT34_ADP010_Q69B_FIELD_SPECIFIC_COMPARATOR_AUTHORITY@1.0.0

semantic hash:

bd834c596f308196eead8ce0db9b5414e3f5f2ed91506b8ca0bdd1774a4b7c5d

Status:

CANDIDATE_NOT_ADOPTED

Jurisdiction:

ONE_FIELD_ONLY__EXACT_ACCEPTED_ADP010_PUBLIC_CLINIC_OR_HOSPITAL_ENCOUNTER_TO_EXACT_AFROBAROMETER_R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRESENT_D08_CONDITIONER

Subordinate semantic refs:

- subject requirement:
  78a7418047dd6ac0b9685d2466eb9ec9892ba9279b2470c768493954c22f1374
- temporal rule:
  2a67c53125bd4892fa562306edd89cc2a69324958eea3364657b6aa776f86fa2
- predicate construction:
  042bb34c596ccdf86803e08a6d58c52bb0bec044df0e809afc7b65fef7e06dbe
- comparator rule:
  7aef68630e4f87fca9c2826ab3b71f61a20c8f5a1e70f3698dae813cbafaed5a
- receipt projection:
  3ce38e06f24872a44a26a5b0c8236e60b0d1b0fece7468018d02a441c2187ef7
- fixed D08 predicate AST:
  d11f3d42cddb2f1eccf58f2f5d7727371a8af0573a0d105c70476cd137f3b7cb

Positive output ceiling only:

EXACT_D08_EMPIRICAL_PREDICATE
+
COMPARATOR_PROVENANCE_RECEIPT

Authority law:

- NO_GENERIC_COMPARATOR_REGISTRY_OR_FRAMEWORK_IS_CREATED
- NO_OTHER_ACTOR_FACT_FAMILY_OR_SURVEY_FIELD_IS_IN_SCOPE
- POSITIVE_OUTPUT_REQUIRES_ALL_EXACT_ACTOR_SUBJECT_TIME_EMPIRICAL_GRAMMAR_CURRENTNESS_AND_REPLAY_BINDINGS
- COMPARATOR_AUTHORITY_DOES_NOT_OWN_D08_PREDICATE_GRAMMAR
- COMPARATOR_AUTHORITY_DOES_NOT_OWN_Q69B_COORDINATE_SEMANTICS
- COMPARATOR_AUTHORITY_DOES_NOT_OWN_ADP010_EVENT_SEMANTICS
- NO_MATCH_BY_LABEL_FUZZY_NAME_CATEGORY_OR_ADJACENT_AUTHORITY
- NO_NEGATIVE_ACTOR_COMPARATOR_FROM_SILENCE
- NO_FREQUENCY_ORDER_USE
- NO_WEIGHTS
- NO_RNG

Conditional adoption gate:

The authority has zero lawful positive use until HQ adopts the exact Q69B coordinate authority and exact bounded-release identities already frozen above.

Any supersession or identity drift yields STALE or UNRESOLVED_EMPIRICAL_AUTHORITY, never fallback selection.

---

# 11. D08 predicate-grammar separation

The earlier M1A defect was exactly an attempt by Q69B coordinate semantics to govern EmpiricalPredicate.

O4 does not repeat that defect.

The Q69B coordinate authority governs only EmpiricalCoordinateFact@1.0.0 semantics and the exact D08 conditioner-use eligibility.

The comparator authority governs only the actor-fact -> empirical-conditioner mapping decision.

The D08/PRE553 predicate grammar remains separately owned.

A positive runtime predicate must carry the exact accepted-current grammar AuthorityRef and that same ref must be preserved in the comparator receipt.

If an exact compatible grammar authority cannot be resolved:

UNRESOLVED_D08_PREDICATE_GRAMMAR_AUTHORITY

and no predicate is emitted.

---

# 12. Replay law

A positive replay must:

1. replay the exact actor record, record hash, actor id, ADP-010 authority/version/artifact identity, actor rule, event id/effect, ledger anchor, and provenance;
2. verify realization_state ENCOUNTER and event_effect_kind OEE_ENCOUNTER_OCCURRED;
3. resolve the exact subject ref under its own separately accepted current semantic owner and reproduce the public-clinic-or-hospital contact/use proof;
4. verify actor effective time/granularity;
5. replay the exact Q69B source/release/universe/coordinate/crosswalk/time/measure/currentness/N2 identities;
6. reconstruct the per-respondent temporal membership decisions from each Q69B coordinate's own DATEINTR anchor under the exact time authority;
7. recompute the exact temporally-comparable respondent member-set hash;
8. resolve the exact accepted-current D08/PRE553 PREDICATE_GRAMMAR authority;
9. recompute the fixed AST hash:
   d11f3d42cddb2f1eccf58f2f5d7727371a8af0573a0d105c70476cd137f3b7cb;
10. rebuild the full EmpiricalPredicate with exact grammar and temporal scope refs and reproduce its content hash;
11. rebuild the comparator provenance receipt and reproduce its content hash.

Any divergence fails closed with no predicate and no downstream authority.

There is no RNG.

---

# 13. Nonownership ceiling

This candidate does not create or authorize:

- PSEPF;
- actor belief;
- actor knowledge;
- actor response;
- actor structural position;
- source portability;
- measurement equivalence;
- metabolism permission;
- CAN-008 authority;
- V3 mutation;
- V2 rendering;
- persona;
- memory;
- Q69B medicine/supplies problem as actor history;
- Q69B ABSENT from actor silence;
- generic actor-to-empirical comparability.

The only lawful semantic movement is:

already-lawful actor encounter fact
->
field-specific comparator decision
->
exact empirical predicate + receipt.

---

# 14. Why the two BLOCK outcomes do not apply

## Subject semantics

O4 does not require ADP-010 itself to own public-clinic/hospital taxonomy.

It requires:
- exact content-addressed subject_ref;
- its own separately accepted-current subject-semantic owner;
- exact owner ref/hash;
- exact proof that the subject means public-clinic-or-hospital contact/use.

No positive result exists without that proof.

Therefore subject semantics are bound exactly enough for a candidate and:

BLOCKED__GT34_O4_ADP010_PUBLIC_CLINIC_SUBJECT_SEMANTICS_NOT_EXACTLY_OWNED

does not apply.

## Temporal semantics

N2 physically materialized exact respondent DATEINTR anchors on every Q69B coordinate.

The exact Q69B time authority already freezes source-native PAST_12_MONTHS, forbids query/wall-clock substitution, and forbids invented disputed-edge inclusion.

O4 therefore defines a deterministic per-respondent temporal-scope resolver whose only positive membership is IN_WINDOW_UNAMBIGUOUS.

Disputed edge/granularity is NONCOMPARABLE_TIME.

Therefore:

BLOCKED__GT34_O4_ADP010_Q69B_TEMPORAL_COMPARABILITY_NOT_EXACTLY_OWNED

does not apply.

---

# 15. Exact candidate hash ledger

Subject semantic requirement:

78a7418047dd6ac0b9685d2466eb9ec9892ba9279b2470c768493954c22f1374

Temporal comparability rule:

2a67c53125bd4892fa562306edd89cc2a69324958eea3364657b6aa776f86fa2

D08 EQ operator ref:

23245d3a8ab3545707768eb85df600c8507366736f7f2b32a8c0ca7be7151708

Q69B PRESENT value ref:

f2317b8c2ab4a3238e030a1ecdd995e6496b1c306703e654864cfd581325ded7

Q69B PRESENT typed-state policy ref:

dfbe0f6f0119badc64e25acad89da76076b8f9a9a1d9dd862792612e279384a2

Fixed D08 predicate AST:

d11f3d42cddb2f1eccf58f2f5d7727371a8af0573a0d105c70476cd137f3b7cb

Predicate construction:

042bb34c596ccdf86803e08a6d58c52bb0bec044df0e809afc7b65fef7e06dbe

Comparator rule:

7aef68630e4f87fca9c2826ab3b71f61a20c8f5a1e70f3698dae813cbafaed5a

Receipt semantic projection:

3ce38e06f24872a44a26a5b0c8236e60b0d1b0fece7468018d02a441c2187ef7

Comparator authority candidate:

bd834c596f308196eead8ce0db9b5414e3f5f2ed91506b8ca0bdd1774a4b7c5d

All hashes were independently recomputed from the exact semantic projections under §3.

---

# 16. Final holding

The first exact field-specific comparator authority candidate is defined.

It is not adopted and is inoperative until HQ adopts the exact Q69B authority/release identities.

It accepts only an exact already-lawful ADP-010 ENCOUNTER with independently authoritative public-clinic-or-hospital subject semantics and exact event time.

It produces only a D08 empirical conditioner predicate selecting Q69B PUBLIC_CLINIC_EXPERIENCE_PRESENT within the exact respondent-specific DATEINTR temporal scope, plus a comparator provenance receipt.

It defines no actor-side negative comparator from silence.

It imports no medicine/supplies-problem content into actor history.

It creates no PSEPF, metabolism authority, CAN-008 authority, V3 mutation, belief, response, structural position, persona, or V2 authority.

PASS__GT34_O4_ADP010_Q69B_FIELD_SPECIFIC_COMPARATOR_AUTHORITY_CANDIDATE_DEFINED__NO_ADOPTION
