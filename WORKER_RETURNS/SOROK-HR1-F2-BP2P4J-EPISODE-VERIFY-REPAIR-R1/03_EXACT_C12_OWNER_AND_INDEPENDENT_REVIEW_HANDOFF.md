# F2 BP2P4J — exact C12 owner and independent review handoff

Observed FINDING: valid BP2P4J SAY episodes fail the independent verifier with `episode:0:body_hash_mismatch`; the durable row's `episode_id` was appended after hashing. Causal INTERPRETATION: the verifier reconstructed the episode preimage from the post-hash durable row. Proposed HQ ACTION: hand this candidate to the original BP2P4J/BP4 C12 owner for replay and adoption decision, then to a separate source-qualified I2 reviewer. Accountable OWNER: original BP2P4J owner and BP4 C12 owner; independent reviewer is distinct from the author.

## Identity and jurisdiction

Repository `maidiu/rawlsing`; candidate branch `agent/sorok-hr1-bp2p4j-episode-verifier-sourcefree-repair-20261029-r1`; sealed startup `3fd8dcb3df520806c7aee820e511092863545f4e`; branch start `2c8da7fcbf721a0e04fb25735cd4bee58754969f`. Original BP2P4J source `5b3e6577400ea1d88971ae6b48e41a118b8059ae`; independent BP2P4JI `3212d716ce66586527c258632ef10c3ff4489803`; HR1 counterexample `40df1e61fb32f9210839d8ddfa9f8bf9a47d7621`. PRE-MAIN pinned `299f41e97a43c67be9cc76a79fa49b48f4e12e54` was read only. PR #514 and #516 were not touched. The original BP2P4J return tree remains unchanged at its own commit; this branch adds only the overlay below.

## Candidate overlay and exact hashes

- `candidate/bp2p4/c12_verify.py` maps to `WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/bp2p4/c12_verify.py`; Git blob SHA-1 `c1699c8da5e944ed079708e272c3af50d5a30a44`; SHA-256 `6ad07d75f3ebb785e847e761e2db65df37abf8eea72559df3a6c54f031141d20`.
- `candidate/tests/test_episode_verifier_regression.py` maps to the same return's `tests/` directory; Git blob SHA-1 `ebe1e8287f9b8485b6c862b66b6c2a9dafcf59aa`; SHA-256 `b55f148f5623458259c7fe3b05b340c19c3bc1a5f721a12145f50df7caa28c58`.
- Original verifier blob: `b8e7cf397dbbbc37aa0a63ce9e0d7ba27a509cd3`.

Replay recipe:

```sh
git worktree add --detach /tmp/bp2p4j-owner-replay 5b3e6577400ea1d88971ae6b48e41a118b8059ae
cd /tmp/bp2p4j-owner-replay/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1
cp <candidate>/candidate/bp2p4/c12_verify.py bp2p4/c12_verify.py
cp <candidate>/candidate/tests/test_episode_verifier_regression.py tests/
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q
```

Expected: baseline original suite without the overlay is 33/33 pass; the focused valid-SAY test on the unmodified verifier is 1 failure with `episode:0:body_hash_mismatch`; the overlaid suite is 38/38 pass. The exact RED row and preimage are in `evidence/04_ORIGINAL_RED_ROW_AND_PREIMAGE.json`. The owner should confirm the original test blobs are unchanged before applying the overlay: `tests/conftest.py` `35c1e1c0cac69c6006f669201b018289348e619a`; `tests/test_joined_product.py` `f0e52ea3a2e39d29c4740ead7032c366cec19eeb`; `tests/test_joined_security.py` `9cffe8a95d23492053f5ccd612128f0d02a96ed9`; `tests/test_joined_severance.py` `9e15af676d0ef3f33a345ebbc3ee0734e09ac63c`; `tests/test_source_closure.py` `cfe1d1b4e155e0d12699280af6b071c320702e95`.

## What the owner must decide

1. Whether the BP4 C12 episode schema has exactly one valid `episode_id` derivation, `TEST_ONLY_BP4_EP_` plus the pre-hash body hash. The candidate enforces that derivation; any other writer or legacy id form would be refused.
2. Whether the derived-id check belongs in this independent add-on, in BP4's own store, or both. The candidate leaves BP4 `C12Store.verify` untouched and does not claim to repair upstream BP4.
3. Whether the raw-SQLite deletion and external-anchor HOLD remains the correct owner boundary. The candidate retains it; it does not add an authenticated anchor.
4. Whether the test-only performed-E2 positive and the A0/A2 consequence are still the same object after the verifier-only change. The candidate asserts a valid SAY row and the existing product/severance suites; it does not reissue science.

## Review independence and acceptance split

ENGINEERING: candidate is eligible for bounded pass after owner replay: exact original RED, minimal preimage repair, same-assertion positive, tamper/refusal, cold reopen, source severance and frozen negatives. SCIENCE: only the existing TEST_ONLY sourcefree E2 positive is preserved; no native practice acquisition, Rule T, C11/C12 or person claim. AUTHORITY: HOLD; no adoption, merge, PRE-MAIN update or PR #514/#516 change is claimed or authorized by this return. The author is not the reviewer and cannot accept this work.

The independent reviewer should be a separate source-qualified I2 engineer appointed by incumbent HQ. Reviewer must not be the original BP2P4J author, the BP4 C12 owner, or this author; the original owners retain adoption authority. First real consumer of the repaired verifier in this evidence is the BP2P4J joined security/audit court (`tests/test_joined_security.py` and the new focused test); no production consumer is claimed. Outstanding receiver: original BP4/C12 owner for the external-anchor/deletion HOLD and original BP2P4J owner for branch adoption.

DONE: exact source/blob mapping, replay recipe, frozen test identities, candidate hashes. REMAINING: owner replay, adoption decision and independent review. CRITICAL BLOCKERS: none for the bounded verifier repair; authority and native receiver remain separate. LARGEST PRODUCTIVE MOVE: owner runs the three-command replay at `5b3e657` against candidate blob `c1699c8d`. FLIGHT: candidate overlay only, no upstream source adoption. DELTA: post-hash episode id is now excluded from the preimage but still exactly checked.
