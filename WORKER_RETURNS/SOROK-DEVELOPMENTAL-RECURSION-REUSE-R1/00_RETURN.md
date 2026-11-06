# SOROK developmental recursion — Phase A selected reuse

**Base:** `33c40a315d3c231cb2021bd8e60f3261547efa62`
**Branch:** `agent/sorok-recursion-reuse-20261106-r1`
**Mode:** sourcefree historical software recovery and ABI trace; one bounded synthetic P2 first-reader smoke; no model call or respondent read.

## Verdict

**`S39_S47_EXACT_SOURCE_AND_FIRST_READER_ABI_DEMONSTRATED__ORIGINAL_V3_EXACT_BYTES_HOLD__NO_ADAPTER__NO_NATIVE_OR_PRODUCTION_GRANT`**

The selected S39–S47 functions are present at exact source commits and exact file hashes. The current `P2ProductFanin` imports the exact `S47Session` inheritance chain and exposes the first-reader path. The original V3 archive is **not** available: the declared staging root/zip is absent, the only observed archive container hash differs from the expected hash, and the local V3 compatibility tree does not match the exact historical source identities. Original V3 is therefore **HOLD**, not claimed as reused. No adapter was emitted.

## Architecture source

Exact Git blob read:

```text
fbfc529230d8b3c13f824cfac31741a5dfaa57e5:
SOROK_PRODUCT_CONTROL_ROOM/USER_DIRECTED_ARCHITECTURE/20261026_USER_SETTLED_BATCH_RECURSION_IMPRESSION_MEMORY_R1.md
blob_sha1 1a888b6a0eaa3d74e0a8afed715b4cd20785a5b2
sha256  38876f6e73ac150754d642b6741fb0be71be255563b352fca32b40f00e5e7859
```

The settled boundary remains: prospective 3–5 events → sequential Rawlsing connected impression/outcome/time computation → retrospective memory/meaning in the first half of the next LLM call. The source explicitly marks implementation as unverified; this return does not turn that architecture into a native or scientific claim.

## Source retrieval

Checked through shared Git objects before proposing any missing code:

```text
fbfc... architecture commit             commit
515b... S50 recovery commit              commit
12433... W1-C source findings            commit (fetched)
e66d... RCF-A 40-function ledger         commit (fetched)
S39/S40/S41/S42/S43/S44/S45/S46/S47 source commits  commit
```

The exact original V3 archive remains unavailable:

```text
expected staging zip: /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip
zip present:          false
staging root:         /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging
staging root present: false
expected container:   953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
observed container:   3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289
```

The only local V3 source is `/Users/matthewsmith/Desktop/Rawlsing/v3`, a compatibility fallback, not the exact archive. W1-C and RCF-A confirm the historical application path and exact member identities, but not current source bytes.

## Original V3 selected functions — HOLD

| ID | Exact symbol | Expected source SHA-256 | Local status |
|---|---|---|---|
| M01 | `BackboneState` | `19e968d4…ada2` | local `6f629f55…4480`; mismatch |
| M01 | `hash_jsonable` / `YearRecord` | `4bbd7518…5cfc2` | file absent |
| M07 | `Registers` | `19e968d4…ada2` | state file mismatch |
| M21 | `run_pressure_flow_cycle` | `6da4effd…1d3d` | `v3/psyche/flow.py` absent |
| M25 | `run_one_year` | `da3147c3…2acb` | local `47c97bfa…5235d`; mismatch |
| M25 | `step_one_year` | `da3147c3…2acb` | same mismatch |
| M25 | `run_n_years` | `5a737c17…d95a` | exact file, but yearly/state dependency mismatch |
| M25 | 19-step order | `90496a2c…ffc` | local `ee7290a8…6770`; mismatch |
| M26 | `DerivedIndices` / `compute_all_derived` | `e479fc3e…1360` | exact file, but state dependency mismatch |
| M29 | `build_render_packet` | `f024debf…cf` | local `9b1a38c1…6a08`; mismatch |
| M29 | `render_year` | `f2f18c1d…653d` | local `c9f4472e…695`; mismatch |
| M30 | `build_persona_sheet` | `4a000953…a00e` | local `b90fe456…c74a`; mismatch |
| M30 | `backbone_state_from_identity` | `cb29c959…3bdda` | local `ead76d12…4f67a`; mismatch |

ABI facts recorded in `01_SELECTED_REUSE_LEDGER.json`:

- `run_one_year(state, derived, v3config, step_order) -> None`: mutates the passed `BackboneState` through the 19-step annual order.
- `step_one_year(state, v3config, step_order, derived) -> DerivedIndices`: returns derived state after a step.
- `run_n_years(state, n, v3config_path=None, step_order_path=None, collect_json_per_year=False) -> tuple[BackboneState, list[str] | None]`: lifespan runner over repeated annual steps.
- `run_pressure_flow_cycle(...) -> dict`: writes pressure-flow history/memory/grooves; exact `flow.py` is absent.
- `build_render_packet(...) -> dict`: read-only packet builder; `render_year(..., render_packet=None, llm_callback=None) -> None`: render-only path.
- `build_persona_sheet(...) -> dict`: historical V2 presentation compiler, not the current actor-safe M6 contract.
- `backbone_state_from_identity(...) -> BackboneState`: initializes persistent state; scalar psychological priors are not authorized.

No original V3 function was executed on the compatibility tree and no adapter was emitted. Exact-file `run_n_years` and `DerivedIndices` are not promoted: their `state.py`/`yearly_step.py` dependency closure is not exact and no current first reader exists.

## S39–S47 selected functions — exact ABI and reuse

All selected source rows match the P2 product source manifest exactly (24 entries; commit/path/blob/SHA-256 checked):

| Group | Source commit | Representative symbols | Current consumer |
|---|---|---|---|
| S39 | `e41513fa…7d90` | `S39GeneratedSession.start/read_generation`; `GeneratedProducer.generate`; `perform_attempt` | `S47Session` inheritance; diagnostic/action API |
| S40 | `79b0357c…4a23` | `S40GeneratedSession.start/read_s40` | `S47Session` inheritance; speech surface |
| S41 | `c72a10d2…b784` | `continue_event`; `read_event` | `S47Session` inheritance; ordered history |
| S42 | `765a441f…a83f` | `admit_event`; `read_event` | `P2Continuation.admit/read_later_event` |
| S43 | `3edd631f…1e54` | `admit_event`; `read_s43_event` | `P2Continuation`; language history |
| S44 | `923278fb…4611` | `start`; `read_root` | `S47Session` inheritance; root material |
| S45 | `f26a138e…04bf` | `say`; `do_help`; `attend`; `read_encounters` | `S45Projection` / `P2ProductFanin` |
| S46 | `f0ef39b9…434e` | `produce_interval`; `read_interval_states`; `current_interval_state`; revoke/restore | `p2_explicit_interval_flow` / P2 |
| S47 | `765a441f…a83f` | `read_c9_conditioning`; `c9_interval_source` | `P2Continuation`; C9/readset |

The `S47Session` MRO is exact and contains, in order:

```text
S47Session, S46Session, S45Session, S44Session, S43Session,
S42Session, S41Session, S40GeneratedSession, S39GeneratedSession, ...
```

`P2ProductFanin` imports successfully from the accepted P2 owner and exposes `start`, `open`, `admit_later_event`, `read_later_event`, `public_opportunity`, `do_help`, `say`, `attend`, `status`, and `current_interval_state`. A bounded P2 first-reader smoke was started against a synthetic local state root, verified `ok=true` with one root event and zero encounters, then closed and removed. It called no model and read no respondent data. Existing accepted P2 execution evidence remains prior owner evidence, not a new native claim here.

## C9, interval and access interface

- `S46Session.produce_interval(domain)` writes the interval state/material/world record.
- `S46Session.current_interval_state(scope_id=None)` reads the current interval.
- `S47Session.read_c9_conditioning(event_ref=None)` reads source/readset/currentness/eligibility and never mutates.
- `S47Session.c9_interval_source()` returns the current interval source.
- `P2Continuation.admit_later_event(...)` / `read_later_event(event_ref)` are the accepted same-root later-event boundary.
- `apply_explicit_interval(state, interval_input, *, base_root=None)` is the accepted interval input path; it does not auto-execute `DO_HELP`.
- `S50Session.materialize_legacy_projection` / `read_projection` / `actual_root_missing` is exact code in Git but has no current P2 consumer and depends on the absent historical archive/root state; HOLD.

## Adapter decision

**No adapter emitted.** The selected S39–S47 APIs are already in one exact inheritance chain consumed by the accepted P2 owner; adding an adapter would duplicate or obscure the existing contract. The original V3 APIs are not exact enough to adapt, and no missing function is guessed.

## Tests and import probe

Build script: `build_reuse_ledger.py`
Focused tests: **8 passed** in 0.06s.

The import probe loads the exact S47 chain and P2 owner without a session; a separate bounded smoke then started and verified one synthetic P2 root. Together they confirm:

- S39–S47 selected source files exact;
- S47 MRO contains the full chain;
- P2 owner import OK;
- V3 compatibility imports load the state/yearly/render/persona modules but `v3.psyche.flow` and `v3.core.year_record` are absent;
- no model call, respondent read, native claim or production write.

## Engineering / science / authority

- **Engineering:** `SCOPED_ACCEPT_FOR_S39_S47_ABI_REUSE__HOLD_ORIGINAL_V3_EXACT`
- **Science:** `HOLD_ABSENT_ORIGINAL_EXECUTION_GRANT`; no CAN/ADP law or native propagation was selected.
- **Authority:** `HOLD_PRODUCTION_AND_ISSUANCE_NOT_GRANTED`; no protected/native/human receiving crossed.

No engine, scheduler, psychological rule, production edit, merge, CI, source issuance, frozen output or native/human validation was created. The lead owns disposition from the exact pins and commands.
