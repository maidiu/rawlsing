# D2 — original SRC17 GSS 1973 C11 construction

This bounded campaign performs the TRUE-HQ-authorized original read of the exact
local SRC17 source through the existing source-read admission and SHA-checked
SAV decoder. It builds an original-bound C11 logical release over the largest
slice whose observed cells are fully covered by the accepted R157 SRC17 rules.

## Result

- Source: `GSS1973.sav`, SHA-256 `59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2`
- Rows/columns/bytes: 1,504 / 339 / 1,984,639
- Configured response slots: 279; selected complete response slots: 258
- Held unbound response slots: 21; selected coordinates: 2
- Release: `2f81b527ba1a62ecb79c7cc858063d60a10826a91af7d689606ed83e6bbd039e`
- Public objects: 779,078; internal records: 1,762
- Response events and routing facts: 388,032 each; coordinate facts: 3,008
- No weight facts; canonical response/coordinate values: none
- Local release bundle: outside Git under the user Library runtime root
- Cold replay: release identity and local bundle hashes match

The accepted config is reused unchanged. A derived runtime config binds the
reader's exact SAV user-missing classification (`-100..-10`) to the existing
response rules; response-state meaning and authority are unchanged. No fixture
authority, canonical ALLOW, routing ALLOW, weight design, or population claim is
created. Original row-wise products remain local; committed evidence contains
only nonidentifying refs, counts, hashes and refusal receipts.

## Limits

- Not an I03/I05 workload, not a population estimate, not an original semantic
  ALLOW, and not M2/M3/F1–F4 completion.
- ROUTING_UNKNOWN and weight-design held premises remain preserved.
- 21 response slots are held because observed values are not exactly covered by
  existing rules; exact per-slot counts are in `evidence/SLICE_SELECTION.json`.
- Distinct independent review is required for qualification.
