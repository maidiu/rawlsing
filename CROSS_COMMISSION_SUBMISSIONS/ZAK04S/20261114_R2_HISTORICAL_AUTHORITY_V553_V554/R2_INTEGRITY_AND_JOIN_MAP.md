# R2 machine-readable evidence repair and closure limits

This is an additive integrity repair to ZAK04S R2's first documentary commit `967ee4e58559688fd85324f8ecce27b8b957d16f`: the initial `MECHANISM_RECONCILIATION.tsv` had deliberate `R2:OP` / `R2:SH` stable references without accompanying definitions and modern_op_ids used descriptive tokens. This later in-branch documentary correction **materializes definitions** for every referenced OP and SH and normalizes the five modern operation refs. No original T added, no source claim altered, no code/test/CI run.

**Join receipts (static table validation):** five edge IDs → 10 op traces → 20 shape definitions → five reverse readers → five authority-use records → 14 evidence IDs → five unjoins and five strictly bounded coverage entries. `FINDINGS.tsv` is intentionally zero rows (no new T), not a missing census. All six search rows now use the exact common R1 header. Scope remains nonexhaustive; five coverage cells are **not** five globally complete T×domain cells.

**Evidence boundary:** `HISTORICAL_PINNED_SOURCE_S1` / `ACCEPTED_HISTORICAL_RULE_S1` / `PROTECTED_CODE_STATIC_READER_S1`, NOT_RUN native selected source, actor and world issuance. Source inputs, authority issuer, reader execution and independent receiving remain separate.
