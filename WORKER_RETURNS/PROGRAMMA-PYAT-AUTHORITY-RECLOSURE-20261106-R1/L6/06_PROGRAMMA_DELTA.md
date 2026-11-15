# L6 — PROGRAMMA delta and hybrid authority-binding architecture proposal

**Commission:** #722, L6 of #716. **Scope:** S0–S1 code/native-provenance reconnaissance at frozen base `9ba4764bef551b1ce498e5772d60b73d69337d4b`; protected PRE-MAIN rechecked at launch `fce43498e16e4709f3c9801e8717f0fdae18126a`. **State:** proposal/worker finding, not an adopted PROGRAMMA change, source custody, original scientific issuance, code implementation, or acceptance. Parent #716 remains STOP.

## 1. Current architecture: actual consumers before a proposed interface

The current authority seam is not a universal on-disk historical-source loader.

| Current seam | Actual contracted input and consumer | Boundary and caveat |
|---|---|---|
| `pre553_empirical_authority.py` | `AuthorityRegistry` and scope-checked `AuthoritySnapshot`, including bound runtime registry fallback | Checks **supplied** snapshot validity/scope; does not establish historic issuer permission or original bytes on its own |
| `pre553_carrier_execution.py` | `RuntimeObjectCatalog.from_documents(authority_documents=...)`; I03/I05 consume the catalog | Caller-supplied documents, not implicit FQRA/scale-binding import |
| `pre553_runtime_authority.py` + `pre553_runtime_context.py` | Caller-supplied adopted authority snapshots and exact hash set; runtime context binding | Exact adopted-history lookup, no arbitrary latest/global grant |
| `pre553_empirical_query.py` | Typed operation, source-family and target-use fit; query executor | Query fitness is not original-source permission or estimand certification |
| `pre553_source_backed_c11_facade.py` | `GovernedC11Projection` and slot-owner-family closure, cached source/projection session | Current sealed materialization, not native source-grant issuance |
| `pre553_route_b_production.py` | Owned source/projection/catalog, exact SHA checks; Route B invokes C11/I03/I05 and emits receipt | Installed Route B validated contracts must remain intact |
| `pre553_parquet_carrier.py`, `pre553_duckdb_direct.py`, `_pre553_c11_execution_view.py` | Content-checked Parquet/DuckDB and optional `RAWLSING_C11_ACCELERATOR_DIR` regenerable event-body acceleration | Physical-view cache provenance must not be promoted to source authority |
| `pre553_physical_decoder.py`, `pre553_structural_admission.py` | Physical SAV/DTA digest verification; separate exact structural admission | Byte readability and field admission still are not scientific approval |
| `pre553_source_native_preimage_adapter.py`, `pre553_native_workload_binding.py` | Test-only `R56-TEST-ONLY-AUTH-*` and `R03-TEST-ONLY-FRONTIER-QUERY-AUTH` self-minting | Sourcefree test evidence; no original authority recovery |
| `pre553_issued_workload.py` | Exogenous `CurrentDecisionResolver`; demand for `CURRENT_GRANTED` and mid-execution recheck | Issuer must be established by authorized holder, not inferred from this consumer |
| `pre553_universal_workload.py`, `pre553_source_local_universe_admission.py` | Caller frontier/policy or source-local RAW claims | Neither is universal population/weight/FieldForge grant |

Exact code anchors, byte SHAs and reviewed candidate line inventory are in the sibling L6 reports. No current active reader was found that automatically promotes legacy `QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv` or 145-key/236-row response semantics into these PRE553 contracts.

## 2. Keep the two trust ledgers separate

**Ledger A — observed source and physical execution:** original file identity, verified bytes/digest, decode policy, discovered schema/field provenance, exact query shape, runtime response receipts, and digest-checked materializations. Its strongest intrinsic claim is observed physical/semantic behavior under a stated reader. It is not permission to use a study for an estimand.

**Ledger B — external permission and science:** source owner or authority issuer, rights scope and decision history, use-specific restrictions, original response-scale and relation issuer, target population/weight/estimand qualification, and exact `CURRENT_GRANTED` or typed unresolved/denied decision. An authorized issuer must fill this ledger. L6 is forbidden to invent it.

Required join is **explicit and exact**: A source-byte and source-view identity may *reference* a B authority record if the original issuer, source version, use, scope and adoption are independently confirmed. Neither ledger auto-upgrades the other. A cache hit in A cannot mint a permission in B; an eligible record in B cannot manufacture absent source bytes in A.

## 3. Hybrid physical architecture decision recourt

The October 28 selected compact, sealed and regenerable hybrid remains the recommendation **at documentary architecture level**, subject to #716 stop and exact source/issuer verification. It combines:

1. **Canonical source- and authority-bound input** for an exact first consumer, with no wildcard or fuzzy vintage fallback.
2. **Economical sealed C11/Route B materialization** with exact source, event, schema, compiler/decoder, provenance and authority-binding signatures.
3. **Rebuildable disposable read acceleration** (e.g. the existing Parquet/DuckDB/private C11 event-body machinery), invalidated if any sealed signature differs.
4. **Separate original science/right-holder decisions** before eligibility-sensitive production requests; absent decisions remain typed HOLD/UNKNOWN/NOT_RUN.

| Choice | Benefit | Cost / risk | L6 treatment |
|---|---|---|---|
| A: materialize every possible original authority/response pair ahead of time | Potential fast reads | Large Cartesian storage, stale or falsely joined vintage, grant promotion | **Do not adopt** as global policy |
| B: reopen original CSVs, SAV/DTA and rights records for every operation | Closest to live originals | Repeated IO, poor reproducibility if original changes, operational expense | Useful as controlled forensic/negative baseline when bytes and rights available |
| C: canonical exact binding + compact sealed view + regenerable acceleration | Economical, content-verifiable, replayable | Needs precise key, invalidation and external authority issuer | **Selected architecture to retain/reclose**, not asserted production-ready |

This is not a retrofit of the legacy V550J compiler as an unconditional PRE553 oracle. The legacy manifest can be a *seed* for a separately reviewed adapter but its `prepared_or_forensic_fallback` and default-empty semantics paths cannot be treated as certified proof.

## 4. Proposed adapter contract, not implementation

The architectural owner may specify one **versioned, read-only authority-binding adapter** that resolves independently supplied historical evidence into current object contracts. Name `AuthorityBindingCapsule` below is a *design shorthand*, not an existing committed type or a mandate to create a second authority framework.

Input, all mandatory or explicitly typed absent:

- `original_source_id`, canonical source path, immutable source-byte SHA-256 and custody/rights holder.
- `source_reader_id`, decoder/version, schema/column profile, physical error evidence and source-local permissions.
- `authority_issuer_id`, original authority artifact path, artifact SHA-256, grant or denial ID, decision version, authority scope and adopted/revoked lifecycle. **No inferred original issuer.**
- Exact question relation and response semantic version/binding IDs if a query demands them; for historic FQRA / scale authority specifically, require original evidence and byte checks, do not migrate guessed columns.
- Requested operation, slot/field, source-family, target-use, population, weighting and estimand; typed independent eligibility from authorized reviewers.
- Exact compiler/normalizer/reader policy and request payload identity.

Output may include:

- A read-only `AuthoritySnapshot`/registry view and `RuntimeObjectCatalog` documents *only if compatible with current contracts and explicitly granted*.
- An exact `GovernedC11Projection` / Route B input binding after source and slot-owner-family checks; original scientific approval remains external.
- A typed `HOLD_MISSING_SOURCE`, `HOLD_MISSING_ISSUER`, `HOLD_SCOPE_MISMATCH`, `HOLD_UNQUALIFIED_ESTIMAND`, `DENIED`, `REVOKED`, `SCHEMA_CONFLICT` or `NOT_RUN` answer with cited evidence, not `ALLOW` by default.

The existing `CurrentDecisionResolver`/issued-workload checking boundary remains the production decision authority. The proposed adapter is a **binding surface** that may supply verified references; it must not self-issue `CURRENT_GRANTED`, bypass the mid-execution recheck, or recast TEST-ONLY unrestricted snapshots.

## 5. Cache sealing, invalidation, and replay

A permissible cache identifier should canonically hash the tuple:

`(original_source_byte_sha256, source_reader_and_decoder_version, exact_schema_and_field_provenance, original_authority_artifact_sha256, issuer_and_adoption_decision_version, grant_scope, relation_and_response_semantics_version, requested_operation_and_target_use, population_weight_estimand_selection, compiler_normalization_version, selected_physical_profile)`.

The exact bytes of each component and serialization specification require implementation-owner review. Null/unknown fields cannot quietly coalesce with granted ones. An authority change, revocation, source-file mutation, changed decoder, row/weight filter, question/scale version or request-use mismatch must miss/evict the grant-sensitive view. Existing runtime `sha256` and manifest guards remain required.

Replay records must separately preserve (a) source byte and lineage receipts, (b) authority issuer and lifecycle observation, (c) requested use and science eligibility, (d) exact materialized output digest, and (e) failure/negative state. Acceptance of a replay receipt proves replay of recorded semantics, not current legal/scientific authority after revocation. Private C11 event-body acceleration is disposable; the sealed canonical source/receipts remain necessary to regenerate it.

Avoid universal eager source×question Cartesian expansion. The 145-key/236-row historic manifests and 27-row FIABC-A02 authority ledger are distinct populations; no join cardinality is certified by this commission. Perform only request-scoped, issuer-reconciled relation/response bindings and account for conflicting/absent records explicitly.

## 6. Compatibility and refusal proof

Required before activation, to be run by a separately authorized implementation/review team with original bytes and runner rights:

- Replay current sourcefree I03/I05/C11/Route B and native-workload golden paths unchanged; confirm snapshot-history/canonical manifest and mid-execution decision checks still reject invalid/revoked decisions.
- Corpus-driven signature tests: alter one source byte, source version, authority artifact byte, scale binding, relation, use/scope, weighting, decoder and compiler independently; each must invalidate a corresponding exact view.
- Mismatched issuer, response semantics, restricted source, missing source SHA, absent current grant, conflicting physical schema, revoke-after-preflight, and stale cache must produce distinct typed refusal without partial execution.
- For each externally approved first consumer, compare canonical original-byte re-read and sealed-regenerable view results under the same exact binding; reconcile row counts, field/response values, null behavior, operations, weights and provenance.
- Negative control: no TEST-ONLY sourcefree snapshot or physical-cache existence may be accepted as historical source grant.

These tests are a **future court plan** only. They were not run; original source bytes, original issuers, comprehensive native execution, and permitted local S2 runner are unavailable in this L6 session.

## 7. Proposed PROGRAMMA package deltas for HQ adjudication

L6 **does not edit** the centralized PROGRAMMA package, PR #724, other workers' returns, or protected PRE-MAIN.

| Proposed delta | Receiving owner / independent gate | State |
|---|---|---|
| Record modern PRE553 first consumer matrix and legacy V550J seeds with exact source line/blob references | PROGRAMMA HQ after L1–L6 returns | Proposed; L6 S1 evidence only |
| Split source byte/digest, rights/issuer, question relation, response scale, weighting/estimand and dynamic runtime histories as separate negative-aware gates | L1/L2/L3/L4/L5 domain owners then HQ | Held, no inferred grant |
| Make explicit exact-source/authority adapter vs current `AuthorityRegistry`, `RuntimeObjectCatalog`, C11, Route B, issued-workload resolver contract | Code owner + science/rights issuers; L7 hostile acceptance | Design proposal; no production edit |
| Preserve selected hybrid architecture and existing Route B validated contracts without claiming source-native closure | Current physical owner and HQ | Conditional carry-forward |
| Reconcile R157 source configuration and FIABC-A02 27-row/nine-blocker authority status with exact current branch and source keeper | Designated ledger/source holder, independent reviewer | Unknown; L6 did not see originals |
| Prove all35 and 18,467 source-native operations under authentic first-consumer/authority, not sourcefree proxies | Authorized runner and independent L7 | NOT_RUN |
| Accept/merge/stop | HQ, protected merger, independent L7 reviewer | **STOP remains** |

## 8. Formal L6 recommendation

**RETURN WITH EXPLICIT HOLDS; NO ACTIVATION.** The live code contains useful and largely exact scope, SHA, catalog, context, replay and sealed-physical boundaries, but the externally governed original-source and original-relation/scale/estimand link is not closed by the present S1 investigation. Recommend retaining October 28's hybrid physical decision as a conditional design, commissioning an exact adapter after L1–L5 issuers and source-custody evidence, and asking L7 to test every negative path. Nothing here changes #716 from DISPATCH-READY/STOP into science issuance, permissions, production readiness or protected acceptance.
