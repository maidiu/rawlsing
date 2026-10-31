# PYAT 845 S1-EVIDENCE REPAIR — 1,279-row six-axis regrade

## Identity and session

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Role | Fresh independent I2/I3 source/code/merit regrader; NOT original S1 author, original reviewer, source/semantic issuer, S6/H1/S7 author or own hostile reviewer |
| Branch | `agent/pyat-845-s1-evidence-regrade-20261030-r1` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-845-s1-evidence-regrade-20261030-r1` |
| Device | `mainMac` (`scutil --get ComputerName`) |
| Harness / agent | OpenCode CLI `1.18.34`, agent `build` |
| Model / effort | `opencode-go/deepseek-v4.1-flash`, session variant `max` |
| Session | `ses_e7285576bffeqo0lE8N0HYK6gc` |
| Immutable original S1 return | `c85db39772a8ac09fd70c6bb94a39dd04274d2cb` |
| Frozen baseline | `750548ddbb9b4392a16ce93097b856f349e16182` |
| Actual current PRE-MAIN at regrade | `5ad805e52a4fd0dbaae3a6b91801164e74ebc6f3` |
| Shared evidence law | `f50651a2bb0758e9fe6d6a2852441dcc782344be` |
| Final pushed SHA | reported externally after push; a commit cannot contain its own hash |

## Exact source cuts

- Original S1 `FUNCTION_COURT.jsonl`: SHA-256 `dfc15e55ee3f4fdfb4327cc031786906f8274d2c72b89b6528b2a19c5e8fa149`.
- Original S1 `BRANCH_DISPOSITIONS.jsonl`: SHA-256 `e295871369aafdc091460d5129fe5d7efec07d06f8581a7daf13f76203976b90`.
- S1 roster: `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/SCOPED_ROSTER/11_S1_HEAD_ONLY_ROSTER.json`, proposal head `becf0bfb04705b8fe0927dd56e7290e1dcd180a8`, blob `146b100e7f3456fabdec2e6ed8059adf0bf8a68d`.
- S0 raw index: Actions `41137105778`; S1 source/AST index: Actions `41142495040` at `3ef4d09bc47789536802b8eae290a57db4c38122`.
- `rawlsing_next` tree is identical between frozen baseline `750548dd` and actual head `5ad805e5`; only `tests/test_copy_paste_commission_r1.py` was added. Current-presence claims were therefore revalidated against the actual head.
- No original branch return was edited. This work adds only the five contracted files under `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S1_EVIDENCE_REPAIR/`.

## Machine invariants

- `FUNCTION_GRADE_CORRECTIONS.jsonl`: **1,279** rows in original order, one for every original `FUNCTION_COURT.jsonl` row; original `function_id` order and `original_row_sha256` match all 1,279 rows; unique keys 1,279.
- `BRANCH_RECONCILIATION.jsonl`: **175** rows, exact original branch-name and tip order/set; all contradicted functions preserved.
- `RECEIVER_TEST_AND_SOURCE_PERMISSION_MATRIX.json`: **1,279** rows keyed to the same original function IDs.
- No dropped, reordered or merged function claim; no original return rewrite.

## Corrected outcomes

| Original S1 label | Rows | Corrected outcome |
|---|---:|---|
| `EXACT_ALREADY_IN_PREMAIN` | 542 | Preserved `EXACT_AST_SAME_PATH` / `NO_ACTION_CODE_PRESENT`; code presence only, **not** source/science acceptance |
| `SUPERSEDED_BETTER` | 73 | All downgraded to `DIFFERENT__COMPARISON_REQUIRED`; no behavioral superiority or current positive/fault-negative receipt was supplied |
| `UNIQUE_USEFUL_NEEDS_ADAPTATION` | 299 | 284 `HYPOTHESIZED_VALUE__NEEDS_ABI_AND_CONSUMER_TESTS`; 15 `HYPOTHESIZED_VALUE__PERMISSION_AND_TESTS_REQUIRED` |
| `UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY` | 331 | 181 `SOURCEFREE_ENGINEERING_CANDIDATE__NEEDS_ABI_CONSUMER_TESTS`; 150 `SOURCEFREE_TEST_ALLOWED__OPERATION_PERMISSION_GRANT_REQUIRED` |
| `EVIDENCE_UNKNOWN` | 34 | Retained `EVIDENCE_UNKNOWN` / `INSUFFICIENT_EVIDENCE` |

Corrected adoption counts: `SOURCEFREE_INTEGRATION_CANDIDATE` 615; `NEEDS_ABI/CONSUMER_TESTS` 480; `CURRENT_PRODUCTION_ACCEPTED_AT_NAMED_SCOPE` 150; `INSUFFICIENT_EVIDENCE` 34. No `READY_FOR_SOURCEFREE_INTEGRATION_COURT`, no proven `INDEPENDENTLY_REBUILT_EQUIVALENT`, no `INVALID/TRASH_WITH_GROUNDS`, and no new source/actor/CAN/ADP/SCI/N11/N12 permission.

## Six-axis correction

Each row now carries separate `HISTORICAL_MERIT`, `CURRENT_FUNCTIONAL_PRESENCE`, `SCIENCE_AND_THEORY`, `COMPATIBILITY`, `PERMISSION`, and `ADOPTION` axes plus `ADOPTION_SCOPE`. The permission axis independently records `SOURCE_NATIVE_READ`, `SCIENTIFIC_RULE_ISSUE`, `MODEL_USE`, `WORLD_STRUCTURAL_ADMISSION`, `N11_N12` and `SOROK_ACTOR` as `NOT_REQUIRED_FOR_SOURCEFREE_SCOPE`, `REQUIRED_UNGRANTED`, `UNKNOWN` or `NOT_REQUIRED_FOR_THIS_FUNCTION_SCOPE`. Data/class rows are not blanket-held; method-level operations are explicitly unassessed. Entrypoint rows name the exact function symbol and competent owner class where a grant is required.

## Contested claims

- **73 same-path/different-AST “better” calls:** all downgraded. Same-path AST difference is not superiority. No current behavior, consumer, positive oracle or fault-negative oracle was executed.
- **331 blanket source holds:** replaced with operation-specific permission axes and sourcefree test applicability. Sourcefree grammar, checkpoint, evidence-binding and workload engineering is not banned by a source-native read restriction.
- **299 adaptation claims:** not proof of unique capability. Path absence and same-name/different-AST candidates are hypotheses only; current ABI, consumer and negative tests remain required.
- **34 unknown rows:** retained unknown, not dropped or promoted.
- **542 exact code rows:** preserved as current code presence; no claim of original-method, source-science, model, actor or N11/N12 acceptance.

## Tests and NOT_RUN

- **No branch code, branch test, branch executable, consumer or original source/response corpus was executed.**
- All compatibility axes are `NOT_TESTED` except static AST parse and static current-reference presence. All test names are evidence locators; none are claimed as passed.
- The original branch-return claims are retained only as historical limited-scope evidence; no E3 current-receiver execution exists in this regrade.

## Unresolved mismatches

- **43 branches** still lack a branch-specific return root; their function rows are reconciled from code/current evidence only and retain `INSUFFICIENT`/`EVIDENCE_UNKNOWN` where applicable.
- **34 functions** remain `EVIDENCE_UNKNOWN`; no promotion is made.
- **Cross-shard duplicates** with R61/P41 and the mandatory H1 #534/S6 #533 join are **not self-assessed** here. S1 does not claim whole-estate uniqueness, equivalence or adoption.
- Current PRE-MAIN may move after this return; if it does, current-presence and receiver rows must be rechecked. At the final pre-commit check, actual head was `5ad805e5` with an unchanged `rawlsing_next` tree relative to frozen baseline `750548dd`.

## Three courts

| Court | Verdict | Basis |
|---|---|---|
| ENGINEERING | `REGRADE_COMPLETE__1279_ROWS_PRESERVED__STATIC_AST_ONLY` | exact original-row identity, six-axis delta, 175 branch reconciliation, no branch execution |
| SCIENTIFIC | `HOLD__NO_ORIGINAL_SOURCE_METHOD_ESTIMAND_OR_WORLD_ACCEPTANCE` | no source/response execution, no independent scientific issuance |
| AUTHORITY | `HOLD__NO_ADOPTION__H1_534_AND_S6_533_CROSS_SHARD_REVIEW_REQUIRED` | no source/actor/model/world/N11/N12 grant, no self-adoption |

## Reviewer independence and hand-back

This author is not the original S1 author, original reviewer, source/semantic issuer or own hostile reviewer. The exact committed SHA must go to the independent H1 #534 review and S6 #533 cross-shard join, then S7 #538. No merge, production-code change, original-return rewrite, protected PRE-MAIN mutation or automatic adoption occurred.

DONE: exact 1,279-row regrade and 175-branch reconciliation; all 73 superiority claims downgraded; 331 blanket holds replaced by permission-specific axes; 299 adaptation claims downgraded to hypotheses; 34 unknowns retained; 542 exact rows preserved as code presence only.

REMAINING: independent H1/S6 review; source/actor/model/world owner decisions; current receiver tests for any future promotion.

CRITICAL BLOCKERS: no source science or actor/model/world grant; no branch/current receiver execution; 43 no-branch-return branches and 34 unknown functions.

LARGEST PRODUCTIVE MOVE: H1/S6 cross-shard join of the corrected S1 rows with R61/P41 and the other 845 shards, then owner-selected sourcefree ABI/consumer tests for the small `HYPOTHESIZED_VALUE` frontier.

FLIGHT: one local sourcefree Git/AST regrade; no branch execution, no model/harness switch, no active-worker worktree changed.

DELTA: the original flat S1 labels are replaced by falsifiable six-axis rows; false superiority and blanket source holds are removed without dropping a function or branch, and every remaining unknown is explicit.

The exact pushed branch SHA is reported externally after push. No self-adoption.
