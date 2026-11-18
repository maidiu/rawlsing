# ANVIL two-edit integrated executable cut

## Status

**Frozen for distinct joined review; postconsumer G5 remains separately pending.**

- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Integration parent: `e0445a00f2fbb9643880aeb83452aa956f8134fe`
- **Integrated code/test commit: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`**
- Source locality archive: `60e767a53ecdffaae289a11fc5ce6c40e5c4ecd0`
- Locality G5 review: `9ff290fd9d5eda87cb1541bd7b48b48897f6e099`
  (`ACCEPT_SCOPED_PRODUCTION_LOCALITY_CORRECTION`)
- Postconsumer author cut: `01dc90cb0d1c5c7cdcf5cb29a02bc0cfda650efd`
  (author-frozen; **separate G5 pending**)
- Own return: `WORKER_RETURNS/ANVIL_ENGINEERING_TWO_EDIT_INTEGRATION_20261118/`
- New source/science/issuer/actor/CURRENT/protected rights: **NONE**
- Self-acceptance/final joined acceptance: **NONE**

## Exact integration

Only these exact frozen locality files were imported from `60e767…`:

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_direct_estate_i03.py` | `d662fc578a1ecb42d54ec8b4bdab87fd7ecec176` |
| `rawlsing_next/tests/test_anvil_production_locality_20261118.py` | `7373c1704e21bcb4155eb690b17de5ecd8bf22dc` |

No merge, cherry-pick, evidence-branch copy, or other production change was
made.

Integration invariants:

- Existing postconsumer blob after integration:
  **`0a2e7b899ebd392761d38b8ceb175f0bf81c6378`** (unchanged from the
  author-frozen postconsumer cut).
- Cut1 integration wrapper:
  **`c568836b7ab1ce88224d4bc5c9de6dca8476a5db`** (unchanged).
- Cut1 Batch runner:
  **`8320f28458fb85aec655d154a2527a161282f56b`** (unchanged).
- Exactly two production files differ from baseline `347baec…`:
  `pre553_direct_estate_i03.py` and
  `pre553_source_postconsumer_receipts.py`.
- Two new focused tests differ from the same baseline:
  production locality and prepared postconsumer.

## One affected-union execution

Command:

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  --basetemp=WORKER_RETURNS/ANVIL_ENGINEERING_TWO_EDIT_INTEGRATION_20261118/tmp/union \
  rawlsing_next/tests/test_anvil_prepared_saved_postconsumer_join.py \
  rawlsing_next/tests/test_anvil_production_locality_20261118.py \
  rawlsing_next/tests/test_anvil_prepared_saved_batch_cut1.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py \
  rawlsing_next/tests/test_pre553_prepared_saved_i03.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  rawlsing_next/tests/test_pyat997_r03_governed_query_issuer_v2.py
```

Result:

```text
113 passed, 0 failed, 0 errors, 0 skipped
exit 0
42.61 s
```

Per-file collection:

- postconsumer focused: **8**
- production locality: **2**
- cut1 prepared Batch: **5**
- native I03 direct estate: **7**
- parquet estate/writer: **24**
- prepared saved I03: **3**
- empirical query: **32**
- original R6 first consumer / S1E: **24**
- R03 v2 guard: **8**

Total: **113**.

Evidence: `evidence/integrated_union.txt`,
`evidence/integrated_union.time`, `evidence/node_inventory.txt`.

## Integrated source → prepared Batch → postconsumer

`evidence/integrated_parity.py` is the existing postconsumer witness with only
its output path changed; it uses the existing sourcefree Q2/native fixture, R03
v2 issuer, saved Batch, prepared admission, and actual postconsumer join.

- Source SHA: `c9911a0c4448b34bbe82175f35345e921fc935276d7e04eaf1eb72dcecf90418`
- Estate manifest:
  `99624c65d0e2fdb61ecd465a5cc182d79104ff63b1e765d6f4882ccb1af82f9e`
- 13-family table; 5 respondents; sourcefree fixture.
- Source stats: one snapshot acquisition, `full_c11_builds=0`, cleanup complete.
- Compiler: v1 **0 QUERY / 1 DISCOVERY**, v2 **12 QUERY / 1 DISCOVERY**.

| Property | Base `SavedC11Admission` | Prepared `PreparedSavedC11Admission` |
|---|---|---|
| Batch units | 13 | 13 |
| States | all COMPLETED | all COMPLETED |
| Prepared index builds | n/a | **1** |
| Postconsumer operations | 22 | 22 |
| ELIGIBLE / HELD | 8 / 14 | 8 / 14 |
| Positive native-linked | 6 | 6 |
| Pending eligible | 2 | 2 |
| Native units rechecked | 13 | 13 |
| Discovery candidates joined | 8 | 8 |
| Issue grants | 0 | 0 |
| Result hash | `886c5d452c8d078beab53486e8b341f5c97d1914766557101328cc585d87c9ec` | same |

Rows, audit, result hash, native refs/replay, and Batch provenance are equal.
This includes the actual integrated source readers, not a test-only substitute.

Proof: `evidence/integrated_parity.json`.

## Locality acceptance retained

The integrated `DirectEstateI03Session._respondent_family` is the exact accepted
production implementation, not a monkeypatched method:

- canonical ref order restored after physical gid/off traversal;
- `_require_live` before every yield;
- per-respondent/family bounded buffer;
- later-row/body malformed refusal remains typed and eager.

Frozen G5 evidence reused, not rerun:

- review: `9ff290fd9d5eda87cb1541bd7b48b48897f6e099`;
- actual production revocation-after-first-yield and 600 canonical refs;
- sealed R2 actual f4: 50 row-group reads, 25,472 rows, 9,600 family objects,
  32-field exact parity, fact `ff607ebd…`, external supervision 6.539 s,
  process-tree RSS 131,907,584 B, scratch 30,368,896 B;
- locality existing courts: 36/37 pass.

No new locality benchmark, body experiment, or sealed-estate rebuild was run.

## Guards and changed input

The union includes:

- postconsumer wrong class/subclass, foreign runner/repository, root/manifest,
  revoked CURRENT, unissued fabricated QUERY, forged receipt;
- S1E source/current refusals, missing receipt/fate guards, and changed
  legitimate source input → changed native fact → exact restore;
- R03 v2 v1/v2 issuer distinction and postconsumer anti-injection guards;
- native I03/body/parquet/prepared/empirical-query negatives.

## Resources and limits

- Union: wall **43.23 s**, user **39.68 s**, sys **10.40 s**, parent max RSS
  **141,873,152 B**.
- Integrated witness: wall **3.17 s**, user **3.56 s**, sys **0.53 s**,
  parent max RSS **124,973,056 B**.
- Staging memory: **NOT_MEASURED**.
- No 100k/full benchmark matrix.
- No cold/shared H/S/Q/O scale run; G5 actual f4 is reused at its accepted
  sealed-estate scope.
- One bounded union execution; no duplicated overlapping invocations.

## Provenance and review

- Locality G5 handoff/receipt read from
  `OWNER/WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/`.
- Postconsumer G5 is separate and still pending; this cut does **not** claim
  final joined acceptance.
- Exactly two production files differ from baseline; no protected merge,
  source/reopen, science, issuer, writer, schema, or CURRENT grant.
- R3 research archive and prior frozen commits untouched.
- No subagents, model switch, or background jobs.

**STOP for distinct joined review.** Survey-scale qualification only after
independent integrated acceptance.
