# BENCHMARK / EXECUTION PLAN — R2-03 NONCIRCULAR COURT

Status: `PLAN_ONLY__CORRECTNESS_BEFORE_RESOURCE`

This plan measures the cost and adequacy of the acceptance court. It does not compare carrier performance except incidentally where needed to execute the same court.

## Phase 0 — exact freeze

Record:

- Authorities 54/55;
- all six pinned Round-1 commit identities;
- exact frozen source/C11/I03/I05/I04 authority identities;
- candidate commit;
- exact built artifact/physical root;
- compiler/configuration/profile;
- cache/index policy;
- tuning disclosure commitment;
- evaluator/control-corpus version.

Fail on mutable/ambiguous input.

## Phase 1 — oracle-control court

Run every mandatory destructive and benign control **before candidate testing**.

Record per control:

- control ID;
- base primitive digest;
- mutant primitive digest;
- base self-reported/candidate-style digest if applicable;
- mutant self-reported/candidate-style digest;
- expected court result;
- actual court result;
- first mismatch witness.

Acceptance of evaluator is conjunctive:

`control_count == expected_control_count`
and every control has exact expected outcome.

No control pass rate can substitute.

The bounded checked-in `ORACLE_CONTROL_PROOF.py` demonstrates only the central marginal-parity/identity-loss principle; it is not the future full mutation runner.

## Phase 2 — full claimed source primitive closure

For every source in the candidate claim:

- verify exact source identity;
- establish source row/variable shape;
- generate expected primitive stream;
- read candidate primitive stream through passive parser;
- compare exact completeness and payloads.

For CLOSED_35, all 35 exact identities participate. Family sampling is forbidden as a replacement.

Record counts by primitive kind and exact stream digests only as summaries; mismatches are determined by exact keyed comparison.

## Phase 3 — self-consistent destructive rehash

On a copy of the candidate artifact:

1. remove/alter one canonical semantic primitive;
2. update every candidate-format member/root digest so the physical artifact is internally valid;
3. run ordinary candidate integrity, if available;
4. run the independent court.

Required:

- candidate-local byte integrity may pass;
- independent semantic/completeness gate MUST fail.

This is the key separation between integrity and semantic equivalence.

## Phase 4 — independent C11/ExactRef closure

For each applicable C11 family/record surface:

- independently construct acceptance projection;
- hash independently;
- compare complete expected/observed ref multisets;
- test one field-targeted mutant;
- validate M01-M18 coverage.

Record:
- expected count;
- observed count;
- missing/extra count;
- first differing field;
- content-hash/ref comparison.

## Phase 5 — I03 court

Run:

- positive supported;
- observed zero;
- zero support;
- valid empty;
- unavailable authority;
- unavailable routing/risk;
- unavailable measure;
- unavailable source;
- noncomparability;
- integrity tamper.

For each factual result record exact scoped respondent-set digest in addition to public fact projection.

Include a respondent-permutation control whose univariate marginals are unchanged.

## Phase 6 — two-stage blind I05

Only after Phase 0 candidate commitments:

1. generate oracle nonce;
2. compile blind frontier;
3. prove no selected workload hash is in tuning disclosure;
4. seal frontier.

Run declared + blind:
- pair;
- k-way;
- conditional;
- reversal/Simpson;
- recursive;
- branch-conditioned;
- co-signature/joint.

Record:
`candidate_count`, `covered_candidate_count`, exact candidate-order/receipt identity.

Required:
`candidate_count == covered_candidate_count`.

## Phase 7 — I04 blocker court

Run each blocker and multi-blocker combinations.

Compare:
- decision;
- public typed state;
- reason;
- evidence/authority/negative refs;
- projection permission.

On independent/frozen disagreement, record `ORACLE_AUTHORITY_CONFLICT`; do not accept candidate.

## Phase 8 — no-cache / stale-cache / laundering court

Primary run:
- physically remove or deny access to every nonauthoritative cache.

Then:
- rebuild;
- rebuild again;
- inject cache from another root;
- corrupt cache only;
- corrupt canonical while leaving cache healthy.

Required:
- cache absence changes only cost;
- stale/corrupt cache cannot change truth;
- canonical corruption yields no result even when cache contains the correct answer.

## Phase 9 — publication/root authorization/integrity

Test:
- byte flip;
- truncation;
- missing member;
- pre-seal visibility;
- stale ExactRef;
- unauthorized but internally valid root;
- no fallback to shadow/legacy/old root.

Record earliest detection and whether any empirical result escaped.

## Phase 10 — deterministic replay/invariance

Repeat clean runs varying as lawful:

- Python hash seed;
- irrelevant file enumeration;
- worker count;
- shard/block grouping;
- row-group size;
- cache absence/presence after primary no-cache pass.

Semantic primitive stream, C11/ExactRefs, I03 sets/facts, I05 coverage/facts and I04 receipt must remain identical.

## Resource accounting

Because this is a release-acceptance instrument, no performance threshold waives correctness.

Measure:

- peak RSS by phase;
- scratch bytes;
- bytes read from source;
- bytes read from candidate;
- external sort/merge scratch;
- wall time;
- number of exact primitives compared;
- number of controls;
- mismatch witness count.

Target implementation property: bounded memory by streaming/sort-merge, but if a simpler full comparison costs more while remaining operationally practical, prefer simplicity.

## Stop rule

For a candidate rejection run, one reproducible authoritative mismatch is sufficient.

For diagnostics, continue to enumerate failures, but final state remains failed.

For the evaluator itself, any mandatory control failure stops the court immediately: the oracle is not adequate to certify anyone.
