# PUBLISH PINS — D3A (correction round)

**Branch:** `agent/anvil-d3a-rabochii-20261117-r1`  
**Immutable prior return:** `13db833601ed2124e64b3b764cc2647e48b3fa36` (unchanged; this commit is its descendant)  
**Correction commit:** `2e4aad9b4b4459587ee807eb1280f7ca97c09616`  
**Scope:** `WORKER_RETURNS/ANVIL_R7_FLEET/D3A/` only.

## Defect closure

| Case | Result |
|---|---|
| fake commit `a*40` (pre-fix) | **ACCEPTED — defect reproduced** |
| fake commit `a*40` | REFUSE (`ORIGIN_COMMIT_OUTSIDE_PINNED_CUTS`) |
| well-formed nonexistent commit | REFUSE |
| real but wrong commit (HEAD) | REFUSE (`ORIGIN_COMMIT_OUTSIDE_PINNED_CUTS`) |
| wrong path, same commit | REFUSE (`ORIGIN_PATH_NOT_IN_COMMIT`) |
| replacement bytes + recomputed self-hashes | REFUSE (`ORIGIN_PATH_BLOB_MISMATCH`) |
| fake ZIP sha256 | REFUSE (`ZIP_CONTAINER_SHA_MISMATCH`) |
| no external anchor | REFUSE (`NO_EXTERNAL_TRUST_ANCHOR`) |
| genuine inventory + real anchors | **PASS_ORIGINAL_CONTAINER_BYTES** |
| exact restoration | PASS |

## Anchors used

- Git object store: `/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/D3A` (read-only use of `git rev-parse` / `git cat-file`)
- Original archive: `/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip`, sha256 `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`
- Allowed commits: `31291d0…`, `596f1230…`, `796452b8…`, `3cc09bba…`

| File | sha256 |
|---|---|
| `GROK_PROOF.md` | `80fa7bd09e4d3662196c125cae3cbcc5097cc3c2060ff3fd1c2d2aea78531941` |
| `GROUNDING_RECEIPT.md` | `d8e77fa32bfbaff661f506a053ceeec77747bbd17dc8a4910f1e8dd0523af361` |
| `GATE_DESIGN.md` | `60652c3a64aa33fe9c0ecfae97de6c3ca4cc6978b2c4dbe127e33ce548da705e` |
| `COLD_BUILDER_OUTPUT_SPEC.md` | `9102157d4a31dd1c33c986e635081b4773738f2a0e2daba059aa90cc5e0f370b` |
| `ALTERNATIVE_AND_COUNTEREXAMPLE.md` | `61dbdc6f049fa39a119d56352d8a550954f7484a2a8a860710fae86b9b6b9219` |
| `RUN_RECEIPT.md` | `e43a23ccd2afb8cd3eb29a24616276947a0161a48eef1f6c24c114a2611b983f` |
| `GATES_CHANGESET.patch` | `71207bedb7a0069f83f1babb04f5cf9ebbd07ae452440202921ca6d4201ac1a9` |
| `TEST_TRANSCRIPT.json` | `8af4feabb499f4e9a935f3a6f5363be6bb397ac68cd48bf7cf6e9f1bfa683098` |
| `PACKAGE/tools/r7_integrated.py` | `a97d8f67b4b1dcf1e701e8160361595bccc5c8c58306146948ae83f607931e6f` |
| `PACKAGE/tools/r7_source_inventory.py` | `3ee12821dcec515e89d35b91c51898fd658fbeb3652d116637d23533e5eda03e` |
| `PACKAGE/tools/r7_builder.py` | `4b0603fa030bf0917701abe3b70a561142b3c2adc834a4355414237850773057` |
| `PACKAGE/tools/d3a_fixture.py` | `7d4d26a18121244631c757f507147f12f33abef4777997d0b84c7a36dc258bd3` |
| `PACKAGE/tools/test_r7_integrated_d3a.py` | `ea477c720cb7c79bbc55eae75716bf7b13e7d3ffdcb1fa6ee36e62309f719910` |
| `PACKAGE/tools/test_r7_integrated.py` | `b1df5a32ec8036662a5b596e59c984b130f219bd6d0b4b16752f48a352ed4a7c` |
| `PACKAGE/tools/r7_transfer_conservation.py` | `cb971052e7cb8668aaa7882f4a7db29a0f485a428c4a05f40b6f9f6f51e578bb` |
| `PACKAGE/D3A_INVENTORY_SAMPLE.json` | `4efdeb62a7fa8eb2dcbca6c4c7970efd0345c513846d8c7a470d119fc56a7ec5` |
| `PACKAGE/D3A_TERMINAL_ORIGINS.json` | `f4894765c4bc4aa7583ede660ee4c67ae009762d3574ba4c586af45f8a55e3bd` |

## Residual holds

- **F26 original body not found** at `31291d0`; probe 4 declares this gap and does not claim readiness on F26.
- Terminal-16 binding remains documentary-token grade.
- No native/100k run, no independent C, no science/actor/source right, no protected H1.
- Fleet-bank forensic audit used as challengeable allegation only; two bank manifest discrepancies respected.
