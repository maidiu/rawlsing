# FFX001-B — CANARY BINDING CHAIN

Canary: `Afrobarometer R5 Q86A–Q86F`

Structure: genuine repeated-measurement matrix/grid retained from FFX001-A.

## Exact current members

| member | question_implementation_id | current disposition | predicate_id | evidence_ref |
|---|---|---|---|---|
| Q86A | `question_impl.phase0.67f036c0efb7fb98ff4a` | `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` | `C04P.9c3bd54f111f068a22f8` | `SEP.U1.NATIVE.9c63ebbd5ad1126a9d88ba07` |
| Q86B | `question_impl.phase0.2fb3a62609dad4c1306d` | `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` | `C04P.34fb5970fdb1af3cbaec` | `SEP.U1.NATIVE.b67bc175b86139b78d81f118` |
| Q86C | `question_impl.phase0.5e173e45a10de7c832fd` | `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` | `C04P.40fdf23da878e2774e48` | `SEP.U1.NATIVE.4236462666e913b0f36f4196` |
| Q86D | `question_impl.phase0.b2b6525f8699525e60ea` | `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` | `C04P.b75dfbead8f71621ac5f` | `SEP.U1.NATIVE.c3ff715d3830f3c01f49c3fb` |
| Q86E | `question_impl.phase0.2aef51cfcb3d44e4870a` | `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` | `C04P.a93e49ae75ebbe415686` | `SEP.U1.NATIVE.a18cdf46693c2ff716ce0c31` |
| Q86F | `question_impl.phase0.0bdb38e7f76aadd487da` | `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY` | `C04P.153aaa6fa7f3c82c4230` | `SEP.U1.NATIVE.965fe312a83fed515af1e2b8` |

All six C04 rows identify:

- source family: `Afrobarometer`
- wave: `R5`
- release scope: `MERGED_35_COUNTRY_ROUND_RELEASE`
- release form: `STANDARDIZED_MERGED_ROUND_RELEASE`
- routing evidence kind: `NATIVE_ROW_READ`
- evidence class: `native_named_country_administration_note`
- source grade: `NATIVE_PRIMARY`
- source overlay: `afrobarometer_R5_semantic_authority_overlay.csv`

## Target proof chain status

| required link | status | exact finding |
|---|---|---|
| CURRENT source/question implementation identity | PASS | Six exact current `question_implementation_id` values are established by C04 and conserved by Contract@2. |
| current respondent-data carrier | NOT ESTABLISHED | No separately governed CURRENT respondent-grain carrier was canonically reached in the bounded search. |
| exact respondent identity/key | NOT ESTABLISHED | No governed respondent key was established for an admissible current carrier. |
| exact source/wave/country/form scope | PARTIAL PASS | Question-level `Afrobarometer/R5/MERGED_35_COUNTRY_ROUND_RELEASE/STANDARDIZED_MERGED_ROUND_RELEASE` is exact; respondent-to-country/form binding is not established. |
| exact variables required by routing predicate | SEMANTICS PASS / BINDING BLOCKED | Required input is `COUNTRY_ALPHA3`; no current governed respondent-grain value binding was established. |
| governed predicate semantics | PASS | All six compile to `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}`. |
| deterministic predicate execution | BLOCKED AT RESPONDENT INPUT | Predicate is deterministic if supplied a governed respondent `COUNTRY_ALPHA3`; no admissible respondent relation was established on which to execute it. |
| exact respondent-level exposure classification | NOT MATERIALIZED | No respondent rows emitted. |
| exact repeated-measurement member exposure/risk set | NOT MATERIALIZED | Q86A–Q86F risk set cannot be emitted without the missing respondent bridge. |

## Broken link

The chain breaks between current question-level predicate authority and a current respondent entity:

`question_implementation_id + predicate(COUNTRY_ALPHA3)`

`--/-->`

`governed CURRENT respondent_key + respondent.COUNTRY_ALPHA3`

No lawful join key was established.

## Why the chain is not repaired by response facts

Neither a present response nor a missing response may be substituted for administration/exposure. Doing so would collapse response into exposure and violate the FFX001-A noncollapse.

## Terminal state

`CURRENT_RESPONDENT_BINDING_NOT_CANONICALLY_REACHABLE_FOR_Q86_CANARY`
