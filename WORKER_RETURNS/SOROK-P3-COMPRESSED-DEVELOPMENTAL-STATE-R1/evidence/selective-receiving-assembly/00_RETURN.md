# P3 selective receiving assembly — return

Status: **ISOLATED CANDIDATE ASSEMBLED / NO PR / NO MERGE / ADDITIVE QUALIFICATION PENDING**.

## Exact assembly

| Item | Exact identity |
|---|---|
| Protected PRE-MAIN base | `integration/pre-main-reconciliation-r1` @ `c852d7516e23fcb6cf2215e9be7c5fa268503516` |
| Isolated candidate branch | `codex/sorok-p3-selective-receiving-20261107-r1` |
| Runtime/evidence source | `agent/sorok-p3-compressed-developmental-state-20261106-r1` @ `16275d03fc4724a694c48ed9d447c4eeadbe25f2` |
| Implementation cut | `486d42a4aa5dcd449564b95567ae93b59c4679a4` |
| Goal-audit source | `agent/sorok-p3-goal-audit-20261107-r1` @ `140b585f9b7321984725cf6f38ae95c2cb2bf89c` |
| Additive residual-proof source | `agent/sorok-p3-goal-residual-proof-20261107-r1` @ `036787c1f0c227cdc47828ba521a62b76c57a903` |
| Focused review | `e85b6f6a733ef5bbd664679bdf9613c04003e3de` — `ACCEPT_SCOPED_TEST_ONLY`, M1/M2/M3 closed |
| HQ disposition | `9abb3eee3d59c76ce20d5131d5b60151f7ca98ae` — `FOCUSED_RECHECK_DISPOSITION.json` |
| Selected paths | **186** = 170 prepared package + 15 focused-review artifacts + 1 disposition |
| Tests rerun | **No** |
| PR publication / receiving / merge | **HELD** |

## Assembly checks

- `PATH_ALLOWLIST.txt` contains all 186 selected paths.
- `BLOB_CHECKS.json` records every selected path, source cut, Git blob, SHA-256, byte count and source-match result.
- All runtime/test files match the accepted source cut byte-for-byte; no code/test/runtime edits.
- Focused-review `REVIEW_MANIFEST.json` hashes verified for 14 listed files.
- `git diff --name-only c852d751…` equals the 186-path allowlist exactly.
- No `SOROK_PRODUCT_CONTROL_ROOM`, PROGRAMMA, `.DS_Store`, `__pycache__` or `.pyc` path is in the candidate delta.
- Protected base and all source refs were remote-verified before assembly.
- Selected dependency closure: accepted #704 engine, S45 projection and P2 fanin are present at base; exact E1 B1 dependency is included; no S1 runtime import; no missing runtime dependency.

## Evidence

- `ASSEMBLY_MANIFEST.json` — assembly pins, counts, dependency closure and limits.
- `BLOB_CHECKS.json` — per-path source/blob/hash checks.
- `PATH_ALLOWLIST.txt` — exact 186-path branch delta.
- `FINAL_PR_DRAFT.md` — final draft body.
- `COMMANDS.md` — exact construction and verification commands.
- `HASH_MANIFEST.json` — hashes of this assembly evidence.

Focused-review acceptance is real at the exact runtime cut but does not accept additive residual proofs. The controlled `036787c1` author proofs remain pending nonauthor qualification. The earlier REVISE negative evidence remains preserved.

## Remaining dependencies

1. Nonauthor qualification of the additive `140b585f` / `036787c1` goal-audit and residual-proof artifacts.
2. HQ final PR publication, protected receiving and merge. This author assembly does not push the protected target and does not create or publish a PR.

No native-science, original-human, actor-B, production, source-grant, CAS, protected-receiving or merge authority is claimed.
