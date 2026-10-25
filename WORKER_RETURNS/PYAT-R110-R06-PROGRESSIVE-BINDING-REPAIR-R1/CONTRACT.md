# R110 pre-code contract — identity, revocation, N10E binding; world-N10W stop

Status: frozen before the R110 code commit. Candidate
`22280a3f43e751bab1bbebe0a9d8c601b3160120`; review
`e38a6a8c07ea6535a0d4de38053c15e4278934d7`; branch
`agent/opencode-pyat-r110-r06-progressive-binding-repair-r1`. Only the two R06
code paths and this return are written.

## Repairs

1. **World/prefix identity.** `configure_progressive_world_context` derives
   universe/release/risk/repository identity from every actual producer prefix,
   requires all prefixes to agree, and requires the world empirical universe,
   release, risk and repository to agree. A mismatch returns a registered
   invalid context; `progressive_world_view` refuses
   `PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH` before world serving.
2. **Empirical revocation.** The P41 world block now carries the selected
   snapshot `empirical` state. `StructuralService.possibilities` reads the
   actual empirical state. A revoked empirical scope yields
   `PROGRESSIVE_WORLD_UNAVAILABLE` /
   `WORLD_EMPIRICAL_REVOKED_OR_UNAVAILABLE`; a clean context restores the same
   view. Field revocation remains.
3. **Actual N10E consumer binding.** Each prefix invokes the actual
   `evaluate_positioned_subject_possibility` on the actual computed evidence.
   Its result hash must equal the producer/extension consumer hash. The P41
   provider emits actual `evaluate_positioned_subject_possibility` trace entries,
   so `n10w.positioned_consumptions` carries the real N10E hashes and
   `LIVE_TRACE`, not cached null placeholders.

## Held dependent change

The pinned P41 receiver does **not** pass world content into
`provider.progressive` or the `n10w` update identity. At
`f27d1101…:runtime/p41_service.py`, `P41Service.progressive` lines 133 and
149–171 compute `steps` from target/ordered conditions and `n9_world`
separately; `n10w` contains only target/ordered identities. Therefore T0/T1
world changes alter the N9/E04 structural sibling but not N10W values. This
cannot be repaired inside the two R06 paths without editing P41. The exact
smallest owner amendment is to extend `P41Service.progressive`/its provider
call with the selected world/snapshot binding (or add a world-conditioned
provider contract) and include that binding in `n10w`/the consuming assertion,
without inventing probability reweighting or changing N9/E04 semantics.

This return does **not** claim N10W world consumption. It preserves the real N9
world dependency and actual N10E/N10W positive, and reports the exact
indispensable P41 amendment.

## Preserved controls

Actual condition-value mutation, second target/prefix shape, minority/zero
retention, T0/T1 world routes, field revocation/restore, empirical
revocation/restore, cold replay, pinned P41, sourcefree scope, actor
`NOT_TOUCHED`, and prior R06 boundary controls remain. No original source,
science, actor, R09/CI/prod, N11/N12, Sorok/J52/W52 expansion.
