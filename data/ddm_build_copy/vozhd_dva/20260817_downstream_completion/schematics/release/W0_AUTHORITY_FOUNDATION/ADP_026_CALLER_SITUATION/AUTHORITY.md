# ADP-026 — Caller / Application Current-Situation Authority

**Authority ID:** `CALLER_CURRENT_SITUATION_AUTHORITY`  
**Authority version:** `1.0.0`  
**Decision packet:** `ADP-026`  
**RA-R00 requirement:** `MUST-026`  
**Owner:** caller/application boundary  
**Status:** `AUTHORITY_CREATED`  
**Mode:** authority only; no production implementation  
**Whole-machine architecture:** `CLOSED`  
**Consumer release sufficiency:** `SUFFICIENT`

## 1. Binding decision

The caller/application boundary may authoritatively describe the **current interaction situation only as field-level, source-bound, subject-bound, time-bounded statements**. Its authority is narrower than the proposition carried by a statement:

- a caller assertion authoritatively proves that the caller asserted the proposition, not that the proposition is objective generated-actor truth;
- an application observation is authoritative only for the property actually observed within the application's measurement jurisdiction;
- a session record is authoritative only for the session/application state it records;
- a deterministic application derivation may guide presentation only and may not increase epistemic authority;
- explicitly synthetic scenario context may guide presentation only when marked nonactual;
- none of these classes becomes V3 generated history merely because it is present, repeated, persisted, rendered, summarized, or plausible.

There is no caller/application authority to synthesize a current biography, randomize a `TodayState`, infer actor identity or belief from location/demographics, or retroactively modify generated history.

`CALLER_CURRENT_SITUATION_AUTHORITY` therefore governs an **ephemeral current-situation statement envelope**, not an actor-state store.

## 2. Constitutional boundary

The closed machine remains:

```text
V3 generated causal truth
  + actor-accessible V3 render boundary
  + caller/application current-situation statements under this authority
      -> V2 RenderSituation / noncausal session behavior

caller/application statement intended to matter causally
      -> PROPOSED_CAUSAL_INPUT
      -> separately governed V2->V3 external-event packaging
      -> V3 external-event admission/rejection
      -> generated causal history only if admitted
```

The following identities are prohibited:

```text
caller assertion != objective actor fact
application/session context != structural prior
caller current situation != V3 generated history
session persistence != causal memory
presentation context != causal event
PROPOSED_CAUSAL_INPUT != admitted event
location != identity, class, sect, ethnicity, party, household, belief, memory, or personality
request/server time != actor effective time unless explicitly bound as such
```

V2 cannot write `ActorCausalState` or use this authority to rewrite earlier V3 events.

## 3. Exact consumers

This authority satisfies `MUST-026` for these RA-R00 consumers only:

1. **`V2-P3` — life-layer migration / factual RenderSituation**
   - may consume lawful `PRESENTATION_ONLY` current-situation statements for the caller/application portion of an ephemeral `RenderSituation`;
   - must combine them without semantic collapse with separately authoritative V3 current generated state where present;
   - may not create Life Container, Life Season, biography, motive, memory, relationship state, or actor facts from missing or caller-only material.

2. **`V2-P4` — typed noncausal SessionState**
   - may retain current-situation statement records, provenance, subject binding, effective-time scope, contradiction sets, and unknown status as session state;
   - persistence does not promote any statement into V3 memory/history or objective actor truth.

3. **`V2-P10` — stable application envelope / hostile harness**
   - may expose authorized presentation/session fields and their epistemic status;
   - must preserve no-inference, no-causal-promotion, contradiction, expiry, and unknown invariants.

`V2-P9`, `V3-P12`, the V2->V3 packaging seam, and V3 external-event admission may later reference records in `PROPOSED_CAUSAL_INPUT` state, but **this authority does not release those consumers and does not define their admission semantics**. Their independently accepted authorities remain required.

## 4. Authorized namespace

Canonical record namespace:

`caller_current_situation.statement[]`

Every statement has exactly one `field_key` from this allowlist. Free-form new field keys fail closed until this authority is versioned.

| `field_key` | Meaning | Allowed subjects | Authorized source classes | Presentation | Causal-candidate eligibility |
|---|---|---|---|---|---|
| `interaction.request_received_at` | application-observed receipt time for the current request/turn | `SESSION`, `APPLICATION` | `APPLICATION_OBSERVED` | yes | no |
| `interaction.channel` | actual application/channel surface used for this interaction | `SESSION`, `APPLICATION` | `APPLICATION_OBSERVED`, `SESSION_RECORDED` | yes | no |
| `interaction.mode_context` | declared session interaction premise/mode metadata that is not itself V3 truth | `SESSION`, `INTERACTION_ENVIRONMENT` | `CALLER_ASSERTED`, `SESSION_RECORDED`, `SCENARIO_DECLARED_NONACTUAL` | yes | no |
| `situation.current_time` | asserted/observed current clock/calendar fact for the bound subject/environment | `CALLER`, `GENERATED_ACTOR`, `INTERACTION_ENVIRONMENT` | `CALLER_ASSERTED`, `APPLICATION_OBSERVED` | yes | conditional |
| `situation.current_location` | asserted/observed current physical location at stated granularity | `CALLER`, `GENERATED_ACTOR`, `INTERACTION_ENVIRONMENT` | `CALLER_ASSERTED`, `APPLICATION_OBSERVED`, `APPLICATION_DERIVED_PRESENTATION_ONLY` | yes | conditional; derived location never eligible |
| `situation.current_device` | current client/device/interface fact, or explicitly asserted in-world device fact | `CALLER`, `APPLICATION`, `GENERATED_ACTOR` | `CALLER_ASSERTED`, `APPLICATION_OBSERVED`, `APPLICATION_DERIVED_PRESENTATION_ONLY` | yes | only an explicit in-world/generated-actor claim; client device data is not actor fact |
| `situation.current_privacy` | current privacy/audibility/visibility condition within source jurisdiction | `CALLER`, `GENERATED_ACTOR`, `INTERACTION_ENVIRONMENT`, `APPLICATION` | `CALLER_ASSERTED`, `APPLICATION_OBSERVED` | yes | conditional when it denotes an in-world observable condition |
| `situation.current_interruption` | interruption occurring now, or current interruption constraint/risk explicitly asserted or directly observed | `CALLER`, `GENERATED_ACTOR`, `INTERACTION_ENVIRONMENT`, `SESSION` | `CALLER_ASSERTED`, `APPLICATION_OBSERVED` | yes | conditional for an actual in-world event/condition; guessed risk is ineligible |
| `situation.current_activity` | activity the bound subject is explicitly asserted/observed to be doing now | `CALLER`, `GENERATED_ACTOR` | `CALLER_ASSERTED`, `APPLICATION_OBSERVED` | yes | conditional |
| `situation.current_availability_constraint` | immediate caller/session communication constraint | `CALLER`, `SESSION` | `CALLER_ASSERTED`, `APPLICATION_OBSERVED` | yes | no by default |
| `situation.interaction_reason` | caller-declared purpose for the current interaction | `CALLER`, `SESSION` | `CALLER_ASSERTED` | yes | no; not generated-actor motive authority |
| `presentation.client_context` | bounded UI/form-factor/accessibility/routing context needed only to render/route the session | `APPLICATION`, `SESSION` | `APPLICATION_OBSERVED`, `APPLICATION_DERIVED_PRESENTATION_ONLY`, `SESSION_RECORDED` | yes | no |

### Explicitly non-authorized legacy/session fields

The existence or persistence of any of the following does **not** make it current-situation authority:

- client IP as identity, precise location, demographic identity, belief, or generated-actor property;
- persisted demographics as current situation or generated-actor truth;
- questionnaire/free-text answers as current objective fact without a new authorized statement envelope;
- `country_resolution` as identity, belief, class, sect, ethnicity, or current physical location without a separately lawful current-location statement;
- `conversation_history`, transcript summaries, topic streams, `EnergeticField`, or chat diagnostics as actor memory, relationship history, personality, motive, causal biography, or current objective fact;
- legacy randomized/default `TodayState` values;
- persona-sheet or generated-biography fields as caller current-situation authority.

## 5. Canonical statement envelope

Every non-`UNKNOWN` statement consumed as current situation MUST carry:

```text
statement_id
field_key
value
subject_binding
source_class
source_ref
recorded_at
source_event_or_observation_time
semantic_effective_time
knowledge_state
certainty_state
disposition
transform_chain[]
authority_id = CALLER_CURRENT_SITUATION_AUTHORITY
authority_version = 1.0.0
```

Optional but preserved when supplied:

```text
measurement_quality
source_declared_confidence
spatial_precision
value_unit_or_format
conflict_set_id
supersedes_statement_id
notes_or_source_locator
```

No consumer may silently manufacture a required envelope field.

## 6. Subject-binding law

`subject_binding` is mandatory and contains:

```text
subject_kind = CALLER | GENERATED_ACTOR | SESSION | APPLICATION | INTERACTION_ENVIRONMENT
subject_id
binding_source
binding_recorded_at
```

Rules:

1. `GENERATED_ACTOR` requires the exact generated `actor_id`; a display/persona name is insufficient.
2. `CALLER` may use an ephemeral session-scoped caller ID where no durable identity is known. Session ID, IP, device ID, account handle, or location does not silently become personal identity.
3. `SESSION` binds only to the session object and cannot be read as a person.
4. `APPLICATION` binds only to the client/runtime surface.
5. `INTERACTION_ENVIRONMENT` denotes a shared/session environment claim and is not a person.
6. A caller statement *about* a generated actor remains `CALLER_ASSERTED` with `GENERATED_ACTOR` as proposition target. Target binding does not convert the caller into an authority over generated-actor truth.
7. No value may be rebound across subjects by analogy, co-location, shared device, geography, or session association.

## 7. Source classes and epistemic authority

### `CALLER_ASSERTED`

Guaranteed truth: **the caller asserted VALUE about SUBJECT for EFFECTIVE_TIME**. It is not guaranteed objective truth of VALUE.

### `APPLICATION_OBSERVED`

A direct application/runtime observation is authoritative only inside its actual measurement jurisdiction: e.g. request receipt time, selected channel, directly exposed device capability, or a location/privacy/interruption signal only when the application genuinely obtained that signal. “Available to the server,” “typical users,” or “probably true” is not observation.

### `SESSION_RECORDED`

A session record may authoritatively describe session mechanics already recorded by the application. It cannot reclassify transcript content, demographic data, summaries, or heuristics into current objective fact.

### `APPLICATION_DERIVED_PRESENTATION_ONLY`

A deterministic derivation from already authorized application observations is permitted only for presentation/session behavior. It MUST retain exact parent statement IDs and transform/version, cannot receive `PROPOSED_CAUSAL_INPUT`, and cannot increase epistemic authority.

### `SCENARIO_DECLARED_NONACTUAL`

Hypothetical/synthetic scenario metadata is lawful only when explicitly marked nonactual and `PRESENTATION_ONLY`. Randomized scenario metadata is permitted only inside this nonactual class and is categorically not a randomized `TodayState` or actual current fact.

### No other source class

LLM output, model inference, demographic stereotype, transcript summary, prior rendered prose, structural prior, historical archive code, mutable “latest” lookup, or heuristic guess is not a source class under v1.0.0.

## 8. Effective-time law

Current-situation authority is temporally explicit.

Every temporally meaningful `situation.*` statement and `interaction.request_received_at` MUST carry:

```text
semantic_effective_time:
  kind = POINT | INTERVAL
  at                     # POINT
  start / end            # INTERVAL; end may be open only when the source explicitly says ongoing
  timezone_or_offset     # when wall-clock interpretation requires it
  basis = CALLER_DECLARED | APPLICATION_OBSERVED | SESSION_EVENT
```

`recorded_at` is always required and remains distinct from semantic effective time.

**No receipt-time laundering:** application request receipt time proves when the request arrived. It does not prove that a caller-described or actor-described condition was effective at that exact time unless explicitly bound so.

**No inferred persistence:** a point/current assertion with no source-authorized continuation is valid for the containing request/turn only. Consumers may not silently carry “at work,” “alone,” “busy,” “at home,” “on phone,” or similar facts forward. When stale or expired, the current view becomes `UNKNOWN` absent a new lawful statement.

A later current-situation statement cannot revise an earlier generated V3 event, actor state, or causal memory.

## 9. Knowledge, certainty, and confidence

Each statement carries one `knowledge_state`:

- `DIRECT_APPLICATION_OBSERVATION`
- `CALLER_SELF_REPORT`
- `CALLER_REPORT_ABOUT_OTHER`
- `SESSION_RECORD`
- `DETERMINISTIC_PRESENTATION_DERIVATION`
- `NONACTUAL_SCENARIO`
- `UNKNOWN`

Each statement carries one `certainty_state`:

- `SOURCE_ASSERTED`
- `SOURCE_EXPLICITLY_UNCERTAIN`
- `MEASUREMENT_QUALIFIED`
- `DERIVED_NO_NEW_CONFIDENCE`
- `UNSPECIFIED`
- `UNKNOWN`

No global trust score exists. Consumers may not invent a numeric confidence from source class, demographics, repetition, plausibility, or model opinion. Source-declared confidence or measurement quality may be retained as provenance, never upgraded by inference.

## 10. Disposition states

### `PRESENTATION_ONLY`

May guide V2 rendering/session behavior only where an exact consumer is authorized. It cannot mutate V3, become structural prior, or be promoted merely because it was displayed or persisted.

### `PROPOSED_CAUSAL_INPUT`

A **noncausal candidate only**. The record remains caller/application evidence and MUST cross the separately governed V2->V3 external-event packaging path and V3 admission gate before any generated causal effect. Before admission it is not a V3 event, cannot mutate actor state, and cannot be cited as generated history. Rejection never becomes history.

Only an otherwise valid statement representing a proposition that could denote an in-world event/condition may receive this disposition. Application-derived presentation context can never receive it.

### `UNKNOWN`

Used when a field is absent, stale, expired, unresolved by contradiction, insufficiently subject-bound, or otherwise not lawfully knowable. `UNKNOWN` must remain representable and must not be auto-filled.

### `INVALID_REJECTED`

Used for malformed or jurisdictionally forbidden records, including missing mandatory provenance/subject/time for a semantic use that requires them. Invalid records cannot be consumed as current situation.

## 11. Contradiction law

Contradiction is first-class evidence, not an invitation to synthesize truth.

- preserve all valid conflicting statements;
- assign a stable `conflict_set_id` for overlapping incompatible claims;
- do not silently overwrite, average, vote, assign a global trust score, or let recency alone resolve the conflict;
- aggregate state is `CONTRADICTED`;
- a consumer requiring one resolved value receives `UNKNOWN` until the conflict is lawfully resolved within a source's own correction jurisdiction or by a separately authoritative source;
- a field-owning application source may replace/correct its own application/session property while retaining audit history;
- no contradiction resolution under this authority changes V3 history.

## 12. Trust / authority precedence

Precedence is **jurisdictional, not scalar**:

1. V3 generated/admitted truth is sovereign for generated-actor causal facts/history.
2. V3 admission receipt is sovereign for whether a causal external event occurred.
3. Direct application observation owns only application/session properties it directly measures.
4. Caller assertion owns the fact and source-declared semantics of the assertion, not objective actor truth.
5. Session record owns session lifecycle/state only.
6. Application derivation may narrow/transform presentation semantics and never increase authority.
7. Nonactual scenario metadata never competes with actual fact.
8. `UNKNOWN` is not lower-quality guessed data; it is the correct result when authority is absent.

No scalar “more trusted source wins” rule may collapse these jurisdictions.

## 13. Relationship to V3 admission

The presentation path is terminally noncausal:

```text
valid current-situation statement
  -> PRESENTATION_ONLY
  -> V2 RenderSituation / SessionState / application presentation
  -> no V3 mutation
```

The causal-candidate path is:

```text
valid source statement
  -> PROPOSED_CAUSAL_INPUT
  -> independently governed V2->V3 external-event package
  -> V3 validates subject/provenance/time/authority under its own admission law
  -> ADMIT or REJECT
  -> only an ADMIT receipt can authorize generated causal effect/history
```

This authority does not implement or redefine the V3 admission gate. It does not use or rely on another W0 worker return; references to other ADP/CAN identifiers state independent future/parallel authority dependencies only.

## 14. Presentation-context law

Presentation-only context may control rendering/session behavior only when an exact consumer contract authorizes it. Typical lawful uses include brevity/modality adjustments, UI layout/routing, displaying a caller-declared current location/time with its epistemic status, or suppressing content based on an explicit current privacy/interruption constraint.

Presentation context may not:

- select or alter structural priors;
- manufacture biography, identity, belief, trait, relationship, memory, or motive;
- become actor causal state through caching/persistence;
- be converted by a summary/LLM into “known facts”;
- be rebound from caller/application to generated actor;
- erase contradiction or unknown state;
- retroactively rewrite actor history.

## 15. Missing-field behavior

Default for every absent authorized field is `UNKNOWN` / omitted-from-render according to consumer contract.

No missing location becomes `home`. No missing privacy/interruption becomes a default risk. No missing device becomes a guessed phone/laptop. No missing current time becomes actor time merely from server time. No missing confidence becomes a numeric score. No missing field may be generated/randomized for “naturalness.”

## 16. Forbidden inferences

Hard failures under v1.0.0 include:

1. location -> nationality, ethnicity, religion/sect, class, party, household, family role, belief, personality, or generated position;
2. IP address -> personal identity, precise physical location, generated-actor location, or belief;
3. device/interface -> age, class, occupation, personality, disability, or generated-actor device;
4. language/locale/channel -> nationality, ethnicity, religion, belief, education, or class;
5. session demographics/questionnaire -> current objective actor facts without a new authorized statement envelope;
6. transcript text/summary/topic stream/`EnergeticField` -> causal memory, relationship state, belief, motive, personality, or current objective fact;
7. caller assertion about a generated actor -> generated actor fact without V3 admission/generation;
8. repeated assertion -> increased objective authority;
9. recency alone -> contradiction resolution;
10. server/request time -> actor event time without explicit binding;
11. application-derived context -> causal candidate;
12. synthetic scenario -> actual current fact;
13. missing field -> default/random/generated value;
14. current caller constraint -> enduring trait;
15. legacy mood/stressor/health/body/battery/location values from `TodayState` -> any semantic authority;
16. caller current context -> V550+ structural prior or producer evidence;
17. caller current context -> retroactive V3 history rewrite;
18. knowledge/certainty state -> invented numeric probability or global trust score.

## 17. Replay / provenance implications

A replayable V2 presentation/session use requires the exact consumed statement IDs plus:

- field key/value hash;
- subject binding;
- source class/source ref;
- recorded time and semantic effective time;
- knowledge/certainty state;
- disposition;
- transform chain/version where derivation occurred;
- authority ID/version;
- conflict/unknown state at the consuming cursor.

Replay must not require mutable “latest,” hidden wall clock, unstored geolocation, unrecorded UI state, or model inference. Causal replay remains owned by V3 admitted external-event ledger/receipts, not by this authority.

## 18. Historical compatibility and evidence boundary

Recovered V2/server machinery was inspected as continuity/negative evidence only. It showed, among other things, legacy `TodayState` defaults/randomization and coarse session dictionaries/database fields, transcript/chat state, demographics/questionnaire material, IP/session data, and country-resolution/session mechanics. Those structures have **zero automatic authority** under this contract.

Recovered session dictionaries/tables may carry the new statement envelopes, but stored legacy keys do not become facts by existence. `conversation_history` remains transcript/session material under its separate retention authority. Legacy `TodayState` generation is incompatible when represented as actual current context. A current-context convenience API, if implemented later, must preserve field-level provenance, semantic effective time, subject binding, expiry/conflict state, and epistemic disposition rather than passing an untyped “context” blob.

At exact base `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`, the repository root contains `README.md`, `data/`, and `section85/`; no current `server/` or application/session implementation tree exists there to inherit as implementation authority. This authority is therefore self-contained rather than a promotion of historical server code.

No historical V5/DDM semantic field is promoted by this authority.

## 19. Evidence inspected

Current/binding evidence inspected directly at the exact base:

- common W0 law and W0-11 assignment in `schematics/release/W0_AUTHORITY_FOUNDATION/LAUNCH_REGISTER.md`;
- `integration/V2_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md` (external-event proposal/admission boundary);
- `schematics/recalibration/TD_R06_V2_PHENOMENOLOGY_EXPRESSION/RESULT.md` (actual caller/session current situation; no randomized Today State);
- `schematics/closure/TD_R07_WHOLE_MACHINE_SYNTHETIC_LIFE/RESULT.md` (Life F transcript/session noncausal boundary);
- `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md` and `RESULT.json` (`ADP-026` / `MUST-026`);
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `state/CURRENT_STATE.md`;
- exact-base repository tree/current application-session source where present.

Historical continuity/authority-recovery evidence inspected directly from archive SHA256 `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`:

- `Rawlsing_code_bundle_staging/v2/life_simulation_schema.py`;
- `Rawlsing_code_bundle_staging/v2/conversation_engine.py`;
- `Rawlsing_code_bundle_staging/server/session_state.py`;
- `Rawlsing_code_bundle_staging/server/session_db.py`;
- `Rawlsing_code_bundle_staging/server/chat/turn.py`;
- `Rawlsing_code_bundle_staging/server/routes/chat.py`;
- `Rawlsing_code_bundle_staging/server/routes/session_bootstrap.py`;
- `Rawlsing_code_bundle_staging/server/routes/session_summary.py`.

The archive was used only after direct SHA verification and only as historical continuity/negative evidence.

## 20. Hostile fixtures

| Fixture | Input/attack | Required result |
|---|---|---|
| `H01_RANDOM_TODAY_STATE` | code randomizes mood/stressor/battery/location/interruption | `INVALID_REJECTED`; never actual current situation |
| `H02_MISSING_LOCATION_DEFAULT` | no location; renderer fills `home` | fail closed to `UNKNOWN` |
| `H03_LOCATION_TO_IDENTITY` | caller/app says Beirut; consumer infers Lebanese/Shia/class/party | reject inference; only exact location statement survives |
| `H04_IP_TO_ACTOR` | server sees client IP; binds generated actor location/identity | reject subject rebinding |
| `H05_CALLER_ASSERTS_ACTOR_FACT` | caller says “actor is at a cafe” | may be `PRESENTATION_ONLY` in explicit noncausal scenario or `PROPOSED_CAUSAL_INPUT`; never direct generated fact |
| `H06_CALLER_ASSERTS_ACTOR_BELIEF` | caller says “actor believes X” | outside current-situation causal fact authority; no belief mutation |
| `H07_CONTRADICTORY_LOCATION` | overlapping caller claims Paris and Berlin | preserve both; `CONTRADICTED`; one-value consumer gets `UNKNOWN` |
| `H08_STALE_CARRY_FORWARD` | prior-turn “at work” lacks continuing interval | unavailable as current after its turn; `UNKNOWN` |
| `H09_REQUEST_TIME_LAUNDERING` | server receipt time used as actor effective time | reject unless explicit actor/time binding exists |
| `H10_SESSION_DEMOGRAPHICS_LAUNDERING` | persisted demographics treated as current actor truth | reject |
| `H11_TRANSCRIPT_SUMMARY_PROMOTION` | summary says “user is busy”; current state set busy | reject; summary is not a source class |
| `H12_DEVICE_REBIND` | caller uses phone; generated actor assumed to use phone | reject |
| `H13_PRESENTATION_TO_CAUSAL` | privacy/interruption used in render then written to V3 memory | reject; no causal promotion path |
| `H14_PENDING_PROPOSAL_AS_HISTORY` | proposed location/interruption stored as actor event before V3 admission | reject; remains noncausal pending input |
| `H15_REJECTED_PROPOSAL_PERSISTS` | V3 rejects candidate; later turn treats it as actor history | reject; session/audit claim may remain only as rejected proposal |
| `H16_SCENARIO_AS_ACTUAL` | randomized hypothetical cafe scenario exposed as actual actor location | reject; scenario must remain nonactual/presentation-only |
| `H17_UNKNOWN_CONFIDENCE_INVENTED` | caller gives no confidence; consumer assigns `0.8/high` | reject; certainty `UNSPECIFIED` |
| `H18_RECENCY_RESOLVES_CONFLICT` | later caller assertion silently overwrites earlier conflicting one | reject; preserve conflict absent source correction semantics |
| `H19_LOCATION_TO_BELIEF` | current location used to infer politics/religion/worldview | reject forbidden inference |
| `H20_CURRENT_TO_RETROACTIVE` | caller says “I live here now”; V2 rewrites past actor residence/history | reject; no retroactive causal rewrite |
| `H21_PRESENTATION_DERIVATION_AS_EVENT` | viewport/UI-derived context packaged as causal event | reject; derived presentation source is never causal-candidate eligible |
| `H22_NO_SUBJECT_BINDING` | value “at home” has source/time but no subject | `UNKNOWN` / `INVALID_REJECTED`; cannot consume semantically |

## 21. Consumer-release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`

Meaning: this authority is complete enough to satisfy the `MUST-026` dependency for `V2-P3`, `V2-P4`, and `V2-P10` once Vozhd Dva accepts/banks it. It **does not** by itself release those packets globally; all other RA-R00 dependencies and production gates remain binding.

No unresolved semantic question inside the bounded ADP-026 jurisdiction requires heuristic implementation. Future field additions or source classes require an authority-version change.

## 22. Final authority token

`ADP_026_CALLER_SITUATION_AUTHORITY = PASS`
