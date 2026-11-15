# SR06 — CORRECTION RETURN ADJUDICATION AND R2 EXECUTION/IDENTITY GATE

Status: `CORRECTION_RETURNED__NOT_ACCEPTED__R2_BOUNDED_CORRECTION_REQUIRED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

SR06 implementation branch: `agent/vozhd-trii-sr06-c11-parquet-duckdb`

Prior returned implementation: `c5e2c5c820c9b3917a4814bd7031074090763cb6`

Corrected returned implementation: `250f43bfdf1432d60ea5c53b95a22a67a0160ae3`

Prior correction authority: `34_SR06_IMPLEMENTATION_RETURN_ADJUDICATION_AND_CORRECTION_GATE.md`

## 1. Correction return accepted as progress, not as G-SR06 closure

HQ accepts the correction as a real bounded implementation return.

The correction is exactly one commit ahead of the prior SR06 return and changes only:

- `rawlsing_next/pre553_physical_decoder.py`
- `rawlsing_next/pre553_parquet_carrier.py`
- `rawlsing_next/pre553_duckdb_direct.py`
- `rawlsing_next/pre553_physical_c11_bridge.py`
- `rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py`

The worker reports:

- SR06 correction tests: `8 passed`;
- full PRE553 suite: `607 passed, 2 unchanged baseline failures`;
- no WVS7, LiTS-I or CLOSED_35 execution;
- no persistent DuckDB/PostgreSQL/SQLite/DATABASE_URL path;
- required correction-return token present.

The correction materially closes important portions of authority 34:

- opaque full-release/object blob duplication is removed;
- canonical Parquet is split into queryable relations;
- respondent-event fields are directly queryable;
- reopen reconstructs the logical release from canonical relations;
- member byte hashes and relation logical digests are manifest-bound;
- a cross-relation semantic mutation is rejected by reconstructed object identity;
- physical incidence no longer retains a complete tuple of `PhysicalCell` objects;
- an explicit physical-to-I02 bridge exists and calls existing `validate_c11_source_release()`.

G-SR06 nevertheless remains open because static HQ inspection found the following bounded correctness/execution defects.

## 2. Blocker A — actual pyreadstat Stata extended-missing token form is still misclassified

The returned implementation recognizes an extended missing only when the reader/metadata token has form `.a` through `.z`:

`len(token) == 2 and token[0] == '.'`

and the direct classifier test injects `.a` manually.

The pyreadstat DTA contract used by this implementation exposes Stata `.a` through `.z` under `user_missing=True` as reader-native single-character values `a` through `z`; `metadata.missing_user_values` likewise lists the single-character values. The source-native Stata notation remains `.a` through `.z`, but the reader execution token is `a` through `z`.

Therefore the real DTA decode path would currently turn a pyreadstat extended-missing declaration such as `a` into generic discrete user-missing and would not emit `FORMAT_EXTENDED_MISSING`.

Disposition:

`BLOCKED_DTA_EXTENDED_MISSING_READER_TOKEN_MISMATCH`

Correction requirement:

- DTA-specific missing-declaration extraction must recognize pyreadstat reader-native `a` through `z` as Stata extended missing;
- preserve both the exact reader-native token and the source-native Stata token (for example `reader_token='a'`, `stata_token='.a'`) without semantic interpretation;
- the corresponding physical cell must emit `FORMAT_EXTENDED_MISSING`;
- add an on-disk DTA fixture using pyreadstat `write_dta(..., missing_user_values=...)` when supported by the installed dependency, not only a hand-injected classifier fixture;
- keep SPSS user-missing behavior separate.

## 3. Blocker B — content-addressed selector/path identity is not bound on reopen

`reopen(source_sha256, release_id, semantic_hash)` constructs a content-addressed directory from the supplied selectors, but after reconstruction it checks the reconstructed release against the manifest rather than checking the manifest/reconstructed identity against all three supplied selectors.

A self-consistent rewritten manifest/relation set could therefore claim a different semantic release identity while residing under the directory named by the caller's old selector.

Disposition:

`BLOCKED_REOPEN_SELECTOR_PATH_IDENTITY_NOT_CLOSED`

Correction requirement:

Before returning any release, prove exactly:

- supplied `source_sha256` is a lowercase 64-hex SHA and equals manifest/reconstructed source artifact content hash;
- supplied `release_id` equals reconstructed/manifest release id;
- supplied `semantic_hash` is a lowercase 64-hex SHA and equals reconstructed release semantic hash and manifest release-ref content hash;
- the canonical directory path derived from the reconstructed identity equals the directory actually opened;
- malformed/path-traversing selectors fail closed.

Add a hostile test that rewrites a complete canonical relation set + manifest into a self-consistent *different* release identity under the old directory path. `reopen(old selectors)` must reject it.

## 4. Blocker C — DuckDB direct query still performs full Python logical reopen first

`query_canonical_release(...)` currently calls `carrier.reopen(...)` before creating DuckDB views.

`reopen(...)` reads every canonical relation with PyArrow, converts every row to Python dictionaries, reconstructs every C11 object, sorts the full public/internal object inventories and reconstructs `C11LogicalRelease`.

Thus a nominal direct-Parquet analytical query still requires full Python materialization of the logical release before DuckDB executes. On WVS7-scale respondent-event incidence this defeats the selected direct-Parquet execution model and recreates the memory problem the carrier was chosen to avoid.

Disposition:

`BLOCKED_DUCKDB_DIRECT_QUERY_FORCES_FULL_LOGICAL_MATERIALIZATION`

Correction requirement:

Separate:

1. full semantic audit/reopen, which may reconstruct a `C11LogicalRelease` when explicitly requested; and
2. analytical query-session opening, which must validate the exact content-addressed carrier without materializing all relation rows/C11 objects.

Implement a bounded in-process DuckDB direct session/path that:

- reads and validates manifest schema + exact selector binding;
- verifies required canonical member inventory and member byte identities once per opened session;
- opens in-memory DuckDB views directly over those exact Parquet members;
- runs multiple queries without reconstructing the full C11 object universe;
- creates no persistent `.duckdb` file;
- exposes the exact verified release/manifest identity in the session receipt.

Relation-level semantic audit remains required for explicit `reopen()` / certification audit, but may not be an implicit prerequisite for every analytical query.

Add a hostile test that monkeypatches/guards full `_read_rows` or object reconstruction and proves DuckDB direct query succeeds without invoking them.

## 5. Blocker D — physical-to-I02 bridge does not bind candidate to physical bytes or real authority refs

The returned bridge defines:

`required_authority_refs: tuple[Any, ...]`

and accepts the bridge whenever that tuple is merely nonempty and `candidate_builder` is callable.

The correction test passes the string `EXPLICIT_SOURCE_AUTHORITY` and a callback that returns a prebuilt synthetic candidate unrelated to the decoded physical source. The bridge then validates that unrelated candidate successfully.

This does not establish the required law:

`these exact physical bytes + these exact source authorities -> this C11 candidate`.

Disposition:

`BLOCKED_PHYSICAL_I02_SOURCE_AUTHORITY_BINDING_NOT_ENFORCED`

Correction requirement:

- `required_authority_refs` must be exact `AuthorityRef` values, not `Any`/arbitrary strings;
- after candidate construction, bridge must verify candidate `source_release_manifest.source_artifact_content_hash == incidence.source_sha256`;
- candidate source artifact identity must be the exact physical source snapshot being bridged;
- every required authority ref must be present in and resolve against the candidate's supplied authority snapshots/declared authority closure as required by existing I02 law;
- missing/mismatched source identity or authority binding fails before admission;
- the bridge must still invoke existing `validate_c11_source_release()` and may not infer source semantics itself.

Add hostile tests for:

- candidate built for a different source SHA;
- arbitrary string/non-AuthorityRef "authority";
- required authority ref absent from candidate authority snapshots;
- valid explicitly-bound candidate passes.

## 6. Blocker E — non-compatibility sources still use unconditional full-frame decode

The correction removed complete `PhysicalCell` tuple materialization, which is accepted progress.

However `_decode(...)` still uses one full `read_sav/read_dta` DataFrame for every source. `iter_batches()` only batches conversion *after* the entire frame is resident.

The already-accepted SR03 execution established a safer physical pattern:

- default/non-compatibility sources use `pyreadstat.read_file_in_chunks(...)`;
- exact compatibility-override sources may use the frozen full-read path where chunked execution is known to fail.

Disposition:

`BLOCKED_DEFAULT_DECODER_UNNECESSARY_FULL_FRAME_MATERIALIZATION`

Correction requirement:

- use metadata-only read for source metadata;
- for sources without a frozen compatibility override, stream/chunk physical rows from the source using the same exact reader configuration;
- only exact SHA allowlisted compatibility sources may retain the explicitly required full-read compatibility path;
- global row ordinal must remain stable across chunks;
- repeated iteration/replay must be deterministic;
- batch-size/chunk-size changes must not change canonical physical-cell identity/digest.

Add a test proving the normal decoder path does not call full `read_sav/read_dta` after metadata acquisition when a chunk path is available.

## 7. Known scale risk deferred to proving-source gate, not silently accepted

Even after physical decoding is streamed, existing `C11SourceReleaseCandidate` / `C11LogicalRelease` APIs use materialized tuple inventories. That representation has only been exercised synthetically and may become the next WVS7-scale pressure point.

This R2 gate does **not** authorize redesign of I01-I07 or M01-M18 semantics to pre-solve that possibility.

Instead, once the bounded defects above are corrected and G-SR06 is otherwise acceptable, G-SR07/G-SR08 must begin with a fail-closed execution-scale preflight that measures the real proving-source path before allowing an uncontrolled full materialization. If existing I02 representation proves operationally impossible, HQ will adjudicate a representation-only implementation extension under the frozen logical semantics.

Do not hide this risk by converting the physical iterator to `list(...)`/`tuple(...)` inside SR06 tests.

## 8. Good correction work to preserve

Preserve unless superseded by the exact fixes above:

- relational Parquet split;
- no complete duplicated release/object blobs;
- direct scalar/queryable respondent-event columns;
- manifest member hashes + relation logical digests;
- relation-driven full logical reopen;
- semantic object content-hash verification on reconstruction;
- cross-relation semantic mutation rejection;
- immutable/content-addressed layout and staging publication;
- exact-SHA compatibility allowlist and compatibility-only authority status;
- in-memory DuckDB only;
- no PostgreSQL/SQLite/DATABASE_URL empirical authority path;
- existing PRE553 semantic behavior and regression expectations.

## 9. Required R2 tests

Preserve prior passing tests and add/pass at minimum:

1. real writer/readback Stata extended-missing test using reader-native `a`-`z` and source-native `.a`-`.z` preservation;
2. exact selector/path/reconstructed identity closure tests;
3. self-consistent wrong-release-under-old-path hostile test;
4. DuckDB direct session test proving no full relation/C11 reconstruction is invoked;
5. multiple queries in one verified in-memory session;
6. bridge wrong-source-SHA rejection;
7. bridge non-AuthorityRef rejection;
8. bridge missing-required-authority rejection;
9. valid source+authority-bound bridge admission;
10. default decoder chunk-path enforcement;
11. compatibility allowlisted full-read exception test;
12. batch/chunk-size-independent physical identity/digest test;
13. all prior SR06 corruption/relational/atomicity tests;
14. existing PRE553 regression suite.

No WVS7, LiTS-I or CLOSED_35 full run is authorized in this R2 correction.

## 10. Gate state

`G-SR06 = CORRECTION_R2_REQUIRED`

G-SR07 and G-SR08 remain blocked.

Required R2 return token:

`PRE553_SR06_R2_EXECUTION_IDENTITY_CORRECTION_RETURNED`

HQ will inspect the corrected branch before issuing any proving-source execution authority.
