# SRC04 full completion — lane D consumer

This lane wires a **stable native empirical product** to an existing
value-consuming downstream owner and then to the existing bounded OC01 consumer
policy. It does not build a replacement empirical engine, does not convert the
D1 descriptive tally into an `EmpiricalFact`, and does not open or decode the
original SRC04 file.

## What is implemented

- `consumer.py`
  - `ProducerContract` / `ProducerBundle`: exact release, query, predicate, fact,
    source identity, authority refs, evidence tier, claim ceiling and use scope.
  - `consume_native_producer`: fixes the previously undefined authority helper,
    runs the existing `execute_empirical_query` / `replay_empirical_query`, then
    actually calls an existing downstream value owner:
    - `pre553_discovery_exact.execute_exact_bounded_discovery`, or
    - `pre553_effective_n.compute_effective_n` when it returns a supported
      weighted effective-N product.
    A ref-only bundle with neither effect is refused with
    `DOWNSTREAM_VALUE_CONSUMER_REQUIRED`.
  - `source_value_sensitive` is no longer hardcoded. It is true only for exact
    measured `SOURCE_LOCAL_CERTIFIED` evidence. Fixture mutation/restoration
    evidence sets `fixture_value_sensitive=true` while source-local remains false.
  - `consume_retained_b0_fixture`: preserved prior receipt-only engineering path.
  - `refuse_d1_tally`: refuses a D1 descriptive tally as a producer family; no
    tally-to-`EmpiricalFact` conversion exists.
- `b0_native_fixture.py`: rebuilds the retained B0 SRC09 P0 nonrespondent fixture
  through existing owners. It is explicitly fixture/test-only and never an SRC04
  source-local claim.
- `run.py`: native fixture command, native producer command, retained-receipt
  command, and D1 refusal.
- `PRODUCER_CONTRACT.json`: exact source-local producer and downstream-value
  contract lane A/C must satisfy.

## Current status

The full SRC04 source-local producer is **not issued**: no original SRC04 file
was stat'ed, hashed, opened or decoded. The lane therefore returns:

- a real **native value-consuming fixture positive** from the retained B0 SRC09
  nonrespondent fixture: OC01 `SUPPORTED_COMPONENT_ONLY`, discovery candidate
  `DISCOVERED_RESULT_SUPPORTED` (condition `1/1` vs substantive baseline `4/4`),
  effective-N `NOT_APPLICABLE` for the RAW grain;
- measured fixture mutation `q101 row-2 2.0 -> 1.0`: consumed fact support changes
  `1/1 -> 2/2`, discovery facts change, and restoration reproduces the original;
- all identity/authority/use negatives refused, plus fixture-label, fixture
  promotion and missing-downstream negatives;
- the exact `FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED` blocker and updated producer
  contract for immediate joining by lane A/C.

The accepted 42-field release `fc111cfa…` is preserved as historical baseline;
it is not treated as the full 163/178-field producer and is not converted into a
tally-as-fact.

## Commands

```sh
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.generate_evidence
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run native-fixture \
  --value-sensitivity-evidence campaign_src04_completion/consumers/evidence/VALUE_SENSITIVITY.json \
  --value-sensitivity-case original \
  --out campaign_src04_completion/consumers/evidence/B0_NATIVE_ORIGINAL_PRODUCT.json
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run b0-fixture \
  --out campaign_src04_completion/consumers/evidence/B0_FIXTURE_CONSUMER_PRODUCT.json
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run refuse-d1-tally \
  --out campaign_src04_completion/consumers/evidence/NEGATIVE_D1_TALLY.json
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run native \
  --producer-module MODULE:FUNCTION --expected-source-id SRC04 \
  --claim-ceiling SOURCE_LOCAL_STATISTIC --use-scope SOURCE_LOCAL_STATISTIC \
  --out campaign_src04_completion/consumers/evidence/SRC04_SOURCE_LOCAL_CONSUMER_PRODUCT.json
PYTHONPATH=. python3 -m pytest campaign_src04_completion/consumers/tests -q -o addopts=''
```

The native command without a producer module writes the exact blocker
`FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED` and returns non-zero; it never fabricates a
positive.

## Consumer boundary

The OC01 policy is a bounded evidence consumer with explicit claim ceilings. It
does not adopt FF/V553, population, weight, structural or canonical authority.
The B0 fixture positive is nonrespondent/test-only and is never promoted to an
SRC04 source-local claim. No original respondent cells or row-wise products are
committed or printed. The fixture mutation is an engineering value probe, not a
scientific edit.
