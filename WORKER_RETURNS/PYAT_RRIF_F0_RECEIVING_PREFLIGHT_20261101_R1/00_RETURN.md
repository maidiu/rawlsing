# PYAT RRIF-F0 — INDEPENDENT PRE-MAIN RECEIVING PREFLIGHT — RETURN R1

Status: `PREFLIGHT_COMPLETE__E4F_INDEPENDENT_REVIEW_RETURNED_POSITIVE__E5_E6_HOLD__NO_MERGE__LEDGER_PENDING_REVIEW_CAS`

Binary receiving recommendation: `E4F_RECEIVABLE_ONLY_WITH_EXACT_INTEGRATOR_RECEIPT__E5_NOT_SELECTABLE__NO_MERGE`

One-line result: the exact E4F and E5 blobs and path sets are pinned and disjoint; PRE-MAIN remains `8e44ca9c`; E1 `ffd03934` still stringifies real SAV/DTA `DATETIME` cells and therefore remains explicitly RED; E5 reproduces `179 passed / 14 failed` and is not green; the independent E4FR return `7cd2206f` approves the exact E4F candidate `f2c0af32`, while the independent E6 return `b0f7675b` holds E5 for a missing owner-authorized versioned M2 fixture amendment. The live preflight refuses both gates without receipts and selects only the six E4F payload paths when the prepared E4FR receipt is supplied; E5 remains blocked. The 34-lineage ledger passes its documentary checks at the commissioned cut and remains `PENDING_REVIEW_CAS`. No merge, protected write, source-native execution, or scientific claim occurred.

## 1. Identity and execution envelope

- Role: independent I2+ receiving-compatibility, exact-source and CAS-preflight engineer. Not Pyat HQ, production integrator, E4F/E5/E6 author, E4FR/E6 reviewer, or own reviewer.
- PRE-MAIN / startup: `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Live PRE-MAIN recheck: `refs/remotes/origin/integration/pre-main-reconciliation-r1` = `8e44ca9c751049d65e6def47600b5c073ee04b29` at `2026-11-01T18:03Z`.
- Host: `oldMac.lan`, macOS 13.7.8 (22H730), Darwin 22.6.0, x86_64.
- Harness: OpenCode 1.18.34, agent `build`, session `ses_e67cec34cffe8Tq2tQ7k2Xpe3V`.
- Model read-back from the local OpenCode database: `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`. The proposed DeepSeek V4.1-Flash / MAX pair was actually active; no model, provider, account, editor, or effort switch occurred.
- Test runtime: CPython 3.11.3; pytest 9.1.1; pandas 3.0.6; numpy 2.4.6; pyreadstat 1.3.6; pyarrow 25.0.1; duckdb 2.0.0. The three non-system packages were installed only in the isolated `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/f0-venv` test virtualenv.
- Execution surface: detached, sparse, throwaway Git worktrees under `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/f0-wt-{premain,e1,e4f,e5}`. No active worker worktree was entered or modified. No raw survey source, native source, actor, N11/N12, Sorok, or PROGRAMMA execution occurred.
- Receipt provenance: the previous commit on this branch referenced temporary worktrees, a canonical repository path, and log files that are absent on this host. Every receipt in this return was re-run here from the exact SHAs; earlier hashes are not relied on. Conclusions that remain true are retained, and live reviewer returns are updated.

## 2. Exact candidates, merge bases, and collision

| Item | Exact identity | Merge base with PRE-MAIN |
|---|---|---|
| PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` | — |
| E1 C3 candidate | `ffd03934d0a86c98ed095d973e45587bd5751013` | `8e44ca9c7` |
| E4 hostile return | `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60` | `8e44ca9c7` |
| E4F corrected candidate | `f2c0af3273d612bff0a7bd2407532b52caf4348b` (parent `ffd03934d`) | `8e44ca9c7` |
| E5 B5/M2 candidate | `96e6d49ac18274332751c5fbb87c6ed370e8fd9c` (parent `f3defd3cb`) | `8e44ca9c7` |
| E4FR reviewer return | `7cd2206fd976606d3816589e2fce03c03c827f39` | `8e44ca9c7` |
| E6 reviewer return | `b0f7675bf4f434bc8964c9b3ebc8392bb33d56fb` | `8e44ca9c7` |
| HQ ledger commissioned cut | `d80901e9de78803c031fa9d25146f7d8b6aeba2c` | — |
| HQ ledger live head | `75eb695ad27652020f9ffc0363f846a7c85ca758` | — |

- E4F payload: two production files plus four tests; six paths.
- E5 payload: two production files plus four tests; six paths.
- Exact payload intersection: **empty**.
- `git merge-tree --write-tree --messages f2c0af32 96e6d49ac` exited `0` and produced tree `d3faba8905802abb505e2cb1b1a7d3cf43b36bdc`; no conflict output.
- The before/after blobs in `EXACT_PATCH_PATH_AND_BLOB_ALLOWLIST.json` were recomputed with `git rev-parse <rev>:<path>` and match the candidate trees. Byte identity is not authority, ABI compatibility, behavioural equivalence, source rights, or scientific meaning.

## 3. Current independent gate state

### E4F — independent review returned positive

- E4FR returned at `2026-11-01T13:00:10-05:00` as `7cd2206f`, reviewing exact E4F `f2c0af32`.
- Reviewer status: `APPROVE_E4F_PHYSICAL_D01_D02_SOURCEFREE_FANIN__ENGINEERING_PASS__SCIENTIFIC_AND_AUTHORITY_HELD__NESTED_ITEM_BOUNDARY_NONBLOCKING`.
- The review records the exact production blobs `4b89c459` / `f5f64d9b` and test blob `c07c2019`, and adjudicates the two-level item chain as a disclosed non-blocking boundary outside the bounded one-level D02 promise.
- The F0 preflight can select the six E4F paths only when the exact E4FR receipt is supplied and the receipt file exists at the live reviewer SHA. This return does not merge or adopt them.
- E4F is still an engineering candidate: scientific and authority claims remain held by the reviewer and by this preflight.

### E5 — independent review returned HOLD

- E6 returned at `2026-11-01T12:55:37-05:00` as `b0f7675b`.
- Reviewer status: `HOLD_E5_LOCAL_SOURCEFREE_FANIN_PENDING_OWNER_AUTHORIZED_VERSIONED_M2_FIXTURE_AMENDMENT`.
- E6 found genuine local sourcefree merit but held fan-in because the two accepted M2 tests remain byte-unchanged and RED and no accepted-M2 owner permission exists for a versioned fixture amendment.
- The required owner decision is absent. E6 states that after an owner amendment the resulting SHA must be re-run and re-reviewed by a distinct reviewer.
- E5 is therefore not selectable on this return.

### Terminal ledger

- The 34-lineage HQ ledger at the commissioned cut passes its existing documentary checks; the live head `75eb695` adds only `06_E4F_RETURN_AND_FINAL_REVIEW_GATE.md` above `d80901e9`.
- The E4FR and E6 returns are outside that HQ cut and are not ledger acceptance.
- Terminal decision remains `PENDING_REVIEW_CAS`.

## 4. Test receipts

All commands used `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, and a JUnit receipt. Exact commands are in `RECEIVING_TEST_AND_CAS_PREFLIGHT.md`.

| Check | Result | Exit |
|---|---|---:|
| PRE-MAIN accepted B5 + M2 | `67 passed` (39 B5 + 28 M2) | 0 |
| PRE-MAIN E2 hostile, serial | `10 failed` | 1 |
| E1 own D01/D02/integration suite | `33 passed` | 0 |
| E1 real SAV/DTA probe | `3 failed`: both formats `str`; naive `Timestamp` subclass unsupported | 1 |
| E4F E1 33 + E4F 12 | `45 passed` | 0 |
| E4F selected regressions | `194 passed, 1 skipped` | 0 |
| E5 unfiltered | `179 passed, 14 failed` | 1 |
| E5 filtered selection | `179 passed, 14 deselected` (selection only) | 0 |
| G01 hostile PRE-MAIN | `2 failed, 6 deselected` | 1 |
| G01 hostile E4F | `2 failed, 6 deselected`, same node ids and assertion values | 1 |
| Preflight unit tests | `16 passed` | 0 |
| Live preflight, no receipts | both gates BLOCKED, `selectable_payload: []` | 2 |
| Live preflight, prepared E4FR receipt | E4F SELECTABLE (6 paths), E5 BLOCKED, `receiving_ready: false` | 2 |
| Ledger documentary precheck | pass; one C3 stale-row warning | 0 |

E5 breakdown: accepted B5 39/39; accepted M2 26/28 (the two named foreign-release fixture conflicts); S06G repair 42/42; E2 independent 10/10; adjacent EE14 asof + world 45/45; frozen S06FR overlay 17 pass / 12 historical `OBSERVED` failures. The filtered selection is not a green full suite.

The PRE-MAIN E2 baseline is timing-sensitive: serial clean runs produced `10 failed`; one run concurrent with a separate pytest process produced `9 failed, 1 passed`, with `test_concurrent_selection_one_winner_one_conflict_and_cold_restore` passing. E6 independently recorded the same nondeterministic race caveat. The E5 candidate passes the E2 court 10/10 in the observed runs.

The E4F selected-suite skip is the known pyreadstat writer limitation: `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation` (`missing_user_values` not exposed). It is not treated as a pass.

The E1 RED is explicit: at `ffd03934`, the real SAV and DTA `DATETIME` cells are `str '2008-04-05 06:07:08'`, and `opaque_decoder_value` rejects the naive `datetime` subclass. E1's own 33 tests are unit-level and do not exercise the real subclass route; selecting only that green suite would misstate D02.

## 5. Preflight tool and refusal behaviour

`receiving_preflight.py` observes Git only and evaluates a pure fail-closed decision. `test_receiving_preflight.py` now covers 16 cases, including:

- absent reviewer receipt, reviewer branch absent, reviewer branch still at PRE-MAIN, reviewer equal to candidate;
- reviewer SHA not matching the live branch, receipt path not declared, receipt path absent at the live reviewer SHA;
- changed PRE-MAIN head, wrong before/after blob, changed path outside the allowlist, payload collision;
- missing M2 owner decision, wrong conflict-test set, filtered selection claimed green;
- selection requires both gates; one gate can be selected only with its own exact receipts.

Live no-receipt result: `receiving_ready: false`, `selectable_payload: []`, exit `2`.
Live prepared-E4FR-receipt result: E4F `SELECTABLE`, E5 `BLOCKED` by `REVIEW_VERDICT 'HOLD' != 'ACCEPT'`, the RED unfiltered status, and the missing owner decision; `receiving_ready: false`, exit `2`.

The prepared receipt is in `receipts_template` in the allowlist. It is a starting receipt transcribed from the returned reviews and the F0 test runs, not an integrator attestation. The integrator must re-verify the exact SHAs, re-run the required tests, and attest the receipt before use.

## 6. Receiving order

1. Recheck live PRE-MAIN equals `8e44ca9c...` immediately before any owner CAS.
2. Recheck E4F equals `f2c0af32...` and E4FR equals `7cd2206f...`.
3. Run the E4F required tests and the E1 RED witness.
4. Supply the exact E4FR receipt; apply only the six E4F payload paths. No branch merge, no E1-alone, no E4 rejection-as-acceptance.
5. Do not receive E5 on the current E6 HOLD. If the accepted-M2 owner later issues a versioned fixture amendment, the resulting SHA needs a fresh full court and a distinct reviewer; update the allowlist, the owner decision, and the test receipts before selection.
6. Apply E5 only as six exact paths after that re-review and owner decision; do not weaken `release_exact`, edit accepted tests in place, or treat the filtered selection as green.
7. Keep the terminal ledger at `PENDING_REVIEW_CAS` until the exact CAS evidence exists.

## 7. Grades

- ENGINEERING: `PASS__F0_RECEIVING_PREFLIGHT_COMPLETE__E4F_REVIEW_RETURNED__E5_ON_INDEPENDENT_HOLD`. Blob/path/collision/test/CAS-refusal work is complete and locally reproducible.
- SCIENTIFIC: `NO_SCIENTIFIC_OR_SOURCE_MEANING_CLAIM__HELD`. No raw source, original U/E_pre, native licence, actor, N11/N12, Sorok, or PROGRAMMA execution or claim.
- AUTHORITY: `HELD`. No protected PRE-MAIN mutation, merge, force-push, branch deletion, owner CAS, adoption, issuer/use, or self-review.

## 8. Holds and NOT_RUN

- HOLD: E5 pending an owner-authorized versioned M2 fixture amendment and a distinct re-review of the resulting SHA.
- HOLD: protected PRE-MAIN receiving CAS and any merge.
- HOLD: terminal RRIF decision, which remains `PENDING_REVIEW_CAS`.
- HOLD: source-native science, original U/E_pre, G01 authority, R9 broker, old S06F owner import, external issuer, N11/N12, Sorok actor, PROGRAMMA.
- NOT_RUN: E4FR/E6 hostile re-review; their returned verdicts are read, not duplicated.
- NOT_RUN: full repository suite; only the exact baseline, E1/E4F/E5 selected courts, G01, preflight, and ledger commands in the receipt document.
- NOT_RUN: new historical census; the ledger check reads existing artifacts at their original scope.

## 9. Return discipline

Only the four return documents and the two sourcefree preflight code/test files are modified on branch `agent/pyat-rrif-f0-receiving-cas-preflight-20261101-r1`; `ledger_precheck.py` is retained unchanged. No production file, candidate test file, PRE-MAIN/main ref, E4F/E5/E6 worktree, ledger branch, protected source, or other worker state was modified. The exact returned 40-hex HEAD is read back from origin with `git ls-remote` after push and reported in the worker terminal response; it is not embedded here because embedding it would change the commit it identifies.

Terminal: `RRIF_F0__E4F_APPROVED_BY_E4FR_7CD2206F__E5_HELD_BY_E6_B0F7675B__ZERO_PATH_COLLISION__E1_D02_RED_RETAINED__NO_MERGE__LEDGER_PENDING_REVIEW_CAS`
