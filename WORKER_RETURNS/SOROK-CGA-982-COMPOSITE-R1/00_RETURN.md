# SOROK CG-A #982 composite corrective return

**Author disposition:** `DELIVERED_FOR_INDEPENDENT_G5`. This is not a G5 acceptance and not an integration approval.
**Frozen base:** `4cbf67398d742eeab0853d047b6c2239c84b8348` (PR #992 report HEAD), whose implementation/test commit is `6f1bc8894d1151d0921140e72bb43f5d1bb50fae`.
**Successor branch:** `agent/sorok-cga-982-composite-stale-receipt-20261113-r1`.
**Final implementation/test HEAD:** `ff30c13eea54e37e2dc8edfa73a7c7447127b735`.
**Final report HEAD:** the commit containing this return; verify with `git rev-parse HEAD`. Its only changes over `ff30c13ee` are this return and its evidence.
**Protected work:** PR #992, PR #986, PR #976, the D1 author branch, the G5 review branch and protected PRE-MAIN were not rewritten or merged.

## 1. Two defects, both closed

### Defect A — P4 source-owner scope redirection

Preserved exactly from PR #992. The four foreground scope fields are validated against the unique source-issued P3 `FORMATION` plan before P4 pending, speech admission, world mutation or actor expression. `response.qualified_scope` validates the plan source/registry/hash; `response.read_response` validates its own scope; `run_p4.act` validates exact keys before pending; `sourcefree_p3_bridge.qualified_p4_scope` delegates to the P4 owner. P4 blobs remain byte-identical to #992.

### Defect B — stale authentic P6 event treated as current actor access

The G5 hostile test at `c597024bb250f014f9a616006f10172ed53e4357` reproduced the defect at the unmodified #992 cut: an authentic `APPROACH` receipt at clock 248 was still accepted after `WAIT 4` advanced the world to clock 253 with a caller interval `{start:247,end:253}`.

The correction binds authority to the latest owner-issued S46 interval state and to the unique `P6_HOUSE_CONDUCT` committed inside the operation that produced that state. The caller interval is only a request to be matched against owner state; it is not authority. No comparison of two caller-editable interval fields grants access. See `01_DEFECT_AND_BINDING.md`.

## 2. Received prior #982 author return

The existing D1 author branch `agent/sorok-cga-g5-d1-current-receipt-repair-20261112-r1` at `4952f62ea1aa175d6ea6b83d8f6beb488e12befb` was read and left unmodified. Its frozen contract is preserved by byte-identical copies of its two test files in this return:

- `test_g5_stale_receipt.py` blob `a1453e799d98b4c47d26c56a12d1d2695bd42557` (original G5 hostile asset).
- `test_d1_receipt_currentness.py` blob `30701f83ee7dcc37aa3cf958a7224cd6229b6816` (D1 contract).

The D1 nine-line interval-equality patch is **not** copied. Its tests pass, but its mechanism relied on comparing caller-editable fields, which is not the security boundary required by #982. This branch composes the stronger owner-state binding on the #992 lineage without changing D1's branch or its frozen contract.

## 3. Exact execution results

Unmodified base RED, original G5 test blob, exit 1:

```text
1 failed in 10.43s
assert current_p3_actor_access(..., source_receipt=old) is False
AssertionError: assert True is False
```

Final source cut `ff30c13ee`, local execution only:

| Group | Result | Exit | Log |
|---|---|---|---|
| Six-group #977 baseline | 37 passed in 2273.44s | 0 | `evidence/GREEN_37_baseline_final.log` |
| New current-operation + original stale + D1 contract | 7 passed in 89.76s | 0 | `evidence/GREEN_repair_final.log` |
| P4 source-owner #992 | 7 passed in 66.07s | 0 | `evidence/GREEN_p4_scope_owner_final.log` |
| Agent B #986 scope | 6 passed in 56.35s | 0 | `evidence/GREEN_agent_b_scope_final.log` |
| Agent A/B + P4 CLI + P5 experience | 14 passed in 270.23s | 0 | `evidence/GREEN_14_group_final.log` |
| P6 initiative/hostile/scene/MII | 45 passed in 587.42s | 0 | `evidence/GREEN_45_p6_final.log` |

The inherited receiver caught one intermediate regression in the first 37-test run: the new conduct lookup initially read the store directly and bypassed the receiver's `session.episodes` revocation probe. The lookup was routed through the actor-scoped reader while retaining owner episode ordering; the exact receiver test then passed, and the final 37-test run is green. The failed intermediate log is preserved at `evidence/INTERMEDIATE_37_first_run_regression.log`.

## 4. Additional hostile variation

Beyond the reproduced stale-broadened receipt:

- A current owner interval copied onto the old authentic receipt still refuses.
- Two operations from the same foundational clock produce different authentic receipts; substituting the other operation's receipt into the current session refuses, while the session's own current receipt remains accepted.
- Missing, malformed, widened, or replayed `state_id` / `receipt_hash` / `episode_id` / `domain_issuance_id` provenance refuses.
- Cold reopen and same-request retry conserve the current receipt; a later operation supersedes it and the old receipt refuses.

## 5. What is not claimed

No second ledger, P3/P4/P6 owner replacement, new person engine, scheduler or general psychology was introduced. No native CAN-008 Rule A, CAN-011 Rule T, memory, transfer, `NO_CHANGE`, actor consciousness, human right or production grant is issued. No stimulus-to-mediator relevance is promoted; it remains `UNISSUED_NATIVE_RULE`. No independent G5 acceptance is claimed.

## 6. Handoff

The exact source cut for one independent nonauthor G5 receiving is `ff30c13eea54e37e2dc8edfa73a7c7447127b735`; the reviewer should verify the report HEAD and inspect both trust boundaries, run the original G5 asset, the D1 contract, the new hostile cases, the 37-test baseline, and the P4/P6 source-preservation checks in `03_G5_HANDOFF.md`.
