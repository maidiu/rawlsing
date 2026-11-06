# P3 vertical resource/recovery repair — bounded author return

**Worker:** `sorok-p3-vertical-resource-repair-r1`  
**Branch:** `agent/sorok-p3-vertical-resource-repair-20261106-r1`  
**Startup / protected:** `8cc2914b1089cfc113ae1737941bd2a9efde622b` / `c852d7516e23fcb6cf2215e9be7c5fa268503516`  
**Code artifact commit:** `31da7feb2ae44b1aff75bc2f6ea346c87a3d38e6`  
**Scope:** sourcefree TEST_ONLY proof-harness repair; author only.

## Status

**`BLOCKED_ACTUAL_STORE_ABI_PLAN_AUTHORITY_OR_GRADE_MISSING`**

The returned store is now present. The actual focused vertical run was stopped
at the existing store boundary before any P2 event or psychological effect:

```text
PsycheStore.reserve
 -> _plan_view
 -> _plan_authority
 -> RecursionRefusal: PLAN_AUTHORITY_OR_GRADE_MISSING
```

The exact current trace is retained in
`evidence/vertical-resource-repair/actual_smoke.log` (`1 failed in 7.49s`).
The actual frozen P3 plans carry the exact `SOURCEFREE_TEST_ONLY` grade but no
separate `authority` field; this is the separately owned store ABI defect, not
a vertical-harness substitute.

No full suite was repeatedly run after this known blocker. No A–H case is
labeled green. No P2 event or durable psychological effect was produced.

## What was repaired/completed

Only the authorized P3 test harness files were changed:

- `tests/p3_fixture_support.py`
- `tests/test_p3_vertical_slice.py`
- `run_p3_vertical_slice.py`

The original `evidence/vertical-slice/` is unchanged. New evidence is under
`evidence/vertical-resource-repair/`.

### Resource receipt implementation

`run_chain_timed` now records actual elapsed time around:

- bootstrap / ordinary / terminal batch calls;
- every actual `P3Owner.realize` event call.

`measure_case` now emits one compact machine-readable receipt containing:

- actual DB/WAL/cycle-logical bytes and per-file bytes, including fixed
  pre-record DB bytes and incremental bytes;
- bytes per record and per event;
- actual source/provenance configuration overhead;
- actual `PsycheStore.stats()` read/write/targeted/full-scan counters;
- an explicit full `store.verify()` timing and row-read delta alongside
  targeted `store.query` counters;
- actual provider context bytes, event-batch count, calls per event batch,
  and calls per cycle;
- two actual retrospective records when the chain completes;
- actual cold-reopen latency;
- E1 B1 numbers explicitly labeled historical, not current measurements.

`run_p3_vertical_slice.py` sets `P3_VERTICAL_METRICS_PATH` to
`evidence/vertical-resource-repair/actual_metrics.json` and preserves the
actual pytest stdout/stderr and failure exit code. It does not manufacture PASS
from metadata or file existence.

Metrics are **NOT_RUN** in this startup because the chain stops at the store
ABI boundary before the two-batch run. No `actual_metrics.json` is claimed.

### Crash/recovery repair

The actual crash fixture now:

- opens the exact existing P2 root with `load_p2().open`, not a new
  `start`/`build_case`;
- reconstructs the same actual source/case/participants and P3 owner;
- stores the initial actual root/payload in the child payload;
- reaches the intended post-base/pre-`save_world` kill;
- reopens the exact same root in the parent and verifies durable recovery and
  one COMPLETE operation.

The cross-root negative test uses two actual roots and refuses source/plan
binding before effects; no fork/inheritance is fabricated or silently migrated.
These definitions are banked but not executed because the shared store block
occurs before their relevant runtime paths.

## Actual execution record

Syntax:

```sh
python3 -m py_compile \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/p3_fixture_support.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/run_p3_vertical_slice.py
```

Result: exit `0` (`evidence/vertical-resource-repair/py_compile.log`).

Focused actual run, once, stopping at the actual shared-store blocker to avoid
repeatedly executing the full known-blocked suite:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
PYTHONPATH=P3:ENGINE:PROJECTION \
python3 -m pytest \
  tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control \
  -q -x -o addopts="" -p no:cacheprovider
```

Result: `1 failed in 7.49s` at
`PsycheStore._plan_authority` -> `PLAN_AUTHORITY_OR_GRADE_MISSING`.
The actual smoke log is the exact failure evidence. The runner was not rerun
against the full known-blocked suite.

The HQ combined run remains preserved at
`evidence/storage_intake_actual.log`: 45 passed, 4 failed, 1 inapplicable
missing-store guard skipped; storage unit run 42 passed. The three owner
positive failures are the same store ABI boundary.

## Coverage map

`evidence/vertical-resource-repair/COVERAGE_MAP.json` maps all 13 test
definitions for PRIMARY, A–H, cross-root, cold/crash, and §11. Only the
PRIMARY test was actually attempted; it failed at the shared store boundary.
The remaining cases are explicitly `NOT_EXECUTED`, not PASS or silently
skipped.

## Source pins

- Store: `40b29d96c359de61fcb62937c08f7cdb73cd68b936247ef2e9219348119586a0`
  (present; ABI blocker)
- P3Owner: `b7b508637258907e4d18df3030b45e040fff83dc6adc992985922e50a9e009f7`
- Test rules: `27272cd43c26b6aa114ee65c97ca07eb56accecbd440841c29696b98e203b4b4`
- Projections: `ca405dda778191537ce38b0b63ff6b6ba8104dcd1ea676d6b458d454b362005b`
- Compression: `49df70d60cbc3b37ec3e484c5a7c64e14ac174faafe8fcaa02e5428c583be4f4`
- P2Owner: `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0`
- Contracts: `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d`
- Fixture support: `5d2dfa081ae9152cbc3fc955d4f3aebebd5f1205f585bab07f655bdae57e550c`
- Vertical tests: `e969d30181d10879b3cd5b73260e2e52121646614c0582144d46232c178d1a1b`
- Runner: `49450f2f8d40187aba956d0368b72ddc187f1261d13dc047e78ef834eb6f770f`

## Runtime / passport

- Assigned model: `opencode-go/deepseek-v4.1-flash#max`
- Runtime observed: `opencode v2.0.22`, Python `3.11.3`, Darwin `22.3.0 x86_64`
- Quota: **UNKNOWN_UNOBSERVED**
- No model/provider/account/region/effort/UI change.

## Known limits / remaining dependencies

- The returned store's plan-provenance ABI must be repaired by its owner. The
  exact frozen `SOURCEFREE_TEST_ONLY` grade is already present; no new
  authority is issued by this harness.
- The store also has a separately reported V3MS kind/hash preservation defect;
  this harness must not bypass or normalize it.
- Until those owner repairs and the owner crash-fixture repair land, the
  actual two-batch PRIMARY/A–H/§11 chain and real resource metrics remain
  **NOT_RUN**.
- No native science, source issuance, ADP-016/017 memory or claim, human
  validity, production, CAS, protected merge, independent review or full P3
  acceptance is claimed.
- The final reviewer must be a distinct nonauthor.

**Code artifact commit:** `31da7feb2ae44b1aff75bc2f6ea346c87a3d38e6`  
The final evidence commit is the branch HEAD after this file; the code artifact
commit above is the exact measured code snapshot. Direct-remote verification is
reported in the final worker return.
