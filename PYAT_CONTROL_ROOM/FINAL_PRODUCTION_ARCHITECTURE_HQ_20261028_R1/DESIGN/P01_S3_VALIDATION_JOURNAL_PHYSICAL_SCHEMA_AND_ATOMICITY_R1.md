# P01-S3 — Exact physical journal, canonical serialization, proof and repository transaction specification

**This is a private ENGINEERING format, not a new C11 semantic carrier/ontology.** I02 original canonical identities always win.
**Base:** current-control code SHA 299f41e97a43c67be9cc76a79fa49b48f4e12e54. See `P01_S3_CODE_OWNER_AND_INTERFACE_SPEC_R1.md`.
**Disposition:** chosen format and API as a build specification; correctness/efficiency require executable proof, not established by this memo.

## A. Journal invariants

J1. Journal construction requires an explicitly scoped, governed projection and verified **source-admission receipt**. Neither a supplied source hash nor a journal checksum alone proves the original source bytes. For source-free tests, mark test-only admission not eligible for original-use promotion.

J2. Each generated native public/internal object is reconstructed at validation boundaries with original constructors, recomputed `semantic_projection`, `content_hash`, `ExactRef`, family and source identity; no physical cache field silently becomes canonical semantic identity. Strict exact source, value, missing, topology and occurrence paths.

J3. Every candidate section's exact-ref **multiset** is retained, including repeats until the original validator rejects any forbidden duplicates. Candidate hash order is sorted section **property names** and per-section `ExactRef.key`; ReplayManifest closure uses a **global** sorted exact-ref multiset including source artifact and snapshot retention. Retained source+retention refs can share content hash yet differ in kind/id.

J4. Source release root is the same `semantic_hash` of existing candidate projection/replay-ref/M01–M18 projection. Physical storage hash and I02 proof hash are never inserted into it.

J5. No low-level frame or manifest can assert semantic validity or source use. **I02 private validator** issues an in-process proof only after all passes complete. Cold reopening a stored proof requires independent verification of its custody/attestation or full replay of original checks; unverified saved receipts are never accepted by declaration.

J6. Exact lookup: (kind,id,content_hash) and returned typed object must match complete requested ExactRef; no fuzzy, closest, latest, or release-reference fallback. Same-ref duplicates and same-ID conflicting hashes must be handled according to current I02/repository checks, not silently coalesced.

J7. Event row ordinal and native occurrence rank must not be conflated. A field can generate 0/1/many events. Routing and coords have independent roles. Physical row/slot duplicate and missing declared row/slot are distinct fatal states; source-spare columns can be legitimately outside selected projection only under existing author authority.

J8. Source-free journal does not upload raw respondents or answer values into Git. Staging and persisted cache remain within approved local secure storage; code and synthetic tests are the only repo artifacts.

## B. Concrete staged directory, with schema contract and persistence law

The selected *implementation-local* staging layout (provisional naming, pinned semantics):

```text
<private-root>/.stage/<run-id>/
    PREPARE.json
    sections/<exact-13-section-name>.frames       # one logical section each
    sections/<name>.refs.sorted                    # externally sorted exact refs, dupes kept
    indexes/respondent-key.sqlite                  # exact (universe, key) and ref lookup
    indexes/question-key.sqlite                    # exact (universe, native question) key
    indexes/occurrence-key.sqlite                  # UNIQUE canonical occurrence key
    indexes/ref-owner.sqlite                       # kind,id,hash -> record locator(s)
    proofs/source-binding.json                     # qualified source-admission receipt locator
    proofs/i02-pass-report.json                    # private pass states, *not* trusted alone
    proofs/replay-closure.refs.sorted              # global multisort w source + retention
    proofs/canonical-hashes.json                   # exact old candidate/replay/C11 root hashes
    PREPARED_MANIFEST.json                         # physical digest of every stage member
<private-root>/verified/<source_sha>/<release_id>/<semantic_release_hash>/
    [same validated immutable payload, atomically published]
```

Only use safe hex SHA selectors; release_id cannot traverse directories or contain separators. An exact release ID with a disallowed physical path is safely encoded for the filesystem, without silently rewriting the *logical* release_id. Make all filenames deterministic independent of host locale/time; run-id is temporary and excluded from logical identity. Hash every member, validate sizes and layout before opening; no symlinks/path escape, no partial restore.

**Physical frame format:** fixed version tag, 64-bit little-endian payload length (bounded), payload digest and source record ordinal followed by UTF-8 canonical encoded payload. Payload includes section name, object family/version, exact ref, canonical semantic field values or reversible explicitly typed fields, physical row/slot/occurrence provenance and source/authority determinant keys. Use a tagged type-preserving codec: `ExactRef`, `AuthorityRef`, `TypedAbsence`, exact int/Decimal/Fraction, tuple/list/maps and `None` distinguished; reject binary floats, nonfinite values and unsupported types. Frame/digest is **physical-only**; on reconstruction call original class constructors and check `obj.ref == stored_ref`.

**Crucial nonloss:** `canonicalize` is appropriate to compute semantic hashes, but its generic JSON form is not always a bijective serializer for original Python field/collection types. Choose an explicitly reversible physical schema and round-trip against every field/type, especially C11 internal record dataclass tuples, native public semantic objects, typed absence and exact numeric values. Do not assume `canonical_json(obj.semantic_projection())` alone is sufficient to reconstruct native `obj`. Test every family and optional section.

**SQLite indexes:** indexes are nonsemantic implementation, require same transaction as section files, index exact UTF-8 canonical keys with byte-wise deterministic collation (not SQLite locale). Exact membership and duplicate constraints must be checked against original I02 equivalence. External sort chunk size and SQLite cache size are configured with memory/disk budgets. No unbounded `to_pylist()` conversion of all rows. Negative hash/collision/integrity cases fail closed.

## C. Two streaming hashes — deterministic exact bytes

**Candidate projection**: Equivalent to `semantic_hash(_candidate_projection(candidate))`, implemented following the already accepted `_candidate_projection_semantic_hash` writer and exact `canonical_json` behavior. Emit `{` + lexicographically sorted keys + `:` canonical values + exact sorted ref lists + `}`; preserve typed-absence mapping with `detail`. Existing `canonical_json` uses `json.dumps(canonicalize(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)`. Retain source manifest's original projection. Do not add journal detritus or cached fields.

**Replay closure**: external merge exact `_all_nonmanifest_refs` sorted by `ref.key`. Do not cast to set, do not filter duplicate source+record refs, and do not insert the ReplayManifest self-ref. Compare against supplied candidate replay closure *in exact tuple order and with multiplicity*. This comparison can stream two ordered ref sequences. The original `ReplayManifest@1.0.0` record's `semantic_projection` must be byte-exact, including `semantic_fields.closure_refs` as full JSON array. Streaming hash must emit the exact same bytes as `canonical_json(manifest.semantic_projection())`; validate the `ReplayManifest.ref` against native old oracle.

**Release root**: call original `semantic_hash({candidate_projection_hash, replay_manifest_ref, m01_m18})` with existing exact canonical order; no new format marker, version or closure compression inside identity.

**Authority set**: use original `authority_snapshot_set_hash` comparator (sort authority ref dicts by `canonical_json`). Do not assume event order or Python hash seed order is stable.

## D. Every legacy validator pass has a proof projection

| Pass | From journal | Old checks and required exact error |
|---|---|---|
| Sections | presence and typed absence by named section; replay presence | `_validate_sections` with per-family mandatory nonempty and exact allowed typed states |
| Manifest | actual universe/auth ref sorted **tuple** and family counts | `_validate_declared_manifest`; declared required 7 families; forbid unknown declared families |
| Authorities | native objects reconstructed per frame + nested authority walks | `_validate_authorities`; original `validate_public_carrier_object`, exact registry, positive replay |
| Universes/respondents | universe exact ref index; respondent `(universe,respondent_key)` uniqueness; grain fact foreign key | `_validate_universe_and_respondent_scope` |
| Questions/occurrences | exact question pair; event occurrence canonical key unique independently of value and ref hash | `_validate_questions_and_events`; original topology |
| Question authority | native binding and respondent identity mapping | `_validate_question_authorities` |
| Relations | DISTINCT_BY_DEFAULT or exact declared-universe subset | `_validate_source_relations` |
| Replay | canonical candidate hash, full multiset closure, authority set, protocol and source substrate refs | `_validate_replay` |
| Coverage | exact counters/typed-absence presence, replay present | `make_m01_m18_coverage` original M01–M18 values |
| Root/seal | exact old source manifest / replay / semantic root, complete I02 report | *Only* I02 private admitted-view factory; never `_make_validated_release` with invented seal |
| Repository | old and new view identity/object collision checks | atomic `_commit_i02_verified_view` across all visible lookups |

**Failure precedence:** Old `validate_c11_source_release` invokes stages in this order: sections -> declared manifest -> authorities -> namespace -> questions/events -> question authorities -> relations -> replay -> coverage -> sealed release. The journal engine can collect data earlier for economy, but its authoritative rejection must match that ordered decision when two defects coexist. Preserve `_classify_integrity_error` mapping or explicitly classify to existing `IngestDisposition` with exact negative tests.

## E. Cross-path repository transaction: no ghost releases

Existing `C11Repository` keeps `_by_ref`, `_by_release_id`, `_objects`. New private indexes must be staged with compatible behaviors. Exact admission algorithm:

1. Build validated journal in inaccessible staging, with complete I02 proof, qualified source receipt and expected exact `release_ref`.
2. Reject prior `release_id` whose semantic release hash conflicts, whether prior is materialized or view. If same `release_ref`, apply existing idempotent behavior ONLY if journal/source/authority binding is compatible; otherwise fail closed rather than silently selecting unrelated source.
3. Iterate exact public/internal/replay ref inventory and check intersection with existing old and view object-ref index. **Full object hash and proper source ownership** are necessary; a simple matching string key is insufficient proof of equal content if namespace collision or hostile corruption is possible. Compare complete reconstructed object as required by old repository semantics.
4. Stage all inserts and proof pointers without mutating `_by_ref`, `_by_view_ref`, `_by_release_id`, `_object_owners`, or `_objects`. Commit durable journal first with crash-safe fsync/atomic rename, then publish in-process index under one lock, or use explicit write-ahead committed manifest and deterministic crash recovery. Choose one exact invariant-preserving transaction implementation before code; no partial visible commit.
5. `release_refs` enumerates union of materialized+verified view refs with old sort by `ref.key`; `snapshot_identity()` emits exact identical canonical JSON for the same ref set. `resolve_object_exact` returns typed genuine object from old dict or verified exact lookup. No release ref object invented as a public object.
6. If any integrity/collision/IO/cache/authority fault occurs before complete commit, previous snapshot/refs remain unchanged; cleanup staging safely. Cold process refuses uncommitted or incomplete journal directories.
7. Current scientific permission checks remain separate from repository existence and exact lookup.

**Do not make the old `C11Repository._commit_validated` eagerly inflate a view's object index**; if it does, the claimed optimization fails. Write an explicit dual-index transaction, test both insertion directions and rollback.

## F. Cache/backend boundary and named performance traps

The initial journal's accepted exact typed native record store is a **validated source-backed execution substrate**, not an independently authorized canonical science source. P02 may build a regenerable Parquet/Zstd accelerator from it with a separate code/schema version and source/authority determinant key. The existing ParquetC11Carrier is an eager trusted materialized *output* adapter, not the new hot cache. Do not replace a 7.9GB pickle with an equally bloated in-memory `to_pylist()`, nested object dict or full JSON receipt. Count all journal/SQLite/Parquet/scratch/replay bytes and peak RSS, not only compressed cells.

**Permitted path to achieve O(bounded residency):** validate each exact reconstructed object and release promptly, retaining indexed fields/ref material only in bounded chunks; spill respondent and occurrence keys to on-disk B-tree and merge refs externally. Full N records still pass through semantic validation once per source/projection version. Audit/materialization can remain high-cost and explicit. Hot I03 must not rebuild all native objects just to count a small target.

## G. Executable differential oracle the builder must implement

On a single synthetic candidate, run old validator and new journal validator; compare:
- `C11LogicalRelease.release_ref`, source manifest hash, replay manifest ref and full reconstructed replay closure, M01–M18, ordered ref tuples and exact resolved objects.
- All old pass classes including duplicate manifest declarations, wrong count, missing mandatory coordinates/routing, bad internal/public authority, different-uni but same respondent key, cross-universe event, 0/1/many events per physical cell, duplicate occurrence with different response values, special missing, held source input and false positive canonical mapping.
- Cold reopen without process memory, no cache, corrupted frame, swapped source hash, mismatched decoder/authority, absent original source or permission, partial commit, forged stored proof, ref collision, mixed old+new releases, same release_id different release hash.
- I03 negative, unary, J2, conditional, J3 and recursive branch tests with EXACT native fact/replay/provenance. Source-free first; authorized original execution distinct.

**Schema is NOT accepted from prose alone.** Only sourcefree dual-implementation executed tests and hostile review can qualify journal and private view; original-source qualification is a later separate grant and reviewer.
