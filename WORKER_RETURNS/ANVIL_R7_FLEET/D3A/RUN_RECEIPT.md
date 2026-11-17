# RUN RECEIPT — what was actually executed, and what was not

All commands below were run in this worktree on 2026-11-17 (UTC). Full machine record: `TEST_TRANSCRIPT.json`.

## 1. Executed

| # | Command (cwd `PACKAGE/tools`) | Return | Meaning |
|---|---|---|---|
| 1 | `python3 r7_source_inventory.py verify ../D3A_INVENTORY_SAMPLE.json --source-root ..` | **0** | 118 rows, every origin byte-located; `PASS_LOCAL_SOURCE_BYTES_ONLY` |
| 2 | `python3 r7_source_inventory.py build --source-root .. --terminal-map ../D3A_TERMINAL_ORIGINS.json --out ../D3A_INVENTORY_SAMPLE.json` | **0** | deterministic re-build of the same 118 rows from exact bytes |
| 3 | `python3 -m unittest test_r7_integrated_d3a -v` | **0** | 24 new hostile tests (S1 / DECISION / C) |
| 4 | `python3 -m unittest test_r7_integrated -v` | **0** | 18 retained integrated tests under the corrected fixture |
| 5 | `python3 run_r7_quality.py` | **0** | 12 command groups incl. R5/R6 inherited, mainMAC R6/R7 references; `PASS_LOCAL_SYNTHETIC_AND_FORMAT_ONLY` |

Pre-flight byte checks performed before any edit:

| Check | Result |
|---|---|
| supplied ZIP sha256 | `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332` — matches `INPUT_PINS.json` |
| ZIP file count | 280 — matches |
| `evidence/original_zip/ANVIL_R7` vs my `PACKAGE/` | `diff -rq` → identical before modification |
| K3 TSV Git blob ids at `31291d0` | `a91214b9…`, `1f5a3ae8…`, `5a84ca8c…` — equal to the frozen ids |
| SEAM/25, SEAM/26, ANVIL/15 blobs | `181ab1aa…`, `a05c21dd…`, `6253a632…` — equal to the frozen ids |
| worktree base | `cea2d4d3009e9087d2267e9d1f53bec28b730dc7` |

## 2. NOT RUN — exact reasons

| Not run | Reason |
|---|---|
| Native SAV/DTA → 13-family C11 → cold I03/I05 → F1–F4 | **correction:** `rawlsing_next/` *is* populated in this worktree (178 files, incl. `_pre553_*`, `bounded_empirical_runtime.py`, `f07_*`, `fiabc_*`). The correct reason for not running is narrower: no original SAV/DTA source permission, no qualified native fixture, and no authorization for a native or 100k execution in this commission — not the absence of the runtime. |
| 100k × 613/690 dense run; process-tree 6 GiB measurement | runtime exists but no authorized native corpus/right and no commissioned benchmark for this defect; inventing numbers would violate `01_DECISION_CONSTITUTION.md` line 20 |
| Real cold revocation against a live C11 store | no installed C11 store; only the structural `negative`/`restore` contract is checked |
| Any FF01/FF02/N9/N10E/N10W/SOROK first effect | those owners are external and held (`T3`–`T7`) |
| Live GitHub re-fetch of #960/#1097/#1108/#1133/#1141 | saved bodies only (`LIVE_GITHUB.json`); no connector call made |
| Reading any sibling worker branch/worktree/draft | **prohibited by the commission**; not done |
| Testing `ANVIL_118_FORENSIC_AUDIT.md` allegations | document absent from supplied evidence; bounded search empty |
| K3 recensus, K4, R5 re-dispatch, 4913b562 re-analysis | out of scope / unaccepted |

## 2b. Fleet-bank evidence (read-only, challengeable)

`ANVIL_FLEET_BANK_20261117/` @ shared source bank `8523007613d411390a76683fa464002c0f25df83` was read as **local read-only evidence**. Its `FORENSIC_RECOVERY/ANVIL_118_FORENSIC_AUDIT.md` is treated as a **challengeable allegation and navigation aid**, not as a peer return or authority. Its two manifest discrepancies recorded in `FLEET_BANK_VERIFICATION.json` (`FORENSIC_RECOVERY/ANVIL_118_SOURCE_IDENTITY_MAP.tsv`; `R7_EXTRACTED/…/SYNTHETIC_DERIVED/EVIDENCE_AND_FALSIFIERS.tsv` CRLF→LF) are respected: neither the bank nor its derived files can override the original `526d835d…` ZIP or my private `PACKAGE` as byte authority. Frozen initial D3B/D4 drafts were **not** read.

## 3. Artifact hashes

See `PUBLISH_PINS.md` (generated after the commit) and `TEST_TRANSCRIPT.json` → `input_pins` for pre-commit sha256 values of every code and source file used.

## 4. Evidence-grade statement

- Source rows: **grade 1** (exact Git bytes / ZIP member).
- Gate behaviour: **grade 3 + 4** (code observed and actually executed locally, sourcefree/synthetic).
- Nothing in this return is grade 5 (native/source permission), 6 (independent review) or 7 (protected receiving).
- The inventory is `SOURCE_QUALIFIED_DOCUMENTARY_NOT_SCIENCE`. The decision and C fixtures are **authored test inputs**, not a real decision.
