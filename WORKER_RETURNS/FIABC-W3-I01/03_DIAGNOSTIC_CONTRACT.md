# FIABC-W3-I01 — Governed Diagnostic Contract

Contract ID: `PRE553_GOVERNED_DIAGNOSTIC_SUCCESSOR@1.0.0`  
Product schema: `PRE553DiagnosticProduct@1.0.0`

## Ownership boundary

Truth input owner: existing governed I03 `EmpiricalFact` + `EmpiricalQuerySpec`.

Diagnostic computation owner: `rawlsing_next.pre553_diagnostics`.

Semantic/source truth owner after computation: unchanged.

The product is a diagnostic measurement artifact, not a new empirical semantic object family.

## Required exact inputs

For association diagnostics:

- exact I03 `EmpiricalFact`;
- exact matching `EmpiricalQuerySpec`;
- exact immutable authority registry resolving their authority closure;
- one or more exact source release refs that are already present in the I03 fact's provenance;
- exact arity-2 complete contingency projection for a computable association value.

For optional joint confidence, additionally:

- focus cell;
- support ratio;
- completion rate;
- effective-N ratio;
- pattern probability;
- exact determinant refs for those supplied components.

No label/frequency/carrier-layout inference is permitted.

## Metric contract

### Entropy reduction

`H(Y) - H(Y|X)`, Shannon base 2.

### Mutual information

`sum_xy p(x,y) * log2(p(x,y)/(p(x)p(y)))`.

### Normalized mutual information

`MI / max(H(X), H(Y))`; typed numerical zero only when the entropy denominator is mathematically zero.

### Cramér's V

`sqrt(chi2 / (N * min(r-1,c-1)))` using positive-support row/column dimensions.

### Uplift

Per joint cell `(x,y)`:

`P(Y=y | X=x) - P(Y=y)`.

### Lift

Per joint cell `(x,y)`:

`P(Y=y | X=x) / P(Y=y)`.

Zero row support or zero baseline support is typed not-applicable at that cell rather than forced to an ordinary score.

### Joint confidence

When every exact component is supplied:

`mean(clamp01(support_ratio), completion_rate, effective_n_ratio, pattern_probability) * 100`.

I01 does not create effective-N. Absence of exact confidence inputs is `UNCERTAINTY_UNQUANTIFIED`.

## Identity contract

The diagnostic replay core binds:

`fact ref + query ref + release refs + authority refs + I03 replay + producer replay roots + support determinants + confidence determinants + source provenance + typed states + metric contract/results`.

The replay ref is the SHA-256 identity of that determinant core.

The final product hash binds the determinant core plus the replay ref.

Both are recomputed on product construction; nested identity material is immutable.

## State contract

| Upstream/current condition | Diagnostic disposition |
|---|---|
| supported exact arity-2 joint fact | point diagnostics available |
| exact underpowered determinant | UNDERPOWERED; point values may be exposed only as underpowered diagnostics |
| uncertainty unquantified | state preserved; point association may remain available; quantitative joint confidence remains unquantified unless exact determinants are supplied |
| positive non-joint fact | NOT_APPLICABLE |
| NONCOMPARABLE | NONCOMPARABLE, no score |
| UNAVAILABLE | UNAVAILABLE, no score |
| UNRESOLVED | UNRESOLVED, no score |
| VALID_EMPTY | VALID_EMPTY, no score |
| INTEGRITY_FAILURE | INTEGRITY_FAILURE, no score |
| malformed claimed arity-2 projection | fail closed with diagnostic integrity error |

## Authority ceiling

Permitted purposes:

- `REPORTING`
- `RANKING_NONCONTROLLING`

Forbidden purposes include:

- empirical truth / I03 truth;
- I05 frontier membership or reachability control;
- structural authority or structural admission;
- semantic interpretation;
- source semantics.

A high diagnostic value has no authority-generating effect.
