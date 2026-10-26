# X01 — formal operators and gates (proposed, NOT ISSUED)

**Status:** conceptual/requirements proposal for the competent scientific owner. Not a CAN/ADP rule, not a native grant, not an implementation instruction. The old V3 functions are historical evidence only.

## 1. Typed input/output requirements

### A. `CareHistoryRecord`
**Inputs:** actor id; counterpart id/role; exact care act/event id; objective availability (time/presence), material provision, warmth/affection, reliability/consistency, responsiveness, repair/rupture events; actor access/perception; source/provenance; effective time.
**Output:** an event-parented care-history record with evidence count, recency, scope (which relationship/need/domain), support conditions, and contradictions.
**First consumer:** the expectation/child-model derivation, then a later same-person event. No scalar 50 fallback; unknown is `UNKNOWN`/`MISSING`.

### B. `ExpectationRecord`
**Inputs:** actor; need axis; scope (relationship/domain/situation); expectation posture; source care/event refs; positive and negative evidence; confidence/uncertainty; support/context; contradiction set; effective time; rule id/version.
**Transform:** a competent rule decides whether the record is created, retained, revised or unchanged, and whether the change is transient or durable.
**Output:** typed expectation record with `CREATE/REVISE/NO_CHANGE`, causal parents, access, scope and uncertainty.
**First consumer:** C9/C12 recognition/recruitment; not a prompt string or hash.
**Old mapping:** M15 categories are a coarse carrier; there is no evidence/scope/confidence/contradiction.

### C. `RelationalChildModelRecord`
**Inputs:** actual care history, household/material conditions, received routines, language/cultural access, later reflective accounts; actor access.
**Transform:** a competent rule separates procedural/bodily anticipation, unspoken expectation, later verbal distinction and later ideological articulation; no category→text default.
**Output:** layered, scoped, uncertain child-model records with provenance and revision/NO_CHANGE.
**First consumer:** event plausibility/recruitment and later reflective meaning; not a hardcoded prompt list.
**Old mapping:** M22 is static category→text; `age` unused.

### D. `ImpressionRecord`
**Inputs:** objective event components; actor access; expectation/need/striving refs; care/material context; counterpart conduct; actual feedback/repair; prior history.
**Transform:** a competent rule classifies challenge/complication/threat (where the taxonomy is issued), assigns positive/negative/uncertain components, intensity/salience, and durable/transient/NO_CHANGE.
**Output:** event-parented impression with mixed components, source/access, causal parents, evidence, and a later semantic consumer.
**First consumer:** C9/C12 actor state/recruitment; not a one-valence shard or narrative line.
**Old mapping:** M17 `expectation_type` from LLM; one gift or disruption; no mixed.

### E. `NO_CHANGE`
**Inputs:** the same event/expectation/child-model inputs plus the competent rule's no-change conditions.
**Output:** a typed `NO_CHANGE` record with reason, evidence, scope and causal parents.
**First consumer:** later event reads no change and does not invent a shard/state.
**Old mapping:** passive skip/absence; no record.

## 2. Challenge / complication / threat

These are **actor-relative relations**, not event labels:

- **Challenge:** the encounter raises required effort or skill but is congruent with the actor's expectation/support and offers a practicable path; it may produce practice/competence effects without threat.
- **Complication:** the encounter contains conflicting components—e.g., care/love is confirmed while availability/material provision is insufficient—so the impression cannot be reduced to a single positive or negative valence; it may or may not become a threat.
- **Threat:** the encounter endangers a valued need/object/relation or the actor's practical ability; objective danger and felt threat must be separable (access, expectation, prior history, support).
- **Repair:** a subsequent event can reduce threat/complication under a rule; it is not automatic and may be scoped/support-limited.

The old code has no challenge/complication/threat taxonomy and no repair rule. It has `kind=opportunity/practice` (challenge-like), binary fulfillment/violation (complication forced one way), `kind=loss/violence/puncture` + `stability_delta` (threat-like), and a transient wound-delta healing path. These are not equivalent.

## 3. Stable history, thickening and repair

A stable-history rule must distinguish:
- repeated routine care without distinctive event memory (thickening);
- a single salient event (possible but not required to change the baseline);
- a complication that coexists with stable love;
- a threat/rupture;
- repair after a rupture;
- support withdrawal/irrelevant event (no change);
- contradictory evidence (preserve both, no forced average).

The old code only has static categories + proxy strivings; repeated care does not thicken the baseline. A `relationship`/`care` event can lower wound sensitivity via `delta_from_event` (`wound_deltas`, 143–154) within an annual cap; that is a transient wound path, not baseline repair.

## 4. Falsifier matrix (conceptual)

Hold actor, world, later event and chronology fixed. Vary only the earlier care history:

| Case | Required semantic difference | Old V3 observable |
|---|---|---|
| A. Reliable loving care + material insufficiency, repeated availability limits, love confirmed | Love/trust expectation preserved; material/world insufficiency represented as a distinct expectation/child-model component; later event recruits both | Both-present coarse split; one-parent/missing collapses; event shard one-valence |
| B. Same material insufficiency, no warmth/reliability | Love/trust expectation lower/uncertain; insufficiency still represented | Threshold heuristics may lower attachment; no reliability/availability |
| C. Same warmth, no material insufficiency | Love preserved; material/world expectation not reduced | Possible; global warm bump may over-raise |
| D. Event not received / no access | No impression/NO_CHANGE; no later change | Skip/no shard; no typed NO_CHANGE |
| E. Verbal-only exposure, no actual care/routine | No earned durable expectation; at most a transient/uncertain record | No distinction; prompt/label can create a shard |
| F. Source hash changed but semantic content unchanged | No change | No semantic hash check/contrast |
| G. Support withdrawn after A | Scoped loss/uncertainty, not total erasure of love | No support-scope model |
| H. Irrelevant later event | No recruitment/NO_CHANGE | No semantic consumer to test |

A correct implementation must make A ≠ B ≠ D ≠ F and preserve mixed components in A. The old probe already shows A (one parent) == missing parent, which is a direct RED.

## 5. Gates and prohibitions

- **Gate S:** a competent owner issues the care/expectation/impression/child-model rule; no X01 or engineering self-issuance.
- **Gate P:** actual source/permission for the caregiver/world history; unknown data remains unknown.
- **Gate T:** typed inputs/outputs and a first C9/C12 consumer; no prompt/hash/label substitution.
- **Gate N:** nonnumeric/qualitative first; any numeric magnitude requires a separately issued semantic unit, scope, evidence and uncertainty. No arbitrary coefficients, 50 midpoints, age multipliers, or global “warm +1” laws.
- **Gate R:** replay/cold read; source/event identity and rule version.
- **Gate C:** contradiction/NO_CHANGE/repair/access/support-withdrawn controls.
- **Gate H:** hostile alternatives (label-only, model-proposed valence, demographic/category shortcut) must fail or be explicitly bounded.

## 6. What the old code cannot answer

- Whether a loving but materially insufficient parent is represented as love + insufficiency (no).
- Whether a missing parent is unknown (no; 50/hopeful/safe-home).
- Whether one event can be both care and limit (no; one shard).
- Whether repeated care thickens an expectation (no; static baseline).
- Whether a later event reads a changed expectation semantically (no; only prompt/persona).
- Whether the child model is procedural/bodily or later verbal (no; hardcoded text).
- Whether repair is lawful and scoped (no rule; only transient wound deltas).

These are the exact competent scientific decisions the next owner must make before engineering.
