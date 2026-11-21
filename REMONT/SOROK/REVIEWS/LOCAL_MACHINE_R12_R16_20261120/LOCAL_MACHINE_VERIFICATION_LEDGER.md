# SOROK REMONT local-machine verification ledger — R12–R17

**Date:** 2026-11-20
**Reviewer execution:** independent session on the same physical machine; GitHub principal `maidiu` is shared, so this is **not credential-independent G5** and does not confer native, scientific, protected or owner authority. Python **3.11.3**; pytest **9.0.2**.
**Method:** exact detached worktree per HEAD, full Python 3.11 court, demo and two-process SQLite reopen, source-manifest/blob check, prior first-fault reproduction, and additional adversarial probes.

## Candidate ledger

| PR | Exact review HEAD | Python 3.11 court | Demo / persistence | Verdict |
|---|---|---|---|---|
| #1199 corrected R12 | `943b52c08d6b0fa9cdfdff9f7b751ab2eafcccb6` | 248/248 normal; 248/248 `-O`; pytest 248 + 16 subtests; R11 reviewer 6/6; R12 hostile repair 6/6 | Seed-stable `bc47d610…`; cold reopen and `PRAGMA integrity_check=ok` | **ACCEPT_SCOPED** for the declared R11-review repair only |
| #1210 R13 | `3b9b58b75bdceec901c3ba7aaa18738ea4989923` | 255/255 normal; 255/255 `-O`; pytest 255 + 14 subtests | Valid chain/cold reopen; fresh runs differ (`2921bbaa…` vs `18f408ca…`) by hash seed | **REVISE_EXACT_DEFECT** — same-event alternate-end `TAKE_UP` |
| #1214 R14 | `f8c0d8dc901116d5fd1bfa7ec992dffa90a9aef0` | 265/265 normal; 265/265 `-O`; pytest 265 + 14 subtests | Valid chain/cold reopen; hash-seed dependent | **REVISE_EXACT_DEFECT** — inherited alternate-end takeup; P004 silent selected-means omission |
| #1220 R15 | `6075792420e1d87b30036ebe6f352815783e47c2` | 276/276 normal; 276/276 `-O`; pytest 276 + 22 subtests | Valid chain/cold reopen; hash-seed dependent | **REVISE_EXACT_DEFECT** — alternate-end takeup + P018 source preflight |
| #1222 R16 | `7a8a18c153ee5a36e1c52eca15f4e5e8862296be` | 280/280 normal; 280/280 `-O`; pytest 280 + 32 subtests | Seed-stable `bc47d610…`; cold reopen and integrity valid | **ACCEPT_SCOPED** for P070 typing, deterministic recruitment and any-end trial guard; **HOLD overall** for inherited P018 |
| R17 repair (new branch) | `7a8a18c` + source-preflight commits | 289/289 normal; 289/289 `-O`; pytest 289 + 32 subtests | Seed-stable `bc47d610…`; cold reopen and integrity valid | Published sourcefree repair candidate; independent review pending |

## Findings

### R12 corrected `943b52c`
The declared R11-review repairs pass: `REORGANIZE_PROJECT` and all `TAKE_UP_POSSIBLE_END` are refused inside an issued trial; typed non-object P070 snapshots and deterministic active-form ordering are present. The imported R12 hostile module is 6/6 and the R11 reviewer module is 6/6. This does not accept R13/R14/R15, which are **not descendants** of this commit. The later R13 falsey-cue-tag fix is absent here: on R12, `cue(tags=False/''/{}/())` is accepted and one invalid case still mutates the clock; that is an R13-scope defect, not part of the R12 R11-review claim.

### R13 / R14 / R15 — alternate-end trial takeup
The prior R13 reviewer's two failure cases reproduce on R13, R14 and R15 under normal and `-O`: index:R13/R14/R15 allow model `TAKE_UP_POSSIBLE_END` for a different end B in the same event that issued a legitimate trial for end A. A new independent probe generalizes this to B with a **different object** (`sing together` trial A, `learn piano` end B): R13/R14/R15 commit the durable project and mark B `TAKEN_UP_AS_PRACTICAL_PROJECT`; R16 refuses with `CURRENT_TRIAL_NOT_MATURE_MOTIVE`. This is the same R13 first fault, not an inherited test passing.

### R15 / R16 — P018 source preflight
Five prior first-fault cases reproduce on R15 and R16: after rewriting a historical source anchor, injecting a source map into an ordinary event, or making a source event payload noncanonical, full `verify_chain()` rejects the history while `source()` still returns content and `commit()` still appends. Two additional independent cases also fail on R15 and R16: a noncanonical **initialization** payload and a noncanonical **ordinary-event** payload are rejected by `verify_chain()` but `source('seed')` still returns content. The fast preflight is not the full audit.

### R14 P004 — selected means omission
`record_activity_afterlife` accepts a `purpose_selection` for an existing project whose `means` do not include the performed operation and silently returns `[]` with no history. It does not fabricate history, but a selected purpose that cannot be the operation is dropped rather than refused. This is a hardening gap, subordinate to the R14 takeup finding.

### R13/R14/R15 demo nondeterminism
Fresh demo runs at the same HEAD produce different event hashes under different `PYTHONHASHSEED` values (`2921bbaa…` and `18f408ca…`) while each chain is internally valid. R16's sorted active-form closure makes fresh R16/R17 runs byte-identical at `bc47d610…`.

### R16 declared scope
R16 P070 typed snapshot tests, 17-form deterministic recruitment test, R12 hostile module, and R13 alternate-end test all pass. Its declared repairs are admitted at scoped sourcefree engineering. R16 does not repair P018; that inherited defect remains RED.

## Genealogy and custody warning

- R13 `3b9b58b` has commit parent `9db0e6f` (original R12), **not** corrected R12 `943b52c`. PR #1210's base branch pointer is the corrected R12 branch, but the commit genealogy is divergent. Do not treat corrected R12 acceptance as inherited by R13/R14/R15; a merge can also revert R12 correction files.
- R14 -> R15 -> R16 form the R13-line chain. R16 selectively carries R12 P070/determinism/cross-end fixes; it does not include the R12 `HOSTILE_G5_CORRECTION` receipt or test file.
- R17 is a new branch stacked on R16; it does not rewrite R13–R16.

## Defect-identity conservation

All reviewed ledgers were checked against the original 71-record source and the 73-record R13 line:

- R12 corrected: 71 P records, original records unchanged; queue_E 6 unchanged.
- R13: original 71 unchanged; adds `SR-P072`, `SR-P073` (author-repaired, review pending).
- R14/R15/R16: all 73 IDs present; original 71 statuses unchanged; only P004/P012/P018 annotations added at the later cuts.
- 53 scoped first-fault review dispositions, 8 open, 8 partial, 4 author-repaired pending review (P070–P073), T=0, E=6 remain.
- Source manifests match exact HEAD files. No protected PRE-MAIN, canonical PROGRAMMA or paired CURRENT_PROGRESS write was performed.

## Published repair

R17 closes the inherited P018 preflight gap by requiring full `verify_chain()` under lock/transaction in `source()`, `commit()` and `seal_source()`. It passes 288/288 normal and `-O`, pytest 288 + 32 subtests, 8/8 focused P018 tests, imported R15 P018 6/6, and the R13 alternate-end module 5/5. Receipt: `REMONT/SOROK/REPAIRS/REMONTATHON_R3_R17_20261120/REPAIR_RECEIPT.md`.

## Outstanding obligations

1. R13/R14/R15 alternate-end takeup remains RED in those frozen candidates; the repair exists in R16 and must be independently received on its own exact HEAD.
2. P018 remains RED in R15/R16; R17 is the repair candidate and still needs a distinct independent reviewer.
3. R16 is accepted only for its declared P070/determinism/any-end scope; overall source custody stays HOLD until R17 receiving.
4. Corrected R12 is accepted only for the R11-review repair; R13's cue-tag and later-line changes are not inherited.
5. Shared GitHub principal means this ledger is not credential-independent G5. No native, scientific, human, production or protected receiving is claimed.

## GitHub review records

- #1199 corrected R12: https://github.com/maidiu/rawlsing/pull/1199#issuecomment-7054467083
- #1210 R13: https://github.com/maidiu/rawlsing/pull/1210#issuecomment-7054470086
- #1214 R14: https://github.com/maidiu/rawlsing/pull/1214#issuecomment-7054471195
- #1220 R15: https://github.com/maidiu/rawlsing/pull/1220#issuecomment-7054473498
- #1222 R16: https://github.com/maidiu/rawlsing/pull/1222#issuecomment-7054474928
- #1230 R17 repair: https://github.com/maidiu/rawlsing/pull/1230


## SORACLE × REMONT #1234 — execution review

**Exact HEAD:** `dbfb35c18ed0ec061050acdd1a1e5000e0bacc6b` (Python 3.11.3). This is the SORACLE builder's R3 × REMONT R18 integration, not an ordinary REMONT repair candidate.

**Execution:** `compileall` PASS. The PR's focused courts are not green: `test_r3_r18_joined_faults` + `test_r3_r16_joined_first_consumer` → 19 ran, 1 ERROR (`P018` corrupt-history test raises untyped `KeyError: 'world'` through `source()`); `test_r17_source_preflight` + R18 P004 + R13 → 25 ran, 1 ERROR (`R13` runtime trial test raises `NO_ACTION_OR_PRACTICAL_OPTION`); `test_joined_longitudinal_demo` → 3 ran, 2 ERROR. Full discover: **524 ran, 27 failures + 51 errors** normal and `-O`. Pytest fails collection on `test_initiative_r9.py` and `test_operative_witness_r9.py` (`ModuleNotFoundError: initiative` / `operative_witness`). The longitudinal demo command fails with `TRIAL_MATERIAL_OBJECT_NOT_UNIQUELY_BINDABLE`.

**Representative regressions:** R6 (19 errors), R8 (13 failures + 1 error; cue tag/modality/threshold and contextual-flag guards), R11/R12 (trial and inherited-review errors), R14 activity (3 failures), relational metabolism (4 failures), plus joined demo failures. The claimed source blobs for joined `storage.py`, `cultural_mediation.py` and `social_vocal_development.py` match the exact tree, so this is execution/contract failure, not a source-identity substitution.

**Verdict:** `REVISE_EXACT_DEFECT` / `HOLD`. The candidate is explicitly `COMMITTED_UNTESTED`; it is not ready for SORACLE or REMONT receiving. SORACLE owns the ordinary initial RED repair. The `KeyError` locus is hardened in the current R17 preflight (`EVENT_ENVELOPE_MALFORMED` / typed `SOURCE_HISTORY_INVALID`), but #1234 still carries the older storage blob and must be reintegrated and rerun.
- #1234 SORACLE×REMONT execution review: https://github.com/maidiu/rawlsing/pull/1234#issuecomment-7058012755
- R17 update (289 tests, malformed envelope hardening): https://github.com/maidiu/rawlsing/pull/1230#issuecomment-7058013087
