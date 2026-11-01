# RRIF-V hostile findings — A × B custody and false subtraction

**Review cut:** canonical `8e44ca9c751049d65e6def47600b5c073ee04b29`; A `84182f9fa7044d67689ea4f80eabf7e9337f15c2`; B `59e6e62600814d82cfefd1a2137b7aa63316bc95`; HQ crossjoin `f5a9facd189af6756c2b15c8daebe680016f658a`; E8 `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`.
**Status:** hostile evidence; not adoption, science, merge, native source or own review.

## 1. Claims that survive at the declared grain

| Claim | Independent result |
|---|---|
| 845 frozen names / 838 distinct tips | PASS. PR #515 shards sum to 845 names / 838 tips; A and E8 names/tips match. All 845 current refs exist; one frozen proposal ref moved (`3b5ff992…` → `becf0bfb…`), historical tips retained. |
| 321 code-bearing branches | **PASS at branch-delta classification.** A/HQ crossjoin agree. The classification is “changed code vs merge base,” not unique author implementation. |
| 276 stranded/diverged; 45 exact-present | **PASS at byte/ancestry classification.** All 45 exact-present branches independently rechecked: every changed code path is exact in PRE-MAIN, no modified/absent code. Ten stranded samples each have at least one absent/modified code path. |
| 195/81 split | PASS as **fate-category** split: 81 code-stranded branches have a `HQ_*`/`REVIEW_*` fate; 195 do not. The 195 is not “no evidence”: it includes two `HQ_OTHER` decision-bearing branches and many candidate returns. |
| 23/22 split | PASS as fate-category split for 45 exact-present branches; 22 classified, 23 not. |
| B has 155 primary-decision-bearing rows / 151 fate-classified / 4 unclassified | PASS only as branch-row/fate counts. It is **not** 155 unique primary decision IDs. |

## 2. A's 2,269 subtraction is not a current PRE-MAIN subtraction

**Claim:** “2,269 source-location subtraction; only 1,333 branch-only exact and 490 evidence/test/document remain.”
**Contradiction:** A's own `EXACT_CURRENT_SUBTRACTION` includes:
- 199 same-path current exact;
- 291 exact-other-path current matches;
- 1,717 branch-tip exact;
- 62 current-modified non-code;
- 1,333 branch-only exact **implementation** records.

The 1,333 branch-only implementation records are not current PRE-MAIN integration. Example `S1-F-0003` (`rawlsing_next/pre553_universal_evidence_binding.py`, blob `00312f84…`) is branch-tip exact but absent from current PRE-MAIN. A includes it in the subtraction because “branch exact” is in the subtraction rule. This is a source-location disposition, not a current-code reduction.

**Consequence:** HQ cannot use 2,269 as “already current, no recovery.” At most 199 same-path current exact records are current source-identity evidence; 1,333 are branch-located only, 291 require responsibility/ABI review, and 928 current variants are modified.
**Correction:** Split the number into:
- `CURRENT_SAME_PATH_EXACT = 199` (155 implementation + 44 non-code);
- `CURRENT_OTHER_PATH_EXACT = 291` (responsibility unverified);
- `BRANCH_ONLY_EXACT = 1,717` (1,333 implementation + 384 non-code);
- `CURRENT_MODIFIED = 928` (866 implementation; 62 non-code).
Do not call 2,269 a current-code or adoption subtraction.

## 3. The 291 exact-other-path matches are not runtime equivalence

**Claim:** 291 variants are current exact via another path.
**Contradiction:** all 291 are byte copies of **11 AT07 `INPUTS/*_law.py`/fixture files** into 11 current paths. 65 land in test/fixture paths; examples:

- `source_fixture_law.py` → `rawlsing_next/tests/test_pre553_empirical_query.py` (48 records).
- `at17_fixture_law.py` → `rawlsing_next/tests/n10e_empirical_slice_fixture.py` (17).
- `objects_law.py` → `rawlsing_next/pre553_empirical_objects.py` (55).
- `adopted_owner.py` → `rawlsing_next/pre553_analytical_composition.py` (35).
- `consumer_law.py` → `rawlsing_next/source_backed_positioned_subject_possibility.py` (30).
- `integrity_law.py` → `rawlsing_next/pre553_c11_integrity.py` (30).

Exact bytes at a different path do not establish same owner, ABI, call direction or runtime responsibility. A's subtraction includes all 291. The current test targets alone prove 65 records are not runtime code.

**Correction:** keep them as `SOURCE_COPY_OR_FIXTURE_RELATED`, not current integration; require owner/path/ABI/consumer comparison before subtraction.

## 4. Function-to-branch attribution remains family-inherited

**Claim:** 1,333 branch-only exact implementations are located on branches.
**Contradiction:** 3,117 of 3,135 A rows use `FAMILY_INHERITED_BRANCH_SET__EXACT_VARIANT_BRANCH_UNVERIFIED`; 851 variants have more than one exact branch-tip hit. The 18 special boundary rows use post-roster S7FIX/I3 branches. A branch-tip exact hit is a location, not the branch that authored the variant.
**Consequence:** branch counts (276 stranded, 321 code-bearing) are not counts of unique code authors or independent implementations. B's crosswalk has 135 records, 12 file-set mappings, 145 observed family IDs in one record, and zero promoted family/function IDs; it does not rescue A's family inheritance.
**Correction:** keep branch-location claims; do not attribute a variant to a branch or family without exact path/blob commit lineage. Deduplicate aliases/ancestor inheritance before commissioning.

## 5. B decision counts and attributions

**Claim:** 155 primary-decision IDs vs 151 classified HQ/reviewer outcomes, plus four `HQ_OTHER`.
**Independent result:**
- 155 **branch rows** have a primary decision ID;
- only **122 distinct primary decision IDs**;
- **135** decision records;
- **151** rows classified by fate;
- **4** rows `HQ_OTHER`/unclassified;
- **5** rows actually have primary class `HQ_OTHER` because `reviewer-pyat-hq201-r1` carries `HQ_OTHER` with a reviewer FAIL verdict.

**Material defects:**
1. `HQD-2026-10-04-202` is one multi-subject row for three branches: hq201-r1/r2 (candidate/withheld) and reviewer-hq201 (FAIL). B assigns the same HQ_OTHER primary to all three; one ID is not three decisions.
2. `HQD-2026-10-01-151` is attached to four branch names and three tips; one HQ_ACCEPT class is spread over four rows. It is a multi-subject decision, not four unique decisions.
3. `HQD-2026-10-03-198` (HQ_OTHER) and `HQD-2026-10-03-199` (HQ_ACCEPT) both name hq197-r1/tip `4b6335ca`; B chooses 199 as primary and loses the 198 contextual blocker for the same tip.
4. `CKPT-20261009-PYAT-HQ274…` has `formal_ledger_status: NOT_A_FORMAL_HQ_LEDGER_DECISION`, scope `…CANDIDATE_BUNDLE_NOT_ADOPTED`, and `code_adoption:false`, yet B fate is `HQ_ACCEPTED`/class `HQ_ACCEPT`. This is a false acceptance signal.
5. Seven duplicate-tip groups include hq143/hq145, hq149/hq151 and hq144/hq147; these are aliases, not independent decisions. The 155/151 denominator must not be read as 155 unique decisions.

**Correction:** report 155 branch rows, 122 unique primary IDs, 135 decision records, 151 fate-classified rows, 4 unclassified `HQ_OTHER` rows and 5 `HQ_OTHER` class rows separately. Keep reviewer verdicts separate from HQ decisions. Do not count checkpoint/documentary intake as HQ acceptance or code adoption.

## 6. Nine accepted integration branches — accepted is not merged

| Branch | Decision | Current code retention |
|---|---|---|
| HQ130 C3 | HQD-131 | 0/3 exact; 3 absent |
| HQ139 C1-01 | HQD-139 | 0/2 exact; 2 absent |
| HQ145 C1-02 | HQD-145 | 5/5 exact |
| HQ147 N10E AT17 | HQD-147 | 3/6 exact; 3 absent (partial) |
| HQ151 C5/N5 | HQD-151 | 0/2 exact; 2 absent |
| HQ159 C1-03R | HQD-159 | 11/11 exact |
| HQ162 C1-03A | HQD-162 | 8/8 exact |
| HQ166 AT07 | HQD-166 | no code delta |
| HQ168 C1-03 join | HQD-168 | 21/21 exact |

None of the nine is an ancestor of current PRE-MAIN. Four are all-exact, one partial, three no-exact, one no-code. The branch-local acceptance documents and B rows coexist; acceptance is historical/scoped, not current retention or merge.

## 7. Counterexamples

- **C3/R5:** exact G01/decoder/R5 codec claims are in C3/R9 return `24847592…`; current `pre553_source_access_broker.py`, `pre553_source_session.py`, `pre553_execution_binding.py`, `closed35_g01_sav_numeric_representation_authority.py` are absent. C3 acceptance/retention is historical; no R9 transplant.
- **R157:** branch `agent/pyat-pre553-r157-final-review@d81bc2c6…` has 34 code deltas, 4 exact current, 6 modified, 24 absent; B records no HQ decision. Its all35 configuration evidence is not native U/E or current implementation.
- **HQ282-P01:** branch `3f91dc22…` has 6 code files absent from PRE-MAIN, including `pre553_governed_batch_checkpoint_integration_candidate.py` and `pre553_v2_durable_consumer_integration_candidate.py`. This is a valid branch-only source case, not a lost capability.
- **P07:** branch `d6ce7101…` has 3 code deltas, 1 absent and 2 modified; no merge and no native P07 authority.

## 8. Unknowns and permitted narrower claims

- 866 current-modified implementation variants need semantic/consumer comparison; 1,333 branch-only exact variants need current integration; 291 other-path exact variants need responsibility/ABI comparison.
- A/B do not prove source-owner authenticity, behavioral equivalence, merge, cherry-pick, production consumer or science.
- Branch creation time is not recorded by Git; tip dates are not creation dates.
- PR/issue review APIs were unavailable (`403`); #577 was not present/returned; no callgraph duplication.
- Local-only refs/worktrees were read-only observed; non-local Mac/session estates are `UNKNOWN`, not empty.

**Permitted reduced scope:** use 845/838, 321 code-bearing branch rows, 276 stranded/diverged branch rows, 45 exact-byte-present branches, and the 195/81 + 23/22 fate splits as **branch-grain triage**. Use 155/151/4 only as branch-row/fate counts with the 122-unique-ID correction. Do not use 2,269 as current code, do not treat 291 other-path as runtime equivalence, and do not treat 1,333 branch-only exact as current PRE-MAIN integration.
