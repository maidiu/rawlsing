# STATUS: SUPERSEDED_BY_LIVE_HEAD_ADVANCE__DO_NOT_USE_FOR_REF_MOVEMENT

PR #216 advanced the cumulative live line to `d203feb48896c1e27234c380f5bdafab7c4c4a3d` after this validation. Its prior ref-movement authorization is withdrawn. See the later Q1 re-grounding/final validation.

# POST-PRE-MAIN CENTRAL STATE RECONCILIATION R1 — VALIDATION AND REF MOVEMENT AUTHORIZATION

Semantic reconciliation candidate:

`74e48c69f03fbd23eaaf0f19bbe946a08f3004c4`

Parent live head:

`acfac12a4ca4b9efa010fd224094ac4dc55d37a8`

## Changed-path envelope

Exact candidate relation to live parent:

- status: `ahead`;
- ahead: `1`;
- behind: `0`;
- changed paths: `15`;
- every changed path is inside the declared PRE-MAIN cognition/state reconciliation envelope;
- no production runtime/source data path changed.

## PRE-MAIN ancestry

Candidate relation to canonical PRE-MAIN ref before movement:

- status: `ahead`;
- ahead: `313`;
- behind: `0`;
- merge base: `d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`.

Therefore the candidate is eligible for a **non-forced fast-forward** of `integration/pre-main-reconciliation-r1`.

## TSV integrity court

Validated unique IDs and exact column counts for:

- `OPEN_OBLIGATIONS.tsv`;
- `DEPENDENCY_RETURN_GRAPH.tsv`;
- `REINTEGRATION_LEDGER.tsv`;
- `NEXT_ACTIONS.tsv`;
- `KNOWN_TENSIONS.tsv`;
- `KNOWN_UNKNOWNS.tsv`.

The first candidate check exposed one inherited formatting defect in `PROJECT_STATE.tsv`: legacy row `S038` had 26 fields against the 27-field schema. That row predated this reconciliation. The terminal seal repairs it by appending the missing empty `notes` field without changing its semantic disposition.

New obligations `OBL048`, `OBL049`, `OBL050`, `OBL051` are present and uniquely identified.

Ground version is `RAWLSING_GROUND_R2`.

## Authority / scope court

No semantic production authority is widened.

Explicitly still not adopted/authorized:

- O4 ADP-010↔Q69B comparator;
- production Q69B-conditioned Q86A PSEPF;
- positive metabolism operation;
- positive CAN-008 rule;
- positive V3 mutation;
- V2 effect;
- global physical architecture winner.

`main` movement remains prohibited by this repair.

## Ref movement authorization

After this terminal seal is committed as a strict descendant of the candidate:

1. fast-forward the historical cumulative working branch to the terminal seal so it does not fork from the canonicalized state;
2. fast-forward `integration/pre-main-reconciliation-r1` to the same terminal seal;
3. use `force=false`;
4. verify both refs equal the terminal seal;
5. verify `main` remains `b53f8843092e776fb83ec584399641f5f2fc3de3`.

`POSTPREMAIN_CENTRAL_STATE_RECONCILIATION_VALIDATION = PASS`

`PREMAIN_NONFORCED_FAST_FORWARD = AUTHORIZED`

`MAIN_MOVEMENT = NOT_AUTHORIZED`
