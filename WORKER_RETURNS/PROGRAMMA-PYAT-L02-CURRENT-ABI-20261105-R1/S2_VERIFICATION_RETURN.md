# PROGRAMMA PYAT L02 — S2 local executable verification return

**Role:** I3+ bounded local executable verifier / exact-head implementation-return worker. This is not the independent R02 receiving review, not original scientific issuance, not protected PRE-MAIN CAS merge authority, and not an actor/authority grant.

**Disposition:** `S2_VERIFIED_READY_FOR_INDEPENDENT_R02_REREVIEW`

**Delivery:** committed as `WORKER_RETURNS/PROGRAMMA-PYAT-L02-CURRENT-ABI-20261105-R1/S2_VERIFICATION_RETURN.md` on top of exact verified head `2123d0b9…`; the return commit changes only this document.

## Exact custody

- PR #703 head (`refs/pull/703/head`) at verification time: `2123d0b9ba71ac02debc90c06861dd66dc563261` — exact required repair head.
- PR #703 merge ref `940b3207003200ddcc1903e382e09d8a76a6a29d`; first parent `33c40a315d3c231cb2021bd8e60f3261547efa62`, second parent `2123d0b9…`. Therefore the live protected PRE-MAIN base is `33c40a315d3c231cb2021bd8e60f3261547efa62` (independently fetched with `git ls-remote`).
- Original branch base: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` (ancestor of the candidate).
- Isolated detached sparse worktree at `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/l02-s2-verify`; HEAD `2123d0b9…`; worktree clean before and after execution. No branch reset, merge, rebase, or protected-base operation was performed.
- Environment: CPython 3.11.3 / pytest 9.0.2 / pandas 2.3.1 / numpy 2.3.2 / pyreadstat 1.3.2 in an isolated venv. (The global interpreter had pytest 9.1.1/pandas 3.0.6 and no pyreadstat; one initial source-projection run exposed three child-process `ModuleNotFoundError: pyreadstat` failures, not L02 behavior. The documented exact environment then produced the results below.)
- Canonical checker identity: `CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py` is git blob `461c8ac0e25ad2078f834ad3071fc1499b140ca1` (SHA-256 `e3125e121babb6f522688e050b1840f514e04796b47fdab81c5d40b140f858ed`) at `8ffec40…`, `9200d360…`, `2123d0b9…`, and protected `33c40a315…` — identical.

## Repair-diff verification

`git diff --name-status 9200d36077b8fdcdb251b68595009bf817050849 2123d0b9ba71ac02debc90c06861dd66dc563261`:

```
M  rawlsing_next/tests/test_l02_joint_receipt_selection.py
A  rawlsing_next/tests/test_l02_joint_receipt_selection.py.proof.json
```

Only those two paths changed relative to `9200d360…`. The test file has four named cases (no parameterized JUnit names): `test_declared_joint_selected_when_marginal_first`, `test_declared_joint_selected_when_joint_first`, `test_missing_declared_joint_never_substitutes_a_supported_marginal`, `test_ambiguous_primary_queries_refuse_instead_of_choosing_first`. The two positive cases retain `assert actual is joint` and `assert actual_query is query`; the two negatives retain their `pytest.raises(DiscoveryConsumptionMismatch)` assertions. No production C1/C11/I03/I05/Batch/Q86/Sorok/R01/R03 or protected code is in this repair diff.

The branch's sole production change is the already-committed C1 consumer repair in `rawlsing_next/pre553_analytical_composition.py` (`beffc445a…`), unchanged at `9200d360…` and `2123d0b9…`: git blob `875e5e2ce4303b9a8eac7437a4894af5e543bdf1`, file SHA-256 `b750e992bd60c48e66070f127b30243c39d1e2a5aebbca2cbbe1a4e956f4cb17`, 61,469 bytes. Test-file SHA-256 `5210fcd6814159834c76c6b0a3de397fb4d107bd72f9574898b55d4598e43a2a`; witness-contract SHA-256 `43afdb27afd2664aac93262f793c401639327d8dba3cebeb1fb808b01360c4f7`.

## Proof-integrity witnesses

Command:

```sh
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  rawlsing_next/tests/test_l02_joint_receipt_selection.py.proof.json --root .
```

Both claims returned `baseline: PASS` / `fault_probe: TARGET_ASSERTION_FAILED` / `grade: BOUNDED_MUTATION_DETECTED`:

- `PROGRAMMA_PYAT_L02_I05_JOINT_PRIMARY_QUERY_MARGINAL_FIRST_SEVERANCE_R1`
- `PROGRAMMA_PYAT_L02_I05_JOINT_PRIMARY_QUERY_JOINT_FIRST_SEVERANCE_R1`

The declared fault inverts the actual primary-query filter (`query_ref not in primary_queries` → `query_ref in primary_queries`). An independent manual mutant run showed both positive orderings select `urn:test:l02:marginal-fact` and fail at `assert actual is joint` (test line 36), not at a later or unrelated assertion. The production file was restored byte-for-byte after every witness run.

Governed changed-test checks were executed with the canonical checker against both bases:

```sh
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed --root . \
  --base 8ffec40a6924848a49f95950aa9ce28c27ee3ec1 --head 2123d0b9ba71ac02debc90c06861dd66dc563261
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed --root . \
  --base 33c40a315d3c231cb2021bd8e60f3261547efa62 --head 2123d0b9ba71ac02debc90c06861dd66dc563261
```

Both returned `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION`, examined only `test_l02_joint_receipt_selection.py`, ran one witness contract, and passed both claims. Elapsed: ~2 s each. Production file SHA-256 remained `b750e992…` after each.

## Executed current-source suites

```sh
python3 -m pytest -q rawlsing_next/tests/test_l02_joint_receipt_selection.py \
  rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py
```
`39 passed` in 6.35 s (4 L02 + 35 retained higher-order).

```sh
python3 -m pytest -q rawlsing_next/tests/test_universal_grammar.py \
  rawlsing_next/tests/test_universal_workload.py
```
`48 passed` in 122.46 s.

```sh
python3 -m pytest -q rawlsing_next/tests/test_universal_source_projection.py
```
`31 passed` in 9.92 s in the exact environment.

Extended C1-related regression suite (analytical composition, replay dependency, state/route, empirical possibility provider, N9/N10W progressive candidate, learned consumer, world binding):

```sh
python3 -m pytest -q \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  rawlsing_next/tests/test_pre553_analytical_replay_dependency.py \
  rawlsing_next/tests/test_pre553_analytical_state_and_route.py \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_universal_world_binding.py
```
`237 passed` in 322.40 s; no skips. (The first run in a deliberately sparse custody worktree lacked checked-in `WORKER_RETURNS` fixtures and produced fixture `FileNotFoundError`s; after adding the repository's own fixture tree, the same command passed 237/237. That was a custody artifact, not candidate behavior.)

## First-consumer and source-response replay

Checked-in scripts were executed in place with `PYTHONPATH=.`; generated differences were inspected and the tracked worktree was restored to HEAD afterward.

`probe_conditioned.py` stdout:

```json
[{"direction": "FORWARD", "selected": 2, "states": ["SUPPORTED"]},
 {"direction": "REVERSE", "selected": 48, "states": ["SUPPORTED"]}]
```

(The printed `states` are lowering states.) Fresh ledger facts: forward D=1 arity-3 joint has `raw_denominator_support=12` and four positive XOR cells `(0,0,0),(0,1,1),(1,0,1),(1,1,0)` at count 3 each, four observed zeros; forward D=0 arity-3 joint has denominator 4 with four positive cells at count 1. Reverse selected 48 conditional operations all show `lowering_status=SUPPORTED` and `result_state=VALID_EMPTY`.

`probe_first_reader.py` stdout: `FORWARD EXACT_SUPPORTED`, `REVERSE EXACT_SUPPORTED`. Its regenerated `probe_first_reader.json` is byte-identical to the checked-in trace: SHA-256 `53c45586c05799233704eb7d57af447322eb531bc73762cd48527027ad4a585b`. Forward consumer geometry: denominator 12, four positive cells at 3; reverse consumer geometry: denominator 4, cells `0→1`, `1→3`.

Inverse I05 distinction: all 246 `DISTRIBUTION_DIFFERS_FROM_BASELINE` validation receipts are `VALID_EMPTY` / `EVALUATED_VALID_EMPTY`; all 48 selected inverse conditional operations expose `result_state=VALID_EMPTY`. The only two supported inverse receipts are `TARGET_CELL_SUPPORTED` for cells 0 and 1, which are the ordinary conditional route consumed directly by E41/C1/N10E; consequently the whole discovery object's `valid_empty` boolean is `False`, but no distribution departure is relabeled and the underlying measured conditional remains separately supported. The I05 validation result remains `VALID_EMPTY`.

Six source/condition/occurrence negative mutations refused, and the checked-in `first-reader-negative-restore.json` is byte-identical: SHA-256 `1afc4749890763c02767eea9ad9161f659f34f05fc1d6f841dbd2c762746db1a`. Forward source/condition/occurrence each raised `ConditionValueRelationMismatch`; reverse source raised `AnalyticalCompositionError`, reverse condition/occurrence raised `ConditionValueRelationMismatch`.

`mutation_restore.py` reproduced the actual source-response mutation:

- original SAV SHA-256 `756e5ab27e72324813a2726e256f53839c01d634dbbcc2f60be53d3164a849b2` (unchanged after restore);
- mutated SAV SHA-256 `7cdb7778b6abbd8fd5b701dc8af3143e3bee6dc3ae5189f37330804c9417cb71` (fresh SAV serialization; the checked-in historical receipt records `a4811a1326a67030f7f94243aa919e7fe15d6198aa6b3923e2d8327a5558dcdb`);
- `positive_numerical_assertion: FAILED_AS_REQUIRED`; original `000=3`; mutated `000=2`, `001=1`;
- `restore: PASS`; restored trace byte-identical with SHA-256 `53c45586…`; SAV restored to `756e5ab…`.

`probe_conditioned.json` replay differs from the checked-in *historical* generated-source ledger (`68c48d4…` vs replay `7d626b8…`), with old native-ledger hashes/denominators in the historical file. The current retained first-reader trace and the independent numerical oracle both give the required 12 / four-cells-at-3 and 4 / 1-and-3 values. I treated the older ledger as the documented initial timestamp-bearing qualification artifact and did not commit the replay difference. Worktree status after all replay: clean; no SAV or probe differences retained.

## Governed court: L02-specific PASS vs inherited FAIL

Exact `.rabochii/court_spec.json` court (8 files), `PYTHONHASHSEED=0`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, CPython 3.11.3:

```sh
python -m rawlsing_next.rabochii_bounded_court .rabochii/court_spec.json --receipt <tmp>/court_receipt.json
```

Result: **144 passed / 3 failed**, exit 1, 23.21 s — matching the reported Actions run 42163321319 (144 PASS / 3 FAIL). The three failures are inherited FIABC/LiTS pinned-blob mismatches, none in L02 code:

1. `test_fiabc_w3_i04_runtime_packaging_rebind.py::RuntimePackagingRebindTests::test_lits_authority_overlay_v2_pins_integrated_normalized_sourcebacked_scope` — `rawlsing_next/_pre553_query_eval.py` expected `f808dfcd2008cc71e9203de3cadf1abe14223974`, actual `64555ce46807b815c6e26cb46b35622c73efe5ab`.
2. `test_fiabc_final_preflight_fanin.py::test_live_candidate_c_and_packaging_bind_final_hq_state` — `rawlsing_next/pre553_candidate_c_production_binding.py` expected `47893688ed455ced2c2f2311ad0aead6fb5bf2d2`, actual `c2451b1b9d54b9588455022e0d6625083bb955d2`.
3. `test_fiabc_final_preflight_fanin.py::test_t5_contract_binds_final_successor_and_lits_current_law` — same candidate-C pin mismatch.

These were not repinned, waived, hidden, or repaired. `test_pre553_candidate_c_production_binding.py` itself passes 7/7; `test_pre553_i03_scale_equivalence_repair.py` passes 16/16. As a supplementary check outside the governed court, `test_pre553_whole_machine_hostile_acceptance.py` gave 22 passed / 1 failed: `test_r15_h15_frozen_semantic_blobs_are_byte_exact` reports 13 inherited pinned-blob drifts (including `_pre553_query_eval.py` expected `4a37830eb23ee03949b8bb3563e6dac802501a58`, actual `64555ce46807b815c6e26cb46b35622c73efe5ab`); no L02 file is in that pin set. These remain with their competent owner.

The Actions run page itself could not be read through the available REST credential (`403 Resource not accessible by personal access token` for pulls/checks/actions). The exact local court-spec reproduction supplies the executable 144/3 evidence and the changed-test gate passed both L02 claims.

## New L02 defects

No genuine new L02 defect was found. The only unexpected values are the documented historical generated-source ledger differences above and the inherited FIABC/LiTS pin failures; neither is in the L02 repair path or its first consumer.

## Terminal return

`S2_VERIFIED_READY_FOR_INDEPENDENT_R02_REREVIEW`

This is an implementation-verification disposition, not independent R02 receiving acceptance. Original35 science, protected CAS, N11/N12, Sorok, and actor authority remain held.
