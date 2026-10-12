# A04SR — v2 identity and the true-oracle adapter question

## Identity kinds and preimages
| kind | v2 | A05 | A04 | interoperable |
|---|---|---|---|---|
| semantic operation key | `{kind, semantic_op_class, semantic_roles, target, condition_order, measure_kind, version}` | `{k:"OP",class,roles,target}` | `{kind:"ELIGIBLE_OPERATION",op_class,roles,target,condition_order,measure_kind,version}` | **NO** |
| expected work key | v2 preimage | `{k:"EXPECTED_WORK",item,op,authority,risk,topology,v}` | folds `consumer` | **NO** |
| schema token | `HQ280_PV3_A04S_CANONICAL_V2@1.0.0` | `HQ280_PV3_A05_EXPECTED_WORK@1.0.0` | `HQ280_PV3_A04_EXPECTED_WORK@1.0.0` | three distinct tokens |

v2 correctly stops reusing A05's token — an improvement in honesty over A04, which falsely declared `A05_COMPATIBLE_SCHEMA_VERSION`. But a distinct token plus a **shape-preserving copy** is a translation, not an interoperability bridge.

## Adapter verdict
`v2_to_a05_universe()` output is A05-*shaped* but carries **v2 keys under a v2 schema**. A05's oracle recomputes its own keys and compares sets, so translated keys can never satisfy it. **A true oracle adapter must map each v2 semantic key to an explicitly derived, verified, injective A05-scope key** (or the oracle must be re-versioned to consume v2 natively). Copying a key into a foreign slot is not a mapping.

## Non-injectivity
`SEMANTIC_TO_DISPATCH` is **3→1** onto `I03_UNARY_OR_JOINT_QUERY`; `fail_closed_on_multiple` is **false**. The commission requires failing closed when several operations map onto one job. Not met.
