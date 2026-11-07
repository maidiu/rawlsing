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
- Positive: `EXACT_SUPPORTED`; denominators `32/16/8`; exact fractions `9/16`, `5/8`, `3/4`; consumer `EXACT_SUPPORTED` at all three steps.
- Negative: wrong conditioner order `ConditionValueRelationMismatch`; false pairing `ConditionValueRelationMismatch`; wrong source universe `PositionedSubjectPossibilityError`; missing authority registry `EmpiricalQueryExecutionError`.
- Cold restore: same step IDs, denominators, cells, evidence refs and consumer states.
- No original respondent/SAV/DTA/DB read; no original J issuer selected; no native/science/actor run.
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
| `00_RETURN.md` | `f1a45319812e8b32835fbde7641e912029d3a3f2750d66a2eb23b9c24bac8d1a` |
| `01_CASES.jsonl` | `5ee7d9072ffb207b8506088a6eabb3937e802d14c1fe95b276bfc5595d6d7802` |
| `02_CASES.tsv` | `7b8529b812005b201ce6db82a3a054c7e6db8ea79061d09e41add586fcefdf2e` |
| `04_MINIMAL_OWNER_ACTIONS.tsv` | `16ef7fc065436049ff0947f0359f63eeba9a3790e043608472cd8deed413cf87` |
| `05_REGISTER_ANTIJOIN.tsv` | `128fb87b803fff412a259def263ba48c6b5c9daa351454196c16c7aeb68c66b4` |
| `probes/probe_joint.py` | `8a460f723ac888ed5ef3373caa52ac606621b8361dcaa6cd642cb4e391df190a` |
| `logs/probe_joint.json` | `952a8311cf03ecd6b81b153c197dfb218249c7aafdfe3029ca67dbe9ffe92f81` |
| `logs/pytest_joint.log` | `9749135c41084e8173dbba868a950d160ec3c5551a45ff1fb5468ed9bb740241` |

`03_TEST_RECEIPTS.md` is this document and is not self-hashed.

## Blocked / not run

- Original J issuer/row selected authority: `NOT_RUN__NO_SELECTED_ORIGINAL_J_RELEASE`; explicit HOLD at O11, not a fabricated proof.
- Original respondent/SAV/DTA/DB: `NOT_RUN` by lease.
- Native/science/actor/current grant: `NOT_RUN`; no production patch.
