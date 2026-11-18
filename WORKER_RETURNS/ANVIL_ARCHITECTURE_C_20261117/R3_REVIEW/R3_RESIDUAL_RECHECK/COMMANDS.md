# R3 residual recheck commands

Read-only target/contract/research inspection; writes only under this root.

```
git -C /Users/matthewsmith/s2b-work/rawlsing rev-parse b5e4babe2835a18de3aeabe76a4bfa0f8b9928dd
git -C /Users/matthewsmith/s2b-work/rawlsing ls-remote origin refs/heads/agent/anvil-r3-downstream-accommodation-20261117-r1
git -C /Users/matthewsmith/s2b-work/rawlsing diff --stat 06e88a5ac7e4c14362a97a046f44e25d8eec4162 b5e4babe2835a18de3aeabe76a4bfa0f8b9928dd -- rawlsing_next
```

Logs:

- `RUNS/target_verify.txt` — target/remote, product diff empty, 8/8
  package hashes, 10 capability rows, 32 ledger entries, protected rev11.
- `RUNS/contract_checks.txt` — corrected field/adapter contract §2–§6 and
  retained decision §3.2–3.3 adapter.
- `RUNS/g1_ff01_cardinality.txt` — FF01KProduct table and R3-RES-032.
- `RUNS/research_checks.txt` — old 27 exact, new 028–032, all refs resolve.

No native/100k, product test matrix or new sourcefree experiment was needed. The
single remaining defect is a static role-cardinality conflict in the proposed
FF01-k contract. No author/product/protected/prior-review file was modified.
