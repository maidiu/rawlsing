# FFIF002 — REVERSIBILITY AND ANCESTRY CONTRACT R1

## Ruling

`REVERSIBLE` does **not** require every transformation to be mathematically invertible.

For FIELD FORGE semantic governance, the governing requirement is:

> Every project-created analytic transformation must preserve an exact, addressable source-native ancestry path and a replayable transform specification, with information loss explicitly typed.

Literal invertibility is one strong case. Ancestry recoverability is the general requirement.

## Reversibility states

### 1. `VALUE_INVERTIBLE`
The transformed value has an exact deterministic inverse to the consumed source-native state/value.

Examples:
- lossless code normalization;
- bijective relabeling with stable source-state IDs;
- unit conversion where precision and original value are retained exactly.

Required receipt state:
- input refs;
- exact mapping/function;
- version;
- inverse or proof of bijection.

### 2. `ANCESTRY_REVERSIBLE`
The output is many-to-one or otherwise lossy, so the output alone cannot reconstruct its input, but each transformed observation/state retains exact source-native ancestor references and the transformation can be replayed from those ancestors.

Examples:
- five categories collapsed to two;
- continuous income binned into quintiles;
- rare categories grouped for one claim;
- ranks replacing amounts within a declared reference universe.

This is lawful only when:
1. the downstream artifact is explicitly marked lossy;
2. the original source-native state/value is not overwritten;
3. the transform receipt identifies all ancestors and the mapping/reference frame;
4. downstream consumers cannot mistake the analytic output for source-native identity.

### 3. `SOURCE_LOSS_INHERITED`
The source itself has already top-coded, rounded, harmonized, censored, grouped, or otherwise erased distinctions before Rawlsing receives the data.

Rawlsing cannot recover information the source never supplies. It can still preserve exact ancestry to the source-native lossy state.

Law:

`PROJECT REVERSIBILITY STOPS AT THE SOURCE-NATIVE BOUNDARY; IT MUST NOT CLAIM PRE-SOURCE RECOVERABILITY.`

Examples:
- source top-coded income;
- source-published grouped age;
- source-provided harmonized education bands.

The inherited loss profile must travel with any later transform. A source-provided harmonized value does not erase the fact that its comparability proposition is source-scoped and may itself be lossy.

### 4. `UNRECOVERABLE_PROJECT_LOSS`
Rawlsing overwrites, drops, or severs the source-native ancestor such that the exact consumed source state/value can no longer be recovered.

This state is unlawful for FIELD FORGE semantic preprocessing and for FFX002 common-input production.

Examples:
- replacing all DK/refused/not-asked values with one NA and discarding original state IDs;
- destructive overwrite of local religion categories with a global canonical category;
- retaining only z-scores after discarding original income and reference-frame metadata.

### 5. `NOT_APPLICABLE_NO_TRANSFORM`
Used for `NONCOMPARABLE` or `UNRESOLVED` dispositions where no analytic transform is authorized.

## Exact ancestry minimum

Every lossy TTAR must make the following reconstructable:

- exact source scope and source-native variable/state identifier;
- exact original value/state identifier as observed in the source substrate;
- any source-native label/order/routing semantics relied upon;
- each intermediate project transformation receipt, in order;
- final analytic state/value;
- claim and representation scope that authorized each project-created semantic step.

An ancestry graph may be many-to-one. It must not be many-to-unknown.

## Continuous values and bins

Binning a continuous value is not reversible from the bin label. It can still be `ANCESTRY_REVERSIBLE` if the exact consumed continuous source value remains addressable and the bin thresholds/boundary convention are frozen.

The receipt must include:
- threshold set;
- inclusive/exclusive boundary convention;
- treatment of out-of-range/top-coded values;
- reference population if quantile bins are used;
- tie handling where applicable.

A later method must not infer a cardinal distance between bins unless separately authorized.

## Many-to-one category collapse

If A, B, and C collapse to X:

- X is an analytic output state, not evidence that A=B=C;
- the output must retain ancestry `{A|B|C}` at observation level or an exact joinable reference thereto;
- the receipt must state what distinctions were lost;
- a consumer outside the authorized claim may not consume X as if it were a project-semantic category.

## Source harmonization

If the source publishes native and harmonized states:

- the harmonized state may be consumed as `SOURCE_NATIVE_HARMONIZATION_CONSUMPTION` only with source scope/evidence;
- the native state remains preferred ancestry where available;
- the source's harmonization does not authorize every project claim, representation, wave, or cross-context transport;
- any extra project use beyond the source's warranted proposition requires a project or claim-scoped receipt.

If only the harmonized state is supplied, Rawlsing records `SOURCE_LOSS_INHERITED`, not fake reversibility.

## Wording drift and claim-local immateriality

Where wording differs across waves but a bounded claim judges the distinction immaterial:

- do not create `PROJECT_SEMANTIC_IDENTITY` unless the evidence warrants sameness independent of the bounded claim;
- prefer `CLAIM_SCOPED_EQUIVALENCE` or `TRANSPORT_EQUIVALENCE` naming the invariant;
- preserve each original wording/state ID below the transform.

## Replay contract

A replay specification must be sufficient to regenerate the analytic output from the preserved source-native ancestors, including:

- function/mapping version;
- ordered rule application;
- parameters and reference universes;
- source/project authority versions;
- deterministic tie/boundary policies;
- for stochastic post-semantic methods, seed/software/version as method provenance.

Stochastic method provenance may reproduce a representation. It may not retroactively authorize a semantic transform.

## Supersession

A transform receipt is immutable after issuance. Correction occurs by supersession:

1. retain old receipt and outputs as historical provenance;
2. issue new receipt with `supersedes` reference;
3. name the invalidation trigger or changed evidence;
4. recompute dependent outputs;
5. prohibit silent mutation of the meaning of an existing receipt ID.

## Final law

`SOURCE_NATIVE RECOVERABILITY + EXPLICIT LOSS + REPLAYABLE TRANSFORM` is the minimum reversibility contract.

Mathematical inversion is sufficient where available. It is not necessary. Destroying project ancestry is neither.