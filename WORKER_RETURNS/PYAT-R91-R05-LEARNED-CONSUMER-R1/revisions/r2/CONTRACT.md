# R91 R05 R2 full product-graph consumer contract

Startup `31d77fd37c501954c088c786db20d8056b6748f5`; same OpenCode author.
This is the settled in-scope R05V repair, not new science/architecture.

## API

`NativeProductGraph(compositions=(AnalyticalCompositionResult,...),
extension_result=<E41 extension result or None>)`.

`evaluate_learned_world_consumer(..., product_graph=NativeProductGraph)`:

- keeps the single-composition positive call compatible;
- requires every graph component to share the same consumer query/model;
- validates every component source universe and producer predicate against the
  M1 disposition;
- evaluates each component's actual evidence independently through the unchanged
  N10E evaluator; no invented aggregation or learned geometry;
- binds joint component count/order, producer route(s), discovery receipt/frontier,
  recursive handoff/lineage and E41 extension route into the result/values;
- includes the E41 extension only when its composition is in the graph and its
  route is actual.

## Typed axes

`LearnedWorldConsumerResult` now carries eligibility/execution/result axes,
denominator, cells, graph refs and `z_unresolved`. Non-supported compositions
return typed `LEARNED_CONSUMER_ZERO_SUPPORT`, `LEARNED_CONSUMER_VALID_EMPTY`,
`LEARNED_CONSUMER_UNKNOWN` etc. with denominator/cells retained; Z UNRESOLVED
denominator 16 is marked `z_unresolved=True`. They are not collapsed to generic
REFUSED.

## Product-to-consumer matrix

| Actual product/route | Expected |
|---|---|
| M01->M1->M2->C1 conditional (single component) | exact supported consumer values |
| joint component fields | joint count/order validated and bound |
| discovery receipt/frontier | refs validated/bound; changed component changes/refuses |
| recursive handoff/lineage | refs validated/bound; modified mismatch refuses |
| E41 direct/multi/discovery/recursive extension | route/composition must match graph |
| blocked/empty learned product | typed refusal before serving |
| ZERO_SUPPORT / VALID_EMPTY / UNRESOLVED16 | typed axes/denominator/cells retained |
| missing current selection when required | typed refusal |

No live J42/P41/E04 service, source/science, F6/F7, CI/prod, N11/N12, Sorok,
J52/W52 or original data authority is claimed. Distinct review follows.
