# R51 exact stage and call graph

## Pinned inputs

| Input | Commit | Exact staged path |
|---|---|---|
| B49 | `b5600da96358f8526471d635a1befa8daa3f098b` | `candidate/rawlsing_next/pre553_inherited_source_rules.py`, `pre553_source_native_preimage_adapter.py`, `pre553_native_workload_binding.py`, `pre553_issued_workload.py` |
| G50 | `d379bafe36b8d89da27ea5bf33614d33aca7f2d2` | `candidate/g50/{types,fixture,enumerate,oracle,native_i05,native_map,plan,canaries}.py` |
| M48 | `91f70358a7682e983276e79777bc591841162392` | policy provenance only; no issued policy |
| H48 corpus | B49 return | `candidate/inputs/source_authority_corpus.json` |
| B49 selected package | B49 return | `candidate/inputs/selected_rule_package_lits_i.json` |
| G50 28-canary matrix | G50 artifact | `candidate/inputs/28_CANARY_DISPOSITION.csv`, `04_M48_CANARY_MATRIX.csv` |

B49 and G50 are independently authored returns. R51 applies no whole-branch merge, no source-teaching, no production edit and no original raw read. Exact byte-custody is in `EVIDENCE_MANIFEST.json`.

## Executed call graph

```text
B49 SourceAuthorityCorpus (35 source identities, H48 documentary records)
  -> select_source_rules(family='LiTS', wave='I')
       selected=50, held=7, excluded=1141, accounted items=1198
  -> build_authority_set + synthetic nonrespondent PhysicalSourceIncidence
  -> materialize_native_preimages
       administered B49 U items=2 (q301_2, q301_7); projection/C11
  -> R51 normalization: g50_bundle(b49)
       source_id=27, wave=I, exact B49 source_sha256
       q301_2/q301_7 + typed reserved roles; frozen domains, no outcome-derived E_pre
       G50 policy = R51-M48-PROPOSED-CANDIDATE-1, grade PROPOSED_TEST_ONLY
  -> g50.enumerate.enumerate_frontier
       17 eligible symbolic operations; E_pre root 1a9bffbe...; not G50's 432 toy
  -> find_eligible(DIST, q301_2)
       op urn:g50:op:b547e734c8fda66149098b314f5037aaa7325740f450ffc939f0a55e9249ffef
  -> lower_to_b49: one-target OperationFixture(q301_2, response=1)
  -> B49 build_projection_catalog -> RuntimeObjectCatalog + I03ExecutionRequest
  -> build_test_only_workload -> TEST_ONLY_SOURCEFREE issued workload
  -> execute_test_only_workload
       U43 admit/execute_issued_workload -> Route B/C11 -> I03 dispatch -> Batch
  -> EmpiricalFact@1.0.0 245098cf... (numerator=1, denominator=1)
  -> same consumer: PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0
```

No G50 `native_i05` call is in this joined path. G50 I05 is separately verified at 15/15 candidates and 13/13 tests; its own source is G50 synthetic `SYNTH-SRC-A`, so it is **not** claimed as the B49 joined consumer. This is the `R51_I05_NATIVE_JOIN_HOLD` edge.

## Actual file imports

`r51_joined_source_producer.py` imports the real staged B49 classes and functions and the real G50 `enumerate_frontier`; it does not reimplement source selection, symbolic enumeration or native execution. `candidate/rawlsing_next/__init__.py` is a path-shim only: B49 candidate modules first, accepted `rawlsing_next` base owners second.
