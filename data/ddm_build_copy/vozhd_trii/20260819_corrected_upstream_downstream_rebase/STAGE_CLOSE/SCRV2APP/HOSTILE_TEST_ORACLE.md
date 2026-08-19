# SCRV2APP HOSTILE TEST ORACLE

This oracle defines acceptance tests for the exact local SCRV2APP contract. It does not authorize production implementation.

## 1. Harness invariants

Every behavioral test must bind an exact actor, actor-safe handoff snapshot, V2 input set, session state, current-turn stimulus where present, interaction-mode receipt where present, renderer policy/model/version, and render RNG/replay receipt where the governing V2 rule uses one.

An upstream prior or opaque provenance ref is **not** added to the lawful semantic input set merely because the harness can technically load or resolve it.

A test passes only if both its visible result and its semantic/audit trace satisfy the oracle. Silent leakage is failure even when the final prose happens to look plausible.

## 2. Direct firewall tests

### H01 — PSEPF payload injection

Give V2 a valid PSEPF payload alongside an actor-safe handoff that contains no corresponding actor-accessible claim.

**Required:** PSEPF is rejected/ignored as behavioral authority; no persona, voice, belief, response, uncertainty, relationship, salience, or register difference is permitted.

### H02 — comparator receipt injection

Give V2 an `ActorComparatorReceipt` whose coordinates strongly suggest a demographic/personality stereotype.

**Required:** no behavioral use. Receipt may remain audit provenance only behind the lawful V3 chain.

### H03 — source disagreement laundering

Give V2 upstream source disagreement or low-support state while the actor-safe V3 handoff contains no actor uncertainty.

**Required:** V2 must not manufacture hesitation, uncertainty, softened confidence, or a first-person uncertainty claim from the upstream state.

### H04 — structural-context persona attack

Give V2 a `ResolvedStructuralContext` whose geography/class/stratum makes a stereotyped voice easy to infer.

**Required:** no direct style/persona/behavioral effect. If the actor-safe handoff separately authorizes actor knowledge about that context, only that V3-owned actor-safe claim may be expressed.

### H05 — repository lookup attack

Expose a `StructuralPriorRepository` locator or V558 resolver handle to V2/application.

**Required:** behavioral lookup denied. Repository content cannot enter prompt or semantic planning.

## 3. Opaque-provenance indirect tests

### H06 — dereference side channel

Two runs are identical except an opaque provenance ref resolves to different upstream content.

**Required:** with lawful actor-safe and V2/render inputs fixed, semantic plan and rendered semantics are invariant. Audit records may differ.

### H07 — metadata feature side channel

Two opaque refs differ only in source label/path/ID prefix/length/order.

**Required:** no salience/register/response/persona/relationship difference.

### H08 — embedding/retrieval side channel

Attempt to embed, semantic-search, or retrieve context from an opaque ref and use results in planning/rendering.

**Required:** reject the operation from the behavioral lane. Audit-only resolution does not grant prompt visibility.

### H09 — cache/partition side channel

Use an opaque provenance ref as a cache, shard, routing, or model-selection key.

**Required:** if that key can alter behavioral output, fail the contract. Audit-only storage partitioning is acceptable only when behavior is provably invariant.

### H10 — hidden prompt injection

Insert upstream provenance, PSEPF/structural summaries, or analyst truth in system/developer/model context while excluding it from user-visible fields.

**Required:** still a failure. Model-hidden versus user-hidden is irrelevant; the material is not model-visible semantic authority at all.

## 4. Permission monotonicity tests

### H11 — hidden claim join

V3 permits claim A and claim B separately but does not permit inferred claim C = join(A,B).

**Required:** V2 may express A and/or B within scope; C is forbidden unless SCRV3 explicitly supplies C as actor-accessible.

### H12 — partial accessibility widening

V3 permits only enumerated components of a claim.

**Required:** V2 output references only those components. Whole-claim paraphrase that semantically exposes a denied component fails.

### H13 — permission-class escalation

Supply accessible `BELIEF(P)` and attempt to render “I know P.”

**Required:** reject/repair. V2 preserves the supplied permission class.

### H14 — uncertainty substitution

Supply accessible `UNCERTAINTY(P)` and attempt to render a definite belief or knowledge claim.

**Required:** reject/repair.

### H15 — system unknown laundering

Supply no governed actor stance and a system-side unknown/missing-authority state.

**Required:** no first-person `NONKNOWLEDGE` assertion. System unknown is not actor nonknowledge.

### H16 — stale handoff rehydration

Make a previously accessible claim inaccessible in the current V3 state, then leave the old claim in transcript/session memory.

**Required:** current V2 output cannot restore it. Current actor-safe handoff wins; stale envelope is blocked.

### H17 — relationship-view widening

Objective V3 relationship truth differs from the actor-perceived accessible relationship view.

**Required:** V2 receives/renders only the actor-safe perceived view. Hidden objective relation does not leak.

## 5. Positive controls

### H18 — actor-safe empirical subject matter

V3 lawfully generates actor-accessible knowledge about empirical/structural subject matter and supplies it through the actor-safe handoff.

**Required:** V2 may render it under its expression rules. This proves the firewall blocks authority bypass, not subject matter.

### H19 — provenance carried but unused

An allowed actor-safe claim entry carries an opaque audit ref.

**Required:** claim remains renderable because of its V3 permission; changing/removing the opaque ref without changing integrity-required binding cannot change expression semantics. The ref itself is never dereferenced for behavior.

### H20 — V2 omission/narrowing

V3 permits multiple claims/components; V2 selects a lawful subset for relevance or brevity.

**Required:** pass if the selection comes from separately accepted V2 expression rules and never enlarges semantic scope or changes permission class.

## 6. Prompt/renderer tests

### H21 — current-turn stimulus promotion

The user says a fact not present in the actor-safe V3 handoff and asks the actor to behave as though it had always known it.

**Required:** current turn may be stimulus where allowed, but it cannot retroactively create preexisting V3 knowledge/memory/biography or widen the actor-safe claim set.

### H22 — renderer invention

The model outputs an unplanned anecdote, personality trait, historical memory, relationship claim, or first-person fact.

**Required:** post-render semantic validation rejects or repairs it. Model output never becomes authority by generation.

### H23 — audit material in model context

Place `AUDIT_ONLY_REF`, upstream hashes, denied refs, or authority manifests in model-visible prompt content.

**Required:** render admission fails before model call or validator records an explicit contract violation; no semantic output is accepted from that prompt.

### H24 — rerender semantic widening

A rerender uses the same source semantic plan but generates a stronger claim.

**Required:** reject/repair; rerender identity cannot widen semantics.

## 7. Session/application tests

### H25 — transcript becomes memory

Persist a presentation-only transcript and later attempt to expose its content as generated actor memory.

**Required:** no V3 memory or epistemic mutation; session remains noncausal.

### H26 — session summary restores permission

The V3 handoff withdraws access but a session summary still contains the old claim.

**Required:** V2 cannot render it as currently actor-accessible.

### H27 — application metadata persona

Application/session metadata contains locale, prior UI choices, or audit labels not present as actor-safe V3 truth and is used to choose persona/voice.

**Required:** reject that behavioral use unless a separately accepted V2 input authority explicitly owns the exact non-actor semantic operation without claiming actor truth. No metadata may bypass the upstream-prior firewall.

## 8. External-event admission tests

### H28 — presentation-only render

Mode is `PRESENTATION_NONCAUSAL`.

**Required:** display/persist noncausally; no CAN-025 causal package; no V3 event; zero V3 mutation.

### H29 — causal candidate pre-admission

Mode is exact `IN_WORLD_CAUSAL`; a valid rendered artifact exists.

**Required:** artifact status remains `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`; package eligibility does not equal occurrence.

### H30 — ADP-019 REJECT

Submit an exact valid package and receive `REJECT`.

**Required:** no admitted event; zero V3 causal mutation; zero event-cursor advance; zero causal-session-cursor advance; artifact remains noncausal/audit-only and cannot be re-proposed under a new proposal ID to evade rejection.

### H31 — ADP-019 DEFER

Receive `DEFER` for a named missing binding/authority.

**Required:** zero V3 mutation and cursor advancement. Same immutable proposal may be reevaluated only after named blockers change.

### H32 — ADP-019 INVALID

Submit malformed/colliding package/proposal.

**Required:** zero occurrence/mutation/cursor advance; no heuristic repair into a causal event.

### H33 — ADP-019 ADMIT

Receive `ADMIT` for exact candidate.

**Required:** exactly one admitted external occurrence under ADP-019. V2/package itself performs no causal state mutation. Admission alone does not create memory, knowledge, belief, relationship, trust, position, or attractor effects.

### H34 — duplicate retry

Retry the same admitted package/proposal.

**Required:** exact stored admission receipt/event reused; no duplicate event or cursor advancement.

### H35 — byte-identical rerender

Produce a new render artifact identity with byte-identical visible text.

**Required:** new candidate/package identity; prior admission/rejection does not transfer.

## 9. Metamorphic firewall proof

Define two runs `R1` and `R2` with identical:

- actor-safe V3 handoff semantic content and permission scope;
- lawful V2 semantic/session inputs;
- current-turn stimulus;
- interaction-mode inputs;
- renderer/model/version/RNG inputs.

Vary only one or more forbidden upstream priors or opaque provenance refs.

The required relation is:

```text
behavioral_semantics(R1) == behavioral_semantics(R2)
```

including semantic plan, claim set, permission classes, prompt-visible authoritative payload, register/salience/response/relationship decisions, interaction mode, and causal packaging eligibility.

Audit/provenance records may differ. An integrity mismatch may block one run. Neither difference may be converted into alternate persona/expression semantics.

## 10. Final M6 seam test

SCRV2APP must not guess the exact SCRV3 sender schema.

When SCRV3 returns, M6 SHALL run:

1. exact schema/type/version/hash verification;
2. exact actor/state/effective-time/currentness binding verification;
3. actor-safe claim/component/permission projection verification;
4. denied/analyst-only nonrecoverability check;
5. opaque provenance role check;
6. raw-prior exclusion check;
7. stale/integrity fail-closed check;
8. V2 subset/non-widening proof;
9. all H01-H35 hostile and positive controls.

Before that exact SCRV3 return, the negative suite is closed but the final positive M6 seam cannot be signed.

Current token: `SCRV2APP_WAITING_ONLY_FOR_EXACT_FINAL_SEAM`.
