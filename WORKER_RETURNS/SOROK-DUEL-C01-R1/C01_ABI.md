# C01 stable supporting-actor participation ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; candidate, not native actor identity or protected acceptance.
**Implementation SHA:** `9229698c5ded4e8c77801398d4d0ecc3e7c9ccb3`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## Root and focal invariants

- The generated S44 root actor list is never changed by registration or participation.
- The focal actor remains `root["actor_ids"][0]`; `P2Owner.actor` and `StateIdentity.actor` remain that stable actor ID.
- A supporting actor is a distinct stable ID registered in the existing branch actor set and P2 world actor state. It is not the user actor, not a root actor, and not a relabel of fixed A/B.

## Registration

```text
register_supporting_actor(
    session, *, alias, actor_id, role="parent", private_state=None
) -> SOROK_P2_SUPPORTING_ACTOR_READ@1
```

The writer uses the actual C12 branch and P2 world checkpoint:

```text
branch actor_ids += alias
C12 episode kind P2_SUPPORTING_ACTOR (private-state custody)
world.actor_state[alias] = {
    actor_id, role="parent", participant_kind="SUPPORTING_ACTOR",
    private_state_hash, private_episode_id, registration{...}
}
world.positions[alias] = focal actor's current position
session.product._checkpoint(branch, world.clock, world)
```

The stored registration binds root, branch, epoch, `actor_id`, `alias`, role and a content-addressed source over the identity plus `private_state_hash`. The private-state values live only in the C12 registration episode, not in the world snapshot. Public reads return `private_state_hash` and `private_state: "NOT_READ"`; only `read_supporting_actor(..., as_actor=actor_id)` reads the private episode.

Registration is idempotent for the same alias/ID/role/private state (`UNCHANGED`) and refuses:

- a root/focal actor ID, a root alias, or the user alias;
- alias reuse across stable IDs (`SUPPORTING_ACTOR_ALIAS_COLLISION`);
- stable-ID reuse across aliases (`SUPPORTING_ACTOR_ID_COLLISION`);
- a different role/private-state/source under the same identity (`SUPPORTING_ACTOR_REGISTRATION_MISMATCH`);
- a missing or altered private-state episode (`SUPPORTING_ACTOR_PRIVATE_STATE_SEVERED`).

No second scheduler, actor owner, world, clock, database or material ledger is added. The branch row update is the same mutable-metadata mechanism the existing `first_session` uses to add actor `U`.

## Participant admission

`P2Owner` now accepts participants that are either:

- actual root actor IDs; or
- stable IDs of currently registered supporting actors.

Requirements:

- the focal actor ID must be present (`P2_FOCAL_PARTICIPANT_REQUIRED`);
- the participant list is nonempty, unique, string-valued;
- every supporting actor is live in branch actor IDs, world actor state, and its private-state episode;
- every supporting actor shares the focal actor's current world position (`P2_SUPPORTING_PARTICIPANT_NOT_COPRESENT`).

Existing root-only `P2Owner` callers remain valid. An existing owner binding may be extended only by adding currently registered supporting IDs; it may not drop the stored participant set or change root/branch/source.

When a proposal carrying supporting participants produces an actual performed world event, `P2Owner.realize` calls:

```text
record_supporting_participation(session, event=world_event, participants=stable_ids)
```

That writes one C12 perception row per co-present supporting actor for the *same* world event and one public `P2_SUPPORTING_PARTICIPATION` episode containing event/actor/role/source/clock/access-channel. It never writes private state into the event or participation receipt. A supporting participant does not author a second event; C03 owns parent-authored action/utterance.

`RealizedEvent.consequences` gains:

```text
focal_actor
supporting_participation: NONE | RECORDED | HELD_NO_PERFORMED_EVENT
supporting_participants: [public participation receipts]
```

Replay re-verifies the registered actor, world event hash/clock, perception row and participation episode. A severed perception or receipt refuses with `P2_SUPPORTING_PARTICIPATION_SEVERED`.

## Actor-relative access

```text
read_actor_access(session, actor_ref, event_id) -> SOROK_P2_ACTOR_ACCESS@1
```

`actor_ref` may be a stable actor ID or an existing branch alias. The reader returns:

- `PERCEIVED` only when that actor has a C12 perception row for the event;
- the public S45 event projection (no `perceived_by_user`, no world snapshot, no private state);
- viewer identity and perception clock/channel.

Otherwise it returns `NOT_PERCEIVED` with no event content. This is the first reader boundary for C01: same world event, separate actor receipts, no private-state transfer.

## Explicit limits

- Role allowlist is `parent` only. Extending it to other supporting actors is a deliberate C05 revision, not silently available.
- C01 does not implement C02 parent antecedent/activity, C03 parent-authored decision/action, C04 hidden-reason/utterance/uptake, C05 relations, D02 situated-field read, or J1/J2.
- Parent private state is developer-visible in the C12 episode to any holder of raw store access; it is not actor-accessible through the C01 readers and is absent from the world snapshot and event objective.
- `p2_owner.py` bytes feed `P3Owner._code_pins()`. Pre-C01 P3 state roots will refuse cold reopen under this code; same-code roots reopen exactly. No migration is invented.
- Full P3 vertical-slice suite was attempted and did not finish within a 900 s budget (3 tests passed before timeout); selected cold-replay/view tests passed. This is not a full-estate claim.
