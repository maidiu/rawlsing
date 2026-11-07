# P3 goal-residual targeted proofs — actual return

## Status

**AUTHOR PROOF COMPLETE FOR TWO RESIDUALS; THIRD HAS AN EXACT P2 FIXTURE LIMIT.**

This is author proof only, not independent acceptance. No runtime, existing
tests, fixtures, contracts, checkers, sourcepack, PROGRAMMA, checkpoint or
prior evidence was edited. The only changes are
`tests/test_p3_goal_residuals.py` and this evidence directory.

- Runtime/evidence cut: `486d42a4aa5dcd449564b95567ae93b59c4679a4` /
  `16275d03fc4724a694c48ed9d447c4eeadbe25f2`
- Test file SHA-256:
  `7fcd6c48a33b0aecb0f689149b235d714599b50d115f1272a7e06dd2b14260d8`
- B1 source SHA-256: `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3`
- Actual command:
  `PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1:WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 python3 -m pytest -q -rs WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py -p no:cacheprovider`
- Result: **3 passed in 27.14s**; `/usr/bin/time -p` real `27.58s`.
  The 13-case matrix and 71-test suite were not rerun.

## Residual dispositions

### 1. Same source/history/later world, only prior formation vs no mediator

**PASS (author) with an exact P2 fixture limit.**

`test_same_history_only_prior_formation_changes_later_response` uses the
existing deterministic actual P2/P3 fixture. Both cases have:

- identical root/actor/branch/clock (`3bcb21fc…`, clock `222`);
- identical source hash (`b1f0ffd1…`);
- identical history hashes (`afb0fdb0…`, `4f684495…`);
- identical later proposal, event time, and objective `world` after the later
  event;
- the only authorized difference: first plan phase `FORMATION` vs
  `STABILITY`.

Actual result:

- formation writes 2 records:
  `d00a4c3a…` (`joint_check`) and `34713acc…` (`private_check`);
- control writes 0 records;
- later formation response streams: `joint_check`, `private_check`;
- later control response stream: `inspect_alone`;
- formation later readset contains both prior record hashes; control readset
  contains neither;
- `native_action_performed` is false in both; actual material eligibility is
  equal.

Exact limit: these are two separately initialized deterministic P2 fixture
roots, not one exact P2 `StateIdentity` copy. Their P2 full `state_hash` is not
asserted equal because the native fixture's generated event/action/language
hashes differ across separately initialized roots. The comparable later
**objective world**, P2 identity/clock, source, and P3 history are equal.
A single actual P2-root snapshot/fork API was not available and no DB deletion
or synthetic record was used. If exact P2 `state_hash` identity is required,
the smallest missing interface is an exact P2 root snapshot/fork/remap API;
that is a reported dependency, not invented or patched here.

### 2. Genuinely distinct sourcefree root / cross-root denial

**PASS (author).**

`test_distinct_sourcefree_root_rejects_cross_root_source_before_effects` uses
the existing `P2ProductFanin.start(..., seed=...)` API with a different seed:

- left actual root: `3bcb21fc…`;
- right actual root: `b43c92c0…`;
- roots genuinely distinct;
- left store has two actual `V3MS_MEDIATOR` records, all bound to left root;
- presenting `left.source` to the right actual P2 owner raises
  `P3_SOURCE_IDENTITY:root` before any right-side P3 config/store creation;
- right P2 snapshot is unchanged; no right `p3_owner_config.json` or
  `p3_psyche.sqlite3` exists;
- no record migration or source string mutation was used.

### 3. Actual-chain B1 source severance/restore

**PASS (author).**

`test_actual_chain_source_severance_and_exact_restore` uses a real P2/P3 owner:

- missing B1 path → `P3_B1_SOURCE_SEVERED`;
- altered B1 bytes/source → `P3_B1_SOURCE_SEVERED`;
- after both denials, P2 StateIdentity and P3 head are unchanged, and no
  operation row exists;
- exact original B1 bytes restored at the exact owner path;
- actual P2 → P3 event then returns `REALIZED`, `accessible=OBSERVED`, and
  operation phase `COMPLETE`;
- same-operation replay returns the identical RealizedEvent and leaves P2/P3
  state unchanged.

No source forgery, retagging, runtime weakening or code-pin edit was used.

## Evidence

- `TEST_LOG.txt` — actual three-test pass log.
- `TEST_TIME.txt` — actual wall/user/system timing.
- `PROOFS.json` — actual roots, records, readset assertions, cross-root error,
  source hashes and source-severance state checks.
- `SOURCE_PINS.json` — exact current source hashes.
- `MANIFEST.json` — evidence hashes.

## Limits

- No 13-case matrix or 71-test suite rerun; no new acceptance gate.
- Same-history proof has the P2 fixture state-hash limit above; no claim of
  exact full P2 state identity for separately initialized roots.
- No native science, human validation, actor-B, production, CAS, protected
  merge, PR or independent acceptance.
- Independent qualification of these three proofs remains separate.
