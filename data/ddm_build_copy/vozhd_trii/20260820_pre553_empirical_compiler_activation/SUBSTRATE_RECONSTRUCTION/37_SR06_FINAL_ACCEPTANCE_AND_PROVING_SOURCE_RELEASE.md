# SR06 — FINAL ACCEPTANCE AND PROVING-SOURCE RELEASE

Status: `G-SR06_ACCEPTED__SR07_SR08_P0_RELEASED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Accepted implementation lineage:

- initial SR06 return: `c5e2c5c820c9b3917a4814bd7031074090763cb6`
- relational correction: `250f43bfdf1432d60ea5c53b95a22a67a0160ae3`
- R2 execution/identity correction: `fc74879bdc3a1d987e3f19022116ac551da582e6`
- semantic-root closure: `606813b01021eb2555017e028d5742b1e6f12e94`
- integration merge into control: `def253c7f62b74d07c7297e6ca279642b7d13904`

## 1. G-SR06 acceptance

HQ accepts SR06.

The implementation now satisfies the frozen physical substrate requirements without reopening I01-I07, M01-M18, I03/I05/I04 semantics, or V553-V558.

Accepted properties include:

- exact-SHA-bound SAV/DTA decoder configuration;
- physical/system/user-missing distinctions, including DTA extended-missing support at the decoder contract;
- metadata-first chunked reads for ordinary sources;
- exact allowlisted compatibility full-read exceptions only;
- deterministic physical row/variable identity across batches;
- explicit non-semantic physical-incidence -> existing I02 validation bridge;
- exact source SHA and AuthorityRef binding at that bridge;
- canonical relational Parquet persistence;
- directly queryable respondent/event/routing/coordinate/weight/authority relations;
- immutable/content-addressed release layout;
- staging-before-publication and member SHA verification;
- relation logical digests;
- exact selector/path closure;
- shared persisted semantic-root verifier using the existing I02 release-hash formula;
- persisted ReplayManifest identity verification;
- full-reopen replay-closure enforcement over reconstructible persisted refs;
- lightweight in-memory DuckDB direct sessions that do not require full logical reopen;
- no authoritative persistent `.duckdb`, PostgreSQL, SQLite, or `DATABASE_URL` path.

The documented pyreadstat writer/readback inability to expose writer-created Stata extended-missing metadata is accepted as a dependency-fixture limitation, not as proof that extended missing cannot occur. Real source absence remains source-specific evidence only.

Reported final test state:

- SR06 tests: `15 passed, 1 documented skip`;
- PRE553 suite: `614 passed, 2 unchanged baseline failures, 1 documented skip`.

The two pre-existing source-relations expectation failures remain outside the SR06 patch lineage and are not adjudicated here.

## 2. Real-source scale risk is now the next burden

SR06 acceptance certifies the implementation contract synthetically. It does not certify WVS7, LiTS I, or any other source.

Existing `C11SourceReleaseCandidate` / `C11LogicalRelease` APIs retain tuple inventories. Full proving-source C11 construction may therefore be memory-expensive even though the physical decoder and analytical carrier are now bounded.

This is not silently accepted.

Before a full WVS7 or LiTS-I C11 build is authorized, each proving-source court must execute a bounded P0 scale preflight over the exact real source bytes and return deterministic resource/identity evidence.

## 3. G-SR07 / G-SR08 release state

`G-SR07 = AUTHORIZED__P0_SCALE_PREFLIGHT_ONLY`

`G-SR08 = AUTHORIZED__P0_SCALE_PREFLIGHT_ONLY`

P0 is not source certification.

P0 may not:

- claim `CERTIFIED`;
- build/persist a complete proving-source C11 release;
- perform full I03/I05 discovery/query certification;
- modify source semantics or authority law;
- modify SR06 implementation;
- use legacy PostgreSQL as truth.

P0 exists to prove that the exact source bytes can enter the accepted SR06 machinery with deterministic physical identity and bounded resource behavior, and to quantify the likely full-I02 materialization burden before HQ authorizes it.

## 4. Next authority

The exact P0 execution law is frozen in:

`38_SR07_SR08_REAL_SOURCE_SCALE_PREFLIGHT_AUTHORITY.md`

HQ must adjudicate both P0 returns before authorizing full G-SR07/G-SR08 source certification.
