# HANDOFF — GT12 R3B E3-01 ADOPTED PERMISSION-DESCENT IMPLEMENTATION REPAIR R1

**BECOME RABOCHII — GT12 R3B E3-01 ADOPTED PRE-V3→M4 PERMISSION BINDING REPAIR R1**

Repository:

`maidiu/rawlsing`

Work on the already-created branch:

`agent/rabochii-gt12-r3b-e3-01-permission-binding-repair-r1`

Exact working-ancestry starting HEAD:

`00374882168f8ca64606fef3ca84e246f1c573e9`

The commit containing this handoff is **instruction evidence only**. Do not make it working ancestry.

## Resource law

**NO LIBRARY.**

Do not acquire or execute governed source/respondent data.

Do not use local-machine Codex unless the bounded repository implementation is otherwise impossible.

## Exact defect to close

E3-01 showed that the relation-specific M1→M4 path accepts fresh caller-supplied:

`producer_allowed_uses`

and can therefore let a caller mint the V554 producer permission ceiling before ordinary V557/V558 subset checks.

That defect is now authority-resolved.

## Exact current adopted authority

Vozhd adoption:

`00374882168f8ca64606fef3ca84e246f1c573e9`

Adoption receipt:

`R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/03_VOZHD_ADOPTION.json`

Adoption disposition:

`R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/04_ADOPTION.md`

Adopted authority:

- id: `GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY`
- version: `1.0.0`
- authority semantic hash:
  `d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`
- adoption receipt semantic hash:
  `fe527dd7d6f5163edd5867adf9da2b03ea581c7d78758fe07bf6857c3fd4c46f`

R3A hostile review:

- terminal SHA:
  `273d5a6f010bb813b64ea0b29ca78624fe8b4422`
- terminal:
  `PASS__GT12_R3A_PERMISSION_TRANSLATION_AUTHORITY_CANDIDATE_LAWFUL_FOR_ADOPTION`

## Exact adopted mapping

For this frozen GT12 relation path only:

`STRUCTURAL_MEDIATION_INPUT -> CONTEXT`

Exact downstream shape:

- producer allowed uses = `("CONTEXT",)`
- V557 decision state = `ALLOW_CONTEXT_ONLY`
- V557 allowed uses = `("CONTEXT",)`
- V558 requested resolution uses = `("CONTEXT",)`

No generic downward closure exists.

The authority does **not** grant `REVIEW`.

The authority does **not** grant `ACTIVE_CAUSAL`.

## Exact positive preconditions

The translation is lawful only when the input is the exact frozen GT2 positive relation-admission lineage and all of the following hold:

- relation family:
  `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`
- relation owner:
  `FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER`
- relation typed state exactly:
  `SUPPORTED`
- admission decision exactly:
  `ADMITTED`
- target use exactly:
  `STRUCTURAL_MEDIATION_INPUT`
- target-use permissions exactly:
  `("STRUCTURAL_MEDIATION_INPUT",)`
- relation permission ceiling remains non-widened;
- no applicable negative/denial/noncomparability refs;
- PRE-V3 admission authority/rule/current-selection are exact and content-addressed;
- downstream contract exactly:
  `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`
- producer family remains V554;
- source is Afrobarometer R5;
- risk set:
  `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- risk-set semantic SHA-256:
  `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- semantic order remains Q86B CONDITIONER -> Q86A TARGET.

## Required implementation

Close only E3-01.

Implement the smallest clean-sideline binding necessary so that the relation-specific path derives its producer permission from the exact adopted authority rather than a fresh caller choice.

The implementation must make the following law executable:

`VERIFIED_FROZEN_GT2_POSITIVE_ADMISSION`
+
`EXACT_ADOPTED_TRANSLATION_AUTHORITY`
+
`EXACT_ADOPTION_RECEIPT`
→
`RELATION_V554_PRODUCER_ALLOWED_USES = ("CONTEXT",)`

A caller must not be able to select or widen the relation-specific producer permission.

It is acceptable for general/empirical M4 adapters to retain their own existing permission input where that is outside this relation-specific authority. Do not redesign unrelated M4 producers.

Preserve the clean-sideline law: production runtime must not depend on mutable stage-close prose or fuzzy repository lookup. If authority material is represented in code, its exact id/version/hash/adoption identity must be frozen and replayable.

The relation-specific direct handoff must retain enough exact identity/provenance to prove the permission derivation.

## Required current surfaces to inspect

At minimum:

- `rawlsing_next/wave1_ff_prev3_relation_admission.py`
- `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py`
- `rawlsing_next/gt12_d_to_m4_typed_bridge.py`
- `rawlsing_next/m4_m1_evaluation_binding.py`
- `rawlsing_next/m4_v557_v558_publication_repository.py`
- `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py`
- `rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py`
- `rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`
- relevant PRE-V3 typed-negative tests;
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py`.

## Mandatory hostile cases

At minimum prove:

1. exact lawful frozen GT2 positive admission derives exactly `("CONTEXT",)`;
2. relation path cannot request or inject `REVIEW`;
3. relation path cannot request or inject `ACTIVE_CAUSAL`;
4. relation path cannot request or inject `("REVIEW","CONTEXT")` or any larger set;
5. missing/wrong authority id fails before V554 object construction;
6. wrong authority version fails before V554;
7. wrong authority semantic hash fails before V554;
8. missing/wrong adoption receipt identity/hash fails before V554;
9. wrong PRE-V3 admission ref/hash fails;
10. wrong admission authority/rule/current-selection fails;
11. wrong relation ref/hash/family/owner fails;
12. wrong target use or non-singleton upstream permission fails;
13. `OBSERVED_ZERO`, `VALID_EMPTY`, denied, unresolved, missing-authority or noncomparable input cannot translate;
14. stripping negative refs cannot rescue a nonpositive typed state;
15. wrong source/risk-set/order cannot reuse the authority;
16. empirical-direct/I04/V553 substitution remains rejected;
17. no V555/V556 fabrication;
18. V557 decision state other than exact `ALLOW_CONTEXT_ONLY` is rejected on this adopted path;
19. V557 allowed use other than exact `("CONTEXT",)` is rejected;
20. V558 requested use other than exact `("CONTEXT",)` is rejected;
21. CAN-003/CAN-004 monotone narrowing/integrity remains intact;
22. no comparator/PSEPF, actor/V3 positive authority, actor mutation or V2 expression is created;
23. later V3 zero-positive guard remains inert and authoritative.

## Existing test semantics that must change

The old GT12 positive mechanics fixture manually used:

`producer_allowed_uses=("REVIEW",)`

with `ALLOW_REVIEW_ONLY` and V558 `REVIEW`.

That fixture is not current semantic authority after adoption.

Update the relation-specific positive test to exercise the adopted exact `CONTEXT` path while retaining a hostile proof that caller-minted `REVIEW` cannot substitute for it.

Do not alter unrelated generic M4 semantics.

## Regression

Run the smallest directly affected no-Library suite including at least:

- relation admission / C→D tests;
- relation M1 ingress tests;
- D→M4 typed bridge tests;
- M4 V557/V558 tests;
- R1B typed-negative sentinels;
- PSEPF zero-positive guard;
- relevant GT0 actual-guard sentinel;
- current GT1/GT2 integration test.

If a bounded regression exposes a direct inherited coupling, include only the smallest relevant inherited subset.

## Explicit prohibitions

Do not:

- reopen FIELD FORGE;
- alter GT2 empirical result semantics;
- alter R1C current query/fact/replay identities;
- mint another translation authority;
- broaden the adopted authority;
- infer `REVIEW` from `ALLOW_CONTEXT_ONLY`;
- infer `ACTIVE_CAUSAL`;
- route through I04;
- fabricate V553/V555/V556;
- create comparator/PSEPF authority;
- create positive V3 or actor-state authority;
- perform E2B;
- perform the final GT12 hostile audit;
- adopt GT1/GT2;
- move PRE-MAIN or `main`.

## Required return

Report:

- exact files changed;
- exact authority-binding representation;
- exact derivation path to `("CONTEXT",)`;
- proof caller-minted relation producer permission is impossible;
- exact hostile cases/results;
- exact tests/counts;
- exact terminal SHA.

Terminal only if E3-01 is actually closed:

`PASS__GT12_R3B_E3_01_PERMISSION_DESCENT_BOUND_TO_ADOPTED_AUTHORITY`

Otherwise return the smallest exact blocker.
