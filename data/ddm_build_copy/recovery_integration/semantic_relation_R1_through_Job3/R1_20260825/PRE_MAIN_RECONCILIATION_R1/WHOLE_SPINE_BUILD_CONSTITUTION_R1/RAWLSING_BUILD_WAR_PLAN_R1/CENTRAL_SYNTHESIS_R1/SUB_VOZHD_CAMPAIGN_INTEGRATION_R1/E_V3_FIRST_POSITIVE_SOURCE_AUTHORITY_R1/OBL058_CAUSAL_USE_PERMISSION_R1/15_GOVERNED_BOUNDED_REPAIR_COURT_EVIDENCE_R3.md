# OBL058 — CAUSAL_USE_PERMISSION — R3 GOVERNED BOUNDED REPAIR COURT EVIDENCE

## Court holding

`PASS__OBL058_R3_PRODUCER_BOUNDED_REPAIR_COURT`

This is producer-side bounded repair evidence only. It is **not** the required fresh distinct independent review of the frozen R3 candidate.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r3`
- exact working-ancestry start: `bea37d508792108e6b9cfc98de5b2fe48e60566c`
- frozen repaired semantic candidate: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- repaired authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.2.0`
- repaired receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@3.0.0`
- producer test commit: `abd4d76b60e4210a04dea03a51c45a3e8f887c34`
- governed wrapper commit: `9ccb1ac3dc795af69559e287d767ab316edfb301`
- governed evidence execution: `6b023c576a8039ca3993ef9b7af758e5fb88b2d6`
- execution-only PR: `#283`, closed unmerged
- PR synthetic merge identity: `948aa8784734f8300c30538a16dcfdd7e5c87804`

## Governed execution

- workflow: `Rabochii Governed Bounded Court`
- run: `34197171529`
- job: `101967385376`
- Python: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.10s`
- bounded-court spec validation: `PASS`
- R3 bounded repair court: `35 passed in 0.07s`
- receipt result: `PASS`
- receipt exit code: `0`
- receipt semantic candidate: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- receipt evidence execution: `6b023c576a8039ca3993ef9b7af758e5fb88b2d6`
- receipt spec SHA-256: `9a52a3a1eb064184ea3a9f65edbe34f02a3b0c38ba28652ede26fa3461ce9449`
- artifact ID: `10044342076`
- artifact ZIP SHA-256: `69f7dfbf39c14823b8808ba45277a49f690c8002e325b66091aba2263a6dddd9`

The downloaded `court_receipt.json` was inspected and reports:

- schema: `RABOCHII_BOUNDED_COURT_RECEIPT@1.0.0`
- determinism: `EXACT`
- result: `PASS`
- exit code: `0`
- governed test: `rawlsing_next/tests/test_subv_e_obl058_causal_use_permission_bounded_repair_r3_court.py`

## R3 repair properties exercised

The 35-test producer court verifies the repaired candidate preserves the R2 controls and closes the four exact source-origin defects reported by the R2 independent review:

1. no module-visible arbitrary-body source-origin wrapper remains;
2. issued receipts have no `_data`, `_marker`, `__dict__`, or addable per-object payload/provenance slots;
3. mutation of a caller-visible scope copy cannot change the source-owned ledger body;
4. plain copies and rewritten dictionaries are rejected as non-source-issued;
5. a fresh object created from the recovered concrete receipt type is rejected because exact issued-object identity is absent from the ledger;
6. ordinary construction of the recovered concrete type is likewise rejected;
7. `copy.copy()` does not transfer source origin;
8. subclass objects and subclass-defined provenance predicates are rejected because validation requires exact concrete type and exact issued identity;
9. a denial copied and rewritten into positive-looking content remains non-source-issued;
10. multiple genuine source-owned issuances are distinct identities and validate independently.

The court also reconfirms:

- exact registered positive basis -> `PERMIT` for exact synthetic scope;
- arbitrary basis -> `DENY`;
- caller permission boolean absent;
- caller basis-kind input absent;
- exact five-field source-basis binding;
- project-current actor/world/subject/time/transition namespaces rejected;
- exact current first-canary subject rejected;
- explicit `PROJECT_CURRENT` fixture label rejected;
- wrong expected scope rejected;
- no public basis registration API.

## Candidate immutability

The candidate was frozen at `c5fa3a8cece8b3444671b2528aa88947a10cc539` before producer test/wrapper/court commits. No candidate code or candidate-definition file changed after that freeze.

## PR disposition

Execution-only PR `#283` was closed unmerged after evidence capture.

`MERGED = NO`

`HQ_ADOPTION_CLAIMED = NO`

## Remaining gate

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R3_CANDIDATE = 0`

The green producer court is necessary but not sufficient for adoption consideration. Frozen candidate `c5fa3a8cece8b3444671b2528aa88947a10cc539` must receive exactly one fresh distinct independent review before SUB-VOZHD E may adjudicate it for any later HQ adoption packet.
