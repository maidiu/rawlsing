# Pyat HQ — C1-02 adopted; N10E correction in narrow rereview

Checkpoint: `20261001-PYAT-HQ145-C1-02-ADOPTED-N10E-REREVIEW-BOUND-R1`

Governing decision:
`HQD-2026-10-01-145`

## C1-02

Accepted implementation:
`bc661188b51e995d9f5d74e55c4e37d2ba358a17`

Independent rereview:
`59d69ba31b8de2d028bd44048e8d7b75f2d82538`

Disposition:
`APPROVE_AT_DECLARED_GRAIN`

Banked integration branch:
`integration/pyat-hq145-c1-02-source-free-accepted-r1`

Integration head:
`bc661188b51e995d9f5d74e55c4e37d2ba358a17`

Accepted grain:
`SOURCE_FREE_AT08_AT13`

Recorded court:
`109 passed, 0 failed, 0 errors, 0 skipped`

Nonblocking documentary correction:
`REREVIEW-DOC-CORRECTION-PRE-REPAIR-EXACT-VALUE-001`

Do not cite the repair packet's historical exact-value row as a valid pre-repair DID-NOT-RAISE witness. The valid false-semantic-ref and ordering-sentinel reproductions independently establish the pre-repair defect.

## N10E

Correction return:
`52e41a41e8bc3b77390016a049095b5aea1721d0`

Disposition:
`PASS_PROOF_AND_PROVENANCE_CORRECTED__NARROW_INDEPENDENT_REREVIEW_REQUIRED`

Provider implementation blob remains:
`23167aa25291fb148b1e3cf210ac33fe7769b783`

Final corrected court:
`88 passed, 0 failed, 0 errors, 0 skipped, 15.14s`

Narrow rereview:

**LAUNCH IN: Browser — GPT-5.6 Sol High**

Branch:
`agent/reviewer-pyat-hq145-n10e-proof-provenance-rereview-r1`

Commission tip:
`80eb275f40ffb2d096433c218fecb009063a0bd1`

Commission:
`WORKER_RETURNS/PYAT-N10E-PROOF-PROVENANCE-REREVIEW-R1/00_COMMISSION.md`

## C1-03 wake condition

C1-02 dependency is satisfied.

C1-03 is ready except for final N10E AT17 provider-core acceptance. Do not duplicate AT17 while that provider is one narrow rereview from adoption.

After N10E acceptance, bind C1-03 AT14-AT19 against:
- accepted C1-02 higher-order/recursive composition;
- accepted N10E AT17 provider seam;
- existing lifecycle/direct/learned/replay/dependency owners.

No raw-source execution.
No C4 execution.
No PRE-V3→V3 actor implementation.
