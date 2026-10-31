# PYAT RABOCHII 845-S1 — independent source/function/merit/successor/integration investigation

## Identity and session custody

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Role | Independent original-source/code investigator and disposition author; NOT PRE-MAIN integrator, source/semantic issuer, original reviewer or own hostile reviewer |
| Output branch | `agent/pyat-rabochii-845-s1-function-investigation-20261030-r1` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rabochii-845-s1-function-investigation-20261030-r1` |
| Device | `mainMac` (`scutil --get ComputerName`) |
| Harness / agent | OpenCode CLI `1.18.34`, agent `build` |
| Model / effort | `opencode-go/deepseek-v4.1-flash`, session variant `max` |
| Session | `ses_e7285576bffeqo0lE8N0HYK6gc`, observed title `Retained GT2 → N10E analytical consumer (H03)` |
| Startup / receiving baseline | `750548ddbb9b4392a16ce93097b856f349e16182` |
| Roster proposal head | `becf0bfb04705b8fe0927dd56e7290e1dcd180a8` |
| Roster blob | `146b100e7f3456fabdec2e6ed8059adf0bf8a68d` |
| S0 raw index | GitHub Actions `41137105778`, completed success |
| S1 machine source/AST index | GitHub Actions `41142495040` at `3ef4d09bc47789536802b8eae290a57db4c38122`, completed success |
| Pre-commit current PRE-MAIN | `750548ddbb9b4392a16ce93097b856f349e16182` (same as receiving baseline) |
| Final pushed SHA | reported externally after push; a commit cannot contain its own hash |

## Scope

Exactly the frozen S1 roster: **175 unique branch names**, **175 distinct pinned tips**, **5 unclassified tip names**, cohort `STRICT_CORE_OCT09_PLUS`. No other shard names were borrowed. All 175 branches are present in `BRANCH_DISPOSITIONS.jsonl`; the set equality against the roster was checked before commit.

## Method and source cuts

Observed FINDING: the S0 and S1 Actions artifacts are complete machine indexes over the exact roster. They give exact branch/tip/tree, merge-base..tip changed paths/blobs, and Python AST symbols, but explicitly do **not** prove function equivalence, test grade, adoption, original source access or scientific authority. I used them as index evidence, then read original blobs and branch-specific returns through Git plumbing and static AST.

- S0 index: `S1_blob_path_index.jsonl`, SHA-256 `7f33d5c41fe17457860a6140b755246ce617854522a9941225946b9516056074`; coverage `path_blob_grains` and `functional_path_blob_grains`; `index_complete=true`, `function_equivalence_proved=false`.
- S1 branch index: `S1_branch_code_return_index.jsonl`, SHA-256 `662dcbb87572d9d626c3b91dddbb56826743a75f139098c321879e88efed636b`.
- S1 variant index: `S1_function_variant_index.jsonl`, SHA-256 `1a7d40c8f03d2e5929a168c45770103f83a05c1226020be59ce45bdac875329e`.
- Current symbol index: built locally from the exact current PRE-MAIN tree (`750548dd`) over all `rawlsing_next/*.py` files, using the same `ast.dump(include_attributes=False)` shape law as the S1 index. 341 current Python paths and 8,149 current symbols.
- Current reference index: 14,892 names / 271,787 `Name`/`Attribute`/import references for consumer/signature mapping.
- Branch-specific returns: matched by branch-name tokens to the return root present at the branch tip; read `00_RETURN.md` and `00_*`/review/verdict files. 132 branches have a branch-specific return root; 43 do not.
- Origin vs inherited: for each of the 176 unique code variants, the branch tips carrying it were compared by `git merge-base --is-ancestor`; tips not descended from another carrier are origin candidates. Per-branch occurrence counts are 197 origin and 1,469 inherited repetitions. A branch name or age alone was not used as evidence.

**No branch code was executed, imported or run as a program. No test in any reviewed branch was run. No original survey/response source was opened or executed.** All test names in the artifacts are static evidence locators, not executed results.

## Counts

| Measure | Count |
|---|---:|
| Roster branches present | 175 |
| Distinct pinned tips | 175 |
| Code-changing branches | 121 |
| No-code/doc-or-return-only branches | 54 |
| Changed source path occurrences | 1,666 |
| Changed test path occurrences | 868 |
| Changed return roots | 1,702 |
| Unique code variants | 176 |
| Candidate Python symbols in variants | 5,800 |
| Function-court rows (top-level public production function/class variants) | 1,279 |
| Branches with branch-specific return root | 132 |
| Branches with no branch-specific return root | 43 |

## Function dispositions

| Disposition | Rows | Meaning in this return |
|---|---:|---|
| `EXACT_ALREADY_IN_PREMAIN` | 542 | exact same path and exact AST at PRE-MAIN `750548dd` |
| `SUPERSEDED_BETTER` | 73 | current PRE-MAIN same-path successor carries the same public symbol with a different AST; current code selected as the integration successor, behavioral equivalence not proven |
| `UNIQUE_USEFUL_NEEDS_ADAPTATION` | 299 | no current equivalent; branch-specific return is scoped positive/review-pending or same-name candidate exists; independent adaptation/tests required |
| `UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY` | 331 | no current equivalent; source/native/production/analytical authority is required and not granted by this investigation |
| `EVIDENCE_UNKNOWN` | 34 | no current equivalent, no exact/no-id AST match and no branch-specific verdict sufficient for a disposition |
| `INDEPENDENTLY_REBUILT_EQUIVALENT` | 0 | no cross-path exact or identifier/docstring-stripped AST match was found |
| `UNIQUE_USEFUL_READY` | 0 | no branch test or consumer was executed; static evidence cannot support READY |
| `INVALID/TRASH_WITH_GROUNDS` | 0 | no production function passed the test/repro exclusion with a latest branch-specific explicit reject/invalid/trash verdict |

Branch summaries use both a dominant `primary_branch_disposition` and a `highest_risk_disposition`: 98 branches are primarily exact-in-PREMAIN, 54 have no code function, 12 are primarily adaptation, and 11 are primarily source/actor held. The highest-risk overlay identifies 81 branches touching at least one held function and 13 touching a current same-path successor.

## Key findings

1. **Much of the S1 code estate is already exact in current PRE-MAIN.** 542 public production function/class ASTs are exact at the same path in `750548dd`; this is the dominant branch outcome.
2. **A second large class is a later same-path PRE-MAIN successor.** 73 historical public symbols share a name with current code but have a different AST. They are not declared equivalent; current PRE-MAIN is selected as the successor and the historical cut needs no separate integration unless an owner identifies a lost behavior.
3. **The largest genuinely missing cluster is the universal evidence/world/workload family.** `pre553_universal_world_binding.py` (150 held functions), `pre553_universal_evidence_binding.py` (144 adaptation + 20 unknown), `pre553_issued_workload.py` (19 held plus exact/superseded), `pre553_observed_response.py` (18 held), and the source-configuration/B5/source-read family are absent from current PRE-MAIN. These are source/authority-dependent or unverified and are not recommended for blind integration.
4. **The HQ280 durable checkpoint and original-workload candidates are real missing engineering capabilities,** but remain adaptation/evidence-unknown because this investigation did not run their tests or a consumer. Their branch returns claim 35-test and hostile-court positives; those claims are recorded as branch-return evidence, not independently re-executed.
5. **No function reached READY.** The absence is a deliberate consequence of the no-execution rule, not a claim that every candidate is bad.
6. **No independent rebuild was proven.** AST exact/no-id cross-path matching found no match between the 176 historical variants and the current 8,149-symbol index. Same-name/different-AST candidates were classified as adaptation/unknown rather than equivalence.
7. **Source and actor permissions remain separate HOLDs.** 97 branches are source/scientific-authority-held; 2 branches have a Sorok/actor dimension and remain test-only. No original source qualification, native execution, generated person, psyche, actor authority, N11/N12 or PRE-MAIN adoption is claimed.

## Three courts

| Court | Verdict | Basis |
|---|---|---|
| ENGINEERING | `INDEX_AND_DISPOSITION_COMPLETE__STATIC_AST_AND_GIT_ONLY__NO_CONSUMER_EXECUTION` | 175/175 branch rows, 1,279 function rows, exact Git/AST custody, branch/return/test evidence, no branch execution |
| SCIENTIFIC | `HOLD__NO_SOURCE_OR_NATIVE_SCIENCE_VERIFIED__ORIGINAL_OWNER_DECISION_REQUIRED` | no original survey/response execution, no source qualification, no model/semantic adoption |
| AUTHORITY | `HOLD__NO_ADOPTION__INDEPENDENT_I2_I3_HOSTILE_ADJUDICATION_REQUIRED` | this author is not the issuer or reviewer; separate hostile adjudication must follow the exact SHA |

## Reviewer independence and next hand-back

The worker is not the independent reviewer, source issuer or PRE-MAIN integrator. The exact cut must be handed to a separate I2/I3 hostile reviewer appointed after this return. No merge, adoption, registry mutation or canonical control update was performed. The reviewer should attack: exact branch-to-row mapping, the 121/54 code split, the 542 exact-current claims, the 73 same-path successor selections, the 331 source-held functions, the 34 unknown functions, the origin-vs-inherited counts, and the absence of executed tests.

## Tests and NOT_RUN

- All **868 changed test-path occurrences across 123 branches** are `NOT_RUN` by this investigation. No pytest, import, branch executable or consumer was executed.
- No original survey, SAV/response corpus, source-native execution or native C11/C12/C9/actor run occurred.
- The S1 Actions index itself reports `function_equivalence_proved=false`, `test_or_review_grade_proved=false`, `original_source_access=false`; the S0 index reports the same class of limits.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

**DONE:** exact 175-branch roster coverage; 1,279 function-level rows; exact tip/tree/merge-base/blob/AST custody; origin-vs-inherited projection; current PRE-MAIN exact/successor comparison; branch-specific return and test-name evidence; source/actor separation; negative/unverified register.

**REMAINING:** independent I2/I3 hostile adjudication; owner decisions on 299 adaptation functions and 331 authority-held functions; consumer/test execution for any function an owner wants to promote; current-head recheck if PRE-MAIN moves.

**CRITICAL BLOCKERS:** no source/scientific authority grant; no branch test/consumer execution; 43 branches lack a branch-specific return; 34 functions remain evidence-unknown; PRE-MAIN currentness must be rechecked at intake.

**LARGEST PRODUCTIVE MOVE:** have the original analytical/evidence/world-workload owners select a small set of `UNIQUE_USEFUL_NEEDS_ADAPTATION` functions (especially the universal evidence binding and durable checkpoint candidates) and authorize exact consumer tests; keep the 331 source-held functions behind the source-owner gate.

**FLIGHT:** one local sourcefree Git/AST investigation; no branch execution, no model/harness switch, no active worker worktree changed.

**DELTA:** the S1 estate now has a complete 175-branch function-level disposition map with exact custody, current equivalents, origin/inherited separation, and a defensible HOLD/adaptation frontier instead of a flat list of branch names or unsupported equivalence claims.

The exact final pushed SHA is reported externally after push. No self-adoption.
