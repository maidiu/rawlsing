# GT12 R3 — RELATION-SPECIFIC PRE-V3 → M4 PRODUCER-PERMISSION TRANSLATION AUTHORITY CONSTITUTION R1

## Status

`CANDIDATE__NOT_ADOPTED__HOSTILE_REVIEW_REQUIRED`

This document constitutes a **candidate authority object only**. It does not yet authorize production code to consume the mapping.

Machine-readable candidate:

`00_AUTHORITY_CANDIDATE.json`

Authority semantic hash:

`d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`

## Why this authority is required

R2A terminal:

`1e75855a8d9e1a10655068e0984567948075cb75`

found:

`PASS__GT12_R2A_NO_EXISTING_COMPETENT_PERMISSION_TRANSLATION_AUTHORITY_FOUND`

The accepted/current surface contains exact PRE-V3 permission authority and exact M4 monotone-narrowing authority, but no authority translating the upstream frozen token:

`STRUCTURAL_MEDIATION_INPUT`

into the M4 producer-permission vocabulary:

`REVIEW | CONTEXT | ACTIVE_CAUSAL`.

R2B independently disposed the current M4 permission semantics:

`PASS__GT12_R2B_M4_PERMISSION_SEMANTICS_AND_MINIMUM_GT2_USE_DISPOSED`

Its minimum semantic finding is:

`STRUCTURAL_MEDIATION_INPUT` requires actor-independent structural-context use, for which the weakest adequate current M4 atom is:

`CONTEXT`

with exact use-set:

`("CONTEXT",)`

and natural minimum V557 state ceiling:

`ALLOW_CONTEXT_ONLY`.

R2B explicitly did **not** authorize that translation.

R2C terminal:

`32aa4746948696c9a466cb7132ed1917087e446d`

proved the post-R1 fan-in green:

`PASS__GT12_R2C_POST_R1_FANIN_AFFECTED_REGRESSION_GREEN__E3_01_STILL_OPEN`

with `222 passed`, E3-02 closed, and E3-01 still open.

Therefore the remaining Wave-1 authority gap is singular and exact.

## Candidate authority

Authority class:

`RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY`

Authority ID:

`GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY`

Version:

`1.0.0`

Owner:

`VOZHD_GT12_WAVE1_PERMISSION_TRANSLATION_AUTHORITY`

Candidate semantic hash:

`d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`

## Exact mapping candidate

Only:

`STRUCTURAL_MEDIATION_INPUT -> CONTEXT`

Mapping kind:

`EXACT_ONE_TO_ONE_PROVENANCE_RECORDED_NON_WIDENING_COMPATIBILITY_TRANSLATION`

Exact producer ceiling:

`producer_allowed_uses == ("CONTEXT",)`

Exact V557 decision state:

`ALLOW_CONTEXT_ONLY`

Exact V557 allowed use:

`v557_allowed_uses == ("CONTEXT",)`

Exact V558 request:

`requested_resolution_uses == ("CONTEXT",)`

The authority does **not** grant `REVIEW` merely because REVIEW is weaker in the M4 lattice. The candidate is intentionally one-to-one and exact rather than a generic downward-closure license.

The authority does **not** grant `ACTIVE_CAUSAL`.

## Exact bounded jurisdiction

This candidate applies only when all of the following remain exact:

- program: frozen GT1/GT2 Wave-1 canary;
- FIELD FORGE relation family:
  `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`;
- relation owner:
  `FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER`;
- PRE-V3 admission owner:
  `PREV3_FIELD_FORGE_RELATION_ADMISSION_OWNER`;
- PRE-V3 authority identity:
  `GT2_FF_PREV3_RELATION_ADMISSION_AUTHORITY@R1`;
- admission rule:
  `FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0`;
- admission receipt:
  `PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0`;
- operation:
  `ADMIT_EXACT_GT2_FIELD_FORGE_RELATION_FOR_STRUCTURAL_MEDIATION_INPUT`;
- upstream target use:
  `STRUCTURAL_MEDIATION_INPUT`;
- relation-specific M1 contract:
  `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`;
- relation M1 signature:
  `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`;
- producer family: `V554` only;
- source family/wave: Afrobarometer R5;
- exact risk set:
  `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`;
- risk-set member count: `19,210`;
- risk-set semantic SHA-256:
  `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`;
- semantic order:
  `Q86B -> Q86A`;
- relation typed state: `SUPPORTED`;
- admission decision: `ADMITTED`;
- admitted target-use permission exactly:
  `STRUCTURAL_MEDIATION_INPUT`;
- no applicable negative/denial/noncomparability refs.

It is **not** a generic PRE-V3→M4 translator.

It applies to no other relation family, target use, source/risk set, M1 contract, M4 atom, Wave-2 authority, or actor path.

## Downstream authority relation

CAN-003 remains V557 owner of runtime-use governance.

Exact inspected identity:

- Authority ID: `CAN-003`
- contract: `CAN_003_V557_RUNTIME_USE`
- version: `CAN-003.v1`
- owner: `V557`
- repository blob: `28941ef1b978fb2d19e4acc0d6841333e5bcba24`

This candidate supplies the missing **producer-side compatibility translation** that CAN-003 requires to already exist; it does not replace or widen CAN-003.

CAN-003 continues to require monotone downstream narrowing.

CAN-004 remains owner of immutable V557→V558 packaging/repository integrity and does not acquire permission semantics.

## Effect ceiling

The only semantic capability proposed here is:

`ACTOR_INDEPENDENT_STRUCTURAL_CONTEXT_AVAILABILITY_AND_EXACT_V558_RESOLUTION_ONLY`

Explicitly not authorized:

- actor applicability;
- comparator/PSEPF authority;
- positive V3 transition;
- actor-state mutation;
- V2 expression;
- `ACTIVE_CAUSAL` structural use;
- FIELD / mechanism / hegemony promotion.

This mapping terminates at the structural-context boundary.

`V558 STRUCTURAL RESOLUTION != POSITIVE V3 AUTHORITY`

`STRUCTURAL WORLD != PERSON`

## Required implementation shape after adoption

If and only if this candidate is independently reviewed and then adopted by Vozhd, the implementation repair must be the smallest content-addressed binding that:

1. consumes the exact positive PRE-V3 relation admission;
2. verifies the exact upstream authority/rule/current-selection/target-use closure;
3. verifies this translation-authority ID/version/hash;
4. derives `("CONTEXT",)` from the authority rather than accepting arbitrary caller input;
5. binds that derivation into the relation-specific M1 direct handoff / M4 producer object lineage;
6. rejects any caller attempt to supply `REVIEW`, `ACTIVE_CAUSAL`, or any other producer atom;
7. retains CAN-003/CAN-004 downstream narrowing/integrity checks;
8. preserves V554-only producer family and no V553/V555/V556 fabrication;
9. preserves V3 `DENY_ZERO_EFFECT` until separately accepted Wave-2 authority exists.

## Evidence anchors

- post-R1 fan-in: `57a062fb262336764f4db2d7e19819b4a954db14`
- R2 evidence fan-in: `578049c5b180338aa5d513115a62671b2958e3b1`
- R2A: `1e75855a8d9e1a10655068e0984567948075cb75`
- R2B branch remained: `57a062fb262336764f4db2d7e19819b4a954db14`
- R2C: `32aa4746948696c9a466cb7132ed1917087e446d`
- E3: `4f5292ecf3bf04bd5b288452d33002187068912e`
- R1C: `1add8682c5921bb30e9ffe9c0e0b8393a3e7ee9d`
- frozen GT12 contract: `a9416094cbb4653dd2de2e4aa7b67577a355560c`
- Wave-1 enable fan-in: `6a4bf89c5403459d43dcb925c1f98a7b30dd6f49`
- Wave-1 program: `17b9abc5c8c3038d14670c6e68136bb868f5073a`
- FIELD FORGE R2 adoption: `096b419ed8fd3d07c87cb74bcc4890c2f1a8ec54`
- accepted FIELD FORGE synthesis: `e1e41f67ba8f3c17f5cc7bd73b81caf90f0f79f6`

## Adoption rule

This candidate may not be consumed as live authority merely because Vozhd authored it.

Required sequence:

`CANDIDATE CONSTITUTION`
→ `ONE BOUNDED INDEPENDENT HOSTILE AUTHORITY REVIEW`
→ if PASS, `VOZHD ADOPTION`
→ bounded E3-01 implementation repair
→ affected regression
→ E2B
→ one final whole-chain hostile audit
→ GT1/GT2 adoption.

Until the hostile authority review and explicit Vozhd adoption occur:

`STRUCTURAL_MEDIATION_INPUT -> CONTEXT`

remains a **candidate mapping, not executable authority**.
