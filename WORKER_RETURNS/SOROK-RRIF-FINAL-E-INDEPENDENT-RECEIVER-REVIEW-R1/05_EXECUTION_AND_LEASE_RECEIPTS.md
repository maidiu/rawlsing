# Execution and lease receipts

## Identity and isolation

```text
Repository: maidiu/rawlsing
Review branch: review/sorok-rrif-final-e-exact-receiver-20261031-r1
Review worktree: /Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-rrif-final-e-review-20261031
Review base/dispatch: f136e9c397a457eecdc4e7c1f993ac1638529ba7
Code under review: 8d9585296ff264b947559f4a78f49f73ca45e53a
PRE-MAIN live head: 8e44ca9c751049d65e6def47600b5c073ee04b29
Host: oldMac, macOS 13.7.8 x86_64
Python: 3.11.3
Pytest: 9.1.1
Git: 2.39.1
Model: DeepSeek V4.1-Flash, MAX requested; actual provider effort UNKNOWN
Session id/url/title: UNKNOWN__OPERATOR_CONFIRMATION_REQUIRED
```

A separate detached PRE-MAIN worktree was created at
`/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/rrif-final-e-premain`
from `8e44ca9` and used only for staging. The author's `/private/.../rrif-final-e`
worktree was not used, modified, cleaned, reset or interrupted.

## Commands actually run

```sh
git worktree add --detach <premain-stage> 8e44ca9...
sh candidate/receiving_packet/apply.sh <premain-stage> candidate
git archive 598d9e9... SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2 | tar -x -C <premain-stage>
sh candidate/receiving_packet/apply.sh <premain-stage> candidate
PYTHONPATH=<candidate>:<review-repo> python3 candidate/run_courts.py
PYTHONPATH=<stage>:<premain-stage> python3 -m pytest <stage>/tests/test_join.py <stage>/tests/test_rrif_r2_c12.py
PYTHONPATH=<stage>:<premain-stage> python3 -m pytest <stage>/tests/test_rrif_e_repair.py
PYTHONPATH=<stage>:<stage>/rrif_r3_extension:<premain-stage> python3 -m pytest <stage>/rrif_r3_extension/tests/test_rrif_r3_extension.py
PYTHONPATH=<stage>:<stage>/rrif_r3_extension:<premain-stage> python3 <stage>/first_consumer_cli.py --root <tmp>
git status --short
```

## Results

```text
Candidate 20 R2 tests:             20 passed in 15.50s
Candidate 9 R3 tests:               9 passed in 8.59s
Candidate 6 R3/E repair tests:      6 passed in 3.70s
Candidate first consumer:           exit 0, PASS_PARTIAL...
Patch alone on absent base:         exit 2, RRIF_E_BASE_R2_MISSING
R2 stage base:                      459 files, 444 vendor rows, manifest 7cfcb467...
Patch on real R2 base:              exit 0, 466 files
Stage R2 tests:                     20 passed in 14.72s
Stage RRIF-E tests:                 collection ImportError c12_guard
Stage R3 tests:                     path missing
Stage first consumer:               exit 1, ImportError c12_guard
```

The actual code-under-review tests are valid; the actual receiving packet is
not. This is the independent receiver finding.

## Lease / safety

- Existing worktrees were enumerated before creating this one.
- No active worker lease was commandeered.
- No PRE-MAIN commit, source-owner branch, Programma, O-LIVE, Pyat, production DB
  or model/provider call was touched.
- No arbitrary historical or native survey/actor script was executed.
- The temporary staging worktree is disposable and contains no committed change.
- Rollback of this review is limited to the review-created candidate path and
  temporary worktrees; no `git clean -fd` in a shared checkout.

## Final remote SHA

The final review branch tip is recorded after ordinary non-force push and
`git ls-remote` readback in the terminal response. The content commit is
recorded separately from the follow-up readback commit.
