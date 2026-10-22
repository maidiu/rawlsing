# R02V r2 — evidence index, exact commands, counts and hashes

All commands were run from
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r02v-r2-projection-requalification-r1`
with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0` for test runs. Node-ID
lists used by the commands are in `evidence/*_nodeids.txt`.

## Commands, exit codes and results

| # | Exact command (node lists supplied by the named file) | Exit | Result | Evidence |
|---|---|---|---|---|
| 1 | `python3 -m pytest $(cat evidence/author15_nodeids.txt) -q -rA -p no:cacheprovider --junitxml=evidence/pytest_author15.xml` | 0 | 15 passed, 0 failed, 0 skipped | `evidence/pytest_author15.log` / `.xml` |
| 2 | `python3 -m pytest $(cat evidence/reviewer9_nodeids.txt) -q -rA -p no:cacheprovider --junitxml=evidence/pytest_reviewer9.xml` | 0 | 9 passed, 0 failed, 0 skipped | `evidence/pytest_reviewer9.log` / `.xml` |
| 3 | `python3 -m pytest $(cat evidence/focused26_nodeids.txt) -q -rA -p no:cacheprovider --junitxml=evidence/pytest_focused26_preexisting.xml` | 0 | 26 passed, 0 failed, 0 skipped | `evidence/pytest_focused26_preexisting.log` / `.xml` |
| 4 | `python3 -m pytest rawlsing_next/tests/test_universal_source_projection.py -q -rA -p no:cacheprovider --junitxml=evidence/pytest_full31.xml` | 0 | 31 passed, 0 failed, 0 skipped | `evidence/pytest_full31.log` / `.xml` |
| 5 | `python3 -m pytest rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_empirical_query.py -q -rA -p no:cacheprovider --junitxml=evidence/pytest_retained42.xml` | 0 | 42 passed, 0 failed, 0 skipped | `evidence/pytest_retained42.log` / `.xml` |
| 6 | `python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint rawlsing_next/tests/test_universal_source_projection.py` | 0 | `AST_LINT_PASS` | `evidence/proof_lint.json` |
| 7 | `python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness rawlsing_next/tests/test_universal_source_projection.py.proof.json --root .` | 0 | 8 claims, baseline PASS, `TARGET_ASSERTION_FAILED` under each fault, adapter restored | `evidence/proof_witness.json` |
| 8 | exact original defect scripts from `a287`, imported and called against the repaired candidate | refusal | D1 `DUPLICATE_RESPONDENT_KEY_MAPPING:1`; D2 `DUPLICATE_NORMALIZED_SOURCE_KEY:0` | `evidence/defect_scripts_on_repaired_candidate.txt` |
| 9 | direct strict-receiver probe with the transformed occurrence declaration | expected `ValueError` | `LiTS observed representation has unexpected missing declaration` | `evidence/strict_receiver_bound_retained.txt` |
| 10 | import/path/hash probe | 0 | actual module paths and SHA-256 identities | `evidence/import_identities.txt` |
| 11 | `python3 <proof_gate> changed --base 6f4be338... --head <reviewer commit> --root .` | 0 | changed-test/proof-integrity gate pass; contract witness rerun | recorded in `04_REMOTE_READBACK.md` and the completion readback |

The proof checker was read from the tracked repository path
`CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py`, blob SHA-256
`e3125e121babb6f522688e050b1840f514e04796b47fdab81c5d40b140f858ed`.

## Counts and honest overlap

| Suite | Tests | Passed | Failed | Skipped |
|---|---:|---:|---:|---:|
| Author 15 | 15 | 15 | 0 | 0 |
| Ported reviewer 9 (7 positives + 2 defects) | 9 | 9 | 0 | 0 |
| Pre-existing focused 26 (15 author + 11 r2) | 26 | 26 | 0 | 0 |
| Full focused 31 (26 + 5 independent r2v-r2) | 31 | 31 | 0 | 0 |
| Retained facade + empirical-query 42 | 42 | 42 | 0 | 0 |

The author 15 and reviewer 9 are subsets of focused 26; focused 26 is a subset
of full focused 31. The five new tests are exactly the `test_r2v_r2_*` names.
**Distinct focused + retained evidence is 73 tests (31 + 42), not 97 or 92 by
summing overlapping suites.** No test was skipped.

New independent tests:

- `test_r2v_r2_original_collision_mappings_refuse_before_c11`
- `test_r2v_r2_normalized_admission_uniqueness_matrix`
- `test_r2v_r2_mixed_numeric_string_identities_conserve_tuples_and_domain`
- `test_r2v_r2_source_domain_faults_same_assertion_and_fresh_restore`
- `test_r2v_r2_scalar_and_separate_unit_positives_retained`

## Candidate and source hashes

| Path | SHA-256 | Meaning |
|---|---|---|
| `rawlsing_next/pre553_source_native_preimage_adapter.py` | `c9ea22ada390babf7b3a977352b784bcfeb498e738dcb0024fc7f4d793b90b95` | repaired candidate adapter; restored exact after witness |
| `rawlsing_next/pre553_source_backed_c11_facade.py` | `03b88d258d21c403542756db7316923aa392871442d99294de904b1744da1d01` | unchanged facade |
| `rawlsing_next/pre553_c11_integrity.py` | `3963facef5c8ae2981991ffa8c5c5c9b717fb4e09f342eec277198fc5cf38a33` | unchanged C11 integrity |
| `rawlsing_next/pre553_c11_ingest.py` | `0c56a0f6f656547a096982a6adab21c9b47d749385411a5d159f2b5390eec8bf` | unchanged C11 ingest |
| `rawlsing_next/pre553_c11_repository.py` | `84a71fe43307cca30f9eeaaedb269d8390468a4744a0fac251aebc2cda7b498e` | unchanged C11 repository |
| `rawlsing_next/pre553_empirical_query.py` | `d45ad313bc57e94c8c3652b4123c7cb03b0fc18d38d577aaaae94435664ef4cb` | unchanged I03 query |
| `rawlsing_next/_pre553_query_eval.py` | `c72d7d35bfa5d3cb4b406bdd90530b2822416850bba48cdd12ce784ba10cd670` | unchanged query evaluation |
| `rawlsing_next/pre553_physical_decoder.py` | `a75a8ff72310949b84adbe682a01375c5dcf5dcee69e94e2a4a8a9b39e17017b` | unchanged decoder |
| `CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py` | `e3125e121babb6f522688e050b1840f514e04796b47fdab81c5d40b140f858ed` | checker |
| `rawlsing_next/tests/test_universal_source_projection.py` at candidate | `3673908c02b6066a10b985bd26106686dfbb0eba463551a3e6d3e21db5327b63` | author r2 test file before reviewer additions |
| `rawlsing_next/tests/test_universal_source_projection.py.proof.json` at candidate | `39ba9ef15d0628d4a56877022d46db18a7403a9ab4a07a734c2743c2a0af72dd` | author r2 proof sibling before reviewer additions |
| `rawlsing_next/tests/test_universal_source_projection.py` after reviewer additions | `6144bf6d210efa4e0c4c7cfda00469158d46dd79e828ff8e7dddfa8be30d61c0` | reviewer test file |
| `rawlsing_next/tests/test_universal_source_projection.py.proof.json` after reviewer additions | `8f1c59bade355f795dedd150e169e0fe058fdbb7999a0092e6a3953934f13598` | reviewer proof sibling |

The candidate author-return declared adapter, test-file and proof-file hashes
were independently checked and match: `c9ea22ad...`, `3673908c...`,
`39ba9ef1...`.

## Proof claims

The sidecar retains the author's four claims and adds:

1. `R2V-R2-ORIGINAL-DESTINATION-COLLISION-REFUSAL` — disable normalized
   destination uniqueness; target test fails by assertion.
2. `R2V-R2-ORIGINAL-SOURCE-KEY-COLLISION-REFUSAL` — disable normalized source
   uniqueness; target test fails by assertion.
3. `R2V-R2-SOURCE-DERIVED-TUPLES-AND-DOMAIN` — poison the canonical value;
   the mixed-identity tuple/domain test fails by assertion.
4. `R2V-R2-SAME-DOMAIN-RESPONDENT-ASSIGNMENT-FAULT` — force every row to the
   first respondent key; the same frozen-domain test fails by assertion.

`evidence/proof_restore_receipt.txt` records adapter before/after equality and
an empty production diff.

## Changed-file allowlist in this reviewer worktree

```
rawlsing_next/tests/test_universal_source_projection.py
rawlsing_next/tests/test_universal_source_projection.py.proof.json
WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/
```

No production, frozen policy, commission, author-return, or foreign-return file
is in the reviewer diff. `git diff` over production paths is empty.
