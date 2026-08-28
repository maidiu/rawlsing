# LMQ-006 DISPOSITION — CURRENT MACHINE D05 R1

## Inherited item

`LMQ-006` — `Future semantic-authority production/maintenance lifecycle successor`

Historical Long Memory status at `669062e6c319f31214f403939dded91300639bde`:

`NOT_PROVED`

Inherited requirement:

`candidate/evidence/adjudication/collision/split/exclusion/revision/seal/promotion/release/current-selection/rollback/replay/invalidation`

Reason inherited as critical: frozen semantic-authority tables preserve today's decisions but do not preserve the machine's ability to admit or correct future semantic terrain.

## Current disposition

`CURRENTLY_OPEN_FUNCTIONAL_GAP`

The current machine has **not** proved an equal-or-stronger successor for the complete LMQ-006 function.

This is not a claim that current authority handling is weak. The current line materially improves several subfunctions:

- `AuthoritySnapshot@1.0.0` gives exact immutable authority identity with version and content hash;
- `AuthorityRegistry` rejects conflicting id/version hashes and resolves exact tuples only;
- latest/default/fuzzy/nearest selection is prohibited;
- the replay inspectorate pins historical authorities and prevents supersession from rewriting history;
- C11 source releases can be package-atomically ingested and replay sealed.

But the current implementation surfaces are intentionally consumption/validation/replay oriented:

- `pre553_empirical_authority.py` states that it validates immutable authority and does not select latest/default authority;
- `pre553_replay_audit.py` states that it is non-semantic and never supplies missing authority or changes runtime semantics;
- `pre553_c11_ingest.py` accepts `authority_snapshots` as candidate inputs and blocks when exact required authority is missing. It therefore proves new-source intake under existing authority, not production of new semantic authority.

No selected current production owner was located for evidence-backed candidate generation, manual/adjudicated correction, semantic collision resolution, split/exclusion revision, governed revision mint/signature, semantic authority promotion/current-selection, rollback execution, or dependency invalidation/recompilation after an authority change.

## Why partial fragments do not close LMQ-006

Authority 39 requires a positive successor claim to carry current authority + current implementation + current test/receipt and to prove same-or-stronger behavior. The current schema and tests prove exact immutable representation and fail-closed consumption. They do not provide the missing producer/adjudicator lifecycle.

Binding distinctions therefore remain:

`FROZEN_AUTHORITY_EXPORTS != MAINTENANCE_CAPABILITY`

`CAN_READ_CURRENT_AUTHORITY != CAN_CORRECT_OR_EXTEND_AUTHORITY`

`SCHEMA_CAN_HOLD_IT != FUNCTION_EXISTS`

`SOURCE_RELEASE_INGEST != SEMANTIC_AUTHORITY_PRODUCTION`

`SUPERSESSION_REPLAY_PROTECTION != ROLLBACK_EXECUTION`

## Historical mechanism disposition

The old P2→P3/P3A/P3C physical machinery is **not** reinstated and is not declared binding implementation. Its valuable lifecycle function remains binding until an equal-or-stronger selected successor is proved.

The C5R2 maintenance prototype remains nonauthoritative and cannot close LMQ-006 by existence alone.

## HQ consequence

Carry LMQ-006 forward as a current functional gap. Future closure should be one bounded maintenance court that proves, end to end, a new/corrected semantic authority can be proposed from evidence, adjudicated, versioned, collision/split/exclusion corrected, atomically promoted as current, rolled back/superseded without rewriting history, and deterministically invalidate/recompile exactly affected dependents while leaving unaffected dependents stable.
