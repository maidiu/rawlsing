# EE-P2R6X — P2X MISCLASSIFIED INFRASTRUCTURE STOP LEDGER/STATE RECONCILIATION PREPARATION

Repository: `maidiu/rawlsing`

## Execution surface
**BROWSER**

## Library access
**NO**

Exact branch:
`agent/rabochii-prev3-ee-p2r6x-p2x-ledger-reconciliation-prep-r1`

Exact base:
`ae8b1db9d8c3288e002950ac01123c70f3138320`

Resolve live HQ first.

Commission-time checkpoint:
`20260919T0327-0400`

Immutable handoff:
`b994ea63d2b9571415677e0d47a16bcd3e8322bf`

Controlling decision:
`HQD-2026-09-19-081`

## Mission

Prepare a deterministic **local reconciliation tool** for the current stopped P2X work root. Do not execute it in Browser.

Current stopped ledger SHA-256:
`7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671`

The following terminalizations are HQ-classified infrastructure misclassifications and must be reopenable after code repair:

- `LITS_I/A/S02_C11_REACHABILITY` — missing common R6A runtime substrate;
- `LITS_I/B/S03_PARITY_ORACLE_GATE` — same missing common runtime substrate;
- `WVS7/A/S01_CANDIDATE_PREPARATION_BUILD` — WVS binder recursion;
- `WVS7/B/S01_CANDIDATE_PREPARATION_BUILD` — WVS binder recursion;
- `COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION` — orphan RUNNING entry from S17 ordering defect.

### Preserve exactly

Do not disturb:

- all lawful DONE__PRESERVE stages;
- LiTS-A first build preservation;
- LiTS-B standalone cacheless preparation preservation;
- any lawful PASS stage before each misclassified blocker;
- LiTS-C frozen q310/q311 nonqualification and its propagation;
- WVS-C preserved portability failure and frozen-law skips;
- source identities;
- continuation map identity;
- existing historical Git evidence.

### Reconciliation algorithm

Create a local tool under `WORKER_RETURNS/EE-P2R6X/` that:

1. requires the exact pre-reconciliation ledger SHA above;
2. validates the exact blocker entry identities and exact exception classes/messages from the current governed P2X return;
3. for each affected candidate, removes only the misclassified blocker ledger entry plus mechanically generated candidate-stop propagation entries whose receipt links back to that blocker;
4. removes only local backend state/scratch artifacts whose identity is owned by the failed attempt and is unsafe to reuse;
5. preserves earlier terminal stage receipts and any repetition-forbidden external/preserved physical carrier;
6. removes the orphan RUNNING S17 entry;
7. leaves all legitimate LiTS-C and WVS-C terminal states untouched;
8. writes a reconciliation receipt with before/after ledger hashes and exact removed/preserved addresses;
9. is idempotent only in the fail-closed sense: a second invocation against an already-reconciled ledger must refuse unless explicitly run in audit-only mode;
10. never touches source carriers or empirical data.

Audit the backend's exact local state paths so the tool does not over-delete valid preserved work. Prefer deletion of only `ee_p2x_backend_state.json` and exact failed-stage scratch/partial outputs where sufficient; do not delete candidate roots wholesale if that would invalidate preserved receipts.

## Qualification

Use synthetic copies of the exact ledger/receipt shape, not carrier data, to prove:

- exact expected ledger rewinds to the correct next stage;
- unrelated ledger drift fails closed;
- valid prior PASS/PRESERVED entries survive byte-for-byte;
- LiTS-C/WVS-C survive;
- wrong exception/failure identity refuses reconciliation;
- orphan S17 RUNNING is removed;
- no measurement/source access.

Required tool:
`WORKER_RETURNS/EE-P2R6X/03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py`

PASS:
`EE_P2R6X_PASS__DETERMINISTIC_P2X_INFRASTRUCTURE_STOP_RECONCILER_READY__PRESERVES_LAWFUL_STAGE_HISTORY__READY_FOR_POST_FANIN_LOCAL_RECONCILIATION`

BLOCK:
`EE_P2R6X_BLOCK__<EXACT_FIRST_LEDGER_OR_LOCAL_STATE_RECONCILIATION_AMBIGUITY>`

Do not move P2X. Return to HQ.
