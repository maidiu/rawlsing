# PYAT HQ225 — F7 SOURCE-RELATION RESOLVER AUTHENTICITY REPAIR — R1 RETURN

**DISPOSITION:** `F7_RESOLVER_AUTHENTICITY_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`  
**BRANCH:** `agent/rabochii-pyat-hq225-f7-resolver-authenticity-repair-r1`  
**COMMISSION:** `cfc023818ccf3a954db0e116a7e045c467375891`  
**STARTUP BASE:** `a190988b58ae1fe5d6a714e0691b19f84eb4e00e`  
**PRIOR REVIEW:** `agent/reviewer-pyat-hq224-f7-final-authority-closure-r1 @ 1b3648bb8a0ecfaafe05ca5d812236f068499b84`  
**CODE-BEARING HEAD BEFORE RETURN PACKET:** `cb57b0a9c75ec0a01e78d2142afae757c131e5fb`

## Exact blocker

`F7-RR-04C__HOSTILE_SOURCE_RELATION_RESOLVER_SUBCLASS_CAN_FORGE_OWNER_DECISION`

Closed locally without source-relation owner mutation or architecture widening.

## Production repair

F7 previously accepted `isinstance(resolver, SourceRelationResolver)` and then dispatched virtually through `resolver.require(...)`. A subclass could therefore pass the type gate and replace the owner's adjudication method with a forged full-shaped AUTHORIZED `RelationDecision`.

The repaired boundary has two parts:

1. **exact concrete owner type:** `type(resolver) is SourceRelationResolver`;
2. **non-virtual adopted-owner adjudication:** F7 invokes `SourceRelationResolver.decide(resolver, ...)` through the adopted class object rather than through caller-controlled instance/subclass attribute lookup.

That combination matters. Exact type alone would still allow an exact instance to shadow `decide` or `require` through its instance dictionary. The non-virtual class call prevents that caller-object substitution.

The resulting `RelationDecision` remains the actual output of the adopted owner implementation. HQ222's exact decision validation and exact relation-authority A/B cross-binding remain intact.

## Production-consumer census

Current production census found no legitimate subclass or adapter owner boundary that F7 must preserve.

- `rawlsing_next/pre553_source_relations.py` owns the concrete `SourceRelationResolver` class, constructor validation, `decide`, `require`, and its typed relation guards.
- Its `execute_i03_composite_query_guarded` surface accepts a `SourceRelationResolver` and forwards it inside the same owner module.
- `rawlsing_next/pre553_temporal_comparability.py` aliases the adopted owner class and consumes the resolver supplied on `TemporalComparisonRequest`; it does not define a second resolver implementation.
- Repository code search found no production `SourceRelationResolver` subclass/factory/adapter outside the adopted owner module. Test code constructs the concrete resolver directly.
- Therefore exact concrete type is the current owner boundary; no legitimate production consumer is displaced.

No change was made to `pre553_source_relations.py`.

## Hostile court

Six HQ225 witnesses were added:

1. full-shaped AUTHORIZED subclass return naming genuine positive B -> refused before override executes;
2. subclass with correct pair/kind/use but no relation in base resolver -> refused before override executes;
3. subclass that would call base and swap relation authority A -> B -> refused before override executes;
4. duck object with owner-shaped API -> refused before any method executes;
5. exact concrete resolver with caller-side instance `decide` shadow -> shadow is bypassed; genuine base owner adjudication remains positive;
6. concrete-owner positive cross-universe control -> remains `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / INCREASE`.

Existing courts remain for:
- concrete DENIED relation;
- concrete wrong universe pair;
- concrete wrong governed use;
- concrete wrong relation kind;
- genuine concrete positive owner.

## Productive adequacy / sustained ceilings

No refuse-everything repair was introduced. Existing same-universe, exact-zero, increase, decrease and 3+ anchor witnesses remain unchanged, and the explicit HQ225 concrete-owner cross-universe control remains in the court source.

The repair adds no authority kind, relation state, reason family, source ontology, F8/ranking/selection/interpolation/trajectory/causation/currentness/pooling/equivalence-creation power, or actor/person capability. The 12-state and 19-authority-kind ceilings are untouched. HQ222 source-scope binding, unrestricted-token law, exact use binding, exact measure binding and A/B cross-binding are untouched.

## Execution truth

This session has GitHub source mutation/read capability but no checkout/runtime capable of executing the repository. No GitHub Actions run is associated with code head `cb57b0a9c75ec0a01e78d2142afae757c131e5fb`. Therefore this packet makes **no fabricated pytest pass claim**.

Static court accounting:
- prior committed F7 collection: 135;
- HQ225 adds 6 scalar test functions;
- expected F7 collection if collection remains otherwise unchanged: 141;
- existing M1 court: 27.

The final independent rereview should execute the F7 and M1 courts and the hostile pre-repair discrimination before HQ adoption.

## Diff / terrain

From commission tip through code-bearing head:
- `rawlsing_next/pre553_temporal_comparability.py`: +18 / -22;
- `rawlsing_next/tests/test_pre553_temporal_comparability.py`: +206 / -0;
- no other production/court files changed.

`F7_RESOLVER_AUTHENTICITY_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`

`HQ225_F7_RESOLVER_AUTHENTICITY_REPAIR_RETURNED__FINAL_REREVIEW_REQUIRED`
