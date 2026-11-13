# SOROK CG-A P4 source-owner local repair — execution return

**Author disposition:** `DELIVERED_FOR_INDEPENDENT_G5`. Not a G5 approval.
**Base:** PR #986 frozen branch `review/sorok-cga-agent-b-scope-custody-20261112-r1` at `5d63d452c96d49a035355d9372b1ec3ddd4af6ba`.
**Branch:** `agent/sorok-cga-p4-source-owner-local-20261112-r1`.
**Code/test commit:** `6f1bc8894d1151d0921140e72bb43f5d1bb50fae`.

## 1. Source custody and environment

- Local clone: `/Users/matthewsmith/Desktop/Rawlsing/FIABC-P2X-protected-b53-retry1` (origin `maidiu/rawlsing`).
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-cga-p4-source-owner-r1`.
- Ancestry verified: `5d63d452c9` is the direct parent of `6f1bc8894d`; no rebase or protected-branch change.
- Isolated writer branch; no other local worktree is checked out on this branch.
- Host: macOS 13.2.1 x86_64, 16 CPUs, 16 GiB RAM.
- Model/session: OpenCode local session, `opencode-go/deepseek-v4.1-flash`.
- Python 3.11.3; pytest 9.2.0; isolated venv at `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/venv-pyat919-s2e-a3`.
- Original working tree and protected PRE-MAIN untouched.

## 2. Original defect reproduced RED on unmodified #986

The new test was added test-only to a detached `5d63d452c9` worktree; production source was not changed.

```bash
python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-P4-SOURCE-OWNER-R1/test_p4_scope_owner.py
```

Result: **exit 1, 6 failed, 1 passed, 49.51 s**.

- The genuine positive passed.
- `project`, `counterpart`, `interlocutor_role`, `relation_ref` substitutions all failed `DID NOT RAISE RecursionRefusal`.
- An extra foreground scope field also failed `DID NOT RAISE`.
- Direct `response.read_response` with substituted scope failed `DID NOT RAISE` and performed the P3 read.

Actual source-level consequence on unmodified #986: after a real P4 SAY with `request_edge=True`, a substituted `project` was accepted; the actor response changed from `joint_check` to `inspect_alone`, and the prior P3 record hashes disappeared from the uptake readset. Speech had already been committed.

## 3. Corrected GREEN

```bash
python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-P4-SOURCE-OWNER-R1/test_p4_scope_owner.py
python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-AGENT-B-SCOPE-CHALLENGE-R1/test_scope_source.py
```

Results at `6f1bc8894d`:

- New P4 source-owner test: **7 passed, 57.50 s**.
- Agent B #986 source-scope tests: **6 passed, 47.97 s**.

The corrected test proves refusal before any P4 pending write, actual speech, world mutation, P3 state change or actor expression. Each tamper state was restored to the exact source scope and then completed the real SAY with `joint_check` and prior P3 records.

## 4. Repair at the original owner

Changed source blobs:

| Path | Blob |
|---|---|
| `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/response.py` | `730d5692c16a4039981d25a632bf97d428eae526` |
| `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py` | `b99d8e82ed8ba25b9d090c5d7041eadb7ebd19d4` |
| `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/sourcefree_p3_bridge.py` | `a041785f88956fc65464e124bc4007d8a4914f95` |
| `WORKER_RETURNS/SOROK-CGA-P4-SOURCE-OWNER-R1/test_p4_scope_owner.py` | `728799b1250e61d3aafc7eeb2c3ed003f514a157` |

- `response.qualified_scope` binds the four foreground fields to the unique source-issued `FORMATION` plan, including exact relation cardinality, plan hash, source hash and registry hash.
- `response.read_response` validates the scope itself, so the exported direct reader cannot be called with a substituted scope. It accepts a full plan plus `relation_ref` for the legitimate direct-reader contract.
- `run_p4.act` validates the ledger scope with exact keys before setting P4 pending or admitting speech. This covers P4, P5 and P6 SAY paths with the optional P6 bridge disabled.
- `sourcefree_p3_bridge.qualified_p4_scope` now delegates to the P4 owner validator, preserving the existing `P6_P3_SCOPE_NOT_SOURCE_BOUND` contract while removing duplicate policy.

## 5. Inherited and G5 baseline execution

Six-group #977 baseline, with test-only receiver asset from `9d3d8ae419998a3e13d88f58147756149e3dddb5` (blob `2b489ba1edd0698ead4899fe64abe19e9f7f4cce`):

```bash
python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_receiver.py \
  WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py \
  WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
```

Result: **exit 0, 37 passed, 2378.06 s** (39:38; 77,320,192-byte max RSS). The four tested source/test blobs are byte-identical to `6f1bc8894d`.

Additional inherited execution:

- Agent A five cue-issuer + Agent B six bridge + P4 CLI + P5 experience: **14 passed, 237.46 s**.
- P6 actor initiative, hostile initiative, scene context and MII: **45 passed, 588.79 s**.

## 6. Separate #982 hold remains

The independent stale-authentic-receipt hostile test was executed with its source-pinned test-only blob `a1453e799d98b4c47d26c56a12d1d2695bd42557` from `c597024bb250f014f9a616006f10172ed53e4357`.

Result: **1 failed, 11.28 s**. An old authentic `APPROACH` receipt at clock 248 was still accepted as current actor access after `WAIT 4` advanced the world to clock 253. This is the separate CGA-G5-D1 obligation under #982 and is not repaired or widened here.

## 7. Concessions and corrections

- Agent A: preserved sensory issuer, performed-event authentication, exact `P6_HOUSE_CONDUCT` parent, separate world/P3 readsets and crash fail-stop. A's source custody did not bind the mutable P4 foreground scope.
- Agent B: correctly identified mutable `ledger["scope"]` redirection and the missing executable evidence; its P6 preflight was not the original owner and left P4 SAY and direct `read_response` exposed.
- Supplied R2 five-file patch was not materialized in the local workspace. Its central proposal was independently evaluated and adopted in smaller form: P4 source/response ownership, exact pre-pending refusal, P6 reuse, and direct-reader defense.
- The repair does not generalize beyond the single sourcefree FORMATION fixture; ambiguous or multi-formation configurations refuse.

## 8. #913 obligations

| Obligation | Status |
|---|---|
| `CGA-P3-ABI` | Preserved; P3 owner/config/store ABI unchanged; new check consumes the source-issued plan only. |
| `CGA-POSITIVE-CAPITAL` | Unchanged; no new actor/psychological capability claimed. |
| `CGA-COLD-LATER-READ` | Preserved and exercised by the 37-test baseline; P4/P6 cold reopen remains green. |
| `CGA-CGB-CD-CONTRACT` | Unchanged; no CG-B/C/D construction. |

## 9. Holds

- #982 stale authentic receipt remains failing and separately leased.
- No native CAN/ADP/PYAT science, actor consciousness, human A5 right, memory issuance or production readiness is claimed.
- No protected merge, no self-G5, no actor authority promotion.
- `G5` remains for an independent receiver at the exact final HEAD.
- Multi-actor/multi-formation scope is not claimed; ambiguous plans refuse.
