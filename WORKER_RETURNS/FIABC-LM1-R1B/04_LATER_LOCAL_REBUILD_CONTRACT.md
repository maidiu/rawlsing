# Later local rebuild contract

## Authorized sequence

1. Confirm the successor authority identity 1be0cccc9938a8ad5594faa58d516ef6574b2daf3182d2ef9cb04a2435bfea88.
2. Confirm there is no already-successful replacement receipt under this authority.
3. Verify canonical LiTS-I SHA-256 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09.
4. Build one fresh LiTS-I Candidate-A R5 with R5CompactLongShardedBuilder blob 92e364b31eaf27be1bca2081eff65f6ffb779c3d and the frozen build defaults.
5. Charge actual observed work as EXECUTED_NOW under T4 C2.
6. Seal the canonical-source receipt, derivative receipt, and parentage bundle, including exact receipt and bundle identities.
7. Require the derivative receipt to bind the physical root, logical stream, row count, member inventory, release, reader/config, builder, operation, candidate ownership, and runtime/workload/currentness determinants.
8. Supply RAWLSING_EE_P2X_LITS_A_R5_ROOT, RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT, and RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT_IDENTITY to the current live court.
9. Continue the existing P2 stage law only after the replacement is admitted.

## Distinguishing old and new

OLD UNPARENTED HISTORICAL R5 has classification PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY, no admissible generic bundle for its first build, and numeric credit zero.

NEW CURRENT R35-PARENTED REPLACEMENT R5 has an EXECUTED_NOW build event plus an externally sealed and exactly pinned FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0 closing to the canonical source and current fixed determinants.

A self-asserted source SHA, copied path, internally consistent root, or plausible metadata cannot convert the old carrier into the new one.
