# PYAT HQ227 — F7 FULL OWNER-PATH AUTHENTICITY REPAIR — R1 RETURN

**DISPOSITION:** `F7_FULL_OWNER_PATH_AUTHENTICITY_COMPLETE__READY_FOR_FINAL_REREVIEW`  
**BRANCH:** `agent/rabochii-pyat-hq227-f7-full-owner-path-authenticity-r1`  
**COMMISSION TIP:** `c609dbfe4c60bbc4fb8886692343bab3878805f3`  
**STARTUP BASE:** `45b721ee13209b9c0d9ecce3023cd1902de21302`  
**PRIOR REVIEW:** `2b8946bfef1506bae34b46a55833bad83bfb9d16`  
**CODE-BEARING HEAD:** `506291b6e08f4e94791c4fb1cf7020691466e167`

## Blockers closed in implementation

- `F7-RR-04D__EXACT_RESOLVER_INSTANCE_CAN_SHADOW_INTERNAL_OWNER_DISPATCH`
- `F7-RR-04E__NESTED_AUTHORITY_REGISTRY_PROVENANCE_NOT_EXACT`
- `COURT-HQ226-01__STALE_REQUIRE_TARGETED_BREAK_AFTER_DECIDE_SWITCH`

HQ225's exact outer type plus non-virtual outer `decide` call was insufficient because the concrete resolver still adjudicated through caller-replaceable state and nested registry dispatch. HQ227 moves the adopted positive path onto construction-time owner custody.

## Production repair

`pre553_source_relations.py` now exposes `authenticated_source_relation_decision`. Construction authenticates and pins:

- exact concrete `AuthorityRegistry`;
- exact `SourceUniverseRelation` objects;
- relation semantic hashes and replay identities;
- the exact nested `AuthoritySnapshot` objects reached by the relation authority refs;
- canonical semantic hashes of those snapshots;
- a deterministic owner-custody hash.

That state is held in a closure-owned `WeakKeyDictionary`, not in the caller-replaceable `resolver._by_ref`, `resolver._by_key`, or `resolver._registry` attributes. Positive adjudication re-authenticates the custodied relation semantic hash/replay identity and the custodied authority snapshot semantic hash before applying the already-adopted P07 authority checks.

The authenticated entrypoint captures its owner-state loader, decider, returned-decision validator, and nested validation/resolution function objects. F7 captures that entrypoint once. Caller monkeypatches to `decide`, `require`, `resolve_exact`, `_validate_positive`, nested relation validation helpers, or `resolver._registry.resolve_exact` therefore cannot redirect the F7 owner path.

`RelationDecision` now carries `owner_custody_hash` and `authority_snapshot_content_hash`, and its replay identity binds those values. F7 validates the returned decision and cross-binds both the relation-authorizing `AuthorityRef` and the exact nested authority snapshot semantic hash against its independently resolved outer SOURCE_EQUIVALENCE authority closure.

No P07 relation semantics were duplicated into F7. No relation kind, authority kind, operation, relation state, or F8/ranking/pooling/causal/actor capability was added.

## Hostile court

The stale `require` targeted break was replaced with a break against F7's actual captured authenticated owner entrypoint.

HQ227 adds attacks for:

1. post-construction relation-map injection into an exact resolver;
2. post-construction registry replacement;
3. hostile `AuthorityRegistry` subclass overriding `resolve_exact`;
4. stale/corrupt relation replay identity;
5. wrong positive `AuthoritySnapshot` semantics under the same outer `AuthorityRef`;
6. monkeypatches of `decide`, `require`, `resolve_exact`, and nested validation seams;
7. post-construction nested registry instance dispatch shadow;
8. returned-decision custody/snapshot/replay provenance;
9. lawful cross-universe productivity.

The pre-HQ227 implementation would accept the relation-map injection path because exact relation lookup read the caller-owned `_by_ref` map; the repaired path reads sealed construction custody instead.

## Productive adequacy and sustained law

The lawful cross-universe path remains source-reachable and has an explicit positive control requiring `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED / COMPARABLE / INCREASE`. Existing same-universe, exact-zero, increase, decrease, 3+ anchor refusal, exact-use, exact-measure, temporal identity, total-precedence, two-token unrestricted law, 12-state ceiling, and 19-authority-kind ceiling are not intentionally widened.

One conservative incidental hardening remains in `SourceRelationResolver.from_c11`: exact resolver/repository/object family checks were tightened while establishing owner provenance. It is not relied on by the F7 repair and should be inspected in rereview for compatibility; no known F7 semantic requirement depends on it.

## Execution truth

No lawful repository runtime was available in this session. The GitHub connector could read/write the private repository, but the isolated shell could not fetch/authenticate the checkout, no workflow-dispatch action was available, and no Actions run exists for the code-bearing head. Therefore this return makes **no pytest pass claim**.

Static accounting:
- HQ225 expected F7 collection: 141;
- HQ227 replaces one stale scalar witness and adds nine additional scalar witnesses: expected F7 collection 150 if prior collection otherwise remains unchanged;
- inherited source-relation/M1 court expectation from HQ225: 27;
- expected targeted aggregate: 177.

Final hostile rereview must execute the exact F7/source-relation courts and independently test the pre-repair discriminators.

`F7_FULL_OWNER_PATH_AUTHENTICITY_COMPLETE__READY_FOR_FINAL_REREVIEW`

`HQ227_F7_FULL_OWNER_PATH_AUTHENTICITY_RETURNED__FINAL_REREVIEW_REQUIRED`
