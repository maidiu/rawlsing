# Fixture details

- Existing `_Sink` / `_IndexSink` native test carrier format.
- Historical DEFER: `SOURCE_SEMANTICS_TOPOLOGY`, `decision_state=DEFER`,
  scope `EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY`.
- Universe authority snapshot refs include the exact historical DEFER ref at
  construction.
- Seven recorded raw categories plus explicit system missing and absent row.
- No reader/index/authority monkeypatching in fixture construction or entry.
- Exact release/event-locator/manifest rows are written to the temporary
  fixture; no original estate is modified.
