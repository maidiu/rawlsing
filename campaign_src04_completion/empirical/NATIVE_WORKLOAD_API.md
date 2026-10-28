# SRC04 Lane C V2 — native workload builder / CLI

The V2 successor consumes the current B-repaired **175 qualified response
fields** and keeps the three residual response fields and all three coordinate
roles explicit.  It replaces the stale 163 ceiling with a scope ledger derived
from the read-only B configuration; it does not claim that 178 fields are
already source-qualified.

## Production API

```python
from campaign_src04_completion.empirical.native_workload import (
    WorkloadPolicy,
    build_native_workload,
    execute_native_workload,
    plan_from_scope,
)
```

- `build_native_workload(repository=..., release_ref=..., contract=..., policy=...)`
  constructs `EmpiricalQuerySpec`/`EmpiricalPredicate` objects through the
  existing PRE553 public owners.  It does not execute.
- `execute_native_workload(..., authority_registry=...)` executes the constructed
  operations through `rawlsing_next.pre553_empirical_query.execute_empirical_query`.
  It refuses a pending/unissued contract before query issuance.
- `plan_from_scope(scope=..., contract=..., policy=...)` produces a
  release-independent finite plan.  Conditional operation instances are not
  fabricated without a qualified release; only the exact target-pair frontier is
  recorded until observed condition values exist.

Every operation receipt records the exact query ref and fact ref, fact state,
raw numerator/denominator, aggregate cells and observed-response ledger.  It
does not record respondent rows or member lists.

## CLI

```sh
# Finite plan from the exact V2 scope + pending contract
PYTHONPATH=. python3 campaign_src04_completion/empirical/run_native_workload.py --mode plan

# Actual nonrespondent fixture execution (44 operations; no original source)
PYTHONPATH=. python3 campaign_src04_completion/empirical/run_native_workload.py --mode fixture-evidence

# Original execution is refused until full release + exact authority exist
PYTHONPATH=. python3 campaign_src04_completion/empirical/run_native_workload.py --mode execute
```

The fixture mode builds the SRC04 nonrespondent fixture through the existing
`source_configuration.factory`, constructs a fixture-only contract, builds the
same production workload objects, and executes them through the existing I03
owner.  It is not original SRC04 qualification.

## Finite frontier

The V2 policy is:

- unary observed distributions: **175** currently qualified response fields;
- same-respondent joint pairs: **15,225**;
- conditional target pairs: **30,450**, with operation instances deferred until
  exact observed condition values come from a qualified release;
- higher-order triples: **877,975 requested, not authorized by this contract**;
- coordinate analytical targets: **0**;
- `ser`: **identity only**;
- `country` and `q701`: role/units not adopted;
- routing: `ROUTING_UNKNOWN`, not used; no routing condition is constructed.

The three residual fields `q217`, `q715withoutmorocco` and
`q716withoutmorocco` remain held.  They are not silently converted to zero or
included in the 175-target contract.
