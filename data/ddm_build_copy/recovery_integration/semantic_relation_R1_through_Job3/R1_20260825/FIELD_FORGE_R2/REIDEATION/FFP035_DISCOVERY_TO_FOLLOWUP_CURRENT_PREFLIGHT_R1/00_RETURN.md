# FFP035 — DISCOVERY-TO-FOLLOWUP CURRENT CARRIER + OUTCOME-BLIND CANDIDATE PREFLIGHT R1

Status:

`DISCOVERY_FOLLOWUP_CURRENT_PREFLIGHT_COMPLETE__OUTCOME_BLIND__READY_FOR_CENTRAL_PREOUTPUT_JOIN`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-field-forge-r2-ffp035-discovery-followup-current-preflight-r1`

Exact starting HEAD: `7c80885c8f59614b79f881af20c94a2195d6dab2`

Instruction evidence only: `7afd7e7d8753797cd1327bce43817952d9891121:data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/FIELD_FORGE_R2/REIDEATION/FFIF012_CENTRAL_POST_SECOND_CANARY_REIDEATION_R1/09_EXACT_NEXT_HANDOFFS.md`, HANDOFF B.

Concurrent FFIF013 return evidence consumed: `NO`.

New sources acquired: `NO`.

No target follow-up comparison was executed.

## 1. Exact current risk set and empirical unit

The current discovery surface is the FFIF012F exact eight-disposition same-unit surface over the FFP017 core common coexposure risk set.

Logical risk-set identity:

`FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`

The materialized FFP017 artifact carries row label `CORE_CLAIM_COMMON_RISK_SET@1`; the logical identity and physical row label are kept distinct rather than silently collapsed.

Exact risk-set evidence:

- respondents: `19,210`;
- semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`;
- physical artifact SHA-256: `c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc`;
- stable Library ref: `libfile_2851ba4555a88191a427ba4785ceba81`.

Empirical unit is the current admitted respondent identified by `(respondent_carrier_identity, respondent_local_id)`, where the admitted respondent identity descends from exact source key `(COUNTRY, RESPNO)`. Row order is not identity.

The FFP017 declared common country scope is:

`COUNTRY_ALPHA3 NOT IN {ALG,BDI,BEN,CAM,CDI,EGY,GHA,GUI,LIB,MAD,MLI,MRC,NGR,NIG,SEN,SRL,SUD,SWZ,TAN,TOG,TUN,ZAM,ZIM}`.

Independent preflight reconstruction from the exact current 51,587-row FFP014 carrier yields exactly `19,210` rows and an exact source-key-set match to the materialized FFP017 risk-set artifact. The physical risk-set artifact is therefore available as replay evidence but is not required merely to regenerate the risk-set membership.

## 2. Exact current carrier and upstream direct-query facts

Source object remains:

- `Data/Afro Barometer Round 5.sav`;
- SHA-256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`;
- `49,689,458` bytes;
- `51,587` rows.

Current admitted FFP014 respondent carrier:

- schema/version `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`;
- carrier identity `sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`;
- physical member SHA-256 `f55741a53a4caed3f74980afba2488233caa93dd4f1a2edcfde8d90e2fcce4be`;
- logical uncompressed member SHA-256 `dd2f12232270d872405ffe4d8111540168b672aa1c9b88cac7c44ee3be13cfd7`;
- rows `51,587`;
- Library ref `libfile_23bfb6d5340881918ac372b6b8b4cf3b`.

Current FFP017 upstream exact facts:

- `selected_response_facts.tsv.gz`: `670,631` rows, SHA-256 `98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709`;
- `selected_exposure_facts.tsv.gz`: `670,631` rows, SHA-256 `0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce`.

All four heavy Library bytes used in this preflight — current carrier, core risk set, selected response facts and selected exposure facts — were rematerialized and hash-checked against the Git-bound receipts. All four matched exactly.

## 3. Exact eight-variable discovery surface

The exact FFIF012F surface is:

| variable | empirical measurement | qimpl | C04 predicate | source evidence |
|---|---|---|---|---|
| Q76A | `Afrobarometer:R5:Q76A` | `question_impl.phase0.6a1a2eb3ed5d31e7e0cf` | `C04P.9bdcc5c20d1ea29494cb` | `SEP.U1.NATIVE.c16e1235f0d08a339b4ff353` |
| Q76B | `Afrobarometer:R5:Q76B` | `question_impl.phase0.2d7f53868dd52feea700` | `C04P.3ef9d75ad37a9afd9538` | `SEP.U1.NATIVE.7426e28136508c6b2daab427` |
| Q86A | `Afrobarometer:R5:Q86A` | `question_impl.phase0.67f036c0efb7fb98ff4a` | `C04P.9c3bd54f111f068a22f8` | `SEP.U1.NATIVE.9c63ebbd5ad1126a9d88ba07` |
| Q86B | `Afrobarometer:R5:Q86B` | `question_impl.phase0.2fb3a62609dad4c1306d` | `C04P.34fb5970fdb1af3cbaec` | `SEP.U1.NATIVE.b67bc175b86139b78d81f118` |
| Q86C | `Afrobarometer:R5:Q86C` | `question_impl.phase0.5e173e45a10de7c832fd` | `C04P.40fdf23da878e2774e48` | `SEP.U1.NATIVE.4236462666e913b0f36f4196` |
| Q86D | `Afrobarometer:R5:Q86D` | `question_impl.phase0.b2b6525f8699525e60ea` | `C04P.b75dfbead8f71621ac5f` | `SEP.U1.NATIVE.c3ff715d3830f3c01f49c3fb` |
| Q86E | `Afrobarometer:R5:Q86E` | `question_impl.phase0.2aef51cfcb3d44e4870a` | `C04P.a93e49ae75ebbe415686` | `SEP.U1.NATIVE.a18cdf46693c2ff716ce0c31` |
| Q86F | `Afrobarometer:R5:Q86F` | `question_impl.phase0.0bdb38e7f76aadd487da` | `C04P.153aaa6fa7f3c82c4230` | `SEP.U1.NATIVE.965fe312a83fed515af1e2b8` |

Every one of these exact C04 predicates uses `COUNTRY_ALPHA3` as predicate input. On the current 19,210-member risk set, preflight structural checks establish exactly `19,210 × 8 = 153,680` unique respondent/variable response pairs, zero duplicates, zero respondents missing any of the eight, `153,680` unique respondent/measurement exposure pairs and zero exposure rows other than `EXPOSED__PROVED`.

Native response states remain exact source-native identities of the form `Afrobarometer:R5:<VARIABLE>:STATE=<source_response_state>`. No state recoding, special-state deletion, metricization or motif interpretation is introduced.

FFIF012F's already-adjudicated result bank reports `1,856` exact labeled eight-variable profiles and `62,609` observed exact conjunction-support rows over all 255 nonempty subsets. Those existing aggregate facts were consumed as provenance only; this worker did not recompute or rank discovered candidates against the follow-up operand.

## 4. Can discovered predicates be reconstructed without stored discovered-membership rows?

`YES__MECHANICALLY_REQUERYABLE_FROM_CURRENT_GOVERNED_FACTS`.

At FFIF012F grain, every discovered predicate is an exact finite conjunction of source-native state equalities over a nonempty subset of the eight frozen variables. Because every current risk-set respondent has exactly one exact native response fact for every one of the eight variables, predicate membership can be recomputed from predicate identity against current upstream response facts.

No stored FFIF012F predicate-membership vector is mechanically required for that reconstruction.

Likewise, direct re-query need not depend on a persisted copy of the FFP017 risk-set member list: the same exact risk-set source-key set is reproducible from the admitted current carrier plus the exact governed FFP017 common-scope/coexposure rule. The materialized risk-set bytes remain useful as replay evidence.

This is an implementation-feasibility receipt only. It does not decide what representation-neutral assertion bundle the later court must require and does not issue an architecture verdict.

## 5. Outcome-blind external follow-up candidate X

Selected candidate:

`X = COUNTRY_ALPHA3`

Exact grain: current respondent/context token already present on the admitted carrier and FFP017 respondent-linked facts.

Why this is the weakest clean current choice under HANDOFF B:

1. it is outside the eight response-measurement discovery surface;
2. it is already constitutive of current respondent context and governed exposure scope;
3. it already participates as the exact predicate input symbol for every selected FFP017 measurement;
4. FFP014 proves its bounded R5 provenance from the same respondent's exact source `RESPNO` token and validates that provenance against source `COUNTRY` for all 51,587 carrier rows;
5. it therefore requires no new semantic-role theory, state equivalence, PRA or TTAR merely to ask an exact country-token-stratified support query.

Exact current risk-set domain, inspected only for domain existence:

`{BFO, BOT, CVE, KEN, LES, MAU, MLW, MOZ, NAM, SAF, UGA}`

Domain cardinality: `11`.

Missing `COUNTRY_ALPHA3` on current risk set: `0`.

Selection receipt:

`PREFERENCE_1_EXISTING_RESPONDENT_CONTEXT_IDENTITY__NO_TARGET_RELATION_INSPECTION`.

No discovered-profile × country distribution, subgroup contrast, direction, reversal, persistence, association strength, predictive value or motif recurrence was inspected or computed before candidate freeze.

## 6. W1/W2/W3/W4/W5-style implementation feasibility

The exact rowwise receipt is `02_CHALLENGER_IMPLEMENTATION_PREFLIGHT.tsv`.

Current mechanical dispositions, with no semantic admissibility ruling:

- `W1_DIRECT_UPSTREAM_REQUERY`: mechanically feasible from exact predicate identity + regenerated governed risk set + current response facts + `COUNTRY_ALPHA3`; no stored discovered-predicate membership required.
- `W2_SUPPORT_ONLY_DISCOVERY_SUMMARY`: mechanically buildable and already demonstrated for discovery support by FFIF012F; `COUNTRY_ALPHA3` is not contained in that support-only object. This is an information-content fact, not an architecture verdict.
- `W3_FOLLOWUP_STRATIFIED_SUMMARY`: mechanically buildable after central preoutput freeze, but deliberately not materialized here because materializing it would execute the forbidden target relation.
- `W4_PREDICATE_PLUS_RESPONDENT_MEMBERSHIP_PLUS_QUERY`: mechanically buildable after freeze from current respondent-linked facts; no claim of necessity or semantic admissibility is made.
- `W5_FULL_LOSSLESS_RESPONDENT_STATE_CARRIER_PLUS_QUERY`: mechanically available from the current governed carrier/fact stack; no promotion to necessary or universal architecture is made.

## 7. Result firewall

`PASS__OUTCOME_BLIND_PREFLIGHT_FIREWALL_HELD`.

Inspected:

- exact identities and currentness;
- byte hashes;
- risk-set reconstruction and key-set equality;
- exposure/coexposure status;
- candidate-X domain existence and nonmissingness;
- respondent/variable structural completeness;
- deterministic query/materialization feasibility.

Not inspected or computed:

- discovered-profile × `COUNTRY_ALPHA3` distributions;
- conditional direction/effect values;
- subgroup contrasts;
- reversal/persistence;
- association strength;
- predictive value;
- motif recurrence;
- any target representation output used to influence candidate selection.

The machine-readable firewall and hostile receipt is `03_FIREWALL_BLOCKERS_AND_FALLBACK_RECEIPT.json`.

## 8. Exact fail-closed blockers and deterministic fallback

No current preoutput blocker was found.

A later execution must fail closed before output if any bound source/carrier/fact hash drifts; if the governed 19,210-member risk set is no longer exactly reconstructible; if any eight-variable qimpl/measurement/C04 identity drifts; if respondent × variable response completeness or proved coexposure fails; if `COUNTRY_ALPHA3` ceases to be exact, governed and same-respondent attachable; or if the requested follow-up silently requires new role/equivalence/recoding/weighting/causal/predictive/motif/transport authority.

The only permitted candidate fallback is triggered by a **preoutput identity/authority/observability failure**, never by an observed relation result. The deterministic procedure is frozen in `03_FIREWALL_BLOCKERS_AND_FALLBACK_RECEIPT.json`: return to the exact FFP017 routing/exposure matrix, restrict to exact source-native measurements outside the eight-item surface already proved coexposed on the same risk set and requiring no new semantic authority for an exact native-state query, then select by fixed lexical `source_variable` order. If no such candidate remains lawful, abstain. Do not acquire a new source and do not choose by interestingness.

Current fallback activation: `NO`.

## 9. Authority / negative ceiling

This preflight mints no PRA, TTAR, CIM, CITC, COCR or CVCR.

It does not:

- execute the discovery-to-followup target comparison;
- decide which W-style challenger is semantically sufficient or weakest;
- establish that respondent membership is or is not universally required;
- promote `COUNTRY_ALPHA3` into a global country ontology;
- harmonize countries or response states;
- create a motif, repertoire, contradiction, causal, predictive, transport or person-level interpretation;
- move PRE-MAIN or main;
- issue a FIELD FORGE architecture verdict;
- consume the concurrent FFIF013 worker return.

The correct next act is the central preoutput join required by the immutable handoff: compare this actual current carrier/candidate feasibility against the independent representation-neutral design return, freeze the exact assertion/support/comparison/closure universe, and only then authorize the smallest target execution if still lawful.

Terminal:

`DISCOVERY_FOLLOWUP_CURRENT_PREFLIGHT_COMPLETE__OUTCOME_BLIND__READY_FOR_CENTRAL_PREOUTPUT_JOIN`
