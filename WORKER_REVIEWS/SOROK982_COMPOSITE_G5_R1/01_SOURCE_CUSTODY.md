# Source custody and independent source checks

## 1. Exact cut

| Item | Exact value |
|---|---|
| Review checkout | `/Users/matthewsmith/.codex/worktrees/sorok982-composite-g5/Rawlsing` |
| Review branch | `codex/sorok982-composite-g5-20261115-r1` |
| Report HEAD under review | `d5cf0c9c9925eb75c21c9a70793947f857917959` |
| Code/test HEAD under review | `ff30c13eea54e37e2dc8edfa73a7c7447127b735` |
| Code/test parent | `4cbf67398d742eeab0853d047b6c2239c84b8348` (PR #992 report head) |
| PR #992 code/test head | `6f1bc8894d1151d0921140e72bb43f5d1bb50fae` |
| Agent B source | `5d63d452c96d49a035355d9372b1ec3ddd4af6ba` |
| PR #976 source | `37c5842e04892421c9ce74a39956c3cdcf57f0f5` |
| Published composite head | `d5cf0c9c9925eb75c21c9a70793947f857917959` (`origin/agent/sorok-cga-982-composite-stale-receipt-20261113-r1`) |
| Local `origin/main` | `25830fe7462bb9e29bc4087e6ae14f3f84cec377` |

Ancestry was verified directly:

- `ff30c13ee^ == 4cbf67398`.
- `4cbf67398` descends `5d63d452`, `37c5842e0` and `origin/main`.
- `d5cf0c9c` descends `ff30c13ee`.
- The report commits after `ff30c13ee` add only `WORKER_RETURNS/SOROK-CGA-982-COMPOSITE-R1/` report, matrix, handoff and evidence files.
- The implementation delta `4cbf67398..ff30c13ee` is exactly five paths: `situated.py` plus four test assets.

`6a5c12f04323d74001f9632063ec907f4fc4468e` (the protected-only MCR-lite lineage cited by #977) is **not** an ancestor of this composite. That is a protected-line staging fact for HQ, not a source defect. No protected merge was performed and no staging campaign was launched.

## 2. Frozen test-asset authenticity

The original hostile test was not rewritten or weakened:

- `a1453e799d98b4c47d26c56a12d1d2695bd42557` is
  `c597024bb250f014f9a616006f10172ed53e4357:WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_hostile_stale_receipt.py`,
  the D1 branch copy, and `HEAD:WORKER_RETURNS/SOROK-CGA-982-COMPOSITE-R1/test_g5_stale_receipt.py`.
- `30701f83ee7dcc37aa3cf958a7224cd6229b6816` is the D1 author contract test at `4952f62ea1aa175d6ea6b83d8f6beb488e12befb` and the composite copy.
- `2b489ba1edd0698ead4899fe64abe19e9f7f4cce` is `9d3d8ae419998a3e13d88f58147756149e3dddb5:WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_receiver.py` and the source-pinned receiver baseline copy.

## 3. P4 #992 scope-owner preservation

The four PR #992 paths are byte-identical at code/test, #992 report, composite code and composite report:

| Path | Blob |
|---|---|
| `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/response.py` | `730d5692c16a4039981d25a632bf97d428eae526` |
| `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py` | `b99d8e82ed8ba25b9d090c5d7041eadb7ebd19d4` |
| `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/sourcefree_p3_bridge.py` | `a041785f88956fc65464e124bc4007d8a4914f95` |
| `WORKER_RETURNS/SOROK-CGA-P4-SOURCE-OWNER-R1/test_p4_scope_owner.py` | `728799b1250e61d3aafc7eeb2c3ed003f514a157` |

The composite P6 change is only:

- base `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py` blob `1433d6885706e7638f7ca5f511de85c93cbbe263`;
- final blob `56d9b2e399c349ab0fcc52619ee48b3a119f19df`.

## 4. Source hashes

SHA-256 of the exact working-tree source/test files at `d5cf0c9c` is recorded in `evidence/SOURCE_STATE.txt`. The reviewer did not edit any product file. The only reviewer-authored files are this `WORKER_REVIEWS/SOROK982_COMPOSITE_G5_R1/` return and its evidence; scratch output is under `.local-logs/sorok982-composite-g5/`.

## 5. P4 scope-owner source check

- `response.qualified_scope` binds the four foreground fields to the unique source `FORMATION` plan, the single relation, the plan hash, the source hash and the registry hash.
- `response.read_response` calls `qualified_scope` itself before the P3 read, so the direct reader cannot be redirected by a mutable ledger.
- `run_p4.act` checks `qualified_scope(..., exact_keys=True)` before `ledger["pending"]`, speech or world mutation.
- `sourcefree_p3_bridge.qualified_p4_scope` delegates to the P4 owner instead of creating a second scope authority.

The P4 7-test group includes four field substitutions, an extra foreground key, a direct-reader substitution with a query-spy assertion, pre-pending/no-mutation proof and a restored positive. It passes at this cut.
