# G03-I0-RUN R2 — successor-head retest

**Status:** `PASS_G1_G4_AT_SUCCESSOR_HEAD__G5_NOT_RUN`
**Implementation HEAD:** `bfe420af96e401342b4d36b942532057a4871575` (PR #972 head; exact `refs/pull/972/head`)
**Prior runner HEAD:** `5cc6595409d224f5331f367e36e4f8b283fe1959`
**Predecessor:** `aa157f23cf7d6284c982595295301036145b7cdf`
**G03_FULL:** `NOT_EVALUATED_G02_MISSING`
**Evidence grade:** `SOURCEFREE_S2_INSTRUMENTATION_ONLY_CANDIDATE_PENDING_G5`

## Change under test

`git diff --name-status 5cc6595 bfe420af` shows exactly one file:

```text
M WORKER_RETURNS/SOROK-G03-I0-P6-MEASUREMENT-R1/test_agent_a_relay.py
```

No P3/P4/P5/P6 producer, actor/world owner or protected source was edited. The change repairs the fixture that precreated the P6 state root.

## Runner and lease

- Fresh exclusive lease created before checkout: `LEASE.json`; host macOS 13.7.8, Darwin 22.6.0, x86_64, Python 3.11.3.
- Fresh detached checkout at exact HEAD; clean `git status --porcelain --untracked-files=all` before and after measurement (`SOURCE_STATE.txt`).
- Child environment is the source's five-key offline allowlist. Provider calls/tokens/retries/cost `UNOBSERVED`, not zero.

## Tests — PASS

Command:

```bash
python3 -B -m unittest -v test_measure test_agent_b test_agent_a_relay
```

Result: **26 passed, 0 failed**, exit 0, 5.334 s. The previously failing `test_original_p6_p3_table_blob_text_collision` now passes.

## Actual P6 measurement — PASS

`measure.py` exit 0; independent `read_receipts.py` exit 0; `expected_scenario_pass=true`.

| Attempt | Exit | Clock | Wall s | CPU user s | CPU sys s | Peak RSS bytes | State before | State after |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| new | 0 | 248 | 5.776975 | 4.957708 | 0.447750 | 52,699,136 | 0 | 1,282,145 |
| view | 0 | 248 | 1.790098 | 1.649552 | 0.115278 | 53,792,768 | 1,282,145 | 1,285,073 |
| wait 1 | 0 | 249 | 2.802581 | 2.530596 | 0.161629 | 55,087,104 | 1,285,073 | 1,390,336 |
| cold view | 0 | 249 | 1.916811 | 1.790627 | 0.111073 | 54,530,048 | 1,390,336 | 1,392,926 |
| wait 0 | 2 REFUSED | null | 1.953972 | 1.807017 | 0.114417 | 55,173,120 | 1,392,926 | 1,392,926 |

- `attempts=5`, `success=4`, `expected_refusals=1`, `unexpected_failed_or_refused=0`, `timed_out=0`, `cold_reopened=1`, `distinct_process_execs=5`.
- Wall total 14.240436 s; direct-child CPU total 13.685647 s (user 12.7355 + system 0.950147); max direct-child RSS 55,173,120 bytes.
- Refused state: physical content changed `true`; logical content changed `false`; typed witness `G03_SQLITE_TYPED_ROWS_AND_OTHER_CONTENT_V2`.
- Provider calls/tokens/retries/billable cost: `UNOBSERVED`.

## Independent first consumer

`read_receipts.py` exit 0; `expected_scenario_pass=true`; index SHA-256:

```text
dca3959d8b0876968bc4f6f4aa2eb0394133d1e002d62ac6d20f29cb0a2cdc73
```

## Seven case outcomes

| ID | Outcome | Evidence |
|---|---|---|
| I0-P01 | PASS | P6 `new` + `view` exit 0, clock 248 |
| I0-P02 | PASS | `wait 1` clock 249; `cold_view` exit 0, clock 249; `cold_reopened=1` |
| I0-N01 | PASS | `wait 0` exit 2, exact refusal, logical state unchanged |
| I0-N02 | PASS | actual-P6 BLOB/TEXT relay test now passes; typed collision detected |
| I0-N03 | PASS | uncheckpointed WAL refused, not misreported |
| I0-R01 | PASS | exact HEAD, clean tree, only the test file differs from prior runner SHA |
| I0-M01 | PASS | actual five-child wall/CPU/RSS/state bytes recorded |

Exact issue #949 case text was not retrievable with the current token scope; mapping derives from the pinned receiving status and the observed commands.

## Gates at successor HEAD

| Gate | State | Basis |
|---|---|---|
| G1 | PASS | exact HEAD, clean tree, source hashes, one-file test-only diff |
| G2 | PASS | five actual P6 children and independent reader at `bfe420af` |
| G3 | PASS | 26/26 hostile suite passes |
| G4 | PASS | durable raw receipts, index and independent reader |
| G5 | NOT_RUN | separate independent nonauthor reviewer not assigned |

## Evidence

Raw tree `evidence/raw/`, test/measure/reader logs, `SOURCE_STATE.txt`, `LEASE.json`, `ENVIRONMENT.txt`, `RUNNER_RESULT.json`, `TEST_RESULTS.json`. Archive SHA-256 printed in the final return and recorded alongside the committed archive.

## Limits

No process-tree RSS, no authenticated provider/token/cost observation, no cold kernel-cache proof, no Linux/GitHub-hosted sample, no G02 cohort, no native science, actor/human authority or protected merge. This is execution evidence, not independent G5 acceptance.
