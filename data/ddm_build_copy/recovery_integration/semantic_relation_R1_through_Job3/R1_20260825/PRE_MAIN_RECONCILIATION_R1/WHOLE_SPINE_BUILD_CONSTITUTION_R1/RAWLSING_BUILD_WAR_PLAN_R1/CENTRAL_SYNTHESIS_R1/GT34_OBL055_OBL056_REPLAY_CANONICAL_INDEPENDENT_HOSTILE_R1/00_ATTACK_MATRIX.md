# GT34 OBL055 H2 — FRESH INDEPENDENT HOSTILE ATTACK MATRIX

## Frozen target

- R3 repair evidence seal: `a18f35b3de4dad6efd1ff3f25d3cd93a2b56c8d4`
- R3 semantic candidate: `702eababa4012512743fd2e729fc9bea167089b1`
- R3 implementation blob: `e8c6edab3b310b797997a3826b8acb32f7f08ce9`
- R3 governed run: `34160840696`
- R3 governed job: `101862191754`
- R3 bounded result: `123 passed`
- R3 court artifact: `10032534409`
- R3 artifact ZIP SHA-256: `019ff94a082bff63555668bf39271b8c6d6f8b24226dae128a3cb752a7dd17a8`

This attack matrix is frozen before hostile-test authoring. The review owns no repair authority and may not modify the target implementation.

## Jurisdiction

`OBL055_ONLY`

`FRESH_INDEPENDENT_HOSTILE_REVIEW_OF_FROZEN_R3`

The review may return PASS, a wholly in-grain OBL055 defect, or the smallest new authority/cross-campaign/trajectory blocker. It may not adopt OBL055 or execute project-current OEE.

## Attack families

### H2-A — canonical receipt wire boundary

1. lawful tuple→JSON-array round-trip must remain accepted;
2. added top-level receipt field must fail;
3. removed receipt field must fail;
4. role mutation must fail;
5. accepted-authority identity/hash mutation must fail;
6. nested scope transition/use mutation must fail;
7. nested subject/object scope mutation must fail;
8. immutable-provenance mutation must fail;
9. negative-limit mutation must fail;
10. receipt-id/hash mutation must fail.

### H2-B — synchronized replay laundering

11. mutate and readdress only the R2 source-bundle receipt while leaving the R1 binding fixed: fail;
12. mutate and readdress only the R1 binding receipt while leaving source bundle fixed: fail;
13. mutate both replay surfaces consistently without a separately valid OBL056 acceptance receipt: fail;
14. inject a caller-defined extra semantic key into both receipt surfaces and readdress: fail;
15. add a second same-role binding/bundle route to create ambiguity: fail.

### H2-C — exact source replay constituents

16. causal semantic pointer swap: fail;
17. causal authentication pointer swap: fail;
18. subject-ingress authentication pointer swap: fail;
19. ADP-008 phase receipt pointer swap: fail;
20. ADP-008 phase authentication pointer swap: fail;
21. positive-applicability authentication pointer swap: fail;
22. contact-occurrence semantic pointer swap: fail;
23. contact-occurrence authentication pointer swap: fail;
24. contact-independence semantic receipt pointer swap: fail;
25. contact-independence authentication pointer swap: fail.

### H2-D — authority-role separation and anti-laundering

26. one contact acceptance receipt reused for both roles: fail;
27. one accepted authority reused for occurrence and independence: fail;
28. caller relabeling/co-location cannot establish occurrence authority;
29. caller relabeling/co-location cannot establish independence authority;
30. currentness relabeling of synthetic acceptance cannot become CURRENT_ACCEPTED.

### H2-E — provenance and replay identity

31. remove R3 successor provenance: fail;
32. remove R2 successor provenance: fail;
33. remove exact HQ OBL056 authority hash provenance: fail;
34. remove exact registry hash provenance: fail;
35. remove exact OBL056 rule hash provenance: fail;
36. readdress candidate/record/event identities after any constituent mutation: still fail unless exact source replay remains valid;
37. source_candidate_id/replay_hash mismatch: fail.

### H2-F — zero-positive and ceiling preservation

38. installed OBL056 registry remains zero-positive;
39. current-positive executor path cannot mint or synthesize a current acceptance;
40. no subject classification truth is minted;
41. no applicability truth is minted;
42. no contact occurrence/independence truth is minted;
43. no exposure/comparator/PSEPF/metabolism/CAN-008/V2 capability appears;
44. W2 lawful transition machinery remains AVAILABLE→OPPORTUNITY→ENCOUNTER only.

## Freshness rule

Hostile test code must be authored only after this matrix commit exists. The court must bind the frozen R3 target and include both fresh H2 attacks and inherited defect-regression suites.

## Hard gates

- `OBL055 = NOT_ADOPTED`
- `POSITIVE_V3_EXECUTION = NOT_AUTHORIZED`
- project-current first-canary OEE = `NOT_AUTHORIZED`
- OBL031 = `BLOCKED_ON_OBL055_HQ_ADOPTION`
- OBL032 = `BLOCKED_ON_OBL031_CENTRAL_CLOSURE`
