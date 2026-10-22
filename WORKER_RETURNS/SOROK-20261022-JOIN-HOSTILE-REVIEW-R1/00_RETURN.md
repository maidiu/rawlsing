# SOROK JOIN-V — independent hostile causal and persistence return

**STATUS:** `PRELIMINARY_REVISE__ROOT_LINEAGE_AND_SOURCE_BINDING_NOT_PROVEN__FINAL_VERDICT_PENDING_JOIN_E_EXACT_SHA`
**ROLE:** independent hostile engineering reviewer; not JOIN-E, J, E, Sorok HQ, native C12/CAN/ADP/Pyat/C11 or human A5 authority.
**BRANCH:** `codex/sorok-join-v-20261022`
**STARTUP / CANDIDATE:** startup `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`; candidate `13dfd6bad54ec19b4bdf31159e54fb6052d5440d`
**AUTHORITY:** independent accession `3de081023406a52ec23e1ae43ade77aea485a3f8`; HQ appointment; effective owner `6456fc57cbe05cdf69e63ef51fa6ca6198401c60`. No native grants.
**WRITE ONLY:** `WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/**`. No candidate/J/E edit.

## Four-column return

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

- **DONE:** froze the candidate, built independent positive and hostile tests, froze test/source hashes, ran candidate/inherited suites, audited import closure and 444-file source manifest, and published preliminary findings.
- **REMAINING:** exact JOIN-E return SHA; rerun the same frozen tests on that immutable cut; final verdict. No polling and no second worker.
- **CRITICAL BLOCKER:** final candidate SHA does not yet exist in this review; this blocks only the final verdict, not the preliminary source/oracle work.
- **LARGEST MOVE:** bind `open()`/`reopen()` to the canonical root, branch and C12 source; then rerun the frozen suite.
- **FLIGHT:** one reviewer on `codex/sorok-join-v-20261022`; candidate `13dfd6bad`; no candidate/J/E edits; no subagents/provider/native operations.
- **DELTA:** preliminary engineering verdict changed from the author's 2/2 green to `PRELIMINARY_REVISE` on lineage/source persistence, while preserving the real single-root material/encounter positives.

## Exact commands and results

Candidate author suite:

```text
python3 -B -m pytest -q WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py -p no:cacheprovider
2 passed
```

Independent positives (cwd own return):

```text
python3 -B -m pytest -q tests/test_join_v_positive.py -p no:cacheprovider
10 passed
```

Independent hostile (cwd own return):

```text
python3 -B -m pytest -q tests/test_join_v_hostile.py -p no:cacheprovider --tb=short
7 failed
```

Failures are the intended lineage/persistence counterexamples, not construction failures: `different_product_root`, `r29p_product_root`, `tampered_branch_id`, `tampered_r31j_source`, `missing_session`, `orphan_product_root_start`, `relocated_session_root`. Full JSON and failure text: `evidence/test_results.json`, `evidence/hostile.xml`.

Inherited provenance (separate processes, candidate worktree):

```text
(cd .../vendor/j && python3 -B -m pytest -q tests/test_r31j.py -p no:cacheprovider)
8 passed
(cd .../vendor/e && python3 -B -m pytest -q tests/test_r31e_expression.py -p no:cacheprovider)
15 passed
(cd .../vendor/e/vendor/r30a && python3 -B -m pytest -q tests/test_r30a_first_session.py -p no:cacheprovider)
10 passed
```

Freeze and evidence:

```text
python3 -B tools/freeze.py
444/444 source-manifest rows verified; 0 missing; 0 mismatched
python3 -B tools/collect_results.py
candidate 2/2; positive 10/10; hostile 0/7; inherited 8/8, 15/15, 10/10
python3 -B tools/import_audit.py
normal and E-first common closures byte-identical; behaviour identical
```

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

## Changed-path allowlist

Only:

```text
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/PRELIMINARY_FINDINGS.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/RESUME_CHECKPOINT.md
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/FROZEN_ORACLES.json
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/tests/**
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/tools/**
WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/evidence/**
```

No candidate, J, E, R30A, R29P, BP2P4J, C8, C12, C9, PRE-MAIN or HQ-control file changed. `git status` shows only this untracked return subtree.

## NOT_RUN

- Final JOIN-E candidate and exact return SHA: `PENDING`.
- Full inherited R31J/R31E/R29P 155–202 denominators: not promoted; only 8 + 15 + 10 affected suites rerun.
- Process-kill crash injection between `_attach_new` and join-meta write: inferred, not injected.
- Protected C12/KMS custody, native CAN/ADP/C8/C9/C11/Pyat, external provider calls, human A5, production/deployment: `NOT_RUN`; no authority.
- Cross-root canonical identity and all J variants/scenarios: not exhaustive; partial observation only.

## Courts

| Court | Preliminary | Ceiling |
|---|---|---|
| **ENGINEERING** | `PRELIMINARY_REVISE` | The real single-root material/encounter path works, but lineage, branch and sidecar source binding are not proven; foreign root/R29P acceptance and donor mutation are concrete counterexamples. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | TEST_ONLY sourcefree material feasibility and structured expression only; no psychology, acquired practice, personhood or A5 claim. |
| **AUTHORITY** | `HOLD` | No native C12/CAN/ADP/C8/C11/Pyat, protected keys, external provider or human A5 grant. |

## Publication

Substantive return commit and exact ordinary non-force remote head are reported in the worker's final response and verified with `git ls-remote` after push. No force/reset, no candidate edit, no self-adoption.
