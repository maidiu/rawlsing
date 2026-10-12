# PYAT HQ282 N04 — Method coverage and owner gaps

## B5 state-changing methods

### WRAPPED by C02J overlay (8 methods)

| Method | Overlay check | Coverage |
|---|---|---|
| `stage_release` | Resolve registered release, repository identity/replay/revocation checks and presented-field comparison | Full |
| `stage_protocol` | Converts protocol, same subject check | Full |
| `register_product` | Registry, then full subject check if staged subject exists | Full |
| `publish_product` | Registry, then full subject check if staged subject exists | Full (event kwargs unchecked) |
| `record_recertification` | Registry lookup only | PARTIAL (no event/authority check) |
| `select_current` | Registry and full subject check when present | Full |
| `declare_no_current` | Registry lookup only if explicit `subject_release_ref` supplied | PARTIAL (omitted subject argument permits bypass) |
| `from_checkpoint` | Accepted restore, then `verify_checkpoint_subject` | CORRECTED (was defective) |

### UNWRAPPED by C02J overlay (9 methods)

| Method | Owner checks | Gap |
|---|---|---|
| `supersede_current` | Owner checks and internal event/selection helpers | No overlay routing |
| `withdraw_product` | Owner checks and internal event/selection helpers | No overlay routing (executed successfully without verifier) |
| `declare_invalidation` | Owner checks and internal event/selection helpers | No overlay routing |
| `record_rebuild_eligibility` | Owner checks and internal event/selection helpers | No overlay routing |
| `link_rebuild` | Owner checks and internal event/selection helpers | No overlay routing |
| `record_cache_materialized` | Owner checks and internal event/selection helpers | No overlay routing |
| `record_cache_dropped` | Owner checks and internal event/selection helpers | No overlay routing |
| `attest_gc_eligibility` | Owner checks and internal event/selection helpers | No overlay routing |
| `record_payload_gc` | Owner checks and internal event/selection helpers | No overlay routing |

### PARTIAL coverage (2 methods)

| Method | Issue |
|---|---|
| `declare_no_current` | Only checked if `subject_release_ref` supplied; omitted argument permits event and selection-state change without a registered verifier |
| `record_recertification` | Registry lookup only; substituted event refs accepted; revoked release recertifies |

## M2 state-changing methods

### WRAPPED by C02J overlay (2 methods)

| Method | Overlay check |
|---|---|
| `register_producer_subject` | Verifier for repository |
| `constitute_release` | Verifier for repository |

### UNWRAPPED by C02J overlay (8 methods)

| Method | Gap |
|---|---|
| `M2Repository.register_subject` | Direct foreign-repository registration executed successfully |
| `M2Repository.register_closure` | No overlay routing |
| `M2Repository.register_release` | No overlay routing |
| `M2Repository.register_representation` | No overlay routing |
| `M2Repository.register_binding` | No overlay routing |
| `constitute_closure` | No overlay routing |
| `register_representation` | No overlay routing |
| `publish_binding` | No overlay routing |

## Which checks actually execute vs require external decision

| Check | Executes now | Requires external decision |
|---|---|---|
| Release identity | Yes (registry lookup) | No |
| Subject authentication | Yes (frozen expectation comparison) | No |
| Revocation | Yes (constructor-supplied sets) | Live revocation source |
| Replay grade | Yes (closure metadata) | Independent replay re-execution |
| Event authority | No (constructor-supplied refs) | Event issuance authority |
| Permission entitlement | No (self-declared ceiling) | Independent permission issuer |
| Expiry/as-of | No (not implemented) | Expiry policy definition |
| Concurrency | No (not demonstrated) | Concurrency correctness |

## Process-local vs principal isolation

The C02J overlay is a process-local monkey-patch layer, not a Python principal isolation boundary. Imports saved before monkey-patching can retain original Python callables. This is documented as a known limitation.
