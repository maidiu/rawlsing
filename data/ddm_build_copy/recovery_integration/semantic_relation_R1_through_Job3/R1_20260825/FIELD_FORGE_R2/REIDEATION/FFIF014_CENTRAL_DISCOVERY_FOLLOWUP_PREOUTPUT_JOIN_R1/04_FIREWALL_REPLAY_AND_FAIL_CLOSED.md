# FFIF014 — RESULT FIREWALL, REPLAY, AND FAIL-CLOSED LAW R1

Status: `FROZEN_BEFORE_TARGET_OUTPUT`

## Result firewall

Before the seal of this court, neither the central join nor either prerequisite worker inspected or computed any predicate × `COUNTRY_ALPHA3` target distribution.

After seal, target outputs may not be used to:

- alter the 62,609-predicate roster;
- choose or replace `COUNTRY_ALPHA3`;
- add/delete/split/fuse a challenger;
- change the empirical unit/risk set;
- recode native states;
- add a support threshold;
- change the exact query relation;
- add weighting/materiality/stability criteria;
- reinterpret a zero or undefined state;
- introduce geometry/motif/field/pressure/causal/person semantics.

Any such mutation invalidates the court and requires a new pre-output freeze.

## Exact upstream hashes that must hold

- risk-set physical SHA-256: `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`
- selected response-facts SHA-256: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
- selected exposure-facts SHA-256: `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`
- frozen predicate-roster canonical SHA-256: `5bf42464f3ff93e97d80f8ce178d670aa7fee98d13144f9c2d29d4f59032bced`

Execution must fail closed on any drift.

## Replay oracle

The normalized canonical oracle is the complete 688,699-row predicate-country support matrix sorted by:

1. frozen predicate roster order;
2. frozen country lexical order.

Canonical fields:

`predicate_id,subset_size,subset_mask,variables,state_pairs_json,original_support,COUNTRY_ALPHA3,country_support,status`

Canonical serialization:

UTF-8 TSV; header present; LF line endings; integer supports in base-10; status exactly `OBSERVED_POSITIVE` or `OBSERVED_ZERO`; no locale-dependent formatting.

The execution must compute a semantic SHA-256 over canonical uncompressed bytes.

At least two independent deterministic realization paths must reproduce that semantic hash for challengers claiming exact representation. Reusing one already-materialized target file as the second path does not count as independent reconstruction.

## Required challenger semantics

### W1

Reconstruct predicate truth directly from the frozen predicate definitions against immutable producer-owned same-unit response facts, attach exact current `COUNTRY_ALPHA3`, and regenerate the complete oracle without any FIELD-FORGE-local predicate-membership table.

### W2

Use only frozen predicate identity/original support. If the external country joint relation cannot be derived, return `UNDEFINED_FOR_OBJECT` rather than fabricated counts.

### W3

Materialize the exact follow-up-specific predicate-country sufficient statistic from one lawful execution path, then independently reconstruct the normalized oracle from that sufficient statistic. Its ceiling is this Q1 only.

### W4

Materialize exact predicate/respondent membership and join to frozen `COUNTRY_ALPHA3`; independently regenerate the complete oracle.

### W5

Use the full lossless claim-relevant respondent state plus `COUNTRY_ALPHA3`; independently regenerate the complete oracle.

### W0

May serve a frozen final assertion cache but cannot satisfy AS07 independent regeneration. Do not call cache serving replay.

## Fail-closed statuses

Use these typed dispositions rather than architecture inference:

- `BLOCKED__DISCOVERY_PREDICATE_IDENTITY_UNRESOLVED`
- `BLOCKED__FOLLOWUP_OPERAND_IDENTITY_UNRESOLVED`
- `BLOCKED__SAME_UNIT_OR_EXPOSURE_UNRESOLVED`
- `BLOCKED__FOLLOWUP_QUERY_AUTHORITY_UNRESOLVED`
- `BLOCKED__PRODUCER_DEREFERENCE_OR_REPLAY_UNAVAILABLE`
- `CLOSURE_ABSTAIN__KNOWN_BLOCKED_CHALLENGER`
- `INVALID__RESULT_FIREWALL_BREACH`
- `INVALID__COMMON_INPUT_OR_RISK_SET_DIVERGENCE`
- `INVALID__REPLAY_OR_INTEGRITY_FAILURE`

A blocker cannot be converted into a W1 failure or evidence for persistence.

## Court ceiling

Even a complete exact W1 PASS proves only that FIELD-FORGE-local respondent membership is not universally necessary for lawful discovery-to-follow-up linkage under this frozen exact Q1 counterexample.

It does not prove arbitrary-future follow-up sufficiency, universal physical architecture, or general semantic equivalence among challengers.
