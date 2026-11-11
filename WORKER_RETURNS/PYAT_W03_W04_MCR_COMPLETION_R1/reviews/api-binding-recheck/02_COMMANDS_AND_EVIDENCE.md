# CCF5-R01 API-binding recheck — commands and evidence

**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-engineering-review-r1`
**Branch:** `review/pyat-w03-w04-api-binding-recheck-r1`
**Exact reviewed source:** `a5a635a794aa701cde0b7d7b3b6c0708c76288b2`
**Author repair:** `cd98ba7ee1d96cef842663c13eac594c90542525`
**Prior focused review:** `f250bded334fd7a300113e7b9a9118f841e597d4` (`REVISE` solely CCF5-R01)
**Original CC-F05 review:** `07c172683c4a720b8d1c37599c3e09a5357e56d8`
**Verdict:** `ACCEPT_AT_CCF5_R01_SCOPE`

All commands used an explicit `cd` into this worktree. Runtime, existing tests, contract, HQ and peer/protected terrain were read-only. Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/api-binding-recheck/`.

## 1. Source, branch and frozen contract identity

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-engineering-review-r1
git branch --show-current
git rev-parse HEAD
git status --short
```

Result:

```text
review/pyat-w03-w04-api-binding-recheck-r1
a5a635a794aa701cde0b7d7b3b6c0708c76288b2
clean except this review lease
```

Reviewed blobs and file hashes:

```text
d1db88c62bda848aee478e13120393153d5a61bf  CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py
ea1edef49b0f11bcc36e45d6cf9f59fdfc1d2fac9684b920df6aa6d9dcb7218a  (file SHA-256)
5b0f1ce787a6d9e6a8c003fa99bef434213ffaa7  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
7b476487f0773a6e129a443f8975b98105985f3d4e66f7185cc764bf1617ccf6  (file SHA-256)
```

Frozen files are unchanged by the repair (`git diff --quiet a5a635a^ a5a635a -- ...` exit 0):

```text
ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166  PYAT_W03_W04_MCR_C_Commission.md
c25dbb96259971a8f623179dd1435bcdc2d684edb2b02a4970565bbb0c5c25e7  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
5de8d68207de353926bd2d42095a8c8c44a36b06ac4038a7c9b16a1b6173428e  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv
```

The frozen 12-ID TSV has 12 data rows (freeze source `5a891a311c70f4cb8c09864008b33405362f7c7c`):

```text
W03-PREVIOUS-CAPITAL, W03-COLD-HIGHWATER, W03-SELECTED-CELLS-CANON,
W03-SEMANTIC-TOPOLOGY, W03-FIRST-CONSUMERS, W04-COLD-PERSIST-REOPEN,
W04-GOVERNED-DEFAULT, W04-AUTHORITY-INVALIDATION, W04-ATOMIC-LIFECYCLE,
W34-RESOURCE-ECONOMY, W34-PRODUCT-BOUNDARIES, W34-REPRODUCIBLE-RETURN
```

The prior review already qualified the wrapper/contract/original-preservation/scalar-composite/CLI/tracking negatives. They are not reopened here; the five-test regression includes the frozen launch/frozen-original checks and the tracked negative.

## 2. Repair diff and signature

```sh
git diff a5a635a^ a5a635a -- \
  CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
git diff --stat a5a635a^ a5a635a -- <same paths>
```

Result:

```text
8 API lines + 21 test lines; 0 deletions
```

The API change reads `returned_path` text and requires exact equality with `returned`; mismatch appends `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH`; read failure appends `MCR_C_EVIDENCE_PATH_UNREADABLE`. The existing `_evidence_externality` still appends `MCR_C_EVIDENCE_PATH_UNAVAILABLE` for missing paths. The signature is identical before and after:

```text
def verify_return(commission, returned, candidate_sha, root, *, returned_path: Path | None = None):
```

The test diff adds one focused test function, no existing test changes and no deletions. The new test asserts the mismatch RED and specific error, a missing-path RED, and restoration with the valid external pair.

## 3. Existing five tests and self-test

```sh
TMPDIR="$PWD/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/api-binding-recheck/tmp" \
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
```

Result: `5 passed in 1.99s`.

```sh
TMPDIR="$PWD/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/api-binding-recheck/tmp" \
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --self-test
```

Result: `PASS_SELF_TEST`; 32 negative mutations rejected.

The five tests include the existing tracked-evidence negative, the wrong-candidate/forged-output-hash negative, the new API mismatch/missing-path test, the launch/frozen-contract test, and the existing self-test check. The 32-mutation self-test retains the grade/no-drop/tracked/wrong-candidate coverage. No full 86-court, proof-gate full range, or 100k matrix was run.

## 4. Independent API/CLI probe

```sh
TMPDIR="$PWD/.../api-binding-recheck/tmp" PYTHONPATH="$PWD" \
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/api-binding-recheck/probes/api_binding_probe.py
```

Observed (`logs/api_binding_probe.json`):

```text
api_mismatch_junk_path       RED_INCOMPLETE; MCR_C_EVIDENCE_TEXT_PATH_MISMATCH
api_valid_external_pair      READY_FOR_INDEPENDENT_RECEIVING; errors=[]
api_missing_path             RED_INCOMPLETE; MCR_C_EVIDENCE_PATH_UNAVAILABLE + MCR_C_EVIDENCE_PATH_UNREADABLE
api_unreadable_directory     RED_INCOMPLETE; MCR_C_EVIDENCE_PATH_UNREADABLE
cli_positive_external        READY_FOR_INDEPENDENT_RECEIVING; exit 0
cli_junk_path                RED_INCOMPLETE; exit 2
```

The probe uses the existing synthetic focused fixture and the existing validator; no source, respondent, native, science or actor operation. The valid external pair is outside/untracked under the documented repository-tracking-only boundary, not a timestamp, signer or PR-origin proof.

## 5. Baseline RED at prerepair and fixed GREEN

The new test was run against the temporarily restored prerepair validator only (the test file remained the repaired version):

```sh
git show a5a635a^:CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  > CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py
python3 -B -m pytest -q ...::test_api_rejects_text_path_mismatch_and_unreadable_path
git checkout -- CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py
```

Prerepair validator: blob `1cdd3e70acd65b6056fd5a7a153c1aba33a7d26e`, file SHA `c0b8a53a3a0c7b64f3cb071c454cbbe29d5171156f7faff65fe1b2f6b3f5544a`.

Result (`logs/baseline_red_prerepair.log`):

```text
FAILED test_api_rejects_text_path_mismatch_and_unreadable_path
AssertionError: assert 'READY_FOR_INDEPENDENT_RECEIVING' == 'RED_INCOMPLETE'
```

This is the exact prerepair CCF5-R01 defect assertion. After restoring the repaired validator (file SHA `ea1edef4...`), the same test is fixed GREEN:

```text
1 passed in 0.69s
```

The worktree was clean except this review lease after restoration; no temporary fault remains.

## 6. Old negatives and boundaries

- Old tracked/wrong-candidate/forged-hash/grade/no-drop negatives are preserved through the existing five tests and the 32-mutation self-test.
- Prior wrapper/contract/original-preservation/scalar-composite/CLI/tracking qualifications are not reopened.
- No whole MCR, final code, economic/100k, final 12-ID same-head PASS, or postcommit external evidence block is accepted.
- External provenance remains repository-tracking-only; no signer, timestamp, PR-origin or stronger authority is invented.
- The final full code and economic receivers must still resume at the same immutable HQ-frozen candidate with all 12 obligations PASS, the SHA-bound external MCR evidence block after commit, `verifier --verify-return`, and all engineering/science/authority courts. Author ceiling remains `DELIVERED_PENDING_RECEIVING`; original35/source/science/actor/FF/N11/Sorok/protected merge remain held.
- No source/respondent/SAV/DTA/DB/native/science/actor operation, environment install, merge, new worker/engine/checker, or model/provider/account/effort change. Same existing OpenCode Go DeepSeek V4.1 Flash MAX session.

## 7. Review output hashes

```text
eea6b3c9fef88324a60b5e36a4bc4212c84dca17e2f0f3ae301128a2a009150c  00_REVIEW.md
227d13361453af0e332f47c953f82f2ca6f64ab2757210bbf6bcab2e0e190c68  FINDINGS.jsonl
df6a1c860bc313e110e168a81f794eccc7ba66c2b5f7b45f3cef19cf26f76911  probes/api_binding_probe.py
fbe8847e8062fdfc8e8fa050319ef7d71ee0aed91a6942dc65874da313b44b0e  logs/verifier_tests.log
68ea1f4af7ca16031af34f48d5e473bfa7c882d04a3b961739e6392e3a7fed44  logs/validator_self_test.log
8adee0b3838993f9b2e275ce13d92413f622487e3feca55be85a306cc1f68621  logs/api_binding_probe.json
c564ed54f5d1672c348cbc2e549bab7e372a7c0be0f654190bff3e0868b7be63  logs/baseline_red_prerepair.log
3b48e0860dc023141693c4f77181cda5b340fb20a1a3707eedab872d4f8fa2ba  logs/fixed_green_after_restore.log
```

**Final:** `ACCEPT_AT_CCF5_R01_SCOPE`; no whole-MCR/final-receiving acceptance.
