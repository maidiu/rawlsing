# V01 COMMISSION — T02 PREDECESSOR-LINEAGE FAIL-CLOSED REPAIR R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w20-v01-t02-predecessor-lineage-repair-r1`

Commission base / HQ authority: `43aafdae67d7b56da13e3e0d0695e36731fe18e7`

Exact grain:

`SDTF_R4_GENERIC_BATCH_ADAPTER_PREDECESSOR_LINEAGE_FAIL_CLOSED_REPAIR_R1_ONLY`

Library: `NO`

## Mission

Repair only the exact T02 defect established by U01:

`PREDECESSOR_CHAIN_INVALID_NOT_FAIL_CLOSED_FOR_UNPRESENTED_PRIOR_SNAPSHOT`

U01 governed blocker:

`4dc4d36f4f64d744a20259ec73e46f46c12c191b`

T02 producer candidate:

`161b207f1efb6f8291c1dae3258bb710438f6b54`

Frozen S03 contract:

`SDTF_R4_GENERIC_BATCH_ENVELOPE_CONTRACT|SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1@1.0.0|abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d`

## Required repair

For generation `N > 0`, the adapter must fail closed unless `predecessor_row_ref` is positively proved to be the **exact prior snapshot ref**, including its exact content hash.

Lawful proof paths at this grain are limited to:

1. a co-present exact prior row whose full exact ref equals `predecessor_row_ref`; or
2. another exact immutable lineage-resolution input that is explicitly bound by the frozen contract/HQ and can prove the full prior-row exact ref without inference.

If no lawful proof surface exists beyond co-presence, fail closed when the prior snapshot is absent. Do not invent a lineage registry merely for convenience.

The U01 counterexample must fail after repair:

- successor generation `1`;
- syntactically correct predecessor kind/object id;
- forged predecessor content hash;
- prior snapshot absent from the batch.

The repaired adapter must emit the existing governed lineage failure state rather than permitting projection.

## Required tests

Add deterministic tests covering at minimum:

- forged predecessor hash with prior snapshot absent -> fail closed;
- exact predecessor co-present -> lawful lineage acceptance;
- wrong predecessor hash with co-present prior -> fail closed;
- generation 0 with non-null predecessor -> fail closed;
- generation >0 with null predecessor -> fail closed;
- unrelated valid rows remain unaffected by one row's lineage failure;
- no change to candidate/batch semantic identity beyond what the exact repair law requires;
- no weakening of duplicate/conflict quarantine, N/A, currentness, authority or R4 projection boundaries.

Use the U01 reproduction artifact as hostile evidence where useful:

`02_REPRO_U01_T02_PREDECESSOR_LINEAGE_BLOCKER.py`

## Hard scope ceiling

This commission does NOT authorize:

- redesign of S03 or R4;
- new generic architecture;
- source/question semantic adjudication;
- authority issuance;
- rule current-selection;
- concrete mechanism rule minting;
- actor/entity fact materialization;
- topology construction;
- V3/person state;
- OBL063 semantics.

Do not repair unrelated defects unless the exact predecessor-lineage repair cannot be made without proving a smaller inseparable blocker. If another defect is merely noticed, record it diagnostically without expanding implementation scope.

## PASS ceiling

PASS may establish only:

`T02_PREDECESSOR_LINEAGE_DEFECT_REPAIRED__FRESH_INDEPENDENT_QUALIFICATION_REQUIRED`

A repair PASS is not independent qualification and does not authorize generic R4 batch production use.

## Blocker law

Return the smallest exact implementation/contract blocker if the predecessor exact-ref law cannot be repaired within the existing S03/T02 contract without redesign.

## Write scope

Modify only the T02 adapter/tests and bounded V01 return/replay artifacts necessary for this repair. Do not mutate MAIN or PRE-MAIN.

## Successor gate

PASS wakes one fresh independent hostile qualification of the repaired T02 adapter.

Because actual-repository execution is currently blocked at the last verified runner state, HQ may bank the repaired candidate and defer qualification execution until the neutral-smoke execution gate recovers. Do not claim qualification by producer-local tests or inspection.