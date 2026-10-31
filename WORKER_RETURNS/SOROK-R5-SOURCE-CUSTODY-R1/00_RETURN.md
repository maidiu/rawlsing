# SOROK R5 — F1CR executable recovery and V3 archive provenance

## Identity and terminal

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-r5-f1cr-executable-and-v3-archive-source-custody-20261030-r1` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-r5-f1cr-executable-and-v3-archive-source-custody-20261030-r1` |
| Current PRE-MAIN | `750548ddbb9b4392a16ce93097b856f349e16182` |
| F1C / F1CI3 / F1CR | `bcea367e…` / `0a884fd5…` / `03be5c22…` |
| RCF-A / RCF-B | `e66dc53a…` / `397c6d61…` |
| Device / harness | `oldMac`; OpenCode `1.18.34`; `opencode-go/deepseek-v4.1-flash`, local variant `max` |
| Session | `ses_e77c423e1ffealQLzYonSQTRRf`; actual title `INDEX_B 282-branch indexing commission`; suggested R5 title not applied |

**Terminal:** `R5_F1C_ORIGINAL_EXACT_RECOVERED__F1CR_PATCHED_SOURCE_NOT_FOUND__RECONSTRUCTED_CANDIDATE__ARCHIVE_CONTAINER_MISMATCH_SELECTED_FILES_GREEN`

Observed FINDING: the original F1C executable is exact at loose blob `104f5bd…`, but the F1CR claimed patched executable `bf7e625…` / SHA-256 `18c96f97…` is absent from all objects, trees and surviving worktrees. The historical archive's selected TD-R05 sources and all 488 Python members match exactly, while the ZIP container SHA differs from `953c9149…`. Causal INTERPRETATION: F1CR's patched source was never committed/survived; a new reconstruction can close the documented defect but cannot claim original bytes. The archive mismatch is consistent with packaging/metadata (AppleDouble, .DS_Store, pycache, pytest cache, Unicode filename encoding), not changed source. Proposed HQ ACTION: use the exact original F1C source, label the reconstructed candidate for owner review, and keep both F1CR exact source and whole-container custody unresolved. Accountable OWNER: original F1C/F1CR author, R31J/C8 and C10/C9 owners, historical V3/V2 owner.

## Part A — F1CR

Exact original: `candidate/f1c_original_104f5bd.py`, blob `104f5bd…`, SHA-256 `7e3492a2…`. It is the original F1C source and the byte-identical F1CI3 candidate.

Frozen test: `candidate/test_full_history_binding.py`, blob `b012e65e…`, SHA-256 `271e6aa1…`.

Missing exact patched executable: `bf7e625e…` absent; no surviving source file in `f1cr-return`, `f1cr-base`, `f1cr`, loose objects, reflogs, trees or archives. `SOURCE_NOT_FOUND`.

Reconstructed candidate: `candidate/f1c_reconstructed_candidate.py`, blob `c6e64b58…`, SHA-256 `12f183a3…`, explicitly `RECONSTRUCTED_CANDIDATE`; adds `live_prior(life)` and A/B/shared digest checks after the frozen-hash check, before C8. It is not the missing F1CR bytes.

Actual tests:

- Original F1C: 13/13 outcomes, exit 0; frozen hash `30fc98b9…`; result SHA-256 `5c3b91dd…`.
- Reconstructed: 13/13 same case names, p01, holds and frozen hash; result SHA-256 `4de846b2…`.
- Original F1CI3 mutation: 3 RED / exit 1, JUnit `d7daf297…`.
- Reconstructed mutation: 3 PASS / exit 0, JUnit `62bec3f6…` with `LIVE_A_HISTORY_CHANGED`, `LIVE_B_HISTORY_CHANGED`, `LIVE_SHARED_HISTORY_CHANGED`.

Required consumer: `f1c.same_receiver_assertion` → `R31JProduct` / `r31j.assertion.p01`; BP4 C10 consumes the C9 target in SHARE. Targetless REFUSE/SILENCE stops at `C9_RECEIVER_HOLD:later_e2:NO_PROPOSAL`; JOIN `RefusalSession` is a separate read-only carrier. No durable C9/C10 targetless adapter is supplied.

## Part B — V3 archive

Archive: `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip`, 21,967,177 bytes, SHA-256 `3f2c5ed9…`; TD-R05 expected `953c9149…`; **container mismatch**. TD-R05 manifest blob `7bc6729e…`.

- 9,808 ZIP members: 4,528 non-Apple files, 4,904 AppleDouble members, 376 dirs; no duplicate names.
- TD-R05 selected sources: **31/31 present with exact bytes/SHA-256**.
- Python members: **488/488 byte-identical** to the extracted directory.
- 4,515/4,520 common files identical; five differences are four `.DS_Store` and one `.pytest_cache` entry.
- Eight only-ZIP reference filenames are mojibake versions of eight directory em-dash filenames with identical content; 34 only-directory files are generated `.pyc`.
- **No `.py`/YAML source module difference found.** Container-level provenance is still `UNKNOWN`/mismatch; do not declare whole-archive custody green.

Safe now (subject to RCF-A invalid-mechanism quarantine): TD-R05 selected code, `BackboneState`, `compute_all_derived`, step order, `run_one_year`, `run_n_years`, `run_pressure_flow_cycle`, `render_year`, and generation readiness. Owner clarification required for M08 identity-seeded wound, M15/M36 50/50/50 defaults, M34 fallback practice, M35 placeholder cracks/frameworks, M39 random rupture, M37 stubs, M31 Enneagram, M38/M40 semantics, and whole-container identity.

## Three courts

- ENGINEERING: **PASS SCOPED** — exact original F1C recovered; missing F1CR patched bytes proved; reconstructed candidate 13/13 and 3/3; archive selected/source-member comparison completed.
- SCIENTIFIC: **HOLD** — sourcefree only; no native B/world/Rule A/T/practice/C9/C12 or person.
- AUTHORITY: **HOLD** — no merge, adoption, original author impersonation or PRE-MAIN/PR mutation.

## Artifacts

- `00_RETURN.md`
- `01_F1CR_EXECUTABLE_TREE_BLOB_AND_RECONSTRUCTION_LEDGER.json`
- `02_ORIGINAL_ARCHIVE_MEMBER_AND_HASH_RECONCILIATION.json`
- `03_REEXECUTION_AND_NEGATIVE_EVIDENCE.md`
- `04_FIRST_CONSUMER_HANDOFF_AND_UNRESOLVED_OWNERS.md`
- `05_PROVENANCE_AND_SESSION.json`
- `candidate/f1c_original_104f5bd.py`, `candidate/f1c_reconstructed_candidate.py`, `candidate/test_full_history_binding.py`

RUN: F1C 13/13 original and reconstructed; F1CI3 3 RED original / 3 PASS reconstructed; member/hash reconciliation.
NOT_RUN: missing F1CR patched executable; C10 durable adapter; full V3/V2 historical suite; TD-R05 80-test aggregate; native source/LLM/production; PRE-MAIN/PR.

DONE: exact original F1C recovery, missing patched executable proof, reconstruction, 13/3 test evidence, archive selected/code match and container mismatch. REMAINING: owner reconstruction decision or missing bytes; C10 targetless/durable C9; archive container provenance. CRITICAL BLOCKERS: missing F1CR bytes; unresolved whole-container identity; no native/C9/C10 authority. LARGEST PRODUCTIVE MOVE: owner accepts/rejects reconstructed candidate or supplies `bf7e625e…`, and archive owner supplies full TD-R05 member manifest. FLIGHT: sourcefree local Git/Python/read-only ZIP. DELTA: exact original recovered, missing patched source proved, reconstruction testable, archive mismatch localized to packaging/metadata.

The exact pushed return SHA is the HEAD of this branch and is reported with the final return message. No self-adoption.
