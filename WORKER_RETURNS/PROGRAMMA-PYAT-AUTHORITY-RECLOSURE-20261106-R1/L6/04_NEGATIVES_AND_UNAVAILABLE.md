# L6 negative semantics, unavailable origins and issue-owner court

**Gate:** `UNBOUND_HISTORICAL_AUTHORITY`. These are S1 code observations and safe future negative test specifications, **not executed original-data evidence**. The authoritative stop and exact SEM-01–12 proof law is [#716](https://github.com/maidiu/rawlsing/issues/716) / PR #724 `05_ACCEPTANCE_AND_NEGATIVE_PROOF.md`.

## Distinct epistemic states — do not collapse

| Condition | Observed code behavior or required refusal | Why this is not yet lineage closure |
|---|---|---|
| Missing exact immutable authority ref | `AuthorityRegistry.resolve_exact` raises `Pre553AuthorityError: exact historical authority unavailable; no fallback permitted` after checking explicit registry/runtime context (`pre553_empirical_authority.py:234–249`). | Registry can be populated by external caller without an audited accepted original file. |
| Same authority ID/version different hash | `AuthorityRegistry.__init__` raises `Pre553AuthorityConflict` (`:215–229`). | Checks internal hashes, not issuer custody. |
| Denied or out-of-scope operation | `require_positive_authority` demands `ALLOW`, exact kind/operation/family/source/use (`:162–203`). | A generated test `ALLOW` snapshot can satisfy code shape absent original adjudication. |
| Query grammar/scope absent | `_require_exact_i03_authority_fitness` demands `query_authority_refs`, matching grammar, operation and conditional target-use permission (`pre553_empirical_query.py:296–440`). | Does not itself load V550 response contract or QSM rows. |
| Source SHA wrong | `decode_sav/decode_dta` verifies expected SHA before physical read (`pre553_physical_decoder.py:740–759`); Route B separately matches source/projection SHA (`pre553_route_b_production.py:517–541`). | Physical identity is not response/route/measurement meaning. |
| I02 missing semantic projection | `GovernedC11Projection` demands universe/respondent/question/response/coordinate/routing/snapshot inputs; explicit owner-set closure (`pre553_source_backed_c11_facade.py:298–356`). | Those inputs are caller-owned; source document loader not observed. |
| V550J cache signature mismatch | Historical `build_v550j_prepared_substrate.py:298–371` checks compendium, family, response, schema, compiler flags before load. | Its `_resolve_hash` and optional argument defaults require L3 hostile tests for absent-expected hash, stale accepted issuer and `prepared_or_forensic_fallback`; cache is never authority issuance. |
| Current C11 session cache key | `SourceBackedFacadeKey(source_sha, projection.cache_identity)` and `SourceBackedC11SessionCache.get` check current source/ref (`pre553_source_backed_c11_facade.py:359–379,616–686`). | Cache does not separately poll a live external revocation issuer; issuer must be rechecked at operation entry. |
| Current event accelerator cache | `RAWLSING_C11_ACCELERATOR_DIR` absent or not private/absolute disables cache; body hash / selector manifest rejects stale bytes, falls back to current sealed release (`_pre553_c11_execution_view.py:160–325`). | Sourcefree semantic parity is not old V550J manual authority portability. |
| Current persistent C11 Parquet | `ParquetC11Carrier.reopen` validates exact source/release/semantic selector and member/relation/root digests (`pre553_parquet_carrier.py:279–356`); DuckDB direct validates same member/root before views (`pre553_duckdb_direct.py:14–67`). | A seal preserves supplied semantic C11 objects; alone it cannot prove the original issuer's semantic grant is still current. |
| Original weighted estimand absent | `pre553_source_local_universe_admission.require_source_local_use` protects claim ceilings (`:538–556`), while `_pre553_query_eval.py:275–314` uses explicit weight facts. | Should **not** block otherwise correctly scoped, unweighted RAW. |
| Structural/FF authority absent | `evaluate_structural_empirical_admission` emits missing/unknown/negative states for null rule or missing snapshot (`pre553_structural_admission.py:578–632`), M1 requires ADMITTED exact relation (`m1_admitted_field_forge_relation_v554_ingress.py:281–355`). | No V552J manifest may substitute an original structure/actor issuer. |
| Currentness/revocation record absent | `pre553_issued_workload.admit` checks external `CurrentDecisionResolver` and requires `CURRENT_GRANTED`; `execute_native_workload` repeats admission mid-run (`:219–261,301–355`). | The externally trusted resolver implementation/data was not traced to the old asset estate in this lane. |
| Zero, missing, excluded, nonrespondent, routing UNKNOWN | Current `PhysicalMissingState` and `TypedAbsence` can preserve distinctions; routing membership uses issued facts in `_pre553_query_eval.py:51–115`. | Explicit old source/routing meaning must precede population count, not be reconstructed from value code `-4`. |

## Concrete unavailability manifest

| Missing evidence | Actual access / result | Competent future owner |
|---|---|---|
| Original frozen QSM CSV, calibration QRA CSV, both response contract CSVs and manifests, four overlay-family exact files per source/wave, joint registries and their current issuer receipts | Only code constants/paths and Git provider tree were read; **no content-byte SHA-256**, acceptance signature, current row or authority-status resolution was obtained. | L5 + authority issuer; L1/L3 check source resolution |
| Original respondent/source files (35 editions), R157 actual `SourceConfig` values and local hash manifest | Not mounted in local scratch; source files were **not** opened; 35-specific source SHA, decoder profile and response/route admission not witnessed. | L5 custodian + R157/I02 source owner |
| FIABC-A02 27 historical authority rows and nine blockers | The parent issue and PR #724 document historical A02 `BLOCKED`. This return **has not imported/dispositioned 27/27** and does not assert that archive material is current. | L5; L7 anti-omission |
| L1–L5 final returns and exact branch heads | Not available when this L6 reconstruction started; 30 curated lines are interim anchors. | L1–L5 then L7 |
| Runtime `AuthoritySnapshot` producer that constructs each accepted original FQRA/response/manual row with source-byte SHA and issuer selection | **No such complete original35 adapter proven** in scanned current modules. `RuntimeObjectCatalog.from_documents` accepts already supplied dictionaries (`pre553_carrier_execution.py:317–350`); `bind_runtime` receives already built `Pre553RuntimeAuthoritySet`. | Pyat authority ingress owner + L5 |
| Authoritative lineage mutation/severance/restore, Parquet cold read/cache parity, all35/18,467 operations | No active original source runner and no checked-out Rawlsing tree in local scratch; **NOT_RUN**. Existing test-source code was inspected, but test execution was not performed. | Authorized local S2 operator; independent L7 receives |

## Explicit original source tests: not run

| SEM | Status | Required proof at exact first consumer |
|---|---|---|
| 01 question identity | `NOT_RUN_SOURCE_UNAVAILABLE` | QSM row/alias withdrawn/wrong SHA must refuse/alter correct I02 event and I03 fact. |
| 02 response certification | `NOT_RUN_SOURCE_UNAVAILABLE` | 236-binding/145-scale present vs revoked/unsigned; no fabricated polarity/intensity. |
| 03 routing | `NOT_RUN_SOURCE_UNAVAILABLE` | Positive source risk-set vs UNKNOWN changes correct denominator or returns HOLD; no `-4` complement. |
| 04 joint topology | `NOT_RUN_SOURCE_UNAVAILABLE` | Joint release order/role change must alter/refuse I05, not generic two-target fallback. |
| 05 typed relation | `NOT_RUN_SOURCE_UNAVAILABLE` | REJECT/BLOCKED/no-positive must not turn into absent. |
| 06 source trust | `NOT_RUN_SOURCE_UNAVAILABLE` | Edition/SHA/host rights revoke mid-read -> no durable positive. |
| 07 cache | `NOT_RUN_SOURCE_UNAVAILABLE` | Change authority SHA with same source bytes -> new key/typed refusal/rebuild only if granted. |
| 08 lifecycle | `NOT_RUN_SOURCE_UNAVAILABLE` | Superseded/withdrawn/current and historical as-of replay must be different when issued. |
| 09 first consumer | `NOT_RUN_SOURCE_UNAVAILABLE` | Remove only original authority while leaving caller test snapshot -> no same-positive I03/Batch. |
| 10 no overblock | `NOT_RUN_SOURCE_UNAVAILABLE` | Correct RAW query still runs when unrelated weight/FF actor grants absent. |
| 11 all35 | `NOT_RUN_SOURCE_UNAVAILABLE` | Each of 35 source manifests and 18,467 prospective operations gets exact disposition, no drop. |
| 12 cache/source | `NOT_RUN_SOURCE_UNAVAILABLE` | Cold original source + issued authority vs warm cached projection yields same typed result/digest. |

**Test code read, not run:** `test_pre553_route_b_production.py` uses `_fixture` and a locally populated `RuntimeObjectCatalog` (e.g., lines 73 and 501); `test_pre553_c11_execution_view.py` imports that fixture and tests warmed cache poisoning; `test_universal_source_byte_custody.py` generates SAV/DTA test files and imports a facade fixture. `test_fiabc_lits_r4a_adopted_authority_snapshot_closure.py` reads a file whose own status is `CANDIDATE__HQ_ADOPTION_REQUIRED`. These are valuable scoped engineering negatives, never native historical QSM/response-asset proof.

**Non-overblock warning:** 5,630 historically marked candidate RAW is not 5,630 approved executions. The received planning denominators (18,276 items / 18,413 slots / 18,250 joins / 18,467 prospective operations) are planning evidence to verify per operation. Absence of optional weight/structural/actor authority does not automatically cancel a separately proven unweighted RAW request.
