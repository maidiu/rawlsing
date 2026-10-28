# SRC04 full completion — lane D consumer

This lane wires a **stable native empirical product** to the existing bounded
OC01 consumer policy. It does not build a replacement empirical engine, does not
convert the D1 descriptive tally into an `EmpiricalFact`, and does not open or
decode the original SRC04 file.

## What is implemented

- `consumer.py`
  - `ProducerContract` / `ProducerBundle`: exact release, query, predicate, fact,
    source identity, authority refs, evidence tier, claim ceiling and use scope.
  - `consume_native_producer`: runs the existing
    `rawlsing_next.pre553_empirical_query.execute_empirical_query` and
    `replay_empirical_query`, verifies the exact fact/release/query/predicate
    identities and authority closure, then calls the existing
    `rawlsing_next.objective_consumer_bounded_evidence.evaluate_oc01_pre553_source_local`.
  - `consume_retained_b0_fixture`: consumes the retained B0 SRC09 P0
    nonrespondent/test-only fixture positive as **engineering evidence only**.
  - `refuse_d1_tally`: refuses a D1 descriptive tally as a producer family; no
    tally-to-`EmpiricalFact` conversion exists.
- `run.py`: exact consuming commands for fixture-only, native producer, and D1
  refusal modes.
- `PRODUCER_CONTRACT.json`: the exact source-local producer contract lane A/C
  must satisfy.

## Current status

The full SRC04 source-local producer is **not issued**: no original SRC04 file
was stat'ed, hashed, opened or decoded. The lane therefore returns:

- a real OC01 consumer positive from the **retained B0 fixture-only** fact
  (`SUPPORTED_COMPONENT_ONLY`, `fixture_only=true`, `source_value_sensitive=false`);
- all identity/authority/use negatives refused;
- the exact `FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED` blocker and producer contract
  for immediate joining by lane A/C.

The accepted 42-field release `fc111cfa…` is preserved as historical baseline;
it is not treated as the full 163/178-field producer and is not converted into a
tally-as-fact.

## Commands

```sh
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.generate_evidence
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
SRC04 source-local claim. No respondent cells or row-wise products are committed
or printed.
