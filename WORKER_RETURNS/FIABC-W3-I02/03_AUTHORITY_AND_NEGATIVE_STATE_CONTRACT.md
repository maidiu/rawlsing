# FIABC-W3-I02 — Authority and Negative-State Contract

## Authority chain for numerical effective-N

A `SUPPORTED` effective-N product requires closure across four distinct layers.

### 1. I03 empirical/query authority

The exact `EmpiricalFact` and `EmpiricalQuerySpec` must retain positive exact authority closure. Their exact identities must agree on:

- query ref;
- source-universe set;
- risk-set ref;
- condition-predicate ref;
- measure-basis ref;
- measure kind.

The exact source release refs supplied to F018 must already occur in the I03 fact provenance.

### 2. Query-owned weight basis

For `GOVERNED_WEIGHTED`, `requested_output_grain.weight_basis_id` must be present and exact.

F018 never selects a weight basis. Missing basis is an integrity failure, not a request to discover a plausible weight.

### 3. Exact respondent weight scope

The caller must provide an exact `authorized_weight_scope_ref`.

Every supplied `WeightMeasureFact` must bind:

- a respondent in the exact I03 denominator;
- a source universe in the exact I03 source scope;
- the exact query-owned weight basis;
- the exact authorized effective scope;
- a weight-fact ref already present in I03 provenance.

Exactly one governed weight fact must cover every I03 denominator member.

### 4. Design and estimand authority

For every positive weight fact, both explicit fields are resolved independently:

- `design_authority_ref`
- `estimand_authority_ref`

Each must resolve exact, positive, and as `WEIGHT_DESIGN_ESTIMAND`.

A positive design authority cannot substitute for absent/denied estimand authority, and vice versa.

## Numerical closure

Only after authority/scope closure:

- parse exact respondent weights;
- reject negative/invalid weights;
- compute exact `sum_w`;
- compute exact `sum_w2`;
- require I03 `weighted_denominator_support_if_authorized == sum_w`;
- require positive nondegenerate sums;
- emit exact `effective_n = sum_w^2 / sum_w2`.

## Negative states

### `NOT_APPLICABLE`

Used for RAW/unweighted empirical grain. No numbers are emitted. Respondent count is not converted to an implicit all-ones weight basis.

### `NOT_AUTHORIZED`

Used where positive weighted authority cannot close, including missing exact weight facts/authority or missing explicit authorized weight scope. No numbers are emitted.

### `INVALID_WEIGHT`

Used for governed weight facts in unusable states or invalid/negative exact numeric values. No partial sums are emitted.

### `DEGENERATE_WEIGHT_SUM`

Used when the exact authorized denominator exists but the resulting weight sums cannot support the formula, including all-zero weights. Numeric zero is not emitted as effective-N.

### `SCOPE_MISMATCH`

Used where supplied weights do not belong to the exact I03 denominator/source/weight-basis/effective-scope/provenance grain, or where their `sum_w` does not reproduce I03's weighted denominator.

### `UPSTREAM_UNAVAILABLE`

Used when a governed weighted call reaches F018 without a positive I03 fact/weighted denominator capable of supporting this derived measurement.

## Integrity failures remain integrity failures

Tampered semantic identities, fact/query ref contradictions, risk-set contradictions, source-universe contradictions, measure-basis contradictions, or release refs absent from I03 provenance raise `EffectiveNError`.

They are not converted into an empirical zero, empty state, or numerical measurement.

## Epistemic ceiling

`EffectiveNProduct` is a derived measurement receipt. It is not a P01 public semantic object and cannot by itself:

- alter `EmpiricalFact`;
- authorize a source semantic;
- authorize a weight or estimand;
- admit structural truth;
- change an I05 frontier;
- change a candidate semantic identity.

