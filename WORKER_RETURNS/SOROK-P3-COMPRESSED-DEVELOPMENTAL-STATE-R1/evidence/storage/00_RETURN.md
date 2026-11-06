# P3 normalized psychological-state sidecar — storage return

Status: **MECHANICAL STORAGE IMPLEMENTED / AUTHOR-ONLY TEST PASS**. This is not independent acceptance, not the HQ-owned P2 wrapper, not integrated P3 product acceptance, and not native science. The original bounded task is complete at the storage scope.

## Scope and files

Owned files only:

- `p3/state_store.py` — `PsycheStore` implementation.
- `tests/test_state_store.py` — 42 mechanical tests.
- `evidence/storage/` — this return, schema, measurements, test logs and hash manifest.

No `__init__.py`, `p3_owner.py`, `compression.py`, P2/#704 code, contracts, accepted code, sourcepack, PROGRAMMA or protected file was changed. `p3` remains a namespace package for HQ ownership.

## Exact API

```text
PsycheStore(path, *, binding, registry_hash, source_hash)

head() -> {"hash": str, "count": int}
query(*, project, counterpart, as_of) -> list[record]
get_operation(operation_id) -> operation | None
pending() -> list[operation]
reserve(operation_id, *, proposal_hash, expected, plan_hash,
        base_before, psyche_before, plan) -> operation
save_world(operation_id, base_result) -> operation
commit_effects(operation_id, *, records, response, event_binding) -> receipt
finish(operation_id, result) -> operation
verify() -> True
stats() -> counters
close()
```

`binding` is exactly `{root, actor, branch}` with nonempty strings. Reopening requires identical binding, schema, registry hash and source hash. `expected` and `base_before` are exact `StateIdentity` documents `{root, actor, branch, clock, state_hash}`. `psyche_before` is `head()` or its `hash`; the store persists the canonical head document. `reserve` is stale-head checked and binds the complete immutable request. `commit_effects` returns the effects receipt; the other mutating methods return the durable operation document.

## Declared document shapes

This contract left some nested shapes implicit. The exact accepted forms are:

### Plan

```json
{
  "root": "...", "actor": "...", "branch": "...",
  "source_hash": "...",
  "authority": "TEST_ONLY",
  "grade": "TEST_ONLY_...",
  "permitted_rules": [
    {"rule_id": "...", "rule_version": "...", "rule_hash": "..."}
  ]
}
```

- Identity may instead be under `identity: {root, actor, branch}`.
- Source may instead be under `source: {hash: ...}` or `source_binding`.
- Authority/grade may instead be under `provenance`.
- `authority` must start with `TEST_ONLY`; `grade` must start with `TEST_ONLY`. Production/native flags are denied.
- Every permitted-rule descriptor is exact; duplicate descriptors are refused.
- `plan_hash` is an opaque nonempty caller identifier, immutable-bound with the full canonical plan. It is not silently recomputed by the store; replay compares both fields exactly.
- Rule-specific evaluation is not performed here. Records must use a descriptor present in the stored plan.

### Record

Exactly these required fields:

```text
root, actor, branch, project, counterpart, record_id, kind, payload,
rule_id, rule_version, rule_hash, registry_hash, source_hash,
effective_from, causal_parents, grade
```

Optional: `operation` (only `CREATE`) and `hash`. Any other field is refused.

- `kind` is `MEDIATOR`, `TENSION` or `PRACTICE`; `V3MS_MEDIATOR`/`V3MS_TENSION`/`V3MS_PRACTICE` are accepted input aliases and normalized to the canonical names.
- `project`/`counterpart` may be a string or null.
- `effective_from` must equal the actual event binding clock.
- `causal_parents` is a list of nonempty refs; when nonempty it must contain the actual admitted event hash.
- `grade` must equal the plan grade.
- `hash` is `digest(record excluding hash)`. A supplied wrong hash is refused; a missing hash is computed.
- Every record is appended immutably. No update/lifecycle API exists.

### Event binding and base result

`event_binding` requires `{root, actor, branch, event_id, event_hash, clock}`; owner identity may be nested under `owner`/`identity`. It is checked against the stored `base_result`.

`base_result` accepts the actual P2 `RealizedEvent.document()` shape, including `before`/`after`, `objective.event.e1_event_id`, `objective.event.e1_event_hash`, and `receipt_ref` `P2_EVENT:<hash>`. For mechanical tests, top-level `event_id`/`event_hash`/`clock`/identity are also accepted. The stored base result is immutable; `before` must equal the reserved `base_before` when present.

### Result

`finish` accepts the serialized #704 `RealizedEvent` document with exactly:

```text
operation_id, proposal_hash, before, after, status, objective,
accessible, consequences, readset, receipt_ref
```

The operation ID, proposal hash and before identity must match the reserved operation. Status must be a core #704 status. If the result carries an explicit effects-receipt hash under `consequences`, it must match the durable receipt.

## Recoverable phases and CAS

```text
reserve        -> PREPARED
save_world     -> WORLD_COMMITTED
commit_effects -> PSYCH_COMMITTED
finish         -> COMPLETE
```

- Every write uses SQLite `BEGIN IMMEDIATE` with `synchronous=FULL`.
- `reserve` checks the current record head before insert; exact repeated requests return the same row, changed requests refuse.
- `commit_effects` requires `WORLD_COMMITTED`, rechecks the exact stored plan, event binding and base result, and compares the current head to the reserved `psyche_before`. A concurrent winner makes the loser fail `STALE_PSYCHE_HEAD`.
- All records are validated before any insert. One bad target rolls back the entire target set, the head update and the phase transition.
- Exact phase replay returns the durable receipt/operation; changed input refuses.
- `pending()` includes `PREPARED`, `WORLD_COMMITTED` and `PSYCH_COMMITTED`, excluding `COMPLETE`; the HQ owner is responsible for blocking unrelated work.
- A cross-database crash protocol is retained in the contract for HQ. This store durably exposes the phases and never pretends that SQLite across two databases is one atomic transaction.

## Head, chain and schema

The initial head is:

```text
digest({schema, root, actor, branch, registry_hash, source_hash})
```

Each inserted record updates:

```text
head = digest({previous: head, record_id, record_hash})
```

`head()` reads one meta row and, when records exist, one last-record pointer row: constant reads, no history replay. `query()` uses the `(root, actor, branch, project, counterpart, effective_from, seq)` index and reads only matching rows. `verify()` is the explicit full scan; normal reads do not call it.

Schema: see `SCHEMA.sql`. Three normalized tables (`p3_meta`, `p3_records`, `p3_operations`), two targeted indexes, immutable record rows, per-record content hashes and chain columns, and durable operation payload hashes. There is no whole-checkpoint rewrite.

## Tests and results

```text
python3 -m py_compile p3/state_store.py tests/test_state_store.py
python3 -m pytest -q tests/test_state_store.py
42 passed in 0.50s
```

Coverage includes real SQLite transactions, cold reopening, wrong binding/registry/source/schema, stale heads, all phase transitions, idempotent replay at every phase, one-bad-target atomic rollback, contradictory records and CAS, record/version/rule/time/parent/grade/hash refusals, production denial, targeted query isolation, O(1) head reads, record/operation tamper detection and measured storage growth. No P2 simulation or model call is used.

## Storage measurements

From `STORAGE_MEASUREMENTS.json` (TEST_ONLY, one record per operation, WAL checkpointed; not a timing guarantee):

| records | record rows | op rows | DB bytes | bytes/record | head reads | targeted rows | targeted row reads | full verify reads |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 49,152 | - | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 53,248 | 53,248.0 | 2 | 1 | 1 | 3 |
| 5 | 5 | 5 | 90,112 | 18,022.4 | 2 | 1 | 1 | 11 |
| 10 | 10 | 10 | 126,976 | 12,697.6 | 2 | 2 | 2 | 21 |
| 25 | 25 | 25 | 241,664 | 9,666.56 | 2 | 5 | 5 | 51 |
| 50 | 50 | 50 | 425,984 | 8,519.68 | 2 | 9 | 9 | 101 |
| 100 | 100 | 100 | 835,584 | 8,355.84 | 2 | 17 | 17 | 201 |

These counts include durable operation/base/result/receipt payloads; a sparse 3–5-event batch is the intended economy. `full verify` reads records plus operations; targeted `query` reads only matched records and remains `full_scans=0`.

## Known limitations / declared gaps

- No P2 wrapper, P2 database transaction, event admission, rule evaluator, projection or integrated P3 vertical slice is in this file.
- Cross-database atomicity remains the HQ owner's recoverable protocol. This store is the sidecar phase/custody surface.
- `plan_hash` is opaque and exact-bound, not recomputed; the full canonical plan is also stored.
- `base_result` extraction supports the actual P2 objective-event shape and declared top-level fallback; HQ must pass the actual P2 result.
- Query is exact project/counterpart scope and effective-from; no lifecycle updates, automatic activation, scalar winner or memory claim.
- No native/scientific/production/human claim. All records require explicit TEST_ONLY provenance.
- No timing promise is made from the measurements.

## Custody

- Startup: `7db475fb29c0977d2c368dc2f83b5471f0a59460`.
- Protected start: `c852d7516e23fcb6cf2215e9be7c5fa268503516`.
- Branch: `agent/sorok-p3-normalized-store-20261106-r1`.
- Code commit: `5dac5447b14a607f450fae3d84a9ecb782a2de19`.
- Model/runtime: OpenCode, `opencode-go/deepseek-v4.1-flash#max`; quota **UNKNOWN**, not observed.
- This author pass is not independent acceptance. HQ owns the P2 wrapper, rule semantics, integrated tests, interpretation and full P3 receiving.
