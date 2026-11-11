# Public API and Owner Receipt

## Contract

`M1_ADJUDICATION_CONTRACT_ID = PYAT_M1_LEARNED_EMPIRICAL_ADJUDICATION@1.0.0`

Default ceiling:

`LEARNED_EMPIRICAL_DISPOSITION_ONLY__NO_PRODUCT_RELEASE__NO_CURRENTNESS__NO_STRUCTURAL_ADMISSION__NO_CAUSAL_PROMOTION__NO_POPULATION_GENERALIZATION_BEYOND_BOUND_SCOPE__NO_PERSON_OR_V3_STATE`

## Exact logical objects

### M1FamilyRuleBinding@1.0.0

Carries exact:

- claim family and claim rule;
- validator AuthorityRef;
- selection purpose: `CURRENT_GOVERNED_USE` or `EXACT_PINNED_REPLAY`;
- exact current-selection authority when current governed use is claimed;
- applicability scope;
- allowed input object families/states;
- required prerequisite channels;
- required source-relation kinds;
- required measure/weight/estimand authorities;
- explicit coverage contract;
- uncertainty policy ref;
- output semantic contract;
- semantic ceiling;
- validator algorithm identity;
- validator parameter ref;
- replay contract ref;
- exact authority closure.

Its deterministic identity includes the validator authority and exact validator contract fingerprint.

### M1AdjudicationInputBundle@1.0.0

Carries full exact preimages for selected:

- DiscoveryResultReceipt objects;
- DiscoveryAuthority objects;
- EmpiricalFact objects;
- EmpiricalQuerySpec objects;
- EmpiricalPredicate objects;
- AuthoritySnapshot objects;

plus:

- exact evaluated-frontier refs;
- exact discovery replay refs;
- exact requested scope;
- typed prerequisite channels;
- extra dependency refs.

The bundle identity hashes the exact object preimages, not merely prose labels or counts.

### FamilyValidationResult@1.0.0

The family-specific validator returns only a typed result. M1 verifies it matches the exact binding.

It carries:

- exact family/rule/binding/validator identity;
- one outcome from:
  - RULE_SATISFIED
  - RULE_NOT_SATISFIED
  - ABSTAINED
  - BLOCKED
  - UNRESOLVED
  - INTEGRITY_FAILURE
- exact reason;
- optional P1 relation proposition identity;
- optional truth-bearing semantic claim identity;
- explicit assertion polarity/state;
- exact semantic ceiling;
- structured validator determinants;
- structured validator explanation;
- exact side-effect vocabulary.

A truth-bearing claim is accepted only when the binding's exact output semantic contract explicitly authorizes claim emission.

### LearnedEmpiricalDisposition@1.0.0

Carries separate axes for:

1. adjudication outcome; and
2. conserved evidence/authority states.

It contains exact refs/material for:

- binding and validator authority;
- current-selection authority or typed N/A;
- discovery receipts and authorities;
- facts, validation facts, queries and predicates;
- source universes, risk sets, topology, measure;
- measure/weight/estimand authorities;
- comparability/composition authorities;
- coverage claims/states;
- empirical state vector;
- authority state vector;
- support/uncertainty state;
- prerequisite channel states;
- blockers;
- semantic ceiling;
- authority closure;
- dependency closure;
- algorithm/parameter identity;
- determinant, explanation and replay refs.

M1 never automatically converts `RULE_NOT_SATISFIED` into negative semantic truth.

### M1DeterminantExplanationReceipt@1.0.0

Carries deterministic:

- input bundle ref and full preimage via determinant manifest;
- binding ref/preimage or exact typed absence;
- validator registration identity;
- FamilyValidationResult ref/preimage;
- all constitutive evidence refs;
- exact frontier/replay refs;
- coverage and conserved state vectors;
- prerequisite states;
- validator determinants;
- structured explanation;
- semantic ceiling;
- all-false downstream effect law.

It derives independent exact refs for:

- determinant manifest;
- explanation;
- adjudication replay.

## Validator registry law

`M1ValidatorRegistry` resolves only this immutable dispatch key:

`(claim_family_id, claim_rule_id, validator_authority_id, validator_authority_version, validator_authority_content_hash)`

The registered validator contract fingerprint, algorithm identity and parameter ref must exactly match the binding.

There is:

- no alias;
- no family-name heuristic;
- no "latest";
- no semver fallback;
- no default validator;
- no previous-success fallback.

## Generic constitutional gates

Before validator execution M1 verifies:

- exact public object identity;
- exact object authority closure;
- receipt -> discovery authority closure;
- receipt -> fact/validation fact closure;
- receipt -> query/predicate role closure;
- winning predicate closure;
- fact -> query/predicate closure;
- receipt dependency inclusion of exact authority/frontier/grammar/winning/fact refs;
- declared frontier identity;
- declared discovery replay identity;
- exact binding family/rule match;
- exact positive binding authority closure;
- explicit current-selection authority for CURRENT_GOVERNED_USE;
- exact scope applicability;
- exact allowed input states;
- explicit coverage allowance;
- every required prerequisite channel;
- required relation kinds;
- required measure/weight/estimand authorities;
- absence of upstream INTEGRITY_FAILURE before substantive validation.

Failures never trigger fallback.
