# RAWLSING CENTRAL PROJECT STATE R1 — SCHEMA

The central-state layer is an operational index over already-governed evidence. It does not mint authority, rewrite historical verdicts, or substitute for the deeper source routes.

## State unit

A `PROJECT_STATE.tsv` row is a project-state unit: a campaign/problem body whose authority, runtime, conceptual, ideation, dependency, reintegration and next-action state must be sweepable without branch archaeology.

Required dimensions remain independent:

- `authority_status`: what may govern at the stated grain.
- `runtime_status`: what is serving/executable/current as runtime.
- `conceptual_status`: closed/open/partial/blocked/stranded/unknown state of the problem.
- `ideation_relevance`: whether future conceptual work must factor it.
- `reintegration_status`: whether the significant result is centrally reconciled and canonically inherited.
- `banking_status`: worker/campaign/HQ/canonical acceptance state.

No column may be inferred from another. In particular, physical presence is not authority; local completion is not project completion; canonical Git ancestry is not runtime-currentness.

## Obligation unit

An `OPEN_OBLIGATIONS.tsv` row is the smallest centrally actionable unresolved project obligation after normalization of the W35 open ledger, W41 unfinished/return-required ledgers, W42-W49 additions, and later PRE-MAIN dispositions.

Every obligation must expose: what is known, what is not known, why it remains open, what must not be assumed, dependencies, closure condition, competent closure authority, return destination where applicable, and a deep route.

Allowed active states include `OPEN`, `PARTIALLY_CLOSED`, `BLOCKED_ON_DEPENDENCY`, `SUSPENDED_ON_DEPENDENCY`, `SPAWNED_SUCCESSOR_RETURN_REQUIRED`, `INTERRUPTED_STRANDED`, `RETURN_REQUIRED`, `UNKNOWN_REQUIRES_SYNTHESIS`, `SUPERSEDED_AT_GRAIN_WITH_SURVIVING_OBLIGATION`, and `ABANDONED_BY_EXPLICIT_DECISION`.

A source row that has since been competently satisfied is mapped in W55 normalization receipts rather than kept falsely open.

## Reintegration unit

A `REINTEGRATION_LEDGER.tsv` row tracks a significant work unit separately from its local success. `LOCAL_COMPLETE_UNRECONCILED`, `CAMPAIGN_ACCEPTED_UNBANKED`, `HQ_BANKED_NOT_CANONICALLY_INHERITED`, `BLOCKED_ON_DEPENDENCY`, `SPAWNED_SUCCESSOR_RETURN_REQUIRED`, and `INTERRUPTED_STRANDED` remain open project states.

Project-level closure requires central disposition and canonical inheritance, or an explicit centrally recorded non-adoption/preservation decision.

## Ground versioning

`00_RAWLSING_GROUND.md` is a versioned cognitive surface, not a self-hashing authority source. Grounding receipts must record the exact canonical project head actually read plus the declared ground version. A later validator must compare both against the then-current canonical project state and fail closed on mismatch for project-level adoption.


## Post-PRE-MAIN maintenance invariant — 2026-09-06

The Sep 2–6 post-PRE-MAIN campaign demonstrated that a project may preserve one lawful cumulative ancestry while still allowing its central cognition to become stale. The following maintenance law is therefore explicit:

```
SIGNIFICANT_HQ_ADOPTION_OR_CENTRAL_FANIN
=> CENTRAL_STATE_DELTA_REQUIRED_BEFORE_NEXT_MAJOR_WAVE
```

A central-state delta must disposition, at minimum, touched project-state rows, obligations, dependencies, reintegration status and next actions. A no-change disposition is permitted, but silence is not.

```
ACTIVE_WORKING_BRANCH != CANONICAL_PROJECT_REF
PHYSICAL_BRANCH_PRESENCE != PROJECT_AUTHORITY
MERGED_BRANCH != AUTOMATICALLY_SAFE_TO_DELETE
```

When a temporary/legacy working branch becomes the de facto cumulative integration line, a competent Vozhd must either re-anchor the declared canonical project ref by verified non-forced fast-forward or record an explicit reason the divergence remains open.

Before launching a new major successor wave, the commissioning authority must verify that the central-state sweep reflects every materially inherited HQ adoption/fan-in on the working ancestry. If not, the legal next phase is `INTEGRATE / CLOSURE_ONLY`, not new semantic expansion.
