# C2 test receipts

All commands run from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer` with `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer/WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C2_JOINT_CONSUMER/tmp`.

## Sourcefree probe

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C2_JOINT_CONSUMER/tmp" \
python3 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C2_JOINT_CONSUMER/probes/probe_joint.py \
> WORKER_RETURNS/.../C2_JOINT_CONSUMER/logs/probe_joint.json 2> .../logs/probe_joint.err
```

- Exit: `0`
- `probe_joint.err`: empty
- Fixture: `E03_PROGRESSIVE_ABC_Y_58`, 58 synthetic nonrespondent rows, `real_subject=False`
- Positive provider state: `EXACT_SUPPORTED_SLICE_PRODUCED` derived from the actual `provide_empirical_possibility_slice` invocation-log output. Composition state: `SUPPORTED`; consumer state: `EXACT_SUPPORTED`. Denominators `32/16/8`; exact fractions `9/16`, `5/8`, `3/4`.
- Negative: wrong conditioner order `ConditionValueRelationMismatch` (asserted by named test); false pairing `ConditionValueRelationMismatch` (asserted by named test); wrong source universe `PositionedSubjectPossibilityError` (observed, not asserted); missing authority registry `EmpiricalQueryExecutionError` (observed, not asserted).
- Same-process deterministic rebuild: same step IDs, denominators, cells, evidence refs and consumer states. Cross-process persisted restore, serialization/cache cold start and durable reconstruction: `NOT_RUN`.
- No original respondent/SAV/DTA/DB read; no original J issuer selected; no native/science/actor run.
- Old-version, shadow and revocation behavior: `NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION`.
- Seed: deterministic synthetic fixture; no RNG seed used.

## Named existing sourcefree tests

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... python3 -m pytest -q -p no:cacheprovider \
  --basetemp=.../tmp/pytest \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_full_progressive_chain_matches_hand_derived_oracle \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_unordered_conditioner_list_is_refused \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_false_pairing_value_is_refused \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_progressive_declares_no_rights_and_no_real_current
```

- Exit: `0`
- Result: `4 passed in 1.55s`
- This is test-only current-owner evidence; not an original J issuer trace and not current native admission.

## Source hashes

| Component | SHA-256 |
|---|---|
| `pre553_empirical_possibility_provider.py` | `99d716051f23e1ef75990a5184afec612aa7855078a67893f6436b44f57b4697` |
| `pre553_analytical_composition.py` | `2358cd2676133e61b8a36dd59295ef6dc16f2ef840bbc7d9792ebcc3961fdd01` |
| `source_backed_positioned_subject_possibility.py` | `9c041cb134a7b9198d12f75a1eb82a7e37cdb781adf5f68033b5ad21e62dbc01` |
| `pre553_n9_n10w_progressive_candidate.py` | `78f85aea938e9a087167af2938ab11aabbf5a731e852194f021918cf21044c8d` |

## Output hashes

| Output | SHA-256 |
|---|---|
| `00_RETURN.md` | `46105573ea1947d44db88df72e1c0cda386551ec518dd6944df594a4cb0ba71b` |
| `01_CASES.jsonl` | `08b8745d25057a8b48ab1af08957e47eefec510582ed4a62c14f818bd40897c3` |
| `02_CASES.tsv` | `caf9d507d43c88c6c674c9c0718b3553cc9de2de549880aed2366a3da7124971` |
| `04_MINIMAL_OWNER_ACTIONS.tsv` | `74448710e7f4cb343c8cc1760843a65575721b99f4ba0cc0797a1ce1957ebe4a` |
| `05_REGISTER_ANTIJOIN.tsv` | `128fb87b803fff412a259def263ba48c6b5c9daa351454196c16c7aeb68c66b4` |
| `probes/probe_joint.py` | `83a9724fc2d705a51afa36c6443fe853c2cbef9546a91dda28c25f00e587372f` |
| `logs/probe_joint.json` | `d061fa82fbce20c695c2e3a0a3ddaf17bd225729e466e2b536c364bc0d77e16b` |
| `logs/pytest_joint.log` | `9749135c41084e8173dbba868a950d160ec3c5551a45ff1fb5468ed9bb740241` |
| `06_REPORTING_CORRECTIONS.md` | `b810754f3f5fdc209e41f715164a0029a50c2f2472bf2cdecf6d8faad04a3414` |

`03_TEST_RECEIPTS.md` is this document and is not self-hashed.

## Blocked / not run

- Original J issuer/row selected authority: `NOT_RUN__NO_SELECTED_ORIGINAL_J_RELEASE`; explicit HOLD at O11, not a fabricated proof.
- Old version, shadow and revocation: `NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION`.
- Cross-process persisted restore/serialization/cache cold start/durable reconstruction: `NOT_RUN`.
- Prior independently reviewed cut `751fb3fab88ab0faef4b20afeb57a89801f7cce8`; these are reporting corrections only.
- Original respondent/SAV/DTA/DB: `NOT_RUN` by lease.
- Native/science/actor/current grant: `NOT_RUN`; no production patch.
