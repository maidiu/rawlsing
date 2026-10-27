# Campaign A1 — SRC04 original-source C11

This bounded campaign reads only the human-authorized SRC04 Arab Barometer Wave 1
SAV on the local Mac, through the existing source-read admission owner and the
exact-SHA physical decoder. It constructs a real `C11LogicalRelease` through the
existing `source_configuration` factory and native source-backed C11 owner.

## Scope

- Source: `SRC04`, `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- Rows: 7,337; physical columns: 181; configured response slots: 178
- Release slice: the first configured response battery (ordinals 3..45) whose
  observed source values/states are all exactly bound, plus `country` and `ser`.
  This is 42 response slots and 2 coordinates.
- Exact exclusions: 15 response slots with observed values/states lacking an
  exact configured rule, and the continuous `q701` coordinate. The remaining
  complete response slots outside the first battery are not claimed.
- Original semantic authority remains `DEFER`; canonical values are withheld.
  No routing eligibility, weight, population, directional, or downstream
  empirical claim is made.
- No weight slots are declared. No original empirical workload is issued.

## Commands

```sh
PYTHONPATH=. python3 campaign_a_src04/run_campaign_a_src04.py --mode tests
PYTHONPATH=. python3 campaign_a_src04/run_campaign_a_src04.py --mode primary
PYTHONPATH=. python3 campaign_a_src04/run_campaign_a_src04.py --mode replay
PYTHONPATH=. python3 campaign_a_src04/run_campaign_a_src04.py --mode return \
  --artifact-commit <code-commit>
```

`primary` performs the actual authorized source read, physical/source-native code
audit, wrong-source and unbound/canonical negatives, and the positive slice release.
`replay` is a fresh process that re-authenticates the grant, re-reads the exact
source through the same owner, rebuilds the slice, and compares the release hash.
`return` assembles `RETURN.json` from the actual receipts.

The full release object bundle is written only under the local runtime root,
outside Git:

```text
~/Library/Application Support/Rawlsing/campaign-a-src04/releases/<bundle-id>/
```

Set `CAMPAIGN_A_RUNTIME_ROOT` only to another path outside the Git worktree. Raw
respondent cells, row-wise response artifacts, and the original source must never
be committed or uploaded.
