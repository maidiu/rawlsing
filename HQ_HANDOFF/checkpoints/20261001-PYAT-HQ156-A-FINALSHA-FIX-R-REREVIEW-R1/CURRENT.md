# PYAT HQ156 — A FINAL-SHA FIX / R REREVIEW

Status:
`C1_03A_R4_FINALSHA_DEFECT_CORRECTION_BOUND__C1_03R_R2_REREVIEW_BOUND__C1_03_JOIN_BLOCKED`

Decision:
`HQD-2026-10-01-156`

Predecessor:
`20261001-PYAT-HQ155-DUAL-C1-03-NARROW-CORRECTIONS-R1 @ e157782e4aa063cf74368fd3c3ec93851a7f5fe5`

Semantic PRE-MAIN:
`902640dfddce431d0c5ba151d3eb851d6b84d7a3`

## C1-03A

Returned:
`3bd481163ac1b2b1e30817b2704e89341099a960`

Worker disposition:
`PASS_C1_03A_REFUSAL_AUTHENTICITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

HQ intake found a direct defect in the exact final SHA:

`OwnerStateProjection.from_empirical_integrity_refusal`
has two consecutive `@classmethod` decorators.

That exact code is non-callable in Python and raises:
`TypeError: 'classmethod' object is not callable`.

Therefore the claimed 208-pass court is not accepted as final-SHA proof.

Surgical correction bound:
`agent/opencode-pyat-hq156-c1-03a-r4-finalsha-callability-r1 @ b2b62c14f4b9a1ec7c97094a2d1ac4101f63314d`

Launch:
`OpenCode — Space Bunny Free`

The refusal-authenticity design is not reopened.

## C1-03R

Returned:
`7f64493758f6b3b77d7e9ce1486c1324ff709edc`

Worker disposition:
`PASS_C1_03R_OWNER_FAILCLOSED_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

Reported court:
`160 passed, 0 failed, 0 errors, 0 skipped`

Narrow independent rereview bound:
`agent/reviewer-pyat-hq156-c1-03r-r2-rereview-r1 @ f6e2b059883bee29b2dadfc1cc59df7a5a4c7735`

Launch:
`Browser — GPT-5.6 Sol High`

Reviewer must explicitly adjudicate:
- duplicate positive replacement rejection;
- strict negative serialization/schema law;
- owner-unknown NOT_GOVERNED behavior;
- known-but-never-transitioned CURRENT reading;
- checkpoint A/U re-derivation;
- genuine mixed rollback witness.

## Join

Still blocked until A and R are independently accepted and HQ-adopted.
AT17 remains already adopted.

## Launch now in parallel

1. A final-SHA callability correction — `b2b62c14...`
2. R narrow Browser rereview — `f6e2b059...`

## Hard prohibitions

No C1-03 join yet.
No C1-R.
No raw sources.
No C4 without exact later warrant.
No C7 implementation.
No PRE-V3→V3 actor/person implementation.
