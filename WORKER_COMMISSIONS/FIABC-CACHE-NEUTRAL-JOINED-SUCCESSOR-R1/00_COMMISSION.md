# FIABC CACHE-NEUTRAL JOINED SUCCESSOR — R1

You are **FIABC CACHE-NEUTRAL JOINED SUCCESSOR — R1**.

Repository:

`maidiu/rawlsing`

Branch:

`agent/rabochii-fiabc-cache-neutral-joined-successor-r1`

Exact branch base / already-qualified T5 failure-semantics implementation:

`41eea54d7610a47f1adc342c6caacaf11324a40c`

Historical protected execution head:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

This branch is the candidate protected successor. Do NOT mutate the historical protected branch itself.

## AUTHORITATIVE INPUT RETURNS

### T5 joined failure-semantics repair — GREEN

Branch:

`agent/rabochii-fiabc-t5-joined-failure-semantics-repair-r1`

Return tip:

`0a0e1e9c19a36bc67c17114e75e4760e3e31b672`

Exact qualified implementation head:

`41eea54d7610a47f1adc342c6caacaf11324a40c`

Terminal:

`PASS__FIABC_T5_JOINED_FAILURE_SEMANTICS_SOURCE_FREE_QUALIFIED__HQ_PROMOTION_REQUIRED`

Read its entire return packet.

The exact repaired blobs at the implementation head include:

- `rawlsing_next/fiabc_live_terminal_control.py` — `e67f0c18bc52f81f2e0924799aa54745a53306a9`
- `rawlsing_next/ee_p2x_darwin_court_driver.py` — `70bf233492b543d3d728cedfdda36218504ef3d4`
- `rawlsing_next/ee_p2x_candidate_process_envelope.py` — `09330e344045e2007104501a4776d72a12db7df7`
- `rawlsing_next/ee_p2x_process_isolated_backend.py` — `6afd66d1234dd59c6eee97c9538b78bee9fcfd28`

Preserve those semantics.

### Worker E cache-neutral successor law — REQUIRED

Branch:

`agent/rabochii-fiabc-split-r2-e-wvs-bytecode-prestate-closure-r1`

Return tip:

`9e062d672677e0e1d0a142909a20c2c55efa219d`

Exact Worker-E implementation head:

`3b3529133da5e92bba41b357464b501af9580675`

Read:

- `WORKER_RETURNS/FIABC-SPLIT-R2-E-WVS-BYTECODE-PRESTATE-CLOSURE-R1/00_RETURN.md`
- `01_EXACT_IMPORT_CACHE_INVENTORY.json`
- `02_PYC_EQUIVALENCE_ANALYSIS.json`
- `03_WVS_ENTRY_PRESTATE_CONTRACT.json`
- `04_CHOSEN_CLOSURE_STRATEGY.json`
- `05_SUCCESSOR_REQUIRED_PATCH.md`
- `06_SOURCE_FREE_HOSTILE_TESTS.json`

Worker E correctly returned BLOCKED for the old physical epoch. Its chosen successor law is authoritative for this court.

## SOURCE / EXECUTION LAW

SOURCE-FREE / CANDIDATE-FREE ONLY.

Do not open, hash, decode, inspect, or infer from raw LiTS/WVS survey files.

Do not launch Candidate A/B/C.

Do not run measured P2X.

Do not touch prior RUN4/RUN5 evidence roots.

Do not modify frozen candidate-owner semantics.

Do not weaken T2/T3/T4/T5 truth or accounting law.

## MISSION

Create and source-free qualify the **new joined protected successor physical-measurement epoch** which combines:

1. the qualified T5 joined failure-semantics repair already present at branch base;
2. Python bytecode-cache NONPARTICIPATION for all measured candidate execution;
3. explicit process-envelope/S15 cache-neutral attestations;
4. a lawful successor to the historical driver binding;
5. a newly qualified canonical joined launcher.

This successor is a prerequisite for later Split R2 fan-in.

---

# J1 — CACHE-NEUTRAL MEASURED ENVIRONMENT

Adopt exactly the Worker-E shared successor law:

Before the measured driver interpreter starts:

```sh
CACHE_PREFIX="$WORK_ROOT/court/_python_cache_neutral_prefix"

test -d "$CACHE_PREFIX" || mkdir -p "$CACHE_PREFIX"
test -z "$(find "$CACHE_PREFIX" -mindepth 1 -print -quit)" || exit 1

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$CACHE_PREFIX"
export RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR=1
```

The cache-neutral variables MUST be set before the measured Python interpreter is created.

Do not claim setting Python globals after startup is equivalent.

The canonical joined successor launcher is:

`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

Modify it only as required to adopt/bind this successor law.

The preflight phase may remain outside cache-neutral measurement if and only if:
- candidate processes cannot start;
- no candidate physical metric is accumulated;
- the cache-neutral measured interpreter begins with a fresh empty redirected prefix;
- any preflight-created ordinary pycs are invisible to measured import because `sys.pycache_prefix` redirects lookup.

Prove this.

# J2 — PREFIX EMPTINESS / NONPARTICIPATION

Require redirected cache prefix:

- zero descendants before measured entry;
- zero descendants at every candidate-cell start;
- zero descendants after every candidate-cell stop;
- zero descendants after S15 replay;
- zero descendants at final measured exit.

A nonempty prefix at any governed check blocks.

Existing source-tree/work-root/repo/site-package `__pycache__` entries must not participate in candidate import lookup under the successor.

Do not delete historical/source-tree caches merely to pass. The law is nonparticipation, not cleanup.

# J3 — PROCESS ENVELOPE ATTESTATION

Extend the already-repaired protected process-envelope law minimally.

Before backend import in every main candidate child, receipt-bind:

- `sys.dont_write_bytecode is True`;
- exact resolved `sys.pycache_prefix == CACHE_PREFIX`;
- `RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR == "1"`;
- redirected cache prefix has zero descendants.

Reject the cell before backend import on mismatch.

This attestation must be part of the candidate process handshake/envelope and included in evidence identity.

Preserve:
- fresh process per source×candidate cell;
- no cross-cell warm state;
- same-cell lifecycle token law;
- outer-nonpass graceful stop law from T5 repair.

# J4 — S15 FRESH REPLAY ATTESTATION

The S15 fresh replay child must independently receipt-bind the same cache-neutral facts.

Do not rely solely on "Popen inherits env" as an unstated assumption.

Qualification must prove:
- inherited env values;
- child `sys.dont_write_bytecode`;
- child `sys.pycache_prefix`;
- empty prefix;
- no pyc creation.

# J5 — GOVERNED RUNTIME

Exact target runtime:

- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- pandas 2.3.1
- numpy 2.3.2
- Darwin x86_64

Run the cache-hostility fixture on exact CPython 3.11.3, not only a later Python.

Required hostile cases:

- valid ordinary timestamp pyc under normal import is consumed;
- same source under cache-neutral successor ignores that pyc;
- normal package import;
- `spec_from_file_location` import;
- work-root immutable module cache;
- exact-owner module cache;
- protected repo module cache;
- controlled writable stand-in for site/stdlib cache where needed;
- no redirected-prefix descendants.

# J6 — NEW PHYSICAL EPOCH

Bank an explicit physical-measurement epoch identity.

It must state:

- old physical metrics from pre-cache-neutral epoch are not successor measurements;
- semantic candidate identities are not changed by cache neutrality;
- candidate code/owners remain unchanged;
- startup/build-open CPU/wall/RSS may differ because warm-pyc compile elision is removed;
- both future joined and split courts must use this exact epoch;
- absolute cross-source physical metric comparison remains forbidden.

Give this successor epoch a deterministic receipt identity that later split control can bind.

# J7 — HISTORICAL 10B IMMUTABILITY / SUCCESSOR BINDING

DO NOT rewrite:

`WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json`

It is historical evidence and remains pinned to the old driver blob.

Create a lawful successor binding, suggested:

`WORKER_RETURNS/EE-P2X/10C_DARWIN_DRIVER_SUCCESSOR_BINDING.json`

or another clearly successor-named immutable artifact.

The successor binding must bind at minimum:

- repaired driver blob;
- repaired process envelope blob;
- repaired process-isolated backend blob;
- repaired T5 terminal-control blob;
- cache-neutral joined launcher blob/identity;
- cache-neutral physical epoch identity;
- existing ledger/backend/supervisor schemas where unchanged;
- exact current six-cell manifest identity;
- exact terminal disposition vocabulary including repaired final non-PASS behavior;
- exact current protected successor commit or a non-circular implementation binding scheme.

Update current driver-bound integration tests/verifier law to consume the successor binding while preserving tests that historical 10B remains immutable history.

# J8 — T5 FAILURE REPAIR CONSERVATION

Re-run the complete T5 repair matrix.

The cache-neutral successor must retain:

- no C/S05 missing-observation crash;
- same-source three-way gate law;
- typed outer T4/T5 failure semantics;
- process stop on outer non-PASS;
- success-only S17;
- typed final non-PASS evidence;
- all-six-PASS no semantic drift.

No regression from cache-law changes.

# J9 — FULL DRIVER-BOUND REQUALIFICATION

The prior T5 repair broader run produced 5 failures solely because historical 10B pinned the old driver blob.

This successor must eliminate that promotion debt with a new lawful binding.

Run the full relevant source-free driver-bound suite against the successor.

There must be:
- zero behavioral failures;
- zero driver-binding drift failures against the successor binding.

Historical 10B tests may assert immutability/history but must not falsely require the successor driver to equal the old blob.

# J10 — CANONICAL LAUNCHER QUALIFICATION

Bank an exact successor qualification receipt for:

`HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`

Prove:
- source SHA gates preserved;
- preflight remains candidate-free;
- cache-neutral vars are applied before measured interpreter;
- measured invocation still uses governed driver/backend;
- no PYTHONPATH injection;
- no candidate execution during qualification;
- old source/candidate governance remains intact.

# J11 — SPLIT REUSE CONTRACT

Produce an exact machine-readable reuse contract for later Split R2 fan-in.

It must state:

- exact joined-successor implementation head;
- protected driver/process/T5 blobs;
- physical epoch identity;
- cache-neutral environment contract;
- process/S15 attestation schema;
- exact successor binding identity;
- exact joined launcher identity;
- requirements a split half must satisfy to claim same physical epoch.

Later split fan-in may not guess these identities.

# J12 — ZERO SOURCE / ZERO CANDIDATE QUALIFICATION

All qualification here must remain:

- raw source opens = 0
- raw source SHA passes = 0
- decoder calls = 0
- candidate process launch attempts = 0
- candidate outputs = 0
- measured execution = false

The CPython cache hostility fixture is not a Candidate A/B/C process.

## ALLOWED IMPLEMENTATION SURFACES

Expected modifications may include:

- `HQ_HANDOFF/launchers/RUN_DISPOSITIVE_FIABC_SIX_CELL.sh`
- Worker-E cache-neutral helper port/successor
- `rawlsing_next/ee_p2x_candidate_process_envelope.py`
- `rawlsing_next/ee_p2x_process_isolated_backend.py`
- narrowly necessary driver/T5 surfaces already changed at base
- driver-bound verifier/test current-binding surfaces
- new successor binding/epoch receipts
- source-free tests

Do not modify candidate owner implementations or survey decoders.

## REQUIRED RETURN

Return under:

`WORKER_RETURNS/FIABC-CACHE-NEUTRAL-JOINED-SUCCESSOR-R1/`

Required at minimum:

- `00_RETURN.md`
- `RETURN.json`
- `01_CACHE_NEUTRAL_PHYSICAL_EPOCH.json`
- `02_PROCESS_CACHE_ATTESTATION.json`
- `03_S15_CACHE_ATTESTATION.json`
- `04_DRIVER_SUCCESSOR_BINDING.json`
- `05_JOINED_LAUNCHER_QUALIFICATION.json`
- `06_T5_FAILURE_REPAIR_REGRESSION.json`
- `07_FULL_DRIVER_BOUND_QUALIFICATION.json`
- `08_SPLIT_REUSE_CONTRACT.json`
- `09_SOURCE_FREE_TELEMETRY.json`
- exact test output
- exact implementation hash/blob table

Bank the exact qualified implementation head separately from later evidence/docs-only commits.

Success terminal:

`PASS__FIABC_CACHE_NEUTRAL_JOINED_SUCCESSOR_SOURCE_FREE_QUALIFIED__HQ_PROMOTION_REQUIRED`

If any cache-neutral, T5, driver-binding, or exact-runtime burden remains:

`BLOCKED__FIABC_CACHE_NEUTRAL_JOINED_SUCCESSOR_REMAINS`

No measured execution.
