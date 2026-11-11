# Exact commands

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py.proof.json \
  --root .

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  --head 8c5ae1c5f345212a6b498a89f89b223f7da0fef1 --root .
```

Result before committing the sidecar: exit 0, two witness contracts, both claims baseline PASS and target assertion failure. After committing, the same full command is rerun at the new candidate head.

No repeated court or benchmark smoke was run.
