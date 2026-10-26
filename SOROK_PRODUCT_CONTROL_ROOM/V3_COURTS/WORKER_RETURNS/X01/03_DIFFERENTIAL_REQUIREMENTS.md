# X01 — differential requirements

**Status vocabulary:** `MEANINGFUL_COVERAGE` / `PARTIAL_WRONG_MEANING` / `INFRASTRUCTURE_ONLY` / `MISSING` / `CONFLICTING` / `UNKNOWN`.

## 1. Mechanism-by-mechanism

### M01 — persistent BackboneState
| Dimension | Finding |
|---|---|
| As-built | `BackboneState` + JSON codec + year-record hash + integrity accumulator; persists baseline/child model/shards. |
| Coverage | `INFRASTRUCTURE_ONLY` for the assigned psychological state. |
| Required Neo-V3 | Time-indexed, event-parented, scoped actor-state records with rule identity, evidence, confidence, actor access and contradiction; canonical causal ledger/checkpoint separation. |
| Retain | Typed state container; stored/derived separation; JSON roundtrip; diagnostic accumulator. |
| Adapt | Add parent/event refs, rule version, scope, uncertainty, access and contradiction to baseline/child-model/shards; do not treat a list/label as a causal record. |
| New | Canonical ledger for the states; later semantic consumer; current C9/C12 owner. |
| First consumer | Today: `striving_update`, Pass 1 summary, persona sheet. Required new consumer: C9/C12 same-person event. |
| Owner | V3 actor developmental causality engine (CAN011/ADP016 jurisdiction suggestion); no issue by X01. |
| Falsifier | Removing/replacing a causal event ref must change the later semantic read; an unchanged later response after a supposedly effective history is a RED. |

### M15 — need axes / expectation baseline
| Dimension | Finding |
|---|---|
| As-built | 10 axes, 4 categories; parent averages → crude thresholds → global YAML modifiers → categories; missing → hopeful; yearly setdefault. |
| Coverage | `PARTIAL_WRONG_MEANING`. |
| Required Neo-V3 | Thick, scoped, historically weighted expectation with separate love/availability/material/reliability/routine/repair, evidence, confidence/uncertainty, contradiction and later recruitment; love and insufficiency can coexist. |
| Retain | Need-axis vocabulary and qualitative posture as a compatibility carrier. |
| Adapt | Replace 50/one-parent averaging with actual caregiver history/material facts; use per-axis rules or a new issued rule; remove global one-size warm bump; separate warmth/love from availability and material provision; add scope/evidence/confidence/contradiction. |
| New | Baseline thickening/revision from repeated care; mixed relational schema; explicit unknown/missing; NO_CHANGE; later semantic consumer. |
| First consumer | `striving_update` (proxy strivings) and Pass 1 prompt; new consumer C9/C12. |
| Owner | CAN011/ADP016/Neo-V3 scientific authority; engineering after rule. |
| Falsifier | Single loving low-material parent must not equal missing parent; insufficiency-only must not preserve love; warmth-only must not create insufficiency; support withdrawal/irrelevant event must not change the baseline. The probe already shows the first equality (RED). |

### M17 — Gift/Disruption shards / expectation events
| Dimension | Finding |
|---|---|
| As-built | One gift or disruption shard per event, valence from LLM `expectation_type`; malheur at identity_load≥60; shards are persona-sheet/persistence only; duplicate creation in the legacy V2 runner; alienation delta lost. |
| Coverage | `PARTIAL_WRONG_MEANING`. |
| Required Neo-V3 | Event-parented actor-relative impression with positive/negative/uncertain components, source/access, expectation match, care/material context, intensity/salience, durable-vs-transient decision, NO_CHANGE and later semantic recruitment. |
| Retain | Typed event-effect record idea; striving/need-axis linkage; malheur/identity-load as a *candidate* severity signal, not law. |
| Adapt | Replace single valence with mixed components; derive from event semantics + actor expectation + actual source/access, not LLM label alone; add event ids/provenance; allow both gift and disruption components; deduplicate; link to baseline/striving. |
| New | Mixed impression record; later V3 consumer; repair/no-change; contradiction preservation. |
| First consumer | Today: V2 persona sheet/backstory only; new consumer C9/C12. |
| Owner | CAN008/CAN011/ADP016; original V3/Neo-V3 authority. |
| Falsifier | Same event (“loving parent works late but calls”) must not be forced into exactly one of gift/disruption; if V3 cannot represent both components or its later response is identical to a single-valence control, RED. |

### M22 — child model / assumed rules / taboos / possible world
| Dimension | Finding |
|---|---|
| As-built | Category→hardcoded rule/taboo list; safe-home default if no forbidden/hopeless axis; `age` unused; static; prompt/scoring only. |
| Coverage | `PARTIAL_WRONG_MEANING`. |
| Required Neo-V3 | Historically generated procedural/bodily anticipation, unspoken expectation and later verbal/ideological articulation, with scope, confidence, access, contradiction, revision and no demographic/category stereotype. |
| Retain | A child-model carrier exposed to the agent/prompt and a structured possible-world field. |
| Adapt | Derive from actual care/household history and received events; layer procedural/bodily/unspoken/verbal; add provenance/scope/uncertainty; do not suppress positive relational rules when one axis is forbidden; age-sensitive. |
| New | Developmental update/repair, fallible access, later ideological rearticulation; explicit unknown. |
| First consumer | Pass 1 summary and rupture scoring; new consumer C9/C12. |
| Owner | CAN011/ADP017/Neo-V3 authority. |
| Falsifier | Missing parent must not produce the safe-home default; a loving-low-material history must not produce only status/competence prohibitions and omit the positive relational rule; a stable caring history must not be overwritten by one event. |

### M36 — hopeful/medium parent defaults
| Dimension | Finding |
|---|---|
| As-built | Multi-layer 50→hopeful→safe-home conversion; one-parent dilution; server exact 50; V2 no-WVS near-50 sampling. |
| Coverage | `CONFLICTING` with required semantics; required operation `MISSING`. |
| Required Neo-V3 | Unknown remains unknown/typed missing; actual caregiver history or an explicitly issued prior; no hidden midpoint; no default type/psyche. |
| Retain | Nothing from the default conversion as science. |
| Adapt | At most keep a typed absence record; any optional prior must be a separately issued rule with provenance, not `_float(...,50)`/`setdefault(...,"hopeful")`. |
| New | Unknown/missing/deferred state; evidence request; later authority-aware resolution. |
| First consumer | Initialization/striving_update/Pass 1; new C9/C12. |
| Owner | Original V3/Neo-V3 authority; data/source owner for actual caregiver history. |
| Falsifier | Missing parent must be distinguishable from known-safe and known-negative parent in state and later response; if all three collapse to the same optimistic baseline, RED. |

## 2. Neo-V3 crosswalk

| Neo-V3 | Old carrier | Coverage | What is missing |
|---|---|---|---|
| N01 needs/motives/objects | M15/M22, `StrivingObject` | `PARTIAL_WRONG_MEANING` | Need axes are static categories; proxy strivings are baseline-generated, not constituted by activity; no object constitution/contradiction. |
| N02 thick relational baselines | M15/M17/M22/M36 | `PARTIAL_WRONG_MEANING` | No actual care history/routine/reliability, no love+insufficiency, no scope/confidence/evidence, no thickening/repair. |
| N03 challenge/complication/threat/repair | M17, `delta_templates` | `MISSING` / `PARTIAL_WRONG_MEANING` | Binary fulfillment/violation; no challenge/complication/threat taxonomy; no repair rule. |
| N05 durable transition | M17/M15/M16 | `PARTIAL_WRONG_MEANING` / `MISSING` | Shards/strivings can persist, but baseline/child model are static; no event-earned durable operation. |
| N08 impression/salience/NO_CHANGE | M17, `delta_templates` | `PARTIAL_WRONG_MEANING` | One-valence shard, intensity only minor/major/shock; no salience/uncertainty; no typed NO_CHANGE. |
| N09 fallible memory/meaning | M17/M22, persona sheet | `INFRASTRUCTURE_ONLY` / `MISSING` | Shards are recent narrative lines; no actor access, forgetting, reconstruction, self-account or later causal reflection. |
| N10 ideology/theology/cosmology | M22 | `PARTIAL_WRONG_MEANING` | Hardcoded taboos/possible-world text, no later ideological mediation or cultural access. |
| N11 3–5 batch recursion | M01/Pass 1/Pass 2 | `MISSING` | Yearly LLM band; no 3–5-event batch, sequential realization, interpressure/time or retrospective first half. |
| N12 actual native person | M01 etc. | `MISSING` / `UNTRACED` | No current C9/C12 consumer, native source/actor/rule or actual person test. |

## 3. Retain / adapt / create / do not reuse

**Retain (carrier only):**
- BackboneState as a typed checkpoint, not a causal ledger.
- The ten axis names and four posture labels as a compatibility vocabulary.
- `StrivingObject` identity/lifecycle as a target carrier, not proof of motive.
- A typed event-effect record shape (replacing the one-valence shard semantics).
- A child-model carrier exposed to a prompt/scoring seam.
- JSON roundtrip and integrity diagnostics.

**Adapt:**
- Parent inference: actual caregiver acts/availability/material/reliability, no 50 defaults.
- Baseline derivation: issued rule, per-axis evidence, scope/confidence/contradiction, no dead YAML, no global warm all-axis bump.
- Event effects: mixed components, event/access provenance, no LLM-label truth, dedup, no lost alienation delta.
- Child model: actual history, layered procedural/unspoken/verbal, age-sensitive, no hardcoded safe home/taboos.
- Yearly maintenance: no `setdefault(hopeful)`, explicit missing/NO_CHANGE.

**Create:**
- Event-parented expectation/child-model records.
- Mixed impression record with positive/negative/uncertain components.
- Actor access/uncertainty/contradiction.
- Later semantic consumer and C9/C12 spine.
- Typed unknown/missing/deferred.
- Rule identity/version and replay.

**Do not reuse as science:**
- 50/hopeful/safe-home defaults.
- Global warm all-axis +1 and threshold cliff.
- One-valence Gift/Disruption pre-classification.
- `identity_load>=60` malheur threshold as a law.
- Hardcoded child-model text/taboos.
- Proxy-striving multipliers as motives.
- Static baseline with no revision.

## 4. Owner and first real consumer

- **Scientific owner:** original V3/Neo-V3 CAN008/CAN011/ADP016/017 competent authority; no X01 issuance.
- **Engineering owner:** existing V3 actor-developmental implementation owner, after a rule; X01 only maps.
- **First real consumer:** the next lawful C9/C12 same-person event that reads the typed semantic value. The current first consumers are historical `striving_update`/Pass 1/persona sheet; they are not enough.
- **Source/permission:** original V3 is historical read-only; current actor/source/rule rights are separate. No native grant is inferred.

## 5. Argument against a shallow “rename”

Renaming `hopeful` to “secure” or `forbidden` to “avoidant,” or adding a “mixed” flag to a shard, does not satisfy N02/N03/N08. The old machine computes a parent-scalar average and a category; it does not retain the actual care act, availability, material condition, routine, evidence, actor access or later semantic read. A mixed flag without event provenance and later consumption remains a label. The adaptation must change the inputs, the stored record, the revision/no-change law and the consumer.
