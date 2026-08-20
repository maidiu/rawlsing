# BROWSER / CODEX FORCE ALLOCATION

## Browser/HQ — default force
All source interpretation, law, contract specification, table disposition, test oracle construction, failure adjudication, and campaign control remain here.

## Codex/local executor — deliberately dumb force
Only four classes of job are authorized:

1. `EXECUTE_SOURCE_METADATA_PROBE` — run a frozen extraction script over exact file hashes and return JSON/Parquet/receipt; no interpretation.
2. `EXECUTE_DB_PROVENANCE_PROBE` — run frozen read-only SQL and return receipt; no interpretation.
3. `IMPLEMENT_FROZEN_DECODER_CARRIER_CONTRACT` — write code against exact tests/contracts; may not change fixtures or semantics.
4. `EXECUTE_HEAVY_INGEST_BAKEOFF_QUERY` — run exact commands/benchmarks and return artifacts/metrics.

Every local order must contain exact repo, base/head, allowed paths, input hashes, commands, prohibited actions, outputs and success/failure token.

No Codex cell may be asked to 'investigate what we should do', 'design the architecture', 'decide what missing means', or 'make it work'.
