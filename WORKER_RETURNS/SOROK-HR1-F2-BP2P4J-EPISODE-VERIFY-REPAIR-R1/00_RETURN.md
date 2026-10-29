# SOROK HR1 F2 — BP2P4J episode hash verifier repair return

## Identity and custody

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-hr1-bp2p4j-episode-verifier-sourcefree-repair-20261029-r1` |
| Sealed startup | `3fd8dcb3df520806c7aee820e511092863545f4e` |
| Branch start / prompt head | `2c8da7fcbf721a0e04fb25735cd4bee58754969f` |
| Original BP2P4J cut | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` |
| Independent BP2P4JI cut | `3212d716ce66586527c258632ef10c3ff4489803` |
| HR1 counterexample | `40df1e61fb32f9210839d8ddfa9f8bf9a47d7621` |
| PRE-MAIN pinned | `299f41e97a43c67be9cc76a79fa49b48f4e12e54` (read only) |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hr1-f2` |
| Editor / model | Local OpenCode / DeepSeek V4.1-Flash (`opencode-go/deepseek-v4.1-flash`); MAX effort requested, actual effort not independently verifiable from inside this session |
| Runtime | macOS x86_64, Python 3.11.3, pytest 9.1.1, SQLite 3.40.1, stdlib only |

Observed FINDING: the original BP2P4J independent verifier fails a valid SAY episode with `episode:0:body_hash_mismatch`. Causal INTERPRETATION: `append_episode` hashes the episode body and only then appends `episode_id`; `verify_branch_chain` removed only `hash`, so it recomputed the preimage including the post-hash id. Proposed HQ ACTION: owner review and adoption decision for this minimal verifier candidate, followed by separate independent review. Accountable OWNER: original BP2P4J/BP4 C12 owner.

## Repair

The candidate changes only `bp2p4/c12_verify.py` and adds one focused regression file. For the `episode` table, the recomputed preimage excludes both `hash` and the derived post-hash `episode_id`; the stored `episode_id` must equal `TEST_ONLY_BP4_EP_` plus the stored body hash. The column-hash, sequence, `world_event`, `checkpoint` and `perception` checks are unchanged. No assertion was waived: tampered episode bodies still yield `body_hash_mismatch`, tampered episode ids yield `episode_id_mismatch`, and tampered world-event bodies still yield `world_event:0:body_hash_mismatch`.

- Candidate verifier SHA-256 `6ad07d75f3ebb785e847e761e2db65df37abf8eea72559df3a6c54f031141d20`, Git blob `c1699c8da5e944ed079708e272c3af50d5a30a44`.
- Candidate test SHA-256 `b55f148f5623458259c7fe3b05b340c19c3bc1a5f721a12145f50df7caa28c58`, Git blob `ebe1e8287f9b8485b6c862b66b6c2a9dafcf59aa`.
- Original verifier blob `b8e7cf397dbbbc37aa0a63ce9e0d7ba27a509cd3`.

## Reproduction and regression

The exact original RED is preserved in `evidence/04_ORIGINAL_RED_ROW_AND_PREIMAGE.json`: episode seq `0`; stored/body hash `c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be`; episode id `TEST_ONLY_BP4_EP_c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be`; canonical preimage excluding `hash` and `episode_id` hashes to the same `c75042da...614be`; stored body JSON SHA-256 is `6a30f3c5e6b017c94a71e4139f2f68df1dfe3fa7552d1d6292d083f607744a27`.

Actual results: unmodified original suite `33 passed`; focused valid-SAY test on the unmodified verifier `1 failed` with `episode:0:body_hash_mismatch`; overlaid full suite `38 passed`, 0 failed, 0 errors, 0 skipped. The five new tests cover the valid positive, tampered episode body, tampered derived id, tampered world event and cold reopen. The existing 7 source-severance tests, 12 security/refusal tests and the 4 source-closure tests all pass unchanged. The original `test_raw_database_access_can_drop_the_append_only_trigger_is_a_residual` remains green and the distinct raw-SQLite deletion/out-of-band-anchor HOLD remains open. Exact commands, JUnit and frozen test blob identities are in `02_REGRESSION_COMMANDS_JUNIT_AND_FROZEN_NEGATIVES.md`.

## Grades and authority

ENGINEERING: `PASS_BOUNDED_RED_TO_SAME_ASSERTION_GREEN` at the candidate overlay. SCIENCE: `TEST_ONLY_E2_POSITIVE_ONLY__NO_NATIVE_PRACTICE_ACQUISITION`; this return does not reissue native Rule T, C11/C12 or person claims. AUTHORITY: `HOLD_NO_ADOPTION`; original BP2P4J/BP4 C12 owners retain adoption rights and a separate source-qualified I2 reviewer must replay against the final SHA. The author is not the reviewer.

First real consumer in this evidence is the BP2P4J joined security/audit court; no production or native consumer is claimed. Outstanding receiver: original BP4/C12 owner for the external deletion/anchor HOLD and original BP2P4J owner for branch adoption. PRE-MAIN, PR #514 and PR #516 were not changed. No unsent files are intended; the pushed branch head is the exact remote return SHA reported with this return.

## Artifacts

- `00_RETURN.md` — this return.
- `01_CANDIDATE_SOURCE_HASH_AND_CHANGED_PATHS.json` — exact overlay mapping, hashes, frozen test blobs and test counts.
- `02_REGRESSION_COMMANDS_JUNIT_AND_FROZEN_NEGATIVES.md` — commands, results, JUnit and retained HOLD.
- `03_EXACT_C12_OWNER_AND_INDEPENDENT_REVIEW_HANDOFF.md` — replay recipe, owner questions and review split.
- `candidate/` — repaired verifier plus focused regression.
- `evidence/` — baseline and repaired JUnit/logs, original RED log/row and patch.

DONE: exact RED, minimal preimage repair, same-assertion GREEN, tamper/cold/severance/residual reruns, source hashes and owner replay instructions. REMAINING: owner replay, adoption decision and independent review. CRITICAL BLOCKERS: none for the bounded verifier repair; native science and authority remain separately held. LARGEST PRODUCTIVE MOVE: original BP4/C12 owner replays candidate blob `c1699c8d` at base `5b3e657`. FLIGHT: sourcefree local Git/Python only; no upstream or PRE-MAIN mutation. DELTA: valid SAY episodes now verify without waiving tamper detection, and the raw-SQLite deletion/anchor HOLD remains distinct.
