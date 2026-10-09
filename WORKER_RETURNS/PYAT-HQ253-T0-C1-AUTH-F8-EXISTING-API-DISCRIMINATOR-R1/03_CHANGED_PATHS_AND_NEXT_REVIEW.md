# HQ253 — changed paths, hashes, and independent review instructions

## 1. Changed paths — EXACTLY TWO, both authorized

| path | change | authorized by commission |
|---|---|---|
| `rawlsing_next/tests/test_pre553_scoped_rich_c1_f8_existing_api_discriminator.py` | **NEW**, 25 tests | "New test file ONLY" |
| `WORKER_RETURNS/PYAT-HQ253-T0-C1-AUTH-F8-EXISTING-API-DISCRIMINATOR-R1/` | **NEW**, 5 return artifacts | "Return directory ONLY" |

**Production owners modified: NONE.** Verified by `git status --short` showing only the single new
test file before staging, and by the diff below containing no production path.

```
 rawlsing_next/tests/test_pre553_scoped_rich_c1_f8_existing_api_discriminator.py | new file
 WORKER_RETURNS/PYAT-HQ253-T0-C1-AUTH-F8-EXISTING-API-DISCRIMINATOR-R1/*            | new files
```

**Not touched:** no production owner, no HQ/control, no authority/issuer, no native or raw inputs,
no other test file.

## 2. Source identities at execution

| identity | value |
|---|---|
| sealed commission tip | `8d61676670506a85ad2e7fabc425c1cb46291e47` (verified vs remote) |
| parent sealed control | `a0a1a0eb2ea1243c2a7341c2b85f22ec1d979a0e` |
| semantic PRE-MAIN | `1f47063c3205a45888b3c55e81e7485943ed1390` |
| R01 review ref | `762cda8ce5b2d9f67b0870f6474df4468ca91630` |
| S01 receipt ref | `b3f28aad418150f4cadd54bcf6a6c2ab34a35898` |
| fixture blob | `0393cc8c17a313b7944b2a5287d0406d6cbe3849` (no drift) |
| F8 binding blob | `4ba00b8ecf73f70ad0f6481e255fd0117744418a` (no drift) |
| F8 result owner blob | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` (no drift) |
| AT09/10/11 court blob | `c8a83d3deffa6f0a10309e15143d7dcc953a8abe` (no drift) |
| runtime | macOS 13.7.8 x86_64, Python 3.11.3, pytest 9.1.1 |
| pyarrow / pandas / pyreadstat | **absent** — no survey, Library or native path reachable |

## 3. Banked execution

| # | exit | outcome |
|---|---|---|
| 1 — new court | **0** | **25 passed** |
| 2 — 5 relevant unchanged courts | **0** | **234 passed** |
| 3 — broader C1/applicability/F8 sweep | 1 | 357 passed, 9 pre-existing collection errors (missing `pandas`/`pyarrow`/unrelated harness; none touch this lane) |

## 4. Independent hostile reviewer instructions

HQ must issue this **separately**. The test author does **not** approve its own result.

The reviewer should attack these five claims specifically:

1. **Oracle neutrality.** Confirm the frozen expectations were pinned from `XOR_ORACLE` and never
   derived from candidate output. Try moving the oracle and check the court fails.
2. **Anti-vacuity.** Confirm Q1/Q2 are genuinely non-interchangeable and that denominators (2 vs 1)
   come from a real `q(A,B)` intersection rather than multiplied marginals.
3. **The custody counterexample.** Confirm that only `provenance_refs` changed and that
   `result_hash` equality is therefore a real false positive — then check the reviewer agrees the
   gap is narrow (i.e. `evidence_ref` and geometry *are* covered).
4. **The second finding.** Independently reproduce the target-use permission divergence and confirm
   the root cause at line 881 of the binding owner. Decide whether it is in scope for T1 or a
   separate defect.
5. **Non-claim discipline.** Verify the court claims no T1 adoption, no EE14 grant, no CURRENT, no
   custody certification, and does not restate AT09/10/11 coverage.

Also confirm: **no production file was modified**, no adapter was introduced, and the nine
collection errors are pre-existing rather than introduced here.

## 5. Self-approval

**None.** No T1 adoption, no production cutover, no self-approval, no HQ/control write. The
worker stops here for independent changed-candidate review.
