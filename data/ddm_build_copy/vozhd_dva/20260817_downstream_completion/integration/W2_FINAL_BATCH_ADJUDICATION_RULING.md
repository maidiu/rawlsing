# W2 Final-Batch Adjudication Ruling

**Date:** 2026-08-18  
**Authority:** Vozhd Dva  
**Architecture:** `CLOSED`  
**Disposition:** `6 ACCEPT / 1 RETURN_FOR_FIX`

## 1. Holding

`W2_FINAL_BATCH = 6_ACCEPTED__1_RETURN_FOR_FIX_ACTIVE`

Seven final W2 canonicalization cells were released from exact common base:

`ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`

All seven were independently reviewed against their exact launch scope, accepted architecture, W0/W1/W2 law, source-evidence requirements, Governing Spirit, no-starvation/no-bloat law, and MD↔JSON machine contract.

Six are accepted and merged. `CAN-023` is returned for one narrow evaluator-authority correction. W2 authority/contract completion is therefore **not closed yet**, and W3 is **not released**.

## 2. Accepted cells and merge commits

1. `CAN-025` — V2→V3 external-event packaging — PR #127 → `0b32ce6172da0036c6f7a1aaf8f8bbb6acf81267`.
2. `CAN-005` — repository / ContextResolver policy binding — PR #128 → `c75e7c59060a9552ee2b15c8d15067daa57bd3e5`.
3. `CAN-007` — static next-context-change vs generated-life requery — PR #129 → `400cc700aab7c3c2090dd6d1b54189fd5ace3f5a`.
4. `CAN-024` — V2 interaction-mode policy — PR #130 → `a2fdaed9278d597e30ff9587c4e311be66d110f5`.
5. `CAN-022` — V2 render-admission / prompt contract — PR #131 → `0a6ab3dfb1b3e7aa865959865d72060358e1fbe9`.
6. `CAN-004` — immutable V557 publication → V558 repository bundle policy — PR #132 → `46cbfe80afa38f779112ef4d081c789bfc593325`.

Every accepted PR changed exactly its two assigned `AUTHORITY.md` / `AUTHORITY.json` files. No production implementation or sibling-cell artifact was modified.

## 3. Accepted holdings

### CAN-004

`V557_V558_IMMUTABLE_PUBLICATION_REPOSITORY_BUNDLE_POLICY@1.0.0` binds immutable content-addressed publication/repository bundles, exact producer-preserving locators, role/cardinality/order-preserving transitive semantic closure, exact CAN-003 item-governance preservation, atomic fail-closed visibility, and deterministic replay. Item denial outranks collection readiness. V558 verifies/links/indexes only and cannot repair, fuzzy-rematch, semantically coalesce, or use mutable `latest` as authority.

### CAN-005

`V558_CONTEXT_RESOLVER_POLICY@1.0.0` binds deterministic query/index/SelectionRecord/resolution-receipt semantics. Temporal precedence remains:

`DIRECT_TEMPORAL_SUPPORT > authorized LATEST_PRIOR > authorized EARLIEST_POST > NO_LAWFUL_ANCHOR`.

ADP-006 owns proxy eligibility; CAN-006 owns generated-position bindings; producer semantics remain producer-owned. Equal-rank singular ambiguity fails closed; separately authorized multiplicity returns the full tied set. No nearest-time/geography, score, semantic similarity, model judgment, clock, raw-stage, network, RNG, or mutable-default inference is lawful.

### CAN-007

`V558_V3_CONTEXT_REFRESH_REQUERY_CONTRACT@1.0.0` binds two noncollapsed refresh channels:

1. repository-static deterministic `next_context_change` → `STATIC_CONTEXT_CHANGE_WAKE`;
2. committed V3 generated-life change that actually changes a declared query-binding fingerprint → `GENERATED_STATE_REQUERY`.

Static wake is not actor-event prediction. Generated event is not automatically query-relevant. Channel B requeries the same immutable repository. Exact-equivalent triggers may coalesce only with complete reason provenance; no annual tick, polling cadence, wall-clock trigger, repository mutation, or prior-history rewrite is authorized.

### CAN-022

`V2_RENDER_ADMISSION_PROMPT_CONTRACT@1.0.0` preserves renderer-as-wording-only. An already-final semantic expression plan is admitted through proof-carrying model-visible semantic, stimulus-only, and audit-only lanes. Valid-empty plan means no model call and no fallback utterance. Prompt compilation is deterministic, LLM/RNG/network-free. Hidden biography/persona/raw V3/V558/analyst context and provenance dereference are forbidden. Rendered output remains draft surface until wording-only semantic conformance is established; unresolved conformance fails closed.

### CAN-024

`V2_INTERACTION_MODE_POLICY@1.0.0` has exactly two modes:

- `PRESENTATION_NONCAUSAL` — constitutional default;
- `IN_WORLD_CAUSAL` — explicit, packaging-eligible only.

Causal mode does not equal V3 admission. TURN and explicitly authorized SESSION scope are cursor/provenance bound; no accidental causal carry occurs. Renderer/model/content cannot select mode. Rerenders never inherit admission.

### CAN-025

`V2_TO_V3_EXTERNAL_EVENT_PACKAGING_CONTRACT@1.0.0` preserves:

`PACKAGING != ADMISSION != OCCURRENCE != DOWNSTREAM CAUSAL EFFECT`.

The package binds the exact candidate artifact ID/hash, render receipt, actor/participants, source turn/session, interaction-mode receipt, proposed causal-time binding, semantic-plan/render provenance, exact event-kind authority where available, submission cursor and ADP-019 projection. Missing event-kind authority fails closed; there is no generic `conversation_event`. Rejected artifacts cannot evade rejection by repackaging. Only ADP-019 may admit and create/advance V3 causal state.

## 4. CAN-023 — RETURN_FOR_FIX

PR #126 / branch:

`agent/vozhd-dva-w2-can-023-v2-native-translation`

Reviewed head:

`53d12985fa0b5a887205f0298d74200560a1c604`

The native/translation pairing, one-plan law, protected semantic-invariant profile, typed failure/non-substitution law, actor-access and causal boundaries, replay identity, historical archive verification, and consumer split are substantively accepted.

The sole defect is evaluator authority.

Current authority states that a bilingual semantic evaluator may be `model-assisted` and JSON sets:

`model_assistance_allowed = true`.

That violates W2 Batch-02 common law: LLM/model output cannot itself become semantic or causal authority. Pinning model/version/prompt/sampling proves provenance, not semantic adjudication authority.

Required correction:

- model/LLM output may supply diagnostic/non-authoritative alignment annotations or candidate evidence only;
- model output alone cannot establish protected-atom preservation, `PLAN_CONFORMANT`, or `SEMANTICALLY_EQUIVALENT`;
- positive semantic adjudication requires an exact separately governed evaluator rule/authority with machine-bound admissible operations and protected-atom comparison semantics;
- absent such authority, return `MISSING_PLAN_ALIGNMENT_AUTHORITY` and/or `EQUIVALENCE_UNRESOLVED` rather than best-effort pass;
- translation generation may still use models under ADP-025;
- stored model judgments remain diagnostic evidence on replay and do not become authority retrospectively.

Exact Vozhd continuation disposition is recorded on PR #126 as issue comment:

`5330958234`.

## 5. Phase consequence

W2 remains open only for the CAN-023 narrow continuation.

Do **not** release W3 authority or implementation work before CAN-023 is corrected, accepted and merged and an explicit W2 closure ruling is banked.

No other final-batch worker should be rerun.

## 6. External posture

SWID / `EXT-001` remains an independent production gate. W2 semantic acceptance does not release V553 production or bypass physical predecessor/publication gates.

PR #125 remains outside this authority court.

**FINAL TOKEN:**

`W2_FINAL_BATCH = 6_ACCEPTED__1_RETURN_FOR_FIX_ACTIVE`
