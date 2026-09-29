# PYAT C3-02 — independent current-baseline repair integration review — R1

Status: `CHANGES_REQUIRED`

Reviewer branch:
`agent/reviewer-pyat-hq126-c3-02-physical-repair-integration-r1`

Commission tip:
`ba4a371fb77543d570c65cfe6e221260b445459a`

Reviewed worker return:
`d3204dc2a74e4628ac34e09e196e60b06ae8e135`

Frozen semantic candidate:
`31fd2f4b7c7c2cdf72bed295b7cb5ca94528349f`

Worker execution-only commit:
`a26279dfad85ddc2a37f7cb396094da308bc58e4`

## Holding

The G01 and D01 current-baseline ports survive independent static inspection and fresh source-free execution at their declared grains. Most D02 positive/hostile cases also reproduce.

The integration is **not acceptable yet** for two independent reasons:

1. the D02 semantic test performs an import-time, unpinned network mutation of the runtime by invoking `python -m pip install pandas` when pandas is absent; and
2. D02's current `_physical_value` route does not actually reject every item()-unwrapped timezone-aware built-in date/time value. The broad exception handler swallows the carrier rejection and falls through to `_jsonable`, which stringifies the timezone-aware value.

Disposition: `CHANGES_REQUIRED`.

This is not a widening request. Both repairs are bounded to the already-accepted D02 representation grain and the execution environment needed to qualify it.

## Evidence labels

### STATIC_INSPECTION

PASS:
- commission-tip `e1420435591d727f48b7a4d5964709f87fcf5a4f` -> semantic candidate changes exactly the frozen six code/test paths;
- source-backed C11 facade remains blob `8a761119e4a8d68eb291fc4edfadb52e027f8284`;
- no historical CLOSED35 census harness or qualified receipt tree is present in the candidate;
- semantic candidate -> worker execution commit changes only `.rabochii/court_spec.json`;
- G01 remains exact-source/exact-variable/exact-ordinal/exact-int-code finite authority over the nine accepted surfaces;
- D01 contains exactly the three declared SHA->encoding pairs, rejects guessing/fallback/wrong pairs, and returns only physical-decoding authority;
- direct naive built-in date/datetime/time carrier behavior is opaque and field/type sensitive;
- direct timezone-aware datetime/time rejects;
- D01 and D02 compose on the same current decoder;
- the unchanged facade binds the opaque carrier.

FAIL:
- D02 item()-unwrapped timezone-aware values do not fail closed;
- the D02 test mutates its own execution environment during import.

DOCUMENTARY RESIDUAL:
- the review commission names `PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/07_C3_EXECUTION_SPEC.md` and `08_REVIEW_AND_INTEGRATION.md` as must-read files, but those exact paths are absent from the commission-tip tree. The active governed-court workflow, court implementation, execution protocol, commission, worker return and exact diffs were inspected directly instead. This residual is recorded rather than silently reconstructed as if the named files existed.

### SOURCE_FREE_EXECUTED

Independent reviewer evidence run:
- PR: #476, closed unmerged;
- workflow: `Rabochii Governed Bounded Court`;
- run: `36619077886`;
- job: `109579533802`;
- attempt: `1`;
- evidence execution SHA: `ba4a371fb77543d570c65cfe6e221260b445459a`;
- CPython: `3.11.16`;
- protocol self-test: `20 passed`;
- governed six-file court: `53 passed`;
- receipt artifact: `11057736422`;
- artifact digest: `sha256:8ef0d0f821a3946082a07bd0d3060288263cb60b2458ba5d335ef0334838236e`.

The reviewer execution SHA is two documentary-return commits above the worker execution commit. The diff from `a26279d...` to `ba4a...` contains only worker/reviewer return documents; production code, tests and `.rabochii/court_spec.json` are unchanged. Thus the relevant executable tree is identical.

The 53-test PASS is retained as execution evidence, but it is **not** accepted as hermetic qualification because the D02 test can install pandas during collection.

### CURRENT_REAL_SOURCE_EXECUTED

Not authorized; not performed.

## Preserved worker failure evidence

The worker's first six-file court remains material evidence:
- run `36614460693`;
- job `109563805093`;
- execution SHA `9a158eea3ff450292486b2d40ae8f19d21fc9f12`;
- collection error: `ModuleNotFoundError: No module named 'pandas'`;
- artifact `11054548103`, digest `sha256:b4cc555128c59d7456ffbae0fc77ee734f65d8932a4ca3805dacdf548808c9b5`.

That failure correctly demonstrated an execution-capability dependency gap. It must not be rewritten as a semantic repair failure, but neither may a semantic test repair the environment by installing a package at import time.

## Minimal required repair grain

### Environment / qualification
- remove the pandas-install bootstrap from `test_closed35_d02_opaque_datetime_carrier.py`;
- provision pandas before pytest at the execution-environment/court layer;
- preferably pin/capture the pandas version or immutable dependency identity used by the qualifying run;
- rerun the exact six-file source-free court with the test unable to install packages.

### D02 fail-closed path
In `pre553_physical_decoder._physical_value`, catch failures of `value.item()` extraction only. Do **not** catch the `R5CodecError` raised by `normalize_decoder_physical_value(item)` for an exact timezone-aware built-in datetime/time. Add hostile coverage for an item-wrapper returning timezone-aware datetime and time and require the same fail-closed carrier rejection as the direct path.

No G01, D01, facade, source-semantic, question-semantic, structural, comparability or historical infrastructure change is authorized by this review.

## Terminal

`C3_02_INDEPENDENT_INTEGRATION_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
