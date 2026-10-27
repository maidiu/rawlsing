# M12 — collective infrastructure: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED`; `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/systems/infrastructure.py` `a062192707bb6697c6d38a1ef3a72ca0ac6daedb759a38fd2fcb2cf4e219c235`; `v3/core/derived.py` `e479fc3eba21734752c372742fb2ee247cbdde6a73ac42545dc30b5039301360`; `v3/psyche/flow.py` `6da4effde2b1ccb7c346f73b17632ceee3a7a8c37a63a10f096753d070ab1d3d`.

## 1. Exact as-built map

| Element | Source | Inputs / state reads | Operation | State writes / outputs | Consumers |
|---|---|---|---|---|---|
| `CollectiveInfrastructure` | `v3/core/state.py:218-227` | `network_density, org_discipline, resource_pool, repression_pressure, elite_splits`; default 0 | dataclass; clamp | stored `state.collective_infrastructure` | JSON codec; derived; flow; attention; topology/boundary |
| `update_collective_infrastructure` | `v3/systems/infrastructure.py:10-46` | `events_this_year[].infrastructure_deltas`; annual cap 15 | sum per field, cap, add, clamp | `state.collective_infrastructure.*` | `run_one_year` via `_run_practice_and_infrastructure` (`yearly_step.py:160-163`) |
| Event source | `v3/engine/event_engine.py:90-94` | deterministic pseudo-random seed | one flavour emits only `network_density`/`org_discipline` deltas | `events_this_year` | infrastructure update |
| Derived use | `v3/core/derived.py:239-256,259-269` | `network_density`, `org_discipline` | `alignment_vector += network*15 + discipline*10`; `health_level += network*10` | derived indices | stability/alignment |
| Attention use | `v3/systems/attention.py:33-62` | `org_discipline`, `network_density` | caps `attention_field_exposure` (discipline/network as negative weights) | `intensity_and_capture.attention_field_exposure` | event plausibility/score |
| Flow use | `v3/psyche/flow.py:366-403` | `social_support`, `network_density`, `repression_pressure` | conductance bonus/penalty for selected channels | trace conductance | pressure-flow |
| Topology/boundary | `v3/systems/topology.py:18-43`; `v3/systems/boundary.py:36` | thresholds on network density/repression | loop topology / boundary transitions | `peak_routing` | later steps |
| Initialisation | `v3/io/identity_to_backbone.py` | — | **no `collective_infrastructure` seeding**; all fields stay 0 | default 0 | first year |

**Unconsumed fields.** `resource_pool` and `elite_splits` are written by `infrastructure.py` and serialized, but no non-test consumer was found. They are dead in the current historical path. `collective_infrastructure` is not in the LLM Pass-1 summary and is not in the persona sheet.

## 2. What this actually models, and what it does not

The code models a **small set of aggregate social-surface scalars** at yearly grain:

- `network_density`: how dense the actor's network is;
- `org_discipline`: how disciplined an organisation is;
- `resource_pool`: a resource quantity (write-only);
- `repression_pressure`: repression (also duplicated by `field.repression_baseline`);
- `elite_splits`: elite fragmentation (write-only).

It does not model:

- actual institutions, organisations, workplaces, unions, churches, schools, clinics or parties;
- actual members, offices, rules, resources, access rights or sanctions;
- which other actor can help, hire, shelter, police or exclude;
- concrete solidarity, duty, betrayal, repression or collective action;
- the difference between “no network” and “unknown network”.

`network_density=0`, `org_discipline=0`, `resource_pool=0` are missing-data defaults, not observed absence. The mechanical event sampler can nudge the first two; it cannot create an institution or a participant.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N06 activity/time/stages/social reproduction | `INFRASTRUCTURE_ONLY` | aggregates exist; no actual institutions, participation, schedules or reproduction |
| N07 independent others/power/love | `MISSING` core; `INFRASTRUCTURE_ONLY` surface | no other actor, institution, access or sanction |
| N12 actual C12 person | `INFRASTRUCTURE_ONLY` / `UNKNOWN` | no current C9/C12 consumer |
| N01/N09 | none | not a need/motive or memory mechanism |

**Disposition: ADAPT.** Keep the explicit infrastructure **surface** and its derived readings. Replace 0-as-unknown. Bind every field to source-qualified generated institutions/networks/actors, or mark it unknown. Delete or justify `resource_pool`/`elite_splits` if no consumer is intended. Do not let an internal aggregate produce solidarity/power as a psyche bonus.

## 4. Harmful defaults / defects to remove

1. **All-zero default = no infrastructure.** Unknown must be typed.
2. **No institution/actor identity.** No stable entity IDs, members, rights, resources or actions.
3. **`resource_pool` and `elite_splits` are write-only.**
4. **Repression duplication.** `collective_infrastructure.repression_pressure` and `field.raw["repression_baseline"]` are separate sources with no declared relation.
5. **Mechanical event deltas** are not collective action or institutional change.
6. **No co-care/collective care** and no network substitution (an aunt, neighbour, clinic, school).
7. **No current consumer** beyond derived/attention/flow.

## 5. Proposed typed seam (nonissuing)

```text
InstitutionRuntime {
  institution_id; kind; members[]; rules/rights; resources; offices;
  access_conditions; sanction_capacity; source_refs; clock; rule_version;
}
NetworkTie {
  actor_id; other_actor_id/institution_id; tie_kind; reciprocity;
  actual_support_events[]; cost; access; source_refs; clock;
}
InfrastructureEvidence {
  actor_id; institution/tie refs; network_density_evidence;
  repression_evidence; resource_evidence; unknown_fields[];
}
```
The evidence record is derived from actual institutions/ties. The C9/C12 consumer reads **access and feasible participation**, not a network-density scalar. `network_density` may remain a convenience view if it has a registered dependency and source.

**Owner:** SDTF/world/ADP019 for institutions and other actors; CAN010/CAN011 for actor participation; C9/C12 for consumer. **Not issued by X05.**

## 6. Counterexamples and hostile alternative

**Counterexample (zero vs unknown).** An isolated rural actor with no formal organisations and an urban actor whose institutions were not queried both start at 0. The old code cannot distinguish these; a later C9 event about a union or clinic should.

**Counterexample (network density without a network).** Two actors have `network_density=80`; one has a real union and one has a label injected by an event. The old code cannot tell them apart; the persona micrograph only maps magnet labels.

**Hostile alternative.** The observed alignment/attention difference may be produced by `social_support` or by the LLM narrative, not by infrastructure. A hostile test holds social support/field fixed, varies only `network_density`, and checks a semantic later read; if nothing changes, the aggregate is inert.

**Falsifier.** If adding a real institution/tie to the world changes a later C9 access/action, while changing only `network_density` does not, the aggregate is not the mechanism. If the reverse, the consumer is reading a policy scalar.

## 7. Tests and limits

- Historical test: `v3/tests/test_step_logic.py:164-174` (event deltas to network density/org discipline). It tests arithmetic only.
- **NOT_RUN:** full old suite; current C9/C12; native person.
- **No native rule or source permission is issued.**

**Required future reviewer:** independent V3 source/consumer reviewer for M12/N06/N07; SDTF/world/ADP019 owner for institutions/networks; current C9/C12 implementer. X05 does not self-adopt.
