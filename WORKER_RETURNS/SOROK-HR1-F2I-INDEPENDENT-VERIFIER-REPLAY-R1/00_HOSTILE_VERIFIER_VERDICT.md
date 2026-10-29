# SOROK HR1 F2I — independent episode verifier replay

**Verdict:** `ENGINEERING_ACCEPT_SCOPED_BOUNDED_VERIFIER__SECURITY_RESIDUALS_HOLD__SCIENCE_TEST_ONLY__AUTHORITY_HOLD`.

This is an independent I2 replay, not adoption. The original BP2P4JI `REVISE` is preserved. The F2 repair is accepted only for the exact episode-preimage defect it claims; it does not establish native C12, practice acquisition, completeness or an authenticated external anchor.

## Identity and host

- Repository: `maidiu/rawlsing` (private).
- Return branch: `review/sorok-hr1-f2-episode-verifier-independent-replay-20261029-r1`.
- Sealed startup: `2c45c58ccaaf5512795774d7690a1a6a320e2a66`.
- Sealed prompt head: `f37c02eca8f8f1f5664239cdd2ae919f1c800adf`.
- Immutable F2 author return: `0636d257f588f8874e65b2cb183d1d47c7f53327`; remote author head matched this SHA at launch.
- Original BP2P4J: `5b3e6577400ea1d88971ae6b48e41a118b8059ae`.
- Original BP2P4JI reviewer: `3212d716ce66586527c258632ef10c3ff4489803`.
- HR1 prior: `40df1e61fb32f9210839d8ddfa9f8bf9a47d7621`.
- PRE-MAIN pin: `299f41e97a43c67be9cc76a79fa49b48f4e12e54` (read only; no path `bp2p4/c12_verify.py` in that tree).
- Host: macOS x86_64 13.7.8; Python 3.11.3; pytest 9.1.1; SQLite 3.40.1; stdlib only.
- Editor/model: OpenCode / DeepSeek V4.1-Flash. No model/harness switch.
- Worktrees: return `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/f2i-return`; replay base `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/f2i-base` detached at `5b3e657`. The author worktree was not read or written as a runtime.
- No PRE-MAIN, PR #519/#514/#516, original BP2P4J/BP4/C12, or author branch was modified. The return branch is the only write target.

## FINDING — the repair is real; the security boundary is not closed

### Baseline reproduced exactly

At original `5b3e657`, before any overlay, the unchanged suite is **33 passed / 0 failed / 0 errors / 0 skipped**. The focused valid-SAY test then fails against the original verifier with exactly:

```text
episode:0:body_hash_mismatch
```

The durable row is intact: stored/body hash `c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be`; episode id `TEST_ONLY_BP4_EP_c75042dacaa6f4b1843c63f5840ed91f3573b17ce344483bd607b083328614be`; canonical preimage excluding `hash` and `episode_id` hashes to the same value; stored body JSON SHA-256 is `6a30f3c5e6b017c94a71e4139f2f68df1dfe3fa7552d1d6292d083f607744a27`.

### Repair reproduced exactly

Only the two claimed blobs were overlaid:

- `bp2p4/c12_verify.py` Git blob `c1699c8da5e944ed079708e272c3af50d5a30a44`, SHA-256 `6ad07d75f3ebb785e847e761e2db65df37abf8eea72559df3a6c54f031141d20`.
- `tests/test_episode_verifier_regression.py` Git blob `ebe1e8287f9b8485b6c862b66b6c2a9dafcf59aa`, SHA-256 `b55f148f5623458259c7fe3b05b340c19c3bc1a5f721a12145f50df7caa28c58`.

The repaired full suite is **38 passed / 0 failed / 0 errors / 0 skipped**: new 5, product 10, security 12, severance 7, source closure 4. The five original test files are byte-identical to their pinned Git blobs. No test was disabled, skipped, xfailed or weakened.

### Independent adversarial escalation

The repair detects what it claims to detect:

- Episode body tamper → `episode:0:body_hash_mismatch`.
- Episode id tamper / legacy-prefix form → `episode:0:episode_id_mismatch`.
- World-event body tamper → `world_event:0:body_hash_mismatch`.
- Cold reopen → chain digest and derived id preserved; 38-suite cold test green.

But independent raw-database probes expose residual HOLDs not repaired by the candidate:

1. **Injected self-consistent world event is accepted.** A raw inserted `world_event` row with a self-consistent body/hash and next `seq` yields `verify_branch_chain(...).ok == True`. Content hashing verifies the attacker's own preimage; it does not authenticate the event's provenance.
2. **Raw episode deletion is not detected by the verifier.** After dropping `episode_no_delete` and deleting one real episode, `verify_branch_chain(...).ok == True` with `counts.episode == 0`; only the unkeyed out-of-band `chain_digest` changes. This remains the author-named HOLD, not a closed guarantee.
3. **Fully rehashed episode forgery is accepted.** Replace an episode body's event id, recompute the body hash and derived `episode_id`, update the row hash: the verifier returns `ok == True`, while the unkeyed `chain_digest` changes. Simple id-only tampering is refused; a fully self-consistent rewrite is not distinguishable without an external anchor.
4. **Upstream BP4 verify remains self-referential.** On the valid episode, the independent verifier is `ok == True`, but `bp4.store.C12Store.verify` is `ok == False`; the candidate intentionally leaves upstream BP4 unpatched.

These are not regressions in the episode-preimage fix. They are the retained external-authenticity/completeness boundary. The candidate does not add an authenticated anchor and must not be read as doing so.

### Source severance

The seven primary and three supplementary severances all preserve the same named assertion `bp2p4.assertion.joined_downstream_a0_a2_assertion`: baseline `red=false`, cut `red=true`, restored `red=false`. Primary edges: BP2_C8_PROOF, BP2_ACTOR_HISTORY, BP2_RULE_A, BP2_RULE_T, BP2_TARGET_HASH, BP2_E2, BP4_C10_M6_ACCESS. Supplementary: BP2_OTHER_HISTORY_ALIASED, BP2_E2_NOT_PERFORMED, BP2_PRACTICE_NOT_MATERIALIZED. This is the same assertion, not a new one.

## INTERPRETATION

The F2 repair is the correct minimal preimage correction: episodes hash before their derived id is appended, and the verifier now excludes both `hash` and `episode_id` while separately enforcing the `TEST_ONLY_BP4_EP_` derivation. It repairs the original BP2P4JI RED without weakening body/world/id tamper checks or severance.

The residual findings are about **authenticity and completeness, not hash syntax**. A self-consistent attacker row is indistinguishable from a legitimate row by content hashing alone. The unkeyed chain digest detects a deletion only if a trusted copy is compared; it is not a signed anchor. The upstream BP4 verifier remains separately defective. The sourcefree performed-E2 positive survives; no native practice acquisition, original actor source, C8 authority, C11/C12 or production C12 is established.

## Three courts

- **ENGINEERING:** `ACCEPT_SCOPED` for the exact episode-preimage repair only. 33 baseline PASS, 1 baseline RED, 38 repaired PASS, same-assertion severance 10/10, cold reopen, tamper and source closure. Residual security HOLDs above remain.
- **SCIENCE:** `TEST_ONLY_E2_POSITIVE_ONLY__NO_NATIVE_PRACTICE_ACQUISITION`. The finite sourcefree A0/A2 consequence and performed-E2 path are preserved; no native psychology, learning, trait, practice or real person is inferred.
- **AUTHORITY:** `HOLD`. Original BP4/C12 and BP2P4J owners retain adoption. No merge, PRE-MAIN update, PR #514/#516 change, signed anchor, native rule or production consumer. The author is not the reviewer and this reviewer does not self-adopt.

## HQ ACTION and accountable owner

**HQ ACTION:** Accept the bounded engineering replay as evidence for the F2 preimage repair; do not adopt it as C12 completeness/authenticity. Require the original BP4/C12 owner to dispose of the upstream self-referential verifier and the raw-deletion/injection/anchor HOLD. Require the original BP2P4J owner to decide whether the derived `TEST_ONLY_BP4_EP_` prefix is the only lawful writer form; the independent probe shows a legacy id is refused. Route any follow-on repair to a fresh owner-scoped cut, not to this reviewer.

**ACCOUNTABLE OWNER:** Original BP2P4J verifier owner and BP4 C12 store owner for the engineering cut; independent key/anchor custodian for completeness; Sorok HQ for intake and a separate post-return reviewer. No native CAN/ADP/SCI05/C11/C12 issuer is claimed.

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** independent 33 baseline, original focused RED, exact two-blob overlay, 38 repaired suite, per-test JUnit, tamper body/id/world, legacy-id refusal, cold reopen, seven+three severances, raw injection/deletion/rehash probes, source/test blob custody.
- **REMAINING:** original-owner replay and adoption; signed/independently custodied external anchor; upstream BP4 verifier repair; legacy-writer policy; production/native consumer.
- **CRITICAL BLOCKERS:** raw SQLite deletion and self-consistent injection/rehash are accepted by content verification; no authenticated anchor; BP4 upstream verify still self-referential.
- **LARGEST PRODUCTIVE MOVE:** original BP4/C12 owner replays candidate `c1699c8d…` at base `5b3e657…`, then decides the anchor boundary before any C12 adoption.
- **FLIGHT:** sourcefree local Git/Python only; no upstream or PRE-MAIN mutation.
- **DELTA:** valid SAY episodes now verify under the independent add-on without weakening tamper/severance checks; the external-anchor/completeness HOLD remains explicit and independently reproduced.

## First consumer and limits

First real consumer in this evidence is the BP2P4J joined security/audit court (`tests/test_joined_security.py` and the new focused regression). No production consumer is claimed. The original BP2P4JI reviewer’s `REVISE`, its retained HOLD caveats, the raw-deletion/anchor HOLD and the unissued native authority remain in force.

## Final remote SHA

The ordinary push binds this return. Its full 40-hex SHA is verified by direct `ls-remote` after the commit and reported in the final response; a commit cannot contain its own final SHA. No force-push, no self-acceptance, no PRE-MAIN mutation.
