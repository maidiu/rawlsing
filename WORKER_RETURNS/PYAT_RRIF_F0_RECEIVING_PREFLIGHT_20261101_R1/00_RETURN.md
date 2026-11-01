# PYAT RRIF-F0 — INDEPENDENT PRE-MAIN RECEIVING PREFLIGHT — RETURN R1

Status: `PREFLIGHT_COMPLETE__BOTH_CODE_GATES_BLOCKED_PENDING_E4FR_E6_AND_M2_OWNER__LEDGER_DOCUMENTARY_PASS__TERMINAL_PENDING_REVIEW_CAS`

Binary receiving recommendation: `DO_NOT_SELECT_OR_MERGE_ANY_CANDIDATE_YET`

One-line result: exact E4F and E5 blob identities are pinned and their path sets are disjoint; PRE-MAIN remains `8e44ca9c`; E1 D02 is still explicitly RED on real pandas `Timestamp`; E5 reproduces 179 pass/14 fail and cannot be selected as green; the live preflight refuses both gates because E4FR has no returned review, E6 has no returned review, and there is no M2 owner compatibility decision. The 34-lineage ledger's existing documentary counts and R157/C5 source/negative/restart pointers pass at their original RRIF-C scope. No PRE-MAIN, protected, source-native, or scientific authority was exercised.

## 1. Identity and execution envelope

- Role: independent I2+ receiving-compatibility, exact-source and CAS-preflight engineer. Not Pyat HQ, production integrator, E4F/E5 author, E6 reviewer, or own reviewer.
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-f0-receiving-cas-preflight-20261101-r1`
- Branch: `agent/pyat-rrif-f0-receiving-cas-preflight-20261101-r1`
- STARTUP_SHA / PRE-MAIN: `8e44ca9c751049d65e6def47600b5c073ee04b29`
- Live PRE-MAIN recheck: `refs/remotes/origin/integration/pre-main-reconciliation-r1` = `8e44ca9c751049d65e6def47600b5c073ee04b29` at preflight.
- E1 C3 candidate: `ffd03934d0a86c98ed095d973e45587bd5751013`
- E4 hostile return: `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60`
- E4F corrected candidate: `f2c0af3273d612bff0a7bd2407532b52caf4348b`
- E4FR reviewer branch: `review/pyat-rrif-e4fr-d02-corrected-consumer-hostile-20261101-r1` at `8e44ca9c...` (no returned review yet)
- E5 candidate: `96e6d49ac18274332751c5fbb87c6ed370e8fd9c`
- E6 reviewer branch: `review/pyat-rrif-e6-b5m2-postpatch-hostile-20261101-r1` at `8e44ca9c...` (no returned review yet)
- HQ ledger commission cut: `d80901e9de78803c031fa9d25146f7d8b6aeba2c`; live branch head observed `75eb695ad27652020f9ffc0363f846a7c85ca758`, one added E4F intake document above the commissioned cut.
- Host: `mainMac.lan`, macOS 13.2.1 (22D68), Darwin 22.3.0, x86_64.
- Harness: OpenCode 1.18.34, agent `build`.
- Session DB read-only: `ses_e680bf28effeGdJ4hyA8lvBrk7`, `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`, version `1.18.34`. MAX was observed active; no model/provider/account/editor/effort switch occurred.
- Python 3.11.3, pytest 9.0.2, pyreadstat 1.3.2, pandas 2.3.1, numpy 2.3.2.
- Execution surface: isolated sparse Git worktrees, source-free pytest and read-only Git inspection. No raw survey source, native source, actor, N11/N12, Sorok, PROGRAMMA, or protected write.

## 2. Exact candidate identities and path collision result

| Candidate | Exact SHA | Production payload | Tests payload | Evidence-only |
|---|---|---|---|---|
| E4F | `f2c0af3273d612bff0a7bd2407532b52caf4348b` | 2 files | 4 files | E1 + E4F return docs |
| E5 | `96e6d49ac18274332751c5fbb87c6ed370e8fd9c` | 2 files | 4 files | E5 return docs |
| E4 hostile | `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60` | 0 | 0 | 4 review docs |
| E4FR | `8e44ca9c751049d65e6def47600b5c073ee04b29` | none returned | none returned | none returned |
| E6 | `8e44ca9c751049d65e6def47600b5c073ee04b29` | none returned | none returned | none returned |

- E1 vs PRE-MAIN: exactly 2 production paths and 3 test paths, plus E1 return docs.
- E4F vs E1: only the two corrected production blobs, one new E4F 314-line test, and E4F return docs.
- E5 vs PRE-MAIN: exactly 2 production paths and 4 test paths, plus E5 return docs.
- E4F payload versus E5 payload: **zero overlapping paths**.
- `git merge-tree --write-tree` between E4F and E5 from PRE-MAIN exited `0` with no conflict message (`d3faba89...` tree).
- Exact before/after blobs and per-path ownership are in `EXACT_PATCH_PATH_AND_BLOB_ALLOWLIST.json`.

Byte identity is not authority. This preflight does not claim ABI compatibility, behavioural equivalence, source rights, scientific meaning, or external issuer authority.

## 3. Test and baseline results

| Check | Result | Exit |
|---|---|---:|
| PRE-MAIN accepted B5 + accepted M2 | 67 passed (39 B5 + 28 M2; 0 failed, 0 skipped) | 0 |
| PRE-MAIN E2 independent hostile | 10 failed, 0 passed | 1 |
| E1 D02 real SAV/DTA `Timestamp` probe | SAV/DTA cells `str`; aware subclass and wrapper `str`; explicit RED | 0 probe |
| E4F E1 33 + E4F 12 | 45 passed | 0 |
| E4F selected regressions | 194 passed, 1 skipped | 0 |
| E5 unfiltered | 179 passed, 14 failed, 0 skipped/errors | 1 |
| E5 filtered selection | 179 passed, 14 deselected (selection, not green) | 0 |
| Receiving preflight unit tests | 12 passed | 0 |
| Live preflight with no reviewer/owner receipts | both gates BLOCKED, nothing selectable | 2 |
| Ledger documentary precheck | pass, with one stale-C3 warning | 0 |

E5 breakdown matches its return:

- Accepted B5: 39/39 pass.
- Accepted M2: 26/28 pass; `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release` fail early with `RELEASE_UNAVAILABLE` at unregistered foreign release/binding setup.
- S06G repair court: 42/42 pass.
- E2 independent hostile court: 10/10 pass on E5, 10/10 failed on PRE-MAIN.
- Adjacent EE14 asof + world composition: 45/45 pass.
- Frozen S06FR overlay: 17 pass / 12 historical defect-presence failures.

The 14 E5 failures are not relabeled green. The filtered 179/14-deselected run is explicitly a selection, not a green full suite.

## 4. Live preflight refusal

Command and exact result are in `RECEIVING_TEST_AND_CAS_PREFLIGHT.md`.

Current blockers:

- E4F gate: E4FR reviewer branch has no returned commit; no independent positive review receipt; no test receipts; not selectable.
- E5 gate: E6 reviewer branch is still at PRE-MAIN; no independent positive review receipt; no M2 owner compatibility decision; no test receipts; not selectable.
- `selectable_payload` is empty.
- Exit `2` (fail closed).

The preflight code also fails closed on changed PRE-MAIN head, wrong candidate SHA, wrong before/after blob, path outside allowlist, payload collision, reviewer branch at PRE-MAIN or equal to candidate, reviewer not distinct, wrong reviewed SHA, missing/failed test receipts, missing M2 owner decision, wrong conflict-test set, or claiming the filtered selection as green.

## 5. Receiving order

1. Recheck live `integration/pre-main-reconciliation-r1` equals `8e44ca9c...` immediately before any owner CAS.
2. E4F gate only after E4FR independent positive review of exact `f2c0af327...`, including explicit adjudication of nested two-or-more-level `.item()` chains and the fact that the first R5 seam is loaded from a pinned historical Git object.
3. Apply only the six E4F payload paths. No wholesale branch merge, no E1-alone, no E4 rejection-as-acceptance.
4. Run the E4F required tests and the explicit E1 D02 RED/GREEN negative witness.
5. E5 gate only after independent E6 positive review of exact `96e6d49ac...` and a versioned M2 owner decision accepting or rejecting the two named fixture amendments. No reviewer may invent the owner decision.
6. Apply only the six E5 payload paths. No wholesale branch merge, no old S06F owner import, no `release_exact` weakening, no accepted-test edit in place.
7. Run E5 unfiltered and record 179/14 honestly; run the filtered selection only as a selection. Do not call it green.
8. Record the final terminal ledger decision as `PENDING_REVIEW_CAS` until HQ receives the exact reviews and CAS evidence.

## 6. Grades

- ENGINEERING: `PASS_CANDIDATE__F0_RECEIVING_PREFLIGHT_COMPLETE__BOTH_GATES_CORRECTLY_BLOCKED`. Blob/path/test/collision/CAS-refusal work is complete and reproducible; it is not an independent review of E4F or E5.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`. No raw source, original U/E_pre, native licence, actor, N11/N12, Sorok, or PROGRAMMA execution or claim.
- AUTHORITY: `HELD`. No protected PRE-MAIN mutation, merge, force-push, branch deletion, owner CAS, adoption, issuer/use, or self-review.

## 7. Holds and NOT_RUN

- HOLD: E4FR independent review of exact E4F SHA.
- HOLD: E6 independent review of exact E5 SHA and M2 owner fixture-amendment decision.
- HOLD: protected PRE-MAIN receiving CAS and merge.
- HOLD: terminal RRIF decision, which remains `PENDING_REVIEW_CAS`.
- HOLD: source-native science, original U/E_pre, G01 authority, R9 broker, old S06F owner import, external issuer, N11/N12, Sorok actor, PROGRAMMA.
- NOT_RUN: full repository suite; only the exact baseline, E4F selected, E5 unfiltered/filtered, preflight, and ledger commands in the return.
- NOT_RUN: new historical branch census. The ledger check reads existing RRIF-C and HQ artifacts at their original scope.
- NOT_RUN: E4F/E5 hostile re-review. That belongs to E4FR/E6, not this engineer.

## 8. Return discipline

Only the four return documents and three minimal preflight code/test files are added on this branch. No production file, test file, PRE-MAIN/main, E4F/E5/E6 worktree, ledger branch, protected source, or other worker state was modified. Exact returned HEAD is read back from origin with `git ls-remote` after push and reported in the worker terminal response; it is not embedded here because embedding it would change the commit it identifies.

Terminal: `RRIF_F0__BLOBS_AND_PATHS_PINNED__ZERO_COLLISION__E1_D02_RED_RETAINED__E5_179_14_HONEST__BOTH_GATES_BLOCKED_PENDING_E4FR_E6_M2_OWNER__TERMINAL_LEDGER_PENDING_REVIEW_CAS`
