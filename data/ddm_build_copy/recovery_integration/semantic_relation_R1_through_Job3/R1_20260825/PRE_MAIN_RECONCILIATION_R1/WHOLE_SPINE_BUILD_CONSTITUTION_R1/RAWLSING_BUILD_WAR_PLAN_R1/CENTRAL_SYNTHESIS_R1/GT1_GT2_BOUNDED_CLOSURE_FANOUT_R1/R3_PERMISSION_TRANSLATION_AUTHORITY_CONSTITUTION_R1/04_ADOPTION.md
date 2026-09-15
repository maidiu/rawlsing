# GT12 R3 — VOZHD ADOPTION OF RELATION-SPECIFIC PRE-V3→M4 PERMISSION TRANSLATION AUTHORITY R1

## Disposition

`ADOPTED__GT12_RELATION_SPECIFIC_PREV3_TO_M4_PERMISSION_TRANSLATION_AUTHORITY__CURRENT_FOR_FROZEN_WAVE1_ONLY`

Vozhd adopts the exact authority candidate reviewed by R3A without semantic modification.

## Exact adopted authority

- authority id: `GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY`
- version: `1.0.0`
- authority semantic hash: `d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`
- candidate tip: `a7a74319cf38bd22b57e7da6d016b36711a2b654`
- R3A hostile-review terminal: `273d5a6f010bb813b64ea0b29ca78624fe8b4422`
- R3A disposition: `PASS__GT12_R3A_PERMISSION_TRANSLATION_AUTHORITY_CANDIDATE_LAWFUL_FOR_ADOPTION`
- adoption receipt: `03_VOZHD_ADOPTION.json`
- adoption receipt semantic hash: `fe527dd7d6f5163edd5867adf9da2b03ea581c7d78758fe07bf6857c3fd4c46f`
- adoption commit: `5ce90e304a25359672591ed2b4a2dd605e3175c0`

## Exact adopted mapping

`STRUCTURAL_MEDIATION_INPUT -> CONTEXT`

and only:

- producer allowed uses: `("CONTEXT",)`
- V557 decision state: `ALLOW_CONTEXT_ONLY`
- V557 allowed uses: `("CONTEXT",)`
- V558 requested resolution uses: `("CONTEXT",)`

This adoption does not infer `REVIEW`, `ACTIVE_CAUSAL`, a larger permission set, or generic downward closure.

## Exact jurisdiction

The adoption is current only for the frozen GT1/GT2 Wave-1 canary:

- relation family: `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`
- source: Afrobarometer R5
- risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- risk-set semantic SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- semantic order: Q86B CONDITIONER -> Q86A TARGET
- PRE-V3 target use: `STRUCTURAL_MEDIATION_INPUT`
- relation M1 contract: `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`
- producer family: V554

Positive application requires exact `SUPPORTED` + exact `ADMITTED` + exact singleton upstream target-use permission + no applicable negative/denial/noncomparability refs.

## Effect ceiling

The adopted effect is exactly:

`ACTOR_INDEPENDENT_STRUCTURAL_CONTEXT_AVAILABILITY_AND_EXACT_V558_RESOLUTION_ONLY`

It does not authorize comparator/PSEPF, actor applicability, positive V3 transition, actor mutation, V2 expression, ACTIVE_CAUSAL use, FIELD/mechanism/hegemony promotion, or any Wave-2 authority.

## Implementation consequence

For the relation-specific path, caller-minted `producer_allowed_uses` is now forbidden as an authority source.

A lawful E3-01 repair must:

1. bind the exact adopted authority id/version/hash and this adoption receipt;
2. prove the exact positive frozen PRE-V3 admission lineage;
3. derive `("CONTEXT",)` from the adopted authority;
4. fail closed on missing/wrong/tampered authority, scope, admission, typed state, target use, or negative refs;
5. require exact `ALLOW_CONTEXT_ONLY`, exact V557 `("CONTEXT",)`, and exact V558 `("CONTEXT",)`;
6. preserve CAN-003/CAN-004 monotone narrowing and packaging law;
7. retain V554-only producer-family routing;
8. create no V553/V555/V556, actor/V3, or V2 authority.

## Non-movement

This adoption does not move `integration/pre-main-reconciliation-r1` or `main`.

It is a GT12 Wave-1 central authority adoption only.
