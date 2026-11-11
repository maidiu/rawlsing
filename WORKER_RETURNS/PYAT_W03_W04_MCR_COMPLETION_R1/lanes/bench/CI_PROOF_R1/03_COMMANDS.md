# Commands

All commands used explicit `cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2`.

```sh
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  rawlsing_next/tests/test_bench_w03_w04_physical.py.proof.json --root .

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 09f97a3a4c77ed7666ee95af586cfdfd91493f73 \
  --head a77d1e052ab5d5022cd88c274dde4d2146265231 --root .

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  --head a77d1e052ab5d5022cd88c274dde4d2146265231 --root .

python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_c11_execution_view.py \
  rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py \
  rawlsing_next/tests/test_pre553_i03_grouping.py \
  rawlsing_next/tests/test_bench_w03_w04_physical.py \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py

python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario full-matrix --profiles narrow,wide,repeat \
  --rows 256 --repetitions 1 --root <temp> --jsonpath bench_smoke_256_non100k.json
```

## Residual

The full frozen gate residual is the preserved independent-review snapshot sidecar outside this lease. No final 100k/full matrix, no economic PASS, no whole 12-ID receiving, no external MCR proof, no protected merge.
