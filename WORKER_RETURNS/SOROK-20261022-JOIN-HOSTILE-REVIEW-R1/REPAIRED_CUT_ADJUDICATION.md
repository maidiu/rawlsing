# JOIN-V adjudication — repaired JOIN-E cc0ff7d

**STATUS:** `REPAIRED_CUT_REVISE__cc0ff7d__TARGETLESS_REFUSAL_PERSISTENCE_LINEAGE_AND_FORK_NOT_BOUND__AWAIT_NEXT_REPAIR_SHA`
**CANDIDATE:** `cc0ff7d0305340b806ba94b020017c3d8d0585dc` (read-only detached worktree)
**PREVIOUS CUT:** `c367777f83367240352c267a2d3750abb7f09397`
**BRANCH:** `codex/sorok-join-v-20261022`
**CONTINUATION:** `0445059a81d0882bc6d1488150697d00f044bd39:.../continuations/04_JOIN_V_REPAIRED_EXACT_CUT.md`
**WRITE SCOPE:** own return only. No candidate/J/E edit.

## Verdict

The repaired joined path is now green against the full preserved hostile suite: all seven previous lineage/persistence counterexamples pass, all ten frozen positives pass, the positive encounter/fork/attention/private/contact/cold behavior is preserved, and the 444-file source manifest is unchanged. The import-order repair is a legitimate improvement: E-first now clears and installs the J-first closure, so the old targeted c367 expectation that E-first must be refused is superseded, not a candidate defect.

The **new targetless refusal path** is not yet persistence- or lineage-bound. Three independent attacks fail on cc0ff7d:

1. coordinated `session.json` + `refusal.json` source tampering is accepted while the C12 `GM01_REFUSAL` episode still carries the original source;
2. a metadata-only branch rewrite to `root` is accepted;
3. `RefusalSession.fork_alt()` returns success but leaves the session on `first_session`; the fork is a silent no-op and cold reopen ignores `alt`.

The targetless path does preserve the legitimate no-tool/no-target behavior: actual B `REFUSE_TOOL` gives zero tools, no performed inspection, `GM01_REFUSAL`, `target_id=""`, no fabricated target, E `HELP_REFUSE`, and no refusal=>help-accept claim. A bounded receiving-edge fault/restore reproduces the E B witness exactly: with source still `REFUSE_TOOL`, forcing the tool state to 1 flips the same E consumer to `HELP_ACCEPT`; restoring a fresh refusal gives `HELP_REFUSE`. This is valid **receiving-edge** evidence, not end-to-end original B pre-C8 severance.

**Final-cut engineering verdict: REVISE.** Only the targetless persistence/lineage/fork path needs the next coherent repair; the joined path should be preserved.

## Results

Frozen test hashes were checked first and all match `FROZEN_ORACLES.json`; no frozen test was edited.

| Suite | Result |
|---|---|
| Frozen independent positives | **10/10 passed** |
| Frozen independent hostiles | **7/7 passed** |
| Targeted c367 tests | **5/6 passed**; the one failure is the superseded E-first-refusal expectation |
| New repaired-cut tests | **6/9 passed; 3 failed** |
| JOIN-E own suite | **15/15 passed** |
| Inherited J / E / R30A | **8/8, 15/15, 10/10 passed** |
| Source manifest | **444/444 verified**, 0 missing, 0 mismatched |

Old targeted failure: `test_import_closure_refuses_e_first_and_accepts_j_first` expected E-first to fail. cc0ff7d's `joined/imports.py` deliberately clears the E-first closure and installs J-first, so E-first now succeeds with J closure. The original test remains unchanged; new `test_e_first_import_adaptation_uses_j_closure` passes and verifies J closure. This is a legitimate import adaptation, not a defect.

New repaired-cut failures:

- `test_refusal_coordinated_meta_sidecar_source_tamper_refused_or_c12_bound`
- `test_refusal_metadata_only_branch_substitution_refused`
- `test_refusal_fork_continuation_or_typed_refusal`

New repaired-cut passes include actual targetless source/no-target behavior, targetless cold reopen/nonmutation, B refusal/share same-omission consumer, receiver-edge fault/restore, private/attention/B ignorance, typed missing/orphan/moved/donor roots, and E-first J closure.

## Claim coverage

| Claim | Status | Evidence |
|---|---|---|
| Joined path canonical root, source actor map, C8/E1/target/C12 binding | **PASS** | All seven frozen hostiles and all ten frozen positives pass; `joined/provenance.py` and `joined/session.py` guards exercised. |
| Legitimate joined `fork_alt`, authorized branch, metadata-only branch rejection | **PASS** for joined path | Frozen branch test and lawful-fork positive pass. |
| Joined typed missing/orphan/moved roots, no donor mutation | **PASS** | Frozen hostiles and positive cold/reopen suite pass. |
| Joined positive encounter, attention, privacy, B ignorance, contact, cold | **PASS** | Ten frozen positives pass. |
| E-first/J-first import closure adaptation | **PASS** | New test verifies E-first now uses J closure; old c367 refusal test is historical/superseded. |
| Actual B refusal source to targetless E consumer, no target/no tool | **PASS_SCOPED_RECEIVING_EDGE** | `RefusalSession.start`: source REFUSE, tools 0, no INSPECT, `GM01_REFUSAL`, `target_id=""`, E `HELP_REFUSE`; share source E `HELP_ACCEPT`; no refusal=>accept claim. |
| Bounded receiving-edge fault/restore | **PASS_SCOPED** | Forcing tool 1 under source REFUSE flips E to `HELP_ACCEPT`; fresh refusal restores `HELP_REFUSE`; not end-to-end B pre-C8. |
| Targetless source/C12/keyed-source persistence | **FAIL** | Coordinated meta+sidecar source tamper opens with `verify=true` while C12 `GM01_REFUSAL` disagrees; loaded source is foreign. |
| Targetless branch authorization | **FAIL** | Metadata-only `branch_id="root"` opens with `verify=true`. |
| Targetless fork | **FAIL** | `fork_alt()` returns OK, leaves `branch_id=first_session` and no lineage; cold reopen remains first_session. |
| Targetless target/grant semantics | **NO FABRICATED TARGET** | `target_id=""`, `targetless=true`, C9 `NO_CHANGE`/`NO_PROPOSAL`, `native_grants` all false; `c9.grant_id=TEST_ONLY_BP2_TARGET_GRANT` is an inherited C9 field, not a new native grant. |
| Refusal=>help acceptance | **NOT CLAIMED** | No-tool refusal is preserved; no DEV-R acceptance oracle adopted. |
| Native/science | **HOLD** | No native grants, science issuance, acquired practice, psychology or A5. |

## Failure details

### R1. Targetless source is not bound to C12/C8

`RefusalSession.open()` reads `meta["j_source"]` and `product/refusal.json`, compares them to each other, then verifies only the C12 chain. It never re-reads the C12 `GM01_REFUSAL` source or the keyed C8 source. Coordinated tamper result:

```json
{"case": "refusal_coordinated_source_tamper",
 "opened": true,
 "meta_matches_sidecar": true,
 "loaded_b_actor": "FOREIGN_B",
 "loaded_b_to_actor": "FOREIGN_A",
 "loaded_b_event_hash": "FOREIGN_HASH",
 "episode_b_actor": "TEST_ONLY_R31J_B",
 "episode_b_to_actor": "TEST_ONLY_R31J_A",
 "episode_b_event_hash": "3e00199d533b793897cd8b9bdc0639830252c60588de732b46dfcec3cc3b9421",
 "verify": true,
 "targetless": true}
```

The source path is label/meta/sidecar-bound, not C8/C12-bound. This is the refusal-path analogue of the joined-side finding that cc0ff7d repaired.

### R2. Targetless branch substitution is accepted

After a valid refusal start, a copy with canonical `product_root`, `meta["branch_id"]="root"` opens successfully:

```json
{"case": "refusal_metadata_branch", "opened": true,
 "branch_id": "root", "recorded_branch_id": "first_session", "verify": true}
```

`RefusalSession.open()` has no branch-lineage receipt or sealed-branch check. The root branch is a valid C12 branch, so C12 verification does not distinguish authorized session branch from metadata substitution.

### R3. Targetless fork is a silent no-op

`RefusalSession` inherits `FirstSession.fork_alt()`. It creates an `alt` C12 branch but does not switch `branch_id`, write `meta["branch_id"]`, or record lineage. Result: `fork_alt()` returns `OK`, session remains `first_session`, and cold reopen remains `first_session`. A caller cannot tell whether a fork was created as product behavior or ignored. This must be either a real persisted fork (same semantics as `JoinedSession.fork_alt`) or a typed refusal.

## B-source proof scope

- **A-action witness:** `test_material_omission_vs_e2_changes_help_without_patch` is narrow A performed/omitted action dependence; preserved.
- **E B witness:** `test_b_source_edge_help_observable_and_targetless_no_target` plus the `_RefusalSeed` fault mutates the source-to-tools read. It proves a generating/decoder receiving edge: source `material_feasible_after` -> tools -> E help admission. It does not prove original B pre-C8 event replacement through C8/C9 into the targetless C12.
- **Independent B check:** actual share source -> E `HELP_ACCEPT`; actual refusal source -> tools 0, `GM01_REFUSAL`, E `HELP_REFUSE`; no target; no refusal=>accept. Bounded fault/restore flips/restores the same consumer through the tool read. This supports the bounded claim, not the broader upstream severance.
- **C12 provenance:** false for the targetless path as shown by R1; a source-derived behavioral witness cannot repair persistence by itself.

## Source and test hashes

- Candidate commit: `cc0ff7d0305340b806ba94b020017c3d8d0585dc`.
- `joined/session.py`: `d7dbabf4f7be3516540f8c1035d4136f2efe61f1f0150b53565fb73aa3c9872f`.
- `joined/imports.py`: `2b49f6ebbbff2d5ca008d350306da229a4798f0f7c075312519d4209c6957cfd`.
- `joined/provenance.py`: `3618beca7997c5674ce6b7490ab600a891fbadbc38e49e4644928d6712c65c1b`.
- `joined/refusal.py`: `9fcd126783fec9bce79334b482a948cdaefcb4a07de04ebd16b967dfe17f3d8d`.
- `joined/readonly.py`: `93e1885e35d078879228b38c716ac5ed0b14b91367433b19d19bf7d4535d2371`.
- `tests/test_join.py`: `932d570bf3d97233fda2d0705a221aa03657ee60532ccf932904e344021a9232`.
- `tests/test_join.py.proof.json`: `4b19724321d3eec3908ab538d007923b5c1429a88fb5d020f1c3ff77b41b0581`.
- New repaired test: `tests/test_join_v_repaired_cut.py` hash `8a7ce8e61253ce6adb9286a4fb44f8ff26a7c851a28738fbacbe06df309f1028`.
- Targeted c367 test hash (unchanged): `6e2f87d773090235a4a5f3567430737f30f16698397c852f799585ff73280de1`.
- Frozen test hashes: unchanged and verified (`FROZEN_ORACLES.json`).
- `SOURCE_MANIFEST.json`: 444/444; no vendor edits.

## Exact commands

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<cc0ff7d worktree>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py -p no:cacheprovider
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_hostile.py -p no:cacheprovider --tb=short
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py -p no:cacheprovider --tb=short
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_repaired_cut.py -p no:cacheprovider --tb=short
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_repaired_cut.py
```

Evidence: `evidence/repaired_cut/results.json`, `evidence/repaired_cut/source.json`, and `evidence/repaired_cut/*.xml`.

## Courts

| Court | Verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `REVISE` | Joined path is repaired and green; targetless refusal path still accepts coordinated source substitution, metadata-only branch substitution, and a silent no-op fork; targetless source is not C12/C8-bound. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | B source witness is bounded receiving-edge and no-tool/no-target; no refusal=>help acceptance, acquired practice, psychology, personhood or A5. |
| **AUTHORITY** | `HOLD` | No native CAN/ADP/C8/C12/Pyat/C11/C5, protected keys, external provider or human A5. |

## Next coherent repair

One repair focused on `joined/refusal.py`:

1. Use a read-only targetless product/reopen that does not write or replay C12 on cold open; preserve the current nonmutating behavior.
2. Bind `session.json` and `refusal.json` source, actor map and C8/E1 receipt to the persisted C12 `GM01_REFUSAL` and keyed C8 source; reject coordinated meta/sidecar substitution.
3. Enforce canonical targetless root and sealed branch lineage; reject metadata-only branch selection.
4. Implement a real targetless `fork_alt` with branch/meta/lineage, or a typed `FORK_UNSUPPORTED` refusal; do not return success on a no-op.
5. Keep no fabricated target/native grant and document the inherited C9 `TEST_ONLY_BP2_TARGET_GRANT` field; continue to refuse with zero tools rather than adopting refusal=>help acceptance.

Then rerun all frozen positives/hostiles, targeted c367 tests, repaired-cut tests and the candidate/inherited suites on the next exact SHA. No polling; same lane.
