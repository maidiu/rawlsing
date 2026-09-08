# OBL058 — CAUSAL_USE_PERMISSION — R4 INDEPENDENT REVIEW MATRIX R1

Status: `FROZEN_BEFORE_PRODUCER_TEST_CONSUMPTION`

Reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r4-independent-review-r1`

Exact reviewer start: `a57f2efdc1b3130b62b60381cf0950a3e817230e`

Frozen candidate: `f02509a25b23365596ccedc7c8bc3a973dce3468`

Campaign instruction: `f7618257604c362097edb3c78dae8480a9499c4a`

This matrix was frozen before reading producer-side R4 test implementation. It defines the reviewer-owned failure-mode families to be exercised against the frozen candidate. Review only; no candidate modification.

## A. Source-origin / authority-boundary families

1. Enumerate all reachable module globals, function globals, closures, defaults, keyword defaults, function attributes, code constants, classes, descriptors, process-launch surfaces, subprocess handles, pipes/file descriptors, atexit callbacks, and dynamically generated request callables.
2. Determine whether any reachable callable accepts caller-built receipt body/content and can make that content authoritative.
3. Determine whether any reachable state acts as a mutable authority ledger/registry/cache whose mutation can turn an unissued or DENY receipt into accepted PERMIT.
4. Invoke any recoverable launcher/transport directly with caller-chosen scope, basis, fixture, object identity, body, protocol fields, reordered fields, omitted fields, duplicated fields, and unexpected fields.
5. Attempt duplicate initialization, reinitialization, child reuse, multiple identity/body bindings per authority instance, and validation-to-issuance state reversal.
6. Attempt stale response reuse, duplicate/reordered request messages, cross-receipt response substitution, and cross-process/cross-handle reuse.
7. Attempt caller-created subprocess/transport lookalikes and caller-fabricated success responses where parent-visible plumbing is replaceable.
8. Exercise child EOF, termination, malformed/partial response, unavailable child, stale handle, restart, orphaning, and repeated/concurrent validation. Any failure must fail closed rather than validate an unissued positive receipt.
9. Exercise object-identity reuse pressure and cleanup paths to detect identity/body confusion.

## B. Receipt identity/body families

10. Plain mapping copy, proxy, shallow/deep copy, reconstruction, serialization/deserialization, exact-type ordinary construction, `object.__new__`, subclass, and dynamic-dispatch variants must not become source-issued.
11. Rebind or mutate every parent-visible receipt slot/body/string/scope projection and verify authority does not follow caller-visible mutation.
12. Cross-receipt body substitution: PERMIT body onto DENY identity, DENY body onto PERMIT identity, body swap between two PERMIT identities, and body swap across scope/basis.
13. Cross-scope replay across each of actor/world/subject/time/transition and across all fields simultaneously.
14. Cross-basis and cross-fixture reuse, including registered basis on wrong scope, unregistered basis on registered scope, and project-current-shaped fixture/scope variants.

## C. Semantic preservation families

15. Valid registered `NONCURRENT_SYNTHETIC` PERMIT control remains functional.
16. Valid unregistered-basis `DENY` control remains functional.
17. Exact authority, schema, fixture, scope digest, basis scope digest, basis proof digest, receipt digest/content-integrity mutation fails closed.
18. Wrong decision/basis-kind combinations and DENY/PERMIT contradictions fail closed.
19. Field-specific `NONCURRENT_SYNTHETIC` namespaces are enforced for actor/world/subject/time/transition, including empty suffix and wrong-field namespace.
20. Exact current first-canary subject and project-current-shaped identifiers are rejected.
21. Classification, routing, occurrence/admission, ADP-010, proximity, co-location, and narrative-like surrogate basis strings cannot infer positive permission.
22. No caller-supplied permission boolean, basis kind, arbitrary registration body, or source-basis registration surface can create authority.

## D. Forbidden-effect / jurisdiction families

23. Enumerate candidate exports and reachable callables for any path that creates/activates current actor state, project-current positive causal-use permission, current-positive OBL056 state, OBL055 execution, ENCOUNTER, OEE, authority-index mutation, or OBL061 unblocking; none is permitted.
24. Verify the candidate remains bounded to OBL058 and does not own OBL059/OBL060 semantics.

## PASS / FAIL rule

`PASS` requires all families to preserve source-origin: every accepted positive receipt must be attributable only to the candidate's source-owned semantic issuance decision, without secrecy of inspectable Python runtime state or caller-mutable authority state.

Any reproducible caller-controlled path that makes a receipt not produced by that semantic decision validate as `PERMIT` is blocking and yields review `FAIL`, regardless of whether the governed test process itself exits green.

`REPAIR_PERFORMED_BY_REVIEWER = NO`
`PROJECT_CURRENT_EFFECT_CREATED = NO`
