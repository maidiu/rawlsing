# RRIF-R2 — INDEPENDENT HOSTILE FIRST-CONSUMER AND C12 PROVENANCE COURT — RETURN

**Decision: `REVISE_MATERIAL_DEFECTS`** (scoped independent review only; no owner acceptance, no native grant, no PREMAIN merge, no self-adoption).

**Immutable subject:** `598d9e9eaba5143950c63317705fd09104fbf463`
**Candidate content commit:** `1745fbb68dddfe150e93eb7789a02c4c0768bd66`
**Review branch:** `review/sorok-rrif-r2-real-code-independent-hostile-first-consumer-20261031`
**Harness:** mainMac.lan; OpenCode 1.18.34; agent build; actual session DB and argv both show `opencode-go/deepseek-v4.1-flash` with `variant: max`; Python 3.11.3; pytest 9.0.2; Git 2.43.0. No model/provider/host/account switch or effort reduction.

## FINDING

1. The 20-test two-file suite independently reruns **20 passed / 0 failed / 0 errors / 0 skipped** in a clean detached worktree at `598d9e9e` (11.26s). The actual CLI first consumer performs SHARE/omit -> `HELP_ACCEPT`, SHARE/e2 -> `HELP_REFUSE`, targetless REFUSE -> no target/E2/practice, cold reopen/fork, privacy/actor-ignorance separation, and C12 uncoordinated episode tamper -> RED -> exact restore -> GREEN.
2. The 444-file vendor closure is exact: every vendor blob and every source-commit/path byte matches R31J `64fec28c...` (217 files) and R31E `a2760d36...` (227 files). The vendor tree is byte-identical to JOIN-E `7bf2...` (`72ff9d0b...`); the 10-module joined tree is also byte-identical (`ea123a84...`).
3. **No new production R2 logic exists.** The only genuinely new R2 code is `tests/test_rrif_r2_c12.py` (92 lines); `test_join.py` changed only path resolution (4 lines), `conftest.py` and the proof JSON were removed, and manifests were added. R2 is a repackaging of JOIN-E, not a new four-asset fan-in.
4. **Material defect R2-T1:** `test_independent_c12_verifier_rejects_forged_episode_hash` is vacuous. On the intact store `QualifiedC12Store.verify` is true, while `bp2p4.c12_verify.verify_branch_chain` is already false with `episode:0/1:body_hash_mismatch` because it does not drop the post-hash `episode_id`. The test asserts false after tamper and has no positive control; the R2 return's "independent verifier" claim is not evidence.
5. **Material defect R2-M1:** the candidate preimage is 458/459 exact. Its own entry declares SHA-256 `9b045ac...`/size 89022; the returned bytes are `641165d2987da460104101accea983afb32050e81b15986eb49ae92f434a53b2`/89341. The return 01 repeats the stale `9b045ac...`. The 444 vendor rows and `SOURCE_MANIFEST.json` SHA `7cfcb467...` are exact.
6. **C12 ceiling:** a raw-DB attacker can drop the append trigger and rewrite an episode/world/checkpoint preimage with recomputed hashes; `QualifiedC12Store` and `JoinedSession.open` stay green. Episode `actor_id`, `clock`, `episode_id` and `kind` columns, `perception` content (no hash; only seq), and `branch` `root_hash`/`created_clock`/`fork_clock` are not covered. A coordinated C12+sidecar+meta source substitution (a lawful refusal source object) passes the C12 verifier but is stopped by the unchanged C8 source witness; a coordinated C8 journal rewrite is stopped by the keyed proof sidecar. The `ExternalCheckpointWitness` is defined at `vendor/j/r26e/c12_integrity.py:83` but not used; its own docstring says same-user DB+witness/key rewrite defeats it (`TRUST_CUSTODY_HOLD`). Recomputed self-hashes and locally keyed proofs are **not** independent owner attestation.
7. **C9 target:** uncoordinated target-body tamper is caught at `BP2_C9_CONSUMED_HASH_MISMATCH`; a coordinated target note plus persisted/artifact consumed-hash update is still caught at `BP2_E2_NOT_ADMITTED: CONSUMED_STATE_MISMATCH`. C9 is more cross-linked than C12, but still a self-hash/receipt chain.
8. **C9/C9C12 incompatibility:** R2 uses old C12 `7bf2` plain-root fork semantics; C9C12-R2's `C12_GUARD_READER@1` returns `fork:alt:legacy_root_unverified` and `fork:first_session:legacy_root_unverified` on the R2 fork. R2 C9 is BP2P4J `CandidateStore`, not `C9_ACTOR_AUTHORITY_R3@1`; C9C12's `read_actor_snapshot` raises `no such table: actor_meta`. On a column-tampered DB, R2 `Qualified` is green while the C9C12 guard is red with `episode_id_column_mismatch`, `actor_id_column_body_mismatch`, and `clock_column_body_mismatch`. C9C12 also returns `OWNER_ANCHOR_REQUIRED`; R2 has no external anchor. R2's `C9C12` disposition "compatible sourcefree candidate unintegrated" is too strong.

## INTERPRETATION

The JOIN-E consumer itself is a real, runnable, cold-reopenable sourcefree C9/C12/JOIN consumer, and its source closure is exact. The R2 **packet** is not acceptance-grade: the only new test contains a false independent-verifier claim, the returned preimage self-entry is stale, the C12 verifier is self-hash-only with an explicit external-anchor ceiling, and the C9C12-R2 compatibility classification is wrong for forks and the C9 actor schema. These are bounded, exact defects—not a reason to re-census RRIF or to touch another worker.

## ACTION

Minimal R2 repair before any owner adoption:

- **R2-T1:** fix or explicitly document the `bp2p4.c12_verify` episode-id preimage; make the test assert green on intact + red on tamper, or assert the known upstream defect and remove the agreement claim.
- **R2-M1:** regenerate/detach the candidate preimage self-entry and update return 01; all 444 vendor rows remain exact.
- **R2-C1:** narrow the C12 wording to episode/world/checkpoint self-consistency + perception sequence; add coordinated rehash/column/perception/branch negatives or adopt the C9C12 guard for C12 integrity.
- **R2-D1:** change the C9C12-R2 disposition to `INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED`.

No native/sourcefull/provider/browser work, no PREMAIN merge, PR alteration, force push or future-work dispatch.

## OWNER

Receiving decision: qualified **Sorok/PREMAIN** owner (not the R2 author, not this reviewer). C12 cut/anchor: C9R/BP4/C12 owner. C9 cut: C9R owner. F1CR/V3/Pyat/native grants: their original owners. This review is an independent scoped input only.

## THREE COURTS

**ENGINEERING: `REVISE_MATERIAL_DEFECTS`.** 20/20 local sourcefree tests pass, source 444/444 exact, CLI/B/cold/fork/privacy behavior reproduced. The only new R2 test is partly vacuous, the preimage self-entry is stale, and C12 column/branch/perception coverage is materially weaker than the C9C12-R2 guard. Not acceptance-grade until R2-T1/M1/C1/D1.

**SCIENTIFIC: `HOLD`.** Sourcefree TEST_ONLY actor/rule/C8/C9/C12 only. No CAN008 Rule A, CAN011 Rule T, ADP/SCI05 actor, native B/E2, native C9/C12, C11, Pyat N11/N12, human A5 or original survey. The surface is deterministic sourcefree fixture behavior, not a generated human person.

**AUTHORITY: `HOLD`.** No original owner acceptance, no PREMAIN integration, no cross-HQ/Pyat grant, no self-review/self-adoption. A green test suite is not an owner grant.

## DONE / REMAINING / BLOCKERS / LARGEST_MOVE / FLIGHT / DELTA

**DONE:** independent clean-worktree 20-test rerun; actual CLI start omit/e2, help, wait, fork, cold return, verify; raw SQLite recompute; C12/C9/B/source tamper-restore court; 444-file source identity; JOIN-E delta; C9C12/C9-R3B comparison; six outputs.

**REMAINING:** R2-T1/M1/C1/D1 minimal repair; owner decision on C12 cut/anchor and C9 cut; CP-A5/B-F1CR/V3CORE/R6/R41 owner dispositions; receiving owner selective fan-in with rollback.

**BLOCKERS:** no external C12 owner anchor/custodian; no native CAN008/CAN011/ADP/SCI05/C8 D1-D2/C9 native/C11/Pyat; no human A5; C9/C12 version split unresolved; R2 packet test/manifest defects.

**LARGEST_MOVE:** the receiving owner should require the four exact repairs, then choose either the JOIN-E consumer under a narrowed self-consistency claim or the C9C12-R2 guard + owner anchor for real C12 integrity. No implementation of RRIF-R3 here.

**FLIGHT:** S2 local Git/Python/SQLite/pytest only. No native/sourcefull/actor/survey/provider/browser call; no PREMAIN/PR/Programma/Pyat/other-worktree edit.

**DELTA:** From author's 20/20 claim to independently reproduced 20/20 plus exact 444-file source identity, and to four concrete defects/ceilings: vacuous independent verifier, stale preimage self-entry, C12 self-hash-only coverage, and C9C12 fork/C9 schema incompatibility. No native person, science, authority or production adoption was created.

## EXACT REMOTE SHA

**Return content commit:** `d047b388b4b3598157b60eeda188e8714bb77565`
**Readback command:** `git ls-remote origin refs/heads/review/sorok-rrif-r2-real-code-independent-hostile-first-consumer-20261031`
**Readback at content commit:** `d047b388b4b3598157b60eeda188e8714bb77565`
**Final exact remote SHA:** the no-force readback commit that contains this complete return; its exact 40-hex is reported in the terminal response of this review.

No force push, no owner adoption, no PREMAIN merge and no self-adoption are claimed.
