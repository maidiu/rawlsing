# SOROK JOIN-V — independent hostile causal and persistence return

**STATUS:** `FORK_ATOMICITY_7BF_ACCEPT_SCOPED__INVALID_EMPTY_FORK_ATOMIC__STOP`
**ROLE:** independent hostile engineering reviewer; not JOIN-E, J, E, Sorok HQ, native C12/CAN/ADP/Pyat/C11 or human A5 authority.
**BRANCH:** `codex/sorok-join-v-20261022`
**STARTUP:** `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`
**PRELIMINARY CANDIDATE:** `13dfd6bad54ec19b4bdf31159e54fb6052d5440d`
**PRIOR FINAL CUT:** `c367777f83367240352c267a2d3750abb7f09397`
**PRIOR REPAIRED CUT:** `cc0ff7d0305340b806ba94b020017c3d8d0585dc`
**PRIOR TARGETLESS CUT:** `75a134ed733acaed2c62ea3421b54fcb09c5442f`
**REVIEWED SHARED-LINEAGE CUT:** `49022f693c99b6cb58226513f8bad71c26bdac3c`
**REVIEWED FORK-ATOMICITY CUT:** `7bf2da302996491ddf34b9a039fea47ac982d135` (read-only detached worktree)
**EXACT COMMISSION SEAL:** `2b8d3067d894941c21ec7fd23d1f883f51b15026`
**AUTHORITY:** independent accession `3de081023406a52ec23e1ae43ade77aea485a3f8`; HQ appointment; effective owner `6456fc57cbe05cdf69e63ef51fa6ca6198401c60`. No native grants.
**WRITE ONLY:** `WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/**`. No candidate/J/E edit.

## Fork-atomicity qualification of 7bf2da3

See `evidence/7bf_atomic/verification.json`.

| Command / check | Result |
|---|---|
| Preserved 30 reviewer tests | **30/30 passed** |
| Adjacent lineage-contract file | **5/5 passed** |
| Positive joined fork + cold | **passed** |
| Positive targetless fork parent/cold | **passed** |
| Author post-create receipt rollback test | **passed** |
| Empty fork, both sessions | **refused; before == after `['first_session','root']`; branch/lineage/store unchanged; verify true** |

The original RED is closed: `fork_alt("")` returns `FORK_REFUSED` with `FORK_BRANCH_EMPTY`, and the C12 store, selected branch, session metadata and lineage are unchanged in both `JoinedSession` and `RefusalSession`. Legitimate forks/cold reopening still pass. The candidate owns a pre-validate and SQLite SAVEPOINT implementation; no implementation edit was made by this reviewer.

| FINDING | CAUSAL INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| Invalid empty fork is atomic in both sessions. | Pre-validation rejects before `product.fork`; store and metadata remain unchanged. | `ACCEPT_SCOPED` for exact 7bf fork atomicity/shared lineage; stop. | JOIN-V independent; HQ adjudicates. |
| Legitimate nested/joined/targetless fork and cold behavior preserved. | Shared lineage receipts and parent isolation remain green. | Preserve. | JOIN-E + JOIN-V. |

**Exact-cut engineering verdict: ACCEPT_SCOPED.** Science remains TEST_ONLY/H0; authority remains none (no native C12/CAN/ADP/C8/Pyat/C11 or human A5). B-source remains bounded receiving-edge. No full 444-file recensus, provider call, native operation or self-adoption.

## Prior shared-lineage adjudication of 49022f6

See `LINEAGE_FINAL_ADJUDICATION.md`. Frozen hashes were checked first and unchanged.

| Suite against 49022f6 | Result |
|---|---|
| Preserved reviewer positives + hostiles + repaired + targetless | **30/30 passed** |
| Targeted c367 | 5/6; one historical E-first-refusal expectation |
| New lineage-contract tests | **4/5 passed; 1 failed** |
| JOIN-E own suite | **17/17 passed** |
| Inherited J / E / R30A | **8/8, 15/15, 10/10 passed** |
| Source manifest | **444/444 verified** |

**PASS:** shared `joined/lineage.py` in both sessions; fork receipts match actual branch rows with non-null clock/root/created fields; nested `first_session -> alt -> alt2` persists and cold-reopens; parent/sibling/root metadata switches are refused without product mutation; missing/tampered receipts and duplicate forks are refused without mutation; parent isolation, nonmutating targetless cold reopen, no target/grant, source/C12/C8, privacy/attention, joined encounter and B-source scope remain intact.

**FAIL:** `fork_alt("")` is refused (`FORK_REFUSED`) but leaves an empty `''` branch in the C12 store in both `JoinedSession` and `RefusalSession`; session metadata remains unchanged. This violates the requested invalid-request/partial-failure consistency.

**Verdict: REVISE.** One atomicity repair: validate the branch name before `product.fork`, or remove the created branch if lineage construction fails. Preserve the passing 30/30 and shared-lineage behavior.

## Prior targetless-repair adjudication of 75a134e

See `TARGETLESS_FINAL_ADJUDICATION.md`. Frozen hashes were checked first and unchanged.

| Suite against 75a134e | Result |
|---|---|
| Preserved reviewer positives | **10/10 passed** |
| Preserved reviewer hostiles | **7/7 passed** |
| Existing repaired-cut tests | **9/9 passed** |
| **Author-reported 26/26** | **independently reproduced 26/26 passed** |
| Targeted c367 tests | 5/6; one historical E-first-refusal expectation |
| New targetless-final tests | **1/4 passed; 3 failed** |
| JOIN-E own suite | **16/16 passed** |
| Inherited J / E / R30A | **8/8, 15/15, 10/10 passed** |
| Source manifest | **444/444 verified** |

**PASS:** coordinated targetless meta/sidecar source tampering is rejected against C12/C8 (`J_PROVENANCE_MISMATCH`); targetless cold reopen is nonmutating; no target/grant is fabricated; fork switches to `alt`, cold-reopens `alt`, and does not corrupt the parent; joined encounter/fork/attention/privacy/contact/cold remain green; E-first J closure adaptation is legitimate.

**FAIL:** the fork receipt records `fork_clock=null`/`root_hash=null` instead of the created branch's values; a forked session can be switched back to parent `first_session` by metadata alone and opens with `verify=true` in both targetless and joined paths. Exact reproducers: `test_refusal_fork_receipt_and_parent_integrity`, `test_refusal_parent_metadata_switch_refused`, `test_joined_parent_metadata_switch_refused`.

**Verdict: REVISE.** One coherent branch-lineage repair remains; the targetless source/C12, no-target and parent-integrity positives are preserved. B-source remains bounded receiving-edge, not original pre-C8 severance.

## Prior repaired-cut adjudication of cc0ff7d

See `REPAIRED_CUT_ADJUDICATION.md`. Frozen test hashes were checked first and were unchanged.

| Suite against cc0ff7d | Result |
|---|---|
| Frozen independent positives | **10/10 passed** |
| Frozen independent hostiles | **7/7 passed** |
| Targeted c367 tests | **5/6 passed**; one superseded E-first-refusal expectation |
| New repaired-cut tests | **6/9 passed; 3 failed** |
| JOIN-E own suite | **15/15 passed** |
| Inherited J / E / R30A | **8/8, 15/15, 10/10 passed** |
| Source manifest | **444/444 verified** |

The joined path is now fully green against the preserved hostile suite: canonical root, source actor map, C8/E1/target/C12 binding, branch/fork receipts, typed missing/orphan/moved roots, read-only cold reopen, full encounter, attention, privacy, contact and B ignorance all pass. E-first now successfully adapts to the J-first closure; the old targeted c367 test expecting E-first refusal is historical and superseded, not a defect.

The new targetless refusal path is **REVISE**:

- coordinated `session.json` + `refusal.json` source tampering opens with `verify=true` while C12 `GM01_REFUSAL` still contains the original source;
- metadata-only branch substitution to `root` opens with `verify=true`;
- `RefusalSession.fork_alt()` returns success but leaves the branch on `first_session` and records no lineage; cold reopen ignores `alt`.

The actual B refusal source is legitimate and bounded: zero tools, no performed inspection, `GM01_REFUSAL`, no target, `HELP_REFUSE`; share source gives `HELP_ACCEPT`. The independent receiving-edge fault/restore flips the same E consumer only through the tool read, not through original B pre-C8 replacement. No refusal=>help-accept claim is adopted; native/science remain HOLD.

## Prior final-cut adjudication of c367777

See `FINAL_CUT_ADJUDICATION.md` for the full table and evidence. Frozen test hashes were checked first and were unchanged.

| Suite against c367777 | Result |
|---|---|
| Frozen independent positives | **9 passed, 1 intentional import-contract refusal** |
| Frozen independent hostiles | **4 passed, 3 failed** |
| New targeted final-cut tests | **3 passed, 3 failed** |
| JOIN-E own suite | **10/10 passed** |
| Inherited J / E / R30A | **8/8, 15/15, 10/10 passed** |
| Source manifest | **444/444 verified** |

**Repaired:** different-source product root, plain R29P fallback/donor mutation, single-sidecar source tamper, moved-root refusal, lawful `fork_alt`, J-first import guard, and an independent B-source refusal/share witness.

**Still/new failures:** a same-source foreign product root is accepted; metadata-only branch selection (`root` and frozen `alt`) is accepted; double sidecar+meta source tampering is accepted while C12 `GM01_SOURCE` disagrees; missing session and orphan-root start still raise raw errors. The E-first frozen positive is now intentionally refused by the final import-closure contract; the frozen test is preserved unchanged and a new targeted J-first/E-first guard passes.

Final-cut engineering verdict: **REVISE**. Await the next repair SHA; keep the frozen tests unchanged and continue this lane.

## Four-column return (preliminary 13dfd6bad; final-cut deltas above)

| FINDING | INTERPRETATION AND RIVALS | HQ ACTION REQUESTED | COMPETENT OWNER |
|---|---|---|---|
| **F1. `open()` accepts a foreign product root, including a plain R29P root.** `session.json` supplies `product_root` and `branch_id` unchecked; `R31JProduct.reopen()` accepts a root with no `r31j_source`, no `r31j_actor_snapshot` and no `GM01_SOURCE`. | Counterexample: A (`omit`) repointed to B (`e2`) opens with `verify=true`, source `a_e2_performed=true`, tools 0, accepted help false, while A's meta still says `omit`. R29P donor opens with `source={}`, `pre_c9_binding={}`, `verify=true`, accepted help true; the donor `bp2_join.json` is mutated with five `r31j_*` keys. Alternative: canonical `state_root/product` and sealed branch required; missing J binding rejected. | REVISE before final acceptance. Require canonical root/branch, non-empty J binding, `GM01_SOURCE`, and no donor mutation on open. | JOIN-R implementer; J/E product owners; Sorok HQ adjudicates. |
| **F2. The persisted J source is a mutable sidecar, not C12-bound.** `R31JProduct.reopen()` reads `r31j_source` from `bp2_join.json`; `verify()` does not compare it with the C12 `GM01_SOURCE` episode. | Counterexample: edit `b_operation` to `REFUSE_TOOL`, quantity 0, actor labels to foreign values; `open()` succeeds, `verify=true`, accepted help true, while the C12 episode still says `SHARE_TOOL`, quantity 1, R31J actors. Normal source actor labels (`TEST_ONLY_R31J_A/B`) are a different namespace from product actor IDs (`TEST_ONLY_BP1_R26V_ACTOR_A/B`), with no documented mapping check. Alternative: use C12 episode/digest as source authority; enforce actor mapping. | REVISE: bind source to C12; make reopen read-only; reject sidecar disagreement or explicitize the actor map. | JOIN-R implementer; J source owner; C12 owner. |
| **F3. Branch substitution is accepted.** | Fork `alt`, rewrite `branch_id` to `alt`; `open()` succeeds, `verify=true`, accepted help true. The recorded `first_session` branch is not enforced. | REVISE: require the sealed `first_session` branch and a stored branch/root receipt. | JOIN-R implementer; R30A/BP4 owner. |
| **F4. Missing/orphan/moved roots are raw errors, not typed refusals.** | Missing `session.json` → raw `FileNotFoundError`; lost `session.json` with existing product → raw `RuntimeError: R31J_PREC9_REFUSED:c8_exclusive_append:C8_OCCURRENCE_NOT_ADMITTED`; moved session root → raw `ValueError: R31J_TIME_COORDINATE_HOLD`. `_attach_new` writes R30A metadata before join metadata, so a crash can leave an unrecoverable non-JOIN session. | Harden with `SessionRefusal(SESSION_NOT_FOUND)`, `SESSION_EXISTS__NO_AUTOMATIC_REROLL`/orphan refusal, and moved-root refusal or rebinding; clean partial startup. | JOIN-R implementer; BP2/C8 owner for the orphan case. |
| **F5. The author's two-test oracle is insufficient.** | `source['b_performed'] is True` is also true for B's `REFUSE_TOOL`; the test does not assert `b_operation=SHARE_TOOL`, `b_quantity=1`, `material_feasible_after`, source-to-episode equality, root/branch identity, or sidecar tamper. Candidate 2/2 passes only its narrow positive path. | Require the frozen hostile suite to pass or an explicit scoped waiver; do not promote 2/2 as the integration denominator. | JOIN-R implementer + independent reviewer; HQ accepts/rejects. |
| **F6. The untampered positive path works.** | E2/omit material edge, B refusal/share contrast, source-to-episode equality, repeated reopen without duplicate GM01/checkpoints, cold child reopen, attention-invariant speech, private/B ignorance, contact/no-contact, and normal-vs-E-first import order all pass independently (10/10). | Preserve these positives while repairing F1–F4. | JOIN-R implementer; HQ. |
| **F7. Cross-root source identity is not canonical.** | Two fresh `omit` roots have the same B/E1/C8 source hashes but different C9 target/consumed hashes and can select different `EXPLAIN_WORK` variants. In-place reopen preserves the root. The candidate records only a commit-level `j_source_ref`. | Clarify whether cross-root canonical identity is required; if so, bind a source-identity hash beyond the commit. | J source owner + JOIN-R implementer; HQ scope decision. |

## DONE / REMAINING / CRITICAL BLOCKER / LARGEST MOVE / FLIGHT / DELTA

- **DONE:** adjudicated exact fork-atomicity cut `7bf2da3`; reproduced 30/30 preserved reviewer tests, 5/5 lineage-contract tests, joined/targetless fork positives and the author post-create rollback test; demonstrated empty-fork no-change.
- **REMAINING:** none for this bounded fork-atomicity qualification; STOP. No polling, new worker or broad recensus.
- **CRITICAL BLOCKER:** none for the exact observed defect; sourcefree native/science limits remain external.
- **LARGEST MOVE:** none; `ACCEPT_SCOPED` for 7bf atomic fork/shared lineage.
- **FLIGHT:** one reviewer on `codex/sorok-join-v-20261022`; exact cut 7bf2da3 read-only; no candidate/J/E edits; no subagents/provider/native operations.
- **DELTA:** prior empty-fork RED is green in both sessions; legitimate fork/cold, 30/30 preserved tests and lineage contract remain green.

## Exact commands and results

Fork-atomicity cut `7bf2da3` (read-only worktree; exact candidate; no frozen test edited):

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<7bf worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1   PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py tests/test_join_v_hostile.py tests/test_join_v_repaired_cut.py tests/test_join_v_targetless_final.py -p no:cacheprovider --tb=short
30 passed

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_lineage_contract.py -p no:cacheprovider --tb=short
5 passed

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py::test_lawful_fork_alt_continuation_is_supported tests/test_join_v_targetless_final.py::test_refusal_fork_parent_not_corrupted_positive -p no:cacheprovider --tb=short
2 passed

cd <7bf worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join.py::test_fork_post_create_receipt_failure_rolls_back -p no:cacheprovider --tb=short
1 passed
```

Empty-fork evidence: both sessions refused with `FORK_REFUSED: FORK_BRANCH_EMPTY`; before/after branches both `['first_session', 'root']`; branch, lineage and store unchanged; `verify=true`. Full small evidence: `evidence/7bf_atomic/verification.json`.

Historical shared-lineage cut `49022f6` (read-only worktree; frozen tests unchanged; hashes checked first):

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<49022f6 worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py tests/test_join_v_hostile.py tests/test_join_v_repaired_cut.py tests/test_join_v_targetless_final.py -p no:cacheprovider
30 passed (author-reported 30/30 independently reproduced)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py -p no:cacheprovider --tb=short
5 passed, 1 failed (historical E-first-refusal expectation)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_lineage_contract.py -p no:cacheprovider --tb=short
4 passed, 1 failed (invalid empty fork leaves '' branch)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_lineage_final.py
candidate own 17/17; inherited 8/8, 15/15, 10/10; manifest 444/444
```

Frozen test hashes all match `FROZEN_ORACLES.json`; no frozen test file was edited. Full JUnit/JSON: `evidence/lineage_final/results.json`, `evidence/lineage_final/source.json`, and `evidence/lineage_final/*.xml`.

Passed on `49022f6`: shared lineage in both sessions; actual fork receipts/nested forks/cold; parent/sibling/root switch rejection; missing/tampered receipt and duplicate fork refusal; parent isolation; nonmutating targetless cold; no target/grant; source/C12/C8; privacy/attention; joined encounter; B-source bounded. Remaining: invalid empty fork partially mutates state by leaving an empty `''` branch.

## Frozen source hashes

| Artifact | SHA-256 |
|---|---|
| `joined/session.py` | `0562fb0405cbe1f989ec10e4ce865c54bc712559757c877342fc1d1d46027956` |
| `tests/test_join.py` | `ca57802caccce9d37547fb10f8c3df2595accb6b4e51d1d600d62b68153ca6fd` |
| `SOURCE_MANIFEST.json` | `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126` |
| `RESUME_CHECKPOINT.md` | `7c03d345bddb03bdb75e99a595dac68da9494890134f7db73c5b0002a63bcad2` |
| `tests/conftest.py` | `fbe854b8428f34350c2e913117c3084b27289e91a38b267fb4f3e628b8ab7c1f` |
| `tests/support.py` | `c72fcf595fe3965e132b9333053e694c3329fd14c7a9d252d649c5b237fec6fb` |
| `tests/test_join_v_positive.py` | `d2216223a02058b549857b632bf818d1814ccaa5b8e1191f4f312abeddb18b9b` |
| `tests/test_join_v_hostile.py` | `c57b57a442ffae915d0c0f8e06b3ac8543eee98a79be6dfe97e4c4ebf42464e3` |

`FROZEN_ORACLES.json` contains the full frozen test and candidate file hashes. Candidate source manifest `444/444`; J source ref `64fec28c374d8f77fb0b412d0c934d798ede03e8`; E source ref `a2760d3687b063513fe0a5b9589c56c998d4ccb5`.

Final-cut c367777 hashes (full list in `evidence/final_cut/source.json`):

| Artifact | SHA-256 |
|---|---|
| `joined/session.py` | `1c1276a047d116a6787824bdb48e2f9d24b28947fdb84778990639203dbf480a` |
| `joined/readonly.py` | `93e1885e35d078879228b38c716ac5ed0b14b91367433b19d19bf7d4535d2371` |
| `joined/closure.py` | `d4c5e46d64e03201c5379eba4a1f2aaa2ec53744ceb22e78395fef05f6e74ff4` |
| `joined/assertion.py` | `ec9a313b271cafc089eeb6353b11a2c74b4b3bac33431b53c830410ae98b9878` |
| `tests/test_join.py` | `87cc0ae9378be0375de1a6b35bd200a0cf158b425557ba8a7703927fc110ef7b` |
| `tests/test_join_v_final_cut.py` | `6e2f87d773090235a4a5f3567430737f30f16698397c852f799585ff73280de1` |
| `tools/collect_final_cut.py` | `fc9d3bed87c6eeade8292e90d6470128816cf27e9b6ee1a0886af2eaa3b41ac8` |

Repaired-cut cc0ff7d hashes (full list in `evidence/repaired_cut/source.json`):

| Artifact | SHA-256 |
|---|---|
| `joined/session.py` | `d7dbabf4f7be3516540f8c1035d4136f2efe61f1f0150b53565fb73aa3c9872f` |
| `joined/imports.py` | `2b49f6ebbbff2d5ca008d350306da229a4798f0f7c075312519d4209c6957cfd` |
| `joined/provenance.py` | `3618beca7997c5674ce6b7490ab600a891fbadbc38e49e4644928d6712c65c1b` |
| `joined/refusal.py` | `9fcd126783fec9bce79334b482a948cdaefcb4a07de04ebd16b967dfe17f3d8d` |
| `tests/test_join.py` | `932d570bf3d97233fda2d0705a221aa03657ee60532ccf932904e344021a9232` |
| `tests/test_join_v_repaired_cut.py` | `8a7ce8e61253ce6adb9286a4fb44f8ff26a7c851a28738fbacbe06df309f1028` |
| `tools/collect_repaired_cut.py` | `373171abd970c08301a1f013ca0525ca6ce716bd867216365be226d647e7a7ae` |

Targetless cut 75a134e hashes (full list in `evidence/targetless_final/source.json`):

| Artifact | SHA-256 |
|---|---|
| `joined/refusal.py` | `17e33bc0e5e37de92b8b9b56e190d7ee97235ff7c188c7923bd2b3868a5a5273` |
| `joined/session.py` | `d7dbabf4f7be3516540f8c1035d4136f2efe61f1f0150b53565fb73aa3c9872f` |
| `joined/imports.py` | `2b49f6ebbbff2d5ca008d350306da229a4798f0f7c075312519d4209c6957cfd` |
| `joined/provenance.py` | `3618beca7997c5674ce6b7490ab600a891fbadbc38e49e4644928d6712c65c1b` |
| `tests/test_join.py` | `26d7c69494037994c3ae5118a8cc91a251707b2ed4b93d9b5e5c0f596977f4bf` |
| `tests/test_join.py.proof.json` | `332f1c23d14e0511b181bf9529f9f630ba7e17b87fcae281478a69be170fe282` |
| `tests/test_join_v_targetless_final.py` | `f5411af4191188f0391dda2019225ab2856c798b2b5d101f2f66f4308473da66` |
| `tools/collect_targetless_final.py` | `ad0a8516a2899f37b396622df9260740743591bc9136e03f33e257b2ba8a7293` |

Shared-lineage cut 49022f6 hashes (full list in `evidence/lineage_final/source.json`):

| Artifact | SHA-256 |
|---|---|
| `joined/lineage.py` | `1c91852f934be58eb6c0250debbc615471469e4bf23a9c80b6d60deaa9308823` |
| `joined/session.py` | `f11e872dbe482b4e99fe93f2df6d86ca8f1803978c6ff1087a9cd00ff991361b` |
| `joined/refusal.py` | `0056dc54020044356f2fd572ebe7cc239c3d9ce029ddd219ca7726d7aff2a1e5` |
| `joined/imports.py` | `2b49f6ebbbff2d5ca008d350306da229a4798f0f7c075312519d4209c6957cfd` |
| `joined/provenance.py` | `3618beca7997c5674ce6b7490ab600a891fbadbc38e49e4644928d6712c65c1b` |
| `tests/test_join.py` | `08badee030b46b41d3cc2cf0cfe06686975f2937465102d359155bc31fb781f0` |
| `tests/test_join.py.proof.json` | `332f1c23d14e0511b181bf9529f9f630ba7e17b87fcae281478a69be170fe282` |
| `tests/test_join_v_lineage_contract.py` | `79fc117a21243e0f3d0c6316d95365244158d07787f8308eafa82741651e8751` |
| `tools/collect_lineage_final.py` | `fae35daace49228255fc62eaf9fda2f3518f842f97274f0cdead3f3a7b7c63cd` |

Fork-atomicity cut 7bf2da3 hashes:

| Artifact | SHA-256 |
|---|---|
| `joined/lineage.py` | `5578951d4dcce3839a114036684336fa759f537b62d8ed1174b0a6a0b03d7383` |
| `joined/session.py` | `ea820ec3e30a2825c3d0d8c5dc66e812afdda40b08f9cc0a8c868c8b3e0dd0da` |
| `joined/refusal.py` | `ca491610a62eda46159f006e7591872e6b31c55f287c4fe6162dbf061ddd984a` |
| `tests/test_join.py` | `8b5e6bb356ee85eca8a67d8a15093e339509e5964650e80fe7ca3b4d98dea81f` |
| V `tests/test_join_v_lineage_contract.py` | `79fc117a21243e0f3d0c6316d95365244158d07787f8308eafa82741651e8751` |

## Changed-path allowlist

Only:

```text
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/PRELIMINARY_FINDINGS.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/FINAL_CUT_ADJUDICATION.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/REPAIRED_CUT_ADJUDICATION.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/TARGETLESS_FINAL_ADJUDICATION.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/LINEAGE_FINAL_ADJUDICATION.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/RESUME_CHECKPOINT.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/FROZEN_ORACLES.json
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/tests/**
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/tools/**
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/evidence/**
```

No candidate, J, E, R30A, R29P, BP2P4J, C8, C12, C9, PRE-MAIN or HQ-control file changed. `git status` shows only this untracked return subtree.

## NOT_RUN

- Next repair SHA: `NONE` for the exact observed defect; bounded 7bf qualification is closed. No polling.
- Full inherited R31J/R31E/R29P 155–202 denominators: not promoted; no broad recensus performed for this bounded qualification.
- Process-kill crash injection beyond the author receipt-failure test: not performed; not needed for the exact empty-fork defect.
- Protected C12/KMS custody, native CAN/ADP/C8/C9/C11/Pyat, external provider calls, human A5, production/deployment: `NOT_RUN`; no authority.
- Cross-root canonical identity and all J variants/scenarios: not imposed; HQ intake explicitly says distinct roots need not have identical target IDs/histories/variants.
- End-to-end original B pre-C8 severance beyond the bounded receiving edge: not proven; unchanged.

## Courts

| Court | Fork-atomicity cut 7bf2da3 | Ceiling |
|---|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED` | Exact empty-fork atomicity now refuses before mutation in both sessions; store, branch, metadata and lineage unchanged; 30/30 preserved tests, 5/5 lineage tests, joined/targetless fork+cold and author receipt rollback pass. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | TEST_ONLY sourcefree; B-source bounded receiving-edge; no original pre-C8 severance, acquired practice, psychology, personhood or A5. |
| **AUTHORITY** | `HOLD` | No native C12/CAN/ADP/C8/C11/Pyat, protected keys, external provider or human A5 grant. |

## Publication

Substantive return commit and exact ordinary non-force remote head are reported in the worker's final response and verified with `git ls-remote` after push. No force/reset, no candidate edit, no self-adoption.
