# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03A — INDEPENDENT-REVIEW REPAIR — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq150-c1-03a-review-repair-r1`

Exact implementation base:
`a3c07426b0ad547287cc729b23cd8428c9fc0018`

Independent review:
`agent/reviewer-pyat-hq149-c1-03a-r1 @ 6bc1cb8ecd5568d6e78e83916763f125e8b888c8`

Review disposition:
`CHANGES_REQUIRED`

This is a bounded repair of the existing C1-03A implementation. Do not reopen C1-02 or redesign the analytical architecture.

Read first:
- original C1-03A commission and return;
- the exact independent review packet at `6bc1cb8...`;
- `rawlsing_next/pre553_analytical_state_and_route.py`;
- the current producer/adaptive-discovery/structural-admission/consumer owners actually used by the tests;
- `PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/05_C1_EXECUTION_SPEC.md`.

## Mission

Correct exactly the three independently established blockers while preserving the valid executed material underneath them.

### 1. C1-03A-REVIEW-BLOCK-STATE-PROJECTION-001

The envelope currently permits caller-supplied `producer_state` and `retained_state` to disagree without proving the retained state is the lawful projection of the owner-produced object.

Repair law:
- retained state must be derived from, or fail-closed validated against, the actual competent owner object/receipt;
- a caller-provided retained-state label alone must never establish analytical state;
- owner-specific typed constructors/validators are acceptable;
- correct the AT16 54/6 positive witness: the real composition is `SUPPORTED`, not `OBSERVED_ZERO`;
- preserve the distinct mandatory negative states without collapsing them.

### 2. C1-03A-REVIEW-BLOCK-ROUTE-DERIVATION-001

`assert_route_not_laundered()` currently trusts caller-supplied `required_route_class`.

Repair law:
- derive the route obligation from an exact current owner/use contract;
- for the structural-admission example, bind the exact owner-produced admission evaluation/receipt, rule identity, requested admission authority, target-use/use-contract identity, and decision needed to establish the route;
- prove one genuine positive `ADMITTED` learned/adjudicated route;
- prove failed/DENY hostiles against the same route law;
- the same underlying evidence must not become direct merely because the caller changes a label;
- do not impose a learned wrapper on genuinely competent direct empirical output.

Do not invent new semantic/model authority. If no current owner can establish the needed positive route, return the exact authority/owner gap.

### 3. C1-03A-REVIEW-BLOCK-HANDOFF-COVERAGE-001

A selected positive recursive handoff can currently be wrapped with no retained access to its full discovery/adaptive coverage record.

Repair law:
- bind the positive handoff to the exact coverage/frontier record from which it was selected;
- reject absent or mismatched coverage custody;
- add the actual hostile: positive handoff + positive retained state + missing coverage record must fail;
- preserve the valid UNVISITED adaptive-budget witness and its exact unvisited refs.

## Preserve

The independent reviewer accepted as real:
- owner-produced negative-state witnesses;
- real adaptive UNVISITED;
- actual structural-admission owner calls;
- the producer -> accepted C1 composition -> named possibility consumer path;
- the handmade/direct-consumer hostile;
- the 157-test arithmetic/provenance.

Do not weaken these to make the repair easier.

## Write terrain

Modify only:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-REVIEW-REPAIR-R1/**`

Do not modify accepted C1-02 production/tests, AT17/N10E, C1-03R, lifecycle/replay owners, structural-world owners, or V3 terrain.

## Required court

Re-run:
- corrected C1-03A court;
- accepted C1-02 six-file court materially relied upon;
- adaptive discovery courts materially relied upon;
- structural-admission courts materially relied upon.

Record one authoritative final run and exact counts. Do not claim a broader regression sweep than actually executed.

## Return

Write only:
`WORKER_RETURNS/PYAT-C1-03A-REVIEW-REPAIR-R1/**`

Required:
- `00_RETURN.md`
- `01_REVIEW_BLOCKER_DISPOSITION.json`
- `02_STATE_ROUTE_COVERAGE_RECEIPT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `PASS_C1_03A_REVIEW_REPAIR__INDEPENDENT_REREVIEW_REQUIRED`
- `EXISTING_OWNER_OR_AUTHORITY_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No raw source access. No C4. No C1-03 join. No C1-R. No V3 actor/person work. No merge/self-adoption.

Terminal:
`C1_03A_REVIEW_REPAIR_RETURNED__HQ_ADJUDICATION_REQUIRED`
