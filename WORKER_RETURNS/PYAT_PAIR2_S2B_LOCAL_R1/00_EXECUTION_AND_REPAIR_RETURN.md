# PYAT S2-B / P2-02 — Local execution and causal repair return R1

**Status: `READY_FOR_INDEPENDENT_G5` at the explicitly scoped evidence below.**
This is not a self-issued G5 and not an original35/CURRENT/P01–P20/T01–T18
rights decision. G5 itself remains **NOT_SELF_ISSUED**.

## 1. Exact lineage and custody

- Governing commission: S2-B / P2-02 / issue #919 under #909 R3/R3C/R3S.
- Frozen code/test/workflow cut: `edd0611d1ea0e80a47692635fe3bd73a079f1bec`.
- Agent A R5 PR #974, last reported docs HEAD:
  `fef8abd4c61508bb85c1797b73006b60c5fe0170` (documentation-only after the code cut).
- Repair branch and draft PR #979:
  `agent/pyat-s2b-r5-local-repair-20261112` →
  https://github.com/maidiu/rawlsing/pull/979, based on
  `agent/pyat-pair2-s2b-a-direct-candidate-20261112-r5`, **not** PRE-MAIN.
- Source/test repair commit: `155cd1b7244ab22ede804386e6d5253a39fe3587`.
  Return documentation is the commit that contains this file; the immutable
  branch HEAD is reported in the final return message.
- Protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e` was not reset,
  modified or merged.

The worktree started exactly at the frozen code cut. No other agent's branch
was overwritten and no protected PRE-MAIN reference was touched.

## 2. Real Linux execution environment

The host was macOS; the court was run in a real Linux VM (Lima 2.3.0 with the
Apple Virtualization framework), not on macOS emulation.

- Linux `7.3.0-9-generic`, Ubuntu 26.10, x86_64, 2 vCPU, 4 GiB RAM.
- `/proc/self/fd` present, so the descriptor-pinned cold verifier executed.
- Python `3.11.18` (uv-managed CPython).
- pytest `9.2.0`, pyarrow `26.0.1`, pandas `3.1.1`, pyreadstat `1.3.7`.
- Full details: `logs/14_ENVIRONMENT.txt`.

Compilation:

```bash
python -m py_compile \
  rawlsing_next/_pre553_direct_i02_sourcefree.py \
  rawlsing_next/_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py
```

Result: `COMPILE_OK`.

## 3. Executed court

### 3.1 Frozen direct court, first execution

```bash
PYTHONPATH=. python -m pytest -vv -x -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py
```

Frozen direct file: **14 passed in 8.78 s** (`logs/00_DIRECT_FIRST_RUN_FROZEN.log`).
No existing test failed. The defects below were found by independent
adversarial probes against the historical validators, not by waiting for a
pytest failure.

### 3.2 Complete inherited court, final branch

```bash
PYTHONPATH=. python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
  --junitxml=s2b-local-full.xml
```

Final result: **129 passed, 0 failed, 0 skipped** in 24.71 s; process max RSS
143,560 KiB. JUnit: `logs/02_S2B_LOCAL_FULL_FINAL.xml`.
Per-file counts: direct 26, external 29, verified range 26, empirical query 32,
repository ingest 16.

GitHub Actions runner assignment remained unavailable. Run `43314303601` at
code/docs cut `1ce6e8c1ae916e69a62e5560a14e7d57ee562374` failed with an empty
`runner_name` and zero executed steps. It is not counted as test execution;
the Linux court above is the actual executed evidence.

### 3.3 Standalone SQLite attack reproduction

```bash
PYTHONPATH=. python rawlsing_next/tests/repro_s2b_sqlite_session_attack_stdlib.py
```

Result: `STANDALONE_G3_G4_PRIMITIVE_REPRODUCTION_PASS`
(`logs/03_REPRO_ATTACK_FINAL.log`), retaining TEMP-shadow, BINARY-collation and
atomic no-clobber primitive protections.

### 3.4 Material probes

- Direct 2,048 one-shot events: **passed** (`logs/04_MATERIAL_2048_FINAL.log`).
- Inherited 2,048-respondent derived-cert probe: **passed**
  (`logs/05_MATERIAL_EXTERNAL_FINAL.log`).
- Additional synthetic direct probe, 100,000 one-shot events / **one**
  respondent: **passed** (`logs/06_SCALE_100000_FINAL.log`).
- Scaling trend 2,048 / 20,000 / 100,000 events:
  `logs/08_SCALE_2048.log`, `logs/07_SCALE_20000.log`,
  `logs/06_SCALE_100000_FINAL.log`.

The 100,000-event run is **not** a 100,000-respondent proof and is not an
original35 or integrated 6 GiB proof.

## 4. Defects reproduced and repairs committed

Every RED input is preserved in `logs/09_RED_NEW_TESTS_ON_FROZEN.log`.
The GREEN rerun is `logs/10_GREEN_NEW_TESTS_ON_REPAIRED.log`.

### D1 — Direct builder accepted duplicate manifest declarations that original I02 rejects

- Obligation: complete source/provenance closure; declared universe and
  authority census must exactly match the package.
- RED: `declared_universe_refs=(u,u)` and a duplicated
  `declared_authority_snapshot_refs` were accepted by the direct builder while
  `validate_c11_source_release` rejected both.
- Repair: exact duplicate-declaration refusal in
  `build_sourcefree_direct_i02` before SQLite staging.
- Test: `test_s2b_a5_direct_duplicate_manifest_declarations_refused`.
- Frozen: `DID NOT RAISE ExternalI02IntegrityError`; repaired: PASS.

### D2 — Direct builder rejected a legacy-valid manifest with no ReplayManifest count

- Obligation: conserve original I02 declared-census requirements.
- RED: original I02 requires only the seven core family declarations; the
  direct builder additionally required `ReplayManifest: 1`.
- Repair: require core declarations; if `ReplayManifest` is declared it must be
  exactly 1, matching the original actual-count comparison.
- Test: `test_s2b_a5_direct_legacy_valid_manifest_without_replay_count`, which
  rebuilds the historical replay manifest, proves original I02 acceptance and
  asserts byte-identical direct projection/replay/release refs.
- Frozen: rejected; repaired: PASS.

### D3 — Malformed direct certificate leaked a raw SQLite error

- Obligation: hostile completeness and typed refusal.
- RED: a direct-schema header on a certificate missing `event_occurrences`
  raised `sqlite3.OperationalError: no such table`.
- Repair: cold verification wraps SQLite structural errors as
  `ExternalI02IntegrityError`, retaining the original exception as cause.
- Test: `test_s2b_a5_direct_cold_verifier_typed_refusal_on_missing_direct_tables`.
- Frozen: raw `sqlite3.OperationalError`; repaired: PASS.

### D4 — Direct atomic publication leaked a raw OSError

- Obligation: atomic no-clobber publication and typed refusal.
- RED: a failing `os.link` raised `OSError` rather than the certificate error.
- Repair: wrap non-collision `OSError` as `ExternalI02IntegrityError`; the
  staged artifact is still removed and no destination is created.
- Test: `test_s2b_a5_direct_publication_oserror_typed_no_clobber`.
- Frozen: raw `OSError`; repaired: PASS.

### D5 — Authority validation escaped as the base C11 error type

- Obligation: consistent certificate-specific typed refusal for untrusted
  sourcefree input.
- RED: a forged event authority ref raised `C11IntegrityError`, not
  `ExternalI02IntegrityError`.
- Repair: public `build_sourcefree_direct_i02` is now a thin refusal boundary
  over the implementation and maps `Pre553IntegrityError`/authority failures to
  `ExternalI02IntegrityError`; existing certificate errors are preserved.
- Tests: `test_s2b_a5_direct_wrong_authority_is_typed_refusal`; RED/GREEN type
  evidence in `logs/11_...` and `logs/12_...`.

### D6 — Direct selectors had no native I03 installation path

- Obligation: G2 direct first-consumer conservation, distinct from S2-C.
- RED: frozen code had no direct-schema native installation; importing
  `install_direct_sourcefree_i02_i03` failed (`logs/13_...`).
- Repair: new `install_direct_sourcefree_i02_i03` accepts only a direct-schema
  cold certificate whose reconstructed historical source, replay and release
  identities exactly equal an already-sealed repository body release. It never
  mints the legacy validation seal and the ordinary legacy installer still
  refuses direct-schema certificates.
- Tests:
  - `test_s2b_a5_direct_historical_identity_installs_native_i03_selectors`
    (positive, wrong-identity refusal);
  - `test_s2b_a5_direct_changed_restored_native_i03_eligible_output`;
  - `test_s2b_a5_direct_sourcefree_drives_full_native_i03_query` (complete
    `execute_empirical_query`, changed numerator 2→3, restoration).

No test was weakened, skipped or replaced by a hand-written statistics model.
The inherited protections remain green.

## 5. Historical replay and release identity parity

The direct producer reconstructs the original identities by streaming
disk-sorted SQLite rows; it does **not** construct `C11LogicalRelease`,
`ReplayManifest.closure_refs` or a private validation seal.

Executed parity against the actual historical `validate_c11_source_release`:

| Case | Projection | Replay ref | Release ref |
| --- | --- | --- | --- |
| Base typed-absence fixture | equal | equal | equal |
| WeightMeasureFact present | equal | equal | equal |
| 19 respondents, reversed section order | equal | equal | equal |
| Canonical + component aliases | equal | equal | equal |
| Multi-universe SourceUniverseRelation | equal | equal | equal |
| All four optional internal replay families | equal | equal | equal |
| Legacy-valid manifest without ReplayManifest count | equal | equal | equal |

The parity probes are in `probes/` and the committed tests. This demonstrates
byte-identical SHA256 identity for the same typed section contents. It is not
an original35 source-equivalence or CURRENT-rights decision.

## 6. Real native I03 conservation

- `_build_release_index`/`_select_respondent_events` actual native selector
  output matches direct selectors in complete ordered lists, including native,
  canonical, component, state filters, multiple occurrences and order.
- `install_direct_sourcefree_i02_i03` installs the direct selector index only
  against an exact sealed body release with matching reconstructed historical
  identities.
- Full native `execute_empirical_query`:
  - original: `raw_numerator_support = 2`;
  - changed response: `raw_numerator_support = 3` and changed result;
  - restored source: original result exactly reproduced.
- A changed direct certificate is refused against the original sealed release.

Body semantics come from the already sealed repository; cold physical body
realization remains the separate S2-C obligation.

## 7. Resource measurements

Environment: 2 vCPU, 4 GiB RAM Linux VM.

| Probe | Scale | Retained SQLite | Build | Cold verify | Python peak | Process max RSS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Direct one-shot | 2,048 events / 1 respondent | 13,135,872 B | 9.673 s | 0.2555 s (+2048 selects) | 2,233,151 B | 42,572 KiB |
| Derived external | 2,048 respondents | 24,801,280 B | 6.8231 s | 0.3105 s | 2,112,349 B | 101,428 KiB |
| Direct one-shot | 20,000 events / 1 respondent | 126,853,120 B | 65.385 s | 1.967 s | 2,231,333 B | 40,520 KiB |
| Direct one-shot | 100,000 events / 1 respondent | 638,414,848 B | 365.843 s | 11.158 s (+100k selects) | 2,231,126 B | 40,328 KiB |

The 100,000-event probe decoded 100,000 generated typed events, selected
100,000 postings and retained the 638 MB SQLite artifact. Sampled
workdir+TMP peak was 685,603,704 B. SQLite scratch-file peak and process-tree
RSS were not separately instrumented; no 100,000-respondent or integrated
6 GiB pipeline was run. These are the exact unmeasured G4 dependencies.

The direct builder does not require a legacy full-object release or a
heap-sized replay closure array. Its Python peak stayed ~2.23 MB from 2,048 to
100,000 events while SQLite did the sorting and retention on disk.

## 8. G1–G5 receipt

- **G1 — satisfied at scoped sourcefree typed-section evidence.** All 13
  families, typed absences, source/authority binding, occurrence identity and
  reconstructed M01–M18 replay are exercised; historical SHA256 parity is
  executed for the cases above. Live S1-B/E decoder-to-section input and
  original35 source equivalence remain separate source-production/rights holds.
- **G2 — satisfied at direct-selector + sealed-body scope.** Direct
  certificates reach the complete index and actual native I03 selector and
  full-query path; changed input changes eligible output and restoration
  reproduces it. S2-C cold physical body realization remains separate.
- **G3 — satisfied at tested hostile scope.** Omissions, duplicate
  occurrences, duplicate declarations, forged selectors, wrong source,
  wrong authority, unlawful typed absence, locally rehashed incomplete
  artifacts, malformed tables and publication failures refuse admission with
  certificate-typed errors. No claim is made against hostile kernel or
  arbitrary co-resident Python introspection.
- **G4 — satisfied at measured sourcefree scope.** Bounded one-shot event
  construction is demonstrated to 100,000 events at ~40 MB RSS with no legacy
  release/closure; 100,000 respondents, full integrated 6 GiB, process-tree RSS
  and exact SQLite scratch peak remain unmeasured and are named as such.
- **G5 — NOT_SELF_ISSUED.** Independent nonauthor receiving is required.

Separate authority holds retained: original35 source equivalence, CURRENT
permission, P01–P20/T01–T18, S2-A receiving, S2-C physical implementation,
W03/W04. They are not used to excuse any executed in-scope failure.

## 9. Strongest remaining adversarial attacks

1. Supply a genuinely live S1-B/E one-shot decoder stream at this exact ABI and
   force real corpus cardinality/respondent cardinality through the builder.
2. Run 100,000 respondents and the integrated 6 GiB pipeline with process-tree
   RSS and SQLite scratch peak instrumentation.
3. Attack the direct installer with a direct certificate whose historical
   identities collide but whose selector/body binding differs at the first
   native query.
4. Exercise exotic typed absence states, multiple instrument versions with
   distinct aliases, and duplicate non-occurrence objects; the direct builder
   deliberately refuses duplicate non-occurrence object refs more strictly
   than the legacy validator.
5. Try hostile physical filesystem/process races beyond the descriptor-pinned
   cold open and atomic no-clobber publication.

## 10. Evidence inventory

All paths are under `WORKER_RETURNS/PYAT_PAIR2_S2B_LOCAL_R1/`.

- `logs/00…14` — execution, JUnit, RED/GREEN, material, environment.
- `probes/` — independent parity, alias, multi-universe, optional-family,
  direct-native, scale and error-typing probes. Run from the repository root:

  ```bash
  RAWLSING_ROOT="$PWD" PYTHONPATH=. python WORKER_RETURNS/PYAT_PAIR2_S2B_LOCAL_R1/probes/probe_scale.py 100000
  ```

- `SHA256SUMS` — checksums of every returned log/probe file.
- Machine receipt: `01_G1_G5_RECEIPT.json`.

No original35 data was used and no source/current permission was invented.
