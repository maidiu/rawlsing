# API and Ownership Receipt

## New M01 API

Module: `rawlsing_next.pre553_route_b_production`

### Contracts

- `ROUTE_B_PRODUCTION_CONTRACT_ID = PYAT_M01_ROUTE_B_PRODUCTION_COMPOSITOR@1.0.0`
- `ROUTE_B_EXECUTION_RECEIPT_SCHEMA = PYAT_M01_ROUTE_B_EXECUTION_REPLAY_RECEIPT@1.0.0`

### Public types/functions

- `I03ExecutionRequest(query_ref, predicate_ref)`
  - exact-only request pair;
  - deterministic request identity;
  - no operation aliasing or lookup.
- `RouteBEmpiricalObjectGraph`
  - exact AuthoritySnapshot preimages;
  - executed EmpiricalPredicate preimages;
  - executed EmpiricalQuerySpec preimages;
  - EmpiricalFact preimages;
  - DiscoveryAuthority preimages;
  - DiscoveryResultReceipt preimages.
- `RouteBProductionResult`
  - exact source identity;
  - governed projection binding receipt;
  - repository/executor binding;
  - sealed C11 logical release;
  - I03 results;
  - I05 result;
  - exact object graph;
  - learned empirical execution receipt;
  - deterministic replay receipt.
- `execute_route_b_production(...)`
  - exact selected-B composition entry point.
- `verify_route_b_replay_receipt(receipt)`
  - deterministic envelope/preimage/tamper verifier.

## Existing owners retained unchanged

| Concern | Existing owner used by M01 | M01 action |
|---|---|---|
| physical/native -> C11 semantic projection | `pre553_source_backed_c11_facade.py` / caller-owned `GovernedC11Projection` | compose only |
| source-backed repository build | `build_source_backed_c11_repository` | bind/invoke only |
| governed projection identity | `governed_projection_binding_receipt` | consume only |
| exact runtime catalog | `RuntimeObjectCatalog` | consume only |
| repository/executor binding | `bind_repository_builder` | consume only |
| I03 execution | `CarrierNeutralResearchExecutor.execute_i03` -> existing I03 engine | invoke only |
| I05 execution | `CarrierNeutralResearchExecutor.execute_i05` -> exact bounded discovery | invoke only |
| learned execution envelope | `learned_empirical_execution_receipt` | consume only |
| public-object authority closure | `AuthorityRegistry` + `validate_object_authority_closure` | revalidate closure only |
| public-object materialization | `materialize_public_object` | replay/tamper verification only |

No existing semantic owner file was edited.

## Exact fail-closed additions at the compositor boundary

M01 additionally requires:

- source SHA == projection expected source SHA;
- all projection-required authorities are present in the runtime catalog;
- the exact projection authority itself is present;
- at least one exact I03 request;
- no duplicate exact I03 request;
- exact catalog resolution of query, predicate, and discovery authority;
- query's exact condition predicate == supplied predicate;
- sealed release source identity == exact physical source identity;
- replay receipt fields and effect flags have exact shape;
- dependency root and outer receipt identity rehash exactly;
- every packaged public-object preimage rematerializes to its exact canonical family/ref;
- graph refs close exactly over packaged preimages.

These checks add no semantic meaning; they prevent composition from silently weakening existing owner law.

## Effect law

Every M01 replay receipt fixes the following to `false`:

- learned empirical adjudication effect;
- learned-product publication effect;
- learned-product current-selection effect;
- structural truth effect;
- causal truth effect;
- actor/V3 effect.
