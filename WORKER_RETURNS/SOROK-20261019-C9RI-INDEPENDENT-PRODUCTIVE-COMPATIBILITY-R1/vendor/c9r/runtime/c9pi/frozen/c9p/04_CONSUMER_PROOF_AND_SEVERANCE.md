# 04 — Consumer proof and dependency severance (T3)

**Status: `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` for all six named edges.** Every integration claim is backed by a named existing downstream consumer that actually reads the source. Each claim turns the SAME named assertion RED when the dependency is severed, in a separate fresh process, by its own assertion — not by an import error, fixture crash or unrelated exception.

## Pre-registered named assertions

Six named assertions were frozen before execution. Each names one edge in the candidate chain:

| Named assertion | Claimed edge | Downstream consumer |
|---|---|---|
| `test_later_action_consumer_reads_committed_target_state` | committed target_state → consumer read | `LaterActionConsumer.read_target` via `read_target_for_later_action` |
| `test_response_lookup_consumes_exact_rule_registry_entry` | rule registry entry → lookup key dereference | `lookup_rule` consumed by `evaluate_response` |
| `test_target_decision_consumes_independent_permission` | TargetPermission → CREATE branch | `evaluate_target` permission validation |
| `test_conditioning_readset_binds_person_world_sources` | ConditioningSource → readset append | `ConditioningView.readset_refs` consumed by `evaluate_response` |
| `test_action_admission_binds_performed_action_receipt` | owner receipt → action admission | `admit_performed_action` receipt binding |
| `test_transaction_readset_binds_admitted_event_witness` | admitted occurrence → receipt identity | `CommitReceipt` joint transaction id and readset |

## Severance results (separate processes)

The runner `severance/run_severance.py` executes each named assertion in its own fresh Python process in the positive baseline, then again in another fresh process with the exact source-code fault applied:

| Claim | Baseline | Fault probe | Proof grade |
|---|---|---|---|
| `C9P_LATER_ACTION_CONSUMER_READS_COMMITTED_TARGET_STATE` | PASS | `TARGET_ASSERTION_RED` | `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` |
| `C9P_RESPONSE_LOOKUP_CONSUMES_EXACT_RULE_REGISTRY_ENTRY` | PASS | `TARGET_ASSERTION_RED` | `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` |
| `C9P_TARGET_DECISION_CONSUMES_INDEPENDENT_PERMISSION` | PASS | `TARGET_ASSERTION_RED` | `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` |
| `C9P_CONDITIONING_READSET_BINDS_PERSON_WORLD_SOURCES` | PASS | `TARGET_ASSERTION_RED` | `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` |
| `C9P_ACTION_ADMISSION_BINDS_PERFORMED_ACTION_RECEIPT` | PASS | `TARGET_ASSERTION_RED` | `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` |
| `C9P_TRANSACTION_READSET_BINDS_ADMITTED_EVENT_WITNESS` | PASS | `TARGET_ASSERTION_RED` | `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` |

Receipt: `evidence/severance_receipt.json`.

## Proof-integrity gate witnesses

Two `.proof.json` contracts are registered beside their test modules, as required by the shared proof-integrity law:

- `tests/test_severance_witnesses.py.proof.json` — 6 claims, all `BOUNDED_MUTATION_DETECTED`
- `tests/test_later_action_consumer.py.proof.json` — 2 claims, all `BOUNDED_MUTATION_DETECTED`

Receipts: `evidence/proof_witness_severance.json`, `evidence/proof_witness_consumer.json`.

## Exact source-code faults

Each fault severs exactly one upstream edge by a single unique source-text substitution in an implementation file (never in a test):

| Fault path | Old (unique) | New | Edge severed |
|---|---|---|---|
| `candidate/later_action.py` | `record, state_hash = consumer.read_target(store, middle_state_id, as_of)` | `record, state_hash = None, ""` | committed state → consumer read |
| `candidate/response_rules.py` | `entry = registry.rules.get(key)` | `entry = None` | registry entry → lookup |
| `candidate/target_rules.py` | `if not _valid(permission):` | `if True:` | permission → CREATE |
| `candidate/conditioning.py` | `readset.append(source_ref)` | `readset.append("SEVERED_SOURCE_REF")` | source → readset |
| `candidate/action_admission.py` | `if owner_receipt is None:` | `if True:` | owner receipt → admission |
| `candidate/transaction.py` | `joint_transaction_id=receipt["hash"],` | `joint_transaction_id="SEVERED",` | occurrence → receipt identity |

## What this proves and does not prove

**Proves:** each named consumer actually reads the source; the dependency is genuine; severing it kills the same named assertion by its own assertion. The candidate transport chain has real source→consumer edges.

**Does not prove:** native C9 person×event positive. The TEST_ONLY chain uses explicitly typed test-only rules and permissions. The release gate stays `C9_NATIVE_POSITIVE_HELD`. `EXECUTED_GREEN` is recorded separately from native science and actor reality.
