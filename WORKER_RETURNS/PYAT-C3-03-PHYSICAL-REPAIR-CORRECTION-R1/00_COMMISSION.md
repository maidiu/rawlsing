# PYAT C3-03 — BOUNDED PHYSICAL REPAIR CORRECTION + HERMETIC SOURCE-FREE QUALIFICATION — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Browser GPT-5.6 Sol High physical-path repair worker

Branch:
`agent/rabochii-pyat-hq126-c3-03-physical-repair-correction-r1`

Exact base / independent C3-02 review head:
`c874a134077e6eb416b584157d0209eabdd0d723`

Reviewed C3-02 worker return:
`d3204dc2a74e4628ac34e09e196e60b06ae8e135`

Prior semantic candidate:
`31fd2f4b7c7c2cdf72bed295b7cb5ca94528349f`

Independent review disposition:
`CHANGES_REQUIRED`

Implementation baseline ancestry:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

Current orchestration/review law may be read by exact external ref:
`d9d042bfe5d15fefcd278f387bd7a0a991e3f86d:PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/07_C3_EXECUTION_SPEC.md`
`d9d042bfe5d15fefcd278f387bd7a0a991e3f86d:PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/08_REVIEW_AND_INTEGRATION.md`

## Mission

Repair exactly the two bounded defects found by independent C3-02 review:

1. remove execution-environment mutation from the D02 semantic test and qualify in an execution layer that provisions the dependency before pytest;
2. close the D02 item()-unwrapped timezone-aware fail-open hole.

Do not change G01 or D01 semantics.
Do not edit the source-backed C11 facade.
Do not replace the decoder wholesale.
Do not resurrect historical CLOSED35 census infrastructure.
Do not access raw survey sources.
Do not widen physical, text-semantic, source-semantic, structural or comparability authority.

## Accepted material to preserve

Independent review already accepts:
- G01 at exact nine-surface grain;
- D01 at exact three SHA->encoding physical-only grain;
- D02 existing direct naive opaque cases;
- direct timezone-aware rejection;
- D01+D02 shared-decoder composition;
- unchanged C11 facade blob `8a761119e4a8d68eb291fc4edfadb52e027f8284`;
- prior candidate->execution separation.

Do not disturb these except where the exact D02 repair necessarily touches the shared decoder/test.

## Semantic repair allowlist

### MODIFY
`rawlsing_next/pre553_physical_decoder.py`

In `_physical_value`:
- catch failure of `value.item()` extraction only;
- if item extraction succeeds and the exact unwrapped type is built-in `datetime`, `date`, or `time`, call `normalize_decoder_physical_value(item)` **outside** the extraction exception handler;
- allow `R5CodecError` for timezone-aware datetime/time to propagate fail-closed;
- preserve all other existing behavior.

Do not broaden accepted date/time types or convert timezone-aware values to strings.

### MODIFY
`rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py`

- remove `importlib.util`, `subprocess`, `sys` and the import-time conditional `pip install pandas` bootstrap;
- add hostile coverage for an item-wrapper whose `.item()` returns a timezone-aware `datetime`;
- add hostile coverage for an item-wrapper whose `.item()` returns a timezone-aware `time`;
- both must raise the same explicit carrier-authority rejection as the direct path;
- retain all previously accepted D02 cases and unchanged-facade compatibility.

No other production/test source file may change.

## Semantic candidate law

First commit the complete semantic/test repair.

Freeze that commit as the **new semantic candidate SHA**.

At semantic candidate:
- only the two semantic repair allowlist files above may differ from the reviewed C3-02 tree, aside from inherited documentary review files;
- no workflow/court provisioning change may be mixed into this semantic candidate.

## Execution-only qualification commit

After freezing the semantic candidate, create one execution-only commit whose delta from the semantic candidate is exactly:

1. `.rabochii/court_spec.json`
2. `.github/workflows/pyat-c3-03-physical-repair-source-free.yml`

No other file may change in that execution-only commit.

Update `.rabochii/court_spec.json` only to point `semantic_candidate_sha` to the new semantic candidate. Keep the exact existing six-test list and deterministic environment fields.

### Dedicated workflow contract

The dedicated workflow must trigger on push to exactly:

`agent/rabochii-pyat-hq126-c3-03-physical-repair-correction-r1`

Use:
- Ubuntu GitHub runner;
- CPython 3.11;
- pinned direct dependencies:
  - `pytest==9.1.1`
  - `pandas==2.3.3`

Dependency provisioning occurs **before any pytest collection**.

The workflow must:
1. checkout the exact pushed execution commit;
2. set up Python 3.11;
3. install the two pinned direct dependencies above;
4. record exact Python, pytest and pandas versions;
5. record a sorted full `pip freeze --all` snapshot and its SHA-256;
6. run the existing Rabochii protocol self-test;
7. validate the existing bounded court spec;
8. execute `rawlsing_next.rabochii_bounded_court` against that spec;
9. upload both the governed court receipt and the environment identity/freeze evidence.

Do not install dependencies from inside any test module.

The six-file court remains exactly:
- `rawlsing_next/tests/test_closed35_g01_sav_numeric_representation_authority.py`
- `rawlsing_next/tests/test_closed35_d01_declared_encoding_admission.py`
- `rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py`
- `rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py`
- `rawlsing_next/tests/test_r35_i01_physical_metadata.py`
- `rawlsing_next/tests/test_pre553_source_backed_c11_facade.py`

Preserve the prior failed worker run and both prior 53-pass runs as historical evidence. Do not rewrite them as accepted qualification.

## Required qualification

A successful return must report:
- new semantic candidate SHA;
- exact semantic candidate changed blobs;
- execution-only SHA;
- exact semantic-candidate->execution diff proving only the two allowed execution files changed;
- workflow run/job/attempt;
- protocol counts;
- exact six-file court pass/fail/error/skip counts;
- receipt artifact identity/digest;
- environment evidence artifact identity/digest;
- Python/pytest/pandas versions;
- pip-freeze SHA-256;
- raw-source access declaration = 0;
- unchanged facade blob identity.

A green worker run is not self-approval; fresh independent review remains required.

## Return terrain

May add:
`WORKER_RETURNS/PYAT-C3-03-PHYSICAL-REPAIR-CORRECTION-R1/**`

Return:
- `00_RETURN.md`
- `01_REPAIR_DIFF.json`
- `02_EXECUTION_ENVIRONMENT.json`
- `03_QUALIFICATION_RECEIPT.json`
- `04_HOSTILE_CASES.json`
- `05_REMAINING_OBLIGATIONS.md`

Do not modify prior C3 worker/reviewer return directories.

Terminal target:
`C3_03_BOUNDED_REPAIR_AND_HERMETIC_SOURCE_FREE_QUALIFICATION_COMPLETE__READY_FOR_INDEPENDENT_REVIEW`
