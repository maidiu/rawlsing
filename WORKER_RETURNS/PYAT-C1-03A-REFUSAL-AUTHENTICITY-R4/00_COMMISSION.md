# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03A — REFUSAL-AUTHENTICITY CORRECTION — R4
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq155-c1-03a-refusal-authenticity-r4`

Exact base:
`767bb9139b80e774093af8e765e57ee57a19e005`

Independent rereview:
`agent/reviewer-pyat-hq154-c1-03a-r3-rereview-r1 @ 3ebde6d268abcb005a48e42eb6d0b52ec4a3c025`

Disposition:
`CHANGES_REQUIRED`

Blocking issue:
`C1-03A-R3-REVIEW-BLOCK-REFUSAL-AUTHENTICITY-001`

This is a narrow AT14 refusal-authenticity correction. Do not reopen R3 G5, E/F/G factory authenticity, AT15, AT16, C1-02, or any owner module.

## Problem

R3 still permits trusted refusal state to be minted from:

`Pre553IntegrityError("caller") + caller ExactRef + caller supporting refs`

or

`Pre553AuthorityError("caller") + caller ExactRef + caller supporting refs`.

Exact exception type is not provenance. Both exceptions are publicly constructible and carry no binding to an actual competent owner execution.

Therefore callers can fabricate:
- `INTEGRITY_FAILURE`;
- `BLOCKED_REQUIRED_AUTHORITY`;
- exact-input custody/provenance.

## Required law

A trusted refusal projection MUST be derived from an actual competent owner execution or from an already-existing canonical owner-produced refusal witness that cryptographically/semantically binds the refused object/context.

A bare exception instance is never sufficient proof.

A caller may not independently choose:
- the retained refusal state;
- the producer/input ref;
- supporting refs;
- owner label.

## Required correction

Inspect the current empirical-query and exact-discovery/authority owner paths and choose the smallest lawful mechanism.

Preferred order:

1. If a canonical current owner-produced refusal witness/receipt already exists and binds the exact refused object/context, consume it.
2. Otherwise introduce a bounded wrapper in the C1-03A module that invokes the ACTUAL competent owner operation itself, catches only the exact expected refusal type, and derives the refusal projection plus exact provenance solely from the same owner-call inputs/result context.

Do NOT accept a caller-supplied exception as authority.
Do NOT accept a caller-supplied producer_ref/supporting_refs separately from the owner execution.

If the exact owner execution cannot expose enough identity to bind AT14 without modifying an owner module, return `EXISTING_OWNER_OR_AUTHORITY_GAP__HQ_ADJUDICATION_REQUIRED` with the minimal counterexample. Do not fabricate a receipt.

## Preserve exact state distinction

The R2 subclass trap remains controlling:

`Pre553AuthorityError` subclasses `Pre553IntegrityError`.

The lawful refusal path must still distinguish:
- empirical integrity refusal -> `INTEGRITY_FAILURE`;
- exact required-authority refusal -> `BLOCKED_REQUIRED_AUTHORITY`.

Do not use broad `isinstance` classification that collapses them.

## Required hostiles

At minimum prove:

1. manually constructed exact `Pre553IntegrityError` cannot mint trusted state;
2. manually constructed exact `Pre553AuthorityError` cannot mint trusted state;
3. a genuine owner-generated integrity refusal cannot be rebound to another object ref;
4. a genuine owner-generated authority refusal cannot be rebound to another object ref;
5. arbitrary supporting refs cannot be injected;
6. the actual empirical owner execution still yields `INTEGRITY_FAILURE`;
7. the actual authority/discovery owner execution still yields `BLOCKED_REQUIRED_AUTHORITY`;
8. those two states remain distinct;
9. G5 remains closed;
10. AT15 genuine ADMITTED route still passes;
11. AT16 54/6 remains SUPPORTED;
12. the stale short-circuited `coverage_custody.completeness_state` reference noted by the reviewer is removed if it is in the commissioned C1-03A module, without altering handoff semantics.

## Preserve

All accepted R3 work remains mandatory:
- exact owner-family gates;
- fixed owner labels;
- adaptive determinant provenance;
- receipt dominance;
- contradictory positive requested_use refusal;
- learned route obligation law;
- recursive custody law;
- no invented completeness;
- eight negative states distinct;
- adaptive UNVISITED real;
- AT16 positive consumer witness;
- C1-02 untouched.

## Write terrain

Modify only:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-REFUSAL-AUTHENTICITY-R4/**`

Do not modify empirical/discovery owner modules. If owner modification is genuinely required, STOP with the typed owner gap.

## Court

Run the same ten-file R3 court plus new refusal-authenticity hostiles.

Historical R3 court:
`199 passed, 0 failed, 0 errors, 0 skipped`.

Record new exact counts; no broader sweep claim.

## Return

Write:
`WORKER_RETURNS/PYAT-C1-03A-REFUSAL-AUTHENTICITY-R4/**`

Required:
- `00_RETURN.md`
- `01_REVIEW_BLOCKER_DISPOSITION.json`
- `02_REFUSAL_AUTHENTICITY_RECEIPT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C1_03A_REFUSAL_AUTHENTICITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `EXISTING_OWNER_OR_AUTHORITY_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption. No raw sources. No C4/C7. No C1-03 join. No C1-R. No V3.

Terminal:
`C1_03A_REFUSAL_AUTHENTICITY_RETURNED__HQ_ADJUDICATION_REQUIRED`
