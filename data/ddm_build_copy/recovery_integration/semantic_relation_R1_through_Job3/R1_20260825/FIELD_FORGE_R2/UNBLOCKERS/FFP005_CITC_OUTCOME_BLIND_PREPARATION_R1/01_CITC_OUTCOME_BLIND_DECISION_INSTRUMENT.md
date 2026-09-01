# FFP005 — CITC OUTCOME-BLIND DECISION INSTRUMENT R1

Status: `PREPARED__NOT_ISSUED`

Authority lane: `FFC003 / CLAIM_MATERIALITY_AUTHORITY`

This instrument prepares the delegated court that will issue the first `CLAIM_INVARIANT_TOLERANCE_CONTRACT` (`CITC`). It does not itself assign a tolerance.

## 1. Preconditions to court opening

The materiality court must not adjudicate a row unless all of the following are available and immutable:

1. one exact first-claim `CLAIM_IDENTITY_MANIFEST` with a resolved proposition hash;
2. assertion-slot identity, empirical unit, population/risk set, estimand, scale/value domain, quantifier, conditioning/baseline if any, semantic-input hash, ordered TTAR sequence, and PRA-bound operand roles where applicable;
3. the claim's candidate invariant-by-loss-dimension rows;
4. source-native ancestry/replay refs;
5. relevant support/uncertainty contract or an explicit declaration that the row is deterministic/exact;
6. evidence refs capable of supporting the proposed criticality/tolerance judgment;
7. an independence attestation satisfying §6;
8. an outcome-blindness attestation satisfying §7.

If any claim identity field needed to determine materiality is unresolved, return `CITC_ROW_UNRESOLVED__CLAIM_PREMISE_MISSING`. Do not manufacture the premise in this court.

## 2. Admissible judgment types

### 2.1 Criticality judgment

Exactly one per assertion-slot/invariant/loss-dimension row:

- `CRITICAL_INVARIANT__ZERO_UNAUTHORIZED_LOSS`
- `BOUNDED_APPROXIMATION_ALLOWED`
- `INFORMATION_NOT_REQUIRED_BY_CLAIM`
- `TOLERANCE_AUTHORITY_UNRESOLVED`
- `NOT_APPLICABLE_TO_ASSERTION_SLOT`

No missing or undecided row defaults to bounded approximation.

### 2.2 Tolerance judgment

Exactly one compatible type per row:

- `EXACT_ZERO`
- `ABSOLUTE_MARGIN`
- `RELATIVE_MARGIN`
- `COMPONENTWISE_RULE`
- `SET_RECALL_RULE`
- `ORDER_OR_TOPOLOGY_RULE`
- `EQUIVALENCE_MARGIN_WITH_TEST`
- `NO_REQUIREMENT_FOR_CLAIM`
- `UNRESOLVED__NO_EXECUTION`

`EXACT_ZERO` is mandatory where the row is a hard-zero same-claim validity condition. `NO_REQUIREMENT_FOR_CLAIM` is not permission to erase information globally; it says only that the named invariant is not required to adjudicate this claim. `UNRESOLVED__NO_EXECUTION` closes the comparison gate until authority is supplied.

## 3. Invariants that cannot be traded away

For same-claim comparison, the court has no authority to convert the following identity conditions into compensable margins:

- empirical-unit identity;
- risk-set identity;
- estimand identity;
- semantic-input hash;
- ordered TTAR sequence bound by the CIM;
- source-native ancestry and replayability;
- constitutive special-state distinctions;
- assertion-slot identity;
- assertion scale/value-domain identity;
- PRA role identity when the operand is role-dependent.

When the proposition itself requires exact existence/configuration/connectivity/order-k identity, the corresponding invariant is also nontradeable. Examples include exact lawful state existence, exact constitutive configuration existence, exact minority-branch retention, exact topology/connectivity, and exact higher-order J.

A hard-zero failure is `INVALID__CRITICAL_INVARIANT_LOSS`. It cannot be averaged with another row and cannot be cured by superior performance elsewhere.

## 4. What may receive a tolerance

A nonzero numeric or typed tolerance is admissible only for a registered, measurable loss dimension and only where the assertion slot is approximate rather than exact. Candidate classes include, claim permitting:

- conditional-distribution error;
- bounded mass error where exact existence is separately preserved;
- higher-order configuration recall/error for an explicitly approximate configuration claim;
- contradiction-mass error where exact contradiction existence is not the claim;
- componentwise transport-signature error;
- authorized order violation or neighborhood distortion;
- target-specific reconstruction/fidelity error;
- inferential/equivalence margins under an authorized error model.

The following do not independently justify an empirical tolerance: estimation error alone, uncertainty width alone, predictive degradation for a nonpredictive claim, downstream query degradation, compression utility for a noncompression claim, storage cost, compute/latency cost, producer convenience, or interpretability.

Any aggregation rule must be separately authorized, limited to commensurable rows for the same proposition, and noncompensatory with respect to hard-zero rows. Default: typed vector, no scalar aggregation.

## 5. Evidence burden for each tolerance

Every nonzero tolerance must record at least one primary basis that actually bears on the named claim and dimension, plus any inferential evidence required by the row.

### 5.1 Claim-semantics basis

Required when logical materiality follows from the quantifier, assertion slot, exactness, or named invariant. Evidence: normalized proposition, CIM coordinates, invariant rationale, competent claim authority.

### 5.2 Source-measurement-resolution basis

Required when source granularity, native response distinctions, top-coding, harmonization, or measurement limits bound distinguishability. Evidence: source/codebook authority and source-native ancestry. Source resolution may establish what can be distinguished; it cannot by itself declare substantively important differences immaterial.

### 5.3 Design/error-model basis

Required for inferential resolution, confidence/equivalence procedures, or any tolerance whose application depends on sampling/design uncertainty. Evidence: governed design/weight/error model, assumptions, calibration where applicable, and the exact uncertainty procedure. Non-significance never establishes equality.

### 5.4 Claim-warranted substantive-minimum-effect basis

Admissible only where the normalized claim itself contains a decision-relevance margin. Evidence: substantive scale/estimand justification and explicit inclusion of that margin in claim identity. No universal default margin exists.

### 5.5 Frozen actor-independent analytic-purpose basis

Admissible only for a bounded, preregistered information requirement that predates view comparison. Evidence: exact query/analytic contract, claim scope, invariant rationale, and forbidden promotions. Consumer convenience cannot become general empirical truth.

Historical precedent or conventional statistical thresholds may support another basis but never close authority alone.

If the evidence does not justify the proposed type or magnitude, return `TOLERANCE_AUTHORITY_UNRESOLVED` / `UNRESOLVED__NO_EXECUTION`.

## 6. Independence from compared-view producers

The CITC adjudicator and any authority supplying the final materiality judgment must be independent of the producers of the compared views for this claim.

Required rules:

- view producers may supply immutable view contracts, transformation/loss manifests, measurement facts, and raw realized dimension values only after freeze where needed for later application;
- a producer may not propose, vote on, narrow, widen, or reinterpret the cross-view tolerance for its own or a rival view;
- no producer-specific tolerance is permitted for views answering the same assertion slot;
- CVCR has application authority only and may not mint or revise a margin;
- TTAR may certify transformation scope/loss but not tolerability;
- PRA may certify role semantics but not tolerability;
- downstream/engineering authorities may set utility or cost requirements only after empirical sufficiency and may not revise the CITC;
- conflicts of role must be resolved by recusal or transfer to a competent independent materiality adjudicator before freeze.

The freeze receipt must identify the adjudicating authority, all evidence suppliers with a view-production role, and the independence disposition.

## 7. Outcome-blind freeze procedure

The first-claim CITC becomes eligible for later comparison only through this sequence:

1. `IDENTIFY_CLAIM`: bind the exact CIM/proposition hash and all claim-constitutive coordinates.
2. `ENUMERATE_ROWS`: enumerate all assertion-slot/invariant/loss-dimension rows before opening any compared-view outcome.
3. `CLASSIFY_CRITICALITY`: assign one §2.1 state per row from claim/evidence authority.
4. `SELECT_TOLERANCE_TYPE`: assign one §2.2 type per row.
5. `JUSTIFY_RULE`: record unit/scale, direction of worse loss, candidate value/rule if and only if lawfully adjudicated later, uncertainty interaction, aggregation rule or `NONE`, authority basis, authority ref, and evidence refs.
6. `HOSTILE_REVIEW`: test explicitly for producer capture, preferred-view rescue, minority-prevalence postselection, metric switching, asymmetric thresholds, and utility-to-truth laundering.
7. `BLINDNESS_ATTESTATION`: attest that no FFX002 compared-view outputs, agreement/disagreement states, fit metrics, compression results, predictive results, interpretability assessments, or preferred-view performance were available to or inspected by the adjudicator in determining materiality.
8. `CANONICALIZE`: canonicalize the completed CITC and compute its immutable contract hash.
9. `FREEZE_RECEIPT`: bind the contract hash, proposition hash, authority refs, evidence refs, adjudicator identity/role, independence disposition, and an explicit list/hash of outcome refs that were unavailable/unopened at freeze.
10. `RELEASE_FOR_COMPARISON`: only after steps 1–9 may compared-view outcomes be opened for CVCR application.

For this FFP005 preparation, step 5 stops before any final tolerance value/rule is assigned. The prepared template therefore carries `UNSET__FFP005_PREPARATION_ONLY` in every final-value field.

Any change after step 9 creates a new comparison-claim version with a new CITC hash and requires replay from immutable raw outputs. The prior frozen result remains historical fact and may not be overwritten.

## 8. No retroactive cures

The following propositions are absolute for this court:

`DOWNSTREAM_AGREEMENT_DOES_NOT_CURE_INVALIDITY`

`FIT_DOES_NOT_CURE_INVALIDITY`

`COMPRESSION_DOES_NOT_CURE_INVALIDITY`

`PREDICTIVE_VALUE_DOES_NOT_CURE_INVALIDITY_EXCEPT_WHERE_THE_CLAIM_IS_THE_EXACT_PREDICTIVE_CLAIM`

`INTERPRETABILITY_DOES_NOT_CURE_INVALIDITY`

`ENGINEERING_PREFERENCE_DOES_NOT_CURE_INVALIDITY`

A later result may show an object useful, predictive, compact, legible, fast, or mutually agreeable while it remains claim-insufficient. The legal order is empirical view-role sufficiency -> claim sufficiency/materiality -> downstream utility -> engineering preference. Later stages cannot run backward and confer authority on earlier failures.

## 9. Court outputs

The later delegated court may issue only:

- a frozen, fully evidenced CITC row/contract;
- `CITC_ROW_UNRESOLVED__CLAIM_PREMISE_MISSING`;
- `CITC_ROW_UNRESOLVED__EVIDENCE_INSUFFICIENT`;
- `CITC_FREEZE_BLOCKED__INDEPENDENCE_FAILURE`;
- `CITC_FREEZE_BLOCKED__OUTCOME_BLINDNESS_NOT_PROVED`;
- `CITC_PREPARED__AWAITING_FINAL_TOLERANCE_ADJUDICATION`.

This preparation issues the last state only.
