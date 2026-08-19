# SV3C — EFFECTIVE-TIME / SOURCE-STATE / NEGATIVE-ADMISSION FEEDER

**Repository:** `maidiu/rawlsing`  
**Exact semantic base:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Branch:** `agent/vozhd-trii-dr-r03-spec-v3-effective-time-source-state`  
**Authority:** `NON_DISPOSITIVE_TO_SCRV3`  
**Production code modified:** `NO`  
**Broad topology amended:** `NO`

## Result

`SV3C_FEEDER_COMPLETE`

SV3C finds no broad-topology contradiction and no authority conflict that prevents a bounded hostile candidate for V3-side effective-time alignment and per-source typed negative admission.

The central finding is that the V3 intake boundary must preserve four distinct clocks and must not use any convenience rule to collapse them:

```text
actor-fact snapshot time
!= PSEPF source/historical time
!= V3 decision/effective time
!= ADP-021 scheduler time
```

A field may be immutable, source-supported and currently present yet still be unlawful for a particular historical or developmental decision. Conversely, a field may remain empirically valid while only its V3 decision/use binding has become stale. Therefore:

```text
UPSTREAM_REQUERY_REQUIRED != STALE_OR_REBIND_REQUIRED
```

The first belongs to the comparator/source/query/field side of the seam; the second is V3 intake applicability over an exact immutable field.

## Binding authority consumed

SV3C read and treated as binding or accepted evidence:

- parent adjudications 24 and 25;
- accepted R03 `FINAL_BROAD_DAG`, `STAGE_CLOSE_READ_CAMPAIGN`, and `WHOLE_MACHINE_CLOSURE_GATE`;
- EPV3 at exact head `c97df88b9461a5ae0d01bc66b2d0f67f1f9337ae`;
- accepted R03D, R03E and R03F hostile returns;
- D15 `REVERSE_POSITIONED_SUBJECT_ARCHITECTURE.md`, including source-indexed PSEPF, typed comparator/source states, exact historical scope and `composition: NONE_BY_DEFAULT`;
- accepted V3 completion law, including stage-blind V3 causal ownership, replay, historical nonretroactivity and scheduler separation;
- accepted ADP-021 `V3_HYBRID_CAUSAL_SCHEDULER_POLICY`, including monotone causal-time coordination and explicit scheduler nonownership of semantic event content;
- accepted non-dispositive SV3M evidence at exact head `0ce8eb656fec6a3ac0d2a36a12c9ba217603e7cb`, including metabolism read-permission ceilings and `NO_PSEPF_TRANSITION_EFFECT` when authority/read permission is absent.

No current implementation shape was elevated above these authorities.

## 1. Time-domain noncollapse

SV3C recommends that SCRV3 freeze explicit clock-role identity in every intake/replay contract.

### Actor-fact snapshot time

The comparator-facing objective actor facts are bound to an exact snapshot/currentness state. If a later generated actor fact materially changes the comparator predicate for the requested empirical field, changing only a V3 timestamp is insufficient. A new upstream comparator/query/PSEPF request is required.

### PSEPF source/historical time

Every source component retains the historical/source scope under which it was produced. V3 may inspect that scope but may not rewrite it, nearest-match it, or promote a newer field into an older decision.

### V3 decision/effective time

This is the V3-side question: may this exact immutable field be consulted for this exact actor, transition owner, use class and decision context now/at the replayed decision time?

This is an admission/applicability decision, not field recomputation.

### Scheduler time

ADP-021 may coordinate when the intake/transition is invoked. It cannot choose the empirical field, set source historical scope, or silently equate current scheduler time with field validity.

## 2. Candidate routing theorem

The candidate admission order is fail-closed:

1. exact immutable identity/integrity;
2. preserve comparator-owned failures;
3. determine whether upstream empirical requery is required;
4. otherwise determine whether V3 rebind is required;
5. prove exact use-specific source/time alignment;
6. preserve per-source support/target/conflict/noncomparability states;
7. require exact metabolism authority and owner read permission;
8. only then admit the exact requested read operation.

Unknown alignment never selects a nearest or latest field.

## 3. Required typed states

SV3C explicitly types at least the commanded states:

- `NO_COMPARATOR`
- `AMBIGUOUS_COMPARATOR`
- `ZERO_SUPPORT`
- `LOW_SUPPORT`
- `SOURCE_COMPONENT_NONCOMPARABLE`
- `SOURCE_CONFLICT`
- `TARGET_UNAVAILABLE`
- `STALE_OR_REBIND_REQUIRED`
- `UPSTREAM_REQUERY_REQUIRED`
- `MISSING_METABOLISM_AUTHORITY`
- `INTEGRITY_FAILURE`

The feeder also preserves/adds candidate intake/action states where needed, including:

- `READ_ADMITTED`
- `READ_NOT_REQUESTED`
- `OWNER_READ_PERMISSION_MISSING`
- `SOURCE_NOT_APPLICABLE`
- `OBSERVED_ZERO`
- `EFFECTIVE_TIME_NONCOMPARABLE`

These additions do not claim a final parent vocabulary. They make hostile distinctions explicit so the parent cannot close them accidentally.

## 4. Negative-state ownership

The canonical rule is:

```text
V3 may preserve/expose an upstream negative
without becoming the semantic owner of that negative.
```

Comparator-owned:
- `NO_COMPARATOR`
- `AMBIGUOUS_COMPARATOR`
- equivalent objective-fact/comparator temporal failure.

Field/source-owned:
- `TARGET_UNAVAILABLE`
- `ZERO_SUPPORT`
- `LOW_SUPPORT`
- `OBSERVED_ZERO`
- source applicability/noncomparability/conflict states.

V3-intake-owned:
- decision/use binding stale or rebind required;
- decision-time alignment unavailable/noncomparable;
- input/use denied;
- metabolism authority/read permission missing;
- intake integrity failure where the V3 binding itself cannot close.

## 5. Action precedence does not erase semantics

The supplied `NEGATIVE_PRECEDENCE_MATRIX.csv` orders **actions**, not truth.

For example, `INTEGRITY_FAILURE` may force the entire intake to reject before a transition can read anything. That does not authorize deletion of an already-known `LOW_SUPPORT`, `TARGET_UNAVAILABLE`, or source-conflict state from the audit/replay state vector.

Likewise, `MISSING_METABOLISM_AUTHORITY` yields zero transition effect even when the field is otherwise perfectly aligned. It does not rewrite the field as unavailable or zero support.

## 6. Requery versus rebind

### Upstream requery

Required when a new empirical question must be asked, including material changes to:

- objective actor-fact snapshot used for comparator resolution;
- comparator mapping/authority;
- source applicability;
- query/target/risk-set identity;
- required source/historical scope.

Result: `UPSTREAM_REQUERY_REQUIRED`.

### V3 rebind

Required when the same immutable PSEPF remains empirically valid but V3-specific decision/use/metabolism applicability changed.

Result: `STALE_OR_REBIND_REQUIRED`.

Neither condition permits mutation of the immutable historical PSEPF.

## 7. Hostile attack dispositions

### Nearest-time alignment

**Rejected.** Numeric temporal proximity is not comparability or use authority.

### Backdating future evidence

**Rejected.** Current availability may not rewrite historical decision information.

### Latest-source substitution

**Rejected.** `TARGET_UNAVAILABLE` or source inapplicability in one universe does not authorize replacement with a newer/broader source.

### Source-majority voting

**Rejected.** Source plurality/conflict remains first-class. No count/support/recency winner becomes actor truth.

### `LOW_SUPPORT -> certainty`

**Rejected.** Weak support remains weak and may only be consulted under an exact owner rule.

### `ZERO_SUPPORT -> actor impossibility`

**Rejected.** No empirical conditional basis is not actor-state zero or metaphysical impossibility.

### `null -> zero`

**Rejected.** Not-asked/inapplicable/unavailable/null remains distinct from `OBSERVED_ZERO` and `ZERO_SUPPORT`.

### source conflict -> one field

**Rejected.** Exact source components and conflict state remain reachable and uncollapsed.

## 8. Metabolism seam

SV3C adopts SV3M's accepted non-dispositive ceiling:

```text
no exact metabolism authority/read permission
=> NO_PSEPF_TRANSITION_EFFECT
```

Effective-time/source-state admissibility cannot itself grant mutation authority. A perfectly aligned field still has no causal effect unless a named V3 owner is allowed to consult it for an exact operation.

Conversely, metabolism permission cannot cure an inadmissible time/source state. Read permission is downstream of exact field/intake admissibility.

## 9. Replay law

Historical replay must bind exact:

- actor-fact snapshot ref/hash and effective time;
- comparator receipts/authorities;
- source-indexed PSEPF IDs/hashes and historical scopes;
- V3 decision/use class and effective time;
- time-alignment rule identity once accepted;
- metabolism authority/read-permission identity;
- exact per-source states and comparison state;
- actual consulted field components/cells where applicable;
- causal parent and RNG receipts where the owner transition uses them.

Replay must not consult `latest`, current scheduler time, nearest wave, or a newer preferred source unless the run is explicitly a new counterfactual rather than replay.

## 10. Parent-close obligations

SV3C leaves one deliberate non-dispositive identity decision to SCRV3:

`SV3C-U01 = FINAL_MACHINE_IDENTITY_AND_CANONICAL_HOME_OF_THE_V3_EFFECTIVE_TIME_ALIGNMENT_RULE_NOT_SELECTED_BY_THIS_FEEDER`

SCRV3 must decide whether the accepted rule lives inside the final `V3EmpiricalPossibilityInput` contract, as a dependency of the accepted metabolism authority, or another already-authorized SCRV3-local contract artifact.

The parent must preserve the semantic ceiling regardless of that packaging choice:

```text
four clocks remain distinct
nearest/latest/backdate substitution forbidden
upstream requery != V3 rebind
source-state vector preserved per component
unknown alignment fails closed
missing metabolism authority means zero PSEPF transition effect
```

## 11. Output inventory

SV3C returns exactly:

1. `RESULT.md`
2. `RESULT.json`
3. `EFFECTIVE_TIME_ALIGNMENT.md`
4. `SOURCE_STATE_ADMISSION_MATRIX.csv`
5. `NEGATIVE_PRECEDENCE_MATRIX.csv`
6. `HOSTILE_FIXTURES.md`
7. `PARENT_HANDOFF.md`

Final feeder token:

`SV3C_FEEDER_COMPLETE`
