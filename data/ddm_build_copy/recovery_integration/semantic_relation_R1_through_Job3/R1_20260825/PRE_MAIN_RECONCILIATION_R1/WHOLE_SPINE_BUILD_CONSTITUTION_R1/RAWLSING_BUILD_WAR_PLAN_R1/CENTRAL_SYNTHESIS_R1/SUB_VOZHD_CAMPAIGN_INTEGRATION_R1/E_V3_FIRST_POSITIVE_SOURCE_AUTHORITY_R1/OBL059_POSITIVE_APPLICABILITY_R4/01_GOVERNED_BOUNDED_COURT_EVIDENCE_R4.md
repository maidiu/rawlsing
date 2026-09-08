# OBL059 POSITIVE_APPLICABILITY — GOVERNED BOUNDED COURT EVIDENCE R4

## Exact identities

Repository: `maidiu/rawlsing`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r4`

Exact start:
`ae3fe2f88694887f5ab57c86723e8cf9fc1b1e59`

Prospective campaign adjudication/instruction:
`c534098e280ca9c5d05d072f1688a1e7496eedff`

Failed frozen R3 candidate retained unchanged:
`4fdb897e8a089787d7407197fd49bbd1ef51f2ef`

Frozen R4 candidate:
`830cc0442f34e8b28405006c031cc1d256893a17`

R4 authority blob:
`8cfc6863f7a666c938e4e4024c7348b5f0d15263`

R4 bounded-court blob frozen with candidate:
`0b184855b4a297ccc899d3c1b0b512c79b105cec`

Governed evidence routing commit:
`127a74c3261dd81b81c35b4b01d20482d18da2f3`

Corrected evidence execution commit:
`d9ca7b881c58a24806d6d218bf338272b8b5d061`

Corrected execution-wrapper blob:
`6bbffb0370c68acc8d1ae787150863bdc4eee4ad`

## Exact repair exercised

The court reruns the inherited R1/R2/R3 bounded controls through R4 and directly checks the R3 review blocker plus the broader R4 command surface.

R4 traverses only exact built-in `dict`, `list`, `tuple`, `set`, `frozenset`, and `bytes` operations in the malformed diagnostic/proof path. Arbitrary/custom values are represented by a fixed JSON-safe diagnostic category without asking them to provide mapping iteration, `items`, `keys`, `values`, length, display, hashing, equality, or ordering behavior.

Direct R4 regressions cover throwing `Mapping.items()` at every required binding; a custom Mapping whose relevant protocol/display/comparison methods all raise; exact built-in mappings containing hostile custom keys/values; mixed nested custom/built-in malformed structures; circular, mutually recursive, shared-reference, and deep graphs; the original bytes/set/frozenset/opaque forms; deterministic repeated receipts and proof hashes; structural distinction; exact JSON-safe R3 preservation; wrong-scope/authority/evidence/project-current controls; malformed-to-positive noncoercion; and unrelated TypeError/ValueError/RuntimeError visibility.

## Governed execution history

### Initial routing run

Run: `34230622456`

Job: `102075532693`

Protocol self-test: `20 passed in 0.08s`

Court-spec validation: `PASS`

Court result: `56 passed, 1 failed, 174 subtests passed in 0.26s`

Artifact: `10057607016`

Artifact ZIP SHA-256:
`548b2031ec998b06fcff31bbdbe7d89202c59e695f2124265a9fb99cbc6fce26`

The sole failure was a court-routing mismatch in inherited R3 test 43: that inherited test temporarily replaced a different separately loaded R3/R2 module instance than R4 actually delegates to. The R4-specific programmer-error preservation test targeted the correct module and was not the failure. No R4 candidate code was changed.

### Corrected governed run

The execution wrapper was corrected only to route the inherited R3 preservation check to R4's actual delegated R3 module. Frozen R4 candidate `830cc0442f34e8b28405006c031cc1d256893a17` and its authority blob were unchanged.

Run: `34230793386` — `success`

Job: `102076114178` — `success`

Protocol self-test: `20 passed in 0.10s`

Court-spec validation: `PASS`

R4 governed court:
`57 passed, 174 subtests passed in 0.21s`

Artifact: `10057679356`

Artifact ZIP SHA-256:
`453a0582be865d9658a3f8b62e48e0b304a0af91d71bf1d835569100adec6aef`

Execution-only PR `#287` was closed unmerged after evidence capture.

## Court disposition

`PASS__OBL059_R4_BOUNDED_REPAIR_GOVERNED_COURT_GREEN__NO_SELF_REVIEW`

The exact commissioned R3 blocker is closed in the producer court, and the wider malformed-diagnostic surface required by the R4 command is green.

This is bounded producer evidence only. It is not an independent-review result and not an adoption act.

## Separation and no-current-effect attestations

`INDEPENDENT_REVIEW_PERFORMED_BY_R4_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ACTOR_CREATED_OR_ACTIVATED = NO`

`ADP008_PHASE_TRANSITION_EXECUTED = NO`

`ADP019_OCCURRENCE_ADMITTED = NO`

`CAUSAL_USE_PERMISSION_OWNED = NO`

`CONTACT_WITNESS_INDEPENDENCE_OWNED = NO`

`ENCOUNTER_CREATED = NO`

`AUTHORITY_INDEX_MUTATED = NO`

`HQ_ADOPTION_CLAIMED = NO`
