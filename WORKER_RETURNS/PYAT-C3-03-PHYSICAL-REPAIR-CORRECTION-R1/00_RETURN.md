# PYAT C3-03 — bounded physical repair correction + hermetic source-free qualification — R1

Status:

`BLOCKED_EXECUTION_CAPABILITY__GITHUB_HOSTED_RUNNER_NOT_ASSIGNED`

Repository: `maidiu/rawlsing`

Assigned branch:
`agent/rabochii-pyat-hq126-c3-03-physical-repair-correction-r1`

Commission tip:
`a68fb242e8a000a4b06037118e8eb804ee3365b5`

Exact base / C3-02 independent review head:
`c874a134077e6eb416b584157d0209eabdd0d723`

## Frozen identities

New semantic candidate:

`901e3e77f905847d3ef8d86b458280d8fe422dd0`

Semantic repair blobs:
- `rawlsing_next/pre553_physical_decoder.py`: `d3d828c171ea9fdd0e90563aff6ef705f5aae2cf`
- `rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py`: `3901f10a487856f5f232ae6700fff407ac99725e`

Execution-only qualification commit:

`283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`

Execution-only blobs:
- `.rabochii/court_spec.json`: `f408ae9a113b19f49c6c30d67c3177e3a7f787e4`
- `.github/workflows/pyat-c3-03-physical-repair-source-free.yml`: `322f5699a3ddd4858887986a6c712e3d61c7c710`

## Semantic repair

The semantic candidate changes exactly the two commission-allowlisted files.

1. `_physical_value` now catches only failure of `value.item()` extraction. If extraction succeeds and yields an exact built-in date/datetime/time, `normalize_decoder_physical_value(item)` executes outside that exception handler, so timezone-aware datetime/time `R5CodecError` propagates fail-closed.
2. The D02 test contains no package-manager or import-time dependency installation logic.
3. Hostile tests were added for item-wrapped timezone-aware `datetime` and item-wrapped timezone-aware `time`, both requiring the same explicit carrier-authority rejection as the direct path.

No G01/D01 semantic file changed. The C11 facade remains blob:
`8a761119e4a8d68eb291fc4edfadb52e027f8284`

No historical decoder/census machinery was resurrected.

## Execution-only boundary

The exact semantic-candidate -> execution diff is one commit and exactly two files:
- `.rabochii/court_spec.json`: one semantic-candidate SHA replacement only;
- `.github/workflows/pyat-c3-03-physical-repair-source-free.yml`: dedicated source-free workflow.

The workflow is configured to:
- trigger on push only to the assigned C3-03 branch;
- use Ubuntu + CPython 3.11;
- provision `pytest==9.1.1` and `pandas==2.3.3` before any pytest collection;
- record exact Python/pytest/pandas/pip identity;
- record sorted `pip freeze --all` plus SHA-256;
- execute protocol self-test, court-spec validation and the exact six-file bounded court;
- upload separate court-receipt and environment-evidence artifacts.

No test module installs dependencies.

## Qualification blocker

Dedicated workflow run:
- run: `36627731035`
- execution SHA: `283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`
- event: `push`
- attempt 1 job: `109608913544`
- attempt 2 job: `109609370151`
- conclusion: `failure` on both attempts
- both jobs: `steps=[]`, `runner_id=0`, empty runner name
- pytest collection reached: **no**
- environment-recording step reached: **no**
- artifacts: **none**

The failed job was rerun once without changing the execution commit. Attempt 2 reproduced the same pre-runner failure.

A temporary evidence-only PR (#477) was opened solely to test the repository's already-established `Rabochii Governed Bounded Court` on the same execution SHA. Its run:
- run: `36628050628`
- job: `109609985991`
- conclusion: `failure`
- `steps=[]`, `runner_id=0`, empty runner name

Thus the failure is not evidence against the new workflow body or semantic repair; the existing governed workflow was also unable to obtain a GitHub-hosted runner. PR #477 was closed unmerged.

No source-free test result is called PASS. No environment identity, pip-freeze hash or receipt artifact is invented.

## Source-access declaration

- raw survey files opened: **0**
- raw survey files materialized: **0**
- raw survey files decoded: **0**
- Candidate A/B/C: **not run**
- measured P2X: **not run**
- current real-source execution: **not run**

## Required continuation

Once an authorized GitHub execution route can actually acquire a runner, rerun the existing dedicated run/commit without changing the semantic candidate. A successful qualification must still produce all commission-required environment and receipt identities before C3-03 can claim the requested terminal target.

Current terminal state:

`C3_03_BLOCKED_EXECUTION_CAPABILITY__HQ_ADJUDICATION_REQUIRED`
