# D2P3 producer-owned reference → reader trace

**Status:** TEST_ONLY, sourcefree, candidate for independent review. No source rights, N5/N6, EE13, N9, OC05, V3 or adoption.

## One registry, one ref namespace

`new/d2p/single_registry.py` contains the single `ProducerRegistry`. The producer emits immutable `ExternalPublishedAggregateField` payloads with an exact content ref `D2P_TESTONLY_FIELD:<sha256 over all scientific fields>`.

The reader (`read_exact` / `read_produced_registry`) accepts only a `ProducerRegistry` and its exact `D2P_TESTONLY_FIELD` refs. There is no `TestOnlyRegistry(rows)` or row-derived second identity in the new path. The reader's `selected_refs` and `dependency_readset` are the producer refs themselves.

Measured refs:

- GSS: `D2P_TESTONLY_FIELD:2b00177b2685b4a2171bfc27ec77a17f7e59b603bf4bd1e0fc10dc8575908f40`
- NCA: `D2P_TESTONLY_FIELD:de36df435bd086fe265af2c3207e0ce4b4e14b66a2c8a148829bf027567c0587`
- Reader state: `TWO_VALUES_READ_TEST_ONLY`
- Reader dependency readset: exactly the same two refs in GSS/NCA order
- Reader snapshot: `D2P3_SNAPSHOT:e306120e8a787980a99790e52cd7964a682874fe22d20726b3964e1487020570`
- GSS numeric: `2,388,192 / 3,288,063`
- NCA numeric: `23,414,527 = 23,237,338 + 177,189`

Full trace: `new/producer_reader_trace.json`.

## Native identity and source clocks

| role | publisher | family | native unit | geography | publication |
|---|---|---|---|---|---|
| GSS | Ghana Statistical Service | GH_GSS_PHC_2021 | RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING | GHANA_RURAL | 2022-02-24 |
| NCA | National Communications Authority | GH_NCA_LICENSEE_REPORTS_2021Q4 | ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS | GHANA_NATIONAL | 2022-07-08 |

The producer checks the exact five GSS submeter keys and sum, exact NCA split, official publisher/family/native unit/geography/measure, publisher documents, observation/publication clocks, and `TEST_ONLY_NO_EXTERNAL_USE_GRANT` before emission. The reader checks the same field payload on dereference.

## Accepted direct transport

`new/d2p/direct_trace.py` invoked the existing accepted `rawlsing_next.pre553_learned_world_composition.compose_direct_producer` in a real process:

- actual module file: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-same-source-resume-consumer-20261103/rawlsing_next/pre553_learned_world_composition.py`
- determinant refs: exact `D2P_TESTONLY_FIELD` refs above, with content hashes matching the producer field digests
- receipt terminal state: `SOURCEFREE_TEST_ONLY_TWO_FIELDS_BOUND`
- reason: `DIRECT_PRODUCER_ROUTE_EXACTLY_AUTHORIZED`
- route: `DIRECT_PRODUCER`
- ceiling: `TEST_ONLY_NO_ISSUANCE`
- N5/N6: false; EE13: false; OC05: false

Trace: `new/d2p/direct_trace_stdout.json`. This transport is not a source issuer and does not create N5/N6, N9, OC05, N7/EE13 or original PDF custody.

## Negative behavior

- Mutated exported field: `FIELD_CONTENT_REF_MISMATCH` (ref is recomputed, never self-rehashed)
- Forged issuer signature: `ISSUER_FORGERY`
- `wind` renamed `hydro_turbine`: `GSS_ELECTRICITY_SUBTYPE_IDENTITY_MISMATCH`
- NCA unit changed to `PERSON_WITH_MOBILE_DATA`: `NATIVE_UNIT_OR_MEASURE_MISMATCH`
- fake publisher: `OFFICIAL_PUBLISHER_IDENTITY_MISMATCH`
- wrong source family: `SOURCE_FAMILY_IDENTITY_MISMATCH`
- registry revocation: `FIELD_REGISTRY_REVOKED`; readset remains two refs and no orphan read is emitted
- pre-publication as-of: `REFUSED_REQUIRED_FIELD_TEST_ONLY`
- 2022-03-01: `PARTIAL_TEST_ONLY_NOT_POSITIVE`
- person exposure/pooling/model use: `PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN`
