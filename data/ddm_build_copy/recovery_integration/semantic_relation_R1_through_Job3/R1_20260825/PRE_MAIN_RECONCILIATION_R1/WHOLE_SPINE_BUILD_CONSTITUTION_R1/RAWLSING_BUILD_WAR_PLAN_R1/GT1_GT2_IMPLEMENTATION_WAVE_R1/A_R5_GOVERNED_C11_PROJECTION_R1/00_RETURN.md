# GT12-A — R5 GOVERNED C11 PROJECTION + DOMAIN/AUTHORITY BINDING R1 — RETURN

Status:

`PASS__GT12A_R5_C11_PROJECTION_READY_FOR_CENTRAL_INTEGRATION`

## Execution identity

- Repository: `maidiu/rawlsing`
- Worker lane: `GT12-A — R5 GOVERNED C11 PROJECTION + DOMAIN/AUTHORITY BINDING R1`
- Branch: `agent/rabochii-warplan-gt12-a-r5-c11-projection-r1`
- Exact working ancestry start: `2c95e64b9be9b9c730028c840e04596dc556893`
- Immutable instruction/evidence ref: `17b9abc5c8c3038d14670c6e68136bb868f5073a`
- Frozen canary contract: `a9416094cbb4653dd2de2e4aa7b67577a355560c`
- Sibling GT12 implementation branches consumed: `NONE`
- Source acquisition: `NONE`
- I03 execution performed by this lane: `NO`
- PRE-MAIN/main movement: `NO`

## Implemented bounded surface

Created:

- `rawlsing_next/wave1_r5_q86_c11_projection.py`
- `rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py`

The implementation reuses current `pre553_source_backed_c11_facade.py`, current PRE553 public/internal object types, current C11 validation, and current exact authority registry. It does not introduce a new empirical engine or a generic Afrobarometer compiler.

Public production entrypoints:

- `build_r5_q86_c11_projection(...)`
- `build_validated_r5_q86_c11_release(...)`
- `q86_target_domain(...)`
- exact domain/currentness/risk-set/target-use reference helpers exported by the bounded module.

`build_validated_r5_q86_c11_release(...)` stops at current validated C11. It does not execute I03; GT12-B retains that jurisdiction.

## Exact frozen source/current carrier identities

The production binding fails closed unless the supplied binding object is exactly the frozen R5 binding:

- source: `Data/Afro Barometer Round 5.sav`
- source SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- source rows: `51,587`
- respondent carrier: `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`
- respondent-carrier identity SHA-256: `6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`
- selected response-fact carrier SHA-256: `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`
- selected exposure-fact carrier SHA-256: `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`
- common risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- risk-set rows: `19,210`
- risk-set semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- Q86 source structure: `cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`
- source-structure identity SHA-256: `ea9614b69e63a8e5bc87e65c944d67445082639fe45262da626bd6aa1a4d9e99`
- governed R5 codebook SHA-256: `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`

## Exact Q86 bindings

Q86A:

- qimpl: `question_impl.phase0.67f036c0efb7fb98ff4a`
- qimpl identity SHA-256: `67f036c0efb7fb98ff4a93dc811bf59cfc095608eda374f6534b006a62241bd3`
- exposure predicate: `C04P.9c3bd54f111f068a22f8`
- predicate: `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}`
- source evidence: `SEP.U1.NATIVE.9c63ebbd5ad1126a9d88ba07`

Q86B:

- qimpl: `question_impl.phase0.2fb3a62609dad4c1306d`
- qimpl identity SHA-256: `2fb3a62609dad4c1306d8cfa14f997eab4d6e65ada56083279386a202544a506`
- exposure predicate: `C04P.34fb5970fdb1af3cbaec`
- predicate: `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}`
- source evidence: `SEP.U1.NATIVE.b67bc175b86139b78d81f118`

The frozen common-risk country domain is retained exactly as:

`{BFO,BOT,CVE,KEN,LES,MAU,MLW,MOZ,NAM,SAF,UGA}`.

That country membership is used only because accepted FFP017 evidence proved that declared scope to be exactly equal to the frozen 12-measurement common-coexposure set for the admitted R5 respondents.

## Source-native Q86A/Q86B domains

The exact source-native state domain for each target is frozen from governed R5 codebook metadata:

| source code | source label | PRE553 response state |
|---|---|---|
| `0` | `No` | `SUBSTANTIVE_RESPONSE` |
| `1` | `Yes` | `SUBSTANTIVE_RESPONSE` |
| `9` | `Don't know` | `DK` |
| `997` | `Not asked` | `NOT_ASKED` |
| `998` | `Refused to answer` | `REFUSAL` |
| `-1` | `Missing` | `MISSING` |

No source-native state is collapsed or dropped. Numeric source codes are identity only and are explicitly denied order/metric authority. Q86A and Q86B receive separate exact domain refs and separate target-domain replay refs.

## Response/exposure separation

The adapter requires distinct governed row fields for:

- Q86A raw response + response state;
- Q86A exposure state;
- Q86B raw response + response state;
- Q86B exposure state.

For every respondent admitted to the exact common risk set, both Q86A and Q86B must independently carry `EXPOSED__PROVED`. A substantive response does not satisfy that requirement. Risk-set membership is not inferred from response presence, response substance, physical co-presence, or Q86 source-block membership.

The production adapter also requires:

- exactly 51,587 governed source rows;
- exact one-to-one row replay coordinates;
- unique admitted `(COUNTRY, RESPNO)` respondent identity;
- exactly 19,210 rows in the frozen common-risk country scope.

These checks are in addition to current C11 facade validation.

## Authority/currentness binding

The bounded projection packages exact immutable `AuthoritySnapshot@1.0.0` records only for the operations required by GT1/GT2:

1. R5 Q86A/Q86B source semantics/topology;
2. exact common-coexposure routing/risk-set semantics;
3. source-native `COUNTRY_ALPHA3` coordinate identity used for the already-governed routing rule;
4. physical/current-carrier reexpression only, with explicit `semantic_owner_transfer = false`;
5. deterministic C11 replay;
6. the frozen GT1/GT2 target-use permission ceiling.

Currentness is pinned to the frozen canary contract and implementation program by exact immutable reference material. No latest/default/fuzzy selection exists.

The target-use ceiling does not create structural or actor authority. GT1 remains empirical-fact-only; GT2 remains empirical input to the separately governed frozen conditional-support path.

## C11 projection behavior

The generated `GovernedC11Projection` contains:

- one exact R5 `EmpiricalUniverse`;
- exact admitted respondent identities;
- exact Q86A/Q86B `QuestionVariableBinding` records;
- exact source-native `RespondentEvent` projection rules;
- exact common-risk `RoutingEligibilityFact` records;
- source-native `COUNTRY_ALPHA3` coordinate facts for routing replay;
- no weights (`NOT_APPLICABLE`);
- no inferred source relation (`DISTINCT_BY_DEFAULT`);
- comparator/discovery replay explicitly `DEFERRED`;
- structural replay explicitly `NOT_APPLICABLE`;
- deterministic projection/replay identity.

The current source-backed C11 facade remains responsible for complete projected-slot coverage, exact authority closure, source-SHA matching, replay sealing, and atomic C11 validation.

## Focused hostile regression

Authored focused tests cover:

1. source-binding tamper and risk-set-hash tamper fail closed;
2. exact Q86 native-domain preservation including `997/998/-1`, plus out-of-domain and response-state mismatch rejection;
3. substantive response cannot substitute for independent exposure proof;
4. missing required authority fails at the current `GovernedC11Projection` constructor;
5. deterministic projection/release/replay identity under input row reordering.

### Execution receipt

- Python syntax validation of the exact authored module/test source: `PASS`.
- Focused pytest execution in this worker runtime: `NOT_AVAILABLE__NO_REAL_REPOSITORY_CHECKOUT_OR_TEST_EXECUTOR`.
- GitHub Actions run on the worker commits: `NONE`.

No pytest count is claimed. The test suite is banked for central integration/real-checkout execution.

## Library use

`YES__BOUNDED_GOVERNED_METADATA_ONLY`.

The already-present Library copy of `merged_r5_codebook_2.pdf` was inspected only to freeze the exact Q86A/Q86B source-native state domain. No source data were acquired, and no empirical response distribution was inferred from the codebook.

## Ceiling

GT12-A does not:

- execute GT1/GT2 I03 queries;
- produce an `EmpiricalFact`;
- infer executable J from Q86 source-block membership;
- use response presence as exposure;
- add weights or estimand authority;
- harmonize Q86 values;
- impose order/metric semantics on source codes;
- create a FIELD FORGE relation;
- admit anything into PRE-V3;
- create actor facts or V3 transition authority;
- select physical architecture;
- move PRE-MAIN or `main`.

Terminal:

`PASS__GT12A_R5_C11_PROJECTION_READY_FOR_CENTRAL_INTEGRATION`
