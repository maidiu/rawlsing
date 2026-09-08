# OBL059 POSITIVE_APPLICABILITY — FROZEN R2 BOUNDED REPAIR CANDIDATE

## Commission

Branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r2`

Exact starting parent:
`3892f32912dba21177f9663797e3f847822f4c7b`

Frozen R1 semantic candidate retained unchanged:
`8f209b52f81a5c1bf5ed158782f25f56153ac68e`

## Exact repair grain

R2 repairs only the R1 negative-receipt construction failure for packets containing malformed values that `json.dumps` cannot serialize.

The R1 evaluator is retained as the governing implementation for all JSON-serializable packets. R2 intercepts only the exact serialization `TypeError` raised while R1 constructs a receipt, repeats the same frozen semantic checks without receipt hashing, and returns a deterministic JSON-serializable negative receipt.

Malformed non-JSON binding values are represented in the returned diagnostic bindings by deterministic JSON-safe projections. The proof field is a SHA-256 of a deterministic JSON-safe projection of the packet.

## Preserved authority contract

The following R1 authority semantics and identifiers are unchanged:

- authority identity: `OBL059_FIRST_POSITIVE_OEE_DIRECT_POSITIVE_APPLICABILITY_SOURCE_AUTHORITY@R1`
- receipt version: `OBL059_DIRECT_POSITIVE_APPLICABILITY_RECEIPT@R1`
- exact first-canary subject;
- exact actor / subject / world / time / ADP-010 opportunity binding law;
- external ownership of OBL048 structural evidence;
- ADP-007 actor activation ownership;
- ADP-008 developmental-phase ownership;
- ADP-010 as downstream consumer/realization owner, not this source authority;
- rejection of V554, CAN-001, CAN-003, ROUTING and ADP-010 as authority aliases;
- `NONCURRENT_SYNTHETIC`-only candidate execution;
- all no-project-current-effect attestations.

## Explicit non-expansion

This repair does not create or activate an actor, execute ADP-008, admit an ADP-019 occurrence, own causal-use permission, own contact-witness independence, create ENCOUNTER, realize OEE, execute OBL055, install current-positive OBL056, or create project-current positive applicability.

It does not modify the frozen R1 candidate or its returned R1 review packet.

## Court requirement

The governed R2 court must rerun the complete 30-test R1 bounded court through the R2 evaluator, add exact regression checks for bytes/set/object malformed bindings, prove the returned negative receipt itself is JSON serializable, and prove ordinary JSON-safe positive and negative outputs remain exactly equal to R1.

No self-review is part of this commission. A green governed court is a bounded repair result only and is not an independent-review PASS or HQ adoption.
