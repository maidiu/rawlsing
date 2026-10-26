# X01 — implementation plan and seam (research only, NOT IMPLEMENTED)

**No production code is written or authorized by this document.** This is a bounded transposition specification for the existing Sorok actor-development owner, contingent on a competent scientific rule and source/permission decisions.

## 1. Reuse at demonstrated grain

| Existing carrier | Reuse | Limit |
|---|---|---|
| `BackboneState` (`state.py:500–614`) | Typed checkpoint/container; JSON roundtrip; stored/derived separation. | Not a causal ledger; no event parentage for baseline/child model/shards. |
| Ten `NEED_AXES` + four postures (`305–309`) | Compatibility vocabulary for expectation records. | Do not treat as a validated ontology or a confidence scale. |
| `StrivingObject` (`312–336`) | Target/lifecycle carrier for practical objects. | Proxy-spawn from baseline is not motive constitution. |
| `GiftShard`/`DisruptionShard` shape (`338–364`) | Event-effect record idea; need-axis/striving linkage. | Replace one-valence semantics and list-position ids. |
| `child_model` carrier (`549`) | Structured assumed-rules/taboos/possible-world slot. | Replace hardcoded category→text and safe-home default. |
| `striving_update` seam (`striving_objects.py:242–272`) | Yearly integration point. | Remove `setdefault(hopeful)`; no baseline invention. |
| `llm_contract.state_summary` seam (`710–739`) | Pass 1 prompt exposure. | Prompt text is not causal state; remove defaults. |
| `persona_sheet` seam (`922–948`) | V2 surface for narrative continuity. | Not a first causal consumer. |
| `apply_deltas_to_state` (`delta_templates.py:254–364`) | Existing delta/event application seam. | Fix alienation-vector mutation; do not duplicate shards. |
| `expectation_event_templates.yaml` | Candidate event vocabulary. | `baseline_high_impact` is currently unused; no template is law. |

## 2. Adapt (same seam, changed semantics)

1. **`infer_parent_baseline_and_regime` / parent input**
   - Input actual caregiver history: warmth/affection, availability/presence, material provision, reliability/consistency, responsiveness, repair, actor access. Separate fields; no father/mother average that silently dilutes one present parent.
   - No default 50 for missing data; emit typed `UNKNOWN`/`MISSING` and, if a product rule requires a prior, require a separately issued prior with provenance.
2. **`derive_child_expectation_baseline`**
   - Consume the issued rule (not a hidden subset of YAML); per-axis evidence/scope/confidence/contradiction; no global all-axis warm bump; no static `setdefault`.
   - Preserve love/trust and material/world insufficiency as distinct components that can coexist.
3. **`update_striving_step`**
   - Do not fill missing axes with `hopeful`; do not manufacture a baseline. Spawn only under an issued object/motive rule; proxy entries are compatibility candidates, not desires.
4. **`apply_gift_disruption_shards_from_events`**
   - Replace `expectation_type`-only valence with an event-parented impression record that can carry positive, negative and uncertain components; derive from actor expectation + actual source/access + care/material context; retain both components for a loving-but-unavailable event.
   - Add event id/hash, actor/access ref, causal parents, rule/version, scope, evidence; no list-position id; deduplicate.
   - Remove the legacy V2 double call; fix the alienation-vector mutation.
5. **`child_model_from_parent_baseline_and_regime`**
   - Derive from actual care/household history; produce layered procedural/bodily/unspoken/verbal records; age-sensitive; no hardcoded cultural taboos/safe-home default; preserve positive relational rules alongside prohibitions; typed unknown/contradiction.
6. **`llm_contract` / `prompts`**
   - Stop treating the baseline/child model as an authority or default. The prompt may present admitted records with provenance/uncertainty; the LLM may propose events, not adjudicate valence or write psyche.
7. **`persona_sheet`**
   - Keep as narrative surface; do not count it as a causal consumer. Mixed records must not be flattened to “gift”/“disruption” lines.

## 3. Create (genuinely new functions/seams)

| New operation | Typed input → output | First consumer |
|---|---|---|
| `CareHistoryRecord` admission | actual caregiver acts/availability/material/reliability/access + source → event-parented care record | expectation/child-model derivation |
| `ExpectationRecord` formation/retention/revise/NO_CHANGE | admitted care/event refs + rule + scope/evidence → typed expectation record with confidence/contradiction | C9/C12 recruitment |
| `RelationalChildModelRecord` formation/update | care history + later language/ideology access + rule → layered child-model records | event plausibility/recruitment; later reflective meaning |
| `ImpressionRecord` mixed impression | objective event components + actor access + expectation/need + care/material + feedback → positive/negative/uncertain components, challenge/complication/threat (if issued), durable/transient/NO_CHANGE | later same-person event/C9/C12 |
| `NO_CHANGE` record | event + rule conditions → typed no-change with reason/parents | later event (no invented change) |
| `SemanticRecruitment` | expectation/child-model/impression semantic value + event context → typed recognition/option/response change or no-change | C9/C12 response/selection |
| `Provenance/rule registry` | rule id/version, source refs, support/scope, actor access → replayable record | all above |

The new operations must be owned by the existing actor-development implementation owner after the scientific owner issues the rule. X01 does not implement them.

## 4. First real consumer and seam

The first real consumer is **not** `striving_update`, the Pass 1 prompt, the V2 persona sheet, a hash, a label or a narrative line. It is a later **C9/C12 same-person event** that:

1. reads the changed expectation/child-model/impression semantic value;
2. changes a typed recognition, option, eligibility or response under a preregistered contrast;
3. preserves access/support/scope/uncertainty;
4. records `NO_CHANGE` when the rule says no change;
5. replays cold with exact source/event/rule identity.

The old code's first consumers are `striving_update` (proxy spawn), `llm_contract` (Pass 1 prompt), `scoring` (rupture fit), `persona_sheet` (V2 narrative). They can be used as temporary research seams, not as proof of the developmental consumer.

## 5. Bounded proof

A sourcefree same-person cell:

- one actual G18/S44 actor/history and world event, not a demographic default;
- a care history with warmth/availability/material/reliability and actual received acts;
- the issued rule applied to produce an expectation/child-model/impression record or NO_CHANGE;
- a later event that reads the semantic value;
- positive (love+insufficiency), insufficiency-only, warmth-only, no-received-event, verbal-only, support-withdrawn, irrelevant-event and source-hash-only controls;
- cold replay and exact provenance;
- a named fault that severs the new semantic edge and makes the later typed response RED.

This is a research cell, not a native person or production. It must not use a paid LLM as the valence oracle.

## 6. What not to build

- Do not build a new psyche or a generic “learning rate.”
- Do not preserve 50/hopeful/safe-home or one-valence shards as science.
- Do not add a mixed flag without event provenance, scope, access and later consumption.
- Do not use the V2 persona sheet/backstory as the first causal consumer.
- Do not implement the 3–5-event batch as a scheduler/receipt demo before the actor-owned cell and the issued coupling/memory rule exist. S48 transport is not the loop; S52 controlled performance is not an independent act.
- Do not seed from demographics, age, class, minority status, religion or parent type.
- Do not claim historical test success is current person integration.

## 7. Dependency and authority

- **Scientific:** CAN008/CAN011/ADP016/017 and original V3/Neo-V3 authority must issue the concrete care/expectation/impression/child-model/coupling rule. Until then: `RULE_UNISSUED`.
- **Engineering:** existing Sorok actor-development owner implements after the rule; X01 returns the map only.
- **Data/source:** actual caregiver/world history and permissions; missing data must remain unknown. No raw survey data in this return.
- **Consumer:** C9/C12 owner; current S50 actual root remains `SOURCE_OWNER_HOLD` and must not be seeded from this research.
- **Review:** independent I2/I3 reviewer after the immutable return; no self-adoption.
