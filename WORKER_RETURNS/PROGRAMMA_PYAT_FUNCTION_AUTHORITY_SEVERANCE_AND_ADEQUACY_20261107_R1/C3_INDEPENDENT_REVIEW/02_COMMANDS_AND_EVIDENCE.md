# C3 independent commands and evidence

All commands run from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-ff-postff-independent-review`.
Writes only under `C3_INDEPENDENT_REVIEW/`.

## 1. Author receipts and source identity

- Inspected `C3_FF_POSTFF_CONSUMER/03_TEST_RECEIPTS.md`,
  `03a_PYTEST_SELECTED.log`, `03b_PYTEST_NEGATIVES.log`: **21 + 10 = 31
  sourcefree tests passed**, exit 0. The full 31-test suite was not repeated.
- Inspected `06_HASH_AND_SOURCE_MANIFEST.tsv`: 11 source rows.
- Verified every source row with `git hash-object --no-filters` and SHA-256:
  **11/11 blob and content hashes match**. `git diff
  7a5429ffbc48efd25e28c912da80c822e66bc182..HEAD -- rawlsing_next` is empty.
- Inspected `05_REGISTER_ANTIJOIN.tsv`: **176 rows, 125 unmatched**, no full #777
  claim.

## 2. Minimal independent edge replay

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest -q \
  -p no:cacheprovider --basetemp=.../C3_INDEPENDENT_REVIEW/probes/pytest-edge \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_actual_c_relation_admits_without_reownership_and_is_lossless \
  rawlsing_next/tests/test_l01_evidence_world_consumer.py::test_actual_request_mutation_refuses_and_restores
```

Result: exit 0, **10 passed in 2.85s**. Log: `logs/edge_replay.log`. This confirms
one Q86 C→D positive and one sourcefree P41 mutation/restore edge; it is not a
31-test repeat.

## 3. Repo-wide non-test caller/registration check

`probes/independent_checks.py` scanned `rawlsing_next` non-test Python files and
`06_HASH_AND_SOURCE_MANIFEST.tsv`; output `logs/independent_checks.log`.

Observed:
- `produce_exact_conditional_support_profile`: only producer module and
  `gt12_c_to_d_relation_bridge`.
- `admit_gt12_c_relation`: only C→D bridge definition.
- `prepare_typed_d_to_e_relation_basis`: only D→M4 bridge definition.
- `compute_pair_support_signature`: no non-test site.
- `select_r05_world_view` / `configure_evidence_world_context`: only their world
  modules.
- No non-test Python import of `gt12_c_to_d_relation_bridge`,
  `gt12_d_to_m4_typed_bridge`, `gf1_pair_support_consumer`,
  `ffx002_r2_integrated_stack`, or `ffx002_r2_local_geometry`.
- Control-room roadmap/register mentions are evidence/candidates, not executable
  consumers. This corroborates no selected non-test generic FF path, but it does not
  prove a real generic FF product demand or an implementation defect.

## 4. Candidate/currentness checks

- Q86 #774 is open/unmerged; protected source is the pre-#774 base
  (`field_forge_conditional_support.py` blob `a70decb...`), as C3 states.
- GF1 #691 is test-only/unmerged candidate (register FFR1:A14; PR #691 repaired head
  `a6b815ecc...`; independent COMMENTED scoped acceptance, not protected).
- FFX A/C and geometry B are historical capital at source commit
  `957628a...`; no current non-test import/demand found.
- Generic I03/I05 is current upstream empirical query, not a generic FF relation
  producer; no upstream FF rebuild inferred.
- Native N9/N10W/FF CONTEXT, structural N5/N6/I04, and M5→M6 actor cases name no
  exact selected request/source/permission/issuer. They are `NOT_RUN`/selection
  UNPROVED, not a proven engineering block.

## 5. Disposition correction

C3's core finding should be **selection/demand and equivalence UNPROVED** for a
generic non-test FF producer/first consumer, not `IMPLEMENTATION_NOT_CURRENTLY_ADEQUATE`
as a demonstrated implementation defect. The Q86 canary is real at bounded scope;
GF1 is test-only/unmerged; FFX is historical capital; generic I03/I05 is current but
not generic FF; no real non-test generic FF operation is named. Native/structural/
actor `BLOCKED` labels are downgraded to `NOT_RUN`/`UNPROVED SELECTION` absent exact
selected request/issuer evidence. All observed positives, sourcefree receipts,
negative evidence, #774/T01/R9 holds, and prior 176-row anti-join are preserved.
