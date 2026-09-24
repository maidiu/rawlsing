# FIABC-W3-I02 — Test and Integrated Execution Protocol

## Browser/GitHub worker execution status

Tests were authored and statically reviewed from the repository surface. They were not executed by this worker because this commission permits GitHub/browser repository tools only and forbids local-machine execution.

No measured P2X execution was performed.

## Exact focused commands for the integrated/local execution surface

Run from repository root after Wave-3 fan-in:

```bash
python -m compileall rawlsing_next/pre553_effective_n.py rawlsing_next/tests/test_pre553_effective_n.py
python -m pytest rawlsing_next/tests/test_pre553_effective_n.py -q
python -m pytest rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_pre553_effective_n.py -q
```

Expected focused collection: ten tests in `test_pre553_effective_n.py`.

## Acceptance criteria

The focused suite must establish all of the following:

- weights 1 and 2 at one exact governed scope produce exact `sum_w=3`, `sum_w2=5`, `effective_n=9/5`;
- presentation order of exact weight facts does not change product/replay identity;
- deterministic replay reproduces exact product and replay refs;
- RAW/unweighted denominator counts return `NOT_APPLICABLE` and no numerical fields;
- missing exact weight authority returns `NOT_AUTHORIZED`;
- invalid weight state returns `INVALID_WEIGHT`;
- all-zero/degenerate exact weights return `DEGENERATE_WEIGHT_SUM`;
- wrong effective-scope ref returns `SCOPE_MISMATCH`;
- missing explicit weight scope returns `NOT_AUTHORIZED`;
- a governed-weighted query without exact `weight_basis_id` cannot infer a default;
- denied/missing estimand authority cannot be hidden by positive design authority;
- a supplied weight set that does not reproduce I03's weighted denominator cannot emit numerical effective-N.

Every non-`SUPPORTED` result must retain `sum_w=None`, `sum_w2=None`, and `effective_n=None`.

## P2X law after this patch

The frozen LiTS-I and WVS7 P2X workloads are RAW/unweighted under the Wave-2 claim-scoped authority closure. Therefore their lawful F018 effective-N result is nonnumeric `NOT_APPLICABLE`; these unit tests must not be used as a pretext to introduce an all-ones default weight vector or a default estimand.

## Stop conditions

Stop and fail closed if the integrated tree introduces any of the following:

- a caller that derives `weight_basis_id` from labels/names/frequencies;
- a caller that supplies an effective weight scope not backed by exact authority;
- a caller that converts RAW respondent count to effective-N;
- a caller that drops either design or estimand authority binding;
- a caller that supplies weight facts absent from the exact I03 fact provenance;
- any result in a nonpositive state carrying partial numeric sums;
- any attempt to use this measurement receipt as I03 truth, I05 frontier control, or structural authority.

