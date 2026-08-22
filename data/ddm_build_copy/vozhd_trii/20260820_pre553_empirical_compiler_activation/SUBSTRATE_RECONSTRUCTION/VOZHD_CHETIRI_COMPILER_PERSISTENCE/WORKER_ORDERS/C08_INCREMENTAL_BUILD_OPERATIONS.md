# VC4 C08 — INCREMENTAL BUILD, UPDATE & OPERATIONS COURT

Status: `PREPARED__NOT_LAUNCHED`
Branch: `agent/vozhd-chetiri-c08-incremental-build`
Write scope: `.../VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C08/`
Runtime writes: `FORBIDDEN`
Raw source probing: `FORBIDDEN_UNLESS_REISSUED`
Launch prerequisite: `G0_PASS`; preferred after accepted C03; final reconciliation requires C04/C05.

## MISSION

Determine the smallest lawful recompilation/invalidation units under persistent-LONG, source-backed and hybrid compiler models, and identify whether any candidate imposes unacceptable operational coupling or stale-authority risk.

## REQUIRED ACCEPTED INPUTS

C01, C02, C06, C07 before launch; C03 before execution-model closure; C04/C05 before final return.

## EXACT PROCEDURE

For each change scenario, trace the dependency DAG from changed determinant to affected empirical computations, discoveries, admissions, structural products, runtime packages and caches.

Scenarios:

1. add a new survey wave/source snapshot;
2. revoke/replace source snapshot;
3. decoder implementation/config/version change;
4. source semantic authority correction;
5. canonical question binding correction;
6. topology/routing/risk-set correction;
7. weight/design/estimand correction;
8. source relation/nonduplication correction;
9. I03 semantic version change if separately authorized;
10. I05 grammar/bound change if separately authorized;
11. I04 admission authority change if separately authorized;
12. one structural prior invalidated;
13. one publication/index/rack corrupt;
14. optional cache deleted;
15. cache stale but source/authority valid;
16. source temporarily unavailable;
17. interrupted compiler run;
18. partial publication/crash before atomic seal.

For each candidate A/B/C, identify minimal invalidation scope and whether exact dependencies make narrower rebuild possible.

## REQUIRED MATRIX COLUMNS

`scenario,changed_determinant,candidate,affected_layers,minimum_rebuild_unit,authoritative_inputs_needed,cache_action,compiled_product_action,runtime_availability_during_rebuild,integrity_failure_mode,global_rebuild_required,reason,terminal_risk`

## OPERATIONAL LAWS

- Optional cache must never be required to recover semantic truth.
- Source-backed does not automatically mean re-run whole corpus.
- Persistent LONG does not automatically mean incremental build is cheap.
- Rebuild convenience cannot justify a second semantic owner.
- Missing source bytes must fail closed for operations that require regeneration; existing already-sealed downstream products may remain usable only if their validity/invalidation law says so.
- No mutable `latest` may determine causal/semantic truth.

## HUMAN-END-PRODUCT CHECK

Invalidation must preserve historical/temporal distinctions. A source/authority correction must not silently rewrite previously generated actor causal history unless the closed runtime law explicitly permits rebinding for future contexts. Distinguish compiler rebuild from retrospective generated-person mutation.

## REQUIRED OUTPUTS

- `INCREMENTAL_COMPILATION_DEPENDENCY_MODEL.md`
- `INVALIDATION_MATRIX.csv`
- `MINIMUM_REBUILD_UNIT_LEDGER.csv`
- `C08_RESULT.json`
- common return files.

## FINAL DISPOSITIONS

- `C08_PASS__INCREMENTAL_DEPENDENCY_MODEL_BOUNDED_FOR_ALL_CANDIDATES`
- `C08_PASS__NAMED_CANDIDATE_REQUIRES_LARGE_BUT_LAWFUL_REBUILD`
- `C08_BLOCK__NAMED_CANDIDATE_CAUSES_UNACCEPTABLE_GLOBAL_RECOMPILATION`
- `C08_BLOCK__STALE_AUTHORITY_OR_SEMANTIC_OWNER_RISK`
- `C08_RETURN__NAMED_EVIDENCE_REQUIRED`

STOP token: `VC4_C08_RETURNED`
