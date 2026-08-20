# IG01-W07-M5-SIDELINE-IMPLEMENT-001

Worker #7 — `CHAT-SV3M`

Class: **SUB-VOZHD**

Most recent submitting agent: `IG_M5_ACCEPTANCE_PREFLIGHT`
New agent: `IG_M5_SIDELINE_IMPLEMENTATION`

Mission branch: `agent/vozhd-trii-ig-m5-runtime-rsc-peer-prior`
Exact branch base: `83694e95e853651c3a34ea1c11008521ba67f072` (accepted IG-M4 runtime head)

## Mission
Implement the frozen IG-M5 runtime RSC / V3 structural peer-prior seam on the clean sideline.

Write ONLY:
- `rawlsing_next/m5_runtime_rsc_peer_prior.py`
- `rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py`

Do not modify any `data/ddm_build/**` or `data/ddm_build_copy/**` runtime/test file. Do not import legacy runtime machinery. Governance artifacts are read-only evidence.

## Binding law
Consume the accepted M4 runtime module `rawlsing_next/m4_v557_v558_publication_repository.py` exactly as implemented at the branch base. Bind concrete M4 symbols from the accepted runtime; do not predict or rename them by analogy.

M4 resolves exact immutable V558 closure and returns `ResolutionResult` / selection and resolution receipts. M4 intentionally does NOT fabricate a `ResolvedStructuralContext`; `ResolutionResult.resolved_structural_context` remains `None`.

IG-M5 owns the separately governed runtime materialization/validation step that may produce an actual `ResolvedStructuralContext` ONLY from exact accepted M4 resolution evidence plus exact M5-owned authority/currentness inputs. "No RSC fabrication" means no invented context from missing, stale, partial, ambiguous, denied, corrupt, permission-invalid, or otherwise insufficient inputs. It does NOT mean a prebuilt RSC must already have been emitted by M4.

## Frozen requirements
- preserve `ResolvedStructuralContext != V3EmpiricalPossibilityInput != ActorCausalState`;
- repository/index/locator/snapshot/persistence are evidence/infrastructure only, never semantic permission;
- every selected root and interpretation-critical dependency must satisfy `resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`;
- missing/stale/ambiguous/corrupt/hash-mismatched/partial required M4 resolution fails closed;
- currentness must be explicit and exact; immutability alone is not currentness;
- refresh is prospective only and must not rewrite historical receipts;
- structural and empirical peer currentness remain independent;
- RSC availability/ACTIVE_CAUSAL eligibility does not mutate actor state;
- no prior -> generated position, memory, belief, knowledge, relationship, action, response, persona, voice;
- no RSC -> PSEPF synthesis;
- provenance never grants source composition/pooling/linkage/estimand authority;
- exact historical receipts replay deterministically; lawful different post-branch histories may diverge later.

Use the completed non-dispositive preflight at `IMPLEMENTATION_GATE/IG_M5_ACCEPTANCE_PREFLIGHT/` as an acceptance oracle only. Where its phrase `may_be_fabricated_by_m5:false` could be read as requiring M4 to emit a prebuilt RSC, the governing interpretation above controls: M5 may materialize an RSC under exact M5 authority from complete M4 evidence, but may never invent missing semantics or currentness.

## Tests
Include hostile tests for incomplete/partial/denied resolution, hash mismatch, stale currentness, permission widening, repository/index-as-authority, provenance composition, RSC/EPI/ActorCausalState collapse, actor-state mutation, historical receipt rewrite, deterministic replay, and explicit currentness/refresh behavior.

No M6 implementation. No situated phenomenology/disclosure implementation. No deployment/cutover/source retirement.