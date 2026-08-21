# SEMANTIC_EQUIVALENCE_ORACLE@1 — PROPOSED CONTRACT

Status: `DESIGN_ONLY__REPRESENTATION_NEUTRAL`

## 1. Purpose

This contract decides whether a future post-R4 physical carrier is semantically equivalent to the frozen PRE553 source/C11/query/discovery/admission machine.

It is intentionally hostile to shared implementation assumptions. The candidate does not define its own expected truth, and R4's physical files do not define expected truth.

## 2. Authority inputs

Every run must pin, by immutable identity:

- campaign/whole-machine governing documents;
- exact CLOSED_35 source-byte manifest;
- exact source-native constitution and decoder contract;
- source-specific certification/recon evidence used by the hostile corpus;
- frozen I01/I02 C11 semantic contract;
- frozen I03 query contract;
- frozen I05 discovery contract;
- frozen I04 admission contract;
- candidate git commit/build identity;
- candidate tuning-workload disclosure hash;
- oracle version;
- explicit oracle run nonce used only for post-freeze blind-workload selection.

No `latest`, default branch, mutable path-only lookup, ambient raw-source discovery, hidden wall clock, or unrecorded randomness may affect expected truth.

## 3. Required candidate seam

The oracle requires a **carrier-neutral logical observation seam**. It may be an adapter supplied with the candidate, but that adapter has no semantic authority.

The seam must expose or reconstruct:

1. release/source identities;
2. the complete source-native physical witness surface required for certification;
3. every public C11 object canonical semantic projection;
4. every internal C11 record canonical semantic projection;
5. exact C11 release/replay manifest material;
6. the normal frozen I03/I05/I04 public seams.

The adapter may not expose physical partition names as semantic fields. The oracle must be able to delete all declared nonauthoritative caches before opening the authoritative candidate.

## 4. Independent expected-truth lanes

### 4.1 Source-native lane

Expected source physical truth is generated from exact source bytes under the frozen decoder/source-native contract or consumed from a sealed source-certification witness whose lineage resolves to those bytes.

Required physical observations include:

- byte identity;
- case/row count;
- dictionary/logical variable count and order;
- raw value;
- physical missing class;
- missing declarations/ranges/extended missing;
- exact labels;
- native type/format;
- native MR metadata;
- reader config/version;
- bounded compatibility-execution exception identity.

Candidate-produced summaries never replace this lane.

### 4.2 Semantic-law lane

Expected logical truth is represented as canonical semantic projections under frozen I01/I02 law.

The oracle recomputes:
- canonical JSON material;
- semantic content hash;
- object id;
- ExactRef;
- release semantic hash/manifest closure.

Stored candidate hashes are checked, never trusted.

### 4.3 Independent incidence/query lane

A deliberately small reference evaluator reconstructs respondent membership and support from canonical C11 observations. It implements only acceptance semantics:

- exact respondent scoped identity;
- target event matching;
- AND/OR/NOT predicate membership;
- routing/risk-set membership;
- source scope;
- exact raw numerator/denominator;
- exact authorized weight application when authority closes;
- typed zero/empty/unavailable/noncomparable distinctions needed by the frozen I03 corpus.

It must not import candidate bitmap/index/materialization code. Frozen I03 is also run. Candidate, frozen I03, and the independent evaluator must agree. If the two oracle lanes disagree, the oracle itself is unresolved and may not accept a candidate.

## 5. Gate protocol

### O0 — Authority Freeze

Produce `ORACLE_RUN_MANIFEST` containing every immutable input ref/hash plus:
- candidate commit;
- candidate build identity;
- tuning disclosure hash;
- oracle nonce;
- test-suite version.

A missing or mutable authority input blocks the run.

### O1 — Source Identity / Shape / Physical Preservation

For each claimed source:
1. bind exact source byte identity;
2. compare source shape;
3. compare physical-state census and sentinel witnesses;
4. compare exact declaration and metadata witnesses;
5. execute source-specific hostile assertions.

This gate cannot be satisfied by aggregate C11/query parity.

### O2 — C11 / M01-M18 / ExactRef

Normalize candidate observations into canonical semantic projections.

Require:
- exact object/record multiset equality;
- exact full field equality;
- independently recomputed ExactRef equality;
- no extra unauthorized public/internal family;
- exact typed-absence representation where frozen law requires it;
- M01-M18 complete coverage;
- exact release/replay closure.

Order of storage records is not equality material unless order/rank is explicitly semantic inside an event/topology field.

### O3 — I03

Run:
- positive supported;
- observed-zero;
- zero-support;
- valid-empty;
- unavailable authority;
- unavailable risk set;
- unavailable measure;
- unavailable source scope;
- noncomparability/composition;
- unsupported topology;
- integrity-tamper cases.

For lawful results compare full `EmpiricalFact` projections and underlying respondent membership/support. For integrity tampering require hard integrity behavior, not a normal negative fact.

### O4 — I05

#### Declared regression frontier

Exercise every frozen I05 family applicable to the fixture catalog:
- `UNARY_SOCIAL_FORK`
- `RESPONSE_X_EMPIRICAL_COORDINATE`
- `BOUNDED_COORDINATE_CONJUNCTION`
- `RESPONSE_X_COORDINATE_CONJUNCTION`
- `PAIR_RESPONSE_COTRAVEL`
- `BOUNDED_K_WAY_RESPONSE_CONFIGURATION`
- `CONDITIONAL_REVERSAL_OR_SIMPSON`
- `MINORITY_OR_NONMODAL_DEPARTURE`
- `RECURSIVE_SUBGROUP_FORK`
- `BRANCH_CONDITIONED_DISTRIBUTION`
- `BRANCH_CONDITIONED_COTRAVEL`

Require complete candidate coverage, canonical candidate-hash order, exact facts, exact validation, exact ancestry, exact replay.

#### Post-freeze blind frontier

The candidate must first freeze:
- its commit;
- its physical build/config;
- a canonical set of exact hashes for every I03/I05 workload used to tune storage.

Only then does HQ record `oracle_nonce`.

The oracle deterministically selects/constructs a finite exact frontier from already-authorized atoms/templates using:

`blind_seed = SHA256(oracle_version || candidate_commit || tuning_disclosure_hash || oracle_nonce || authority_snapshot_set_hash)`

Selection rules:
1. exclude every disclosed tuning workload hash;
2. include at least one pair cotravel;
3. include at least one bounded `k >= 3` configuration where authority permits;
4. include at least one conditional query;
5. include at least one reversal/Simpson grid;
6. include at least one recursive subgroup fork;
7. include at least one branch-conditioned distribution or cotravel;
8. include at least one co-signature/joint pattern used to form a cloud-like diagnostic surface;
9. include at least two non-WVS/LiTS source families whenever the certified catalog permits;
10. seal exact selected candidates and frontier hash before evaluation.

The nonce is public in the run receipt after selection and is required for replay. There is no hidden randomness.

#### Cloud-like diagnostics

Exact joint/co-signature facts are authoritative only through ordinary frozen empirical fact law. `CLOUD_SCORE`, MI/NMI, lift, association strength and similar quantities remain diagnostic-only.

Metamorphic test: perturb/disable diagnostic ranking while holding the exact frontier/facts fixed. Reachability, fact identity and structural admission must not change.

### O5 — I04

Run positive and each nonpositive decision class.

Inject multiple simultaneous blockers to test frozen precedence. Compare:
- P06 decision state;
- public typed state;
- reason code;
- empirical query/fact refs;
- admission authority;
- source/native scope;
- target use/permission;
- structural identity/proposition;
- time;
- estimand;
- measure/weight authority;
- support/uncertainty;
- negative/denial/noncomparability refs;
- authority closure;
- positive projection permission.

Only exact `ADMITTED` may project positive structural evidence.

### O6 — Replay / Integrity / Cache

#### Fresh process

At minimum three clean-process runs:
- different `PYTHONHASHSEED`;
- permuted irrelevant filesystem enumeration;
- different lawful worker count;
- cache absent on one run.

All canonical outputs must be identical.

#### Corruption

Inject independently:
- authoritative member byte flip;
- member removal/truncation;
- stale/mismatched stored semantic hash;
- stale ExactRef;
- authority snapshot hash mismatch;
- partial/pre-seal publication visibility.

Required outcome: no semantic truth is returned from the invalid release.

#### Cache

For every candidate-declared nonauthoritative cache:
1. build/open baseline;
2. delete cache;
3. open/rebuild and compare;
4. rebuild again in fresh process and compare;
5. substitute stale cache from another release.

Deletion must not remove truth. A stale cache must be rejected or deterministically rebuilt before semantic use.

## 6. Real-source hostile corpus law

A generic SAV fixture plus a DTA fixture is insufficient.

Initial real-source witnesses must retain all nine families:
- Afrobarometer;
- Arab Barometer;
- Asian Barometer;
- EVS;
- GSS;
- Latinobarometro;
- LiTS;
- South Asia;
- WVS.

`HOSTILE_CASES.csv` names the minimum rare/compound facts already established in checked-in evidence.

Where a source-specific semantic authority remains unresolved, the oracle expectation is itself blocked/typed-negative. For example, the frozen Latin1 compatibility execution path for EVS 1999/2008 does not authorize intended label text.

Generated hostile fixtures may enlarge coverage but may never certify a real source by analogy.

## 7. Property/metamorphic generator dimensions

The bounded generator should cross-product or pairwise-cover these independent dimensions:

- 0/1/N respondents;
- duplicate/zero/missing native IDs;
- multiple source scopes;
- one/many native questions;
- raw-identical metadata-distinct variables;
- ordinary/system/user/extended physical missing;
- semantic substantive/missing/DK/refusal/IAP/inapplicable/not-asked/special/unresolved;
- missing declaration present with zero incidence;
- all-one-typed-state columns;
- ordinary blank/control/NUL-bearing strings;
- large integer-like raw values versus narrow display formats;
- exact finite decimals and signed-zero/native numeric edges where decoder permits;
- variable labels/value dictionaries;
- overlapping/alias MR sets;
- multiselect/repeated/componentized/ordered/ranked topology;
- routing eligible/ineligible/unknown/rule unavailable;
- observed/unknown/nonconditionable coordinates;
- weight valid/missing/invalid/not-authorized/unresolved;
- one/multiple design/estimand authority bundles;
- source relation authorized/denied/unknown/distinct-by-default;
- query supported/observed-zero/zero-support/valid-empty/unavailable/noncomparable;
- admission blocker combinations.

Each generated base case must have at least one paired mutation with a known expected invariance or sensitivity.

## 8. Equality rules

### Semantic equality

Two observations are equal only when their canonical semantic projections are byte-identical under frozen canonicalization and all exact refs/hashes close.

### Set equality

Set-like semantic fields use frozen canonical set semantics. Sequence/order equality remains exact where the schema makes sequence/order identity-bearing.

### Numeric equality

No tolerance is introduced into identity-bearing exact material. Binary floating approximation cannot substitute for exact integer/Decimal/Fraction/string representation where the frozen contract requires exactness.

### Negative equality

`UNKNOWN`, `MISSING`, `NOT_ASKED`, `INAPPLICABLE`, `UNAVAILABLE`, `NONCOMPARABLE`, `VALID_EMPTY`, `INTEGRITY_FAILURE`, and related frozen typed states are not interchangeable.

## 9. Acceptance rule

For a claimed scope:

`ACCEPT` iff every applicable O0-O6 assertion is `PASS`.

`BLOCKED_BY_MISSING_AUTHORITY` means the carrier is not accepted for that claimed surface. It does not authorize a guessed expectation.

Any reproducible semantic mismatch is `FAIL`.

There is no scoring, majority vote, waiver, performance tradeoff or candidate-specific relaxation.

## 10. Non-goals

This contract does not:
- choose a physical carrier;
- prescribe normalization;
- prescribe columnar/row orientation;
- prescribe compression;
- prescribe indexes/bitmaps;
- certify any source not actually run;
- repair source text;
- infer semantic mappings;
- promote diagnostics into facts;
- alter C11/I03/I05/I04.
