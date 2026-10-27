# Campaign B0 commands

From the repository root:

```sh
# Focused adapter/evidence checks
PYTHONPATH=. python3 -m pytest campaign_b0_src04/tests -q -o addopts=

# Generate the blocked original request plan, fixture-only construction positive,
# discriminating negatives, and RETURN.json
PYTHONPATH=. python3 campaign_b0_src04/run.py --artifact-commit <code-commit>
```

Expected original result: a 42-request exact source/release/field plan with
`query_constructed=false` and exact missing-authority dependencies. The SRC04
fixture remains a typed `UNAVAILABLE` negative. Expected positive fixture result:
the separately labelled SRC09 P0 nonrespondent fixture constructs an actual
`EmpiricalQuerySpec`/`RuntimeObjectCatalog` and executes to `SUPPORTED` 1/1,
with the count independently checked from fixture cells. Expected negatives:
release identity mismatch and non-administered fixture target.

Pinned inputs:

- Program: `campaign_a_src04/evidence/PROGRAM.txt`
  SHA-256 `9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50`
- C11 release: `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- Source: `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
