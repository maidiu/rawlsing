# 08_ACTOR_INITIATIVE_COMMITTED_MOVE

**Domain**: P6_ACTOR_ACTION; **Seams**: XS:014;E002; **Grade**: SOURCEFREE_REAL_ACTOR_MOVE_CODE_PRESENT__NATIVE_SCIENCE_NOT_ISSUED.
**Protected source**: `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/actor_initiative.py` at `6a5c12f04323d74001f9632063ec907f4fc4468e`, Git blob `c9d2e1e93314ef2ec2dd767f998fd2775be78663`, lines 99-263.

## Inputs and authority
Grounded actor selection action VISIT_ADJACENT, route source SOURCEFREE_ACTOR_LOCAL_ADJACENCY, exact actor/world checkpoint, packet, clock, room and declared eligibility.

## Concrete producer→consumer transformation
_select_visit verifies all identity/route/action/decision fields and stores session-local one-shot token. visit_adjacent_room rechecks fresh checkpoint, consumes token before writer IO, moves A, creates MOVE event and actor episode, projects user perception only if eligible.

## Output and meaning
True sourcefree actor A world MOVE, committed position, source event/hash and episode, distinct from mere model thought and user private gaze.

## Protective negative
Missing/stale token, wrong source/hash/actor/route, unavailable target fail. Failure after token consumption is P4 pending operation, not automatic replay.

## First reader and actual grade
situated.reconsider → _select_visit → visit_adjacent_room → P4 world writer

## Discriminating next test (NOT_RUN in R7)
Force stale clock after selection; deny duplicate event, then exact restore under authorized P4 pending semantics.

**Exact evidence records:** R7:EV:15;R7:EV:24;R7:EV:02

No newly minted original historical function or native human-science/actor source authority. Current sourcefree code is real; native scientific equivalence remains a separately owned question.
