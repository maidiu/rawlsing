# Private MainMac q103 execution preparation

## Pinned inputs

Controller-only private execution directory contains:

- `inputs_private.json` — exact owner-decision path/SHA, R2 source/manifest/
  release/universe/replay binding, scope, expected denominator/oracle and
  local-only safe output path.
- `expected_private.json` — exact aggregate raw-code bins, expected owner
  interpretation, denominator inventory, duplicate policy and replay invariant.
- `parity_check.py` — future output comparison helper; not an evaluator.
- `negative/` — changed-decision, revoked-scope and wrong-release fixtures.

The owner decision file is exactly
`e3de52e027cc5418544f3f9bf72f62995ea81ce6ae6148faa000fa3b9f6a96f5`.

## Reusable preparation command

```bash
cd "$P0_WORKTREE"
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  "$P0_PRIVATE_PROOF_DIR/q006_q103_execution/q006_q103_prepare.py"
```

The denominator inventory was checked with the bounded event/locator scan; the
raw category bins were reused from the existing private qualification.

## Future execution gate

Do not run until the exact implementation is accepted. The eventual command
must consume `inputs_private.json`, write only to the private safe-output path,
and compare against `expected_private.json`.

## Verification method

- exact raw mappings: 1–4 substantive, 97 special, 98 DK, 99 refusal;
- physical missing separate;
- recorded code totals must sum to the recorded denominator;
- distinct recorded respondent occurrences, no duplicate refs/respondents;
- exact replay and unchanged source/release/current decision;
- any changed decision, revoked scope, wrong release/source or unknown code
  refuses.

No counts are published.
