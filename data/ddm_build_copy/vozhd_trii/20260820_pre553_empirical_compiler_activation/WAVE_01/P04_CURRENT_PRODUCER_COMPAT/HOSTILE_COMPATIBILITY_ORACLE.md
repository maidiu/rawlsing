# PRE553 P04 — Hostile Compatibility Oracle

Every case below is a required fail-closed property for an I04 adapter consuming the P04 compatibility matrix.

| ID | Hostile input / condition | Required outcome |
|---|---|---|
| P04-H01 | Candidate parses as a V550-family object but exact producer/source authority is absent | `REJECT_PROVENANCE_MISMATCH` |
| P04-H02 | Candidate has a familiar V55x filename/schema but carrier identity is ambiguous | `REJECT_AMBIGUOUS_CARRIER_IDENTITY` |
| P04-H03 | A `query_failed`, `missing` or `not_observed` producer state is normalized to numeric `0` | `REJECT_NEGATIVE_SEMANTICS_COLLAPSE` |
| P04-H04 | A valid generated numeric `0` is treated as missing/unknown because it is falsey | reject implementation; valid zero must survive as value |
| P04-H05 | A valid generated Boolean `false` is treated as absent/unknown | reject implementation; valid false must survive as value |
| P04-H06 | Producer scope is `filtered` but migration labels it as `all` | `REJECT_SCOPE_DOWNCAST` |
| P04-H07 | Aggregate or finite-universe evidence is downcast to a narrower/different universe without exact authority | `REJECT_SOURCE_UNIVERSE_MISMATCH` |
| P04-H08 | V550J is accepted as V550 solely because their names/shapes look related | `REJECT_UNPROVEN_PARITY` |
| P04-H09 | V551J is accepted as V551 solely because their names/shapes look related | `REJECT_UNPROVEN_PARITY` |
| P04-H10 | V552J is accepted as V552 solely because their names/shapes look related | `REJECT_UNPROVEN_PARITY` |
| P04-H11 | Missing PRE553 meaning is repaired by invoking a retired V550/V551/V552 runtime path | `REJECT_RETIRED_RUNTIME_FALLBACK` |
| P04-H12 | Active V558 repository/metadata state is used as present empirical runtime context | `REJECT_V558_CURRENT_RUNTIME_FALLBACK` |
| P04-H13 | A retired carrier is chosen because it returns a value where current ingress cannot prove one | `REJECT_RETIRED_RUNTIME_FALLBACK` |
| P04-H14 | Candidate uses an R1-like object from a study other than exact `ATP_W135` | `REJECT_SOURCE_UNIVERSE_MISMATCH` |
| P04-H15 | R1 source file hash differs from `6cec90ec72df360341236f7634d5d76c9a0604168d4174a03e8b8efd388bbbae` | `REJECT_SOURCE_UNIVERSE_MISMATCH` |
| P04-H16 | R1 manifest hash differs from `84009652424d200ced06933173eb8b2f8fb89d51f7909d3da40f6f59ad5da9d9` | `REJECT_SOURCE_UNIVERSE_MISMATCH` |
| P04-H17 | R1 respondent identity is reconstructed from row order rather than exact source-backed respondent keys | `REJECT_SOURCE_UNIVERSE_MISMATCH` |
| P04-H18 | Provenance says two objects share an origin and adapter therefore composes them without composition authority | reject; provenance is not composition authority |
| P04-H19 | Exact parity cannot be proved, but adapter accepts because all inspected numeric values happen to agree | `REJECT_UNPROVEN_PARITY` |
| P04-H20 | Adapter resolves ambiguity using `latest`, filesystem order, filename resemblance, fuzzy matching, embeddings, LLM judgment or randomness | reject as unproved/nondeterministic parity |
| P04-H21 | Producer generated-content success condition is not met but migration supplies a constant/default value | reject; generated empirical meaning not established |
| P04-H22 | Artifact type changes but exact semantic dimensions are preserved and mechanically proved | `ADMIT_EXACT_PARITY` — artifact-class difference alone is not semantic |
| P04-H23 | Exact R1 authority, universe, hashes, respondent identity and exclusions all match | `ADMIT_R1_EXACT_AUTHORITY` |
| P04-H24 | Candidate passes representation validation but loses one interpretation-critical source/scope/state dimension | reject; syntactic success cannot override semantic failure |

## Invariant oracle

For every accepted candidate:

`accepted(candidate) => exact_identity && exact_authority && scope_preserved && semantic_state_preserved && negative_semantics_preserved && no_retired_runtime_fallback`

For every candidate requiring a carrier-class substitution:

`accepted(candidate) => semantic_parity_proved`

There is no inverse implication from artifact presence, parser success, provenance reachability or historical family membership to admission.
