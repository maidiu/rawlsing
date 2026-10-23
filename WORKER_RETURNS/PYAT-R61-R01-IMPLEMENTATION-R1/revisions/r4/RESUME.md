# R01 R4 resume

Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`

R4 code commit: `009dc5119ae21cd1bc943eeb49019cd25e22eaa6`

Startup: `9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r4/junit.xml \
  -o addopts=''
```

Expected: exit `0`, `24 passed`, no skips.

Key recurrence tests:

- `test_bounded_adaptive_recurrence_three_generations_actual_native`
- `test_recurrence_k_bound_and_budget_leave_explicit_unrun_work`
- `test_recurrence_issued_mutation_and_invalid_parent_identity`
- `test_recurrence_persisted_handoff_roundtrip_and_renamed_profile`

## Boundary

- Frozen profile: `CONTRACT_AND_TEST_PROFILE.md`, `test_profile.json`.
- A4 implemented as candidate; independent reviewer must qualify.
- R03 remains NOT_STARTED; R04/original science/N11/N12/production/CI/J52-W52
  remain NOT_REACHED.
- V1/R2/R3 reports and reviewer trees immutable; no self-adoption.
