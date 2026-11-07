# C2 independent review — commands and evidence

All commands ran from:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-independent-review`

No author/production/test/HQ/peer/protected files were modified. All outputs
are under:
`WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C2_INDEPENDENT_REVIEW/`

## Replayed author probe

```sh
PYTHONDONTWRITEBYTECODE=1 \
TMPDIR='.../C2_INDEPENDENT_REVIEW/tmp' \
python3 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C2_JOINT_CONSUMER/probes/probe_joint.py \
  > .../C2_INDEPENDENT_REVIEW/03_PROBE_REPLAY.json \
  2> .../C2_INDEPENDENT_REVIEW/04_PROBE_REPLAY.err
```

- exit `0`; stderr empty; JSON bytes `10739`.
- `diff -u` against the author probe log: **no differences**
  (`09_PROBE_DIFF.txt`).
- The probe exercises the current N10E provider, C1 composition, and F8
  evaluator over the 58-row synthetic nonrespondent fixture
  (`real_subject=False`).

## Author's four named sourcefree tests

```sh
PYTHONDONTWRITEBYTECODE=1 \
TMPDIR='.../C2_INDEPENDENT_REVIEW/tmp' \
python3 -m pytest -q -p no:cacheprovider \
  --basetemp=.../C2_INDEPENDENT_REVIEW/tmp/pytest \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_full_progressive_chain_matches_hand_derived_oracle \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_unordered_conditioner_list_is_refused \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_false_pairing_value_is_refused \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_progressive_declares_no_rights_and_no_real_current
```

Result: **4 passed in 1.52s** (`02_FOCUSED_TEST_LOG.txt`).

## Additional focused checks

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_production_and_consumption_are_distinct_invocations \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_single_conditioner_step_uses_real_provider_state_vocabulary \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py::test_cross_sample_join_is_refused
```

Result: **3 passed in 1.22s** (`05_EXTRA_FOCUSED_TESTS.log`).

Direct check of actual provider state and missing-authority behavior
(`06_ACTUAL_PROVIDER_AND_MISSING_AUTH.txt`):

```text
step.producer_fact_state= SUPPORTED
actual invocation provider_state= EXACT_SUPPORTED_SLICE_PRODUCED
actual call= provide_empirical_possibility_slice
missing_authority= EmpiricalQueryExecutionError authority_registry must be exact immutable AuthorityRegistry
```

## Source hashes

`07_SOURCE_HASHES.txt`:

```text
99d716051f23e1ef75990a5184afec612aa7855078a67893f6436b44f57b4697 rawlsing_next/pre553_empirical_possibility_provider.py
2358cd2676133e61b8a36dd59295ef6dc16f2ef840bbc7d9792ebcc3961fdd01 rawlsing_next/pre553_analytical_composition.py
9c041cb134a7b9198d12f75a1eb82a7e37cdb781adf5f68033b5ad21e62dbc01 rawlsing_next/source_backed_positioned_subject_possibility.py
78f85aea938e9a087167af2938ab11aabbf5a731e852194f021918cf21044c8d rawlsing_next/pre553_n9_n10w_progressive_candidate.py
```

These match `C2_JOINT_CONSUMER/03_TEST_RECEIPTS.md`.

## Independent fixture arithmetic

`08_FIXTURE_ARITHMETIC.txt`, derived directly from `_CELL_COUNTS`, not from
owner output:

```text
rows 58
A=1: denominator 32, Y=1 18, 9/16
A=1,B=1: denominator 16, Y=1 10, 5/8
A=1,B=1,C=1: denominator 8, Y=1 6, 3/4
```

## Actual positive calls and refusals

- The probe reports first-consumer calls:
  `provide_empirical_possibility_slice` once,
  `compose_positioned_subject_possibility` twice,
  `evaluate_positioned_subject_possibility` three times.
  The extra production/consumption test independently passes and verifies the
  F8 consumption uses each step's own produced evidence.
- Refusal observations:
  - wrong conditioner order: `ConditionValueRelationMismatch`;
  - false pairing: `ConditionValueRelationMismatch`;
  - wrong source universe: `PositionedSubjectPossibilityError`
    (`conditioner source/release mismatch; no implicit bridge`);
  - missing authority registry: `EmpiricalQueryExecutionError`
    (`authority_registry must be exact immutable AuthorityRegistry`).
- The four named tests assert wrong-order and false-pairing; wrong-source is
  independently covered by the extra test; missing-registry is independently
  observed by the direct check. The author probe's broad `except Exception`
  still records these two as observational, not typed assertions.

## Reporting limits

- Probe `provider_state` at `probes/probe_joint.py:166` is hardcoded
  `EXACT_SUPPORTED`; actual provider state is
  `EXACT_SUPPORTED_SLICE_PRODUCED` (provider constant line 53; test line 413).
  This is a reporting correction; the positive behavior is proven.
- Probe “cold restore” at `probes/probe_joint.py:147-155` calls
  `build_synthetic_world()` again in the same process and compares outputs.
  It is a deterministic same-process rebuild, not a persisted/cross-process
  cold restore. Cross-process persisted restore is `NOT_RUN`.
- F17/F19/F20/F21 matching is bounded to this O11 witness. No selected original
  J issuer/row/version is present; this is not historical absence, a
  whole-pipeline equivalence, or a severance verdict. C2-J01 already records
  `historical_j_equivalent=UNPROVED`, `proven_severance=False`, and
  `old_version_shadow_revoked=NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION`.
  C2-J02's “no justified current consumer” label is stronger than the evidence;
  relabel to “no selected J issuer at O11; demand not established.”
- No original respondent/SAV/DTA/DB bytes were read. The fixture is synthetic,
  nonrespondent, and no native/science/actor/current/protected authority is
  claimed.

## Test scope

The author’s full suite was not repeated. This review ran the four named
sourcefree tests and three additional focused tests; it did not accept full
pipeline or historical J equivalence from those tests.
