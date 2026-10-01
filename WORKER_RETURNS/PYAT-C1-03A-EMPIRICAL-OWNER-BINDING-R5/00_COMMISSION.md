# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03A — EMPIRICAL REFUSAL OWNER-BINDING CORRECTION — R5
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq158-c1-03a-empirical-owner-binding-r5`

Exact base:
`b46fcf2b951d3ecbc7d17be45a36b37ff7c2f494`

Final rereview:
`agent/reviewer-pyat-hq157-c1-03a-r4-final-rereview-r1 @ 599833bb77d29abd21cf08ab0500491bef7ea49c`

Disposition:
`CHANGES_REQUIRED`

Sole blocker:
`C1-03A-R4-FINAL-REVIEW-BLOCK-EMPIRICAL-CAPTURE-OWNER-FAMILY-001`

Do not reopen G5, AT15, AT16, discovery-refusal authenticity, callability, or C1-02.

## Governing law

The accepted C1 execution spec says mandatory negative states need not all occur on the empirical-query path: if a state cannot occur there, identify and exercise the **competent path** where it genuinely occurs.

For the current INTEGRITY_FAILURE fixture, the competent path is the canonical integrity rejection of an exact `RespondentEvent` body with stale sealed identity. It is NOT `execute_empirical_query`.

Therefore:
- do not relabel a canonical constructor refusal as empirical-query refusal;
- the witness must bind the exact governed object family/path that actually refused;
- a broad `CanonicalSemanticObject` `isinstance` gate is forbidden.

## Required correction

Repair only `capture_empirical_integrity_refusal` and its exact supporting fixture/tests.

The strongest narrow shape is preferred:

1. Accept governed repository/release/object identity, not an arbitrary object instance:
   - resolve the exact `C11LogicalRelease` through the current repository path;
   - resolve the exact public object from that release by exact ref;
   - require the resolved object to be exactly `RespondentEvent` at this declared AT14 source-free grain;
   - reject any other canonical family;
   - reject caller-defined `CanonicalSemanticObject` subclasses;
   - reject a ref not present in the declared release.

2. Invoke the real canonical `RespondentEvent` construction/integrity path on the tampered body.

3. The witness owner label must truthfully identify the operation that actually refused. Do NOT use:
   `rawlsing_next.pre553_empirical_query.execute_empirical_query`
   unless that function actually performed the refusal.

   Use a stable exact owner label for the `RespondentEvent` canonical integrity constructor/path, and make the AT14 fixture/receipt state that competent owner truthfully.

4. Bind:
   - exact release ref;
   - exact resolved `RespondentEvent.ref`;
   - exact owner/family identity;
   - the exact attempted body / invocation binding;
   - the object's real authority/dependency/replay closure.

5. If the constructor ACCEPTS the body, no refusal witness exists.

Do not create a generic “any CanonicalSemanticObject integrity” authority. This correction is intentionally bounded to the exact AT14 `RespondentEvent` path already exercised.

## Required hostiles

At minimum prove:

1. genuine governed `RespondentEvent` from exact declared release + tampered stale identity -> witnessed `INTEGRITY_FAILURE`;
2. witness owner label equals the actual canonical RespondentEvent integrity operation, not empirical-query;
3. genuine canonical object from another family is rejected before capture;
4. caller-defined `CanonicalSemanticObject` subclass is rejected;
5. caller-defined subclass of `RespondentEvent` is rejected;
6. genuine `RespondentEvent` not present in the declared release is rejected;
7. caller cannot substitute another release ref;
8. caller cannot substitute another object ref;
9. bare exception still cannot mint;
10. caller cannot inject producer/supporting refs/reason/owner label;
11. owner acceptance produces no witness;
12. discovery refusal path remains unchanged and sound;
13. refusal states remain distinct;
14. G5 remains closed;
15. AT15 genuine ADMITTED route remains green;
16. AT16 54/6 remains SUPPORTED;
17. producer → C1 composition → named consumer remains green.

## Preserve

All independently accepted C1-03A work:
- receipt dominance;
- exact owner gates elsewhere;
- adaptive determinant provenance;
- recursive custody;
- no invented completeness;
- eight-state distinction;
- adaptive UNVISITED;
- final-SHA classmethod cleanup;
- discovery refusal authenticity;
- C1-02 untouched.

## Write terrain

Modify only:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `WORKER_RETURNS/PYAT-C1-03A-EMPIRICAL-OWNER-BINDING-R5/**`

Do not modify C11, empirical-query, empirical-object, discovery, composition, consumer, or authority owner modules.

If exact governed-release membership cannot be established without owner modification, return a typed owner gap with the smallest counterexample. Do not fake provenance.

## Court

Run the same ten-file C1-03A court.

Current final baseline:
`212 passed, 0 failed, 0 errors, 0 skipped`.

Record exact new count and runtime.

## Return

Write:
`WORKER_RETURNS/PYAT-C1-03A-EMPIRICAL-OWNER-BINDING-R5/**`

Required:
- `00_RETURN.md`
- `01_BLOCKER_DISPOSITION.json`
- `02_OWNER_BINDING_RECEIPT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C1_03A_EMPIRICAL_OWNER_BINDING_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `EXISTING_OWNER_OR_AUTHORITY_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption. No C1-03 join.

Terminal:
`C1_03A_EMPIRICAL_OWNER_BINDING_RETURNED__HQ_ADJUDICATION_REQUIRED`
