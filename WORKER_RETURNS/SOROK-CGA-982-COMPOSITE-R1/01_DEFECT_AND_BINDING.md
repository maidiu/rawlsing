# CGA-G5-D1 defect and the source-grounded correction

## 1. Previous trust-boundary violation

The exported helper `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py:226` `current_p3_actor_access` accepted an authentic historical receipt as evidence of current actor access.

The real call chain is:

```text
run_p6.experience
  -> P4 act / optional P6 conduct
  -> PACE owner-issued S46 interval
  -> reconsider(session, receipt, ...)
  -> current_p3_actor_access(session, interval, world, house, packet,
                             source_receipt=receipt)
```

At the G5 reproduction:

1. `new` establishes the sourcefree house.
2. `approach` commits a real `APPROACH` world event and its `P6_HOUSE_CONDUCT` parent at clock 248.
3. `PACE` commits the owner-issued S46 interval state `{start:248,end:249}`.
4. `WAIT 4` advances the world to clock 253 and commits a new S46 interval state.
5. A caller supplies the old authentic receipt with interval `{start:247,end:253}`.
6. The old code accepted it because it checked cue identity, performed-event identity, actor, sensory rederivation and a conduct parent, but did not bind the receipt to the currently admitted operation or to the owner-issued interval.

The old receipt is authentic. Its event is authentic. Its conduct parent is authentic. Its clock is inside the caller's broadened interval. Authenticity of the historical event was therefore being confused with present authority.

## 2. Why interval equality alone is insufficient

The received D1 author fix at `4952f62ea1aa175d6ea6b83d8f6beb488e12befb` compared `source_receipt["interval"]` to the caller's `interval` and to `world.clock`. Both intervals are supplied by the caller to this helper. A caller can copy or edit either. That closes the specific old-receipt replay only because the caller in the probe did not edit one side; it does not create a source-owned boundary.

The correction here does not derive authority from either caller interval. It derives it from owner-persisted episodes that already exist at the check point, before the enclosing P4 turn is appended to the ledger.

## 3. Source-grounded binding

Three owner facts are required.

### 3.1 The latest owner-issued interval state

`_owner_current_interval` (`situated.py:136`) reads `session.read_interval_states()`. The S46 producer (`S46_INTERVAL_STATE`) seals `state_id`, `receipt_hash`, `domain_issuance_id`, root, branch, actor, start and end. `read_interval_states` recomputes currentness from the actual episode order: a later same-scope state marks the earlier one `SUPERSEDED`.

The helper accepts only the last state when it is `CURRENT`, ends at `world.clock`, and matches the live root, branch and actor. The caller interval must equal that state's start/end. A superseded state, a different root/branch, or a widened caller interval refuses.

### 3.2 The receipt must be that exact owner episode

`_bound_interval_receipt` (`situated.py:165`) requires the caller's `source_receipt["interval"]` to carry the same `state_id`, `receipt_hash`, `episode_id` and `domain_issuance_id`, plus the same start, end, root, branch and actor as the owner state. A copied, edited or replayed receipt identity refuses. Comparing these fields is not the authority: the authority is the owner state found in the episode store; the receipt must identify it exactly.

### 3.3 The outward event must belong to that operation

`_current_operation_conduct` (`situated.py:185`) finds the unique `P6_HOUSE_CONDUCT` committed between the previous `S46_INTERVAL_STATE` and the current one, using the actor-scoped `session.episodes(user)` reader for the conduct and the owner episode order for the interval window. It requires:

- exactly one outward conduct in the operation window;
- conduct clock equal to the current state start and to the event clock;
- conduct body equal to `{event_id: <performed event>, operation: <event kind>}`.

An old authentic event from an earlier operation has no conduct inside the current operation window. A same-clock event from another operation is not the unique current conduct. A current event with a forged or missing receipt has no owner identity.

The complete helper then uses the owner state's `start`/`end` for every event bound and every near-term `event.clock > start` check.

## 4. Execution point

The check runs inside `reconsider`, after `PACE` has persisted the S46 interval state and before `run_p4.act` appends the turn to `ledger["turns"]`. It does **not** read a future ledger entry. The owner evidence it uses is already committed:

- `S46_DOMAIN_ISSUANCE` and `S46_INTERVAL_STATE` episodes from the existing S46 producer;
- the world event from the existing P2/BP4 writer;
- the `P6_HOUSE_CONDUCT` episode from the existing P6 outward owner.

No second canonical ledger, owner, scheduler or receipt table is introduced.

## 5. P4 source-owner repair preserved

Defect A remains closed at the original P4 owner:

- `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/response.py:20` `qualified_scope` validates the four fields against the unique source `FORMATION` plan, relation cardinality and source/registry hashes.
- `response.py:64` `read_response` validates the scope itself before the P3 read, protecting the direct reader.
- `run_p4.py:239` validates exact scope keys before `ledger["pending"]` or speech.
- `sourcefree_p3_bridge.py:17` delegates to the P4 owner rather than maintaining a second scope authority.

P4 source/test blobs are byte-identical to #992. This return changes only the P6 consumer binding and adds tests/evidence.

## 6. What remains unissued

The admitted current world event is evidence of present actor access only at the sourcefree TEST_ONLY engineering grain. No native rule establishes that this event is relevant to any particular P3 mediator. That field remains `UNISSUED_NATIVE_RULE`. No actor memory, psychology, permission, human right or production authority is promoted.
