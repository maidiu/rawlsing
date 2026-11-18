# R3 review commands and logs

Read-only target inspection from the shared Git store; no product/author edit.

```
git -C /Users/matthewsmith/s2b-work/rawlsing rev-parse c548ef10bc2276cbe6016a53b8a39b9728cbc922
git -C /Users/matthewsmith/s2b-work/rawlsing ls-remote origin refs/heads/agent/anvil-r3-downstream-accommodation-20261117-r1
git -C /Users/matthewsmith/s2b-work/rawlsing diff --stat 06e88a5ac7e4c14362a97a046f44e25d8eec4162 c548ef10bc2276cbe6016a53b8a39b9728cbc922 -- rawlsing_next
git -C /Users/matthewsmith/s2b-work/rawlsing show c548...:WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117/R3_DOWNSTREAM_ACCOMMODATION/...
```

Logs:

- `RUNS/target_verify.txt` — target/remote, product diff empty, 6/6
  package hashes, 10 capability rows, 22 research entries, protected
  `5d387a` rev11.
- `RUNS/claim_checks.txt` — exact R3 source/FF01/row claims and the absence of
  R3-RES identifiers from the architecture decision/TSV/falsifier.
- `RUNS/code_checks.txt` — exact product schema and FF01 code fields.
- `RUNS/ledger_summary.json` — 22-entry research custody summary.

No native/100k run, no product test matrix, no new sourcefree test was needed:
the decisive defects are static schema/code/contract mismatches. No author root,
product, protected PROGRAMMA, or prior C evidence was modified.
