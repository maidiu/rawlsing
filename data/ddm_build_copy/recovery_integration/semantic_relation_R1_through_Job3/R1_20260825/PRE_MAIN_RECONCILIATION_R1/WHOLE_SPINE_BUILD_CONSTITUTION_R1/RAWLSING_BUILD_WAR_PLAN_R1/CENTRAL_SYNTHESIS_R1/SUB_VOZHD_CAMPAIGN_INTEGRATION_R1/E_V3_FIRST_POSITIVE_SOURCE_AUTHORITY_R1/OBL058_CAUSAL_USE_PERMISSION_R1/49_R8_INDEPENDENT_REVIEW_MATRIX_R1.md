# OBL058 — CAUSAL_USE_PERMISSION — R8 FRESH DISTINCT INDEPENDENT REVIEW MATRIX R1

## Freeze status

`INDEPENDENT_MATRIX_FROZEN_BEFORE_GOVERNED_EXECUTION = YES`

Frozen target: `50063aa6667371e3de5a19c775b1b0818b2f734a`

Reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r8-independent-review-r1`

Exact review start: `6214240a643934fa9f5f520587bf1b465da917a2`

Immutable campaign authority: `90adb6897b804ea0b18ea893f509db6051c5bc2d`

This matrix is independently specified from the commissioning command and the prior R7 review finding. Producer tests are prior context only and are not this review matrix.

## Primary review question

Does frozen R8 remove correctness dependence on caller-mutable Python transport construction for broker identity and decision validation, while preserving the independently confirmed R7 lifecycle, requester-generation, scope, source-basis and noncurrent-only controls?

## Matrix families

### A. Transport-construction independence

1. Unregistered-basis `DENY` under `socket.socket` replacement before importing R8.
2. The same control under replacement before issuance.
3. The same control under replacement after issuance but before validation.
4. The same control while repeated validation is occurring.
5. Replacement of `_socket.socket` where reachable from ordinary Python state.
6. Rebinding Python module aliases/import-visible constructor names must not alter accepted broker identity or decision.
7. No ordinary Python callback/cached callable accepted by the public R8 path may provide peer identity or decision in place of the native broker exchange.
8. Caller-supplied peer PID, UID, process-start, authority-instance or decision fields are rejected or ignored as non-authoritative.

### B. Broker identity and response binding

9. Genuine positive and genuine negative controls prove the court is not fail-all.
10. Accepted response must match the exact request identity and authority-instance identity.
11. Replayed, duplicated, reordered or wrong-request responses must not validate.
12. Unrelated endpoint replacement must fail closed.
13. Broker process loss must fail closed.
14. One-shot authority child loss must fail closed.
15. Native broker PID/UID/process-start identity must be source-owned/OS-observed rather than caller supplied.

### C. Native lifecycle and object-generation preservation

16. Ordinary weak-reference/finalizer registries do not control R8 receipt lifetime.
17. Caller reference release plus collection cannot create stale reusable authority.
18. Explicit close revokes validation before lifetime reservation release.
19. Duplicate close does not restore or duplicate authority.
20. Bounded issue/close cycles return native lifecycle accounting to baseline.
21. Later object/address reuse cannot inherit a prior broker record.
22. Native generation state is not assignable through ordinary Python receipt/module attributes.

### D. Requester generation and process isolation

23. Forked genuine `PERMIT` copy rejects.
24. Forked genuine `DENY` copy rejects.
25. Repeated fork-child validation remains rejected while the parent remains valid.
26. Fork-child close cannot retire the parent record.
27. Requester PID/UID/process-start generation is verified from OS-observed connection state.

### E. Receipt identity, reconstruction and module isolation

28. Equal semantic inputs yield distinct authority-instance identities.
29. Cross-receipt body reuse rejects.
30. Cross-scope reuse rejects across all five scope fields.
31. Direct constructor and `object.__new__` forms reject.
32. Subclass, Mapping/proxy, JSON reconstruction, copy/deepcopy and serialization forms reject.
33. Alias/reimport/reload/cross-module receipt use cannot transplant authoritative generation state.
34. Reimport/reload must not reset or duplicate live native generation authority in a way that makes a reconstructed receipt validate.

### F. Semantic preservation

35. Exact registered synthetic basis and exact five-field scope produce `PERMIT`.
36. Unregistered basis produces `DENY`.
37. Registered basis on any changed actor/world/subject/time/transition field produces `DENY`.
38. Field-specific `NONCURRENT_SYNTHETIC` namespace law remains exact.
39. Exact current first-canary and other project-current-shaped identities reject.
40. Classification/routing/occurrence/proximity/narrative-like surrogate basis strings remain `DENY`.
41. Authority/schema/fixture/scope/basis-proof/authority-instance/content-integrity checks remain exact.
42. No public source-basis registration surface exists.

### G. Stability and no-current-effect boundary

43. Repeated same-process validation remains stable.
44. Concurrent same-process validation remains stable without response mixing.
45. No project-current positive causal-use permission is created.
46. No current-positive OBL056 entry, actor/current transition, OBL055 execution, ENCOUNTER, OEE, authority-index effect or OBL061 unblocking is created.

## Disposition law

If any commissioned family reveals a correctness blocker, return the smallest exact blocker and stop without repair. If no blocker remains, return PASS for SUB-VOZHD E consideration only.

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R8_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`
