# C01 Agent B revised ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; candidate, not native actor identity or protected acceptance.
**B implementation commit:** `0e526f043027e4256b353d42240e80d85ad39265`.
**Parent / attacked A HEAD:** `7e347c45d991df322b987c4fdc70558b1857d9f6` (A implementation `9229698c5…`).
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## Root and focal invariants (preserved from A)

- The generated S44 root actor list is never changed by registration or participation.
- The focal actor remains `root["actor_ids"][0]`; `P2Owner.actor` and `StateIdentity.actor` remain that stable actor ID.
- A supporting actor is a distinct stable ID registered in the existing branch actor set and P2 world actor state. It is not a root actor, the user actor, or a relabel of fixed A/B.

## Registration

```text
register_supporting_actor(
    session, *, alias, actor_id, role="parent", private_state=None
) -> SOROK_P2_SUPPORTING_ACTOR_READ@1
```

The writer commits one C12 transaction (`BEGIN IMMEDIATE`, or a savepoint inside an outer transaction):

```text
branch actor_ids += alias
C12 episode kind P2_SUPPORTING_ACTOR (private-state custody)
world.actor_state[alias] = {actor_id, role, participant_kind, private_state_hash,
                            private_episode_id, registration{...}}
world.positions[alias] = focal actor's current position
session.product._checkpoint(branch, world.clock, world)
```

The registration binds root, branch, epoch, `actor_id`, `alias`, role and a content-addressed source over identity plus `private_state_hash`. Private values live only in the C12 registration episode. Public reads return `private_state_hash` and `private_state: "NOT_READ"`; only `read_supporting_actor(..., as_actor=actor_id)` returns the values.

Namespace reservations (new in B):

- alias may not equal a root stable ID, a root alias, the user alias, or any existing actor stable ID;
- stable ID may not equal an existing alias, a root alias, or the user alias;
- alias/stable-ID reuse across different identities refuses `ALIAS_COLLISION` / `ID_COLLISION`.

Idempotence and refusal:

- identical registration returns `UNCHANGED` with no new rows;
- a different role/private state/source under the same identity refuses `REGISTRATION_MISMATCH`;
- duplicate registration episodes, a missing/altered private episode, or an ambiguous identity refuses;
- a cold partial from the earlier non-atomic cut returns `RECOVERED`: a branch alias plus a matching registration episode and no world row is completed from the episode; a branch alias with no episode/world row is reclaimed and fully written; a mismatched episode/row fails closed.

Statuses are `REGISTERED`, `UNCHANGED`, `RECOVERED`.

## Participant admission

`P2Owner` accepts participants that are actual root actor IDs or stable IDs of currently registered supporting actors. Requirements:

- the focal actor ID must be present (`P2_FOCAL_PARTICIPANT_REQUIRED`);
- the list is nonempty, unique, string-valued;
- every supporting actor is live in branch actor IDs, world actor state and its private-state episode;
- every supporting actor shares the focal actor's current world position (`P2_SUPPORTING_PARTICIPANT_NOT_COPRESENT`);
- the proposal document is pre-scanned for supporting private values (`SUPPORTING_PRIVATE_STATE_LEAK`) before reservation/admission.

**Owner binding (changed in B):** the persisted binding is the original root/branch/source invariant over `root_participants` (the actual root actor tuple). Declared owner participants are validated live and are no longer a second invariant. Legacy binding rows from the baseline or A's cut migrate when root/branch/source match and the stored list still names the focal actor. This lets the ordinary P3 reopen shape `tuple(root["actor_ids"])` and a parent-scoped C01 owner coexist on one root in either order. It is a deliberate repair of A's `P2_OWNER_BINDING_MISMATCH` lockout.

When a proposal carrying supporting participants produces an actual performed world event, `P2Owner.realize` calls:

```text
record_supporting_participation(session, event=<actual store event>,
                                participants=<stable IDs>)
```

That function:

1. resolves the event from the branch store and requires hash/clock/kind/location to match, then canonical equality; a detached/forged event refuses `SUPPORTING_PARTICIPATION_EVENT_MISMATCH`;
2. validates every participant's registration, co-presence and private leak **before the first write**;
3. writes one C12 `co_present` perception per participant and one public `P2_SUPPORTING_PARTICIPATION` episode per participant in one transaction;
4. refuses duplicate participation episodes.

`RealizedEvent.consequences` keeps A's fields plus `focal_actor`, `supporting_participation: NONE | RECORDED | HELD_NO_PERFORMED_EVENT` and `supporting_participants` public receipts. A supporting participant does not author a second event; C03 owns parent-authored action/utterance.

Replay re-verifies registration, event hash/clock/kind/location, receipt clock/channel and participation episode. A severed or forged perception/receipt refuses `P2_SUPPORTING_PARTICIPATION_SEVERED`.

## Actor-relative access

```text
read_actor_access(session, actor_ref, event_id) -> SOROK_P2_ACTOR_ACCESS@1
```

- accepts a stable actor ID or an existing branch alias;
- root actors: `PERCEIVED` only with their C12 perception receipt; otherwise `NOT_PERCEIVED` with no event content;
- supporting actors: additionally require the live registration **and** the public participation episode **and** the receipt at the event clock/channel; a bare/forged perception row, missing episode or forged receipt refuses `P2_SUPPORTING_PARTICIPATION_SEVERED`;
- an alias that is simultaneously a root stable ID and another actor's alias refuses `ACTOR_ACCESS_IDENTITY_AMBIGUOUS`;
- returns the public S45 projection with `perceived_by_user` removed, no world snapshot and `private_state: "NOT_READ"`.

## Explicit limits

- Role allowlist is `parent` only; C05 must deliberately extend roles/relations.
- C01 does not implement C02 antecedent/activity, C03 parent-authored decision/action, C04 hidden-reason/utterance/uptake, C05 relations, D02 situated field, or J1/J2.
- Parent private state is developer-visible in the C12 episode to any holder of raw store access; it is absent from the world snapshot, event objective and public/child reads. Leak scanning is string-based; non-string private values are not scanned.
- Registration and participation are atomic at their own C12 write boundaries. Event admission plus participation is not one composite transaction; a post-admission participation refusal leaves the inherited P2 ambiguous reservation (`P2_AMBIGUOUS_PRIOR_OPERATION_HOLD`). E03 owns composite recovery.
- Fork/copy preserves the exact incompatibility: a C12 fork copies the branch actor list and episodes but `read_supporting_actor` refuses `SUPPORTING_ACTOR_ROOT_OR_BRANCH_MISMATCH` because the registration binds its origin branch. Pair1 B's verified-lineage helper at `362719b40…` is a future composition input, not adopted here.
- `p2_owner.py` bytes feed `P3Owner._code_pins()`. Same-code roots reopen; pre-B01/pre-C01 roots refuse cold reopen. No migration invented.
- No native, scientific, rights, actor, human or protected-merge authority is issued.
