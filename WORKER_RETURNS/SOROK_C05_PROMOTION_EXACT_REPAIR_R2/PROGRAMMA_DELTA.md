# PROGRAMMA_DELTA — C05 R2 exact promotion repair

**Disposition:** `AUTHOR_C05_R2_CANDIDATE_FOR_SAME_NONAUTHOR`
**Candidate:** `5d771dd86767655534b23576075e5da2db4fba78`
**Frozen start:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Grade:** `SOURCEFREE_S2_C05` / `SOURCEFREE_S2_ONLY`

## Corrected

- `promote_relation` now computes its pre-write current depth from the full
  verified scope history including prior `PROMOTE` episodes.
- A second depth-2 promotion with a new operation ID refuses
  `RELATION_PROMOTION_NOT_DEEPER` before any append: zero episode, change,
  head, world-event, perception or checkpoint delta.
- Relation history/context remain `QUALIFIED` and byte-exact; the original
  promotion retry and fresh-process cold remain exact.
- One-line product patch; `supporting_actor.py` and all other product unchanged.

## Preserved

- Original C05 positive/negative/cold path, original 5 tests, 89-check
  independent normal/negative/cold probe, C01 6, C04 identity 6, C04 custody
  12, P2 owner 5.
- Caller-supplied exposure/relations, both-party exposure, `DATED_EXPOSURE_ONLY`,
  no owner receipt for relation knowledge, coherent public append boundary.
- Normal physical event `PERCEIVED` remains distinct from relation exposure.

## Not released

Native ADP-015/C4 relation authority, household/genealogy issuance, maternal
psychology, independent volition/autonomy, generated language, G2 selection,
complete J1/Nadia response, D04/D05, durable acquisition, human/scientific/
source-rights receiving, protected merge, #939 fleet, PYAT/Browser actions,
concurrent same-operation uniqueness, branch-fork replay, depth > 2, C04
parent-metadata/D03 residuals.

## Next gate

Same nonauthor reviewer’s one focused readback of this frozen candidate. No
self-G5, new opponent, automatic author round or new campaign. STOP after this
correction.
