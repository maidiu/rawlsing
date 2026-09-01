# FFX002 — DOWNSTREAM ABLATION CONTRACT

Status: `DESIGN_ONLY__PRE_V3_INTERFACE_TEST`

## 1. Jurisdiction

This is an information/utility test for a **PRE-V3 actor-independent possibility packet**. It does not generate a persona, infer an individual's beliefs, score psychological plausibility, or design V3 personality machinery.

Question:

> Given an exact positioned query and the governed empirical canary, does a geometric view add information or compression beyond the direct atlas, and does the atlas preserve important empirical alternatives that geometry discards?

## 2. Frozen downstream target

Define a neutral packet schema before either representation is built:

`PREV3_POSSIBILITY_QUERY_RESULT {
 query_id;
 exact_position_query;
 risk_set_ref;
 estimand;
 support_posture;
 disposition_outcome_distribution;
 higher_order_complex_distribution_where_lawful;
 minority_alternatives[];
 uncertainty_posture;
 evidence_level;
 observability_limits[];
 provenance_refs[]
}`

No field may contain a realized actor state.

## 3. Query families

Freeze from the design partition/schema:

1. high-support exact position configurations;
2. minority but observed position configurations;
3. sparse configurations requiring lawful walkback/backoff;
4. configurations that differ by one authorized position state;
5. configurations crossing at least two position-role families;
6. disposition targets containing at least one order>=3 lawful joint/complex;
7. counterpattern queries where the modal disposition does not exhaust the observed distribution.

## 4. Ablation arms

### A0 — `MARGINAL_BASELINE`

Uses only global/risk-set disposition marginals plus exact support/observability metadata. No position representation.

### A1 — `ATLAS_ONLY`

Uses compact atlas configuration/dependence objects plus its frozen hierarchical walkback decoder. Exact raw facts remain available for evidence/replay but the consumer is charged the compact representation size.

### A2 — `GEOMETRY_ONLY`

Uses frozen position/disposition coordinates, distances/neighborhood summaries, and a decoder trained only on the design partition. No atlas configuration IDs or motif flags may enter.

### A3 — `ATLAS_PLUS_GEOMETRY`

Uses A1 plus geometric coordinates/neighborhood summaries. This isolates **incremental geometry value beyond atlas**.

### A4 — `GEOMETRY_PLUS_ATLAS`

Same combined information as A3, evaluated from the geometry baseline perspective to isolate **incremental atlas value beyond geometry**. A3/A4 may share one underlying fitted combined decoder; the comparison reference differs.

## 5. Common decoder discipline

Where a probabilistic decoder is needed, use the same preregistered decoder family across arms as far as representation shape permits. Recommended bounded canary decoder:

- regularized multinomial logistic model for categorical single-item targets;
- regularized multinomial model for enumerated supported complex states;
- hyperparameters selected by design-partition cross-validation only;
- no semantic labels or LLM judgments as features;
- final scoring only on frozen holdout.

Atlas direct conditional queries that require no model are also reported separately; do not force an unnecessary learned decoder merely to make the atlas geometric.

## 6. Primary downstream metrics

Report per target/query family and overall vectors:

- M03 held-out conditional-distribution total variation;
- M04 held-out log loss;
- M05 higher-order J preservation;
- M06 counterpattern preservation;
- M15 representation size/query latency;
- M16 compression-fidelity curve;
- M17 incremental information gain.

No one metric dominates by fiat.

## 7. Material incremental value

Geometry supplies `MATERIAL_INCREMENTAL_VALUE_BEYOND_ATLAS` only if at least one of these holds **without violating preservation/hard gates**:

1. A3 reduces held-out log loss relative to A1 by >=10% and the paired 95% descriptive bootstrap interval for the delta excludes zero; or
2. A2/A3 achieves equivalent frozen-query fidelity (median M03 TV within .02 of A1 and required minority/J recall gates) at >=4x smaller serialized representation cost; or
3. geometry supplies a stable neighborhood/rank relation required by a declared downstream query that atlas intentionally cannot express without introducing a metric, and that relation survives the geometry stability/null courts and improves held-out empirical reconstruction.

Atlas supplies `MATERIAL_INCREMENTAL_VALUE_BEYOND_GEOMETRY` if A3/A4 vs A2 meets the analogous predictive criterion **or** if atlas preserves required exact/minority/higher-order facts beyond geometry's preservation tolerances.

The numerical bars are preregistered engineering materiality rules for this bounded duel, not universal epistemic thresholds.

## 8. Minority/contradiction veto

A downstream compression gain is not admissible as a primary-role victory if it is purchased by systematic erasure of minority alternatives.

For primary-role candidacy:

- geometry M02 minority recall >=.90;
- high-support configuration recall >=.95;
- median nonmodal/counterpattern probability-mass error <=.02 relative to atlas/raw heldout empirical target;
- higher-order J recall >=.90 on the frozen high-support J set.

Failure of these does not prove geometry useless. It restricts it to a derived/diagnostic role unless the atlas itself also fails the relevant empirical target.

## 9. Sparse-query test

Atlas faces its hardest consumer test where exact high-order configurations are sparse. Its walkback path must state exactly which positional predicates were removed and expose the lower-order evidence used.

Geometry faces the reciprocal test: it may interpolate through a neighborhood, but must prove that the neighborhood is stable, exposure-lawful, and not created by arbitrary encoding/block choices.

Compare held-out error and uncertainty posture on the same sparse-query manifest.

## 10. Packet audit

Every returned packet must allow a downstream consumer to know:

- what was actually observed;
- what was directly estimated vs geometrically/model-derived;
- what support/risk set applies;
- what minority alternatives exist;
- what information was unavailable;
- how to replay the result.

A smaller packet that hides these distinctions is not superior compression; it is information loss.

## 11. Prohibited scoring

Do not use:

- LLM preference for which representation tells a better story;
- axis interpretability scores;
- sociological elegance;
- persona realism judged by prose;
- personality typing accuracy;
- any V3 realized-life outcome.

FFX002 ends at actor-independent empirical representation adequacy.
