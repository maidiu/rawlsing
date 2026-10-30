# SOROK G17 — hostile material / future-child / C9 custody repair candidate

## Identity and terminal disposition

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-g17-forged-material-future-child-c9-source-repair-r1` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-g17-forged-material-future-child-c9-source-repair-r1` |
| Sealed startup | `342164a09e10aa70812299c12386ed0923308228` |
| Branch head at launch | `a9291cf6cd5a5d777c84bf5d20de914fa369402a` |
| PRE-MAIN pin | `299f41e97a43c67be9cc76a79fa49b48f4e12e54` (verified; unchanged) |
| Original author cut | `90d0eb7925de54635559a879ee76fc1b97b9ff61` |
| Original reviewer cut | `156b84cc8481b65c4196b42574010eb7920d6f44` |
| F3 reconciliation cut | `6477a89bb9160eba1dd10607c47534fa4dce6cc2` |
| Editor / model | Local OpenCode / DeepSeek V4.1-Flash (`opencode-go/deepseek-v4.1-flash`); MAX selected/requested by the user but actual effort not independently observable from inside the session; no model/harness switch |
| Execution | S2 isolated local Git/Python/pytest, sourcefree only |

**Terminal:** `SOURCEFREE_ACCEPT_SCOPED__ENGINEERING_REPAIR_CANDIDATE`
**Dispatch condition:** `CONDITIONAL_SOURCE_OWNER_SCOPED__NO_INTEGRATION`

Observed FINDING: the original G17 reviewer cut is exactly **11 PASS / 3 RED** and the three failures are real: forged material cash 100058, nested future-child alias COMMITTED, and forged C9 material ACCEPTED with cash 100055. Causal INTERPRETATION: the author paths authenticated only references/after-states; they did not authenticate the owner-canonical material event or recursively inspect nested visible input. Proposed HQ ACTION: owner replay of the separate three-file candidate, then independent review; no merge or adoption. Accountable OWNER: original G17 author, C9 owner and separate source-qualified reviewer under incumbent HQ.

## Candidate result

A separate candidate overlay (not an edit to the original branches) repairs the three exact assertions:

- `continuation.py`: owner-canonical material event authentication plus participation event-preimage and material causal-parent checks.
- `pipeline.py`: recursive future-child partition scan over nested dict/list/string visible fields.
- `c9_handoff_consumer.py`: owner-canonical material authentication and handoff payload equality before C9 acceptance.

Original assertions are unchanged. Forged material now returns `None`; nested alias returns `FUTURE_CHILD_INFORMATION_LEAK`; forged C9 material raises `C9Refusal("MATERIAL_SOURCE_NOT_AUTHENTIC")`. Exact hashes and mappings are in `01_SOURCE_PATCH_AND_ORIGINAL_REDS.json`.

## Tests actually run

| Court | Actual result |
|---|---|
| Original reviewer baseline, unchanged test `83f17006…` | **11 passed / 3 failed** |
| Patched reviewer, same test | **14 passed / 0 failed** |
| Patched reviewer, fresh-process replay | **14 passed / 0 failed** |
| Patched author positive, author test | **13 passed / 0 failed** |
| Patched author positive, fresh-process replay | **13 passed / 0 failed** |

JUnit and logs are under `evidence/`; exact commands and fault details are in `02_REPRODUCED_TESTS_JUNIT_AND_FAULTS.md`. C9 genuine handoff, source severance and forged-material refusal are exercised by the reviewer test. Cold-process replay is used because this G17 slice has no durable C9 store; durable C9 reopen remains NOT_RUN/HOLD.

Original corpus and native authority: **not used**. No survey/respondent data, native Rule A/T, M2/MP fabrication, C11/C12 weld, child/person generation, PR514/516/519 or PRE-MAIN mutation. M2 grammar and MP known-counterpart coverage remain typed HOLDs; full C9 E1/RULE_A/RULE_T/E2 remains `HOLD_UNISSUED`.

## Three courts

- ENGINEERING: **PASS SCOPED** — original RED reproduced, same assertions repaired, author positives preserved, cold-process replay stable.
- SCIENTIFIC: **TEST-ONLY / HELD** — material/current-state method only; no native person, biology, calibrated psychology or original science.
- AUTHORITY: **HOLD** — no merge, adoption, production or source-authority transfer; original G17/C9 owners and a separate reviewer must decide.

## Artifacts and exact return SHA

- `00_RETURN.md`
- `01_SOURCE_PATCH_AND_ORIGINAL_REDS.json`
- `02_REPRODUCED_TESTS_JUNIT_AND_FAULTS.md`
- `03_ORIGINAL_OWNER_AND_REVIEWER_HANDOFF.md`
- `candidate/lab_sgi1/continuation.py`, `candidate/lab_sgi1/pipeline.py`, `candidate/c9_handoff_consumer.py`
- `evidence/01…07` JUnit/log/fault receipts

The exact pushed remote SHA is the HEAD of this worker branch and is reported with the final return message. Worktree is clean apart from untracked host `.DS_Store` files; no unsent return files.

DONE: exact original 11/3, three repairs, 14/14 reviewer, 13/13 author, cold replay, C9 positive/severed/forged, hashes and handoff. REMAINING: original owner replay and independent review. CRITICAL BLOCKERS: native C9 E1/E2, M2/MP, Rule A/T and person authority remain held; none block the bounded engineering candidate. LARGEST PRODUCTIVE MOVE: original G17 author applies the three candidate blobs at `90d0eb79…`; C9 owner reviews `receive_handoff`. FLIGHT: sourcefree local Git/Python only, no PR or PRE-MAIN mutation. DELTA: the three original REDs are closed under unchanged assertions while every prior negative and authority HOLD is preserved.
