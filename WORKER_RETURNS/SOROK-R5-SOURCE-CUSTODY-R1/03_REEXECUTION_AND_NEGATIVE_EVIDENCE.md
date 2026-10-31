# R5 — reexecution and negative evidence

Observed FINDING: the exact original F1C executable is recoverable, but the F1CR patched executable is not. Causal INTERPRETATION: the F1CR return's successful runs survive as logs/results, yet the source bytes claimed by `18c96f97…` are absent; a newly labeled reconstruction closes the documented live-history defect but cannot inherit the missing author bytes. Proposed HQ ACTION: accept the original F1C source as exact, use the reconstructed candidate only after owner review, and keep the F1CR patched executable `SOURCE_NOT_FOUND`. Accountable OWNER: original F1C/F1CR author, R31J/C8 and C10/C9 owners, separate reviewer.

## F1CR exact original and reconstruction

Original F1C executable: loose blob `104f5bd7826c8676192eac96753d980e35d8a80a`, SHA-256 `7e3492a267acbc0fa11d8792158bdaa2acc9dfb6053f16141ed637dc1cd2881b`; recovered in `candidate/f1c_original_104f5bd.py`.

Claimed F1CR patched executable: SHA-256 `18c96f97eca5480893c0f38a06f21c0d985fe0c6c997e63e0898001157351dfb`, blob `bf7e625e1f208908e583ea72ebb73992ad7d19ae`; **absent from batch-all-objects, all trees and surviving worktrees**. Status `SOURCE_NOT_FOUND`.

Reconstructed candidate: `candidate/f1c_reconstructed_candidate.py`, blob `c6e64b5874938045d80aae348de94930539d5cd2`, SHA-256 `12f183a379bd1fabf37433b0e3ac893221f78370cd73d2a7c173554a1db14871`; adds `live_prior(life)` and A/B/shared digest checks after the frozen-hash check and before C8. It is explicitly `RECONSTRUCTED_CANDIDATE`, not the missing F1CR bytes.

Unchanged frozen test: `candidate/test_full_history_binding.py`, blob `b012e65eb92c21e8733bdd92f46ca4a88aa709e5`, SHA-256 `271e6aa15af8b2c3217ed2fdb94f2514e70c0bf9a9fa3122e3fe4d7f0aebdc6b`.

## Actual commands and results

Run in a temporary copy under the R5 worktree so the recovered F1C `runtime/` has a `.git` ancestor:

```sh
# Original exact F1C
cp candidate/f1c_original_104f5bd.py <tmp>/f1c.py
cd <tmp>
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest test_full_history_binding.py -q
# 3 failed, exit 1  (live A, live B, shared witness all DID NOT RAISE)
PYTHONDONTWRITEBYTECODE=1 python3 f1c.py > original_13.json
# 13 cases, exit 0

# Reconstructed candidate
cp candidate/f1c_reconstructed_candidate.py <tmp>/f1c.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest test_full_history_binding.py -q
# 3 passed, exit 0
PYTHONDONTWRITEBYTECODE=1 python3 f1c.py > reconstructed_13.json
# 13 cases, exit 0
```

| Run | Result | JUnit / result hash |
|---|---:|---|
| Original F1C, 13 outcomes | 13 cases, exit 0 | result JSON `5c3b91dd…` |
| Reconstructed candidate, 13 outcomes | 13 cases, exit 0; same case names, p01, holds and frozen hash `30fc98b9…` | result JSON `4de846b2…` |
| Original F1CI3 mutation test | 3 failed, exit 1 | JUnit `d7daf297…` |
| Reconstructed F1CI3 mutation test | 3 passed, exit 0 | JUnit `62bec3f6…` |

The original and reconstructed 13 outputs have identical frozen object, frozen hash, case set, `p01` values and exact holds. The three mutations are refused only in the reconstructed candidate with `LIVE_A_HISTORY_CHANGED`, `LIVE_B_HISTORY_CHANGED`, `LIVE_SHARED_HISTORY_CHANGED`. The original F1C behavior (including RETROACTIVE_A `A_B_OR_SHARED_PREHISTORY_CHANGED`) is preserved.

## Part B archive reexecution/identity

The archive itself was not executed in this R5 pass; its selected source tests are attributed from RCF-A (`e66dc53a…`) at 40 selected tests: 4 architecture + 12 step logic + 24 pressure-flow, plus named step-order mutation. R5 independently verified archive/member identity:

- ZIP SHA-256 `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289`; TD-R05 expected `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`; **container mismatch**.
- 9,808 ZIP members (4,528 non-Apple files, 4,904 AppleDouble files, 376 dirs); no duplicate member names; 1,285 duplicate-content pairs.
- TD-R05 manifest: 31/31 selected rows present with exact bytes/SHA-256; 488/488 Python members byte-identical to the extracted directory.
- 4,515/4,520 common files identical; five differences are `.DS_Store`/pytest cache; eight only-ZIP reference filenames are mojibake versions of eight only-directory em-dash names with identical content; 34 only-directory files are generated `.pyc`. No `.py`/YAML source module change found.
- Container-level provenance remains `UNKNOWN`/mismatch; do not declare whole-archive custody green.

RCF-A attributed tests/mutation: `v3/tests/test_architecture_invariants.py` 4 passed, `test_step_logic.py` 12 passed, `test_v5_pressure_flow.py` + golden 24 passed; mutation of `render_layer` before `field_update` failed `test_step_order_immutable` with named core-spine assertion. R5 did not rerun these.

## RUN / NOT_RUN

RUN: F1C original 13, reconstructed 13; F1CI3 mutation 3 RED original / 3 PASS reconstructed; exact blob/hash searches; ZIP member and selected manifest reconciliation.

NOT_RUN: F1CR claimed patched executable (absent); C10/durable C9 adapter; full V3/V2 historical suite; TD-R05 80-test aggregate; LLM/provider calls; native source/respondent data; PRE-MAIN/PR/CI mutation.

## Negative conclusion

The original F1C code is safe as an exact source donor. The reconstructed candidate is a sourcefree candidate, not the original F1CR executable. The archive's selected source and all Python members are byte-identical, but the container identity is unresolved; historical mechanisms with invalid defaults/placeholders/random rupture still require owner quarantine. No test was weakened, no original author impersonation, no scientific rule issuance.

DONE: exact F1C recovery, missing F1CR identification, reconstructed candidate, 13/13 and 3/3 before/after, archive member reconciliation. REMAINING: F1CR owner review of reconstruction; C10 handoff; archive owner/container provenance; invalid-mechanism owner decisions. CRITICAL BLOCKERS: missing F1CR bytes; unresolved container; native C9/C10/C12 authority. LARGEST PRODUCTIVE MOVE: owner confirms reconstruction or supplies `bf7e625e…`, and archive owner supplies full TD-R05 member manifest. FLIGHT: sourcefree local Git/Python only. DELTA: exact original recovered, missing patched bytes proved, reconstruction testable, and container mismatch localized to packaging/metadata.
