# Typed-state and scientific error conservation

## Repaired boundary

The consumer first verifies the relation's committed self-hash. That proves only self-consistency, not external issuer authenticity. It then validates both top-level risk counts as exact nonnegative integers. A producer-blocked or non-`SUPPORTED` relation is handled before any empty-profile classification. For a supported populated profile, it enforces two ordered conditioner states and two ordered target states, exact native role labels, exact nonnegative counts, cell-state/count consistency, per-condition denominator equality, and total support no greater than eligible joint risk.

| Input condition | Decision | Separation class | Downstream value |
|---|---|---|---:|
| Wrong object type | `CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION` | `None` | false |
| Identity mismatch | `CONSUMER_RELATION_IDENTITY_MISMATCH` | `None` | false |
| Negative/coerced count, impossible cell/profile/denominator/risk | `CONSUMER_RELATION_INTEGRITY_REJECTED` | `None` | false |
| `MISSING_TARGET_STATE`, `UNRESOLVED_TARGET_STATE`, `NONRESPONSE` | `CONSUMER_PRODUCER_TYPED_STATE_BLOCKING` | `None` | false |
| Typed `ZERO_SUPPORT` | `CONSUMER_PRODUCER_TYPED_STATE_BLOCKING` | `UNDETERMINED_ZERO_SUPPORT_RISK` | false |
| `SUPPORTED`, empty profile | `RESPONSE_INPUTS_VALID_EMPTY` | `None` | false |
| `SUPPORTED`, eligible risk 0 and support 0 | `PAIR_SUPPORT_SIGNATURE_COMPUTED` | `UNDETERMINED_NO_ELIGIBLE_RISK` | true, qualified |
| `SUPPORTED`, eligible risk positive and support 0 | `PAIR_SUPPORT_SIGNATURE_COMPUTED` | `UNDETERMINED_ZERO_SUPPORT_RISK` | true, qualified |
| `SUPPORTED`, positive support but a conditioner level absent | `PAIR_SUPPORT_SIGNATURE_COMPUTED` | `UNDETERMINED_NO_ELIGIBLE_RISK` | true, qualified |

The two computed undetermined classes retain a result value because the input is internally consistent and the class itself is the bounded result. Neither class says anything about a human actor. A typed producer block yields no downstream value even when it names the zero-support class.

GF1F100 is retained as historical regression evidence: the original consumer passes all 100. Four GF1F tests fail under the repaired semantics: `test_universe_class_and_derived_fields[0000]`, `test_named_cases[zero_supported_risk]`, `test_missing_suppressed_relation_is_empty_response`, and `test_cold_process_consumer_replay_bit_identical`. The first two expect the former inverted class; the third expects a blocking missing state to be valid empty; the fourth expects the old class histogram. GF1G's independently preregistered oracle and the explicit GF1H commission require the corrected readings. GF1I's two “consumer absent” failures also remain historical; the consumer is physically present and imports.

This patch does not impose a new equality between the count of risk-member references and the numerical eligible risk total: those references are owner lineage and may have a different cardinality grain. It enforces the source-native numerical equalities expressible from the actual 2×2 projection and bounds supported observations by eligible risk.
