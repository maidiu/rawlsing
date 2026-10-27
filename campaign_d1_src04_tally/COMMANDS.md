# D1 commands

```sh
# Build the accepted local-release aggregate tally
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode primary

# Focused field/partition/control/refusal checks
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode tests

# Fresh-process aggregate replay, including every field count
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode replay

# Assemble final RETURN.json
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode return \
  --artifact-commit <code-commit>
```

Pinned inputs:

- local C11 bundle: `SRC04-fc111cfa78d0fc23`
- release: `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- source: `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- source records: 7,337
- accepted fields: 42

No original SAV reread, I03/I05 issuance, weights, canonical scales, eligibility,
population or causal claim is part of D1.
