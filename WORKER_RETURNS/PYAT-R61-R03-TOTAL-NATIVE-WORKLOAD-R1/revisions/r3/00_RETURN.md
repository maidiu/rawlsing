# R61 R03 R3 successor author return — five demonstrated repairs

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r61-r03-total-native-workload-r1`
- Startup: `2d32d68e2a5acb9cac136c313e82068dfb8e6ba1`
- Contract commit: `8f2864ff648f63542746f69e6687de0d36117294`
- Code commit: `f87166a27d0e2e54ccc7e31fac58fa5487888035`
- R2 review: `3853c2a8c609e53cbc6d6ebf852540faa40bd6c2`
- Executor: same OpenCode DeepSeek V4.1-Flash MAX/Global.

## Repairs

1. **Cold expected native identity** — governed ledger now includes exact
   `expected_jobs`, expected candidate IDs, compilation material/hash, native
   receipts/facts, per-operation expected/received candidates, typed/coverage
   states, receipt refs and fact refs. Restore re-derives and verifies all
   relations, multiplicity and fact coverage. Self-consistent strips/duplicates/
   removals refuse.
2. **Live fact closure** — `execute_governed_frontier` now requires every
   receipt fact ref to resolve to a native fact and the receipt union to cover
   the native fact set; removing a receipt's fact refs makes adapter
   `no_drop_ok` false. The owner `native_receipt_anti_join` remains unchanged as
   required; closure is enforced in the authorized compositor.
3. **Expected native job/typed rows survive restore** — ledger exposes and
   restore checks jobs/candidates/rows; deletion refuses.
4. **Recursive root-release severance** — `bind_recursive_workload` checks
   snapshot checkpoint, campaign/root identity, nonempty root releases and exact
   equality with every receipt's release set; severance refuses.
5. **HELD/UNKNOWN separation** — compilation carries dispositions; rows keep
   `eligibility_state` and normalize HELD/UNKNOWN distinctly, including cold
   restore.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R03-TOTAL-NATIVE-WORKLOAD-R1/revisions/r3/junit.xml -o addopts=''
```

Exit `0`; `13 passed`, `0 failed/errors/skips`; `46.79s`. Retained R01 suite:
`32 passed`. JUnit/log included.

Successor tests cover stripped-self-rehashed ledger, removed fact refs,
expected-job/candidate persistence, count-preserving substitution, restored
ledger, held/unknown live and cold, recursive root severance, and retained
native governed D3 positives.

## Boundary

`native_receipt_anti_join` owner is unchanged; direct old probe H2 that calls the
owner alone still returns its old result. R03's authorized compositor now
enforces exact fact closure. The reviewer should target the R03 consumer
assertion. No R04 durable custody/cryptographic authority or original science
is claimed. R04/R05/R06/R07/N11/N12/CI/prod/J52-W52 remain NOT_REACHED.
Distinct reviewer required; no self-adoption.
