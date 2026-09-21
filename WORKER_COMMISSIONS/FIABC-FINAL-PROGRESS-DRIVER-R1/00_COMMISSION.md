# FIABC FINAL DRIVER PROGRESS + SIX-CELL CLEANUP — R1

**AGENT TYPE: BROWSER / GITHUB ONLY**

**Recommended intelligence: GPT-5.6 Sol Medium or High**

Repository: `maidiu/rawlsing`

Exact base: `445c2fd534db61de0d0d348a6d77a11faa419cc3`

Branch: `agent/rabochii-premain-fiabc-final-progress-driver-r1`

Return: `WORKER_RETURNS/FIABC-FINAL-PROGRESS-DRIVER-R1/`

## Hard law

Do not use the user's Mac/local runtime.
Do not open LiTS/WVS survey bytes.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not alter candidate meanings, telemetry semantics, oracle law, Lock1/Lock2, or workload semantics.

## Mission A — manifest-derived progress

The real Terminal court must report progress itself. Codex/UI elapsed time is not evidentiary.

Add deterministic progress reporting to `rawlsing_next/ee_p2x_darwin_court_driver.py`, derived from the loaded current execution manifest — never hardcoded counts.

Report both:
1. human-readable progress to stderr; and
2. structured JSONL progress suitable for later UI/log parsing.

Progress events should include, as applicable:
- overall governed position `#/total`;
- executable-stage `#/total`;
- cell `#/6`;
- source/candidate name;
- stage ID and stage `#/17`;
- stage disposition;
- START / PASS / SKIP / PRESERVE / BLOCKED / CANDIDATE_LOCAL_FAILURE;
- next stage;
- stage elapsed monotonic wall;
- current resource snapshot when available;
- final cell/court completion status.

Current manifest facts must be derived dynamically. At the sealed base the manifest has six cells × 17 stage slots plus S17; current entry begins at LiTS/A S01. Do not bake 102, 89, 6, or 17 into execution logic.

Progress emission is C4 court administration and must not redefine evidentiary candidate metrics.

## Mission B — stale six-cell plumbing

Audit and repair stale historical assumptions in the live driver/backend path.

Confirmed defect:
`rawlsing_next/ee_p2x_darwin_stage_backend.py::_cell()` currently constructs a sequence list containing:
`LITS_I/A, LITS_I/B, LITS_I/C, WVS7/A, WVS7/B`
and omits `WVS7/C`.

That helper is used by failure receipt serialization, so a lawful WVS7/C failure can hit stale five-cell indexing instead of producing the intended governed failure receipt.

Repair it so all six current cells are handled from current manifest law, ideally without duplicating a hardcoded cell list.

Search for and eliminate other live five-cell / historical WVS-C assumptions that conflict with the current six-cell execution manifest. Historical evidence files themselves remain immutable history.

## File ownership

Primary ownership:
- `rawlsing_next/ee_p2x_darwin_court_driver.py`
- driver-focused tests
- narrowly scoped backend change only for stale cell-order/failure serialization if unavoidable

Do not modify telemetry semantics/completeness law owned by Workers A/B.

## Progress UX target

A real run should visibly resemble:

```
FIABC P2 [001/...] CELL 1/6 LiTS-I/A
STAGE S01 [2/17] CANDIDATE_PREPARATION_BUILD START
...
STAGE S01 [2/17] PASS elapsed_stage=... next=S02_C11_REACHABILITY
```

For governed skips/preserved stages, print the disposition rather than pretending work executed.

At cell terminal, print a compact cell-complete line. At court terminal, print exact terminal plus ledger identity.

Structured progress must be write-once/append-only or otherwise deterministic under resume. Resume must not falsify stage counts or re-label already terminal stages as newly executed.

## Tests

Source-independent tests must prove:
- counts/ordinals derive from arbitrary manifest shapes;
- six-cell current manifest yields correct ordering;
- resume starts reporting from the correct next stage while retaining total context;
- skip/preserve/executable stages are distinguished;
- WVS7/C failure receipt path works and no five-cell index remains;
- progress does not mutate ledger/candidate semantic state;
- final S17 progress/terminal is emitted;
- stdout machine result remains parseable if human progress is sent to stderr.

No real measured court.

## Return

Return changed files, exact progress event schema/examples, stale-assumption audit, tests, and statement that no candidate execution or measured P2X occurred.
