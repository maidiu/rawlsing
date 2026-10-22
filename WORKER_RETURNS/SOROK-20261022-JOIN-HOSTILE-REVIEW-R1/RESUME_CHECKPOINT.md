# JOIN-V resume checkpoint — shared-lineage cut 49022f6

**STATUS:** `LINEAGE_FINAL_REVISE__49022f6__INVALID_FORK_PARTIAL_BRANCH_LEAK__AWAIT_NEXT_REPAIR_SHA`
**BRANCH:** `codex/sorok-join-v-20261022`
**REVIEWED CUT:** `49022f693c99b6cb58226513f8bad71c26bdac3c` (read-only detached worktree)
**PRIOR CUTS:** 75a134e (REVISE), cc0ff7d (REVISE), c367777 (REVISE), 13dfd6bad (preliminary)
**WRITE SCOPE:** own return only; no candidate/J/E edit.

## Results against 49022f6

| Suite | Result |
|---|---|
| Preserved 30 reviewer executions | **30/30 passed** (author-reported 30/30 independently reproduced) |
| Targeted c367 | 5/6; historical E-first-refusal expectation |
| New lineage-contract tests | 4/5; one failure |
| JOIN-E own suite | 17/17 passed |
| Inherited J / E / R30A | 8/8, 15/15, 10/10 passed |
| Source manifest | 444/444 verified |

Frozen hashes match `FROZEN_ORACLES.json`; no frozen test edited. Full evidence: `LINEAGE_FINAL_ADJUDICATION.md`, `evidence/lineage_final/`.

## Passed shared-lineage coverage

- `joined/lineage.py` used by both `JoinedSession` and `RefusalSession`.
- Fork receipts match actual created branch rows, including non-null clock/root/created fields.
- Nested `first_session -> alt -> alt2` forks persist, cold-reopen, and leave parent untouched.
- Metadata-only parent/sibling/root switches are refused without product mutation.
- Missing/tampered receipt chains and duplicate fork requests are refused without mutation.
- Parent/donor state remains stable on rejected metadata operations.
- Nonmutating targetless cold reopen, no target/native grant, source/C12/C8, privacy, attention, joined encounter and B-source bounded scope remain intact.
- Old E-first-refusal expectation remains historical/superseded by J closure.

## Remaining exact failure

`fork_alt("")` raises `SessionRefusal('FORK_REFUSED')` but leaves an empty `''` branch in the C12 store in both joined and targetless paths:

```text
before: ['first_session', 'root']
after:  ['', 'first_session', 'root']
session metadata: unchanged on first_session
```

This violates invalid-request/partial-failure consistency. New test: `test_invalid_empty_fork_is_atomic`.

## Next safe move

Await next repair SHA. Re-run 30 preserved tests, targeted c367, lineage-contract tests, candidate/inherited suites. The remaining repair should validate the requested branch name before `product.fork`, or remove the created branch if lineage construction fails; preserve all other lineage behavior.
