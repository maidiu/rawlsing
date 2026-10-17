# PYAT R32 WG0P9 — INDEPENDENT CLEAN NATIVE REPLAY — VERDICT

**Disposition: HOLD — the native scientific courts are PHYSICALLY REPRODUCED, but the
published WG0P8 transport is NOT self-contained as shipped. No `SELFCONTAINED_PASS` and no
independent adoption until five exact publication defects are repaired.**

Reviewer: independent source-free physical execution reviewer, **not** the WG0P8 author,
**not** HQ, **not** a semantic/issuer/world/actor owner.

---

## 1. Independence and clean checkout

- Fresh isolated clone/worktree of `maidiu/rawlsing` at the pinned P8 commit
  `e1d82971f8c07147550ce53ef3c4bc52f349fed3` (remote branch
  `agent/userdirect-pyat-20261017-r31-wg0p8-selfcontained-publication-repair-r1`,
  direct `git ls-remote` = same SHA), at `/tmp/wg0p9_p8`, **detached, clean**.
- No reliance on any WG0P7/WG0Q reviewer local worktree. Write branch starts at the R32
  sealed startup `32b867444a9a466768d00ea31ef249394a5253f3`.
- Actual Python 3.11.3, pytest 9.1.1, Git, subprocess, real OS cold processes.

## 2. Custody and input verification (actual, not documentary)

`repro/wg0p8_publication.py verify` in the clean checkout:

- **187/187** declared source inputs present, SHA-256 + Git-blob + byte-length exact;
- **11/11** restored inherited observation files exact;
- corrected derived `SOURCE_INPUTS.json` P5 row = repaired module
  `89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`
  (Git blob `62895078908ff748771da9a9fbcec6b36d34a803`), no stale `06fadc…` alias;
- derived `SOURCE_INPUTS.json` SHA-256
  `2e7d47d2a14fe1fec12fd574c1183fadf50ee25b6f10a62ffae8858e29885418`;
- zero symlinks; repaired and direct P5 are distinct files;
- verifier terminal: `PASS_SOURCEFREE_FILE_CUSTODY`.

Direct import of the repaired P5 under the pinned P6 bootstrap resolves to
`…/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py`, SHA-256
`89fed0…`, `VERSION = WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1`.

## 3. Real frozen courts — actual execution

| Court | Claimed | Independently executed | Notes |
|---|---:|---:|---|
| P8 9 transport guards | 9 | **9 passed** | real JUnit, `transport9.xml` |
| Original WG0O 17 | 17 | **16 passed / 1 failed as published; 17/17 with one exact-Git inherited restore** | missing WG0N verdict, see D5 |
| Reviewer WG0Q 36 | 36 | **36 passed** | all 11 negatives + 3 positives + body/revocation/temporal |
| Inherited mandatory 236 | 236 | **236 passed** = 33 WG0M + 65 original + 3 original3 + 44 J + 11 K + 80 owners | each suite real JUnit |
| Fresh source-view 42 | 42 | **42 passed** | in writable execution copy; pristine P8 teardown error, see D3 |
| Positive consumer | 42 cells / 4 I03 | **42 cells, 4 I03, effects SHA `4b9d0324…`** | P1/P2/P4 served; P3 replay 0 I03 |
| Cold crash → resume | exit 23 / 0 | **exit 23 then 0; PIDs 22473 / 22474** | 1 then 2 I03, same 3-unit manifest `bcd255…`, original receipt `caac243f…` |
| Cold pointer forgery | refused | **1 passed** | `IdentityError`, 0 new I03, 3 units, 0 restored receipts, custody/journal unchanged |

All exits and JUnit are in `02_REAL_FROZEN_COURTS_AND_JUNIT/`; cold raw records in `cold/`.

## 4. Hostiles — independently forced

- **Verifier fail-closed** (exit 86 with exact typed message): missing source file
  (`MISSING_OR_SYMLINK`), modified declared SHA (`INPUT_HASH_OR_BLOB_CHANGED`), stale
  `06fadc…` alias (`STALE_SOURCE_INPUT_HASH_ALIAS`), repaired P5 swapped to pristine direct
  (`INPUT_HASH_OR_BLOB_CHANGED`), omitted predecessor at import
  (`WG0P6_BOOTSTRAP_REFUSE`), repaired P5 swapped at import (`SOURCE_PREIMAGE_CHANGED`).
- **Authority seam**: wrong issuer, same-hash foreign signed body, foreign governed operation,
  foreign authority tuple, stale issuer epoch (HELD), self-rehashed checkpoint foreign
  signature, captured callback fabrication, source-artifact revocation not release tag,
  missing independent issuer, alias across genuine universes → all typed
  `IdentityError`/`RevocationError`/`ColdRestartError`/`AuthorityCurrentnessHold`, served
  false, 0 I03.
- **Authority body**: B1–B12 forged/substituted bodies → `IdentityError REFUSED`; R1 withdrawn
  and R2 revocation unknown → `RevocationError`; R3/R4/R5 cold forgery → `ColdRestartError`;
  S1–S5 source swaps → `IdentityError`/`FrontierError`; T1–T7 temporal → HELD/refused.
- **Issuer by hash matching**: A3/A4 same-hash foreign signed body/operations and B1/B8
  self-rehash/false-content-hash are refused. Issuer identity is not invented by hash equality.

## 5. Exact publication defects (why this is HOLD, not PASS)

These are real defects of the P8 **transport/publication**, not of the native science:

- **D1** `probe_import` expects `VERSION == "WG0P4_NATIVE_FRONTIER_COLD@1"` on the repaired P5,
  whose actual verified version is `WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1`. The shipped
  `run` command therefore refuses the **correct** module with exit 86
  (`WRONG_DIRECT_OR_UNREPAIRED_RUNTIME_MODULE`). A false-negative transport, not a security hole.
- **D2** `bootstrap_p6` atexit receipt writes `candidate/observations/imports`; the directory
  and its parent do not exist and `mkdir` has no `parents=True`. No import-audit receipt is
  produced; the exception is swallowed.
- **D3** `candidate/observations` and `candidate/runtime` are absent in the published tree.
  The fresh-42 autouse teardown errors in the pristine checkout; the cold-pointer test fails at
  `mkdir`. With these directories created, 42/42 passes.
- **D4** `cold_comparison.json` stores a sanitized `cold_directory`
  (`<WORKTREE>/WORKER_RETURNS/PYAT-R27-WG0P6…/cold/cold-face4d…`) and the inherited cold
  directory contains only `checkpoint/crash/resume/commands` — **no `owner/`**. The frozen cold
  pointer test cannot run as published. It passes only after a genuine cold crash/resume is
  re-executed (PIDs 22473/22474) to regenerate `owner/`, with the path restored in the execution
  copy. Frozen test source is unchanged.
- **D5** `reviewer_frozen/03_INHERITED/WG0N/02_PHASE_B_VERDICT.md` is omitted. The frozen WG0O
  17 test requires it (`PRESERVED_MARKERS`), so the suite is **16/17 as published**. Restoring
  the exact Git blob from WG0N Phase B `6cd28b429` (SHA-256
  `839adc7508fcd81bd0a59af8f0fc8793b8ea075c80661683b776124cb90a228b`) gives **17/17**, and the
  test then confirms the five unconstructible controls and two historical characterisation
  failures remain NOT GREEN.

## 6. Preserved NOT GREEN

- Five WG0N unconstructible historical cases remain unconstructible; no fields manufactured.
- Two historical stronger-refusal/characterisation contradictions remain unchanged; neither is
  relabelled as green.
- Original RED observations are retained; no inherited XML is replayed as a new run.

## 7. Verdict and next action

**HOLD.** The native P8 code and frozen suites are genuinely executable and the claimed
17/36/236/42/4-I03/cold/pointer results are independently reproduced, with one exact-Git
inherited-file restore and harness directory/path reconstruction. But P8's own verifier and cold
transport cannot complete a clean self-contained replay as published. Publish a bounded WG0P10
repair:

1. fix the repaired-P5 VERSION expectation (or check the published version);
2. create `candidate/observations`/`candidate/runtime` with `parents=True` or add them;
3. restore or regenerate the cold `owner/` fixture and remove the `<WORKTREE>` placeholder
   dependency from the frozen comparison (or ship a resolver);
4. restore the omitted WG0N `02_PHASE_B_VERDICT.md` at its exact Git blob;
5. re-run `verify`, `probe-import`, WG0O 17, WG0Q 36, 236, 42, cold and pointer with no manual
   overlay, and publish the resulting JUnit.

Until then: no `SELFCONTAINED_PASS`, no WG0N/HQ acceptance, no issuer/semantic adoption.

## 8. Non-grants

No original SAV/DTA/raw data, no U/E_pre, no signed issuer, no independent source-artifact
revocation support (NOT_SUPPORTED), no temporal/semantic adoption, no N11/N12, no actor/V3
rights, no HQ self-adoption, no production owner commit.
