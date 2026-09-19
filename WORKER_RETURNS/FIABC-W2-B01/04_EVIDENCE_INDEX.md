# FIABC-W2-B01 — Evidence Index

All conclusions in this return distinguish **accepted/canonical authority**, **current implementation**, **worker qualification/claim**, and **governed live execution evidence**. Static call-path reachability is never promoted to a live receipt.

## A. Commission and Wave-1 authority

| Evidence class | Exact ref | Path / object | Use in this return |
|---|---|---|---|
| Canonical Wave-1 fan-in authority | `agent/vozhd-premain-fiabc-wave1-fanin-r1` at `dfdae1dfcef5e3061094935312c3db2cc0fde2f0` | `WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/00_RETURN.md` | Governing succession model and Wave-1 terminal. |
| Canonical Wave-1 succession ledger | same ref | `WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/02_MASTER_SUCCESSION_LEDGER.csv` | F010/F032/F033 live-disconnection baseline and current PRE553 owner relations. |
| Canonical contradiction map | same ref | `WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/03_CROSSWORKER_CONTRADICTION_MAP.md` | `CURRENT_IMPLEMENTATION_EXISTS != LIVE_EXECUTABLE_CONSUMPTION`. |
| Canonical invariant draft | same ref | `WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/04_ABC_INVARIANT_MANIFEST_DRAFT.csv` | INV009–INV018 baseline. |
| Canonical open-cell ledger | same ref | `WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/05_OPEN_CELL_LEDGER.csv` | OC05 exact post-repair consumption question; OC07 parity-oracle gap. |
| Commission authority | same ref | `WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/06_WAVE2_COMMISSION_MATRIX.md` | Exact FIABC-W2-B01 branch, return path, burden, outputs, and PASS terminal. |

## B. Current P2X identity and fan-in

| Evidence class | Exact ref | Path / object | Fact proved |
|---|---|---|---|
| Current branch identity | `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1` | Git ref | Audited current tip is `617c9c9426db12a3c0f7fea6b68a582c10759553`. |
| Current fan-in commit | `617c9c9426db12a3c0f7fea6b68a582c10759553` | Git commit | Parent is held pre-repair P2X `ae8b1db9d8c3288e002950ac01123c70f3138320`; message: `EE-P2X: fan in adopted R6U R6V R6W runtime and reconciliation repairs`. |
| Fan-in delta | compare `ae8b1db9...` → `617c9c9...` | Git compare | Runtime substrate, WVS materializer, driver/backend/binding, and R6X reconciler changed; no post-repair LOCAL_COURT PASS evidence was added by the fan-in commit. |

## C. Repair ownership

| Evidence class | Worker / exact branch ref | Path / exact product | Fact proved |
|---|---|---|---|
| Qualified repair worker return | R6U branch `agent/rabochii-prev3-ee-p2r6u-r6a-runtime-substrate-fanin-r1`, observed tip `85c1c00c4dfa0b63d029dc3d20ec865f4d3ed3e8` | `WORKER_RETURNS/EE-P2R6U/00_RETURN.md` | R6U owns exact adopted R6A runtime substrate fan-in and LiTS runtime requalification. |
| Machine-readable R6U audit | same branch | `WORKER_RETURNS/EE-P2R6U/01_RUNTIME_SUBSTRATE_AUDIT.json` | Exact 13 adopted target blobs; no later incompatible adopted runtime conflict. |
| Qualified repair worker return | R6V branch `agent/rabochii-prev3-ee-p2r6v-wvs-binder-recursion-repair-r1`, observed tip `75fcb21893919208423edadd24a2b43adf71c099` | `WORKER_RETURNS/EE-P2R6V/00_RETURN.md` | R6V owns WVS projection binder recursion repair; authority identities preserved. |
| Qualified repair worker return | R6W branch `agent/rabochii-prev3-ee-p2r6w-s17-orchestration-repair-r1`, observed tip `c7cb149a11795d6b9651a4303258534058fd027f` | `WORKER_RETURNS/EE-P2R6W/00_RETURN.md` | R6W owns S17 ordering and common-court failure normalization repair. |
| Qualified preparation worker return | R6X branch `agent/rabochii-prev3-ee-p2r6x-p2x-ledger-reconciliation-prep-r1`, observed tip `689995c798fece3c36d56905e4aaa67957ce8d79` | `WORKER_RETURNS/EE-P2R6X/00_RETURN.md` | R6X owns deterministic stopped-ledger reconciler preparation and explicitly states the real stopped ledger was not reconciled in Browser. |
| Qualified reconciler implementation | current P2X `617c9c9...` | `WORKER_RETURNS/EE-P2R6X/03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py`, blob `12836e591be9ed0aa4d46436deacebde038d9de0` | Tool is present; presence is not a reconciliation receipt. |

## D. Current static consumption implementation at `617c9c9...`

| Evidence class | Path | Exact blob / identity | Static fact proved |
|---|---|---|---|
| Current implementation | `rawlsing_next/ee_p2x_darwin_court_driver.py` | `02ca7cc9f5bf8665de712980a05fdcc059b93331` | Exact A/B/C owners are pinned; `DriverServices.compose_p2r1_binding()` constructs RuntimeObjectCatalog, exact projection, exact repository builder, common executor. |
| Current implementation | `rawlsing_next/ee_p2x_darwin_stage_backend.py` | `b223d309b5f5fa45389badec719ce2882e672cca` | LiTS/WVS projection/runtime preparation, source-specific A/B binding, `_i03`, `_i05`, typed C stops, and repaired court-scope serialization. |
| Current implementation | `rawlsing_next/pre553_carrier_execution.py` | `e7cda773e6a2426bfa12b22790fd8e005fe75153` | Carrier-neutral P2R1 C11→I03/I05 seam; exact projection/repository binding and learned-empirical receipt. |
| Current implementation | `rawlsing_next/pre553_runtime_authority.py` | `2ddc591f2572983d18f8f3e8f81a33b80b3bca7b` | Exact adopted successor runtime-authority registry. |
| Current implementation | `rawlsing_next/pre553_runtime_context.py` | `3c26c77892395a4825b377b740e37df7ea1148d4` | Exact opt-in `bind_runtime(Pre553RuntimeAuthoritySet)` context. |
| Current implementation | `rawlsing_next/pre553_empirical_query.py` | `482778348d6b450f46985c2161af32f2961d8384` | Current I03 executor includes exact runtime-authority fitness path. |
| Current implementation | `rawlsing_next/pre553_discovery_exact.py` | `c7380774e8a1959da5ed8c6f23c2fc3cf99ad18d` | Current exact-bounded I05 complete-frontier executor. |
| Current implementation / preserved authority package | `WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py` | `9406bacfd928393f6a159a46216aa1f7ec129f34` | Materializes LiTS runtime package and `Pre553RuntimeAuthoritySet`; 50 candidates / 77 query-role executions are identity checked by backend. |
| Current implementation / source-specific projection | `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py` | `11b28416aac5a4899706150721f2f8ac8bb6ee43` | R6V-repaired guarded exact WVS projection binder, no recursive self-call. |
| Current driver binding | `WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json` | `24311d54ca92a3255dcbbf05e7bc2b8d3ef19cb0` | Current packet binds repaired driver blob `02ca7cc9...` and finalization law. |

### Exact current identities used by the static graph

- LiTS projection: `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`
- LiTS runtime catalog: `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`
- LiTS active binding: `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`
- LiTS runtime release: `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`
- WVS projection: `838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d`
- WVS coordinate authority: `9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d`
- WVS Lock2 / tie-order: `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`
- WVS discovery authority: `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`
- Exact owner commit: `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
- Candidate-A owner blob: `d4915e7e6755ba1850756aebff72f982f73a332b`
- Candidate-B owner blob: `7c509c2098d0030f253344eb3f682471378812a8`
- Candidate-C owner blob: `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`

## E. Governed live execution evidence still present at current tip

These are **live/historical execution receipts**, not implementation descriptions. They prove what the last governed run actually consumed and where it stopped.

| Evidence class | Current P2X path at `617c9c9...` | Exact fact proved |
|---|---|---|
| Governed execution return | `WORKER_RETURNS/EE-P2X/00_RETURN.md` | Status remains `BLOCKED__CANDIDATE_RUNTIME_AND_FINAL_VERIFIER`; no final two-source measured PASS claimed. |
| Governed candidate-local failure | `WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/LITS_I__A__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json` | Pre-fan-in S02 `ModuleNotFoundError` for `pre553_runtime_authority`. |
| Governed candidate-local failure | `WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/LITS_I__B__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json` | Pre-fan-in S03 `ModuleNotFoundError` for `pre553_runtime_authority`. |
| Governed candidate-local failure | `WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/WVS7__A__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json` | Pre-R6V S01 `RecursionError`. |
| Governed candidate-local failure | `WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/WVS7__B__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json` | Pre-R6V S01 `RecursionError`. |
| Governed final-verifier receipt | `WORKER_RETURNS/EE-P2X/LOCAL_COURT/91_DRIVER_BOUND_FINAL_VERIFICATION_RECEIPT.json` | Old driver blob `c3a368270f6f7a6f613efb78e31972e64a092c88`, stopped ledger SHA-256 `7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671`, terminal RUNNING-S17 blocker. |

No one of these receipts proves live use of the current repaired runtime substrate, repaired WVS binder, repaired S17 ordering, or real R6X reconciliation.

## F. Wave-1 independent analyses retained as historical evidence

| Evidence class | Exact branch/path | Use |
|---|---|---|
| Wave-1 live-consumption analysis | `agent/rabochii-premain-fiabc-b02-p2x-live-consumption-graph-r1:WORKER_RETURNS/FIABC-B02/00_RETURN.md` | Establishes pre-Wave2 baseline: current repairs present but not post-fan-in live-consumed. |
| Wave-1 failure falsifier | `agent/rabochii-premain-fiabc-b05-p2x-succession-failure-falsifier-r1:WORKER_RETURNS/FIABC-B05/00_RETURN.md` | Distinguishes recurrent integration failures from genuine Candidate-C/missing-relation capability gaps. |

## G. Inferences made by FIABC-W2-B01

The following are **this worker's bounded inferences from the exact evidence above**, not accepted authority:

1. The four admitted A/B cells now have a continuous **static** call graph from source-specific runtime/projection material to P2R1, I03, and I05.
2. The prior LiTS missing-runtime-module and WVS recursive-binder defects have been removed from the current repository tree.
3. No post-repair governed live receipt proves those four cells traversed the repaired path.
4. Candidate-C remains outside the admitted common-runner set under current frozen behavior.
5. R6X reconciler presence does not prove the real stopped work root was reconciled.
6. S03 remains a self-replay parity check rather than an independently produced parity oracle; this is outside B01's repair authority and remains a separate Wave-2 court issue.
