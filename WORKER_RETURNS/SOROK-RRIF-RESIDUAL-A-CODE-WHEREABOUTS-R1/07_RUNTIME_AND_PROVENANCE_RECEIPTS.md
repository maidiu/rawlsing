# RUNTIME AND PROVENANCE RECEIPTS

## Harness, model, host, and effort

| Field | Observed value |
|---|---|
| Host | `mainMac` (`scutil --get ComputerName`); macOS 13.2.1 x86_64 |
| Harness | OpenCode 1.18.34, agent `build` |
| Provider/model | `opencode-go/deepseek-v4.1-flash` |
| Session variant | `max` |
| Session id | `ses_e6b415bc2ffePeFOG07HecrJxc` |
| Process argv | `opencode run --dir …/sorok-rrif-residual-a-code-whereabouts-20261031-r1 --model opencode-go/deepseek-v4.1-flash --variant max --agent build --title SOROK RRIF residual A 97 code whereabouts --auto --format json …` |
| Actual session DB row | `session.model = {"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`, `agent=build`, `version=1.18.34` |
| Git | 2.43.0 |
| Python | 3.11.3 |

Model/provider/host/editor were not switched. Provider-side effort/account quota is not visible from
inside the session; the local session row proves `variant: max` was active.

## Git cuts and readbacks

| Item | Exact value |
|---|---|
| Assigned branch | `research/sorok-rrif-residual-a-code-whereabouts-20261031-r1` |
| Branch start tip | `8989b59488fb3da1290a7f71fc0b0a7aca434777` |
| Frozen Gate01 input commit | `bbc65ea28dcebdd38507ca270c0a642a7c0290bd` |
| Gate01 content commit | `dfb161655ffc4e90eea6a79db69a73f5664a295d` |
| Current PREMAIN start readback | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Current PREMAIN end readback | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Remote PREMAIN readback command | `git ls-remote origin refs/heads/integration/pre-main-reconciliation-r1` |
| Remote branch start readback | `8989b59488fb3da1290a7f71fc0b0a7aca434777` |

`origin/main` is an older canonical line (`25830fe7462b...`); the frozen comparison and live
PREMAIN read use `integration/pre-main-reconciliation-r1` exactly as commissioned.

## What was actually read/checked

- All 97 pinned tips resolved with `git rev-parse` / `git cat-file` (all present; all equal their
  frozen remote branch tips).
- Primary source paths/blobs checked against the current PREMAIN tree: **0/97 blobs, 0/97 paths**.
- Branch-local changed files inspected by diff against the nearest known 97/accepted ancestor, or
  against the substantive implementation commit for branches without such an ancestor.
- Actual S37-S52 `s37/`...`s52/` packages inspected, not just the shared `candidate/__init__.py`.
- Later carrier trees inspected: RRIF R2/R3 (`248618e6`), I1 (`7d44e300`), G17 repair
  (`8b9a39da`), RA-D (`6d3610c5`), F0-R3 (`70470a9f`), M04R (`8f200fd6`), OC5 (`e8b127b6`),
  C0RI (`5abd3c5d`), HR1 BP2P4J repair (`0636d257`), BP4R (`693d25bf`), C0P/C0R2.
- Exact blob carriers checked with `git ls-tree` and `SOURCE_MANIFEST.json`; no semantic
  equivalence was inferred from name/path alone.
- `git diff HEAD -- WORKER_COMMISSIONS/SOROK-RRIF-RESIDUAL-A-CODE-WHEREABOUTS-R1` is empty;
  neither commission file was modified.
- No RRIF/PREMAIN/source-owner branch was written. Output writes were confined to
  `WORKER_RETURNS/SOROK-RRIF-RESIDUAL-A-CODE-WHEREABOUTS-R1/`.

## Test execution honesty

- **Original branch code was NOT executed.**
- **No original survey/native world/actor/person generation was run.**
- Later-carrier test/JUnit results are quoted from their returns; they were **NOT_RUN** by this
  investigator. Specifically:
  - RRIF R2 **20/20** and R3 extension **9/9** (carrier return; not rerun here).
  - I1 **50/50** (carrier return; not rerun here).
  - G17 repair **14/14** reviewer and **13/13** author (carrier return; not rerun here).
  - RA-D **131 focused tests** (carrier return; not rerun here).
  - M04R **51/51** and **587/587** (carrier return; not rerun here).
- `06_COVERAGE_AND_MUTATION_CHECKS.json` records the static coverage/mutation checks that did run.

## Final publication

- Output content commit: `30e6f3553e9dc4b6fab33b5c978a01e0bce760eb` (9 files, 1465 insertions).
- Push: normal non-force push to `origin/research/sorok-rrif-residual-a-code-whereabouts-20261031-r1`.
- First remote readback: `30e6f3553e9dc4b6fab33b5c978a01e0bce760eb` (matches content commit).
- A readback-only follow-up commit records this receipt. The final remote tip is reported in the
  terminal response; it is not embedded in this file to avoid a self-referential commit hash.
- No PR, merge, self-adoption, self-dispatch, or future work was performed.
