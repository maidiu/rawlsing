# GF1E — cold-process consumer reconstruction

The consumer is exercised in a **fresh OS process** (not a thread, not a
re-import) exactly as the commission requires, and the results are compared for
bitwise identity.

Command (per process, `repro/cold_consumer_child.py`):
```
python3 repro/cold_consumer_child.py observations/gf1e_cold_consumer_<i>.json
```

Each child rebuilds the four differential-pattern relations from scratch, runs
`compute_pair_support_signature` on each, and writes its own PID plus the
results.

## Result

| process | PID | classes |
| --- | --- | --- |
| 0 | 70419 | EXACT / NO_PAIR / NO_ELIGIBLE / ZERO_SUPPORT |
| 1 | (distinct) | EXACT / NO_PAIR / NO_ELIGIBLE / ZERO_SUPPORT |

* **Distinct PIDs** — two independent OS processes.
* **Bit-identical** — `json.dumps(result_0, sort_keys=True) == json.dumps(result_1, sort_keys=True)`.
* **Class map** — `{EXACT_PAIR_SEPARATION, NO_PAIR_SEPARATION, UNDETERMINED_NO_ELIGIBLE_RISK, UNDETERMINED_ZERO_SUPPORT_RISK}` all produced.
* **Matches in-process** — the cold-process result for every pattern equals the
  in-process `compute_pair_support_signature` result byte-for-byte.

Raw artifacts: `observations/gf1e_cold_consumer_0.json`,
`observations/gf1e_cold_consumer_1.json` (asserted in
`tests/test_gf1e_consumer_differential.py::test_cold_process_consumer_reconstruction_bit_identical`).

No persisted ledger, no actor grant, no registry service is touched: the cold
replay reconstructs the consumer value purely from the immutable relation
inputs, which is the exact property this lane must prove.
