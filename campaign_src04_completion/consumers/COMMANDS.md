# Lane D commands

```sh
# Rebuild all lane-D evidence from the retained B0 fixture receipt and D1 ref.
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.generate_evidence

# Consume the retained B0 fixture fact through the existing OC01 consumer.
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run b0-fixture \
  --receipt campaign_src04_completion/consumers/evidence/B0_FIXTURE_POSITIVE.json \
  --out campaign_src04_completion/consumers/evidence/B0_FIXTURE_CONSUMER_PRODUCT.json

# Prove D1 tally refusal (never converted to EmpiricalFact).
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run refuse-d1-tally \
  --tally campaign_src04_completion/consumers/evidence/D1_TALLY_REF.json \
  --out campaign_src04_completion/consumers/evidence/NEGATIVE_D1_TALLY.json

# Future full source-local producer (lane A/C):
# the module must return ProducerBundle; no original read is performed by lane D.
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run native \
  --producer-module MODULE:FUNCTION \
  --expected-source-id SRC04 \
  --claim-ceiling SOURCE_LOCAL_STATISTIC \
  --use-scope SOURCE_LOCAL_STATISTIC \
  --out campaign_src04_completion/consumers/evidence/SRC04_SOURCE_LOCAL_CONSUMER_PRODUCT.json

# Focused tests.
PYTHONPATH=. python3 -m pytest campaign_src04_completion/consumers/tests -q -o addopts=''
```

Expected current results:

- B0 fixture consumer: `SUPPORTED_OBJECTIVE_RESULT` at
  `SUPPORTED_COMPONENT_ONLY`, explicitly fixture-only.
- D1 tally: `REFUSED` with
  `PRODUCER_FAMILY_REFUSED__D1_TALLY_NOT_EMPIRICAL_FACT`.
- Native command without a full producer: `BLOCKED` with
  `FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED`.
- Focused tests: 8 passed.
