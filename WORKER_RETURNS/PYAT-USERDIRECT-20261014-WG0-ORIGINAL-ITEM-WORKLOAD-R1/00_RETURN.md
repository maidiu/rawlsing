# PYAT WG0 -- Original Item-to-Workload Production Return

**Commission:** PYAT-USERDIRECT-20261014-WG0-ORIGINAL-ITEM-WORKLOAD-R1
**Branch:** `agent/userdirect-pyat-20261014-wg0-original-item-workload-r1`
**Sealed startup:** `01c6f77dfa755fdc932d2ab6b92abf2382ae8926`

## Reverse-trace result

Traced `i03_requests`, `DiscoveryAuthority`, `predicate_catalog`, `query_template_catalog`, `BatchManifest` through:
- `pre553_route_b_production.py` -- consumes caller-supplied `i03_requests`
- `pre553_discovery_exact.py` -- compiles caller-supplied `predicate_catalog`/`query_template_catalog`
- `pre553_batch_runner.py` -- executes caller-supplied `BatchManifest.units`

**Finding:** No existing general workload builder or item enumerator found at these interfaces. The engine owners consume prepared inputs but do not construct them. Per the critical gate: "If truly missing at this exact interface, author minimum versioned sourcefree producer only."

## What was built

`wg0_workload_builder.py` -- source-free generic builder that:
1. Accepts heterogeneous native item instances (ordinal, household/multiple-response, routed)
2. Mechanically enumerates eligible operations (marginal, conditional) per operation class
3. Assigns typed dispositions (PRODUCED, HELD, NOT_APPLICABLE, INADMISSIBLE, UNDECIDED)
4. Provides no-drop oracle, deterministic sharding, resume, frontier freeze

## Two heterogeneous items tested

| Item | Kind | Unit | Options | Missing |
|---|---|---|---|---|
| ITEM-ORDINAL-001 | ORDINAL | respondent | 0,1,2,3,9 | 9,997,998 |
| ITEM-HOUSEHOLD-MR-002 | HOUSEHOLD | household | food,rent,health,education,none | 997,998 |

## Test results: 11/11 PASS

- Two heterogeneous items, original options preserved
- Operation enumeration (marginal + conditional, same-unit only)
- No-drop oracle: every item+operation has exact disposition
- Frontier freeze blocks post-hoc additions
- Deterministic sharding and resume
- Duplicate item rejection
- Route vs skip distinction (NOT_APPLICABLE)
- Zero/null/minority preservation
- Source custody HOLD declared for invented fixtures

## Producer-engine-consumer route

`WorkloadBuilder` -> `pre553_route_b_production.py::execute_route_b_production` (consumes `i03_requests`) -> `pre553_batch_runner.py::BatchExecutionRunner` (consumes `BatchManifest`)

The builder produces the inputs these engines consume. The connection is at the `i03_requests`/`BatchManifest` interface.

## Source/estimate ceilings

- Invented fixtures with `FIXTURE-SRC-*` identity and source-custody HOLD
- No raw survey execution, no canonical changes, no V3
- Not all35, not 1,890 cells, not 101 task classes
- Independent review required before owner adoption

## Remaining obstruction

Real source metadata access requires exact source/E/model issuer authority. The builder is source-free; promotion to real sources requires separate grant.

## Terminal

`PYAT_WG0_ORIGINAL_ITEM_WORKLOAD_BUILDER_IMPLEMENTED__SOURCEFREE_TESTS_PASS__AWAITING_INDEPENDENT_REVIEW__NO_ALL35_CLAIM`
