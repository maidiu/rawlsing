# C06 — Provenance Minimum Sufficient Receipt

Status: `INFORMATIONAL_REQUIREMENT__NOT_NEW_PUBLIC_ONTOLOGY`

This document specifies the **information a durable replay/provenance receipt must bind**. It does not mint a new semantic family or prescribe a deployment/storage technology.

## Sufficiency equation

A historical result is replay/audit sufficient only when the retained closure can establish:

`SOURCE`
`+ EXECUTABLE_DECODER_CLOSURE`
`+ HISTORICAL_AUTHORITY_CLOSURE`
`+ SEMANTIC_IDENTITY/REPLAY_LAW`
`+ SOURCE_AND_SEARCH_COMPLETENESS_STATE`
`+ GOVERNED_VALIDATION/SELECTION_STATE`
`+ LEARNED_PRODUCT_LINEAGE`
`+ I04/STRUCTURAL/PUBLICATION_CLOSURE`
`= EXPLAINABLE PINNED RESULT`.

No duplicate respondent payload is required by this equation.

## Minimum bound fields

### A. Source
- exact source artifact/content ref and SHA-256;
- source release/study/wave/instrument/time/universe identity;
- expected source shape/inventory sufficient to prove traversal completeness;
- source relation/noncomparability authority refs where relevant.

### B. Decoder
- decoder code/content identity;
- format path and exact configuration;
- compatibility rule/override authority;
- exact output-sensitive dependency/native-library/runtime determinants;
- immutable package/build artifacts or equivalent resolution refs;
- hostile decode test-vector set identity and expected result digest;
- extraction manifest/result digest.

### C. Semantic authority and C11
- historical authority id/version/hash closure;
- semantic projection/canonicalization/hash law version;
- C11 release/ref and ReplayManifest ref;
- respondent/source-row coordinate law;
- question/variable/topology/transform refs;
- expected semantic release root and pinned object ExactRefs as needed by downstream references.

### D. Query/discovery
- query/predicate ExactRefs and risk/target/source/measure scope;
- discovery authority/search-family/algorithm refs;
- candidate universe/grammar/frontier identity;
- backend-independent logical ordering/tie law;
- pruning/branch expansion rules;
- budget and stop law;
- RNG algorithm/stream/seed or explicit `NONE`;
- subsampling and validation split identities;
- frontier accounting and state transitions;
- final typed search outcome;
- source traversal completion ref;
- failures/retries/compatibility-path outcomes.

### E. Validation and learned empirical product
Where governed, bind:
- candidate refs and branch/factor ancestry;
- validation/model-selection rule id/version/hash;
- source universe, wave/time/scope and risk set;
- weights/design/estimand;
- respondent-set hash or replay coordinates, not duplicated payload;
- raw/weighted support;
- uncertainty/evidence state;
- validation data/split/resampling identity and randomness;
- decision state;
- accepted empirical learned release/product ExactRef;
- search/frontier final status.

If exact authority for any required validation/model-selection field is absent, the receipt records `MISSING_AUTHORITY`; it does not invent a default.

### F. I04 and structural publication
- StructuralEmpiricalAdmission ExactRef;
- admission rule/authority and decision state;
- focal structural proposition and target-use refs;
- time/scope/measure/uncertainty/negative-limit refs;
- structural producer object/build ExactRefs;
- V557 publication and V558 repository exact identities;
- role/cardinality/order-preserving dependency-closure digest.

### G. Replay result
- replay protocol authority/version;
- clean-process/no-cache condition;
- expected versus actual source, semantic release, learned release and structural roots;
- typed result: verified / input missing / authority unavailable / hash mismatch / semantic mismatch / nondeterministic replay;
- no hidden mutable `latest`, path fallback, wall-clock selection, filesystem-order semantics, or unnamed randomness.

## Exact-negative receipt

A `COMPLETE_AUTHORIZED_SEARCH__NO_RELATION` receipt is valid only if it binds:
1. exact source universe and source traversal complete state;
2. exact query/search frontier authority and definition;
3. all frontier accounting required by that law;
4. zero unresolved reader/decode/compatibility failures;
5. exact budget and a stop reason that is **completion**, not exhaustion;
6. zero missing transient/cache partition on which semantics depended;
7. final validation/search state under the governed state machine.

Anything less is not an empirical negative.

## Historical pinning

Recomputability does not eliminate the need to retain a small expected historical reference. A self-consistent rerun is not enough: the rerun must match the historical `ExactRef`/release root or else return drift/nondeterminism.

## Invalidation

The receipt is invalid for identity equality when any bound source, decoder, authority, semantic rule, query/search law, validation/model-selection law, randomness, admission rule, learned release dependency, or publication dependency changes. A changed determinant produces a new replay identity; it is not repaired by relabeling it as the old run.
