# R91 R05V R2 independent review — defects

## P1 — Graph fields are copied/echoed, not validated against actual native owners

Location:
`rawlsing_next/pre553_learned_world_composition.py::NativeProductGraph`,
`_graph_refs`, `evaluate_learned_world_consumer`.

`NativeProductGraph` validates only tuple-of-`AnalyticalCompositionResult`.
`_graph_refs` concatenates discovery/recursive refs, takes the first frontier,
sums joint counts and concatenates hashes. The success path uses only the
primary `composition` for values/consumer result and echoes the aggregate graph
fields. E41 validation only checks that a caller-supplied object has a
`composition_result` equal to a graph component and a truthy `producer_route`.

Independent probes (`probes/test_r05v_r2_graph_gap.py`):

```text
copied_graph_labels:
  joint_component_count=2 (actual composition=1)
  forged discovery/recursive refs echoed
  state=LEARNED_CONSUMER_EXACT_SUPPORTED

duplicate_component:
  graph=(composition, composition)
  state=LEARNED_CONSUMER_EXACT_SUPPORTED
  component_hashes duplicated

fake_e41_route:
  FakeExtension(composition_result=actual, producer_route="FAKE_ROUTE")
  state=LEARNED_CONSUMER_EXACT_SUPPORTED
  extension_route="FAKE_ROUTE" echoed
```

No actual multi-component/joint/recursive/discovery graph route is demonstrated
by the author; the only actual graph test is one composition plus direct E41.
The R05V R2 commission explicitly says copied labels, metadata keys and echoes
are not implementation.

Missing function: validate each actual component and E41 extension against
native evidence/receipt/frontier/lineage/root-parent, component order/count/
morphology and order semantics; reject duplicates/forged labels/fake extension;
bind actual native objects, and exercise a materially different actual
multi/joint/conditional/recursive/discovery route through existing owners.

## P2 — False exact support when producer and analytical state disagree

The success path requires `composition.producer_fact_state == "SUPPORTED"` and
non-null evidence, returns hardcoded `SUPPORTED`, and does not check
`composition.analytical_state`.

Probe `::test_non_supported_analytical_state_cannot_be_false_exact`:

```text
input: producer_fact_state=SUPPORTED, analytical_state=ZERO_SUPPORT,
       denominator=0, evidence present
observed: state=LEARNED_CONSUMER_EXACT_SUPPORTED,
          result_state=SUPPORTED, denominator=0
expected: typed ZERO_SUPPORT/non-exact or refusal, never exact support
```

The author's typed-status test sets both producer and analytical state to the
same value, so it does not cover disagreement. Missing function: validate the
complete native axes/evidence jointly before exact support; retain
ZERO_SUPPORT/VALID_EMPTY/UNKNOWN/HELD/Z16 without false exact/generic collapse.

## P3 — Duplicate consumer definition block

`rawlsing_next/pre553_learned_world_composition.py` contains two `__all__`
blocks and two copies of `NativeProductGraph`, `LearnedWorldConsumerResult` and
`evaluate_learned_world_consumer` (first around 1413-1719, second around
1952-2007; last wins). This is unrequested duplicate code and a maintenance
hazard; remove the duplicate block and keep one implementation.

## Already-qualified partial

- Author 36/36; R05V R1 probes 4/4; provider 43/43 with exact AT07 fixture;
  analytical composition 13/13.
- Actual single M01/C1 positive and direct E41 delegation; consistent-status
  typed ZERO_SUPPORT/VALID_EMPTY/UNRESOLVED16 cases pass.
- Accepted R03/R08/native/evaluator bodies unchanged.
