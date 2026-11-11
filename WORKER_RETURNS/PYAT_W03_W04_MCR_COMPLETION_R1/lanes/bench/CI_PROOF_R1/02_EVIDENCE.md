# Evidence index

## Code and proof bytes

```text
518628a7b752746b509dd6ac04e130e5e8f6f8a01eb543b8dbd711222c93837e  .github/workflows/pyat-w03-w04-physical-economy.yml
2108ebc9ac7103b9a91f063b381b57a63261f94ac66c55631a3cb0b9b133d876  rawlsing_next/tests/test_bench_w03_w04_physical.py
949918f44a6bab0850997c304f1a1c890d7bcdb65ac41a5041ac9117223d21d5  rawlsing_next/tests/test_bench_w03_w04_physical.py.proof.json
675ad4d5e014e81ab3db19ab45b30d62adfc4e2b4c356630cdb8883ebe88aeaa  rawlsing_next/tests/test_pre553_w03_w04_cold.py
f62cbd2263487ee2a8c8c395434d84b100b0c0cbc7548458282ddafa32a1fa07  rawlsing_next/tests/test_pre553_w03_w04_completion.py
```

## Gate receipts

- `proof_gate_targeted_09f_to_a77d.json` — PASS; examined benchmark test, ran one witness.
- `proof_gate_full_frozen_to_a77d.json` — RED, only the preserved review snapshot residual shown in `00_RETURN.md`.
- `proof_gate_selftest.out` — existing checker self-test: 9 tests OK.
- `workflow_tests_86.out` — exact affected CI test selection: 86 passed.
- `bench_smoke_256_non100k.json`, `smoke_summary.json` — 256-row non-final smoke; `final_matrix_eligible=false`.

## Mutation/restore integrity

The proof witness changed only `rawlsing_next/_pre553_query_eval.py` during the gate, then restored it. Post-witness file blob equals `HEAD`/base; no test, oracle or assertion was mutated. The test change in this lease is assertion-strengthening only; all old assertions remain.
