# R95 R06R3 pre-code contract — four public-boundary repairs

Status: frozen before the R3 code commit. Startup
`08fa9a2560ff5a37313434a3edb3d61e702926eb`; same R95 branch/author session.
Prior R1/R2 evidence remains immutable in history. Only the two authorized R06
code paths and this R3 return are written.

## 1. Actual P41/E04 invocation, not caller receipt

`R05ActualExecution` is host-retained actual-execution input:
`p41_runtime`, actual R05 `empirical` source objects, actual learned-provider
`step`, the exact `learned_consumer`, `structural_revision`, and coordinator
original ref. `select_r05_world_view` itself:

1. requires the exact learned original and actual-execution inputs;
2. imports the pinned P41 packet from `p41_runtime`;
3. constructs `SelectedWorldCatalog` over the R05 source, the R05 provider, the
   structural service, and the actual `P41Service`;
4. invokes actual P41 N10W progressive and unchanged E04 `consume` for T0/T1;
5. validates the actual returned receipts and R05 bindings.

`R05WorldConsumerRequest.consumer` is retained only as a rejected legacy input:
a non-None caller callback returns `CALLER_CALLBACK_NOT_ACCEPTED` and is never
called. Optional `claimed_receipts` are compared by content hash to the actual
receipts; any mismatch returns `R05_CLAIMED_RECEIPT_MISMATCH`. A canned mapping
alone therefore cannot mint accepted actual execution. No signing key, new R09
service or subject-selected verifier is introduced.

## 2. Actual temporal consumer-value dependence

T0/T1 are declared synthetic P41 snapshots (HISTORICAL/2026-06-01/2026-04-15
and AS_OF/2027-09-01/2027-09-01). A modeled structural revision changes
`training_access` 1->0 and `exit_cost` 2->8, changing actual E04 routes
`ELIGIBLE/WITHIN_MODELED_BUDGET` ->
`BLOCKED_BY_MODELED_RULE/RESOURCE_CONSTRAINED`. `temporal_changed=True` only
when the normalized actual consumer payload differs:

- E04 structural routes;
- N10E target/conditioners/state/denominator/cells;
- N10W positioned consumptions/chain state.

Clock labels, receipt hashes and incidental provenance are excluded from the
comparison. Distinct clocks plus identical actual payload return
`R05_TEMPORAL_PAIR_NOT_CONSUMED`; identical clocks return a clock refusal.
This is synthetic modeled-rule software evidence, not original F7 issuance.

## 3. Cross-unit linkage

Different units return `CROSS_UNIT_LINKED_QUERY_UNAVAILABLE` in every public
wrapper. A transport ref/authorized boolean is not a linked indexed query. No
pooling or invented linkage is accepted. Same-unit two-field positive remains.

## 4. Context promotion

A CONTEXT field requires an exact `StructuralEmpiricalAdmission` instance with
typed state `ADMITTED_FOR_EXACT_STRUCTURAL_USE`, target use
`STRUCTURAL_MEDIATION_INPUT`, matching source universe and structural semantic
field refs. An arbitrary FF ref or absent admission refuses; a non-null label is
not authority. The direct STRUCTURAL synthetic positive remains.

## Regression contract

Actual R05 learned/coordinator -> same P41 N9/N10W/E04 view, two fields, cold
fresh-process replay, current/as-of, revocation, learned/source/evidence/fact/
receipt severance and restore remain. R1 J42/N10E genuine positives are
preserved; R1 cross-unit transport-label positives are replaced by typed
UNAVAILABLE. No original source/science/F5/F6/F7/F8/CI/prod/N11/N12/Sorok/
J52/W52 and no self-adoption.
