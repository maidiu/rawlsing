# FFX002 R2 — DOWNSTREAM PRE-V3 ABLATION CONTRACT

Status: `DESIGN_ONLY__ACTOR_INDEPENDENT_INFORMATION_TEST`

## 1. Boundary

The downstream consumer is PRE-V3 only.

It may request bounded actor-independent possibility information. It may not:
- instantiate a person;
- assign beliefs to an individual;
- infer personality;
- claim motives;
- generate realized biography;
- convert distributions into deterministic actor states.

## 2. Neutral output packet

`PREV3_MULTI_VIEW_QUERY_RESULT {
  query_id;
  claim_scope_ref;
  common_semantic_input_manifest_hash;
  risk_set_ref;
  estimand_ref;
  support_and_uncertainty;
  direct_conditional_answer;
  exact_configuration_alternatives[];
  minority_and_counterpattern_alternatives[];
  optional_stable_local_geometry_relations[];
  higher_order_coexistence_where_lawful[];
  representation_dependence;
  information_loss_by_view[];
  observability_limits[];
  provenance_refs[];
}`

Fields absent because a view `DOES_NOT_REPRESENT` them stay absent with a typed reason.

## 3. Downstream arms

### P0 — `SUBSTRATE_CONDITIONAL_ONLY`
Core C + source/risk/support/provenance. Weakest useful possibility baseline.

### P1 — `P0 + CONFIGURATION_VIEW`
Adds Core A.

### P2 — `P0 + GEOMETRY_VIEW`
Adds Core B.

### P3 — `P0 + CONFIGURATION + GEOMETRY`
Core multi-view package.

Optional later:
- P4 + motif
- P5 + latent/model
only after separate admission.

## 4. What counts as downstream value

A view adds value only if it does at least one of the following on frozen holdout while passing its loss/hostile gates:

- improves bounded disposition-distribution fidelity;
- preserves required minority/counterpattern alternatives unavailable from the weaker packet;
- preserves required higher-order coexistence unavailable from the weaker packet;
- supplies a stable local neighborhood/order relation required by a preregistered query;
- materially reduces representation/query cost at equivalent required fidelity;
- exposes material representation dependence that the weaker packet would conceal.

## 5. Materiality guidance inherited from original FFX002

For the first canary, retain as preregistered engineering guidance:
- >=10% relative heldout log-loss improvement with paired descriptive 95% interval excluding zero; or
- >=4x smaller serialized representation at equivalent frozen-query fidelity; or
- a preregistered unique required relation/query becomes lawfully answerable and survives hostile/null tests.

These are canary thresholds, not universal epistemic constants.

## 6. Minority/contradiction veto

A smaller or more predictive packet is not superior if it systematically hides lawful minority alternatives or contradiction required by the query.

A view may therefore be:
`INCREMENTALLY_USEFUL__SUPPLEMENTARY_ONLY_DUE_TO_CRITICAL_LOSS`.

## 7. Representation dependence

For each query, compare lawful answers across P0–P3.

If material answer differences survive:
- common-input equality;
- support/uncertainty checks;
- hostile tests;
- representation-specific adequacy gates;

emit a typed `REPRESENTATION_DEPENDENCE` object rather than averaging the views.

## 8. Prohibited metrics

No:
- persona realism;
- story quality;
- sociological elegance;
- axis interpretability;
- LLM preference;
- personality prediction;
- theoretical-label agreement.

FFX002 R2 ends before realized-person design.
