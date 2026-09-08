# OBL058 — CAUSAL_USE_PERMISSION — R9 FRESH DISTINCT INDEPENDENT REVIEW MATRIX R1

## Status

`INDEPENDENT_MATRIX_FROZEN_BEFORE_GOVERNED_EXECUTION`

Target: `9b293aca913cff7f4d52d9e10dc08fcdb99127d9`

Review branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r9-independent-review-r1`

Exact review start: `8abf6a7ecbb72a847c01011f1de253fed0eda558`

Immutable campaign authority consumed prospectively: `b948aed197506905f4b5f1cab20a92e3ce6949b9`

This matrix is review-only. It defines the independent questions and decision criteria before governed review execution. It does not modify the frozen target and does not prescribe or perform a repair.

## Primary question

Determine whether R9 genuinely binds the accepted native core to the repository-owned native mechanism, instead of merely moving trust from the R8 import-cache key to another ordinary Python-controlled import/spec/loader/module/cache/alias/callable surface.

## Independent review families

### A. Pre-existing cache and import-time substitution

1. Preseed `sys.modules['_obl058_r8_native']` with a normal Python module that matches expected names, module name, claimed file/origin and return shapes; candidate import must reject it before issuance.
2. Repeat with Python-defined callables whose types/names are made as similar as ordinary Python permits; source-origin validation must still reject.
3. Preseed before candidate import, then remove/replace before first issue; only a verified genuine native core may become authoritative.
4. Replace the cache entry after genuine candidate import and before first issue; retained genuine binding must remain authoritative.
5. Replace the cache entry after a genuine receipt is issued but before validation/close; live operations must remain tied to the genuine core.

### B. Spec, loader and module metadata

6. Mutate `__file__`, `__spec__`, `__spec__.origin`, `__loader__` and ordinary module attributes on a normal substitute; metadata claims alone must never establish origin.
7. Mutate the same metadata on the genuine module and invoke the R9 verification helper/reload path; inconsistent origin must reject or fail closed.
8. Replace `importlib.util.spec_from_file_location`, `module_from_spec`, or an actually consulted loader path so it yields a Python module; verification must reject before the object is retained as authoritative.
9. Remove the genuine cache entry and reload/reimport the candidate. The path must either re-establish a verified genuine core or fail closed; no ordinary Python substitute may be accepted.
10. Alias the genuine module under extra cache names and alias the candidate module under alternate names; aliasing must not create a second authority or transfer receipt validity across separately loaded candidate surfaces.

### C. Post-verification mutable Python state

11. Replace correctness-relevant module-dict entries after genuine verification (`start_broker`, observation methods, `NativeReceiptBase` attribute) where ordinary assignment is possible. Existing R9 receipt operations must not switch to the replacement; a later verification/reload must reject inconsistent state.
12. Replace cached Python aliases/callables used around native loading after import. Issuance and validation must remain bound to the verified native object rather than dynamically resolving a caller-selected alias.
13. Verify the accepted module entry points are genuine C-extension built-ins bound to the exact module object and the receipt methods are genuine native descriptors, not merely name/shape matches.

### D. Decision correspondence and prior transport boundary

14. Genuine registered synthetic input must produce `PERMIT`; an unregistered synthetic basis must produce `DENY` under every relevant cache/spec/loader substitution attempt.
15. Ordinary `socket.socket` and `_socket.socket` replacement before and after genuine binding must not alter the native broker/source decision path.
16. Broker endpoint replacement, broker loss and authority-child loss must fail closed rather than produce an accepted substituted response.
17. Request/response identity and authority-instance correspondence must remain exact; stale, duplicated or cross-receipt responses must not validate a different receipt.

### E. Lifecycle and requester-generation preservation

18. Explicit close revokes validation before native lifetime reservation release; duplicate close cannot restore authority.
19. Bounded repeated issue/close cycles return lifecycle accounting to baseline and do not leave a correctness-relevant stale identity.
20. Weak-reference/finalizer manipulation remains irrelevant to correctness.
21. Forked copies of genuine `PERMIT` and `DENY` receipts reject; child close cannot retire parent authority; parent remains valid after child rejection.
22. Requester PID/UID/process-start generation remains derived from the source-owned/OS-observed boundary rather than caller-provided fields.

### F. Receipt identity, reconstruction and scope law

23. Equal semantic inputs produce distinct authority-instance identities; cross-receipt body/identity reuse rejects.
24. Constructor, `object.__new__` where reachable, subclass, mapping/proxy, JSON reconstruction, copy/deepcopy and serialization forms reject.
25. Cross-scope validation rejects independently across actor/world/subject/time/transition.
26. Cross-module/candidate-alias receipt reuse rejects.
27. Exact registered source basis remains bound to the exact five-field scope; inference-like or surrogate basis strings remain `DENY`.
28. Field-specific `NONCURRENT_SYNTHETIC` enforcement, exact current-first-canary rejection, project-current-shaped rejection, wrong fixture and empty basis remain exact.

### G. Determinism, concurrency and authority ceiling

29. Repeated and concurrent validation of a live genuine receipt is stable and does not mix responses.
30. No public source-basis registration surface is introduced.
31. No project-current permission, current-positive OBL056 entry, actor/current transition, OBL055 execution, ENCOUNTER, OEE, authority-index effect or OBL061 unblocking is created.

## Decision law

Semantic PASS requires all commissioned review families to hold with genuine positive and genuine negative controls proving the court is not fail-all. Any reproducible ordinary-Python/runtime path that makes an unregistered basis validate `PERMIT`, substitutes a non-genuine native decision source, transfers authority across object/process/module generations, or reopens a preserved boundary is a semantic FAIL. If a blocker is found, return the smallest exact blocker and perform no repair.

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R9_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`
