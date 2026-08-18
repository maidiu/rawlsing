# VT3-CM-R06 — MINIMAL CONDITIONAL-EVIDENCE ARCHITECTURE

## Cell metadata

- Cell: `VT3-CM-R06`
- Mission: minimal lawful architecture for position-conditioned empirical meaning
- Exact launch base: `8c87f7725ba58202b5377c974548140420709fa9`
- Assigned branch: `agent/vozhd-trii-vt3-cm-r06`
- Production-code modification: **FORBIDDEN / NONE**
- Verdict: **PASS_WITH_SPINE_REVISION**

## Executive ruling

The valuable terminal core of the present V550 determinicity terrain can be represented by a substantially smaller authority-first architecture, but the proposed serial spine must be revised.

The minimum lawful empirical object is a governed **conditional empirical distribution**: a replayable distribution of a governed response/target over an explicitly normalized structural-position predicate, historical/cell scope, denominator regime, weighting authority, support state, uncertainty state, and provenance. It is evidence about a historical comparison population. It is never an actor identity, belief, trait, destiny, or permission to infer membership.

V551 signed evidence and V552 position-conditioned pressure are distinct semantic projections over that empirical authority. They may be selectively materialized or cached for terminal latency, but they must not replace or erase the underlying conditional distribution where terminal consumers require its plurality, support, uncertainty, or provenance.

The physical chain must **not** require V550 meaning to be copied through V551, V552, and V553–V557 merely to reach runtime. Accepted V557/V558 and V3 architecture requires two-phase resolution: generic structural context can be bound before an actor's generated position exists; once V3 has lawfully generated the exact period-entry position, V558 may re-resolve the same immutable structural authority using that exact position. V553–V557 therefore remain owners of their own distinct temporal/mediation/interaction semantics, not a mandatory transport corridor for V550–V552 conditional evidence.

This ruling is intentionally architecture-only. Exact field-by-field producer/consumer archaeology and measured savings remain dependent on R01–R05 as identified in section I.

## Governing invariants

1. Preserve real subgroup heterogeneity, including minority and multimodal configurations.
2. Preserve denominator, weighting, support, uncertainty, suppression, and source authority; do not emit false certainty.
3. Population correlation or conditional frequency never establishes actor membership, identity, belief, intention, or response.
4. Negative authority and typed absence remain first-class; absence is not zero, neutrality, or population-average fallback.
5. Identical structural position and identical empirical evidence must permit multiple lawful generated lives.
6. Every terminal fact must be provenance-replayable to governed source snapshots and transform authority.
7. Semantic jurisdiction does not imply mandatory stage-local materialization.
8. A canonical family survives only if deleting it would starve a distinct required terminal meaning that cannot be lawfully reconstructed from retained canonical authority.

---

# A. Semantic DAG

```text
GOVERNED SOURCE / VARIABLE / TRANSFORM / WEIGHT AUTHORITY
                         |
                  WORKLOAD COMPILER
                         |
              SHARED RESPONDENT FACT SUBSTRATE
                         |
          CONDITIONAL_EMPIRICAL_DISTRIBUTION (CED)
                    /                    \
                   /                      \
       V551 SIGNED CONDITIONAL        eligible direct
              EVIDENCE  ----------------> V552 PRESSURE
                   \                       /
                    \                     /
                     -----> V558 <---------
                              ^
                              |
                    V3 exact position_t

V553 -- V554 -- V555 -- V556 -- V557 ----> V558
     (only each stage's own distinct authoritative semantics)
```

### Semantic ruling

- CED is the canonical empirical meaning: `distribution(target | governed position predicate, scope, time, authority regime)`.
- V551 owns a **signed/directional comparison projection**, not the underlying historical population itself.
- V552 owns **position-conditioned structural pressure**, retaining component disagreement/support rather than replacing plurality with a bare scalar.
- V553–V557 remain independently authoritative for their accepted jurisdictions; they do not acquire ownership of CED merely because runtime eventually joins all structural context.
- V558 owns exact runtime composition and applicability resolution.
- V3 owns generated actor position and developmental trajectory.

The semantic DAG is therefore branched, not a lossy serial pipeline.

---

# B. Physical DAG

## Canonical persistent families

```text
Authority snapshots / governed dictionaries / transform rules
                    |
Terminal-reachable conditional workload manifest
                    |
Shared respondent fact substrate + immutable source hashes
                    |
Canonical CED facts
          |                     |
          | deterministic       | deterministic / governed
          v projection          v projection
V551 signed-evidence cache   V552 pressure cache
          \                     /
           \                   /
              V558 resolver
                   |
          ephemeral ResolvedStructuralContext
```

The minimum physical persistence set is:

1. governed source/variable/weight/transform authority and immutable source snapshot identities;
2. the terminal-reachable workload specification that states which lawful conditional questions were compiled;
3. a shared respondent fact substrate sufficient for exact replay of retained conditional facts, subject to governing retention law;
4. canonical CED facts.

V551 signed evidence and V552 pressure are semantically real products, but their **materialization policy** is separable from their jurisdiction. They may be deterministic on-demand projections, selective persisted caches, or compatibility materializations. If persisted, their identity must include projection/aggregation rule version and canonical source references; they must not become independent empirical source authority.

`ResolvedStructuralContext` is runtime composition, not a new historical authority. It is disposable/recomputable from its referenced authorities.

No V553–V557 stage-local mirror of CED/V551/V552 is required solely for transport.

---

# C. Minimal schemas

## C1. Canonical conditional empirical object

```text
ConditionalEmpiricalDistribution {
  identity: {
    conditional_fact_id,
    schema_version
  },
  subject: {
    dataset_id,
    governed_target_id,
    target_domain
  },
  conditioning: {
    predicate,
    canonical_position_key?,
    cell_scope,
    temporal_scope
  },
  distribution: {
    values[] {
      canonical_value,
      raw_n,
      weighted_n,
      estimate
    }
  },
  denominator: {
    eligible_n,
    matched_n,
    target_observed_n,
    target_missing_n,
    weighted_denominator,
    denominator_rule_id
  },
  weighting: {
    weighting_authority_id,
    weight_variable_id?,
    normalization_rule,
    survey_design_id?,
    replicate_method?
  },
  support: {
    support_status,
    effective_n?,
    minimum_support_rule_id
  },
  uncertainty: {
    method,
    intervals[],
    design_effect?,
    suppression_status?
  },
  authority: {
    source_snapshot_ids[],
    source_hashes[],
    respondent_substrate_hash,
    workload_spec_id,
    workload_spec_hash,
    transform_rule_id,
    transform_version
  },
  absence: {
    absence_type?,
    reason_authority_id?
  }
}
```

`conditional_fact_id` is deterministic over source/snapshot authority, governed target, normalized predicate, cell/spatial scope, temporal scope, weighting regime, denominator semantics, and schema/transform version. Filename, stage number, MI rank, branch-tree location, outlier status, or generation order are not identity.

Equal numerical estimates under different weighting, denominator, time, source, or transform authority are distinct facts.

### Predicate representation

Use a typed normalized predicate AST, restricted to authorized operators actually needed by terminal workload:

```text
EQ(field_id, canonical_value)
IN(field_id, canonical_values[])
RANGE(field_id, lower, upper, closure)
AND(...)
OR(...)
NOT(...)
```

Canonicalization sorts commutative operands and normalizes governed values so logically equivalent authorized predicates share identity. A predicate identifies a historical comparison population. It does not assert that a runtime actor possesses an ungenerated trait.

## C2. V551 signed projection

```text
SignedConditionalEvidence {
  evidence_id,
  empirical_fact_refs[],
  evidence_axis,
  comparator_ref?,
  direction: POSITIVE | NEGATIVE | NEUTRAL | INDETERMINATE,
  magnitude?,
  comparison_measure?,
  support_ref,
  uncertainty_ref,
  projection_rule_id,
  projection_rule_version,
  provenance_refs[],
  absence_type?
}
```

`NEUTRAL` is an observed/provenance-backed evidentiary result. It must not be used as the encoding for missing, suppressed, unsupported, or inapplicable evidence.

## C3. V552 pressure projection

```text
PositionConditionedPressureFact {
  pressure_fact_id,
  position_predicate,
  temporal_scope,
  pressure_axis,
  components[] {
    signed_evidence_ref,
    contribution,
    support_ref,
    uncertainty_ref
  },
  aggregate_pressure?,
  aggregation_rule_id,
  aggregation_rule_version,
  disagreement_state,
  support_state,
  uncertainty_state,
  provenance_refs[],
  absence_type?
}
```

An aggregate scalar may be exposed, but it cannot be the sole retained semantics when terminal interpretation requires knowing that components conflict, are weakly supported, or differ in uncertainty.

## C4. Runtime exact-position resolution

Conceptual contract:

```text
resolve_structural_context(
  run_id,
  dataset_id,
  cell_before,
  cell_after,
  census_year_before,
  census_year_after,
  year_fraction,
  exact_position_key,
  position_effective_time
) -> ResolvedStructuralContext
```

Phase B resolution performs exact position applicability, temporal selection, governed fallback, authority/provenance joins, and typed absence. It may combine direct CED matches, V551 signed evidence, V552 pressure, and the independent authoritative outputs of V553–V557.

It must not discover new cohorts, select a statistically "best" predictor, infer actor psychology or membership, turn pressure into destiny, conceal weak support, or silently broaden a failed predicate.

---

# D. Jurisdiction ownership

| Meaning | Owner | Physical consequence |
|---|---|---|
| Source/variable semantics, admissibility, weight and transform authority | governed upstream authority | canonical |
| Which conditional questions are lawful/terminally reachable | workload compiler | canonical manifest |
| Respondent observations required for replay | shared fact substrate | canonical subject to retention law |
| Conditional empirical distribution | V550 conditional-empirical jurisdiction | canonical CED |
| Signed/directional comparison evidence | V551 | deterministic semantic projection; persist/cache only as justified |
| Position-conditioned structural pressure | V552 | deterministic/governed semantic projection; persist/cache only as justified |
| Temporal/mediation/interaction and other accepted 553–557 semantics | V553–V557 respectively | retain only their distinct authority; no CED transport mirrors |
| Runtime exact applicability/composition | V558 ContextResolver | ephemeral/recomputable resolved context |
| Generated actor position, mobility and developmental life | V3 | runtime/generated authority |

No later stage gains authority to reinterpret an upstream statistical association as actor identity merely by receiving or referencing it.

---

# E. Replacement mapping for current V550/V551/V552 terrain

This table gives the R06 architectural disposition of every named conditional/determinicity family in scope. R01 remains authoritative for final field-level producer/consumer archaeology and can tighten individual mappings if it proves hidden semantics.

| Current family / field | R06 disposition | Replacement / rule |
|---|---|---|
| V550 `position_distribution` | **CANONICAL CORE** | normalize into CED distribution + denominator + weighting + support + uncertainty + provenance |
| V550 `position_indicator_summary` | **DERIVED COMPATIBILITY VIEW** | deterministic view from CED and governed comparator/projection rule |
| V550 `indicator_answer_matrix` | **DERIVED / DIAGNOSTIC** | reproducible cross-tab/view over shared respondent facts/CED; not independent authority |
| V550 `outlier_cohort_summary` | **DIAGNOSTIC** | compute on demand from canonical facts; never runtime identity authority |
| V550 `secondary_indicator_summary` | **DIAGNOSTIC / DERIVED** | reproducible analysis over canonical facts |
| mutual information | **DIAGNOSTIC** | on-demand analysis; no canonical artifact absent R02/R04 starvation proof |
| Cramér's V | **DIAGNOSTIC** | on-demand analysis; no canonical artifact absent starvation proof |
| entropy | **DIAGNOSTIC** | on-demand analysis |
| secondary gain | **DIAGNOSTIC** | on-demand analysis |
| recursive branch/tree nodes | **REMOVE AS CANONICAL FAMILY** | finite workload predicates plus reproducible diagnostics replace recursive materialization |
| branch signatures | **NORMALIZE** | predicate identity/cache key only; never empirical authority by itself |
| V551 `position_field` / `position_value` | **REFERENCE** | canonical governed predicate/position key |
| V551 `strata_path` | **REFERENCE / COMPAT VIEW** | normalized predicate ancestry only where semantically needed; no duplicated empirical authority |
| V551 `subject_position_signature` | **REFERENCE** | normalized predicate/position-key identity, not actor belief/identity inference |
| V551 `position_conditioning` | **REFERENCE** | CED refs + applicability metadata |
| V551 `position_modifiers` | **PROJECT** | V551 signed-evidence refs; compatibility view if legacy shape is only a mirror |
| V551 `conditional_strata_weights` | **CONDITIONAL RETENTION** | retain only if it encodes a distinct governed projection weighting regime; otherwise point to canonical CED weighting/support authority |
| V551 signed conditional compiler/product | **SEMANTICALLY RETAIN** | deterministic SignedConditionalEvidence projection from CED with rule/version/provenance refs |
| V551J joint packets/component indexes | **PROJECTION / COMPATIBILITY** | references to canonical component facts unless R02 proves irreducible joint weighting/admissibility semantics |
| V552 `position_conditioning_profile` | **CONTRACT TO REFS** | CED + V551 refs plus pressure-specific metadata; no copied empirical mirror |
| V552 pressure observations/components | **SEMANTICALLY RETAIN** | PositionConditionedPressureFact with component refs/support/uncertainty/disagreement |
| V552 aggregate pressure scalar | **DERIVED OUTPUT** | may be cached, but may not erase components/disagreement/support required by terminal use |
| stage-local copies of upstream provenance/support | **REMOVE COPIES** | immutable canonical refs |

The deletion criterion is semantic, not computational: if R01/R02/R04 proves that a nominally diagnostic family contains terminally required information not reconstructible with identical authority, weighting, support, uncertainty, absence semantics, and replayability, that information must be moved into the canonical core before the family is demoted.

---

# F. Compatibility views

Legacy shapes may remain during migration only as deterministic non-authoritative views:

```text
CompatibilityViewMetadata {
  compatibility_view: true,
  canonical_source_refs[],
  derivation_rule,
  derivation_version,
  legacy_schema_version
}
```

Every legacy output must be classified as exactly one of:

- **canonical** — unique terminal semantic authority;
- **derived compatibility** — deterministic reconstruction for an unmigrated consumer;
- **diagnostic** — reproducible analytical output with no runtime authority.

Compatibility views may be emitted at legacy paths temporarily, but must expose canonical sources and derivation identity. They may not acquire independent empirical authority merely because they are persisted.

---

# G. Failure, negative authority, absence, fallback, multi-position and mobility

## Typed absence vocabulary

Minimum architecture must distinguish at least:

```text
PRESENT
VALID_NULL
INVARIANT
NOT_APPLICABLE
NO_MATCHING_SUPPORT
INSUFFICIENT_SUPPORT
SUPPRESSED
SOURCE_UNAVAILABLE
AUTHORITY_UNAVAILABLE
PREDICATE_UNRESOLVABLE
POSITION_UNRESOLVED
NO_POSITION_AUTHORITY
NO_COMPARATOR_AUTHORITY
NO_SIGNED_EVIDENCE
NO_PRESSURE_AUTHORITY
INTENTIONALLY_UNBOUND
UNBOUND_REQUIRES_RUNTIME_POSITION
```

Binding laws:

```text
absence != zero
unknown != neutral
suppressed != zero
no matching cohort != population-average cohort
weak support != deterministic claim
```

Fallback is lawful only under an explicit governed rule. A fallback result records the requested predicate, fallback predicate, conditions dropped or generalized, rule/reason authority, and resulting support/uncertainty state. Silent broadening to population average is forbidden.

## Multiple simultaneous positions

A runtime actor may occupy several structural positions simultaneously. Resolution uses either an authorized compound position key or an explicit conjunction in the normalized predicate. Marginal conditional distributions must not be multiplied or combined under an assumed independence relation unless such a relation is itself governed authority.

## Mobility and historical change

At period `t`:

```text
V3 owns position_t
  -> V558 Phase B resolves facts valid for position_t and time_t
  -> V3 generates one lawful developmental continuation
  -> a governed transition may produce position_(t+1)
  -> V558 rebinds/re-resolves for the new position/time
```

Conditional facts therefore require temporal validity/scope. A former-position fact cannot remain attached to an actor as a permanent identity after a mobility event unless a separate lawful history/exposure rule says so.

Central invariant:

```text
same structural position + same empirical evidence != same generated life
```

---

# H. Migration order

1. Freeze accepted V3/V558 two-phase runtime query semantics and exact-position authority.
2. Freeze CED identity, normalized predicate, denominator, weighting, temporal, support, uncertainty, provenance, and absence contracts.
3. Establish the shared respondent fact substrate/replay authority and retention rules.
4. Compile the finite terminal-reachable conditional workload from governing authority rather than recursively exploring every candidate split.
5. Produce an equivalence corpus comparing CED against current V550 terminal-reachable outputs, including minority, weak-support, multimodal, null, suppressed, and contradictory cases.
6. Re-express V551 signed evidence as a deterministic governed projection over CED; preserve negative/neutral/indeterminate distinctions.
7. Re-express V552 pressure over CED/V551 references while retaining component disagreement/support/uncertainty.
8. Switch V558 exact-position Phase B resolution to direct authoritative lookup of V550/V551/V552 meaning; do not route it through V553–V557 transport mirrors.
9. Replace copied stage-local payloads/provenance with immutable refs.
10. Provide deterministic compatibility views for unmigrated consumers.
11. Demote MI, Cramér's V, entropy, secondary gain, outlier cohorts, secondary summaries, and recursive trees to diagnostics only after R01/R02/R04 establish no terminal starvation.
12. Remove eager computation/materialization only after R05 cost measurement plus replay/equivalence/negative-authority tests pass.
13. Retire compatibility views as consumers migrate; retain canonical CED and distinct semantic projections only where terminal law requires them.

No migration step may trade semantic loss for compute savings.

---

# I. Claims dependent on R01–R05

R06 is a design court, not the synthesis court. The following claims remain explicitly contingent on sibling evidence and must be adjudicated by Vozhd Trii/R00 rather than silently assumed here.

| Sibling court | R06 dependency |
|---|---|
| **R01 — V550 conditional-value archaeology** | final producer/consumer reachability for each named V550/V551/V552 artifact; whether any apparently redundant field contains unique terminal authority; exact stranded/duplicated/superseded paths |
| **R02 — conditional information-loss court** | whether proposed diagnostic families hide irreducible weighting, denominator, provenance, uncertainty, admissibility, negative-authority, replay, or joint semantics; any such semantics must be promoted into canonical core before deletion |
| **R03 — downstream recreation court** | whether V551–V558/V3 already reconstruct equivalent CED meaning; proven equivalence may eliminate duplicate storage, while non-equivalence confirms CED must remain independently reachable |
| **R04 — terminal position-conditioning requirements** | exact terminal distinctions, lawful predicate language, fallback rules, support/uncertainty fields, and workload cardinality that the minimal CED must satisfy |
| **R05 — conditional compute/cardinality court** | measured savings, cache/materialization choices, and the point at which recomputation becomes cheaper than persistence; compute evidence cannot authorize semantic deletion |

### Findings that do not depend on sibling measurement

The following are consequences of binding accepted architecture and therefore stand unless higher authority changes:

- actor position is generated-side authority, not inferred from empirical prevalence;
- conditional population evidence cannot be converted into actor belief/identity;
- typed absence and negative authority cannot be collapsed into zero/neutral;
- V558 exact-position resolution occurs after the runtime position is available and may query immutable structural authority directly;
- semantic jurisdiction does not require stage-mirror materialization;
- V553–V557 need not and should not be mandatory transport mirrors for V550–V552 conditional evidence;
- multiple lawful lives must remain possible under identical structural conditions.

---

# Acceptance tests for the proposed architecture

The sparse architecture is lawful only if an implementation pass can demonstrate all of the following against the existing machine:

1. terminal-reachable conditional distributions reproduce governed current results under identical source, denominator, weighting, and transform authority;
2. minority and multimodal distributions remain distributions rather than winner-take-all labels;
3. weak support and uncertainty survive through V551, V552, and V558;
4. absence/suppression/inapplicability never become zero, neutral, or silent population fallback;
5. V551 signs and V552 pressures are replayable to CED and projection rules;
6. contradictory pressure components remain observable;
7. V558 can resolve exact period-entry position without any inference from prevalence;
8. mobility causes temporal re-resolution rather than permanent attachment of a former conditional fact;
9. legacy views are byte/semantic-equivalent where compatibility is required, or differences are explicitly adjudicated;
10. eliminating recursive determinicity computation cannot change the set of lawful terminal queries defined by authority.

## Final architecture disposition

**`MINIMAL_CONDITIONAL_EVIDENCE_ARCHITECTURE = PASS_WITH_SPINE_REVISION`**

The smallest lawful architecture is an authority-first, workload-bounded conditional-fact substrate centered on canonical CED facts, with V551/V552 as governed projections and V558 as the exact-position runtime join. It removes recursive/exploratory determinicity families and stage-mirror transport from canonical runtime architecture unless R01–R05 prove a specific starvation case. The design preserves plurality, uncertainty, provenance, typed absence, negative authority, mobility, and actor/runtime jurisdiction while allowing the broad current determinicity surface to collapse into a much smaller canonical core plus reproducible views and diagnostics.

## Binding source terrain inspected at the launch base

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/TERMINAL_DEMAND_ENVELOPE.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/ARCHITECTURE_PASS_LAW.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/SEAM_INTEGRITY_CLOSURE_RULING.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/recalibration/TD_R04_V557_V558/RESULT.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/recalibration/TD_R05_V3_DEVELOPMENTAL_RUNTIME/RESULT.md`
- existing V550–V552 artifact/implementation terrain at launch base as implementation evidence, not physical-architecture authority
