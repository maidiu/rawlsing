# PYAT HQ284 L01 — Source-free runtime qualification (SECONDARY Mac)

**TERMINAL:** `PYAT_R3_HQ284_L01_SOURCEFREE_RUNTIME_QUALIFICATION_COMPLETE__GITHUB_PUSHED`
**Role:** independent local runtime evidence collector, **NOT** HQ. **No provider/model/cost identity invented** — the harness configured the session; no cost or model claim is made here.
**Branch:** `agent/rabochii-pyat-r3-hq284-l01-sourcefree-runtime-qualification-r1` @ `0e8de4daf5bd27c7c7d8dc0223551fe2451e9ec2`
**Environment:** macOS 13.7.8 x86_64 · Python 3.11.3 · pytest 9.1.1 · isolated sparse worktree `/…/Rawlsing_Worktrees/hq284l01` on the shared object store. **No clone, no reset, no merge, no frozen-oracle modification.**

## 1. Results matrix — actual commands, totals, exits

| WS | candidate | suite run | total | passed | failed | errors | skipped | exit |
|---|---|---|---|---|---|---|---|---|
| **A** | S00C `54f14553` | `test_r3_s02_seam_witness.py` | 27 | **26** | **1** | 0 | 0 | 1 |
| **B** | complete P01/S05J `73d45f3a` | `…v2_durable_consumer_integration_candidate.py` | 25 | **25** | 0 | 0 | 0 | 0 |
| **B** | complete tree, 5-suite aggregate | verifier + governed batch + durable + mutation hostiles + integration | 175 | 83 | 86 | 0 | 6 | 1 |
| **C** | S03 `69a16865` + S03R `34cc7bdb` | `test_hq283_s03r_f6_method_hostile.py` | 11 | 0 | 0 | **11** | 0 | 1 |
| **D** | S04 `9ae87f22` | `test_s04_temporal_policy.py` | 17 | **17** | 0 | 0 | 0 | 0 |

## 2. Per-workstream findings

### A — S00C `54f145538ed0880f8257368f838baa5b0e12e2d3`
`test_r3_s02_seam_witness.py` → **26 passed, 1 failed** (14.85 s). The single failure is
`test_s00_contract_manifest_exists_and_is_valid` → `FileNotFoundError: WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/s00_target_contract.json`.
**That is a missing sibling return-tree artifact, not a code defect** — a checkout-scope limitation of materialising only `rawlsing_next/`. Recorded as **terrain**, not as a candidate failure. The other 26, including the repaired consumer, P04 regression and numeric value-use tests, **pass**.

### B — complete composed tree `73d45f3ac6a50fbee6666ad3a5023840f01ef196`
I used the **complete composed tree**, never the incomplete sibling — and verified it *is* complete: it carries **seven** candidate suites (`…v2_verifier_candidate`, `…contract_v2_candidate`, `…binder_candidate`, `…governed_batch_checkpoint_integration_candidate`, `…batch_durable_checkpoint_candidate`, `…v2_mutation_hostiles_candidate`, `…v2_durable_consumer_integration_candidate`).

**The integrated composition suite passes 25/25** — this independently re-confirms my S05J result on the full lineage.

The **5-suite aggregate is 86 failed / 83 passed / 6 skipped**, and I do **not** report that as a candidate result. The mechanism is proven by A's identical failure signature: these suites read `WORKER_RETURNS/…` fixture artifacts from their own lineages, and I materialised only `rawlsing_next/`. **Graded NOT GRADED (terrain)**, neither PASS nor defect. Closing it requires materialising the full `73d45f3a` `WORKER_RETURNS/` tree.

**S05JR `8df031cad5e6bdb9eb4032839c406fefb879a308` adds no Python** — its six documents (`00`–`05`, incl. `03_HOSTILES_AND_EXECUTION.md`, `05_FINAL_HOSTILE_EXPANSION_AND_HANDOFF_R2.md`) are **documentary** hostiles/telemetry, not a runnable oracle. There is therefore no S05JR Python file to execute; I executed the complete tree instead and say so rather than implying a reviewer suite was run.

### C — S03 `69a1686528bb46c2db3051a75710989a46fe5c45` + S03R `34cc7bdb28664ecbc707528470c2b4397aa96f12`
11 cases, **11 errors** — and the error is **by design**:
```
RuntimeError: HOLD: S03_CANDIDATE_ROOT absent; no project runtime executed
  rawlsing_next/tests/test_hq283_s03r_f6_method_hostile.py:38
```
The frozen review test **self-guards**: it requires the S03 candidate tree at an explicit root and **refuses to run** rather than fabricate a result. This is **`HOLD_BY_DESIGN`**, exactly the "expected-red scientific hostiles" and "exact candidate hash checks" the commission told me to preserve. I did **not** modify it, point it at a substitute tree, or weaken the guard. To execute it, the S03 candidate must be checked out at the path the test expects.

### D — S04 `9ae87f2227384e0567190c6a2d5f3a33a60d4b4c`
`test_s04_temporal_policy.py` → **17 passed**, exit 0. **No `xfail`/`xpass` observed in this run**, so the commission's warning ("do not mistake expected xfails for scientific acceptance") does not arise here — but I note explicitly that **17 passing tests are a technical result, not scientific acceptance**, and no temporal/scientific claim is made. S04R `755fb501` adds **`00_RETURN.md` + `01_REVIEW_FINDINGS.json` only — no Python tests**, so there is no S04R reviewer suite to execute.

## 3. Honest grading

| workstream | technical result | grading |
|---|---|---|
| A | 26/27 pass, 1 terrain failure | **QUALIFIED (source-free)** with 1 documented terrain gap |
| B | integration **25/25** on the complete tree | **QUALIFIED (source-free)** for the composed route; sibling suites **NOT GRADED (terrain)** |
| C | 11/11 self-HOLD by design | **HOLD_BY_DESIGN** — preserved, not a failure |
| D | 17/17 pass | **QUALIFIED (technical only)**; **no scientific acceptance implied** |

**No original survey data was read. No production or frozen oracle was edited. No protected CURRENT was touched. No provider/model/cost identity was invented.**

## 4. Exact checked-out SHAs and provenance

Candidate trees materialised sequentially from the shared object store by exact SHA: A `54f145538ed0880f8257368f838baa5b0e12e2d3`; B `73d45f3ac6a50fbee6666ad3a5023840f01ef196`; C `69a1686528bb46c2db3051a75710989a46fe5c45` + test `34cc7bdb28664ecbc707528470c2b4397aa96f12`; D `9ae87f2227384e0567190c6a2d5f3a33a60d4b4c`. Review commits fully resolved: S05JR `8df031cad5e6bdb9eb4032839c406fefb879a308`, S04R `755fb501e4b6405136bd77d71d434919c7b6c371`.

**Terminal:** `PYAT_R3_HQ284_L01_SOURCEFREE_RUNTIME_QUALIFICATION_COMPLETE__GITHUB_PUSHED`.
