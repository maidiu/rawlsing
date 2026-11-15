# HQ207 — R9 bounded repair + service-source applicability independent review — R1

Status:
`R9_REVIEW_ACCEPTED__BOUNDED_PORTING_REPAIR_AUTHORIZED__SERVICE_SOURCE_IMPLEMENTATION_READY_FOR_HOSTILE_REVIEW`

Control base:
`6879e657b6c5b010b755a5a81781eafa929e91d4`

Inputs:
- R9 fan-in candidate: `dfdf5659fd78e9bc996b07383349094059a5553d`
- R9 independent adjudication: `7a5cf25ab3fb98fe5311e0a394b4432a498f6546`
- service-source implementation candidate: `e7d3598494472a9aea7dd2c69f6aacb11585905c`

## R9 adjudication

HQ accepts:
- the 55-test R7 denominator belongs to the accepted C4C3 lineage, not current control;
- current control must NOT import foreign C3 production merely to satisfy that denominator;
- current-control qualification must use its own sanctioned court set plus the reachable 25-test R7 subset;
- the two SR06 failures are a porting gap caused by pairing the accepted decoder with the old SR06 test;
- both invariants remain binding and no test retirement is authorized;
- the accepted SR06 test blob `dfd063227e4a0897` is the correct co-evolved test for decoder `b406d45fae419c02`;
- the governed R7 interpreter exists and must be used for the repair qualification.

Authorized repair:
1. retain the accepted R9 runtime blobs already placed by `dfdf5659...`;
2. adopt the accepted SR06 test revision only;
3. rebase the fan-in qualification criterion onto current-control sanctioned courts + reachable R7 subset;
4. rerun R9 and reachable R7 courts in the governed interpreter;
5. no decoder changes, no C3 production backport, no test retirement, no environment reconstitution.

## Service-source applicability adjudication

The implementation candidate `e7d35984...` is strong but not yet adopted.

Independent hostile review is required against the HQ-ratified authority form:
`ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`.

Review must attack:
- exact request-key completeness;
- state-family separation;
- COMPLETE vs INCOMPLETE honesty;
- NO_ADMITTED_SOURCE only under COMPLETE coverage;
- absence of ranking/selection/pooling/backfill/currentness/permission-grant/F8-transform power;
- evidence-sufficiency noncollapse;
- replay-only canonical ordering;
- zero-regression and court adequacy.

## Pending HQ206 returns

Still not visible on origin at this checkpoint:
- C1 prune repair;
- V556 repair;
- F7 temporal authority contract.

They remain independent and should be pushed, not rerun.

No Astra referral.
No raw/live/warrant/C7/actor work.
