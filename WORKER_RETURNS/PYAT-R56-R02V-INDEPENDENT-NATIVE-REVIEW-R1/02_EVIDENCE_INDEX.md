# R56-R02V — evidence index and exact commands

All commands were run from
`/Users/matthewsmith/Desktop/Rawlsing/R56-R02V-independent-projection-review-wt`
with `PYTHONDONTWRITEBYTECODE=1`. The proof witness was run from the repository
root with the repository's own checker, not a `/tmp` copy.

## Commands and exit codes

| # | Command (abridged) | Exit | Result | Evidence |
|---|---|---|---|---|
| 1 | `python3 -m pytest rawlsing_next/tests/test_universal_source_projection.py -q -rA` before reviewer changes | 0 | 15 passed | author receipt; reproduced again as #2 |
| 2 | Author 15 node IDs only, after reviewer changes | 0 | 15 passed | `evidence/pytest_author15.log` |
| 3 | `python3 -m pytest rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_empirical_query.py -q -rA` | 0 | 42 passed | `evidence/pytest_retained.log` |
| 4 | Independent 7 positive/consumer tests | 0 | 7 passed | `evidence/pytest_r02v_positive.log` |
| 5 | Independent 2 defect reproducer tests | 1 | 2 failed, `DID NOT RAISE` | `evidence/pytest_defects.log` |
| 6 | Full focused file after reviewer additions | 1 | 22 passed, 2 failed | `evidence/pytest_full.log` |
| 7 | `python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint rawlsing_next/tests/test_universal_source_projection.py` | 0 | `AST_LINT_PASS` | `evidence/proof_lint.json` |
| 8 | `python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness rawlsing_next/tests/test_universal_source_projection.py.proof.json --root .` | 0 | 2 claims, both `TARGET_ASSERTION_FAILED` under injected fault, baseline PASS | `evidence/proof_witness.json` |
| 9 | `python3 evidence/defect_normalized_respondent_key.py` | 0 | false `SUPPORTED` denominator 1 for 2 source respondents | `evidence/defect_normalized_respondent_key.out.json` |
| 10 | `python3 evidence/defect_ambiguous_source_key.py` | 0 | ambiguous normalized key accepted, source 0 becomes P1 | `evidence/defect_ambiguous_source_key.out.json` |
| 11 | `python3 evidence/build_r02v_receipt.py` | 0 | exact per-run 4x3 and 3x2 missing identities | `evidence/r02v_independent_receipt.json` |
| 12 | strict-envelope receiver probe | 0 | `ValueError: LiTS observed representation has unexpected missing declaration` | `evidence/envelope_strict_receiver_probe.out.txt` |

The failure in #5 is intentional evidence of the defect, not an environment or
import failure. #6 therefore contains both the 15 author passes and the 7
independent positive passes, plus the 2 defect failures.

## Code and policy hashes actually used

| Path | SHA-256 |
|---|---|
| `rawlsing_next/pre553_source_native_preimage_adapter.py` (candidate, unchanged) | `2cf5e98bc29081678c364d3ff591c71f11ce7ebf3564419af8a26f5f04113b64` |
| `rawlsing_next/pre553_source_backed_c11_facade.py` (unchanged) | `03b88d258d21c403542756db7316923aa392871442d99294de904b1744da1d01` |
| `rawlsing_next/pre553_c11_integrity.py` (unchanged) | `3963facef5c8ae2981991ffa8c5c5c9b717fb4e09f342eec277198fc5cf38a33` |
| `rawlsing_next/pre553_c11_ingest.py` (unchanged) | `0c56a0f6f656547a096982a6adab21c9b47d749385411a5d159f2b5390eec8bf` |
| `rawlsing_next/pre553_c11_repository.py` (unchanged) | `84a71fe43307cca30f9eeaaedb269d8390468a4744a0fac251aebc2cda7b498e` |
| `rawlsing_next/pre553_empirical_query.py` (unchanged) | `d45ad313bc57e94c8c3652b4123c7cb03b0fc18d38d577aaaae94435664ef4cb` |
| `rawlsing_next/_pre553_query_eval.py` (unchanged) | `c72d7d35bfa5d3cb4b406bdd90530b2822416850bba48cdd12ce784ba10cd670` |
| `rawlsing_next/pre553_physical_decoder.py` (unchanged) | `a75a8ff72310949b84adbe682a01375c5dcf5dcee69e94e2a4a8a9b39e17017b` |
| `rawlsing_next/tests/test_universal_source_projection.py` (reviewer-edited) | `615985874ca0752142b30354cf51aaef08145e301d86275b01d199513a9eb046` |
| `rawlsing_next/tests/test_universal_source_projection.py.proof.json` (reviewer-edited) | `7008b2f7a4fe54a0a114e753541d3c8c05304b737b256e3d52a130e1c0fa2caf` |

The candidate author's original test-file and proof blobs are
`887e3346a823eb286a18ccc46a6a19802b4f6c68` and
`8a9b7c9ffe7dacc47e587912c8437341ea804a7d` (Git blob identities). The
reviewer kept all 15 author tests unchanged; see `evidence/r02v_test_additions.patch`.

## Evidence file hashes

| Evidence file | SHA-256 |
|---|---|
| `00_RETURN.md` | recorded in `manifest.json` |
| `01_SESSION_AND_STARTUP_PROVENANCE.md` | recorded in `manifest.json` |
| `03_R02V_OPEN_CHALLENGE_ADJUDICATION.md` | recorded in `manifest.json` |
| `evidence/build_r02v_receipt.py` | `744b5cb1f324712579b234242d9d574c7bbc2141b2982bfb1d29ed4ddbe7533b` |
| `evidence/defect_ambiguous_source_key.out.json` | `d357963231e95f57a8ad43e7f799210634bad2ff27d2f3fc367af55332905b40` |
| `evidence/defect_ambiguous_source_key.py` | `0549e5dff6c9d6cdcadad926c3bcf6809e45f86cb892fb2250ae6f5ae663239b` |
| `evidence/defect_normalized_respondent_key.out.json` | `2777495f024b5912545a5a51c11c6410a948ccc91c9e4cb096ec39f60acafa0e` |
| `evidence/defect_normalized_respondent_key.py` | `177d68636b34a6323b160af86467a62b4e8857fec7020175d898b818cd9c7ec4` |
| `evidence/envelope_strict_receiver_probe.out.txt` | `dcee2769c3c9c902666652740d312a38daa362137861b5bcad8f9e5c8842b4e6` |
| `evidence/proof_lint.json` | `a477dd4d5965979cf2973cef236a1ddd2435f214148c8dcac5f1a35954bf6ce9` |
| `evidence/proof_witness.json` | `cb00fb1dd08d2835611f3a2475e2843303c0df292fcea7eab1fc361fe534c4d6` |
| `evidence/pytest_author15.log` | `6bb9ffa5032566cfda3b3ea6767c0ee11be0fbc5df15d3e8ea3954e061837c02` |
| `evidence/pytest_author15.xml` | `adf626cbdfa53e34c5f5061b79e7fc3438f9b01daec3e201b0ad30db50d134d9` |
| `evidence/pytest_defects.log` | `912abda5723bc165659493bdf16cf6130d2f90aaa47a518870f0f624c68da1f4` |
| `evidence/pytest_defects.xml` | `bb824d8180deb9edc85fbef79c10c5c4926e0a30aef932da3ccd79479d39345c` |
| `evidence/pytest_full.log` | `ef789c77e105d1ad3aa256c3e840ea332c2ab697fac0df187d31cb29d1b050b4` |
| `evidence/pytest_full.xml` | `d91bf744a2c5ff48b4426289d1660f1e6c5808a394e48b390104beab5a061086` |
| `evidence/pytest_r02v_positive.log` | `81d6a75461fb2ee1b2f4a831460fbf5a25210075e300eed98c4fb4d501590161` |
| `evidence/pytest_r02v_positive.xml` | `21dce440a56d34fb2bb4e40104f93e117c1e55535d52b267616787185a98174e` |
| `evidence/pytest_retained.log` | `2cea8f43749121e57de44747c44a8573a8b86e100d5fd901c2cd720313295e7d` |
| `evidence/pytest_retained.xml` | `101488af74ff8b99b64b6e4667bd6afedb3e1f71f6153dbd5698b2ce42b117ec` |
| `evidence/r02v_independent_receipt.json` | `46315fa0d1f8bad7425ebc5beb1ac2437059705c7059d7cbbf08e1be8ff37a13` |
| `evidence/r02v_proof_additions.patch` | `225d8ce7ea4d88b150bde81c0ad92e7d4d4f85f6d4f7173bc2711ed226897404` |
| `evidence/r02v_test_additions.patch` | `022ae1762b3b3a976eb09f52c2a68f3c917f53637d7beda4a5ff9afa5e4dc44e` |

## Proof-integrity claims

1. `R56-R02-OCCURRENCE-TUPLES` — author claim retained. Fault:
   `canonical = rule.value_aliases.get(raw_token, raw_token)` ->
   `canonical = "0"`. Baseline PASS; target assertion RED.
2. `R02V-INDEPENDENT-SOURCE-DOMAIN` — reviewer claim. Fault:
   `respondent_token_by_row[row_ordinal] = mapping[respondent_token]` ->
   `respondent_token_by_row[row_ordinal] = next(iter(mapping.values()))`.
   Baseline PASS; target assertion RED.

The checker restored the adapter after each fault; the adapter hash was
verified equal to the candidate hash after the witness.
