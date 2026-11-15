# P3 owner glue — bounded implementation return

## Scope and status

This unit implements only the P3 owner glue requested for
`WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1`:

- `p3/p3_owner.py`
- `tests/test_p3_owner.py`
- `evidence/owner/`

The unit is **BOUNDED IMPLEMENTATION BANKED; DEPENDENT INTEGRATION NOT
EXECUTED**. The normalized `p3/state_store.py` requested by the separate
storage worker is not present in this startup. No fake store, in-memory
fallback, private-worktree import or alternate storage engine was created.
The six actual-P2/store tests are therefore explicitly skipped with
`DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE`; this is not a
green integrated acceptance.

## Constructed API

`P3Owner(base_owner, *, source, history, plans, catalog=None,
compression_specs=None, standpoints=None, mode="TEST_ONLY")`

- Composes an unchanged actual `P2Owner`; the P2 owner retains the one actual
  root/actor/branch/clock and all world custody.
- Accepts only explicit `SOURCEFREE_TEST_ONLY`; validates the source identity,
  exact source reference and source hash.
- Validates sealed history through `test_rules.validate_history`.
- Accepts sealed proposal-ID plans, validates rule/version/source/selectors,
  and calls `test_rules.validate_plan` again before effects.
- Builds the frozen registry with `test_rules.make_registry(source_hash)`.
- Hashes and persists one canonical owner configuration file under the actual
  P2 `session.state_root`; reopening requires the exact config and code pins.
- Uses the frozen `PsycheStore` API lazily. Absence raises
  `DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE`; there is no
  storage fallback.
- `snapshot()` returns a `StateIdentity` over the actual P2 state hash, the
  committed store head and the owner config hash.
- `validate_proposal()` calls the unchanged base preflight plus source,
  history, rule, plan and optional compression preflight. It has no effects.
- `realize()` uses a root-local lock and the frozen
  `PREPARED -> WORLD_COMMITTED -> PSYCH_COMMITTED -> COMPLETE` flow, stable
  deterministic base operation IDs, saved `base_before` on recovery,
  explicit ambiguity refusal for a base reservation without a result, and
  exact completed-result replay checks.
- Sourcefree formation/response computation uses actual `actor_experience`,
  `test_rules.evaluate_event` with targeted prior records, and the pure
  `projections.activate`/`project_views` readers.
- The returned `accessible` surface is the actual actor projection. A user
  surface is included only as `consequences.test_only_user_surface` from a
  configured read-only standpoint. No ADP016 formed memory or ADP017
  first-person claim is emitted.
- `durable_psychological_transition` remains `MISSING_RULE`; native action
  feasibility is retained from the actual P2 result and is never rewritten.

## Executed checks

Command (from the repository worktree):

```text
PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1:WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 \
python3 -m pytest -q -rs WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py -p no:cacheprovider
```

Observed: **2 passed, 6 skipped in 0.10s** (`evidence/owner/TEST_LOG.txt`).

The two executed checks are:

1. Production/non-`TEST_ONLY` mode refuses before base/store access.
2. Missing returned state store is an explicit refusal, not a silent fallback.

`python3 -m py_compile` of both new Python files passed.

## Blocked checks

The following meaningful tests are authored but not executed because their
required returned module is absent:

- actual P2 root configuration and combined state hash;
- sourcefree formation -> stored records -> later response/control;
- pure actor/user projection surfaces;
- wrong source, rule version and config mutation;
- idempotent replay and cold owner reopening;
- real subprocess crash boundary after the base effect and before
  `save_world`.

Their skip reason is exactly
`DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE`.

## Actual sources and exact limits

Read/used in this implementation:

- `p3/test_rules.py` (`27272cd43c26b6aa114ee65c97ca07eb56accecbd440841c29696b98e203b4b4`)
- `p3/projections.py` (`ca405dda778191537ce38b0b63ff6b6ba8104dcd1ea676d6b458d454b362005b`)
- `p3/compression.py` present but still REVISE; only its declared optional
  preflight/bind API is referenced, with no positive compression claim
- `developmental_recursion/p2_owner.py`
  (`fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0`)
- `developmental_recursion/contracts.py`
  (`9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d`)

Not present/not executed: `p3/state_store.py`, actual P2 test root, any
durable store row, any two-batch/cold/crash actual-P2 proof, any native
psychological transition, any ADP016/ADP017 state, any human validation or
final independent runtime review.

No edits were made to `p3/test_rules.py`, `p3/projections.py`,
`p3/compression.py`, `p3/state_store.py`, `p3/__init__.py`, other tests or
evidence, sourcepack, PROGRAMMA, accepted #704/P2, production registry or the
protected tree. `S1_INDEPENDENT_INPUT_REVIEW 7466d37bf` remains unchanged.

## Next HQ action

Once the normalized storage return is imported, resume this same bounded
owner task/session: execute the six skipped actual-P2/store checks, correct
only owner glue against the returned store API if needed, then hand the
integrated candidate to a distinct E1 nonauthor runtime reviewer. This return
is not self-accepted, merged, native-authorized or complete.
