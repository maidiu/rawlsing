# PYAT #997 — test-harness patch R2

## Status

**`TEST_PATCH_READY_75_OF_75__FRESH_PROCESS_Q2_PROOF_PASS__NOT_ADOPTED__NOT_G5`**

- Candidate: `2c476e739a263dd0069b54706c6cfa63b07190c1`
- Product parent: `534fb6602cce60fd991abd7972ebd95c92f3146c`
- Branch at authoring: `agent/pyat997-native-proof-r1`
- Startup SHA: `229544e23435f608272c2bead78cc5c2cfc786f5`
- Canonical product/test edits: **NONE**
- Patch artifact: `proposed.patch`
- Patch SHA-256:
  `e79990e0c650924ab989a5cdc1b0777d1314032281ebcec0148261783cf4ca35`
- Adoption: **NOT ADOPTED**; Browser owner must review/apply.

## Exact result

| Run | Result |
|---|---|
| Original six-suite baseline | **75 tests, 68 pass, 7 fail, 0 errors, 0 skipped** |
| Patched six-suite | **75 tests, 75 pass, 0 fail, 0 errors, 0 skipped, 42.753s** |
| R5 frontier/census focused | **5 passed, 15 deselected in 8.15s** |
| Patch apply check | **PASS** against isolated canonical-copy tree |
| Product Python hashes | **182/182 unchanged; canonical diff empty** |

Evidence:

- `evidence/baseline_68_of_75.txt` + baseline JUnit
- `evidence/six_suite_75_pass.txt` + JUnit
- `evidence/node_outcomes.json`
- `evidence/r5_5_pass.txt`
- `evidence/product_hash_compare.json`
- `evidence/apply_check.txt`

### All seven baseline failures now pass

The baseline JUnit contains exactly the seven previously observed nodes.
The patched JUnit contains the same 75 nodes with zero failures. Node-level
mapping is `evidence/node_outcomes.json`.

## What changed, and why it is not weakening

Only copies of the three candidate test files were changed. No product file,
issuer, CURRENT, source, S2-C/D implementation, or canonical test was modified.

### 1. Exact restore: preserve source bytes

- **Causes:** independently regenerated SAV/DTA fixtures carry a new file
  timestamp and therefore a different source SHA-256 despite equal values.
- **Patch:** reuse the exact baseline fixture/source for restored builds.
  Changed source remains separately generated. Root, source SHA, native fact,
  cell values and postconsumer receipt refs are still compared exactly.
- **Proof:** `evidence/delayed_fixture_probe.txt` shows equal values generated
  1.2s apart have different SHA-256; the patched restore reuses the baseline
  bytes and passes exact root/fact/join equality.
- No normalization or identity hash substitution.

### 2. Intended q101 I03 query

- **Cause:** the old helper returned the first fact from the first supported
  lowering record. That is a country-coordinate query with
  `RISK_SET_UNAVAILABLE`, not the causal q101 response query.
- **Patch:** select the exact compiled query whose target is
  `QUESTION_NATIVE ...:q101`; assert `SUPPORTED`, denominator `5`, cell total
  `5`, and expected cell movement. Keep the country-coordinate query as a
  separate `UNAVAILABLE / RISK_SET_UNAVAILABLE / denominator 0` negative witness.
- **Test data correction:** the source-bridge changed/restore test now uses
  values in the compiled q101 target domain `0/1`; it still changes an actual
  source response cell and produces a different native fact. This is a test
  fixture-domain correction, not a product semantic change.
- **Not a scan-for-any-green:** the selection is by exact compiled q101 target.

### 3. Stale refusal expectations

- `HELD -> ELIGIBLE` promotion now asserts the actual earlier guard
  `Q2_ORIGINAL_FROZEN_FATE_CENSUS_DRIFT`.
- `unresolved_routing` now asserts
  `Q2_REALIZATION_ROUTING_CENSUS_DRIFT`.
- Both assert the runner has **zero receipts** after refusal; no positive
  attribution or protected native execution occurred.
- No alternation, generic `Exception`, skip, or xfail.

## Fresh-process Q2 proof

The previous `native_proof_harness.py` used only a `git rev-parse` subprocess;
that did **not** establish producer-exit -> fresh-consumer-process cold reading.
The existing repository fresh-process tests use the S2C direct-estate fixture,
not the Q2 source-produced estate. This return supplies the missing Q2 proof.

`fresh_process_producer.py` (separate interpreter):

```text
TEST_ONLY generated SAV
  -> Q2 SourceI02Handoff + SourceSavedBodySink
  -> S2-C persisted 13-family estate
  -> actual I03/I05/Batch oracle
  -> write capsule, exit
```

`fresh_process_consumer.py` (new interpreter after producer exit):

```text
capsule root/estate roots/release + existing TEST_ONLY catalog
  -> SavedC11Admission.open
  -> actual execute_saved_i03 / execute_saved_i05 / execute_saved_batch
```

Observed:

- producer return code `0` before consumer start: **true**
- source file deleted before consumer: **true**
- consumer source opens: **0**
- consumer full C11 repository builds: **0**
- I03 fact refs equal: **true**
- I05 receipt refs equal: **true**
- Batch states/count equal: **true**
- Batch shape: **1 issued DISCOVERY unit, 0 issued QUERY units**

Evidence: `evidence/fresh_process_proof.json`,
`evidence/fresh_process_run.txt`.

## Remaining precise obligation

The real frozen issued workload has **0 query requests and 1 discovery unit**.
The q101 query is a real compiled supported I03 query, but it is not an issued
Batch query. This test patch does not mint or alter issuance to make a Batch
QUERY unit appear.

If original #997 requires a Batch QUERY positive, Browser/issuer owner must
provide a legitimately issued query unit or state the narrower accepted scope.
This is the remaining `BATCH_QUERY_UNIT_NOT_ISSUED` obligation, not a test
failure and not a product edit made here.

## Adoption request

Browser #997 owner can apply:

```bash
patch -p1 < WORKER_RETURNS/PYAT997_NATIVE_FIRST_CONSUMER_PROOF_R1/test_patch_r2/proposed.patch
```

Expected patched blobs:

- `148c7c29d8c407ee831f379d95c898018d049977`
  `test_pyat997_s1e_saved_native_first_consumer.py`
- `c3077ce89c05d6e39349c08468ce4022a3a6f506`
  `test_pyat997_s1e_saved_source_bridge.py`
- `3ca7396a50312b7b8daf2d29e4119aba71d63db9`
  `test_pyat997_s1e_source_saved_body_bridge.py`

Then rerun the same six suites and R5 group, and separately adjudicate the
zero-issued-query Batch shape.

## Engineering / scientific / authority

- Engineering: test-only patch + actual 75/75 + Q2 fresh-process proof.
- Scientific: no original35 source/measurement/science acceptance.
- Authority: TEST_ONLY sourcefree only; no production CURRENT, issuer, source
  permission, host grant, protected merge or 1002 authority.
- #1006 benchmark: not run.
- G5: not run; this is not independent acceptance.

## Self-critique

- The patch changes test fixture baseline values in the source-bridge q101 test
  to match the compiled target domain; that is a test fixture correction and is
  called out explicitly.
- The test suite is green while the issued Batch shape still has no query unit.
  That distinction is not hidden.
- The fresh-process proof is small TEST_ONLY evidence, not a resource or
  scientific acceptance.
- No product or canonical test file was modified; adoption remains the
  Browser owner's decision.
