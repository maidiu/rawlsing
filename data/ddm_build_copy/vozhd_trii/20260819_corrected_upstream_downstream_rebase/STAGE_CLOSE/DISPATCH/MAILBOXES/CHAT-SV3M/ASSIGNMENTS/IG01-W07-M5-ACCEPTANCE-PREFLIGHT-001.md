# IG01-W07-M5-ACCEPTANCE-PREFLIGHT-001

Worker #7 — `CHAT-SV3M` — most recent submitting agent `M5_FINAL` -> new agent `IG_M5_ACCEPTANCE_PREFLIGHT`.

Worker class: **SEAM PREFLIGHT SPECIALIST** (non-dispositive).

## Mission
Prepare the exact acceptance/test/oracle package for the future IG-M5 runtime implementation while M4 is being built. Do not implement M5 runtime and do not predict or fabricate the actual M4 runtime API.

Branch: `agent/vozhd-trii-ig-m5-acceptance-preflight`
Branch base: `f67c09948310fac9b48bcc4a223358fc6f590b94`
Frozen M5 semantic head: `54f163b38fb0589327ea7b50fd98b537d7d91831`
Frozen whole-machine reclosure: `c4a3524f54af368a67ca50ccc85f5d5dca3d803b`

## Write scope
Write only under:
`data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/IMPLEMENTATION_GATE/IG_M5_ACCEPTANCE_PREFLIGHT/**`

Governance/test-spec artifacts only. No executable runtime/test code, no `rawlsing_next/**` writes.

## Burden
Freeze the future M5 acceptance oracle for deterministic exact V558 closure resolution to an actual runtime `ResolvedStructuralContext`; exact stale/hash/ambiguity/missing failures; no RSC fabrication; repository/persistence/index/snapshot nonsemanticity; exact currentness; prospective refresh without rewriting historical receipts; RSC remains distinct from V3EmpiricalPossibilityInput and ActorCausalState; no prior->psyche shortcut.

Define the minimum exact M4 interface facts M5 must consume, but leave concrete function/class names `UNBOUND_UNTIL_ACCEPTED_M4_RUNTIME` where M4 has not yet returned. Do not invent an API.

Required outputs: `RESULT.md`, `RESULT.json`, `M5_ACCEPTANCE_ORACLE.md`, `M5_HOSTILE_FIXTURES.json`, `M4_TO_M5_RUNTIME_BINDING_REQUIREMENTS.json`.

Return token: `IG_M5_ACCEPTANCE_PREFLIGHT_COMPLETE` or a bounded conflict token.