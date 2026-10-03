# PYAT HQ196 — R9 broker + selected-read hostile review — R1

Repository: `maidiu/rawlsing`

Role: **HOSTILE INDEPENDENT SOURCE-FREE REVIEWER**

Preferred model: **DeepSeek V4.1 Flash**

Branch:
`agent/reviewer-pyat-hq196-r9-broker-selected-hostile-review-r1`

Documentary base:
`d43756fb3c80645ac887cca90026ecbdb10dd18c`

Checkout mode:
`SPARSE_REQUIRED`

Sparse materialization manifest:
- `/WORKER_COMMISSIONS/PYAT-HQ196-R9-BROKER-SELECTED-HOSTILE-REVIEW-R1/`
- `/WORKER_RETURNS/PYAT-HQ196-R9-BROKER-SELECTED-HOSTILE-REVIEW-R1/`
- `/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ196_R9_THREE_WAY_ADJUDICATION_R1.md`

The exact startup SHA is supplied by HQ after this commission commit.

Do not clone the repository.
Do not materialize a full worktree.
Read historical code/evidence with exact Git-object commands.

## Independence

Do not inspect the parallel HQ196 implementation branch or its return before forming your own conclusions.

You MAY inspect:
- HQ195 runtime feasibility `63f10827e673a4b3c53a0a123303b2b9bb96c59a`;
- HQ195 stage return `66929dad727410b8bfd33831cd2d8c632d5ccf4a`;
- HQ195 contract review `6df3257c5e362947c988d3260302cef2372e0809`;
- exact C4 freeze `8ff40d37de69db2d8a6053a7c2242f481677f1a4`.

## Mission

Hostile-review two claims:

### A. Broker feasibility

Attack the claim that pyreadstat 1.3.6's existing file-like-object route permits literal O1-C07 path-open accounting without rebuild or privilege.

Independently inspect the installed/source package behavior and reproduce with synthetic carriers.

Establish or falsify:
- a caller-supplied object with `.read/.seek` actually causes pyreadstat/ReadStat to use the Python bridge;
- the parser receives no usable source path / no compiled path-open requirement on that route;
- the application-owned file open is therefore the complete source-path open at that route;
- read count and byte accounting occur at the actual I/O owner;
- excess read/byte operations can fail before the excess operation executes;
- loud failure is returned, not truncated/partial success;
- the accepted pyreadstat binary/package identity is unchanged;
- the seam is version-sensitive/private and must be pinned.

Attack D1:
- DTA chunk/batch reading;
- reused broker versus fresh broker/reset semantics;
- whether a safe design can preserve one governed path-open budget while satisfying the reader's position/reset requirements.

Do not infer zero compiled opens merely from inability to observe them. Tie the conclusion to source/control-flow evidence plus synthetic behavior.

### B. Selected-read implementation gap

Read exact freeze law:
`8ff40d37...:WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.json`

and exact freeze decoder:
`8ff40d37...:rawlsing_next/pre553_physical_decoder.py`

Attack HQ196's finding that:
- SRC02/SRC06/SRC14 require `expected_selected_reads=1`, `expected_full_reads=0`;
- the executable decoder contains no `usecols`;
- `PhysicalSourceIncidence.iter_batches` calls `read_file_in_chunks` without selected-column configuration;
- therefore the frozen executable route appears to perform a full-column read rather than the authorised selected-variable read.

Determine:
1. whether any other call/consumer layer supplies an equivalent selected-column restriction;
2. whether pyreadstat's relevant reader/chunk route supports a `usecols`-style restriction;
3. whether selected-read count is truly owner-missing, or whether the implementation is missing the selected-read operation itself;
4. whether this is a material pre-live implementation gap.

## Contract ceiling

The HQ195 independent review's contract interpretation is adopted for this review:
- literal path-open account cannot be relabelled;
- expected budgets/instrumentation are pre-launch;
- observed exact counts are runtime/return evidence.

Do not reopen that meaning absent a concrete contradiction.

## Source-free only

Synthetic SAV/DTA permitted.
R7 qualification environment may be used read-only.
Zero real survey/source access.

## Allowed dispositions

Exactly one:
- `BROKER_ROUTE_CONFIRMED__SELECTED_READ_IMPLEMENTATION_GAP_CONFIRMED`
- `BROKER_ROUTE_CONFIRMED__SELECTED_READ_GAP_NOT_ESTABLISHED`
- `BROKER_ROUTE_MATERIAL_COUNTEREXAMPLE__DO_NOT_IMPLEMENT`
- `MATERIAL_CONTRACT_OR_RUNTIME_UNRESOLVED`

## Return packet

- `00_REVIEW.md`
- `01_BROKER_SEAM_SOURCE_CONTROL_FLOW.json`
- `02_SYNTHETIC_BROKER_REPRODUCTION.json`
- `03_DTA_CHUNK_RESET_REVIEW.json`
- `04_SELECTED_READ_CALL_PATH_REVIEW.json`
- `05_R7_IDENTITY_AND_REQUALIFICATION_EFFECT.json`
- `06_FINAL_DISPOSITION.json`

## Return law

Commit, push, re-fetch, verify remote == local.
Artifacts bind substantive review SHA; report pushed tip separately.

Terminal:
`HQ196_R9_BROKER_SELECTED_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

## Holds

Zero locator discovery, real-source access, warrant issuance, live C4, production mutation, C7 or actor/person work.
