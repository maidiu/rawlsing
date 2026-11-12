# C01 AGENT B — independent reconstruction (recorded before reading A's handoff/diff)

**Agent:** B, Pair 3 (session `ses_e31295826ffe6kteacpU7p3nQW`), opponent SAME A
`ses_e31295836ffeW9bYwX9iiMMcXS`. **Branch:** `codex/sorok-duel-c01-b-20261112-r1`.
**Frozen source state under attack:** `7e347c45d991df322b987c4fdc70558b1857d9f6`
(implementation commit `9229698c5ded4e8c77801398d4d0ecc3e7c9ccb3`).
**Frozen programme inputs:** `01`–`05`, the user-directed rolling person–world
requirement, and the owner reconciliation `32` at #911
`b50b1282aeb7eb58d4f34791470912eebb2e2694` (verified byte-identical here:
SHA256 `0893c6d1fc695660ec701255d5d1666c3cebb4e3980d5bccf4abfe45cc5ee025`).
**Writing constraint preserved:** the two full Library architecture records remain
NOT_INSPECTED locally; no claim is made from their contents.

This reconstruction is from the governing programme and the pre-existing owner
code only. It was completed before opening A's handoff, ABI, evidence, tests or
diff.

## 1. What C01 is actually for

C01 is a CG-C component of the single rolling Nadia life, not a generic
multi-agent feature. The frozen packet says:

- title: *Stable other-actor identities and dynamic participation without changing
  Nadia root*;
- producer owner: `C4/ADP-015 actor identity; shared P2 world`;
- existing capital: generic P3 `EventProposal.participants`, P2 fixed-tuple local
  adapter, MIII actor source;
- terminal consumer: **same-world two-actor event admission and separate
  actor-relative perception**;
- positive oracle: **parent becomes independent participant with persistent state
  ID; Nadia remains focal root**;
- negative oracle: **parent added by replacing focal root, ghost participant or
  private state exposed**;
- restoration/replay: **reopen two actor roots/participation and prevent duplicate
  registration**;
- PW links 05/06/10; grade `SOURCEFREE_S2_ONLY`.

Read through `32` §3 rows 05/06/10 and §4, C01 must make the *existing* P2
objective world admit a stable new actor identity (parent) who participates in
the same objective events as Nadia, while:

1. Nadia stays the one focal `StateIdentity.actor` / P3 developing actor; the
   root, branch, clock and state hash continue to describe Nadia's root.
2. The parent has a persistent actor identity and its own continuing actor state,
   acquired through the *same* objective world/episode machinery (no second world,
   scheduler or person ledger). `P2Owner`'s fixed participant tuple is admitted to
   be a **local adapter restriction**, not generic P3 law, so it may be extended
   at that adapter boundary.
3. Admission binds participants to registered source-bearing actors of the actual
   root; a format-valid proposal naming an unregistered actor, a user, or a
   fabricated "ghost" must fail closed. Re-registration of the same identity is
   idempotent, not a duplicate or a re-root.
4. Actor-relative perception stays separate: an objective co-present event is not
   automatically a qualified percept. Private parent state (hidden reason,
   computation, psyche) must not be projected outward to Nadia or the user, and an
   accession/perception capability must come from the actual registered actor's
   receipts, not narration.
5. Cold reopen of the same root re-reads the same two actor identities,
   participation and event history; no partial/ghost actor survives a crash or a
   refused registration. Duplicate registration must be detected, not silently
   appended.
6. C01 must not fake C02 (parent antecedent/employment), C03 (parent decision/
   action admission), or C04 (utterance/hidden reason split). It only establishes
   the stable identity, shared-world participation and separate perception seam
   those packets will consume.

The governing user intent (`20261111` doc) adds: the focal actor remains Nadia but
participant membership may change; one common occurrence may have distinct
objective, participant-specific and later developmental consequences; objective
world, what others privately know, what Nadia perceives, and what the user sees
must remain distinct. `32` §4.2 explicitly warns that the mother's private
landlord/noise calculation is *not* Nadia's accessible uptake.

## 2. What the pre-existing code actually supplies (before A's C01 commit)

- `contracts.py`: generic `EventProposal.participants: tuple[str, ...]`,
  `StateIdentity(root, actor, branch, clock, state_hash)`, `RealizedEvent` with
  `objective` and `accessible` sections. A `DevelopmentOwner` protocol with
  `snapshot` / `validate_proposal` / `realize`. Nothing freezes participants to
  one actor at this layer.
- `p2_owner.py` before C01: constructor requires
  `participants == tuple(root["actor_ids"])` (`P2_PARTICIPANTS_NOT_BOUND_TO_ROOT`)
  and picks `actor = root["actor_ids"][0]`; `validate_proposal` requires
  `proposal.participants == self.participants` plus `ADMIT_EVENT`, exact
  `source_refs`, future clock, optional interval, real `history_refs`. `realize`
  writes one S47 event through `s.admit_event(case, source, ...)`, snapshots Nadia's
  state, records `actor_experience` compiled from that actor's actual perception
  receipts, and explicitly labels `durable_psychological_transition: MISSING_RULE`
  and `independent_B: CONTROLLED_SOURCEFREE_PARTICIPANT_ONLY`.
- `P2Owner.snapshot()` material digest includes world vars, events, intervals and
  encounters; the world already has two aliases `A` and `B` with `actor_state`,
  and root `actor_ids`. So the pre-existing two-actor fixture is *static root
  configuration*; there is no registration/idempotence/duplicate-refusal path and
  no dynamic addition of a parent identity after root construction.
- `actor_experience(event, after_clock)` refuses if `event.actor_id != self.actor`;
  it uses the event's actual action binding, resolves the alias, and requires the
  actor's own perception receipts before exposing projected events. It removes
  `perceived_by_user`. This is the seed of separate actor-relative perception but
  is hard-wired to the single developing actor.
- `house.py` (B01 A) writes `p6_household` through
  `P2Owner`/`write_material_fact`; the household owner is an existing root actor
  slot ("A"), bound to the actual `world.actor_state` identity. B01's
  `parent_choice_input` is a frozen material input, explicitly
  `parent_decision NOT_EVALUATED`, `first_consumer NONE_VERIFIED`; it is not a
  parent identity or participant registration.
- The world `actor_ids` and `actor_state` are root-level; `WorldState` snapshots
  positions/actor_state/resources/events. The P3 engine selects 3–5
  `EventProposal`s; `P2Owner` is the current local admission adapter.

Therefore the C01 gap is real: the adapter's participant check collapses the
world's multi-actor data to one fixed tuple and one developing actor; a parent
cannot be registered, independently sourced, admitted as a co-participant, or
read through its own perception stream without re-rooting Nadia.

## 3. Concrete positive, negative, restore proof I require before concession

Positive: on one actual P5/P6/P2 state root, register a parent identity with a
persistent state ID; admit one genuinely two-actor event through the existing
world writer with **actual** source-bearing participants; Nadia's root/branch/
actor remain Nadia's; parent actor state persists and cold-reopens; each actor has
its own accessible projection while the objective event is shared.

Negative: attempt to admit the same event with (a) the parent replacing the focal
root, (b) an unregistered/format-only participant or user alias, (c) a duplicate
registration of the same identity, (d) an event whose "source" is merely the
proposal/document rather than a registered owner source, or (e) a private parent
field exposed in Nadia's or the user's accessible projection. Each must refuse or
be provably absent, not merely be untested.

Restore: sever the parent registration/participation and demonstrate Nadia's root
still reopens and the two-actor read fails closed; restore and get the exact prior
identity/history; cold Python subprocess reread yields identical state and no new
owner/scheduler/write.

## 4. Boundaries I will hold B to

- No change to Nadia's `StateIdentity.actor`, root or branch as a side effect of
  parent registration.
- No new world, scheduler, person ledger, psychological owner, trait/motive
  fabrication, `MISSING_RULE → NO_CHANGE`, native/actor/human/source authority.
- Objective registered event ≠ qualified percept; private parent state does not
  become child knowledge or user-visible content.
- C01 must not pre-solve C02/C03/C04; no employment history, decision, utterance,
  hidden reason or durable psychology may be faked as C01 completion.
- The P3 pin break disclosed by B01 is a composition constraint, not something I
  may silently rebase: C01 must record its own pin impact and not pretend the
  current code includes Pair1 B's later fork-aware readers (`362719b40…`).
- Preserve A's historical records; my return is additive under `WORKER_RETURNS/SOROK-DUEL-C01-R1/B_RETURN_R1/` and the
  supporting-actor implementation, not an overwrite of A's handoff/evidence.

## 5. My starting hypothesis (to be tested, not assumed)

A likely implemented a registration/participation layer but may have:
(a) let registration mutate root actor lists or persist an actor identity outside
the verified world checkpoint; (b) accepted `participants`/`source_refs` on
format rather than binding them to actual registered actor state and the real
`admit_event` action; (c) conflated objective participation with each actor's
accessible projection; (d) made retry/duplicate registration append a second
identity or leave a partial actor after refusal; (e) narrowed the focal actor to
the new parent or re-rooted; (f) added a private parent-state field that leaks
through `accessible` or the C12 episode snapshot. I will verify each against the
actual diff, tests and executions before asserting any of it.
