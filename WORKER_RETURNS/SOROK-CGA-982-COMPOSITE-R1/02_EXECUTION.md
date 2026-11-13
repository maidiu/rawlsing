# Execution record

## Environment

- Host: macOS 13.7.8, x86_64 (`Darwin 22.6.0`), 16 CPUs, 16 GiB RAM.
- Local worktree: `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/cga982-composite-20261113`.
- Python: `/usr/local/bin/python3` 3.11.3.
- pytest: 9.1.1.
- Actual model/session identity: `opencode-go/deepseek-v4.1-flash`. A "MAX" model was not separately verified and is not claimed.
- No GitHub Actions, no provider call, no network execution, no protected merge.

## Source custody

- Base: `4cbf67398d742eeab0853d047b6c2239c84b8348` (PR #992 report HEAD).
- Implementation/test cut: `ff30c13eea54e37e2dc8edfa73a7c7447127b735` (direct child of the base).
- D1 author branch read only: `4952f62ea1aa175d6ea6b83d8f6beb488e12befb`.
- G5 review branch read only: `c597024bb250f014f9a616006f10172ed53e4357`.
- G5 hostile test blob: `a1453e799d98b4c47d26c56a12d1d2695bd42557`.
- D1 contract test blob: `30701f83ee7dcc37aa3cf958a7224cd6229b6816`.
- #977 receiver asset blob: `2b489ba1edd0698ead4899fe64abe19e9f7f4cce`.

## Base RED

At the unmodified `4cbf67398` worktree, before any source edit, the exact G5 test was extracted from `c597024bb` to its original repository-relative path and run:

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_hostile_stale_receipt.py
```

Result: **exit 1, 1 failed, 10.43 s**:

```text
assert current_p3_actor_access(..., source_receipt=old) is False
AssertionError: assert True is False
```

Log: `evidence/RED_base_c597024_hostile.log`.

## Final GREEN at `ff30c13ee`

### Six-group #977 baseline (37 tests)

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-982-COMPOSITE-R1/test_receiver_977_baseline.py \
  WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py \
  WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
```

Result: **exit 0, 37 passed, 2273.44 s**. Log: `evidence/GREEN_37_baseline_final.log`.

### Current-operation repair, original stale asset and D1 contract (7 tests)

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-982-COMPOSITE-R1/test_current_operation_binding.py \
  WORKER_RETURNS/SOROK-CGA-982-COMPOSITE-R1/test_g5_stale_receipt.py \
  WORKER_RETURNS/SOROK-CGA-982-COMPOSITE-R1/test_d1_receipt_currentness.py
```

Result: **exit 0, 7 passed, 89.76 s**. Log: `evidence/GREEN_repair_final.log`.

### P4 source-owner #992 (7 tests)

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-P4-SOURCE-OWNER-R1/test_p4_scope_owner.py
```

Result: **exit 0, 7 passed, 66.07 s**. Log: `evidence/GREEN_p4_scope_owner_final.log`.

### Agent B #986 scope custody (6 tests)

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-AGENT-B-SCOPE-CHALLENGE-R1/test_scope_source.py
```

Result: **exit 0, 6 passed, 56.35 s**. Log: `evidence/GREEN_agent_b_scope_final.log`.

### Agent A/B + P4 CLI + P5 experience (14 tests)

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py \
  WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_cli.py \
  WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1/test_experience.py
```

Result: **exit 0, 14 passed, 270.23 s**. Log: `evidence/GREEN_14_group_final.log`.

### P6 initiative, hostile initiative, scene context and MII (45 tests)

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_initiative.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_initiative_hostile.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_scene_context.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py
```

Result: **exit 0, 45 passed, 587.42 s**. Log: `evidence/GREEN_45_p6_final.log`.

## Intermediate regression caught and repaired

The first 37-test run at the working cut failed one inherited receiver probe:

```text
FAILED .../test_receiver_977_baseline.py::test_real_current_cue_requires_issuer_parent_not_just_event_identity
assert True is False
1 failed, 36 passed in 2336.97s
```

Cause: `_current_operation_conduct` initially read `session.product.store.episodes` directly, bypassing the receiver's deliberate `session.episodes` revocation monkeypatch. The lookup was changed to read the conduct through the actor-scoped `session.episodes(user)` reader while keeping owner episode ordering. The exact probe then passed, and the final 37-test run is green. The failed log is preserved at `evidence/INTERMEDIATE_37_first_run_regression.log`.

## Not run

- GitHub Actions (runner allocation was not relied upon).
- Protected PRE-MAIN merge.
- New native science, actor/human authority or production claims.
- CG-B–CG-G fleet resumption.
