# A04T — Versioned V2 key grammar and A05 migration map

```json
{
  "a05_migration": {
    "full_key_equality": "NONREPRESENTABLE_ALWAYS (different kind tags, preimage shapes, versions)",
    "nonrepresentable_where": [
      "BOUNDED_DISCOVERY (no A05 counterpart)",
      "GOVERNED_WEIGHTED (no A05 distinction; coercion would collide)",
      "non-empty condition_order (no A05 field; coercion would collapse q(C|A)/q(C|A,B))"
    ],
    "old_oracle_status": "valid for its own contract only; never pretended v2-compatible",
    "set_verdict_this_fixture": "NONREPRESENTABLE__SHARED_A05_TRIPLE_WOULD_COLLIDE (Y-RAW/Y-WEIGHTED)",
    "triple_mapping": "(semantic_op_class, roles, target) correspondence where grammar overlaps"
  },
  "accepted_expected_schema": "HQ280_PV3_A04S_CANONICAL_V2@1.0.0",
  "consumer_rule": "structural join on purported receipts; actual_consumer_court always HOLD in this scope",
  "custodian_rule": "structural consistency checked; EXTERNAL_CUSTODIAN_ISSUER_HOLD unconditional; timestamps recorded never trusted",
  "dispatch_classes": [
    "I03_UNARY_OR_JOINT_QUERY",
    "I05_BOUNDED_DISCOVERY"
  ],
  "identity_kinds": [
    {
      "inputs": [
        "source",
        "wave",
        "item",
        "form",
        "slot",
        "version"
      ],
      "kind": "V2_DOCUMENTARY_ITEM"
    },
    {
      "inputs": [
        "semantic_op_class",
        "roles",
        "target",
        "condition_order",
        "measure_kind",
        "version"
      ],
      "kind": "V2_SEMANTIC_OPERATION"
    },
    {
      "inputs": [
        "dispatch_class",
        "roles",
        "target",
        "condition_order",
        "measure_kind",
        "version"
      ],
      "kind": "V2_DISPATCH_OPERATION"
    },
    {
      "excludes": [
        "consumer"
      ],
      "inputs": [
        "item_key",
        "semantic_operation_key",
        "dispatch_operation_key",
        "source_identity",
        "authority_ref",
        "risk_identity",
        "topology_identity",
        "version"
      ],
      "kind": "V2_EXPECTED_WORK"
    },
    {
      "inputs": [
        "expected_work_key",
        "consumer",
        "version"
      ],
      "kind": "V2_CONSUMER_OBLIGATION"
    },
    {
      "inputs": [
        "expected_work_key",
        "attempt_index",
        "version"
      ],
      "kind": "V2_EXECUTION_ATTEMPT"
    },
    {
      "inputs": [
        "expected_work_key",
        "result_type",
        "value",
        "version"
      ],
      "kind": "V2_OUTPUT_IDENTITY"
    }
  ],
  "independence_rule": "stdlib-only module; recompute-and-compare from separately authored raw fields; supplied keys checked never trusted; candidate key constructors never invoked",
  "join_rule": "produced jobs match expectations by exact owner dispatch-ref equality AND by producer-claimed expectation mapping cross-checked against recomputed refs",
  "schema": "HQ280_PV3_A04T_VERSIONED_V2_KEY_GRAMMAR_AND_MAPPING@1.0.0",
  "semantic_operation_classes": [
    "BOUNDED_DISCOVERY",
    "NONSCALAR_TOPOLOGY_PRESERVATION",
    "PAIR_RESPONSE_COTRAVEL",
    "UNARY_DISTRIBUTION"
  ],
  "semantic_to_dispatch": {
    "BOUNDED_DISCOVERY": "I05_BOUNDED_DISCOVERY",
    "NONSCALAR_TOPOLOGY_PRESERVATION": "I03_UNARY_OR_JOINT_QUERY",
    "PAIR_RESPONSE_COTRAVEL": "I03_UNARY_OR_JOINT_QUERY",
    "UNARY_DISTRIBUTION": "I03_UNARY_OR_JOINT_QUERY"
  },
  "verifier_contract": "PYAT_HQ280_A04T_V2_INDEPENDENT_VERIFIER_CANDIDATE@1.0.0",
  "verifier_schema": "HQ280_PV3_A04T_V2_VERIFIER@1.0.0"
}
```
