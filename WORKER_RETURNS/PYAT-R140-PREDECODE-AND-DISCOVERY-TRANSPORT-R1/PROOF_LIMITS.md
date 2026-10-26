# R140 proof limits

- Synthetic SAV values only; no actual source package, checkpoint, original file,
  all35 wave, learned product or FF/V553 output.
- The predecode `IssuedSourceReadDecision` and discovery authorities are test
  harness objects constructed in tests. Their fixtures prove ordering, exact
  field binding, native execution and refusal behavior only. They are not actual
  source/scientific/current grants.
- `ORIGINAL_SOURCE_GRANTED` in the discovery test is a transport code-path label.
- The source-read decision test proves the wrapper does not touch the path before
  the resolver callback and does not call decoder/open/stat/read on refusals. It
  does not establish a trusted deployment resolver or issuer.
- Discovery uses a synthetic scalar source and the existing R01 frontier/lowering
  law. Its 150-candidate declared frontier, 98 supported and 52 valid-empty
  receipts are fixture-scope only, not all35/representative science.
- Source response fixtures are deleted after tests; no source output is retained.
