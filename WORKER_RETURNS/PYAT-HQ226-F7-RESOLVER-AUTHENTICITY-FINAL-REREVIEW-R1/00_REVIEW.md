# PYAT HQ226 — F7 RESOLVER AUTHENTICITY FINAL HOSTILE REREVIEW — R1

**DISPOSITION:** `F7_RESOLVER_AUTHENTICITY_REPAIR_PARTIAL__NAMED_DEFECT`

**COMMISSION:** `2768e28eb12834884e7cd1b8108a5a7d2ef029e5`  
**CANDIDATE RETURN:** `45b721ee13209b9c0d9ecce3023cd1902de21302`  
**CODE-BEARING HEAD:** `cb57b0a9c75ec0a01e78d2142afae757c131e5fb`  
**PRIOR REVIEW:** `1b3648bb8a0ecfaafe05ca5d812236f068499b84`  
**MODE:** independent hostile rereview; no repair; no adoption

## Bottom line

HQ225 closes the **specific outer dispatch defect** identified by HQ224: subclasses and duck objects no longer pass the F7 owner boundary, and an exact concrete resolver's direct `decide` instance shadow is bypassed by the non-virtual call `SourceRelationResolver.decide(resolver, ...)`.

It does **not** yet establish a genuinely non-forgeable boundary to the full adopted source-relation owner path.

Two blocking findings remain.

### F7-RR-04D — exact resolver instance can shadow internal owner dispatch

`SourceRelationResolver.decide(resolver, ...)` is a non-virtual **entry** only. Inside the adopted base method, owner-critical operations are still reached dynamically through the caller-supplied exact instance:

- `self.resolve_exact(relation_ref)`;
- `self._relation_object_key(candidate)`;
- `self._validate_positive(...)`;
- and `_validate_positive` then reads caller-held resolver state, including `self._registry`.

`SourceRelationResolver` has no sealed/immutable instance boundary here. Its `_by_ref`, `_by_key`, and `_registry` are ordinary instance attributes, and its helper methods are ordinary descriptors. Therefore an object can satisfy `type(resolver) is SourceRelationResolver` while carrying caller-side replacements for an internally consulted method. For example, an exact resolver constructed with no registered relation can have `resolve_exact` shadowed after construction to return an otherwise lawful positive relation; the trusted base `decide` then continues through the genuine base validation path and can authorize material absent from the resolver's constructor-validated relation set. More aggressive exact-instance shadows can replace `_relation_object_key` or `_validate_positive` as well.

This is the same threat model HQ225 itself admits by testing `concrete.decide = forged_decide`; the new outer class call blocks only that one method name, not the rest of the owner call graph.

A second provenance weakness reinforces this: the resolver constructor accepts `isinstance(authority_registry, AuthorityRegistry)`, while base validation later calls `self._registry.resolve_exact(...)` virtually. Thus an AuthorityRegistry subclass can remain nested behind an exact resolver. F7's outer A/B cross-bind compares the returned `AuthorityRef` identity to the independently resolved outer snapshot, but it does not prove that the internal owner validation consumed that same snapshot semantics at the full SourceUniverseRelation scope.

### COURT-HQ226-01 — inherited fail-capability witness is stale after the repair

The committed F7 court still contains:

`test_hq219_targeted_break_rr04_owner_decision_is_actually_consulted`

That test monkeypatches `sr.SourceRelationResolver.require`, then asserts that the patch reopens the positive cross-universe path.

HQ225 production no longer calls `require` at this boundary. It calls `SourceRelationResolver.decide(resolver, ...)` directly. Therefore the monkeypatch cannot affect the candidate path, and the witness's asserted reopened authorization is contradicted by the committed implementation. HQ225 added six tests but did not modify/remove this inherited witness; the candidate diff is +206/-0 in the F7 court.

So the candidate's expected `141`-case F7 collection is **not a source-consistent passing court**. I do not invent a runtime failure count, but this named witness is statically stale and must be repaired before a passing court can exist.

## Mandatory attack disposition

- production call-site census: no legitimate production subclass/adapter found; exact top-level type gate does not show authority overreach;
- hostile subclass overriding `require()`: closed by exact-type gate;
- hostile subclass overriding `decide()`: closed by exact-type gate;
- subclass base-then-swapping relation/authority refs: closed by exact-type gate;
- duck object: closed by exact-type gate;
- unmodified concrete resolver with relation absent: source-level refusal path present;
- concrete DENIED / wrong pair / wrong kind / wrong use: inherited source-level refusal paths remain present;
- attacker-controlled subclass descriptor behavior: outer form closed;
- **attacker-controlled exact-instance internal helper dispatch: open / blocking**;
- genuine unmodified concrete positive cross-universe path: source-reachable.

## Runtime truth

No exact repository runtime could be obtained.

- GitHub Actions runs attached to `cb57b0a9c75ec0a01e78d2142afae757c131e5fb`: **0**.
- Reviewer container: Python **3.13.5**, pytest **9.0.2**.
- Repository checkout: unavailable.
- Direct `git ls-remote https://github.com/maidiu/rawlsing.git HEAD`: failed because the container cannot resolve `github.com`.
- Targeted F7/M1 pytest execution: **not obtained**.
- Hostile subclass/exact-instance witnesses executed here: **no**.
- Runtime PASS counts claimed: **none**.

The disposition is not `F7_RESOLVER_FINAL_REREVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE` because the commission expressly permits source-level proof of a defect, and both defects above follow from the committed source without requiring an empirical runtime observation.

## Productive adequacy and ceilings

HQD-216's operative requirement from the commission remains source-level satisfied: the repair is not refuse-all. Same-universe comparison, exact zero, increase, decrease, and the genuine unmodified concrete-owner cross-universe positive path remain represented. The repair changes no authority taxonomy or temporal algebra.

The 12 relation states, 19 authority kinds, exact-zero law, two exact unrestricted tokens, source-scope identity binding, exact measure/use binding, total precedence, 3+ anchor refusal, and the no-F8/ranking/selection/interpolation/trajectory/causation/currentness/pooling/equivalence-creation/actor-power ceilings remain source-level unchanged.

## Required bounded successor

Do not reopen the architecture or create new authority. Bind the **complete** source-relation owner adjudication path, not merely its outer `decide` entry: constructor-validated relation custody, exact authority-registry provenance, relation lookup, key validation, positive validation, and returned decision must not be caller-replaceable after the authenticity boundary. Then repair the stale targeted-break witness to attack the actual `decide` path and add an exact-instance internal-subdispatch/state-poisoning witness. Finally run the targeted F7 court plus the M1 regression court on an exact executable checkout.

`HQ226_F7_RESOLVER_AUTHENTICITY_FINAL_REREVIEW_RETURNED__FULL_OWNER_PATH_AUTHENTICITY_AND_COURT_REPAIR_REQUIRED`
