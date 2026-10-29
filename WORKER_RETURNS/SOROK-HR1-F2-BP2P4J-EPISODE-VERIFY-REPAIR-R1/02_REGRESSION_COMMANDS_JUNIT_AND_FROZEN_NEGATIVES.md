# F2 BP2P4J — exact regression commands, JUnit and frozen negatives

Observed FINDING: the unmodified BP2P4J verifier reports `episode:0:body_hash_mismatch` for a valid SAY episode because `append_episode` hashes the body before appending `episode_id`, while `verify_branch_chain` excluded only `hash`. Causal INTERPRETATION: the verifier's episode preimage was reconstructed from the durable row instead of the pre-hash row. Proposed HQ ACTION: review this candidate overlay and decide adoption; do not treat this return as owner acceptance. Accountable OWNER: original BP2P4J/BP4 C12 owner, then independent I2 reviewer.

## Environment

Local macOS x86_64, Python 3.11.3, pytest 9.1.1, SQLite 3.40.1, stdlib only. Base worktree was detached at original BP2P4J `5b3e6577400ea1d88971ae6b48e41a118b8059ae`; return branch worktree is at startup `2c8da7fcbf721a0e04fb25735cd4bee58754969f`. Environment overrides for every run: `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1`.

## Commands and actual results

Baseline original suite, before adding the focused test, at base `5b3e657`:

```sh
cd .../hr1-f2-bp2p4j-base/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q --junitxml=.../hr1-f2-baseline.xml
```

Result: `33 passed`, 0 failed, 0 errors, 0 skipped. The original suite does not verify a chain after a successful `say`, so the defect is latent under it.

Frozen valid-SAY RED on unmodified `c12_verify.py`:

```sh
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_episode_verifier_regression.py::test_valid_say_episode_is_green_and_preserves_the_post_hash_id -q
```

Result: `1 failed`, assertion report `{'ok': False, 'errors': ['episode:0:body_hash_mismatch'], 'counts': {'episode': 1, ...}}`. The exact durable row is preserved in `evidence/04_ORIGINAL_RED_ROW_AND_PREIMAGE.json`:

- episode seq: `0`
- stored/body hash: `c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be`
- episode_id: `TEST_ONLY_BP4_EP_c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be`
- canonical preimage SHA-256 excluding `hash` and `episode_id`: `c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be`
- stored body JSON SHA-256: `6a30f3c5e6b017c94a71e4139f2f68df1dfe3fa7552d1d6292d083f607744a27`

Repaired full suite with the candidate overlay:

```sh
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q --junitxml=.../hr1-f2-final.xml
```

Result: `38 passed`, 0 failed, 0 errors, 0 skipped. Per-file: `test_episode_verifier_regression` 5, `test_joined_product` 10, `test_joined_security` 12, `test_joined_severance` 7, `test_source_closure` 4.

The five added tests are: valid SAY is green and preserves the post-hash id; tampered episode body stays `episode:0:body_hash_mismatch`; tampered `episode_id` is refused as `episode:0:episode_id_mismatch` without waiving the body preimage; tampered world-event body stays `world_event:0:body_hash_mismatch`; cold reopen preserves the episode hash, derived id and chain digest.

Existing cold-reopen coverage `test_cold_reentry_in_a_new_process_keeps_the_bp2_target` passed in the same suite. Existing source-severance coverage `tests/test_joined_severance.py` passed 7/7. Existing forgery/refusal coverage in `tests/test_joined_security.py` passed 12/12, including the shape-valid envelope, self-E2, self-occurrence, forged world receipt and C12 append-only guards.

## Frozen negatives and HOLD retained

All original test files are byte-unchanged. Pinned blobs: `tests/conftest.py` `35c1e1c0cac69c6006f669201b018289348e619a`; `tests/test_joined_product.py` `f0e52ea3a2e39d29c4740ead7032c366cec19eeb`; `tests/test_joined_security.py` `9cffe8a95d23492053f5ccd612128f0d02a96ed9`; `tests/test_joined_severance.py` `9e15af676d0ef3f33a345ebbc3ee0734e09ac63c`; `tests/test_source_closure.py` `cfe1d1b4e155e0d12699280af6b071c320702e95`.

`test_raw_database_access_can_drop_the_append_only_trigger_is_a_residual` still passes and still reports the distinct HOLD: raw SQLite access can drop the C12 append-only trigger and delete rows; content hashing alone cannot detect the deletion, and only the out-of-band `chain_digest` comparison does. This repair does not claim an authenticated external anchor or close that HOLD.

`test_upstream_bp4_store_verify_is_self_referential` still passes: BP4's own `C12Store.verify` remains self-referential and unpatched; this candidate only repairs the independent add-on verifier.

## Evidence files

- `evidence/01_BASELINE_ORIGINAL_33.xml` SHA-256 `209343acb2333b8f4cf0fe2b343663f79d0983d3f79702df43bd22d313f43109`; log `cb27fd7f42b6d224dfa05db3fc71777af0a383bcb32d6cfe1be44ebfcab22739`.
- `evidence/02_REPAIRED_38.xml` SHA-256 `876e78612b93c20b34e98ba60f01223860faf7eb20806cf4718e23db48feb5ef`; log `8e0dd3e259f68c193f05e3e04acef6407a9ed36e5124438d9f9a04fbd0db33db`.
- `evidence/03_ORIGINAL_RED_SAY.log` SHA-256 `9eb49d88b37425f6ab3797b9d3f2d4ce95397b44527e01792e44119c27791d9f`.
- `evidence/04_ORIGINAL_RED_ROW_AND_PREIMAGE.json` SHA-256 `5407d5440489435231dc2292e19bd33609cb46d748c9a101b1e65e33e5428a1e`.

## NOT RUN

No native survey/respondent data, source-rule issuance, C11/C12 native adoption, production deployment, PRE-MAIN mutation, PR #514/#516 change, push of upstream branches, or independent review was performed. The repaired verifier was not run by the original owner; owner replay remains outstanding.

DONE: exact original RED, minimal candidate, same-assertion GREEN, tamper/cold/severance/residual reruns. REMAINING: owner replay and adoption decision. CRITICAL BLOCKERS: none for the bounded engineering repair; authority and native science remain separately held. LARGEST PRODUCTIVE MOVE: original BP4/C12 owner replays the five commands against the candidate SHA. FLIGHT: sourcefree local Git/Python only, no upstream mutation. DELTA: episode preimage now excludes only the derived post-hash id and separately validates its derivation.
