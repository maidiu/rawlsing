# Lane D commands

```sh
# Rebuild all lane-D evidence from the retained B0 fixture receipt, the native
# B0 engineering seam, and the D1 refusal ref.
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.generate_evidence

# Execute the fixed native value-consuming path on the retained B0 fixture.
# The product is explicitly fixture-only; OC01 is policy, discovery is the
# actual value-consuming owner.
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run native-fixture \
  --value-sensitivity-evidence campaign_src04_completion/consumers/evidence/VALUE_SENSITIVITY.json \
  --value-sensitivity-case original \
  --out campaign_src04_completion/consumers/evidence/B0_NATIVE_ORIGINAL_PRODUCT.json

# Execute the one-cell upstream value mutation (q101 row 2: 2.0 -> 1.0).
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run native-fixture \
  --mutate-q101-2-to-1 \
  --value-sensitivity-evidence campaign_src04_completion/consumers/evidence/VALUE_SENSITIVITY.json \
  --value-sensitivity-case mutated \
  --out campaign_src04_completion/consumers/evidence/B0_NATIVE_MUTATED_PRODUCT.json

# Restore the original fixture and prove the consumed result returns to 1/1.
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run native-fixture \
  --value-sensitivity-evidence campaign_src04_completion/consumers/evidence/VALUE_SENSITIVITY.json \
  --value-sensitivity-case restored \
  --out campaign_src04_completion/consumers/evidence/B0_NATIVE_RESTORED_PRODUCT.json

# Preserved prior receipt-only fixture path (engineering evidence only).
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run b0-fixture \
  --receipt campaign_src04_completion/consumers/evidence/B0_FIXTURE_POSITIVE.json \
  --out campaign_src04_completion/consumers/evidence/B0_FIXTURE_CONSUMER_PRODUCT.json

# Prove D1 tally refusal (never converted to EmpiricalFact).
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run refuse-d1-tally \
  --tally campaign_src04_completion/consumers/evidence/D1_TALLY_REF.json \
  --out campaign_src04_completion/consumers/evidence/NEGATIVE_D1_TALLY.json

# Future full source-local producer (lane A/C):
# the module must return ProducerBundle with a substantive downstream value
# consumer (discovery input or supported weighted effective-N input); no original
# read is performed by lane D.
PYTHONPATH=. python3 -m campaign_src04_completion.consumers.run native \
  --producer-module MODULE:FUNCTION \
  --expected-source-id SRC04 \
  --claim-ceiling SOURCE_LOCAL_STATISTIC \
  --use-scope SOURCE_LOCAL_STATISTIC \
  --out campaign_src04_completion/consumers/evidence/SRC04_SOURCE_LOCAL_CONSUMER_PRODUCT.json

# Focused tests.
PYTHONPATH=. python3 -m pytest campaign_src04_completion/consumers/tests -q -o addopts=''

# Frozen independent review witness.  The defect discriminator is intentionally
# RED after the repair because it asserts the historical omission.  Do not edit it.
PYTHONPATH=. python3 -m pytest campaign_src04_completion/empirical/review/test_cd_boundary_review.py -q -o addopts=''
```

Expected current results:

- Native B0 fixture: `FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE`, OC01
  `SUPPORTED_OBJECTIVE_RESULT` at `SUPPORTED_COMPONENT_ONLY`, discovery
  `DISCOVERED_RESULT_SUPPORTED`, effective-N `NOT_APPLICABLE`.
- Retained B0 receipt path: `SUPPORTED_OBJECTIVE_RESULT` at
  `SUPPORTED_COMPONENT_ONLY`, explicitly fixture-only.
- Mutation: fact support `1/1` -> `2/2`; restoration returns to `1/1`.
- D1 tally: `REFUSED` with
  `PRODUCER_FAMILY_REFUSED__D1_TALLY_NOT_EMPIRICAL_FACT`.
- Native command without a full producer: `BLOCKED` with
  `FULL_SRC04_SOURCE_PRODUCT_NOT_ISSUED`.
- Joined C observed profile: exact status/contract/entire ledger preserved on
  the primary product and both discovery facts.
- Frozen review defect discriminator: intentionally RED (`1 failed, 7 passed`);
  the review-owned test is unchanged and remains the historical witness.
- Focused consumer tests: 15 passed.
