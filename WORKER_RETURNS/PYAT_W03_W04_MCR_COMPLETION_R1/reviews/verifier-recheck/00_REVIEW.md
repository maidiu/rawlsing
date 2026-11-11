# CC-F05 verifier/artifact focused recheck

**Review:** independent focused CC-F05 verifier/artifact review only.
**Exact worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1`
**Branch/head:** `review/pyat-w03-w04-verifier-focused-recheck-r1` at `6658b630f114186099177cbdaf00cab854b18b09`; source tree 406 files, clean.
**Verdict:** **`REVISE` at CC-F05 scope**, for one precise API binding defect. The wrapper/launch, CLI, original-contract preservation, scalar/composite identity correction, tracking negative checks, and existing checker tests otherwise pass at this scope. No whole 12-ID or economic acceptance.

## 1. Sources and exact reviewed blobs

- Original combined review: `07c172683c4a720b8d1c37599c3e09a5357e56d8`, CC-F05.
- Frozen commission: `PYAT_W03_W04_MCR_C_Commission.md`, SHA-256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`; byte-identical to the intake (`git diff 26f70635e...HEAD -- PYAT...` is empty).
- Verifier author candidate: `df32985387da3da26f587ddbcd75ad031b837773`; integrated `09f97a3a4c77ed7666ee95af586cfdfd91493f73`; current head `6658b630f...`.
- Reviewed blobs:
```text
1cdd3e70acd65b6056fd5a7a153c1aba33a7d26e  CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py
6994a3356d0c62e34fcf9c5c184a299fa97fd185  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
b30926e911b9ccdc4b86e23e76ed9a4c08d2a2a2  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
47faaf3d115c213de2319f8123d4ac17d4d1cf8e  PYAT_W03_W04_MCR_C_Commission.md
```
- Read: frozen commission/12-ID TSV, runtime selection, `MCR_EXECUTABLE_LAUNCH.md`, VERIFIER_R1 return/tests/logs/boundary, and the exact validator diff. Runtime selection is the existing `opencode-go/deepseek-v4.1-flash#max`; wrapper addendum records it without contract changes. No model/provider/account/effort change.

## 2. What passes

### 2.1 Frozen contract and executable wrapper

- Original frozen file remains byte-identical and still returns the historical RED:
```text
RED_INVALID_FOR_DISPATCH: REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK
```
- The wrapper `MCR_EXECUTABLE_LAUNCH.md` has a single fenced launch prompt and passes the existing checker:
```text
PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH
mcr_completion_contract_sha256 = 1e7d6a905bb702c289708d636627625759cee38f883851c60a502126f5b47583
mcr_required_obligation_count = 12
```
- The wrapper's extracted MCR block is **byte-for-byte identical** to the original frozen block (`1e7d6a90...` in both); 1 scope, 12 obligations, 1 receiving record. Sources, grades, no-drop text, and receiving requirements are preserved. The original `no_drop_check` text is preserved inside the block; the addendum provides the corrected executable command. No new obligation, grade, source, signer, approval gate or authority was added.
- The author's original literal command remains RED; it is not relabeled as fixed. The wrapper is the corrected presentation and is separately validated.

### 2.2 Evidence API/CLI negatives and identity correction

Using the author's synthetic focused fixture plus the existing validator (no new checker):

- CLI positive external evidence: `READY_FOR_INDEPENDENT_RECEIVING`, exit 0.
- CLI tracked-at-candidate evidence: `RED`, exit 2, `MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE`.
- CLI path/text mismatch (external file containing junk): `RED`, exit 2; the CLI reads the supplied path and therefore binds text to that path.
- API direct tracked evidence: RED; API symlink-to-tracked evidence: RED (`MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE`).
- API missing proof ID: RED (`MCR_C_MISSING_PROOF_OBL-B`); extra proof ID: RED (`MCR_C_UNCONTRACTED_PROOF_OBL-EXTRA`); bad grade: RED (`MCR_C_INSUFFICIENT_EVIDENCE_GRADE_OBL-A`); no evidence path: RED (`MCR_C_EVIDENCE_EXTERNALITY_UNVERIFIED`).
- Author's new 4 tests pass; existing self-test passes 32 negative mutations.
- The scalar identity correction is correct for the actual frozen TSV enumerator: `_expected_id_set` returns 12 raw IDs exactly equal to `cut -f1` (`scalar_set_matches_tsv_cut=true`, no JSON brackets). The `len(cols)>1` branch is unchanged and still returns canonical JSON composite identities; a synthetic two-column check returns `["A1","B1"]`/`["A2","B2"]`. Old checker negatives remain green.

### 2.3 Tracking boundary

The author correctly distinguishes repository tracking exclusion from wall-clock/PR provenance. `_evidence_externality` marks `REPOSITORY_TRACKING_ONLY__NO_TIMESTAMP_OR_STRONGER_PROVENANCE`. A copy outside the candidate root is accepted as external under this tracking-only rule; that is a documented residual, not a timestamp/provenance claim. A symlink resolving to tracked candidate evidence is rejected. No new signer or approval gate was invented.

## 3. Finding requiring repair

### CCF5-R01 (P2) — `verify_return` API does not bind `returned` text to `returned_path`

**Location:** `CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py:331-340, 716-720`.

`verify_return(commission, returned, candidate_sha, root, *, returned_path=None)` checks that `returned_path` is external/untracked, but it validates the separately supplied `returned` text and never reads or compares `returned_path` contents. Independent probe:

```python
# returned = valid evidence text; returned_path = external file containing junk
validator.verify_return(commission, evidence_text, candidate, repo, returned_path=junk_external)
# -> READY_FOR_INDEPENDENT_RECEIVING, errors=[]
```

Thus the API can claim external evidence using an arbitrary external path while the text is unrelated to it. The CLI is correct because `main()` reads `args.verify_return.read_text()` and passes that path; the CLI junk-path case is RED. The 4 focused tests pass because they use a consistent external text/path pair and do not test this mismatch.

**Minimum exact repair:** in `verify_return`, read `returned_path` and require its text to equal `returned` (or simplify the API to accept only `returned_path` and derive the text), adding a `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH`/equivalent RED error. Add one focused test with valid evidence text + an external junk path. Do not weaken the existing tracked/wrong-candidate/forged/digest/no-drop/grade checks, add a new signer, or create a new checker. The CLI already binds; no wrapper/contract change is needed.

## 4. Residual and boundary

- **CC-F04 full-range proof gate:** the author verifier range passes the existing proof-integrity gate (`MECHANICAL_PROOF_GATE_PASS`; no sidecar for the new verifier test). A full `26f70635e..6658b630f` proof-gate run still flags the pre-existing benchmark integration test missing its sidecar; that is the queued CC-F04 bench-owner residual, not a new verifier-test waiver. It was not reopened or fixed here.
- **External boundary:** repository tracking only; no wall-clock/PR origin; copies outside candidate are accepted under that documented rule. This is a qualified residual, not a stronger assurance.
- **No whole acceptance:** no final `RECEIVING_EVIDENCE.md`, delivered IDs, 12 same-head PASS records, final postcommit block, whole 12-ID, economic/100k, original35/SAV/DTA/DB/source bytes, native/S3/science/actor effect, install, protected merge, CI waiver, new engine/worker, or model/provider/account/effort change. Prior W04 F01/F02/F03 and CC-F01 are already accepted and were not reopened. CC-F02 economic-method work and CC-F03/F04 remain outside this lease; final both receivers must share the final immutable code/economic SHA with full 12/external proof.

## 5. Review output and commit

Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/verifier-recheck/`. All production/test/contract/HQ files are read-only. Actual model is the existing OpenCode Go DeepSeek V4.1 Flash MAX; no change.

**Final:** `REVISE` at CC-F05 scope solely for CCF5-R01; wrapper/CLI/original-preservation/scalar-composite identity and external-tracking boundary pass at this scope; no whole MCR or economic acceptance.
