# SOROK developmental recursion — cycle coordinator

**Worker:** `sorok-recursion-cycle-r1`  
**Branch:** `agent/sorok-recursion-cycle-20261106-r1`  
**Startup:** `0d4edae634b3ef19643a7d0eb7752081013e5d83`  
**Scope:** sourcefree local implementation only; `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1`

## Delivered

- `developmental_recursion/model_cycle.py`
- `tests/test_model_cycle.py`
- `cycle_evidence/` receipts, source pins, sanitized passport and test log

`contracts.py`, `ABI.md`, `engine.py` (absent), accepted P2 code and the P2
adapter were not written or changed.

## Result

**PASS_SCOPED** for the model coordinator at the frozen stub-engine boundary.

The implementation provides:

- durable JSON cycle store with atomic replacement and an exclusive lock;
- `bootstrap`, `advance`, `finish` sequencing;
- one provider call per method/batch, never between events;
- bootstrap with no previous batch and no invented retrospective memory;
- ordinary call that completes the preceding retrospective and proposes the
  next prospective batch in the same call;
- terminal retrospective with no next batch;
- 3–5 strict prospective event documents with exact keys and owner admission;
- bound, ordered retrospective event IDs and exact batch/history hash identity;
- actor-accessible-only previous payloads; no objective history to provider;
- detached JSON context and no state writer passed to the provider;
- durable model-call reservation before every provider call;
- pre/post provider owner-snapshot equality check;
- ambiguous provider/engine failures held without blind retry;
- history rewrite, missing preceding batch, terminal-next-batch, malformed
  response and extra-key rejection;
- proposed impressions stored separately in `proposed_impressions`, never
  applied to canonical owner state;
- owner root/actor/branch and clock custody checks.

The runtime contains no fixed questions, actor names, workshop IDs or narrative
outcomes. Tests use generic contract fixtures only; they do not assert invented
psychology.

## Tests

Command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
PYTHONPATH=WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 \
python3 -m pytest \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_model_cycle.py \
  -q -o addopts="" -p no:cacheprovider
```

Observed: **19 passed in 0.24s**.

Coverage includes the full cycle, store reopen, strict proposal counts/keys,
owner source refusal, bootstrap fictitious memory, terminal next batch,
history rewrite, missing preceding batch, provider mutation, durable
reservation, ambiguous provider call, engine failure, root/clock custody,
detached context, accessible-only prior events and separate impressions.

## Source pins

- ABI: `08a44f995990f24060b430f96c58a4a8c0d421ef0deb0cb5ee7df90b5afc7489`
- Contracts: `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d`
- Architecture pin: `fbfc529230d8b3c13f824cfac31741a5dfaa57e5`
  (`20261026_USER_SETTLED_BATCH_RECURSION_IMPRESSION_MEMORY_R1.md`,
  blob `38876f6e73ac150754d642b6741fb0be71be255563b352fca32b40f00e5e7859`)
- Model cycle: `d9688f3d8351b6b078a4890754c1fdd14e715f7f43dee2d19c0e14fa5003d18c`
- Tests: `4c9b35bee0ca9547108782b174314ac48dee7c7d541aad700a9dba85765803ed`

## Runtime / passport

- Assigned model: `opencode-go/deepseek-v4.1-flash#max`
- Runtime observed: `opencode v2.0.22`, Python `3.11.3`, Darwin `22.3.0 x86_64`
- Quota: **UNKNOWN_UNOBSERVED**; no quota probe was made.
- Sourcefree local execution; no original SAV/DTA or respondent read.
- No new coefficients/laws, human validity, native/source issuance, production
  edit, protected merge or CI.

## Evidence files

- `cycle_evidence/TEST_RESULTS.json` — commands, pass count, runtime.
- `cycle_evidence/SOURCE_PINS.json` — ABI/contracts/architecture/code pins.
- `cycle_evidence/PASSPORT.json` — sanitized model/runtime passport.
- `cycle_evidence/pytest.log` — observed test log.
- `cycle_evidence/MANIFEST.json` — evidence hashes.
- `cycle_evidence/00_RETURN.md` — this return.

**Commit:** `PENDING_ARTIFACT_COMMIT`  
**Final state:** commit and push this exact branch, verify remote, then stop.
