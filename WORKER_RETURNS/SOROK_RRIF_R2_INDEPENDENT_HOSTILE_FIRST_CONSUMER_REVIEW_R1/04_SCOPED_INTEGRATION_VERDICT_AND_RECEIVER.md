# Scoped integration verdict and receiving-owner packet

Subject: `598d9e9eaba5143950c63317705fd09104fbf463` (content `1745fbb68dddfe150e93eb7789a02c4c0768bd66`).
Review branch: `review/sorok-rrif-r2-real-code-independent-hostile-first-consumer-20261031`.
Decision: **`REVISE_MATERIAL_DEFECTS`** (not owner acceptance, not a native grant, not a PREMAIN merge).

## 1. Verdict

| Court | Verdict | Basis |
|---|---|---|
| ENGINEERING | `REVISE_MATERIAL_DEFECTS` | The JOIN-E consumer reruns 20/20 and behaves cold/fork/B/privacy; the 444-file vendor closure is exact. But the only new R2 test contains a vacuous "independent verifier" assertion, the returned preimage self-entry is stale, and the C12 verifier is materially weaker than the C9C12-R2 guard. The packet is not acceptance-grade until the named minimal repairs below. |
| SCIENTIFIC | `HOLD` | Sourcefree TEST_ONLY actor/rule/C8/C9/C12 only. No CAN008 Rule A, CAN011 Rule T, ADP/SCI05 actor, native B/E2, native C9/C12, C11, Pyat N11/N12, human A5 or original survey. |
| AUTHORITY | `HOLD` | No original owner acceptance, no PREMAIN merge, no cross-HQ/Pyat grant, no self-review/self-adoption. The receiving decision remains with the qualified Sorok/PREMAIN owner. |

A passed suite is not an accepted owner grant. This return is an independent scoped review only.

## 2. What is compatible and actually runnable

**App/code root:** `SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`.

**Exact source closure:** JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`; vendor tree `72ff9d0b3af0dc3f4dd33ac2135fcb039a754dcc` (444 files, exact), joined tree `ea123a84cd5ba97b7fe9666a1581bd3236462184` (10 modules, exact). The 444 rows are exact preimages of R31J `64fec28c...` (217 files) and R31E `a2760d36...` (227 files). JOIN-V `4387dc...` is only a same-root fork/cold review; no new code.

**First consumer actually called:** `joined.cli` / `JoinedSession.start/open`, which reads:
`R31J pre-C9 source -> BP3/C8 keyed journal -> BP2P4J C9 CandidateStore -> R29P/R26E QualifiedC12Store -> R31E actor expression -> JoinedSession`.
`audit_loaded` resolves the intended J/E/LIVE modules in the clean worktree and is green.

**Positive consumer:** `perform=omit` gives `SHARE_TOOL`, persisted `tools_remaining=1`, `HELP_ACCEPT`; `perform=e2` gives `SHARE_TOOL`, `tools_remaining=0`, `HELP_REFUSE`. Both cold reopen and verify.

**Negative consumer:** targetless `REFUSE_TOOL` gives `target_id=""`, `c9.target_branch=NO_CHANGE`, `c9.target_reason=NO_PROPOSAL`, no E2/practice/target, `HELP_REFUSE`; cold refusal reopens and remains refused.

**B/privacy:** SHARE/REFUSE difference is visible through the E help surface; actor ignorance yields `UNKNOWN_B`; private query yields `PRIVATE_BOUNDARY`; no private tokens or source hash cross the surface.

**Not promoted native:** CLI status `native=false`, session grade `TEST_ONLY_SOURCEFREE_NOT_NATIVE`, C12 grade `TEST_ONLY_QUALIFIED_C12_NOT_NATIVE`, checkpoint/world `native=false`. No sourcefree result was promoted to a native person.

## 3. Material defects requiring exact repair

### R2-T1 — vacuous independent-verifier test

`tests/test_rrif_r2_c12.py:66-92` (`test_independent_c12_verifier_rejects_forged_episode_hash`) asserts that `bp2p4.c12_verify.verify_branch_chain` is false after a forged episode. But that function is already false on the intact store:

```text
QualifiedC12Store.verify(root)              -> ok=true, errors=[]
bp2p4.c12_verify.verify_branch_chain(root)  -> ok=false, errors=[episode:0:body_hash_mismatch, episode:1:body_hash_mismatch]
```

The cause is exact: `verify_branch_chain` recomputes the episode preimage without dropping the post-hash `episode_id`; `QualifiedC12Store` does drop it (`vendor/j/r26e/c12_integrity.py:35-50`). The test therefore has no positive control and its "independent verifier" claim is not evidence.

**Repair:** either (a) make the independent verifier use the actual row preimage (drop `episode_id`) and assert green on intact + red on tamper, or (b) explicitly assert and document the upstream defect and remove the claim of agreement. Do not silently delete the test or the historical oracle.

### R2-M1 — stale candidate preimage self-entry

`RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json` is 458/459 exact. Its own entry declares size `89022` and SHA-256 `9b045ac...`; the returned bytes are size `89341` and SHA-256 `641165d2987da460104101accea983afb32050e81b15986eb49ae92f434a53b2`. `01_SOURCE_PREIMAGE_MODULE_AND_FIRST_REAL_CONSUMER.json` repeats the stale `candidate_audit_sha256` `9b045...`.

**Repair:** exclude the preimage from its own `files` list with an explicit detached/self-hash convention, or regenerate a correct two-file audit; update the return's `candidate_audit_sha256`. The 444 vendor rows and `SOURCE_MANIFEST.json` SHA `7cfcb467...` are already exact and should not be changed.

### R2-C1 — C12 claim is self-hash only

The candidate verifier does not cover:

- episode row columns (`actor_id`, `clock`, `episode_id`, `kind`);
- `perception` content (the table has no hash; only `seq` is checked);
- `branch` rows (`root_hash`, `created_clock`, `fork_clock`), which a direct UPDATE changed while `verify` and `JoinedSession.open` stayed green;
- semantic cross-field binding; coordinated episode/world/checkpoint rehash stays green;
- any external anchor; `ExternalCheckpointWitness` is defined but not used.

The code/docstring is honest that the witness is TEST_ONLY and same-user, and the return 03 says "perception: sequence integrity." The **claim** must stay exactly that: episode/world/checkpoint self-consistency plus perception sequence, not C12 integrity or authenticity. If a later consumer needs column/origin/fork integrity, use the C9C12-R2 `C12_GUARD_READER@1` (below), not `QualifiedC12Store` alone.

**Repair:** narrow the return's C12 wording, add explicit negative tests for the coordinated rehash/column cases, or adopt the C9C12 guard as the C12 reader under owner decision.

### R2-D1 — C9C12-R2 disposition is not "compatible unintegrated"

The R2 return 04 currently calls C9C12-R2 `COMPATIBLE_SOURCEFREE_CANDIDATE_UNINTEGRATED__VERSION_CUT_NOT_SELECTED`. The exact comparison is stronger:

- R2 uses old C12 `7bf2` vendor store and plain branch `root_hash`; C9C12-R2's guard reports `fork:alt:legacy_root_unverified` and `fork:first_session:legacy_root_unverified`.
- R2 C9 is BP2P4J `CandidateStore` (`occurrence`/`target_state`); C9C12-R2's `read_actor_snapshot` requires `C9_ACTOR_AUTHORITY_R3@1` / `actor_meta` and fails on R2 C9 with `no such table: actor_meta`.
- C9C12-R2's guard checks episode_id/actor_id/clock columns; R2's `Qualified` does not. On the same column-tampered DB: R2 `ok=true`; C9C12 guard `ok=false` with `episode:0:episode_id_column_mismatch`, `episode:0:actor_id_column_body_mismatch`, `episode:0:clock_column_body_mismatch`.
- C9C12-R2 returns `OWNER_ANCHOR_REQUIRED` on the R2 root cold read; R2 has no external anchor.

**Repair:** change the disposition to `INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED`; use the guard as the RRIF-R3 input, not the old R2 verifier.

## 4. Receiver packet (owner-held; not self-adopted)

```text
RECEIVER_PACKET_RRIF_R2_INDEPENDENT_REVIEW@1
subject                    598d9e9eaba5143950c63317705fd09104fbf463
candidate                   SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2
candidate_content_commit    1745fbb68dddfe150e93eb7789a02c4c0768bd66
source_closure              JOIN-E 7bf2da302996491ddf34b9a039fea47ac982d135
vendor_tree                 72ff9d0b3af0dc3f4dd33ac2135fcb039a754dcc
joined_tree                 ea123a84cd5ba97b7fe9666a1581bd3236462184
tests_status                20/20 PASS on mainMac.lan, Python 3.11.3, pytest 9.0.2
first_consumer              joined.cli / JoinedSession.start/open
native_grant                NONE
owner_adoption              NONE
premain_merge               NONE
receiver                    qualified Sorok/PREMAIN owner (not author, not this reviewer)
rollback                    do not adopt this exact packet; restore/withdraw by branch/commit; no PREMAIN write performed
required_before_adoption    R2-T1, R2-M1, R2-C1, R2-D1
```

The JOIN-E **consumer** itself is behaviorally green and can be handed to the receiving owner for inspection; the **returned R2 evidence packet** is not acceptance-grade until the four exact repairs. The next fan-in for RRIF-R3 is the C9/C12 root/reader under the C9C12-R2 guard and a named owner anchor, not a merge of this packet as-is.

## 5. Next owner fan-in (bounded, no implementation here)

1. **Owner:** Sorok/PREMAIN receiving owner; C9R/BP4/C12 owner for C12 cut; original C9/C12/Pyat owners for native grants.
2. **App:** use the JOIN-E `JoinedSession` sourcefree consumer only after R2-T1/R2-M1 are corrected; keep TEST_ONLY grade.
3. **C12:** if C12 integrity is required, select C9C12-R2 `C12_GUARD_READER@1` + `C9C12_R2` guard semantics, and require the owner-issued external anchor. Do not claim R2's `QualifiedC12Store` is equivalent.
4. **C9:** decide whether the BP2P4J CandidateStore is the intended C9 or whether the C9 R3B actor store (`C9_ACTOR_AUTHORITY_R3@1`) is canonical. R2 cannot read the latter; C9C12-R2 cannot read R2's C9.
5. **Negative:** preserve C9 R3B 14/1, BP4R 7/2, B3, F1CI3, G17I, CAN3, OC5E, M04, and F1CR SOURCE_NOT_FOUND. Do not rewrite an oracle to green.
6. **No self-adoption, no self-merge, no PR/PREMAIN/Programma work** from this review.
