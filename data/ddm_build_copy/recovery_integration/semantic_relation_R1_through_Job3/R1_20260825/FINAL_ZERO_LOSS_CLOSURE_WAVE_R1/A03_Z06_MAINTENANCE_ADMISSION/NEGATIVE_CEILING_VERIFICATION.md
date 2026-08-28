# A03 Negative Ceiling Verification

Status: `PASS__NEGATIVE_CEILINGS_HOLD_AT_RUNTIME`

The A03 court admits the Z06 maintenance lifecycle only. It does not widen semantic jurisdiction.

Executed or source-identity verified ceilings:

- `CANDIDATE != AUTHORITY` — source onboarding test verifies no snapshot exists at candidate creation.
- `EVIDENCE != ADJUDICATION` — evidence receipts do not mint authority.
- `APPROVED_ADJUDICATION != CURRENT_SELECTION` — seal and promotion remain distinct operations.
- `SEAL != PROMOTION` — current selection changes only through exact release.
- `SOURCE_ONBOARDING != SEMANTIC_AUTHORITY` — onboarding originates a candidate and still requires adjudication/seal.
- `CONFLICT_DETECTION != MERGE_OR_EQUIVALENCE_AUTHORITY` — same id/version conflict fails closed.
- `ROLLBACK != HISTORY_MUTATION` — runtime rollback preserves both historical immutable revisions.
- `CURRENT_SELECTION != LATEST_VERSION_SEARCH` — no latest/default API and exact selection receipt is required.
- `DEPENDENCY_GRAPH_REACHABILITY != DOMAIN_RECOMPUTATION_SEMANTICS` — affected refs require an explicit recompiler.
- `CHECKPOINT_PRESENT != REPLAY_PROVED` — deterministic from-checkpoint replay identity is executed.

Additional required A03 negatives:
- latest/default/fuzzy selector tokens rejected;
- same id/version conflicting content rejected;
- rejected candidate nonpromotion executed;
- deferred candidate nonpromotion executed;
- partial-evidence positive adjudication rejected;
- correction without required scope/genealogy rejected;
- missing recompiler for affected dependents rejected;
- hostile recompiler failure is atomic with respect to current selection/event chain;
- unaffected dependents remain stable.

C5R2 prototype ref `b4dae70ee524c7a3297f7b48bdfd0d0c927eac21` is evidence-only historical context and is absent from the admitted production module as an owner/implementation identity.

No architecture selection, V3 work, or sibling-A-lane inference is authorized by this receipt.
