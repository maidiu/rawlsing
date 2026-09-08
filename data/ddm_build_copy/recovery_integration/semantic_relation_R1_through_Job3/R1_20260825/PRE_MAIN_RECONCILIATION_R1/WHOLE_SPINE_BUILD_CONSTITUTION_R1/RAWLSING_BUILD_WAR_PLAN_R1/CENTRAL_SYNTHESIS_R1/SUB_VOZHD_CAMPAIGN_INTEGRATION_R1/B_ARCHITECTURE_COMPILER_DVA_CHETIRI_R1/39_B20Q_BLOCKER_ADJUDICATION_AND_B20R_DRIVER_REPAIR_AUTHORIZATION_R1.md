# SUB-VOZHD B — B20Q BLOCKER ADJUDICATION + B20R QUALIFICATION-DRIVER REPAIR AUTHORIZATION R1

Status:
`B20Q_EXACT_DRIVER_BLOCKER_ACCEPTED__ROUTE_C_IMPLEMENTATION_REMAINS_FROZEN__B20R_DRIVER_ONLY_REPAIR_AUTHORIZED__B19Q_CONTINUES_IN_PARALLEL`

Campaign branch:
`agent/sub-vozhd-architecture-compiler-dva-chetiri-r1`

B20Q worker branch:
`agent/rabochii-subv-b-as4i-route-c-cacc1-cacc2-parity-qualification-r1`

B20Q final tip:
`cf0f394f4b5ea5550a1d60eacb01615f02bb6832`

Campaign bank merge:
`46fba94930e1f4e59ee9da23ae26e3bec8da58e4`

Accepted B20Q terminal:
`AS4I_ROUTE_C_CACC1_CACC2_PARITY_QUALIFICATION__EXACT_BLOCKER_PROVED`

## 1. Exact reproduced failure

Two independent clean worktrees at exact commissioned B20Q tree:
`3cc730b04a4da31b97b80c8d1bf612da4301a9bf`

Environment:
- CPython 3.13.15
- pyarrow 25.0.1
- pandas 3.0.5

Both runs fail identically before CACC1 construction:

`TypeError: unhashable type: 'dict'`

at frozen qualification-driver expression:

`fact.question_or_target_ref in allowed_qrefs`

Normalized stderr SHA-256:
`79c75644492d00c6821dd40bb739478451c10017eb3b252d16db5991d9d52ac5`

No CACC1/CACC2 qualification, query parity, I05 parity, hostile court, delete/regenerate proof, or internal fresh-process replay was entered.

## 2. Route-C implementation status

Route-C implementation remains frozen and unmodified.

Implementation file:
`rawlsing_next/pre553_route_c_accelerators.py`

Frozen implementation blob:
`ed249de09b15b1b948d9e79bd3056e58967d2e66`

Frozen implementation SHA-256:
`d949394ad18c89e1956ec317d43993d36477d9ef4ebe1c3bdb1f5f12d4a8aa17`

No defect in Route-C accelerator semantics has yet been proved.

The blocker is in the bounded qualification fixture filter.

## 3. Canonical repo-native normalization law

`RoutingEligibilityFact.question_or_target_ref` is canonical semantic mapping material at runtime.

The repo-native exact reference converter is:

`rawlsing_next.pre553_empirical_objects.exact_ref(value, name)`

It accepts an `ExactRef` or exact mapping:
`{"kind","object_id","content_hash"}`

and returns the exact hashable `ExactRef`.

Therefore the smallest lawful repair is:

- import/use `exact_ref`;
- normalize `fact.question_or_target_ref` before membership comparison against the frozen allowed `ExactRef` set.

Conceptual replacement:

`exact_ref(fact.question_or_target_ref, "routing question_or_target_ref") in allowed_qrefs`

No other semantic, fixture, accelerator, query, discovery, or parity law may change without a separately proved defect.

## 4. B20R authorized grain

Authorize exactly:

`B20_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR`

B20R may modify ONLY:
- the committed B20 qualification driver;
- B20R repair/identity receipts.

B20R MUST NOT modify:
- `rawlsing_next/pre553_route_c_accelerators.py`;
- common query/discovery/source-backed semantic modules;
- frozen Route-C candidate definitions;
- B20Q evidence.

## 5. Repair proof

B20R must:
1. bind the exact pre-repair driver blob/SHA;
2. make the minimum canonical `exact_ref` normalization change;
3. commit the repaired driver before any validating execution;
4. prove the diff is limited to the normalization/import necessary for this exact failure;
5. run a minimal fixture-construction smoke check proving the prior TypeError is gone;
6. stop before claiming full Route-C qualification PASS.

If the smoke check reaches beyond the former failure point without a new driver defect, B20R returns:
`B20_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR_COMPLETE__READY_FOR_B20Q2_FULL_QUALIFICATION`

If a different committed-driver defect emerges during smoke:
`B20_ROUTE_C_QUALIFICATION_DRIVER_REFERENCE_NORMALIZATION_REPAIR__EXACT_BLOCKER_PROVED`

Do NOT patch additional defects in the same repair unless they are an immediate mechanical consequence of the same reference-representation normalization and are explicitly evidenced.

## 6. B19Q remains active

B19Q:
`agent/rabochii-subv-b-as4i-route-a-adapter-qualification-r1`

Handoff:
`0adb463d97b9f4726eb4aad8cc112c9cc092ae13`

Its qualification remains incomplete and independent.

Do not interrupt or rebranch B19Q merely because B20Q blocked.

## 7. Common harness remains gated

HB04 common deterministic A/B/C harness remains closed until:
- B19Q PASS;
- repaired Route-C driver is fully requalified by a separate B20Q2 PASS.

## 8. Hard stops

B20R must NOT:
- alter Route-C implementation;
- claim Route-C qualification PASS;
- execute real C09;
- execute WVS7;
- benchmark/rank candidates;
- implement common harness;
- launch OBL037;
- select architecture/topology;
- enter positive V3;
- mutate central/PRE-MAIN/main.

Terminal:
`SUB_VOZHD_B_B20Q_BLOCKER_ACCEPTED__B20R_DRIVER_ONLY_REPAIR_NEXT__B19Q_CONTINUES__COMMON_HARNESS_GATED`
