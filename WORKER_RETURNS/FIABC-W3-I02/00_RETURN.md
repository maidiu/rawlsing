# FIABC-W3-I02 — GOVERNED F018 EFFECTIVE-N SUCCESSOR

Worker: `FIABC-W3-I02`  
Repository: `maidiu/rawlsing`  
Branch: `agent/rabochii-premain-fiabc-w3-i02-effective-n-successor-r1`  
Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

## Terminal

`FIABC_W3_I02_EFFECTIVE_N_SUCCESSOR_IMPLEMENTED__READY_FOR_FANIN`

## Holding

The missing F018 effective-N operation now has a current governed PRE553 successor without reviving historical V550/V550J ownership and without changing I03/I05 semantic ownership.

The implementation is intentionally downstream of the current I03 truth owner:

1. I03 owns exact query, source/release provenance, risk-set/condition scope, denominator membership, and the weighted denominator when weighting is lawful.
2. C11 `WeightMeasureFact` owns each exact respondent weight plus its weight basis, source, effective scope, design authority ref, and estimand authority ref.
3. `pre553_effective_n.py` owns only the derived F018 measurement receipt: exact `sum_w`, exact `sum_w2`, exact effective-N, typed negative state, provenance, and deterministic replay/product identity.

No new public semantic-object family was introduced. No `EmpiricalFact` is minted or altered by this operation.

## Exact operation

Contract:

`PRE553_F018_EFFECTIVE_N@1.0.0`

Formula:

`SUM_W_SQUARED_OVER_SUM_W2_EXACT@1.0.0`

For a lawful governed weighted denominator:

`effective_n = (sum_w * sum_w) / sum_w2`

All computation uses exact `Fraction` arithmetic. Historical `numeric_formulas.effective_n_v1` was treated only as evidence of inherited function; it is not imported and is not made current authority.

A positive result binds:

- exact I03 `EmpiricalFact` identity;
- exact `EmpiricalQuerySpec` identity;
- exact source release refs already present in I03 provenance;
- exact source-universe refs;
- exact risk-set ref;
- exact condition-predicate ref;
- exact measure-basis ref;
- exact source-scope mode;
- target-topology identity;
- exact I03 denominator-member refs;
- exact query-owned `weight_basis_id`;
- exact caller-supplied authorized weight-scope ref;
- exact weight-fact refs and weight-source refs;
- distinct design-authority refs and estimand-authority refs;
- complete authority closure;
- exact `sum_w`, `sum_w2`, and effective-N;
- exact provenance refs;
- content-addressed replay identity;
- content-addressed product identity.

## No second semantic owner

The successor does not recompute routing, applicability, source semantics, target semantics, risk-set membership, or denominator membership. It accepts those only through the exact I03 fact/query identities.

A numerical effective-N is impossible unless:

- every exact I03 denominator member has exactly one supplied weight fact;
- every supplied weight fact belongs to that denominator and exact source universe;
- every weight fact has the exact query-owned weight basis;
- every weight fact has the exact authorized effective-scope ref;
- every weight fact ref is already present in the I03 fact provenance;
- every weight fact is `WEIGHT_VALID_AUTHORIZED`;
- the weight object's authority closure is positive;
- its explicit design authority resolves exact and positive as `WEIGHT_DESIGN_ESTIMAND`;
- its explicit estimand authority separately resolves exact and positive as `WEIGHT_DESIGN_ESTIMAND`;
- the exact summed weights reproduce I03's weighted denominator;
- `sum_w` and `sum_w2` are positive and nondegenerate.

The implementation never scans labels, names, values, source layout, or frequencies to discover a weight.

## RAW / current P2X disposition

For exact `RAW` / unweighted queries the operation returns:

`NOT_APPLICABLE`

with:

- `sum_w = null`;
- `sum_w2 = null`;
- `effective_n = null`.

A respondent count is never treated as an implicit all-ones weight vector. Supplying weight inputs to a RAW call is rejected as an integrity error.

This preserves the Wave-2 LiTS-I and WVS7 court law: the current frozen P2X workloads remain RAW/unweighted and do not acquire a fabricated numerical effective-N merely because exact respondent counts exist.

## Typed negative-state law

The successor defines only measurement-level result states:

- `SUPPORTED`
- `NOT_APPLICABLE`
- `NOT_AUTHORIZED`
- `INVALID_WEIGHT`
- `DEGENERATE_WEIGHT_SUM`
- `SCOPE_MISMATCH`
- `UPSTREAM_UNAVAILABLE`

Every non-`SUPPORTED` product is forbidden by constructor validation from carrying `sum_w`, `sum_w2`, or effective-N. Exact identity contradictions remain hard integrity failures rather than being laundered into an empirical negative.

## Hostile qualification added

`rawlsing_next/tests/test_pre553_effective_n.py` covers:

1. exact weighted effective-N, replay identity, and input-order invariance;
2. RAW/unweighted respondent counts cannot manufacture effective-N;
3. absent weight authority -> typed `NOT_AUTHORIZED`, no numeric fields;
4. invalid governed weight state -> typed `INVALID_WEIGHT`, no numeric fields;
5. zero/degenerate weight sums -> typed `DEGENERATE_WEIGHT_SUM`, not numeric zero;
6. mismatched authorized weight scope -> typed `SCOPE_MISMATCH`;
7. absent explicit weight scope -> typed `NOT_AUTHORIZED`;
8. governed-weighted query lacking exact `weight_basis_id` cannot infer a default weight;
9. design and estimand authority bindings are independently checked;
10. the effective-N weight set must reproduce the I03 weighted denominator.

## Tests not executed here

No runtime tests were executed by this worker because the commission restricts this execution surface to GitHub/browser repository tools and explicitly forbids local-machine work. No measured P2X execution was performed.

These exact non-measurement commands should be run after fan-in on the integrated execution surface:

```bash
python -m compileall rawlsing_next/pre553_effective_n.py rawlsing_next/tests/test_pre553_effective_n.py
python -m pytest rawlsing_next/tests/test_pre553_effective_n.py -q
python -m pytest rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_pre553_effective_n.py -q
```

Do not treat those unit/regression commands as authorization for measured P2X execution.

## Files

Implementation:

- `rawlsing_next/pre553_effective_n.py`

Focused tests:

- `rawlsing_next/tests/test_pre553_effective_n.py`

Return package:

- `WORKER_RETURNS/FIABC-W3-I02/00_RETURN.md`
- `WORKER_RETURNS/FIABC-W3-I02/01_IMPLEMENTATION_DIFF_INVENTORY.md`
- `WORKER_RETURNS/FIABC-W3-I02/02_TEST_AND_EXECUTION_PROTOCOL.md`
- `WORKER_RETURNS/FIABC-W3-I02/03_AUTHORITY_AND_NEGATIVE_STATE_CONTRACT.md`
- `WORKER_RETURNS/FIABC-W3-I02/RETURN.json`

## Exact blockers

None at this worker's bounded implementation grain.

The current frozen P2X workloads still have no positive weight/design/estimand claim by design. That is not a blocker to this successor; it means their effective-N disposition is lawfully nonnumeric.

