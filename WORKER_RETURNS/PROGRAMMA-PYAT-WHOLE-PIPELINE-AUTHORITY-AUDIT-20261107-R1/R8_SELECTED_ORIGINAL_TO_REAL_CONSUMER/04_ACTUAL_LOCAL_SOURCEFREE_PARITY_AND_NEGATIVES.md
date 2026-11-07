# Execution receipt — deterministic S1 tests versus local S2 NOT_RUN

Repository: maidiu/rawlsing
Protected exact observation / R8 branch start: 7a5429ffbc48efd25e28c912da80c822e66bc182
R8 branch: research/pyat753-r8-selected-original-to-current-consumer-authority-20261107-r1
Inspection surface: S0–S1 authenticated private GitHub contents + deterministic in-memory UTF-8/CSV comparison. NOT mainMac, NOT local Python S2, NOT native respondent/SAV or original Mac archive.
Commission: https://github.com/maidiu/rawlsing/issues/766


## Actually executed (in-memory S1, not local Python)
Source inputs: both protected GitHub CSV responses and protected `wave1_gt12_i03_positive_facts.py` inspected through the authenticated connector at exact protected observation. A pure JavaScript SHA-256 algorithm was independently sanity-checked against the standard `sha256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` vector and then applied to the **UTF-8 encoded bytes** of the returned full CSV text. The read itself was GitHub UTF-8 content, not a byte-for-byte local Mac archive read.

| Case | Expected | Actual | Grade |
|---|---|---|---|
| AR-0007 Git text UTF-8 bytes | 5,734; `89d0cb28c20f014278a58fcbb269b8726efe8a9580f2d470caa299ab113f00eb` | Exact byte length and SHA matched | S1 PASS |
| AR-0046 Git text UTF-8 bytes | 76,430; `d270f59da94029780b0e7f26f78cc0f5ede418ed431b5ababeefd2c5e2a00fc8` | Exact byte length and SHA matched | S1 PASS |
| Binding release cardinality | 236 unique source/wave/var tuples | 236 / 236 | S1 PASS |
| Scale registry cardinality | 145 unique contract hashes, all `CERTIFIED/NO_REVIEW` | 145 / 145 | S1 PASS |
| All binding indices | in `[0,145)`; all 145 contracts referenced | all in range; all covered | S1 PASS |
| Correct `Afrobarometer/R1/dememp` | index 37 → `44c656ab...37bd43ba1ab` | exact | S1 PASS |
| Wrong wave `Afrobarometer/R2/dememp` | no exact AR-0007 binding | absent | S1 PASS negative |
| Wrong source `ArabBarometer/R1/dememp` | no exact AR-0007 binding | absent | S1 PASS negative |
| Real selected `Afrobarometer/R5/Q86A` | no AR-0007 binding | absent | S1 PASS negative |
| Real selected `Afrobarometer/R5/Q86B` | no AR-0007 binding | absent | S1 PASS negative |

**Not executed** (and not silently upgraded to PASS): instantiate `ResponseSemanticsContractAuthority.from_repository`, `build_snapshot_for_bindings`, `GovernedC11Projection`, `project_c11_candidate_from_physical_cells`, `C11Repository` ingest or `execute_empirical_query` end-to-end; generate events from a synthetic real source cell; compare R5 signed projection to current C11 governed field; pytest. **Reason:** the active environment has authenticated private GitHub S0–S1 but no local Git checkout, mainMac original source custody or authorized S2 Python runner. R5 adapter code is observed in candidate commit only; the protected C11 tests use synthetic fixtures but no selected historic R1 dememp demand.

## Reviewed-code negatives, NOT_RUN

- Historical R5 reader: wrong contract for a valid key → `AUTHORITY_BINDING_CONTRACT_MISMATCH` diagnostic; unbound source/wave/var → `AUTHORITY_BINDING_NOT_MEMBER`; no positive snapshot for missing member. These are inspected code branches, not executed tests here.
- C11 facade `pre553_source_backed_c11_facade.py:504-512,538-541`: absent explicit governed projection; source SHA mismatch; incomplete row/respondent map; unbound physical response. Inspected guards, not execution.
- C11 `GovernedC11Projection:303-356`: semantic/authority closure, duplicate owner restrictions, explicit positive scopes. Inspected guards, not execution.
- I03 `pre553_empirical_query.py:311-438`: exact operation/family/source fit and complete target-use triple. Inspected guards, not execution.
- Shadow/withdrawn alternate: R4 records **no competing release** for this AR-0007/AR-0046 pair. A manufactured "withdrawn" row is neither executable nor evidence; no such source was tested.
- `test_wave1_gt12_i03_positive_facts.py` has a 3-respondent synthetic test fixture and monkeypatch of frozen SHA; this is **not** re-running the 19,210 native R5 respondents.

## Owner-run replay (authorized checkout only, not performed)

1. Pin protected `7a5429ff...`, inspect checkout and exact file SHA and no conflicting owner lease; obtain required frozen docs through approved Git reader.
2. Verify AR-0007/AR-0046 hashes and sorted index 37; exercise `ResponseSemanticsContractAuthority.from_repository` at the candidate R5 code commit **in a separate sourcefree test branch**, not by copying it into protected production. Negative wrong expected digest, key, wave, source, contract.
3. If a **real selected R1 dememp modern source producer** is issued, construct only its exact synthetic `PhysicalCell` plus `GovernedC11Projection` with signed/scoped authority snapshots and test `project_c11_candidate_from_physical_cells`; verify positive + wrong SHA, wrong value/state, withdrawn/superseded authority, missing target-use. Do not create synthetic ALLOW for a claim of current scientific authority; mark replay-only.
4. Run tracked sourcefree tests `pytest -q rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py` if their local deps/permissions exist. Capture actual exit, source/commit and log; never treat this proposed command as executed.

**Measured receipt:** S1 PASS for source identity/structural join/selected current nonmembership; **S2 NOT_RUN**; **S3 native NOT_AUTHORIZED/NOT_RUN**.
