# PYAT HQ282 N04R — Recommended next change

## Minimum owner changes (source-free interface defects)

1. **Fix checkpoint event replay**: Modify `from_checkpoint` to replay event transitions and derive state, then compare with saved claims. This closes the altered-state and truncated-history gaps.

2. **Wrap remaining B5 methods**: Route `supersede_current`, `withdraw_product`, `declare_invalidation`, `record_rebuild_eligibility`, `link_rebuild`, `record_cache_materialized`, `record_cache_dropped`, `attest_gc_eligibility`, `record_payload_gc` through the overlay.

3. **Wrap remaining M2 methods**: Route `M2Repository.register_subject`, `M2Repository.register_closure`, `M2Repository.register_release`, `M2Repository.register_representation`, `M2Repository.register_binding`, `constitute_closure`, `register_representation`, `publish_binding` through the overlay.

4. **Fix `declare_no_current` partial coverage**: Require `subject_release_ref` or route through overlay unconditionally.

5. **Fix `record_recertification` partial coverage**: Add event/authority check, not just registry lookup.

## Competent authority decisions (non-code)

1. **Independent event authority**: Define who can issue event references. Current constructor-supplied refs are unproved.

2. **Independent permission entitlement**: Define who can validate permission ceilings. Current self-declared ceilings are unproved.

3. **Revocation authority**: Define live revocation source and expiry/as-of policy.

4. **Concurrent mutation/verification**: Define concurrency correctness requirements.

5. **Replay completeness**: Establish replay completeness independently of stored labels.

## Scope boundaries

These recommendations are for the **bounded source-free** interface layer only. They do NOT authorize:
- Production publication
- External producer identity
- Event/revocation issuers
- G0b, N9, or V3
- Scientific acceptance

## Priority

1. **High**: Checkpoint event replay (closes altered-state and truncated-history gaps)
2. **High**: Wrap remaining B5 methods (closes unwrapped mutation paths)
3. **Medium**: Fix `declare_no_current` and `record_recertification` partial coverage
4. **Medium**: Wrap remaining M2 methods
5. **Low**: Competent authority decisions (separate work)
