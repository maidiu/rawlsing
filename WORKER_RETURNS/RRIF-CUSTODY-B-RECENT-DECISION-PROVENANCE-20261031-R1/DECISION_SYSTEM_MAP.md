# Decision system map — recent RRIF branch estate

**Scope:** 845 frozen branch names / 838 distinct tips from PR #515 and E8 `BRANCH_ROSTER_845.json`; source cut `8e44ca9c751049d65e6def47600b5c073ee04b29`; roster source `becf0bfb04705b8fe0927dd56e7290e1dcd180a8`; E8 ledger `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`. This is a sourcefree Git/documentary reconciliation, not a new HQ or adoption.

## 1. What counts as a decision

A branch name, a green test, an author return or an E8 family status is not an HQ decision. This reconciliation separates:

1. **Worker candidate returned** — a branch-local return, disposition or completion packet.
2. **Independent reviewer verdict** — a distinct reviewer branch/return stating `ACCEPT`, `REVISE`, `HOLD`, `REJECT` or `FAIL`.
3. **HQ decision** — a decision-ledger row, checkpoint disposition/adoption, or integration-branch acceptance naming the branch/commit.
4. **Integration/staging incorporation** — a branch contains the candidate commit, but does not itself prove HQ acceptance or PRE-MAIN retention.
5. **PRE-MAIN retention** — the exact commit is an ancestor, or exact code blobs are present at the same paths. Acceptance and retention are reported separately.

## 2. Where decisions actually lived

| System | Exact source | What it can prove | Limits |
|---|---|---|---|
| Central decision ledger | `HQ_HANDOFF/DECISION_LEDGER.jsonl` | 444 appended HQ rows; 323 dated, 121 date-less | Two generations; `code_adopted` absent on 324 rows and `false` on 120; no `true` |
| HQ checkpoints | `HQ_HANDOFF/checkpoints/*/CURRENT.json` | 452 branch-return/disposition snapshots | Many are active-worker metadata, not decisions |
| Branch-local HQ adoption | `00_HQ_ADOPTION.md`, `00_INTEGRATION_RECEIPT.md` | Exact accepted implementation/branch/reviewer/scope | Not appended to the central ledger |
| Reviewer returns | `00_RETURN.md`, `00_REVIEW.md`, `*_FINAL_DISPOSITION.json` | Bounded independent verdicts | Reviewer independence is asserted, not re-run here |
| Accepted integration branches | `integration/pyat-hq*-accepted-r1` | HQ code adoption at a branch tip | Most are not ancestors of current PRE-MAIN |
| PR merges | #525, #526, #563 merge commits | Later code/control recovery into PRE-MAIN | PR descriptions/reviews inaccessible via API |
| E8 family ledger | `ALL_1885_FAMILY_DISPOSITIONS.jsonl` | Functional identity/disposition at 1,885-family grain | Not a branch-level acceptance ledger |

The central ledger has two incompatible generations. The older rows use `decision_id/date/status/subject/holding/authority_refs`; the newer rows use `id/checkpoint_id/decision/director_evidence/code_adopted`. A missing `code_adopted` is not `false`; `code_adopted:false` means only that this row did not adopt code, not that no code was adopted elsewhere. A historical `ACCEPT` or `ADOPTED` may cover evidence, design, a bounded grain or a handoff, not a merge.

## 3. Chronology

| Date / commit | Event | Consequence |
|---|---|---|
| 2026-09-27 18:56:30Z `ef46892f` | Last dense regular `rawlsing_next` implementation-tree commit | Conservative start of the stopped-integration window |
| 2026-09-29 to 2026-10-01 | C3, C1-01, C1-02, N10E, C5/N5, C1-03R, C1-03A, AT07 and C1-03 join accepted on `integration/pyat-hq*-accepted-r1` | Decisions and code adoption exist, but on integration branches |
| 2026-10-04 to 2026-10-09 | Sparse transition receipts; last code touch `79e0e74e` at 2026-10-09 22:31:19Z | Branch returns continue; central code fan-in becomes sporadic |
| 2026-10-10 to 2026-10-27 | Branch-return estate expands; ledger R-series decisions continue | Rows repeatedly record `code_adopted:false`; branch-local adoption/reviewer evidence carries the disposition |
| 2026-10-30 `99951b87`, `750548dd` | PR #525/#526 code recoveries into PRE-MAIN | No central-ledger row for either merge commit |
| 2026-10-31 `8e44ca9c` | PR #563 S7FIX acceptance into PRE-MAIN | Current PRE-MAIN; PE RED and V2K retirement preserved; no production import |
| 2026-10-31 `e95d6edb` | E8 1,885-family functional disposition | Later functional ledger, not a substitute for branch acceptance |

## 4. Continuity failure

- The central ledger did not stop completely; it stopped being a complete branch-level acceptance record. Recent decisions were recorded in checkpoints, branch-local adoption docs and reviewer returns.
- Nine accepted `integration/pyat-hq*-accepted-r1` branches exist. Their exact code retention at current PRE-MAIN is uneven: 4 all-exact, 1 partial, 3 no exact current blob, 1 no code delta.
- Many accepted integration branches are **not ancestors** of current PRE-MAIN. Their code was accepted on a separate branch and may have been adapted, superseded or never incorporated.
- PR #519's control PR is based on `299f41e9`, not current PRE-MAIN; reviewed/accepted is not merged.
- Branch creation timestamps do not exist in Git. All dates here are tip/commit dates; a branch created later on an old commit can be missed by a tip-date proxy.

## 5. Recovered coverage

Decision-record sources: **51** central-ledger records, **72** independent-review returns, **9** checkpoint dispositions, **3** PR merge records (135 records total). A single ledger row may name more than one branch; the fate ledger reports the primary decision per branch.

- **845** branch rows, **845** unique names, **838** unique tips, **7** duplicate-tip groups.
- **155** branches have a primary HQ/checkpoint/reviewer decision record.
- **72** branches have an explicit reviewer verdict.
- **595** branches carry a candidate-return signal.
- **694** branches are explicitly reported as candidate/documented/control without a located HQ decision.

## 6. Limits

- GitHub issue/PR/review APIs return `403 Resource not accessible by personal access token`; issue #574, PR descriptions, reviews and comments could not be read.
- Branch-local document inheritance is common. The extractor used branch-specific paths/frequency and exact branch/head matching; it does not treat inherited templates as the branch's own decision.
- `code_adopted`, E8 `RETIRE`/`HOLD_EXACT_DECISION`, and reviewer `ACCEPT` are scoped by their own documents; none is promoted to whole-family or production acceptance.
- This map does not adjudicate pending reviews or relaunch work.

## 7. Validation and custody

- Evidence worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-rrif-custody-b-20261031`; branch `review/pyat-rrif-custody-b-recent-decision-provenance-20261031-r1`; HEAD `8e44ca9c751049d65e6def47600b5c073ee04b29`; no PRE-MAIN, PR #519, E8, seed or progress mutation.
- `RECENT_BRANCH_FATE_LEDGER.jsonl`: **845** rows, exact roster order, **845** unique names, **838** unique tips, **7** duplicate-tip groups.
- `RECENT_DECISION_PROVENANCE.jsonl`: **135** JSON records — 51 HQ ledger, 72 reviewer, 9 checkpoint, 3 PR merge.
- `DISPOSITION_TO_FUNCTION_CROSSWALK.jsonl`: **135** JSON records; **12** file-set mappings, **123** branch/decision scope mappings; **0** whole-family promotions.
- All JSONL files parse as one JSON object per line. Candidate-return flags are booleans. Duplicate-tip and accepted-integration links are explicit.
- GitHub API remained `403 Resource not accessible by personal access token`; no issue/PR review text was fabricated.
- Branch creation time is not a Git property; tip dates are recorded as tip dates, never as creation proof.
