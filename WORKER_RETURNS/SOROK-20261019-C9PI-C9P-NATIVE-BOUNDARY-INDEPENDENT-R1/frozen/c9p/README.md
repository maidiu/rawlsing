# SOROK C9P candidate tranche

Noninstalling, fail-closed candidate transaction/consumer path for the Sorok C9/C12
native V3 actor/event/response/target/later-action chain.

**Status:** `C9_NATIVE_POSITIVE_HELD__MAXIMAL_LAWFUL_TECHNICAL_TRANCHE_DELIVERED`.

## Layout

```
candidate/          12 modules implementing the complete (a)–(h) chain
tests/              90 tests covering every stage, branch and negative control
severance/          separate-process dependency-severance runner
evidence/           JUnit, proof-witness, severance and source-hash receipts
00_RETURN.md        main return
01_…05_             T0 inventory, T1 path, T2 gate, T3 proof, T4 matrix
case_matrix.json    preregistered case matrix
run_repro.sh        exact reproducible runner
```

## Run

```sh
# Full suite
python3 -m pytest WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1/tests/ -q

# Severance court (separate processes)
python3 WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1/severance/run_severance.py \
    --root . --receipt WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1/evidence/severance_receipt.json

# Everything
bash WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1/run_repro.sh
```

## Key constraints

- Production CAN008 and CAN011 rule registries are empty; the native release gate
  stays `C9_NATIVE_POSITIVE_HELD`.
- TEST_ONLY fixtures are explicitly typed and never presented as native authority.
- No hand-authored later action, no psychological state from response text.
- Six severance witnesses prove each named consumer actually reads its source.
