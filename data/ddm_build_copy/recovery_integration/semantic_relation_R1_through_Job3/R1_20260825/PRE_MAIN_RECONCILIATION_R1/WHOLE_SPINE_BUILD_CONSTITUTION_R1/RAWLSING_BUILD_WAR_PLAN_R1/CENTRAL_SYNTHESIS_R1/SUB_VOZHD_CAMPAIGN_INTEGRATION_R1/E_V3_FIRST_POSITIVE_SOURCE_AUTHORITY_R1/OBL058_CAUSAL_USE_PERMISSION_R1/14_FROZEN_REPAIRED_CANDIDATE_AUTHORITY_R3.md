# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R3

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

This R3 candidate repairs only the remaining source-origin provenance defects identified by the fresh distinct R2 independent review. It preserves the already-green R2 source-basis, exact-scope, noncurrent-synthetic fixture, and fail-closed semantics.

It does **not** perform the required fresh distinct independent review of R3.

## Revised identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.2.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@3.0.0`
- executable: `causal_use_permission_candidate.py`

## Exact semantic decision

The candidate decides whether `CAUSAL_USE_PERMISSION` is granted for the exact tuple:

`(actor_id, world_id, subject_id, time_id, transition_id)`

A `PERMIT` may arise only from the frozen source-owned basis registry entry bound to the exact scope digest. Caller-supplied permission booleans, caller-supplied basis kinds, surrogate facts, project-current identifiers, and arbitrary receipt content remain insufficient.

## R3 source-origin repair

The R2 independent review established four remaining defects in the prior receipt-origin wrapper:

1. a caller-accessible arbitrary-body wrapper could confer source-issued status;
2. an issued receipt carried a mutable `_data` slot whose content could be rebound while provenance survived;
3. the receipt exposed a transferable `_marker` usable to construct another accepted receipt;
4. `isinstance(...)` plus a dynamically overridable provenance predicate allowed subclass-defined behavior to satisfy origin checking.

R3 removes all four mechanics.

### Exact issued-object identity ledger

The bounded authority surface is built in one closure. It owns a strong ledger of pairs:

`(exact_issued_object_identity, immutable_source_body)`

The receipt object has `__slots__ = ()` and carries no payload slot, provenance marker, token, decision bit, basis pointer, or mutable per-object authority state.

Validation accepts source origin only when:

- `type(receipt)` is the exact closure-local concrete receipt type; and
- the exact object being validated is present in the issuance ledger by Python identity (`is`).

Equality, hashing, marker possession, subclass predicates, and caller-reconstructed content do not establish origin.

### Immutable authoritative validation body

The authoritative body is stored only in the source-owned ledger as a read-only mapping, with the nested scope also read-only. The public Mapping surface materializes scope copies for inspection; validation does not trust caller-visible Mapping dispatch. It validates the immutable ledger body associated with the exact issued object.

Therefore changing a public copy, constructing a new object of the recovered concrete type, creating a subclass, or changing caller-visible method behavior cannot turn caller content into the exact ledger body produced by the source-owned issuance decision.

## Preserved R2 controls

R3 preserves all of the following:

- `NONCURRENT_SYNTHETIC` only;
- field-specific synthetic namespaces for actor/world/subject/time/transition;
- rejection of the exact project-current first-canary subject;
- exact five-field scope digest binding;
- one frozen registered positive source-owned basis;
- arbitrary or unmatched basis IDs produce `DENY`;
- no caller permission boolean;
- no caller basis-kind input;
- positive basis proof digest bound to exact scope;
- public content digest is treated only as content integrity, never authority origin;
- plain Mapping copies and reconstructed dictionaries are not source-issued receipts;
- no public basis-registration API;
- no current runtime integration, OBL056 positive installation, OBL055 execution, OEE realization, ENCOUNTER creation, or HQ adoption.

## Bounded trust statement

This candidate is a repository-local Python semantic authority fixture, not a network credential or cryptographic identity system. Its R3 claim is exact within the bounded supported authority surface: accepted receipt origin is tied to the exact in-process object identity recorded by the source-owned issuance decision and to the immutable source-owned ledger body for that object.

## Required next gate

After the producer-side governed bounded court is green, R3 still requires:

`EXACTLY_ONE_FRESH_DISTINCT_INDEPENDENT_REVIEW`

The repair worker must not self-review and must not claim adoption readiness until that distinct review returns PASS.
