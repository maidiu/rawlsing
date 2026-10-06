# PYAT HQ226 — F7 RESOLVER AUTHENTICITY FINAL HOSTILE REREVIEW — R1

**DISPOSITION:** `F7_RESOLVER_AUTHENTICITY_REPAIR_PARTIAL__NAMED_DEFECT`

**COMMISSION:** `2768e28eb12834884e7cd1b8108a5a7d2ef029e5`  
**CANDIDATE RETURN:** `45b721ee13209b9c0d9ecce3023cd1902de21302`  
**CODE-BEARING HEAD:** `cb57b0a9c75ec0a01e78d2142afae757c131e5fb`  
**PRIOR REVIEW:** `1b3648bb8a0ecfaafe05ca5d812236f068499b84`

HQ225 closes the direct subclass, duck-object, and top-level virtual-dispatch form of HQ224's finding. It does not yet establish a fully authenticated path to the adopted source-relation owner.

The remaining blocker is:

`F7-RR-04D__EXACT_RESOLVER_INSTANCE_CAN_SHADOW_INTERNAL_OWNER_DISPATCH`

HQ225 now requires exact concrete type and invokes `SourceRelationResolver.decide(resolver, ...)` through the adopted class object. That correctly prevents a subclass override of `require` or `decide`, rejects duck-shaped objects, and bypasses a direct instance-side replacement of `decide`.

But the adopted base `decide` method still performs dynamic instance lookup internally:

- `self.resolve_exact(relation_ref)`
- `self._relation_object_key(candidate)`
- `self._validate_positive(...)`

and `_validate_positive` in turn consults instance-resolved owner helpers/state.

Because the exact resolver type is not slot-sealed or otherwise immutable at this boundary, an exact instance can still replace an internally consulted method while continuing to satisfy `type(resolver) is SourceRelationResolver`. The HQ225 exact-instance witness replaces only `decide`; it therefore proves the outer bypass but does not prove the full owner call chain is fixed to adopted implementations.

This is sufficient source-level proof of a remaining local F7 authority-authenticity defect. Runtime would demonstrate the witness, but is not required to establish that Python attribute resolution still permits this path.

The production call-site census did not reveal a legitimate production subclass or adapter that makes exact concrete type an authority overreach. The exact-type part of HQ225 is therefore supportable at current observed production grain.

Mandatory attack status:
- subclass overriding `require`: closed by exact-type gate;
- subclass overriding `decide`: closed by exact-type gate;
- subclass base-then-swap: closed by exact-type gate;
- duck object: closed by exact-type gate;
- unmodified concrete resolver with absent relation: refuses;
- concrete DENIED / wrong pair / wrong kind / wrong use: refusal paths remain present;
- outer subclass descriptor substitution: closed;
- exact-instance internal owner subdispatch: **open / blocking**;
- unmodified concrete positive cross-universe path remains source-reachable.

No exact runtime surface was available in this reviewer environment. The repository is private, no local checkout is present, and GitHub reports no Actions run for the HQ225 candidate. No pytest PASS counts are claimed.

The disposition is not `BLOCKED_BY_MISSING_EXACT_EVIDENCE` because the remaining defect follows directly from the committed method-dispatch chain and from the same exact-instance mutability model HQ225's own court already treats as in scope.

HQD-216 productive adequacy remains source-level intact: same-universe, exact-zero, increase, decrease, and an unmodified concrete-owner cross-universe path remain representable. The 12-state / 19-authority-kind ceilings and the prior source-scope, unrestricted-token, exact-use, exact-measure, total-precedence, and 3+ anchor laws are unchanged.

A bounded successor must bind the entire owner lookup/validation path, not only the outer `decide` call. No architecture reopen or new semantic authority is indicated.

`HQ226_F7_RESOLVER_AUTHENTICITY_FINAL_REREVIEW_RETURNED__INTERNAL_OWNER_DISPATCH_AUTHENTICITY_REPAIR_REQUIRED`
