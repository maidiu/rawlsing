# OBL059 POSITIVE_APPLICABILITY — FROZEN R3 BOUNDED REPAIR CANDIDATE

## Commission

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r3`

Exact starting HEAD:
`917ee1655f7a4c26277896ef12d788acce15a1c9`

Campaign adjudication consumed prospectively:
`9695eab9fa5b31db4bfc6c7bb977e5af95bbc66c`

Failed frozen R2 candidate retained unchanged:
`ff4f7c8a135997a4e4dd0b9dcb405a143fc6f749`

R2 review blocker:
`BLOCKER__OBL059_R2_NEGATIVE_RECEIPT_FALLBACK_COVERS_ONLY_ONE_JSON_ERROR_SHAPE`

## Exact R3 repair grain

R3 changes only the malformed required-binding negative-receipt serialization boundary.

For ordinary JSON-safe packets, including valid positives and ordinary negative cases, the frozen R2 evaluator remains the governing implementation and R3 delegates to it unchanged.

For a required binding that is already semantically malformed, R3 mirrors R1/R2 initial packet materialization and then performs a dedicated JSON-serialization probe. If that probe reports a serialization-boundary failure, R3 constructs the already-required negative receipt directly rather than asking raw malformed content to pass through R1 receipt hashing.

The repair does not key behavior to exception-message text and does not wrap arbitrary evaluator failures.

## Cycle-safe diagnostic projection

The fallback proof/diagnostic path:

- preserves ordinary JSON-safe values;
- projects bytes by length and SHA-256;
- projects mappings as deterministically sorted key/value projections;
- projects lists/tuples with explicit sequence type;
- projects sets/frozensets with deterministically sorted projected items;
- represents cycles with an explicit type-tagged cycle marker;
- applies a deterministic depth ceiling before Python recursion limits;
- represents opaque objects by stable type identity rather than memory address or repr.

Projected malformed bindings remain structured diagnostic values and cannot become valid string identifiers.

## Preserved authority contract

R3 preserves the R1/R2 authority identity, receipt version, exact first-canary subject, actor/subject/world/time/ADP-010 opportunity binding law, structural/runtime evidence ownership, V554/CAN-001/CAN-003/ROUTING/ADP-010 non-alias law, `NONCURRENT_SYNTHETIC` restriction, and all no-current-effect attestations.

It does not create or activate an actor, execute ADP-008, admit ADP-019, own OBL058 permission, own OBL060 independence, create ENCOUNTER, realize OEE, execute OBL055, install current-positive OBL056, or create project-current applicability.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R3_REPAIR_WORKER = NO`

This worker freezes and tests the R3 repair only. A later distinct reviewer, if commissioned by SUB-VOZHD E, must target this new frozen R3 candidate.
