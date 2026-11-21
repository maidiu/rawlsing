# CGA-P3-ABI evidence

## Source identity

Command:

```bash
git rev-parse HEAD
git hash-object WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/contracts.py
git hash-object WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py
git hash-object WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/P3_RULEBOUND_DEVELOPMENT_SOURCEPACK_R1/09_ALREADY_EXECUTED_DEVELOPMENTAL_CODE_AND_REVIEW_DELTA.md
```

Observed:

```text
HEAD 2be0cf252662ad021571db6f0d38b12c205c56ae
contracts.py c4ce557cdb6d1e5ad8f3217e72d16a5a91c2a0e8
p2_owner.py 3160eb157675453c0bfee5f9bd4b400f9c999c17
house.py af556c143e7e4eaa2f60a68fa402954091737dd4
sourcepack09 c3cdc7c1e151cf3ece8159f7cc384b2359212e6c
```

The declared startup commit `1f77f2036427a410429184780ef884ec4f253ad0` is not an object in the local repository; `git cat-file -t` fails. The four declared blobs are exact at `2be0cf25`, so the source content is equivalent even though the commit identity is not.

## Exact engine symbols

| Symbol | File:line | Contract |
|---|---|---|
| `StateIdentity` | `contracts.py:31-40` | root, actor, branch, clock, state_hash |
| `EventProposal` | `contracts.py:43-54` | event id/time, operation, source refs, participants, circumstances, optional interval |
| `RealizedEvent` | `contracts.py:57-71` | operation/proposal binding, before/after, status, objective/accessible/consequences, readset, receipt |
| `DevelopmentOwner` | `contracts.py:74-89` | snapshot, validate_proposal, realize |
| `BatchEngine.run_batch` | `engine.py:337-500` | 3–5 ordered proposals, durable reservations, owner result validation |
| `BatchEngine._check_new_batch` | `engine.py:888-923` | strictly forward event times, running-batch block, event id conflict |
| `BatchEngine._validate_owner_result` | `engine.py:633-679` | operation/proposal/before/after identity, status set, JSON surfaces |
| `RecursionCycle.bootstrap` | `model_cycle.py:199-239` | provider reservation, no bootstrap memory, first batch |
| `RecursionCycle.advance` | `model_cycle.py:240-288` | retrospective binding before next batch |
| `RecursionCycle.finish` | `model_cycle.py:289-331` | terminal retrospective only |
| `RecursionCycle._call` | `model_cycle.py:332-381` | detached request, provider mutation refusal, durable reservation |
| `P2Owner.__init__` | `p2_owner.py:38-61` | fixed participant tuple and first actor |
| `P2Owner.validate_proposal` | `p2_owner.py:79-139` | operation/source/participants/history/clock/interval |
| `P2Owner.realize` | `p2_owner.py:140-146` | lock, idempotent operation |
| `P2Owner._realize` | `p2_owner.py:190-274` | reservation, stale state refusal, native event/interval, actor experience |
| `P3Owner.snapshot` | `p3_owner.py:225-233` | base state plus sidecar head |
| `P3Owner.validate_proposal` | `p3_owner.py:352-365` | base validation, plan/history/source/compression |
| `P3Owner.realize` | `p3_owner.py:654-740` | expected identity/state, reserve, base, effect, complete |
| `P3Owner._effect` | `p3_owner.py:548-604` | store query readset, activation, rules, commit |
| `PsycheStore.query` | `state_store.py:784-822` | exact actor/project/counterpart/as_of indexed read |
| `PsycheStore.reserve` | `state_store.py:846-930` | identity, plan, source, head, durable phase |
| `PsycheStore.commit_effects` | `state_store.py:963-1162` | all-or-nothing records, event/source/rule binding |
| `PsycheStore.finish` | `state_store.py:1163-1199` | COMPLETE with receipt/result linkage |
| `house.establish` | `house.py:151-166` | root/branch/source/epoch house resource |
| `house.read_house` | `house.py:206-228` | exact root/branch/source/provenance read |

## Schema/contract refusals observed in source

```text
P2_PARTICIPANTS_NOT_BOUND_TO_ROOT
P2_PARTICIPANT_SCOPE_MISMATCH
P2_EVENT_CLOCK_NOT_FUTURE
P2_INTERVAL_CROSSES_EVENT_CLOCK
P2_AMBIGUOUS_PRIOR_OPERATION_HOLD
P2_STALE_ROOT_BRANCH_CLOCK_OR_STATE
BATCH_EVENT_TIMES_NOT_FORWARD
OWNER_ROOT_ACTOR_BRANCH_MISMATCH
OWNER_RESULT_IDENTITY_CHANGED
STALE_PSYCHE_HEAD
OPERATION_REUSE_MISMATCH
DUPLICATE_RECORD_ID
P6_HOUSE_SOURCE_OR_ROOT_MISMATCH
P6_OBJECT_PROVENANCE_MISMATCH
```

## Execution evidence

`evidence/engine71.log`: 71 passed in 278.95 s.
`evidence/engine_material_cold.log`: 2 material/C9 tests passed in 260.26 s.
`evidence/p3_owner_cold.log`: 1 cold/replay/source-restore test passed in 280.92 s.
`evidence/p3_negatives.log`: 3 identity/cross-root/crash tests passed in 14.03 s.

## Commit-identity deviation

The declared `1f77...` commit is unavailable. The author did not create a substitute commit with that hash. The worktree at `2be0cf25` is the source-equivalent cut. Any receiving decision that requires the literal hash must mark this obligation's commit-identity part incomplete; the source-content comparison above remains exact.
