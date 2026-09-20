# FIABC-W3-I05 — WVS7 Candidate-Neutral Oracle Materialization Protocol

This is the deterministic local protocol required to turn the implemented WVS oracle contract into a real frozen expected-truth bundle. This document records procedure only. **No WVS result was materialized by FIABC-W3-I05.**

## Preconditions

The integrated tree must already contain the accepted current common semantic path needed to realize:

`exact WVS source -> governed source-backed C11 -> exact I03 facts -> complete fixed I05 learned empirical product`.

Before beginning, the local operator must possess the exact WVS Wave 7 source:

- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- expected source shape after accepted physical decode: `97,220 rows × 613 variables`.

The oracle run must use a new **court-owned** process/root. It must not point at any candidate A/B/C durable root, scratch root, cache, session, transformed carrier, output receipt, or repository-local candidate state.

## Frozen candidate-neutral authority inputs

Bind exactly:

- Lock2: `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`;
- Lock2 replay: `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`;
- DiscoveryAuthority: `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`;
- EmpiricalUniverse: `f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e`;
- risk set: `0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7`;
- RAW/unweighted measure basis: `6ed5d61b77c8d77affeb4b49b55c2cc23a4c25dbd65d02719c6ab7a3069a3c79`;
- the exact current question/response/topology/routing/query/predicate authority closure accepted by FIABC-W2-L02;
- the exact ordered 46-candidate Lock2 frontier from `WORKER_RETURNS/EE-P2F2/05_WVS7_DISCOVERY_AUTHORITY_AND_FRONTIER_BINDING.json`.

The exact family shape is:

- `UNARY_SOCIAL_FORK = 10`;
- `PAIR_RESPONSE_COTRAVEL = 1`;
- `BRANCH_CONDITIONED_DISTRIBUTION = 10`;
- `BOUNDED_K_WAY_RESPONSE_CONFIGURATION = 25`.

## Materializer contract

Invoke:

`rawlsing_next.pre553_independent_parity_oracle.materialize_wvs7_oracle(...)`

with:

- `source_path` = exact WVS source file;
- `frozen_authority` = the candidate-neutral authority bundle above;
- `neutral_materializer` = an integrated common-semantic callable;
- `freeze=FreezeContext(...)` proving no candidate output/state exists.

The neutral materializer callable is intentionally candidate-free. Its input signature is:

`(exact_source_path, frozen_candidate_neutral_authority) -> materialization document`.

It must not receive a candidate id or candidate repository/session/cache.

It must return `contract = RAWLSING_FIABC_WVS7_ORACLE_MATERIALIZER@1.0.0` and these exact classes of material:

- exact source identity and shape;
- exact Lock2/court constitution refs;
- exact transitive semantic authority closure;
- exact current projection/C11 release/replay refs;
- the exact ordered 46-candidate frontier and named family counts;
- exactly one expected typed fact record for every frontier member, in canonical frontier order;
- the complete governed I05 learned product identity;
- semantic identity;
- replay identity;
- exact output identity;
- I05 coverage material;
- exact replay/dependency manifest;
- complete exact-ref manifest;
- candidate-neutral build provenance.

The implementation rejects candidate-owned dependency classes and rejects any same-cardinality WVS frontier that differs from the frozen ordered Lock2 hash list.

## Required causal sequence

1. Start a fresh court-owned process/root.
2. Assert that no candidate output exists.
3. Assert that no candidate-owned root has been consulted.
4. SHA-256 the source bytes inside the materialization process.
5. Decode only through the accepted generic physical decoder.
6. Reconstruct the accepted source-backed C11 logical surface under the frozen WVS projection/authority closure.
7. Execute the complete candidate-neutral I03 fact workload needed by the 46 frozen I05 candidates.
8. Execute I05 over the complete frozen frontier; do not prune, rank, substitute, extend, or adapt the frontier.
9. Preserve every typed negative/nonpositive state exactly.
10. Build the materialization document defined above.
11. Call `materialize_wvs7_oracle(...)`.
12. Persist the returned frozen oracle bundle and its `oracle_identity_sha256`.
13. Mark the oracle bundle read-only.
14. Terminate/close the oracle process state.
15. Do **not** mount oracle-created caches, sessions, transformed carriers, C11 repositories, or scratch state into A, B, or C.
16. Only after steps 1-15 succeed may candidate A begin.

## Freeze receipt conditions

The resulting freeze receipt must state:

- `candidate_outputs_seen = 0`;
- `candidate_owned_roots_consulted = []`;
- `candidate_owned_state_reused = false`;
- a freeze ordinal earlier than any first candidate-output ordinal;
- `state = FROZEN_READ_ONLY`.

Any violation stops the court as `FAIL_CLOSED__ORACLE_NOT_INDEPENDENT` or equivalent integration-level failure.

## Candidate comparison

Each candidate must later construct an observation containing:

- source identity;
- court constitution refs;
- exact semantic authority closure and digest;
- projection/release refs;
- complete frontier and digest;
- exact I03 fact manifest and typed states;
- complete I05 learned product/coverage;
- semantic/replay/exact-output identities;
- replay/dependency closure;
- exact refs;
- negative-state manifest;
- the frozen oracle identity.

Then invoke `validate_candidate_observation(...)` independently for A, B, and C.

Only after all three individual receipts PASS may the court invoke `validate_three_way_parity(...)`.

Pairwise A/B/C equality is corroborative only. It never supplies expected truth.

## Stop conditions

Stop without measured candidate execution if any of the following occurs:

- source hash/shape mismatch;
- missing or stale Lock2/authority ref;
- fuzzy/default/latest authority resolution;
- frontier count, membership, order, or family-shape drift;
- candidate-owned state enters oracle provenance;
- materialization attempts to infer semantics from labels/frequencies/layout/missingness;
- typed negative states collapse;
- C11/I03/I05 fails closed;
- oracle freeze occurs after a candidate output;
- oracle bundle mutates after freeze.

## Result status in this worker

`SOURCE_MATERIALIZATION_PENDING_LOCAL_EXECUTION`.

No local source bytes were opened and no WVS empirical values/product identities were fabricated.
