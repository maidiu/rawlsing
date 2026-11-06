# Exact commands and observed results

Worktree:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-recursion-reuse-r1`

Subject:
`7c4907d0b5c42eaf0f6eb92a538516453a922933`

## Fast core/engine and model-cycle assertions

```sh
OUT=WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-REPAIR-REVIEW-R1
S=WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1
cd "$S"
TMPDIR="$PWD/../SOROK-DEVELOPMENTAL-RECURSION-REPAIR-REVIEW-R1/evidence/tmp" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B -m pytest -q -p no:cacheprovider \
  tests/test_engine.py tests/test_model_cycle.py \
  --junitxml="../SOROK-DEVELOPMENTAL-RECURSION-REPAIR-REVIEW-R1/logs/fast_junit.xml"
```

Observed: **64 passed in 1.03s**.

## Actual owner and two-batch integration assertions

```sh
cd "$S"
TMPDIR="$PWD/../SOROK-DEVELOPMENTAL-RECURSION-REPAIR-REVIEW-R1/evidence/tmp" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B -m pytest -q -p no:cacheprovider \
  tests/test_p2_owner.py tests/test_recursion_integration.py \
  --junitxml="../SOROK-DEVELOPMENTAL-RECURSION-REPAIR-REVIEW-R1/logs/slow_junit.xml"
```

Observed: **6 passed in 267.61s** (0:04:27). Combined focused/core run: **70 passed**.

Important included witnesses:

- `test_actual_material_effect_reaches_c9_and_owner_receipt_survives_reopen` — actual material interval → C9; actor perception severance → HELD; restoration → OBSERVED.
- `test_wrong_source_clock_state_and_unknown_operation_do_not_mutate_owner` — source/root/branch/clock/operation severances preserve owner snapshot; source mutation restored.
- `test_invalid_batch_chronology_is_refused_before_effects` — inverted, equal and nonfuture event times refused before effects.
- `test_bad_history_in_later_proposal_is_refused_before_first_interval` — missing/malformed/duplicate native grounding refused before interval/operation writes; valid native ID/hash forms pass.
- `test_two_real_batches_retrospection_and_cold_root` — two actual batches, carry-forward, actor-bound retrospective input, terminal nonmutation, cold continuity.
- `test_material_antecedent_changes_later_native_c9_result` — ACTUAL `[False,False,False]` vs SCHEDULED_ONLY `[True,True,True]`.

## Cold file-transport CLI

```sh
cd "$S"
TMPDIR="$PWD/../SOROK-DEVELOPMENTAL-RECURSION-REPAIR-REVIEW-R1/evidence/tmp" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B run_cold_cli_witness.py \
  "../SOROK-DEVELOPMENTAL-RECURSION-REPAIR-REVIEW-R1/evidence/cold_cli_review.json"
```

Observed:

```text
bootstrap / advance / finish
batch_event_counts = [3, 3, 0]
retrospective_count = 2
same_root = true
before_clock = 222
after_clock = 258
provider_calls_between_events = 0
cold_verified = true
retrospective_uses_developing_actor_perceptions = true
default_output_omits_actor_private_experience = true
native_psychological_transitions = MISSING_RULE
```

The file transport is an explicit TEST_ONLY model-response fixture; it is not a provider or native participant call.

## Evidence files

- `logs/fast.log`, `logs/fast_junit.xml`
- `logs/slow.log`, `logs/slow_junit.xml`
- `logs/cold_cli_review.log`
- `evidence/cold_cli_review.json`
- `01_REVIEW_RECEIPT.json`
- `PASSPORT.json`

No subject source or test file was modified by this review.
