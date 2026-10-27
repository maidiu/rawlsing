# Campaign B0 — SRC04 consumer preparation

This bounded campaign prepares the missing consumer seam between the frozen
SRC04 source-native C11 release and the existing I03/I05 owners. It does not
execute an original query, read the original SAV, or read the local original
release bundle.

## Scope

- Source-native C11 release: `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- Exact 42 accepted response fields and two coordinates from the accepted
  Campaign A slice.
- Raw unary source-native distribution request identities are prepared over the
  42 fields.
- Original semantic authority remains `DEFER`; canonical values remain withheld.
- Routing remains `ROUTING_UNKNOWN`; no eligibility or population inference.
- The original request is not a query: it is a blocked request plan until the
  exact competent issuer supplies operation/predicate authority, target use if
  needed, runtime catalog preimages, historical parent, and routing/risk-set
  decision.
- The SRC04 nonrespondent fixture remains a typed `UNAVAILABLE` negative because
  its routing/authority is held; it is not promoted.
- A separately labelled SRC09 P0 nonrespondent fixture is used for the existing
  consumer positive seam: it constructs a real query/catalog and returns a
  `SUPPORTED` `EmpiricalFact` with independently checked 1/1 support. Its
  test-only authority is never reused for an original request.

## Commands

```sh
PYTHONPATH=. python3 -m pytest campaign_b0_src04/tests -q -o addopts=
PYTHONPATH=. python3 campaign_b0_src04/run.py --artifact-commit <code-commit>
```

The runner writes only `campaign_b0_src04/evidence/*` and
`campaign_b0_src04/RETURN.json`. It reads committed Campaign A metadata, the
pinned program, the SRC04 config, and the permitted fixture. No original source
or local original release is opened.
