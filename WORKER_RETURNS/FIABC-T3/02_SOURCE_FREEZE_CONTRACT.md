# FIABC-T3 — Generic Source Freeze Contract

Schema:

`RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0`

## Purpose

This receipt is the execution-level candidate-neutral freeze boundary consumed before any A/B/C candidate process starts.

It is deliberately source-family agnostic. The current T2 manifest happens to execute LiTS-I and WVS7; the contract itself does not encode either name and can bind any source exposed by a future CLOSED_35 execution manifest.

## Required top-level fields

- `schema`
- `candidate_neutral = true`
- `frozen_before_candidate_execution = true`
- `candidate_outputs_seen = 0`
- `candidate_owned_roots_consulted = []`
- `candidate_owned_state_reused = false`
- `state = FROZEN_READ_ONLY`
- `source_freezes`
- `authority_identities`
- `workload_identities`
- `oracle_identities`
- `freeze_order`

Candidate-specific top-level fields such as `candidate`, `candidate_id`, `candidate_owner`, or `selected_candidate` are forbidden.

## Source entry

`source_freezes` is keyed by source ID.

Every entry must carry:

- `source_id` — exactly equal to the map key;
- `canonical_source_sha256` — exact 64-hex physical source root;
- `source_identity_authority_ref` — nonempty authority/evidence reference;
- `derivative_identity` — null unless a derivative is the admitted physical carrier;
- `derivative_to_source_provenance_ref` — null unless a derivative is used.

The two derivative fields form one indivisible provenance assertion:

`derivative_identity present ⇔ derivative_to_source_provenance_ref present`.

A derivative may never replace the canonical source root. It may only stand as a carrier whose provenance closes back to the frozen canonical source SHA.

## Oracle entry

`oracle_identities` is also keyed by source ID and must cover exactly the source set frozen by the receipt.

Each entry requires:

- `oracle_identity_sha256`;
- `oracle_freeze_authority_ref`.

The execution freeze receipt does not allow a candidate output, candidate cache, candidate session, candidate transformed carrier, majority vote, or first-successful candidate to supply this identity.

The actual I05 oracle bundle remains independently content-addressed under `pre553_independent_parity_oracle.py`.

## Freeze order

`freeze_order` requires integer sequences satisfying:

`source_identity_freeze_sequence < authority_workload_freeze_sequence < oracle_materialize_freeze_sequence`.

Candidate process start is not itself written into the upstream receipt, because the receipt must already exist before that process starts. The process envelope later records the candidate-local start timestamp and the exact upstream receipt SHA-256.

## Manifest binding

Before live execution, the driver iterates the source registry exposed by the current execution manifest.

For every admitted source it requires:

`manifest.sources[source_id].sha256 == source_freezes[source_id].canonical_source_sha256`.

This is a generic manifest/source-root equality rule. No LiTS/WVS switch is used.

The process envelope repeats that equality check at cell start against `StageContext.source_sha256`.

## CLOSED_35 safety property

A future manifest can expose any of the CLOSED_35 waves and reuse this exact contract by supplying:

- that wave's `source_id`;
- canonical exact-source SHA-256;
- accepted source-identity authority reference;
- optional derivative identity and exact provenance reference;
- frozen authority/workload identities;
- source-local independent oracle identity.

No per-wave process adapter is required.
