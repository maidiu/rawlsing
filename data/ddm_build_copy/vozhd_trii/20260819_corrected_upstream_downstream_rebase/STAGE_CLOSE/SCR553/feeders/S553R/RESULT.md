# S553R — HOSTILE USE-CHAIN ROUTING / SOURCE-COMPARABILITY FEEDER

**Role:** optional floating specialist S553R  
**Authority:** `NON_DISPOSITIVE_TO_SCR553_AND_M1`  
**Repository:** `maidiu/rawlsing`  
**Exact base SHA:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Branch:** `agent/vozhd-trii-dr-r03-spec-v553-routing`  
**Write scope:** `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/STAGE_CLOSE/SCR553/feeders/S553R/` only  
**Production code modified:** `NO`  
**D15 upstream reopened:** `NO`  
**Broad DAG reopened:** `NO`

## 1. Feeder disposition

S553R returns:

`S553R_FEEDER_COMPLETE`

No binding authority conflict was found, and no exact counterexample requires reopening the R03 broad topology.

The hostile result is a finite routing law for SCR553/M1:

> **V553 need is evaluated per exact governed downstream use chain, never once per admission object. Source relation/comparability/pooling authority is a prerequisite owned outside V553. V553 may create only the temporal/comparability semantics it owns after those source prerequisites are positively governed, or it must emit/preserve typed temporal negative authority or fail closed. A temporal/source negative for one exact use may never be silently downgraded into a direct positive V554 basis for that same use.**

The four mission attacks all resolve inside the frozen R03 topology:

1. one use may bypass V553 while a later use over the same admission requires V553;
2. timestamps/history metadata do not require V553 when no new V553-owned transform is requested;
3. source/time similarity never creates source equivalence, respondent linkage, pooling, estimand compatibility, or composition authority;
4. a V553 temporal limit/noncomparability/missing-authority result blocks positive fallback for the exact governed use, while leaving genuinely different uses independently routable.

## 2. Binding authorities read

S553R read and treated as binding or evidentiary in the required order:

- parent authority `24_DR_R03_SYNTHESIS_RETURN_ADJUDICATION_AND_STAGE_CLOSE_GATE.md` at exact base;
- parent authority `25_STAGE_CLOSE_READ_PARALLEL_COMMAND_AND_LAUNCH_AUTHORITY.md` at exact base;
- accepted R03 synthesis `RESULT.md` and `RESULT.json` on `agent/vozhd-trii-dr-r03-synthesis`;
- accepted `FINAL_BROAD_DAG.md`;
- accepted `WHOLE_MACHINE_CLOSURE_GATE.md`;
- accepted `STAGE_CLOSE_READ_CAMPAIGN.md`;
- `STAGE_CLOSE_READ_BURDEN_MATRIX.csv`, SCR553 row;
- EP553 evidence head `f90cb641cb9f5c18883befd41aac9e5d63002376`;
- R03A head `3d96c1213b46d3e6a908c83c2525f1ef20282f88`;
- R03F head `9f661931d51e03f137601b27eeaecf77ab11ad2f`;
- accepted V553 completion law `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V553_COMPLETION_IMPLEMENTATION_RULING.md`.

The sources converge on the same ceiling:

- R03 S01: temporal routing is governed-use-chain scoped;
- R03 S02: direct V554 is lawful only for an exact temporally-complete positively governed target use;
- R03 S08: source plurality and negative authority are first-class;
- parent 24 law 3/11/12: source relation/comparability/pooling authority remains distinct from V553, provenance is not composition authority, and source-specific states remain distinct;
- SCR553 G553 burden: close the use-chain predicate, source applicability/negative behavior, later-use demand, and deterministic fail-closed routing;
- accepted V553 law: shared columns, readiness, source identity, labels, confidence, and file presence cannot substitute for certified comparability; no semantic delta exists across noncomparable observations.

## 3. Derived governed-use-chain V553 need predicate

Let:

- `A` = one exact positive `StructuralEmpiricalAdmission` plus immutable authority/provenance refs;
- `U` = one exact governed downstream use instance, including consumer, proposition/use identity, rule ID/version/hash, and requested semantic operation;
- `SRC_REQ(A,U)` = the source/universe relation prerequisites required by `U`;
- `SRC_STATE(A,U)` = exact separately-owned source relation/applicability/comparability result for those prerequisites;
- `NEW_T(A,U)` = V553-owned temporal/comparability semantics required by `U` that are **not already lawfully complete** in `A` for `U`;
- `V553_AUTH(op,A,U)` = exact positive V553 authority for each requested temporal operation;
- `TEMP_BLOCK(A,U)` = applicable hard temporal/source negative, noncomparability, ambiguity, conflict, missing-authority, or unresolved state that blocks the requested positive operation;
- `DIRECT554(A,U)` = exact V554 rule/signature positively admits direct `StructuralEmpiricalAdmission` as basis for `U`.

### 3.1 Source prerequisite gate

Before a positive cross-source temporal operation:

```text
if U requires cross-source relation/comparison/harmonization:
    require SRC_STATE(A,U) == POSITIVE_FOR_EXACT_OPERATION
else:
    no cross-source source-relation grant is inferred or needed
```

The grant is operation-specific. A source relation may authorize comparison without authorizing pooling, respondent linkage, synthetic same-person construction, or estimand composition.

If the required source relation is `MISSING`, `UNKNOWN`, `AMBIGUOUS`, `DENIED`, or `NONCOMPARABLE`, V553 cannot repair it. The only lawful outcomes are:

- a governed `TEMPORAL_LIMIT`/negative object that references the blocking source authority state, if V553 owns that negative result for the attempted temporal operation; or
- no positive V553 result / no positive downstream route.

### 3.2 Positive routing predicate

```text
ROUTE(A,U):

1. if A is not positively admitted/applicable for U:
       NO_POSITIVE_ROUTE

2. evaluate required source relation/applicability prerequisites for U.
   if a hard/unknown source prerequisite blocks U:
       V553_NEGATIVE_LIMIT_ONLY, if an exact V553 limit rule owns the attempted operation;
       otherwise NO_POSITIVE_ROUTE

3. compute NEW_T(A,U).

4. if NEW_T(A,U) is nonempty:
       require positive V553 authority for every requested temporal operation.
       if authority missing/unknown:
           V553_NEGATIVE_LIMIT_ONLY where explicitly governed;
           otherwise NO_POSITIVE_ROUTE
       else:
           A -> V553 -> exact TEMPORAL_* output(s)
           -> downstream consumer if separately eligible

5. if NEW_T(A,U) is empty:
       V553 is not required for U.
       if DIRECT554(A,U) and all U-specific applicability/negative gates pass:
           A -> V554
       else:
           NO_POSITIVE_ROUTE
           # never synthesize a V553 wrapper merely to obtain transit
```

### 3.3 The crucial non-global rule

```text
ROUTE(A,U1) does not determine ROUTE(A,U2).
```

A lawful example:

```text
U1 = bounded affordance at exact admitted 1985 point
ROUTE(A,U1) = A -> V554

U2 = later request: persisted from 1985 to 1995?
ROUTE(A,U2) = A/other governed observation(s) -> V553 temporal relation/limit -> downstream
```

The earlier direct decision is not evidence that the admission is globally `NON_TEMPORAL`. The later use must be re-evaluated against its own requested semantics and authorities.

## 4. What does not trigger V553

None of the following, alone, is a lawful `NEEDS_V553` predicate:

```text
HAS_TIMESTAMP
HISTORICAL_SOURCE
HAS_PERIOD_LABEL
SAME_CALENDAR_YEAR
V553_ARTIFACT_EXISTS
V553_COMPATIBILITY_VIEW_EXISTS
SAME_CANONICAL_LABEL
SAME_GEOGRAPHY_STRING
SAME_SOURCE_FAMILY
HIGH_CONFIDENCE
HIGH_SUPPORT
RECENT_ARTIFACT
FILE_ORDER
ROW_ORDER
```

A direct V554 use remains lawful when the exact admission already contains all temporal scope/effective-time meaning required by that use and an exact V554 rule admits the direct basis.

## 5. What does trigger V553, conditionally

`NEW_T(A,U)` is nonempty when the exact use needs new V553-owned semantics, including the accepted families/operations:

- canonical temporal identity/observation semantics not already lawfully complete for the use;
- cross-wave/cross-time temporal comparability;
- governed harmonization across temporal representations;
- derived interval/effective period;
- sequence/before-after/relation timing;
- delta/change;
- persistence;
- drift;
- reversal;
- rupture/revision only under explicit deterministic rule authority;
- temporal/source-time relation;
- temporal limit/noncomparability needed as a first-class result.

The trigger creates only a **need for V553-owned transformation**, not a source relation grant. Positive source prerequisites and exact V553 operation authority remain independently required.

## 6. Source-comparability boundary

S553R derives a strict separation among four questions that convenience code could otherwise collapse:

1. **Are two observations in the same or lawfully related respondent/source universe for this operation?**  
   Owner: source/universe relation/applicability authority, not V553.

2. **Are their constructs/semantic references comparable for the requested temporal operation?**  
   Requires the accepted certified semantic/directionality/position/comparator authority; V553 may consume that authority but may not infer it from labels.

3. **May V553 create a temporal relation/harmonization/limit over them?**  
   Owner: V553 temporal operation authority, after 1/2 are satisfied or typed negative input is available.

4. **May their respondent samples/weights/estimands be pooled, joined, or numerically composed?**  
   Owner: separate positive linkage/pooling/composition/estimand authority. Temporal comparability does not answer this question.

Therefore:

```text
COMPARABLE_FOR_TEMPORAL_OPERATION
!= SAME_RESPONDENT_UNIVERSE
!= RESPONDENT_LINKAGE_AUTHORIZED
!= POOLING_AUTHORIZED
!= ESTIMAND_COMPOSITION_AUTHORIZED
```

and:

```text
PROVENANCE_REACHABLE
!= SOURCE_RELATION_AUTHORIZED
```

## 7. Temporal negative precedence

For the **same exact governed use** `U`:

```text
applicable TEMPORAL_LIMIT / NONCOMPARABLE / MISSING_AUTHORITY / CONFLICT
> any convenience attempt to reuse A as a direct positive basis for the semantic that was blocked
```

This is not a global poison rule. A negative for cross-source comparison `U2` does not invalidate a distinct same-source point use `U1` that does not require the blocked relation.

Required negative behavior:

- `NONCOMPARABLE` is not `NO_EFFECT`, `ZERO`, or `FALSE_RELATION`;
- `MISSING_AUTHORITY` is not `TEMPORALLY_COMPLETE`;
- `INSUFFICIENT_PERIODS` is not permission to use the latest point as persistence evidence;
- `BASELINE_UNAVAILABLE` is not permission to invent a baseline;
- `CONFLICT` is not permission to choose the higher-support or newer source;
- a V553 negative/limit may not be dropped merely because a direct admission object is physically available;
- a direct basis remains lawful only for a different use whose own predicates independently pass.

## 8. Hostile mission conclusions

### Later-use temporal demand

**Attack:** U1 bypasses V553, U2 later requests persistence/change over the same admission.

**Result:** broad topology survives. The route decision is recomputed for U2; U1 is not precedent. U2 must consume V553 temporal semantics or fail closed.

### Timestamp but no transform

**Attack:** exact point admission has a year/timestamp and legacy V553 adapter can wrap it.

**Result:** direct route survives. Metadata presence is not semantic work; no-op V553 transit is forbidden.

### Source/time similarity

**Attack:** two sources share year, labels, canonical coordinate names, and similar values.

**Result:** no source equivalence follows. Cross-source positive temporal operation requires separate positive relation/comparability authority. Pooling/linkage/composition require still-separate grants.

### Temporal negative fallback

**Attack:** V553 returns or must preserve `TEMPORAL_LIMIT`/noncomparability, while a direct admission remains physically available.

**Result:** no direct positive fallback for the same use. The negative is semantic authority and must survive. Different uses remain independently routable.

## 9. No broad-topology counterexample

Every hostile case can be satisfied by the accepted R03 owners/edges:

- `StructuralEmpiricalAdmission` remains the structural admission boundary;
- V553 remains conditional on new temporal/comparability meaning for the exact use;
- direct V554 remains lawful for exact temporally-complete eligible uses;
- source relation/pooling remains separately governed;
- `TEMPORAL_LIMIT` remains first-class negative authority;
- M1 remains the correct seam to reconcile SCR553 routing with SCR554 basis/negative/duplicate precedence.

No new broad owner or edge is required. Therefore S553R does **not** emit `S553R_BROAD_TOPOLOGY_COUNTEREXAMPLE_CANDIDATE`.

## 10. Exact handoff burdens to SCR553 and M1

SCR553 should freeze a machine-readable contract equivalent to the predicate above with explicit fields/refs for:

- exact governed use identity;
- requested V553 temporal semantic operation(s);
- proof that required temporal meaning is or is not already complete for that use;
- exact separately-owned source relation/applicability/comparability refs and states;
- exact V553 operation authority refs;
- exact hard-negative/limit precedence;
- output family mapping to `TEMPORAL_KEY`, `TEMPORAL_OBSERVATION`, `TEMPORAL_RELATION`, `TEMPORAL_LIMIT`;
- deterministic replay/identity bindings;
- no raw `EmpiricalFact` intake and no source equivalence invention.

M1 should prove jointly with SCR554 that:

- direct and V553 temporal basis classes are selected by exact use, not object-global labels;
- an applicable temporal/source negative for a use cannot be bypassed by the direct basis;
- source-comparability prerequisites are not silently reinterpreted as V554 temporal completeness;
- a prior direct decision for U1 does not suppress V553 need for U2;
- unknown/missing source relation or temporal authority fails closed;
- the M1 seam does not make V553 the source-equivalence owner or V554 the temporal-negative override owner.

## 11. Feeder token

`S553R_FEEDER_COMPLETE`
