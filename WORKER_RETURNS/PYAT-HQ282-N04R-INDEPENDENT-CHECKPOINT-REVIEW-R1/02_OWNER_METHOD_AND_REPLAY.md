# PYAT HQ282 N04R — Owner method and replay analysis

## Reachable B5 methods (independently tested)

| Method | Overlay coverage | Independently tested | Result |
|---|---|---|---|
| `stage_release` | WRAPPED | No (covered by owner tests) | — |
| `stage_protocol` | WRAPPED | No (covered by owner tests) | — |
| `register_product` | WRAPPED | No (covered by owner tests) | — |
| `publish_product` | WRAPPED | No (covered by owner tests) | — |
| `record_recertification` | PARTIAL | No | — |
| `select_current` | WRAPPED | Yes (independent reviewer) | PASS |
| `declare_no_current` | PARTIAL | No | — |
| `from_checkpoint` | WRAPPED (corrected) | Yes (independent reviewer) | PASS |
| `supersede_current` | UNWRAPPED | Yes (independent reviewer) | PASS (reachable without verifier) |
| `withdraw_product` | UNWRAPPED | Yes (independent reviewer) | PASS (reachable without verifier) |
| `declare_invalidation` | UNWRAPPED | Yes (independent reviewer) | PASS (reachable without verifier) |
| `record_rebuild_eligibility` | UNWRAPPED | No | — |
| `link_rebuild` | UNWRAPPED | No | — |
| `record_cache_materialized` | UNWRAPPED | No | — |
| `record_cache_dropped` | UNWRAPPED | No | — |
| `attest_gc_eligibility` | UNWRAPPED | No | — |
| `record_payload_gc` | UNWRAPPED | No | — |

## Reachable M2 methods (independently tested)

| Method | Overlay coverage | Independently tested | Result |
|---|---|---|---|
| `register_producer_subject` | WRAPPED | No (covered by owner tests) | — |
| `constitute_release` | WRAPPED | No (covered by owner tests) | — |
| `M2Repository.register_subject` | UNWRAPPED | No | — |
| `M2Repository.register_closure` | UNWRAPPED | No | — |
| `M2Repository.register_release` | UNWRAPPED | No | — |
| `M2Repository.register_representation` | UNWRAPPED | No | — |
| `M2Repository.register_binding` | UNWRAPPED | No | — |
| `constitute_closure` | UNWRAPPED | No | — |
| `register_representation` | UNWRAPPED | No | — |
| `publish_binding` | UNWRAPPED | No | — |

## Exact unresolved source-free defects

1. **Checkpoint restores saved state without replaying events**: The `from_checkpoint` method restores `_publication`, `_validity`, `_selection_state_kind` etc. from the checkpoint payload without replaying event transitions to derive and compare state. This means altered publication state and truncated history are accepted by the raw executor.

2. **Unwrapped B5/M2 methods**: 9 B5 + 8 M2 state-changing methods are not covered by the C02J overlay. Representative examples (`withdraw_product`, `declare_invalidation`, `supersede_current`) are confirmed reachable without a verifier.

3. **`declare_no_current` partial coverage**: Only checked if `subject_release_ref` supplied; omitted argument permits event and selection-state change without a registered verifier.

4. **`record_recertification` partial coverage**: Registry lookup only; substituted event refs accepted; revoked release recertifies.

5. **No independent event authority**: Event references are constructor-supplied; no issuer authorization check.

6. **No independent permission entitlement**: Permission ceiling is self-declared in custody.

7. **No expiry/as-of policy**: No expiry timestamp, live revocation source, effective interval or as-of policy exists.

8. **Process-local monkey-patch**: The overlay is a process-local monkey-patch layer, not a Python principal isolation boundary.
