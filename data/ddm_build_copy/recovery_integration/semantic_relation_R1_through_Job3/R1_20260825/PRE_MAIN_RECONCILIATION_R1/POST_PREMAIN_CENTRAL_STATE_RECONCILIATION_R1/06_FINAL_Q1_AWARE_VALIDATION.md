# POST-PRE-MAIN CENTRAL STATE RECONCILIATION R1 — FINAL Q1-AWARE VALIDATION

Validated reconciliation candidate:

`a3eba9b2b5ee5300c29386c188be035e2f5aa742`

## Live-line race disposition

The original reconciliation correctly halted when PR #216 advanced the cumulative live line.

Re-grounded live parent:

`d203feb48896c1e27234c380f5bdafab7c4c4a3d`.

The validated candidate has both:
- the complete reconciliation lineage; and
- the Q1 live lineage

as ancestors.

Relative to the Q1 live parent, the candidate is `ahead`, 0 behind. Its additional changed paths are restricted to PRE-MAIN cognition/state reconciliation surfaces.

## Canonical PRE-MAIN ancestry

Before ref movement:

`integration/pre-main-reconciliation-r1 = d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`.

Candidate relation to PRE-MAIN:

- status: `ahead`;
- ahead: `318`;
- behind: `0`;
- merge base: `d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`.

A non-forced fast-forward is therefore structurally lawful.

## Central-state integrity

Exact schema-width and unique-ID validation passes for:

- `PROJECT_STATE.tsv` — 39 rows / 27 columns;
- `OPEN_OBLIGATIONS.tsv` — 51 rows / 19 columns;
- `DEPENDENCY_RETURN_GRAPH.tsv` — 49 rows / 8 columns;
- `REINTEGRATION_LEDGER.tsv` — 42 rows / 20 columns;
- `NEXT_ACTIONS.tsv` — 19 rows / 13 columns;
- `KNOWN_TENSIONS.tsv` — 12 rows / 8 columns;
- `KNOWN_UNKNOWNS.tsv` — 11 rows / 8 columns.

No duplicate IDs were found.

The inherited malformed `S038` row is repaired without semantic disposition change.

## Q1 exact state

Q1 is banked as negative/repair evidence, not adoption:

`FAIL__GT34_Q1_O4_SUBJECT_REQUIREMENT_AUTHORITY_OVERLAP_DEFECT_PROVED__REPAIR_CANDIDATE_DEFINED`.

Repaired O4 requirement candidate:

`GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.1.0`

hash:

`219fe6714efbcda30b6d9ea69cec6b99f3fe86a92c43ae7122a68e404f795fca`.

OBL048 remains OPEN/RETURN_REQUIRED for an independently accepted exact subject-classification owner/proof.

## Authority ceilings preserved

Still not authorized/adopted:
- repaired O4 requirement as current authority;
- O4 comparator;
- first production PSEPF;
- positive metabolism operation;
- positive CAN-008 rule;
- positive V3 execution;
- V2 effect;
- physical architecture winner;
- arbitrary branch deletion.

`main` movement is not authorized.

## Fail-closed ref movement

Legal next actions are exact and race-safe:

1. non-forced fast-forward the de facto cumulative working ref from `d203feb4...` to the terminal reconciliation seal;
2. non-forced fast-forward `integration/pre-main-reconciliation-r1` to the same seal;
3. if either update fails because a newer live commit landed, stop and reconcile that delta;
4. verify both refs equal the terminal seal;
5. verify `main` remains `b53f8843092e776fb83ec584399641f5f2fc3de3`.

`POSTPREMAIN_CENTRAL_STATE_RECONCILIATION_FINAL_VALIDATION = PASS`

`Q1_LIVE_DELTA_RECONCILED = PASS`

`PREMAIN_NONFORCED_FAST_FORWARD = AUTHORIZED`

`MAIN_MOVEMENT = NOT_AUTHORIZED`
