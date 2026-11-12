# SOROK CG-A independent G5 receiving — PR #976

**Status:** `REVISE_EXACT_DEFECT`
**Implementation under review:** PR #976 head `37c5842e04892421c9ce74a39956c3cdcf57f0f5`
**Tested checkout:** `9d3d8ae419998a3e13d88f58147756149e3dddb5` (review branch; exactly two added files over PR head)
**Commission:** issue #977 (body not retrievable with the current token; gate criteria reconstructed from the user instruction, the review-branch workflow, and the pinned author handoffs)
**Integration verdict:** `NOT_READY_FOR_GENERAL_INTEGRATION__SCOPED_P6_CLI_PATH_GREEN__DIRECT_HELPER_REVISE`
**Evidence grade:** `SOURCEFREE_S2_INSTRUMENTATION_ONLY_CANDIDATE_PENDING_REPAIR_AND_RECEIVING`
**G03_FULL:** `NOT_EVALUATED_G02_MISSING`
**G5:** `REVISE`, not APPROVE.

## 1. Source custody

- PR #976 head verified by `refs/pull/976/head`: `37c5842e04892421c9ce74a39956c3cdcf57f0f5`.
- Review branch head tested: `9d3d8ae419998a3e13d88f58147756149e3dddb5`.
- Merge base: `37c5842e0`; the review branch is the PR head plus:
  - `.github/workflows/sorok-cga-independent-receiving-r1.yml`
  - `WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_receiver.py`
- No implementation, P3/P4/P5/P6 owner, protected PRE-MAIN or native source file was changed by the review branch.
- Tracked worktree diff was empty during testing; only untracked `__pycache__` from the test run existed.

## 2. Execution

Exact command, run at the tested checkout:

```bash
python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_receiver.py \
  WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py \
  WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
```

Result: **37 passed, 0 failed**, exit 0, 2330.68 s. Full quiet output preserved in `G5_EVIDENCE/37_tests.log`. This includes the four existing independent receiver probes, the Agent A/B first-consumer tests, and the wider P3/P4/P6 regressions. The actual implementation code is unchanged from PR #976 head; the review branch only adds the receiver probe and workflow.

## 3. New hostile probe and finding

New test: `test_hostile_stale_receipt.py` (not one of the four existing receiver probes).

```bash
python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_hostile_stale_receipt.py
```

Result: **1 failed**, exit 1, 12.72 s. Failure:

```text
assert current_p3_actor_access(..., source_receipt=old) is False
AssertionError: assert True is False
```

Sequence: actual `new` → actual `approach` commits receipt E1 at clock 248 → actual `wait 4` advances the world to clock 253 → direct call to `situated.current_p3_actor_access` with the old authentic receipt E1 and a caller-supplied interval `{start=247, end=253}` returns `True`. The old cue is replayed as current authorization.

**Exact cause:** `situated.py:136` `current_p3_actor_access` validates cue equality, performed-event equality, event actor, sensory rederivation and a `P6_HOUSE_CONDUCT` parent, but it does not bind `source_receipt` to the *current* operation and does not require the receipt's own interval to equal the caller's interval. The outward-cue loop permits `start <= event.clock`, so an earlier authentic event is accepted when the caller broadens the interval.

**Impact:** a direct internal caller can replay an old authentic cue as current actor access; with a prior P3 mediator and a direct/injected decision, this can condition a later sourcefree utterance. The actual P6 CLI path passes the current receipt and the 37-test suite is green; this review did **not** demonstrate a bypass through the normal CLI path. The defect is in the exported helper’s enforcement boundary, exactly the direct-caller risk the author handoff had already flagged.

**Minimal repair requirement:** require the receipt to be current-operation-bound (operation/request identity) and/or require the receipt interval to match the current interval exactly; then rerun this test plus the 37-test suite. Adding only `event.clock > start` is insufficient because a caller can set `start` before the old event. Do not patch Agent A in this receiving branch.

## 4. Gate findings

| Gate | State | Basis |
|---|---|---|
| G1 Contract and custody | `PASS_SOURCE_CUSTODY__COMMISSION_TEXT_NOT_ACCESSIBLE` | PR head exact; review branch adds only two files; no protected/owner changes |
| G2 Actual execution | `PASS` | 37/37 tests, including actual P3/P4/P6 paths; full log preserved |
| G3 Hostile tests | `FAIL` | new stale-receipt replay probe fails; the four existing probes pass |
| G4 Raw evidence and durability | `PASS_AFTER_ARTIFACT_COMMIT` | log, exact SHAs, failure trace, environment, committed artifacts |
| G5 Independent receiving | `REVISE` | real direct-helper defect; not an approval |

## 5. Integration readiness

**`NOT_READY_FOR_GENERAL_INTEGRATION` until CGA-G5-D1 is repaired and the 37-test suite plus the new hostile test pass.**

The bounded P6 CLI first-consumer path remains green at the declared sourcefree TEST_ONLY grain. This verdict does not reject the existing P6 path wholesale; it rejects promoting the exported actor-access helper as a general interface while it accepts stale authentic receipts.

## 6. Authority and limits

No native CAN/ADP/Pyat rule, independent mother, dated home-period, actor/human right, production rule, protected PRE-MAIN merge or GitHub Actions execution is claimed. Provider calls/tokens/costs are `UNOBSERVED`. The issue #977 body was not accessible through the current token; no claim is made about unread commission text.

## 7. Evidence

- `G5_EVIDENCE/37_tests.log` — complete quiet output of the 37-test run.
- `G5_EVIDENCE/hostile_stale_receipt.log` — complete failure output.
- `G5_EVIDENCE/SOURCE_STATE.txt` — exact SHAs and two-file review delta.
- `G5_EVIDENCE/ENVIRONMENT.txt` — host/Python/pytest.
- `G5_01_GATE_FINDINGS.json` — machine-readable findings.
- `G5_02_EXECUTION.md` — exact commands and counts.
- `G5_03_INTEGRATION_READINESS.md` — scoped verdict.
- `G5_04_REPAIR_REQUIREMENT.md` — minimal repair acceptance.
