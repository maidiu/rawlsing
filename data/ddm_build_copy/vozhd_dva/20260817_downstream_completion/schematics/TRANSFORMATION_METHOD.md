# Boundary Transformation Method

For every current stage `B` with downstream consumer `C`, do not assume the immediate predecessor is the whole upstream world. Determine the stage contract by reconciling **everything lawfully available upstream** with **what the downstream consumer actually needs**.

The governing sequence is:

`UPSTREAM AVAILABILITY → DOWNSTREAM REQUIREMENT → LAWFUL INTAKE SELECTION → STAGE-SPECIFIC TRANSFORMATION → REACHABLE OUTPUT ENVELOPE → REQUIRED OUTPUT CONTRACT`

The accepted contract is the minimum semantically complete output that both:
1. B can lawfully create from available upstream authority; and
2. C actually needs in order to perform its own assigned transformation without guessing, reaching behind B, or forcing B to perform C's work.

## 1. Upstream availability envelope

Inventory the richest lawful objects, authorities, and contexts available anywhere upstream that B could potentially consume. Start from actual canonical implementation outputs and concrete dependencies, not an imagined neat serial interface.

For every available surface record:
- producer/stage;
- artifact/object/field;
- object grain and stable IDs;
- structural/temporal/scope identities;
- values, relations, directionality, conditions;
- provenance/lineage;
- epistemic class;
- uncertainty/confidence;
- absence, noncomparability, blockers, permissions, negative authority;
- whether B currently consumes it;
- whether it arrives through the immediate handoff or by direct reach-back.

Classify its possible jurisdiction as one of:
- `PRIMARY_HANDOFF`;
- `LAWFUL_DIRECT_CO_INPUT`;
- `AUTHORITY_CONTEXT`;
- `PROVENANCE_CONTEXT`;
- `VALIDATION_CONTEXT`;
- `SHOULD_BE_CARRIED_THROUGH_HANDOFF`;
- `SHOULD_NOT_BE_CONSUMED`;
- `UNRESOLVED`.

The existence of a current read path does not prove that the dependency belongs in the final architecture.

## 2. Downstream demand envelope

Before defining B's operation or output, work backward from C.

Determine:
- what operation C is actually responsible for performing;
- what information C must receive from B in order to perform it;
- what information is truly required versus merely convenient;
- what C would otherwise have to guess, reconstruct, or reach upstream to recover;
- what C must explicitly receive as unresolved, absent, noncomparable, blocked, or uncertain;
- which requested meanings actually belong to C or a later stage and therefore must not be pre-resolved by B.

This defines the **backward floor**: the minimum semantically complete input C needs from B.

## 3. Lawful intake selection for B

Now determine which parts of the upstream availability envelope B should actually consume.

For each downstream-required information class ask:
- is it already present in the immediate governed handoff?
- if not, does a lawful direct co-input exist upstream?
- is the direct co-input genuinely necessary, or does its necessity expose a handoff gap?
- is the source semantic payload, authority context, provenance context, or validation context?
- if multiple upstream surfaces appear to provide the same meaning, which one is authoritative and what are the others allowed to do?

If richer governed information exists upstream but current B consumes a lossy compatibility surface, record a seam defect rather than designing around the loss.

## 4. B-specific transformation obligation

Only after upstream availability and downstream demand are known, state exactly what new class of meaning B must create.

Use the form:

`SELECTED LAWFUL INPUT GRAINS → B-AUTHORIZED OPERATION → B-DERIVED OBJECT GRAINS`

The operation must identify what B computes, derives, compares, groups, conditions, temporalizes, or re-expresses that upstream sources did not already know.

Every proposed derived field must have:
- a lawful source basis;
- an explicit transformation rule or governed derivation class;
- retained lineage to its basis;
- an epistemic/permission state;
- a clear reason B rather than an upstream or downstream stage owns the derivation.

## 5. Reachable output envelope

Given the complete lawful intake composition and B's authorized operation, determine **everything B is actually capable of emitting without invention**.

This is the **forward ceiling**.

Separate:
- directly preserved upstream meaning;
- losslessly reformatted meaning;
- governed B-derived meaning;
- lawful aggregation with lineage;
- unresolved/negative states that must survive;
- meanings B cannot lawfully create.

The reachable output envelope may be richer than what C currently needs. Do not automatically turn every reachable field into a required contract field.

## 6. Required B output contract

Intersect the reachable output envelope with the downstream demand envelope.

The required output contract is the minimum object set that:
- lets C perform its own transformation without upstream reach-back;
- preserves all distinctions needed by named downstream capabilities;
- preserves lineage and authority for every B-derived value;
- carries unresolved/absence/noncomparability/blocker states where they matter;
- does not pre-resolve responsibilities belonging to C or later stages.

If B can lawfully produce useful information that C does not currently require but a named later capability does require, preserve it when dropping it here would force downstream reconstruction. Record that downstream consumer explicitly.

## 7. Preservation / transformation ledger

Classify each important incoming distinction as:
- `PRESERVE` — identity/meaning must remain directly or by stable reference;
- `DERIVE` — B may compute a governed new value while retaining lineage;
- `REFORMAT` — storage/representation may change losslessly;
- `AGGREGATE_WITH_LINEAGE` — compression permitted only with reversible/auditable source linkage;
- `DROP_EXPLICITLY` — information may be discarded only because no named downstream capability needs it and the loss is recorded;
- `FORBIDDEN_TO_INFER` — B may not manufacture the value;
- `UNRESOLVED` — authority is insufficient and the unknown must survive.

Silent loss is never a valid category.

## 8. Reconciliation outcomes

For every downstream requirement compare the backward floor with the forward ceiling and classify:
- `MEETS` — lawful reachable output satisfies downstream need;
- `UPSTREAM_INFORMATION_LOSS` — required meaning exists earlier but is not reaching B;
- `MISSING_AUTHORITY` — downstream desire exceeds everything lawfully available upstream;
- `MISPLACED_RESPONSIBILITY` — requested meaning belongs to another stage;
- `CONTRACT_GAP` — B can lawfully create the needed meaning but current code/schema does not;
- `REPRESENTATION_GAP` — semantics exist but are not preserved in B's downstream handoff;
- `REDUNDANT_REACH_BACK` — B reaches upstream for meaning already carried by its governed handoff;
- `HANDOFF_GAP` — B legitimately needs upstream meaning that the immediate handoff should probably carry but does not.

## 9. Worked transformations

At least two concrete examples should travel through:

`upstream availability → selected inputs → B operation → reachable outputs → downstream-required subset`

Prefer one ordinary and one adversarial/ambiguous case.

## 10. Hostile cases

Test at least:
- contradiction/competing evidence;
- absence versus observed zero;
- unknown versus low confidence;
- noncomparability;
- temporal drift/rupture uncertainty where relevant;
- duplicate/competing upstream authorities;
- direct structure-to-person/personality inference pressure.

## 11. Session termination

A session ends with only:
1. accepted upstream availability/intake map;
2. accepted downstream demand map;
3. accepted stage transformation equation;
4. accepted reachable output envelope;
5. required downstream output contract;
6. preserve/derive/drop/forbid/unresolved ledger;
7. concrete seam/reach-back defects;
8. implementable producer/consumer obligations;
9. unresolved questions requiring Vozhd adjudication;
10. adjacent seams that must be informed.

No production implementation begins merely because a breakout worker proposes a schema.
