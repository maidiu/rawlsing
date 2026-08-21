# SR06 — DECODER / C11 PARQUET-DUCKDB IMPLEMENTATION AUTHORITY

Status: `AUTHORIZED__CODEX_IMPLEMENTATION__NON_SEMANTIC`

Repository: `maidiu/rawlsing`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Exact implementation launch HEAD is supplied separately by HQ after governance closure.

## 1. Dependency closure

G-SR04 is accepted by:

`32_SR04_REAL_B2_R4_ADJUDICATION_AND_CARRIER_SELECTION.md`

Selected physical carrier:

`PARQUET_DUCKDB_DIRECT`

G-SR05 is already accepted.

Therefore G-SR06 is unblocked for implementation.

## 2. Binding architecture

The runtime boundary remains:

`rawlsing_next/**`

Existing PRE553 logical semantics and object contracts remain binding.

In particular, inspect and preserve:

- `rawlsing_next/pre553_empirical_objects.py`
- `rawlsing_next/pre553_empirical_authority.py`
- `rawlsing_next/pre553_c11_integrity.py`
- `rawlsing_next/pre553_c11_ingest.py`
- `rawlsing_next/pre553_c11_repository.py`
- `rawlsing_next/pre553_empirical_query.py`
- `rawlsing_next/pre553_discovery_exact.py`
- existing PRE553 tests under `rawlsing_next/tests/`

`C11Repository` is an accepted file-neutral logical repository. Its exact-key, append-only, validated-release semantics are not replaced by a database-product model.

SR06 adds physical source decoding and the selected persistent carrier beneath the accepted logical layer.

## 3. Required implementation result

Implement one coherent format-neutral path:

`exact source bytes -> thin physical decoder -> deterministic source-native incidence -> existing C11 logical ingest/validation -> immutable canonical Parquet persistence -> embedded DuckDB direct read/query adapter`

The implementation must contain:

1. one format-neutral physical decoder result/interface;
2. a SAV decoder plugin obeying `10_FORMAT_DECODER_CONTRACT.md`;
3. a DTA decoder plugin obeying `10_FORMAT_DECODER_CONTRACT.md`;
4. one deterministic C11 physical writer/repository adapter using canonical Parquet;
5. one direct embedded-DuckDB read/query adapter over the canonical Parquet relations;
6. deterministic content/replay manifests sufficient to prove that reopening the persistent carrier reproduces the accepted logical identities;
7. tests proving physical persistence does not mutate existing logical C11 semantic identities or source evidence.

Exact file split/name is implementation detail, but all new production runtime must remain under `rawlsing_next/**` and tests under `rawlsing_next/tests/**`.

## 4. Selected carrier law

Canonical persistent empirical state is Parquet.

Requirements:

- immutable/content-addressed release or snapshot layout;
- deterministic file naming/layout from exact logical/source identities;
- ZSTD Parquet compression unless a narrower existing dependency constraint requires the already-tested equivalent;
- deterministic row ordering where ordering participates in replay/digest identity;
- direct embedded DuckDB reads against Parquet;
- no authoritative `.duckdb` database file;
- no PostgreSQL or SQLite empirical truth path;
- no `DATABASE_URL` dependency;
- no second canonical empirical copy;
- partial writes cannot become a visible committed C11 release;
- exact reopen/readback must fail closed on missing/corrupt manifests or Parquet members.

A derived DuckDB object/view may exist only in-process/nonauthoritatively and must be reproducible from canonical Parquet.

## 5. Physical decoder law

Read and obey exactly:

- `09_SOURCE_NATIVE_CONSTITUTION.md`
- `10_FORMAT_DECODER_CONTRACT.md`
- `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`

The decoder is a dumb byte-to-source-incidence adapter.

It may expose file-format facts. It may NOT:

- infer semantic missing states from labels;
- choose canonical questions;
- select a preferred weight;
- infer routing from pattern alone;
- harmonize waves;
- consult legacy Postgres as truth;
- drop user-missing/system-missing cells;
- replace row identity after filtering;
- guess encodings;
- upgrade compatibility reader encoding to text/semantic authority.

SAV must preserve SPSS system missing, discrete/range user missing, raw values, labels, metadata and physical topology metadata.

DTA must preserve ordinary values, system missing, extended missing when present, labels and storage/display metadata. Ordinary labeled DK/refusal/N/A codes remain ordinary source values until source authority says otherwise.

The exact frozen compatibility allowlist in `10_FORMAT_DECODER_CONTRACT.md` is binding.

## 6. Logical C11 preservation law

Do not redesign M01-M18 or object semantics.

The physical adapter must preserve existing logical:

- exact refs;
- semantic hashes;
- source artifact refs;
- validated-release sealing;
- replay manifests;
- authority snapshots;
- event occurrence identity;
- respondent incidence;
- topology/routing/design records;
- typed absence distinctions;
- no-latest/no-fuzzy exact resolution behavior.

If the selected physical carrier cannot represent a required existing logical distinction, STOP with:

`BLOCKED_POTENTIAL_FROZEN_CONTRACT_CONTRADICTION`

Do not repair the logical contract.

## 7. Implementation acceptance tests

At minimum add and pass tests for:

### A. Synthetic SAV physical decoder

A tiny generated/controlled SAV fixture must exercise:

- ordinary numeric value;
- system missing;
- SPSS user-missing discrete value;
- SPSS user-missing range;
- raw code retained independently of value label;
- row ordinal retained;
- variable ordinal/name retained;
- value/variable metadata retained.

### B. Synthetic DTA physical decoder

A tiny generated/controlled DTA fixture must exercise:

- ordinary numeric/string value;
- Stata system missing;
- extended missing when the chosen writer/reader fixture can lawfully create it, otherwise explicit typed fixture limitation;
- ordinary labeled nonresponse-like code remaining ordinary;
- row/variable identity and metadata retention.

### C. Compatibility-encoding enforcement

Test that:

- only exact allowlisted source SHA/config may request a frozen compatibility override;
- an unallowlisted automatic fallback/guess is rejected;
- compatibility authority status remains `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

No full 35-source scan is required in SR06.

### D. Logical release persistence round-trip

Construct an accepted C11 logical release through the existing I02 validation path, persist it to canonical Parquet, reopen it, and prove:

- exact release ref equality;
- exact semantic release hash equality;
- exact public/internal object ref inventory equality;
- replay manifest equality;
- M01-M18 coverage equality;
- deterministic persistent manifest identity;
- a second identical write is idempotent or resolves to the same exact content-addressed release;
- conflicting same-release identity fails closed.

### E. Corruption/atomicity hostile tests

Prove fail-closed behavior for at least:

- missing Parquet member;
- mutated Parquet bytes;
- mutated persistent manifest;
- incomplete/staging directory presented as committed;
- wrong source/release hash;
- attempted fuzzy/latest lookup;
- attempted authoritative DuckDB-file substitution.

### F. DuckDB-direct query smoke

Directly query the reopened canonical Parquet relations with embedded DuckDB and prove the result is derived from those exact Parquet bytes, without creating a persistent DuckDB database file.

### G. Existing PRE553 regression suite

Run at minimum the existing tests directly touching:

- C11 repository/ingest;
- empirical objects/authority;
- empirical query;
- replay audit;
- source equivalence;
- source relations;
- discovery exact;
- structural admission.

Any regression caused by changing accepted semantics is a failure, not permission to update the test expectation.

## 8. Scope boundary versus SR07/SR08

SR06 implements machinery. It does not certify WVS7 or LiTS I source equivalence.

Do not claim G-SR07/G-SR08 evidence merely because a decoder can read those formats.

Real proving-source certification remains a separate gate after SR06 implementation is accepted.

A bounded real-source smoke may be run only if required to prove reader mechanics without semantic certification, and must be explicitly labeled non-dispositive.

## 9. Required return

Commit implementation + tests to the assigned SR06 worker branch.

Return to HQ:

- exact starting HEAD;
- branch name;
- final commit SHA;
- changed-file list;
- implementation summary;
- exact Parquet canonical layout;
- exact commit/atomicity protocol;
- exact decoder interface and SAV/DTA plugin behavior;
- exact compatibility-encoding enforcement mechanism;
- test commands and complete pass/fail summary;
- hostile corruption-test results;
- existing PRE553 regression results;
- proof no persistent DuckDB database file is authoritative/required;
- proof `DATABASE_URL` is unused;
- final `git status -sb`.

Then STOP for HQ adjudication.

Required implementation return token:

`PRE553_SR06_DECODER_C11_PARQUET_DUCKDB_IMPLEMENTATION_RETURNED`

G-SR06 remains open until HQ inspects the committed implementation and acceptance evidence.
