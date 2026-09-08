# SUB-VOZHD B — B20I03R ACCEPTANCE + B20Q3 FULL ROUTE-C QUALIFICATION AUTHORIZATION R1

Status:
`B20I03R_DRIVER_LOCAL_REPAIR_ACCEPTED__B20Q3_FULL_ROUTE_C_QUALIFICATION_AUTHORIZED__HB04_STILL_CLOSED`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

Campaign tip before this adjudication:
`8c0ce7ef0692aa25f444842dd90828604160ab2c`

## 1. B20I03R accepted

Immutable B20I03R return:
`68608be0f85ba466e12815e8b6a68b69707e8838`

Bank merge:
`8c0ce7ef0692aa25f444842dd90828604160ab2c`

Terminal:
`B20_ROUTE_C_I03_QUALIFICATION_FIXTURE_REPAIR_COMPLETE__READY_FOR_B20Q3_FULL_QUALIFICATION`

Accepted classification:
`A — QUALIFICATION_FIXTURE_OR_DRIVER_DEFECT`

Exact pre-repair negative fact:
`urn:rawlsing:pre553:EmpiricalFact:sha256:5a3449468fa0a161524d52f3fb2cc7d013ca7b6e12cd32c9fcf8ac142a062cfd`

State:
`INTEGRITY_FAILURE`

Exact originating error:
`EmpiricalQueryExecutionError: realized exact target cell is absent from the query-declared full target domain`

Responsible origin:
`rawlsing_next._pre553_query_eval._evaluate_index_group()`, line 408.

The proved defect was test/driver representation mismatch:
- source-backed Route-C fixture preserves exact integer response values `0/1`;
- imported generic test helpers declared scalar target domains as strings `["0","1"]`;
- imported response helper converted exact predicate value with `str(value)`;
- BASELINE selected actual respondents and exposed the mismatch;
- CONDITION happened to return lawful `ZERO_SUPPORT`.

Shared I03 correctly emitted `INTEGRITY_FAILURE`.
Shared I05 correctly refused to launder it.
Route-C accelerator implementation was not implicated.

## 2. Accepted driver repair

Repair commit:
`2f087524283ce40ead3ddc24af5b11411fde748e`

Repaired qualification driver:
- Git blob `9ed1a68300453bfcd4af4877bab397ed00b0e0e6`;
- SHA-256 `497a9cb64fa4a1a57a3bf2ec6882aaf5fd996ea6408e7c7bbaf272fe534321ee`.

Frozen Route-C implementation remains:
- Git blob `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`;
- SHA-256 `a07e73c514c6216c350ac7a69cb099256cf71680a49fe0796aac6729483b417d`.

The repair changed only driver-local Route-C predicate/query construction so exact response value/domain representation matches the physical source-backed fixture.

No shared I03/I05 code changed.
No Route-C implementation code changed.
No CACC1/CACC2 law changed.

## 3. Post-repair smoke accepted

Authoritative workflow:
`34283938457`

Artifact:
`10078718395`

Environment:
- CPython 3.13.15;
- `pyarrow==25.0.1`;
- pandas 3.0.5.

Accepted smoke evidence:
- same source-backed fixture built;
- ordinary cacheless I03 returned `SUPPORTED`;
- one cacheless I05 candidate completed;
- both candidate I03 facts returned `SUPPORTED`;
- zero `INTEGRITY_FAILURE`;
- one exact `DiscoveryResultReceipt` emitted;
- accelerated I05 completed;
- cacheless/accelerated receipt identity parity exact.

Exact receipt identity:
`cdb6dd705accfaf30a58547109c208ef72bf8531c1287f74b0faf19e3743db6a`

This smoke is repair validation only. It is not Route-C qualification authority.

## 4. B20Q3 authorized grain

Authorize exactly:

`B20Q3_FULL_ROUTE_C_QUALIFICATION_ON_REPAIRED_DRIVER_AND_UNCHANGED_REPAIRED_IMPLEMENTATION`

B20Q3 is qualification-only.

Frozen inputs:
- qualification driver blob `9ed1a68300453bfcd4af4877bab397ed00b0e0e6`;
- qualification driver SHA-256 `497a9cb64fa4a1a57a3bf2ec6882aaf5fd996ea6408e7c7bbaf272fe534321ee`;
- Route-C implementation blob `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`;
- Route-C implementation SHA-256 `a07e73c514c6216c350ac7a69cb099256cf71680a49fe0796aac6729483b417d`;
- `pyarrow==25.0.1`;
- compatible pandas / CPython 3.13.

No qualification code edits are authorized.

## 5. Required full court

B20Q3 must execute the ENTIRE repaired Route-C qualification driver at least twice in genuinely independent clean outer executions.

Each authoritative outer execution must begin from:
- a clean checkout/worktree;
- the exact commissioned Q3 qualification tree;
- the exact frozen driver blob above;
- the exact frozen implementation blob above;
- fresh temp roots;
- fresh pycache;
- a distinct Python process.

Each complete execution must reach and validate all of:

### CACC1
- deterministic build;
- deterministic read;
- source-backed release reconstruction;
- exact cacheless/accelerated release identity parity;
- stale/corrupt fail-closed behavior where required by the driver.

### Ordinary I03 / CACC2
- cacheless empirical query;
- CACC2 deterministic build/read;
- required role-mask membership checks;
- accelerated empirical query;
- exact cacheless/accelerated QueryExecutionResult identity parity.

### Exact I05
- cacheless exact-bounded discovery completes;
- accelerated exact-bounded discovery completes;
- zero `INTEGRITY_FAILURE` facts;
- exact `DiscoveryResultReceipt` identity parity.

### Hostile court
Reach and prove every hostile check encoded by the full driver, including:
- stale CACC1 fail-closed;
- corrupt CACC1 fail-closed;
- stale CACC2 fail-closed;
- corrupt CACC2 fail-closed;
- unauthorized extra cache material fail-closed.

### Delete / regenerate
- CACC1 delete/regenerate proof;
- CACC2 delete/regenerate proof;
- regenerated identities exactly match the deterministic expected identities.

### Internal replay
- driver's internal required fresh-process replay section completes;
- internal fresh executions are genuinely separate processes with fresh state.

### Hard-count invariants
- exactly two accelerators: CACC1 and CACC2;
- zero real C09;
- zero WVS7;
- zero benchmark/ranking;
- zero architecture/topology selection;
- zero positive V3.

Both outer executions must independently reach the complete PASS frontier.

## 6. Freshness and execution-tree law

The qualification return must record:
- exact execution tree HEAD;
- exact driver Git blob and SHA-256;
- exact implementation Git blob and SHA-256;
- Python / pyarrow / pandas versions;
- clean pre-execution Git status;
- distinct outer temp/pycache roots;
- exact command for each outer run;
- exit code;
- output qualification receipt hash;
- stderr/stdout hashes;
- complete reached/not-reached court summary.

If a transient GitHub Actions workflow is required solely as an execution vehicle:
- it is non-authoritative;
- the authoritative test process must check out and execute the exact frozen Q3 qualification tree;
- no transient workflow file may exist in the final returned tree;
- wrapper behavior may not alter driver semantics.

## 7. PASS / blocker terminals

PASS only if BOTH complete fresh outer runs reach the full court:

`AS4I_ROUTE_C_CACC1_CACC2_PARITY_QUALIFICATION_COMPLETE__READY_FOR_COMMON_ABC_HARNESS_INTAKE`

Otherwise:

`AS4I_ROUTE_C_CACC1_CACC2_PARITY_QUALIFICATION__EXACT_BLOCKER_PROVED`

If blocked:
- preserve the exact first failing boundary;
- reproduce it independently when possible;
- do not repair on the qualification branch;
- return to SUB-VOZHD B for separate adjudication.

## 8. HB04 gate

HB04 remains CLOSED during B20Q3.

Only after B20Q3 lawfully PASSes may SUB-VOZHD B:
1. bank/adjudicate B20Q3;
2. freeze exact qualified Route-A / Route-B / Route-C intake interfaces;
3. commission the separate HB04 COMMON DETERMINISTIC A/B/C HARNESS grain.

B19Q2 Route A remains already qualified:
`AS4I_ROUTE_A_ADAPTER_QUALIFICATION_COMPLETE__READY_FOR_COMMON_ABC_HARNESS_INTAKE`

No rerun is required absent exact new evidence.

## 9. Hard stops

B20Q3 must NOT:
- modify the repaired driver;
- modify Route-C implementation;
- modify shared I03/I05;
- repair failures in place;
- execute real C09;
- execute WVS7;
- benchmark/rank A/B/C;
- implement HB04;
- launch OBL037;
- select architecture/topology;
- enter positive V3;
- mutate central/PRE-MAIN/main.

Terminal:
`SUB_VOZHD_B_B20I03R_ACCEPTED__B20Q3_FULL_ROUTE_C_QUALIFICATION_AUTHORIZED__HB04_CLOSED`
