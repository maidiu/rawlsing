# Boundary Transformation Method

For every seam `A → B`, analyze the transformation using the same sequence.

## 1. Upstream authority

Inventory the richest lawful objects and distinctions actually emitted by A. Start from canonical implementation outputs, not an imagined cleaner interface.

Record:
- object grain and stable IDs;
- structural/temporal/scope identities;
- values, relations, directionality, conditions;
- provenance/lineage;
- epistemic class;
- uncertainty/confidence;
- absence, noncomparability, blockers, permissions, negative authority;
- distinctions explicitly forbidden from downstream inference.

## 2. Lawful intake into B

Determine which upstream objects B should consume and at what grain. If B currently consumes a lossy compatibility surface while richer canonical information exists upstream, record that as a seam defect rather than designing around the loss.

## 3. B-specific operation

State exactly what new class of meaning B is responsible for adding.

Use the form:

`INPUT GRAIN → AUTHORIZED OPERATION → OUTPUT GRAIN`

The operation must say what B computes, derives, groups, conditions, or re-expresses that A did not already know.

## 4. Preservation ledger

Classify each important incoming distinction as:
- `PRESERVE` — identity/meaning must remain directly or by stable reference;
- `DERIVE` — B may compute a governed new value while retaining lineage;
- `REFORMAT` — storage/representation may change losslessly;
- `AGGREGATE_WITH_LINEAGE` — compression permitted only with reversible/auditable source linkage;
- `DROP_EXPLICITLY` — information may be discarded only because no named downstream capability needs it and the loss is recorded;
- `FORBIDDEN_TO_INFER` — B may not manufacture the value;
- `UNRESOLVED` — authority is insufficient and the unknown must survive.

Silent loss is never a valid category.

## 5. Required B output

Describe the minimum semantically complete object B must emit after performing its own operation. This should be rich enough for the next transformation without incorporating responsibilities that belong downstream.

## 6. Downstream need

Work backward from C, the next stage after B:
- what does C need to perform its assigned operation?
- which B outputs are causal inputs versus audit/provenance support?
- what would C otherwise be forced to guess or reconstruct?

Do not require B to resolve actor-specific facts or semantics that belong to C or later runtime stages.

## 7. Forward/backward reconciliation

Compare:
- **forward ceiling:** what B can lawfully derive from A;
- **backward floor:** what C minimally requires from B.

Outcomes:
- `MEETS` — lawful output can satisfy downstream need;
- `UPSTREAM_INFORMATION_LOSS` — required meaning exists earlier but is not reaching B;
- `MISSING_AUTHORITY` — downstream desire exceeds what evidence can support;
- `MISPLACED_RESPONSIBILITY` — requested meaning belongs to another stage;
- `CONTRACT_GAP` — B can create the needed meaning but current code/schema does not;
- `REPRESENTATION_GAP` — semantics exist but are not preserved in the downstream handoff.

## 8. Worked transformations

At least two concrete examples should travel through the seam field-by-field. Prefer one ordinary and one adversarial/ambiguous case.

## 9. Hostile cases

Test at least:
- contradiction/competing evidence;
- absence versus observed zero;
- unknown versus low confidence;
- noncomparability;
- temporal drift/rupture uncertainty where relevant;
- direct structure-to-person/personality inference pressure.

## 10. Session termination

A session ends with only:
1. accepted/proposed transformation equation;
2. required preserve/derive/drop/forbid ledger;
3. concrete seam defects;
4. implementable producer/consumer obligations;
5. unresolved questions requiring Vozhd adjudication;
6. adjacent seams that must be informed.

No production implementation begins merely because a breakout worker proposes a schema.
