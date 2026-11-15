# PYAT HQ160 — A EXACT REFUSAL-CLASS R6

Status:
`C1_03R_ACCEPTED__C1_03A_EXACT_REFUSAL_CLASS_R6_BOUND__C1_03_JOIN_BLOCKED_ONLY_ON_A`

Decision:
`HQD-2026-10-01-160`

Predecessor:
`20261001-PYAT-HQ159-R-ADOPTED-A-FINAL-REREVIEW-R1 @ 899608db608e85c2cd7baf676d58e795a8a5b004`

Semantic PRE-MAIN:
`902640dfddce431d0c5ba151d3eb851d6b84d7a3`

## C1-03R — remains adopted

Accepted branch:
`integration/pyat-hq159-c1-03r-source-free-accepted-r1 @ 9ec7eaff2646c1effd5192002967407a5c66bbef`

## C1-03A

R5 implementation:
`7a316e4deb655a64853eccdfd719efcd83f140e4`

Final rereview:
`bd16efae659fe3c44f700d756a2016f1dd6b246c`

Disposition:
`CHANGES_REQUIRED`

Everything except the refusal-class boundary is preserved.

Sole blocker:
`C1-03A-R5-FINAL-REVIEW-BLOCK-REFUSAL-CLASS-001`

The current capture catches the `Pre553IntegrityError` family. A canonical subclass such as `Pre553SemanticCollapseError` can therefore be certified as the same AT14 integrity refusal.

R6 bound:
`agent/opencode-pyat-hq160-c1-03a-exact-refusal-class-r6 @ 310dadf0a6057cd6a473e8562532410e40945119`

Launch:
`OpenCode — Space Bunny Free`

R6 law:
witness only an exception whose exact runtime type is `Pre553IntegrityError`; reject all subclasses.

## Join

C1-03 join is blocked only on:
- A R6 return;
- one narrow final rereview;
- HQ adoption of A.

AT17 is already adopted.
R is already adopted.

## Hard prohibitions

No reopening accepted A terrain.
No C1-03 join before A adoption.
No C1-R.
No raw sources.
No C4 without exact later warrant.
No C7.
No PRE-V3→V3 actor/person work.
