# FIABC B07 tests and expected assertions

Test file:

`rawlsing_next/tests/test_fiabc_succession_producer.py`

## Authored source-free tests

1. `test_generated_commit_sha_tracks_supplied_exact_head`
   - both I07 and P10 carry supplied exact head;
   - both are pre-candidate frozen.

2. `test_stale_or_wrong_head_is_rejected`
   - stale embedded manifest head blocks;
   - mismatched expected head blocks.

3. `test_wvs7_c_is_sixth_cell_and_order_matches_current_t2`
   - exact six-cell order;
   - WVS7/C index is sixth.

4. `test_lits_a_s01_remains_measured_current_work`
   - S01 is READY;
   - source access true;
   - physical measurement true;
   - no historical preservation classification.

5. `test_candidate_local_and_common_source_failure_scopes_are_exact`
   - all six candidate-local successor edges equal current T2;
   - common-source and common-court dispositions remain typed and distinct.

6. `test_candidate_b_and_wvs7_c_no_cache_laws_are_preserved`
   - B retains `PURE_B_NO_CACHE`;
   - WVS7/C retains `C_ZERO_ACCELERATOR_NO_CACHE`.

7. `test_generated_manifest_and_context_pass_existing_evaluator_on_synthetic_exact_refs`
   - generated structure is evaluated by the **existing** I07 evaluator;
   - expected result is PASS for all P00-P10 phases.

8. `test_candidate_outputs_or_processes_cannot_be_nonzero`
   - hostile nonzero process/output;
   - candidate-owned root consultation;
   - ranking/selection;
   all block.

9. `test_current_owner_mapping_covers_exact_profile_required_function_set`
   - exact 29 required functions mapped;
   - no extras;
   - all 36 functions are required ∪ explicitly deferred.

10. `test_current_manifest_law_rejects_preserved_lits_a_s01`
    - stale historical S01 preservation fails closed.

11. `test_current_manifest_law_rejects_nonzero_accelerator_cache_escape`
    - WVS7/C cache execution replacing zero-accelerator frozen skip fails closed.

12. `test_checked_out_head_is_derived_from_git_not_a_baked_commit`
    - HEAD comes from exact `git rev-parse HEAD^{commit}`.

13. `test_dirty_worktree_blocks_before_production`
    - dirty tree is rejected.

## Static audit completed in this lane

GitHub-only inspection established:

- producer current-worker blob before return packet:
  `045c4803191ad6a0b8f06f035dbc30163fd2647f`;
- test blob:
  `c26bfe8408819c08674739eccf3ad4cae8f833fb`;
- owner map count = profile required count = 29;
- missing owner-map function IDs = none;
- extra owner-map function IDs = none;
- deferred count = 7;
- full function count = 36;
- immutable Candidate-A/B owner blobs resolve exactly at accepted owner commit;
- producer has no LiTS/WVS source decode path;
- producer has no Candidate A/B/C run-stage/backend invocation;
- producer has no branch-update operation.

## Execution status

The tests are **authored but not executed** in this worker lane. The commission is browser/GitHub-only and explicitly forbids GitHub Actions triggering; no result is fabricated.

Expected integrated qualification command after HQ fan-in:

```bash
python -m pytest -q rawlsing_next/tests/test_fiabc_succession_producer.py
```

and the producer's own runtime gate then requires the existing I07 evaluator to PASS before outputs are accepted.
