# 03_P6_USER_GO_REAL_WORLD_WRITE

**Domain**: P6_WORLD_EVENT; **Seams**: XS:014;E002; **Grade**: MERGED_PROTECTED_SOURCEFREE_TRUE_WORLD_EVENT_WRITE.
**Protected source**: `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` at `6a5c12f04323d74001f9632063ec907f4fc4468e`, Git blob `af556c143e7e4eaa2f60a68fa402954091737dd4`, lines 247-295.

## Inputs and authority
User GO/INSPECT action in P6 sourcefree two-room house, actual world clock, room positions, object availability and P4 session.

## Concrete producer→consumer transformation
house.perform admits only in-scene and available target, commits world.positions[user], MOVE/INSPECT event and P6_HOUSE_CONDUCT episode, checkpoints world. MOVE perceived user; INSPECT additionally invokes _perceive_if_present A/B.

## Output and meaning
Exact performed world event, source event hash, position mutation and user/public projection; named sourcefree actor presence hook for INSPECT.

## Protective negative
Unavailable room edge/item refuses. User MOVE is not automatically actor-perceived by A/B. An event is sourcefree material occurrence, not direct actor awareness.

## First reader and actual grade
P6 run_p6 conduct=writer, then PACE, optionally movement_evidence and reconsider.

## Discriminating next test (NOT_RUN in R7)
Player GO with actor other-room or unqualified sightline must not create Nadia sensory registration despite committed MOVE.

**Exact evidence records:** R7:EV:02;R7:EV:09;R7:EV:10;R7:EV:11;R7:EV:19

No newly minted original historical function or native human-science/actor source authority. Current sourcefree code is real; native scientific equivalence remains a separately owned question.
