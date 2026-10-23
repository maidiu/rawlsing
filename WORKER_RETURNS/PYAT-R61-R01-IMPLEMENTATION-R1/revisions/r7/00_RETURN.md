# R61-R01 R7 OpenCode successor author return — retained owner completion

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted. R03 stays
NOT_STARTED.

## Identity and executor correction

- Branch: `agent/codex-pyat-r61-r01-r7-retained-owner-repair-r1`
- Startup: `7e021bd0eb539baccbd79f19a5e51efa19661e44`
- Successor directive: `7e05980717b8bf28b1c386b0293b467b7fc15856`
- Contract commit: `3f96169b2` (frozen before partial code)
- Partial patch retained: `7e021bd0e` (`native_map.py` only; unqualified)
- OpenCode completion commit: `0271a7e37a3ccccce5ff69db99f56f7745a62875`
- Executor now SAME existing OpenCode DeepSeek V4.1-Flash MAX/Global. Branch
  name records the interrupted Codex history, not the actual successor executor.
  The partial native patch was inspected and completed, not rewritten.

## Function delivered

The R6 campaign owner is now a full local retained-record state machine.

- `create_campaign` resolves actual releases, query/target semantics, root and
  condition predicates against the configured repository/authority closure;
  duplicate typed catalog keys refuse; query/root/J mismatches refuse before
  native work.
- Issue preserves chronological issuance independently from discovery generation;
  any root0 batch can issue generation1; multiple gen1 batches count exactly.
  Cumulative counts derive from retained expected-operation records. Zero cap is
  explicit stopped-budget/no-work.
- Execute resolves the retained issuance, full parent lineage/ancestry,
  source/root/query/native authority context and predecessor chain again before
  native invocation. It stores a complete activation preimage: authority,
  grammar frontier, every receipt with typed state, canonical handoffs and
  no-drop reconciliation. Retry of a completed issuance returns the retained
  execution without a second native call or budget charge.
- Activate consumes the same checked projection live and cold. Completed
  execution before activation restores and activates without re-executing the
  original issuance. Repeated activation returns the original activation.
- Snapshot/restore serialize all records and handoffs. Restore requires the
  separately supplied original checkpoint pin, validates frozen native context
  and full record/plan/count/receipt/handoff/lineage closure, then replays
  administrative transitions only. Altered/rehashed bytes fail the unchanged
  pin.
- Inspect returns detached material; mutation cannot rewrite retained authority.
  Run-local RLock serializes transitions. Inflight/ambiguous execution stays
  typed HOLD.

## Qualification

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r7/junit.xml -o addopts=''
```

- Exit `0`; `31 passed`, `0 failed/errors/skips`; `26.31s`.
- JUnit `junit.xml`; log `pytest.log`.
- Campaign D3 measured separately: 3 issuances/executions, `2.925s`, peak RSS
  about 39 MB.
- New R7 successor tests cover create source/query/catalog refusals; execute
  context substitution; multi-batch gen1 exact counts (4 then 8); pre- and
  post-activation restore; actual later-generation N+1; retry native-call
  conservation (2 calls for 2 executions, unchanged after retries/activations);
  typed receipt states; inspect mutation; fixed-pin altered snapshot refusal;
  genuine restore PASS.
- Retained original suite covers changed-data D3, root/parent arithmetic,
  hidden 75/25 minority, nonwinning exploration, cold persisted-parent N+1,
  conditioned JOINT/CO_TRAVEL, A1-A3.
- Imported owner blobs: `pre553_discovery_exact.py`
  `905f24d114419dbdd93879ad2bee5b59dd2f23af`, `pre553_recursive_handoff.py`
  `868f43bf9869af5501fd67c3de7a2703ba4cb1b4`,
  `pre553_empirical_objects.py`
  `a61365b994e5c3c50de0f598fcf40e90abf757b6`.

## Changed paths and blobs

| Path | Blob |
|---|---|
| `rawlsing_next/universal_grammar/types.py` | `e7b196efe5b1f86134c27a80bfdd8f472be76e5d` |
| `rawlsing_next/universal_grammar/enumerate.py` | `fd9203a0b272f98771c24070d01a9e5287c9b099` |
| `rawlsing_next/universal_grammar/native_map.py` | `fd3dc6138ade59a2f7b2ffd7a4514604e916d25f` |
| `rawlsing_next/tests/test_universal_grammar.py` | `f5360894a8271cf8492e2ee39d9f7ab91ccbb5e5` |

Report artifacts are SHA256-listed in `manifest.json`, which excludes itself.

## Limits

Local trusted-host campaign authority only; no protected issuer/signing service,
global durable uniqueness, anti-rollback/fork, or R09 capture. Snapshot pins
establish exact restored history, not latest-state knowledge. R04/R09 custody,
R03/U43/Batch, R05 grades, original 35/1890, global F6/F7/F8, N11/N12, Sorok,
production/CI and J52/W52 remain NOT_REACHED. Distinct independent native review
required.
