# PYAT HQ174 — LOCAL D2M + DARWIN RUNTIME QUALIFICATION BOUND

Status:
`NON_MAC_OVERCONSTRAINT_CORRECTED__LOCAL_D2M_AND_DARWIN_ANCHOR_RUNTIME_BOUND__RAW_SOURCE_EXECUTION_HELD`

Decision:
`HQD-2026-10-02-174`

## Correction

Omega-1 did not require a non-Mac execution surface.

Its actual law:
- freeze the actual execution environment;
- honor Darwin/x86_64 when relying on the retained physical reproducibility anchor;
- a different environment requires explicit equivalence qualification.

C4C2 proved:
`P2X_DARWIN_GATES_NOT_ON_C4_PATH`

Therefore HQ withdraws the non-Mac-only constraint for source-free C4 qualification.

## D2M local retained-checkpoint export — BOUND

Branch:
`agent/opencode-pyat-hq174-lits-d2m-local-checkpoint-export-r1`

Tip:
`ffd85e5e92e07e32f14e013485c983e7a4c575e5`

Launch:
`OpenCode — Space Bunny Free — local Mac`

Reads only the exact retained checkpoint after fresh size/SHA gate.

Raw LiTS source access remains prohibited.

## C4C3 Darwin-anchor runtime — BOUND

Branch:
`agent/opencode-pyat-hq174-c4c3-darwin-anchor-runtime-r1`

Tip:
`eba2f4249fb7cd315851ff687269bc43ade19ce8`

Base:
`8f7efe690a161902e79358eb31650c238a4c0be8`

Launch:
`OpenCode — Space Bunny Free — local Mac`

Environment seed:
- CPython 3.11.3
- pytest 9.1.1
- pandas 2.3.3
- numpy 2.4.6
- pyreadstat 1.3.6
- pyarrow 25.0.1

Required authoritative C3 court:
`55/55`

Synthetic SAV/DTA only. No real survey source access.

## After both return

Fan in:
- C4A
- C4B
- D2M
- C4C3

Then:
1. emit one executable-freeze candidate;
2. one independent review;
3. separate exact source warrant;
4. only then live C4 source execution.

## Held

- raw survey source access
- C4 live production
- C7
- PRE-V3→V3 actor/person
