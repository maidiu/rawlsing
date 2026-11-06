# 01 — Three mechanism contracts, provenance, opacity and computational budgets
**S0–S1 NONISSUING SCIENTIFIC / CONSTRUCTIVE DESIGN.** Not a new CAN registry, not code, not P3-E1's ABI conclusion.

## I. Representation rule: compress the evidence and trajectory, not the number of supposed witnesses

An admitted selected episode may be one of five **analytical evidence forms**. These forms characterize the *meaning of the modeler's selected unit*; they do **not** create five kinds of event in CAN/ADP or authorize new `EventProposal` keys.

| Form | Ontological reference | What it may establish | What it must not fabricate |
|---|---|---|---|
| `SINGULAR_OCCURRENCE` | One actual event and permitted actor participation | Event-specific world/actor experience | A repeated habit, full past, memory or general character |
| `REPRESENTATIVE_EPISODE` | One actually realized case plus a **separately sourced** repeated institutional relation | Example that is characteristic *of those conditions* | Thirty individually witnessed acts from one example; a statistically representative sample without a sampling frame |
| `ACCUMULATED_INTERVAL` | Time-bounded actual social/material process; duration and source coverage explicit | Continued work, care, coercion, opportunity or constraint with specified partial observations | Invented episodes, continuous psychological state change, multiplicative experience counts |
| `RETROSPECTIVE_CRYSTALLIZATION` | Later actor-experienced trigger + prior fixed objective/actor history | New present relevance, a remembered connection, or changed actor interpretation if lawfully emitted | Changing past objective facts or making the actor remember analyst-only content |
| `RUPTURE_CANDIDATE` | Specific discontinuity in material relations/relations among activities | A possible inflection to test under CAN-012 or other qualified authority | Automatically trauma, pathology, conversion, reversal or rupture merely because narratively dramatic |

The **selection function** is artistic/architectural: among source-admissible events and intervals choose a compact set that probes different historically relevant relationships and event functions. Selection must not create a psychological effect just to justify salience. Background-period condensation may bundle already grounded **objective relations and time coverage**, but cannot assert simulated firsthand episodes absent an appropriate admission source.

### Proposed sidecar (noncanonical) — `CompressionEvidenceEnvelope@TEST_ONLY/1`

```json
{
  "envelope_id": "content-addressed evidence ref",
  "event_id": "existing actual event id",
  "representation_form": "SINGULAR_OCCURRENCE|REPRESENTATIVE_EPISODE|ACCUMULATED_INTERVAL|RETROSPECTIVE_CRYSTALLIZATION|RUPTURE_CANDIDATE",
  "represented_window": {"from_clock": "exact", "to_clock": "exact", "coverage_basis": "explicit"},
  "episode_ref": "actual event hash or null for interval-only interpretation",
  "recurrence_basis_refs": ["institution-level recurring relation; not actor participation proof"],
  "actor_participation_refs": ["exact actor-owned performance or access receipts"],
  "actor_history_scope": "UNKNOWN_ACTOR_HISTORY",
  "evidence_scope_roles": ["INSTITUTIONAL_RECURRENCE", "UNKNOWN_ACTOR_HISTORY"],
  "other_actor_contribution_refs": ["real coactor labor/action sources"],
  "material_relation_refs": ["household/work/institution/permission/reward/cost"],
  "scope_and_missingness": {"observed": ["exact"], "unobserved": ["exact"]},
  "eligible_analytical_functions": ["CONSOLIDATION", "REVELATION_TO_OBSERVER"],
  "proposed_semantic_rule_refs": [],
  "objective_history_binding": "root/branch/clock/hash",
  "interpretation_grade": "DESIGN_CONSTRUCTIVE_HYPOTHESIS"
}
```

This is a **documentation shape**, not presently accepted runtime JSON: IDs, `coverage_basis`, exact source readsets, type/value grammar and content hashes would require a bounded owner/ABI design. The accepted `EventProposal` has only `event_id,event_time,operation,source_refs,participants,circumstances,interval`. The current `P2Owner` further accepts only `ADMIT_EVENT`, circumstances `history_refs/language_context`, interval `ACTUAL/SCHEDULED_ONLY` with span. Therefore the sidecar must be **read-only external evidence linked by permitted source identity**, or await owner validation; adding it to `circumstances` would presently be refused. `ACTUAL` interval does not itself prove independent psychological accumulation. No imaginary execution of this shape is claimed.

The minimal necessary distinction in all cases is:
`objective_world_occurrence != actor_actually_participated != actor_causal_state != actor_memory != actor_knowledge != rendered_observation`.

### Source-grain court: institutional repetition is not personal repetition

Four **noninterchangeable evidence scopes** describe source meaning, not new canonical CAN/ADP kinds or executable `EventProposal` fields:

| Evidence scope | Admissible assertion | Illicit promotion |
|---|---|---|
| `INSTITUTIONAL_RECURRENCE` | A relation/practice persists across a sourced interval, possibly enacted by many people | This actor repeatedly performed it, perceived it or remembered it |
| `ACTOR_PARTICIPATED_INTERVAL` | This exact actor participated over a qualified interval, to the specificity the participation source actually warrants | A fabricated number of discrete acts, continuous feeling, or automatically acquired practice |
| `COACTOR_CONTRIBUTION` | Another identified actor performed their own work/contribution | Attribution of that labor, learning or access to the selected actor |
| `UNKNOWN_ACTOR_HISTORY` | Actor participation over the interval is unobserved/unevaluable, even if the institution's recurrence is known | `NO_PARTICIPATION`, `NO_CHANGE`, prior practice, or inferred memory |

The prototype sidecar's `recurrence_basis_refs` and `actor_participation_refs` must be evaluated **independently**; its illustrative `actor_history_scope` is `UNKNOWN_ACTOR_HISTORY` until qualified actor-owned participation establishes `ACTOR_PARTICIPATED_INTERVAL`. `COACTOR_CONTRIBUTION` is explicitly attached to the other actor, even when indispensable to the selected actor's livelihood. Such scopes could be represented by a validated read-only external evidence index, but this text does **not** issue an ABI or guarantee that the sample JSON can be admitted directly to P2Owner.

**Adversarial paired test:** keep one witnessed actor meeting plus a five-year source-backed institutional interval, but remove any actor-owned **earlier interval participation**: institution/history and coactors stay real; the actor gains **no** five-year practice, private memories or longitudinal motive by inference. Conversely, retain a qualified actor-participated interval and remove/withhold the latest selected meeting from the actor's perceptions: the prior qualified participation remains, but no memory or state update from the unperceived meeting is licensed. This is a no-fictitious-history rule, **not** an exhaustive microepisode requirement or a uniform small effect constraint.

### Four-grade transition court — what a constructive test is allowed to do

| Lane | Result when the target rule/observation is available | State and later-reader discipline |
|---|---|---|
| `NATIVE_ISSUED_RULE` | Original competent source/actor authority permits a named target-specific CAN/ADP effect with exact root, rule, clock and source | Only qualified owner commits canonical state; first consumer must actually read that committed state |
| `TEST_ONLY_HYPOTHETICAL_EFFECT` | Explicitly named artistic/scientific **assumption** may generate a reversible **sandbox-only** response/mediator/memory *surrogate* to test whether it changes a later sandbox consumer | Isolated namespace, fixed actor/root/branch/clock, declared provenance and assumption, input mutation/severance RED, cold/replay/rollback, later test-only reader; cannot appear as accepted CAN/ADP fact, original memory or native proof |
| `MISSING_RULE` / `UNEVALUABLE` | Native issuer absent, source/participation insufficient, or state target cannot be evaluated | Native positive result is refused/held; sandbox may explore a distinct **labeled** counterfactual, never replace the native hold |
| `EVALUATED_NO_CHANGE` | Only an actual qualified evaluation found no target change | Certified nonchange is **not** a synonym for unissued rule, missing actor history or sandbox null output |

The TEST_ONLY surrogate **may be persisted inside its isolated experimental namespace solely to prove later conditional dependence**, and its persistence is not a CAN-011 lifecycle transition, ADP-016 memory issuance or extension of #704 production authority. Declare its source and *hypothetical* rule, not fabricated probabilities or universal effect magnitudes. Compare matched positive/negative runs with the same runtime and source cuts; deleting the assumption or actor participation must remove the simulated positive while native holds remain unchanged. No extra model call between the settled 3–5-event batch events is implied.

## II. Mechanism H1 — Historically condensed participation (material activity → possible developmental organization)

**MECHANISM.** A selected actual episode samples a longer history of work, school, caregiving, worship, household duty or collective organization. Mechanistic parents are **activity, object, available means, other people's labor, institutional rules, timing, stakes and actor participation**, not an event adjective. The event may maintain a relation, expose dependence, recruit prior competence, create a new resource constraint, or support *a candidate* acquired operation.

**SOURCE WARRANT.** Leontiev, supplied Portuguese *Actividade, Consciência e Personalidade*, PDF pp. 18–24 and 29–31 (needs become object-directed and one action may realize competing motives); Sève, *Man in Marxist Theory*, printed 193–202 (the worker's own activity and the wages/product available to them are socially mediated rather than immediate equivalents); Kohn & Schooler, 1982 AJS 87:1257–1286 (longitudinal reciprocal relations; work conditions and selection); Elder & Shanahan 2007 (historical timing, trajectories, transitions, turning points); Mortimer 2003 ch. 6 (different work quality and perceived developmental outcomes).

**CONSTRUCTIVE HYPOTHESIS.** A few temporally extended/representative samples can convey a background of recurring material relations when the objective interval and social-process evidence are kept separately from the actual event and from inferred learning. The selection is fictionalized historical *coverage*; not proof of a naturally large one-off psychological effect.

**COMPRESSION METHOD.** Use `REPRESENTATIVE_EPISODE` for one socially typical actual episode, or `ACCUMULATED_INTERVAL` for source-bound continuing constraints/work. Store **one coverage reference**, not dozens of synthetic act IDs. A highly consequential final confrontation may be `RETROSPECTIVE_CRYSTALLIZATION` of that interval. No invented witness count; no global multiplier.

**ACTOR STATE.** Read immutable actor/root/branch/clock and owner-qualified event, ADP-015 relations, actual material opportunities, CAN-010 scoped expectations/strivings and existing CAN-011 PRACTICE/MEDIATOR/TENSION. Possible effect target: qualified CAN-010 expectation or striving, CAN-011 practice/mediator/tension, or **world/relationship-only** update. ADP-016 memory is separate.

**CAUSAL RULE (TEST_ONLY candidate).** (1) Validate event/interval receipt and scope. (2) Check actor-specific *actual* participation and the other party's distinct contribution. (3) Read preexisting capacity, task opportunity, affordance and role permission. (4) Return an explicit alternative set: `WORLD_ONLY`, `RECRUIT_PREEXISTING`, `POSSIBLE_NEW_PRACTICE`, `RELATIONAL_CHANGE`, `UNEVALUABLE`. (5) If and only if original target-specific Rule T/other issuer is accepted, construct an authorized actor-state proposal bound to exact parent/rule/version and commit through `DevelopmentOwner`. Otherwise **no native positive** and retain `MISSING_RULE`; a future competent evaluator's genuine NO_CHANGE is not identical. A separately isolated `TEST_ONLY_HYPOTHETICAL_EFFECT` may try a reversible practice surrogate under a named assumption and source severance, without writing canonical CAN-011 state. Institutional recurrence alone never supplies the actor-participated training history. This is *qualitative inference*, not a terminal enum.

**CONTEXT DEPENDENCE.** Work ownership, tools, coworkers' help, freedom to refuse, childcare, exhaustion, time, state enforcement and task scope can alter expression while leaving a capacity stable. No passive reinforcement or age decay.

**CONTRADICTION.** A craftsperson's growing inspection skill and shrinking control over schedule/pay can coexist. Family duty and rest, wages and craft pride, can remain competing objects.

**OPACITY.** A worker may narrate success as personal grit while failing to notice a coworker's contribution or wage dependency. Analyst-side other labor remains intact; actor claim requires ADP-017 authorization. A user sees the act and authorized expression, not inferred cognitive causation.

**BUDGET.** One interval/evidence reference, minimal actor state readset, one owner evaluation **per selected event only if qualified**, sparse state effect receipts; no LLM calls between events. Storage cost proportional to *selected source refs + state changes*, not supposed hidden acts. Confirm via measured bytes/event, DB reads/event, provider calls/batch and cold-resume time.

**FALSIFIER.** New practice appears despite removal of actor participation, or after swapping B's work into A's actor slot; material opportunity lost deletes learned capacity; an interval with no observed work is encoded as ten performed episodes; preserving same complete prior state and opportunity but swapping class label changes the result.

**AUTHORITY.** Historical theory + study-specific observational findings support scientific plausibility; the synthetic transition is TEST_ONLY. Original CAN-010/011/ADP issuance and later E2 would be required for native behavioral claims.

## III. Mechanism H2 — Conditional plural dispositions and materially contradictory commitments

**MECHANISM.** One actor carries *multiple history-bound, scope-specific* modes of practice/interpretation, obligations and strivings. The current encounter may **activate/inhibit** them through opportunity, authority, sanction, relational trust, situation/role and the other participant. Incompatibility need not be reconciled. Repertoire is not a flat inventory of personality labels.

**SOURCE WARRANT.** Lahire, *The Plural Actor*, printed 50–65 (PDF 71–81: conditional dispositions, negative power of context and inhibition) and printed 66–77 (conditional transfer); Dreier, *Psychotherapy in Everyday Life*, ch. 8, printed 181–189 (conduct of life across sites and coparticipants); Leontiev, PDF 18–24 (activities and motives are organized relationally); Sève, printed 193–202 (social relations among acts); social-structure empirical caution from Kohn & Schooler and Elder. A 2019 Lahire article (DOI 10.1080/21582041.2017.1399213) reinforces the need for successive and parallel biographies.

**CONSTRUCTIVE HYPOTHESIS.** A few actor-local conditional records and exact relational/world pointers can yield dramatically different yet causally compatible encounters **without increasing scene count**. The model must not invent an activated disposition merely to create surprise.

**COMPRESSION METHOD.** Preserve a small set of *source-earned* mediator, TENSION, practice and CAN-010 expectation/striving records with scope and origin refs. For visible event selection, choose contexts that make different already-formed relations relevant; event need not issue a new record. **Latent** here means *not operative/expressed under these conditions*, **not** CAN-011 `DORMANT` lifecycle unless a qualified transition explicitly changes lifecycle.

**ACTOR STATE.** Read CAN-011 records `V3MS_MEDIATOR` (role-tagged), `V3MS_TENSION`, `V3MS_PRACTICE`; CAN-010 expectation scopes, competing striving IDs; ADP-015 actual relationship; current material role power and ADP-017 actor-access rules. No “class”, “religion” or Enneagram variable directly emits a state.

**CAUSAL RULE (TEST_ONLY candidate).** Input is `(actor_identity, current_world_event, actor_access, scoped prior records, relations, actual affordances, authorized Rule-A)`. Derive the set of *eligible action/response streams* by matching exact trigger/readsets; mark inhibited possibilities from denied tools/role/sanction; retain independently qualified inconsistent streams. The actor may comply visibly and experience competing motives, or refuse, defer, evade, or not know what to do. If original CAN-008 Rule A is unissued, the **native** path returns its typed `MISSING_RULE`/`UNEVALUABLE` hold, not an authorized response or CAN-011 mutation. Separately, the declared `TEST_ONLY_HYPOTHETICAL_EFFECT` sandbox may construct a reversible conditional response candidate and test a later **test-only** reader; it cannot write canonical actor state, confer Rule A or turn a counterfactual into a native event. No generic “winner = highest weighted motive”.

**CONTEXT DEPENDENCE.** Audience, punishment risk, membership, bodily fatigue, legal consequences, location, who can observe, access to help, and when the encounter occurs. Transfer across domains is **unknown until tested or separately warranted**; one act of public deference does not make a global trait.

**CONTRADICTION.** Source-backed competing obligations persist across batches; time alone never resolves or strengthens them. A legitimate response may intentionally postpone, compartmentalize or simply fail to reconcile.

**OPACITY.** Actor may recognize only one reason; unspoken motives and social dependencies can remain in the computational model without first-person knowledge. Two observers, one trusted and one exercising institutional power, may see different slices of the same actor. Do not make secret pathology the default explanation for normal conduct.

**BUDGET.** Read a small sparse neighborhood of exact mediator/striving/relationship refs by event target and power relation; store no per-tick activation flags unless owner-required; no continuous recomputation. Measure candidate set size, reads, latency, context bytes and number of refusals.

**FALSIFIER.** Replacing only actor's demographic label generates different behavior while history/relations are fixed; opposite actions are random rather than explained by contexts; unperformed action is counted as a new habit; two users seeing different behavior alter objective prior history; an actor's absence of confession forcibly ends a tension.

**AUTHORITY.** Source-backed plural socialization and cross-context conduct; TEST_ONLY selective-response hypothesis. Any response selection/effects need competent CAN-008 issuance; persistent transformation needs CAN-010/011 issuer.

## IV. Mechanism H3 — Retrospective recontextualization and asymmetrical access

**MECHANISM.** Later practical events, changed social relations and actor-visible signs alter what *earlier occurrences mean now* for the actor and what the actor is able/willing to say. The original event itself remains fixed. “Deep past” may shape later behavior through a lawful **causal trace without a declarative recollection**; the interlocutor sees only a situated expression surface.

**SOURCE WARRANT.** Leontiev's “bitter candy” passage (Portuguese PDF 18–19: conflicting practical/social significance becomes evident after the act), Dreier ch. 8 (socially distributed present/retrospective understanding), Lahire printed 42–65 (past repertoires emerge under present contexts), Elder's timing/linked lives; Archer *Structure, Agency and the Internal Conversation* (2003) is a **conceptual alternative** emphasizing self-deliberation, not a warrant that all causes are conscious. Original ADP-016/017 machine law is **stronger** than these theories for concrete memory/claim semantics.

**CONSTRUCTIVE HYPOTHESIS.** One present event can make a small, previously established history legible in a new way without generating fictional memories or past acts; a successful renderer should preserve both unspoken history and plausible misrecognition. This is not universal “reconsolidation therapy” or automatic insight.

**COMPRESSION METHOD.** Keep immutable exact objective history refs plus a selective actor-memory/epistemic readset; present event has explicit `RETROSPECTIVE_CRYSTALLIZATION` role only when the actor can perceive/participate. A small representation of past relation(s) is enough to produce changed *context of interpretation*. No rewriting objective time/event hashes.

**ACTOR STATE.** Objective ADP-019 occurrence and C9 history; ADP-016 `EVENT_REFERENTIAL_MEMORY` or `CAUSAL_TRACE_MEMORY` if formed; ADP-017 `KNOWLEDGE/BELIEF/UNCERTAINTY/NONKNOWLEDGE` if separately admitted; CAN-010/011 if authorized new practical orientation; V2 renderer reads only `ActorAccessibleRenderEnvelope`. LLM retrospective impressions remain proposals.

**CAUSAL RULE (TEST_ONLY candidate).** (1) Keep objective event ledger unchanged. (2) Later event has an independently admitted actor-facing exposure. (3) Read which prior features were retained, inaccessible or unknown: NEVER rehydrate `UNAVAILABLE` from analyst history. (4) Under accepted ADP-016 formation/reactivation and ADP-017 epistemic effects, propose a changed time-scoped interpretation/claim; otherwise maintain `DEFERRED_MISSING_MEMORY_BASIS` or unknown. (5) Any claim "I misjudged X" requires actual epistemic effect; analyst detection of a mistaken interpretation does not entail actor insight. (6) User renderer selects only permitted public expression and relationship-sensitive presentation. If no authorized rule exists, demonstrate **no hidden native write**, not fake developmental realization. A distinct reversible TEST_ONLY surrogate may probe hypothetical retrospective interpretation against already actor-accessible features; it cannot restore unavailable memory from objective history, grant new actor knowledge or appear as a canonical ADP-016/017 effect.

**CONTEXT DEPENDENCE.** Audience safety, present evidence, old actor-access, strategic silence, relation with user, institutional risk and exact scope of current question.

**CONTRADICTION.** Later understanding may sharpen rather than heal an earlier obligation; multiple interpretations can remain unresolved. A person can give a confident but false self-description while truth/provenance remains private to the system.

**OPACITY.** Three non-equivalent views: objective history and causal ledger; actor's partial memory, belief and knowledge (including possible **mistaken** beliefs); user-visible allowed dialogue. Neither actor nor user receives a privileged analyst causal explanation. A second user does not gain secrets by asking for “full diagnosis”.

**BUDGET.** Few stable memory/epistemic refs and target-scoped retrieval instead of loading biography; recontextualization only at selected relevant events/retrospective half, not every tick. No new LLM call between 3–5 events; existing retrospective/prospective call remains unchanged. Measure envelope sizes, model context, access/denial rate, hallucinated knowledge and retrieval latency.

**FALSIFIER.** The actor accurately describes analyst-only causes without actor provenance; objective prior event hash changes when interpretation changes; model-written “I remember” directly creates ADP-016 memory; opaque action always comes with explanatory confession; changing audience causes the engine to mutate objective history; hidden contradiction required in every ordinary actor.

**AUTHORITY.** Theoretical/creative plausibility is TEST_ONLY; native memory formation/epistemic effects require competent ADP-016/017 issuers. V2 can render only issued/accessible content; no renderer authority to amend actor state.

## V. Budget envelopes and stopping rules

| Envelope | Records and reads | Calls | Honest capability | First limit |
|---|---|---|---|---|
| **Minimal** | Exact history pointer, 1–2 current relation/activity refs, very few conditional actor records; narrow last-batch accessible projection | Existing call N prospective / N+1 retrospective only | Coherent continuity and occasional revelation, limited transfer and opacity | Underrepresentation of long contradictions; prefer HOLD over inventoried psychodynamics |
| **Moderate (preferred first)** | Sparse interval anchors, a few scoped mediators/strivings/practices, explicit objective-vs-memory-vs-epistemic references and per-event readset | No additional ordinary calls; bounded owner-side table reads | Conditional activation, multiple commitments, two-user asymmetry, small retrospective change | Need owner-qualified evidence and disciplined context selection |
| **Rich (still sparse)** | More historical relation anchors, contexts, multiple independent actor traces, narrower domain-transfer contrasts | Same 3–5 boundary; optionally more pre/post evaluation *outside* runtime experiments | More complex social development, joint world/person trajectories and evaluated subtle opacity | Source/currentness and runtime latency, not lack of invented episodes |

**No measured token/cost figure is claimed.** Instrument: input+output tokens per prospective/retrospective half; model invocations/batch; bytes per immutable history record, sidecar and actor state; database reads and fetched history/window per event; median/p95 realization latency; cold reopen/replay time; proof failures by missing source/actor/rule; observer leakage and source-substitution failures. Use per-budget measurements to choose actual policy, not premature constants.

**Stopping rule:** A positive effect that needs a scientifically/semantically unissued rule remains TEST_ONLY or HELD, while actor/world sourcefree demonstrations and qualitative human evaluations can proceed. Never redefine `MISSING_RULE` as `EVALUATED_NO_CHANGE`. Never demand exhaustive hidden lifetimes, but never forge a repeated observation to make sparse lives appear statistically dense.
