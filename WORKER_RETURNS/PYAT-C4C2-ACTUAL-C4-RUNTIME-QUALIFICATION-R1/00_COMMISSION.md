# LAUNCH IN: Codex — Sol High
# ROLE: PYAT C4C2 — ACTUAL-C4-PATH NON-MAC RUNTIME QUALIFICATION — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/codex-pyat-hq172-c4c2-linux-runtime-qualification-r1`

Exact base:
`30686b185d4ceb2c94f61815ef70d8c8e76255d6`

Governing inputs:

- Omega-1 decision:
  `01762d7379be4e423dad3e21bcdcee47c536902d`
- C4C blocker return:
  `5efcae137cdcab2fbb0be0cbc54c0d83da799480`
- accepted C1-03 branch/tip:
  `integration/pyat-hq168-c1-03-successor-join-accepted-r1 @ 149c3d2636160d8de9b5a8be0c8b87195158077d`
- accepted C3 integration:
  `integration/pyat-hq130-c3-source-free-accepted-r1 @ 30686b185d4ceb2c94f61815ef70d8c8e76255d6`

This is a blocker-resolution lane for Omega-1 O1-C05.

Do not access raw survey data.
Do not run measured P2X.
Do not run Candidate A/B/C.
Do not mutate accepted semantic owners.
Do not use the user's Mac.

## Mission

Qualify one exact non-Mac execution environment for the **actual planned C4 Route-B/decoder/facade path**, not for the historical EE-P2X Darwin court unless exact static call-graph evidence proves that C4 must traverse that court.

The prior C4C return established that its local OpenCode surface had no non-Mac runtime and that historical EE-P2X modules hard-gate Darwin/x86_64. HQ static inspection additionally observed:

- `ee_p2x_darwin_court_driver.py` self-identifies as the resumed EE-P2X court;
- C4 explicitly forbids measured P2X;
- accepted C4 public APIs are the current decoder + source-backed C11 facade + analytical/provider/consumer path;
- `pre553_source_backed_c11_facade.py` imports `pre553_physical_decoder` and `pre553_r5_codec`, not the EE-P2X Darwin court driver.

Your first obligation is therefore to adjudicate runtime-path applicability before proposing any gate change.

## PHASE 0 — exact provenance and environment

Verify:

- branch base exactly `30686b185...`;
- accepted C3 blobs exactly:
  - G01 authority `31a9afd7d91ed4cb2fb1c1aab3ef86a5fdda1f85`
  - physical decoder `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf`
  - R5 codec `6000a1704d713f65e07610d81e9b3fd8bdd515ca`;
- source-backed facade blob at this tree is `8a761119e4a8d68eb291fc4edfadb52e027f8284`;
- no raw source access occurs.

Record exact Codex environment:
- OS/version;
- architecture;
- Python implementation/version;
- libc/runtime where relevant;
- package-manager state.

If the execution surface is not non-Mac, stop:
`C4C2_NON_MAC_SURFACE_UNAVAILABLE__HQ_ADJUDICATION_REQUIRED`.

## PHASE 1 — actual C4 call-path adjudication

Construct a static import/call-path trace beginning from the accepted C4 interfaces:

- `decode_sav`
- `decode_dta`
- `build_source_backed_c11_repository`
- `execute_source_backed_empirical_query`
- `compose_positioned_subject_possibility`
- `provide_empirical_possibility_slice`
- named positioned-subject consumer

Determine whether either of these historical gates is actually on the planned C4 path:

- `ee_p2x_darwin_court_driver.EXPECTED_RUNTIME`
- `ee_p2x_darwin_stage_backend.FROZEN_PYREADSTAT_VERSION`

Approval path A:
`P2X_DARWIN_GATES_NOT_ON_C4_PATH`

requires exact static evidence that planned C4 does not import/call the EE-P2X measured court.

If the planned C4 path really does require those modules, do not waive or patch them. Return:
`C4C2_RUNTIME_OWNER_CONTRACT_CONFLICT__HQ_ADJUDICATION_REQUIRED`
with the exact path.

No measured P2X execution is permitted.

## PHASE 2 — exact non-Mac dependency qualification

On the non-Mac execution surface, create an isolated environment for source-free qualification.

Required fixed anchors where relied upon:
- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1

Do not silently substitute versions. If exact CPython 3.11.3 is unavailable, either provision it reproducibly or return an exact blocker.

Resolve current accepted dependency evidence for:
- pandas;
- numpy;
- pytest;
- duckdb only if the **actual C4 call path** requires it.

Do not assume historical banked builders are current C4 dependencies merely because they exist in the repository.

Where accepted materials conflict on pandas/numpy versions:
1. identify exact competing accepted artifacts and chronology;
2. determine which version is actually required by current accepted C3/C4 code, if any;
3. if both are compatible and neither is semantically authoritative, run differential source-free probes and freeze one exact version with explicit rationale;
4. if HQ semantic/authority adjudication is required, return that exact residual instead of guessing.

Produce a reproducible dependency-lock candidate including distribution versions and artifact/wheel hashes where available.

Installation in the ephemeral qualification environment is allowed.
Do not install-on-import or mutate accepted production code.

## PHASE 3 — freeze exact reader options

For pyreadstat 1.3.6, explicitly bind every C4-relevant reader option, including at minimum:

- `metadataonly`
- `apply_value_formats`
- `user_missing`
- `encoding`
- `formats_as_category`
- `dates_as_pandas_datetime`
- `disable_datetime_conversion`
- `row_limit`
- `row_offset`
- `output_format`
- extra date/datetime/time formats
- ordered-category behavior

Distinguish:
- explicit repository arguments;
- exact frozen defaults inherited from pyreadstat 1.3.6.

No C4 behavior may remain dependent on an unidentified library default.

## PHASE 4 — source-free synthetic reader probes

Using only synthetic files created in the qualification environment, exercise the actual accepted C3 decoder/codec path.

Required probes:

### SAV / D01
- source-declared exact-SHA encoding admission behavior;
- `encoding=None` behavior;
- explicit BIG5 and WINDOWS-1252 paths;
- metadata-only behavior;
- required reader-option effects;
- no automatic guess/fallback widening.

### SAV / G01
- native integer storage arriving through pyreadstat/pandas;
- exact Python/scalar boxing at the decoder boundary;
- native-int -> float64 representation witness behavior;
- user-missing vs observed-storage distinction;
- exact big-endian R5 float bit tokens.

### D02
- actual arrival type for naive date/datetime/time values from the synthetic reader;
- accepted opaque carrier normalization;
- timezone-aware hostile rejection;
- `.item()` wrapped hostile behavior.

### DTA / LiTS physical layer
- synthetic DTA read path through `decode_dta(..., encoding="latin1")` where applicable;
- extended/user-missing carrier shape needed by current accepted LiTS physical bridge;
- exact reader-option effects.

No raw respondent source may be used.

## PHASE 5 — physical identity stability

Verify on the chosen environment:

- `reader_version` enters physical-metadata identity exactly as current code specifies;
- exact version 1.3.6 is frozen;
- synthetic fixture replay is byte/identity stable across repeat runs;
- no retained physical identity is falsely claimed to transfer across a different reader version;
- host endianness does not alter explicit R5 float token law.

For resource accounting, freeze the chosen surface's native `ru_maxrss` unit and define a surface-specific future C4 measurement law. Do not reuse Darwin byte semantics on Linux.

## PHASE 6 — transfer condition to A's final combined tree

C4A is running independently and will produce the authoritative combined C1+C3 tree.

This lane may qualify runtime behavior against the exact accepted C3 runtime-sensitive blobs and unchanged facade now.

Return a **transfer predicate**:

qualification transfers to C4A/fan-in only if its exact final tree contains:
- the same accepted C3 G01/decoder/codec blobs;
- the same source-backed facade blob;
- no new import/call edge from the planned C4 path into an unqualified runtime owner.

Do not claim A's unknown future SHA is already qualified.

## Return

Write only:

`WORKER_RETURNS/PYAT-C4C2-ACTUAL-C4-RUNTIME-QUALIFICATION-R1/**`

Required:
- `00_RETURN.md`
- `01_ENVIRONMENT_AND_DEPENDENCY_LOCK.json`
- `02_ACTUAL_C4_CALL_PATH.json`
- `03_READER_OPTION_FREEZE.json`
- `04_SYNTHETIC_READER_PROBES.json`
- `05_PHYSICAL_IDENTITY_AND_RESOURCE_LAW.json`
- `06_TRANSFER_PREDICATE_TO_COMBINED_TREE.json`
- `07_EXECUTION_RECEIPT.json`
- `08_FINAL_DISPOSITION.json`

Allowed dispositions:

- `PASS_C4C2_NON_MAC_ACTUAL_PATH_RUNTIME_QUALIFIED__FANIN_READY`
- `C4C2_NON_MAC_SURFACE_UNAVAILABLE__HQ_ADJUDICATION_REQUIRED`
- `C4C2_RUNTIME_OWNER_CONTRACT_CONFLICT__HQ_ADJUDICATION_REQUIRED`
- `C4C2_DEPENDENCY_VERSION_AUTHORITY_REQUIRED__HQ_ADJUDICATION_REQUIRED`
- `C4C2_SOURCE_FREE_READER_BEHAVIOR_BLOCKER__HQ_ADJUDICATION_REQUIRED`

No raw source access.
No self-adoption.
No C4 live execution.

Terminal:
`C4C2_ACTUAL_C4_RUNTIME_QUALIFICATION_RETURNED__HQ_FANIN_REQUIRED`
