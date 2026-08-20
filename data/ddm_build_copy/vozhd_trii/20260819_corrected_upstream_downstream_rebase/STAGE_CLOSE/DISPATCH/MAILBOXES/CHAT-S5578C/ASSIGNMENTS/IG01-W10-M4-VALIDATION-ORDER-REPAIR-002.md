# IG01-W10-M4-VALIDATION-ORDER-REPAIR-002

Worker #10 — `CHAT-S5578C`
Agent: `IG_M4_VALIDATION_ORDER_REPAIR`
Class: SUB-VOZHD
Authority: bounded implementation repair under frozen M4 semantics only.

Repository: `maidiu/rawlsing`
Exact base: `b66e282f4185ece6682723bc5e53c1a23534d5f0`
Mission branch: `agent/vozhd-trii-ig-m4-validation-order-repair`

Observed exact local full-suite result: 259 passed, 1 failed. The malformed partial V556 package is rejected, but generic dependency-edge validation fires before the V556-specific participant-closure validator, so the frozen test's expected `partial n-ary` failure path is unreachable.

Allowed write ONLY:
- `rawlsing_next/m4_v557_v558_publication_repository.py`

Forbidden:
- any test edit;
- any other runtime edit;
- semantic redesign;
- legacy runtime;
- SPDM;
- deployment/cutover/retirement.

Required repair:
Inside `build_v558_repository_bundle`, for each positive supported V556 entry, execute the already-existing `_validate_v556_participant_edges(entry, by_object, edge_by_source)` before the generic `required_dependency_refs + negative_dependency_refs` role-preserving-edge loop. Remove/avoid the later duplicate invocation so the V556-specific participant-shape check occurs once. Both the V556-specific check and generic dependency closure remain mandatory. Do not alter acceptance/rejection conditions or exception classes/messages.

If local execution is available, run at minimum the failing M4 test and the complete nine-file final suite. If not, commit only the one-file repair and return exact head/diff.

Success token: `IG_M4_VALIDATION_ORDER_REPAIR_COMPLETE`
Failure token: `BLOCKED_M4_REPAIR_SEMANTIC_DRIFT_REQUIRED`
