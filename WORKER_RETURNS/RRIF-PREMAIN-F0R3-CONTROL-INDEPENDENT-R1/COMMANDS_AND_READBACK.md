# Commands and readback

## Environment

- macOS local Git; Python 3.11.3.
- Local OpenCode / `opencode-go/deepseek-v4.1-flash`; MAX effort not independently observable.
- HQ dispatch: issue `#574`, exact authorized SHA `696fbf97cc1f9bab16daf2e5a9f6a6800b449130` (explicit HQ authorization; not inferred from HEAD).
- Exclusive worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/rrif-574-exclusive-20261031`.
- Local session branch: `rrif-session-574-20261031`; HEAD verified exactly at the dispatch SHA; worktree clean.
- Review branch: `review/pre-main-rrif-f0r3-control-gate-independent-20261031-r1`; remote head verified equal to the dispatch SHA before work.
- Earlier provisional work from the pre-amendment review worktree was preserved and copied into this exclusive worktree; nothing was reset or erased.
- No active worktree/session collision. No PR #519, PRE-MAIN, F4, progress pair or source owner was edited.

## Source readback

```sh
git ls-remote origin refs/heads/integration/pre-main-reconciliation-r1
# 8e44ca9c751049d65e6def47600b5c073ee04b29

git ls-remote origin refs/pull/519/head refs/pull/519/merge
# 59c9a7a4a4fae60d809c1ef545ff4e48906d0dd0 refs/pull/519/head
# 7abc24f2ec3884702d0bc41248ae13d7a367a6ae refs/pull/519/merge

git log -1 --format='%H%nparents %P%n%s' 7abc24f2
# 7abc24f2…; parents 299f41e9… 59c9a7a4…; "Merge 59c9a7a4 into 299f41e9"

git rev-parse 59c9a7a4:CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py
# 6fa0ce132e68f1fea7d67321129a2af2627a5d94
git rev-parse 59c9a7a4:CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/00_FROZEN_INITIAL_SEED.json
# 4ffe5f95b84505431a928f7ef6d0e7b5931f63d8
git rev-parse 59c9a7a4:CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/01_RETURN_EVENT_LOG.json
# 60fd8e26b3d8c4bd66f27900b82c9359cf4ad652
git rev-parse 59c9a7a4:CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/02_FLIGHT_AND_PR_REGISTER.json
# 9306df304a8f12029c8daacb2eb97c9fcb58df56
git rev-parse 59c9a7a4:.github/workflows/pre-main-branch-fanin-receipts.yml
# ce1ef40b5f2568c52a44d1ddc01a98647f3bf322
```

F0R3 candidate source/test blobs verified with `git hash-object`:

```text
verify_branch_fanin.py          2fc1c3c7ae6113d12b70abb655ff123a6ae9c895
verify_branch_fanin.py.patch    424d87370b0e5fdfad13705335558eff37be9257
test_f0r3_postseed_witnesses.py 80eaf4feaaa34760129c7efe3a4019f67465052a
reproduce_f0r3.py               d5ce55cbfbecf8f8da264977e9c365cd15d4f388
```

## Candidate execution

```sh
# current PR519 32/32 corpus, candidate validator
python3 current_head_59c9a7a4/verify_branch_fanin.py --selftest \
  --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54
# PASS sourcefree record integrity: 32 events and 32 flights; NO ADOPTION ALLOWED
# PASS: 20 mutation witnesses rejected + valid nonadopted owner-candidate stage

# original validator against the same current data
cd original
python3 verify_branch_fanin.py --selftest \
  --baseline-ref 299f41e97a43c67be9cc76a79fa49b48f4e12e54
# PASS sourcefree record integrity: 32 events and 32 flights; NO ADOPTION ALLOWED
# PASS: 13 mutation witnesses rejected + valid nonadopted owner-candidate stage

# candidate unittest
cd WORKER_RETURNS/PREMAIN-F0R3-POSTSEED-AUTHORITY-LOG-REPAIR-R1/candidate
python3 test_f0r3_postseed_witnesses.py
# Ran 12 tests ... OK
# PASS: 20 mutation witnesses rejected + valid nonadopted owner-candidate stage

# independent N1–N7 reproduction on current data
python3 reproduce_f0r3.py --data-dir current_head_59c9a7a4
# N1–N4, N6, N7 admitted by original and rejected by candidate
# N5 rejected by both (candidate adds append-reuse code)
# legal OWNER_ADOPTION_CANDIDATE accepted by both, adoption=false

# patch applicability against live PR519 source
cd .tmp-f0r3-review/applycheck
git init -q
git add CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/verify_branch_fanin.py
git commit -qm source
git apply --check verify_branch_fanin.py.patch
# exit 0
```

## Live protection readback

```sh
ghapi repos/maidiu/rawlsing/branches/integration/pre-main-reconciliation-r1
# protected: false; commit: 8e44ca9c…

ghapi repos/maidiu/rawlsing/rulesets
# []

ghapi repos/maidiu/rawlsing/branches/integration/pre-main-reconciliation-r1/protection
# 403 Resource not accessible by personal access token
ghapi .../protection/required_status_checks
# 403 Resource not accessible by personal access token
```

The 403 means this credential cannot verify installed required checks; it does not prove protection. The branch metadata `protected=false` and empty rulesets are direct.

## Other currentness

```sh
git show 8e44ca9c:SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md | head -3
# revision36
git show 8e44ca9c:SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json
# revision 35
git merge-base --is-ancestor 9fb7caeb 8e44ca9c; echo $?
# 1 (not an ancestor)
```

F0R3's observed governed run 41082521136 (144 pass / 3 fail) is attributed, not rerun: the Actions API returned 403 for this credential. It is separate from the receipt-contract job.

## Return artifacts

`WORKER_RETURNS/RRIF-PREMAIN-F0R3-CONTROL-INDEPENDENT-R1/`
- `00_RETURN.md`
- `PR519_HEAD_AND_CANDIDATE_PATCH.md`
- `INDEPENDENT_NEGATIVE_WITNESSES.md`
- `ADMIN_PROTECTION_AND_OWNER_CAS_GATES.md`
- `EXACT_REMAINING_OWNER_ACTIONS.md`
- `COMMANDS_AND_READBACK.md`

The exact final remote return SHA is reported after push and direct `ls-remote` readback; it is not self-embedded. No self-adoption or model switch.
