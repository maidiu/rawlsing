# Real Git and sourcefree receipts

## 1. Worktree and cut

```text
Host: oldMac.lan
OS: macOS 13.7.8 (Darwin 22.6.0 x86_64)
Python: 3.11.3
Git: 2.39.1
Worktree: /private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/oneo-r1
HEAD: c061dc018e8a52a8a75ae7c82156100e04506418
STARTUP_SHA: cee8a09b33ccfb08e5db7e0bc3be45fda8938766
STARTUP_ANCESTOR: yes (git merge-base --is-ancestor exit 0)
WRITE_SCOPE: WORKER_RETURNS/SOROK_PROGRAMMA_ORIGINAL_NEO_V3_ACTUAL_ENGINEERING_ESTATE_R1/**
```

The branch contains the sealed commission head above the startup. The startup
scope files `00_PROGRAMMA_SOROK.md`, `01_LIVING_REFERENCE...` and
`00A_NONNEGOTIABLE...` were read from the startup object; worktree source files
were read at the current branch head.

## 2. Commands actually run

```sh
git rev-parse HEAD
git merge-base --is-ancestor cee8a09b33ccfb08e5db7e0bc3be45fda8938766 HEAD
git status --short
git show <ref>:<exact source path>
git rev-parse <ref>:<exact source path>
git ls-tree -r --name-only <ref>
python3  # AST-only parse of every selected source file
python3  # zip member vs extracted byte comparison
python3 -m json.tool <output>.json
git diff --check
```

No historical source was imported into this branch. No sourcefree script from a
historical return was executed.

## 3. Original V3 source verification

```text
External extracted source:
/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging/v3

Python modules:                         114
Functions:                              579
Classes:                                43
Parser errors:                          0
```

Archive comparison:

```text
Archive: /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip
Archive SHA-256: 3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289
v3/*.py archive members: 114
Byte-identical extracted members: 114/114
```

The archive container does **not** equal the earlier expected ruling hash
`953c9149...`; this is a container identity mismatch. The member bytes are
present, checked, and reported; that does not retroactively establish the
missing container identity.

## 4. Selected source parse counts

```text
Registry source files:                  192
Original V3 package modules:            114
Original V3 package functions:          579
Original V3 package classes:            43
Current PREMAIN selected modules:        32
Historical selected modules:             29
JS/spec records:                         8
Graph nodes / edges:                    37 / 35
```

Every selected Python file parsed as AST with zero parser errors. This is a
static read, not an import or execution.

## 5. JSON and graph validation

```sh
python3 -m json.tool 01_HISTORICAL_AND_CURRENT_V3_NEO_SOROK_SOURCE_PREIMAGE_AND_FUNCTION_REGISTRY.json
python3 -m json.tool 02_ACTUAL_PRODUCER_TO_FIRST_CONSUMER_AND_NEEDED_FUNCTION_GRAPH.json
python3 -m json.tool 04_FULL_C12_A5_BACKWARD_MISSING_FUNCTION_PARALLEL_FLIGHTS.json
python3 -m json.tool 05_TYPED_SOURCE_GRADED_PROGRAMMA_INGEST_PATCH.json
```

All four exit 0. The graph has 37 nodes and 35 typed edges. The original V3
registry contains exact source-object identity for each file, and the graph
references exact symbols/line ranges where the source is Python.

## 6. Source-free tests and execution

`NOT_RUN` in this flight:

- No external V3 test suite was executed. The archive is not owned by this
  flight and no per-run execution permission was supplied.
- No `server/generation/simulation.py`, FastAPI app, database, chat turn, model
  API, provider call or HTTP endpoint was started.
- No BP2/BP2P4J/R31J/R31E/JOIN sourcefree tests were executed. Their historical
  author/reviewer results are cited only as evidence at their exact cuts.
- No C9/C12 SQL, key, anchor or database was executed.
- No Pyat world/source/N11/N12/C11 work or raw survey execution was attempted.
- No human A5, actor model, production integration or PREMAIN/O-LIVE R2 change
  occurred.

This is why the engineering verdict is **static source/consumer
reconciliation**, not executable acceptance. The return does not claim
`ALL_CODE_VERIFIED` or a passed S2 test suite.

## 7. Non-disturbance check

The return was authored only in its own worktree and directory. O-LIVE R2's
branch/worktree/terminal was not inspected, edited, reset, rebased, merged,
cherry-picked, or interrupted. The user's statement that R2 is running was
treated as authoritative; no process was probed or killed.
