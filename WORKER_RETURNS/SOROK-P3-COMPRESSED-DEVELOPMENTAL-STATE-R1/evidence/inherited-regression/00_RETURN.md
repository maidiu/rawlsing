# Inherited #704 regression — actual return

## Status

**PASS — inherited accepted engine compatibility regression executed on the
current integrated checkout.** This is author-run evidence only, not
independent review or P3 full-task acceptance.

- Startup: `d1a6817b3210880812f68090bcd2b1109ec68ef9`
- Branch: `agent/sorok-p3-inherited-regression-20261106-r1`
- Protected base: `c852d7516e23fcb6cf2215e9be7c5fa268503516`
- No runtime/source/test edits were made. Writes are limited to
  `evidence/inherited-regression/`.

## #704 source preservation

`git diff --name-status c852d751... -- <engine-root> <#697-closure-root>`
returned **empty**. Therefore the accepted engine root and pinned #697 closure
root are byte-identical to protected base at this checkout.

Key source pins:

| Path | SHA-256 |
|---|---|
| `.../developmental_recursion/contracts.py` | `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d` |
| `.../developmental_recursion/engine.py` | `ba6caa74b2c57e567dbefa57571bc931bac8e4e5108bf844efe2966754ae9586` |
| `.../developmental_recursion/model_cycle.py` | `af83f8f1a3d31c4281dc2550e07fa0e5c31304cfd3fb1bc9538f674c95f46df5` |
| `.../developmental_recursion/p2_owner.py` | `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0` |
| `.../SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/SOURCE_MANIFEST.json` | `2535398efa2c376731aec17cd7b2ceda2e0fee477f064ae049870393b838b94b` |

Full engine and closure source pins, including suite-file hashes, are in
`PROTECTED_PINS.json`.

## Executed 71-test engine suite

Exact documented command:

```text
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests
```

Observed:

```text
71 passed in 286.10s (0:04:46)
```

`/usr/bin/time -p` observed `real 286.84`, `user 276.52`, `sys 6.26`. The
accepted #704 baseline was 279.35s; this is the same suite, not a new
performance gate. Full output is in `engine71.log`; timing is in
`engine71.time`.

No tests were renamed, deleted, skipped, filtered or plugin-modified.

## Cold-process result

Exact documented command:

```text
python3 -B WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/run_cold_cli_witness.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/inherited-regression/cold_cli.json
```

Observed receipt:

- `commands`: `bootstrap`, `advance`, `finish`
- `model_modes`: `BOOTSTRAP`, `ORDINARY`, `TERMINAL`
- `batch_event_counts`: `[3, 3, 0]`
- `retrospective_count`: 2
- `same_root`: true
- `cold_verified`: true
- `before_clock`: 222; `after_clock`: 258
- `provider_calls_between_events`: 0
- actual wall time: `200.21s` (`real`)
- receipt: `cold_cli.json`; log: `cold_cli.log`; timing: `cold_cli.time`

This demonstrates three cold processes using the same actual root, two
retrospectives and no between-event provider call.

## Limits

- This is inherited compatibility proof only; it does not accept P3 code,
  run the 13 new full P3 cases, establish full A–H or resource acceptance,
  review independently, merge or issue native science.
- The full actual P3 vertical harness remains owned by the separate harness
  author/reviewer.
- No source/native/memory/claim/B/human/production/CAS/protected merge
  authority is exercised.
- The prior P3 evidence directories were not modified; this return adds a
  separate `inherited-regression/` evidence directory only.
