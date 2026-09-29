# PYAT C3-03 — CODEX SOURCE-FREE EXECUTION FALLBACK — R1

Status: ISSUED__USER_MEDIATED_CODEX_LAUNCH_REQUIRED

Role: Minimal deterministic Codex execution fallback

Recommended model:
Codex 5.6. Use 6.0 only if 5.6 exposes a concrete execution/reasoning limitation.

Branch for commission + return only:
`agent/codex-pyat-hq126-c3-03-source-free-execution-r1`

Exact branch base / independent static-review head:
`1b92286cc1f8e40f73b8a3bcf61e11d36aabe2a0`

Exact semantic candidate under test:
`901e3e77f905847d3ef8d86b458280d8fe422dd0`

Exact execution commit under test:
`283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`

Independent C3-03 static review:
`1b92286cc1f8e40f73b8a3bcf61e11d36aabe2a0`

Static disposition already accepted for this fallback's input:
`PASS_AT_DECLARED_GRAIN`

GitHub CI qualification is blocked before runner assignment after four attempts:
run `36627731035`;
latest attempt-4 job `109643559497`;
`runner_id=0`;
`steps=[]`;
no logs/artifacts.

This is the exact verified capability-block case authorized by the Omega routing law for a bounded Codex fallback.

## Mission

Execute the exact C3-03 source-free qualification locally/cloud-side in Codex against the **unchanged exact execution commit**:

`283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`

Do not modify the code, tests, court spec or workflow under test.

Use a detached checkout/worktree or equivalent exact-commit execution directory so the tested tree identity is unambiguous.

The commission/return branch is only for documentary evidence after execution.

## Hard prohibitions

Do not use the user's Mac.

Do not open, materialize, inspect, decode or infer from raw survey files.

Do not run Candidate A/B/C.

Do not run measured P2X.

Do not run current real-source C11 materialization.

Do not edit:
- `rawlsing_next/pre553_physical_decoder.py`
- `rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py`
- `.rabochii/court_spec.json`
- `.github/workflows/pyat-c3-03-physical-repair-source-free.yml`
or any other production/test file.

Do not create new semantic/comparability authority.

## Exact environment

Use:
- CPython 3.11;
- isolated environment if supported;
- direct pinned dependencies:
  - `pytest==9.1.1`
  - `pandas==2.3.3`.

Before any pytest collection:
1. record Python version;
2. record pip version;
3. record pytest version;
4. record pandas version;
5. record sorted `pip freeze --all`;
6. compute SHA-256 of the exact sorted freeze bytes.

If the exact dependency versions cannot be installed, return a typed execution-environment block; do not silently substitute versions.

## Exact identity checks before execution

Verify:
- HEAD / detached tested commit is exactly
  `283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`;
- `.rabochii/court_spec.json` binds
  `semantic_candidate_sha = 901e3e77f905847d3ef8d86b458280d8fe422dd0`;
- the court spec contains exactly the commissioned six test paths;
- source-backed C11 facade blob is
  `8a761119e4a8d68eb291fc4edfadb52e027f8284`;
- working tree is clean before tests.

## Required execution

Run the exact Rabochii protocol self-test:

`python -m pytest -q rawlsing_next/tests/test_rabochii_execution_protocol.py rawlsing_next/tests/test_rabochii_bounded_court.py`

Require:
- 20 passed;
- 0 failed;
- 0 errors;
- 0 skipped.

Validate the exact court spec:

`python -m rawlsing_next.rabochii_execution_protocol court .rabochii/court_spec.json`

Require validation PASS.

Then execute the exact bounded court with:

`RABOCHII_EVIDENCE_EXECUTION_SHA=283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`

and no synthetic PR merge SHA:

`python -m rawlsing_next.rabochii_bounded_court .rabochii/court_spec.json --receipt <controlled_receipt_path>`

The court spec's own deterministic environment must remain effective.

Require the exact six-file court to complete with:
- 0 failed;
- 0 errors;
- 0 skipped.

Record the exact pass total rather than assuming the prior 53-test count, because C3-03 added hostile cases.

## Post-execution integrity

After execution:
- verify the tested working tree remains clean;
- hash the exact court receipt bytes;
- retain the complete court receipt;
- retain the environment identity/freeze evidence;
- declare raw survey source reads/materializations/decodes = 0.

Do not reinterpret earlier GitHub CI failures.

## Return terrain

On the commission branch, add only:

`WORKER_RETURNS/PYAT-C3-03-CODEX-SOURCE-FREE-EXECUTION-R1/**`

Required return:
- `00_RETURN.md`
- `01_EXECUTION_ENVIRONMENT.json`
- `02_PROTOCOL_RECEIPT.json`
- `03_COURT_RECEIPT.json`
- `04_SCOPE_AND_INTEGRITY.json`
- `05_FINAL_DISPOSITION.json`

The committed `03_COURT_RECEIPT.json` should preserve the exact normalized/generated bounded-court receipt content, not a prose paraphrase.

Allowed execution dispositions:
- `PASS_SOURCE_FREE_QUALIFICATION`
- `FAIL_SOURCE_FREE_QUALIFICATION`
- `BLOCKED_CODEX_EXECUTION_CAPABILITY`

A PASS must bind:
- exact execution SHA;
- semantic candidate SHA;
- exact environment versions;
- pip-freeze SHA-256;
- protocol counts;
- six-file court counts;
- court receipt SHA-256;
- clean-tree proof;
- raw-source access = 0.

Stop after returning evidence. Do not integrate or adopt C3 yourself.

Terminal:

`C3_03_CODEX_SOURCE_FREE_EXECUTION_FALLBACK_COMPLETE__HQ_ADJUDICATION_REQUIRED`
