# OBL058 — CAUSAL_USE_PERMISSION — R11 FRESH DISTINCT INDEPENDENT REVIEW MATRIX R1

## Status

`INDEPENDENT_MATRIX_FROZEN_BEFORE_GOVERNED_EXECUTION`

Repository: `maidiu/rawlsing`

Reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r11-independent-review-r1`

Exact review start: `9087deafcf9fc8adbd8e893ac8f63b20cbf48c71`

Immutable campaign authority: `2be93091bd5b1b6b479bd9c46686d0fc4ce35b81`

Frozen R11 target: `c11d7c15626f0d249a3b44b87d5cb46dcfe7feef`

Mechanism: `OBL058_CAUSAL_USE_PERMISSION_RETAINED_VALIDATION_CAPABILITY_R11@1.0.0`

This matrix is review-only. The frozen candidate is immutable. No repair is authorized.

## Review question

Determine whether the exact validation capability authenticated by R11 is the exact capability retained and later invoked for the lifetime of the accepted path, with no later ordinary Python module/class/instance/descriptor/alias/import/cache/reload/loader selection surface able to substitute a different decision path.

## Independent families

### A. Baseline and exact identity

1. Genuine registered source basis returns `PERMIT`.
2. Genuine unregistered source basis returns `DENY`.
3. Exact authority/schema/mechanism revision remains unchanged.
4. The authenticated `public_validate`, the establishment-returned capability, and the initially exported `validate_receipt` object are identical by object identity.
5. Genuine `PERMIT` and `DENY` validation advance native transport evidence.

### B. Retained-capability boundary

6. Reproduce the R10 module-dictionary/module-attribute divergence before R11 establishment; ordinary module attribute mediation must not redirect establishment or validation.
7. Mediation of the capability module `__dict__` that replaces one component with a Python callable must fail closed.
8. Mixed genuine/substitute capability bundles must fail closed unless every retained component satisfies the exact source-origin/binding contract.
9. Rebinding capability-module exported names after establishment must not redirect a previously retained capability.
10. Replacing `sys.modules` entries and adding aliases after establishment must not redirect a previously retained capability.
11. Loader/spec substitution before establishment must fail closed rather than establish a Python fallback.
12. Receipt-class `_source_validate`, descriptor, `__getattribute__`, subclass, and instance-level substitutions must not redirect a previously retained capability.

### C. Public-path selection after retention

13. Test ordinary rebinding of the candidate module's public `validate_receipt` export after establishment and then resolve the public API again through the candidate module. Record whether the newly resolved public path still invokes the retained authenticated capability or can return a caller-selected decision without native transport evidence.
14. Test candidate-module `__class__` / `__getattribute__` mediation for `validate_receipt` after establishment while leaving the underlying retained capability object and module dictionary entry unchanged. Record whether ordinary public attribute resolution can substitute the decision path.
15. Test a fresh `from candidate import validate_receipt` performed after candidate-module mediation/rebinding. Record whether imported public consumers receive the retained capability or a substituted object.
16. Distinguish saved-capability integrity from public-path integrity: it is not sufficient that a previously saved function object remains correct if the commissioned public lookup surface can later select a different decision object.

Decision criterion for this family: if ordinary public API resolution after establishment can return `PERMIT` for a genuine unregistered-basis receipt without corresponding native transport evidence, the retained-capability invariant is not established for the public accepted path.

### D. Preserved source/core and transport controls

17. R9 fake native-core import-cache objects remain rejected.
18. Ordinary `socket.socket` / `_socket.socket` replacement before and after import/issuance/validation remains irrelevant to the native source exchange.
19. Endpoint replacement, broker loss, and authority-child loss remain fail closed where independently reachable.
20. Caller-supplied peer/decision metadata is not an authoritative input.

### E. Lifecycle and process generation

21. Explicit close revokes validation.
22. Duplicate close cannot restore authority.
23. Live native lifetime reservation and bounded issue/close cleanup remain stable.
24. Forked `PERMIT` and `DENY` copies reject.
25. Child close cannot retire parent authority; parent remains valid after child rejection.
26. Repeated and concurrent same-process validation remains stable.

### F. Origin, reconstruction, scope, and semantic preservation

27. Direct construction, `object.__new__` where reachable, subclass, Mapping/proxy, JSON reconstruction, copy/deepcopy, and serialization remain non-authoritative.
28. Equal semantic inputs retain distinct authority-instance identities.
29. Cross-scope validation rejects all five actor/world/subject/time/transition fields.
30. Registered positive basis is exact across all five fields; nearby scope changes produce `DENY` rather than borrowed positivity.
31. Field-specific `NONCURRENT_SYNTHETIC` boundaries and exact current/project-current-shaped rejection remain intact.
32. Surrogate classification/routing/occurrence/proximity/narrative basis strings remain `DENY`.
33. No public source-basis registration surface appears.
34. No project-current actor, OBL056 positive entry, OBL055 execution, ENCOUNTER, OEE, authority-index effect, or OBL061 unblocking is created.

## Semantic disposition law

Workflow color is evidence-execution status only. If a check intentionally records a reproducible incorrect-positive public-path substitution, a green court confirms the finding and the semantic disposition is `FAIL`.

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R11_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`
