# C06 — Source-Backed Replay and Integrity Contract

Status: `NON_DISPOSITIVE__RETURN_EVIDENCE`
Cell: `VC4-COMPILER/PERSISTENCE — C06`

## Holding

C06 finds **no identity or integrity law at the launch HEAD that proves a permanent full canonical event payload is irreducible**. Current PRE553 public objects derive `object_id` and `content_hash` from canonical semantic projections, `ExactRef` is `(kind, object_id, content_hash)`, C11 internal records are likewise content-addressed, and current R5 law already separates semantic-release identity from physical-carrier identity.

That does **not** justify a full C06 pass. End-to-end deletion of transformed empirical copies is not yet proven replay-complete because four independent requirements remain unclosed:

1. `SOURCE→C11 OCCURRENCE IDENTITY`: source law requires occurrence/event/slot identity where applicable and C11 validates distinct occurrences, but C06 did not find a general frozen derivation law for `response_event_id_or_deterministic_index`; therefore exact source-backed recreation of every event-occurrence identity is not yet proved;
2. `R12/R20`: recovered adaptive autonomous discovery lacks a frozen search/termination/state-transition law sufficient to prove backend-independent replay and typed completeness;
3. `R13`: durable executable decoder replay is not closed by `pyreadstat` package/version plus ordinary dependency labels alone;
4. `R08/R14`: the recovered candidate→validation→governed empirical learned-product boundary requires exact validation/model-selection authority and lineage not established by the current exact-bounded I05 implementation.

Disposition therefore remains `C06_RETURN__NAMED_EVIDENCE_REQUIRED`, not a full-event-persistence block.

## 1. Minimum persistent layers

### P1 — authoritative past
Persist immutable source bytes and their exact snapshot/release manifests. Paths, `latest`, filenames alone, cache membership, and transformed carrier roots are not source identity.

### P2 — governed semantics and learned products
Persist exact historical semantic/source authority snapshots. Persist any accepted empirical learned release and structural learned release as first-class governed products even when rebuildable. Rebuildability is not semantic disposability.

### P3 — replay/provenance receipts
Persist the smallest closure that proves:
- exact source and release identity;
- executable decoder identity/closure;
- authority root;
- exact source→C11 respondent/question/topology/event-occurrence derivation law or historical replay binding;
- semantic projection/canonicalization/replay protocol;
- pinned historical ExactRefs and semantic release roots;
- source traversal completeness;
- exact query/frontier definitions;
- typed search completion/stop/failure state;
- adaptive branch/frontier determinants when such law exists;
- validation state/evidence and model-selection rule when governed;
- I04 admission provenance;
- learned-product explanation lineage;
- publication/dependency closure;
- explicit randomness and fresh-process replay comparison.

### P4/P5/P6
Caches are optional and nonauthoritative; compiler working sets are transient; exact C11 projections/IDs/hashes may be derived on demand only when their complete determinant set and derivation rules are closed.

## 2. Exact identity without a full event carrier

For current PRE553 semantic objects:

`semantic_projection -> canonical_json -> SHA256 -> content_hash`

and:

`object_id = family-scoped URN(content_hash)`

then:

`ExactRef = (kind, object_id, content_hash)`.

For a `RespondentEvent`, the projection includes universe/respondent/question/component/event-occurrence/raw+canonical response/transform authority/topology/order-rank/state determinants. Therefore the physical row in a Parquet/R5 member is not itself the semantic identity determinant.

However, content-addressability only proves identity **after the semantic projection is known**. Source-backed replay must also reproduce every identity-bearing field in that projection. `09_SOURCE_NATIVE_CONSTITUTION.md` requires source occurrence/event/slot identity where applicable; `pre553_c11_integrity.py` rejects duplicate occurrence material; but current C11 ingest consumes `event_group_id` and `response_event_id_or_deterministic_index` rather than supplying a general source→occurrence derivation rule. C06 therefore cannot certify universal source-backed `RespondentEvent` identity recreation until that derivation/replay determinant is frozen. This is a missing-law witness, not an event-payload-persistence witness.

Historical consumers should retain the expected ExactRef/release root in P3 even if it is recomputable. Replay is verification against a pinned historical identity, not merely a new self-consistent rehash.

## 3. Source replay and completeness

A source-backed negative is lawful only when the run can prove all of the following for the exact source snapshot and decoder replay identity:
- every governed source region required by the operation was traversed;
- expected rows/variables/events or another governed source inventory are reconciled;
- no read/decode failure occurred;
- no compatibility path failed or silently fell back;
- no interrupted build remains ambiguously publishable;
- any optional cache/partition omission was either irrelevant to semantics or regenerated;
- terminal EOF is corroborated by governed inventory/count/coverage evidence.

`reader EOF` alone is not semantic proof.

## 4. Query/search completeness law

The following states are non-interchangeable:

`COMPLETE_AUTHORIZED_SEARCH__NO_RELATION`
`PARTIAL_FRONTIER`
`SEARCH_BUDGET_EXHAUSTED`
`UNSUPPORTED_OR_NONCOMPARABLE_DOMAIN`
`CANDIDATE_FOUND__VALIDATION_FAILED`
`CANDIDATE_FOUND__VALIDATED`.

A complete negative requires both source-traversal completeness and governed query/search-frontier completeness. A stale cache, empty result, exception-swallowing path, reader failure, or budget stop can never be promoted into empirical absence.

Current `PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0` has a valid narrow proof: authority fixes a finite/finitely constructible frontier; pruning is `NONE_EXACT_EVALUATE_ALL`; proposal RNG is absent; tie order is `CANONICAL_CANDIDATE_HASH_ORDER`; `candidate_count == covered_candidate_count` is required. That proves the exact declared frontier only.

It does **not** prove the recovered adaptive program because the implementation explicitly declares `No adaptive traversal`.

## 5. Adaptive backend-independence

When adaptive discovery becomes executable, semantic replay must bind every execution choice capable of changing which candidates are reached or accepted: logical candidate enumeration, branch expansion, tie and floating comparison law, budgets, stop conditions, randomness, subsampling, validation splits, frontier accounting, and candidate/validation state transitions.

Physical backend iteration order, worker scheduling, filesystem order, shard boundaries, cache dictionary order, or parallel arrival order may affect cost but may not silently change the learned world. If any such order is intentionally semantic, it must first become explicit governed logical order and enter replay identity.

## 6. Decoder replay

`reader = pyreadstat` plus `reader_version = X` is useful provenance but not durable executable closure. The source decoder imports a native/package stack at runtime and its code performs output-sensitive normalization and compatibility handling.

C06 therefore requires content-addressed retention or immutable addressing of the decoder code and every output-sensitive executable dependency/environment determinant, plus hostile decode vectors with expected results. An executable capsule is one possible realization; it is not prescribed.

## 7. Learned-product and structural provenance

An empirical learned release requires its own identity and explanation lineage. A structural admission must retain exact empirical evidence refs, I04 rule/authority, target use, scope/time/weight/uncertainty and nonpositive-limit refs. V557/V558 then preserves producer object identity/build/hash and transitive closure; repository IDs remain administrative.

Deleting an empirical carrier therefore need not break structural provenance if the source/decoder/source→C11 derivation/authority/replay/learned/admission/publication closure survives.

## 8. Cache law

A cache key must bind every semantic determinant relevant to its contents, including source, decoder, authority, compiler/query/search/model identity and semantic release/root. Any mismatch is stale. Cache absence or deletion changes cost only. Cache state cannot prove a negative, seal completeness, enlarge/restrict discovery vocabulary, or serve as empirical authority.

## 9. Delete-transforms thought experiment

| Test | C06 finding |
|---|---|
| 1. reconstruct exact C11 identities | `PARTIAL__SOURCE_ROOTED_IN_PRINCIPLE`; deterministic object hashing is closed, but universal event-occurrence index derivation is not yet proved |
| 2. reproduce ExactRefs/content hashes | `YES_WHEN_ALL_IDENTITY_BEARING_PROJECTION_FIELDS_ARE_REPRODUCED`; occurrence-field gap prevents universal certification |
| 3. distinguish true negative from incomplete/budget exhausted | `YES_FOR_CURRENT_EXACT_BOUNDED_FRONTIER`; `NOT_YET_CLOSED` for recovered adaptive/general search |
| 4. reproduce adaptive discovery when law exists | `YES_REQUIREMENT_DEFINED`; current law not sufficiently frozen |
| 5. detect source/authority/decoder drift | source/authority `YES`; durable decoder replay `NOT_YET_CLOSED` |
| 6. reconstruct explanation lineage | `YES_IF_P3_LINEAGE_RECEIPT_PERSISTS`; current recovered empirical product law incomplete |
| 7. audit learned empirical relation | `NOT_YET_END_TO_END` until occurrence replay where relevant, validation/model-selection and adaptive lineage are frozen |
| 8. audit structural admission | `YES` for an already-persisted exact I04 admission/producer closure; fresh source-backed reconstruction of its empirical antecedents inherits the occurrence/decoder gaps |
| 9. fresh-process deterministic replay | `NOT_YET_END_TO_END` because occurrence-derivation/R12/R13/R08 gaps remain |

The smallest missing things are **not demonstrated to be event payloads**. They are: a frozen/replayable event-occurrence derivation or exact historical occurrence binding; a frozen adaptive search/termination/state-transition authority; durable executable decoder closure; and the governed validation/model-selection lineage needed for accepted empirical learned products. After those laws exist, compact P3 completeness/replay receipts can preserve historical execution without duplicating respondent payloads.

## 10. Integrity failure rule

Fail closed on wrong source hash, wrong decoder closure/config, missing source→C11 occurrence derivation/replay binding, missing historical authority, ExactRef mismatch, semantic projection mismatch, incomplete source traversal, partial publication, stale cache, interrupted build, unproved frontier coverage, budget exhaustion presented as negative, adaptive replay divergence, missing validation authority, or broken learned-product/admission/publication closure.

No finding in this return selects A/B/C or reopens active R5 authority.
