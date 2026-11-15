# VC4 C01 — TERMINAL PRODUCT & V3 CONSUMPTION AUDIT

Status: `PREPARED__NOT_LAUNCHED`
Branch: `agent/vozhd-chetiri-c01-v3-runtime-persistence`
Write scope: `.../VOZHD_CHETIRI_COMPILER_PERSISTENCE/returns/C01/`
Runtime writes: `FORBIDDEN`
Raw source probing: `FORBIDDEN`

## MISSION

Determine exactly what the finished Rawlsing application/V3 runtime must consume persistently, and separate those requirements from build-only empirical/compiler artifacts.

This is a backward terminal-demand audit, not a redesign.

## DEPENDENCIES

None beyond campaign launch and the common worker contract.

## ADDITIONAL READ-FIRST

Read accepted completion/implementation rulings for V553, V554, V555, V556, V557/V558, V3, V2 and seam integrity; current StructuralPriorRepository/ContextResolver/V3 runtime code only after accepted contracts establish intended behavior.

Inspect historical V550–V552/J only to identify producer functionality lineage feeding the closed chain, not to reopen it.

## EXACT PROCEDURE

1. Start at application/V2 and walk upstream through V3, ResolvedStructuralContext, V558, V557, V556, V555, V554, V553 and producer structural authority.
2. For every object family encountered, record producer, consumer, semantic owner, normal runtime access frequency, persistence requirement and provenance/replay role.
3. Separate intended architecture from current implementation residue.
4. Search specifically for any ordinary production path that reaches respondent/event-grain empirical data after structural publication.
5. If such a path exists, classify it as accepted architecture, implementation debt, audit/replay-only, or unresolved.
6. Identify which compiled products must be optimized for runtime speed/lightness because they directly serve V3/application.
7. Identify provenance objects that need not be in the hot runtime path but must remain reachable for audit/replay.
8. Apply the full 24-row terminal vision checksum.

## REQUIRED LEDGER COLUMNS

`object_family,producer_stage,semantic_owner,consumer_stage,ordinary_runtime_required,build_required,replay_required,audit_only,persistence_class,hot_path_latency_sensitive,rebuildable_from,invalidated_by,current_implementation_dependency,accepted_architecture_dependency,terminal_capabilities_protected,notes`

## MANDATORY QUESTIONS

- Does V3 ever need raw respondent/event incidence in ordinary runtime?
- Does V558 ContextResolver need empirical substrate after StructuralPriorRepository publication?
- Are any runtime empirical dependencies merely legacy implementation residue?
- What exactly is the first artifact family that crosses the build/runtime boundary?
- What runtime indexes/racks are genuinely justified by accepted consumption patterns?
- Can empirical carrier deletion leave ordinary runtime fully functional?
- What must remain reachable to prove a structural prior's lineage?

## REQUIRED OUTPUTS

- `V3_RUNTIME_PERSISTENCE_REQUIREMENT_LEDGER.csv`
- `BUILD_RUNTIME_BOUNDARY_EVIDENCE.md`
- `C01_RESULT.md`
- `C01_RESULT.json`
- common return files from `13_COMMON_WORKER_CONTRACT.md`

## BLOCKING CONDITIONS

Return a minimal witness if:

- accepted architecture requires ordinary live V3 respondent/event empirical query;
- a permanent empirical object is required to preserve a terminal capability and cannot be replaced by reference/replay;
- architecture and implementation are impossible to distinguish with available authority;
- terminal vision checksum finds starvation/leakage.

## FINAL DISPOSITIONS

- `C01_PASS__RUNTIME_CONSUMES_COMPILED_STRUCTURAL_PRODUCTS__EMPIRICAL_RUNTIME_DEPENDENCY_NOT_REQUIRED`
- `C01_PASS__NAMED_EMPIRICAL_RUNTIME_DEPENDENCY_REQUIRED`
- `C01_BLOCK__UNRESOLVED_BUILD_RUNTIME_BOUNDARY`
- `C01_BLOCK__TERMINAL_STARVATION_OR_LEAKAGE`
- `C01_RETURN__NAMED_EVIDENCE_REQUIRED`

STOP token: `VC4_C01_RETURNED`
