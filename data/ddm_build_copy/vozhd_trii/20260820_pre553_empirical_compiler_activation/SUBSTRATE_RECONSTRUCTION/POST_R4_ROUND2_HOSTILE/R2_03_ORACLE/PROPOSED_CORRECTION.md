# PROPOSED CORRECTION — NONCIRCULAR_ACCEPTANCE_COURT@2

Status: `DESIGN_ONLY__ROUND2_REQUIRED_CORRECTION__NO_RUNTIME_AUTHORITY`

## 1. Purpose

`NONCIRCULAR_ACCEPTANCE_COURT@2` is the minimum correction required before a post-R4 physical carrier can receive dispositive semantic-equivalence acceptance.

It preserves the scope of Round-1 `SEMANTIC_EQUIVALENCE_ORACLE@1` but changes **who is allowed to define expected truth** and adds an explicit court on the oracle itself.

The corrected court is governed by:

`source/authority truth -> independent primitive expectation`

and

`candidate immutable bytes -> independent passive physical observation`

followed by independently encoded acceptance semantics.

R4, current production code, and candidate-owned adapters are valuable differential witnesses. None is allowed to be the sole source of expected truth.

## 2. Independence zones

The court has four code/evidence zones.

### Z0 — frozen authority/source inputs

Contains only immutable inputs:

- exact source identities and source-native/decoder authority;
- frozen C11/I03/I05/I04/whole-machine contract identities;
- exact candidate commit;
- exact candidate built artifact/physical root;
- compiler/configuration/profile identity;
- cache/index policy;
- complete tuning-workload disclosure commitment;
- court/evaluator version.

No mutable `latest`, default branch, ambient source lookup, directory enumeration, wall clock, or hidden randomness may define truth.

### Z1 — passive candidate physical reader

The reader:

- consumes the exact immutable root under test;
- implements the published/frozen physical format needed to parse that carrier;
- independently hashes exact bytes and manifests;
- emits the common `PRIMITIVE_WITNESS@2` stream;
- may use ordinary format libraries only as byte/physical decoders under a frozen profile;
- imports no candidate semantic/materialization/query/discovery/admission code;
- imports no R4 physical reconstruction code;
- imports no production `rawlsing_next` semantic/query/discovery/admission implementation.

A candidate-supplied logical export may be run only as a secondary lane.

If the carrier format cannot be read without executing candidate semantic code, the candidate is not dispositively testable.

### Z2 — independent expected truth + mini-evaluator

Expected primitive truth originates from exact source/authority material, not from candidate manifests.

The mini-evaluator implements only what is necessary to decide acceptance:

- exact typed primitive serialization;
- bounded external sort/merge or equivalent exact comparison;
- declarative C11 acceptance projections;
- independent content-hash/ExactRef recomputation;
- simple scoped respondent-set algebra;
- routing/risk-set membership;
- exact support and authorized weight arithmetic;
- bounded I05 frontier compilation/evaluation;
- minimal I04 blocker precedence/projection rule.

It is not a second production compiler, repository, query planner, cache system, discovery optimizer or structural engine.

### Z3 — frozen production/R4 differential witnesses

May include:

- frozen C11 constructors/integrity;
- frozen I03/I05/I04 execution;
- accepted R4 artifacts where useful.

Z3 is corroborative. A Z3 match cannot override a Z1/Z2 mismatch. A Z2-versus-Z3 disagreement on an authoritative fixture yields `ORACLE_AUTHORITY_CONFLICT` and blocks candidate acceptance.

## 3. Common primitive witness

The physical reader and source truth normalizer converge to one carrier-neutral typed record grammar.

At minimum the grammar must represent all identity/completeness-bearing material needed for the claimed scope:

- source/release identity;
- source row ordinal;
- native variable ordinal/name;
- raw typed value / explicit no-payload physical state;
- physical missing state;
- variable type/format/labels/dictionaries;
- missing declarations including zero incidence;
- source topology/MR/repeated/ranked/component relations;
- canonical C11 inputs and authority bindings;
- routing/applicability/risk-set material;
- coordinates;
- weights/design/estimand/normalization authority;
- source relation/nonduplication provenance;
- replay/authority/dependency bindings.

The primitive grammar is an **acceptance interchange**, not a new public ontology.

Candidate physical record ordering is ignored unless order is itself semantic. Identity-bearing order/rank/multiplicity fields remain exact.

## 4. Mandatory oracle-control gate

Before judging a candidate, the court must prove itself.

`C0_ORACLE_CONTROL` runs seeded controls with known expected outcomes.

### Destructive controls that MUST be rejected

- respondent permutation preserving per-question marginals;
- compensating event drop/duplicate preserving selected counts;
- zero-incidence declaration deletion;
- raw-identical/dictionary-distinct collapse;
- physical/semantic missing-state collapse;
- typed negative-state flattening;
- rank/order/multiplicity mutation;
- routing denominator mutation with raw responses fixed;
- weight/design authority mutation with numeric vector fixed;
- source relation/provenance mutation with data fixed;
- semantic field mutation with stale ExactRef;
- semantic deletion followed by recomputation of all candidate-format hashes;
- oracle-target field mutation designed to expose an omitted comparison field.

### Benign controls that MUST remain equivalent

- physical record/file enumeration reorder;
- lawful shard/row-group/grouping variation;
- cache absence;
- lawful worker-count variation;
- representation-only re-layout that does not alter semantic order fields.

If any required destructive mutant survives, or any required benign invariant is rejected, `C0_ORACLE_CONTROL=FAIL` and no candidate can be accepted.

A pass percentage is forbidden.

## 5. Gate order

### C0 — Oracle adequacy

Run mandatory destructive and benign controls.

Outcome:
- `PASS`
- `FAIL`

No candidate evaluation occurs on `FAIL`.

### C1 — Court freeze / commitment

Freeze Z0.

For blind I05, the commitment order is:

1. candidate commit;
2. exact built artifact/physical root;
3. compiler/configuration/profile;
4. cache/index policy;
5. complete tuning-workload disclosure commitment;
6. court commitment of 1–5;
7. generate and record oracle nonce;
8. compile frontier;
9. exclude disclosed workload hashes;
10. seal frontier and later publish nonce/frontier in replay receipt.

Any mutation to 1–5 after step 6 restarts the court.

### C2 — Source/authority primitive expectation

For every source/surface claimed:

- bind exact source identity;
- produce exact expected source/metadata/identity primitives under governing decoder/source authority;
- bind semantic authority inputs;
- explicitly mark unresolved authority as blocked, never guessed.

The nine-family hostile corpus is exercised here as a sensitivity set. It does not replace complete claimed source inventory.

### C3 — Passive candidate physical observation

With all nonauthoritative caches absent/inaccessible:

- independently open the exact root under test;
- independently verify byte/member/root claims needed to read;
- emit complete candidate primitive stream;
- do not consult candidate manifest as the definition of what *should* exist.

### C4 — Primitive/C11/ExactRef equivalence

Require:

- exact expected/observed primitive completeness;
- exact identity-bearing multiset/order semantics;
- full applicable C11 field closure;
- independent canonical projection;
- independent ExactRef/content-hash recomputation;
- no extra unauthorized primitives/objects;
- no missing primitives/objects.

Candidate and R4 hashes have no authority at this gate.

### C5 — I03 noncircular behavior

From primitive truth:

- independently build scoped respondent membership;
- apply exact target/condition/routing/risk/source/measure rules;
- compute raw and authorized weighted supports;
- classify positive and frozen negative states.

Compare independent result with candidate public seam and frozen I03 secondary lane.

Exact respondent membership is compared, not only count.

Integrity failure remains outside ordinary negative query states.

### C6 — I05 declared + post-commit blind frontier

Exercise applicable exact-bounded families and a post-commit blind frontier.

Minimum blind shapes where authority permits:

- pair;
- k-way, `k >= 3`;
- conditional;
- reversal/Simpson;
- recursive subgroup;
- branch-conditioned distribution/cotravel;
- co-signature/joint input to cloud-like diagnostics.

Every compiled candidate is evaluated. No bitmap/index/cache vocabulary may define reachability.

Diagnostic score perturbation must not change factual frontier, facts or I04 admission unless separately authorized.

### C7 — I04 independent blocker/admission court

Encode the frozen finite precedence and projection permission needed by the acceptance corpus.

Run:

- each blocker separately;
- multi-blocker combinations;
- ADMITTED;
- exact authority/evidence/negative refs;
- projection permission.

Only exact `ADMITTED` may project positive structural evidence.

### C8 — integrity/cache/replay/authorization

Required controls:

- byte flip;
- missing/truncated member;
- pre-seal/partial publication;
- stale semantic hash/ExactRef;
- self-consistent semantic deletion + all candidate-format rehashes;
- unauthorized but internally valid root;
- all caches absent;
- stale cache from another root;
- canonical corruption with healthy cache;
- no shadow/legacy/old-root fallback;
- fresh-process/layout/hashseed/worker variants.

Byte integrity, semantic completeness and root authorization are separate judgments.

## 6. Acceptance states

Per claimed source/surface:

- `PASS`
- `FAIL`
- `BLOCKED_BY_MISSING_AUTHORITY`
- `ORACLE_AUTHORITY_CONFLICT`

`BLOCKED_BY_MISSING_AUTHORITY` is not a pass.

`ORACLE_AUTHORITY_CONFLICT` is not a vote. It blocks acceptance until authority/evaluator disagreement is adjudicated.

Overall candidate acceptance requires:

`C0 PASS`
`AND all applicable C1-C8 PASS`
`AND no BLOCKED surface inside the claimed acceptance scope`
`AND no ORACLE_AUTHORITY_CONFLICT`.

## 7. Cache/fallback isolation

Primary candidate equivalence is executed with nonauthoritative cache namespaces physically unavailable.

The exact root under test is isolated from:

- prior canonical roots;
- shadow candidates;
- rollback candidates;
- legacy databases;
- materialized query caches.

Fallback behavior is tested separately as a hostile case. Returning a correct fact from the wrong authority after corruption is still failure.

## 8. Source-scope law

A family-balanced sample is not release certification.

For a `CLOSED_35` claim the court requires all 35 exact governed source identities and the complete primitive/source-shape closure claimed by the release.

A named source surface with unresolved authority remains blocked. In particular, EVS 1999/2008 compatibility decoding does not create intended text authority.

## 9. Non-goals

This correction does not:

- select a carrier;
- require long/columnar/matrix storage;
- require Merkle integrity;
- alter source semantics;
- alter C11/I03/I05/I04;
- certify a source by synthetic analogy;
- create new harmonization;
- create a second production query engine;
- reward performance for semantic loss.

## 10. Dispositive rule

The minimum dispositive equation is:

`ORACLE_CONTROL_PASS`
`AND INDEPENDENT_PRIMITIVE_EQUIVALENCE_PASS`
`AND INDEPENDENT_SEMANTIC_I03_I05_I04_PASS`
`AND INTEGRITY_CACHE_REPLAY_AUTHORIZATION_PASS`
`=> CANDIDATE_EQUIVALENCE_PASS`.

One authoritative mismatch is sufficient to defeat the claimed mechanism/scope.
