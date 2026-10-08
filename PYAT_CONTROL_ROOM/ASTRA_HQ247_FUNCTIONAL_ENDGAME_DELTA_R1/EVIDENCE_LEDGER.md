# P0 evidence ledger — baseline bank

Audit evidence only; no HQ adoption. Entry Git census and its read-only reproducer are in `phases/`.

- **P0-E01 / CONFIRMED:** Direct control `675b0793fd2a2b75463fc00d2b884eefdc95e9f9` selects HQ248 packet `91595263d2888091e1f28af1ed38429b7c02966f`. All packet checks passed. Exact bindings and observation interval: `phases/P0_GIT_CENSUS_ENTRY.json`. Disproof: newer direct control ref or mismatched manifest/blob.
- **P0-E02 / CONFIRMED at Git grain:** R3 refcount branch unchanged; T1 `58934231d6e5bc895f937b069433237f7edce594` and N10E `e64379e542b931df1e7df47f1b37955a1cb9a3a9` descend from commissioned tips, modifying only their respective return directories. Content review pending in this bank. No local worker status inferred.
- **P0-E03 / CONFIRMED:** HQ248 has adjudicated the prior three HQ247 returns. Exact decision record and immutable CURRENT read; f09 review covers frozen f09 only, R2 remains partial, N10E prospective documentary warrant is not issuer activation. Disproof: superseding sealed HQ record.
- **P0-E04 / CONFIRMED:** Pointer legacy `last_hq_decision` says HQ247 while manifest/CURRENT and explicit `hq248_decision` agree on HQ248. Read operative packet rather than using the legacy scalar alone. No pointer mutation authorized.

Next: inspect full return artifacts, inherited Atlas, and governing functional laws; seed F1–F8 without mistaking inherited status for fresh runtime proof.
