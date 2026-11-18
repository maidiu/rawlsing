# ANVIL CUT1 — EXECUTABLE PREPARED-SAVED BATCH CONTRACT

## Status

**`CUT1_IMPLEMENTED_READY_FOR_DISTINCT_NONAUTHOR_REVIEW`**

Baseline evidence below is preserved; the implemented descendant and owner ACK
are recorded in the final section.

- Product baseline: `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`
- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Worktree: `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER`
- This turn: baseline execution and exact cut contract only.
- Production writes/test additions under `rawlsing_next`: **NOT AUTHORIZED YET**
- No protected/source/science/current/actor/issuer grant.
- Original S2-D terminal all-seven proofs are not reopened.

## Baseline evidence

Existing tests were run with the qualified local runtime:

```text
Python 3.11.3
pyarrow 22.0.0
duckdb 1.5.2
pyreadstat 1.3.2
pytest 9.0.2
```

### Focused cut1 suite

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_prepared_saved_i03.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py \
  rawlsing_next/tests/test_pre553_batch_runner.py
```

Actual result: **58 passed, 0 failed, 0 errors, 0 skipped, 17.523 s**.

Per-class node inventory:

| Class | Nodes |
|---|---:|
| `test_pre553_prepared_saved_i03` | 3 |
| `test_pre553_direct_estate_i03` | 7 |
| `test_pyat997_s1e_saved_native_first_consumer` | 24 |
| `test_pyat991_s2d_saved_admission` | 8 |
| `test_pre553_batch_runner` | 16 |

### Existing Batch / five-reader court

```bash
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat991_s2d_five_readers.py \
  rawlsing_next/tests/test_pre553_batch_runner.py
```

Actual result: **23 passed in 6.13 s**.

The five-reader file includes the actual native saved Batch scheduler and
NORMAL/COMPLETED/PARTIAL/ABSENT/fresh-process paths
(`test_saved_batch_actual_native_scheduler`,
`test_saved_normal_matches_legacy_native_and_never_opens_source`,
`test_saved_completed_partial_absent_use_existing_resume`,
`test_saved_normal_and_completed_survive_fresh_process`). Legacy saved Batch
baseline works.

## Prepared path verified before the cut

Existing `test_pre553_prepared_saved_i03.py` passes all 3 nodes:

- prepared session matches baseline and builds **one** `DirectEstateI03Session`
  index across **four** operations;
- all facts/projections equal legacy native facts;
- revocation and wrong-condition refusal;
- prepared I05 exact discovery parity.

This is the direct prepared path that the new Batch cut must preserve.

## Known RED — desired new prepared-Batch surface

The current wrappers reject the prepared subclass by exact type:

- `execute_saved_i03`:
  `SavedC11AdmissionError: exact SavedC11Admission required`
- `BatchExecutionRunner(..., saved_mode=True)`:
  `BatchIntegrityError: repository must be accepted I02 C11Repository or exact SavedC11Admission`

Return-local witness:

- `evidence/test_prepared_abi_witness.py` — **2 passed**, proving the baseline
  rejection.
- `evidence/abi_probe.py` output:
  - admission type `PreparedSavedC11Admission`
  - manifest SHA-256
    `87f5c6c68da3707c4fa565b929c9411ffc6b18f161533788885dd2be943496a9`
  - direct I03 error exact message
  - Batch error exact message
  - disposition `BASELINE_READY_PENDING_CURRENT_OWNER_ACK`

This is a **RED for the desired new prepared-Batch feature**, not a failing
existing-test claim.

## Exact planned production write scope — TWO files only

### 1. `rawlsing_next/pre553_saved_workload_integration.py`

Current blob: `cc8aa32512378261406d765f0b049c748cb3e11f`

Allowed change surface only:

- imports: add
  `from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission`
- `execute_saved_i03` line 42 guard:
  replace exact base-only `type(...) is not SavedC11Admission` with exact
  whitelist:
  `type(admission) not in (SavedC11Admission, PreparedSavedC11Admission)`.
  Error: `exact SavedC11Admission or PreparedSavedC11Admission required`.
  On acceptance, call inherited `admission.execute_i03` unchanged.
- `execute_saved_i05` line 54 guard: same exact whitelist and inherited call.
- `execute_saved_batch` lines 94–139:
  - same exact whitelist at line 94;
  - if exact `PreparedSavedC11Admission`, enter
    `with admission.prepared_i03() as prepared:` **once** around
    `runner.run(...)`;
  - each QUERY unit dispatches to `prepared.execute_i03`;
  - each DISCOVERY unit dispatches to `prepared.execute_i05`;
  - base `SavedC11Admission` executes the existing `admission.execute_i03` /
    `admission.execute_i05` path unchanged;
  - retain `admission.check_current()` before and after each unit and after
    `runner.run`;
  - retain `BatchExecutionRunner` construction exactly, `saved_mode=True`,
    `prior_receipts`, `max_units`, executor bindings, replay ref and
    `ExecutionOutcome` result refs;
  - context closes exactly once on success or exception.

No edit to `execute_saved_normal`, `execute_saved_completed`,
`execute_saved_partial`, `execute_saved_absent`, `resume`, or the prepared
module.

### 2. `rawlsing_next/pre553_batch_runner.py`

Current blob: `49e3974c658d66a270815d9faa3798b40d4488b1`

Allowed change surface only:

- import `PreparedSavedC11Admission` from
  `pre553_prepared_saved_i03` (no cycle: prepared imports only the saved base);
- `BatchExecutionRunner.__init__` lines 398/404–410:
  annotation and exact guard become
  `SavedC11Admission | PreparedSavedC11Admission`;
  `saved_mode is True and type(repository) in (SavedC11Admission, PreparedSavedC11Admission)`.
- error text:
  `repository must be accepted I02 C11Repository or exact SavedC11Admission or exact PreparedSavedC11Admission`
- no other changes. `resolve_release_exact` remains inherited; `run`,
  `record_receipt`, schedule, receipts, states and provenance are untouched.

**No third production file is indispensable.** `PreparedSavedC11Admission`
already provides the exact one-session context; changing it is outside this
cut.

## Exact whitelist / dispatch / lifecycle

### Whitelist

Accept only:

```text
type(admission) is SavedC11Admission
type(admission) is PreparedSavedC11Admission
```

Do not use broad `isinstance`, duck typing, factory monkeypatches, synthetic
`C11Repository`, class-name checks, or arbitrary subclass acceptance.

### Context dispatch

- Direct `execute_saved_i03`/`execute_saved_i05` on prepared admission:
  one inherited operation; no prepared context required.
- `execute_saved_batch` on prepared admission:
  one `prepared_i03()` context for the whole deterministic Batch run.
- Legacy base `SavedC11Admission`:
  existing per-operation dispatch remains byte-for-byte behaviorally unchanged
  and may rebuild its existing per-operation session.
- Full `C11Repository` path:
  completely unchanged.

### Lifecycle

- Prepared Batch owns exactly one `DirectEstateI03Session`.
- `with` exit closes it exactly once.
- `max_units` partial leaves pending units explicit; it does not close or
  recreate an index for the unexecuted remainder.
- A failure inside any unit closes the context and produces the existing
  Batch FAILED/DEFERRED receipt behavior; no positive receipt is fabricated.
- No source factory, no full C11 repository, no second body corpus, no second
  evaluator.

### Per-unit CURRENT

- `PreparedI03Session._require_open` calls `admission.check_current()` before
  each operation.
- `execute_saved_batch` also checks current before and after every unit.
- A revocation during a prepared Batch must refuse before result handoff or
  receipt completion; the existing revocation semantics are not weakened.
- No cached grant, no stale admission, no fallback to `item.record`.

### Receipt preservation

- Same `BatchManifest`, unit order, `max_units` semantics and
  `UnitExecutionReceipt` schema.
- Same `manifest_hash`, `unit_ref`, `attempt_index`, `state`,
  `result_refs`, `provenance_refs`, `executor_ref`, failure codes and
  `record_receipt` acceptance rules.
- Each QUERY outcome uses native fact refs; each DISCOVERY outcome uses native
  receipt refs.
- Replay ref remains `admission.replay_ref`.
- No extra receipt, no fabricated completed state, no changed attempt indexing.

## New focused test — after owner ACK only

New file:

`rawlsing_next/tests/test_anvil_prepared_saved_batch_cut1.py`

Use the existing `test_pre553_prepared_saved_i03._fixture` fixture, no new
source bytes, no hard-coded host paths, no arbitrary factory monkeypatch.

Required positive assertions:

1. `execute_saved_i03(prepared, ...)` accepts exact prepared admission and
   returns the same native fact ref/projection as the existing prepared
   baseline.
2. A four-query `BatchManifest` over the prepared admission executes through
   `execute_saved_batch`, all four units COMPLETED, with
   `DirectEstateI03Session._build` counted exactly **one**.
3. Every prepared Batch fact/ref/projection/replay identity equals the
   pre-existing legacy/prepared baseline.
4. Base `SavedC11Admission` legacy saved Batch remains accepted and green.
5. A prepared context closes on success; closed-session use refuses.

Required refusal/restoration assertions:

- wrong exact release, unknown query/predicate, malformed manifest, and
  arbitrary non-whitelisted admission class refuse before any positive receipt;
- revocation before Batch/inside Batch refuses with zero completed positive
  units and no protected restore/serve;
- baseline facts/replays restore exactly after the refused path;
- no source-factory call, no full C11 repository build, no second corpus or
  index for the prepared Batch context.

No existing test may be deleted, skipped, weakened or rewritten. Existing
legacy Batch and all S2-D tests must remain unchanged.

## Source/corrective preservation check

Current source pins equal `evidence/CUT1_SOURCE_PINS.json`:

| File | Current blob |
|---|---|
| `pre553_saved_workload_integration.py` | `cc8aa325…` |
| `pre553_batch_runner.py` | `49e3974c…` |
| `pre553_prepared_saved_i03.py` | `bcb146ed…` |
| `pre553_saved_c11_admission.py` | `22749add…` |

W05 three production blobs are retained exactly:

| File | Current / W05 blob |
|---|---|
| `pre553_direct_estate_i03.py` | `8825832f8067c7fce7a99a94505743cbb4eada06` |
| `pre553_source_direct_parquet_estate.py` | `e8622ac6bf59c4d1ec052e21410e63aab7dd9aa1` |
| `_pre553_query_eval.py` | `87849f7cc41a2d4647582aba2eae00ab4531b90b` |

These match the W05 `1c37e2d` / composite `357a0fb` source pins. The R03
later-corrective source remains preserved as its independent snapshot; no old
branch was merged and no duplicate implementation was introduced. No source
science/current/issuer rights follow.

## Owner gate

This contract does **not** execute the new feature and does **not** change
product. Required before implementation:

1. Fresh current owner ACK for the two exact production files and the new test.
2. Confirmed current lease/session ownership.
3. Confirmation that the prepared session is the intended reuse surface for
   the Batch feature; if an owner decides otherwise, return exact boundary
   refusal before editing.

Only after that ACK may the same branch implement the two-file change and new
focused test, run the bounded positive/refusal/restoration court, and return a
new exact source cut for receiving.

## Stop

`CUT1_IMPLEMENTED_READY_FOR_DISTINCT_NONAUTHOR_REVIEW` at code/test commit
`a13d69cf5636de5541660cd60115f8b61d66261b`; evidence head
`eb450254bd7d10a884cab3edc16bf06bf8083cba`.

No production code/test edit, no owner poll, no 1/10/100 wide run, no 100k,
no source/original35/current/science/actor/issuer/protected merge.

---

# ACTUAL IMPLEMENTATION EVIDENCE — same cut1 branch

Owner ACK received:
`a744a5a4e4bb31ba9e93a650c7200c064d4d2e11:WORKER_RETURNS/ANVIL_ENGINEERING_CUT1_OWNER_20261117/owner_ack.json`.

## Exact implemented source/test hashes

| Path | Base blob | Implemented blob |
|---|---|---|
| `rawlsing_next/pre553_saved_workload_integration.py` | `cc8aa32512378261406d765f0b049c748cb3e11f` | **`c568836b7ab1ce88224d4bc5c9de6dca8476a5db`** |
| `rawlsing_next/pre553_batch_runner.py` | `49e3974c658d66a270815d9faa3798b40d4488b1` | **`8320f28458fb85aec655d154a2527a161282f56b`** |
| `rawlsing_next/tests/test_anvil_prepared_saved_batch_cut1.py` | new | **`bf00eb591bdee1087e9a10085d808c1ed2aadf88`** |

No third production file was changed. The public function parameter lists remain
unchanged; the `BatchExecutionRunner.__init__` repository annotation remains
the original `C11Repository | SavedC11Admission` (prepared is its exact
subclass), while the runtime exact whitelist adds the prepared class.

## Executed evidence

- Baseline before cut: 58 PASS + 23 PASS; prepared ABI rejection witness
  2 PASS; old RED evidence preserved.
- After cut boundary: **70 passed, 0 failed, 0 errors, 0 skipped, 28.959 s**.
- New focused file: **5 passed, 0 failed, 6.10 s**.
- One prepared Batch context: `_build` count **1** for four distinct operations.
- Four Batch receipts: all `COMPLETED`; four output refs.
- Selected/F2-forward/F4-k>=3/raw full fact/projection/denominator/cell/release
  parity against one-shot baseline.
- Plain `SavedC11Admission` legacy path green.
- Arbitrary class, wrong release, changed manifest binding, revoked CURRENT
  before and mid-Batch refuse; mid-Batch failure closes context; relaxed CURRENT
  restores exact four-operation completion.
- Resource probe: wall `0.1597 s`, parent RSS `104,222,720 B`, estate/root
  `783,936 B`, source reads by new Batch `0`, full C11 builds by new Batch `0`,
  one index build, four outputs. Small TEST_ONLY only.

Evidence: `evidence/after_cut1.txt`, `after_cut1.junit.xml`,
`evidence/new_focused.txt`, `evidence/resource_probe.json`.

This is implementation evidence pending distinct nonauthor review; it is not G5
or protected/source/science/current authorization.
