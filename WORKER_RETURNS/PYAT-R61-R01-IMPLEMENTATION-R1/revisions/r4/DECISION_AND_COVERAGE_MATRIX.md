# R61 R01 R4 decision and coverage matrix

| Requirement | Implementation | Test/evidence | Status |
|---|---|---|---|
| E1 receipt-bound parent reuse | `RecurrenceParent`, existing `RecursiveBranchHandoff`/`DiscoveryBranchReplayBinding`, actual `execute_exact_bounded_discovery_with_handoffs` | three-generation native test; persisted handoff roundtrip | PASS |
| E2 finite versioned adaptive issue | `RecurrencePolicy@r61.r4.1`, `build_recurrence_issue_plan`, frozen expected operation/rule IDs before execution | exact anti-join per generation; mutation/restore | PASS |
| E3 issued vs unissued/activation ledger | `RecurrenceIssuePlan.unissued`, `RecurrenceActivation.activation_ledger/waiting/stopped` | budget unrun test; protected exploratory ledger | PASS |
| E4 distinct root/parent comparators | separate `ROOT_RELATIVE` and `IMMEDIATE_PARENT_RELATIVE` rules and receipts | gen2 differing comparator states | PASS |
| E5 separate J/K/D and counting | policy bounds + `ANCESTOR_CONDITIONS_COUNT_TOWARD_K`; D generation check; K ancestor check | D=2 stop; K=2 third-ancestor refusal | PASS |
| E6 exploration vs finding | nonwinning exploratory parent has no winner receipt; no result promoted | exploratory parent kind, neutral aggregate/hidden minority case | PASS |
| Source-root and immediate-parent views | exact baseline predicate refs in expected operations and receipts | actual I05 receipts | PASS |
| Protected minority/counterpattern | protected slot reserved from followup cap; deterministic op-id tie order | `PROTECTED_NONWINNING_EXPLORATION`; gen3 hidden differentiation | PASS |
| Finite budget | per-generation cap + cumulative `total_issued_before` cap; explicit unissued | budget test | PASS |
| Persisted N+1 fresh process | `write/load_recursive_handoff_bundle`; fresh subprocess loads parent and executes | cold subprocess test | PASS |
| Renamed/heterogeneous mechanism | second source names and transformed profile | renamed profile test | PASS |
| Invalid parent/baseline/source/replay | explanatory parent cannot claim receipt; authority/grammar mismatch typed refusal | invalid parent test; authority mismatch | PARTIAL (wrong-source/replay negative is explicit via existing owner closure, not separately mutated) |
| Preserve R3 work | conditioned JOINT/CO_TRAVEL, typed identity, axes, anti-joins | existing R3 tests retained in 24-test suite | PASS |
| R03/R04/R05/science/N11 | not implemented/claimed | NOT_REACHED | HOLD unchanged |
