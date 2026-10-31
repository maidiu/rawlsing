# Safe tests, hashes, and NOT_RUN

## 1. Source-read proof for the 39 rows

Input: RCF-D `5446395925996f4c2e4d3aabef2e06ba97d16fcd`, ledger row
classification `CLOSED_MECHANICALLY__BRANCH_LOCAL_CANDIDATE_RUNTIME_NO_PREMAIN_IMPORTER`.

- **39** unique row identities (branch + cut).
- **94** unique candidate file paths across those rows.
- **94/94** actual Git object bytes read and AST-parsed.
- **0** files `UNRECOVERABLE_EXACT`.
- **39/39** rows have at least one source file read and a disposition.
- File hashes, blob IDs, functions, classes, imports and per-file dispositions
  are in `01_ALL_39_SOURCE_PATH_FUNCTION_CONSUMER_DISPOSITIONS.json`.

This was read-only inspection. No candidate branch code was executed before
that read. No arbitrary branch hook, provider, raw survey or native source was
run.

## 2. Selected safe sourcefree tests

All test copies were extracted under
`/private/var/folders/.../T/opencode/`; the return worktree and source branches
were not modified. Commands used `PYTHONDONTWRITEBYTECODE=1`.

| Target | Command shape | Result |
|---|---|---:|
| R41 dependency reconstruction | `python3 reconstruct_owners.py --verify` | `{"verified_files": 133}` |
| R41 selected harness | `pytest -q tests/test_native_world.py` | 26 passed in 70.20s |
| EE-R5B adapter | `pytest -q 06_test_bounded_w4_adapter.py` | 9 passed |
| WG0 workload builder | `pytest -q test_wg0_workload_builder.py` | 11 passed |
| EST1 omission oracle | `pytest -q test_est1_omission_oracle.py` | 14 passed |
| M48 constitution | `pytest -q test_constitution.py` | 14 passed after exact matrix fixture supplied |
| **Selected total** | | **74 passed, 0 failed, exit 0** |

M48 note: the first run had 13 pass / 1 `FileNotFoundError` because the test
expected `PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/ESTATE_35X_REQUIREMENTS_MATRIX.json`
at its repository-relative parent. The exact file was extracted from the same
cut into the temporary test parent; the unchanged test then passed 14/14. This
was a fixture-path condition, not a source defect or a new RED.

R41 note: the selected `tests/test_native_world.py` is the branch-local
read-only world harness test. It was run after `reconstruct_owners --verify` and
after source inspection. The prior author-reported 94 core + 33 EE1 + 1
temporal-regression counts were not independently rerun.

## 3. Hash anchors

| Object | SHA-256 |
|---|---|
| Startup/refresh PRE-MAIN `5fc1d43e...` | commit identity, not recomputed as file |
| RCF-D ledger cut | `5446395925996f4c2e4d3aabef2e06ba97d16fcd` |
| R41 `objective_world.py` | `66feab937ac168254ecb5bdea15d9fb9cb4ef3d7facdad0ab6eff4fcf9b1a096` |
| R41 `w41_bootstrap.py` | `9ffc5dbac035b3131ac935e8493aaab666330ca8033b8f137491c95f65332b3a` |
| R41 owner archive | `996df032812585d67400ba75b036dfc7b1a9b2f31dde69b4371d5b45f6f22710` |
| R41 owner pins | 133 preimages; archive membership 133; `--verify` pass |
| 39 candidate file hashes | exact per-file SHA-256 in `01...json` |

No hash was normalized or replaced after inspection.

## 4. Explicit NOT_RUN

- Full original tests for all 39 candidate branches. Only the five selected safe
  sourcefree suites above were run.
- GF1H/GF1K/GF1M tests and the generic pair candidate. The source was read, but
  the exact staged owner/test environment was not recreated.
- R41 full 94 core / 33 EE1 / one temporal-regression suite. Only 26 selected
  R41 tests were run.
- `capture_products.py`; it writes a 39,212,431-byte receipt and generates 84
  views. Its author evidence is read, not re-executed.
- Any Pyat raw survey, SAV, provider/model call, native N11/N12 acceptance,
  C0 actor initialization, C9/C12 ownership or production import.
- Any branch-wide `pytest`, arbitrary hook, arbitrary script execution or
  network-facing test.
- Any integration, merge, PR creation, review acceptance or PRE-MAIN mutation.

## 5. Source closure recommendation

- **39-row historical source estate:** source read and disposition closed at
  94/94 files; 0 exact-unrecoverable.
- **R41 dependency graph:** closed at the source/archive level; 133/133 owner
  preimages verified; selected 26-test consumer passes.
- **R41 product/adoption:** not closed; `UNWIRED_SOURCE_PRESENT`, no current
  PRE-MAIN importer, no native authority.
- **Remaining uninspected material source:** none in the exact 39 rows; R41
  support files were read through archive pins. The remaining gaps are owner
  decisions, grants, consumers and native execution—not a hidden 40th source
  estate in this finite set.
