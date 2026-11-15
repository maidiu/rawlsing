# Independent execution record

## 1. Host and interpreter

- Host: `oldMac.lan`, Darwin 22.6.0, x86_64 (macOS 13.7.8), 16 CPUs, 16 GiB RAM.
- Python: `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python` 3.11.3.
- pytest: 9.1.1.
- Model/session: `opencode-go/deepseek-v4.1-flash`, session `ses_e221462b9ffeDc6SKxZGtXojUH`; variantMAX availability accepted from the user's verified launch, but provider checkpoint/org/quota and token/cost metadata are `UNOBSERVED`.
- No provider calls were made by the tests; the P6 first-consumer probe injects its own interpret callback, and the P6/CLI tests are local.
- No GitHub Actions, hosted CI, browser, subagent, VM, server, install or protected merge was used.
- Every test command used `TMPDIR=/Users/matthewsmith/.codex/worktrees/sorok982-composite-g5/Rawlsing/.local-logs/sorok982-composite-g5/tmp`, `PYTHONDONTWRITEBYTECODE=1`, `python -B`, and `-p no:cacheprovider`. `/usr/bin/time -l` captured wall time and peak RSS.
- Raw logs are in `WORKER_REVIEWS/SOROK982_COMPOSITE_G5_R1/evidence/`.

## 2. RED at the unmodified #992 cut

The base source was materialized from `4cbf67398d742eeab0853d047b6c2239c84b8348` with `git archive` into assigned scratch; the original hostile test blob `a1453e799d98b4c47d26c56a12d1d2695bd42557` was extracted from `c597024bb250f014f9a616006f10172ed53e4357` to its original review path. No product file in the review checkout was changed.

```bash
git archive 4cbf67398 | tar -x -C .local-logs/sorok982-composite-g5/base-4cbf67398
git cat-file blob a1453e799d98b4c47d26c56a12d1d2695bd42557 \
  > .local-logs/sorok982-composite-g5/base-4cbf67398/WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_hostile_stale_receipt.py
# run from that base tree:
TMPDIR=.../.local-logs/sorok982-composite-g5/tmp PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/time -l /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_hostile_stale_receipt.py
```

Result: `EXIT=1`, **1 failed in 29.85s**, max RSS 61,222,912 bytes. The assertion is `assert True is False` at test line 33: the old authentic receipt is accepted as current actor access. Log: `evidence/RED_base_4cbf67398_hostile.log`.

## 3. GREEN at the composite cut

All commands were run from the exact checkout at `d5cf0c9c9925eb75c21c9a70793947f857917959` (`ff30c13ee` code/test). Suites were run sequentially within this worker; no test campaign was multiplied.

| Group | Exact paths | Result | Exit | Wall | Max RSS | Log |
|---|---|---|---|---|---|---|
| Repair 7: current operation + original stale + D1 | `test_current_operation_binding.py`, `test_g5_stale_receipt.py`, `test_d1_receipt_currentness.py` | 7 passed | 0 | 162.66s | 64,974,848 | `GREEN_repair_7.log` |
| P4 #992 source-owner | `test_p4_scope_owner.py` | 7 passed | 0 | 149.87s | 63,111,168 | `GREEN_p4_scope_7.log` |
| Agent B #986 scope | `test_scope_source.py` | 6 passed | 0 | 149.88s | 58,404,864 | `GREEN_agent_b_scope_6.log` |
| Agent A/B + P4 CLI + P5 | `test_cue_issuer.py`, `test_bridge.py`, `test_cli.py`, `test_experience.py` | 14 passed | 0 | 489.50s | 61,026,304 | `GREEN_ab_p4cli_p5_14.log` |
| P6 initiative/hostile/scene/MII | `test_actor_initiative.py`, `test_actor_initiative_hostile.py`, `test_actor_scene_context.py`, `test_mii.py` | 45 passed | 0 | 915.33s | 68,431,872 | `GREEN_p6_45.log` |
| Original six-group #977 baseline | receiver baseline + Agent A + causal bridge + P3 vertical slice + P4 response + P6 house | 37 passed | 0 | 3241.23s | 69,795,840 | `GREEN_37_baseline.log` |
| Named decisive assets | original G5 hostile, D1 contract, internal-trust receiver probe | 3 passed | 0 | 39.33s | 64,782,336 | `GREEN_named_decisive.log` |
| Reviewer independent probes | `test_review_independent_g5.py` | 2 passed | 0 | 53.11s | 60,628,992 | `GREEN_reviewer_independent_r3.log` |

The 37-test command was:

```bash
TMPDIR=... PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -l \
  /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-982-COMPOSITE-R1/test_receiver_977_baseline.py \
  WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py \
  WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
```

The other commands in the table use the same interpreter/TMPDIR/time wrapper with the listed paths. The 37-test receiver asset is the source-pinned blob `2b489ba1edd0698ead4899fe64abe19e9f7f4cce`, byte-identical to `9d3d8ae419998a3e13d88f58147756149e3dddb5:WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_receiver.py`.

## 4. Named decisive result

```text
test_old_authentic_receipt_cannot_be_replayed_as_current_operation PASSED
test_stale_authentic_receipt_is_not_current_authorization PASSED
test_explicit_internal_trust_boundary_not_mistaken_for_protected_source PASSED
3 passed in 39.33s
```

This confirms the original hostile asset is unweakened and the D1 contract and internal-trust hold are green at the same source head as the P4 #992 scope-owner group.

## 5. Reviewer probe corrections (disclosed)

The reviewer-authored probe was corrected twice before passing; neither correction weakened a safety assertion:

1. Initial run: `KeyError: 'p3_record_readset'` because the live packet field is `sourcefree_p3["readset"]`; the private P4 receipt names it `p3_record_readset`. Fixed the comparison only. Log: `GREEN_reviewer_independent.log` (1 failed, 1 passed, 86.82s).
2. Second run: `TypeError: 'WorldState' object is not subscriptable` because `session.world()` returns a `WorldState`; changed to `.actor_state`. Log: `GREEN_reviewer_independent_r2.log` (1 failed, 1 passed, 40.71s).
3. Final run: 2 passed, 53.11s. Log: `GREEN_reviewer_independent_r3.log`.

The same-clock identity probe is `evidence/inspect_same_clock.py`; its raw output is `evidence/same_clock_identity_probe.txt`. It is exploratory sourcefree evidence, not a substitute for the author's test.

## 6. Replay

To replay the GREEN groups, run the table commands from the exact cut in the table order or separately. To replay the independent probe:

```bash
TMPDIR=... PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider \
  WORKER_REVIEWS/SOROK982_COMPOSITE_G5_R1/test_review_independent_g5.py
```

To replay RED, re-materialize `4cbf67398` with `git archive`, copy blob `a1453e7...` to the original review path, and run the base command in section 2. The reviewer checkout itself is never edited to make RED.

## 7. Not run / held

- GitHub Actions or any hosted CI; no dispatch.
- Protected PRE-MAIN merge or staging branch.
- Full crash-injection recovery; only same-request retry conservation, cold reopen, pending reconciliation and fail-closed owner-reader behavior were exercised or inspected.
- Native CAN-008 Rule A, CAN-011 Rule T, memory/transfer/`NO_CHANGE`, actor/human rights, production grant and scientific authority.
- Provider token/cost/checkpoint/org/quota telemetry: `UNOBSERVED`.
