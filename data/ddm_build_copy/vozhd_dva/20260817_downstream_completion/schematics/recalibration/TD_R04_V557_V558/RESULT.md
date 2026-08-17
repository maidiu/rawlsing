# TD-R04 — V557/V558 Terminal-Demand Architecture Recalibration Result

## 0. Court identity and verdict

- **Worker:** TD-R04
- **Branch:** `agent/vozhd-dva-td-r04-v557-v558-recalibration`
- **Exact base:** `e4689b25c10753ce832f02486ad0fee5b70f9ad1`
- **Mode:** architecture only
- **Production implementation:** none
- **Binding law:** accepted TD-R00 V553, TD-R01 V554, TD-R02 V555, TD-R03 V556 and their integration rulings; terminal-demand envelope; architecture-pass law; banked runtime-prior-resolution exploration.

### Verdict

Current/Wave-0 V557 and V558 are **not terminal-demand sufficient**. They contain useful fail-closed/governance machinery, but their current semantic shapes are superseded.

The replacement architecture is:

```text
producer-owned mixed semantic DAG
  V552 refs
  V553 temporal authority
  V554 affordances/applicability
  V555 canonical atomic route edges
  V556 governed interactions/topology
        ↓
V557 lossless runtime publication + item-use/epistemic governance
        ↓
V558 immutable stage-agnostic StructuralPriorRepository
     + deterministic read-only ContextResolver
        ↓
ResolvedStructuralContext + SelectionRecord + CoverageFidelityProfile
        ↓
stage-blind V3 developmental runtime
```

**V557 owns no new domain-semantic family.** It owns preservation, admission/use governance, epistemic separation, referential-closure proof, manifests/hashes and the runtime-publication boundary.

**V558 owns no replacement producer-domain family.** It owns repository/link/index publication plus the deterministic resolver interface at V558→V3.

**No V559 is justified.** Dynamic resolution is a V558→V3 boundary function, not a third independent semantic jurisdiction.

---

## 1. Binding producer law

| producer | binding canonical meaning | terminal invariant |
|---|---|---|
| V553 | `TEMPORAL_KEY`, `TEMPORAL_OBSERVATION`, `TEMPORAL_RELATION`, `TEMPORAL_LIMIT / NEGATIVE_AUTHORITY`, exact governed structural refs | evidence time and negative authority remain V553-owned; no runtime proxy selection/interpolation inside V553 |
| V554 | `BOUNDED_STRUCTURAL_AFFORDANCE`, `STRUCTURAL_MEDIATION_APPLICABILITY_CONDITION`, V554→V555 handoff | applicability is structural possibility; runtime actor position is not generated here |
| V555 | `STRUCTURAL_MEDIATION_ROUTE_CANDIDATE`, route condition, V555→V556 handoff | **V555 route ID is the canonical atomic graph-edge identity**; no downstream re-ID |
| V556 | `STRUCTURAL_PRESSURE_INTERACTION_RELATION`, `STRUCTURAL_ATTRACTOR_PREREQUISITE_TOPOLOGY`, V556→V557 handoff | higher-order topology remains V556-owned; V555 route IDs remain base edges; no relation inference from coexistence |

The runtime graph is therefore **mixed-producer by design**. Runtime convenience never licenses serial semantic re-ownership.

---

## 2. Current/Wave-0 terrain verdict

### V557

Current completion-grade V557 is a renderer-oriented boundary packet. Its central projection reduces V556 inputs to `slot_name`-keyed rows. That is structurally insufficient because slot labels cannot carry:
- canonical V555 route identity;
- V556 interaction participant roles/order;
- V556 attractor-prerequisite topology;
- direct V552/V553/V554/V555 authority refs.

Its source/generated/rendered separation, no-dialogue/no-voice/no-autobiography restrictions, fail-closed checks, manifests and audits are worth retaining as **operational/governance mechanics**, not as the primary semantic shape.

Current prompt-shape aggregation also contains a defect: existence of an audit row is aggregated as if it meant existence of a violation, so a clean baseline row can become a blocker. Repair the aggregation; do not infer violation from row presence.

### V558

Current V558 is primarily a runtime-input/readiness gate. It normalizes statuses, governance prose and global flags rather than publishing the mixed-producer structural prior graph. It therefore cannot yet be the stage-blind V3 prior repository.

There is also a producer-consumer shape mismatch: V558 expects fields such as thin-path `future_consumer_notes` / `app_wiring_boundaries` that completion-grade V557 does not canonically emit. Those prose fields must not become semantic dependencies.

Current global epistemic flags are insufficient. Runtime authority must be item-level.

### Duplicate authority surfaces

Thin/scaffold and completion-grade V557/V558 paths expose competing semantic-ish payloads. Terminal implementation must leave one canonical contract per stage; thin/smoke paths become compatibility/test facades only.

**Current/Wave-0 verdict:** `SUPERSEDED_TERMINAL_DEMAND_RECALIBRATION_REQUIRED`.

---

## 3. Fourteen-question terminal-demand answer set

| # | question | combined boundary answer | V557 | V558 / Resolver |
|---:|---|---|---|---|
| 1 | Nine-strata field | preserve every governed finite-stratum/position ref; never infer actor occupancy | admit/preserve exact refs and item permission | index native stratum/position requirements; missing actor binding → `UNBOUND_REQUIRES_RUNTIME_POSITION` |
| 2 | Relational direction | source/target/direction, simultaneous pressure/counter-pressure and contradiction remain structured | reject slot/prose flattening and broken ref closure | retain V555 route participants and V556 F1/F2 roles/order/topology; no inferred interactions |
| 3 | Time | preserve V553 evidence time/gaps/limits/noncomparability; select query-relative anchors deterministically | preserve temporal authority; bind explicit proxy eligibility | direct → latest prior → earliest post → no anchor; no default interpolation |
| 4 | Mediation | structural mediation possibility survives without becoming realized history | preserve V554 affordances and V555 routes/conditions | evaluate only governed predicates against supplied bindings; V3 realizes history |
| 5 | Orientation-to-strata | prerequisites survive; actor orientation remains downstream | preserve stratum/position refs and conditions | Phase B re-query after V3-generated bindings; resolver does not create orientation |
| 6 | Absolute Horizon | governed AH remains distinct from finite stratum/religiosity | preserve exact AH refs/limits/use state | index/return AH as distinct logical context; never infer it from labels |
| 7 | Pressure-flow | V555 routes remain base edges; V556 owns higher-order topology; V3 realizes actual flow | preserve canonical route IDs + V556 topology | query exact graph objects; never replace with `route_axis_*` or slots |
| 8 | Attractors | multiple historically conditioned prerequisite pathways remain possible; no final type inference | preserve V556 F2 participant structure and valid-empty state | return applicable/deferred prerequisite topology; never assign final Enneagram/personality |
| 9 | Vitality/organism | structural pressure is not actor need/desire/vitality | epistemic/use governance prevents category collapse | context remains structural; V3 owns organism state and realized response |
| 10 | Genealogy | recursive parent/partner/child generation queries same repository without pre-generating biography | preserve temporal/geographic priors and limits needed later | ordinary Phase A/B resolution for parent development, encounter, household, child |
| 11 | Epistemic separation | source evidence, structural prior, resolver context, generated fact and rendered expression stay distinct | owns runtime-publication epistemic/use governance | preserves class in repository/context/ledger; generated bindings remain separate runtime facts |
| 12 | Negative authority | absence, uncertainty, noncomparability, valid-empty and forbidden inference remain first-class | publish typed negative/empty states and never widen permission | enforce them during selection; return typed absence instead of zero/neutral guesses |
| 13 | DAG reuse | original authoritative objects remain reachable through stage-agnostic locators | publish exact producer IDs/hashes/ref closure | link/index without semantic re-ID; V3 never fetches raw stage files |
| 14 | No-starvation | every primary object protects a terminal capability; objects without a proof are excluded | object governance, collection state and publication manifest are independently necessary | repository, locators, indexes, resolver, replay, fidelity and refresh are independently necessary |

All fourteen questions have a lawful path without inflating V557/V558 into actor-generation stages.

---

## 4. Jurisdiction and semantic-family verdicts

### V557

**Domain-semantic-family verdict: NONE.**

V557 is nevertheless a justified logical stage because runtime publication is a distinct authority question: which exact producer-owned objects are admitted, under what item-level use/epistemic/proxy permissions, with what immutable closure and provenance?

Canonical V557 boundary objects:

1. `RUNTIME_AUTHORIZED_OBJECT_RECORD`
   - authoritative collection/object ID/hash;
   - producer build/schema/version refs;
   - producer permission;
   - narrowed V557 item-use state;
   - epistemic class;
   - proxy-eligibility rule refs where applicable;
   - negative/uncertainty/noncomparability refs;
   - admission/denial reason.

2. `RUNTIME_AUTHORIZED_COLLECTION_MANIFEST`
   - collection kind and producer;
   - schema/compiler/build/hash identity;
   - object count;
   - `VALID_NONEMPTY`, governed valid-empty, denied, missing-authority, integrity/version state;
   - item-governance completeness;
   - referential-closure status.

3. `V557_V558_RUNTIME_PUBLICATION_HANDOFF`
   - immutable publication bundle identity;
   - collection/object manifest hashes;
   - governance/policy versions;
   - referential-closure audit refs;
   - publication content hash.

V557 permission is **monotone-narrowing**: producer permission ≥ V557 permission. V557 may deny or narrow; it may not invent new causal permission.

### V558

**Producer-domain semantic-family verdict: NONE.**

V558 owns stage-agnostic repository/publication interface objects:
- immutable `StructuralPriorRepository`;
- collection registry;
- object locator index;
- reference graph;
- temporal/geographic/stratal/position/negative/provenance indexes;
- resolver-policy binding.

Dynamic boundary products:
- `ContextQuery`;
- `ResolvedStructuralContext`;
- `SelectionRecord`;
- `CoverageFidelityProfile`;
- deterministic next-context-change metadata.

Those are interface/resolution objects, not replacement structural ontology.

---

## 5. Multi-producer preservation architecture

Forbidden:

```text
V555 route
→ re-ID as V556 edge
→ flatten to V557 slot
→ normalize to V558 status
```

Required:

```text
V555 route R17 ───────────────┐
V555 route R22 ───────────────┤
V556 interaction I4(R17,R22) ┤
V556 topology T3(R17,R22,I4) ┤
V554 affordance/condition refs│
V553 temporal/limit refs ─────┤
V552 fact/position refs ──────┘
             ↓ exact locators + item governance
       V557 authorized publication
             ↓
       V558 repository linker/indexes
```

No later layer acquires semantic ownership of R17, R22, I4 or T3.

### Referential closure

V557 must prove that every runtime-published object can reach every authoritative dependency required to interpret it, including where applicable:
- V555 route participants of V556 F1/F2;
- V556 F1 participants of F2;
- V554/V555 conditions;
- V553 temporal keys/observations/relations/limits;
- V552 structural facts/positions;
- finite-stratum/native-geography refs;
- Horizon/AH refs;
- rule/predicate/negative-authority refs.

A dependency may remain context-only/audit authority even when not active-causal. If an indispensable semantic dependency is missing/corrupt, the dependent object is not runtime-admissible.

### Identity law

V555 route ID remains canonical graph-edge identity. V558 may create a nonsemantic lookup alias such as `hash(collection_kind, authoritative_object_id, authoritative_object_hash)`, but that alias never replaces the route ID.

V556 n-ary relation cardinality, participant roles/order and F2 motif structure must remain structured. Index projections may aid lookup; they may not become the authority of record.

---

## 6. Immutable `StructuralPriorRepository` contract

```text
StructuralPriorRepository {
  repository_bundle_id,
  repository_schema_version,
  publication_policy_version,
  resolver_policy_version,
  source_publication_manifest_hash,
  source_build_manifest_hashes[],
  collection_registry,
  object_locator_index,
  reference_graph,
  temporal_indexes,
  geographic_indexes,
  stratal_indexes,
  position_requirement_indexes,
  negative_authority_index,
  provenance_index,
  collection_fidelity_manifest,
  repository_content_hash
}
```

A new producer build, V557 authorization decision, policy binding or repository material produces a new immutable bundle. Existing bundles never mutate.

### Logical collection map

| logical collection | semantic owner | V558 role |
|---|---|---|
| structural facts/positions | V552 / accepted upstream owner | locate/index/reference |
| temporal key/observation/relation/limit | V553 | locate/index/select under resolver law |
| bounded affordance/applicability condition | V554 | locate/index/evaluate governed predicates |
| route candidate/route condition | V555 | locate/index; route ID stays canonical edge |
| interaction relation/attractor-prerequisite topology | V556 | locate/index; preserve participant topology |
| Horizon/AH refs where governed | accepted upstream owner | locate/reference only |
| uncertainty/absence/noncomparability/forbidden-use authority | owning producer | locate/index/enforce |

### Object locator

```text
ObjectLocator {
  locator_id,
  logical_collection_kind,
  authoritative_object_id,
  authoritative_object_hash,
  authoritative_producer_family,
  authoritative_build_id,
  repository_bundle_id,
  storage_locator,
  provenance_locator
}
```

`locator_id` is lookup infrastructure, not a new semantic ID.

### Reference graph

V558 materializes stage-agnostic **reference arcs**, not new domain edges. Examples:
- V556 topology → V555 routes/V556 relations;
- V555 route → V554 affordance/conditions;
- V554 affordance → V553/V552 authority;
- V553 observation → temporal key/governed structural refs.

### Index law

Indexes may project already-authorized fields for deterministic lookup:
- time/support;
- native geography;
- finite stratum;
- position requirement;
- relation/route/topology participants;
- applicability predicates;
- negative authority;
- epistemic/use class/provenance.

Every result remains reversible to authoritative object ID/hash and full producer semantics.

### Standalone publication

A completed V558 bundle must resolve with raw V553–V556 stage directories absent. Any hidden `latest_v553_root`, stage-file discovery or raw survey read is a boundary failure.

---

## 7. Item-level epistemic/use governance

### Epistemic classes

At minimum distinguish:
1. `SOURCE_EVIDENCE`;
2. `DERIVED_STRUCTURAL_PRIOR`;
3. `NEGATIVE_OR_LIMIT_AUTHORITY`;
4. `RESOLVER_DERIVED_CONTEXT`;
5. `GENERATED_RUNTIME_FACT`;
6. `RENDERED_EXPRESSION`.

Repository authority contains lawful structural/source/negative objects. Resolver output is class 4. V3-generated positions/history are class 5 and return only as explicit query bindings. Dialogue/voice/persona are class 6 and never causal structural authority.

### Item-use states

At minimum:
- `ALLOW_ACTIVE_CAUSAL_CONTEXT`;
- `ALLOW_CONTEXT_ONLY`;
- `ALLOW_REVIEW_ONLY`;
- `DENY_CAUSAL_USE`;
- `NOT_APPLICABLE`.

A healthy stage/global build cannot override an individual denied item. No global readiness boolean may substitute for item permission, uncertainty or negative authority.

Runtime permission remains monotone:

```text
producer permission ≥ V557 publication/use permission ≥ resolver query-relative permission
```

---

## 8. `ContextQuery` and resolver ownership

Minimum deterministic query:

```text
ContextQuery {
  repository_bundle_id,
  query_time,
  query_time_granularity,
  geographic_path,
  generation_subject_ref,
  developmental_or_generation_phase,
  generated_position_bindings[],
  generated_relationship_bindings[],
  household_or_family_bindings[],
  requested_prior_kinds[],
  query_purpose,
  resolver_policy_version
}
```

Each generated binding carries binding kind, generated runtime-fact ID, effective time and any authoritative structural-position ref. The resolver consumes bindings; it never fabricates them.

`ContextResolver` belongs to the **V558→V3 boundary jurisdiction**. It may be packaged inside the V558 library or as a separately importable read-only module, but no V559 is needed.

For fixed bundle/query/policy/bindings it must be pure and deterministic: no wall-clock dependence, randomness, filesystem order, mutable `latest` pointers, hidden network/raw-stage reads or LLM inference.

The resolver may locate candidates, enforce item permission/negative authority, select lawful temporal anchors, match native geography, evaluate producer-governed predicates against supplied bindings, defer unbound items, and emit replay/fidelity/refresh metadata.

It may not invent actor positions/history, synthesize V556 interactions, interpolate by default, infer Enneagram/personality or transform structure into dialogue/autobiography.

---

## 9. Temporal proxy eligibility, selection, tie and no-anchor law

V553 owns evidence time. V557 governs runtime proxy eligibility. V558 selects among lawful candidates for a query.

### Required modes

- `DIRECT_TEMPORAL_SUPPORT`;
- `LATEST_PRIOR_OBSERVATION_PROXY`;
- `EARLIEST_POST_QUERY_PROXY`;
- `EARLIEST_POST_BIRTH_ANCHOR` retained as a typed specialization of earliest-post selection;
- `NO_LAWFUL_TEMPORAL_ANCHOR`.

### Direct support

Direct support exists only when producer-governed support contains the query time at the declared granularity. A 1994 point observation is not silently a 1992–1998 interval. A genuine producer-declared interval may support its declared interval.

### Explicit proxy authority

Chronological proximity is not authority. A governed registry must specify, per eligible object/semantic-key family:
- prior-proxy allowed?;
- forward-proxy allowed?;
- eligible query phase/purpose;
- maximum lag or explicit no-cap token;
- negative-authority precedence;
- rule/version ID.

If no matching rule exists, proxy use is missing authority/denied. Direct support may still be used when independently lawful.

### Deterministic precedence

For each governed temporal semantic key at query time `T`, after permission/negative/noncomparability filtering:
1. all lawful `DIRECT_TEMPORAL_SUPPORT` candidates;
2. else lawful prior candidates at the greatest governed support endpoint/observation time `< T`;
3. else lawful forward candidates at the least governed support start/observation time `> T`, **only when explicitly authorized**;
4. else `NO_LAWFUL_TEMPORAL_ANCHOR`.

No default interpolation.

`EARLIEST_POST_BIRTH_ANCHOR` is the reporting specialization used when a birth/developmental precoverage query lawfully selects the earliest post-query proxy. It is not a competing precedence algorithm.

### Tie/collision law

Lexicographic ID order may stabilize serialization, never semantic precedence.
- If equal-rank multiplicity is lawful, return the complete tied set in canonical stable order.
- If one winner is required and no governed precedence distinguishes the candidates, fail closed with `AMBIGUOUS_EQUAL_RANK_AUTHORITY` and no active winner.
- Only exact same authoritative ID + hash storage duplicates may deduplicate.

### Proxy metadata

Every proxy SelectionRecord preserves:
- query time;
- producer evidence/support start/end;
- selected observation time;
- signed and absolute lag;
- prior-staleness or forward-anchor lag;
- proxy rule ID/version;
- lag-ceiling status;
- `historical_observation_at_query_time=false`.

Future proxy evidence remains future evidence. Any relation/metadata whose basis depends on evidence after query time belongs in `explanatory_only_temporal_metadata` unless separately authorized as causal at that time.

Once direct/prior coverage exists, it outranks ordinary forward proxy. Forward proxy after coverage begins requires explicit exceptional authority.

A proxy never means that the actor or parent personally held the measured belief.

---

## 10. Geography and progressive position binding

Higher-stratum priors may apply at their **native stratum** to a subject located within that scope. They may not be relabeled downward. A national Lebanon prior can bear on a person in Tyre as national context; it cannot become a Tyre-local estimate.

Before a generated actor position exists, a conditioned prior is:

```text
UNBOUND_REQUIRES_RUNTIME_POSITION
```

The resolver never invents class, sect, party, household, family, institution, occupation or Self position. Geography, labels, coexistence and prevalence are not substitutes.

If Phase A needs population/position distributions, those require an actual governed producer. Missing authority stays `MISSING_AUTHORITY`.

### Two-phase initialization

**Phase A:** query with time, geography, generation/development phase and already-known environment/relationships. Return unconditional lawful priors and typed unbound position-conditioned objects.

**V3/genealogy:** generate lawful actor positions, relationships, household/institution/occupation state and realized history as `GENERATED_RUNTIME_FACT`.

**Phase B:** re-query the **same repository bundle** with those generated bindings. Newly applicable V554/V555 conditions may resolve; V556 topology may become relevant according to producer conditions. SelectionRecords identify which generated binding caused applicability.

No repository mutation occurs. Phase B produces a new resolved context, not retroactive producer evidence.

---

## 11. `ResolvedStructuralContext`, replay, fidelity and refresh

### Resolved context

```text
ResolvedStructuralContext {
  resolved_context_id,
  repository_bundle_id,
  context_query_id,
  resolver_policy_version,
  generation_subject_ref,
  query_time,
  geographic_path,
  developmental_or_generation_phase,
  applied_generated_bindings[],
  active_structural_priors {
    structural_facts[], temporal_authority[], bounded_affordances[],
    mediation_routes[], pressure_interactions[],
    attractor_prerequisite_topologies[], horizon_or_AH_context[]
  },
  applicable_conditions[],
  deferred_unbound_objects[],
  context_only_objects[],
  review_only_objects[],
  negative_authority_and_limits[],
  explanatory_only_temporal_metadata[],
  selection_record_ids[],
  coverage_fidelity_profile,
  next_context_change,
  context_content_hash
}
```

Active routes retain V555 IDs. V556 relations/topology retain exact IDs and participant refs. No `slot_name`/prose/status substitute is sufficient.

### `SelectionRecord`

Emit one record for every considered candidate, selected **or rejected/deferred**, including:
- bundle/query/policy IDs;
- semantic resolution key;
- object locator + authoritative ID/hash;
- epistemic/use state;
- decision;
- temporal mode/specialization/evidence times/lag/proxy rule;
- native geography/stratum;
- required and matched generated bindings;
- tie group/rank/outcome;
- negative-authority refs;
- rejection/deferral reason;
- provenance refs;
- record hash.

Minimum decisions include selected active/context-only/explanatory-only; deferred unbound; rejected permission/not-applicable/temporal-rank/proxy-not-authorized/negative-authority/noncomparable/geographic-scope/ambiguous-tie.

The same bundle + query + policy + bindings must reproduce the same canonical selection semantics without raw stage reads.

### `CoverageFidelityProfile`

Descriptive dimensions, not a universal readiness score:
- candidate/selected/rejected/deferred counts by collection;
- temporal mode counts;
- signed/absolute proxy-lag distribution;
- direct-support fraction;
- native geographic-scope and finite-stratum coverage;
- unbound-position counts by binding kind;
- V555 route and V556 relation/topology coverage;
- valid-empty/missing-authority/noncomparability/negative counts;
- active/context/review/deny counts;
- provenance/hash verification;
- temporal observation/support density where meaningful.

Any later aggregate score is diagnostic only and cannot gate semantics.

### Refresh / next-context-change

Repository bundles are immutable. Context changes by re-resolution when:
- query time crosses a known support/observation/limit/relation boundary;
- geography changes;
- generation/development phase changes where predicates depend on it;
- generated position, household, family, relationship, institution or occupation binding changes;
- governed applicability facts change;
- repository or policy version changes.

`next_context_change` may name only deterministic known repository boundaries or caller-supplied planned inputs. It must not predict future generated relationships/positions.

New producer evidence creates a new V557 publication and V558 bundle; old bundle/context remain replayable.

---

## 12. Genealogy / precoverage and ordinary runtime proofs

### Earlier-born parent

Parent born before coverage:
1. query parent developmental context by known time/geography;
2. if no direct/prior anchor, use `EARLIEST_POST_BIRTH_ANCHOR` only when explicit forward-proxy authority exists;
3. preserve future evidence time and lag;
4. otherwise return `NO_LAWFUL_TEMPORAL_ANCHOR`;
5. leave class/sect/party/etc conditioned priors unbound;
6. V3 generates parent positions/history;
7. Phase B re-resolves same bundle;
8. later direct/prior observations supersede the early future proxy under ordinary precedence.

Encounter/partner relationship and household formation are V3-generated facts, not repository assertions. Once generated, they become query bindings. Child generation/development then queries the same repository plus generated family history. Structural priors never become “the father believed X.”

**Genealogy/precoverage verdict: PASS as ordinary architecture**, conditional on explicit forward-proxy authority where such a proxy is used.

### Ordinary 1980s/1990s target person

Reference target born 1988 with known country/region. Repository has one genuine 1987–1989 direct-support national interval and another key observed at points 1985 and 1990, plus position-conditioned V554/V555 objects and governed V556 topology.

Phase A must:
- select the interval as `DIRECT_TEMPORAL_SUPPORT` at national native scope;
- use 1985 as latest-prior proxy for the second key only if explicit prior-proxy authority permits it;
- not prefer 1990 merely because it may be numerically closer;
- return class/sect-conditioned objects unbound;
- preserve V555/V556 identity/topology without realizing actor flow.

After V3 generates positions, Phase B re-query may activate lawful conditioned routes/topology. No selected prior becomes an actor belief or final type.

---

## 13. Stage-blind V3 consumer proof

Forbidden V3 behavior:

```text
open v553_* / v554_* / v555_* / v556_* files
if producer_stage == ...
```

Lawful behavior:

```text
repository = StructuralPriorRepository.open(bundle_id)
context_a = ContextResolver.resolve(repository, query_a)
# V3/genealogy generates lawful runtime facts
context_b = ContextResolver.resolve(repository, query_b_with_generated_bindings)
```

V3 consumes logical structural collections and exact object locators. Provenance may remain inspectable, but behavior cannot depend on stage filenames or stage discovery.

Completion proof: run the reference consumer with raw producer stage directories unavailable. Identical queries over the same standalone bundle must resolve identically.

---

## 14. Boundary verdicts

### V557→V558

Required handoff:
- exact admitted producer material/locators;
- collection/object IDs/hashes/schema/build identity;
- item epistemic/use/proxy governance;
- transitive semantic reference closure;
- valid-empty/negative/missing-authority state;
- policy/governance versions;
- immutable publication manifest hash.

V558 verifies hashes, ID uniqueness, closure, no duplicate V555 route identity, V556 topology preservation, item-governance completeness and version compatibility. Partial/corrupt publication fails closed.

**Current boundary:** FAIL / superseded.  
**Terminal-demand architecture:** PASS.

### V558→V3

Required product:

```text
StructuralPriorRepository + ContextResolver + ContextQuery
→ ResolvedStructuralContext + SelectionRecord + CoverageFidelityProfile
```

Explicitly excluded: raw survey rows, raw stage files, final traits/Enneagram, dialogue/voice/autobiography, invented positions, geographic down-imputation, default interpolation.

**Current runtime-input-gate shape:** FAIL / superseded.  
**Terminal-demand stage-blind boundary:** PASS.

---

## 15. Component/artifact/publication target

### V557 canonical target

- `RUNTIME_AUTHORIZED_OBJECT_RECORD`
- `RUNTIME_AUTHORIZED_COLLECTION_MANIFEST`
- `V557_V558_RUNTIME_PUBLICATION_HANDOFF`
- referential-closure audit
- item-use/epistemic/proxy-governance manifest
- immutable publication content hash

Prompt/render audits may remain operational sidecars but are not V557 domain semantics.

### V558 canonical target

Immutable bundle components:
- repository manifest;
- collection registry;
- object locator index;
- reference graph;
- temporal/geographic/stratal/position indexes;
- negative-authority and provenance indexes;
- fidelity manifest;
- immutable producer-object material or content-addressed closure sufficient for standalone use;
- resolver-policy version binding.

Runtime-facing library contracts:
- `ContextQuery`;
- `ContextResolver.resolve`;
- `ResolvedStructuralContext`;
- `SelectionRecord` ledger;
- `CoverageFidelityProfile`;
- next-context-change metadata.

Publication must be atomic/stale-safe: no partial build becomes a valid repository bundle.

---

## 16. Finite completion court and hostile cases

| case | required result |
|---|---|
| exact V555 route ID survives V557/V558 | PASS |
| V556 n-ary participant roles/order survive | PASS |
| V556 F2 topology retains exact V555/F1 refs | PASS |
| direct V552/V553/V554/V555 authority reachable from resolved route/topology | PASS |
| valid-empty V556 F1/F2 publishes as typed valid-empty | PASS |
| denied item inside healthy collection stays denied | PASS |
| point observation attempted as silent interval | FAIL CLOSED |
| latest prior vs ordinary future proxy after coverage | latest prior wins |
| forward proxy without explicit eligibility rule | `NO_LAWFUL_TEMPORAL_ANCHOR` / missing authority |
| equal-rank singular candidates without governed precedence | `AMBIGUOUS_EQUAL_RANK_AUTHORITY` |
| national prior queried from locality | may apply as national; no local relabel/imputation |
| missing class/sect/party binding | `UNBOUND_REQUIRES_RUNTIME_POSITION` |
| Phase B with generated binding | re-resolve same bundle and record binding cause |
| raw survey/category offered as actor trait | REJECT |
| structural prior offered as final Enneagram/personality | REJECT |
| rendered dialogue/voice offered as causal prior | REJECT |
| repository-only consumer with stage dirs removed | PASS |
| same bundle/query/policy/bindings repeated | deterministic replay-equivalent |
| clean prompt baseline row with zero violations | no false blocker |
| completion-grade V557→V558 without thin-only prose fields | PASS |
| changed producer evidence time/hash under same identity | FAIL CLOSED |
| duplicate/re-IDed V555 route edge in V558 | FAIL CLOSED |
| V556 topology flattened to slot/prose only | FAIL CLOSED |
| hidden raw-stage fetch during resolve | FAIL CLOSED |

### Hostile temporal-authority mutation

If a V553 observation ID is republished with changed evidence time without matching lawful producer hash/lineage, publication fails. If V557/V558 rewrites a point observation into a direct-support interval, the object fails authority verification. Old immutable bundles remain unchanged.

### Hostile geographic imputation

If only Lebanon-national authority exists and query subject is in Tyre, the national prior may be active at national scope. A synthetic `Tyre_local_value = national_value` is forbidden; local authority remains missing.

### Hostile position invention/persona leakage

If a condition requires working-class position but Phase A has no class binding, defer it. Do not infer class from geography, prevalence or labels. If structural priors/routes/topology are converted into “father believes X,” biography, voice or final Enneagram, reject as epistemic/jurisdiction violation.

---

## 17. Architecture checksum, no-starvation and no-bloat

| family | disposition |
|---|---|
| nine-strata identities/relations | `PRESERVE_BY_REFERENCE` |
| inter-strata pressure/counter-pressure | `PRESERVE_BY_REFERENCE` |
| source/target/direction | `PRESERVE_BY_REFERENCE` |
| temporal history/limits | V557 preserve; V558 resolver query-relative selection |
| contradiction/coexisting pressure | `PRESERVE_BY_REFERENCE` |
| mediation | `PRESERVE_BY_REFERENCE` |
| buffer/amplify/deflect/block | `PRESERVE_BY_REFERENCE` as V555 unary route semantics |
| governed cross-route reroute/interaction | `PRESERVE_BY_REFERENCE` as V556 only |
| orientation-to-strata | upstream/downstream reuse; resolver position-gated only |
| Absolute Horizon | `PRESERVE_BY_REFERENCE` where governed |
| pressure-flow topology | `PRESERVE_BY_REFERENCE` |
| attractor prerequisites | `PRESERVE_BY_REFERENCE` |
| actor developmental causality | `DOWNSTREAM_OWNS` — V3 |
| genealogy | `DOWNSTREAM_OWNS` — V3; resolver supplies context |
| V2 phenomenology/expression | `DOWNSTREAM_OWNS` |
| epistemic/provenance runtime governance | V557 `OWN_AND_DERIVE_HERE`; V558 preserves + records query decisions |
| uncertainty/absence/noncomparability | `PRESERVE_BY_REFERENCE` |
| temporal proxy eligibility | `MISSING_AUTHORITY` until governed runtime registry exists |
| query-relative temporal selection | V558 resolver `OWN_AND_DERIVE_HERE` |
| generated actor position | `DOWNSTREAM_OWNS`; V558 consumes binding only |

### Primary-component starvation proof

- Remove V557 object governance → item permission/epistemic/proxy authority disappears.
- Remove V557 collection manifest → valid-empty/integrity/version state disappears.
- Remove V557 closure audit → V556 topology can survive while required V555/V554/V553 meaning is lost.
- Remove V557 handoff hash → V558 consumes mutable/unfrozen publication.
- Remove V558 collection registry → V3 cannot discover logical collections stage-blindly.
- Remove ObjectLocator → authoritative ID/hash/replay reachability is lost.
- Remove reference graph → mixed-producer dependency traversal/topology closure is lost.
- Remove temporal/geographic/stratal/position indexes → deterministic bounded queryability is lost or hidden in stage-aware scans.
- Remove negative-authority index → denied/noncomparable/absence material can be silently bypassed.
- Remove ContextQuery → authority-relevant runtime inputs and policy become implicit/unreplayable.
- Remove ContextResolver → V3 must become stage-aware or duplicate selection law.
- Remove ResolvedStructuralContext → V3 receives raw repository complexity/prose instead of a typed causal-context boundary.
- Remove SelectionRecord → exact ranking/rejection/proxy/tie/binding replay is impossible.
- Remove CoverageFidelityProfile → gaps, proxy lag, valid-empty and unbound positions become invisible.
- Remove refresh contract → contexts become stale after time/location/generated-binding changes.

### No-bloat proof

Objects deliberately **not** created:
- V557 domain ontology;
- V558 replacement route/topology IDs;
- inferred population-distribution family;
- actor-position generation family;
- interpolation family;
- V559 stage;
- renderer prose as structural causal state.

V557 adds only the publication/governance jurisdiction necessary to prevent permission widening and information loss. V558 adds only repository/link/index and deterministic query-resolution machinery necessary for stage-blind consumption.

---

## 18. Implementation packet plan and current-code disposition

### V557 packets

1. **P1 mixed-producer admission/collection manifest** — exact collection/object identities, hashes, valid-empty/integrity state.
2. **P2 item epistemic/use/proxy governance** — producer permission binding, monotone narrowing, explicit proxy rules or missing authority.
3. **P3 referential-closure/lossless preservation court** — V555 edge uniqueness, V556 topology closure, earlier authority reachability.
4. **P4 canonical V557→V558 handoff** — immutable manifest/hash/policy versions.
5. **P5 completion/compatibility cleanup** — fix prompt aggregation, demote renderer audit, eliminate thin/completion competing authority.

### V558 packets

1. **P1 immutable repository linker** — collection registry, object locators, reference graph, bundle hash.
2. **P2 stage-agnostic indexes** — temporal/geographic/stratal/position/relation/topology/negative/provenance.
3. **P3 deterministic resolver** — query normalization, permissions, temporal law, native geography, progressive binding.
4. **P4 context/replay/fidelity/refresh contracts** — context, SelectionRecord, coverage profile, next-change.
5. **P5 stage-blind V3 reference consumer/completion court** — raw stage dirs absent; Phase A/B; genealogy/precoverage; hostile leakage tests; legacy gate consolidation.

### Current code: keep / repair / merge / demote / deprecate

**Keep:** fail-closed presence/version/hash checks; stale-safe/manifest/build-record mechanics; source/generated/rendered separation intent; no-dialogue/no-voice/no-autobiography restrictions; governance review guards.

**Repair:** prompt baseline aggregation; producer-consumer schema mismatch; item-level epistemic/use state; standalone immutable publication.

**Merge/consolidate:** thin and completion-grade authority surfaces into one canonical contract each for V557/V558.

**Demote:** prompt-shape/render audits and app-wiring governance prose to operational safety/completion sidecars.

**Deprecate/supersede:** slot-name projection; `route_axis_*` generic topology; readiness-score semantics; status-only normalized runtime input; global `generated_not_evidenced_flag`; generic handoff rows without producer object identity; thin-only prose fields as semantic dependencies.

No production implementation is authorized by this result.

---

## 19. Open missing authority

1. **Runtime publication/use-governance registry** beyond producer-native permission, specifying active/context/review/deny policy by governed object family/item condition.
2. **Runtime temporal proxy-eligibility registry** specifying prior/forward permission, eligible query phase/purpose, lag rule and negative-authority precedence. Until accepted, proxy use fails closed.
3. **Producer direct-support interval authority** where support broader than point/granularity is desired. Without it, point observations remain point/granularity support only.
4. **Phase-A actor-position population/distribution authority**, if ever required. None may be synthesized in V557/V558.
5. Inherited **finite-stratum / universal mapping / Horizon-AH authority** where upstream completion still lacks it.
6. Explicit **cross-scope interaction applicability** where V556 rule authority does not already provide it.
7. Upstream rule registries already identified by TD-R01–TD-R03 for V554 affordance generation, V555 routes and V556 interactions/topology.

These are dependencies or separate authorities, not permission for V557/V558 to re-own upstream semantics.

---

## 20. Unresolved Vozhd decisions

1. Freeze runtime-use and temporal-proxy governance as two logical registries (recommended) versus one physical registry with separate rule families.
2. Freeze `EARLIEST_POST_BIRTH_ANCHOR` as a specialization tag of `EARLIEST_POST_QUERY_PROXY` (recommended) rather than a separate precedence branch.
3. Preserve logical V557 authorization → V558 repository separation even if physically co-packaged in one library/deployment (recommended).
4. Select repository storage/index engine later; architecture requires deterministic immutable identity/replay, not a particular engine.
5. Permit producer/stage provenance as opaque audit metadata while keeping V3 behavior stage-blind (recommended).
6. Omit a canonical scalar fidelity score unless a dashboard explicitly needs one (recommended); typed dimensions are sufficient.

None requires launching V3 architecture or implementation in TD-R04.

---

## 21. Final architecture statement

### THIS STAGE/BOUNDARY IS RESPONSIBLE FOR

**V557**
- lossless mixed-producer runtime publication;
- item-level admission/use/epistemic/proxy governance;
- permission monotonicity;
- referential-closure proof;
- valid-empty/negative-authority preservation;
- immutable manifests/hashes and V557→V558 handoff.

**V558 / V558→V3**
- immutable stage-agnostic `StructuralPriorRepository`;
- producer-preserving object locators/reference graph;
- temporal/geographic/stratal/position/negative/provenance indexes;
- deterministic read-only `ContextResolver`;
- explicit temporal proxy selection/tie/no-anchor law under governed eligibility;
- native geographic-scope enforcement;
- progressive position binding and Phase A/B re-resolution;
- `ResolvedStructuralContext`, `SelectionRecord`, `CoverageFidelityProfile`, deterministic refresh/next-change;
- standalone stage-blind V3 consumer boundary.

### THIS STAGE/BOUNDARY IS NOT RESPONSIBLE FOR

- any new structural domain ontology merely because V557/V558 are numbered;
- re-IDing V555 routes or V556 relations/topology;
- inferring V556 interactions from coexistence;
- actor class/sect/party/household/family/institution/occupation/Self generation;
- invented Phase-A population distributions;
- producer evidence-time mutation or invented support intervals;
- default interpolation;
- geographic down-imputation;
- raw survey→actor trait/personality inference;
- structural prior→final Enneagram assignment;
- realized actor flow/attractor history/genealogy/biography;
- dialogue/voice/persona/autobiography as causal state;
- V2 expression;
- V3 implementation/architecture launch;
- V559 without a genuine independent jurisdiction proof.

### TERMINAL CAPABILITIES PROTECTED

- nine-stratum structural context;
- inter-strata pressure/counter-pressure and contradiction;
- temporal persistence/drift/rupture/gap/noncomparability authority;
- structural mediation and buffer/amplify/deflect/block semantics;
- canonical V555-edge pressure-flow graph plus nonflattened V556 topology;
- multiple attractor-prerequisite pathways without final-type inference;
- distinct Horizon/AH context where governed;
- two-phase initialization and progressive position binding;
- recursive parent/partner/child context resolution;
- source/prior/resolver/generated/rendered epistemic separation;
- item-level negative authority and forbidden inference;
- deterministic temporal proxy replay/fidelity accounting;
- stage-blind V3 consumption from an immutable standalone repository.

### OPEN MISSING AUTHORITY

- runtime publication/use rules beyond producer-native permission;
- temporal proxy-eligibility rules;
- broader direct-support intervals where desired;
- any lawful Phase-A population/position distribution producer;
- inherited finite-stratum/Horizon-AH mapping where missing;
- cross-scope applicability not already governed by V556;
- upstream V554/V555/V556 rule registries already banked by TD-R01–TD-R03.

---

## 22. Architecture-only verification

Verified against the exact assigned base terrain and binding upstream law:
- assigned branch exists at exact base `e4689b25c10753ce832f02486ad0fee5b70f9ad1` before result writes;
- TD-R04 assignment read fully;
- accepted TD-R00/01/02/03 results and V553/V554/V555/V556 integration rulings treated as binding;
- terminal-demand envelope, architecture-pass law and runtime-prior-resolution exploration cross-checked;
- Wave-0 R0-04/R0-05 used as evidence only;
- completion-grade and thin/scaffold V557/V558 terrain inspected for slot projection, topology loss, prompt aggregation, shape mismatch, status-only normalization, global epistemic flags and duplicate authority surfaces;
- no production code modified;
- no V3/V2 implementation launched;
- no V559 created;
- deliverable restricted to `RESULT.md` and `RESULT.json`.

Architecture-only verification status:

`PASS_ARCHITECTURE_ONLY_TERMINAL_DEMAND_RECALIBRATION`

Current/Wave-0 V557/V558 verdict: **SUPERSEDED**.  
V557 semantic-family verdict: **NO NEW DOMAIN-SEMANTIC FAMILY**.  
V558 object verdict: **IMMUTABLE REPOSITORY/LINKER/INDEX + RESOLVER BOUNDARY OBJECTS; NO PRODUCER-SEMANTIC RE-OWNERSHIP**.  
Genealogy/precoverage verdict: **ordinary lawful case under explicit proxy authority**.  
V557→V558 boundary verdict: **terminal architecture PASS; current shape FAIL/superseded**.  
V558→V3 boundary verdict: **terminal architecture PASS; current gate shape FAIL/superseded**.

**V557_V558_ARCHITECTURE_TERMINAL_DEMAND_READY = PASS**
