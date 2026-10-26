# Review environment

| Item | Observed |
|---|---|
| Host | macOS 13.7.8 / Darwin 22.6.0 / x86_64 |
| Python | 3.11.3 (`/usr/local/bin/python3`) |
| pytest | 9.1.1 |
| numpy | 2.4.6 |
| Git | 2.39.1 |
| GitHub CLI | not installed |
| Review worktree | isolated worktree outside active worker worktrees |
| Review branch | `agent/reviewer-sorok-20261026-ra-d-independent-runtime-evidence-r1` |
| Review HEAD at start | `007d94a155cd42a89de35b141fec5ca2139f6365` |
| Review target | `6d3610c576dc0ef3ceccbf7ac122c197f22be6fa` |
| Source extraction | disposable `git archive` of `c821b488…` (S36/S37/S39–S49/S51/S52) plus `515b9a8e…` (S50) |
| S52 Python files | 183/183 exact against the commit |
| S50 selected source files | 31/31 exact |
| Provider calls | 0 |
| Raw data calls | 0 |
| Accepted-source edits | 0 |
| Production writes | 0 |
| Native grants | none |

**Isolation:** the review worktree was created from the sealed startup commit. Source extraction and runtime state were kept outside the repository in a disposable scratch directory. Only review artifacts were written under `WORKER_RETURNS/SOROK-20261026-RA-D-INDEPENDENT-EVIDENCE-REVIEW-R1/`.

**Scratch bootstrap note:** the vendored M35 bootstrap discovers the repository root by looking for a `.git` directory. The disposable archive root received an empty `.git` directory marker solely to satisfy that path discovery. No git repository semantics were used in the archive.

**External roots:** G18, JOIN-E, language mediation and the historical V3 bundle were read only. Their exact hashes are in `SOURCE_INDEX.json`.

**No provider/model call:** all executions were local Python/pytest; S48 remains a fake-runner/test-only path.
