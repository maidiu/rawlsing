# JOIN-V adjudication — shared-lineage repair 49022f6

**STATUS:** `LINEAGE_FINAL_REVISE__49022f6__INVALID_FORK_PARTIAL_BRANCH_LEAK__AWAIT_NEXT_REPAIR_SHA`
**REVIEWED SHA:** `49022f693c99b6cb58226513f8bad71c26bdac3c`
**PREVIOUS:** `75a134ed733acaed2c62ea3421b54fcb09c5442f` (REVISE)
**BRANCH:** `codex/sorok-join-v-20261022`
**WRITE SCOPE:** own return only. No candidate/J/E edit.

## Verdict

The shared `joined/lineage.py` contract works for the requested positive and hostile transitions:

- fork receipts in both `JoinedSession` and `RefusalSession` match the actual created branch rows, including non-null `fork_clock`, `root_hash` and `created_clock`;
- metadata-only switches to parent `first_session`, sibling `alt`, and root are refused with `UNAUTHORIZED_BRANCH`/`BRANCH_LINEAGE_MISMATCH`, without product mutation;
- legitimate nested forks `first_session -> alt -> alt2` persist, cold-reopen on `alt2`, and leave the parent untouched;
- missing/tampered receipt chains and duplicate forks are refused without mutation;
- the 30/30 preserved reviewer tests pass; the candidate's own suite is 17/17; inherited J/E/R30A are 8/8, 15/15, 10/10; the source manifest is 444/444.

One exact partial-failure remains: `fork_alt("")` is refused, but the failed request leaves an empty `''` branch in the C12 store in **both** paths. The session metadata remains on `first_session`, but the store now contains a branch that no legitimate lineage selected.

**Verdict: REVISE.** One small atomicity repair remains: validate the requested branch name before calling `product.fork`, or remove the created branch on lineage failure. Preserve the passing shared-lineage behavior.

## Exact reproducer

```text
before: ['first_session', 'root']
call:   session.fork_alt('')
raise:  SessionRefusal('FORK_REFUSED', 'ValueError:FORK_NEW_BRANCH_INVALID')
after:  ['', 'first_session', 'root']
session metadata: branch_id='first_session', branch_lineage unchanged
```

Observed on both `JoinedSession` and `RefusalSession`. The request is refused but the product store is mutated (orphan empty branch), so invalid requests do not preserve consistent state. New test: `test_invalid_empty_fork_is_atomic`.

## Coverage

| Claim | Status |
|---|---|
| Shared lineage contract loaded by both sessions | PASS |
| Fork receipt clock/root/created fields match branch rows | PASS |
| Parent/sibling/root metadata switches refused | PASS |
| Nested forks persist and cold-reopen correctly | PASS |
| Parent isolation across nested forks/cold reopen | PASS |
| Missing/tampered receipt chains refused without mutation | PASS |
| Duplicate fork refused without mutation | PASS |
| Invalid empty fork is atomic | **FAIL** (empty branch remains) |
| Rejected metadata operations do not mutate product/donor | PASS |
| Preserved 30/30 reviewer tests | PASS |
| Candidate own 17 tests | PASS |
| Inherited J / E / R30A | PASS (8/8, 15/15, 10/10) |
| Nonmutating targetless cold reopen | PASS |
| No fabricated target/native grant | PASS |
| Source/C12/C8 binding | PASS |
| Privacy, attention, joined encounter | PASS |
| B-source proof | PASS_SCOPED receiving-edge only; not original pre-C8 severance |
| Old E-first-refusal expectation | historical/superseded by J closure |

## Exact results

| Suite | Result |
|---|---|
| Frozen positives | 10/10 passed |
| Frozen hostiles | 7/7 passed |
| Repaired-cut tests | 9/9 passed |
| Targetless-final tests | 4/4 passed |
| **30/30 preserved reviewer executions** | **independently reproduced** |
| New lineage-contract tests | 4/5 passed; 1 failed |
| Targeted c367 | 5/6; one historical E-first expectation |
| Candidate own suite | 17/17 passed |
| Source manifest | 444/444 verified |

New targeted test that fails: `test_invalid_empty_fork_is_atomic`. The other four new lineage tests pass: nested forks/receipts/cold parent isolation; parent/sibling/root metadata switches; missing/tampered receipts; duplicate fork.

## Source and test hashes

- Candidate: `49022f693c99b6cb58226513f8bad71c26bdac3c`.
- `joined/lineage.py`: `1c91852f934be58eb6c0250debbc615471469e4bf23a9c80b6d60deaa9308823`.
- `joined/session.py`: `f11e872dbe482b4e99fe93f2df6d86ca8f1803978c6ff1087a9cd00ff991361b`.
- `joined/refusal.py`: `0056dc54020044356f2fd572ebe7cc239c3d9ce029ddd219ca7726d7aff2a1e5`.
- `tests/test_join.py`: `08badee030b46b41d3cc2cf0cfe06686975f2937465102d359155bc31fb781f0`.
- New lineage test: `tests/test_join_v_lineage_contract.py` hash `79fc117a21243e0f3d0c6316d95365244158d07787f8308eafa82741651e8751`.
- Repaired-cut test hash: `8a7ce8e61253ce6adb9286a4fb44f8ff26a7c851a28738fbacbe06df309f1028`.
- Targetless-final test hash: `f5411af4191188f0391dda2019225ab2856c798b2b5d101f2f66f4308473da66`.
- Targeted c367 hash: `6e2f87d773090235a4a5f3567430737f30f16698397c852f799585ff73280de1`.
- Frozen hashes unchanged/verified; `SOURCE_MANIFEST.json` 444/444; no vendor edits.

## Exact commands

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<49022f6 worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py tests/test_join_v_hostile.py tests/test_join_v_repaired_cut.py tests/test_join_v_targetless_final.py -p no:cacheprovider
30 passed

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py -p no:cacheprovider --tb=short
5 passed, 1 failed (historical E-first-refusal expectation)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_lineage_contract.py -p no:cacheprovider --tb=short
4 passed, 1 failed

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_lineage_final.py
candidate own 17/17; inherited 8/8, 15/15, 10/10; manifest 444/444
```

Evidence: `evidence/lineage_final/results.json`, `evidence/lineage_final/source.json`, and `evidence/lineage_final/*.xml`.

## Courts

| Court | Verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `REVISE` | Shared lineage, nested forks, switch rejection, receipt tamper/duplicate handling and 30/30 preserved tests pass; invalid empty fork leaks an orphan empty branch. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | B-source remains bounded receiving-edge; no original pre-C8 severance, acquired practice, psychology, personhood or A5. |
| **AUTHORITY** | `HOLD` | No native CAN/ADP/C8/C12/Pyat/C11/C5, protected keys, external provider or human A5. |

## Next coherent repair

1. Validate `new_branch_id` before `product.fork` in both shared callers: non-empty, not current/parent, not root, not an existing branch.
2. Or, if `new_lineage` raises after `product.fork`, remove the just-created branch before re-raising; do not leave an unowned branch row.
3. Add the empty/invalid-name atomicity to the author tests; rerun frozen 30, lineage 5 and the candidate/inherited suites on the next exact SHA.

No polling; same lane.
