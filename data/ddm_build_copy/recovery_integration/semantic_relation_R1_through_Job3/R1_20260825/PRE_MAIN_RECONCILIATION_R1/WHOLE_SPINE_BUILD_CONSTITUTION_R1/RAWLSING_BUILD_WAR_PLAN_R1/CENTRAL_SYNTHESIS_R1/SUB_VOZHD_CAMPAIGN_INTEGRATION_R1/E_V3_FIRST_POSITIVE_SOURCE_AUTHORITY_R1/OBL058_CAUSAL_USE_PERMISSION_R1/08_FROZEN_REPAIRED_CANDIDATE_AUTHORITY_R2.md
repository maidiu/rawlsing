# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R2

Status: `FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED__REQUIRES_FRESH_DISTINCT_INDEPENDENT_REVIEW`

This R2 candidate repairs the five blocking validation/provenance defects returned by the prior independent review while preserving the OBL058 lane boundary.

The exact candidate freeze is the commit containing this file after the repaired executable was installed. The immutable SHA is recorded in the governed court specification and the R2 return artifact rather than self-referentially in this file.

## Authority identity

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.1.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@2.0.0`
- fixture class: `NONCURRENT_SYNTHETIC`

This is a repaired candidate revision of the same OBL058 source-authority family. It is not adopted project authority.

## Owned semantic decision

The authority decides only whether one exact bounded synthetic tuple:

`(actor_id, world_id, subject_id, time_id, transition_id)`

has an explicit source-owned `CAUSAL_USE_PERMISSION` basis.

It does not create actor identity, encounter, applicability, contact occurrence, OEE realization, OBL056 current acceptance, OBL055 execution, ADP-010 realization, or any project-current positive fact.

## R2 provenance law

A positive receipt is lawful only when all of the following hold simultaneously:

1. every scope identifier is in its exact field-specific `NONCURRENT_SYNTHETIC` namespace;
2. the requested `basis_id` exists in the source-owned frozen basis registry;
3. that registry record is bound to the exact scope digest;
4. the registry record itself decides `PERMIT` and carries the source-owned basis kind;
5. the returned receipt carries the registry-derived basis proof digest;
6. the receipt is an opaque receipt object emitted by this bounded source-authority instance rather than an arbitrary caller-constructed Mapping;
7. the receipt validates against the exact expected scope and its content-integrity digest.

The public receipt digest remains only a content-integrity check. It is deliberately not treated as an authority seal. Source-issued provenance is a separate condition.

## Repair mapping to prior blocking findings

### R2-F1 — source-owner authenticity

Arbitrary dictionaries are no longer accepted as authority receipts, even when all visible fields and public hashes are recomputed correctly. Validation requires source-issued receipt provenance created by the bounded authority boundary.

### R2-F2 — basis existence and exact-scope binding

The caller can no longer assert an `explicit_source_permission` boolean or choose a magic `basis_kind`. Positive issuance derives only from a frozen source-owned basis record whose stored scope digest equals the exact requested tuple.

### R2-F3 — decision/basis rewriting under public rehash

Returned receipt objects are read-only at the mapping surface. Copying visible fields into a new mapping loses source-issued provenance, so changing `DENY` to `PERMIT`, relabeling basis truth, and recomputing the public digest does not produce a receipt accepted by the validator.

### R2-F4 — fixture-class/scope binding

`ExactScope.validate()` now enforces exact field-specific `NONCURRENT_SYNTHETIC` namespace prefixes and nonempty suffixes. A current-shaped actor, world, subject, time, or transition cannot be admitted merely by retaining the synthetic fixture label.

### R2-F5 — independently verifiable source-permission proof inside the bounded candidate

Positive receipts carry `basis_scope_digest` and `basis_proof_digest`, both checked against the source-owned frozen basis registry. The discarded caller boolean from R1 no longer exists in the public issuance contract.

## Deliberate boundedness

The R2 source-issued provenance mechanism is an in-process bounded candidate mechanism. It is not represented as a cryptographic network credential, durable production signing service, or current runtime adoption mechanism. A future adopted runtime integration must preserve an equivalent or stronger competent source-owned provenance boundary; this repair does not authorize that integration.

The only positive basis presently frozen in the candidate is an explicit `NONCURRENT_SYNTHETIC` court fixture. It exists only to prove the positive semantic branch can be exercised without creating current state.

## Fail-closed requirements

The candidate must reject or deny as appropriate:

- any project-current or unknown fixture label;
- any scope field outside its exact noncurrent-synthetic namespace;
- empty or whitespace-only basis IDs;
- arbitrary/unregistered basis IDs as positive permission;
- reuse of the registered positive basis against a different actor/world/subject/time/transition scope;
- plain mappings or reconstructed copies presented as if source-issued receipts;
- wrong expected scope;
- malformed receipt content;
- positive decisions not backed by the exact registered source-owned basis.

## Adoption boundary

This freeze is eligible only for a governed bounded court followed by exactly one fresh distinct independent review. The R2 repair worker must not self-review.

No SUB-VOZHD E adjudication, HQ adoption packet, project-current positive permission, OBL055 execution, or OBL061 unblocking is authorized by this candidate freeze alone.
