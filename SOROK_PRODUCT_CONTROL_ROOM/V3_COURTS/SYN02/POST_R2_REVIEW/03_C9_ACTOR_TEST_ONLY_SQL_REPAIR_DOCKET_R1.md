# C9 R3 test-only repair targets from RRP0-R2

Actual S36 seven-table `CandidateStore._logical_readset()` covers full schema and each table, so **do not add actor_head/outbox to legacy S36**. Preserve old receipt/hash domain. Option A actor authority separate SQLite + C12 read-only mirror is **ACCEPT_SCOPED direction**, not owner-frozen.

**P0 exact sourcefree failures to repair in proposed actor helper:**
1. `event_attempt.idempotency_key` same key/same digest must return original receipt exactly; current helper inserts and throws raw UNIQUE constraint. Same key/different digest typed conflict; finalized event cannot rerun Rule T.
2. `HELD_MISSING_RULE` must never have `rule_t_status='COMMITTED_CHANGE'`; enforce SQL/application cross-axis invariants, with held operational attempt but no semantic version, and owner-qualified requalification.
3. Test two actors sharing old local target id, branched epoch, concurrent CAS, source digest changed, world committed actor HELD, no cross-DB atomicity, C12 mirror false-clean prohibition, C0–C7 killpoints.
4. Actual C9 actor publisher and C12 mirror writer remain **TO_BUILD**, not to be simulated as authorized native person. The test-only helper repair may be authored in a new exclusive evidence branch as engineering proof. No C9/C12 production edit unless storage owner grants exact separate write scope.
5. C12 fork original-source guard/patch must be owner-approved and independently accepted **before** any clean actor-aware fork, C9/C12 joint storage freeze or F1.1 live build.

Full historical person and user N/N+1 remain architecture drivers, but no Rule A/T or SCI05 scientific law may be fabricated to make code green.
