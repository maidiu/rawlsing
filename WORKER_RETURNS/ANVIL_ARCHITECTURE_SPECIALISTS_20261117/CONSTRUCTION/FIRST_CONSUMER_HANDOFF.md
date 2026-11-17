# FIRST CONSUMER HANDOFF — CONSTRUCTION

**Purpose:** minimal real first-consumer operation for the architect/query lane, using existing accepted sourcefree symbols. No new evaluator, no new canonical store, no native/source/actor claim.

## 1. Preconditions (all exact, none inferred)

- Authorized generic SAV/DTA source and an actual source-read grant owned outside this specialist. If the source is original (not fixture), `build_source_i02_handoff` requires an independently supplied resolver plus `host`, `purpose`, `consumer_use`, `semantic_use_scope`; without them it holds (`SOURCE_READ_RESOLVER_REQUIRED` / `SOURCE_READ_REQUEST_FIELDS_REQUIRED`). This specialist does not grant them.
- `SourceConfig`, S1-C `FrozenInputCensus`, `SourceInventory`, `GrammarPolicy`, `ScientificFrontier` at their exact accepted/sourcefree grade.
- An existing owner-private storage root (`authorized_private_root`); the writer never defaults to a global cache.
- `SourceReleaseManifest` exact release/universe/instrument identity and declared counts.
- For native consumer admission: an independently held manifest SHA-256 and exact `ExternalI02Roots` (logical, physical, release, source, replay, universe, schema), an exact reconstructed v1 release ref, and a live current/rights callback. The callback is a required guard, not a grant minted by the reader.

## 2. Current accepted path (what exists now)

```python
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink

sink = SourceSavedBodySink(
    certificate_path=<caller-owned new .sqlite Q2 certificate path>,
    authorized_private_root=<existing owner-private root>,
    chunk_rows=512,
)
handoff = build_source_i02_handoff(
    config=config,
    source_path=<authorized SAV/DTA path>,
    destination=<caller-owned new .sqlite Q2 certificate path>,
    census=census,
    inventory=inventory,
    policy=policy,
    frontier=frontier,
    row_native_keys=<independently derived or None>,
    universe_ref=<exact selected EmpiricalUniverse ref>,
    batch_size=512,
    chunk_size=512,
    resolver=<required for original source>,
    host=<required for original source>,
    purpose=<required for original source>,
    consumer_use=<required for original source>,
    semantic_use_scope=<required for original source>,
    body_sink=sink,
)
receipt = sink.receipt
```

`handoff.roots` is the Q2 direct-I02 certificate; `receipt` is the `EstateReceipt` for the published Parquet estate (`receipt.path`, `receipt.manifest_sha256`, `receipt.i02`, `receipt.reconstructed_v1_release_ref`, `receipt.family_counts`, `receipt.retained_bytes`). The current path builds a second I02 in `write_direct_estate`; the recommended reduction (A1/A2) removes that only after the physical verifier is strengthened and the owner accepts the Q2 certificate as the sole I02 proof. This handoff does not implement that change.

## 3. Minimal real first-consumer operation (I03)

```python
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission

admission = PreparedSavedC11Admission.open(
    root=<owner-private root>,
    exact_path=receipt.path,
    independently_held_manifest_sha256=receipt.manifest_sha256,
    independently_held_i02=receipt.i02,
    release_ref=receipt.reconstructed_v1_release_ref,
    runtime_catalog=<exact RuntimeObjectCatalog with the exact query/predicate>,
    current_authorizer=<live callback returning True only for the exact source/release/authority>,
)

with admission.prepared_i03() as prepared:
    fact = prepared.execute_i03(
        query_ref=<exact EmpiricalQuerySpec ref>,
        predicate_ref=<exact query.condition_predicate_ref>,
    )
    assert fact is not None
    receipt_prepared = prepared.receipt()
```

`PreparedSavedC11Admission.open` is inherited from `SavedC11Admission.open` and returns the prepared subclass; `prepared_i03()` creates one `DirectEstateI03Session` and one `PreparedI03Session`, so one posting index is reused across the operations in the context. `execute_i03` calls the existing `execute_empirical_query`; it does not introduce a second evaluator. The result must be labeled **sourcefree** and must not be relabeled native.

## 4. Minimal real first-consumer operation (I05)

```python
with admission.prepared_i03() as prepared:
    discovery = prepared.execute_i05(
        discovery_authority_ref=<exact DiscoveryAuthority ref>,
    )
    receipt_prepared = prepared.receipt()
```

`execute_i05` calls the existing `execute_exact_bounded_discovery` with `group_scope=None` and the exact admission release; it does not qualify grouped/pooled science by fiat. Branch/minority/recursive/negative/replay semantics remain in the existing owner.

## 5. What to verify before treating the operation as real

1. **Exact source/currentness:** source SHA/row count/census; current callback true before and after each materializing operation; revoked source/release refuses.
2. **Exact identity:** all 13 families present; event/locator counts equal; typed absences are not converted to empty; weights invalid/nonpositive not repaired to 1.0; native question/option/form/language/routing retained in body.
3. **True person/occurrence:** repeated/ranked events are separate occurrence rows; no first-value pivot; F1–F4 same-person k≥3 and directional denominators are evaluated by the existing native code, not by a pairwise product.
4. **Evidence/replay:** output facts/references/replay are the existing fact/replay construction; do not synthesize a second evidence format. The `SavedBindingReceipt` counter status is `DECLARED_ZERO__NOT_A_MEASUREMENT`; do not cite it as measured zero source opens.
5. **Negative/revocation:** revoke after preparation; the next operation must refuse at `check_current`/`_live`. Corrupt one member; cold open must refuse. Corrupt/miss a derived index (when adopted); rebuild from canonical, do not reuse stale.
6. **No native claim:** `SavedC11Admission` is a consumer admission over the S2-C estate; the physical estate is sourcefree scoped. Native original35, source/science, F1–F4 native first reader, FF02/N9/N10W/SOROK and 100k/6GiB remain held.

## 6. Minimal lawful discriminating test (not executed)

If the architect needs to choose between A0 (current two-certificate) and A1/A2 (one-certificate/one-journal), use one fixed sourcefree fixture containing:

- all 13 families;
- at least one repeated/ranked event and one ordinary event;
- one typed missing/UNKNOWN response, one routing-unknown/inapplicable, one weight absence/invalid;
- one `SourceUniverseRelation` with `DISTINCT_BY_DEFAULT` or an exact relation authority;
- one exact I03 query and one I05 discovery;
- one corruption injection for body/selector/locator and one crash injection before manifest.

Compare A/B on: Q2 roots, persisted member SHA-256, all-family body/selector parity, native I03/I05 fact/risk/replay/negative/revocation results, build wall, peak disk by artifact class, process-tree RSS, cold open, and 1/10/100 operations. No native/heavy benchmark, no original survey data; this is a bounded sourcefree witness only if the architect judges it indispensable. Analytical predictions in `COST_MODEL.json` are not measurements.

## 7. Handoff to the integrated architect

- Adopt A1+A2+A5+A10 as the minimal package only after the full physical proof against Q2 is accepted and the crash-recovery frame requirement is adjudicated.
- If A1 cannot preserve independent source comparison without the second certificate, keep A0's second certificate and take only A2+A5+A10 (one journal, durable index, atomic recovery).
- Keep the query lane's evidence-output/replay work separate: construction does not decide outputfact amplification or grouped scientific counting.
- No final architecture acceptance, no protected adoption, no native/source/actor/science promotion.
