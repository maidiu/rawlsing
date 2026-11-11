# CAN-012 — V3 Rupture & Metabolization Canonicalization

**Assignment:** `W1-B02-05`  
**Canonicalization:** `CAN-012`  
**Canonical contract:** `V3_RUPTURE_METABOLIZATION_RULESET@1.0.0`  
**Owner:** `V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w1-can-012-v3-rupture-metabolization`  
**Exact base SHA:** `c84ce0704ae33f0226e9603738c1752fa19823fd`  
**Mode:** authority canonicalization only; no production code; no V3 implementation  
**Verdict:** `PASS`

## 1. Binding holding

CAN-012 canonicalizes the recovered rupture/metabolization mechanism as **actor-specific generated developmental causality with exact causal parentage**.

The terminal law is:

```text
structural pressure / adverse circumstance / event label
    != rupture

already-generated/admitted causal event(s)
+ exact actor-specific prior causal state/history
+ exact CAN-012 rupture rule
+ complete authority/provenance
    -> rupture candidate court
    -> ADMITTED_RUPTURE | lawful nonadmission | deferred | denied | integrity failure

ADMITTED_RUPTURE
    -> immutable rupture causal history
    -> persistent metabolization-process tracker
    -> 0..n later rule-governed process transitions/effects
```

An admitted rupture is not a wound, belief, memory, attractor, Enneagram type, moral lesson or rendered story. A metabolization process is not a promise of healing. It may remain raw, active, provisional, sealed, chronic, recurrent, partially reorganized, integrated with residue, or unchanged for as long as the generated history and governing rules warrant.

The recovered code's strongest idea survives: a rupture can persist as a causal problem across later life and can be reactivated or reorganized by later events. Its weakest idea does not: age bands, adverse labels, module-global randomness, default psychological values, template priors and hard-coded thresholds may not manufacture that causal history.

`MUST-018` remains the sole attractor-transition authority. CAN-012 may publish exact rupture/metabolization history that a later attractor rule consumes; it cannot perform the transition.

## 2. Authority hierarchy and jurisdiction

This result obeys, in order, the Batch-02 register, accepted V3/whole-machine architecture, accepted W0/W1 authority, recovered explicit source semantics, and `RAWLSING_GOVERNING_SPIRIT.md` only as a tie-break inside genuine lawful ambiguity.

### CAN-012 owns

- actor-specific rupture candidate evaluation and admission semantics;
- the immutable V3 causal rupture record;
- persistent metabolization-process identity tied to an admitted rupture;
- CAN-012-owned process-state transitions, persistence, recurrence/reactivation and lawful no-change;
- CAN-012 transition/effect receipts and replay provenance;
- the boundary by which a CAN-012 transition may propose/apply a typed effect to another already-governed V3 state owner.

### CAN-012 does not own

- V550+ structural pressure, route, topology or producer semantics;
- opportunity/encounter/exposure generation (`ADP-010`);
- V555 route realization or V556 F1/F2 realization/satisfaction;
- framework, wound, practice, material, need, expectation or other neighboring V3 state semantics merely because historical rupture code wrote those fields;
- causal memory (`ADP-016`) or actor knowledge/claim accessibility (`ADP-017`);
- external-event admission (`ADP-019`);
- causal randomness (`ADP-020`);
- scheduler precedence or universal slow cadence (`ADP-021`);
- attractor transition/type/interpretation (`MUST-018`);
- V2 phenomenology, narration or expression.

The closed V3 event-family law remains intact. Rupture/metabolization stays inside the bounded V3 developmental event/state-transition vocabulary; CAN-012 does not create a new ontology sink.

## 3. Required archive verification and direct source court

Required archive: `Rawlsing_code_bundle_staging.zip`.

- Expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- Directly computed SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- Verdict: `EXACT_MATCH`
- ZIP entries: `13,138`

Recovered V3/V2/server code is continuity/authority-recovery evidence only. Historical V5/DDM has zero authority over current V550+.

Directly inspected recovered rupture/metabolization source, state, config, coupling and tests include:

| File | SHA256 | Role |
|---|---|---|
| `v3/engine/effects/metabolization_effects.py` | `d4775271ca097e99e615cee19b381a478ad6d90a25051c5fce1b1e0e3c1adb1e` | primary recovered rupture/metabolization implementation |
| `v3/core/state.py` | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` | `RuptureShard`, `MetabolizationProcess`, `NarrationSupport`, persistent state |
| `v3/engine/effects/delta_templates.py` | `7d99ddf26fd45b52e5e3c10074066ba5e06d17cdaf1fabad06298af3770815f0` | event-to-rupture/reactivation coupling |
| `v3/engine/yearly_step.py` | `da3147c3da7ff2724a61dd26d595055668899c83beb541400f58633568b92acb` | historical annual invocation/cadence coupling |
| `v3/engine/effects/rupture_templates.yaml` | `8c1821659a5335b511555b3c41b0a3b67fee9a05793e91afd1bfe29deafa7c94` | event-specific age/severity/mode/narrator priors |
| `v3/engine/rupture_templates.yaml` | `d15b5644f23c587fb9eb6184a39c22b4c663510bf5ba9f9e2151305b28afd929` | age-band template priors |
| `v3/systems/stability_inertia.py` | `5a11c8b07eafe2b8f1d7e9864c9cb066a5c45f19c2c45a8d4223b3a64c394c78` | persistence/dissipation/reactivation coupling |
| `v3/tests/test_metabolization_effects.py` | `8152dda6f99ac6d019e7f6234bda79e8c11cc8773cf9728635905ddd80a323ef` | historical mechanism tests |
| `v3/tests/test_wave4.py` | `10f8978cf5cfdd52395102ba7b1c01d7475ffaf14665a3edfd50b60249e60e90` | automatic selected-event rupture behavior test |
| `v3/specLLM.txt` | `52df5549828701c400d0b0815a1c0025eb9c7b54c7c28283c239680e0a634a18` | recovered explicit rupture/metabolization semantics |
| `v3/HOW_BASELINE_STRIVING_MAGNETS_RUPTURE_WORK.md` | `308ab6ef75e6e31e63f00f4626a9fcc22b14035a45a62654a04271619b7e9867` | historical wiring description |
| `v3/docs/STABILITY_INERTIA_MAXIMAL_SPEC.md` | `2069588c1d28223f16e0802196b9dcad7f99075a63f708e736c84123ec099d61` | heuristic status/recurrence proposal |
| `v3/v3_yearly_step_order.yaml` | `90496a2cc852ca00ef99c8bd4fcb2b41c9aa43c4aaa9108d3ac8cce0ebe22ffc` | historical annual step order |
| `v3/io/json_codec.py` | `c4bc07dd73c249c35d788f5b459f4b0c1b23702a7d55157a4eb3fdbc74b1cf14` | persistence/default evidence |
| `v3/core/invariants.py` | `81298f3fc51b46cda8d72d0db914b672b17b9a35e13004fe59a9b0e29dada5e3` | legacy clamping/integrity terrain |
| `v3/engine/llm_contract.py` | `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf` | historical rupture candidate parsing; LLM proposal is nonauthority |
| `v3/engine/scoring.py` | `36833287c72ffa40d0ece1ebc66fb0d685a92fc71aab1d211be9b21bfd0a82cb` | proposal selection seam evidence |
| `v3/engine/run_llm_band.py` | `120e177462219e8ccd5d5e0d7fdb23de993639f5af8be6c40a06db36e0b37a38` | candidate execution seam evidence |
| `v3/io/persona_sheet.py` | `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e` | downstream narrative projection; noncausal here |
| `v3/engine/active_magnets.py` | `68a7b75aa4bb98f7251f72a05747425edb40d24edbe06611ce998e7b6c26a391` | plasticity-window consumer; neighboring state seam only |
| `v3/systems/cracks.py` | `b11a87e87be216d78c84f76ff645e26a39bb40512475558c95a279c78796bec3` | plasticity-window consumer; neighboring state seam only |
| `v3/systems/frameworks.py` | `0d59fc6e177009da92e39eb61ea729eace97f50392baa93999cb6513f81dd2cb` | plasticity-window consumer; neighboring state seam only |
| `v3/core/derived.py` | `a11d270d80981478ca5820e232a7664cd6dd22d08e359819331574351c7e9673` | stability/metabolic derived consumer; not CAN-012 authority |

Focused historical test court:

```text
PYTHONPATH=. python -m pytest -q v3/tests/test_metabolization_effects.py v3/tests/test_wave4.py -q
20 passed
```

The tests prove the recovered mechanism exists. They do **not** constitutionalize legacy shortcuts. In particular, a historical test asserting that every selected `epistemic_rupture` creates a shard/process is evidence of behavior to adapt, not terminal proof that a label self-admits rupture.

Current-repo terrain was also checked. No current terminal V3 rupture/metabolization production implementation is present at this base; V3 production remains unreleased. Historical source therefore cannot be mistaken for current implementation authority.

## 4. Recovered mechanism disposition

| Recovered mechanism | Disposition | Canonical holding |
|---|---|---|
| persistent `RuptureShard`-like record | `ADAPT` | Preserve immutable actor-specific rupture history keyed to exact causal parents and rule/admission provenance. Historical free-text domain/assumption/default fields are not sufficient semantic identity. |
| persistent `MetabolizationProcess`-like record | `PRESERVE_ADAPT` | Preserve one persistent process tracker per admitted rupture as the time-extended locus for later governed transitions. Process existence is not proof that beneficial change occurred. |
| prediction-error / opacity distinction | `ADAPT` | Preserve as optional governed qualitative classifiers with exact classifier-rule/basis refs. Never default missing values to `medium`. |
| raw/working/provisional/integrated/sealed/chronic process states | `ADAPT` | Preserve branching persistent-state meaning; no universal transition graph, threshold or guaranteed progression. |
| assimilation/accommodation/sealing/collapse/transmutation/mis-aim modes | `COMPATIBILITY_ONLY` | May appear only under a separately bound CAN-012 classifier/transition rule. No default mode or mode-effect formula. |
| persistence and reactivation | `PRESERVE_ADAPT` | Preserve path dependence and recurrence; replace string/domain keyword matching with exact later causal-event/state refs and rule predicates. |
| `maybe_inject_rupture_at_band_age` | `REMOVE_REJECT` | Global RNG + hard-coded age probabilities fabricates rupture without actor-specific causal parentage. |
| nearest-age template and severity/mode/narrator priors | `COMPATIBILITY_ONLY_QUARANTINED` | Historical design evidence only; age brackets and priors are not terminal semantic authority. |
| unnamed `_sample_from_priors` / mode sampling | `REMOVE_REJECT` | Implicit `Random()`, float weights and fallback defaults violate ADP-020. |
| direct rupture-domain -> wound-vector mutation | `REMOVE_REJECT` | Rupture does not automatically create a wound or choose its dimension; middle-state ownership remains separate. |
| rendered-narrative keyword -> `NarrationSupport` | `REMOVE_REJECT` | Rendered text is not causal truth; support/relationship effects require exact generated/admitted V3 inputs. |
| cluster deltas / mode scalars / malheur multiplier / downstream biases | `COMPATIBILITY_ONLY_QUARANTINED` | Preserve only a typed effect-target interface; formulas/bias labels are under-governed. |
| numeric plasticity window / susceptibilities | `COMPATIBILITY_ONLY_QUARANTINED` | Time-extended susceptibility is continuity evidence, but 1–3 years and fixed sensitivities are not governed. No canonical plasticity scalar is created here. |
| stability-threshold inertia / heuristic dissipation | `COMPATIBILITY_ONLY_QUARANTINED` | Persistence/residue evidence only; scalar inertia, drains, annual leak and transition thresholds are not CAN-012 authority. |
| annual metabolization update | `ADAPT` | Preserve slow-process invocation interface only; ADP-021 owns scheduling and CAN-012 authorizes no default annual cadence. |
| JSON persistence / roundtrip | `PRESERVE_ADAPT` | Preserve stable persistence/replay identity; remove defaults that turn missing data into `medium`, `major`, `accommodation` or `50`. |
| plasticity consumers in magnets/cracks/frameworks/derived state | `SEAM_EVIDENCE_ONLY` | Inspected because coupled historically. CAN-012 does not acquire those state owners or authorize automatic changes. |
| historical tests | `COMPATIBILITY_ONLY` | `20 passed` proves recovered behavior exists; automatic rupture tests are not terminal acceptance criteria. |

The recovered semantic core is therefore narrower and stronger than the legacy implementation: an epistemic rupture is more than a bad event; it is a generated actor-specific mismatch that persists in causal history, may be reorganized/sealed/reactivated by later history, and need not resolve toward a beneficial end.

## 5. Rupture candidate / admission / transition contract

### 5.1 Candidate is noncausal

A `RuptureCandidateEvaluation` or terminal equivalent is an evaluation record, not a causal event. It cannot advance the V3 causal cursor.

Every candidate requires:

1. exact `actor_id`;
2. `1..n` exact already-generated/admitted V3 causal `parent_event_ref`s, including at least one precipitating parent;
3. exact actor causal-state/checkpoint identity **before** the precipitating event;
4. `1..n` exact actor-specific `rupture_basis_ref`s from separately governed generated state/history sufficient for the CAN-012 rule to evaluate the mismatch;
5. exact CAN-012 rule ID/version/content hash;
6. exact effective time and DevelopmentalEventLedger anchor;
7. exact causal-use permission/provenance for every required input;
8. ADP-020 stochastic inputs/receipts only when the CAN-012 rule explicitly declares a stochastic branch.

Insufficient on their own:

- a structural row/ref or pressure magnitude;
- prevalence, geography or demographic category;
- adverse-event label/intensity;
- historical template age/severity prior;
- analyst interpretation;
- V2/persona/rendered narrative.

### 5.2 Actor basis without belief invention

The recovered field `violated_assumption` is not canonical first-person belief authority.

Terminal CAN-012 stores exact `rupture_basis_ref[]` to already-generated actor causal state/history. If another accepted state owner provides an expectation, organizing framework, striving, orientation or terminally equivalent basis, CAN-012 may reference it. If no lawful basis exists, the rupture court returns `DEFERRED_REQUIRED_ACTOR_CAUSAL_BASIS`; it does not fabricate a sentence about what the actor believed.

Recovered `prediction_error` and `opacity` preserve useful distinctions, but `LOW/MEDIUM/HIGH` is populated only with exact classifier rule/version and basis refs. Missing remains `UNRESOLVED`; `medium` is not a default.

Historical `micro/major/malheur` severity is compatibility vocabulary unless an exact rule defines it. There is no universal trauma threshold or canonical `malheur` numeric gate in CAN-012 v1.

### 5.3 Admission dispositions

Every rupture candidate terminates in exactly one state equivalent to:

- `ADMITTED_RUPTURE`;
- `VALID_EMPTY_NO_GOVERNED_RUPTURE_BASIS`;
- `VALID_EMPTY_LAWFUL_NONADMISSION`;
- `DEFERRED_REQUIRED_ACTOR_CAUSAL_BASIS`;
- `DEFERRED_REQUIRED_RULE_AUTHORITY`;
- `DENIED_CAUSAL_USE`;
- `INTEGRITY_FAILURE`.

`VALID_EMPTY_*` is healthy. An event may be painful, important or consequential under another V3 rule without qualifying as a CAN-012 rupture.

### 5.4 Admission mutation

On `ADMITTED_RUPTURE`, V3 commits one bounded rupture/metabolization causal event or terminal equivalent and persists:

- immutable rupture-event identity;
- actor/effective-time identity;
- exact parent event refs;
- pre-state/checkpoint hash;
- rupture-basis refs;
- CAN-012 rule/admission receipt;
- optional governed qualifier/classifier refs;
- ADP-020 Decision/Draw receipts if stochastic;
- event/history hashes.

Admission creates exactly one persistent process tracker keyed to the rupture in v1. **Creating the tracker does not assert that metabolization has occurred or that change is beneficial.**

Any nonadmission/deferred/denied/failure result creates no rupture event/process.

## 6. Metabolization process / effect / state contract

### 6.1 Process identity

A `MetabolizationProcessRecord` or terminal equivalent is actor-owned generated causal state associated with exactly one admitted rupture in v1.

Multiple processes may coexist. They are never automatically merged, averaged, winner-selected or made a personality descriptor.

The process begins in `RAW`: rupture is admitted, but no later process transition has yet been established.

### 6.2 Canonical process states

| State | Canonical meaning |
|---|---|
| `RAW` | Admitted rupture is present in causal history; no subsequent metabolization transition is established. |
| `WORKING` | One or more governed post-rupture process transitions are active; direction or value is not implied. |
| `PROVISIONAL_ORGANIZATION` | A governed provisional reorganization exists. Historical `provisionally_narrated` is compatibility-only; this does not assert actor belief or rendered narration. |
| `INTEGRATED_WITH_RESIDUE` | The rupture has been incorporated into current developmental organization under a governed rule while preserving causal residue/reactivation possibility. It does not mean healed, resolved, true, good or morally improved. |
| `SEALED` | A governed process is persistently closed/blocked/compartmentalized under its own rule. It may persist or later reactivate with exact causal parentage. |
| `CHRONIC` | Persistent/recurrent unresolved process under generated history. It is a developmental process state, not a medical diagnosis or personality label. |

These are process states, not a mandatory ladder. CAN-012 v1 binds no universal state-transition graph. Every edge requires a versioned CAN-012 rule and exact causal parents. A process may remain in the same state indefinitely.

### 6.3 Modes are optional compatibility vocabulary

Recovered `assimilation`, `accommodation`, `sealing`, `collapse`, `transmutation`, `mis_aim` are not universal required fields and receive no default probabilities.

A registered CAN-012 rule may assign a process mode only when it defines semantics, inputs, classifier, provenance and—if stochastic—the ADP-020 contract. Without that rule, mode is unresolved/not-applicable. `accommodation` is never fallback truth.

### 6.4 Typed effects and neighboring owners

One admitted process transition may carry `0..n` typed effects. CAN-012 does not thereby acquire ownership of the target state.

A cross-state effect must identify:

```text
source CAN-012 transition
+ target state owner/authority/rule
+ exact target state ref or allowed creation contract
+ exact operation/before-state identity
+ exact resulting state/effect identity
+ provenance/replay hashes
```

If target authority is absent or does not admit the effect, the effect is valid-empty/deferred. CAN-012 may not replace absence with a wound increment, framework switch, capacity delta, expectation bias, narrative interpretation or attractor move.

A claimed CAN-012 causal transition commits all mandatory CAN-012 state/effects and provenance atomically. Missing mandatory reference/hash/rule/RNG receipt blocks it; partial causal mutation is forbidden.

## 7. Causal parentage

### Rupture

```text
1..n already-committed/generated V3 causal events
or ADP-019-admitted external events
+ exact pre-event actor-state/checkpoint
+ exact actor-specific rupture-basis refs
+ exact CAN-012 rule/admission receipt
```

Structural references may remain transitively in those parents' provenance, but they are never sufficient rupture parents by themselves.

### Metabolization transition

```text
prior process-state hash
+ exact later generated/admitted event/state refs required by rule
+ exact transition/effect rule
+ scheduler trigger/receipt refs when invoked through ADP-021
+ ADP-020 Decision/Draw receipts when stochastic
```

A relationship, support, explanation, practice, loss, repeated encounter or other later influence matters only after its own owner has generated/admitted the causal fact. Historical narrator strings and prose keywords are not causal inputs.

### V2 / external interaction

Rendered text cannot parent CAN-012. If observable conversation changes the generated actor, it must first re-enter V3 and be admitted under ADP-019 as a new causal event. Only that admitted event may appear in CAN-012 parentage.

## 8. Persistence, recurrence and lawful no-change

1. An admitted rupture remains immutable causal history even if process state later changes.
2. A process may persist in any governed state indefinitely.
3. `INTEGRATED_WITH_RESIDUE` preserves causal residue and reactivation possibility; integration does not erase the rupture.
4. Reactivation/recurrence requires exact later causal parentage and a versioned rule. Keyword/domain/string trigger matching is forbidden.
5. A process evaluation may yield `NO_CHANGE`. It may receive a replay/scheduler receipt, but creates no pseudo-event and does not advance the causal cursor solely because it was evaluated.
6. No absence of change is interpreted as resistance, repression, healing, failure, pathology or success unless another explicit authority establishes that meaning.
7. A life with zero rupture records/processes is valid and complete.

The same precipitating event may lawfully produce different results for different actors because CAN-012 evaluates each actor's exact generated history and state. The same actor may also develop differently under later divergent events. Randomness may contribute only where exact rule authority permits bounded contingency under ADP-020; contingency is never a substitute for causality.

## 9. Stochastic, numeric and cadence disposition

### 9.1 Stochasticity

```text
DEFAULT_CAN012_STOCHASTICITY = DISABLED
```

A CAN-012 rule may invoke randomness only when it supplies all ADP-020 requirements: exact semantic rule/version, static `v3.causal.*` stream, finite lawful candidate/parameter contract, permitted operation, candidate-set hash/authority, draw coordinate and Decision/Draw receipts.

Historical `random.random()`, `random.choices()`, implicit `Random()`, float-weight priors and random fallback from invalid/empty priors are rejected. Empty candidate sets consume no draw and create no rupture/process transition.

RNG selection is not rupture admission.

### 9.2 Numeric quarantine

The following recovered values are **not** canonical semantic authority:

- rupture age bands and age-specific injection probabilities;
- nearest-age template selection;
- severity/mode/narrator priors;
- default `medium`, `major`, `accommodation`, `50` values;
- 0–100 intrusive-return/support/plasticity scales as universal semantics;
- 1–3 year plasticity windows;
- cluster deltas, mode/severity scalars and `MALHEUR_MULTIPLIER`;
- hard-coded wound increments;
- support-quality thresholds and text-scoring coefficients;
- stability-inertia bumps, drains, caps, leak rates and status-transition thresholds.

The mechanism interface survives. Exact rules may classify or produce finite numeric effects when units, target state, formula, bounds and provenance are explicitly governed. The historical numbers cannot fill that authority.

### 9.3 Cadence

ADP-021 owns hybrid scheduling and the slow-cadence binding interface.

```text
DEFAULT_SLOW_CADENCE = NONE
ANNUAL_SLOW_CADENCE = NOT_AUTHORIZED_BY_CAN_012_OR_ADP_021
```

A metabolization process is not due merely because a year passed. Event-triggered CAN-012 evaluation may occur when its causal parent arrives. A slow update may run only through exact `V3SlowCadenceBinding` with explicit process and cadence authority. Historical yearly execution is compatibility evidence, not ontology.

If cadence authority is absent, no slow transition is fabricated. Persistence/no-change remains lawful.

## 10. Unknown, missing, valid-empty, denied and integrity law

- **Unknown** is not `medium`, `major`, `accommodation`, `50`, healed or zero.
- **Missing CAN-012 rule** -> `DEFERRED_REQUIRED_RULE_AUTHORITY`; no mutation.
- **Missing actor causal basis** -> `DEFERRED_REQUIRED_ACTOR_CAUSAL_BASIS`; no rupture.
- **No qualifying/admitted rupture** -> valid-empty, not error.
- **No target-state effect** -> valid-empty target effect, not an invitation to invent one.
- **Required input denied for causal use** -> `DENIED_CAUSAL_USE`.
- **Missing/tampered parent ID, event hash, prior-state hash, rule/version, transition receipt, candidate-set identity or RNG receipt** -> `INTEGRITY_FAILURE` before mutation.
- **Corrupted process state** -> integrity failure, never silently `sealed`, `chronic` or `integrated`.
- **No rupture** does not mean no suffering.
- **Rupture** does not mean wound.
- **Metabolization process** does not mean improvement.
- **Integration** does not mean healed/resolved.
- **Chronic** does not mean type/personality.

## 11. Replay and provenance

Every admitted rupture persists at minimum:

- `rupture_event_id`, `actor_id`, effective time;
- exact parent event refs;
- pre-state/checkpoint hash;
- rupture-basis refs;
- CAN-012 rule ID/version/content hash;
- candidate/admission receipt hash;
- optional qualifier classifier refs;
- ADP-020 Decision/Draw receipt refs if stochastic;
- causal event index/history hash.

Every process transition persists at minimum:

- process ID and rupture-event ref;
- prior process-state hash;
- resulting process-state hash when changed;
- transition/effect rule ID/version/hash;
- exact causal parent refs;
- scheduler trigger/receipt refs;
- ADP-020 receipts if stochastic;
- typed effect refs;
- resulting causal event/index where mutation occurred.

Identical immutable causal history, actor state, CAN-012 rules, scheduler inputs and ADP-020 inputs must reproduce the same rupture decisions, process transitions/no-change receipts and causal state/event hashes. Missing provenance blocks replay; implementation may not reconstruct rupture history from labels, prose, age or current-state plausibility.

## 12. Hostile fixtures

| ID | Attack | Required result |
|---|---|---|
| `H01` | High structural pressure/magnitude with no generated actor event | `VALID_EMPTY_NO_GOVERNED_RUPTURE_BASIS`; no rupture/process. |
| `H02` | Adverse event label/intensity alone | No automatic rupture; exact actor-specific causal basis and rule required. |
| `H03` | Same precipitating event for two actors with different generated histories | Different lawful admission/process outcomes permitted; no event-label determinism. |
| `H04` | Proposal lacks pre-event actor-state/basis refs | `DEFERRED_REQUIRED_ACTOR_CAUSAL_BASIS`; no default assumption/prediction-error/opacity. |
| `H05` | Legacy age-band `maybe_inject` / nearest-age template | Authority violation; no causal mutation. |
| `H06` | Empty/invalid mode priors fallback to accommodation/random key | No default/no draw; mode unresolved/not applicable. |
| `H07` | module-global `random.*` or unnamed `Random()` | Reject stochastic mutation under ADP-020. |
| `H08` | Exact stochastic CAN-012 rule with ADP-020 candidate/parameter/stream receipts | Replay-identical choice under same seed/rule/candidates; selection remains distinct from admission. |
| `H09` | Historical numeric age/severity/support/plasticity threshold without governed rule | Quarantine number; transition blocked/deferred rather than guessed. |
| `H10` | Annual tick exists only because historical loop exists | No invocation; exact slow-cadence binding required. |
| `H11` | Governed process evaluation yields no qualifying change | `NO_CHANGE` receipt only; no pseudo-event; process persists. |
| `H12` | Stabilized/integrated process receives exact later reactivation parent | Recurrence may be admitted by rule; prior rupture/history remains immutable. |
| `H13` | Process reaches `INTEGRATED_WITH_RESIDUE` | No healing/resolution/moral-progress claim; residue/reactivation provenance remains. |
| `H14` | Rupture domain mapped directly to wound/framework/crack state | Forbidden; separate target-owner rule/effect required. |
| `H15` | Rupture record used to create belief/knowledge/first-person claim | Forbidden; memory/access/ADP-017 remain separate. |
| `H16` | Rupture/metabolization used to assign attractor/type | Forbidden; MUST-018 remains separate. |
| `H17` | V2/persona/rendered narrative keywords used as causal narration support | Forbidden unless observable interaction separately admitted into V3. |
| `H18` | Missing/tampered parent event, state hash, rule hash or receipt | `INTEGRITY_FAILURE`; no partial mutation/replay salvage. |
| `H19` | Multiple rupture/process records coexist | Preserve independent identities/history; no merge/winner/scalar net. |
| `H20` | Lawful life has no rupture candidates/processes | `VALID_EMPTY` complete and healthy; no filler trauma. |

## 13. Exact downstream consumers and separate blockers

### Direct consumer

`V3-P8` — rupture/metabolization + causal-memory integration.

CAN-012 supplies:

- bounded rupture candidate/admission court;
- persistent process-state contract;
- typed effect boundary;
- persistence/recurrence/no-change law;
- ADP-020 stochastic boundary;
- ADP-021 cadence boundary;
- replay/provenance/failure contract.

`ADP-016` remains causal-memory owner and is already accepted/banked. CAN-012 does not absorb it.

Neighboring CAN-008/009/010/011 remain separate authorities. This result uses their historical modules only as continuity/seam evidence and consumes no sibling Batch-02 result as accepted authority. Optional effects into their future canonical states remain valid-empty/deferred until their owners are accepted.

`MUST-018` remains separate attractor-transition authority. Later `V3-P10` may consume exact CAN-012 generated history as evidence, but CAN-012 cannot update attractor state, assign type or supply interpretation rules.

ADP-017 remains actor knowledge/claim accessibility; ADP-019 external-event admission; ADP-020 causal randomness; ADP-021 scheduler/cadence coordination. V2 has no direct CAN-012 causal authority.

### Consumer release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__CAN_012_SEMANTIC_BLOCKER_CLOSED_FOR_V3_P8_AFTER_VOZHD_ACCEPTANCE__NO_PRODUCTION_IMPLEMENTATION_RELEASED`

CAN-012 is sufficient for its direct V3-P8 semantic dependency after Vozhd acceptance. It does **not** launch or globally release V3 implementation, waive packet/wave gates, or make optional cross-state effects lawful before their owners are accepted.

## 14. Governing Spirit check

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`

**Ambiguity:** recovered source contains both a strong persistent, branching, reactivatable mechanism and convenient age priors, random injection, defaults and fixed numeric transitions that would make suffering mechanically predictive.

**Lawful alternatives:** freeze historical priors/thresholds as canonical policy, or preserve only the source-supported actor-specific persistent/branching mechanism while quarantining under-governed numbers/shortcuts.

**Choice:** preserve causal parentage, persistence, multiple coexisting processes, recurrence, lawful no-change, nonteleological integration and divergent outcomes; remove automatic trauma, default mode, direct wound mutation, rendered-text causality and ungoverned stochastic/numeric/cadence policy.

**Tie-break principles:** historical causality without inevitability; mediation rather than structure-to-psyche shortcut; dynamic history over classification; lawful absence and uncertainty; enough openness for the same field/event to yield divergent lives; the person exceeds suffering; minimum sufficient machinery.

The Governing Spirit supplies no missing semantic predicate, threshold, event or psychological content.

## 15. Forbidden regressions

- structural pressure -> rupture;
- adverse event label/intensity -> rupture;
- rupture -> wound/framework/capacity change without target-owner rule;
- rupture/metabolization -> belief, knowledge or first-person claim;
- rupture/metabolization -> attractor/type;
- rendered narrative -> V3 causal support/metabolization input;
- default `accommodation`, `medium`, `major`, `50` or nearest-age repair;
- age-band/random rupture injection;
- unnamed/global RNG;
- historical numeric thresholds/timescales promoted to law;
- annual ontology/filler slow ticks;
- forced healing/improvement/integration;
- erasure of rupture after integration;
- scalar merge/winner-selection across multiple processes.

## 16. Final authority statement

CAN-012 preserves the recovered mechanism's deepest continuity without preserving its accidental determinism.

Rupture is a generated actor-history claim with exact causal ancestry, not a synonym for adversity. Metabolization is an open causal process, not a teleology. Its state can change, persist, recur, seal, remain unresolved or do nothing at a given evaluation. The same structural conditions or precipitating event do not contain one inevitable developmental future. Where actual generated history and exact rule authority differ, lawful consequences may differ; where authority is missing, the machine says so instead of writing trauma into the person.

`CAN_012_V3_RUPTURE_METABOLIZATION_CANONICALIZATION = PASS`
