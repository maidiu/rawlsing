# Real V2K / I03 / I05 / P01 Field Forge consumer proof

Everything below is from `observations/cold_first.json` and
`observations/cold_replay.json`, produced by two genuinely separate Python
processes (`repro/pv2_cold_process.py`).

## Positive witness

```
first  : original keys=6  legacy V2 keys=3  Field Forge consumers=6  durable calls=[3,3]  held=2
replay : original keys=6  legacy V2 keys=3  Field Forge consumers=6  durable calls=[0,0]  held=2
```

`links`, `nonrunnable`, `pv2_register` (committed root, source-inventory root,
obligation multiset, held obligations) and the persisted expected-payload
digest are **byte-identical** between the two processes.  On replay every owner
report records `run.executed == []` and `recovery.recovery_safe == true`, i.e.
no owner unit is silently re-executed.

## Numerical producer-to-consumer witness

For each `PAIR` and `B` link, `consumer_material.conditional_count_profile`
over the joint respondent risk set (audited against the register's independently
declared synthetic rows):

| slot | condition | denominator | target counts |
|---|---|---|---|
| PAIR (X→Y) | `0` | 1 | `0 → 1`, `1 → 0` |
| PAIR (X→Y) | `1` | 1 | `0 → 0`, `1 → 1` |
| B (Y→X) | `0` | 1 | `0 → 1`, `1 → 0` |
| B (Y→X) | `1` | 1 | `0 → 0`, `1 → 1` |

`DISCOVERY` links carry the bounded I05 winning-query profile: condition `0`
has a supported zero denominator (both cells zero, `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`),
condition `1` has denominator 1 with `(1,1) → OBSERVED_POSITIVE` count 1.  The
zero denominator is a supported observed zero, not an invented probability.

Six distinct sourceful original identities are preserved while only three
legacy V2 keys exist, and they reach six distinct Field Forge consumers; the
two HELD `ORDERED` obligations survive with
`hold_reason = ORDERED_OWNER_NOT_ISSUED` and exact native `m01-O` /
`ORDERED_SEQUENCE` / `AB,BA` scope.  `missing_consumers == []`.

## Real accepted owners (not reimplemented)

| Owner | Calls in `first` | Calls in `replay` |
|---|---|---|
| `ingest_c11_source_release` (C11 ingest) | 6 | 0 |
| `execute_empirical_query` (I03) | 6 | 0 |
| I05 bounded discovery | 2 | 0 |
| `BatchExecutionRunner` / P01 Field Forge consumer | 6 | 0 |

Per-link bindings verified: `link['producer_result_ref'] ==
link['consumer_material']['producer_fact_ref']`,
`relation_family == EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`,
`semantic_owner == FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER`,
`relation_semantics == EXACT_CONDITIONAL_SUPPORT_COUNT_PROFILE_WITHIN_SCOPE`,
`typed_state == SUPPORTED`, and
`participant_role_order == ["CONDITIONER","TARGET"]`.

## Route and entry points

1. `author_sourcefree_original_scope_register()` — independently authored register.
2. `repro/emit_pv2_register.py` — precommit to `freezes/`.
3. `pv2_sourcefree_fixture.pv2_sourcefree_fixture(root)` — builds the sourcefree
   original scope and freezes all records **before** any producer.
4. `PV2.run_sourcefree_with_register(...)` — reconcile the register, validate
   roles against the real topology, then delegate to the adopted
   `K.run_sourcefree` (→ `P.run_integrated` → real C11/I03/I05/P01).
5. `PV2.read_current_consumer_material(register, report)` — current-permission
   consumer read.

## Registry / blobs

Everything imported is the pinned, unmodified accepted owner:

| Module | Git blob |
|---|---|
| `rawlsing_next/pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` |
| `rawlsing_next/pre553_c11_ingest.py` | `37cd35fa2e3420a3eea272a2902e96ab9ba38aba` |
| `rawlsing_next/pre553_c11_repository.py` | `67c6eb6494522cd11aab1b93d0e73f9cef6036f3` |
| `rawlsing_next/pre553_c11_integrity.py` | `7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd` |
| `rawlsing_next/pre553_empirical_query.py` | `03facecf70890bfd13b80418620d274cbcd69d02` |
| `rawlsing_next/pre553_discovery_exact.py` | `905f24d114419dbdd93879ad2bee5b59dd2f23af` |
| `rawlsing_next/pre553_route_b_production.py` | `2385cd327dced3c5b887b59085aa0d21b04d78c3` |
| `rawlsing_next/pre553_carrier_execution.py` | `e7cda773e6a2426bfa12b22790fd8e005fe75153` |
| `rawlsing_next/pre553_batch_runner.py` | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` |
| `rawlsing_next/field_forge_conditional_support.py` | `a70decb20747d84cbcbe27d1280babc6de88ef33` |
| `rawlsing_next/pre553_source_backed_c11_facade.py` | `8a761119e4a8d68eb291fc4edfadb52e027f8284` |
| `pre553_original_workload_contract_v2_candidate.py` | `08bb75c431d3352cb0d17e9a65f7d855b4d35e59` |
| `pre553_v2_durable_consumer_integration_candidate.py` | `dc146e920909c8577b5c3c316cd9a8631e96ffd8` |
| `pre553_governed_batch_checkpoint_integration_candidate.py` | `44807c6a287145507d7332138c944cd61da363bf` |
| `pre553_batch_durable_checkpoint_candidate.py` | `719c8d878bcfb3b6c61c844c9bf974ada8365929` |
| `pre553_original_workload_v2_verifier_candidate.py` | `996c8e907f2befde93af09b60154b610c1ffeb63` |
| `pre553_original_identity_v2k_successor_candidate.py` | `e3ef9a2469966b8ecfbcd178b971f54c687aef22` |

All staged from pinned runtime `3f91dc22d2eb863bc1d2facccfd33e6c05349503`; the
accepted owners are byte-identical to the startup tree.  `module.__file__` is
the staged runtime copy in every run.

## Field Forge label caveat (carried forward, not promoted)

The retained owner is GT2-specific and still emits the hard-coded
native-variable labels `Q86B` (conditioner) and `Q86A` (target) even for the
synthetic X/Y refs.  The exact participant refs and arithmetic survive; this
specialised label must not be promoted into a generic original-science label
grant, and no I05/Route B execution claim is made.
