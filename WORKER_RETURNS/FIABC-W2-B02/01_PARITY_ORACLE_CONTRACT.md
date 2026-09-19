# FIABC-W2-B02 — Independent Semantic / Negative-State Parity Oracle Contract

Worker: `FIABC-W2-B02`

Branch: `agent/rabochii-premain-fiabc-w2-b02-independent-parity-oracle-r1`

Base: `dfdae1dfcef5e3061094935312c3db2cc0fde2f0`

Commission terminal on successful specification:

`FIABC_W2_B02_INDEPENDENT_A_B_C_PARITY_ORACLE_SPECIFIED`

## 1. Court question

The A/B/C court needs an oracle that proves that candidate-specific physical realization has not changed the invariant logical workload. The oracle must therefore be **candidate-neutral, causally prior to candidate output, exact-ref aware, frontier-complete, replay/provenance aware, authority-closure aware, and typed-negative-state aware**.

The current P2X S03 mechanism does not meet that standard. At the Wave-1 audited P2X ref `617c9c9426db12a3c0f7fea6b68a582c10759553`, Wave-1 B03 records that S01 marks candidate output before S03 freezes its oracle; S03 then performs same-candidate I03 replay through the same binding and maps one equality result across multiple parity categories. That proves at most self-replay consistency. It cannot prove that A/B/C preserve a candidate-independent expected truth.

The replacement contract below deliberately separates:

1. **who owns semantic truth** — accepted common upstream authority and canonical PRE553 semantic law;
2. **who pays to realize it** — candidate A/B/C physical implementations under the measurement court; and
3. **who adjudicates parity** — a court-owned oracle bundle that neither candidate defines nor mutates.

## 2. Core theorem

For a source-local court `S`, let `O_S` be one immutable candidate-neutral oracle bundle and let `R_{S,c}` be the governed output receipt for candidate `c ∈ {A,B,C}`.

A three-way semantic parity PASS is lawful only if all of the following hold:

- `O_S` was frozen before any `R_{S,c}` existed;
- `O_S` depends only on exact source identity, accepted candidate-neutral semantic/routing/query/discovery authority, accepted immutable prior empirical evidence where explicitly allowed, and current common semantic producers;
- `O_S` contains the complete fixed workload frontier and the expected semantic/replay/authority material required by this contract;
- each candidate receipt independently matches the same `O_S` at every applicable assertion row;
- no candidate output, candidate repository, candidate cache, candidate session, or candidate-specific transformed carrier is in the transitive dependency closure of `O_S`;
- pairwise candidate equality is treated as corroboration only, never as the source of expected truth;
- typed negative and governance states are compared at their correct layer and never collapsed into ordinary empirical values.

Formally:

`PARITY_PASS(S) = FREEZE_OK(O_S) ∧ COMPLETE(O_S) ∧ ⋀c MATCH(R_{S,c}, O_S)`

and **not**:

`R_{S,A} = R_{S,B} = R_{S,C}`

alone, nor:

`REPLAY(R_{S,c}) = R_{S,c}`

alone.

If one candidate is currently nonqualified for a source, the court may record candidate-specific evidence, but it may not emit a three-way parity PASS for that source.

## 3. Oracle bundle contract

Each source-local oracle is a content-addressed object with schema conceptually equivalent to:

`RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0`

It SHALL contain:

- `source_identity`: exact filename/release identity, byte length, SHA-256, rows/variables where frozen;
- `court_constitution_refs`: exact Lock1/Lock2 refs and hashes relevant to the source;
- `semantic_authority_closure`: the exact set of authority snapshot refs/ids/versions/content hashes required by the frozen workload;
- `projection_and_release_refs`: exact current governed projection/C11/replay identities where already frozen as invariant inputs;
- `frontier_manifest`: exact candidate hashes, role/query/predicate refs, canonical order, family shape, and completeness claim;
- `expected_fact_manifest`: one expected semantic fact record for every frozen query/role/candidate result required at the comparison terminal, including typed state, exact semantic fields, denominator/support or other exact measure material, and all canonical exact refs that are current-object invariants;
- `expected_learned_product`: exact governed learned-product identity/hash and semantic replay identity when the comparison terminal includes I05 learned production;
- `replay_manifest`: deterministic replay roots and dependency refs for each compared object/fact/product;
- `negative_state_manifest`: all typed distinctions required by Section 8 below;
- `authority_closure_digest`: canonical digest over the exact authority-ref set;
- `frontier_digest`: canonical digest over the full ordered frontier, not merely the candidate count;
- `oracle_build_provenance`: immutable builder/ref, exact inputs, common semantic producers used, and source-open receipt where applicable;
- `freeze_receipt`: oracle bundle hash, freeze event/order, candidate-output count observed at freeze (`0` required), candidate-owned roots consulted (`[]` required), and read-only/final state.

The oracle bundle is court evidence. It is not a new semantic owner and does not move authority away from the accepted upstream producers.

## 4. Independence law

### 4.1 Permitted dependencies

The oracle MAY depend on candidate-neutral common upstream material because A/B/C are not intended to re-adjudicate semantic truth. Permitted dependencies include:

- exact source bytes and the accepted format-neutral physical decoder;
- accepted source-specific semantic/routing/topology/query/discovery authority;
- canonical PRE553 object constructors and exact-ref/replay rules;
- the common governed source-backed C11 semantic facade **when invoked as a court-neutral semantic producer, not through a candidate measured repository/session**;
- the common I03 exact empirical semantics and I05 exact-bounded discovery semantics;
- accepted immutable prior empirical products explicitly frozen into the court, such as the LiTS ASTRA-D04-R2 learned empirical product.

This reuse is lawful because those components own invariant semantic truth, not the candidate-specific physical treatment.

### 4.2 Forbidden dependencies

The oracle MUST NOT depend on:

- `R_{S,A}`, `R_{S,B}`, or `R_{S,C}` or any field derived from them;
- the current candidate's `binding.repository`, durable root, scratch root, cache, transformed carrier, accelerator state, or session state;
- a candidate-selected query/frontier subset;
- a candidate-emitted ExactRef used as the expected ExactRef;
- a candidate-emitted replay root used as the expected replay root;
- majority vote or agreement among candidate results;
- “first successful candidate” output;
- latest/default/fuzzy authority selection;
- post-outcome frontier editing, pruning, ranking, substitution, or candidate deletion.

A court-neutral invocation of common semantic code must use separate oracle-owned roots and must be completed/frozen before candidate execution. Its produced state may not be mounted into a candidate run.

## 5. Source-specific oracle construction

### 5.1 LiTS-I

LiTS has accepted candidate-neutral empirical truth that predates the A/B/C court. The primary semantic-fact anchor is:

- commit `e631de162c582423639b7067a4f36b29f8aa4d89`;
- `WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json`;
- exact source SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- frozen frontier `50` candidates / `77` query roles, frontier seal `ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`;
- terminal counts `49 EVALUATED_SUPPORTED + 1 EVALUATED_VALID_EMPTY`;
- learned-product SHA-256 `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`;
- semantic replay hash `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`.

Lock1 additionally freezes LiTS projection/C11 identity:

- projection cache identity `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`;
- C11 logical release `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`;
- C11 replay manifest `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`.

LiTS semantic facts MAY be imported from the immutable D04-R2 product. Current ExactRef/authority-closure expectations SHALL be frozen from the current accepted PRE553 authority/catalog objects before candidate execution; an older product must not be treated as authority for a newer ExactRef schema merely because its semantic facts are accepted.

The LiTS oracle therefore joins **accepted prior factual truth** with **current candidate-neutral exact-ref/authority truth**. Neither side may be taken from the candidate under test.

### 5.2 WVS7

Lock2 freezes the WVS workload before source outcomes:

- source SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- Lock2 hash `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`;
- Lock2 replay hash `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`;
- candidate grammar `a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6`;
- DiscoveryAuthority `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`;
- EmpiricalUniverse `f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e`;
- risk set `0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7`;
- raw/unweighted measure basis `6ed5d61b77c8d77affeb4b49b55c2cc23a4c25dbd65d02719c6ab7a3069a3c79`;
- exact ordered 46-candidate list in `WORKER_RETURNS/EE-P2F2/05_WVS7_DISCOVERY_AUTHORITY_AND_FRONTIER_BINDING.json` at `22667bd395e7293f99b285daddad36fe3a4377ef`;
- family shape `10 unary + 1 pair-cotravel + 10 directed branch-conditioned + 25 joint-support`.

Lock2 does **not** contain WVS outcomes. Therefore a lawful WVS oracle MUST materialize the 46-candidate expected fact/product bundle after exact source verification but **before A, B, or C produces a candidate output**.

That materialization SHALL use only the exact WVS source plus the accepted candidate-neutral semantic/routing/query/discovery closure. It may use the current common decoder/C11/I03/I05 semantic producers in a court-neutral invocation, but it may not use any candidate measured repository/session/cache/output. The resulting 46-record fact manifest, learned-product identity, exact refs, replay roots, and authority closure are then frozen as `O_WVS7` and made read-only before candidate execution starts.

This is not post-outcome workload mutation: the frontier, authorities, query roles, and validation laws are already frozen by Lock2. Only the expected empirical values for that pre-existing frontier are being materialized.

## 6. Freeze and causal-order law

For each source:

1. verify exact source identity;
2. verify Lock1/Lock2 and exact authority closure;
3. materialize the complete candidate-neutral oracle bundle;
4. canonicalize and hash the bundle;
5. write an immutable freeze receipt proving `candidate_outputs_seen = 0` and `candidate_owned_roots_consulted = []`;
6. only then start candidate A, followed by B and C under the separate measurement constitution.

The verifier MUST reject any run where:

- `oracle_freeze_event >= candidate_output_first_event`;
- an oracle dependency path resolves into a candidate-owned root;
- the oracle hash changes after the first candidate starts;
- the candidate frontier differs from the oracle frontier;
- the candidate itself supplies a missing oracle field.

The present S03 ordering therefore cannot be grandfathered merely because same-candidate replay is deterministic.

## 7. Exact parity dimensions

Every executed candidate SHALL be checked independently against the same source-local oracle on all applicable dimensions:

1. **Source identity parity** — exact source hash/release, no substitute bytes.
2. **Authority closure parity** — exact authority refs/versions/hashes; no candidate-specific semantic authority and no latest/default/fuzzy selection.
3. **Projection/release parity** — exact current governed projection and C11/replay identities where frozen.
4. **Frontier parity** — exact candidate list, role list, predicate/query refs, canonical order, family shape, and no missing/extra work.
5. **Semantic fact parity** — every expected fact's typed state and exact semantic fields, including exact denominator/support/joint/conditional material as applicable.
6. **ExactRef/identity parity** — kind/object_id/content_hash for all canonical objects where current object identity is invariant.
7. **Replay parity** — producer replay roots, dependency refs, negative-fact replay refs, learned-product replay identity.
8. **Learned-product parity** — complete governed product identity/hash, not just a count summary.
9. **Typed negative parity** — all Section 8 distinctions at exact fact/event/governance grain.
10. **Fail-closed parity** — missing authority, unresolved routing, topology incompatibility, source relation uncertainty, or integrity failure must stop/return the same typed disposition rather than silently produce a usable fact.

Performance is admissible only after every required parity dimension passes for that candidate/source cell. Pairwise A/B/C equality is a secondary check after oracle matching, not a replacement for it.

## 8. Negative-state law inherited from Wave-1 B04

The oracle SHALL preserve the following distinctions explicitly:

- physical missingness != semantic response state;
- routing unknown/rule unavailable != nonmember != inapplicable;
- `UNKNOWN` typed absence/authority/source meaning != Python `None`/omitted key;
- all-missing/topology incompatibility/no-event/empty multiselect are not interchangeable;
- source-local unresolved relation != inferred cross-source equivalence;
- `VALID_EMPTY` != unavailable/unresolved/integrity failure;
- `DENIED` / `NONCOMPARABLE` != scalar ordinary value;
- `BLOCKED` and manual-review are governance/court dispositions, not public empirical values.

For `BLOCKED` or review-needed conditions, the oracle compares **governance behavior and preserved underlying typed evidence**, not a fabricated response/fact value. A court stop cannot be counted as `VALID_EMPTY`, `UNKNOWN`, zero support, or an ordinary result.

## 9. Authority-closure law

For every expected object/fact/product, the oracle stores the exact transitive authority/dependency closure that is required at the comparison terminal. A candidate passes only if:

- the observed closure equals the expected exact set at the governed grain;
- every ref resolves to the frozen accepted owner/version/hash;
- there is no candidate-specific additional semantic authority;
- there is no missing expected authority;
- no historical/stale authority is silently substituted for the current accepted owner;
- no semantic fact is accepted merely because its scalar value matches while its authority or replay closure differs.

This contract does not claim that Wave-2 L02's P2X claim-scoped authority BOM is already complete. When L02 supplies the closed BOM, that BOM becomes the authoritative closure set consumed by this oracle. If L02 returns a typed unresolved/missing authority required by the selected comparison boundary, this oracle must fail closed at that exact proposition; it must not synthesize the missing authority.

## 10. Full-frontier law

A parity PASS requires complete coverage, not spot checks.

- LiTS: all 50 frozen candidates and all 77 frozen query roles must be represented and compared; lane counts and the one `EVALUATED_VALID_EMPTY` case are part of the expected result surface.
- WVS7: the exact ordered 46 hashes from EE-P2F2 must be present, once each, with the frozen 10/1/10/25 family shape and all referenced roles/predicates/queries. Missing, duplicate, extra, reordered-when-order-is-canonical, or post-outcome substituted candidates fail the frontier gate.

Hash equality over a summary object is useful but not sufficient by itself. The verifier must also validate membership/cardinality/order and per-record bindings so that an incorrectly scoped summary cannot hide an omitted cell.

## 11. Self-replay exclusion proof

The court SHALL record three separate predicates:

- `SELF_REPLAY_OK(c)`: candidate `c` can reproduce its own output from its own governed determinants;
- `ORACLE_MATCH(c)`: candidate `c` matches the candidate-neutral oracle;
- `CROSS_CANDIDATE_PARITY`: all required candidates independently satisfy `ORACLE_MATCH` against the same frozen oracle.

`SELF_REPLAY_OK(c)` is valuable replay evidence but has no implication to `ORACLE_MATCH(c)`.

The verifier MUST have no transition of the form:

`SELF_REPLAY_OK -> SEMANTIC_PARITY_PASS`

and MUST reject a receipt that maps one same-binding equality bit onto semantic, ExactRef, replay, fail-closed, and frontier/typed-negative parity categories.

The negative-test fixture table in `03_HOSTILE_ORACLE_FIXTURES.csv` exercises the principal false-PASS routes.

## 12. Cost/accounting interaction

Oracle materialization is candidate-neutral court work. It SHALL NOT become candidate-owned state and SHALL NOT be reused to satisfy one candidate's measured physical construction. Its cost treatment and any required cache/host reset are delegated to FIABC-W2-B03's equal-work accounting constitution.

This contract therefore specifies **semantic independence**, not a new performance-accounting rule.

## 13. What this PASS does and does not prove

This specification closes Wave-1 open cell OC07 at design-contract grain: it defines a candidate-neutral oracle capable of proving semantic/typed-negative parity without using candidate output as expected truth.

It does **not** claim:

- that current P2X has executed this oracle;
- that A/B/C have measured parity;
- that Candidate C is qualified on both sources;
- that L02 authority closure, L01/L05 comparison-boundary adjudication, B01 post-repair live consumption, or B03 equal-work accounting has passed.

Those are separate Wave-2 burdens. The oracle fails closed on their exact unresolved inputs rather than papering over them.

Terminal:

`FIABC_W2_B02_INDEPENDENT_A_B_C_PARITY_ORACLE_SPECIFIED`
