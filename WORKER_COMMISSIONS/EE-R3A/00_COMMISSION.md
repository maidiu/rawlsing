# EE-R3A — N04-R4A 18,012 selector reseal

You are **EE-R3A — RESPONSE SELECTOR RESEAL**.

Repository: `maidiu/rawlsing`

Exact grain: `DETERMINISTICALLY_RESEAL_ONE_CANONICAL_18012_ID_SELECTOR_FROM_ACCEPTED_N04_R3_STATUS_VECTOR_AND_CANONICAL_LEDGER_ONLY`

Read current canonical HQ authority from `HQ_HANDOFF/LATEST.json`, then this commission.

Inputs to reconcile:
- N04-R3 accepted status-vector authority at `8e0266703bbf3b060abcd6fbe53c7ef6c49062c5`;
- N04-R4A return at `238800fe20f257194530916514289492601eeff1`;
- EE-R2C blocker at `e87b6c2339079f65c9bed91b77a7959d7843f750`;
- HQ R2 fan-in under `PREV3_EMPIRICAL_ENGINE_COMMON_CONTRACT_R1/10_EE_R2_RETURN_FANIN_AND_RESEARCH_MACHINE_RECONCILIATION.md`.

Authority: deterministic predecessor repair/reseal only.

Required result:
1. reproduce the accepted 18,276-row canonical ledger and N04-R3 status vector;
2. apply exactly `status_code == 3` as the selector rule;
3. publish one lossless exact 18,012-ID selector carrier plus mask and one-based ordinal stream;
4. freeze exact raw/encoded hashes and counts;
5. provide an independent replay verifier and second-run identity proof;
6. explicitly supersede only the inconsistent N04-R4A selector-carrier/hash fields while preserving the accepted semantic conclusion that the selected rows lack an exact response-semantics binding at that prior grain.

Do not infer or repair any response semantics. Do not alter the 18,012 membership rule. Do not touch routing, T03, Field Forge, V3, MAIN, or semantic PRE-MAIN.

PASS wakes EE-R2C successor partitioning on the resealed selector. Return the smallest exact blocker otherwise.
