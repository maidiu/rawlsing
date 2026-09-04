# GT12 R3B — E3-01 ADOPTED PRE-V3→M4 PERMISSION BINDING REPAIR R1

## Terminal

`PASS__GT12_R3B_E3_01_PERMISSION_DESCENT_BOUND_TO_ADOPTED_AUTHORITY`

## Scope / identity

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt12-r3b-e3-01-permission-binding-repair-r1`
- exact working-ancestry start: `00374882168f8ca64606fef3ca84e246f1c573e9`
- immutable instruction evidence: `b95a0adf92bc47234491a20f4526c3108c42ac62`
- instruction path: `R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/05_R3B_EXACT_IMPLEMENTATION_HANDOFF.md`
- Library: `NO`
- local-machine Codex: `NO`
- governed source/respondent acquisition or execution: `NO`
- E2B: `NOT PERFORMED`
- final GT12 hostile audit: `NOT PERFORMED`
- FIELD FORGE reopened: `NO`
- PRE-MAIN / main movement: `NO`

This repair closes E3-01 only.

## Adopted authority bound

The clean-sideline runtime binding freezes and validates the adopted content-addressed authority:

- authority ID: `GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY`
- authority version: `1.0.0`
- authority content hash: `d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`
- adoption receipt ID: `GT12_PERMISSION_TRANSLATION_AUTHORITY_ADOPTION`
- adoption receipt version: `1.0.0`
- adoption receipt content hash: `fe527dd7d6f5163edd5867adf9da2b03ea581c7d78758fe07bf6857c3fd4c46f`
- adoption commit: `00374882168f8ca64606fef3ca84e246f1c573e9`

Exact derived permission law:

`STRUCTURAL_MEDIATION_INPUT -> CONTEXT`

and only:

- V554 producer use: `("CONTEXT",)`
- V557 decision state: `ALLOW_CONTEXT_ONLY`
- V557 allowed use: `("CONTEXT",)`
- V558 requested use: `("CONTEXT",)`

No `REVIEW`, no `ACTIVE_CAUSAL`, no generic downward-closure grant and no generic PRE-V3→M4 translator were created.

## Exact implementation

### `rawlsing_next/gt12_permission_translation_authority.py`

New bounded executable authority binding. It:

1. freezes exact authority ID/version/hash and adoption-receipt ID/version/hash;
2. accepts only actual `Prev3FieldForgeRelationAdmission`;
3. requires `SUPPORTED + ADMITTED`;
4. requires exact singleton upstream target-use permission and relation ceiling `("STRUCTURAL_MEDIATION_INPUT",)`;
5. recomputes the frozen GT2 PRE-V3 rule and requires exact admission authority, rule and current-selection identities;
6. requires exact FIELD FORGE relation family/owner/hash closure;
7. requires exact Afrobarometer R5 source artifact dependency, exact 19,210-member risk set/hash and exact Q86B CONDITIONER → Q86A TARGET participant order;
8. refuses applicable negative/denial/noncomparability refs;
9. derives a content-addressed permission-binding material object whose producer permission is exactly `("CONTEXT",)`;
10. requires the exact downstream `ALLOW_CONTEXT_ONLY / CONTEXT / CONTEXT` use shape.

### `rawlsing_next/gt12_d_to_m4_typed_bridge.py`

The relation-specific M4 helper no longer accepts a `producer_allowed_uses` argument.

Before constructing any V554 `StructuralObject`, it now:

1. verifies the adopted translation authority and adoption receipt;
2. derives the exact permission binding from the frozen positive PRE-V3 admission;
3. rejects any non-exact V557/V558 use shape;
4. requires the M1 F1 lineage to point to the exact admission and exact FIELD FORGE relation used for translation;
5. calls the existing general M4 adapter with the internally derived fixed `("CONTEXT",)` producer ceiling;
6. verifies every resulting relation-path V554 object carries exactly `("CONTEXT",)`;
7. binds both the translation authority and adoption receipt into the producer locator rule bindings;
8. includes the permission-binding hash in build/contract/provenance identity;
9. retains existing CAN-003 V557 narrowing and CAN-004/V558 repository/integrity mechanics unchanged.

The generic/empirical M4 adapter remains unchanged. This repair removes caller-minted permission only from the adopted relation-specific GT2 seam.

## Proof caller-minted relation producer permission is impossible

The public relation helper signature no longer contains:

`producer_allowed_uses`

The only producer permission supplied to `structural_objects_from_accepted_m1(...)` on this path is the module-owned adopted constant:

`ADOPTED_PRODUCER_ALLOWED_USES == ("CONTEXT",)`

A caller can no longer submit `REVIEW`, `ACTIVE_CAUSAL`, a larger set, an empty set, or another producer permission to this relation-path API.

The remaining downstream arguments are also constrained to the adopted exact shape before V554 object construction. Attempts to request `REVIEW`, `ACTIVE_CAUSAL`, `{REVIEW, CONTEXT}`, a different V557 state, or a different V558 requested use fail closed.

## Hostile disposition

The focused R3B tests directly establish the required hostile law:

1. lawful exact positive GT2 lineage derives `("CONTEXT",)` and completes V558 resolution;
2. caller-minted relation `producer_allowed_uses` parameter is absent;
3. `REVIEW` path rejected;
4. `ACTIVE_CAUSAL` path rejected;
5. `{REVIEW, CONTEXT}` widening rejected;
6. V558 `REVIEW` request rejected;
7. V558 `ACTIVE_CAUSAL` request rejected;
8. wrong V557 decision state rejected;
9. wrong translation authority ID rejected;
10. wrong translation authority version rejected;
11. wrong translation authority hash rejected;
12. wrong adoption receipt hash rejected;
13. wrong PRE-V3 admission authority rejected;
14. wrong PRE-V3 admission rule rejected;
15. wrong PRE-V3 current-selection rejected;
16. wrong FIELD FORGE relation owner rejected;
17. wrong relation family rejected;
18. wrong relation/hash closure rejected;
19. changed admission identity cannot reuse a prior M1 lineage;
20. wrong upstream target use / non-singleton permission or ceiling rejected;
21. `OBSERVED_ZERO`, `VALID_EMPTY`, denied, unresolved, missing-authority and noncomparability states cannot translate even with negative refs stripped;
22. wrong source dependency, risk-set identity or participant order cannot reuse authority;
23. empirical-M1/V553 coercion, V555/V556 creation and actor/V3 authority remain absent/rejected.

Inherited CAN-003/CAN-004/M4, typed-negative, PRE-V3, M1 and V3 zero-effect sentinel tests remained green in the same court.

## Regression execution

Execution used an ordinary GitHub-hosted runner through a temporary test-only side branch. The workflow file was not added to this worker branch. The side branch contained exact code candidate:

`d37e2a96cc092608920900e8f309366ebbc7a84c`

plus only the temporary workflow file.

GitHub Actions run:

`33838451514`

Environment:

- Ubuntu 24.04.4 LTS
- CPython 3.11.16
- pytest 9.1.1
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`
- `PYTHONHASHSEED=0`

Exact focused command:

```sh
python -m pytest -q \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py \
  rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py \
  rawlsing_next/tests/test_m4_v557_v558_publication_repository.py \
  rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py \
  rawlsing_next/tests/test_psepf_zero_positive_guard.py \
  rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py \
  rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py \
  rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py
```

Result:

- passed: **171**
- failed: **0**
- skipped: **0**
- pytest exit code: **0**
- elapsed pytest summary: **0.94 s**

The disposable checkout contained only pytest-created untracked `__pycache__/` directories after execution.

An earlier execution exposed nine hostile-test setup errors because deliberately malformed admissions were correctly rejected by the pre-existing D→E gate before reaching the new R3B permission gate. No production defect was found. Those test fixtures were narrowed to pair the tampered admission with an already-valid M1 evaluation so the R3B gate itself was exercised; the corrected court is the 171/171 green run above.

## Changed-file boundary before this return artifact

Comparison from exact start `00374882168f8ca64606fef3ca84e246f1c573e9` to tested code candidate `d37e2a96cc092608920900e8f309366ebbc7a84c`:

- ahead: 4 commits
- behind: 0
- production/test files changed only:
  - `rawlsing_next/gt12_permission_translation_authority.py` — new bounded authority binding;
  - `rawlsing_next/gt12_d_to_m4_typed_bridge.py` — relation-specific permission descent;
  - `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py` — exact hostile/regression coverage.

No FIELD FORGE production file, PRE-V3 admission semantics, generic M4 permission law, V3 positive authority, PRE-MAIN ref or main ref was changed.

## Final disposition

E3-01 is closed at the exact adopted GT2 relation-specific seam:

`PRE-V3 STRUCTURAL_MEDIATION_INPUT`

`-> adopted content-addressed translation authority`

`-> V554 producer permission ("CONTEXT",)`

`-> V557 ALLOW_CONTEXT_ONLY / ("CONTEXT",)`

`-> V558 exact request ("CONTEXT",)`

with no caller-minted producer permission and no actor/V3/V2/strong-noun authority promotion.

`PASS__GT12_R3B_E3_01_PERMISSION_DESCENT_BOUND_TO_ADOPTED_AUTHORITY`
