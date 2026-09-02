# WAVE 1E — M1 RELATION-BASIS COMPATIBILITY FINDINGS R1

## 1. Exact current M1 surface inspected

Current implementation:

`rawlsing_next/m1_temporal_v554_admission_dedup.py`

Exact PRE-MAIN blob:

`e8bd6376720a2de132b384e7771d71d8d39cf261`

Current tests:

`rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`

Exact PRE-MAIN blob:

`e6471ace122466988bb17019f70816a59a04f1f7`

Current contract IDs:

- `M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0`;
- `SCR554_V554_BASIS_DEDUP_AFFORDANCE_EXACT_CONTRACT@1.0.0`.

Current target use is exactly:

`STRUCTURAL_MEDIATION_INPUT`.

Current basis kinds are exactly:

```text
DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION
V553_TEMPORAL_OBJECT
```

Current signatures are exactly:

```text
V554-SIG-001-NONTEMPORAL-EXACT
V554-SIG-002-TEMPORAL-POINT-EXACT
V554-SIG-003-TEMPORAL-RELATIONAL-EXACT
```

The current evaluator chooses the required basis kind from the signature:

- SIG-001 → `DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION`;
- SIG-002/003 → `V553_TEMPORAL_OBJECT`.

That is not a generic structural-basis interface.

## 2. Concrete reason a FIELD FORGE relation cannot reuse the direct basis

The current direct candidate parser requires all of these structural-empirical-admission slots:

```text
structural_empirical_admission_id
structural_empirical_admission_content_hash
admission_authority_id
admission_authority_version
admission_authority_hash
admission_decision_state
focal_structural_proposition_ref
structural_semantic_identity_refs
native_scope_identity_refs
target_use_permission_refs
effective_time_or_interval_refs_required_by_target_use
source_universe_refs
estimand_refs
measure_and_weight_authority_refs
applicable_negative_denial_noncomparability_refs
interpretation_critical_authority_refs
producer_replay_locator_or_reference_root
```

The current equivalence key additionally hard-binds:

`originating_structural_empirical_admission_lineage_fingerprint`.

Therefore relation IDs cannot be inserted into the current direct projection without asserting a false object class and false lineage class.

The WSC001C second-pass correction explicitly forbids this maneuver.

## 3. Concrete reason a FIELD FORGE relation cannot reuse the current V553 basis

The current V553 candidate projection requires:

```text
v553_object_id
v553_object_content_hash
v553_object_family
originating_structural_empirical_admission_refs
focal_structural_proposition_ref
rule_relevant_temporal_semantic_refs
native_scope_identity_refs
source_universe_refs
estimand_refs
measure_and_weight_authority_refs
source_relation_comparability_authority_refs_where_required
applicable_temporal_limit_negative_refs
interpretation_critical_authority_refs
producer_replay_locator_or_reference_root
```

The current V553 route is therefore also structurally anchored to structural-empirical-admission lineage.

A FIELD FORGE relation requiring new temporal meaning needs a relation-aware V553 origin/lineage extension before it can lawfully use the temporal M1 signatures. That is not needed for the first non-temporal relation path and should not be prebuilt merely for completeness.

## 4. Current M1 behavior worth preserving exactly

The current M1 implementation already contains the right behavior for most downstream logic:

### 4.1 Exact signature gating

No basis kind may satisfy a signature it does not own.

Tests already prove, among other things, that a direct basis cannot satisfy a temporal signature and that a no-op V553 duplicate does not add SIG-001 support.

### 4.2 Temporal negative precedence

V553 negative temporal authority cannot be downgraded to a direct positive path.

### 4.3 Typed hard negatives

K05/K06/K07/K08/K09 remain typed and block F1 at their exact meanings.

### 4.4 Deferred context

K01-K03 can remain F2 context without falsely blocking a lawful F1.

### 4.5 Exact dedup

Exact same-kind duplicates with identical equivalence and rule-relevant semantics collapse to one support with provenance aliases.

### 4.6 No winner heuristic

Near-duplicates that differ in source universe produce conflict rather than an arbitrary selected winner.

### 4.7 Equivalence fail-closed

Missing equivalence components return `EQUIVALENCE_UNKNOWN`.

### 4.8 Valid empty

Coherent zero candidate support remains `VALID_EMPTY`; M1 invents no filler basis.

### 4.9 Deterministic output identities

F1/B1/direct-handoff identities are pure hashes of exact canonical semantic material.

These behaviors should be inherited by the relation evaluator rather than redesigned.

## 5. Recommended architecture: second M1 ingress, same downstream V554 object grammar

### 5.1 Preserve the empirical evaluator unchanged

Do not change the meaning of:

`evaluate_m1_temporal_v554_admission_dedup(...)`.

Do not expand `BasisKind.DIRECT` to mean “any admitted structural thing.”

Do not rename the current empirical lineage field in-place and then pretend historical/current empirical hashes are unchanged.

### 5.2 Add relation-specific ingress at the same V554 ownership boundary

The future implementation should add a sibling evaluator surface equivalent to:

```text
evaluate_m1_admitted_relation_v554(...)
```

with contract:

`M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`.

It may live in the same module or a narrowly scoped adjacent module. The semantic requirement is that the current empirical evaluator remains independently addressable and behaviorally unchanged.

The relation evaluator should return the current `M1Evaluation` data type so downstream code does not need a second result grammar.

### 5.3 New relation basis kind

```text
ADMITTED_FIELD_FORGE_RELATION
```

This is not a third generic synonym. It means exactly:

> one actor-independent FIELD FORGE exact relation has passed a separately governed relation→PRE-V3 admission court for the exact declared target use and is eligible to be considered by V554 at the relation-basis signature.

### 5.4 New first relation signature

```text
V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT
```

The signature is necessary because current M1's design correctly makes basis type a governed-use decision rather than an availability contest.

SIG-004 should require only the relation basis kind.

Current direct/V553 candidates may be carried as references for replay/audit if desired, but they do not count as support for SIG-004.

## 6. Relation-basis preparation adapter

The adapter is a compatibility producer, not a semantic authority court.

It consumes the exact independently admitted relation object and either emits one positive `M1AdmittedRelationBasisCandidate@1` or emits one typed nonpositive preparation decision.

It does not decide whether the relation is true, socially meaningful, actor-relevant, temporally meaningful, or publishable.

### 6.1 Positive preparation requirements

Require all:

1. exact relation-admission object identity and hash;
2. exact relation-admission authority identity/version/hash;
3. positive admitted state;
4. exact originating FIELD FORGE relation identity/hash;
5. exact producer ownership refs;
6. exact focal structural proposition for the V554 governed use;
7. exact target-use permission including `STRUCTURAL_MEDIATION_INPUT`;
8. exact relation role/order/cardinality identity where claim-constitutive;
9. exact native scope;
10. exact source universe;
11. exact effective-time/interval requirements for this use;
12. exact estimand/measurement/weight authority where claim-constitutive;
13. exact comparison/transport authority where actually required;
14. exact applicable negatives;
15. exact interpretation-critical authority refs;
16. replay/provenance root;
17. authority snapshots/currentness sufficient to replay;
18. explicit information-loss declaration.

### 6.2 Nonpositive preparation law

Preserve upstream meaning. At minimum:

```text
VALID_EMPTY
DENIED
DEFERRED_MISSING_AUTHORITY
UNRESOLVED
NONCOMPARABLE
TARGET_USE_NOT_PERMITTED
TEMPORALIZATION_REQUIRED
INTEGRITY_FAILURE
```

Only `RELATION_BASIS_READY` may emit a candidate.

Do not pass a nonpositive relation into M1 as `candidates=[]` unless the upstream semantics are truly valid-empty. Otherwise M1's `VALID_EMPTY` would erase the actual blocker.

This point matters: **M1 valid-empty is not a universal wrapper for every upstream nonpositive result.**

## 7. Relation projection

The positive basis projection should carry semantic equivalents of:

```text
relation_admission_ref
relation_admission_authority_ref
relation_admission_decision_state
field_forge_relation_ref
relation_semantic_identity_refs
relation_participant_role_order_cardinality_refs
focal_structural_proposition_ref
native_scope_identity_refs
target_use_permission_refs
effective_time_or_interval_refs_required_by_target_use
source_universe_refs
estimand_refs
measure_and_weight_authority_refs
source_relation_comparability_authority_refs_where_required
applicable_negative_denial_noncomparability_refs
interpretation_critical_authority_refs
producer_replay_locator_or_reference_root
information_loss_declaration
```

Exact field names must be reconciled to the independently constituted W1D output during central fan-in. Semantic correspondence is required; name similarity is not enough.

## 8. Relation equivalence key

Current M1 dedup is not merely object-ID dedup. It deduplicates rule-relevant basis semantics under a complete equivalence key.

The relation path should retain that architecture with a relation-specific key:

```text
focal_structural_proposition_ref
target_use
v554_rule_id
v554_rule_version
v554_rule_hash
basis_semantic_class
rule_relevant_structural_semantic_identity_fingerprint
relation_participant_role_order_cardinality_fingerprint
native_scope_identity_fingerprint
rule_relevant_effective_time_semantics_fingerprint
originating_admitted_relation_lineage_fingerprint
source_universe_fingerprint
estimand_fingerprint
measure_and_weight_authority_fingerprint
rule_relevant_source_relation_comparability_authority_fingerprint
interpretation_critical_semantic_authority_fingerprint
```

### Why basis class must be inside the relation identity

Without it, a relation-derived basis could collide with an empirical-direct basis that happens to name the same focal proposition/scope/source. That would collapse different authority genealogies.

### Why participant role/order/cardinality must be explicit

For a relation, participant structure may be claim-constitutive. Dropping it would let an ordered relation, unordered relation, role-swapped relation, or different-cardinality relation deduplicate accidentally.

## 9. F1 identity and ownership

For relation SIG-004, the canonical basis semantic identity should be hashed from at least:

- relation equivalence key;
- required basis kind `ADMITTED_FIELD_FORGE_RELATION`;
- selected rule-relevant basis semantics.

The resulting V554 F1 may use the existing F1 shape because current F1 already names the V554-owned canonical basis semantic identity, V554 rule/signature/target-use, and authority bundle.

Ownership remains layered:

```text
FIELD FORGE owns relation semantics
relation-admission owner owns relation admissibility for target use
V554 owns F1 applicability/affordance result
V557 owns publication permission
V558 owns immutable resolution
```

No layer reowns the previous one.

## 10. F2 / B1 reuse

Existing F2/B1 semantics are reusable if the exact condition grammar applies to the selected relation use.

- K05 explicit denial remains hard block.
- K06 missing authority remains hard block.
- K07 unknown/conflicting authority remains hard block.
- K08/K09 negative temporal/source authority remain hard blocks.
- K01-K03 remain deferred downstream conditions rather than invented current structure.

B1 may mark V555 structural use allowed only when the relation F1 is genuinely `ELIGIBLE`.

This does not require V555 to exist for GT2. The first relation can still publish directly from V554 to V557 when exact publication authority permits it.

## 11. Temporal path

### 11.1 First-version direct route

The minimum relation extension should support only a relation that is already temporally complete for the exact V554 target use and requires no new V553-owned meaning.

This keeps GT2 from paying a temporal-schema expansion if the selected weakest relation does not need one.

### 11.2 If temporal meaning is required

Fail closed.

Do not:

- reuse current V553 object slots with a fake structural-empirical-admission ancestor;
- manufacture a no-op V553 object;
- reinterpret a FIELD FORGE relation as a current V553 object;
- downgrade missing temporal meaning into a direct relation positive.

The activation condition for relation-aware V553 work is exact and narrow:

> central selects a first relation whose governed V554 use cannot be semantically complete without new V553 temporal observation/relation meaning.

At that point commission the smallest relation-origin V553 intake/lineage extension.

## 12. M4 / V557/V558 compatibility

Current `m4_v557_v558_publication_repository.py` imports:

- `M1Evaluation`;
- `M1_CONTRACT_ID`;
- `SCR554_CONTRACT_ID`.

`structural_objects_from_m1(...)` requires:

```text
isinstance(evaluation, M1Evaluation)
evaluation.contract_id == M1_CONTRACT_ID
```

and then validates the current direct `V554_TO_V557_DIRECT` handoff plus exact F1/F2/B1 hashes.

The relation design can reuse all of the latter validation unchanged.

The future M4 adaptation should therefore be only:

```text
accepted M1 evaluation contract IDs = {
  current empirical M1 contract,
  admitted-relation M1 ingress contract,
}
```

while still requiring exact `M1Evaluation`, exact V554 handoff route, exact object family, exact hash, producer family `V554`, and permission ceilings.

No duck-typing or arbitrary M1-like object acceptance.

## 13. Suggested future hostile tests

The eventual implementation should add, at minimum:

1. exact admitted relation + SIG-004 → exactly one eligible F1;
2. current empirical SIG-001 behavior byte/semantic regression unchanged;
3. relation basis offered to SIG-001 → no positive support;
4. direct empirical basis offered to SIG-004 → no positive support;
5. same relation basis with two provenance aliases → one support + both aliases;
6. role swap / order change / cardinality change → no dedup;
7. source-universe difference → no winner selection;
8. missing relation-lineage fingerprint → `EQUIVALENCE_UNKNOWN`;
9. selected rule-relevant semantic disagreement → `EQUIVALENCE_UNKNOWN`;
10. upstream DENIED does not become M1 `VALID_EMPTY`;
11. upstream NONCOMPARABLE does not become M1 `VALID_EMPTY`;
12. target-use permission absent → no candidate;
13. temporalization required → no SIG-004 positive;
14. no fake V553 object on temporalization blocker;
15. no fake `StructuralEmpiricalAdmission` anywhere in relation path;
16. M4 accepts exact relation M1 contract only after explicit allowlist binding;
17. unknown M1 contract remains rejected by M4;
18. F1/F2/B1 publication hashes remain deterministic;
19. V555 remains absent unless separately required/authorized;
20. zero V556 objects remains lawful;
21. no V3 actor state, PSEPF, claim permission, memory or realization is produced.

## 14. Scope exclusions

This lane does not:

- choose the empirical canary;
- choose the final FIELD FORGE relation family;
- constitute the relation→PRE-V3 admission court;
- define substantive FIELD/CAPITAL/HEGEMONY/HOMOLOGY/PRESSURE/MECHANISM semantics;
- implement relation-aware V553 temporalization;
- build V555/V556;
- select source-backed/persistent/hybrid architecture;
- close OBL001/002/003/004;
- create actor comparator/PSEPF/developmental authority;
- infer actor truth.

## 15. Central fan-in decision rule

If W1A/B/C/D yield a first positive relation that is:

- exact;
- actor-independent;
- positively admitted for the exact V554 target use;
- non-temporal at the required V554 semantic grain;

then central should freeze the relation-specific M1 ingress/signature and issue the narrow implementation/harness wave.

If the selected relation requires new temporal semantics, either choose an equally lawful cheaper non-temporal relation or activate the explicit V553 relation-origin gate. Do not widen current M1/V553 by convenience.

Terminal:

`PASS__WAVE1E_M1_RELATION_BASIS_DESIGN_READY`
