# RRIF custody — receiver and staging map

**Status:** sourcefree custody evidence. Not HQ, not science, not adoption, not a merge decision.
**Canonical PRE-MAIN:** `8e44ca9c751049d65e6def47600b5c073ee04b29`.
**Current `main`:** `25830fe7462bb9e29bc4087e6ae14f3f84cec377` (ancestor of PRE-MAIN; no newer receiving delta in this cut).
**Frozen estate:** PR #515 roster, 845 names / 838 distinct tips; E8 `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`; overlay `00489a8b2e8e04ed2264d87371f6b0ec4a2d9347`.

## Answer: where is the code stored?

1. **Some is already in PRE-MAIN at exact blob identity.** Of 3,135 original variants, 199 match at the same path, 291 match at a different current path (copy/move unverified), and the remaining current-path variants are modified (928). There are 446 implementation variants with exact current implementation blobs; this is source identity, not behavioural equivalence.
2. **Most historical variants are still recoverable on frozen branch tips.** 1,717 variants have an exact original blob at at least one inherited branch tip; 1,333 of those are implementation code. This is a location fact, not a merge or acceptance fact.
3. **321 branches contain a code delta against their proper merge base.** 276 are stranded or diverged relative to PRE-MAIN; 45 have their changed code blobs already exactly present in PRE-MAIN, but the transfer mechanism (merge, cherry-pick, copy) is unverified. 458 branches are evidence/admin-only; 66 have no delta versus merge base / are ancestors.
4. **“accepted” integration branches are not automatically merged.** The 10 accepted/staging accepted-named branches include 9 Pyat `integration/...accepted` branches; none is an ancestor of PRE-MAIN. Four contain code blobs now exact in PRE-MAIN, four remain stranded/diverged, one is evidence-only. Staging branches are mostly ancestors/no-delta; two Sorok staging branches are separate direct heads.
5. **Recent review/return branches can be already included.** PR #525, #526 and #563 heads are ancestors of PRE-MAIN; PR #563 is the S7FIX/PE/V2K intake included by the PRE-MAIN merge. Both J2I branches are ancestors with no new code delta.
6. **Some implementation remains branch-only.** R157 final review has 34 code deltas, only 4 exact current, 24 absent. HQ282-P01 has 6 code files absent from PRE-MAIN, including the governed-batch/durable-consumer candidates. P07 has 3 code deltas, 1 absent. C3/R5’s exact historical C3 assets are in its recovery return, but current D01/D02/R9 production paths are absent; G01 behavior may be rebuilt without the authority wrapper.
7. **No fresh not-located set is forced by this pass.** Every original variant has a current or frozen-branch location at the declared grain. 866 implementation variants have only a modified current path, so exact location is uncertain; they are not called lost capabilities.

## Chronology and cutoff

The PR #515 roster records the last dense integration at `ef46892f8e2752b62eef0778b1bdb53a86d80e70` (2026-09-27T18:56:30Z) and the last observed implementation-tree touch at `79e0e74e14d8e09cc2f3af061aa178a149cb1674` (2026-10-09T22:31:19Z). Its shards contain 524 strict-core and 321 transitional names; all 845 listed tip dates are after the cutoff. Git does not record branch-creation time, so creation-versus-tip chronology is `UNKNOWN`; the roster's own limitation `TIP_DATE_NOT_CREATION_DATE` is retained. The only current-ref exception is the PR #515 proposal branch moving from its frozen tip to `becf0bfb…`; no frozen historical tip was rewritten.

## Frozen denominator and current refs

| Measure | Exact |
|---|---:|
| Frozen names | 845 |
| Distinct frozen tips | 838 |
| Current remote refs present | 845 |
| Frozen tips moved after roster | 1 (`proposal/pyat-stranded-branch-recovery-20261028-r1`, `3b5ff992…` -> `becf0bfb…`) |
| Evidence/admin-only branches | 458 |
| Code-exact-present branches | 45 |
| Stranded/diverged code branches | 276 |
| No-delta/ancestor branches | 66 |

Roster identity digests are in `BRANCH_IDENTITY_CUSTODY.json`; the name/tip digests match the PR #515 manifest shards. The one moved current ref is PR #515 itself; its frozen tip is retained.

## Variant disposition counts

| Location | Functions |
|---|---:|
| PRE-MAIN exact, same path | 199 |
| PRE-MAIN exact, different path (copy/move unverified) | 291 |
| PRE-MAIN modified same path | 928 |
| Frozen branch tip exact | 1,717 |
| Fully not located | 0 |
| **Total** | **3,135** |

| Implementation class | Functions |
|---|---:|
| Current exact implementation | 446 |
| Current modified implementation | 866 |
| Branch-only exact implementation | 1,333 |
| Evidence/test/document (not implementation) | 490 |

`EXACT_CURRENT_SUBTRACTION.json` has **2,269** variants with no new missing-source recovery warranted at this grain (exact current, exact frozen-branch, or non-code evidence). `UNCERTAIN_OR_MISSING_CODE.jsonl` has **866** implementation variants whose current path is modified and whose exact original is not current or exact on a frozen tip. Neither file implies semantic equivalence, merge, native capability, or scientific acceptance.

## Accepted/staging branches

`INTEGRATION_RECEIVER_MAP.json` records 27 branches: 10 accepted-named and 17 staging. Highlights:

| Branch class | Finding |
|---|---|
| Pyat `integration/...accepted` (9) | None is an ancestor of PRE-MAIN. Code exact current: HQ145 1/1, HQ159 3/3, HQ162 2/2, HQ168 5/5; HQ130 0/3 exact, HQ139 0/1, HQ147 1/2, HQ151 0/1, HQ166 0 code. “Accepted” is a label, not a merge proof. |
| Pyat `integration/staging-...` (15) | All tested staging heads are ancestors/no-delta at this cut. |
| Sorok staging direct heads (2) | `staging-sorok-b3a-accepted-sql-repair` and `staging-sorok-c9r3b-sourcefree-recovery` are separate direct heads not in the frozen 845 roster; no product-code transfer assumed. |

## Counterexamples audited

| Item | Exact finding |
|---|---|
| PR #525 | Head `a0a4e6b0184b5c5de1f723913103bc34a833b9f6` is an ancestor of PRE-MAIN; proof-only, no code delta. |
| PR #526 | Head `6a38ef25057e577b7b546449844a8b33fc647a82` is an ancestor; workflow-only, no code delta. |
| PR #563 | Head `91a854a9123ad33e84e5b847d8f4aecd60508046` is an ancestor; included by PRE-MAIN `8e44ca9c`. |
| J2I | HQ122 `bbcec05d…` and HQ123 `35aac47f…` are both ancestors; no new delta. |
| C3 R5 | Exact G01 `31a9afd7…`, decoder `d3d828c1…`, R5 codec `6000a170…` are located in C3/R9 return `24847592…`; D01/D02/R9 current production paths are absent. No R9 transplant. |
| R157 | `agent/pyat-pre553-r157-final-review@d81bc2c6…`: 34 code deltas, 4 exact current, 24 absent; config/stranded branch, not native U/E. |
| HQ282 P01 | `agent/rabochii-pyat-hq282-p01-v2-durable-consumer-integration-r1@3f91dc22…`: 6 code files absent from PRE-MAIN, including governed-batch and durable-consumer candidates. |
| P07 | `agent/space-bunny-pyat-hq242-f7-t1-native-p07-owner-implementation-r1@d6ce7101…`: 3 code deltas, 1 absent; not merged; native P07 remains unsafe. |

## Local-only and inaccessible estates

- Read-only local observation: 13 local-only refs and 153 registered worktrees. They are outside the frozen 845 denominator. The local `agent/pyat-index-s0…` head is the PR #515 roster/proposal tooling, not product implementation.
- Non-local Mac/session estates and unregistered working copies are **UNKNOWN**, not empty. No active worker worktree was changed.

## Limits

This map proves file/blob location and branch ancestry only. It does **not** prove semantic/behavioural equivalence, a merge mechanism, source-owner authenticity, scientific meaning, production acceptance, or that a branch named “accepted” was merged. A modified current path is not automatically the historical variant; a branch-exact blob is not automatically adopted. The next bounded action is owner review of the location exceptions (R157, HQ282-P01, P07, C3 D01/D02/R9) and a merge/cherry-pick/consumer decision; no new census is warranted.
