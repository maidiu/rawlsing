# X01 — phenomenon and causal claims

**Scope:** source-grounded interpretation of M01/M15/M17/M22/M36. No new primary literature was read for this return; the competing interpretations below are about what the code actually does, not claims about human development.

## 1. The phenomenon the old code claims

The V3 files repeatedly use a developmental vocabulary:

- ten need axes (`attachment`, `safety`, `belonging`, `status`, `competence`, `autonomy`, `meaning`, `justice`, `beauty_play`, `eros_intimacy`);
- four expectation postures (`entitled`, `hopeful`, `forbidden`, `hopeless`);
- a parent/transmission regime (`warmth`, `coercion`, `openness`, `anxiety`, `shame`, `modeling_consistency`);
- child-model `assumed_rules`, `taboos`, `what_counts_as_possible`;
- `GiftShard`/`DisruptionShard` as positive/negative prediction-error records attached to active strivings;
- proxy strivings for `forbidden`/`hopeless` axes.

The implicit claim is that early care organizes a person's expectations, that later expectation events can install “gifts” or “disruptions,” and that the child model conditions which events are plausible/volatile. The Pass 1 prompt states this interpretation explicitly (`prompts.py:28–29`).

## 2. What the code actually computes

The computational core is much thinner than the vocabulary:

1. **Parent behavior → category vector.** `infer_parent_baseline_and_regime` averages two caregiver records on three scalars (warmth, authority, material support), defaults missing values to 50, and applies a few threshold rules. It is labelled “Heuristics” in the source (line 55). It does not read availability, reliability, care routines, work schedule, actual material conditions, or the child's received care.
2. **Category vector → category vector.** `derive_child_expectation_baseline` maps parent categories to scores, applies four global modifiers from `need_axis_rules.yaml`, and maps back. The extensive per-axis YAML rules are not consumed. Environment keys are not consumed. Missing axes become `hopeful`.
3. **Yearly maintenance.** `striving_update` sets missing axes to `hopeful` and spawns proxy strivings from a static YAML map. It does not revise the baseline from events, care, feedback, or repair.
4. **Event labeling.** `apply_gift_disruption_shards_from_events` trusts an LLM-supplied `expectation_type` and `striving_object_id`; it appends a single positive or negative shard. It does not read the baseline, the event's actor-relative meaning, the care relationship, material conditions, or the prior shard history.
5. **Child model.** `child_model_from_parent_baseline_and_regime` turns forbidden/hopeless categories into a small hardcoded text list; if no such category exists, it asserts a safe-home default. `age` is unused. There is no revision, scope, evidence, or procedural layer.
6. **Prompt/surface.** The baseline/child model reach the Pass 1 prompt; the shards reach the V2 persona/backstory surface. These are semantic prompts/narrative lines, not a V3 causal transition.

## 3. The love + material-insufficiency case

The user-settled phenomenon is: a reliably loving caregiver plus material absence can produce coexisting felt love and sufficiency-deficit, with neither reducing to the other.

**Old V3 result (probed):**

- **Both parents present, warmth 85 / authority 45 / material 20:** the parent baseline is `attachment/belonging/autonomy/safety/...=hopeful`, `status/competence=hopeless`. The global warm+consistent modifier then raises all axes by +1, producing most relational axes `entitled` and `status/competence=forbidden`. The child model contains only “Status is for others”/“You’re not allowed to be good at this,” and **not** “Home is safe”/“Adults are mostly fair” or an explicit “parent loves me but cannot provide.”
- **One present parent with the same 85/45/20, other missing:** the missing parent’s 50 is averaged in, yielding 67.5/47.5/35.0; no threshold fires. All axes are `hopeful`; the child model is the default “Adults are mostly fair / Friends don’t betray you / Home is safe.” This is **identical to both parents missing for this threshold-boundary input** and erases the actual loving parent’s warmth and material insufficiency. Lower material could cross a threshold, so the general failure is the missing love/availability schema plus the dilution, not a universal one-parent erasure.
- **Event level:** the same event “Parent works late but calls to say she loves me” becomes a GiftShard if the LLM says `fulfillment`, or a DisruptionShard if it says `violation`. It cannot be both. There is no mixed shard, no per-component love/availability record, and no baseline change.

**Interpretation:** the old code can produce a coarse cross-axis split only in a narrow both-present configuration. It does not represent the relational phenomenon; it represents thresholded category differences. In the single-parent configuration it collapses to the missing-parent default; at the event level it forces one valence. The code has no confidence, evidence, scope, routine, support, contradiction, or repair for the baseline, and no mixed impression record.

## 4. Competing explanations of the old design

| Explanation | Evidence for | Evidence against / limit |
|---|---|---|
| **Coarse trait/temperament model** | Stable categories, parent averages, proxy strivings, fixed thresholds. | No temporal updating, no evidence, no scope; categories are not traits; missing data becomes a “normal” trait. |
| **Narrative scaffold for an LLM** | Baseline/child model are only prompt text; shards are only persona-sheet lines; no V3 causal consumer. | The scaffold still writes persistent state and proxy strivings; it can influence event selection and later narrative, so it is not inert. |
| **Legitimate first-pass carrier needing adaptation** | Typed axes, four postures, event records and a state container are reusable. | The semantics (50/hopeful, one-valence, hardcoded taboos, static baseline) are wrong for the required phenomenon; reuse must be at carrier level only. |
| **Scientific model of early care** | Source vocabulary and prompt claims. | No issued coefficients/rules; thresholds are legacy; tests do not validate the core claims; per-axis rules are dead. This is not an empirically warranted law. |

The defensible reading is the third plus a warning: the old code is a **carrier and a prompt scaffold**, not a validated developmental mechanism. Treating its defaults or categories as science is a category error.

## 5. Challenge, complication, threat, repair

- **Challenge:** a supported difficulty that is congruent with the actor's expectation and practical ability. The old code has no challenge type; it can appear as `opportunity`/`practice` or a fulfillment expectation event, with skill/practice/coherence deltas. There is no challenge-specific operator or later challenge recognition.
- **Complication:** a conflicting configuration where care and insufficiency coexist. The old code forces a single fulfillment/violation shard. It cannot represent a complication as both.
- **Threat:** danger to a valued need/object. A violation shard can be marked `malheur_risk` if `identity_load>=60`; trauma-kind events can add `stability_delta`. There is no objective-vs-subjective threat distinction, no challenge-vs-threat distinction, and no repair rule for expectation violations.
- **Stable history/repair:** repeated relationship/care events can reduce wound sensitivities through `delta_from_event` (`wound_deltas`, lines 143–154) within caps. The baseline/child model/shards do not change; this is a transient wound-delta path, not developmental repair.
- **NO_CHANGE:** an event without `expectation_type` or an active striving is skipped; no typed NO_CHANGE record is written. The yearly `striving_update` still fills missing axes with `hopeful`. The old code has a passive skip, not a lawful no-change state.

## 6. What would count as a genuinely different Neo-V3 result

A Neo-V3 result would need at least:

- an actor-relative expectation record with scope, source, evidence, confidence/uncertainty, support and contradiction;
- a care history that distinguishes warmth/love, availability, material provision, reliability, routine, repair and actual received acts;
- an event impression with separate positive/negative/uncertain components, not a single LLM label;
- a child model that can hold “my parent loves me” and “the world may not provide” simultaneously, with procedural/bodily and later verbal layers;
- a later same-person event that reads those semantic values and changes a typed response, or a typed NO_CHANGE;
- provenance and cold replay.

The old code has none of these at the required grain. It has carriers that could be adapted, but the adaptation is not a rename.

## 7. Claim ceiling

Nothing here establishes a human developmental law, a native CAN/ADP rule, an empirical effect size, or a current person. The probes establish only what the historical source computes under the specified inputs. The old defaults are legacy policy; the old tests are presence/wiring tests, not validation of the phenomenon.
