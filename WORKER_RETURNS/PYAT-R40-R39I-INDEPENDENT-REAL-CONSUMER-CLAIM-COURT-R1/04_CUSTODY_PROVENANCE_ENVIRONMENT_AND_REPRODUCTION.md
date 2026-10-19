# Custody, provenance, environment and reproduction

## Exact refs

| Role | Ref |
|---|---|
| Sealed startup (reviewer branch base, verified HEAD) | `1150e836ef58553255abc0f588e66c1327db4932` |
| E04L target (branch tip) | `daf0d085e930696708c755e687879b155653c215` |
| E04L implementation commit | `14135c1f52d54252ccada5fb40f50ae5a5a09a8f` |
| F6P target (branch tip) | `912467aaacb715fd6e80ebc8c2bdd7285c26120b` |
| F6P implementation commit | `7d7ed1cb01bfd32383ee487996d2595c666a07b2` |
| E04JR historical correction | `b39b756564790f4742f28af92e2e7848cf54a419` |
| F6C historical correction | `c1ebe091fa2bd12b254e5599cf37975fe438d462` |
| Prior authors' code substrate | `2e6c189fd54b818556a44419b19691938ea76d5a` |
| Reviewer branch | `agent/reviewer-pyat-r40-r39i-learned-f6-consumer-independent-r1` |

## Independent source blobs (reviewer `git hash-object`)

E04L:
- `readthrough.py` (only new executable edge) `f8e73a6a65713c968c1427381c62ced54de9150c`
- `fixture.py` `ad672fea7c9981f0684e8027830e1f6bc7f2f8a6`
- `test_readthrough_consumer.py` `409c6cf4e2bb38582c99848ed4de90c050bd3f41`
- `test_readthrough_consumer.py.proof.json` `ba83b7e9da63ea9413fdabfbc1dafed8aa30d759`
- original consumer `vendor/product/nonparent.py` `2181b832d3c4376d4b9428e13f4354f273be8f32`
- original service `vendor/product/service.py` `facf1c86911a8a4c37db112be51d8c7109cd9f3b`

F6P:
- consumer `f6p_partial_bound_evidence_consumer.py` `8fa992899293f454d7abded36831a4b4a362df8e`
- F6M `native/rawlsing_next/pre553_heterogeneous_synthesis.py` `2df811d76db258d98d89ffb43c830cb221ff9a7d` (sha256 `2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871`)
- corrected A `…_A.py` `fc5e37fa5b2f0eb689593b42d95479d1327cb94c`
- A0 historical control `…_A0.py` `182cc7970d7624f6614015f5a51d0602e1630d52`
- oracle worlds `oracle/f6c_oracle_worlds.py` `8beb245a9b6261baac5b73bd7c0354c63b00ceed`
- method C `oracle/f6c_method_c.py` `58ef09ea020fed5b8c9bff1b6fc20271526d0abc`
- tests `tests/test_f6p_consumer.py` `9e61b287351ddcb4aa052de7a651d2f25d8cbdfd`, `tests/f6p_fixtures.py` `e0d2240e15e029c8fb1a7b4b5d016dea1c805a60`, `tests/test_f6p_abc_oracle.py` `10204a02b2a6ae051d65a4c91cf2c0a42e47804b`

## Environment

macOS 13.2.1 (Darwin 22.3.0, x86_64); Python 3.11.3; pytest 9.0.2; git 2.43.0.
Warm local host, shared Git object store, no paid API call observed. The author's F6P passport reported pytest 9.1.1; the reviewer host has 9.0.2. All suites pass identically on both. Incremental cash/quota cost: **UNKNOWN**.

## Reproduction (from repository root of the reviewer worktree)

Court A — author court:
```
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=$PWD python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/test_readthrough_consumer.py \
  WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/.runtime/e04jr/tests/test_e04j_native_original_consumer_join.py
```
(`.runtime/` is rehydrated read-only from E04JR `b39b75656` by the author's `rehydrate_original.py`; it is gitignored, not authored content.)

Court A — reviewer independent oracle + hostiles:
```
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1/evidence/court_a/test_court_a_e04l_independent.py   # 10 passed
python3 -B CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1/evidence/court_a/test_court_a_e04l_independent.py.proof.json --root .
```

Court B — author court + reviewer court + gate:
```
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/tests/  # 32 passed
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1/evidence/court_b/test_court_b_f6p_independent.py   # 8 passed
python3 -B CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py witness \
  WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1/evidence/court_b/test_court_b_f6p_independent.py.proof.json --root .
```

Logs and receipts: `evidence/logs/` (`court_a_*`, `court_b_*`), plus the gate receipts embedded by the proof runs.
