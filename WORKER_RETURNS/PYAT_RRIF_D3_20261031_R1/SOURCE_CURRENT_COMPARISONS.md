# Source and current comparisons

**PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`
**RRIF-C:** `b75addf621c3a6c1a3b196bd92a810fad77ae3ae`
**RRIF-V:** `bec050449f0b38606718e4e9691caa1721fcd94f`
**A:** `84182f9fa7044d67689ea4f80eabf7e9337f15c2`
**B:** `59e6e62600814d82cfefd1a2137b7aa63316bc95`
**A×B:** `f5a9facd189af6756c2b15c8daebe680016f658a`
**E8:** `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`

## 1. Exact current source identity

| Path | Current blob | Lines | Current importer(s) |
|---|---|---:|---|
| `rawlsing_next/pre553_batch_runner.py` | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` | 690 | `pre553_issued_workload`, `pre553_native_workload_binding`; tests |
| `rawlsing_next/pre553_issued_workload.py` | `31e84f49d624f5524906e9e7839d2873106f8249` | 342 | `pre553_native_workload_binding`; no direct production consumer |
| `rawlsing_next/pre553_native_workload_binding.py` | `dac73e484f8619088f5c6701b2b6991c07540f3b` | 1,089 | `pre553_universal_workload`; tests |
| `rawlsing_next/pre553_universal_workload.py` | `8e7fe00a3ed008361d9f3c501e7782b2de3a636e` | 1,221 | tests only |
| `rawlsing_next/pre553_source_native_preimage_adapter.py` | `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c` | 916 | `pre553_native_workload_binding`, `pre553_universal_workload`; tests |
| `rawlsing_next/pre553_learned_world_composition.py` | `4a8e27a226a9c06606f5ba493d2cc7356d491a7b` | 1,426 | tests only |
| `rawlsing_next/pre553_learned_product_lifecycle.py` | `a11c9eb73abab9be118ef4f0b6e325e676059f27` | 2,882 | `pre553_learned_world_composition`; tests |
| `rawlsing_next/universal_grammar/native_map.py` | `3db04a006802276f131442f299009b1402cb42c9` | 2,816 | `pre553_native_workload_binding`, `pre553_universal_workload`; tests |
| `rawlsing_next/universal_grammar/enumerate.py` | `fd9203a0b272f98771c24070d01a9e5287c9b099` | 550 | tests |
| `rawlsing_next/universal_grammar/types.py` | `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` | 887 | `pre553_native_workload_binding`, `pre553_universal_workload`; tests |

Absent current paths: `pre553_production_binding.py`,
`pre553_source_read_admission.py`, `pre553_universal_evidence_binding.py`,
`pre553_universal_empirical_extension.py`, `s06_trusted_release_replay.py`,
`pre553_batch_durable_checkpoint_candidate.py`,
`pre553_governed_batch_checkpoint_integration_candidate.py`,
`pre553_v2_durable_consumer_integration_candidate.py`, and the three
`pre553_original_workload_*_candidate.py` files.

No production top-level importer reaches the R61 workload chain. The only
top-level importer of `pre553_universal_workload` is its test file. The only
top-level importer of `pre553_learned_world_composition` is its test file. This
is a test-only retained estate, not a production capability.

## 2. Candidate presence and exact blobs

| Lineage | Candidate path | Candidate cut/blob | Current status |
|---|---|---|---|
| HQ282 durable batch | `pre553_batch_durable_checkpoint_candidate.py` | `EF93F014` / `719c8d878bcfb3b6c61c844c9bf974ada8365929` (787 lines) | ABSENT |
| HQ282 durable batch | `pre553_governed_batch_checkpoint_integration_candidate.py` | `92CB2534` / `44807c6a287145507d7332138c944cd61da363bf` (617) | ABSENT |
| HQ282 durable batch | `pre553_v2_durable_consumer_integration_candidate.py` | `3F91DC22` / `dc146e920909c8577b5c3c316cd9a8631e96ffd8` (313) | ABSENT |
| HQ282 durable batch | `pre553_original_workload_binder_candidate.py` | `CBE047CF` / `7d8b3902c3f8f257637b7c07ad9feb5e096d48e5` (1,155) | ABSENT |
| HQ282 durable batch | `pre553_original_workload_contract_v2_candidate.py` | `56574BEC` / `08bb75c431d3352cb0d17e9a65f7d855b4d35e59` (1,151) | ABSENT |
| HQ282 durable batch | `pre553_original_workload_v2_verifier_candidate.py` | `C1DF9842` / `996c8e907f2befde93af09b60154b610c1ffeb63` (941) | ABSENT |
| R61 evidence binding | `pre553_universal_evidence_binding.py` | `FC4597FB` / `00312f84afa5677c94193cefd94cdfd951f05222` (2,714) | ABSENT |
| R61 evidence binding | `pre553_universal_empirical_extension.py` | all cuts | ABSENT |
| R61 evidence binding | `pre553_learned_world_composition.py` | all cuts / `4a8e27a226a9c06606f5ba493d2cc7356d491a7b` | exact current, but not the evidence-cache owner |
| R61 production binding | `pre553_production_binding.py` | `CCF97C89` / `ad5abfe7d71b76eb421f729c1b88e4ac56a59591` (439) | ABSENT |
| R61 production binding | `pre553_source_read_admission.py` | `CCF97C89` / `652ea3cdf0f53cd9ce14c4419486f6c1a81f3584` (216) | ABSENT |
| R61 grammar | `universal_grammar/native_map.py` | R7 reviewer `BFEBAEEF` / `fd3dc6138ade59a2f7b2ffd7a4514604e916d25f` | current later blob `3db04a00...`, R8-repaired |
| R61 workload | `pre553_universal_workload.py` | R03 candidate `61356022` / `8e780b2430b8a6a930f45329596cfdec2f1aa46c` | current `8e7fe00a...` |
| S06 replay | `s06_trusted_release_replay.py` | `4FEC074C` / `40b1009512aea909612a5fa01081ec3d0955860d` (314) | ABSENT |

The exact candidate/current blob table is machine-readable in
`test_receipts/candidate_blob_compare.json`.

## 3. The all35 question

The probe in `test_receipts/lineage_probe.json` establishes:

- `original35_roster(waves)` validates 35 caller-supplied wave dictionaries and
  refuses 34. It is an identity validator, not a request constructor.
- `reconcile_estate_workloads(waves, workloads, frontier)` requires
  caller-supplied workloads and an `IssuedEstateFrontier`.
- `compile_universal_workload(*, bundle: NativePreimageBundle, ...)` constructs
  operations for one bundle only.
- `original35_roster` and `reconcile_estate_workloads` have **zero callers**
  outside `pre553_issued_workload.py`.
- `compile_universal_workload` has exactly one caller: the test file.

**Finding:** general all35 request construction is **not implemented**. Current
code is an executor/admission layer for supplied requests plus a caller-supplied
35-identity validator. There is no current function that reads 35 source
manifests, constructs 35 request sets, and feeds them to the executor.

## 4. A/B/V/E8 custody reductions (not recounted)

RRIF-V is the governing correction; this lane did not rerun the whole estate.

- `845` frozen branch names / `838` distinct tips.
- `321` code-bearing branch rows; `276` stranded/diverged; `45` exact-present.
- `195/81` and `23/22` fate-category splits.
- A's `2,269` is **not** a current subtraction: `199` same-path exact, `291`
  exact-other-path (source-copy/fixture-related), `1,333` branch-only exact
  implementations, `62` modified non-code. `1,717` are branch-only exact;
  `866` implementation variants are current-modified.
- B is `155` branch rows / `122` unique primary decision IDs / `135` decision
  records / `151` fate-classified / `4` unclassified `HQ_OTHER` / `5` rows with
  `HQ_OTHER` class. A checkpoint is not code adoption.
- E8 is a mechanical inventory: `1,885` families, `3,135` IDs, `845` branches;
  its 602 HOLD / 243 RETIRE / 101 ALREADY_CURRENT statuses are inputs, not
  authentic dispositions. This lane does not use them as decisions.

The six lineages below were compared from exact source cuts, original reviews,
current code, tests and receiver/import evidence. No branch-only row is treated
as current integration because it is named `accepted` or appears in E8.
