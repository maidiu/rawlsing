# G03-I0-RUN — one-off execution handoff

**Status:** `REVISE_EXACT_DEFECT` — the mandated relay test suite is not green; the actual P6 measurement scenario itself passes.
**Implementation HEAD:** `5cc6595409d224f5331f367e36e4f8b283fe1959` (PR #968 head verified by `refs/pull/968/head`)
**Predecessor:** `aa157f23cf7d6284c982595295301036145b7cdf`
**Evidence grade:** `SOURCEFREE_S2_INSTRUMENTATION_ONLY_CANDIDATE_PENDING_G5`
**G03_FULL:** `NOT_EVALUATED_G02_MISSING`
**G5:** `NOT_RUN`

## Runner and lease

- Host: macOS 13.7.8, Darwin 22.6.0, x86_64, host `oldMac.lan`.
- Python: 3.11.3. Git: see `git_version.txt`.
- Exclusive local lease created atomically before checkout: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/g03-i0-run-20261112T144430/LEASE.json`, SHA-256 in `ENVIRONMENT.txt`.
- Clean detached checkout at exact HEAD; `git status --porcelain --untracked-files=all` empty before and after measurement in `SOURCE_STATE.txt`.
- No Codex/OpenCode controller, paused worker, P3/P4/P5/P6 owner, native/psychological authority or protected merge was touched.
- Child environment is the source's five-key offline allowlist. Provider calls/tokens/retries/cost are `UNOBSERVED`, not zero.

## Test results

| Set | Command | Result |
|---|---|---|
| inherited A/B | `python3 -B -m unittest -v test_measure test_agent_b` | **23 passed**, exit 0, 0.415 s |
| new A relay | `python3 -B -m unittest -v test_agent_a_relay` | **2 passed, 1 failed**, exit 1, 0.271 s |
| combined mandated | `python3 -B -m unittest -v test_measure test_agent_b test_agent_a_relay` | **25 passed, 1 failed** (26 total), exit 1, 0.735 s |

Failure:

```text
FAIL: test_original_p6_p3_table_blob_text_collision
AssertionError: 2 != 0 : Original P6 new failed:
```

Exact cause: the test's `setUp` creates `state/actual-p2` before it invokes the original P6 `new` command. The original P6 refuses an existing state root:

```text
exit 2
{"status": "REFUSED", "reason": "P4_STATE_ALREADY_EXISTS"}
```

This is a test-fixture defect, not a P6 production RED. The measurement command uses a fresh state root and the five P6 attempts pass. Raw reproduction: `repro/` (stdout, stderr, exit code, source excerpt). No source patch was applied in this runner commission.

## Actual P6 measurement

Command: `measure.py --repo "$PWD" --out "$EVIDENCE"`; exit 0. Independent reader: exit 0, `expected_scenario_pass=true`.

| Attempt | Exit | Clock | Wall s | CPU user s | CPU sys s | Peak RSS bytes | State before | State after |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| new | 0 | 248 | 5.379366 | 4.672217 | 0.392117 | 52,064,256 | 0 | 1,282,124 |
| view | 0 | 248 | 2.225274 | 1.995389 | 0.161544 | 53,673,984 | 1,282,124 | 1,285,052 |
| wait 1 | 0 | 249 | 3.411117 | 2.965691 | 0.199935 | 52,486,144 | 1,285,052 | 1,390,315 |
| cold view | 0 | 249 | 2.135164 | 1.951018 | 0.133205 | 53,927,936 | 1,390,315 | 1,392,905 |
| wait 0 | 2 REFUSED | null | 2.001685 | 1.867926 | 0.114135 | 54,874,112 | 1,392,905 | 1,392,905 |

- `attempts=5`, `success=4`, `expected_refusals=1`, `unexpected_failed_or_refused=0`, `timed_out=0`, `cold_reopened=1`, `distinct_process_execs=5`.
- Wall total 15.152606 s; direct-child CPU total 14.453177 s (user 13.452241 + system 1.000936); max direct-child RSS 54,874,112 bytes.
- CPU/RSS scope is direct `wait4` child only, not the process tree. macOS `ru_maxrss` is bytes.
- Refused state: physical content changed `true`; logical content changed `false`; typed SQLite witness `G03_SQLITE_TYPED_ROWS_AND_OTHER_CONTENT_V2`; physical SQLite churn is not equated with actor change.
- Provider calls/tokens/retries/billable cost: `UNOBSERVED`.

## Independent first consumer

`read_receipts.py` exit 0; `expected_scenario_pass=true`; `index_sha256=79d737d96e4cc952d5a260efff8a99a6a913c13d7ab59143cee1a6b086a23d3b`.

This external index digest is pinned outside the raw archive in this handoff and in `RUNNER_RESULT.json`.

## GitHub Actions admission diagnosis

Run `#43288957593` was not reachable through the current fine-grained token:

- run, jobs, check-runs, attempt-2, timing, Actions permissions and billing APIs: `403 Resource not accessible by personal access token`;
- commit status for `5cc6595`: HTTP 200, `total_count=0`, `state=pending`;
- GitHub Status: `All Systems Operational`.

The exact check-run annotation bodies, billing/usage and repository/organization runner policy remain **NOT_ACCESSIBLE / UNVERIFIED** with this token scope. Billing limit, runner provisioning, policy and security are hypotheses, not verified causes. The failed hosted jobs executed no source; this run does not label them implementation RED.

## Seven case outcomes

| ID | Outcome | Evidence |
|---|---|---|
| I0-P01 | PASS | P6 `new` + `view` exit 0, clock 248 |
| I0-P02 | PASS | `wait 1` clock 249; `cold_view` exit 0, clock 249; `cold_reopened=1` |
| I0-N01 | PASS | `wait 0` exit 2, exact `P6_WAIT_DURATION_OUT_OF_RANGE`/REFUSED, logical state unchanged |
| I0-N02 | REVISE | actual-P6 BLOB/TEXT relay test fails before assertion because its fixture precreates the state root; simple typed-collision test passes |
| I0-N03 | PASS | uncheckpointed WAL refused, not misreported as logical |
| I0-R01 | PASS | exact HEAD, clean tree, no P3/P4/P5/P6 owner diff |
| I0-M01 | PASS | actual five-child wall/CPU/RSS/state bytes recorded |

Exact issue #949 case text was not retrievable with the current token scope; this mapping is derived from the pinned receiving status and the observed commands, and is not a claim about unread text.

## Gates at tested SHA

| Gate | State | Basis |
|---|---|---|
| G1 | PASS | exact HEAD, clean tree, source hashes, seven ID set, no owner edit |
| G2 | PASS | five actual P6 children and independent reader, `expected_scenario_pass=true` |
| G3 | FAIL | mandated relay suite has one test-fixture failure |
| G4 | PASS | durable raw receipts, index and independent reader |
| G5 | NOT_RUN | separate independent nonauthor reviewer not assigned |

## Evidence

- Raw evidence tree: `evidence/raw/` (44 files, manifest, index, summary, 5 attempts, sourcefree state).
- Test logs: `tests.*`, `inherited23.*`, `relay3.*`.
- Reproduction: `repro/`.
- Admission API receipts: `admission/`.
- Archive and external SHA-256: printed in the final return; the archive is committed with this handoff on the runner branch.

## Limits

No process-tree RSS, no authenticated provider/token/cost observation, no cold kernel-cache proof, no Linux/GitHub-hosted sample, no G02 cohort, no native science, actor/human authority or protected merge. The failed relay test is a test-fixture defect; the instrument itself is not thereby declared RED.
