# OBL058 — CAUSAL_USE_PERMISSION SOURCE AUTHORITY — FROZEN CANDIDATE R1

## Candidate identity

`OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.0.0`

Status: `FROZEN_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

## Exact jurisdiction

This candidate owns exactly one upstream semantic decision: whether `CAUSAL_USE_PERMISSION` is granted for one exact tuple:

`(actor_id, world_id, subject_id, time_id, transition_id)`

for later consumption as an input to ADP-010 / `V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`.

A positive decision exists only when this source owner receives an explicit source-owned causal-use permission basis bound to that exact tuple. Permission never arises by implication, inheritance, proximity, downstream use, or narrative plausibility. An exact-scope negative decision is also source-owned, but neither decision performs any downstream runtime effect.

The candidate intentionally does not embed or manufacture a project-current actor/world/time/transition identifier. A later lawful caller must supply the exact governed tuple, and a later consuming surface must bind explicitly to an adopted receipt contract before any current use can occur.

## Receipt/proof contract

Receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@1.0.0`.

Required fields are exactly:

- `authority_id`
- `schema_version`
- `fixture_class`
- `scope` containing exactly actor/world/subject/time/transition identifiers
- `scope_digest`
- `decision` = `PERMIT` or `DENY`
- `basis_kind`
- `basis_id`
- `receipt_digest`

Validation is fail-closed. Missing/extra fields, wrong authority/schema, wrong actor/world/subject/time/transition, stale time scope, wrong digest, tampering, or a non-source-owned positive basis fail. The bounded candidate can issue receipts only when `fixture_class == NONCURRENT_SYNTHETIC`; all project-current/unknown fixture issuance is rejected.

`SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL`, ADP-010 realization authority, occurrence/admission, actor/world/time proximity, narrative plausibility, and downstream consumption are explicitly non-authoritative surrogate bases and cannot yield `PERMIT`.

## Relationship to current repository authority

OBL048's current proof that the first-canary subject is `SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL` is classification evidence only. It does not imply causal-use permission.

ADP-010 owns OEE realization. It cannot self-supply this upstream permission input.

OBL055 is HQ-current and OBL056 acceptance-binding authority is HQ-current but ZERO-POSITIVE. Neither delegates OBL058 source-owner jurisdiction, and this candidate does not execute OBL055 or install any OBL056 entry.

## Explicit non-ownership

This candidate does **not** own or create:

- actor identity, actor creation, or actor activation;
- positive applicability;
- occurrence admission;
- contact-witness independence;
- ENCOUNTER;
- OEE realization;
- any project-current positive permission instance;
- comparator, PSEPF, OBL032, architecture/topology selection, or sibling-campaign work.

It performs no runtime integration and updates no project-current authority index.

## Court-only issuance guard

The executable candidate deliberately exposes only `issue_noncurrent_synthetic_receipt(...)`. It rejects `PROJECT_CURRENT` and every fixture class other than `NONCURRENT_SYNTHETIC`. This is a constitutional guard, not a claim that this worker owns future adoption/runtime wiring.
