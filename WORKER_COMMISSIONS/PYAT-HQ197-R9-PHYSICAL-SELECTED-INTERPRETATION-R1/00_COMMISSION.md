# PYAT HQ197 — physical-selected operation interpretation — R1

Repository: maidiu/rawlsing

Role: documentary forensics worker — Space Bunny

Branch:
agent/rabochii-pyat-hq197-r2

Checkout mode: SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ197-R9-PHYSICAL-SELECTED-INTERPRETATION-R1/
- /WORKER_RETURNS/PYAT-HQ197-R9-PHYSICAL-SELECTED-INTERPRETATION-R1/
- /PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ197_R9_CANDIDATE_ADJUDICATION_R1.md

Use exact Git-object reads for historical files. Do not clone or create a full checkout.

## Question

The frozen operation classes say:

SRC02/SRC06:
BOUNDED_FRESH_PHYSICAL_SELECTED_VARIABLE_READ

SRC14:
BOUNDED_FRESH_PHYSICAL_READ_EXACT_VARIABLE

and all three specify:
selected_reads = 1
full_reads = 0.

Current technical evidence shows pyreadstat 1.3.6 usecols returns only the requested columns but underlying read calls and byte totals are unchanged from an unfiltered read.

Determine what the frozen words mean.

Possibility A:
PHYSICAL identifies the physical-source/witness layer, while SELECTED_VARIABLE_READ identifies the reader invocation/output scope. Under that meaning, an API-level selected invocation can be truthful even when the format parser scans bytes needed to parse the file.

Possibility B:
the law requires byte-level or column-level physical suppression of unselected data, so a projection-only route is insufficient.

Do not choose by convenience.

## Exact record to inspect

At c2af4f61d68e9803af83f8e26f633acfe31062fa:
- WORKER_RETURNS/PYAT-C4B-WORKLOAD-ORACLE-FREEZE-R1/00_COMMISSION.md
- 00_RETURN.md
- 01_EIGHT_SOURCE_WORKLOAD_FREEZE.json
- 02_AUTHORITY_API_CONSUMER_FREEZE.json
- 07_UNSIGNED_SOURCE_WARRANT_TEMPLATE.json

At 8ff40d37de69db2d8a6053a7c2242f481677f1a4:
- WORKER_RETURNS/PYAT-C4-EXECUTABLE-FREEZE-FANIN-R1/07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.json

Also trace the accepted C3 G01/D02 materials referenced by C4B for:
Q10B, Q101, Q2061B, v372.

Find the first authoritative use of:
PHYSICAL
SELECTED_VARIABLE_READ
READ_ONLY
expected_selected_reads
expected_full_reads

For each, identify what layer/object the term modifies.

## Distinctions that must remain separate

- physical source/witness layer
- reader invocation mode
- returned frame projection
- parser byte traffic
- path-open accounting
- downstream variable use

Determine specifically what full_reads=0 means.

## Technical facts to use

Independent review:
2e43b8c1e975974add3ac2cecfbd6daa96afd98b

Implementation candidate:
d5ce4ecff6acc25d199577a7859de7e98514e9fd

Both report projection-only usecols behavior. Treat that as a fact, not as the definition of the governing term.

## Required result

If A is supported, give the exact truthful accounting rule for selected_reads=1/full_reads=0 without claiming byte suppression.

If B is supported, state the smallest runtime/reader change needed and the resulting requalification burden.

If the historical record cannot distinguish A from B, return an Astra decision requirement.

Allowed dispositions:
- PHYSICAL_SELECTED_MEANS_SOURCE_LAYER_PLUS_SELECTED_READER_MODE__USECOLS_ROUTE_COMPATIBLE
- PHYSICAL_SELECTED_REQUIRES_TRUE_COLUMN_IO_SUPPRESSION__CURRENT_ROUTE_INSUFFICIENT
- PHYSICAL_SELECTED_MEANING_AMBIGUOUS__ASTRA_DECISION_REQUIRED
- MATERIAL_AUTHORITY_CONFLICT_FOUND

Write only:
WORKER_RETURNS/PYAT-HQ197-R9-PHYSICAL-SELECTED-INTERPRETATION-R1/**

Commit, push, re-fetch, verify.

Terminal:
HQ197_R9_PHYSICAL_SELECTED_INTERPRETATION_RETURNED__HQ_ADJUDICATION_REQUIRED

Source execution and all later programme stages remain out of scope.
