# M04 — reproduction constraints: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED`; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/systems/reproduction.py` `6f3a815d7ef6c5e7fd6003c4b4fd1b3bf1b2dc90cedcdcd332088737ee701916`; `v3/core/derived.py` `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360`; `v3/psyche/gating.py` `4a82c7c91828b87bb61cd651c777159f04b5733e64158f8679a24efcec1ccfc6`; `v3/io/identity_to_backbone.py` `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda`.  
**Surface:** S2 local Mac; no production edit; no current C9/C12 execution.

## 1. Exact as-built map

| Element | Source | Inputs / state reads | Operation | State writes / outputs | Callers / first consumers |
|---|---|---|---|---|---|
| `ReproductionConstraints` | `v3/core/state.py:58-70` | `dependents, housing_insecurity, legal_status (=100 secure), debt, job_insecurity, caregiving_load` | dataclass, clamp | stored `state.reproduction_constraints` | connector; yearly steps; JSON codec |
| `update_reproduction_constraints` | `v3/systems/reproduction.py:10-66` | `state.events_this_year[].reproduction_deltas`; annual cap (`v3config.delta_caps.reproduction_constraints_fields`, default 20) | sum deltas per field; cap summed delta; add; clamp | `state.reproduction_constraints.*` | `run_one_year` at `reproduction_constraints_update` (`yearly_step.py:131`); derived `hostage_index` then recomputed |
| `compute_hostage_index` (canonical) | `v3/core/derived.py:34-58` | reproduction constraints | weighted sum: dependents .25, housing .20, legal insecurity .15, debt .15, job .15, caregiving .10; weights sum 1.0 | `DerivedIndices.hostage_index` | derived AC, mis_aim, stability, alignment, metabolic style, registers, scoring |
| `_derive_hostage_index` (private gate) | `v3/psyche/gating.py:61-71` | reproduction constraints | different weighted sum: housing .35, legal .25, dependents .60, debt .30, job .30, caregiving .35; weights sum 2.15; clamp 0–100 | used by `apply_expression_gating` | pressure-flow pre-route gating |
| Initial constraints | `v3/io/identity_to_backbone.py:286-312` | identity class only | `dependents=0, housing_insecurity=0, legal_status=100, debt=class lookup, job_insecurity=class lookup, caregiving_load=0` | `state.reproduction_constraints`; `initial_state_provenance` | server generation; v2→v3 connector |
| Parent baseline bridge (adjacent M15/M36) | `v3/io/parent_baseline_from_behavior.py:25-86` | parent behaviour warmth/authority/material | averages father/mother with 50 defaults; maps to need-axis labels and transmission regime | `identity["parent_expectation_baseline"]`, `transmission_regime` | `backbone_state_from_identity`, child model; not actual care |

**Defaults and hidden laws.** Everyone starts with `dependents=0`, `housing_insecurity=0`, `legal_status=100` (secure), and `caregiving_load=0`; only debt and job insecurity vary by class (`identity_to_backbone.py:286-312`). The default construction therefore treats “no dependents, no housing insecurity, secure legal status, no caregiving” as the normal baseline, not as unknown. `caregiving_load` is a single adult scalar; it does not say whether the caregiver is present, warm, coercive, absent, or whether another person supplies care. `dependents` is a number, not a household roster with ages/needs/co-residence. There is no schedule of absence/presence and no actual care transaction.

## 2. What this actually models, and what it does not

The code models **objective-ish constraint quantities** that affect a derived `hostage_index` and an expression gate. It does not model:

- actual co-residence, custody, shift work, migration, illness or school hours;
- actual co-care by kin, neighbours, institutions or paid workers;
- realised caregiving conduct (warmth, coercion, neglect) or the child's received care;
- the difference between a parent's love/intention and practical availability;
- the difference between material presence and coercive parenting;
- a child's own objective dependence and feasible participation.

The parent-behaviour bridge uses warmth/authority/material support and converts them to need-axis labels and a transmission regime. That is a **parent-behaviour prior**, not a record of realised care. It can say “low material support → status/competence forbidden” but cannot say “the parent loves the child, works two shifts, and the grandmother feeds the child.” Conversely, high material support plus high authority can produce a coercive parent label, but the old code has no independent parent actor who actually acts.

The private `_derive_hostage_index` differs from the canonical `compute_hostage_index`; the same state can be 52.5 on one and 100.0 on the other (X05 probe). That is a semantic conflict, not two names for one quantity.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N01 needs/motives/objects | `INFRASTRUCTURE_ONLY` | constraints are objective preconditions, not needs or motives |
| N06 activity/time/stages/social reproduction | `PARTIAL_WRONG_MEANING` | constraints/hostage arithmetic exists; no activity schedule, caregiving realisation, co-care, or stage-attainable participation |
| N07 independent others/power/love | `INFRASTRUCTURE_ONLY` / `MISSING` core | no independent parent/co-caregiver; no actual relation of care or power |
| N12 actual C12 person | `INFRASTRUCTURE_ONLY` / `UNKNOWN` | no current C9/C12 consumer |

**Disposition: ADAPT, with one conflict to repair.** Keep a typed objective constraint record and a canonical derived index. Remove the duplicate private gate until an owner declares which formula is authoritative. Add source-qualified household/work/care/co-care records. Separate objective constraint, caregiver conduct, child's received care, and actor-accessible significance.

## 4. Harmful defaults / defects to remove

1. **No-dependents/no-caregiving/secure-legal default.** `0/0/100/0` is a silent optimistic household; unknown must be explicit.
2. **Class → debt/job insecurity only.** No actual occupation, hours, contract, benefits, housing tenure or household composition.
3. **One scalar for caregiving.** `caregiving_load` cannot express “loving but unavailable”, “present but coercive”, “absent but materially providing”, or “co-care substitutes”.
4. **Duplicate hostage formulas.** Canonical weights (sum 1.0) vs private gate weights (sum 2.15); the private gate can saturate. Owner must choose or keep two explicitly named indices.
5. **Parent behaviour → child baseline without actor care.** The bridge can convert unknown/midpoint parent behaviour into hopeful/forbidden child labels; it is not evidence of realised care (see M15/M36 and RX01).
6. **Care is not a write.** No `care_received` record; the child's care is inferred from adult constraints/behaviour.

## 5. Proposed typed seam (nonissuing)

```text
HouseholdConstraintRecord {
  household_id; actor_ids[]; co_residence; dependents[]; legal_status;
  housing_tenure; debt; work_contracts[]; caregiving_obligations[];
  source_refs[]; unknown_fields[]; clock; rule_version;
}
CareArrangement {
  dependent_id; caregiver_id; start/end clock; presence; realised_actions[];
  warmth/coercion evidence; co_caregiver_ids[]; source_refs; access;
}
```
`CareArrangement` must be produced by independent actor/world records, not by averaging parent fields. The first consumer should be:
1. `FeasibleParticipation` (can the dependent actually be fed, schooled, accompanied, left alone?);
2. `ActorAccessibleCare` (what the child can perceive/remember);
3. a scoped `Expectation`/`CareAvailability` record under CAN010/011;
4. a later C9 semantic read.

**Owner:** SDTF/world/ADP019 for the objective household and schedule; CAN010/CAN011 for the actor-side expectation/formation; ADP016/017 for memory/access; C9/C12 for the consumer. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Case A — loving but work-constrained.** Parent warmth 85, authority 45, material 20, works long hours; grandmother provides daily care. Old code can set low material support and high caregiving load, but cannot represent the grandmother's realised care or the child's actual receipt. The child may acquire warm expectancy and worldly insufficiency in reality; the old code cannot lawfully derive that from the separate adult scalars.

**Case B — materially present but coercive.** Parent warmth 30, authority 80, material 80. Old parent-type inference can label the parent type 8 and the child model can become safety/autonomy forbidden; but the code has no independent parent who performs coercive acts, and high material provision may coexist with coercion. The old code's labels are not a record of care.

**Case C — competing co-care.** Mother and aunt both provide care; mother is absent for work, aunt is warm. Old code has one `caregiving_load` and parent magnets labelled mother/father; there is no aunt actor, no co-care ledger, and no way to distinguish which caregiver supplied which care.

**Hostile alternative.** The apparent effect of reproduction constraints may be mediated by parent warmth or by the child's temperament, not by material constraint. A hostile test holds parent warmth/type and event stream fixed, varies only the actual work/co-care interval, and checks whether the child's later semantic expectation changes. If it does not, the old `hostage_index` is not a care mechanism.

**Falsifier.** If two households with identical `hostage_index` but different realised co-care produce different child care/expectation, the old index is too coarse. If changing the index alone changes a C9 semantic read while care is fixed, the consumer is reading a policy scalar, not the world.

## 7. Tests and limits

- Sourcefree probes (X05): canonical hostage 52.5 vs private gate 100.0 on the same constraint state; reproduction delta `+100` capped to `+20`; capacity/reproduction caps confirmed.
- Related historical test: `v3/tests/test_step_logic.py:27-60` (reproduction delta/cap, hostage movement). It tests arithmetic only.
- **NOT_RUN:** full old suite; any actual household/care schedule; current C9/C12; native person.
- **No native rule, coefficient, or source permission is issued.**

**Required future reviewer:** independent V3 source/consumer reviewer for M04/N06/N07; SDTF/world/ADP019 owner for household and care facts; CAN010/CAN011 for expectation/formation; current C9/C12 implementer. X05 does not self-adopt.
