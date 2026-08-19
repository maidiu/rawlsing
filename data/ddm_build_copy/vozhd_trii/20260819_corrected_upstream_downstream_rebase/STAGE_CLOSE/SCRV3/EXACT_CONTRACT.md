# SCRV3 — V3 Empirical Possibility Exact Contract

**Authority:** `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0`  
**Thin boundary:** `V3EmpiricalPossibilityInput@1.0.0`  
**Disposition:** local exact contract closed; only the final `ResolvedStructuralContext` integration signature waits on SCR5578.

## 1. Constitutional boundary

```text
ResolvedStructuralContext
!= V3EmpiricalPossibilityInput
!= generated actor fact/history/state
```

The two upstream objects are peer, noncollapsed priors. Neither owns V3 causal state. Existing V3 semantic authorities remain the only mutation owners.

`PositionedSubjectEmpiricalPossibilityField` (PSEPF) is population-empirical possibility geometry. `V3EmpiricalPossibilityInput` is only a V3-side reference, lifecycle, temporal-admission, read-permission and replay-binding envelope over exact immutable PSEPF objects.

## 2. Exact thin input

The normative machine-readable schema is `EXACT_CONTRACT.json`. The envelope contains only identity, immutable references/hashes, source-typed admission state, effective-time bindings, lifecycle disposition, exact V3 transition/use binding, metabolism-authority identity, intake causal-parent receipt, replay-reference identity and provenance closure.

It MUST NOT copy field geometry. In particular it MUST NOT embed joint masses, response configurations, supports, query ASTs, comparator rule text, source-universe manifests, respondent incidence, uncertainty payloads, or J-way/minority/multimodal geometry. Those remain behind exact producer-owned PSEPF refs/hashes and MUST remain dereferenceable without lossy normalization.

`ResolvedStructuralContext` is explicitly forbidden inside the thin input.

## 3. Objective actor-fact / comparator snapshot seam

The actor snapshot is an immutable ref/hash to already-lawful objective generated facts at an exact effective time. It is not created from survey coordinates. Comparator provenance MUST be transitively reachable by exact ref/hash.

`ActorComparatorReceipt` is provenance-only in V3. It cannot become a prior, candidate, weight, actor fact, causal parent, witness, or mutation authority.

A comparator-relevant actor-fact change invalidates the old empirical conditioning binding and requires upstream requery. V3 may not reinterpret or silently retarget the old field.

## 4. Per-source typed admission

Every source keeps its own `source_key`, authority ref, PSEPF ref/hash where one exists, effective interval, and source state.

The minimum union is:

`PRESENT | ABSENT_IN_CATALOG | DECLARED_NONE | UNSPECIFIED | NO_FIELD | SOURCE_NOT_APPLICABLE | TEMPORAL_NONCOMPARABLE | TARGET_UNAVAILABLE | ZERO_SUPPORT | LOW_SUPPORT | UNCERTAINTY_UNQUANTIFIED`.

These are not interchangeable. A mixed-source field may therefore contain positive and negative source states simultaneously. No majority/modal collapse is allowed. Source disagreement is evidence geometry, not actor state.

## 5. Effective-time alignment

`SCRV3_EFFECTIVE_TIME_ALIGNMENT_V1` binds four clocks/coordinates without inventing a universal time unit:

1. objective actor-fact snapshot effective time;
2. each empirical source's represented/effective interval;
3. V3 decision effective time;
4. owning V3 transition causal time.

No hidden `latest`, interpolation, future-proxy backdating, or timeless-immutable assumption is allowed.

If a required source is temporally noncomparable under its producer/comparator authority, PSEPF contribution is exactly zero for that invocation. The lifecycle disposition must then be upstream requery or unavailable; never guess.

## 6. Lifecycle and ownership

Lifecycle state is `CURRENT | STALE | REFRESH_REQUIRED | INVALIDATED | UNAVAILABLE`. Staleness ownership is `NONE | V3_REBIND | UPSTREAM_REQUERY`.

### V3 rebind

V3 owns only wrapper-local rebinding when the exact PSEPF refs/hashes and comparator snapshot remain valid but a new V3 decision invocation/use-class/causal-parent receipt requires a fresh envelope. Rebind creates a new thin input; it never mutates PSEPF or history.

### Upstream requery

The upstream comparator/query/field chain owns recomputation when comparator-relevant actor facts changed, source applicability/time changed, target/source set changed, producer authority invalidated the field, or exact geometry cannot be dereferenced. V3 cannot repair, normalize, interpolate, or reinterpret an upstream field.

Committed causal history is prospective-only and never rewritten by refresh.

## 7. Intake and replay receipts

`V3EmpiricalPossibilityCausalParentReceipt` binds the exact ordered already-lawful V3 causal parents/ledger anchor to the intake binding. PSEPF refs are prior provenance, not causal parents.

`ReplayReceipt` is audit/replay-only. Its presence cannot grant a missing read permission, replace a missing semantic rule, or mutate actor state.

## 8. Read-permission law

`READ_PERMISSION_MATRIX.csv` is normative.

A PSEPF contribution is permitted only when all of the following are true:

- the thin input validates;
- lifecycle is `CURRENT`;
- effective-time alignment passes;
- metabolism authority ID/version/hash match;
- the matrix grants the transition surface/use class;
- the exact owning V3 rule version explicitly binds that same empirical use class and exact field refs/provenance;
- ordinary causal-parent, target-authority, scheduler and RNG requirements independently pass.

If any condition is absent, **PSEPF transition effect is exactly zero**.

An `ALLOW_IF_RULE_BOUND` row does not itself create a formula. Existing V3 rule registries with no explicit empirical binding remain zero-effect.

## 9. Lawful empirical operation ceiling

Only three operation classes exist:

- `OBSERVE_ONLY`: diagnostic/audit read; zero candidate/state/RNG effect.
- `RULE_DECLARED_EMPIRICAL_CONSTRAINT`: exact deterministic predicate may reject/retain an already-lawful candidate. PSEPF cannot create candidates or witnesses.
- `RULE_DECLARED_EMPIRICAL_WEIGHT`: exact versioned owner formula may transform pinned geometry into exact rational/integer weights over an already-lawful candidate set. ADP-020 alone performs any stochastic draw.

There is no generic `mass -> actor probability` operation. Modal cells, source majorities and disagreement never directly assign actor response, belief, memory, knowledge, identity, relationship, developmental state, or persona.

## 10. Divergence and replay

Identical peer priors do not imply identical lives. Two actors with the same PSEPF and structural prior may diverge because their generated causal histories, encounters, relationships, rule versions, or lawful ADP-020 decisions diverge.

This is compatible with deterministic replay:

```text
same thin-input hash
+ same exact peer structural-context receipt
+ same ordered causal-history/parent ledger
+ same rule/registry hashes
+ same scheduler receipts
+ same ADP-020 RNG receipts
+ same intake/provenance/replay identities
=> same replayed outcome
```

Changing any lawful causal parent or RNG receipt changes replay identity rather than licensing nondeterminism.

## 11. Final seam

SCR5578 has not yet frozen the exact terminal `ResolvedStructuralContext` signature on its designated branch. Therefore SCRV3 does not invent it.

Everything in this contract is closed independently of SCR5578. The only pending item is the final joint V3 integration signature that accepts the already-separate `ResolvedStructuralContext` and `V3EmpiricalPossibilityInput` peer priors without merging them.
