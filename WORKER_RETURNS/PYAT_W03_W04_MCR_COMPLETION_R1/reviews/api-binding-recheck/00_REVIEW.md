# CCF5-R01 API-binding recheck

**Verdict:** `ACCEPT_AT_CCF5_R01_SCOPE`

This is a finite narrow recheck of the new API-binding repair only. It completes the exact residual left by the focused CC-F05 review `f250bded334fd7a300113e7b9a9118f841e597d4` (`REVISE` solely for CCF5-R01). It is **not** a whole-MCR, final-code, economic/100k, or final-receiving acceptance.

## Exact source and reviewed identity

- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-engineering-review-r1`
- Branch: `review/pyat-w03-w04-api-binding-recheck-r1`
- Exact reviewed source: `a5a635a794aa701cde0b7d7b3b6c0708c76288b2`
- Author repair commit: `cd98ba7ee1d96cef842663c13eac594c90542525` (`Bind verifier returned text to supplied evidence path`)
- Prerepair parent: `a5a635a^` (the temporary baseline RED used the parent validator blob only; restored before commit)
- Frozen commission: `PYAT_W03_W04_MCR_C_Commission.md` SHA-256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`
- Frozen 12-ID TSV: `WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv` SHA-256 `5de8d68207de353926bd2d42095a8c8c44a36b06ac4038a7c9b16a1b6173428e`; 12 rows; freeze source `5a891a311c70f4cb8c09864008b33405362f7c7c`
- Launch wrapper: `WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md` SHA-256 `c25dbb96259971a8f623179dd1435bcdc2d684edb2b02a4970565bbb0c5c25e7`
- No diff to the frozen commission, 12-ID TSV, or launch wrapper in the repair (`git diff --quiet a5a635a^ a5a635a -- ...` empty).

Reviewed code/test blobs at `a5a635a`:

```text
d1db88c62bda848aee478e13120393153d5a61bf  CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py
ea1edef49b0f11bcc36e45d6cf9f59fdfc1d2fac9684b920df6aa6d9dcb7218a  (file SHA-256)
5b0f1ce787a6d9e6a8c003fa99bef434213ffaa7  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
7b476487f0773a6e129a443f8975b98105985f3d4e66f7185cc764bf1617ccf6  (file SHA-256)
```

The prerepair validator file was temporarily restored from the parent only for the baseline RED test; its hash was `c0b8a53a3a0c7b64f3cb071c454cbbe29d5171156f7faff65fe1b2f6b3f5544a` and the repaired file was restored to `ea1edef4...` before any commit. The worktree is clean except this review lease.

## Residual and repair

The prior independent counterexample is retained: at prerepair, valid evidence text plus an external junk path returned `READY_FOR_INDEPENDENT_RECEIVING` with `errors=[]` because `verify_return` checked the path only for external/untracked status and never compared the path text to the separately supplied `returned` text. The CLI was already bound because `main()` reads the path.

The repair adds exactly eight lines to `verify_return`: when `returned_path` is supplied, it reads the path text, requires exact equality with `returned`, and appends `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH` on inequality; read failures append `MCR_C_EVIDENCE_PATH_UNREADABLE`. The existing `_evidence_externality` still adds `MCR_C_EVIDENCE_PATH_UNAVAILABLE` for missing paths. The public signature is unchanged:

```text
def verify_return(commission, returned, candidate_sha, root, *, returned_path: Path | None = None):
```

The test diff adds one focused test (`test_api_rejects_text_path_mismatch_and_unreadable_path`), 21 lines, no deletions; no existing test assertion was changed.

## Independent re-execution

### Existing tests and self-test

```text
5 passed in 1.99s
PASS_SELF_TEST; 32 negative mutations rejected
```

The five tests include the existing tracked-evidence negative, wrong-candidate/forged-output-hash negatives, the new API mismatch/missing-path test, the launch/frozen-contract test, and the existing self-test check. The self-test covers the no-drop/grade/tracked/wrong-candidate negative mutation set at the existing scope; no full suite or proof-gate matrix was repeated.

### API/CLI probe (synthetic existing fixture, no source/respondent data)

| Case | Observed |
|---|---|
| API valid text + external junk path | `RED_INCOMPLETE`, `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH` |
| API valid text + valid external path | `READY_FOR_INDEPENDENT_RECEIVING`, `errors=[]` |
| API missing path | `RED_INCOMPLETE`, `MCR_C_EVIDENCE_PATH_UNAVAILABLE` + `MCR_C_EVIDENCE_PATH_UNREADABLE` |
| API unreadable directory path | `RED_INCOMPLETE`, `MCR_C_EVIDENCE_PATH_UNREADABLE` |
| CLI valid external path | `READY_FOR_INDEPENDENT_RECEIVING`, exit 0 |
| CLI junk path | `RED_INCOMPLETE`, exit 2 |

The added test covers the mismatch and missing-path cases plus restoration with the valid external pair. The truly unreadable path is independently exercised with a directory path and also fails closed with the new `UNREADABLE` error; this is a test-coverage observation, not a behavior gap.

### Baseline RED and fixed GREEN

The new test was run against the temporarily restored prerepair validator (blob `1cdd3e70a`, file SHA `c0b8a53a...`):

```text
FAILED test_api_rejects_text_path_mismatch_and_unreadable_path
AssertionError: assert 'READY_FOR_INDEPENDENT_RECEIVING' == 'RED_INCOMPLETE'
```

This is the exact prerepair defect assertion. After restoring the repaired validator (`ea1edef4...`):

```text
1 passed in 0.69s
```

The repaired API therefore produces the expected fixed GREEN on the same test. No assertion was weakened; the prerepair run fails on the intended mismatch assertion, not on fixture construction.

## Scope findings

- **CCF5-R01 is closed at this scope.** The API now reads the supplied path and requires exact text equality; valid external pairs remain READY, mismatched/unreadable/missing paths fail closed.
- The five-test suite and self-test 32-negative set are green; the old tracked/wrong-candidate/forged-hash/grade/no-drop negatives remain preserved at the existing tested scope.
- The frozen commission, 12-ID TSV, launch wrapper, source tuples, grades, no-drop text and receiving requirements are unchanged. Prior CC-F05 wrapper/contract/original-preservation/scalar-composite/CLI/tracking qualifications are not reopened.
- Repository-tracking-only remains the exact external boundary: the valid external pair is outside/untracked, not a timestamp, signer or PR-origin proof. No new signer, authority, approval gate or provenance claim is invented.

## Limits

This verdict does not accept whole MCR, final code, economic/100k, or any missing 12-ID proof. The final full-code and economic receivers must still resume at the same immutable HQ-frozen candidate with all 12 obligations PASS, the SHA-bound external MCR evidence block after commit, `verifier --verify-return`, and all engineering/science/authority courts. The author ceiling remains `DELIVERED_PENDING_RECEIVING`; original35/source/science/actor/FF/N11/Sorok/protected merge remain held. No source/respondent/SAV/DTA/DB/native/science/actor operation, install, merge, new worker/engine/checker, or model/provider/account/effort change was performed. Same existing OpenCode Go DeepSeek V4.1 Flash MAX session; no change.

## Evidence files

- `FINDINGS.jsonl` — recheck, baseline RED, and boundary records.
- `02_COMMANDS_AND_EVIDENCE.md` — exact commands, blob/hash restoration, results.
- `logs/verifier_tests.log`, `logs/validator_self_test.log`, `logs/api_binding_probe.json`, `logs/baseline_red_prerepair.log`, `logs/fixed_green_after_restore.log`.
- `probes/api_binding_probe.py` — independent synthetic probe using the existing fixture/validator.

**Final:** `ACCEPT_AT_CCF5_R01_SCOPE`; no whole-MCR or final-receiving acceptance.
