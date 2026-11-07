# C3 test and proof receipts

## Environment and scope

- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-ff-postff-consumer`
- Branch: `agent/pyat777-ff-postff-consumer-20261107-r1`
- Startup: `03d054f1c693524e781767d96a287ca9e937e3ff`
- Protected source: `7a5429ffbc48efd25e28c912da80c822e66bc182`
- All commands used absolute worktree paths. `PYTHONDONTWRITEBYTECODE=1`;
  `TMPDIR` and pytest `--basetemp` were under the C3 output root;
  `-p no:cacheprovider` was used. No production/test source file was edited.
- The selected tests are sourcefree/canary tests. They do not read original
  respondent/SAV/DTA/DB bytes and do not run S3/native/science/actor issuance.
- Seed: no random seed is used by these deterministic synthetic/fixture tests
  (`seed=N/A`). The test fixtures are fixed sourcefree dictionaries.
- No production edge was selected for a severance mutation; therefore a
  `severance RED -> restoration` claim is **not applicable** here. The Q86
  replay/permission tests and the sourcefree P41 mutation/restore tests are
  negative/cold-restoration evidence only, not a production severance claim.

## Primary selected court (positive and negative)

Command run from the worktree root:

```bash
OUT='WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C3_FF_POSTFF_CONSUMER'
TMPDIR="$OUT/tmp" PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' \
python3 -m pytest -q \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_actual_c_relation_admits_without_reownership_and_is_lossless \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_c_observed_zero_blocker_cannot_be_laundered_to_admitted \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_positive_gt2_admission_is_exact_and_narrow \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_observed_zero_is_nonpositive_even_without_blocker_refs \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_positive_relation_m1_derives_adopted_context_and_reaches_v558 \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_typed_negative_or_nonpositive_input_cannot_translate_even_with_refs_stripped \
  rawlsing_next/tests/test_l01_evidence_world_consumer.py::test_signed_r08_evidence_reaches_actual_nonparent_numbers_and_world_routes \
  rawlsing_next/tests/test_l01_evidence_world_consumer.py::test_actual_request_mutation_refuses_and_restores \
  --basetemp="$OUT/tmp/pytest"
```

Result:

```text
.....................                                                    [100%]
21 passed in 3.31s
exit=0
```

## Additional negative/replay/authority tests

Command run from the worktree root:

```bash
OUT='WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C3_FF_POSTFF_CONSUMER'
TMPDIR="$OUT/tmp" PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' \
python3 -m pytest -q \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_deterministic_receipt_and_historical_replay \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py::test_source_artifact_hash_tamper_is_integrity_failure \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_ref_hash_rule_source_and_risk_tamper_fail_closed \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_wrong_source_dependency_risk_set_or_participant_order_cannot_reuse_authority \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_actual_pre553_ref_authority_material_survives_d_to_e_losslessly \
  rawlsing_next/tests/test_l01_evidence_world_consumer.py::test_current_p41_receipt_owner_closes_historical_r53_failures \
  --basetemp="$OUT/tmp/pytest_neg"
```

Result:

```text
..........                                                               [100%]
10 passed in 2.04s
exit=0
```

**Total selected sourcefree tests: 31 passed, 0 failed, exit 0.** These tests
cover:

- exact Q86 role/order, source family/wave/artifact, risk set, permission and
  context scope;
- positive Q86 C→D admission and D→M1/M4/V558 typed terminal;
- zero/nonpositive/blocker/typed-negative refusal; source/risk/role tamper
  refusal; deterministic replay; no laundering of observed zero;
- sourcefree signed R08/E41 → N9+N10E→N10W positive world route;
- sourcefree request mutation/restore, permission/source/edition/clock/risk
  negatives, and P41 historical R53 negative closure.

## Static currentness and caller check

Run from the worktree root:

```bash
grep -RIn --exclude-dir=tests --exclude='*.pyc' -E \
 'produce_exact_conditional_support_profile|admit_gt12_c_relation|prepare_typed_d_to_e_relation_basis|field_forge_conditional_support' \
 rawlsing_next
```

Observed: the producer/admission definitions and the internal C→D/D→M4 bridge
calls only; no non-test product orchestrator selects an FF relation. A search for
imports of `gt12_c_to_d_relation_bridge` and `gt12_d_to_m4_typed_bridge` outside
tests returned no production entrypoint. This corroborates the #772 Q86 matrix
rows `Q86-S01`, `Q86-S03`, `Q86-S04` (`BOUNDED_CANARY_ONLY`, direct producer/court
only, no production orchestrator) and `Q86-S16` (generic I03/I05 current, but not
a generic FF producer).

The Q86 source-identity guard is PR #774, head
`9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8`; it is open/unmerged/pending
independent review. The protected source used here is the pre-#774 base
(`field_forge_conditional_support.py` blob
`a70decb20747d84cbcbe27d1280babc6de88ef33`). No #774 code is claimed as current
or as generic FF.

## Source hashes and currentness

| source | blob at protected `7a5429` |
|---|---|
| `rawlsing_next/field_forge_conditional_support.py` | `a70decb20747d84cbcbe27d1280babc6de88ef33` |
| `rawlsing_next/wave1_ff_prev3_relation_admission.py` | `c5fb675fd6f95cb7dc9e0ad505224803839cc645` |
| `rawlsing_next/gt12_c_to_d_relation_bridge.py` | `ea04ec079e8d60e6e5c7236ec5b54898876be4b3` |
| `rawlsing_next/gt12_d_to_m4_typed_bridge.py` | `ca3d6b8d832d7ca8d959bd19e19a23b08cabde76` |
| `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py` | `0aeacd9e66c7e4340b36e1b622bb5c9bf2865fd5` |
| `rawlsing_next/pre553_evidence_world_consumer.py` | `75ff3b9a73b1533c5fa6619e36577b69a4c65aed` |
| `rawlsing_next/pre553_universal_world_binding.py` | `fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d` |
| `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` | `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` |
| `rawlsing_next/m4_v557_v558_publication_repository.py` | `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360` |
| `rawlsing_next/m5_runtime_rsc_peer_prior.py` | `18735bdb31a220aed032aa722574d685e2bdddf5` |
| `rawlsing_next/m6_actor_safe_expression.py` | `74d9701cdc7dabccf61eb5089498db290c1efd9c` |

`git diff 7a5429ffbc48efd25e28c912da80c822e66bc182..HEAD -- rawlsing_next` is
empty. The worktree head adds only the issue777 goal/control room to the
protected source.

## Output hashes

The hashes of `01_CASES.jsonl`, `02_CASES.tsv`, `03_TEST_RECEIPTS.md`,
`04_MINIMAL_OWNER_ACTIONS.tsv`, `05_REGISTER_ANTIJOIN.tsv`, and the review logs
are recorded in `06_HASH_AND_SOURCE_MANIFEST.tsv`.

## Limits / non-claims

- The selected Q86 tests are test/court/canary tests, not a selected non-test
  production first consumer. No generic FF positive is fabricated.
- The sourcefree P41 world tests are sourcefree/synthetic; they are not an
  original/native N9/N10W proof.
- No original respondent/SAV/DTA/DB read, no native release/S3/science, no actor
  output, no asset byte copy/upload, no host-trust claim, and no protected merge.
- No original selected issuer/row for the Q86 canary, GF1 generic relation, or
  native N9/N10W is proved here; those remain `UNKNOWN`/`UNPROVED` as stated in
  the cases.
