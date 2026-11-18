# R3 G1–G5 recheck commands

All reads are from the shared Git store or product checkout; writes are only
under `R3_REVIEW/R2_RECHECK/`.

## Target / manifest / product

```
git -C /Users/matthewsmith/s2b-work/rawlsing rev-parse b567ceee8291b4927004dfc4b5b109ae29ba0294
git -C /Users/matthewsmith/s2b-work/rawlsing ls-remote origin refs/heads/agent/anvil-r3-downstream-accommodation-20261117-r1
git -C /Users/matthewsmith/s2b-work/rawlsing diff --stat 06e88a5ac7e4c14362a97a046f44e25d8eec4162 b567ceee8291b4927004dfc4b5b109ae29ba0294 -- rawlsing_next
```

Log: `RUNS/target_verify.txt` — 8/8 package hashes, 10 capability rows,
27 research entries, product diff empty, protected `5d387a` rev11.

## G1 / G2 / G3 / G5 claims

```
git show b567...:WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117/R3_DOWNSTREAM_ACCOMMODATION/R3_ARCHITECTURE_DECISION.md
git show b567...:.../R3_CAPABILITY_ACCOMMODATION.tsv
git show b567...:.../R3_FIELD_AND_ADAPTER_CONTRACT.md
git show b567...:.../R3_RESEARCH_LEDGER.jsonl
```

Log: `RUNS/g1_g5_checks.txt`, `RUNS/g4_checks.txt`,
`RUNS/research_checks.txt`, `RUNS/external_lookup_check.txt`.
Results: old 22 ledger entries byte-preserved; new 023–027; 24/23/10 research
refs resolve; FF01-2/FF01-k split correct; F6 fields correctly external/absent.
Residual: exact FF01-k field/receipt table absent; external source/codebook
lookup has no concrete artifact resolver.

## G4 view/adaptor counterexamples

```
git show b567...:.../R3_FIELD_AND_ADAPTER_CONTRACT.md | nl -ba | sed -n '40,132p'
sed -n '975,990p' rawlsing_next/_pre553_query_eval.py
sed -n '455,485p' rawlsing_next/_pre553_query_eval.py
sed -n '70,90p' rawlsing_next/pre553_empirical_query.py
sed -n '439,478p' rawlsing_next/pre553_direct_estate_i03.py
```

Logs: `RUNS/g4_checks.txt`, `RUNS/code_checks.txt`.
Decisive: state is in the identity keys; `SelectionMembership` is count-only
while `_build_fact` requires full risk/denominator member refs; selected-row
group RAM claim does not account for full-universe routing/denominator
membership.

No product test matrix, native/100k run, or sourcefree experiment was needed:
the remaining defects are static contract/schema/evaluator mismatches. No author
root, product, protected PROGRAMMA, or prior review evidence was modified.
