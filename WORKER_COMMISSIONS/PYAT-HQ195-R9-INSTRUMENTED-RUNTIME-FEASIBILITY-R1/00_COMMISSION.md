# PYAT HQ195 — R9 minimally instrumented runtime feasibility — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / SOURCE-FREE RUNTIME FEASIBILITY IMPLEMENTER — SPACE BUNNY**

Branch:
`agent/rabochii-pyat-hq195-r9-instrumented-runtime-feasibility-r1`

Implementation base:
`9dd3cac1fea3620f2ab7769cf4b90ab111f0ae01`

Checkout mode:
`SPARSE_REQUIRED`

Dedicated worktree root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/`

Sparse materialization manifest:
- `/WORKER_COMMISSIONS/PYAT-HQ195-R9-INSTRUMENTED-RUNTIME-FEASIBILITY-R1/`
- `/WORKER_RETURNS/PYAT-HQ195-R9-INSTRUMENTED-RUNTIME-FEASIBILITY-R1/`
- `/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/R9-INSTRUMENTED-RUNTIME-FEASIBILITY-R1/`
- `/rawlsing_next/`

Historical R9 evidence is read by exact Git object; do not materialize historical return estates.

The exact commissioned startup SHA is supplied by HQ after this commission commit.

## Mission

Determine whether a **minimal, source-free, non-semantic runtime instrumentation change** can make the literal O1-C07 path-open/read account observable and enforceable without privileged tracing.

This is feasibility/proving work, not production adoption.

Do not access real survey sources.

## Mandatory sparse startup

Use canonical clone:
`/Users/matthewsmith/Desktop/Rawlsing`

Do not clone.

Fetch origin, verify the exact remote branch/startup SHA, read this commission from the exact object, then use:

`bash /Users/matthewsmith/Desktop/Rawlsing/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/runtime/prepare_sparse_worktree.sh ...`

with exactly the manifest above.

Do not silently convert to a full checkout. If full-tree materialization becomes genuinely necessary, stop and return:
`CHECKOUT_MODE_INSUFFICIENT__HQ_RECOMMISSION_REQUIRED`.

## Governing technical facts

Accepted HQ192 result:
`81a006638b8a21a19150fa35c9caba544d272550`

It established:
- Python interception cannot see compiled pyreadstat internal opens;
- unprivileged DYLD interposition failed on this host;
- privileged tracing is outside authority;
- header-prefix and Python-level operations are observable;
- literal internal path-open account remains unsatisfied.

Do not repeat the same failed DYLD experiments except as a control where necessary.

## Feasibility routes to inspect

Prefer minimal and explicit changes.

Investigate, in order:

1. **pyreadstat / bundled ReadStat source instrumentation**
   - determine where file opens/reads occur;
   - determine whether a local source build can add exact counters/guards around those operations;
   - no semantic decoding changes;
   - no global install.

2. **link/build-time wrapper or callback**
   - if ReadStat/pyreadstat exposes a lawful file or I/O callback surface, test it;
   - do not assume one exists.

3. **application-owned access broker**
   - determine whether the reader can consume an already-open descriptor, buffer, file-like object, or brokered path such that the application can govern the access before compiled code;
   - if not, state that clearly.

A disposable source package/build may be downloaded or built only inside lane-owned temporary/tooling space. Prefer the already installed package/source metadata first. Do not modify global Python or system libraries.

## Required proof if instrumentation is feasible

Using synthetic SAV/DTA carriers only:

- instrument actual compiled-reader path opens at the owner where they occur;
- observe counts with explicit measurement basis;
- impose a maximum and refuse the excess operation before it occurs;
- distinguish open count, reader invocation, decoder invocation and byte count;
- show ordinary synthetic decode results remain equivalent to the uninstrumented runtime at the declared test grain;
- exercise metadata, normal decode and `read_file_in_chunks`/batch path where feasible.

Do not claim survey-semantic equivalence from tiny synthetic fixtures. State the exact requalification burden.

## Requalification analysis

If a modified pyreadstat/ReadStat binary is required, specify:
- exact binary/source difference;
- whether the R7 runtime identity changes;
- which R7/C3/C4C3 courts must rerun;
- whether previous source-free 55/55 qualification can be reused or must be repeated;
- what new reviewer acceptance is required before any live use.

Do not mutate the accepted R7 environment in place. Build a disposable candidate environment.

## Write terrain

Only:
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/R9-INSTRUMENTED-RUNTIME-FEASIBILITY-R1/**`
- `WORKER_RETURNS/PYAT-HQ195-R9-INSTRUMENTED-RUNTIME-FEASIBILITY-R1/**`

No `rawlsing_next/**` edits; it is materialized read-only for analysis/tests.

## Required return

- `00_RETURN.md`
- `01_IO_OWNER_SOURCE_MAP.json`
- `02_MINIMUM_INSTRUMENTATION_DESIGN.json`
- `03_SYNTHETIC_PROOF.json`
- `04_ENFORCEMENT_NEGATIVE_CASES.json`
- `05_OUTPUT_EQUIVALENCE_AT_TEST_GRAIN.json`
- `06_R7_REQUALIFICATION_BURDEN.json`
- `07_LIMITATIONS.json`
- `08_FINAL_DISPOSITION.json`

Allowed dispositions:
- `INSTRUMENTED_RUNTIME_FEASIBLE__R7_REQUALIFICATION_REQUIRED`
- `INSTRUMENTED_RUNTIME_FEASIBLE__SEMANTIC_EQUIVALENCE_NOT_YET_PROVED`
- `CURRENT_RUNTIME_CANNOT_SATISFY_LITERAL_O1_C07_WITHOUT_PRIVILEGE_OR_ARCHITECTURE_CHANGE`
- `R9_RUNTIME_FEASIBILITY_BLOCKED`
- `CHECKOUT_MODE_INSUFFICIENT__HQ_RECOMMISSION_REQUIRED`

## Return law

Commit, push, re-fetch, verify remote == local.
Artifacts bind substantive result SHA; pushed tip reported separately.

Terminal:
`HQ195_R9_RUNTIME_FEASIBILITY_RETURNED__HQ_REVIEW_REQUIRED`

## Holds

Zero real-source operations, locator discovery, warrant issuance, live C4, production mutation, C7 or actor/person work.
