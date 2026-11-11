# S14-T15 — NORM_PRACTICAL_REALIZATION source-first successor contract R1

## Status and jurisdiction

This is an **append-only source-first reconstruction contract** for a proposed new S14 relation channel, `S14-T15`.
It does **not** mutate sealed O10 R1, does not redefine S14-T06, does not authorize Job 3, and does not rebuild O11/O12.
After worker reconstruction and central adjudication, Vozhd may install an O10 successor that adds T15 and then rebuild O11/S16 and O12.

Existing S14-T06 remains the high-precision **norm ↔ same-predicate stated/intended/realized conduct** relation.
T15 exists because source review shows useful norm→realization relations that cannot be represented safely by strict T06 identity.

## Relation type

`S14-T15`
`relation_type = NORM_PRACTICAL_REALIZATION`

A T15 edge says that the second member is a source-governed **realization, enactment, exercise, violation, or explicit means/application** of the first member's normative proposition.

It is not a generic "related attitude" edge.

## Allowed manifestation subtypes

### 1. DIRECT_ENACTMENT
The praxis member is a concrete/narrower performance that directly satisfies or instantiates all or a bounded part of the norm.

Examples:
- "people should help less-fortunate others" → contributing time to help needy people.
- source norm encouraging sadaqa/charitable giving → respondent monetary donation to charity/those in need.

The link must follow from the source semantics themselves. Shared topic is insufficient.

### 2. RIGHT_OR_PERMISSION_EXERCISE
The norm grants, endorses, or treats as criterion a right/freedom/permission to perform action X; the praxis member measures exercise or concrete instantiation of X.

Examples:
- freedom/right to participate in protests → respondent protest participation.
- freedom to travel abroad → respondent travel abroad.
- ability/right to join organizations → membership in a source-compatible organization subtype.

Target narrowing must be explicit and recorded.

### 3. PRACTICAL_VIOLATION
The praxis member directly instantiates a prohibited, rejected, noncompliant, or contrary practice on the norm's action/target axis.

Examples:
- president should obey laws/courts → observed presidential noncompliance.
- norm rejecting political violence → respondent violence/willingness when the source establishes the same action axis.

Absence of the desired behavior is not by itself a violation. The contrary action or noncompliance must be source-provable.

### 4. INSTITUTIONAL_OR_SOCIAL_REALIZATION
The norm defines an institutional/social criterion or ought-state; the second member measures whether that state is actually realized.

Examples:
- free/genuine electoral choice as a democracy criterion → whether voters actually receive genuine choice.
- guaranteed basic civil rights as a democracy criterion → measured extent of those rights being guaranteed.

This subtype is a norm→world-realization edge, not respondent self-conduct. `praxis_shore_kind` must identify the institutional/social actor.

### 5. INSTRUMENTAL_ENACTMENT
The second member is an explicit means toward satisfying the norm/end even though the surface action differs.

This is the highest-risk subtype and requires one of:
- `SOURCE_EXPLICIT_MEANS`: the native instrument itself states the means/end relation;
- `GOVERNED_T04_BRIDGE`: an already governed T04 goal↔means relation establishes it;
- `SOURCE_NATIVE_BATTERY_BRIDGE`: a shared source stem/battery explicitly defines the action as a way of realizing the norm/end.

General social-science knowledge, ideology, causal intuition, driver/facet overlap, embeddings, or "this would probably help" are forbidden.

A policy stance may appear here only when the source or a governed bridge explicitly establishes it as a practical means/application. Example: "help the poor" → "support redistribution" is **BLOCKED_NEEDS_MEANS_BRIDGE** unless the source itself binds redistribution to poverty relief or a governed goal↔means/application relation does so.

## Orthogonal fields

Every positive records:
- `praxis_shore_kind`: `STATED_INTENDED_CONDUCT | REALIZED_SELF_CONDUCT | REALIZED_OTHER_CONDUCT | LIFE_STATE | INSTITUTIONAL_STATE | POLICY_APPLICATION | OTHER_SOURCE_PROVEN_REALIZATION`
- `relation_polarity`: `ENACTS | EXERCISES | SATISFIES | VIOLATES | REALIZES | FRUSTRATES`
- `realization_distance`: `D1_DIRECT | D2_NARROWER_INSTANCE | D3_EXPLICIT_MEANS`
- actor alignment and actor-instance basis;
- target alignment / any target narrowing;
- routing and respondent-universe intersection;
- exact source provenance;
- bridge basis.

## T06 overlap rule

T15 must **not duplicate a strict T06 edge**.
If the norm and second shore satisfy strict T06 same-predicate actor/target/action identity, preserve/use T06 and record the pair in `T15_T06_OVERLAP_AND_BOUNDARY.csv` with `EXCLUDE_FROM_T15__STRICT_T06`.

If a previously accepted worker T06 is better characterized as one of the T15 subtypes, record `RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW`; do not silently revoke it.

## Candidate discovery

For every assigned wave:

1. Load the prior source-first T06 implementation accounting as the baseline.
2. Treat prior `NORM_SHORE` and `CONDUCT_SHORE` as seeds, **not exhaustive authority** for T15.
3. Re-open `OTHER`/ambiguous items where source semantics could make them:
   - normative principles/obligations/rights/criteria;
   - actual/intended conduct;
   - concrete life states;
   - institutional/social realization states;
   - explicit policy/application/means shores.
4. Build source-native signatures for candidate shores:
   - actor;
   - action/state;
   - target/end;
   - modality;
   - condition/routing;
   - source battery/stem;
   - normative proposition or practical proposition.
5. Crosswalk bidirectionally:
   - every norm → plausible praxis/realization;
   - every praxis/realization → plausible norm.
6. Reconstruct explicit source batteries as batteries.
7. Search all five T15 subtype channels; do not stop after finding strict-T06-style pairs.
8. Where an instrumental/application link is plausible but not source-proven, BLOCK; never infer it from ideology or common sense.

## Dispositions

`POSITIVE_T15`
`BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY`
`NOT_T15_SOURCE_PROVEN_MISMATCH`

Inability to prove a bridge is BLOCK, never negative.

## Hard anti-heuristic law

The following alone can never create T15:
- same topic;
- same driver/facet;
- same political/ideological valence;
- lexical similarity;
- embedding similarity;
- source-wave co-presence;
- demographic association;
- empirical V550 co-travel;
- a plausible causal story supplied by the worker.

Empirical co-travel remains independent downstream evidence and must never be converted into semantic relation truth.

## Completeness gate

A wave is complete only when:
- every prior norm shore has participated in T15 search;
- every newly recovered norm shore is ledgered;
- every praxis-capable shore has participated in reverse search;
- all five subtypes have been considered where source terrain exists;
- exact-T06 overlaps are excluded/ledgered rather than duplicated;
- every instrumental/policy application positive carries explicit bridge authority;
- blocks and coverage defects are preserved;
- zero-positive waves receive hostile sparse-wave review.

