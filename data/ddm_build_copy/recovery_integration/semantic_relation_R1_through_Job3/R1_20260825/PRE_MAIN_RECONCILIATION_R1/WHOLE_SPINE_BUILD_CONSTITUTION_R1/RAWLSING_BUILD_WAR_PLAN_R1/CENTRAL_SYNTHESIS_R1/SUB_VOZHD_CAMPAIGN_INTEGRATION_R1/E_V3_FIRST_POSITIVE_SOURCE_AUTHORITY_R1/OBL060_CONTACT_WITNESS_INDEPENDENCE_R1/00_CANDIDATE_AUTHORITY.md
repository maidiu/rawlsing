# OBL060 CONTACT-WITNESS-INDEPENDENCE — FROZEN CANDIDATE AUTHORITY R1

Status: `CANDIDATE_ONLY__NOT_PROJECT_CURRENT__NONCURRENT_SYNTHETIC_ONLY`

Candidate authority identity:

`V3_CONTACT_WITNESS_INDEPENDENCE_SOURCE_AUTHORITY_CANDIDATE@1.0.0`

Receipt kind:

`V3_CONTACT_WITNESS_INDEPENDENCE_RECEIPT_CANDIDATE@1.0.0`

## Exact jurisdiction

This candidate owns only the proof contract by which one already-identified contact-occurrence witness can be shown, for ADP-010/OEE consumption, to be grounded in a source-owner record that is distinct from the occurrence authority.

It does not admit, create, validate, or activate an occurrence. It does not own ADP-019. It does not realize OEE. It does not create ENCOUNTER, actors, applicability, causal-use permission, current independence, OBL055 output, or OBL056 current-positive entries.

## Occurrence-vs-independence non-identity

Occurrence authority is fixed, solely as an input identity, to:

`V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0`

The independence source-owner authority identity is the candidate identity above. The two identities MUST be unequal. An occurrence receipt is linkage material only; it cannot self-certify independence and cannot be reused as the independence source record or independence receipt.

ADP-019 remains occurrence admission authority under its own law. Nothing here converts, aliases, extends, or treats ADP-019 as witness-independence authority.

## Exact proof contract

All executable candidate paths require `fixture_class == NONCURRENT_SYNTHETIC`.

A passing proof requires all of the following:

1. an occurrence envelope naming the exact occurrence, exact ADP-019 occurrence-authority identity, occurrence scope, independent occurrence-receipt id, and digest;
2. a separate source-owner witness record, owned by this candidate authority and bound to the same occurrence under the exact independence scope;
3. the exact positive basis `DISTINCT_SOURCE_OWNER_BOUND_WITNESS_RECORD`;
4. a separate source record id, evidence digest, and independence receipt id that cannot reuse the occurrence receipt id/digest;
5. exact source-record and receipt digest binding;
6. an unexpired validity interval; and
7. exact expected occurrence, authority, and scope match.

The digest checks are integrity/binding controls for the explicit synthetic fixture. They do not mint live trust, validate ADP-019, or establish a project-current fact.

## Mandatory rejection law

The following are insufficient, individually or in any mixture, and are hard rejected even when mixed with the positive basis:

- `SELF_CERTIFICATION`
- `AUTHORITY_IDENTITY_REUSE`
- `RECEIPT_REUSE`
- `CO_LOCATION`
- `CO_PRESENCE`
- `SAME_GEOGRAPHY_TIME`
- `SHARED_ENDPOINT`
- `INSTITUTION_CLASSIFICATION`
- `NARRATIVE_PLAUSIBILITY`

Unknown additional bases also fail closed, preventing laundering through renamed or extra plausibility assertions.

## Non-ownership / no-effect attestation

The candidate module is a pure in-memory contract. It imports no network, database, filesystem-write, subprocess, or project-current mutation mechanism. Its exported forbidden-effect surface set is test-checked for absence.

No project-current occurrence or independence fact is created by the candidate or its court.
