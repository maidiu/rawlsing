# PYAT HQ117 — Dependency, Replay, Reconstruction and Explanation Contract

## 1. Purpose

M2 release identity is only durable if a future auditor can answer four different questions without substitution:

1. What exact semantic subject was released?
2. From which exact governed prerequisites was it derived?
3. What exact changes could invalidate or alter it?
4. How can the historical result be reconstructed or explained now?

This file separates those questions into dependency, determinant, replay/reconstruction and explanation closures.

## 2. Closure noncollapse

Freeze:

DEPENDENCY_CLOSURE != DETERMINANT_CLOSURE != REPLAY_CLOSURE != EXPLANATION_LINEAGE

A single content-addressed DAG may physically store all four, but the semantic roles remain distinct.

### Dependency closure

Exact prerequisites consumed by the producer-owned semantic subject.

### Determinant closure

Exact governed identities whose change can alter the subject's derivation, validity, scope, or reconstruction.

### Replay/reconstruction closure

Exact material needed to recover the historical result or execute the promised historical operation under the declared replay grade.

### Explanation lineage

Exact reverse path proving why the released subject exists, including typed negatives, refusals, ceilings and authority roots.

## 3. Dependency contract

Every release must bind an exact direct-dependency closure supplied or certified by the semantic producer.

Rules:
- dependencies use exact refs;
- dependency role is explicit where order/cardinality/role matters;
- no dependency is inferred from physical co-location;
- no dependency is omitted because an upstream object is "obvious";
- no producer object is copied into M2 ownership;
- a direct dependency on another release points to that exact release id, never to its mutable current selector;
- a direct dependency on a producer object may remain a direct producer ref where no release wrapper is required.

The dependency graph may contain both released and directly referenced upstream objects.

## 4. Determinant contract

A determinant is a governed identity whose change can alter a product's lawful reconstruction, semantic validity or claimed completeness.

Typical determinant classes include:
- source content/release identity;
- decoder/executable projection identity;
- source-semantic/question/value/topology/routing/risk-set authority;
- weight/design/estimand authority;
- discovery authority/frontier/profile;
- validation/adjudication authority;
- source-universe relation or comparability authority where required;
- model/proxy authority;
- algorithm/compiler/model/configuration identity;
- random stream, subsampling, tie-breaking, branch expansion, search budget and stop rules for adaptive procedures;
- prerequisite-universe/completeness receipts where the claim depends on completeness;
- exact upstream learned release where the subject is derived from it.

Rules:
- determinant membership is producer-/operation-governed, not guessed by M2;
- a physical cache key is not a semantic determinant unless the cache itself is the governed subject;
- wall-clock time, Git recency and mutable environment state are forbidden hidden determinants;
- if executable environment closure is required for exact replay, it must be explicitly pinned or the release must declare a weaker replay grade.

## 5. Selective invalidation law

C07/C08 and Authority31 constrain future M2/M3 integration:

CHANGED_EXACT_DETERMINANT
-> EXACT_DIRECT_DEPENDENTS
-> TRANSITIVE_AFFECTED_DEPENDENCY_CLOSURE

not:

ANY_CHANGE -> GLOBAL_PURGE

Examples:
- source-wave content change affects descendants citing that exact source/release root;
- question/semantic binding change affects descendants of that binding;
- validation-rule change affects validated/released products depending on that rule, not immutable source facts that do not;
- possibility-model change affects that model release and derived possibility fields, not unrelated empirical facts;
- structural admission change affects structural descendants under that admission edge;
- cache corruption affects the cache/materialization only if the semantic subject is independently reconstructible.

M2 records enough exact graph information for a lifecycle engine to find affected releases.

M2 does NOT infer the lifecycle meaning of the change.

Freeze:

DEPENDENCY_EFFECT_IS_DERIVATIVE
LIFECYCLE_MEANING_IS_GOVERNED_ELSEWHERE

## 6. Replay grades

Every release must declare one exact replay/reconstruction grade.

### R1 — EXACT_MATERIALIZED_DEREFERENCE

The exact semantic subject is immutably materialized and can be verified directly.

Required:
- exact subject hash/ref;
- exact release core;
- representation integrity;
- producer identity;
- authority/dependency/determinant closure;
- explanation lineage.

### R2 — EXACT_DETERMINISTIC_REBUILD

No durable payload representation is required, but the exact semantic subject can be reconstructed deterministically.

Required:
- exact source/upstream roots;
- complete non-source-derivable semantic bindings;
- exact executable decoder/projection/compiler/model configuration where constitutive;
- exact algorithm/search/randomness determinants;
- exact rebuild instructions;
- exact expected semantic identity/hash;
- hostile check that a rebuild cannot silently substitute current authority.

### R3 — EXACT_SERVICE_REEXECUTION

The release subject is a governed learned service contract and a historical invocation can be replayed from an exact invocation receipt.

Required:
- exact service release id;
- exact invocation input refs;
- exact authority closure;
- exact model/algorithm/configuration determinants;
- named random stream/subsampling/search determinants where applicable;
- exact expected output identity or output-check contract;
- typed handling of external dependency unavailability.

### R4 — HISTORICAL_EXPLANATION_ONLY

The release remains a valid historical semantic citation but executable reconstruction is not promised.

Required:
- exact historical subject identity;
- exact producer identity;
- authority/dependency/explanation closure;
- explicit reason executable replay is not claimed;
- no misleading "replayable" label.

R4 is lawful where history must remain citable but old execution environments cannot be exactly reproduced. It cannot satisfy a consumer that explicitly requires executable replay.

## 7. Virtual/rebuildable release theorem

A release can be durable while its payload is virtual.

A virtual release is lawful iff:
- exact semantic subject identity is durable;
- source/upstream roots remain accessible or separately governed as durable inputs;
- non-source-derived semantic authority/configuration is durable;
- replay grade is explicit;
- reconstruction instructions and expected identity are exact;
- reconstruction failure fails closed;
- no mutable "current" authority can be substituted.

Therefore:

NO_DURABLE_PAYLOAD != NO_RELEASE

but also:

SOURCE_BYTES_EXIST != REPLAY_CLOSURE_COMPLETE

## 8. Decoder/environment closure

C06 established that naming a decoder library/version alone is not automatically durable executable closure.

A future M2 implementation must either:
- pin a sufficiently exact executable dependency/environment closure;
- supply a hostile decode/rebuild oracle proving the historical semantics under an accepted portable contract; or
- declare that exact executable replay is not promised.

It may not overclaim R2/R3 replay grade from a package name.

## 9. Adaptive discovery/service replay

Where a released subject depends on adaptive/open-ended discovery, replay determinants may include:
- initial frontier;
- candidate enumeration order;
- branch expansion law;
- tie-breaking;
- budget accounting;
- stop conditions;
- named random streams;
- subsampling/split identity;
- validation split;
- state-transition/checkpoint identity;
- coverage/unvisited-state accounting.

A partial/nonexhaustive search release must preserve that status and may not replay as an exhaustive absence claim.

## 10. Explanation lineage contract

Explanation lineage is not a prose note. It is a governed reverse-reference graph.

Minimum reverse walk:

RELEASE_ID
-> RELEASE_SUBJECT_REF
-> PRODUCER_CONTRACT_REF
-> PRODUCER EVIDENCE / ADJUDICATION REFS
-> AUTHORITY CLOSURE
-> SOURCE / UPSTREAM RELEASE ROOTS

Where relevant it additionally traverses:
- query/predicate identity;
- risk-set/denominator identity;
- support/uncertainty;
- validation rule;
- comparison/composition authority;
- model/proxy authority;
- structural admission;
- typed refusal/blocker.

The lineage must not skip a negative or unresolved node merely because it makes the final product harder to summarize.

## 11. Explanation versus semantic ownership

M2 may aggregate exact refs into an explanation graph.

It may not translate them into a new semantic proposition.

An explanation view is a projection over producer-owned facts.

If M2 materializes human-readable text:
- it is nonauthoritative unless separately governed;
- exact refs must remain available beneath it;
- paraphrase cannot replace typed semantic state.

## 12. Historical authority pinning

Historical release replay resolves the exact authority instance ids/versions/hashes bound by the release.

Forbidden:
- latest;
- default;
- fuzzy;
- nearest;
- semver fallback;
- "newest compatible";
- repository-presence inference;
- reinterpretation under a successor authority merely because it is current today.

A historical product is replayed under its historical authority closure.

A later recertification/correction is a separate release/lifecycle fact.

## 13. Reconstruction parity

A rebuilt representation passes only if it preserves the release subject's exact semantic identity at the producer's grain.

Byte-identical physical output is not universally required.

Semantic parity may be sufficient only when the producer contract defines exact semantic identity independent of physical bytes and all identity-bearing anatomy is recovered.

Examples:
- row order may be physical-only in one product and semantic in another;
- serializer whitespace is normally non-semantic;
- higher-order role order may be semantic and must survive;
- typed absence classes may be semantic and must survive.

M2 cannot decide these distinctions generically; it enforces the producer contract.

## 14. Replay failure states

Resolution/replay MUST distinguish at least:
- RELEASE_NOT_FOUND
- PUBLICATION_BINDING_NOT_FOUND
- SUBJECT_REF_MISMATCH
- AUTHORITY_CLOSURE_MISMATCH
- DEPENDENCY_CLOSURE_MISMATCH
- DETERMINANT_CLOSURE_MISMATCH
- REPLAY_PREIMAGE_INCOMPLETE
- EXECUTABLE_DEPENDENCY_UNAVAILABLE
- SOURCE_CONTENT_MISMATCH
- SEMANTIC_REBUILD_MISMATCH
- INTEGRITY_FAILURE

No failure state may fall back to another release.

## 15. M3 interface

M2 provides M3:
- exact release ids;
- exact determinant/dependency graph;
- exact historical closures;
- exact reconstruction/replay grade.

M3 can then apply explicit typed lifecycle law and current selection.

The dependency engine may compute an affected set, but M3 or the competent lifecycle authority classifies the event.

This preserves P2:

DEPENDENCY_ENGINE_EXECUTES_CONSEQUENCES__DOES_NOT_INFER_LIFECYCLE_MEANING
