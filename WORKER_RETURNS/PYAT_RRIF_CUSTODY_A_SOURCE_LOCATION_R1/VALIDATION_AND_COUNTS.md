# RRIF custody validation and counts

**Status:** sourcefree read-only Git/JSON evidence. No PRE-MAIN, main, worker branch, source or actor execution.

## Source cuts

| Item | Exact cut |
|---|---|
| Canonical receiving branch | `integration/pre-main-reconciliation-r1` @ `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| Current `main` | `25830fe7462bb9e29bc4087e6ae14f3f84cec377` (ancestor of PRE-MAIN) |
| Frozen E8 return | `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba` |
| Retention overlay | `00489a8b2e8e04ed2264d87371f6b0ec4a2d9347` |
| PR #515 roster head | `becf0bfb04705b8fe0927dd56e7290e1dcd180a8` |
| PR #515 roster source run | `3b5ff992a8579d35285c63c98efa1b7dccfb6d96` |

## Commands and exits

```sh
python3 validators/build_branch_summary.py
# exit 0; 845 names / 838 tips; branch summary generated

python3 validators/build_variant_ledger.py
# exit 0; 3,135 functions / 1,883 variant-bearing families + 2 external; ledger generated

python3 validators/validate_custody.py --root WORKER_RETURNS/PYAT_RRIF_CUSTODY_A_SOURCE_LOCATION_R1 --output VALIDATION_RESULTS.json
# exit 0; PASS

cd validators && python3 -m unittest -v test_validate_custody.py
# exit 0; 7 tests OK
```

`PYTHONDONTWRITEBYTECODE=1` and pytest/unittest cache suppression were used. No candidate/historical source module was imported or executed.

## Frozen counts

| Count | Exact |
|---|---:|
| Frozen branch names | 845 |
| Distinct frozen tips | 838 |
| Current remote refs present | 845 |
| Current refs moved after freeze | 1 (`proposal/pyat-stranded-branch-recovery-20261028-r1`) |
| Original variants | 3,135 |
| Variant-bearing families | 1,883 |
| External zero-member families | 2 |
| Branch code-delta branches | 321 |
| Stranded/diverged code branches | 276 |
| Exact-code-present branches | 45 |
| Evidence/admin-only branches | 458 |
| No-delta/ancestor branches | 66 |
| Exact-current/branch-source subtraction | 2,269 |
| Current-modified code uncertainties | 866 |

## Variant location counts

| Location | Functions |
|---|---:|
| PRE-MAIN exact same path | 199 |
| PRE-MAIN exact other path (copy/move unverified) | 291 |
| PRE-MAIN modified same path | 928 |
| Frozen branch tip exact | 1,717 |
| Fully not located | 0 |
| **Total** | **3,135** |

Implementation classes: current exact 446; current modified 866; branch-only exact 1,333; evidence/test/document 490. The branch-tip exact count includes code and non-code; branch attribution is family-level unless a boundary-specific branch is named.

## Spot checks

- All 845 names/tips match the PR #515 roster and the E8 roster; the frozen name/tip digests match the PR #515 manifest shards (`c781d59a…`, `5f7fe089…`).
- Every current path/blob in `CODE_LOCATION_LEDGER.jsonl` that claims a current location resolves to PREMAIN tree `8e44ca9c` at the exact blob.
- `EXACT_CURRENT_SUBTRACTION.json` has 2,269 unique function IDs; `UNCERTAIN_OR_MISSING_CODE.jsonl` has 866 unique current-modified implementation IDs. Both are subsets of the 3,135.
- `INTEGRATION_RECEIVER_MAP.json` covers 27 accepted/staging branches; `COUNTEREXAMPLE_AUDIT.json` covers PR #525/#526/#563, J2I, C3 R5, R157, HQ282-P01 and P07.
- `BRANCH_IDENTITY_CUSTODY.json` preserves all 845 names, tips and order; the single current ref move is PR #515 itself, not a historical-tip overwrite.
- 13 local-only refs and 153 worktrees were observed read-only outside the frozen denominator. Non-local Mac/session estates are `UNKNOWN`, not empty.

## Limits

A blob match is source identity, not semantic/behavioural equivalence. A branch-tip exact blob is not a merge or adoption. A branch named `accepted` is not assumed merged. A modified current path is not necessarily the historical variant. No owner signature, native source, science, actor, or production consumer is claimed. PR #577 was not present/returned at this cut, so no #577 callgraph was duplicated.
