# PYAT HQ192 — R9 OS accounting interposition and higher-layer completion — R1

Repository: `maidiu/rawlsing`

Role: **RABOCHII / SOURCE-FREE LOW-LEVEL ACCOUNTING IMPLEMENTER — SPACE BUNNY**

Branch:
`agent/rabochii-pyat-hq192-r9-os-accounting-interposition-r1`

Exact implementation base:
`491dac21b9f833c57bcb2ddb39f442c3dba0017c`

The exact commissioned startup SHA is supplied by HQ after this commit is published.

Return directory:
`WORKER_RETURNS/PYAT-HQ192-R9-OS-ACCOUNTING-INTERPOSITION-R1/`

## Mission

Attempt to close the remaining literal O1-C07 accounting gap without weakening or relabeling it.

Governing partial court:
`agent/rabochii-pyat-hq191-r9-budget-enforcement-court-r1 @ 1067828d75f3eab483e9b2a95e4b3ef703661118`

R9 remains open because Python-level instrumentation cannot observe compiled-reader OS opens and because selected/header/byte operations belong at other layers.

## Startup

Fetch origin; verify exact remote startup SHA; isolated clean worktree; no blind pull; stop on mismatch.

## Hard rule

No sudo.
No kernel/system tracing changes.
No raw-source access.
Synthetic carriers only.
No production mutation.

## Part A — OS-level open/read observability

Test whether a **process-local, user-space interposition mechanism** can observe and enforce the compiled reader's file operations without elevated privilege.

Preferred options, in order of least invasive:
1. process-local `DYLD_INSERT_LIBRARIES` interposer against a local non-protected Python interpreter;
2. another reversible per-process libc interposition mechanism;
3. read-only tracing available to the user without privilege.

A local interposer may be compiled with system `clang` into a disposable lane-owned directory.

At minimum attempt to intercept relevant functions such as:
- `open`, `openat`, `fopen`/variants;
- `read`/`pread` if needed for byte accounting;
- `close` for lifecycle correlation.

Do not install globally.

Demonstrate with synthetic SAV/DTA carriers:
- reader succeeds;
- actual path-level opens are observed at the lower layer;
- a declared maximum can stop an excess attempt **before** the excess open;
- measurement basis is explicit and reproducible.

If SIP/hardened-runtime/library behavior prevents lawful interposition, record that as evidence and do not fake a count.

## Part B — selected-column layer

Trace the exact higher layer that consumes the physical incidence and enforces selected-variable/ordinal exactness for SRC02/SRC06/SRC14.

Determine whether O1-C07's selected-read account can be satisfied there with:
- explicit selected variable set;
- count/budget;
- pre-operation enforcement;
- no source access.

Do not create a decoder-layer selected-read count for an operation it never performs.

## Part C — SRC26 header-prefix layer

Locate the exact source-free code/contract that would perform or govern the 176-byte header-prefix operation.

If an executable source-free layer exists:
- instrument it on a synthetic carrier;
- bind operation count and byte maximum separately;
- prove pre-operation ceiling enforcement.

If no executable layer currently exists, state the exact missing owner/consumer and preserve the blocker.

## Part D — byte accounting

Where the low-level interposer can observe read/pread byte counts, determine whether a safe byte ceiling can be expressed and enforced as policy.

Do not claim that synthetic byte totals predict real-source byte totals. A policy maximum must be justified as an authorization ceiling or remain unset.

## Candidate law

Preserve C1/C2/C3 separation:
- C1 historical expected counts;
- C2 synthetic observations;
- C3 policy hard maxima.

Do not relabel.

If a full set becomes governable, produce a **non-authorizing** successor candidate under:
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/R9-OS-ACCOUNTING-INTERPOSITION-R1/**`

It remains unsigned, unissued, authorizes_access=false, execution_authorized=false, locators unfilled.

## Required packet

At minimum:
- `00_RETURN.md`
- `01_INTERPOSITION_METHOD_AND_HOST_LIMITS.json`
- `02_OS_OPEN_OBSERVATIONS.json`
- `03_OS_OPEN_ENFORCEMENT_NEGATIVE_CASES.json`
- `04_SELECTED_LAYER_BINDING.json`
- `05_SRC26_HEADER_LAYER_BINDING.json`
- `06_BYTE_ACCOUNTING.json`
- `07_SUCCESSOR_CANDIDATE_OR_BLOCKER.json`
- `08_LIMITATIONS.json`
- `09_FINAL_DISPOSITION.json`

## Allowed dispositions

Exactly one:
- `R9_COMPLETE_CANDIDATE_READY_FOR_HOSTILE_REVIEW`
- `R9_PARTIAL__LOWER_LAYER_STILL_UNGOVERNABLE`
- `R9_PARTIAL__HIGHER_LAYER_OWNER_MISSING`
- `R9_POLICY_AUTHORITY_REQUIRED`
- `R9_MATERIAL_CONTRADICTION_FOUND`

A complete-candidate claim requires independent hostile review before HQ removes R9.

## Return law

Commit, push, re-fetch, verify remote == local.
Artifacts bind substantive SHA; report pushed tip separately.

Terminal:
`HQ192_R9_OS_ACCOUNTING_RETURNED__HQ_REVIEW_REQUIRED`

## Holds

Zero real-source operations, locator discovery, warrant issuance, live C4, production mutation, C7 or actor work.
