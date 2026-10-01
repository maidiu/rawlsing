# PYAT N10E — P6 PROOF / EXECUTION PROVENANCE CORRECTION — R1

Status: ISSUED__NARROW_PROOF_AND_PACKET_CORRECTION

**LAUNCH IN: DeepSeek Harness — DeepSeek V4.1 Flash — Standard mode**

Repository:
`maidiu/rawlsing`

Branch:
`agent/deepseek-pyat-hq144-n10e-proof-provenance-correction-r1`

Exact branch base:
`58ba4320635162e8103ed38681ea5ae3e3bac014`

Independent review return:
`b89268d1824409d20a91a37a0a3ff7751a7ae75a`

Review disposition:
`CHANGES_REQUIRED`

Blocking findings:
- `REV-N10E-001`
- `REV-N10E-002`

Nonblocking documentary correction:
- `REV-N10E-003`

Read first:
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-INDEPENDENT-REVIEW-R1/05_FINAL_DISPOSITION.json`
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-INDEPENDENT-REVIEW-R1/03_HOSTILE_REPLAY_AND_EXECUTION_AUDIT.json`
- original commission:
  `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/00_COMMISSION.md`

## Governing adjudication

The independent reviewer accepted the provider implementation at the declared AT07/AT17 R1 grain.

Do **not** modify:

`rawlsing_next/pre553_empirical_possibility_provider.py`

unless a corrected P6 hostile produces a genuine provider-code counterexample.

The required work is proof/provenance correction.

## REV-N10E-001 — repair the vacuous changed-source proof

Current test:

`test_p6_geometry_is_recomputed_not_fixed_when_the_empirical_slice_changes`

constructs `narrowed_rows` but reruns the unchanged provider case.

Repair the test so the provider actually consumes changed empirical input.

Preferred proof:
- construct a second source-free fixture/case from the changed/narrowed rows;
- run the real provider on that changed case;
- prove the produced denominator/cell geometry follows the changed empirical product and differs from the canonical case as expected;
- prove the result still comes through the accepted composition/provider seam;
- do not hard-code geometry inside the provider or bypass the producer.

If the existing fixture API cannot cleanly rebuild a changed case without modifying production code, use the smallest fixture-only extension necessary.

Do not merely rename the test or weaken H13 unless a real changed-input court is technically impossible. A genuine changed-source proof is preferred.

## REV-N10E-002 — one final execution record

Because the provider test file will change, rerun exactly the commissioned four-file court once after the corrected test is coherent:

`rawlsing_next/tests/test_pre553_analytical_composition.py`
`rawlsing_next/tests/test_pre553_empirical_query.py`
`rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`
`rawlsing_next/tests/test_pre553_empirical_possibility_provider.py`

Record one exact final run consistently across:
- corrected return;
- execution receipt;
- final pytest output.

Counts, duration and command must agree.

Do not preserve conflicting durations from earlier runs as “final”.

## REV-N10E-003 — stale provenance language

Rewrite the old limitation saying commission tip `b631e1c...` was unavailable locally.

Preserve the historical truth:
- it was unavailable during the early local phase;
- credentials later became available;
- the branch was fetched/rebased onto the governed commission tip;
- final ancestry is lawful.

Do not present the early unavailability as a current final limitation.

## Preserve accepted review findings

Do not reopen or weaken:
- provider seam;
- no handwritten-evidence provider bypass;
- owner blob preservation;
- forward/reverse slice proof;
- P3 determinant closure;
- receipt identity well-foundedness;
- P5 fail-closed behavior;
- P7 replay;
- authority ceiling;
- no AT33 / real-source / structural-world / actor-person claim.

## Write allowlist

You may edit only:

1. `rawlsing_next/tests/test_pre553_empirical_possibility_provider.py`
2. optional `rawlsing_next/tests/n10e_empirical_slice_fixture.py`
3. optional `rawlsing_next/tests/n10e_empirical_slice_fresh_process_runner.py` only if genuinely required
4. `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/00_RETURN.md`
5. `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/03_FIXTURE_AND_ORACLE_FREEZE.json`
6. `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/05_HOSTILE_AND_REPLAY_AUDIT.json`
7. `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/06_EXECUTION_RECEIPT.json`
8. `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/07_FINAL_DISPOSITION.json`
9. `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/08_FINAL_PYTEST_OUTPUT.txt`
10. `WORKER_RETURNS/PYAT-N10E-PROOF-PROVENANCE-CORRECTION-R1/**`

Do not edit the independent review return directory.
Do not edit the provider implementation unless the corrected changed-source test establishes a real implementation counterexample; if that happens, stop with `COUNTEREXAMPLE_REQUIRES_PROVIDER_REOPEN`.

## Required return

Write:

`WORKER_RETURNS/PYAT-N10E-PROOF-PROVENANCE-CORRECTION-R1/**`

Required:
- `00_RETURN.md`
- `01_CHANGED_SOURCE_PROOF_AUDIT.json`
- `02_EXECUTION_PROVENANCE_RECONCILIATION.json`
- `03_DOCUMENTARY_CORRECTION_AUDIT.json`
- `04_FINAL_DISPOSITION.json`
- optional exact final output copy if useful.

Allowed dispositions:
- `PASS_PROOF_AND_PROVENANCE_CORRECTED__NARROW_INDEPENDENT_REREVIEW_REQUIRED`
- `FAIL_PROOF_CORRECTION`
- `COUNTEREXAMPLE_REQUIRES_PROVIDER_REOPEN`

Do not self-adopt.
Do not merge.

Terminal:

`N10E_PROOF_PROVENANCE_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`
