# CC-F05 verifier/artifact recheck — commands and evidence

**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1`
**Branch:** `review/pyat-w03-w04-verifier-focused-recheck-r1`
**Reviewed head:** `6658b630f114186099177cbdaf00cab854b18b09`
**Verdict:** `REVISE` at CC-F05 scope, solely for CCF5-R01 API path/text binding.

All commands used an explicit `cd` into this worktree. Production/test/contract/HQ were read-only. Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/verifier-recheck/`.

## 1. Worktree and source identity

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1
git branch --show-current
git rev-parse HEAD
git status --short
git ls-tree -r --name-only HEAD rawlsing_next | wc -l
find rawlsing_next -type f | wc -l
```

Result:

```text
review/pyat-w03-w04-verifier-focused-recheck-r1
6658b630f114186099177cbdaf00cab854b18b09
clean before this review lease
406
406
```

Reviewed blobs:

```text
1cdd3e70acd65b6056fd5a7a153c1aba33a7d26e  CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py
6994a3356d0c62e34fcf9c5c184a299fa97fd185  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
b30926e911b9ccdc4b86e23e76ed9a4c08d2a2a2  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
47faaf3d115c213de2319f8123d4ac17d4d1cf8e  PYAT_W03_W04_MCR_C_Commission.md
```

Author candidate: `df32985387da3da26f587ddbcd75ad031b837773`; integrated: `09f97a3a4c77ed7666ee95af586cfdfd91493f73`; prior review: `07c172683c4a720b8d1c37599c3e09a5357e56d8`.

## 2. Frozen contract and wrapper

```sh
git diff --quiet 26f70635e8493c7759fa087b17da269104bd8922..HEAD -- PYAT_W03_W04_MCR_C_Commission.md
shasum -a 256 PYAT_W03_W04_MCR_C_Commission.md
python3 -B CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py PYAT_W03_W04_MCR_C_Commission.md
python3 -B CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
```

Result:

- frozen file diff empty; SHA-256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`.
- Original literal command: exit 2, `RED_INVALID_FOR_DISPATCH: REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK`; preserved historical RED, not relabeled.
- Wrapper: exit 0, `PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH`; 12 obligations; contract hash `1e7d6a905bb702c289708d636627625759cee38f883851c60a502126f5b47583`.
- Extracted original/wrapper MCR blocks are byte-identical (`blocks_equal=true`); 1 scope/12 obligations/1 receiving. Runtime addendum records the same `opencode-go/deepseek-v4.1-flash#max`; no new obligation/source/grade/no-drop/receiving requirement/signature/approval gate.

Logs: `logs/frozen_contract_red.log`, `logs/launch_validate.log`, `logs/contract_identity_scalar.log`.

## 3. Scalar and composite identity

Actual frozen TSV (source at `5a891a...`) was read through the existing validator:

```text
contract_scope = 12
contract_obligations = 12
expected_scalar_ids_count = 12
scalar_set_matches_tsv_cut = true
scalar_ids_have_no_json_brackets = true
```

A synthetic two-column source check for the unchanged composite branch:

```text
columns ["a"]   -> ["A1","A2"]
columns ["a","b"] -> ["[\"A1\",\"B1\"]","[\"A2\",\"B2\"]"]
```

Logs: `logs/contract_identity_scalar.log`, `logs/composite_scalar_branch.log`. The single-column correction matches the actual frozen enumerator and preserves old composite JSON semantics; self-test 32 negative mutations remains green.

## 4. Existing tests and self-test

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/$OUT/tmp" python3 -B -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
```

Result: **4 passed in 1.19s**.

```sh
python3 -B CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --self-test
```

Result: `PASS_SELF_TEST`; 5 positive kinds; 32 negative mutations rejected.

Logs: `logs/verifier_tests.log`, `logs/validator_self_test.log`.

## 5. API/CLI evidence binding probe

Synthetic temporary Git repository using the author's focused fixture and existing validator; no source/respondent/native/science/actor operation.

```sh
TMPDIR="$PWD/$OUT/tmp" PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 \
python3 -B "$OUT/probes/verifier_probe.py"
```

Key results (`logs/verifier_probe.stdout.json`):

```text
CLI positive external evidence       READY_FOR_INDEPENDENT_RECEIVING; exit 0
CLI tracked candidate evidence       RED_INCOMPLETE; exit 2; MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE
CLI external junk path/text mismatch RED_INCOMPLETE; exit 2
API tracked                          RED; MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE
API symlink-to-tracked               RED; MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE
API no path                          RED; MCR_C_EVIDENCE_EXTERNALITY_UNVERIFIED
API missing proof ID                 RED; MCR_C_MISSING_PROOF_OBL-B
API extra proof ID                   RED; MCR_C_UNCONTRACTED_PROOF_OBL-EXTRA
API bad grade                        RED; MCR_C_INSUFFICIENT_EVIDENCE_GRADE_OBL-A
API copy outside candidate           READY under repository-tracking-only boundary
API path/text mismatch               READY_FOR_INDEPENDENT_RECEIVING; errors=[]
```

The CLI reads `--verify-return` text and passes that path, so it is bound. The public API does not read or compare `returned_path` to the supplied `returned` text. This is CCF5-R01.

## 6. Proof-integrity gate

```sh
python3 -B CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py lint \
  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
python3 -B CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base df32985387da3da26f587ddbcd75ad031b837773^ \
  --head df32985387da3da26f587ddbcd75ad031b837773 --root .
```

Result: lint `AST_LINT_PASS`; author repair range `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION` with 0 witness contracts. No verifier-test sidecar is required or waived.

A broader `26f70635e..6658b630f` proof-gate run remains RED only on the pre-existing `rawlsing_next/tests/test_bench_w03_w04_physical.py` missing its `.proof.json`; that is CC-F04 queued to the bench owner, not a verifier-test waiver. Logs: `logs/proof_gate_lint_verifier.log`, `logs/proof_gate_changed_verifier_author.log`, `logs/proof_gate_changed_verifier.log`.

## 7. Boundary and hashes

- No final `RECEIVING_EVIDENCE.md`, delivered IDs, 12 same-head PASS package, final postcommit block, whole 12-ID/economic/100k, original35/SAV/DTA/DB/source bytes, native/S3/science/actor effect, install, protected merge, CI waiver, new engine/worker, model/provider/account/effort change. Prior W04 F01/F02/F03 and CC-F01 are accepted and not reopened. CC-F02/CC-F03/CC-F04 remain outside this lease.
- External provenance is repository-tracking-only; copy outside candidate is accepted by that rule; wall-clock/PR origin remains unproven. This is documented residual, not an invented assurance.
- `logs/review_hashes.log` records SHA-256 of this review, findings, probes/logs and exact source/test blobs.

**Final:** `REVISE` at CC-F05 scope solely for CCF5-R01; wrapper/contract/CLI/scalar/composite/tracking negatives pass at this scope. No whole MCR or economic acceptance.
