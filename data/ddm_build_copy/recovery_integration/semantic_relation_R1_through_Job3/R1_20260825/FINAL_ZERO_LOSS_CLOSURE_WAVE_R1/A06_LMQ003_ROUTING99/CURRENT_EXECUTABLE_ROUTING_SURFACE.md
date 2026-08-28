# A06 — CURRENT EXECUTABLE ROUTING SURFACE

The current PRE553 predicate evaluator already supports an exact `ROUTING_APPLICABILITY_STATE` leaf. Its lawful positive path requires:

- an exact `question_semantic_ref`;
- an exact `routing_or_applicability_state_ref`;
- an exact `routing_authority_ref`;
- positive resolution of that exact authority snapshot;
- a matching `RoutingEligibilityFact`;
- the exact routing authority ref to bind that matched fact;
- an exact desired `routing_state`, checked against routing/applicability state.

This is sufficient **machinery** for exact routing evaluation. It is not the missing LMQ-003 authority.

For the historical 99 rows, A06 would additionally need a positively recovered exact historical-row identity plus row-specific source-native routing authority/provenance that can be compiled to the current predicate form. That membership/authority input was not recovered.

Binding negative ceiling:

`CURRENT_ROUTING_PREDICATE_ENGINE != HISTORICAL_99_ROW_MEMBERSHIP`

`EXACT_700_ROW_IDENTITY_CONTINUITY != PROOF_OF_WHICH_99_ROWS`

`SOURCE_COLUMN_PRESENCE != ROUTING_AUTHORITY`

`LATER_ROUTING_SIGNAL_STATUS != HISTORICAL_R3_PARTITION_MEMBERSHIP`

No production runtime change is justified by this court.
