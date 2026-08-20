# IG01-W10-M4-SIDELINE-IMPLEMENT-001

Worker #10 — `CHAT-S5578C` — most recent submitting agent `M4_FINAL` -> new agent `IG_M4_SIDELINE_IMPLEMENTATION`.

Worker class: **SUB-VOZHD**.

## Mission
Implement the frozen M4 V557 publication-governance / V558 immutable-repository seam as clean sideline runtime, cumulatively on accepted M3.

Exact branch: `agent/vozhd-trii-ig-m4-publication-repository`
Exact branch base: `f67c09948310fac9b48bcc4a223358fc6f590b94`
Frozen M4 semantic head: `988fa8abe755eee636e52a6b6eb09072b5a0f111`
Frozen whole-machine reclosure: `c4a3524f54af368a67ca50ccc85f5d5dca3d803b`
Sideline law: new runtime/tests only under `rawlsing_next/**`; no runtime imports from `data/ddm_build*` or `data/ddm_build_copy*`.

## Exact write allowlist
- `rawlsing_next/m4_v557_v558_publication_repository.py`
- `rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`

No other writes.

## Binding behavior
Preserve V557 and V558 as logically distinct authorities. V557 owns publication/use governance; V558 owns immutable repository/resolution. Preserve exact producer identity and typed state for M1/M2/M3 objects; enforce `resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`; locator/index/readiness/provenance never grants permission; V556 role/order/cardinality/multiplicity survive repository closure; no fuzzy/latest/raw-stage/network repair; standalone closure is exact; no source-composition authority may be inferred from co-location/provenance; no RSC fabrication; no actor/persona/phenomenology/render semantics.

The direct M1/M2 publication paths and M3 higher-order path must coexist without filler or re-identification.

## Required tests
Hostile tests must cover permission nonwidening, V557/V558 noncollapse, producer identity preservation, direct M1/M2 publication, M3 structure preservation, exact immutable closure/resolution, stale/hash/locator failure, standalone closure positive+negative deps, provenance nonauthority, and rejection of actor/V3/V2 objects from the structural repository.

No deployment, source retirement, semantic-contract changes, or legacy runtime edits.
