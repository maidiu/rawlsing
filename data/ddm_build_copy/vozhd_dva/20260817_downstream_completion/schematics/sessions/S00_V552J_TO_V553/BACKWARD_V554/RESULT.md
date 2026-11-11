# S00-B — Backward from V554 total need

**Perspective:** `BACKWARD_V554`  
**Status:** `COMPLETE_WITH_FINDINGS`  
**Worker branch:** `agent/vozhd-dva-s00-backward-v554`  
**Analysis base / branch head at start:** `5190803a5586f289c2fee01c73ff2411d2d12665`  
**Target:** `agent/vozhd-dva-s00-integration`

## Executive ruling

The correct V553→V554 seam is **not a serial handoff in which V553 republishes everything V554 might need**. V554's lawful intake is a composed DAG.

The minimum architecture is:

`V554 COMPOSED INTAKE = earlier governed structural/authority objects used for the meanings they still own + V553 temporal overlay used only for meanings that require cross-wave temporal derivation`

The strongest earlier reusable structural objects are already present:

- V552 structural facts own the measured structural-pressure observation and exact V552 lineage;
- V552 temporal-key-source rows own stable structural source identity/candidate lineage but explicitly do **not** own temporal-field authority;
- canonical V552J join/input/handoff rows provide a verified, permission-bearing envelope over V552 facts plus exact structural dimensions, V551J lane/state, support/directionality/authority/comparability/confidence state, and V552 temporal-key-source references;
- governed V550 semantic/directionality/position authority surfaces remain direct authority for the particular uses they explicitly authorize, including position/demographic coordinates where their use gates permit that use.

What these earlier objects do **not** own is the relationship **between waves**. V553 is needed to establish a lawful comparable structural key across waves, order authorized anchors in historical time, derive per-key temporal observations and authorized deltas, preserve gaps/noncomparability/temporal uncertainty, and optionally mark a structural rupture **candidate** without inventing an external event or causal explanation.

Current V553 already contains most of this residual machinery in its sparse-key path. The principal seam failure is therefore not absence of a giant new V553 ontology. It is that current V554 primarily consumes the older aggregate country-year/harmonization surface and reconstructs synthetic pressure/contradiction identifiers instead of composing direct earlier structural authority with the richer sparse V553 temporal contract.

## Control-artifact note

The assignment-required `schematics/CUMULATIVE_UPSTREAM_MAP.md` does not exist on either the latest worker branch or `agent/vozhd-dva-s00-integration`; repository search also found no file with that name. I did not invent it. The absence did not block this reconstruction because the assignment's frozen facts and the actual V550/V552/V552J/V553 producers expose the relevant authority boundaries directly. Vozhd should restore or remove the stale read-order reference.

## 1. What operation is V554 actually responsible for?

V554 is a **bounded structural-temporal affordance composer** for later mediation. Its lawful operation is:

`governed structural position/pressure authority + governed V553 temporal state → bounded seed affordance, explicit limits, downstream mediation requirements, and prohibitions`

V554 may:

- choose which lawful structural and temporal inputs are relevant to a bounded downstream affordance;
- classify readiness/use permission from governing upstream states;
- create V554-owned affordance IDs and V555 mediation requirements;
- preserve negative authority, absences, uncertainty, and prohibitions;
- require later household/family/carrier/orientation/pressure-flow mediation without pretending those facts already exist.

V554 may not create persona, biography, a concrete household/family relation, parent/co-parent psychology, carrier membership, psyche, Enneagram type, wound, striving object, pressure-flow route, memory, dialogue, or runtime text.

The current implementation's broad shape is consistent with that jurisdiction, but its intake is too serial and aggregate: `_build_seed_affordance_index()` is driven mainly by V553 readiness/harmonization plus the V553 country-year pressure frame even though substantially richer earlier and sparse-temporal objects exist.

## 2. V554 total information need

V554 needs the following classes of information. They are not all V553 obligations.

1. **scope and provenance identity** — source family, country/scope, wave identity, producer run/artifact/row lineage;
2. **underlying structural-pressure fact** — lawful pressure value/status and measurement/evidence state;
3. **exact structural identity** — relation axis, target entity, driver facet, structural channel and/or horizon constraint where authorized;
4. **governing semantic/directionality/position authority** — including use permissions and review/blocked state;
5. **support, confidence, permission, and negative authority** — not collapsed into a single readiness scalar;
6. **position/demographic/regional constraints** where an earlier authority surface actually authorizes them;
7. **stable cross-wave comparable identity** for a structural pressure that is claimed to persist or change through time;
8. **ordered temporal anchors/observations** tied to that comparable identity;
9. **pressure-over-time change relation** — authorized delta/direction and, only if governed, higher-level persistence/drift/change classification;
10. **gap/noncomparability/interpolation state** — including explicit known-unknown spans and temporal confidence;
11. **contradiction/competing-pressure identity over time** where distinct upstream pressures actually coexist or conflict;
12. **rupture-candidate state** if supported by temporal change, while external-event attribution remains separate authority;
13. **downstream mediation requirements and forbidden uses**, which V554 can derive from its own stage contract;
14. **explicit missing authority** for household/family/carrier/locality or other requested meaning that no upstream source supports.

## 3–8. Authority allocation and exact residual V553 obligation

### Earlier material V554 can reuse directly

#### V552 structural fact index

A V552 structural fact already owns the measured structural-pressure observation: stable fact ID, source artifact/row/hash, empirical-distribution identity, pressure formula/scale/measurement hash, semantic and structural identity signatures, exact relation/target/driver fields, pressure score/status, evidence status and downstream permission. V554 should reference this object directly when it needs the underlying structural fact rather than accepting a V553 re-copy as a new source of structural authority.

#### V552 temporal-key-source index

This object is useful **directly for structural lineage and key-source identity only**. Its producer deliberately sets `allowed_for_v553_temporal_field=False`; V552 pressure handoff also states `direct_v553_authorization=False` and `temporal_authority=False`. The name “temporal key source” therefore does not authorize V554 to claim temporal persistence/change from it.

#### Canonical V552J join/input/handoff surface

V552J is a particularly useful direct V554 reference surface because one verified row carries or points to:

- exact V552 structural fact and temporal-key-source identity;
- relation/target/driver/channel/horizon dimensions;
- V551J lane/certification/review/support/directionality/authority state;
- structural resolution state;
- read/probe/temporal-field/runtime permissions and blocker reason;
- comparability/confidence/readiness context.

V554 may use these meanings directly where they remain the authority. It must not reinterpret V552J's per-row comparability/readiness context as a completed cross-wave temporal comparison.

#### Earlier V550 authority/position surfaces

The authority contract explicitly separates semantic classification from permission and exposes use-specific gates. A certified position coordinate can be lawful as a demographic predictor, branch-position signature, or parent-prior coordinate only when the corresponding `allowed_as_*` field is true. V554 may directly reuse such a governed structural coordinate as a **constraint/prior coordinate**, not as a generated person fact. If a requested demographic/locality dimension lacks such authority, V553 may not manufacture it merely because V554 wants it.

### Meaning that genuinely requires V553

Direct earlier reuse is insufficient for any claim whose truth depends on relations across time. V553 therefore owns the residual operation:

1. select lawful per-wave structural candidates from canonical V552J and exact V552 fact/key-source references;
2. require certified semantic/directionality/position harmonization authority for the cross-wave comparison;
3. build a stable `comparable_temporal_key` at an authorized structural grain;
4. distinguish `AUTHORIZED_SPARSE_TEMPORAL_KEY`, probe-only, blocked, and fallback/lower-grain states;
5. bind each authorized wave/year observation to the same comparable key and exact upstream lineage;
6. derive pairwise authorized structural deltas only when both endpoints are authorized comparable anchors;
7. preserve missing spans as known unknowns, with value inference disallowed unless a separate interpolation authority exists;
8. preserve temporal confidence/authority/noncomparability rather than replacing them with neutral/zero;
9. optionally identify a structural rupture **candidate** from authorized change while asserting no external-event claim;
10. publish a V554-facing temporal use/absence contract keyed to the same stable temporal identity.

V553 must leave unresolved:

- concrete demographic/position/locality facts absent upstream;
- household/family/carrier membership or events;
- actor orientation, biography, psyche, memory or developmental response;
- causal explanation of a structural change;
- an external event behind a rupture unless a governed event authority is supplied;
- actor-specific cohort/developmental windows (the current V553 cohort-window rows are correctly only reserved requirements);
- persistence/drift category thresholds unless Vozhd explicitly governs them. Numeric authorized deltas are safer than pretending arbitrary thresholds are ontology.

## 9. Does composed intake satisfy V554 total need?

**Schematic answer: yes, conditionally. Current implementation answer: not yet.**

The lawful composed intake is sufficient for V554's bounded-affordance responsibility if:

- V554 consumes/refers directly to earlier structural/position authority for meanings still owned upstream;
- temporal claims are accepted only from the authoritative V553 sparse temporal path;
- V553 temporal rows retain stable references to their V552/V552J basis;
- missing direct authority remains missing instead of becoming a V553 placeholder;
- V554's own mediation/prohibition machinery remains explicitly V554-owned rather than falsely attributed upstream.

Current V554 does not satisfy that composition rule. It loads many V553 artifacts but constructs seed rows primarily from readiness/harmonization and the aggregate country-year pressure surface. Exact sparse temporal keys, exact V552/V552J lineage, typed gaps/noncomparability and pairwise delta identity are therefore not the primary seed authority today.

## Required composed-intake matrix

| V554 need | Earlier authoritative object available? | Direct V554 reuse lawful? | Why / conditions | Requires V553 derivation? | Required V553 contribution | Final source in V554 composed intake |
|---|---|---|---|---|---|---|
| source/country/run/wave provenance | V552/V552J manifests and rows | yes | stable scope/producer identity remains upstream authority | only to order/relate waves | temporal anchor association | `EARLIER_PLUS_V553` |
| underlying per-wave structural pressure value/status | V552 structural fact / V552J joined fact | yes | V552 owns measured structural pressure and evidence state | not for the per-wave fact itself | reference it from temporal observation | `EARLIER_PLUS_V553` |
| exact relation/target/driver identity | V552 fact + V552J | yes | structural identity does not become more authoritative by being copied through V553 | only to prove the *same comparable structural grain* across waves | comparable-key binding | `EARLIER_PLUS_V553` |
| structural channel / horizon constraint | V552J where resolved and authorized | yes | direct structural constraint is lawful at its original grain | only for cross-wave continuity/comparability | include in comparable-key basis when available | `EARLIER_PLUS_V553` |
| V551J certification/support/directionality/authority context | V552J | yes | V552J already carries governing lane/state and scores | temporal authority is separate | preserve/reference in temporal authorization basis | `EARLIER_PLUS_V553` |
| structural read/probe/blocked permission | V552/V552J | yes | permission must survive unchanged for the original object | V553 must derive a separate temporal-use permission | key/observation temporal authority status | `EARLIER_PLUS_V553` |
| semantic/directionality/position authority metadata | governed V550 overlays/use contracts | yes | original authority surface should remain cited; only certified rows count | yes for cross-wave shared compatibility | harmonization/comparability ruling | `EARLIER_PLUS_V553` |
| static governed demographic/position coordinate | earlier position-coordinate / use-authorized structural surface when present | yes, only with explicit use permission | can constrain a bounded seed without becoming actor fact | no unless a temporal claim about the coordinate is made | none for static direct use | `EARLIER_UPSTREAM_DIRECT` |
| requested demographic/position dimension with no governing row | no | no | demand is not evidence | no—V553 cannot create it | preserve missing authority | `MISSING_AUTHORITY` |
| country-level geographic scope | producer scope identity | yes | existing scope fact | only for historical indexing | attach temporal key/year | `EARLIER_PLUS_V553` |
| subnational/locality fact absent upstream | not necessarily | no if absent | V553 temporalization cannot invent locality | no | none; explicit unresolved/missing state | `UNRESOLVED` |
| stable cross-wave comparable pressure identity | no completed earlier object; V552 key-source is candidate only | no | requires comparison of multiple waves under shared authority | yes | `comparable_temporal_key` + grain/basis + authorization state | `V553_DERIVED` |
| ordered authorized pressure observations over time | individual earlier facts exist, relation does not | no for temporal relation | ordering and same-key authorization are V553 meaning | yes | per-key wave/year observations | `V553_DERIVED` |
| authorized cross-wave delta/change | only endpoint facts exist | no | subtracting endpoint values is illicit without V553 comparability authorization | yes | pairwise delta with interpretation permission and endpoint refs | `V553_DERIVED` |
| persistence/drift/change label | no governing earlier temporal object | no | depends on authorized temporal relation and governed thresholds | yes | at minimum numeric/directional delta; label only if governed | `V553_DERIVED` |
| temporal gap / known unknown | endpoint facts may exist around the gap | no | gap is a property of temporal coverage | yes | gap/absence state with `value_inference_allowed=false` | `V553_DERIVED` |
| interpolation | endpoint facts exist | no by default | interpolation is a temporal inference needing explicit authority | yes | explicit interpolation policy/state; current sparse path correctly defaults to none | `V553_DERIVED` |
| temporal confidence/noncomparability | per-wave confidence exists | not sufficient alone | pairwise/series confidence and noncomparability are temporal | yes | temporal authority, confidence penalties, comparability state | `EARLIER_PLUS_V553` |
| competing/contradictory structural pressures over time | distinct upstream pressures may exist | yes for each pressure separately | preserve each original pressure and conflict evidence | yes for their time-indexed coexistence/change | stable separate temporal keys plus conflict/contradiction lineage; do not infer contradiction from overlay row-count imbalance | `EARLIER_PLUS_V553` |
| structural rupture candidate | endpoint pressures/delta basis upstream | no | candidate is temporal change meaning | yes | candidate tied to authorized delta; no external-event claim | `V553_DERIVED` |
| external event / causal explanation for rupture | no event authority in current V553 | no | temporal magnitude is not event causation | V553 cannot create from current input | explicit unresolved event authority | `MISSING_AUTHORITY` |
| concrete household/family/carrier signal | not generally present in inspected authority | only if a separate governed earlier object actually supplies it | generic V554 requirement does not prove a signal | no, unless the signal itself is a temporal structural object with authority | do not manufacture it | `MISSING_AUTHORITY` |
| requirement that later mediation occur | stage law | n/a | this is V554's own contract responsibility | no | none | `V554_OWN_DERIVATION` |
| forbidden downstream uses / no-personhood boundary | stage law + upstream prohibitions | n/a | V554 must enforce its own jurisdiction | no | preserve any upstream prohibitions as additional constraints | `V554_OWN_DERIVATION` |
| V552/V552J lineage for a temporal seed | earlier lineage exists | yes | source authority remains upstream | V553 must bind temporal state to it | stable reference from temporal key/observation/delta | `EARLIER_PLUS_V553` |

## 10. Current V553 output classification

### Useful and close to the residual contract

- canonical fail-closed V552J intake and harmonization context;
- `v553_temporal_key_candidate_index` and typed blocker states;
- `v553_harmonized_pressure_key_index` with exact structural dimensions, V552 fact/key-source lineage, V552J packet/input lineage, comparable key grain/basis and authorization state;
- `v553_temporal_pressure_observation_index` separating authorized structural anchors from probe-only values;
- `v553_cross_wave_delta_index` separating authorized structural deltas from probe deltas and exposing interpretation permission;
- `v553_interpolation_segment_index` and `v553_temporal_gap_and_absence_index`, especially the default preservation of unknown gaps with no inferred value;
- `v553_temporal_authority_ledger` and comparability/noncomparability audits;
- `v553_temporal_pressure_field` as a bounded temporal view when it stays keyed to sparse observations/deltas;
- `v553_v554_handoff_index` as the right conceptual location for V554 temporal permission, though it needs stronger references to the canonical sparse objects;
- `v553_structural_rupture_candidate_index` only as a **candidate** surface with no external-event claim.

### Lossy or dangerous as primary V554 authority

- the older aggregate `_build_pressure_rows()` / country-year route that derives `pressure_intensity` from counts of certified overlay rows, absence and uncertainty penalties;
- its `contradiction_pressure = abs(directionality_row_count - semantic_row_count) / total_rows`, which is coverage imbalance, not a lawful structural conflict ontology;
- synthetic `shared_relation_axis::<semantic_signature>`, `shared_target_entity::<...>`, etc. in the aggregate shared-axis path;
- aggregate harmonization/readiness scores when used as substitutes for typed evidence, permission and comparability state;
- V554's current synthetic `country:year`, `contradiction::year`, and wave-pair IDs when exact sparse pressure/delta/provenance identities exist.

These aggregate objects may remain diagnostics or compatibility views, but they should not supersede exact earlier structural authority plus the sparse temporal transform.

### Redundant duplication

V553 does not need to republish the entire V552/V552J object as new structural authority. It needs enough stable identifiers and governed state to bind its temporal derivation back to those objects. V554 can retrieve the original object directly for the underlying structural meaning.

### Missing / unsettled residual semantics

- one canonical V554-facing temporal composition contract that makes the sparse key/observation/delta/gap authorities—not the aggregate country-year surface—the authoritative temporal contribution;
- an explicit conflict-set/competing-pressure linkage if downstream needs require multiple pressures to be treated as one conflict set; this must preserve distinct upstream pressure identities rather than inventing a scalar contradiction;
- governed persistence/drift category thresholds if those labels are desired beyond numeric/directional delta;
- repaired rupture-candidate semantics (see seam defect below);
- external event authority remains genuinely missing, not a V553 implementation gap to fill with inference.

## 11. Illicit bypass cases

Cross-stage reuse is lawful **until the claimed meaning requires the skipped transformation**. The following are illicit:

1. V554 subtracting two V552 pressure scores from different waves and calling the result drift/change without a V553 comparable-key authorization.
2. Treating `v552_temporal_key_source_id` as temporal authority. Its producer explicitly marks it as not authorized for the V553 temporal field.
3. Treating V552J `comparability_score`, readiness score, or `must_temporalize` as proof that two waves are actually comparable. These are inputs/requirements for V553, not the completed cross-wave relation.
4. Treating a V550 row eligible as a temporal-pressure indicator as a temporal trajectory. Eligibility authorizes use as input; V553 still owns cross-wave comparison.
5. Using an earlier structural fact to fill a missing year with zero/neutral because neighboring years exist. The V553 sparse path correctly represents the missing span as known unknown.
6. Calling a large structural delta a named historical event or causal rupture without separate event authority.

## 12. Minimum new V553 output contract

Once direct earlier reuse is allowed, V553 does **not** need a self-contained copy of every structural object. The minimum logical contract is a **temporal overlay** with three grains; existing physical artifacts may implement these grains separately.

### A. Comparable temporal key grain

One row per governed cross-wave structural identity:

- `comparable_temporal_key` / stable V553 temporal key;
- source/country scope;
- key grain and exact key basis;
- exact upstream refs: V552 structural fact(s), V552 temporal-key-source(s), V552J packet/input/handoff IDs;
- relation/target/driver/channel/horizon identity as identifying context, explicitly derivative of/referential to upstream authority;
- harmonization/comparability authorization state;
- probe/blocked/fallback reason;
- no-personhood class.

### B. Temporal state grain

One row per key × observed anchor or explicit gap:

- wave/year;
- authorized structural pressure value **or null**;
- temporal status (`observed_authorized_anchor`, probe-only, known-unknown gap, noncomparable);
- temporal use permission;
- confidence/uncertainty;
- direct upstream observation refs;
- interpolation state/policy where relevant.

### C. Temporal relation grain

One row per key × ordered anchor pair/span:

- endpoint wave/year IDs;
- authorized structural delta or null;
- direction and raw magnitude;
- interpretation permission;
- comparability/authority/confidence state;
- explicit gap/noncomparability between endpoints;
- optional structural rupture-candidate flag/ref;
- `external_event_claim_made=false` unless an independent governed event source exists.

A compact V553→V554 handoff/index should then say which keys/states/relations are legal seed-affordance inputs and what absence handling is mandatory. It should reference, not duplicate, the earlier structural objects V554 can consume directly.

This is the minimum residual contribution because everything else belongs either to earlier authority or to V554's own bounded-affordance classification.

## Preservation ledger

| Information | S00-B treatment | Authority owner / rationale |
|---|---|---|
| V552 structural fact ID/value/status/measurement lineage | `PRESERVE` by direct reference | V552 remains source authority |
| V552 temporal-key-source ID | `PRESERVE` as source lineage only | explicitly not temporal-field authority |
| V552J packet/input/handoff identity and permission | `PRESERVE` | canonical verified envelope |
| exact structural dimensions | `PRESERVE` from V552/V552J | V553 may bind but must not replace their authority |
| V550 semantic/directionality/position authority | `PRESERVE` / direct reuse where use-authorized | authority metadata remains earlier-stage law |
| cross-wave comparable identity | `DERIVE` | genuinely V553 temporal relation |
| ordered temporal anchor state | `DERIVE` | genuinely V553 |
| authorized pairwise delta | `DERIVE` | genuinely V553 after comparability gate |
| gaps/noncomparability | `DERIVE` as temporal coverage state | do not fill |
| interpolation | `UNRESOLVED` unless explicitly authorized | current sparse path rightly defaults off |
| rupture candidate | `DERIVE` only as structural candidate | causal/event meaning remains unresolved |
| external historical event explanation | `UNRESOLVED` | no current event authority |
| demographic/position coordinate | `PRESERVE` directly if earlier use-authorized | not a V553 invention |
| missing household/carrier/locality fact | `UNRESOLVED` | downstream demand cannot create upstream evidence |
| V554 mediation requirement | `DERIVE` in V554 | V554-own jurisdiction |
| persona/biography/psyche/etc. | `FORBIDDEN_TO_INFER` | outside V553 and V554 |

## Worked transformations

### Worked case A — direct earlier reuse plus related V553 temporal meaning

Suppose V552 structural fact `F1` is an authorized pressure observation for relation `R`, target `T`, driver `D` in wave `W1`, and canonical V552J row `J1` verifies `F1`, its exact dimensions, evidence lane and permission. V554 needs those structural identities and the underlying W1 pressure fact.

**Direct reuse:** V554 should reference `F1/J1` for the structural fact, dimensions, evidence state and provenance. V553 does not need to become the new owner of those facts.

Suppose a related authorized `F2/J2` exists in `W2`. V553 may establish that `F1/J1` and `F2/J2` share one governed comparable key, create authorized temporal observations for W1/W2 and derive the authorized W1→W2 delta.

**Composed V554 intake:** `F1/J1 + F2/J2` provide structural authority; V553 provides “these are comparable members of one temporal structural pressure and changed by Δ under state C.” A V554 seed can therefore keep exact structural lineage and temporal meaning without forcing V553 to duplicate the whole V552J row.

### Worked case B — earlier reuse is insufficient

Suppose V552 has valid pressure facts at 2000 and 2010 with the same apparent relation/target/driver labels. V554 wants to claim “this structural pressure persisted/increased between 2000 and 2010.”

Direct reuse is insufficient. V552 explicitly does not authorize direct V553 temporal-field use, and the apparent labels alone do not prove cross-wave semantic/directionality/position comparability. V553 must select the authorized wave surfaces, prove a shared comparable key, produce authorized observations and then an interpretable delta. Only then may V554 consume a temporal persistence/change affordance.

### Worked case C — hostile gap/noncomparability/rupture ambiguity

Suppose W1 has an authorized V552/V552J pressure fact. W2 exists structurally but its directionality authority is unresolved, or a whole middle year is absent. W3 is authorized and differs sharply from W1.

V554 may still reuse the W1 and W3 facts directly **as facts at those waves**. It may not call W2 zero, interpolate the missing year, or claim a continuous trajectory. V553 must mark W2 probe/blocked or the missing span known-unknown, carry noncomparability/confidence state, and deny value inference.

A large authorized W1→W3 delta may justify a `structural rupture candidate`; it does not identify an external event or causal mechanism. If endpoint comparability itself is blocked, even the delta interpretation must remain blocked.

The current rupture builder reinforces why this must stay schematic: delta rows use `comparability_status="authorized_comparable"`, while the rupture builder tests for literal `"comparable"`, so interpretation permission is mismatched. It also labels any sufficiently large up/down delta `direction_reversal` rather than detecting an actual reversal across successive directions. These are current V553 implementation defects, not grounds to move rupture meaning into V554.

## Seam defects / concrete findings

### S00-B-D01 — V554 consumes the wrong temporal authority surface

**Class:** semantic/contract gap.  
V554 loads a number of V553 artifacts but its seed construction is driven mainly by V553 readiness/harmonization and aggregate country-year pressure. It does not make the canonical sparse comparable key, temporal observation, delta, gap/noncomparability and exact upstream lineage the primary temporal source.

**Required behavior:** V554 composed intake must use direct earlier structural authority + authoritative sparse V553 temporal state.

### S00-B-D02 — current V554 synthesizes weaker identities where exact lineage exists

Current regional seed rows synthesize source pressure IDs like `country:year`, contradiction markers like `contradiction::year`, and wave-pair strings. These cannot replace stable sparse V553 key/delta IDs plus V552/V552J lineage.

### S00-B-D03 — aggregate V553 pressure path is not adequate structural-pressure authority

The older aggregate path derives pressure intensity from certified-overlay row-count coverage and synthetic shared structural identifiers. That can be a diagnostic coverage surface; it must not supersede exact V552/V552J structural pressure facts or sparse V553 temporal relations.

### S00-B-D04 — rupture-candidate contract mismatch

Current V553 delta status and rupture-consumer status vocabulary disagree (`authorized_comparable` vs `comparable`), and the current “direction reversal” test does not actually compare successive direction signs. Freeze only “bounded structural rupture candidate, no external event claim” at this session; return exact candidate classification/threshold semantics for implementation adjudication.

### S00-B-D05 — V554 demographic/position placeholders should not imply V553 obligation

V554 currently emits generic required demographic/region slice contracts. Where earlier governed position-coordinate authority exists and explicitly permits the use, V554 may consume it directly. Where it does not exist, the correct state is missing/unresolved authority—not a requirement for V553 to generate a demographic fact.

### S00-B-D06 — assigned cumulative map artifact is missing

`schematics/CUMULATIVE_UPSTREAM_MAP.md` is absent on both worker and target integration branches. This is a control-plane/documentation defect, not a semantic block for S00-B because actual producer contracts were inspectable.

## Implementation obligations for later work

1. **V554 composed-input resolver:** make source selection semantic-purpose-specific rather than serial-stage-specific.
2. **Direct structural reference rule:** V554 should retain exact V552/V552J authority references for structural fact/dimensions/permissions instead of accepting V553 copies as replacement authority.
3. **Temporal bypass guard:** any V554 field that claims comparison/change/persistence/drift/gap/temporal confidence must cite a V553 temporal key/state/relation with lawful interpretation permission.
4. **Sparse V553 authority:** freeze the sparse key/observation/delta/gap family as the candidate canonical V553 temporal contribution; relegate aggregate country-year/coverage-derived surfaces to diagnostic/compatibility use unless separately justified.
5. **Typed absence rule:** gaps, noncomparability, probe-only and blocked states must not become zero/neutral or positive seed readiness.
6. **No duplication rule:** a V553 temporal row should carry stable upstream references and only the upstream fields needed to define its temporal key; it should not become a second structural-fact authority.
7. **Position/direct-reuse gate:** only explicitly use-authorized earlier position/demographic objects may enter V554 directly.
8. **Rupture repair:** reconcile comparability enums, define real reversal semantics, and keep external-event causation outside V553 absent event authority.
9. **Conflict identity:** if later mediation needs a conflict set, preserve distinct pressure IDs and add only a governed linkage; do not use aggregate coverage imbalance as contradiction.
10. **Regression tests:** include a direct-reuse+temporal-overlay case, an illicit direct-delta bypass case, a known-gap-not-zero case, and a rupture-candidate-without-event case.

## Unresolved questions for Vozhd

1. Should V554's canonical direct structural reference be the V552 structural fact itself, the canonical V552J joined/handoff row as a permission-bearing envelope around that fact, or a normative pair of references? S00-B recommends the pair when both meanings are needed: V552 owns the fact; V552J owns the governed join/handoff state.
2. Which exact earlier position/demographic artifact family should be named as V554's canonical direct-use source? The authority contract proves that selective direct reuse is lawful, but S00-B does not freeze a particular physical V550 table without the missing cumulative map.
3. Does Vozhd want qualitative `persistence/drift/rupture` categories in V553, or only authorized numeric/directional deltas plus candidate flags until thresholds are explicitly governed?
4. If downstream mediation requires a formal conflict-set identity, which stage owns the linkage among distinct structural pressure keys? S00-B rules out the current aggregate row-count “contradiction pressure” as sufficient authority but does not assign a new ontology unilaterally.
5. What governed event authority, if any, will allow V553 to distinguish a structural rupture candidate from a historically identified rupture/event? Current V553 explicitly has no event registry supplied.
6. Restore `schematics/CUMULATIVE_UPSTREAM_MAP.md` or remove it from session read orders.

## Recommended Vozhd ruling

Adopt the following S00 backward principle for synthesis:

> **V553 is a temporal overlay, not a universal downstream serializer.** Earlier structural facts, position/authority objects, permissions and lineage remain directly reusable by V554 for the meanings they still own. V553 owns only the new cross-wave temporal relationship: comparable-key authorization, ordered temporal states, authorized change relations, temporal limits/uncertainty and bounded rupture candidates. V554 composes the two authority classes and performs its own bounded-affordance/mediation-requirement derivation.

Under that principle, current upstream material is sufficient to reach a coherent V554 contract without reopening V552/V552J. The remaining work belongs chiefly to the V553→V554 seam: select the sparse V553 authority surface, deepen the V554 composed intake, and repair the bounded rupture semantics.
