# F0R4 — validator patch and CI receipts

**Candidate validator:** `WORKER_RETURNS/F0R4-R4/candidate/verify_branch_fanin.py`
**Candidate blob:** `2fc1c3c7ae6113d12b70abb655ff123a6ae9c895`
**Candidate patch:** `WORKER_RETURNS/F0R4-R4/candidate/verify_branch_fanin.py.patch`
**Patch blob:** `424d87370b0e5fdfad13705335558eff37be9257`
**Source validator:** `6fa0ce132e68f1fea7d67321129a2af2627a5d94`
**Live PR #519 head:** `59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0`

## 1. Patch application receipt

The F0R3 patch applies to the exact live source validator and produces the exact candidate validator:

```text
git apply --check candidate/verify_branch_fanin.py.patch   # exit 0
git apply candidate/verify_branch_fanin.py.patch           # exit 0
git hash-object CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py
# 2fc1c3c7ae6113d12b70abb655ff123a6ae9c895
```

The patch changes only `verify_branch_fanin.py`. It adds the F0R3 fail-closed controls for post-seed source authority, scientific/authority promotion, reviewer target returned-only, PR remote status, append SHA reuse and PR append order. It does not change the seed, event log, flight register, workflow, PR #519 or any original source.

## 2. Candidate selftest receipts

### Current live 32/32 data (`59c9a7a4...`)

```text
cd candidate/current_head_59c9a7a4
python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54
# exit 0
# First install: EVENT baseline missing; candidate seed source is separately frozen, owner approval still PENDING
# First install: FLIGHT baseline missing; candidate seed source is separately frozen, owner approval still PENDING
# PASS sourcefree record integrity: 32 events and 32 flights; NO ADOPTION ALLOWED
# PASS: 20 mutation witnesses rejected + valid nonadopted owner-candidate stage
```

### Sealed 19/19 data (`342164...`)

Same command in `candidate/sealed_342164`; exit 0; `19 events and 19 flights`; `PASS: 20 mutation witnesses rejected + valid nonadopted owner-candidate stage`.

The logs are preserved as `evidence/f0r4_candidate_current_selftest.log` and `evidence/f0r4_candidate_sealed_selftest.log`.

## 3. Independent twenty-witness harness

`candidate/f0r4_twenty_witness_run.py` does not call the validator's own selftest. It applies each mutation to a deep copy, calls `validate()`, and checks the expected error family.

| Data cut | Candidate `2fc1c3...` | Original `6fa0ce...` |
|---|---|---|
| Current 32/32 | 20/20 expected rejections (`W1–W5,B1–B8,N1–N7`); no admissions; legal nonadopted candidate accepted; exit 0 | 13/13 original expected rejections; `N1,N2,N3,N4,N6,N7` admitted; `N5` rejected only by the old flight-SHA mismatch; exit 0 report-only |
| Sealed 19/19 | 20/20 expected rejections; no admissions; legal nonadopted candidate accepted; exit 0 | same old-13 behavior and six admissions |

The old validator has no `APPEND_REUSES_PRIOR_IMMUTABLE_SHA` result; its `N5` rejection is an incidental `FLIGHT_LOG_EXACT_SOURCE_MISMATCH_F0-RETURN-20261029`. The candidate rejects `N5` with the intended append-reuse error.

Machine-readable harness outputs:

- `evidence/f0r4_candidate_current_32.json`
- `evidence/f0r4_candidate_sealed_19.json`
- `evidence/f0r4_original_current_32.json`
- `evidence/f0r4_original_sealed_19.json`

## 4. Seed and currentness

The frozen seed blob `4ffe5f95...` has 11 events, 11 workers and 4 PRs. Direct comparison against the live 32-event / 32-worker / 5-PR control data confirms the first 11 events, 11 workers and 4 PRs are byte-equal parsed records. This is prefix equality, not owner approval; `owner_approval_status` is still `PENDING`.

## 5. CI source and actual exits

The candidate CI source is `candidate/ci/run_f0r4_ci.sh`. It runs the candidate selftest on both snapshots, checks for `PASS: 20 mutation witnesses` and `"all_expected": true`, and exits 0.

```text
WORKER_RETURNS/F0R4-R4/candidate/ci/run_f0r4_ci.sh   # exit 0
# PASS sourcefree record integrity: 32 events and 32 flights; NO ADOPTION ALLOWED
# PASS: 20 mutation witnesses rejected + valid nonadopted owner-candidate stage
# PASS sourcefree record integrity: 19 events and 19 flights; NO ADOPTION ALLOWED
# PASS: 20 mutation witnesses rejected + valid nonadopted owner-candidate stage
# PASS F0R4 candidate 20-witness CI
```

Log: `evidence/f0r4_ci_run.log`.

**Existing workflow:** `.github/workflows/pre-main-branch-fanin-receipts.yml` at blob `ce1ef40b...` already runs `verify_branch_fanin.py --selftest --baseline-ref 299f...`. When the exact validator patch is applied, the existing command exercises the 20-witness suite. No workflow YAML change is required for the count. The owner must apply the validator patch and obtain a real required CI run at the exact patched head.

**Candidate CI on GitHub:** `NOT_RUN`. The patch is not applied to PR #519 and no candidate PR was created. The local exact-equivalent script exit 0 is not a hosted required-check receipt.

## 6. Old live CI is not 20-witness CI

The live receipt job on `59c9a7a4...` is:

- run `41082520979`, job `124155062531`, conclusion `success`;
- command `python3 CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py --selftest --baseline-ref 299f41...`;
- stdout `PASS: 13 mutation witnesses rejected + valid nonadopted owner-candidate stage`.

That is the old 13-witness suite. It is explicitly **not** evidence for N1–N7. The current live original validator admits N1–N4 and N6–N7 on the same 32/32 data, and rejects N5 only incidentally by the old flight mismatch.

The separate governed job remains run `41082521136`, **3 failed / 144 passed**, with the same FIABC identity/packaging assertions. It is a separate original-owner issue and was not weakened.

## 7. Replay commands

```bash
cd WORKER_RETURNS/F0R4-R4/candidate
./ci/run_f0r4_ci.sh

# Individual current-head replay
cd current_head_59c9a7a4
python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54

# Individual sealed replay
cd ../sealed_342164
python3 verify_branch_fanin.py --selftest --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54

# Independent harness (candidate and old)
cd ..
python3 f0r4_twenty_witness_run.py --validator verify_branch_fanin.py \
  --control-dir current_head_59c9a7a4 --expect candidate
python3 f0r4_twenty_witness_run.py --validator verify_branch_fanin.py \
  --control-dir sealed_342164 --expect candidate
```

Expected candidate exits are 0. The old validator report-only exits are 0 with six admitted IDs and one incidental error.

## 8. No source mutation

No PR #519, workflow, seed, event log, flight register, PRE-MAIN, QF2/F4 or original source was changed. The patch and snapshots are under the F0R4 return tree only. The candidate is ready for owner-authorized application and distinct review, not for merge.
