# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C4C — NON-MAC EXECUTION RUNTIME QUALIFICATION — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq170-c4c-runtime-qualification-r1`

Exact base:
`149c3d2636160d8de9b5a8be0c8b87195158077d`

Governing Omega-1:
`01762d7379be4e423dad3e21bcdcee47c536902d`

This is lane C of three parallel C4-preparation lanes.

Mission: close Omega-1 O1-C05 by qualifying and freezing the intended non-Mac execution environment for the future governed C4 source run.

Do not merge C3 or own the final combined tree.
Do not access raw survey files.
Do not install dependencies at import time.
Do not silently upgrade dependencies.

## Historical anchors

Retained physical reproducibility anchor where applicable:
- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- Darwin/x86_64

Accepted C3 source-free qualification has its own recorded runtime/toolchain; preserve that as a distinct evidence grade.

Do not infer that a different OS/architecture/runtime is equivalent merely because tests import or versions share names.

## Work

1. Record the exact available OpenCode execution environment:
   - OS/kernel
   - architecture
   - Python implementation/version
   - pytest
   - pyreadstat
   - pyarrow
   - pandas and relevant decoder/runtime dependencies
   - full pinned dependency inventory/hash where feasible
2. Determine, from accepted code/contracts and library behavior available without survey data, which future C4 operations are runtime-sensitive:
   - SAV declared-encoding handling;
   - G01 native-int→float64 representation path;
   - D02 built-in naive date/time carrier behavior;
   - DTA/LiTS read path;
   - any Arrow/reader boundary actually relied on.
3. Build source-free compatibility probes/fixtures for those runtime-sensitive operations without using respondent files.
4. If the environment can lawfully qualify, freeze:
   - exact environment identity;
   - exact package versions;
   - exact reader options/configuration;
   - compatibility evidence;
   - any residual platform limitations;
   - execution-surface identifier to be used later in the source warrant.
5. If exact physical reproducibility depends on Darwin/x86_64 behavior that cannot be established on the available non-Mac environment, do not waive it. Return:
   `C4_RUNTIME_EXECUTION_SURFACE_QUALIFICATION_REQUIRED`
   with the smallest exact missing qualification/wake condition.
6. Do not attempt to use the user's Mac as a fallback.

The purpose is not to recreate every historical environment. It is to establish whether one exact non-Mac environment is competent for the future C4 claim, and at what proof grade.

## Return

Write only:
`WORKER_RETURNS/PYAT-C4C-RUNTIME-QUALIFICATION-R1/**`

Required:
- `00_RETURN.md`
- `01_AVAILABLE_ENVIRONMENT.json`
- `02_RUNTIME_SENSITIVITY_MATRIX.json`
- `03_SOURCE_FREE_COMPATIBILITY_PROBES.json`
- `04_QUALIFIED_EXECUTION_ENVIRONMENT.json`
- `05_EXECUTION_RECEIPT.json`
- `06_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C4C_NON_MAC_RUNTIME_QUALIFIED__FANIN_READY`
- `C4_RUNTIME_EXECUTION_SURFACE_QUALIFICATION_REQUIRED`
- `C4C_PROVENANCE_DRIFT__HQ_ADJUDICATION_REQUIRED`

No raw source access. No self-adoption.

Terminal:
`C4C_RUNTIME_QUALIFICATION_RETURNED__HQ_FANIN_REQUIRED`
