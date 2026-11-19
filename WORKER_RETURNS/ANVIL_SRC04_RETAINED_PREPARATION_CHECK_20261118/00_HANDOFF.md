# SRC04 R3 retained preparation — recovery decision

## Decision

**IMPOSSIBLE_WITHOUT_RE_DECODE_OR_NEW_AUTHORITY.**

The stopped Wave 1 R3 run left a completed three-family projection spool, but
no authenticated prepared-sections checkpoint, no complete static/replay
sections, no persisted `SourceReleaseManifest`, no expected I02 roots, and no
current/grant/decision binding. Existing aggregate receipts record sizes,
terminal counts and the abort, not a trusted projection identity.

## Retained spool metadata (read-only, no payload read)

Private root:
`/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/evidence/anvil-src04-candidate-31rqm9z_/private-runs-aligned/SRC04_WITNESS_7e8a35957bdb11fd/private`

Spool:
`.s1e-i02-spool-6iefwk6i`

| Family | Bytes |
|---|---:|
| RespondentEvent | 4,441,824,241 |
| EmpiricalCoordinateFact | 63,210,302 |
| WeightMeasureFact | 0 |

Only **3 of 13** required families are present in the spool. The other ten
static/replay families are not in the spool. The empty weight file is
ambiguous between a valid typed absence and an interruption; no checkpoint
records which.

The body journal contains 13 file names but only five are nonempty:

- `AuthoritySnapshot` 13,717
- `QuestionVariableBinding` 357,808
- `RespondentEvent` 5,476,601,716
- `RespondentIdentity` 8,956,035
- `RoutingEligibilityFact` 2,874,659,125

It is incomplete: R3 terminal accounting records `RoutingEligibilityFact`
887,855 of 1,298,649 expected, zero later coordinate lines, and no Parquet or
final verification. It is an interrupted tee stream, not a manifest-bearing
complete section set.

## Missing state

- `private/prepared-sections.checkpoint.json`
- `private/checkpoint.key`
- A trusted checkpoint binding exact source/config/request/grant/decision,
  per-family spool path/size/SHA/count, and expected I02 roots.
- Complete `SourcefreeDirectI02Sections` static/replay families.
- `SourceReleaseManifest` and its semantic projection, declared counts,
  declared universe/authority refs, source snapshot retention ref, and manifest
  digest.
- Replay protocol authority/version/tie-order refs and exact typed absences.
- Exact projection identity, key-witness outcome, universe ref, and current
  acceptance.
- A producer or resume receipt written before the writer; the stopped caller
  writes `producer_receipt.json` only after the construction call returns.

## Exact stopped code

Stopped runner commit: `11626da5c94a699cf3776362ed48863efb616c6e`.
`WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_WITNESS_RUNNER_20261118/witness_caller.py`
lines 184–227 calls `build_source_i02_construction_only(...)` with
`SourceSavedBodySink` and writes `producer_receipt.json` only after the call.
No checkpoint is written in that stopped code.

The current/later `single_pass_handoff.py` does require an HMAC checkpoint plus
exact config, request, grant, decision and spool hashes, but that code is not in
the stopped runner commit and the stopped private root has neither checkpoint
nor key.

## Existing receipts checked

- `SRC04_REAL_CONSTRUCTION_R3_RECEIVING.json`: abort/terminal metadata only.
- `supervisor_receipt.json`: `ABORTED / FREE_FLOOR_BREACH`, resource caps only.
- `SRC04_LIVE_STAGING_FOOTPRINT.json`: sizes, not hashes/counts/acceptance.
- `CHECKPOINT.json`: runner/source scope, not section identity.

## Boundary

No source `.sav` was read, hashed, statted, or decoded. No respondent payload
was read into the model. The interrupted SQLite and its journal were not
opened, parsed, copied, or recovered. No retained artifact was mutated, copied,
or deleted. No original build was started. No product code was changed. No new
authority or certification was derived from leftovers.
