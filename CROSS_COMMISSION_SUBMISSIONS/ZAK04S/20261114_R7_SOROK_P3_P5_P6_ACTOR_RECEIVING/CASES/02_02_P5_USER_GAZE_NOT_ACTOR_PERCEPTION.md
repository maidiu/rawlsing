# 02_P5_USER_GAZE_NOT_ACTOR_PERCEPTION

**Domain**: P5_USER_EXPOSURE; **Seams**: XS:014; **Grade**: PROTECTED_SOURCEFREE_PRESENTATION_READER__ZERO_ACTOR_SOURCE.
**Protected source**: `WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1/gaze.py` at `6a5c12f04323d74001f9632063ec907f4fc4468e`, Git blob `554c3388193fad754412776de842e18f3ba28c6c`, lines 17-85.

## Inputs and authority
Received P4 public projection with event IDs, perceived_by_user flag, user attention history (up to 12 distinct event choices).

## Concrete producer→consumer transformation
visible_events excludes anything not user-perceived; attend records an explicit existing event ID once; orientation ranks channel under recent history; render chooses up to two details preserving source event IDs and verbatim spoken text.

## Output and meaning
User-visible narration and private user attention orientation. No actor-world mutation or Nadia epistemic claim.

## Protective negative
User gaze does not create an event/actor sensory cue. Excluded/unperceived event cannot enter output; repeating attend event has no new effect.

## First reader and actual grade
P5.run_p5.render; P6 imports same gaze.render for user output; not a Sorok C11 actor fact.

## Discriminating next test (NOT_RUN in R7)
Same actual world and actor recorded perceptions, change only gaze history: actor reasoning inputs and world must stay the same.

**Exact evidence records:** R7:EV:02;R7:EV:07;R7:EV:08;R7:EV:16;R7:EV:19

No newly minted original historical function or native human-science/actor source authority. Current sourcefree code is real; native scientific equivalence remains a separately owned question.
