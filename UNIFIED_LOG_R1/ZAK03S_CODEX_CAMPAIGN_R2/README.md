# ZAK03S_CODEX_CAMPAIGN_R2 — producer/binding documentary return

This is the R2 source tract for ZAK-03S. It preserves the frozen R1 package at `0098b058…::UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R1/` and does not edit it. The question is who actually produces `StructuralAdmissionRule` and `target_use_permission_refs`, and what binds them to selected source/QSM/version/row.

**Start here:** [00_RETURN.md](00_RETURN.md) → [HUMAN_STORY.md](HUMAN_STORY.md) → [SCOPE_CONTRACT.md](SCOPE_CONTRACT.md) → [CASES/ZAK03S_CASE_R2_RULE_PRODUCER_MAP.md](CASES/ZAK03S_CASE_R2_RULE_PRODUCER_MAP.md) → [PRODUCER_CONSUMER_MAP.tsv](PRODUCER_CONSUMER_MAP.tsv).

**Exact cuts:** protected `6a5c12f04323d74001f9632063ec907f4fc4468e`; historical `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`; candidates `b5600da9…`, `d81bc2c6…`, `ad17076c…`, `0d90c247…`. **Grade:** S0/S1 static documentary only; test modules read as fixtures, not executed. **Status:** no protected non-test rule producer found; selected-QSM candidate binds to I03, not I04; receipt consumer is real but test-called. `OPEN_PROOF_GAP`, not global absence.
