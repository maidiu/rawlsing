# CGA-CGB-CD-CONTRACT evidence

## Pinned source objects

```text
P3Owner         2be0cf25:WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/p3_owner.py
                blob e735ada798533a8f568739e823767bb2e2b4272c3c03d84dc2cd47f73cf65df1
PsycheStore     2be0cf25:WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/state_store.py
                blob 173d4d6d3e94580804cac90039a01bfe6e3adfffcda9e806a56132b10ecc06bf
house.py        2be0cf25:WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py
                blob af556c143e7e4eaa2f60a68fa402954091737dd4
                sha256 7d78d48dd1b12a1bc95d3fc844df31cb41364eedbe5943a9c69c50699296c645
situated.py     2be0cf25:WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py
                blob 8b434ff2f1b96b13b02be59704518d622ebecbd6
                sha256 655e94418ee340a34a579592d13a8c7b3f4e747f248ff15cac844231be3df7ee
actor_initiative 2be0cf25:WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/actor_initiative.py
                blob c9d2e1e93314ef2ec2dd767f998fd2775be78663
                sha256 dc2df7a18f1901818387f98f029133e800f6dd17fe072f7d46a68560bb48d295
```

The declared P6 blob `af556c143e...` is exact at `2be0cf25`.

## Exact capabilities

`p3_owner.py`:

- `snapshot` (`225-233`) hashes the base state plus the store head.
- `validate_proposal` (`352-365`) calls base validation, history validation, plan validation, and compression preflight.
- `realize` (`654-740`) checks expected identity and P3 state, reserves, runs the base owner, performs `_effect`, and completes.
- `_effect` (`548-604`) queries the store by `project`, `counterpart`, `as_of`; activates records; evaluates rules; commits the effect; builds the readset.

`state_store.py`:

- `PsycheStore.__init__` (`722-777`) binds exact `(root, actor, branch)` and registry/source hashes.
- `query` (`784-822`) is indexed by root/actor/branch/project/counterpart/effective time.
- `reserve` (`846-930`) requires exact identity, plan hash, source/registry, stale-head check.
- `commit_effects` (`963-1162`) validates every record against the plan/event/source/rule and rolls back all on one bad target.
- `finish` (`1163-1199`) binds the immutable result to the receipt.
- `verify` (`1200-1246`) checks the head chain and operation integrity.

`house.py`:

- `establish` (`151-166`) writes `world.resources["p6_house"]` with root/branch/source/epoch/rooms/objects/history.
- `read_house` (`206-228`) checks root, branch, source hash, rooms/objects, and history provenance.
- `facts_for` (`84-94`) validates chronological object history.

`situated.py`:

- `recent_speech` (`35-49`) reads only actor-A perceived speech.
- `reconsider` (`134-230`) builds the actor-local packet, validates a grounded decision, and commits speech via `session.product.say(text, actor="A")`.
- It does not call `PsycheStore`.

`actor_initiative.py`:

- `route_from_context` (`37-61`) accepts only actor-local sourcefree routes.
- `destination_if_eligible` (`63-83`) checks scene, actor, house, and route.
- `_select_visit` (`99-151`) binds a selected visit to the actual packet/world; `visit_adjacent_room` (`153-190`) writes the action.

## Missing-function source evidence

```text
p2_owner.py:45-47       participants == tuple(root["actor_ids"]); actor = root["actor_ids"][0]
state_store.py:730-736  binding set must be exactly {root, actor, branch}
p3_owner.py:116-195     one P3Owner -> one base actor -> one store
situated.py:35-49       recent_speech only for "A"
situated.py:222-227     say(text, actor="A") only
house.py:151-165        p6_house epoch/history; no home_period from_clock/to_clock/home_ref
```

No source function was found for a second actor's sidecar, a dated home period, an independent mother speech writer, or a `situated.reconsider` -> `PsycheStore` readset. These are the exact BUILD/HOLD cards.

## Manual probes

The author inspected the pinned objects directly with `git show`, `git hash-object`, and `shasum -a 256`; no adapter or mock was created for the absent functions. The selected store-level and owner-level tests in `tests/` exercise only what exists.

## NOT_RUN

- No CG-B/C/D implementation was attempted.
- No mother actor, home period, or independent speech test exists because the current adapter is absent.
- No new scheduler or parallel ledger was created.
