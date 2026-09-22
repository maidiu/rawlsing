# Required hostile tests — source-free court

All tests below are synthetic/source-independent. They must not open or materialize any raw survey carrier. They are designed to reject illegal adapters and missing provenance before any candidate execution.

| Test | Source(s) | Failure class / check | Synthetic mutation | Required result |
|---|---|---|---|---|
| HT01_R5_INT_FLOAT_NONINTERSECTION | all | `DECODER_RUNTIME_TYPE__GOVERNED_KEY_NONINTERSECTION` | Build a governed key from Python `int(1)` and present a physical cell whose qualified decoder form is `float(1.0)` with otherwise identical state/declaration. | Keys differ; no numeric-equality fallback; runtime package is rejected until exact decoder representation is bound. |
| HT02_R5_BOOL_INT_NONINTERSECTION | all | C01 | Compare `True` with `1` under identical physical state/declaration. | Typed keys remain different; host-language equality must not collapse them. |
| HT03_MISSING_DECLARATION_IS_KEY_MATERIAL | all | C01/C02 | Keep raw value/state fixed but mutate the exact user-missing declaration. | Physical binding key changes; consumer cannot ignore declaration form. |
| HT04_SYSTEM_USER_ORDINARY_NONCOLLAPSE | EVS2008/WVS1/LAT2011; EVS1999 after C02 repair | C02 | Present ordinary storage, system missing, and user-missing state with numerically similar/same sentinel material. | Three physical forms remain distinguishable; no generic null/sentinel rewrite. |
| HT05_EVS_COMPAT_TEXT_NO_SEMANTICS | EVS1999/EVS2008 | `LAWFUL_AUTHORITY_REPRESENTATION__CONSUMER_IGNORES_FORM` | Supply readable/contradictory latin1 compatibility text beside exact producer documentary authority. | Producer documentary authority wins; compatibility rendering remains physical/debug evidence only. |
| HT06_EVS1999_TYPED_MISSING_DIMENSION_REQUIRED | EVS1999 | C02 | Construct a candidate physical expectation that omits missing-state/declaration evidence while claiming exact `user_missing=True` preservation. | Reject. This test is expected to remain red until the source-free C02 contract gap is closed. |
| HT07_EVS2008_V372_NO_SUBCODE_INVENTION | EVS2008 | C10 | Supply the rendered v372 sentinel and ask runtime adapter to choose one of -1..-5 without a separately authorized numeric/storage witness. | Reject; retain unresolved negative-domain state/detail. |
| HT08_EVS2008_MR_ALIAS_TOPOLOGY | EVS2008 | C03/C11 | Collapse exact alias set identities or overlapping subset identities because member vectors match. | Reject; preserve all admitted native MR identities and membership/order. |
| HT09_WVS1_S007_DISPLAY_NOT_RAW | WVS1 | form preservation | Replace large numeric S007 raw storage with an F2.0-derived display string/truncated value. | Reject; raw storage and display metadata remain independent witnesses. |
| HT10_WVS1_ALL_SYSTEM_COLUMN_SURVIVES | WVS1 | C02/C11 | Drop `I_WOMPOL` or another all-system column, or replace it with a generic absent column. | Reject; exact variable identity, rowwise system-missing incidence, and declared user-missing metadata survive. |
| HT11_WVS1_RISK_SET_FROM_MISSINGNESS | WVS1 | `RISK_SET_DECLARED__MEMBERSHIP_PREIMAGE_UNAVAILABLE` | Manufacture eligibility/risk membership from an all-system block, a “Not asked” label, or missingness frequency. | Reject with authority-blocked/unknown outcome; no risk-set ref may be minted. |
| HT12_WVS1_DEFAULT_WEIGHT_FROM_NAME | WVS1 | C03/C10 | Select V236 because label says “Weight”, or choose any of 13 carriers by name/suffix alone. | Reject; no default/design/estimand authority is created. |
| HT13_LAT2011_QUESTIONNAIRE_STORAGE_CODE_COLLAPSE | LAT2011 | form preservation / C06 | Treat questionnaire-layer response code as released-SAV storage code for P1ST merely because numbers look equivalent/near-equivalent. | Reject; exact authority layer remains part of the binding. |
| HT14_LAT2011_WT_DEFAULT_OR_POOL | LAT2011 | C03/C10 | Emit a valid PRE553 WeightMeasureFact from WT presence alone, with invented pooled estimand/default design authority. | Reject; exact design and estimand authorities are mandatory. |
| HT15_LAT2011_ORDINAL_CONVENTION | LAT2011 | C03/C11 | Bind WT using packet zero-based ordinal 413 as though it were the generic decoder's one-based slot 413 instead of explicit 414 decoder slot identity. | Reject slot mismatch; index convention must be declared and exact variable name+decoder slot preserved. |
| HT16_NATIVE_ID_NOT_REPLAY_KEY | WVS1/LAT2011 | C03/C11 | Replace source-SHA+row-ordinal replay with S007/V3 or NUMENTRE/IDENPA+NUMENTRE because a field/pair is injective in one snapshot. | Reject; snapshot uniqueness is not identity authority. |
| HT17_CROSS_QUESTION_EQUAL_CODE_NO_BINDING | all | `QUESTION_VALUE_BINDING__EXACT_RESPONSE_REF_UNAVAILABLE` | Reuse a response rule for question B because question A has the same numeric physical code. | Reject unless exact question/value authority and question-specific response ref are present. |
| HT18_HISTORICAL_AUTHORITY_AMBIENT_CURRENT_SWAP | all | `HISTORICAL_FILE__AMBIENT_CURRENT_DEPENDENCY` | Replace the frozen historical authority snapshot with an ambient current document/version while preserving apparent labels/schema. | Reject authority closure even if product shape matches. |
| HT19_RUNTIME_CATALOG_SCOPE_DRIFT | all | `HISTORICAL_SUCCESSOR__RUNTIME_CATALOG_SCOPE_NOT_ENFORCED` | Resolve an exact historical/successor ref against a different current runtime catalog identity. | Reject; no latest/default/nearest catalog fallback. |
| HT20_DYNAMIC_QUERY_STATIC_CATALOG_ONLY | all runtime packages | `DYNAMIC_QUERY_REF__STATIC_CATALOG_ONLY_RESOLUTION` | Present a generated query ref that is absent from a static catalog but has a valid generated preimage; then separately present one with no preimage. | First must resolve through its retained generation path; second must reject/defer. Static catalog absence alone cannot falsify a lawful dynamic ref. |
| HT21_I05_FACT_WITHOUT_PREIMAGE | all runtime packages | `I05_FACT_EXISTS__POSTCONSUMER_PREIMAGE_MISSING` | Give post-I05 consumer an exact fact ref/result but delete its query/predicate/source-scope construction preimage or semantic input refs. | Reject/defer consumption; fact existence is insufficient. |
| HT22_SOURCE_STATE_TO_GENERIC_FIELD_SUBSTITUTION | all | `SOURCE_SPECIFIC_TERMINAL_DOMAIN__GENERIC_FIELD_SUBSTITUTION` | Put source-local unknown/missing/routing detail into a generic PRE553 state solely because the name seems close. | Reject unless an exact authority-backed adapter establishes the mapping; otherwise retain source detail/explicit absence. |
| HT23_RISK_MEMBER_REPLAY_MUTATION | EVS1999/EVS2008 runtime routing packages | risk-set ownership | Keep risk_set_ref/routing rule fixed but mutate one respondent in member-set replay. | Reject exact routing fact/package identity. |
| HT24_PRODUCT_SHAPE_NOT_PRIOR_TRUTH | all runtime packages | `CURRENT_PRODUCT_SHAPE_MATCHES__SUBSTANTIVE_PRIOR_TRUTH_NOT_PROVED` | Produce the same terminal counts/schema shape as an accepted historical product but omit exact semantic replay/provenance authority. | Do not treat shape equality as substantive prior-truth proof. |
| HT25_WHOLE_SOURCE_EDGE_DIMENSION_DROP | all | C11 | Remove one source-declared required physical dimension while leaving semantic outputs unchanged. | Reject physical qualification; semantic agreement cannot cure physical loss. |

## Required source-specific assertions

### EVS 1999

The hostile court must include a deliberately mismatched documentary-code/R5 representation pair. It must prove that a future adapter cannot build an integer/string key from the documentary code and then silently accept a numerically equal decoder float. It must also keep the existing malformed-text quarantine tests. HT06 is the only deliberately red source-free test identified by this audit.

### EVS 2008

The court must preserve exact MR set names, ordered members, aliases/overlaps, negative missing vocabulary scope, and v372's bounded unresolved state. A `-4` code in one admitted question/country context is not a license to classify every physical `-4` in the source as generic NOT_ASKED/IAP.

### WVS Wave 1

The court must combine S007 raw/display separation, user/system missing distinction, all-system retention, and the 13-carrier no-default law in one compound test. This catches adapters that individually preserve each field but later choose semantics from display width, missingness incidence, or a weight label.

### Latinobarometro 2011

The court must include the P1ST layer-boundary fixture and the WT ordinal convention. The exact source-local variable identity is source SHA + exact variable name + generic decoder ordinal; a packet's zero-based reporting ordinal is documentary evidence, not a substitute for the decoder slot convention.

## Execution boundary

These tests are specifications only in this lane. They were **not executed**. No raw source is needed to author them, and introducing a raw survey carrier into this return would violate the commission.
