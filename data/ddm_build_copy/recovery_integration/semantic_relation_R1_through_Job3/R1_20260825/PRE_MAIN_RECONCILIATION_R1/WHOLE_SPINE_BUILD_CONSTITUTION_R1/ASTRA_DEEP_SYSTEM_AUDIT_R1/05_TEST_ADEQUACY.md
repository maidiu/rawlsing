# Test adequacy and bounded observations

**298 accepted focused tests passed; 33 active focused tests passed.** The counts measure the selected suites, not acceptance and not whole-system coverage. The new checks show precisely how important propositions can remain false while those suites are green.

## Execution record

Environment: Python 3.12.13; pytest 9.1.1 installed only in the scratch test-dependency directory; external pytest plugins disabled; cache provider disabled. No production files changed. Initial execution lacked pytest; after dependency installation and materializing only the required import closure, both bounded runs completed.

Accepted run: cwd `accepted`, PYTHONPATH contains `test_dependencies` and the accepted mirror. Command: `python -m pytest -q -p no:cacheprovider rawlsing_next/tests --disable-warnings`, with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. That local tests directory contains only the sixteen modules listed in coverage. Result: **298 passed in 1.16s**.

Active run: the accepted direct dependency mirror plus the seven relevant active files. Command: `python -m pytest -q -p no:cacheprovider active_runtime/rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py active_runtime/rawlsing_next/tests/test_pre553_repo_native_seal.py active_runtime/rawlsing_next/tests/test_pre553_i03_scale_equivalence_repair.py --disable-warnings`, with that overlay and test dependencies on PYTHONPATH and external plugins disabled. Result: **33 passed in 0.35s**. These small test durations are not a benchmark of real current-source execution.

## Which propositions are and are not proved

| Existing proof surface | Proposition it does prove | Proposition left unproved |
|---|---|---|
| [same marginals/different joint; storage-order replay](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_empirical_query.py) | Properly constructed immutable source differences affect exact joint facts; storage order is not semantic incidence. | Post-seal mutation through a public nested alias cannot change incidence under old source refs (ASTRA-001). |
| [positive authority exact family/scope validator](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_empirical_objects_authority.py) | The dedicated validator rejects inapplicable scope. | Every shared I03 operation invokes an equivalent fitness check (ASTRA-002). |
| [lawful current I03 fixture and frozen literal tests](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py) | The frozen builder's scope/risk/order rules work against a small fixture and separately pinned literals. | A small fixture with monkeypatched size/risk is the actual 19,210-member execution, or all generic callers must pass through that builder. |
| [no caller permission parameter; wrong authority/use shape](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py) | The governed wrapper derives adopted permissions and rejects widening. | The separate exported relation adapter cannot accept caller-selected uses. Signature inspection alone cannot establish that (ASTRA-002). |
| [future real public-entry negatives](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py) | A synthetic/historical wrong current hash fails early. | A genuine ordinary current query can pass a later target comparison; an early failure cannot exercise it (ASTRA-003). |
| [synthetic ordinary full-chain test](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py) | The private bounded shape chain can reach exact structural context and the zero terminal. | The public current-object boundary accepts the genuine current pair; `_run` calls `_run_bounded_chain` rather than that public current gate. |
| [zero-positive and internal accepted-owner tests](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_psepf_zero_positive_guard.py) | Production accepted-positive registry is empty and the pure guard makes no positive transition. | Future stateful owner execution is source-bound, replay-safe, and correctly observed through real actor/ledger/cursor/RNG/scheduler state (ASTRA-004). |
| [negative closure and itemwise dependency permission](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_m4_v557_v558_publication_repository.py) | The ordinary builder and resolver enforce declared closure and noninheritance. | A later codec reconstructs the exact same validated dependency-role obligations (ASTRA-006). |

## Isolated contract checks and reproduction boundaries

No probe edited production source, changed a repository branch outside audit output, reran real current empirical execution, or introduced a positive owner. The fixture helpers named below are the exact committed helper implementations, not replacements for production constructors. Full observed result values are preserved here and in the machine summary.

**P1 — sealed source identity.** Use [_build_source; _query_authority; _branch_predicate; _query; _registry](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_empirical_query.py) to construct a valid sealed two-respondent, two-target source with cells (0,0) and (1,1). Execute the ordinary joint query. Read the same sealed release through exact resolution. Through the public `as_dict()['semantic_fields']` views of its two Q2 events, exchange the nested scoped-respondent reference dictionaries. Execute the same ordinary query again. The four cell counts move from `[1,0,0,1]` to `[0,1,1,0]`, both SUPPORTED, while release/event/query/provenance refs stay the same. Call `verify_public_object_integrity` separately: it rejects the stale body. No current GT2 fact is involved.

**P2 — independently inapplicable ALLOW authorities.** Construct two fresh canonical query authority snapshots from the same fixture helper. Keep kind, operation and ALLOW state valid. In one case, name only ReplayReceipt as the governed family. In the other, retain normal families but give an empty exact source scope. Recompute the declared authority body hash and ordinary canonical snapshot/query hashes. The dedicated positive validator refuses each. Ordinary shared I03 still emits SUPPORTED. These are independent single-dimension controls, not stale-hash or missing-object failures.

**P3 — exact current query representation.** Use the active manifest's `actual_query.constructor_semantic_projection`, extract its semantic_fields and call unmodified EmpiricalQuerySpec. Recompute and compare its ref to the committed current ref. Evaluate the active checker's component normalization and target tuple comparison. Dictionary targets differ from ExactRef components; converting both through exact_ref makes them equal. This reproduces a necessary-condition obstruction without claiming the full current fact or E2B run was executed.

```json
{
  "current_query_target_representation": {
    "candidate_harness_equality": false,
    "full_current_fact_constructed": false,
    "normalized_types": [
      "ExactRef",
      "ExactRef"
    ],
    "ordinary_query_constructor_verified": true,
    "query_hash": "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0",
    "semantic_exact_ref_equality": true,
    "target_types": [
      "dict",
      "dict"
    ]
  },
  "query_authority_scope_negative_controls": [
    {
      "authority_ref_hash_matches_declared_body": true,
      "direct_authority_validator": "object family not named by exact authority",
      "query_and_authority_hashes_valid": true,
      "query_execution_state": "SUPPORTED",
      "scope": "isolated synthetic source; one authority dimension is unfit",
      "variant": "family_only"
    },
    {
      "authority_ref_hash_matches_declared_body": true,
      "direct_authority_validator": "exact authority scope does not include source_universe_refs",
      "query_and_authority_hashes_valid": true,
      "query_execution_state": "SUPPORTED",
      "scope": "isolated synthetic source; one authority dimension is unfit",
      "variant": "source_scope_only"
    }
  ],
  "sealed_source_immutability": {
    "after_cells": [
      {
        "cell": [
          "0",
          "0"
        ],
        "n": 0
      },
      {
        "cell": [
          "0",
          "1"
        ],
        "n": 1
      },
      {
        "cell": [
          "1",
          "0"
        ],
        "n": 1
      },
      {
        "cell": [
          "1",
          "1"
        ],
        "n": 0
      }
    ],
    "after_state": "SUPPORTED",
    "before_cells": [
      {
        "cell": [
          "0",
          "0"
        ],
        "n": 1
      },
      {
        "cell": [
          "0",
          "1"
        ],
        "n": 0
      },
      {
        "cell": [
          "1",
          "0"
        ],
        "n": 0
      },
      {
        "cell": [
          "1",
          "1"
        ],
        "n": 1
      }
    ],
    "before_state": "SUPPORTED",
    "event_projection_hashes_stale": [
      true,
      true
    ],
    "event_refs_unchanged": true,
    "fact_identity_changed": true,
    "known_expected_fact_replay_would_detect": true,
    "query_ref_unchanged": true,
    "release_ref_unchanged": true,
    "same_provenance_refs": true,
    "scope": "isolated two-respondent synthetic sealed C11 release",
    "separate_carrier_integrity_check": "public object semantic projection/hash mismatch"
  }
}
```

**P4 — shared M4 permission boundary.** Construct the valid relation evaluation from [_evaluate](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py). The exported shared adapter accepts REVIEW and returns two objects bearing that producer use. The governed publication wrapper rejects the corresponding non-CONTEXT shape. The check stops before publication, resolution or V3.

**P5 — future guard binding and its present counterexample.** Use the existing [_accepted; _presentation; _request](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_psepf_zero_positive_guard.py) internal test-only registry fixtures. Two distinct source refs/hashes with otherwise identical inputs produce equal delegation decisions. Send the request to the production entry: it denies. No owner or state mutation occurs.

```json
{
  "relation_m4_boundary": {
    "relation_contract": "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0",
    "generic_adapter_producer_uses": [
      [
        "REVIEW"
      ],
      [
        "REVIEW"
      ]
    ],
    "governed_wrapper_result": "adopted GT2 path requires ALLOW_CONTEXT_ONLY",
    "production_v3_invoked": false,
    "scope": "existing synthetic relation fixture; REVIEW-only negative control"
  },
  "future_guard_binding": {
    "internal_test_registry_only": true,
    "decisions_equal_for_distinct_sources": true,
    "delegation_result": "DELEGATE_TO_ACCEPTED_OWNER",
    "public_production_outcome": "DENY_ZERO_EFFECT",
    "owner_executed": false,
    "state_mutations": false
  }
}
```

## Minimum proof additions after HQ disposition

For ASTRA-001, cover public alias mutation and same-ref replay, including a deep-freeze repair's canonical-byte compatibility. For ASTRA-002, place negative composition tests at shared operation entry, one invalid scope dimension at a time. For ASTRA-003, test ordinary current-query representation and later a genuine current full public entry; retain wrong-current negatives. For ASTRA-004, test the separately accepted stateful owner against real state and invocation identity when it exists. For ASTRA-006, one accepted codec roundtrip with required and negative dependencies is the next bounded proof.

Do not add more copies of the private shape chain or signature-only permission test as substitutes. Do not rerun expensive source production merely to re-prove deterministic ref conversion. The requested independent review was not duplicate execution.
