# WG0 Owner and Inheritance Crosswalk

## Reverse-traced owners

| Interface | Owner module | Role | Builder present? |
|---|---|---|---|
| `i03_requests` | `pre553_route_b_production.py` | Consumer of prepared requests | NO -- caller-supplied |
| `DiscoveryAuthority` | `pre553_discovery_exact.py` | Compiles finite frontier | NO -- caller-supplied |
| `predicate_catalog` | `pre553_discovery_exact.py` | Query grammar | NO -- caller-supplied |
| `query_template_catalog` | `pre553_discovery_exact.py` | Query templates | NO -- caller-supplied |
| `BatchManifest.units` | `pre553_batch_runner.py` | Batch execution | NO -- caller-supplied |

## Inherited lineage checked

- V550/J compilers: `build_determinicity_repository_v550.py`, `build_v550j_prepared_substrate.py`
- V553 harmonization: `ddm_v553_harmonization.py`, `ddm_v553_canonical_harmonization.py`
- Wave1 producers: `wave1_gt12_i03_positive_facts.py` (specific to GT1/GT2, not general)

**Conclusion:** No general automatic workload constructor exists at the inspected interfaces. The builder fills this gap at the source-free level.

## Producer -> Engine -> Consumer route

1. `WorkloadBuilder.add_item()` / `.enumerate_operations()` -> produces item/operation candidates
2. `.disposition_all()` / `.no_drop_oracle()` -> typed dispositions
3. `.shard()` / `.resume()` -> deterministic batch units
4. `pre553_route_b_production.py::execute_route_b_production()` -> C11/I03/I05 execution
5. `pre553_batch_runner.py::BatchExecutionRunner` -> batch manifest execution
