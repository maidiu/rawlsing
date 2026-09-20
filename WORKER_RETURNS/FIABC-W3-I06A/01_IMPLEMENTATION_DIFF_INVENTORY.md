# FIABC-W3-I06A — Implementation Diff Inventory

Base SHA: 56697a27e94eb9603dfa412a15ab8f1feb819b0c

Production implementation tip: dc5b8a249b197bacf5c94d9f2c14043ebee67e53

## Production

### rawlsing_next/ee_p2x_candidate_process_envelope.py

New process-boundary implementation.

Introduced interfaces and contracts:

- PROCESS_ENVELOPE_SCHEMA = RAWLSING_FIABC_P2X_CANDIDATE_PROCESS_ENVELOPE@1.0.0
- FREEZE_RECEIPT_SCHEMA = RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@1.0.0
- PROTOCOL_SCHEMA = RAWLSING_FIABC_P2X_CELL_PROCESS_PROTOCOL@1.0.0
- ProcessIsolationController
- load_frozen_upstream_receipt
- IsolatedBackendResult
- fail-closed errors:
  - FrozenUpstreamError
  - RootIsolationError
  - ColdStateViolation
  - ForeignCandidateStateError
  - PreStartContaminationError
  - CrossCandidateReuseError
  - WarmStatePolicyError
  - CellProcessProtocolError

Execution behavior:

1. Validate candidate-neutral freeze receipt and exact source SHA.
2. Validate exact non-symlink candidate roots.
3. Enforce cold or explicitly authorized same-cell resume state.
4. Assert actual inner backend / candidate owner modules are absent in parent before boundary.
5. Take candidate-local parent start monotonic timestamp.
6. Create the cell owner marker.
7. Spawn fresh Python child with exact cell attribution environment.
8. Child verifies attribution before importing actual candidate backend.
9. Child requires exposed _SESSIONS to be empty at start.
10. Driver stages for the same cell execute through that child only.
11. Same-cell process retention requires an explicit lifecycle authorization token.
12. Any cross-cell command is rejected.
13. Cell transition/terminal/failure stops and waits for the child.
14. Stop validates exposed session keys remain cell-local and emits raw process-local resource observations.

No metric total is computed in this module.

### rawlsing_next/ee_p2x_process_isolated_backend.py

New driver-facing adapter preserving the existing backend contract:

RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0

It is safe for the long-lived driver to import because it does not import the real candidate backend. It lazily creates only a neutral ProcessIsolationController.

Configuration surfaces:

- RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT — required path to already-frozen candidate-neutral receipt.
- RAWLSING_EE_P2X_INNER_BACKEND — optional inner backend override; default is rawlsing_next.ee_p2x_darwin_stage_backend.
- RAWLSING_EE_P2X_EXPLICIT_RESUME_CELLS — comma-separated exact SOURCE/CANDIDATE cells whose already-existing state is deliberately resumed.
- RAWLSING_EE_P2X_WARM_STATE_TRANSITIONS — comma-separated exact FROM_STAGE_ID>TO_STAGE_ID tokens authorizing same-process warm retention.

The adapter converts I06A's internal result object back into the driver's already-existing mapping contract. It therefore does not require a new semantic driver API.

## Hostile-test support

### rawlsing_next/tests/fiabc_i06a_process_probe_backend.py

Test-only backend exposing controlled session, heap/RSS, scratch-state, and descendant-process behaviors. It produces no performance claims and no synthetic P2X result.

### rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py

Nine hostile tests:

1. Candidate A session/process/RSS history cannot enter candidate B.
2. An active A process cannot service B.
3. Same-cell process retention fails without explicit lifecycle authorization.
4. Scratch/durable state remains in the owning cell; a foreign owner marker fails.
5. A cold run fails when candidate-owned warm state already exists.
6. Same-candidate retained state is usable only through explicit resume.
7. Candidate-specific backend initialization in the parent before lawful start is detected.
8. Candidate-neutral frozen material is reused by A and B without becoming candidate-owned state.
9. A descendant child inherits exactly one cell identity and freeze identity.

## Existing files intentionally untouched

No semantic authority files, HQ handoffs, decision ledgers, accepted source documents, parity-oracle truth, candidate identity definitions, final comparison terminal definitions, or current P2X measured receipts were changed.

The audited P2X driver/backend were not copied into this branch. Their already-existing backend plugin contract is the fan-in seam; this avoids duplicating or silently superseding sibling production ownership.
