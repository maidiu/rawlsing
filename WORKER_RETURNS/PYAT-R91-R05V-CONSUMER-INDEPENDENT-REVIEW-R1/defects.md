# R91 R05V independent review — defects

## P1 — Single-composition canary is not the full R03/M1/M2/B5/I4/E41 consumer integration

Location:
`rawlsing_next/pre553_learned_world_composition.py::evaluate_learned_world_consumer`.

Signature (`inspect.signature`):
`learned, *, composition, consumer_query, model_rule, producer_query_ref,
producer_predicate_ref, require_current_selection=False`.

Only one `AnalyticalCompositionResult` is accepted. There is no product/evidence
collection, E41 extension result/route, discovery frontier, recursive handoff/
lineage, joint component set, minority/counterpattern disposition or conditional
graph input.

Independent probe
`probes/test_r05v_consumer_gap.py::test_joint_recursive_discovery_bindings_affect_consumer`:

```text
input composition: joint_component_count=2, discovery_receipt_refs=...,
discovery_frontier_ref=..., recursive_handoff_refs=...,
recursive_lineage_refs=...
observed: state=LEARNED_CONSUMER_EXACT_SUPPORTED
consumer values keys: b5_selection_receipt_ref, consumer_query_ref,
consumer_result_hash, consumer_result_state, consumer_values_read,
evidence_ref, learned_receipt_ref, m1_disposition_ref, m2_release_ref,
producer_predicate_ref, producer_query_ref, product_contract_ref, schema
missing: joint_component_count, discovery_receipt_refs, recursive_handoff_refs,
producer_route
```

The E41 extension direct route is separately actual and delegates correctly, but
its result is not an input to this learned consumer; the extension's
multi/discovery/recursive routes are likewise not bound by the R05 consumer.
The author's four new tests exercise one M01 case, one C1 composition and one
direct E41 call. They do not cover joint/conditional/recursive/minority/
counterpattern integration, so they cannot establish full R05.

Exact missing function: accept and validate the complete actual native product
graph (M1 minority/counterpattern/axes, M2/B5 currentness, I4 joint/conditional/
recursive/discovery components, E41 route/receipt) and feed it to the unchanged
N10E consumer, with each component's refs/facts/evidence affecting the same
assertion and sever/restore proof.

## P2 — Typed status/axes are collapsed to generic refusal

Location:
`rawlsing_next/pre553_learned_world_composition.py::evaluate_learned_world_consumer`.

The function checks only `composition.producer_fact_state == "SUPPORTED"` and
evidence presence, then returns `_learned_refusal` with
`EMPIRICAL_EVIDENCE_NOT_SUPPORTED` for non-exact cases. It ignores
`composition.analytical_state`, denominator/cells/axes and ZUNRESOLVED, and
`LearnedWorldConsumerResult` has only `LEARNED_CONSUMER_EXACT_SUPPORTED` or
`REFUSED` states with `consumer_values_read=None` on refusal.

Independent probe
`probes/test_r05v_consumer_gap.py::test_typed_status_axes_are_preserved_by_consumer`:

```text
ZERO_SUPPORT  -> REFUSED / EMPIRICAL_EVIDENCE_NOT_SUPPORTED
VALID_EMPTY   -> REFUSED / EMPIRICAL_EVIDENCE_NOT_SUPPORTED
UNRESOLVED16  -> REFUSED / EMPIRICAL_EVIDENCE_NOT_SUPPORTED
```

Observed zero cells exist only inside the single exact-supported composition;
the wrapper does not distinguish observed zero from absent/valid-empty/held and
does not preserve all-missing Z UNRESOLVED denominator 16. This violates the
R05/R05V status requirement.

Exact missing function: project the complete empirical/consumer status axes
through the learned consumer result (eligibility/execution/result, denominator/
cells, observed zero vs absent/valid-empty, unsupported/held, Z UNRESOLVED16)
and typed-refuse only the genuinely inapplicable cases.

## What already holds

- Actual M01 → discovery/facts → M1 RULE_SATISFIED → M2 release/protocol → C1
  evidence → unchanged N10E `EXACT_SUPPORTED`; consumer hash
  `8e54f8b0...`.
- Single-case blocked-product, wrong-predicate and wrong-query refusals restore
  the positive.
- E41 direct extension delegates to accepted provider/composition and produces
  the same consumer hash; source is not a duplicate evaluator.
- Author 34/34; provider suite 43/43 after exact AT07 fixture materialization
  (the author's 8 fixture-missing tests are materialized and pass; 34+43=77,
  not 69/8 passes). No semantic fixture failure remains.
- Accepted R08 blobs and accepted C1/provider/evaluator/empirical owners are
  unchanged; R05 code is exactly three allowlisted paths plus its return.
