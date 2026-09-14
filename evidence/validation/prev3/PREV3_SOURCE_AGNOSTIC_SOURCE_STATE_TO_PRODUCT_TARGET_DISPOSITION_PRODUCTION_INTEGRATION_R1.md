# PRE-V3 source-state → product-target production integration R1

## Result

**PASS at the producer/implementation ceiling.** K02 productionizes J02's reusable source-agnostic contract in a bounded PRE553 adapter without changing the ordinary PRE553 query implementation and without consuming K03 or any other ninth-wave return.

The production path is fixed as:

`RAW_SOURCE_STATE -> SOURCE_LOCAL_GOVERNED_STATE -> PRODUCT_TARGET_DISPOSITION -> DENOMINATOR_RESOLUTION_CHECK -> EMPIRICAL_RESULT`

## Production seam

`rawlsing_next/source_state_target_disposition_contract.py` is the generic contract core. Its schema has no native/raw/source-family key for target bindings. Raw response material contributes only an opaque audit hash; the lookup key is the exact governed tuple `(empirical universe, response state, authorized canonical response value)`. `TARGET_MEMBER`, `RESOLVED_NON_TARGET`, and `UNRESOLVED` are the only target-stage dispositions. Post-outcome denominator deletion is therefore not expressible at the target stage.

`rawlsing_next/pre553_source_state_target_disposition.py` binds that core to the existing PRE553 C11/query seam. It requires exact content-addressed `SOURCE_SEMANTICS_TOPOLOGY`, `TARGET_USE_PERMISSION`, `ROUTING_RISK_SET`, and `REPLAY_PROTOCOL` authority bindings for every exact query universe and target. Target-use and risk-set authority must be distinct. Risk-set authority is fixed as `FROZEN_PRE_OUTCOME` and is checked on the exact routing fact before any target event is inspected.

For every condition-selected denominator member, the adapter inspects all matching target events without using the legacy `included_states` filter as an exclusion mechanism. Missing events, unmapped governed states, missing authorized canonical values for substantive responses, incompatible topology, or unresolved target disposition remain in the frozen expected-record ledger and fail the denominator gate. The ordinary PRE553 `execute_empirical_query` producer is called only after every contract gate passes. A resolved `SUPPORTED` fact must satisfy `raw_resolved_target_support == raw_denominator_support`.

The replay identity includes the normalized source-state/authority bindings, complete denominator ledger and record audits, gate hashes, query/release identities, emitted fact identities, and final result hash.

## Targeted self-test

Exact candidate contents were executed in isolated scratch before commit. The self-test passed **15/15** checks and both production modules plus the self-test passed Python bytecode compilation. The fixed synthetic replay identities are:

- contract hash: `7d0f34e62ca4ae1d1806de6e9aeaf8c3e6af463c2d0d206539f94fcd50dbe798`
- denominator gate hash: `7710fcc7a32dbea7aeff11b2039adf586f6a02390572b196cae8da1123ccaefd`
- empirical-result hash: `6cb2b30265cedec2dedda35fbbedb61cfa7b34ae1fdb47f05677c22d9d79b3de`
- replay identity: `505cd5e1b3611e600b55267e9245135035cc9e56c0a2d16396cf6cf9427bf014`

The checks cover same opaque native material with different governed source-local meanings, fail-closed unmapped/nonresponse states, denominator retention, pre-result gating, exact record accounting, prohibition of target-stage denominator deletion, distinct target/risk authority, frozen pre-outcome risk authority, inexpressibility of native-code tables in the generic schema, prohibition of raw fallback for substantive resolution, support-equality enforcement, deterministic replay, source-agnostic adapter content, and the OBL063 quarantine boundary.

Repository replay commands after checkout:

```text
python3 evidence/selftest/prev3_source_state_target_disposition_production.py
python3 -m py_compile rawlsing_next/source_state_target_disposition_contract.py rawlsing_next/pre553_source_state_target_disposition.py evidence/selftest/prev3_source_state_target_disposition_production.py
```

## Bounds / successor gate

No LiTS or other survey-specific meaning is present in generic production logic; no native numeric/string meaning is assigned; no learned 50-candidate workload was executed; no K03 return was consumed; no V553+ structural, V3, or V2 behavior was changed. This lane does **not** independently qualify itself. Fresh independent qualification is required before HQ may centrally integrate this producer. K02 and K03 converge only at HQ before learned-world re-execution.
