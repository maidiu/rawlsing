# B20I03R RETURN — ROUTE C QUALIFICATION I03-INTEGRITY FIXTURE REPAIR R1

Status: **PASS — DRIVER-LOCAL REPAIR SCOPE ONLY**

Terminal:
`B20_ROUTE_C_I03_QUALIFICATION_FIXTURE_REPAIR_COMPLETE__READY_FOR_B20Q3_FULL_QUALIFICATION`

Branch:
`agent/rabochii-subv-b-as4i-route-c-i03-qualification-fixture-repair-r1`

## Exact I03 negative fact exposed

The B20Q2 failure was reproduced from the exact frozen handoff tree and instrumented without editing shared I03/I05.

Exactly one I03 call returned `INTEGRITY_FAILURE`: the **BASELINE** role of candidate
`ab5ad90c81a0708ed48bfc42093ca29ed92367224f076de9d1cb23c7033d8259`.

Its exact fact is:
`urn:rawlsing:pre553:EmpiricalFact:sha256:5a3449468fa0a161524d52f3fb2cc7d013ca7b6e12cd32c9fcf8ac142a062cfd`

Fact state:
`INTEGRITY_FAILURE`

Execution detail and earliest underlying I03 exception:
`rawlsing_next._pre553_query_common.EmpiricalQueryExecutionError: realized exact target cell is absent from the query-declared full target domain`

Origin:
`rawlsing_next._pre553_query_eval._evaluate_index_group()`, line 408.

The CONDITION role was lawful and returned `ZERO_SUPPORT`; it did not raise an underlying exception.

## Defect classification

Classification:
`A — QUALIFICATION_FIXTURE_OR_DRIVER_DEFECT`

The Route-C source-backed fixture carries physical integer response values `0` / `1`. Its `ResponseValueRule` objects do not authorize canonical-value transforms, so the façade lawfully preserves those exact integers as the response semantics.

The B20 qualification driver imported generic I03 test helpers that instead:
- declared target domains as strings `["0","1"]`;
- converted response-leaf values with `str(value)`.

The baseline therefore selected real respondents, realized integer target cells, and hit the exact I03 domain-integrity guard because those integers were absent from the string-valued declared domain.

Shared I03 behaved correctly by emitting the negative fact. Shared I05 behaved correctly by refusing to launder it. The failure occurs cachelessly, so Route-C accelerator semantics are not implicated.

## Driver-only repair

Committed before smoke:

`2f087524283ce40ead3ddc24af5b11411fde748e`

Repaired driver:
- blob `9ed1a68300453bfcd4af4877bab397ed00b0e0e6`
- SHA-256 `497a9cb64fa4a1a57a3bf2ec6882aaf5fd996ea6408e7c7bbaf272fe534321ee`

The repair is limited to driver-local Route-C query construction:
- response predicate exact values retain integer `1`;
- scalar target domains are exact integers `(0, 1)`.

The physical fixture, target refs, risk-set refs, authorities, topology, CACC1/CACC2 laws, shared I03, shared I05, and Route-C implementation are unchanged.

## Post-repair smoke

Authoritative run:
`34283938457`

Artifact:
`10078718395`

The exact repaired commit was checked out under CPython 3.13.15, `pyarrow==25.0.1`, pandas 3.0.5.

PASS proof:
- same source-backed fixture built;
- ordinary cacheless I03 completed with `SUPPORTED`;
- one exact cacheless I05 candidate completed;
- one `DiscoveryResultReceipt` was emitted;
- both cacheless candidate I03 facts were `SUPPORTED`;
- zero observed I03 facts were `INTEGRITY_FAILURE`;
- accelerated I05 completed;
- accelerated and cacheless discovery receipts were exactly identical:
  `urn:rawlsing:pre553:DiscoveryResultReceipt:sha256:cdb6dd705accfaf30a58547109c208ef72bf8531c1287f74b0faf19e3743db6a`.

Frozen Route-C implementation remains blob:
`abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`

B20I03R does **not** claim full Route-C qualification. The next exact gate is B20Q3 full Route-C qualification using the repaired driver plus the unchanged repaired implementation.

HB04 remains closed until B20Q3 PASSes.
