# EE-P2R6U — governed return

## Disposition

PASS.

`EE_P2R6U_PASS__EXACT_ADOPTED_R6A_RUNTIME_SUBSTRATE_MATERIALIZED_AND_R6S_LITS_RUNTIME_REQUALIFIED__READY_FOR_HQ_SELECTIVE_FANIN`

## Authority

Live HQ remained sealed at checkpoint `20260919T0330-0400`, immutable handoff `9540aba11d40fc749ffa59827e871c1ba00e7ec6`, under `HQD-2026-09-19-081` / `082`.

Branch: `agent/rabochii-prev3-ee-p2r6u-r6a-runtime-substrate-fanin-r1`

Commissioned head: `3a381d0f50d6c54ddf0ccea8c39c3f4299e9246d`

Exact materialization commit: `84bd90b292469b835664efdf47ff2300b2083607`

P2X remained held at `ae8b1db9d8c3288e002950ac01123c70f3138320`; this worker did not move it.

## Conflict audit

The five query/discovery files present on the held P2X-derived tree were proven byte-for-byte equal to the exact **pre-R6A** blobs at R6A base `6586da01…`, not later supersessions. The three runtime modules and five R4A fixtures were absent. The P2X post-merge delta touched R6S/P2X support, receipts, and backend files, not any of the 13 commissioned substrate paths.

No later incompatible adopted runtime authority was found.

## Exact adopted substrate

All 13 commissioned R6A blobs are now materialized exactly. The authoritative list and Git blob identities are sealed in `01_RUNTIME_SUBSTRATE_AUDIT.json`.

Production runtime includes:

- runtime-aware query/discovery stack: 5 exact adopted blobs;
- `pre553_runtime_authority.py`: `2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`;
- `pre553_runtime_composition.py`: `3753c183ddb25b1b0eb0ce84db1868f39f50d3fa`;
- `pre553_runtime_context.py`: `3c26c77892395a4825b377b740e37df7ea1148d4`;
- all five exact R4A authority fixtures.

## R6S LiTS requalification

The proof is content-addressed against the already governed Browser execution, not a surrogate rerun.

R6S governed execution head `e44d6abb115b9d4274127ae8eeb61ff9af4c2a73` contains the **same 13 Git blobs** now present on R6U and the same LiTS support module blob `9406bacfd928393f6a159a46216aa1f7ec129f34`.

Its authoritative Browser court:

- run `35422824788`;
- job `105843490615`;
- **12 passed** plus protocol **20 passed**;
- artifact `10578125850`, digest `sha256:7063aeac0dfb1cfa22df071fcc3c992061013ebad98850cfb78bcd8708b59bcb`.

That executed test imports the exact R6S support module, calls `materialize_runtime_package()`, and proves exactly:

- catalog `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`;
- active binding `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`;
- runtime release `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`;
- **50 candidates / 77 query-role executions**.

The same executed path constructs `r4_runtime()` and passes it through `bind_runtime`, whose production gate requires an exact `Pre553RuntimeAuthoritySet`. `materialize_runtime_authority_set()` is exactly `return r4_runtime()`. Mixed R4A composition is exercised and asserted against authority `0d7cfaac…`.

Legacy/no-runtime-context behavior remains the exact adopted R6A behavior: governed R6A Browser run `35391614229` / job `105751024028` passed **63 tests**, including the explicit unchanged legacy same-grammar composition and response-leaf evaluator tests.

PR #417 also checked out the exact R6U materialization and passed the protocol self-tests (**20/20**). Its bounded court was intentionally skipped because this commission does not authorize writing a root `.rabochii/court_spec.json`; no semantic PASS is attributed to that skipped step.

## Boundaries

No Library access. No LiTS or WVS carrier/source bytes. No empirical outcomes. No performance measurements or surrogate metrics. No candidate redesign. No P2X movement.

Exact receipts:

- `WORKER_RETURNS/EE-P2R6U/01_RUNTIME_SUBSTRATE_AUDIT.json`
- `WORKER_RETURNS/EE-P2R6U/02_R6S_LITS_RUNTIME_REQUALIFICATION_RECEIPT.json`

Wake exactly: **HQ selective fan-in of the qualified R6A runtime substrate to the held P2X lineage; HQ adjudication only.**
