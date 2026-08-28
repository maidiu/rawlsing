# D01 Inherited Long Memory Baseline Schema

Status: `NORMALIZED_IMPORT_ONLY__NO_CURRENT_MACHINE_ADJUDICATION`

Binding laws:
- `LONG_MEMORY_BASELINE != CURRENT_MACHINE_CERTIFICATION`
- `NORMALIZE != REINTERPRET`
- `OLD_STAGE_NAME != CONSERVATION_UNIT`
- `NO_ROW_DROPS`

## INHERITED_44_OBLIGATION_BASELINE.csv
One row per inherited `LMX-001..LMX-044` conservation unit. It preserves the exact historical obligation text, terminal prior disposition, prior semantic/function owner, prior architecture-selection consequence/gate, residual debt, old owner-crosswalk material, old campaign-crosswalk material, and exact historical commit/path/blob provenance.

Where the historical owner crosswalk deliberately maps one LMX row into more than one function family, D01 preserves all owner rows joined with ` || `; it does not choose one.

`current_machine_certification` is always `NOT_EVALUATED_BY_D01`.

## INHERITED_LMQ_QUEUE.csv
Carries all `LMQ-001..LMQ-030` rows with every original column unchanged. D01 appends provenance/normalization columns only. It does not close, delete, reprioritize, modernize, or silently omit any queue item.

## BASELINE_SOURCE_AND_HASH_LEDGER.csv
Records exact commit/path/blob identities for all normalized Long Memory surfaces used in this import and for current Authority 39/D01 command control.

## Ceiling
This is inherited baseline normalization, not a modern successor court. Current implementation/test/receipt/disposition fields belong to later Authority-39 delta lanes and final HQ join.
