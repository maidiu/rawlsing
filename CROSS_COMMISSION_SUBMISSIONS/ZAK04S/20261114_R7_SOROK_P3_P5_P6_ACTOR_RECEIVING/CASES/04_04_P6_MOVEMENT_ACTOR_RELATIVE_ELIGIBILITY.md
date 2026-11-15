# 04_P6_MOVEMENT_ACTOR_RELATIVE_ELIGIBILITY

**Domain**: P6_MOVEMENT_CUE; **Seams**: XS:014;E002; **Grade**: SOURCEFREE_ELIGIBILITY_READER_FOUND__REGISTRATION_OWNER_HELD.
**Protected source**: `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/encounter.py` at `6a5c12f04323d74001f9632063ec907f4fc4468e`, Git blob `cc88eec8c01bae59501126b8a9c8eee41e18e1ba`, lines 20-72.

## Inputs and authority
Committed GO event+episode, root/branch/clock/room, optional VISUAL_FIXTURE with sightline and actor-specific facing/location.

## Concrete producer→consumer transformation
movement_evidence checks exact event, world, source and episode parent; computes A/B modality by location and facing; emits ELIGIBLE, UNAVAILABLE or UNKNOWN, with distinct uptake HOLD_ACTOR_REGISTRATION_OWNER_MISSING for eligible.

## Output and meaning
Actor-relative sensory eligibility receipts with cue source/hash and unmet durable registration note; no direct actor memory.

## Protective negative
Without exact sourcefree fixture, produces UNKNOWN (not seeing). Facing away produces UNAVAILABLE. Forge event/episode or stale source refuses.

## First reader and actual grade
P6.run_p6 passes only ELIGIBLE A rows to situated.reconsider; registered-perception writer remains distinct.

## Discriminating next test (NOT_RUN in R7)
Same GO with A facing doorway vs away, B facing away: distinct traceable eligibility and no invented durable memory.

**Exact evidence records:** R7:EV:10;R7:EV:11;R7:EV:23;R7:EV:19

No newly minted original historical function or native human-science/actor source authority. Current sourcefree code is real; native scientific equivalence remains a separately owned question.
