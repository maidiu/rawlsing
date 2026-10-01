# PYAT HQ159 — C1-03R SOURCE-FREE ADOPTION

Decision:
`HQD-2026-10-01-159`

Accepted implementation:
`c690bb0b1e6f071c9a640a6825769b96f30dd79a`

Independent final rereview:
`agent/reviewer-pyat-hq158-c1-03r-r3-final-rereview-r1 @ aebb12a160c21b3b1000ab96700120e1c4821f79`

Reviewer disposition:
`APPROVE_AT_DECLARED_GRAIN`

Accepted branch:
`integration/pyat-hq159-c1-03r-source-free-accepted-r1`

## Accepted grain

C1-03R AT18–AT19 source-free lifecycle/replay grain, including:
- Astra Option A generic lifecycle owner extension;
- exactly one generic noncurrent disposition;
- exact R/N partition over affected dependents;
- promotion/rollback shared law;
- error→noncurrent prohibition;
- positive-only historical receipt compatibility;
- negative receipt schema fail-closed behavior;
- duplicate replacement rejection;
- owner-unknown NOT_GOVERNED;
- zero-release known-dependent NOT_GOVERNED / NO_GOVERNING_RELEASE;
- checkpoint A/U independent re-derivation;
- current-vs-historical visibility;
- sealed-successor exact binding and decoy separation;
- mixed AT19 replacement/noncurrent/unaffected witness;
- omitted-edge hostile;
- AT18 replay-grade separation.

## Nonblocking residuals

1. `R3-NB-EXCEPTION-WORDING-001`
   - legacy adapter exception class/message `OwnerUnknownDependent / OWNER_UNKNOWN_DEPENDENT` is coarse for the owner-known zero-release case;
   - authoritative lifecycle owner state/reason remain correct;
   - adapter fails closed and returns no current product;
   - maintenance only, not a lifecycle/currentness blocker.

2. `F-2`
   - unknown extra top-level serialized receipt field is dropped/unhashed;
   - no authority-laundering path found;
   - strict schema closure remains an owner-versioning decision.

## Court

Implementation return reported:
`167 passed, 0 failed, 0 errors, 0 skipped`

Final independent rereview reconciled that exact four-suite court and found no blocking counterexample.

## Scope ceiling

This adoption does not authorize:
- raw-source execution;
- C4/C7;
- C1-03 join before C1-03A adoption;
- C1-R;
- V3 actor/person implementation.

AT17 remains separately adopted.

Terminal:
`C1_03R_R3_ADOPTED_AT_DECLARED_GRAIN`
