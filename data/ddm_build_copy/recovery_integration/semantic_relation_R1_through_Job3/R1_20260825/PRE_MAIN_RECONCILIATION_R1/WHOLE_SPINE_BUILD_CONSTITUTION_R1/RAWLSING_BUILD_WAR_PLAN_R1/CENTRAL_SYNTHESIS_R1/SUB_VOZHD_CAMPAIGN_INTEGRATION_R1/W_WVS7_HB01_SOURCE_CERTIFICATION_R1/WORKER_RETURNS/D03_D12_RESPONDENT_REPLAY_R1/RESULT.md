# WVS7/HB01 — D03 + D12 RESPONDENT REPLAY AUTHORITY R1

Status:
`WVS7_D12_SCOPED_RESPONDENT_REPLAY_AUTHORITY_COMPLETE__D03_PERSON_POSITION_PRESENCE_EXACTLY_DISPOSITIONED__READY_FOR_SUB_VOZHD_W_JOIN`

This result supersedes both earlier same-branch transport blockers. The exact Library carrier was successfully materialized and executed.

## Exact source gate — PASS

Carrier:

- Library object: `WVS Wave 7.sav.zip`
- Library file ID: `file_00000000386c820d8760e748b25ad7e1`
- contained source: `WVS Wave 7.sav`
- contained SAV size: 185,163,494 bytes
- exact contained SAV SHA-256:
  `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- exact shape: 97,220 rows × 613 released variables = 59,595,860 physical cells

The populated physical probe was not used.

## D12 — PASS

Accepted respondent identity protocol:

`SOURCE_SHA256_PLUS_SOURCE_ROW_ORDINAL`

For every source row 1..97,220, the worker deterministically constituted a scoped respondent ref from the exact source snapshot SHA plus source row ordinal. Exact source scope is bound independently by source-native `S025 + B_COUNTR + A_YEAR`.

The exact source partitions into 66 non-overlapping contiguous source scopes covering all 97,220 rows exactly once.

Compact ledger:

`COUNTRY_SOURCE_SCOPE_ROW_RANGES.csv`

Ledger SHA-256:

`cf0dfaae7a2f0f19b34ccc536b93e6aedbf37bf047d5d864e5c812fe9602d6a9`

Global ordered row-binding digest:

`895fed8dd6811307c4452194e8fa1a1fba4c670644da8f17f5b7a628d610bac9`

Exact replay ref:

`urn:rawlsing:pre553:gsr07:wvs7:d12-scoped-respondent-replay:sha256:9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b`

Replay content hash:

`9d44d5097258b96c5c49faf968b85701f80ecd75df6b214a528abb6fb15ef44b`

### Fresh replay parity

Two independent executions each began from the exact raw SAV and independently decoded all 97,220 rows.

Both raw projections reproduced:

`7e69d799e37d26c2e6ae749674d4994a276f93aaf89e43085bed34a5fd122ec9`

Both replay builds reproduced:

- the same 66-scope ledger SHA;
- the same ordered row-binding digest;
- the same exact replay ref;
- the same full generated manifest SHA
  `3b5b0ee0997fcd483786a428be97cf2fca6a1c46a09d4c5c878f971759ff6f24`.

The two raw projections, scope ledgers, and generated replay manifests were byte-identical across executions.

### D_INTERVIEW / S007 anti-promotion proof

`D_INTERVIEW` is not unique in the exact source:

- 97,220 rows
- 96,221 distinct values
- value `858069901` occurs 1,000 times

`S007` has 97,220 distinct values in this exact release, but uniqueness does not authorize canonical identity. It remains source-native only because the accepted identity protocol is source snapshot SHA + row ordinal.

Neither `D_INTERVIEW` nor `S007` participates in scoped respondent identity.

## D03 — exact fail-closed disposition

Targets:

`Q276/Q276A/Q277/Q277A/Q278/Q278A/Q280/Q282/Q283`

All nine remain:

`ROUTING_UNKNOWN`

This is now a source-backed adjudication, not an unexecuted inherited placeholder.

The entire 613-variable source dictionary was inspected for independent spouse/mother/father person-position presence inputs.

### Spouse

The source contains `Q273` marital status, but neither the accepted routing law nor the source-owner instrument supplies an exact Q273-category → spouse/partner-presence routing map. Ordinary-language assumptions are not authority.

The spouse target fields themselves encode not-applicable/filter states, but using target response/missingness to determine their own applicability is forbidden.

Therefore no positive or negative spouse-presence fact was minted.

### Mother

The source contains mother migration/birth/co-residence material such as `Q264`, `Q267`, `V002`, `V002A_01`, and `Q271`. These encode immigration, birthplace, or co-residence content; none is an independent mother-existence/person-position roster.

The mother target fields cannot self-route from their response/missingness.

Therefore no positive or negative mother-presence fact was minted.

### Father

The source contains father migration/birth/co-residence material such as `Q265`, `Q268`, `V001`, `V001A_01`, and `Q271`. These are not independent father-existence/person-position presence inputs.

For `Q283`, the source-owner questionnaire explicitly requires last-job fallback even when the father had already died when the respondent was 14; current survival/presence therefore cannot substitute for the governed historical person-position determinant.

Therefore no positive or negative father-presence fact was minted.

Exact per-target adjudication is banked in:

- `D03_PERSON_POSITION_ADJUDICATION.csv`
- `D03_SOURCE_FIELD_INVENTORY.csv`

## Boundary

This worker did not:

- create D11 EmpiricalUniverse objects;
- execute GSR07 full certification;
- execute C09;
- alter C11/I03/I04/I05 semantics;
- infer routing from missingness, response incidence, frequencies, or row complement.

D12 is complete for all 66 source scopes. D03 remains exact typed `ROUTING_UNKNOWN` for the nine person-position targets.

Terminal:

`WVS7_D12_SCOPED_RESPONDENT_REPLAY_AUTHORITY_COMPLETE__D03_PERSON_POSITION_PRESENCE_EXACTLY_DISPOSITIONED__READY_FOR_SUB_VOZHD_W_JOIN`
