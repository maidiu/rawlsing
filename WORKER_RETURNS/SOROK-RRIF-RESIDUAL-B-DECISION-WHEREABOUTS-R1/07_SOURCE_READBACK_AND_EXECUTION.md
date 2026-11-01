# SOURCE READBACK AND EXECUTION

## Frozen source and live custody

| Item | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Assigned branch | `research/sorok-rrif-residual-b-decision-whereabouts-20261031-r1` |
| Gate01 return | `bbc65ea28dcebdd38507ca270c0a642a7c0290bd` |
| Gate01 content commit | `dfb161655ffc4e90eea6a79db69a73f5664a295d` |
| PRE-MAIN observed | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| PRE-MAIN live readback | `8e44ca9c751049d65e6def47600b5c073ee04b29` (`refs/heads/integration/pre-main-reconciliation-r1`) |
| Gate01 return live readback | `bbc65ea28dcebdd38507ca270c0a642a7c0290bd` (`refs/heads/research/sorok-rrif-hq-decision-subtraction-first-20261031-r1`) |
| Remote branch at start | `42ad21a53cc82e3c17445b099903c12d927b2f12` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-rrif-residual-b-20261031-r1` |
| Local branch HEAD at start | `42ad21a53cc82e3c17445b099903c12d927b2f12` |
| Content commit | `1cf5eb3d3676632c1f7b2fbe66c6a1ed73318160` |
| Final returned content SHA | `1cf5eb3d3676632c1f7b2fbe66c6a1ed73318160` (direct `ls-remote` readback) |
| Receipt-only follow-up | branch HEAD recorded in the final handback; contains this readback update only |

The worktree was created from the canonical private clone at `~/Desktop/rawlsing_r02v_r2_canonical` using the exclusive assigned branch. No other session/worktree was modified. No force, reset, branch deletion, source-native execution, PRE-MAIN write, Pyat work or PROGRAMMA work occurred.

## Host / model / effort

- Host: **mainMac**, macOS 13.2.1 (22D68), x86_64, Intel Core i9-9880H.
- Harness: **OpenCode 1.18.34**.
- Session: `ses_e6b412564ffeeBfEjjDzcgYT2f` (title `SOROK RRIF-RESIDUAL-B — WHERE WERE DECISIONS ON THE 97 UNRESOLVED RECENT SOROK BRANCHES ACTUALLY MADE?`).
- Agent: `build`.
- Model surface: provider `opencode-go`, model `deepseek-v4.1-flash`, local session variant `max`.
- **MAX verification:** local OpenCode session metadata reports `variant: "max"`; there is no provider-side attestation. This is actual local-session MAX evidence only, consistent with the launch requirement but not a remote entitlement proof.
- No model/harness switch, no subagent delegation for the adjudication, no paid provider call, no branch test execution.

## Actual source reads

### Gate01 and input

- `WORKER_RETURNS/RRIF-SOROK-GATE01-HQ-DECISION-SUBTRACTION-R1/05_TRUE_UNDECIDED_SOROK_RECOVERY_SURVIVORS.jsonl` (97 rows; SHA-256 and byte count in `06`).
- Gate01 `01_HQ_CHRONOLOGICAL_DECISION_EVENTS.jsonl` (19 prior events, baseline reused).
- Gate01 `04_ACCEPTED_NOT_INCORPORATED_INTEGRATION_ONLY.jsonl` (eight accepted-scoped records, guarded in `06`).
- Gate01 `00_PLAIN_ENGLISH_RETURN.md`, `06_UNRESOLVED_SOURCE_OR_OWNER_CONFLICTS.md`, `07_COVERAGE...json`, `SESSION_LOCATOR.json`.
- `SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md` and `.json` at PRE-MAIN `8e44ca9c` and at `865b5b01` where present.

### HQ motions (at Sorok working-HQ `865b5b01e1a27e99020cf2bb389af8cd4c874b57`)

Read directly, among others:

- `20261019_C9P_C0X_M2R4E_THREE_RETURN_HQ_ADJUDICATION_R1.md`
- `20261019_G15_C0R3_C9PI_RETURN_FANIN_AND_OWNER_DECISION_R1.md`
- `20261019_G16I_C8O_C0R3I_FANIN_OWNER_MOTION_AND_TERMINAL_FLIGHT_R1.md`
- `20261019_G17I_C8OI_C9R_RETURN_INTAKE_AND_G18_C9RI_FLIGHT_R1.md`
- `20261020_BP1_BP3_INTAKE_AND_BP2_BP4_CONSTRUCTION_DISPATCH_R1.md`
- `20261020_SOROK_SUCCESSOR_EFFECTIVE_CUT_AND_BP2_BP4_TWO_RETURN_INTAKE_R1.md`
- `20261020_P0_PS0_PA0_G18_FOUR_RETURN_HQ_NEEDS_FIRST_BUILD_DISPOSITION_R1.md`
- `20261020_R25_BP2P4J_HQ_RETURN_INTAKE_AND_NEXT_NATIVE_SCIENCE_SECURITY_FLIGHT_R1.md`
- `20261020_R26_TWO_RETURNS_REAL_C12_REPAIR_AND_FIRST_ACTOR_PRODUCER_FLIGHT_R1.md`
- `20261020_R27_R26E_R26V_RETURN_INTAKE_AND_FIRST_SOURCE_POSITIVE_FLIGHT_R1.md`
- `20261021_R29_R28S_SCIENCE_COURT_ADJUDICATION_AND_GENERATIVE_PERSON_BUILD_FLIGHT_R1.md`
- `20261021_R30_R29P_R29M_RETURN_INTAKE_MATERIAL_MECHANISM_AND_FIRST_NEIGHBOR_SESSION_FLIGHT_R1.md`
- `20261021_R31_R30G_R30A_TWO_RETURN_INTAKE_AND_WHOLE_ACTOR_SOURCE_EXPRESSIVE_ALPHA_FLIGHT_R1.md`
- `20261022_CODEX_HQ_EFFECTIVE_APPOINTMENT_AND_SAME_PERSON_EXECUTION_R1.md`
- `20261022_JOINED_POSITIVE_ACCEPT_SCOPED_AND_TARGETLESS_LINEAGE_REPAIR_R1.md`
- `20261024_R3_BROWSER_HQ_HUMAN_APPOINTMENT_AND_BOUNDED_ACTING_EFFECTIVE_CUT_R1.md`

### Reviewer / return documents

Read directly at exact commits (full list and blob identities in `01` and `02`):

- CLR3 `de9a525c`, CLR3R1 `f982580d`; M2R2 `e8b2d6be`, M2R3 `a4129eaf`, M2R4 documentary `8e74be26`, M2R4 executable `d09aeab9`.
- C0R3I `43328571`; C8OI `f4200eb0`; G16I `683aa568`; G17I `156b84cc`; G17I2 `95f15026`.
- BP2P4JI `3212d716`; F2 `0636d257`; F2I `26cf5352`; BP4I3 `0aaf119f`; M04/M03 `3a993abc`; M04I2 `09497812`.
- HR1 `40df1e61`; 294 RC1 `47e9c80a`; RRIF-R1 `c1765e0a`; RRIF three-return `b07b2233`.
- R3 HQ297–HQ320 reviewer returns listed in `01` rows 047–081; V2 HQ322–HQ330 returns in rows 091–098.
- Userdirect C0 `66d012c4`, C0F `df31181c`, C0R `98fdbdf0`, C0RI `5abd3c5d`.
- RA-A `ff47e917`, RA-C `d01454f6`, RA-D `6d3610c5`, RA-D review `c02139257`; N10W `c433be86`.
- M35 `4170fbf19`; S36 `8da78d80`; S37–S52 `278/280–293`; RFA-R `e65846bb`.

### GitHub PR layer

Read-only `gh pr list` and selected `gh pr view` for Sorok/RRIF PRs. The only decision-bearing PR comment located was PR #517’s comment repeating the HR1 `40df1e61` verdict; it is already captured. No PR description/comment located for the historical 97 branches (they were direct-push agent/reviewer branches, not PRs). Draft PR #514/#516/#518 remain drafts and were not treated as merges.

### Local session stores

Read-only SQLite queries against `~/.local/share/opencode/opencode.db` for the assigned session and for `onecall/userdirect/M35/S36/HQ324` terms; read-only compressed-session greps against `~/.codex/sessions/2026/10` and `~/.codex/archived_sessions`. No original M35/S36/S37–S52/userdirect one-call acceptance chat was found. Those cases are marked `UNKNOWN_SOURCE` with exact branch pointers; no chat decision was invented.

## Commands actually run

- `git` read-only: `show`, `ls-tree`, `log`, `rev-parse`, `cat-file`, `for-each-ref`, `ls-remote`, `merge-base`, `worktree list`.
- `gh` read-only: `pr list`, `pr view`.
- `sqlite3 -readonly` for the local session metadata.
- `python3` only for local parsing/generation of this return (not for branch source/actor scripts).
- No branch test suite, no branch Python module, no source/actor/native execution, no model call, no PRE-MAIN mutation.

## Unaccessed or not proved

- **PR review comment bodies for every PR:** not exhaustively read. The Sorok/RRIF PR set was listed; only #517 had a decision-bearing comment. The historical branch decisions were found in committed returns/HQ motions.
- **Original direct chat/session orders** for M35/S36/S37–S52 and userdirect one-call C0: **UNKNOWN_SOURCE** in the local stores searched. Exact branch/return pointers are given; no invention.
- **Provider-side MAX attestation:** not available. Local session variant is `max`.
- **Semantic equivalence of current PRE-MAIN code:** not assessed. Gate01’s exact-blob absence statement is preserved; this worker did not execute or compare branch code.
- **Pyat scope:** not accessed or adjudicated (`SOROK294-261` marked out of Sorok scope).
