# Commands, blobs, tests and session handoff

## 1. Session custody

- **DEVICE:** `oldMac`.
- **DEVICE_VERIFICATION:** local-machine-name-verified: `scutil --get ComputerName` → `oldMac`; `scutil --get LocalHostName` → `oldMac`; `hostname` → `Matthews-MBP.lan`.
- **HARNESS:** `OpenCode` (`OPENCODE=1`; process comm `opencode`).
- **AGENT_NAME:** `opencode` (process/interface name; no separate operator-supplied profile name exposed).
- **AGENT_ID:** `UNKNOWN_NOT_EXPOSED`.
- **AGENT_ROLE:** `Independent I2 hostile sourcefree security reviewer`.
- **AGENT_MODE:** `UNKNOWN_NOT_EXPOSED__SINGLE_AGENT_INTERACTIVE`.
- **MODEL_PROVIDER:** `opencode-go`.
- **MODEL_ID:** `opencode-go/deepseek-v4.1-flash`.
- **REASONING_EFFORT_REQUESTED:** `MAX`.
- **REASONING_EFFORT_VERIFIED:** `UNVERIFIED` (not observable from inside this session).
- **SESSION_NAME / ID / URL:** `UNKNOWN_NOT_VISIBLE`; no app title or deep link invented. Terminal supplement: `TERM_SESSION_ID=0DD2D45D-C6CC-4DC3-AB20-BC31967BB316`; `OPENCODE_PID=27700` (process identifier only, not an agent/provider ID).
- **WORKTREE:** `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/g17i2-return`; test workspace `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/g17i2`.
- **ORIGINAL IMPLEMENTING SESSION:** `UNKNOWN`; exact author lane is `agent/sorok-g17-forged-material-future-child-c9-source-repair-r1` at `8b9a39da…`, worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-g17-forged-material-future-child-c9-source-repair-r1`; original author cut `90d0eb7925de54635559a879ee76fc1b97b9ff61` at worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/g17`. No session title/link was recovered; `SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION`.
- **INDEPENDENT REVIEWER SESSION:** `NOT_ASSIGNED`.
- **CENTRAL REGISTRY:** not modified by this worker; incumbent HQ must append the G17I2 row to `CROSS_HQ_CONTROL_ROOM/SESSION_LOCATORS.json` after direct return readback. This worker’s write scope is `WORKER_RETURNS/G17I2-R3/**`.
- **NO AUTONOMOUS HARNESS/MODEL SWITCH:** satisfied.

The machine-readable row is `SESSION_LOCATOR.json`.

## 2. Exact source and candidate blobs

| Role | Path | Git blob | SHA-256 |
|---|---|---|---|
| Original continuation | `.../G17-MATERIAL-HISTORY-INDEPENDENT-LIVES-R1/candidate/lab_sgi1/continuation.py` | `c9318dcf33d041a673cfae15aff8fc51712f53e7` | `89921be043daed114d734550afb828d3b252d6a5ee3bf631cc669df4356736d1` |
| Original pipeline | `.../candidate/lab_sgi1/pipeline.py` | `fc954993ef966d20d1915546e04a122daa93538f` | `04c2f07ed435db19cbe14bb377c52d2be0f854eca4cc5985e0d6419272f209bb` |
| Original C9 | `.../c9_handoff_consumer.py` | `47e59c12b79c04b05c18e73ad76078a29d0d7b3c` | `5ccfa3e230975b7507817fc96a2b4c4ccce16ee9ab9ffd1997c02d351a01164b` |
| Candidate continuation | `.../SOROK-G17-HOSTILE-MATERIAL-CUSTODY-REPAIR-R1/candidate/lab_sgi1/continuation.py` | `705ef1a4568ec84020638b3cf32d348066945e86` | `80823bde776f09a2ae7bf02dd7458982625a318fb9248228a5df2401e88d9426` |
| Candidate pipeline | `.../candidate/lab_sgi1/pipeline.py` | `d07bb06c7a44cd337a43c387f55a17906c5307e3` | `b5d19758da9b8115642e832efff17343cebfab1987fb37cf5afbfc59b362376c` |
| Candidate C9 | `.../candidate/c9_handoff_consumer.py` | `bd7a179e846e4067e324360fc3411806b2a537d4` | `2c0430340512b7c2447c73de019227481f43f7156ba3d1b19d1fd8e16f7f4c6d` |
| Reviewer test | `.../G17I.../tests/test_g17i_independent.py` | `83f17006b22271f17c87f4563608de08395d7a1c` | `0e4535a708d83a85d763c592f3d206f0b21dbc599846d7ffcd89cd82f145a5e6` |
| Author test | `.../G17.../tests/test_g17_material_history_consumer.py` | `ab422636ef4a0d51f58049275b0fc4d19a609448` | recorded in `01_...json` |
| Additional hostile test | reviewer-patched `tests/test_g17i2_additional.py` | not committed separately | `10f9250aa580ce66b9d093e8c479c2fea2cf1c0699456c2a8f657ef57b3fdb1b` |

Original test files were byte-identical and unchanged. The additional test source is embedded in `01_...json`.

## 3. Commands and actual exits

```sh
# original reviewer baseline
cd .../g17i2/reviewer-base/WORKER_RETURNS/SOROK-20261019-G17I-MATERIAL-HISTORY-INDEPENDENT-R1
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_g17i_independent.py -q -p no:cacheprovider --junitxml=.../01_original_reviewer_11p3r.xml
# exit 1; 14 tests; 11 passed; 3 failed; 0 errors; 0 skipped

# patch only the three candidate files into target_candidate, then:
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_g17i_independent.py -q -p no:cacheprovider --junitxml=.../02_patched_reviewer_14.xml
# exit 0; 14 passed; 0 failed/errors/skipped

# author positive after the same overlay
cd .../author-patched/WORKER_RETURNS/SOROK-20261019-G17-MATERIAL-HISTORY-INDEPENDENT-LIVES-R1
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_g17_material_history_consumer.py -q -p no:cacheprovider --junitxml=.../04_author_patched_13.xml
# exit 0; 13 passed; 0 failed/errors/skipped

# independent additional hostiles
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_g17i2_additional.py -q -p no:cacheprovider --junitxml=.../05_additional_3.xml
# exit 0; 3 passed; 0 failed/errors/skipped

# cold-process reruns in fresh Python processes
# reviewer 14/14, author 13/13, additional 3/3 (JUnit 06/07/08)
```

The exact JUnit XML for all eight runs is embedded in `01_...json`. SHA-256 examples: original reviewer `b9f30f7d…`, patched reviewer `a4ac44c0…`, author patched `b09eae9b…`, additional `e2b74743…`. All runs have 0 errors and 0 skips.

## 4. Independent additional assertions

- `test_deep_nested_future_child_alias_refused`: nested `metadata.nested[0].future_child_personality` returns `FUTURE_CHILD_INFORMATION_LEAK` with the expected component/field.
- `test_c9_owner_canonical_material_forgery_refused`: canonical handoff + material with `owner_id=FAKE_CANONICAL_OWNER` raises `C9Refusal("MATERIAL_SOURCE_NOT_AUTHENTIC")` through the same `receive_handoff`.
- `test_c9_canonical_material_still_accepts`: genuine canonical material returns `ACCEPTED`; `e2_later_authority` remains `HOLD_UNISSUED`.

## 5. C9 R3B / C12 handoff

- C9 R3B branch `fac064c9…` is unlaunched; writer blob `67f34f69…` SHA-256 `ee4765e2…`; reader blob `5ef6a278…` SHA-256 `331cdae8…`.
- No G17 adapter, no durable actor SQLite, no C12 branch/mirror. C9 R3B tests **NOT_RUN** (separate unlaunched source closure).
- Durable C9 reopen and C9/C12 interoperability are **HOLD**, not claimed.

## 6. FINDING / INTERPRETATION / ACTION / OWNER

**FINDING:** G17 candidate passes the exact original reviewer/author assertions and independent deeper/owner-canonical/C9 probes. It is not a durable C9/C12 consumer.

**INTERPRETATION:** The patch repairs material-owner authentication, recursive future-child partitioning and the bounded C9 handoff without changing oracles. Cold-process replay is source-level repeatability, not persistent custody.

**ACTION:** Original G17 author/C9 owner replay and accept or reject the three blobs; C9/C12 owners decide the adapter/durability cut; incumbent HQ assigns a separate reviewer. No merge/adoption.

**OWNER:** Original G17 author; C9 handoff owner; C9 R3B/C12 owners; incumbent Sorok HQ; separate reviewer.

## 7. DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

- **DONE:** exact 11/3, 14/14, 13/13, cold replay, 3/3 additional hostiles, session locator, C9 R3B interface read.
- **REMAINING:** owner replay/acceptance; C9 R3B/C12 adapter and durable cold reopen; native Rule A/T/M2/MP.
- **BLOCKERS:** no durable C9/C12 consumer; C9 R3B unlaunched/incompatible; no native source grant.
- **LARGEST MOVE:** original G17 author applies the three candidate blobs at `90d0eb79…` and replays; C9/C12 owners decide whether an adapter is worth a separate commission.
- **FLIGHT:** sourcefree local Git/Python; no PRE-MAIN/PR/original branch mutation.
- **DELTA:** three original G17I REDs closed under unchanged assertions, with C9 durability explicitly still HOLD.

## 8. Final remote SHA

The ordinary push binds this return. Exact 40-hex SHA is read back with `git ls-remote` and reported in the final response; no self-reference is embedded. No force-push, no self-adoption.
