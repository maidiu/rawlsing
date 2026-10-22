# SOROK JOIN-V — independent hostile causal and persistence return

**STATUS:** `FINAL_CUT_REVISE__c367777__PERSISTENCE_ROOT_BRANCH_C12_SOURCE_NOT_PROVEN__AWAIT_NEXT_REPAIR_SHA`
**ROLE:** independent hostile engineering reviewer; not JOIN-E, J, E, Sorok HQ, native C12/CAN/ADP/Pyat/C11 or human A5 authority.
**BRANCH:** `codex/sorok-join-v-20261022`
**STARTUP:** `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`
**PRELIMINARY CANDIDATE:** `13dfd6bad54ec19b4bdf31159e54fb6052d5440d`
**FINAL CUT:** `c367777f83367240352c267a2d3750abb7f09397` (read-only detached worktree)
**AUTHORITY:** independent accession `3de081023406a52ec23e1ae43ade77aea485a3f8`; HQ appointment; effective owner `6456fc57cbe05cdf69e63ef51fa6ca6198401c60`. No native grants.
**WRITE ONLY:** `WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/**`. No candidate/J/E edit.

## Final-cut adjudication of c367777

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

- **DONE:** froze the preliminary candidate and oracles, adjudicated the final E cut `c367777`, reran all frozen positives/hostiles and new targeted tests, verified unchanged frozen hashes, audited the 444-file source manifest and J-first import closure, ran candidate/inherited suites, and inspected E's mutation witness.
- **REMAINING:** next repair SHA from human/HQ; rerun the same frozen tests plus the targeted final-cut tests; final verdict. No polling and no second worker.
- **CRITICAL BLOCKER:** c367777 still accepts a same-source foreign product root, metadata-only branch selection, and double sidecar+meta source tampering that disagrees with persisted C12; missing/orphan roots remain raw failures.
- **LARGEST MOVE:** bind `open()` to canonical root/branch receipts and C12 `GM01_SOURCE` lineage, then add typed missing/orphan refusals and rerun the same suite.
- **FLIGHT:** one reviewer on `codex/sorok-join-v-20261022`; final cut c367777 read-only; no candidate/J/E edits; no subagents/provider/native operations.
- **DELTA:** final-cut engineering verdict is `REVISE`; four preliminary hostile failures are repaired, three frozen and three targeted final-cut counterexamples remain, while the author's 10/10 positives, lawful fork, B-source witness and inherited suites are preserved.

## Exact commands and results

Final cut `c367777` (read-only worktree; frozen tests unchanged; hashes checked first):

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<c367777 worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py -p no:cacheprovider
9 passed, 1 failed (E-first IMPORT_CLOSURE_INVALID; superseded by targeted closure guard)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_hostile.py -p no:cacheprovider --tb=short
4 passed, 3 failed (metadata-only alt branch, missing session, orphan root)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py -p no:cacheprovider --tb=short
3 passed, 3 failed (root branch metadata, same-source foreign root, double sidecar+meta source)

SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_final_cut.py
candidate own 10/10; inherited 8/8, 15/15, 10/10; manifest 444/444
```

Frozen test hashes all match `FROZEN_ORACLES.json`; no frozen test file was edited. Full JUnit/JSON: `evidence/final_cut/results.json`, `evidence/final_cut/source.json`, and `evidence/final_cut/*.xml`. The original preliminary evidence remains in `evidence/test_results.json` and `evidence/hostile.xml`.

Repaired on the final cut: different-source product root, R29P donor fallback/mutation, single-sidecar source tamper, moved-root refusal, lawful `fork_alt`, J-first import guard, and an independent B-source refusal/share witness. Still failing/new: same-source foreign product root, metadata-only branch selection, double sidecar+meta source tampering not bound to C12, missing session, orphan root.

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

## Changed-path allowlist

Only:

```text
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/PRELIMINARY_FINDINGS.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/FINAL_CUT_ADJUDICATION.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/RESUME_CHECKPOINT.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/FROZEN_ORACLES.json
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/tests/**
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/tools/**
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/evidence/**
```

No candidate, J, E, R30A, R29P, BP2P4J, C8, C12, C9, PRE-MAIN or HQ-control file changed. `git status` shows only this untracked return subtree.

## NOT_RUN

- Next repair SHA after c367777: `PENDING`; final verdict waits for that immutable cut.
- Full inherited R31J/R31E/R29P 155–202 denominators: not promoted; only 8 + 15 + 10 affected suites rerun on the final cut.
- Process-kill crash injection between `_attach_new` and join-meta write: inferred, not injected.
- Protected C12/KMS custody, native CAN/ADP/C8/C9/C11/Pyat, external provider calls, human A5, production/deployment: `NOT_RUN`; no authority.
- Cross-root canonical identity and all J variants/scenarios: not imposed; HQ intake explicitly says distinct roots need not have identical target IDs/histories/variants. No cross-root determinism failure is claimed.

## Courts

| Court | Final cut c367777 | Ceiling |
|---|---|---|
| **ENGINEERING** | `REVISE` | c367777 repairs four preliminary failures and preserves the positive encounter/fork/attention/import/closure and B-source witness, but same-source foreign roots, metadata-only branch selection, double sidecar+meta source disagreement with C12, and missing/orphan raw failures remain. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | TEST_ONLY sourcefree material feasibility and structured expression only; B refusal is a lawful no-tool/no-target boundary, not a help-accept claim; no psychology, acquired practice, personhood or A5. |
| **AUTHORITY** | `HOLD` | No native C12/CAN/ADP/C8/C11/Pyat, protected keys, external provider or human A5 grant. |

## Publication

Substantive return commit and exact ordinary non-force remote head are reported in the worker's final response and verified with `git ls-remote` after push. No force/reset, no candidate edit, no self-adoption.
