# PYAT RRIF-CUSTODY-A — POST-LOGGING-GAP SOURCE AND RECEIVER LOCATION COURT

**Status:** sourcefree custody evidence — not HQ, science, adoption, production integration or merge.
**Repository:** `maidiu/rawlsing` private.
**Branch:** `agent/pyat-rrif-custody-a-source-location-20261031-r1`.
**Base/current PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`.
**Current main:** `25830fe7462bb9e29bc4087e6ae14f3f84cec377` (ancestor of PRE-MAIN).
**Frozen estate:** PR #515 roster `becf0bfb04705b8fe0927dd56e7290e1dcd180a8`; E8 `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`; overlay `00489a8b2e8e04ed2264d87371f6b0ec4a2d9347`.
**Harness:** local OpenCode / `opencode-go/deepseek-v4.1-flash`, MAX requested; actual variant/account/quota not independently instrumented.
**Live source state:** unchanged. PRE-MAIN remains `8e44ca9c…`; this evidence branch writes only the custody return tree.

## FINDING / INTERPRETATION / ACTION / OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| 845 frozen names / 838 distinct tips match PR #515 and E8. All 845 current remote refs exist; one frozen ref moved (PR #515 proposal itself). | The roster is a stable historical denominator, not the current branch universe; historical tips must remain frozen. | Preserve every original name and tip; record current ref status separately. | RRIF custody / HQ |
| 321 branches contain code deltas versus their correct merge base. 276 are stranded or diverged; 45 have changed code blobs already exact in PRE-MAIN; 458 are evidence/admin-only; 66 have no delta/ancestor. | Code was stored in three places: canonical PRE-MAIN, exact/diverged branch tips, and evidence-only worker branches. Branch names and `accepted` labels do not prove merge. | Publish per-branch and per-variant locations; do not merge or census again. | Original branch owners / PRE-MAIN integrator / HQ |
| 1,717 of 3,135 variants have exact source blobs at frozen branch tips; 199 are exact same-path current, 291 exact other-path current, 928 current-modified; 866 implementation variants have only modified current paths; 0 fully not located at this grain. | Most code is findable; a minority is exact in PRE-MAIN, many are branch-only, and 866 require semantic/merge comparison because only a modified current path exists. Blob identity is not behavioral equivalence. | Use `CODE_LOCATION_LEDGER.jsonl` and `RECEIVER_AND_STAGING_MAP.md`; send exact exceptions to owners. | Owner reviewers / branch authors |
| Nine Pyat `integration/...accepted` branches are not ancestors of PRE-MAIN. Four have all changed code exact in PRE-MAIN, four are stranded/diverged, one is evidence-only. Staging heads are mostly ancestors; two Sorok staging heads are separate. | An “accepted” integration branch was not automatically merged into canonical PRE-MAIN; some code was copied/cherry-picked, some remains branch-only. | Audit merge/cherry-pick/consumer disposition before any integration claim. Do not self-CAS. | Incumbent PRE-MAIN integrator / HQ |
| PR #525/#526/#563 are ancestors of PRE-MAIN; J2I branches are ancestors with no delta. R157 final, HQ282-P01 and P07 remain branch-only; C3/R5 exact assets are in its return but current D01/D02/R9 paths are absent. | “Recent branch exists” is not “merged code”; conversely a merged branch may add only evidence. | Use counterexample audit; bounded follow-up on R157/HQ282-P01/P07/C3 D01/D02/R9. | Original owners / PRE-MAIN integrator |

## ENGINEERING

**PASS at location-map scope; HOLD on merge/consumer acceptance.**

- 3135/3135 original variants have a row; 845/845 branch names have exactly one summary row.
- 845 names, 838 tips, 3135 functions, 1883 variant-bearing families + 2 external zero-member families.
- 2,269 exact-current/branch-source subtraction; 866 current-modified code uncertainties; 0 fully not located.
- 27 accepted/staging branches audited; PR #525/#526/#563, J2I, C3 R5, R157, HQ282-P01, P07 spot-checked.
- Validator PASS; 7 mutation tests OK.

## SCIENTIFIC

**HOLD.** No original source meaning, U/E_pre, CAN/ADP/SCI05, Pyat N11/N12, N9/N10W, C9/C12, actor science or human product is issued. Blob identity is not science.

## AUTHORITY

**HOLD.** No source-owner authenticity, production adoption, merge, PREMAIN/main mutation, priority, or self-review. Branch ownership and receiver acceptance remain separate.

## WHERE THE CODE IS

- **Canonical PRE-MAIN:** 199 exact same-path + 291 exact other-path variants; 928 current-modified; 446 implementation variants exact current.
- **Frozen branch tips:** 1,717 exact variant blobs; 1,333 exact implementation variants; 321 branches with code deltas (276 stranded/diverged; 45 exact-present).
- **Evidence/admin branches:** 458 branches have no product-code delta; 66 are no-delta/ancestors.
- **Accepted/staging:** 27 branches; accepted labels not merge proof; 9 Pyat accepted branches are not PRE-MAIN ancestors.
- **Known branch-only examples:** R157 final (34 code deltas, 4 exact current, 24 absent), HQ282-P01 (6 code files absent), P07 (3 code deltas, 1 absent).
- **C3/R5:** exact G01/decoder/R5 assets located in `24847592…`; current D01/D02/R9 production paths are absent. No R9 transplant.
- **No fully unlocated variant** at this grain. 866 implementation variants have a modified current path but no exact current/branch blob; they are uncertainties, not “lost capabilities.”

## DONE

- Reproduced PR #515 845/838 roster, its 524 strict/321 transitional split and cutoff notes; joined E8 3,135 variants/1,885 families.
- Branch-creation time is not recorded by Git; only post-cutoff tip dates and the one moved current ref are asserted.
- Computed 838 merge-base deltas and branch classifications; preserved all 845 original names.
- Joined 3,135 variants to current exact, current modified, other-path exact, frozen branch exact, and absence.
- Built `CODE_LOCATION_LEDGER.jsonl`, `BRANCH_LOCATION_SUMMARY.jsonl`, `EXACT_CURRENT_SUBTRACTION.json`, `UNCERTAIN_OR_MISSING_CODE.jsonl`, `RECEIVER_AND_STAGING_MAP.md`.
- Audited 27 integration branches and the required counterexamples.
- Observed 13 local-only refs and 153 worktrees read-only; non-local estates remain UNKNOWN.
- Validator and 7 mutation tests pass.

## REMAINING

- Owner review of branch-only exceptions (R157, HQ282-P01, P07, C3 D01/D02/R9).
- Merge/cherry-pick/copy verification for the 45 exact-present branches; source identity alone does not prove transfer method.
- Semantic/behavioural comparison for 866 current-modified variants and 1,333 branch-only exact implementations where integration is proposed.
- Receiver/consumer verification for accepted/staging branches.
- #577 was not present/returned at this cut; no behavioral callgraph was duplicated.

## BLOCKERS

- No source-owner authenticity or adoption.
- No merge/cherry-pick provenance for all exact-present branches.
- No semantic equivalence for modified/branch-only code.
- No production consumer, native Pyat, C3/C12 actor, N9/N11/N12 or human product authority.
- Non-local Mac/session estates inaccessible: UNKNOWN, not empty.

## LARGEST_MOVE

Have the incumbent PRE-MAIN integrator/owners review the small exact exception set: R157, HQ282-P01, P07, C3 D01/D02/R9, and the 45 exact-present branches. Use the ledger to decide merge/cherry-pick/consumer disposition. Do not reopen the 845-branch census or start another whole-history investigation.

## FLIGHT

S2 read-only full Git history, frozen roster/ledger JSON, merge-base diffs, batch `cat-file`, Git ancestry, Python/JSON validation, 7 unit tests. No source recensus, native source/survey/actor execution, PREMAIN/main/worker branch writes, or merge.

## DELTA

`+` complete 845-name/3,135-variant where-map; `+` 838 correct-merge-base branch summary; `+` 2,269 exact-source subtraction and 866 typed uncertainties; `+` accepted/staging and PR/J2I/C3/R157/HQ282/P07 audit; `−` no semantic equivalence, merge proof, source adoption or product acceptance.

## FINAL SHA

`FINAL_SHA: reported in the terminal push readback after non-force commit/push; a file cannot contain the SHA of the commit that contains it.`

**TERMINAL:** `RRIF_CUSTODY_MAP_COMPLETE__845_NAMES_838_TIPS_3135_VARIANTS__321_CODE_DELTA_BRANCHES__2269_EXACT_SOURCE_SUBTRACTION__866_UNCERTAIN__NO_MERGE_OR_ADOPTION`.
