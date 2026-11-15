# R0-04 — V557/V558 Runtime Boundary and V3/V2 Consumer Requirements

**Worker:** R0-04  
**Wave:** Vozhd Dva Wave 0  
**Status:** COMPLETE_WITH_FINDINGS  
**Branch:** `agent/vozhd-dva-r0-04-runtime-contract`  
**Base SHA:** `958983139b8f75dc5cda65d5bf71b376d17820df`  
**Target base:** `agent/vozhd-dva-wave0-integration`

## Mission outcome

R0-04 traced the current V556-facing information through V557 and the V558 review gates, worked backward from the frozen V3/V2 responsibilities, and defined the minimum information boundary required for a future V3 consumer without implementing V3, V2, genealogy, prompt generation, or a production V557/V558 rewrite.

The central result is that the present boundary is safe in the narrow sense that it attempts to prevent raw evidence, dialogue, voice, and persona material from crossing into runtime, but it is not yet an adequate runtime information boundary. The current path reduces upstream semantics into readiness, blocker, and governance metadata. A future V3 actor engine could not reconstruct historically situated pressures, nine-strata relations, mediation, causal routing, or attractor dynamics from V558 alone. Reaching back into V553–V556 would therefore be unavoidable, which would violate the intended architecture.

The starvation begins before V558. Current completion-grade V556 is itself still a boundary contract: it emits mediation-derived slot names/channels, candidate-dynamics labels, attractor requirements, absence ledgers, stop reasons, and handoff rows, but not a realized causal pressure-flow topology. V557 then further reduces those V556 rows to renderer-boundary rows keyed mainly by `slot_name` plus safety/audit flags. V558 normalizes the resulting governance surface. The implementation wave therefore needs coordinated producer/consumer hooks: V556 must eventually emit the structural semantics V3 needs; V557 must preserve them while enforcing rendering separation; V558 must expose them as governed runtime priors.

No production semantics were modified in Wave 0.

---

## 1. Current V557 → V558 trace

### 1.1 V556 material available to V557 today

The completion-grade `ddm_v556_pressureflow.py` consumes V555 mediation slots and emits:

- `v556_pressureflow_contract_slots.parquet`;
- `v556_attractor_generation_requirements.parquet`;
- `v556_psyche_generation_absence_register.parquet`;
- `v556_pressureflow_stop_reason_ledger.parquet`;
- `v556_v557_handoff_index.parquet`;
- `v556_pressureflow_attractor_packet.json` and readiness/handoff metadata.

A pressure-flow slot currently preserves roughly:

- `pressureflow_slot_id`;
- `slot_name`;
- `slot_channel`;
- `pressure_status = candidate_dynamics_only`;
- `pressure_family = pressureflow`;
- `blocked_from_runtime_psyche`;
- `blocked_from_enneagram_assignment`;
- `source_v555_mediation_slot_status`.

The attractor requirement rows carry a `slot_name`, a generic `requires_v555_mediated_history` status, and symbolic candidate dynamics (`route_axis_1` through `route_axis_6`). The packet explicitly declares itself boundary-only and `ready_for_runtime_consumption = false`.

This is useful governance and staging information, but it is not yet the V556 structural topology implied by the frozen destination. In particular it does not encode a routable causal graph with typed/signed relations, temporal support, reinforcement/destabilization conditions, or actor-initialization priors.

### 1.2 What current V557 preserves

`ddm_v557_renderer_contract.py` reads the V556 packet/readiness and cross-wave harmonization metadata. It preserves:

- V556 run/readiness/status context;
- the existence/count of harmonization evidence;
- the `slot_name` for each V556 pressure-flow slot;
- source/generated/rendered separation rules;
- renderer prohibitions;
- prompt/generation/runtime-authority audit requirements;
- coarse readiness scores;
- blocker and handoff ledgers.

For every V556 slot, `_build_requirements()` creates renderer rows whose semantic payload is essentially the slot name plus boundary flags (`may_render_dialogue = false`, `may_render_voice = false`, `may_render_autobiography = false`), audit requirements, and a V558 handoff row whose `allowed_v558_use` is currently `false`.

### 1.3 What current V557 discards or reduces

V557 does **not** preserve the V556 pressure-flow rows as a runtime-consumable collection. It does not copy through, in a structured form suitable for V558/V3:

- `slot_channel`;
- `source_v555_mediation_slot_status`;
- pressure status/family beyond coarse readiness prose;
- V556 attractor requirement rows;
- candidate-dynamics semantics;
- V556 absence/stop-state semantics as typed runtime priors;
- any future routable topology if it were added only to V556 without a corresponding V557 pass-through contract.

The V557 packet does retain V556 *readiness context*, but readiness context is not a substitute for the structural object being declared ready.

### 1.4 Current V557 prompt-audit defect

The completion-grade V557 prompt audit contains a concrete aggregation bug. `_prompt_audit_rows()` emits a baseline row with `prompt_shape_detected = false`, `prompt_shape_violation_count = 0`, and `prompt_shape_clear = true` when there are no blockers. The packet-level and emitted audit-level summary then computes:

- `prompt_shape_detected = bool(prompt_payload)`;
- `prompt_shape_violation_count = len(prompt_payload)`;
- `prompt_shape_clear = false`.

Because the baseline audit itself is a row, `bool(prompt_payload)` is true even when that row says no prompt shape was detected. A clean baseline is therefore summarized as a prompt violation. V558 treats those aggregate flags as blocking. This is a real current producer/consumer defect, not a future design preference.

### 1.5 What current V558 normalizes/exposes

`ddm_v558_runtime_input_gate.py` reads the V557 readiness report, renderer packet, prompt-shape audit, forbidden-inference audit, and governance inventory. Its `normalized_runtime_input` currently exposes:

- run/root and V557 status fields;
- prompt-shape detected/count/clear/allowed flags;
- V557 packet leak flags;
- `renderer_input_contract`;
- `runtime_wiring_contract`;
- `source_to_generation_separation_ledger`;
- `render_blockers`;
- `memory_governance_requirements` (sourced from V557 `future_consumer_notes`);
- `narrative_governance_requirements` (sourced from V557 `app_wiring_boundaries`);
- handoff/readiness booleans;
- a permission lane and render permission state;
- source-to-generation separation status;
- authority status/source;
- memory/narrative write permissions;
- a single `generated_not_evidenced_flag`;
- blocker identifiers and normalization timestamp.

`ddm_v558_runtime_graft_readiness.py` adds a review decision around V557 presence/status, prompt-shape safety, governance presence, packet leak flags, and authority-document presence. It explicitly remains a review gate and never authorizes the runtime graft.

`ddm_v558_plus_governance.py` adds deployment/evaluation/memory/narrative governance statuses, but likewise does not restore structural information that was never preserved across V557.

### 1.6 Current V557/V558 handoff mismatch

V558 calculates `v558_handoff_requirements_present` by requiring, among other things, V557 `future_consumer_notes` and `app_wiring_boundaries`. Those fields exist in the older/thin `_payload_v557` path, but the completion-grade `ddm_v557_renderer_contract.py` packet instead emits its renderer contract, runtime-wiring contract, separation ledger, blockers, audits, and `blocked_shortcuts`; it does not emit `future_consumer_notes` or `app_wiring_boundaries`.

Thus the current completion-grade producer and current V558 normalizer are not fully shape-aligned even before the future semantic contract is considered.

---

## 2. V558 information-preservation gap table

| Information V3 requires | Current V556 | Current V557 | Current V558 | Required disposition |
|---|---|---|---|---|
| Historically situated structural pressure | Temporal/harmonization authority is referenced; pressure-flow slots are symbolic | Reduced to readiness/harmonization context | Not exposed as runtime priors | Preserve typed pressure priors with time/scope/provenance |
| Nine-strata relations and orientation-to-strata | Not represented in a V3-consumable topology here | Not preserved | Absent | Expose typed relation/orientation slices for all applicable strata, including typed absence |
| Carrier/institutional/household mediation | V555-derived slot/channel names survive partly into V556 | `slot_channel` and mediation status are dropped | Absent | Preserve mediation channel, state, constraints, source layer, uncertainty |
| Position/capacity/reproduction constraints | Not present as a runtime boundary object | Absent | Absent | Expose bounded constraints/affordances, not biographies |
| Expectations/frameworks/buffers/cracks/alienation | Only very coarse symbolic contract concepts (e.g. expectation baseline) | Reduced to slot names/blockers | Absent | Preserve typed prior/state affordances sufficient for V3 initialization |
| Pressure-flow routing | Generic candidate dynamics / route-axis placeholders only | Not preserved as topology | Absent | Future V556 must emit routable typed semantics; V557/V558 must preserve them |
| Attractor formation/reinforcement/destabilization | Attractor requirement rows exist but remain generic | Dropped as structured data | Absent | Preserve attractor candidate semantics, conditions, uncertainty; no final identity assignment |
| Temporal support / validity window | V553 authority is referenced upstream | Only coarse harmonization evidence summary | Absent at item level | Every runtime prior needs temporal scope and interpolation/observation status |
| Per-prior provenance | Mostly run/file/readiness context | Coarse run/layer context | `authority_source` is effectively packet-level | Require stable prior IDs plus producer layer/artifact lineage and hash-bound manifest |
| Per-prior uncertainty | Coarse readiness scores | Coarse readiness scores | No item-level uncertainty | Require typed uncertainty/completeness/bounds where applicable |
| Known absence / unresolved state | Upstream absence/stop ledgers exist | Not normalized as runtime prior state | Mostly blockers, not domain absence | Preserve `VALID_EMPTY`/not-applicable/unresolved/blocked distinctions |
| Causal-use permission | Boundary-level booleans/prohibitions | Renderer/global prohibitions | Global gate state | Add item/collection-level permission: usable as V3 prior vs review-only vs denied |
| Epistemic class | Boundary prose distinguishes source/generation | Separation ledger is prose | One global `generated_not_evidenced_flag = false` | Require item-level source-derived/derived/generated/rendered classification |
| Queryability | Artifact files exist upstream | Renderer packet/indexes | One normalized object | Provide both an immutable bundle manifest and queryable prior slices |

The decisive distinction is between **governance metadata about an upstream object** and **the governed object itself**. Current V558 largely contains the former.

---

## 3. Proposed minimum V558 → V3 runtime information contract

This section specifies information requirements only. It does not prescribe a service, object model, actor algorithm, storage engine, or V3 implementation.

### 3.1 Contract form: both immutable bundle and queryable slices

V558 should expose both:

1. **A one-shot, immutable runtime-prior manifest/bundle** that binds run identity, contract/schema versions, artifact identities/hashes, producer lineage, authority status, completeness, and the complete set of runtime-consumable prior collections. This is necessary for reproducibility, fail-closed validation, and deterministic offline startup.
2. **Queryable prior slices** over the same hash-bound collections, keyed at minimum by prior kind, temporal scope, structural stratum/relation where applicable, geography/scope, and any actor-seed cohort/demographic scope lawfully supported upstream. This allows V3 to load the relevant structural context without reading raw DDM internals or materializing an undifferentiated global payload.

“Queryable” here is an information/interface requirement, not a requirement to build an API or service. Canonical tables plus a manifest can satisfy it.

### 3.2 Required envelope fields

The runtime-prior manifest must, at minimum, bind:

- `contract_version` / schema version;
- V558 run ID and stable bundle ID;
- upstream producer lineage sufficient to identify the V553/V554/V555/V556/V557 derivation chain without V3 fetching those producers;
- artifact content/file hashes for every canonical prior collection;
- scope identity and scope grain;
- build/integrity state;
- evidence/authority state;
- downstream causal-use permission state;
- known-absence/completeness state;
- source/generated/rendered separation policy version;
- explicit statement that the bundle contains no raw survey/DDM rows and no rendered/persona material.

### 3.3 Required metadata on every runtime-consumable prior

Every V3-consumable prior row/object must carry, directly or by a stable foreign key to a hash-bound metadata table:

- stable `prior_id`;
- `prior_kind`;
- structural/temporal/scope identity sufficient to know *what the prior applies to*;
- producer layer and canonical artifact identity;
- opaque lineage/provenance reference sufficient for audit without requiring V3 raw-evidence access;
- `epistemic_class` distinguishing at least source-attested structural evidence, derived structural prior, and later generated runtime fact; V558 should not mislabel derived priors as source facts;
- `authority_status` / evidence status;
- `causal_use_permission` (`ALLOW`, `DENY`, `REVIEW_ONLY`, `NOT_APPLICABLE` or equivalent typed states);
- typed uncertainty/completeness state and, where numerically meaningful, bounds/confidence/support rather than a global readiness score;
- known-absence/unresolved state;
- valid temporal interval/support period and whether the value is observed, harmonized, interpolated, or otherwise derived;
- transformation/version identity sufficient to detect stale or mixed-contract rows.

A packet-level `authority_source` and a single boolean `generated_not_evidenced_flag` are not adequate substitutes for this metadata.

### 3.4 Minimum governed prior collections

The following are the minimum semantic collections V558 must make available if the corresponding upstream authority exists. A collection may be valid-empty or unresolved; absence must be typed rather than silently omitted.

#### A. Structural pressure priors

Must carry the historically situated pressure/context information from which V3 may initialize or constrain actor-specific state, including:

- pressure/context ID and kind;
- affected scope/stratum;
- direction/polarity where defined upstream;
- magnitude/intensity/bounds where defined upstream;
- time support/validity;
- capacity/reproduction/position constraints or affordances when upstream has them;
- uncertainty and authority metadata.

These are structural priors, not person beliefs or memories.

#### B. Nine-strata relation and orientation priors

For each applicable relation:

- source/target stratum identity using the canonical nine-strata ontology;
- relation/orientation type;
- directionality and position semantics;
- temporal/scope support;
- applicable/unresolved/not-applicable state;
- authority, permission, and uncertainty metadata.

V3 must be able to tell the difference between “no relation is applicable,” “relation evidence is unresolved,” and “relation data was accidentally dropped.”

#### C. Mediation constraints

Household/caregiver, carrier, institutional, and other mediation information may cross only as bounded structural/generative constraints:

- mediation channel/type;
- applicability/state;
- bounded influence/constraint semantics when upstream has them;
- temporal support;
- source layer/lineage;
- uncertainty/permission.

No named parent psychology, household biography, membership-as-fact, or invented life event crosses V558.

#### D. Pressure-flow topology semantics

Future completion of V556 must provide, and V557/V558 must preserve, the minimum routable semantics required to realize pressure flow rather than merely name it:

- stable topology node/route identifiers;
- typed/signed relation or transition semantics;
- structural/mediation inputs each route depends on;
- gating/precondition state;
- reinforcement, attenuation, contradiction, destabilization, or transformation conditions where those concepts are part of the upstream contract;
- temporal applicability;
- uncertainty and provenance.

R0-04 does **not** specify the V3 update equations or require any particular graph library. The requirement is only that the information needed for causally attributable routing not be collapsed into prose such as “candidate dynamics only.”

#### E. Attractor priors

To support the frozen Enneagram-like destination without survey-to-type inference, V558 must preserve:

- attractor candidate/axis identity from V556;
- formation prerequisites;
- reinforcement/destabilization affordances or route dependencies;
- uncertainty/permission;
- explicit prohibition on treating candidate/axis information as a finished personality or Enneagram type.

The canonical actor-specific attractor state is generated later by V3 and must be labeled generated runtime state.

#### F. Typed absence / unresolved ledger

V558 must carry a runtime-consumable ledger distinguishing at least:

- present/usable;
- valid empty / not applicable;
- applicable but unresolved;
- review-only;
- blocked/denied;
- missing/corrupt integrity failure.

Missing and not-applicable are not interchangeable.

### 3.5 Minimum V3 initialization inputs

A reference V3 consumer should be able to initialize a **test actor context**, without generating a full actor implementation, from V558 alone using:

- actor/runtime seed identity supplied by the runtime caller, not inferred from survey respondents;
- simulation time/origin and structural scope;
- the applicable structural pressure slices;
- nine-strata relation/orientation slices;
- applicable mediation constraints;
- pressure-flow/attractor topology priors;
- typed absence/unresolved state;
- per-prior provenance, uncertainty, and permission.

V3 may then generate actor-specific state/history under its own jurisdiction. V558 should not contain a finished psyche, autobiography, or voice merely to make initialization convenient.

---

## 4. Explicit forbidden-crossing list

The following must not cross V558 into V3 runtime input as causally authoritative actor facts or prompt material:

1. Raw survey/DDM respondent rows or microdata.
2. Raw response values, option text, question wording, or respondent-level evidence re-expressed as person memory/belief.
3. Review-only or denied upstream evidence stripped of its permission state.
4. Unmediated structural aggregate values presented as direct individual traits.
5. Source claims converted into autobiography.
6. Finished biography, household story, named parent psychology, or carrier membership not generated by the runtime with explicit generated lineage.
7. Finished psyche/profile/persona.
8. Dialogue, voice samples, speaking style, prompt text, or V2-rendered narration.
9. Direct survey/country/region-to-Enneagram assignment or a V556 attractor candidate relabeled as final identity.
10. V2 prose or self-narration treated as causal authority for V3 state mutation.
11. User messages that directly mutate V3 state without first becoming an explicit V3-mediated runtime event.
12. Priors with missing scope, authority, permission, temporal validity, or epistemic class when those omissions make causal interpretation ambiguous.
13. Generated values presented as source-attested evidence.
14. Raw-upstream fetch handles that make V3 depend on reaching behind V558 to recover missing semantics. Audit lineage references may be retained, but V3 must not require raw upstream retrieval to operate.
15. Rendered outputs written back into source or structural provenance stores.

---

## 5. Proposed minimum V3 reference-consumer assertions

These assertions can be implemented before the full V3 engine exists. They validate the V558 contract rather than simulate an actor.

### Contract and integrity

1. The V558 manifest has a recognized contract/schema version and binds all required canonical prior artifacts by content/file hash.
2. Run/scope identities are coherent across manifest and prior slices; cross-run or cross-scope mixing fails closed.
3. Valid-empty/not-applicable collections pass integrity without being coerced into “present,” while missing/corrupt required artifacts fail closed.
4. Every consumable prior has a typed authority/evidence state and causal-use permission.

### Provenance and epistemic separation

5. Every consumable prior has stable lineage and an epistemic class; derived priors cannot silently become source-attested facts.
6. No raw respondent-level survey/DDM material, raw question/response text, dialogue, voice, autobiography, or persona fields are present in the V3 runtime input collections.
7. Review-only/denied priors cannot be selected as causal inputs.
8. Generated runtime facts, when a future V3 produces them, must receive new generated lineage and never overwrite the V558 source/derived provenance class.

### Semantic sufficiency

9. The consumer can select structural priors by simulation time/scope without reading V553–V557 directories.
10. Applicable nine-strata relation/orientation rows retain canonical source/target strata plus direction/position semantics; unresolved/not-applicable rows remain distinguishable.
11. Mediation constraints retain channel/type and applicability rather than only a slot name.
12. Pressure-flow topology data is machine-routable/typed and is not reducible to blocker prose or a list of generic route-axis labels.
13. Attractor candidate semantics survive as candidate/formation constraints, while any field that directly assigns a finished Enneagram/personality identity is rejected.
14. Item-level temporal support and uncertainty survive normalization.

### Causal-jurisdiction guard

15. A synthetic “user interaction” or environmental occurrence used by a future reference harness is accepted only as a typed **event proposal/input** to V3; it cannot directly overwrite causal state.
16. The V558 bundle contains enough information to construct a minimal V3 initial-context fixture without raw-upstream access. The assertion does not require implementing V3’s evolution algorithm.

These tests should reuse the existing strict-boundary patterns for hashes, scope identity, typed empties, evidence/permission states, and fail-closed behavior.

---

## 6. Proposed minimum V3 → V2 boundary

V2 must remain phenomenological/rendering jurisdiction. The minimum boundary therefore needs a read-only, versioned projection of generated V3 state/history plus a controlled event-return path.

### 6.1 Information V3 may expose to V2

A minimum V3→V2 render context should carry:

- actor/runtime identity;
- immutable V3 state version and simulation time;
- generated causal-state facts/constraints that V2 is permitted to express, each with generated provenance and renderability/visibility rules;
- selected event-history projection: event IDs/types/times and V3-governed memory/access/salience/reliability constraints needed for phenomenological expression;
- current attractor/pressure-flow consequences only as generated V3 state, not as raw V556 evidence;
- public/private/intimate availability constraints or equivalent access labels where V3 has causally determined them;
- typed uncertainty/ambiguity needed to prevent V2 from converting indeterminate state into certainty;
- explicit `causal_write_permission = false` for V2.

V2 may transform this material into noticing, remembering, naming, hiding, misrecognition, symbolization, desire, self-narration, voice, and conversation. Those renderings are downstream outputs, not new structural authority.

### 6.2 Controlled return path

If V2/user interaction should affect the actor:

1. V2 emits a typed interaction/event proposal containing the user/environmental occurrence and the V3 state version against which it occurred.
2. V3 accepts/rejects/mediates that event under its causal rules.
3. V3 appends an explicit event and any resulting state mutation with generated provenance.
4. V2 receives a new read-only state/history projection.

There is no direct V2 state write-back and no route from rendered prose to source-attested authority.

### 6.3 Source/generated/rendered separation at this boundary

The minimum epistemic classes must remain distinguishable across the runtime:

- **source/derived structural prior** — arrives through V558 and remains auditable;
- **generated runtime fact/state/event** — becomes canonical within the simulation because V3 generated/accepted it, while remaining epistemically generated;
- **rendered phenomenology/narrative/dialogue** — V2 expression of runtime state and history, never retroactively source authority.

---

## 7. Existing tests: useful patterns and obsolete/misleading assumptions

### 7.1 Tests that remain useful as contract patterns

`tests/test_w05_pipeline_boundary_contract.py` contains patterns that should be retained/generalized for V558→V3:

- anchored typed status interpretation rather than substring permission;
- contradiction rejection (`ALLOW` cannot coexist with failed integrity);
- valid-empty versus corrupt artifact distinction;
- strict manifest identity and artifact-hash binding;
- fail-closed behavior on hash mismatch;
- canonical machine-output policy and stale-safe publication.

`test_w03_v551j_v3_consumer.py`, `test_w03_v551j_v3_fail_closed.py`, and `tests/test_w05_v551_v3_consumer.py` also contain reusable *boundary-testing patterns*:

- preserve typed `PRESENT` / unresolved / not-applicable states;
- preserve neutral/review semantics;
- demote/deny on incomplete authority;
- reject unexplained missing promotable artifacts;
- reject wrong hashes and scope identities;
- allow typed empty bundles.

`tests/test_w05_final_cross_stage.py` reinforces useful invariants around typed empties, hash-bound lineage, integrity-versus-permission separation, canonical Parquet output, and cross-scope rejection.

### 7.2 Misleading/obsolete interpretation to reject

The filenames/symbols `v551_v3_consumer` refer to the **V551 v3 producer/schema contract**, not to the future V3 causal/temporal actor runtime described in this assignment. These tests are not evidence that a V558→V3 runtime consumer already exists. Reusing their fail-closed mechanics is correct; treating their payload shape as the future actor-runtime contract is not.

Likewise, current cross-stage tests that terminate around V551/V552/V552J prove upstream boundary integrity, not downstream semantic sufficiency for V3. Presence/readiness of V557/V558 governance artifacts cannot substitute for assertions that the structural priors themselves survive to V558.

### 7.3 New test focus required in the implementation wave

Future V557/V558 tests need to assert **semantic conservation**, not merely safe blocking:

- V556 runtime-prior fields that are authorized for V3 must survive V557 and V558 with IDs, values/types, scope, provenance, uncertainty, and permission intact;
- forbidden raw/rendered fields must still be absent;
- a legal clean prompt audit must stay clean across V557→V558;
- V557 and V558 must agree on required handoff field names/shapes;
- V558 must be sufficient for a reference V3 contract consumer without upstream reads.

---

## 8. Findings

### R0-04-F001 — Current V556 is not yet a V3-sufficient pressure-flow topology

**Class:** SEMANTIC_GAP  
**Severity:** BLOCKING for eventual V3 runtime graft; not a Wave 0 execution blocker.

Current V556 is a lawful boundary contract, but its pressure-flow rows and route-axis placeholders do not yet encode the causal topology/attractor semantics the frozen V3 destination requires. This is a cross-hook for the V556 completion prong. R0-04 does not prescribe the algorithm; it requires that future semantics be explicitly serializable and preservable downstream.

### R0-04-F002 — V557 performs substantive information reduction

**Class:** INFORMATION_LOSS  
**Severity:** HIGH.

V557 derives renderer rows from V556 slots but carries forward mainly `slot_name` plus prohibitions/audit flags. It does not preserve V556 slot-channel/mediation status, attractor requirements, or a structured pressure-flow object. A future V556 topology would also be lost unless the V557 contract is explicitly changed to preserve authorized runtime priors.

### R0-04-F003 — V558 normalized input is governance-rich but causally starved

**Class:** INFORMATION_LOSS / INTERFACE_REQUIREMENT  
**Severity:** BLOCKING for future V3 consumption.

The normalized object exposes statuses, prompt flags, renderer contracts, ledgers, blockers, and global permissions, but no structural pressure, strata relation, mediation, temporal, uncertainty, or attractor prior collections. V3 cannot meet its frozen responsibilities from this object alone.

### R0-04-F004 — Provenance/uncertainty/permission are too coarse for causal use

**Class:** INTERFACE_REQUIREMENT  
**Severity:** HIGH.

Current authority/readiness is largely packet-level. A causal runtime needs item/collection-level provenance, temporal support, epistemic class, uncertainty/completeness, and causal-use permission to avoid converting aggregate or derived claims into individual facts.

### R0-04-F005 — Completion-grade V557 prompt-audit aggregation creates false violations

**Class:** DEFECT  
**Severity:** BLOCKING for the current V558 gate.

A baseline audit row explicitly marked clear is nevertheless summarized as `prompt_shape_detected = true`, nonzero violation count, and `prompt_shape_clear = false` because aggregate state is calculated from audit-row presence rather than the row’s violation fields. V558 correctly blocks on those aggregate flags, so the producer summary must be fixed rather than relaxing V558.

### R0-04-F006 — Completion-grade V557 and V558 disagree on required handoff fields

**Class:** DEFECT / INTERFACE_REQUIREMENT  
**Severity:** HIGH.

V558 requires `future_consumer_notes` and `app_wiring_boundaries` to mark handoff requirements present. Those fields are not emitted by completion-grade `ddm_v557_renderer_contract.py` (though related fields existed in the thin path). Producer and consumer must share one canonical shape.

### R0-04-F007 — Existing `v551_v3_consumer` tests are not future V3 runtime tests

**Class:** HAZARD  
**Severity:** MEDIUM.

Their integrity patterns are valuable, but the “v3” label denotes the V551 v3 producer/schema contract. Counting them as V3 actor-runtime coverage would conceal the actual V558→V3 gap.

---

## 9. Producer → consumer obligations

### V556 → V557

**Must preserve:** future pressure-flow topology semantics, attractor candidate semantics, mediation linkage, temporal/scope identity, typed absences, provenance/uncertainty/permission.  
**May transform:** storage shape, indexing, naming/version wrappers, provided semantic identity is conserved and auditable.  
**Must not infer:** finished psyche, Enneagram type, voice, autobiography, person belief.

### V557 → V558

**Must preserve:** all runtime-authorized V556 prior semantics plus source/generated/rendered separation and rendering prohibitions.  
**May transform:** normalize into canonical runtime-prior tables/manifest and attach governance metadata.  
**Must not infer:** missing persona facts, dialogue, voice, biography, or additional causal claims.

### V558 → V3

**Must preserve/expose:** structural/relational/mediation/pressure-flow/attractor priors with temporal scope, typed authority, item-level provenance, uncertainty, epistemic class, and causal-use permission.  
**May transform:** select/query applicable slices and copy them into V3 initial context while retaining lineage.  
**Must not infer:** actor-specific state from raw survey rows; survey-to-Enneagram identity; source-attested memories/biography.

### V3 → V2

**Must preserve:** generated runtime state/event history identity and version, renderability/access constraints, generated provenance, uncertainty.  
**May transform:** V2 may produce phenomenological expression and conversation.  
**Must not infer/write:** V2 cannot directly mutate causal state, rewrite source provenance, or make rendered prose causally authoritative.

---

## 10. Cross-hooks required

### R0-04-H001 — V556 completion prong

**Blocking for future runtime adequacy:** yes.

Future V556 completion must emit a machine-preservable pressure-flow/attractor structural object sufficient for downstream causal routing, with typed provenance/uncertainty/absence. R0-04 does not authorize or prescribe the dynamics implementation.

### R0-04-H002 — V557 completion prong

**Blocking:** yes.

V557 must stop collapsing runtime-authorized V556 semantics into slot-name/blocker rows; instead preserve the authorized structural priors while adding renderer/governance separation. It must also fix the prompt-audit aggregate defect and align its handoff shape with V558.

### R0-04-H003 — V558 completion prong

**Blocking:** yes.

V558 must normalize the preserved priors into a hash-bound runtime-prior manifest plus queryable slices, attach item/collection-level provenance/uncertainty/permission, and remain free of raw DDM and rendered/persona material.

### R0-04-H004 — Future V3 prong

**Blocking for final runtime integration, not Wave 0:** yes.

V3 should consume V558 only, validate the contract fail-closed, generate actor-specific causal state/events with generated lineage, and expose all causal changes through explicit event/state history. This is a consumer obligation, not an implementation request from R0-04.

### R0-04-H005 — Future V2 prong

**Blocking for final phenomenological integration, not Wave 0:** yes.

V2 requires a read-only V3 state/history projection and may return only typed interaction/event proposals for V3 mediation. No direct causal write-back.

---

## 11. Acceptance evidence

R0-04 acceptance requirements are met by this report:

- current V557→V558 trace: Sections 1.1–1.6;
- V558 information-preservation gap table: Section 2;
- proposed minimum V558→V3 contract: Section 3;
- explicit forbidden-crossing list: Section 4;
- proposed V3 reference-consumer assertions: Section 5;
- proposed minimum V3→V2 boundary: Section 6;
- existing-test disposition: Section 7;
- concrete findings and cross-hooks: Sections 8–10;
- no V3/V2/genealogy implementation or broad V557/V558 rewrite performed.

## 12. Vozhd decision requested

Accept R0-04 findings for integration and route the blocking cross-hooks to the V556, V557, V558, and later V3/V2 implementation prongs. The most immediate repair order is:

1. fix the concrete V557 prompt-audit aggregation defect and canonical V557↔V558 field-shape mismatch;
2. define/implement the future V556 topology semantics in its owning prong;
3. make V557 semantically conservative over runtime-authorized V556 priors;
4. make V558 the sole governed, hash-bound, queryable prior boundary consumed by V3;
5. validate with a reference consumer before building out V3 evolution behavior.

That order prevents downstream code from being written against a causally empty normalization surface.