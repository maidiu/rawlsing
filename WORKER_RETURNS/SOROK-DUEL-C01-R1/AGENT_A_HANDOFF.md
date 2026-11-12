# SOROK C01 AGENT A — adversarial construction handoff

**Packet:** C01, `Stable other-actor identities and dynamic participation without changing Nadia root`, CG-C.
**Grade:** `SOURCEFREE_S2_ONLY`. No native ADP-015/C4, CAN/ADP/Pyat, actor/human/source right, or protected merge is issued.
**Branch:** `codex/sorok-duel-c01-a-20261112-r1`.
**Implementation SHA:** `9229698c5ded4e8c77801398d4d0ecc3e7c9ccb3`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a` (programme PR #938).
**Frozen start / B01 cut:** `edbb4b344d54731a527fd415a965bc848ed964e1`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. Exact artifact

Changed product code:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/supporting_actor.py` | New adapter: stable supporting registration, participant resolution, C12 perception participation receipts, public/self-only actor reads, replay severance verification. |
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | `P2Owner.__init__`, `validate_proposal`, `realize/_realize` participant-admission path only. Module-level material functions, `material_fact`, `house.py` and P3 were not edited. |

Return/evidence files are under `WORKER_RETURNS/SOROK-DUEL-C01-R1/`.

Commands actually run from this worktree with the qualified environment:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-C01-R1/test_c01_supporting_actor.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_scene_context.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_engine.py \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_model_cycle.py \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_recursion_integration.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore" \
  "WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_g_actor_and_user_views_are_narrower_than_objective_state"
```

## 2. Governing contract

The frozen C01 packet requires: a parent becomes an independent participant with a persistent state ID while Nadia remains the focal root; the terminal consumer is same-world two-actor event admission and separate actor-relative perception; the negative is parent-by-root-replacement, ghost participant, or private-state exposure; restoration is reopening two actor roots/participation and preventing duplicate registration. Dependencies: B01. PW links 05, 06, 10.

Governing sources actually read:

- `02_SOROK_IMPLEMENTATION_PROGRAMME_R1.md` C01 and proof-grain gate.
- `20261111_ROLLING_PERSON_WORLD_DURATION_MATERIAL_MEDIATION_R1.md`: one Nadia-centered historical root may contain independent/opaque parents; different actor-relative experiences; no second scheduler/duplicate world/time ledger; material conditions are practical, not object psychology.
- `32_ROLLING_PERSON_WORLD_OWNER_RECONCILIATION_20261111_R1.md` lines 21, 60 and 64: `StateIdentity.actor` need not change for other participants, generic `EventProposal.participants` exists, fixed tuple/`ADMIT_EVENT` belongs to the current P2Owner adapter; PW-06 is `EXTEND_DYNAMIC_PARTICIPATION`; PW-10 is `INTEGRATE_SAFELY; NO_SECOND_LEDGER`.
- B01 frozen handoff/ABI/code at `edbb4b344d54731a527fd415a965bc848ed964e1`, including its P6 household and P2 material-fact boundary.
- Full `01_USER_ORIGINAL_DUEL_PERSONAS_UNABRIDGED.md`, `03_TASK_PACKETS_R1.json`, `04_CODEX_RELAY_AND_CONTRACT_EVOLUTION_R1.md`, `05_CODEX_LAUNCH_PROMPT_R1.md`.

The two full ChatGPT Library architecture records remain **NOT_INSPECTED locally**; their identities and that limitation are preserved. No contents are claimed.

## 3. Strongest achieved result

A real generated S44/P2 root can now register a parent as a distinct supporting stable ID without changing the root actor list:

```text
register_supporting_actor(
    session, alias="P", actor_id="TEST_ONLY_C01_PARENT", role="parent",
    private_state={"motive": <secret>}
)
```

Actual writer path:

```text
supporting_actor.register_supporting_actor                    supporting_actor.py:165
  -> branch actor_ids += P (same mutable metadata path used by first_session.py:110 for U)
  -> C12Store.append_episode (kind P2_SUPPORTING_ACTOR)       bp4/store.py:146
     private state lives only in this episode; world row stores hash/ID
  -> world.actor_state[P] + world.positions[P]
  -> BP4Product._checkpoint                                   bp4/product.py:101
  -> C12Store.checkpoint                                      bp4/store.py:216
  -> WorldState.snapshot                                      bp4/world.py:323
```

`P2Owner.realize` with participants `(focal_actor_id, supporting_actor_id)`:

- verifies the focal actor is present and the parent is live, registered and co-present;
- admits the actual P2 event through the existing S47/S42 path;
- records the parent's C12 perception of the same performed world event;
- writes a public `P2_SUPPORTING_PARTICIPATION` episode with event hash, role, source and access channel;
- returns `consequences.supporting_participation = RECORDED` and public participant receipts.

Demonstrated evidence:

- **Positive producer → first reader:** 5/5 C01 tests pass. The parent is a distinct stable ID in branch actor IDs and world actor state; the root actor list and `P2Owner.actor` remain Nadia/focal.
- **Changed-value/dynamic participation:** an owner created with root participants can later admit a registered parent; a separately created owner can bind `(focal, parent)` additively. A proposal with the parent participates only when the parent is registered and co-present.
- **Separate actor-relative access:** both focal and parent have `PERCEIVED` receipts for the same event with distinct viewer identities; for a prior `ARRIVAL` event the focal actor is `PERCEIVED` while the later-registered parent is `NOT_PERCEIVED` with no event content.
- **Private state:** the secret is absent from the world snapshot, the event body, `RealizedEvent.accessible`, `RealizedEvent.objective` and both public access reads. The self read (`as_actor=parent_id`) returns it; the public read returns `NOT_READ`. A fabricated event containing the secret refuses `SUPPORTING_PRIVATE_STATE_LEAK`.
- **Duplicate registration:** the second identical registration returns `UNCHANGED` with unchanged episode/checkpoint/world-event/perception counts. Replay is idempotent.
- **Severance/restoration:** replay refuses `P2_SUPPORTING_PARTICIPATION_SEVERED` when the parent perception is hidden from the reader; restoring the real perception makes replay return the exact stored result.
- **Cold:** a fresh Python subprocess opens the same state root and reads the same parent registration and two actor-relative perceptions; a close/reopen in-process test also verifies snapshot equality, replay equality and unchanged counts.
- **Regression:** P2 owner 5/5, P3 owner 9 passed/1 skipped, B01 4/4, engine/model-cycle/integration 66/66, P6 actor scene 2/2, selected P3 cold-replay/view tests 2/2.

## 4. Own hostile findings

1. **Private state was initially in `world.actor_state`.** The full world snapshot and the S42 event read's `world_before/world_after` would have exposed it in the developer objective record. I moved actual private state into a C12 registration episode and left only its hash/ID in the world. The world snapshot, event objective, accessible record and public reads no longer contain the secret. The remaining exposure is raw C12 episode access by a developer/holder of the store; that is disclosed, not concealed.
2. **Participant validation could have passed empty co-presence.** I added a nonempty focal position check and a focal-alias resolution requirement before comparing positions.
3. **Actor-ID collision with the user.** Registration now refuses a stable ID already used by any existing alias, not just root actor IDs.
4. **Replay could have accepted a severed perception.** `verify_supporting_participation` now checks the event hash/clock, perception row, participation episode body, alias, role and source. The test patches the perception reader to prove replay fails closed and restores.
5. **Duplicate registration could have appended duplicate episodes.** Registration searches for the exact private-state episode body first and returns `UNCHANGED` for an identical registration; the tests assert unchanged counts.
6. **P3 code pins break.** `p2_owner.py` is byte-pinned by `P3Owner._code_pins()`. This return changes that pin; pre-C01 P3 state roots will refuse cold reopen. Same-code roots reopen exactly and P3 owner tests pass. No migration was invented.
7. **First version of the private-state design was weaker.** I repaired it after noticing `result.objective` contained the world snapshot; the final test asserts the secret is absent there.

## 5. Unresolved challenges

- **Parent is not yet an author.** C01 records parent participation/perception of the focal actor's performed event. C03 must implement parent-authored decision/action/utterance; C04 must separate hidden reason, performed utterance and Nadia-qualified uptake.
- **No parent antecedent/continuation.** C02 must add independent parental history/activity and material conditioning. This return only gives the stable identity and participation boundary.
- **No relations/dyads.** C05 must extend roles beyond `parent` and prove relationship history, forks and separate access.
- **No situated-field read for a next actor decision.** D02 must consume public receipts, not the raw world snapshot or private episode.
- **No native actor identity.** This is an engineering registration over the existing C12 branch/world, not ADP-015/C4 issuance. It does not create a child, household, relationship entity or genealogy.
- **Fork/copy is not proven.** Branch fork copies the registration and private episode, but no fork-specific C01 test was run.
- **Private-state leak guard is string-only.** It scans string values from private state in the event canonical. Non-string private values are not leak-scanned.
- **Full P3 vertical-slice suite did not finish within 900 s** (3 tests passed before the timeout). Selected cold-replay/view tests passed. No full-estate claim.
- **Controller/provider cost unknown.** No token, latency, RSS or retry instrumentation was available or invented.

## 6. Likely attack surfaces for SAME B

- Replace the branch-actor row registry with an existing C4/ADP-015 actor-source record while preserving stable cold identity and no duplicate registration.
- Prove fork/copy behavior: parent registration, private episode, participation perception and duplicate prevention across a real branch fork.
- Make a **next actual consumer** read the parent's public access and change a real decision; this return stops at the adapter reader.
- Attack the direct `UPDATE branch SET actor_ids` metadata write: crash between branch update and checkpoint, concurrent registration, orphan episode reuse, and cold reconciliation.
- Try to make an absent or ghost parent participate through an alias, fork, user actor, or root actor collision.
- Try to leak private state through event summary/body, projection public fields, `RealizedEvent.objective`, participation episode, hash-only world row, or a self-read authorization bypass.
- Try to make replay accept a participation episode whose event hash/clock/role/source is forged but whose perception row exists.
- Try to break the P3 code-pin disclosure by reopening an old root; that is expected refailure, not a hidden success.

**Hardest concrete challenge for SAME B:** implement the next real consumer of this boundary — a parent-authored performed act in the same P2 world (C03 direction) or a D02 situated-field read that changes an actual later decision from the parent's public access — without adding a second actor owner/scheduler and while keeping Nadia's focal root, private-state non-leak and cold replay exact. A registration/reader-only improvement will not defeat this cut; a real second actor-authored operation with downstream effect will.

## 7. Rejected alternatives

- **Use fixed actor B or user U as the “parent.”** Rejected: the packet says do not relabel fixed A/B as generic participation; U is the portal user. The parent is a new stable supporting ID.
- **Change `StateIdentity.actor` to the parent.** Rejected: Nadia remains focal; root actor list and `P2Owner.actor` stay unchanged.
- **Add a `SupportingActorOwner`, second scheduler, actor database or world.** Rejected: reuses C12 branch/world/checkpoint/perception and P2Owner; no duplicate ledger.
- **Store private state directly in `world.actor_state`.** Rejected after hostile testing: it entered the world snapshot and event objective. Private state now lives in a C12 registration episode; world stores only hash/ID.
- **Treat a registered parent as a ghost/id-only participant.** Rejected: participation requires live registration, branch membership, world actor state and co-presence; perception rows are actual C12 receipts.
- **Call `read_supporting_actor` with `as_actor` omitted and return private state.** Rejected: public read returns `NOT_READ`; only the same stable ID self-read returns private state.
- **Let any role token register.** Rejected for C01: role allowlist is `parent` only. C05 must deliberately extend it.
- **Use a second world event to represent parent participation.** Rejected: the parent perceives the same focal event; a second event would fabricate an occurrence. C03 owns parent-authored events.
- **Claim old P3 roots survive.** Rejected: the code-pin break is real and disclosed.

## 8. Proof boundaries

Do not claim any of the following from this return:

- Native ADP-015/C4 actor identity, relationship/household/genealogy, CAN/ADP/Pyat science, human validity, source/use rights or protected merge.
- A parent decision, parent-authored action, parent utterance, hidden motive accessible to Nadia, or a parent first consumer.
- C02 antecedent/activity, C03 decision/action admission, C04 utterance/uptake, C05 relations/variable-depth actors, D02 situated field, J1/J2.
- Relationship entity, household membership, child generation, or independent parent movement.
- Fork/copy equivalence; only same-branch cold reopen and fresh-process read are proved.
- Private-state protection against raw C12 store access; the private episode is developer-visible there.
- Non-string private-state leak coverage.
- Full P3 vertical-slice or full-estate coverage.
- Cheap/small cost: controller/provider cost is `UNKNOWN`; only bounded test wall times are recorded.

## Measured cost and limits

| Command | Result | Evidence |
|---|---|---|
| C01 packet tests | 5 passed in 13.19 s | `evidence/c01_supporting_actor.log` |
| P2 owner regression | 5 passed in 15.26 s | `evidence/p2_owner_regression.log` |
| P3 owner regression | 9 passed, 1 skipped in 29.90 s | `evidence/p3_owner_regression.log` |
| B01 adjacent regression | 4 passed in 33.88 s | `evidence/b01_adjacent_regression.log` |
| Engine/model-cycle/integration | 66 passed in 160.27 s | `evidence/engine_regression.log` |
| P6 actor scene | 2 passed in 25.32 s | `evidence/p6_actor_scene_regression.log` |
| Selected P3 vertical slice cold/view | 2 passed in 333.51 s | `evidence/p3_vertical_selected_regression.log` |
| Full P3 vertical slice | timed out at 900 s after 3 passing tests | not counted as a completed run |

Controller/provider token use, latency, process RSS and retry cost: `UNKNOWN`. No controller or provider instrumentation was available or invented.

Hard limits: `SOURCEFREE_S2_ONLY`; parent role only; participation is perception/co-presence of a focal performed event; private state is C12-developer-visible but not actor-accessible; same-code cold only; pre-C01 P3 roots break; full estate unrun.
