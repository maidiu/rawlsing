# P01-S2 — Validator-complete, identity-exact bounded I02 journal and source-view admission

**Owner:** Browser Architecture HQ, DIRECT, NO RABOCHII.
**Date / cut:** 2026-10-28. Exact control source `299f41e97a43c67be9cc76a79fa49b48f4e12e54`.
**Decision:** one source-authoritative compact regenerable hybrid; I02-validated verified source-backed view within existing `C11Repository`, retaining unchanged materialized `C11LogicalRelease`.
**State:** DESIGN AND VALIDATOR MAPPING COMPLETE AT NAMED CURRENT-CONTROL SOURCE; small source-free canonical/validity oracles PASS; streaming validator itself NOT IMPLEMENTED, NOT fully equivalent, NOT original-survey-executed. Work remains in S3 for exact coding tickets and complete dual-engine tests.
**Companions:** `P01_S0_CURRENT_C11_CONSUMER_AND_IDENTITY_AUDIT_R1.md`; `P01_S0_CONTROL_SYMBOL_CENSUS.json`; `P01_S1_SEALED_SOURCE_EXECUTION_VIEW_CONTRACT_R1.md`; `P01_HIGH_RESOLUTION_RETURN_LEDGER.json`. Mandatory HQ nondelegation document 14.

## 1. Exact owned source, not secondhand worker assertions

Verified via direct GitHub current-control file and locally SHA-checked packet (Git blob):
- `rawlsing_next/pre553_c11_ingest.py` **37cd35fa2e3420a3eea272a2902e96ab9ba38aba**: sections / candidate hashing / closure / validation / sealing.
- `rawlsing_next/pre553_c11_integrity.py` **7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd**: internal object and ReplayManifest identity, per-public-object validation and M01–M18.
- `rawlsing_next/pre553_c11_repository.py` **67c6eb6494522cd11aab1b93d0e73f9cef6036f3**: sealed logical release, exact lookups, _commit_validated.
- `rawlsing_next/pre553_empirical_objects.py` **a61365b994e5c3c50de0f598fcf40e90abf757b6**: canonical_json, semantic_hash, ExactRef, semantic objects.
- `rawlsing_next/pre553_empirical_authority.py` **ca65a7fd4d52f0c44447434559b1d09412e7aa39**: authority registry.
- `rawlsing_next/pre553_source_backed_c11_facade.py` **8a761119e4a8d68eb291fc4edfadb52e027f8284**: SHA and source-retention checks, complete slot coverage, source-backed projection and current full-object session cache.

**Known external consumers:** `pre553_source_equivalence.py` strict concrete C11; `pre553_replay_audit.py` concrete C11 and full object audit; `pre553_parquet_carrier.py` eager Parquet/Zstd and _make_validated_release; `pre553_empirical_query.py` + `_pre553_query_predicate.py` scans; `pre553_recursive_handoff.py`, batch runner and SRC04 producer/reader. The present design does not erase any of these.

## 2. Accepted I02 validator — EVERY pass and its streaming proof obligation

The current top-level `validate_c11_source_release` at ingest lines **743–790** invokes these stages in order. S2 reimplements EXACT accepted predicates, not a weaker convenience validator. For diagnostic compatibility, accumulate bounded per-stage fail records in canonical stage order even if physical indexed passes are executed in different order; emit the legacy nearest applicable `IngestDisposition` and do not mutate repository on any failure.

| Ordered legacy stage | Current call / line | Necessary exact check | Selected bounded implementation | Fatal omission |
|---|---|---|---|---|
| V00 input candidate | 743–745 | correct C11SourceReleaseCandidate contract | private streaming candidate journal descriptor is new I02-owned input type with strict signature/schema, not duck-typed arbitrary source | casual list/generator bypass |
| V01 sections | _validate_sections 485–550 | mandatory NONEMPTY universe, respondent, question, event, routing, coordinate, authority; typed-absence policy for all optional sections; replay present | per-section counters, exact allowed absence-state enum; check section family/types during append; complete ledger before admission | treating missing section as typed absence; silently dropping needed coordinates |
| V02 source manifest | _validate_declared_manifest 451–482 | exact declared vs actual universe refs AND authority refs (ordered sorted, duplicates retained); declared family count consistency; seven core count keys present; no unknown declared count families | exact sorted section ref streams and counters, compare declared multiset (not set); maintain optional family handling precisely | falsely accepting same-count different-universe or missing declarations |
| V03 authorities | _validate_authorities 553–575 | validate each authority snapshot, build current AuthorityRegistry, validate each public object with `validate_public_carrier_object`, recursively walk every semantic-field and internal-record authority ref, positive exact REPLAY_PROTOCOL | authority snapshots bounded resident; transiently reconstruct each exact original object per spool record; run ORIGINAL public and internal checks; include deep nested authority walk; retain per-record pass receipt and failure ordering | hash-of-ref-only validation or unguarded canonical normalization |
| V04 namespace | _validate_universe_and_respondent_scope 578–620 | unique declared exact universe, respondent pair (universe, respondent_key), source scoped respondent ref, all event/route/coord/weight universe+respondent linkage, no cross-universe respondent | key-unique index over exact RespondentIdentity refs AND pair key; external B-tree/SQLite or bounded RAM under measured cap; join all fact grain records; foreign key/namespace proof | assuming row ordinal uniqueness or conflating respondent keys across universes |
| V05 question & event | _validate_questions_and_events 623–641 | question bindings by exact (universe,native_question); every event binds one; `ensure_distinct_event_occurrences` key = canonical_json(universe/ref, respondent/ref, native question/ref, component, event_group_id, response_event_id/index) | exact question-key index; external sort by canonical occurrence JSON or disk B-tree UNIQUE; preserve duplicate exact event refs until rejected; original component/rank fields included | dedup values, treating multiresponse as scalar or overlooking two distinct records with same occurrence key |
| V06 question authorities | _validate_question_authorities 644–661 | binding semantic/topology authority exact; positive NATIVE_CANONICAL_MAPPING_HARMONIZATION for canonical question; respondent identity-map authority exact | per-binding & respondent bounded pass using native registry; no promote canonical where absent | unauthorized source semantics |
| V07 source relations | _validate_source_relations 664–680 | exact DISTINCT_BY_DEFAULT typed absence OR each relation's exact universe refs subset of declared universe set | direct source relation pass with exact refs; disallow implied cross-source pooling or new same-person join | confusing distinct sources with automatically combinable sample |
| V08 replay | _validate_replay 683–721 | frontier/projection protocol IDs; byte-exact candidate projection hash; authority_snapshot_set_hash; exact SOURCE_ARTIFACT source substrate ref singleton; `closure_refs` EXACT tuple equals `_all_nonmanifest_refs` sorted WITH multiplicities; replay authority positive | comparator streams exact sorted global closure against supplied replay stream; separately compute full identical ReplayManifest semantic projection hash/ref; check metadata/authority and all duplicates. No replacement of closure list by single digest under @1.0.0 | fake replay/unstable identity |
| V09 coverage | make_m01_m18_coverage in integrity 510–553, called ingest 755–770 | M01–M18 exact labels, condition on NONEMPTY section and explicit typed absence, not arbitrary generic PASS | exact boolean/counter map plus optional-section explicit bits; call identical coverage semantics; persist map in deterministic versioned header | treating absent weight or discovery as nonexistent evidence without typed absence |
| V10 release root | ingest 772–776 | semantic_hash({candidate_projection_hash, replay_manifest_ref, m01_m18}) | build SMALL canonical root object using existing `semantic_hash`, no new hash formula | semantic hash drift |
| V11 full object realization | ingest 777–788 | old sorted public/internal tuples plus private-sealed C11LogicalRelease | for new path do NOT construct full tuples; retain complete validated journal with exact ref lookup and I02-only issue receipt. **This is a new I02 implementation contract, not old validator identity reused merely by calling _make_validated_release.** Legacy materialized path continues untouched | claim a private seal with no complete validation |
| V12 repository atomic admission | repository _commit_validated 89–111 and ingest ingest_c11_source_release 793–830 | reject collision, same release_id different semantic hash, exact object identity, all or nothing, return original IngestDisposition/accepted status | private commit of verified source-view header, exact release-ref inventory and object-ref mapping transaction; staged journal never visible until fully verified; preserve snapshot_identity sorted refs | exposed partial release, cache as authority, inconsistent source-view and legacy state |

**Pass order detail:** V02 has only declared count keys it actually checks plus seven core required. `make_m01_m18_coverage` uses flag/presence, not an assertion that the contents are materially empirically sound beyond other validators. Do not strengthen claims retrospectively. Typed absence allowed sets differ by section. _validate_sections currently REQUIRES at least one empirical coordinate; changing that is a separate I02 policy/version question, not an optimization.

## 3. Selected source-backed validation journal — private physical proof, NOT a new public family

In a source- and permission-qualified local work directory, create a **temporary journal** with:
- Immutable pending identity header: exact source artifact ref and SHA, source retention ref, decoder/code/config/projection authority roots, governed row/slot provenance, total logical family count declarations and physical schema/checksum version. This *binds* physical evidence but is not a scientific root by itself.
- Per-section append-only framed canonical record material. Each record retains section/family, exact `ExactRef`, canonical object projection (or exact reconstructible fields), universe/ref/respondent/ref, question/ref, occurrence material, authority refs, event topology, typed state, and a checked content hash. Frames are length-prefixed/checksummed; validation must reconstruct exact old object and recompute its semantic projection/content hash (not trust cache text).
- Bounded sorted **by section** exact-ref streams for candidate hash; **global** sorted closure stream from all nonmanifest sections plus BOTH source artifact and retention refs; no `set()` or de-dup. External merge sort can use old R5/Audit69 streaming/integrity engineering if exact semantics preserved. Explicit tie ordering where duplicated identical ref bytes are harmless, but duplicates must remain until appropriate validator accepts/rejects them.
- Indexed scoped `(universe,respondent_key)`, respondent ref, question `(universe,native_question_ref)`, global occurrence-key UNIQUE, and public object `ExactRef` resolution; use externally spooled/b-tree index when memory ceiling requires it.
- Compact per-section declaration/presence counts and typed-absence identity, replay proof, complete authority-resolution evidence, M01–M18 result. Physical hash/CRC and versioned source determinant binding are **nonsemantic cache** metadata.
- Minimal verified view header (S1) and exact native event/record reconstruction pointers. Read-only opening verifies staged artifact integrity AND independently accepted I02 proof; cache availability never grants current query/source authority.
- Do NOT persist all native public object pickle files plus a giant expanded JSON replay as a necessary newly compiled release. The journal may be compacted into a regenerate-on-demand Parquet/Zstd read view after sealing, but that cache is nonauthoritative.

Memory model: target **O(section/frame chunk + authority/universe metadata + configured indexes)** resident, with indexes spilled to B-tree when required; source decode/projection needs O(N) CPU to inspect and validate N source events even if resident object count is bounded. External sort complexity O(N log N) comparisons / O(N) scratch, subject to concrete implementation. No promise that compression alone fixes I03 evidence generation.

## 4. Two different exact sorts, both preserved

**Candidate projection:** `_candidate_projection_semantic_hash` ingest 280–351 sorts the **13 section property names lexically**, and sorts each section's exact refs by `ref.key`, then emits JSON via `canonical_json` (UTF-8, `sort_keys=True`, compact separators, non-ASCII unescaped). TypedAbsence is encoded as a **JSON mapping** including `detail:null`, not an empty array. Manifest root projection is included, manifest self-reference excluded.

**Replay closure:** `_all_nonmanifest_refs` ingest 354–377 concatenates source artifact + retention + ALL 13 present section reference sequences and sorts the **entire multiset** by `ref.key`. This is **not** a set, does not share per-section ordering, and both source refs are included even if their content hashes happen to match.

**ReplayManifest@1.0.0:** `C11InternalRecord.semantic_projection` integrity 144–152 includes `record_family`, `record_version`, and sorted `semantic_fields`; `closure_refs` is a full canonical list of exact-ref dictionaries. It can be hashed incrementally only if the exact serialized bytes are identical to `canonical_json(manifest.semantic_projection())`; no ref-only hash substitute. `ReplayManifest.ref` is determined by this hash, and C11 root depends on its ref.

**Authority set hash:** `authority_snapshot_set_hash` integrity 467–472 sorts authority-ref dictionaries by `canonical_json`, **not** by a guessed dictionary iteration order or necessarily `AuthorityRef.key`. Maintain exact comparator.

**Occurrence key:** `ensure_distinct_event_occurrences` integrity 487–508 hashes/compares the full canonical occurrence material; this is NOT the same as `RespondentEvent.ref.key`, raw answer value or row-question pair.

## 5. Small executable source-free oracles actually run this turn

These executed with `PYTHONPATH=/mnt/data/pyat_src04_unpacked/04_CURRENT_EXECUTION` and exactly SHA-matching core I02 modules. They do NOT use SAV/DTA or full original-source C11 nor prove the new streaming validator.

**O-S2-01, synthetic canonical byte identity**: 4 cases (normal vs reversed section order × unique vs duplicate internal refs) including Unicode and TypedAbsence. For each, `semantic_hash(_candidate_projection(candidate)) == _candidate_projection_semantic_hash(candidate) == independent streamed canonical JSON hash`; also the full `ReplayManifest.content_hash` == an incrementally produced hash of the **same** full semantic projection, not only the closure. All 4 PASS. The fixture deliberately lacks mandatory I02 sections; use only as hash oracle.

**O-S2-02, valid complete synthetic C11 acceptance**: Native original `validate_c11_source_release` accepted a 1-universe/1-respondent, 1-question, 2-multiselect-occurrence, explicit-routing, explicit-coordinate, 3-authority fixture; produced release hash `2418397e79c936502c17df873c14426cf2c083bd1d10d9febfef47338a8ee308` and replay hash `a1f37b4d1f74351619c842663314dfd1028c83d061113373ccdcd102d0419a43`; all M01–M18 nonempty; `C11Repository` exact release/object lookups work. Reversing the two event tuple positions kept BOTH exact hashes unchanged. Source-free, no original input.

**O-S2-03, negative native fixture**: Mandatory routing, coordinates, question, universe, replay, record-count mismatches all rejected. Deep cases with **updated manifest counts AND regenerated replay** also rejected: duplicate respondent namespace, duplicate event occurrence identity, unbound event target, cross-universe event and unknown event authority. Tampered replay closure rejected as `REJECTED_REPLAY_NONDETERMINISM`. These counterexamples target semantic validators, not merely count mismatch.

**O-S2-04, important newly demonstrated boundary**: Change `SourceReleaseManifest.source_snapshot_retention_ref.content_hash` to a DIFFERENT 64-hex hash from `source_artifact_content_hash`, regenerate otherwise valid replay closure, call `validate_c11_source_release`. **I02 ACCEPTED** the internally self-consistent fixture with release hash `2e429f3b7ca2ae62454b2fa56874ea80a7bc28b2cd53a5f47d20ce9aa4596f32`. This is not evidence that full source-backed projection accepts inconsistent source bytes: facade `GovernedC11Projection.__post_init__` at 297–298 and `_verify` at 576–584 guard source SHA/retention, and bridge imposes source SHA checks. It **does prove that I02 logical sealing alone is not a source-byte attestation**. New source-view registration MUST bind independently verified physical source and correct retention hash, not infer source correctness from I02 accepted status or cache content.

Oracle files local to this Browser turn: `/mnt/data/p01_s2_sourcefree_canonical_oracle.py` SHA-256 `070a596eee8e0e7f7b8836341e2151f433c631c5440b2b5e2af79a28ac933d53`, and `/mnt/data/p01_s2_full_fixture_oracle.py` SHA-256 `60de307c865c6b9c66f38c370a770d92513ab76a107b51fadf5e947216137b25`. These are sourcefree **local** scripts; the portable authoritative test suite must be implemented against pinned existing `rawlsing_next/tests/test_pre553_c11_repository_ingest.py` at control cut in S3/S4. DO NOT claim the local paths will exist in another ChatGPT session.

## 6. Independent original bytes gate, distinct from logical I02

For future streaming views, require the actual qualified source-admission owner to furnish an immutable approved source-evidence receipt including **actual source byte SHA verification**, decoder/physical provenance, row/slot completeness, source snapshot-retention congruence, exact governed projection and current source-read permit. Source snapshot access and cache replay have distinct authorities. A correctly internally hashed candidate produced from fake or stale source data is NOT sufficient. Source-authority revocation, missing original source, and historical artifact replay need exact policy distinctions; do not invent them. This gate is an explicit dependency of the new private I02 view factory.

## 7. Atomic commit and private constructor risk

Current `C11LogicalRelease` checks private `_C11_VALIDATION_SEAL` at repository 15–45, and `C11Repository._commit_validated` 89–111 stages all objects before mutating. **But** `_make_validated_release` is an importable helper, and the existing `pre553_parquet_carrier.py::reopen` calls it after its own relation verification, without rerunning all I02 ingest passes. Do not falsely describe the Python module-private seal as a cryptographic impossibility of alternative construction. Existing trusted historical persisted-carrier reopening has a separate trust path and must be audited.

New selected view registration must enforce: a private I02-issued typed validation receipt binding exact complete pass outcomes and source-admission receipt; off-line staged journal with verified physical digests; release_id/hash collision checks against BOTH view and old materialized releases; exact object-ref collision checks; all-or-none publish; no partial release in `release_refs` or `snapshot_identity`; never infer permission from repository presence. Cold existing accepted materialized releases retain their old validation/audit behavior. On crash/rebuild, fail closed, do not invent new release identity from partial journal.

## 8. Selected S3 coding sequence — one design, no alternatives

S3.0 Build new `rawlsing_next/tests/test_pre553_c11_streaming_parity.py` (or appropriate existing suite) using official accepted sourcefree fixture plus multi-universe, multiselect, rank/repeat, weighted/not-authorized, typed negatives and bad authority. Golden hashes/refs and exact old refusals from the old I02 engine, before editing source owners.

S3.1 Implement private canonical spool writer and deterministic per-section global multiset merge under I02 ownership; prove candidate and ReplayManifest hashes against the old implementation for every fixture, including Unicode, duplication, source retention and typed absence. Commit immutable journal records only after exact object hash identity check.

S3.2 Implement per-pass validators V01–V08 over the same journal/indexes, reusing original helper checks (and exception semantics) wherever possible, plus exact M01–M18 and root. No trust leap from physical hash to logical meaning.

S3.3 Implement a **trusted source-attestation and I02 admission transaction**, then new `C11VerifiedSourceView` + `C11ExecutionView` + exact repository registration. Protect against compromised staging, source-retention mismatch, changed authority and legacy view collisions. No public `register_untrusted_view`.

S3.4 Implement lazy exact object reconstruction and explicit legacy materialization under bounded/observable resource contract. Maintain existing old C11/Parquet/audit/equivalence code path and independent replay auditing.

S3.5 Adapt native I03/I05/index/workload consumers to the view only after S1/S2 APIs are fully proved. P03's shared computation is a separate dependent performance stage; no changed estimand, occurrence, denominator or native fact hashes in P01.

S3.6 Bind P02 nonauthoritative Parquet/Zstd accelerators and P05 consumer/resume. Record cold, warm, cache corrupt/delete, host RSS, scratch and per-phase timing; real original source only under exact grant and independent scientific acceptance.

## 9. S2 acceptance / what remains NOT proved

**S2 accepted only as HQ design and bounded source-free baseline-oracle result.** NOT a complete new streaming implementation. The full old-vs-new proof must show exact logical release/ref/replay/closure/M01–M18/objects and failure taxonomy, no source-file misbinding, no silent partial commit, and proper consumer outputs. S3/S4 need full code-level native regression and original qualified host measurement. The high-resolution ledger names every unresolved seam.

**This is the implementation design we are proceeding with.** We are not launching an A/B/C bakeoff or a new semantic court.
