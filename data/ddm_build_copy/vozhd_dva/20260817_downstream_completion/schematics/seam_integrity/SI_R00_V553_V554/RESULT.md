# SI-R00 — V553→V554 Hostile Seam-Integrity Court

**Role:** seam-integrity Rabochii SI-R00  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-si-r00-v553-v554`  
**Exact base:** `e5bf198a59b561b4db2f092c115d7a6e5cbf562d`  
**Mode:** architecture/seam audit only; no production-code modification  
**Method:** original four-way seam method, hostile falsification of accepted TD-R00/TD-R01 hypothesis  
**Court verdict:** `HARDEN`

---

## 1. Executive finding

The accepted TD-R00 V553 and TD-R01 V554 architecture survives hostile seam-integrity review.

It does **not** survive unchanged as a statement about the present production implementation.

The present V553→V554 implementation seam contains multiple concrete behaviors that would violate the accepted terminal-demand law if allowed to remain canonical:

1. V552J retains a semantic-score fallback that can choose a V552 structural fact by scoped field overlap rather than by an already-governed exact association.
2. Present V553 invokes that resolver while building temporal keys, so an absent exact producer-bound association can become a reconstructed V553 association.
3. Present V553 groups rows by a comparable structural key and can average the `pressure_score` of multiple exact V552 structural facts into one wave/key value.
4. The grouped row retains one `source_v552_structural_fact_id` as the primary identity while relegating the full set to diagnostic JSON, which is insufficient for the accepted simultaneous-exact-pressure law.
5. Present V553 schemas do not yet expose the complete TD-R00 `GOVERNED_STRUCTURAL_REFERENCE_SET`, including role-qualified 0..n finite-stratum refs, separately governed generic-Horizon and Absolute-Horizon refs, full source/driver-position and target/receiving-position authority refs, inherited relation refs, or `reference_contract_version` as the canonical sparse spine.
6. Present V553 still contains interpolation, country-year pressure, score-derived component, rupture-candidate and related legacy surfaces that may exist only as secondary/non-authoritative compatibility material under the accepted architecture.
7. Present V554 is still the legacy `v0.1` seed contract: it constructs hard-coded seed classes, synthetic seed IDs, scalar readiness/strength/confidence composites and interpolation-conditioned seed readiness rather than the accepted immutable F1/F2/B1 model.

These are serious current-seam defects. They are **not proof that the accepted architecture must be reopened**, because the lawful producer terrain already exposes stable V552 fact identity, V552 temporal-key-source identity, V552J packet/join identity, admission/use-permission state and manifest/hash lineage. The accepted architecture can therefore be realized by removing/restricting illicit rematching and many-to-one semantic collapse, adding the frozen exact reference spine, and replacing the legacy V554 consumer with its already-accepted F1/F2/B1 contract.

No new semantic family, no new stage jurisdiction, and no change to the TD-R00/TD-R01 ownership split is required.

**Disposition:** preserve the accepted architecture, harden its implementation court and exact seam invariants before production release.

---

## 2. Court standard

This audit held four views simultaneously.

### A. Cumulative lawful upstream reality

The seam is not only whatever V553 copies into its own tables. V550–V552J retain producer-owned authority that later stages may reach directly through stable DAG references.

Material upstream capabilities presently include:

- fail-closed semantic/use authority distinctions in V550;
- V551 canonical signed-direction evidence and directionality authority separation;
- V552 stable structural-fact IDs, source artifact/row/hash lineage, measured pressure status/value, relation-axis/target/driver-facet identity and stable V552 temporal-key-source IDs;
- V552J stable join/packet identity, exact V552 fact and V552 temporal-source fields, admission/use permission, evidence state, source scope and producer manifest hashes.

The accepted architecture is therefore entitled to reference these producer-owned objects directly. It is not entitled to invent missing authority, infer absent finite-stratum/AH mappings, or reconstruct an association by descriptive similarity.

### B. Present V553 reality

Present V553 is a partially hardened legacy temporal-pressure implementation, not the frozen TD-R00 physical contract.

It already contains useful exact-ID and fail-closed work, but it also contains:

- a provisional `v0.2` schema family;
- canonical-harmonization compatibility machinery;
- semantic-score structural rematching through the imported V552J resolver;
- sparse-looking temporal keys whose grouping grain is still axis/target/driver/channel-or-Horizon/signature based;
- many-to-one wave/key aggregation over multiple source V552 facts;
- arithmetic mean pressure composition across those facts;
- score/readiness aggregates;
- interpolation/country-year surfaces;
- no complete physical `GOVERNED_STRUCTURAL_REFERENCE_SET` contract.

### C. Immediate V554 demand

Accepted V554 no longer needs a generic seed score or country-year interpolated pressure field.

It needs exact machine-addressable structural/temporal inputs from which it can lawfully construct:

1. `BOUNDED_STRUCTURAL_AFFORDANCE` (`F1`), positive immutable eligibility only;
2. `STRUCTURAL_MEDIATION_APPLICABILITY_CONDITION` (`F2`), machine-addressable requirements/limits/deferred bindings;
3. `V554_V555_HANDOFF` (`B1`), exact-reference boundary.

V554 must be able to reach exact V552/V552J/V553 and earlier producer authority without descriptive rematching and without treating V553 aggregate/interpolation artifacts as canonical structural meaning.

### D. Total Rawlsing terminal demand

The seam must leave later stages able to preserve or construct, in their own jurisdictions:

- the nine finite relational strata;
- downward/upward/lateral structural pressure;
- simultaneous and contradictory pressures;
- exact structural source/target/direction;
- temporal observation, relation, absence, noncomparability and limits;
- mediation and route conditions;
- Absolute Horizon as distinct from finite strata and generic Horizon material;
- V556 pressure-flow/interaction topology;
- V3 actor-specific position, exposure, orientation-to-strata, genealogy, development and attractor realization;
- epistemic separation among source evidence, structural prior, runtime fact and rendered expression;
- V2 phenomenology without upstream personhood fabrication.

The terminal requirement is preservation of lawful prerequisites, not expansion of V553 into later-stage semantics.

---

## 3. Read set and inspected present terrain

The court directly inspected, at the exact base SHA, at minimum:

### Governing architecture

- `TERMINAL_DEMAND_ENVELOPE.md`
- `ARCHITECTURE_PASS_LAW.md`
- `schematics/synthesis/RUNTIME_PRIOR_RESOLUTION_EXPLORATION.md`
- accepted TD-R00 `RESULT.md` / `RESULT.json`
- `integration/V553_COMPLETION_IMPLEMENTATION_RULING.md`
- accepted TD-R01 `RESULT.md` / `RESULT.json`
- `integration/V554_COMPLETION_IMPLEMENTATION_RULING.md`
- later accepted implementation rulings through:
  - V555
  - V556
  - V557/V558
  - V3

### Present V550–V554 seam implementation

- `ddm_v550_authority_contract.py`
- `ddm_v551_directionality_expectation.py`
- `ddm_v552_contract.py`
- `ddm_v552_structural.py`
- `ddm_v552j_schema.py`
- `ddm_v552j_handoff.py`
- `ddm_v553_schema.py`
- `ddm_v553_temporal_identity.py`
- `ddm_v553_canonical_harmonization.py`
- `ddm_v553_temporal_pressure.py`
- `ddm_v554_seed_contract.py`

### Present tests / earlier seam evidence

- `tests/test_postg5_v552j_v553_consumer_contract.py`
- `test_w06_v552j_join.py`
- `tests/vozhd_dva_wave0/test_vertical_continuity.py`
- `tests/vozhd_dva_wave0/vertical_continuity.py`
- earlier Wave-0 and seam architecture evidence where useful.

The court did not treat a prior architecture summary as proof of current behavior.

---

## 4. Upstream reality: what actually reaches the seam

### 4.1 V550 authority is richer than a semantic label

Current V550 authority code explicitly separates semantic classification from downstream permission.

It exposes distinct authority states and independent downstream-use gates, including a dedicated `allowed_as_temporal_pressure_indicator` permission. Directional applicability is derived from governing directionality authority rather than from row-level confidence or promotability.

**Seam implication:** V553 need not own or duplicate V550 semantic/use authority. It must preserve an exact reference to the governing object/decision whenever that authority is part of a temporal object's lawful basis.

### 4.2 V551 directionality is producer-owned structural evidence

Current V551 directionality coverage uses explicit response direction/intensity stamps and rejects incomplete directionality coverage.

That structural direction is not the same semantic class as V553's later temporal delta direction (`up/down/flat`).

**Seam implication:** V553 may preserve the V551/V550 structural-direction authority reference, but may never reconstruct it from a temporal delta.

### 4.3 V552 exposes stable fact and temporal-source identities

Current V552 constructs deterministic structural fact IDs (`v552sf__...`) and temporal-key-source IDs (`v552tks__...`). A structural fact also retains source artifact, source row identity/hash, pressure measurement provenance/status, relation axis, target entity and driver facet.

This is enough to anchor an exact V553 observation to a producer-owned measured fact without inventing a replacement fact identity.

V552's temporal-key-source object is lineage/candidate identity only; it is not itself cross-wave comparability authority.

### 4.4 V552J exposes a stable join surface — but also an illicit fallback

Current V552J join rows expose:

- `v552j_join_id`;
- packet identity;
- V552 fact identity;
- V552 temporal-key-source identity;
- relation/target/driver/channel/Horizon compatibility fields;
- join permission;
- allowed downstream use;
- V553 probe/temporal-field gating;
- source manifest hashes.

That producer-bound row can serve as exact association/admission/use lineage.

However, `_packet_structural_dimension_resolution` does not require a pre-existing exact association. When one is absent it can score in-scope V552 facts by overlap in relation axis, target, driver facet and question, accept partial structural matches, choose the highest-scoring fact as `primary`, and then publish that fact ID as the resolved source.

The tests expressly exercise this fallback. An in-scope candidate with a different question can still obtain sufficient score to become the chosen structural fact.

**Court finding:** the fallback may remain diagnostic/repair tooling, but it cannot be an authoritative path into canonical V553 under TD-R00.

---

## 5. Present V553 hostile findings

### 5.1 Exact identity exists, but exact identity is not yet the grouping invariant

Present `_v553_temporal_key_profile` carries `source_v552_structural_fact_id` in its basis metadata, but the structural/comparable temporal key itself is generated principally from:

- source;
- country;
- relation axis;
- target entity;
- driver facet;
- structural channel or Horizon constraint;
- semantic signature.

This can place more than one exact V552 fact into the same `comparable_temporal_key` group.

### 5.2 Present V553 performs a concrete many-to-one pressure collapse

In `_build_v553_temporal_key_tables`, V553 groups enriched input rows by `comparable_temporal_key`.

Inside a group it:

- collects all exact V552 structural fact IDs;
- chooses `group.iloc[0]` as the profile;
- calculates means of readiness/support/directionality/authority/comparability/confidence scores;
- fetches `pressure_score` for all matching V552 facts;
- computes `matching_fact_pressure.mean()`;
- writes one singular `source_v552_structural_fact_id` while the full set survives only in `source_v552_structural_fact_ids_diagnostic_json`.

This is a direct hostile-test failure for the **present implementation** whenever two simultaneous exact V552 pressures fall into the same comparable key.

It violates the accepted rule that simultaneous exact pressure identities survive independently and that an aggregate cannot become the sole semantic carrier.

It does **not** require architecture reopening, because the source fact IDs are still present before grouping. The lawful repair is to make exact pressure identity cardinality-preserving in the canonical sparse path and move any explicit governed aggregation to the secondary reversible projection.

### 5.3 Present V553 can rematch when exact association is missing

`_build_v553_temporal_key_tables` calls V552J `_packet_structural_dimension_resolution` for each input row and fills empty fields from its result.

Therefore present V553 can inherit the V552J semantic-score fallback instead of failing closed on absent exact association.

TD-R00 already forbids this.

### 5.4 Structural direction and temporal delta are not physically complete enough yet

Present V553 has a `delta_direction` field for cross-wave change. It also carries some upstream structural axis fields.

It does not yet publish the complete separately namespaced structural-direction authority/ref set required by TD-R00.

**Risk:** downstream code could treat `delta_direction` as the only direction available.

**Required hardening:** the sparse reference spine must carry structural-direction refs independently and tests must prove that deleting temporal delta does not delete structural direction, and vice versa.

### 5.5 0..n finite-stratum preservation is not implemented

Current V553 schemas do not provide the accepted role-qualified 0..n finite-stratum reference contract.

A scalar `horizon_constraint` is not a substitute for this multiplicity.

The architecture remains correct: V553 preserves governed mappings if supplied and leaves them empty if no governed mapping exists. It does not infer the nine-strata assignment.

### 5.6 Absolute Horizon is not physically distinguished yet

Current V553 has `horizon_constraint_id`, but the accepted architecture requires a distinct explicit Absolute-Horizon reference class and prohibits inference from generic Horizon/religiosity/ideology/finite-stratum semantics.

The current field is insufficient as the final physical reference contract.

This is implementation hardening, not a new V553 semantic family.

### 5.7 Temporal observation/relation/limit families are only partially represented by present schemas

Present V553 contains observations, deltas, gaps/absence, noncomparability-related registers and blocker material. It therefore contains useful implementation substrate.

But the live schema family is broader and older than TD-R00, and several surfaces encode score/readiness/interpolation semantics that are not canonical under the accepted architecture.

The accepted four-family decomposition remains the cleaner terminal contract:

- exact keys;
- exact observations;
- exact temporal relations only when comparable;
- typed temporal limit/negative authority otherwise.

### 5.8 Interpolation must be demoted out of semantic authority

Present V553 includes routines that linearly interpolate pressure/contradiction/absence/uncertainty between waves and builds country-year pressure fields.

TD-R00 and runtime-prior law prohibit V553 from using interpolated runtime temporal proxies as canonical semantic truth.

A legacy compatibility projection may exist only if explicitly non-authoritative and reversible to the sparse anchors. It cannot feed accepted V554 F1/F2 as authority.

---

## 6. Present V554 hostile findings

Current `ddm_v554_seed_contract.py` remains a pre-TD implementation.

It builds hard-coded seed types such as regional, national, demographic, class-status and household-mediation seeds. It synthesizes IDs from run/type/scope, computes bounded strength/confidence/specificity/certifiability scores, and conditions readiness on V553 country-year/interpolation outputs.

That is not the accepted V554 contract.

The accepted consumer instead needs to:

- address exact producer objects by ID/ref;
- apply a governed V554 rule ID/version;
- materialize F1 only for positive immutable eligibility;
- materialize F2 for exact machine predicates/requirements/limits/deferred bindings;
- expose B1 without inventing actor position, route, runtime proxy, geographic substitution or pressure-flow semantics.

**Court finding:** the current V554 consumer cannot be used as evidence that the accepted V553 handoff is sufficient. It is a legacy consumer slated for replacement under the already-frozen TD-R01 implementation ruling.

That replacement does not require changing V553 ownership.

---

## 7. Required family/boundary chain audit

### 7.1 `TEMPORAL_KEY`

**Upstream basis**  
Exact V552 structural fact identity + V552 temporal-source lineage + V552J exact association/admission/use lineage + earlier governing semantic/directionality/position/use refs + native source/scope identity.

**Present implementation**  
Stable sparse-like keys exist, but current grouping is based on comparable structural fields and can admit reconstructed V552 associations. Multiple exact facts can enter one group.

**V554 need**  
An immutable exact temporal identity that V554 can reference without text rematching, together with the complete producer reference spine.

**Terminal capability protected**  
Historically situated structural priors, simultaneous pressure preservation, resolver queryability, V3 exposure/history and orientation-to-strata.

**Loss/bloat test**  
Removing exact key identity starves later temporal applicability. Republishing all upstream semantics inside the key bloats V553 and breaks producer ownership. Exact references are the minimal solution.

**Disposition**  
`HARDEN`. Keep the family; prohibit many-to-one exact-pressure collapse in the canonical sparse key path; require exact producer-bound ingress.

### 7.2 `TEMPORAL_OBSERVATION`

**Upstream basis**  
One exact V552 measured fact at one governed temporal anchor, with exact V552J permission/association lineage and all applicable producer refs.

**Present implementation**  
Observation objects exist, but their source can be a grouped/averaged wave-key value and the row may name only one of several grouped exact facts as primary.

**V554 need**  
Exact observation IDs whose measured value and epistemic state trace to lawful producer evidence.

**Terminal capability protected**  
Time-specific structural context, V558 query resolution, V3 chronological exposure and distinction between observed zero and absence.

**Loss/bloat test**  
A grouped mean can erase simultaneous pressures; a duplicated copy of all V552 semantics is unnecessary. One exact observation plus reference closure is sufficient.

**Disposition**  
`HARDEN`. One canonical observation must not conceal multiple semantically independent exact V552 facts.

### 7.3 `TEMPORAL_RELATION`

**Upstream basis**  
Two or more exact observations linked only under governed comparability authority.

**Present implementation**  
Cross-wave deltas exist and distinguish delta direction, but older harmonization/readiness machinery and aggregate keys remain in the path.

**V554 need**  
Exact relation IDs/from/to observation refs, direction-of-temporal-change distinct from structural source→target direction, and explicit non-relation when comparison is unauthorized.

**Terminal capability protected**  
Persistence/change history without inventing causal rupture; later route temporal applicability and V3 historical development.

**Loss/bloat test**  
Without relation identity later stages would recompute temporal meaning. Giving V553 cross-key structural conflict/competition semantics would duplicate V556 jurisdiction.

**Disposition**  
`CONFIRM_WITH_HARDENING`. Keep temporal relation only; no new cross-key structural interaction.

### 7.4 `TEMPORAL_LIMIT / NEGATIVE_AUTHORITY`

**Upstream basis**  
Producer absence/denial/use limits, missing comparability authority, gap state, noncomparability and V553-local temporal-operation blockers.

**Present implementation**  
Multiple gap/absence/noncomparability/blocker registers exist, but legacy score/readiness surfaces can blur semantic negative authority and orchestration state.

**V554 need**  
Exact typed V553 limit refs where temporal use is blocked, while original upstream denial remains producer-owned and directly reachable.

**Terminal capability protected**  
Epistemic separation; absence/noncomparability never becoming zero/neutral; resolver/V3 fail-closed behavior.

**Loss/bloat test**  
Dropping negative authority invites downstream inference. Copying every validation error into semantic limits bloats the ontology.

**Disposition**  
`HARDEN`. Keep only downstream-meaningful temporal negative authority as semantic rows; keep transport/schema/build failures nonsemantic.

### 7.5 `GOVERNED_STRUCTURAL_REFERENCE_SET` — required reference contract, not family

**Upstream basis**  
All governing producer-owned objects that determine what the V553 temporal object means or may lawfully be used for.

**Present implementation**  
Partial reference fields exist, but no complete final TD-R00 reference envelope exists physically. Important classes are absent or scalarized.

**V554 need**  
Machine-resolvable exact refs for V552 fact, V552J association/admission/use, semantic/directionality/position/use authority, endpoints, channel, role-qualified 0..n finite strata, Horizon/AH distinction, inherited relation refs, provenance/version.

**Terminal capability protected**  
Direct DAG reuse, native nine-strata relational field, exact structural direction, AH distinction, runtime repository linkability and V3 causal auditability.

**Loss/bloat test**  
Without it V554/V558 must rematch labels. Turning it into a fifth V553 semantic family would duplicate producer-owned meaning.

**Disposition**  
`HARDEN`. Freeze as typed exact reference closure with cardinality and versioning; do not semanticize it.

### 7.6 Secondary reversible aggregate projection

**Upstream basis**  
Canonical sparse V553 objects only.

**Present implementation**  
Aggregate/interpolated country-year and score-derived surfaces are prominent and currently feed legacy V554.

**V554 need**  
None as semantic authority. Compatibility consumers may temporarily inspect a projection, but accepted V554 must prove operation with aggregate absent.

**Terminal capability protected**  
Prevents scalar collapse and maintains exact producer identity.

**Loss/bloat test**  
Removing the aggregate cannot starve terminal semantics if sparse refs are complete. Promoting it to authority would be bloat and information loss.

**Disposition**  
`HARDEN_TO_SECONDARY_ONLY`.

### 7.7 Exact V553→V554 reference handoff

**Upstream basis**  
Canonical V553 families plus their exact producer reference closure; direct upstream DAG reuse remains legal.

**Present implementation**  
A V553→V554 handoff schema exists, but it exposes legacy permitted/blocked seed payloads rather than the complete TD-R00 reference spine. A separate downstream compatibility handoff is explicitly marked legacy shadow in present V553 code.

**V554 need**  
Exact IDs/ref envelope sufficient for F1/F2/B1 construction without labels, scores, interpolation or synthetic rematching.

**Terminal capability protected**  
Lossless V554 eligibility/applicability; V557/V558 mixed-producer graph; ContextResolver queryability; V3 history.

**Loss/bloat test**  
Without exact handoff/addressability V554 must inspect/reconstruct semantics. Copying producer payloads into V553 is unnecessary; refs suffice.

**Disposition**  
`HARDEN`.

---

## 8. Hostile test matrix

| Hostile test | Present seam result | Accepted architecture result | Court disposition |
|---|---|---|---|
| V552/V552J exact fact/admission/use → V553 temporal identity | Partial: stable IDs exist, but semantic-score rematch remains possible | Requires exact producer-bound lineage and fail-closed disagreement | `HARDEN` |
| Structural source/target/direction vs temporal-delta direction | Present physical ref spine incomplete; `delta_direction` exists | Explicitly separate semantic classes | `HARDEN` implementation, architecture confirmed |
| Simultaneous exact-pressure preservation | **Fails present implementation** when same comparable key groups multiple facts and averages pressure | Explicit noncollapse law | `HARDEN` canonical sparse grouping |
| 0..n finite-stratum refs | Not physically implemented in current V553 schema | Explicit role-qualified 0..n refs, valid-empty if absent | `HARDEN` |
| Explicit Absolute Horizon distinction | Current generic `horizon_constraint_id` insufficient | Explicit AH refs only under designation authority | `HARDEN` |
| Observation/relation/limit/noncomparability | Partial live substrate; legacy extras remain | Four-family typed contract | `HARDEN` consolidation |
| Exact negative authority | Partial registers, mixed with legacy readiness/blockers | First-class typed limit where semantically meaningful | `HARDEN` |
| Exact V553 reference spine | Partial, not terminal contract | Frozen `GOVERNED_STRUCTURAL_REFERENCE_SET` | `HARDEN` |
| V554 immutable F1/F2 without text rematch | Current V554 cannot do this | Accepted V554 explicitly can once V553 spine + rule registry land | `HARDEN`; no reopen |
| Direct DAG reuse around V553 | Producer IDs/authority remain reachable | Explicitly preferred over republishing | `CONFIRM` with locator hardening |
| Any V3-required distinction irrevocably lost at first seam | Current code can lose simultaneous fact distinctions, but loss occurs inside replaceable pre-completion implementation while exact producer inputs still exist | Accepted sparse/reference contract prevents it | `HARDEN`; starvation not irreversible |

---

## 9. REOPEN grounds court

### 9.1 STARVATION

**Finding:** `NOT_PROVEN_AT_ARCHITECTURE_LEVEL`.

Present V553 can starve downstream consumers by collapsing exact facts and omitting reference classes. But the exact producer facts/joins remain available upstream, and the accepted V553 architecture already requires their preservation/direct reachability.

No terminally necessary meaning was found that has no lawful producer and no lawful downstream path under TD-R00/TD-R01.

### 9.2 BLOAT / DUPLICATION

**Finding:** `NOT_PROVEN_AGAINST_ACCEPTED_ARCHITECTURE`.

TD-R00's reference-set design and TD-R01's direct-DAG preference specifically avoid forcing V553 to republish V550/V551/V552/V552J semantics.

The live implementation does contain aggregate/score/interpolation surfaces that become bloat if retained as semantic authority. The accepted architecture already demotes/removes that authority.

### 9.3 JURISDICTION ERROR

**Finding:** `NOT_PROVEN_AGAINST_ACCEPTED ARCHITECTURE`.

The accepted boundaries remain coherent:

- V552 measured structural fact;
- V552J association/admission/use;
- V553 time;
- V554 bounded eligibility/applicability;
- V555 mediation routes/conditions;
- V556 pressure-flow/cross-pressure topology and attractor prerequisites;
- V557 lossless publication;
- V558 repository/resolution interface;
- V3 actor-specific generation, history, orientation and attractor realization;
- V2 expression.

No hostile case requires moving one of these meanings into V553 or V554.

### 9.4 CURRENT-SEAM MISMATCH

**Finding:** `PRESENT_BUT_REPAIRABLE_WITHIN_ACCEPTED_ARCHITECTURE`.

The live producer/consumer shapes do not satisfy TD-R00/TD-R01 today.

However, the mismatch does **not** meet the assignment's REOPEN threshold, because realization does not require illicit reconstruction or a semantic-family redesign. Exact producer IDs and permission lineage already exist; the necessary repairs are:

- remove canonical rematching;
- stop canonical many-to-one pressure averaging;
- publish the exact reference spine;
- keep aggregate/interpolation compatibility surfaces non-authoritative;
- implement the already-accepted V554 F1/F2/B1 consumer.

Therefore `CURRENT-SEAM_MISMATCH` triggers `HARDEN`, not `REOPEN`.

---

## 10. Binding hardenings from this court

These hardenings add no semantic family and change no jurisdiction.

### H01 — Exact producer-bound V553 ingress only

Canonical V553 rows may be admitted only with an already-governed exact V552/V552J association.

The semantic-score path in `_packet_structural_dimension_resolution` may be diagnostic/repair evidence only. It may not choose or substitute the authoritative V552 fact for canonical V553.

If exact association is absent, canonical result is unresolved/blocked and ownership returns upstream to V552J repair.

### H02 — No many-to-one exact-pressure collapse

Within a wave, two distinct exact V552 facts may not become one canonical V553 observation/value merely because their comparable structural key is equal.

Canonical temporal identity must preserve exact pressure multiplicity. An explicit upstream-governed composition object may authorize a composition, but V553 may not manufacture one with `mean()`.

### H03 — Diagnostic ID arrays are not semantic preservation

A singular primary `source_v552_structural_fact_id` plus a diagnostic array of other fact IDs does not satisfy losslessness when the other facts are semantically independent contributors.

Every canonical observation must have unambiguous exact source identity/cardinality.

### H04 — Typed reference spine is joinable, versioned data

Implement `GOVERNED_STRUCTURAL_REFERENCE_SET` as machine-resolvable typed refs, not free text or compatibility labels.

Every ref must identify producer/stage, object class, object ID or producer-owned deterministic row/hash locator, authority role and contract version as applicable.

### H05 — Preserve cardinality and role

Role-qualified finite-stratum refs, inherited relation refs and other multi-valued governed refs are 0..n.

No `first()`/mode/scalar convenience projection may become their canonical semantic representation.

### H06 — Separate direction namespaces

Structural pressure direction/source→target refs and V553 temporal-delta direction must be separately typed/named.

Completion tests must prove neither can be reconstructed from the other.

### H07 — Explicit Absolute-Horizon channel

Generic Horizon material and explicit Absolute-Horizon designation refs must be separate reference classes.

No current `horizon_constraint_id`, religiosity field, ideology label or finite-stratum mapping may be promoted to Absolute Horizon without governed designation authority.

### H08 — Typed negative/noncomparability closure

Observed zero, absent, denied, unresolved, missing authority, noncomparable and validation failure remain distinct.

Only semantic temporal blockers become `TEMPORAL_LIMIT / NEGATIVE_AUTHORITY`; infrastructure/build failures remain nonsemantic.

### H09 — V554 no-rematch/no-score ingress

Accepted V554 F1/F2/B1 must consume exact IDs/ref closure and explicit rule/predicate IDs.

Legacy V554 seed scores, hard-coded seed classes, interpolation-conditioned readiness and synthetic semantic IDs cannot be canonical authority.

### H10 — Direct-DAG closure test

V553 and V554 completion must prove that producer-owned V550–V552J authority remains resolvable by exact reference without requiring V553 to copy its semantic payload.

The proof must run with V553 aggregate/compatibility projections absent.

### H11 — Hostile seam fixture

Before `V553_COMPLETE_FOR_V554 = PASS`, add a production-seam fixture containing at least:

- two simultaneous same-wave exact V552 facts capable of colliding under the current comparable-key grain;
- opposite or materially distinct structural pressures;
- exact V552J permission/admission lineage;
- one denied/unresolved case;
- 0..n role-qualified finite-stratum refs, including a multi-stratum case;
- generic Horizon without Absolute Horizon;
- separately explicit Absolute-Horizon authority in another case;
- a noncomparable wave pair;
- native geographic scope that must not be downscaled;
- independent structural and temporal directions.

The fixture passes only if V554 F1/F2 can trace each lawful object back to exact producer IDs without text rematching and no simultaneous pressure is averaged, neutralized or selected away.

---

## 11. Direct DAG reuse verdict

`DIRECT_DAG_REUSE = CONFIRMED_AND_REQUIRED`.

This seam would become bloated if V553 were required to duplicate every V550/V551/V552/V552J semantic field.

The correct pattern is:

`V550/V551/V552/V552J producer object`
`→ exact typed reference in V553 semantic object`
`→ exact V553 temporal object`
`→ V554 F1/F2 object`
`→ mixed-producer transitive reference closure`
`→ V557/V558 repository`
`→ ContextResolver / V3`

The later resolver/repository must be able to resolve the reference closure with raw stage directories absent. That is a V557/V558 publication/indexing obligation, not permission for V553 to duplicate ownership.

---

## 12. Structural-direction / temporal-direction verdict

`SEPARATION_REQUIRED_AND_ARCHITECTURALLY_SOUND`.

Structural direction asks which governed structural position/source bears on which receiving position/target and in what producer-owned direction.

Temporal delta asks how the value of the same comparable pressure identity changes between two lawful observations.

A temporal increase in a pressure does not tell V554/V3 what the pressure's structural source→target direction is.

Present V553 has `delta_direction`, so the final reference spine must make structural direction just as explicit and independently addressable.

---

## 13. Simultaneous-pressure verdict

`PRESENT_IMPLEMENTATION_FAIL__ACCEPTED_ARCHITECTURE_PASS_AFTER_HARDENING`.

The hostile court found an actual many-to-one path:

`multiple exact V552 facts`
`→ same V553 comparable key group`
`→ mean pressure value`
`→ one canonical-looking key/wave row`
`→ one primary fact ID + diagnostic list`.

That path must not survive canonical completion.

The repair is already inside TD-R00 jurisdiction: exact sparse identity and aggregate-secondary enforcement.

No V554 relation family should be reintroduced to repair this. V554 receives distinct affordances; V556 later owns newly derived cross-pressure interaction topology.

---

## 14. Finite strata and Absolute Horizon verdict

### Finite strata

`0..N_ROLE_QUALIFIED_REFS_REQUIRED`.

Current absence of the physical fields is an implementation gap. It does not authorize a one-stratum fallback.

If governed mapping exists upstream, preserve it exactly. If it does not, preserve valid-empty/missing authority.

### Absolute Horizon

`EXPLICIT_DESIGNATION_ONLY`.

Current generic Horizon fields are not sufficient to infer AH.

AH remains outside the nine finite strata and must remain separately addressable when and only when governed authority exists.

---

## 15. Temporal negative authority verdict

The accepted `TEMPORAL_LIMIT / NEGATIVE_AUTHORITY` family is necessary and correctly scoped.

It protects distinctions the terminal system cannot safely reconstruct:

- observed zero vs absence;
- absence vs denied use;
- denied use vs missing authority;
- missing authority vs noncomparability;
- noncomparability vs neutral temporal change;
- semantic blocker vs build/transport failure.

Current code has pieces of these distinctions, but completion must consolidate them into the accepted typed semantic family and keep orchestration errors outside it.

---

## 16. V554 constructability test

### Question

Can accepted V554 construct immutable F1/F2/B1 without text rematching if TD-R00 is implemented as ruled?

### Answer

`YES`.

Required inputs already have lawful homes:

- measured fact/value/provenance: V552;
- association/admission/use: V552J;
- earlier semantic/directionality/position/use authority: original producer objects;
- time/key/observation/relation/limit: V553;
- native geography/source identity: producer identity chain;
- finite-strata/Horizon/AH refs: upstream governed refs when present;
- V554 rule/predicate authority: V554 rule registry.

V553's job is to supply its temporal semantics plus exact reference closure, not to rewrite all of these into text.

The current V554 implementation cannot perform this construction, but TD-R01 already marks production implementation blocked pending final V553 physical bindings and V554 rule authority. That is precisely the correct sequencing response to the present mismatch.

---

## 17. V3 first-seam loss audit

The court specifically asked whether a distinction V3 will need is already irrecoverably lost at V553→V554.

### Present implementation

If current V553 many-to-one grouping were treated as authoritative, **yes**: simultaneous pressure identity could be lost before V3 ever sees it.

If current legacy V554 seed score/composition were treated as authoritative, additional endpoint/position/epistemic distinctions could also be flattened.

### Accepted architecture

Those losses are not irreversible at the repository base because exact source facts and association lineage remain upstream and the completion implementation has not been released as the terminal contract.

TD-R00 exact sparse preservation + direct producer refs, followed by TD-R01 F1/F2/B1, leaves V3 able to receive through V558:

- distinct pressure identities;
- exact structural endpoints/direction;
- time and noncomparability;
- native scope;
- finite-strata/AH prerequisites;
- unresolved actor-position requirements rather than invented actor facts;
- epistemic/use authority.

The hostile audit therefore finds **repairable pre-completion implementation loss**, not architecture-level terminal starvation.

---

## 18. Wave-0 evidence disposition

Wave-0 vertical continuity remains useful but cannot by itself certify this seam.

Its reference fixture correctly protects contradictory pressures, temporal distinctions, mediation/flow distinctions and epistemic boundaries. It explicitly labels those packets as reference contracts rather than production outputs, and its current-production slices are strict expected failures where later continuity is not yet implemented.

For SI-R00, the key value of Wave-0 is therefore negative: it confirms that artifact-shape success must not be mistaken for semantic readiness.

The new hostile seam fixture in H11 must exercise the actual V552J→V553→V554 identities, not only reference payload copying.

---

## 19. Architecture-change court

### Semantic families

No change.

V553 remains exactly:

1. `TEMPORAL_KEY`
2. `TEMPORAL_OBSERVATION`
3. `TEMPORAL_RELATION`
4. `TEMPORAL_LIMIT / NEGATIVE_AUTHORITY`

`GOVERNED_STRUCTURAL_REFERENCE_SET` remains a required reference contract, not a fifth family.

V554 remains exactly:

1. `BOUNDED_STRUCTURAL_AFFORDANCE`
2. `STRUCTURAL_MEDIATION_APPLICABILITY_CONDITION`
3. `V554_V555_HANDOFF` boundary B1.

### Jurisdictions

No change.

### Canonical artifact topology

No architecture change requested. Implement the already accepted TD-R00/TD-R01 publication targets.

### New requirement introduced by SI-R00

Only sharper completion invariants/tests H01–H11, principally:

- exact producer-bound ingress;
- no same-wave many-to-one exact-pressure averaging;
- diagnostic arrays do not satisfy semantic preservation;
- direct-DAG exact-locator closure;
- hostile collision fixture.

These are hardenings of the accepted architecture, not a redesign.

---

## 20. Implementation sequencing consequence

`V553_COMPLETE_FOR_V554` must remain blocked until the accepted P1–P5 implementation satisfies the hardened seam court.

In particular:

1. P1 must eliminate canonical rematch authority and bind the final exact producer-reference envelope.
2. P2 must ensure canonical sparse key/observation cardinality does not collapse independent exact pressures.
3. P3 must preserve temporal relation vs structural direction and typed negative authority.
4. P4 must make all interpolation/aggregate compatibility surfaces non-authoritative and reversible.
5. P5 must prove accepted V554 F1/F2/B1 construction with aggregate absent and no descriptive rematching.

V554 production remains blocked until both its existing rule-registry blocker and the final V553 physical reference binding are satisfied.

---

## 21. Final four-way adjudication

### A — Cumulative lawful upstream reality

**PASS WITH IMPORTANT DIRECT-REUSE REQUIREMENT.** Exact producer identities and authority gates exist sufficiently to support the accepted reference architecture. Missing terminal mappings remain missing rather than invented.

### B — Present V553 reality

**FAILS TERMINAL COMPLETION TODAY.** It retains illicit fallback rematching, many-to-one pressure averaging, incomplete reference closure and legacy interpolation/aggregate authority surfaces.

### C — Immediate V554 demand

**ACCEPTED ARCHITECTURE IS SATISFIABLE; PRESENT CONSUMER IS NOT.** The new F1/F2/B1 consumer can be built from the preserved exact DAG; the current seed contract must not be canonical.

### D — Total Rawlsing terminal demand

**NO ARCHITECTURE-LEVEL STARVATION PROVEN AFTER HARDENING.** Nine-strata relation, AH distinction, temporal history, mediation/pressure-flow prerequisites, V3 development/genealogy/attractor paths and epistemic separation remain reachable if H01–H11 are enforced.

### Court result

`HARDEN`.

The hostile audit falsified any claim that the **current implementation** already satisfies TD-R00/TD-R01. It did **not** falsify the accepted architecture or prove the REOPEN threshold.

---

V553_V554_SEAM_INTEGRITY = HARDEN
