# HQ280 WVQ — Append-only WVF T3 typed-count corrigendum

**Target original file, unchanged:**
`WORKER_RETURNS/PYAT-HQ280-WVF-WVS7-Q291-ORIGINAL-OPERATION-BINDING-R1/03_INDEPENDENT_EXPECTED_VS_46_ACTUAL.json`
at WVF return commit `b3c460c6ba2d1f750905f5ef95429065d7904ff5` / Git blob `38310b626e65a6629345821372ab439422657f95`.

**Incorrect field:** `cross_oracle_grain_preservation.t3_coverage_limited_count = 0`.

**Corrected field:** `cross_oracle_grain_preservation.t3_coverage_limited_count = 46`.

**Original source of correction:** actual retained T3 oracle
`WORKER_RETURNS/PREMAIN-FIABC-LITS-INDEPENDENT-ACCEPTANCE-T3-FREEZE-R1/court/oracles/WVS7.standard.json`
at exact Git blob `60146f39598b7dae2e87cf30a1e88954db404022` (read at WVQ sealed tip), with
`expected_learned_product.coverage.candidate_count = 46`,
`expected_learned_product.coverage.typed_terminal_counts.COVERAGE_LIMITED = 46`,
`len(expected_fact_manifest) = 46`; all 46 manifest entries have `typed_state = COVERAGE_LIMITED`.

**Preserve:** ordered candidate 46/46 exact frontier (zero adds, zero drops); `frontier_digest cf8255816dc2ba5a51f6fc5918f09e901a5190f147a5192bd805f2908987299e` identical R1M/T3; `authority_closure_digest b9be2091764654a91e6b2c62e6e05311c677b60af3b5d8b942f5041280e056c4` identical. Pre-I05 expected identities at GATE_3 are **not** pre-I05 truth. Truth oracle built at GATE_6, after two I05 executions at GATE_5.

**Additional grading clarification from the original T3 JSON, not a second mutation:** the T3 `expected_fact_manifest` contains 46 candidate dispositions and 58 query-role fact entries; **all 58** `support_uncertainty_state.fact_states` are `UNAVAILABLE` and all **58** `raw_denominators` are **zero**. Fact *reference* existence does **not** prove supported respondent measurements or positive scientific execution eligibility. Do not conflate `COVERAGE_LIMITED` candidate count with substantive positive EmpiricalFact outputs. This observation qualifies WVF prose claiming "actually measured"; it does NOT erase the already proved candidate-frontier no-drop.

**Method:** direct read of original retained T3 JSON; no raw SAV, no new I05, no rewrite of WVF/T3 files. This document is an append-only correction.
