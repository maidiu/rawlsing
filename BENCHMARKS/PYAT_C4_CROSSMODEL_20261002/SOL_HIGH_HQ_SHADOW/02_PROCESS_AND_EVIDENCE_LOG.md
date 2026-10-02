# Sol High HQ process and evidence log

This is a reproducible process record, not private chain-of-thought. It records the sequence of evidence gathering, checks, intermediate issues, and adjudicative decisions actually used.

## 1. Live-state reconciliation

Resolved three live refs before trusting the returned summary:

- control `integration/pre-main-reconciliation-r1` → `8fdfc1b05f187a6fa785b5987f0345debebfd803`
- Sol final-review branch → `fe6103cd50c634b92233f49815cc6d4abe49964d`
- C4 fan-in branch → `8ff40d37de69db2d8a6053a7c2242f481677f1a4`

Finding: the control branch had advanced from HQ180 to HQ181, so the HQ first checked whether that movement had already adopted the Sol result.

## 2. HQ181 benchmark-state audit

Compared prior HQ180 control state against HQ181. HQ181 had:
- recorded the Sol return as present but explicitly unadjudicated;
- bound an ALT-B Space Bunny reviewer lane;
- declared parallel blind cross-model comparison;
- kept source access and live execution held.

Finding: HQ181 was benchmark orchestration, not C4 adoption. Therefore a Sol shadow HQ adjudication remained lawful and uncontaminated at that stage.

## 3. Sol return hygiene

Compared `42f54d6345ed31669f8c37d7dc23b8e042968986...fe6103cd50c634b92233f49815cc6d4abe49964d`.

Observed exactly one return commit and exactly the eight commissioned return files:
- 00_REVIEW.md
- 01_COMMIT_GRAPH_AND_BLOB_REVIEW.json
- 02_O1_C01_C05_REVIEW.json
- 03_ORACLE_D02_RUNTIME_REVIEW.json
- 04_ACCOUNTING_RETENTION_CLAIM_REVIEW.json
- 05_WARRANT_CANDIDATE_REVIEW.json
- 06_OPEN_ITEMS_AND_RESIDUALS.json
- 07_FINAL_DISPOSITION.json

No production changes.

## 4. Read the full Sol return

The reviewer disposition was `APPROVE_AT_DECLARED_GRAIN`.

Material reviewer correction discovered:
C4C3's claimed 21-module "actual C4 path" starts below the M01 producer. Once the confirmed Route-B producer and carrier are included, the producer-inclusive static repository closure is at least 23 modules.

HQ treated that as the highest-risk review finding and did not accept the PASS until independently determining whether the omitted modules introduced a new runtime/platform gate.

## 5. Fan-in graph and tree reconstruction

Independently checked:
- commissioned fan-in tip `01256977...`
- merge `39015a90...`
- import commit `f8c8e2e4...`
- final `8ff40d37...`
- C4C3 side `1df64cc5...`
- C4A `8f7efe690...`

GitHub comparison reports five total reachable commits after the commission tip.

Adjudication:
- three are first-parent fan-in commits;
- two are the C4C3 side commits made reachable by the merge;
- therefore the worker's "3 commits on commissioned tip" and GitHub's "5 ahead" are compatible counting conventions, not hidden work.

## 6. Production-tree conservation

Fetched the Git tree at C4A and at final fan-in.

`rawlsing_next` subtree SHA at both:
`b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0`

Finding: zero production-tree movement from C4A through final fan-in.

## 7. Direct blob verification

Re-fetched and compared the expected Git blob identities for:
- five C1 owner modules;
- six accepted C3 code/test blobs;
- source-backed C11 facade;
- named positioned-subject consumer;
- Route-B producer.

All exact.

Also re-resolved the retained historical D02 fixture at `3bc063aa...`; blob exactly:
`12f6adb77ef5692511055c8f0520e42c454f3867`.

## 8. Route-B ownership adjudication

Inspected:
- `rawlsing_next/pre553_route_b_production.py`
- `rawlsing_next/pre553_carrier_execution.py`
- HQ decision ledger.

The producer blob is:
`2385cd327dced3c5b887b59085aa0d21b04d78c3`

It declares:
`PYAT_M01_ROUTE_B_PRODUCTION_COMPOSITOR@1.0.0`

and exposes:
`execute_route_b_production`.

HQD-2026-09-27-118 explicitly integrated the M01 selected-B execution compositor.

Finding: the fan-in producer binding is the current adopted M01 production/compositor owner, not an incidental module.

## 9. Reviewer 21→23 closure correction adjudication

Inspected C4C3's `02_ACTUAL_C4_CALL_PATH.json`. Its 21-module closure begins at:
decoder → facade → provider → analytical composition → named consumer.

It did not begin at the current M01 Route-B producer.

HQ then compared the exact blobs at the original qualified M01 candidate `46f3bec824c1c9da7037bacf94ec08923bc33506` against the C4 freeze:
- producer: exact
- producer tests: exact
- carrier: exact
- carrier tests: exact

The M01 return records a governed 61/61 source-free bounded court, including 11 compositor tests.

Static import inspection of producer/carrier found no new:
- `ee_p2x_*` edge;
- DuckDB edge;
- subprocess edge;
- dynamic-loader/importlib execution edge.

Adjudication:
the 21-module wording is incomplete and must be corrected, but absence of a Darwin-specific M01 rerun is nonblocking at the declared source-free freeze grain because the added pure-Python composition modules are exact already-qualified blobs and introduce no new platform-sensitive runtime gate.

Claim ceiling required by HQ:
"The exact frozen source-free implementation is accepted at the declared grain, supported by existing M01 source-free qualification and Darwin-qualified downstream C4 runtime evidence; no claim is made that the complete producer-inclusive M01 path was freshly rerun on Darwin."

## 10. Warrant candidate independent digest

Fetched exact GitHub bytes of:
`WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json`

HQ independently SHA-256 hashed those bytes.

Computed:
`d57420f8016bf49cc0353f39dcd2271e6f370c3bd9b7e81f08466c0a1f574e0a`

Expected:
same.

Verified:
- candidate-only status;
- signed=false;
- authorizes_access=false;
- issued=false;
- execution_authorized=false;
- seven fresh-source slots;
- SRC35 excluded from fresh authorization;
- all seven access locators unfilled;
- approvals unset.

## 11. Omega-1 / C4B / D2P / C4C3 cross-check

Read exact governing artifacts by commit identity, including objects not ancestral to the review branch.

Checked:
- eight-source set and SHAs;
- one fresh full Route-B source (SRC27);
- six bounded physical-only sources;
- retained-only SRC35;
- D01 metadata-only scope;
- D02 v372@466 retained witness;
- LiTS retained object counts;
- D2P B001/B002/B003 closure;
- C4C3 environment, reader defaults and six-file 55-test authoritative court;
- all-35 arithmetic and claim ceilings.

No semantic widening found.

## 12. D2P claim ceiling

Preserved as explicit limits, not silently upgraded:
- 3.4 GB checkpoint body absent on StarriyMac;
- checkpoint SHA not independently recomputed there;
- 120 giant deferred-member digests not independently recomputed there;
- extraction not byte-replayed there;
- checkpoint_identity and canonical_closure_identity remain recorded-but-not-independently-verified labels.

Finding: nonblocking only at the declared retained-custody/source-free freeze grain.

## 13. Accounting and residuals

Confirmed:
- zero retry is a lawful stricter budget, not an expansion;
- a corrected rerun requires new HQ-bound authority;
- 35 sources / 8 selected / 27 excluded / 280 F1-F8 cells;
- all nine claim ceilings preserved;
- C2-EPCLASS-PAYLOAD-001 carried;
- fresh-process provider→consumer→lifecycle bridge limitation carried;
- C7 comparable-wave gate remains held.

## 14. Shadow disposition fixed

HQ concluded:
`APPROVE_C4_EXECUTABLE_FREEZE_AT_DECLARED_SOURCE_FREE_GRAIN__REVIEWER_RUNTIME_WORDING_CORRECTION_ADOPTED__O1_C06_REMAINS_UNISSUED`

No permanent action was taken.

## 15. Post-adjudication contamination event

After the substantive Sol HQ disposition had already been fixed, HQ performed one final branch-status check.

At that moment, the ALT-B Space Bunny reviewer branch had advanced and GitHub exposed its commit-message summary.

HQ did NOT:
- fetch the ALT-B return packet;
- read its eight review files;
- change the Sol shadow disposition;
- import novel ALT-B residuals into the Sol result.

This is recorded so Astra can score benchmark blindness accurately.
