# PYAT HQ116-C — Exact Missing Route-B Composition Seams

## Holding

There is **no missing semantic architecture between current Route B and the pre-Field-Forge learned world**.

The live code already contains the exact semantic owners needed for the baseline path:

```text
PhysicalSourceIncidence / ExactPhysicalCellStream
+ exact GovernedC11Projection
        |
        v
pre553_source_backed_c11_facade.build_source_backed_c11_repository
        |
        v
pre553_carrier_execution.bind_repository_builder
        |
        v
CarrierNeutralResearchExecutor.execute_i03 / execute_i05
        |
        v
pre553_carrier_execution.learned_empirical_execution_receipt
```

The missing production surface is a **thin composition seam over those owners**.

## S1 — the one implementation-blocking seam

### Missing capability

There is no current, generic, post-HQD109 production entrypoint which:

1. accepts one exact already-decoded/certified physical source incidence or exact physical cell stream;
2. accepts one explicit governed source-specific projection;
3. accepts one exact runtime object catalog and, where required, its runtime authority set;
4. invokes the **live** Route-B facade;
5. binds the resulting exact C11 release into the common carrier-neutral executor;
6. executes the exact named I03/I05 workload;
7. returns a Field-Forge-ready exact object graph plus deterministic replay/provenance receipt;
8. performs none of the semantics above on behalf of their existing owners.

The closest existing function is:

`pre553_carrier_execution.bind_repository_builder(...)`

It already composes an accepted repository builder with an exact runtime catalog and yields a `RepositoryBuilderBinding` carrying a `CarrierNeutralResearchExecutor`. What is absent is the last small orchestration layer that standardizes **Route-B builder selection + exact execution + exact pre-Field-Forge export**.

### Smallest lawful implementation

Add one composition-only module, recommended working path:

`rawlsing_next/pre553_route_b_production.py`

It should contain no source-family lookup and no new semantic authority. Its baseline call should be equivalent to:

```python
projection_receipt = governed_projection_binding_receipt(projection)

binding = bind_repository_builder(
    repository_builder=build_source_backed_c11_repository,
    builder_kwargs={
        "source": source,
        "projection": projection,
        "cache": optional_cache,
        "batch_size": batch_size,
    },
    builder_identity={
        "route": "B__SOURCE_BACKED_VIRTUAL_C11",
        "facade_contract": PRE553_SOURCE_BACKED_C11_FACADE,
        "projection_binding": projection_receipt,
    },
    runtime_catalog=runtime_catalog,
)

with bind_runtime(runtime_authority_set, ...):   # only where the supplied runtime requires it
    result = binding.executor.execute_i05(
        discovery_authority_ref=discovery_authority_ref
    )

execution_receipt = learned_empirical_execution_receipt(result)
```

The new module owns only orchestration and export. It does not own the projection, source semantics, query, discovery, validation, lifecycle, or Field Forge decision.

## Required pre-Field-Forge return surface

The compositor should return the live objects **and** a deterministic non-semantic orchestration manifest sufficient for exact dereference/replay.

Minimum fields:

- exact source identity carried by the decoded incidence/stream;
- governed projection binding receipt;
- exact logical C11 release ref;
- exact C11 replay ref / release replay closure;
- repository-builder binding receipt;
- runtime-catalog receipt;
- exact discovery authority ref;
- exact candidate grammar/frontier/replay refs;
- all executed query and predicate exact refs;
- all `EmpiricalFact` exact refs and object preimages;
- all `DiscoveryResultReceipt` exact refs and object preimages;
- all AuthoritySnapshot refs/preimages required by those objects;
- learned empirical execution receipt;
- typed terminal/negative states without scalar repair;
- exact dependency root over the exported graph;
- explicit `structural_truth_effect=false`, `causal_truth_effect=false`, `actor_v3_effect=false`;
- deterministic reconstruction/replay instructions or lawful dereference handles.

This manifest is a **composition receipt**, not a new learned semantic ontology and not a universal master carrier.

Field Forge R2 explicitly permits direct exact producer information or lawful dereference. Therefore the first campaign must not invent a mandatory extra learned-release wrapper merely to make the pipeline look stage-shaped.

## S2 — source-specific binding is a boundary, not a generic missing seam

The generic facade correctly refuses to infer source meaning.

A source-specific caller must provide:

- exact decoder/source-format contract;
- exact `GovernedC11Projection`;
- exact source-semantic / mapping / routing / weight authorities as applicable;
- exact runtime catalog;
- exact runtime realization authority if the workload needs one.

Current proof surfaces already exist for LiTS and WVS7. Other sources/waves must earn their own binders from existing documentary/source authority. The generic compositor must never select a projection by filename, labels, variable proximity, family resemblance, or observed values.

Therefore:

`MISSING_SOURCE_BINDER != MISSING_GENERIC_ROUTE_B_ARCHITECTURE`.

## S3 — learned-product currentness is an authority gap, not permission for the compositor to invent lifecycle law

Current `pre553_authority_maintenance.py` owns AuthoritySnapshot maintenance/current selection, not generic learned-product current selection.

The B5 OBL034 learned-product lifecycle contract is explicit historical **candidate** material with no project-current effect.

Consequently the first Route-B compositor may:

- expose exact determinants and replay closure;
- expose explicit publication/current-selection receipt refs **if a competent caller supplies them**;
- preserve a no-current-selection / no-currentness-claim condition operationally.

It may **not**:

- declare its newest output current;
- choose a current product by chronology or repository presence;
- import B5 candidate rules as current law;
- create learned-product supersession/withdrawal/GC authority.

An explicitly pinned Route-B product can still be handed to Field Forge by exact ref/object graph. R2.1 already holds that a universal extra learned-release/current-selection wrapper is not a prerequisite to exact Field Forge consumption.

## What is not missing

Do not create replacements for:

- physical decoding;
- source-backed C11 projection;
- C11 release validation;
- runtime catalog identity;
- I03;
- I05;
- empirical fact/discovery receipt ontology;
- replay integrity;
- Field Forge structural admission;
- conditional support;
- V554/M1 relation ingress.

The first implementation campaign should fail if it starts re-owning any of those.

## Exact conclusion

`SMALLEST_MISSING_SEAM = LIVE_ROUTE_B_REPOSITORY_BINDING -> EXACT_I03/I05_EXECUTION -> PREFIELD_FORGE_EXACT_OBJECT_GRAPH_EXPORT`

This is a composition problem, not an invitation to invent a new stage.
