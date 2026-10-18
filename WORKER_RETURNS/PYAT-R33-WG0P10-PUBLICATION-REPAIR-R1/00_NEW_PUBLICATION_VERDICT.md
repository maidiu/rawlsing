# WG0P10 — NEW PUBLICATION VERDICT

## `PASS_PUBLICATION_TRANSPORT_REPAIRED__D1_TO_D5_CLOSED__D6_DISCLOSED__INDEPENDENT_WG0P11_REQUIRED`

| | |
|---|---|
| **Role** | Bounded sourcefree transport author. **NOT** HQ, **NOT** WG0P9's independent I2 reviewer, **NOT** original-source signatory, **NOT** model/world/actor owner. |
| **Branch** | `agent/userdirect-pyat-20261017-r33-wg0p10-five-publication-defects-repair-r1` |
| **Commission** | `WORKER_COMMISSIONS/PYAT-R33-WG0P10-FIVE-PUBLICATION-DEFECTS-REPAIR-R1/00_COMMISSION.md` @ `90e6b5cc713780df0fb617d9357feed14c00ed24` |
| **Inputs** | WG0P8 candidate `e1d82971f8c07147550ce53ef3c4bc52f349fed3`; WG0P9 independent verdict `c2bfed5b2e11d229068dfdf78a3df16467704d14`; WG0N Phase B `6cd28b429504ad47e1bbc0fbcc6c4ef91db59ccd` |
| **Write terrain** | `WORKER_RETURNS/PYAT-R33-WG0P10-PUBLICATION-REPAIR-R1/` only |
| **No mutation** | P7/P8/P9 evidence and all frozen tests preserved; 187/187 inherited preimages byte-exact |

This is a **transport/publication** repair. It makes the published candidate self-contained
and executable in a clean Git checkout. It makes no scientific claim.

---

## 1. Five commissioned defects — all demonstrated failed-before / passed-after

| # | Defect | Before | After |
|---|---|---|---|
| **D1** | `probe_import` expected `WG0P4_NATIVE_FRONTIER_COLD@1`; the repaired module declares `WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1`, so the shipped `run` **refused the correct module** | `WG0P8_PRE_I03_REFUSE:WRONG_DIRECT_OR_UNREPAIRED_RUNTIME_MODULE` | `probe-import` returns the correct module, `sha256 89fed0a6…`, real version |
| **D2** | `bootstrap_p6` atexit receipt used `mkdir(exist_ok=True)` without `parents=True`; exception swallowed, no import audit emitted | `FileNotFoundError …/candidate/observations/imports`, 0 receipts | receipts emitted per process, authenticated |
| **D3** | `candidate/observations` and `candidate/runtime` absent from the published tree | `fresh42: 42 passed, 1 error` | `fresh42: 42 passed, 0 errors` |
| **D4** | `cold_comparison.json` held a literal `<WORKTREE>` token and the named cold dir had **no `owner/`** | `cold_pointer: 1 failed` | `cold_pointer: 1 passed` |
| **D5** | `reviewer_frozen/03_INHERITED/WG0N/02_PHASE_B_VERDICT.md` omitted | `wg0o17: 16 passed, 1 failed` | `wg0o17: 17 passed` |

D5 is restored at its **exact Git preimage** from WG0N Phase B `6cd28b429…`:
blob `8678d29b10cdf26ef944b90563dfecdf1832afad`, SHA-256
`839adc7508fcd81bd0a59af8f0fc8793b8ea075c80661683b776124cb90a228b`. **No fabricated verdict.**

## 2. A sixth defect, discovered and disclosed separately

**D6 — not in the commissioned set.** The published `run_suites` omitted
`WG0L_PHASE_B_ADAPTER=phase_b_adapter_v1` and `WG0M_RUN=phase_b_P5`, which the candidate's
*own* documented invocation contract
(`candidate/court/02_ACTUAL_EXECUTION_OR_TYPED_HOLD.json`) requires. `test_precommitted_phase_b.py`
refuses collection without it (`PHASE_B_NOT_AUTHORIZED_WITHOUT_PUBLISHED_CANDIDATE_READ_CUT_AND_VERSIONED_ADAPTER`),
so the published runner produced **65 errors** where the contract says 65 passed.

I fixed it, and I am labelling it explicitly as **not** one of the five. Leaving it would have
made the commissioned `mandatory236` evidence undeliverable in a clean checkout.

## 3. D4 — how the cold fixture was made honest

The frozen `tests/test_cold_pointer_process.py` is **unedited**. The fix has two parts:

1. **Genuine regeneration**, not substitution. `repro/wg0p10_regenerate_cold.py` runs the
   pinned, unmodified `phase_b_cold_worker_v1.py` in two real processes:
   `crash` → exit **23**, `resume` → exit **0**. Real PIDs, real `fsync` → `replace` → `fsync`
   durability calls, real manifest.
2. **Safe runtime resolver.** The published JSON carries a repository-relative path;
   `candidate/tests/conftest.py` promotes it to absolute using *this* checkout's root.

No developer machine path is baked into the artifact. No receipt is forged. **Cold identity is
not weakened:** the manifest hash is `bcd255228ef35edcb9b59436b76e1eb78947c07180f2936779572f510981c140`,
identical to the historical identity WG0P9 independently recorded.

**What this does NOT prove:** `os._exit(23)` and process exit exercise *process death*, not
machine power loss. This is not power-loss durability evidence.

## 4. Fresh clean Git checkout — no overlay, no archived JUnit

Cloned fresh at the published SHA. Working tree clean. Every JUnit under
`02_FRESH_CLEAN_GIT_IMPORT_COURTS_JUNIT/` has a **fresh timestamp from this session**.

| Suite | Cases | Result |
|---|---:|---|
| wg0o17 | 17 | **17 passed** |
| wg0q36 | 36 | 36 passed |
| wg0m33 | 33 | 33 passed |
| original65 | 65 | **65 passed** (was 65 errors) |
| original3 | 3 | 3 passed |
| j44_k11 | 55 | 55 passed |
| owners80 | 80 | 80 passed |
| fresh42 | 42 | **42 passed** (was 42 + 1 error) |
| cold_pointer | 1 | **1 passed** (was 1 failed) |
| transport9 | 9 | 9 passed (JUnit regenerated fresh) |
| **published runner total** | **331** | **331 passed / 0 failed / 0 errors / 0 skips** |

`mandatory236` = wg0m33 33 + original65 65 + original3 3 + j44_k11 55 + owners80 80 = **236**.

`verify` → `PASS_SOURCEFREE_FILE_CUSTODY`. `probe-import` → correct module, `sha256
89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`, version
`WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1`.

## 5. Custody

- **187/187 inherited `SOURCE_INPUTS` preimages verified byte-exact** after every change.
- `CANDIDATE_CODE_PIN.json` carries 10 entries: 8 byte-identical to WG0P8 (including the two
  frozen test files), 1 changed (`bootstrap_p6/sitecustomize.py`, D2), 1 added
  (`tests/conftest.py`, D4 resolver).
- WG0P8 force-tracked the nested `runtime_phase_b` past its own `/runtime_phase_b/` gitignore;
  the derived artifact does the same, so a clean checkout is genuinely self-contained.
- No original canonical/P8 tree was mutated.

## 6. What is explicitly NOT claimed

No scientific adjudication of the native claims. No real institutional custody, issuer
signatures, independent revocation or owner temporal supersession — all **held** in
`04_HISTORICAL_NOT_GREEN_AND_ISSUER_HOLDS.md`. WG0N's five unconstructible controls and the
two historical characterisation conflicts remain **NOT GREEN**; nothing was relabelled.
No production ADP019 grant, no human perception, no physical-world event, no semantic
adoption, no V3 operation.

**No self-adoption.** A distinct independent **WG0P11** court follows.

## 7. Artifacts

| Path | Purpose |
|---|---|
| `01_FIVE_DEFECT_BEFORE_AFTER_SHA.json` | per-defect before/after, SHA ledger, suite tallies |
| `02_FRESH_CLEAN_GIT_IMPORT_COURTS_JUNIT/` | fresh JUnit + stdout, before/after matrices |
| `03_COLD_CRASH_OWNER_RECOVERY_AND_WRONG_IMPORT.json` | real crash/resume PIDs, durability calls, manifest identity, resolver proof |
| `04_HISTORICAL_NOT_GREEN_AND_ISSUER_HOLDS.md` | retained NOT GREEN + authority holds |
| `candidate/` | the new versioned self-contained derived candidate + bootstrap |
| `repro/wg0p8_publication.py` | repaired publication runner (D1, D6) |
| `repro/wg0p10_regenerate_cold.py` | genuine cold fixture regeneration (D4) |
| `repro/wg0p10_before_after.py` | before/after harness |
| `reviewer_frozen/03_INHERITED/WG0N/02_PHASE_B_VERDICT.md` | restored exact preimage (D5) |
