# PROGRAMMA PYAT L03 R03 — focused capacity-miss guard review

**Status:** `ACCEPT_FOCUSED_EARLY_MISS_GUARD` for
`9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`; `WHOLE_L03_NOT_COMPLETE`.
**Reviewer:** same independent R03 reviewer. Earlier `ACCEPT_SCOPED_P2` for
`409be32f7e4b4b961a360be1c8f44a17b5c62173` (review `e2f6c164...`) and the phase-3
compact assessment `5dfef26d...` are preserved, not rewritten or extended to whole
L03.
**Frozen implementation/test:** `9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`
**Capacity evidence commit:** `2a41b4682cfbbdc2b5e12ba71d114adb431c670f`
**Published head:** `ba5783cbc79ee6541194f6bed400af321250eb8a`
**Exact-head checkout:** isolated detached worktree under
`.local-logs/pyat-l03-r03/checkout-9a5c`; published review history remains intact.
No production edit, protected branch, guide, cache/default policy, or source
adoption was performed.

## Verdict

| Field | Verdict | Basis |
|---|---|---|
| New production delta scope | **PASS** | Only `_miss_capacity_exhausted` plus its call in `evaluate`; test file gains four tests; no other production/test file changes between `141df637` and `9a5c` |
| Early guard on MISS after HIT | **PASS** | Existing HIT path is evaluated before the guard; independent gate and 15-test suite |
| Full-capacity HIT reuse | **PASS** | A core at `max_groups=1` is still hit/reused; no early fallback on the hit |
| New MISS avoids core builder | **PASS** | Independent monkeypatch counted `_evaluate_index_group_core` calls = 0; same facts as no-scope |
| Normal query/authority/identity/refusal not skipped | **PASS** | Normal miss fact parity; authority-DENY, unsupported-topology, and W2 weight-refusal with a full scope all produced the same typed negative as no-scope |
| Member cap exhausted vs unknown prospective size | **PASS** | Exhausted member cap early-falls back without build; unknown prospective denominator still builds then uses the post-build fallback |
| Receipt counters honest | **PASS** | `core_build_attempts`, `core_builds`, `core_hits`, `capacity_fallbacks`, `early_capacity_fallbacks` are consistent in independent receipts |
| Cleanup/error unchanged | **PASS** | No close/error-path change; the 15-test focused suite (including the earlier cleanup test) passes |
| Focused tests | **PASS** | 15 passed in 6.91 s at exact `9a5c` |
| Author capacity receipts | **PASS_SCOPED / AUTHOR_GRADE** | Receipts internally consistent; before/after/no-scope medians match the author’s claim; timings are author-grade and not re-timed by R03 |
| Physical / W03/W04 | **UNCHANGED / NOT COMPLETE** | Guard is a bounded capacity behavior fix; compact cold/peak-memory deficit and default-persistent boundary remain unresolved |
| Whole L03 | **NOT_COMPLETE** | No whole-L03 completion is claimed |
| R03 disposition | **ACCEPT_FOCUSED_EARLY_MISS_GUARD** | Focused new delta accepted; no performance claim by reviewer |
| Next work | **STOP** | No new court/architecture/default policy; author retains economics/profile allocation |

## Exact new delta

Between `141df637d49281fa1d33fa6ad275e09f0f6bd9d4` and
`9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3`:

- `rawlsing_next/pre553_empirical_query.py` (+25/−3): adds
  `I03GroupedExecutionScope._miss_capacity_exhausted(cached_members)`, calls it
  after the HIT path and before `_evaluate_index_group_core`, adds
  `early_capacity_fallbacks` to the receipt, and keeps the existing post-build
  prospective-member check.
- `rawlsing_next/tests/test_pre553_i03_grouping.py` (+128): four focused tests.
- No other production/test files changed.

`git diff --name-only 409be32..9a5c -- rawlsing_next/` contains only
`pre553_empirical_query.py` and the grouping test; earlier phase-2 grouped files
are unchanged. Production/test blobs are identical at `9a5c`, `2a41b4682`, and
`ba5783cbc`.

## Focused behavior verified

Using the actual `CarrierNeutralResearchExecutor.execute_i03` and
`I03GroupedExecutionScope` at exact `9a5c`:

1. **Fill + HIT at group capacity.** `max_groups=1`: first operation builds one
   core; a second identical operation hits it. Receipt: builds 1, hits 1,
   early 0, capacity 0.
2. **Early MISS.** A different target-plan operation on the full scope triggers
   the guard. The core builder is not called, facts equal no-scope, receipt:
   attempts 1 (unchanged), builds 1, hits 1, early 1, capacity 1.
3. **Restored HIT.** The original operation still hits after the early miss;
   hits becomes 2; early/capacity stay 1.
4. **Authority DENY on the full scope.** The normal `UNAVAILABLE` /
   `MISSING_REQUIRED_AUTHORITY` negative matches no-scope and the scope receipt
   is unchanged (the prechecks still run).
5. **Unsupported topology on the full scope.** `UNRESOLVED` /
   `UNSUPPORTED_RESPONSE_TOPOLOGY` matches no-scope; scope receipt unchanged.
6. **W2 weight refusal after an actual early MISS.** A different target plan with
   `GOVERNED_WEIGHTED` and no W2 weights takes the early fallback, then the
   unshared path still runs weight validation and publishes the same
   `UNAVAILABLE` / `MEASURE_UNAVAILABLE` negative. Early and capacity counters
   each increment by one; `core_build_attempts` does not increase.
7. **Member cap already exhausted.** With `max_cached_members=1` and a cached
   one-member core, a new larger-denominator operation early-falls back without a
   builder call; facts equal no-scope.
8. **Unknown prospective member size.** With `max_cached_members=1` and a
   24-member new core, cached members are below the cap so the guard does not
   fire; the existing post-build check falls back honestly: attempts 1, builds 0,
   early 0, capacity 1; repeated operation attempts 2, builds 0, early 0,
   capacity 2.
9. **Close.** `close()` clears groups and reports `closed: true`,
   `open_groups: 0`.

The independent gate receipt is in `evidence/early_miss_gate.json`. The focused
15-test suite passed at exact `9a5c` in 6.91 s.

## Author capacity receipts: consistency only

The author’s `capacity_summary.json` at `2a41b4682` reports N=200, 3 rounds,
`raw_Y` fill / `joint_XYZK` miss:

| Side | Miss median | Attempts | Builds | Hits | Early | Capacity | Facts |
|---|---:|---:|---:|---:|---:|---:|---|
| before | 0.3383 s | 2 | 1 | 1 | 0 | 1 | equal |
| after | 0.2001 s | 1 | 1 | 1 | 1 | 1 | equal |
| no-scope | 0.1989 s | — | — | — | — | — | equal |

These medians match the author’s claim (0.3383 / 0.2001 / 0.1989) and the
before/after counters match the intended guard effect. The “before” side is new
code with `_miss_capacity_exhausted` forced to `False` (guard-disabled A/B), not a
run of old commit `409be32`; that is acceptable for isolating the guard effect but
should be read as such. **R03 did not run a timed benchmark and makes no
performance/timing claim.** Author economics remain author-grade.

## W03/W04 and full-L03 status (unchanged)

- W03/P01 exact composed function: **present**, unchanged.
- W03/W04 economical compact capability: **not fulfilled**; compact cold/peak
  memory remains higher than native and warm cache did not materially improve
  total wall at N=1,000 in the phase-3 evidence.
- W04 default persistent acceleration: **competent-owner/default-policy
  boundary**, not a missing codec/engine; no blanket cache default.
- The capacity guard is a bounded capacity-cost improvement; it does not complete
  W03/W04 or whole L03.
- No original35, production, native/science, actor/human, Sorok, or cache-policy
  grant is claimed.

## PROGRAMMA_DELTA (ordinary return)

- `ROADMAP:S03.3`, W05/P03: **early cache-MISS capacity guard accepted at
  `9a5c` for the bounded capacity behavior; HIT reuse, normal query/authority/
  refusal, unknown-prospective fallback, counters, and cleanup verified.**
- Capacity fallback: **guard avoids duplicate core construction when the cache is
  already at the group/member bound; existing post-build prospective-member
  fallback retained; no eviction/LRU/default change.**
- `ROADMAP:S03.2`, W03/W04: **status unchanged; exact composed function present,
  economical cold/peak-memory capability and default persistent activation remain
  unresolved; WHOLE_L03_NOT_COMPLETE.**
- P2 acceptance: **earlier `409be32` / `e2f6c164` scope preserved; `5dfef26d`
  phase-3 assessment preserved; this focused acceptance does not extend to whole
  L03 or author economics.**
- No new court, architecture, global config, cache default, or production merge.

## Artifact map

- `01_FOCUSED_REVIEW.md` — exact delta, isolation, tests, evidence boundary.
- `02_COMMANDS_AND_NOT_RUN.jsonl` — commands and explicit NOT_RUNs.
- `03_W03_W04_STATUS.md` — unchanged W03/W04/full-L03 status.
- `evidence/early_miss_gate.json` — independent gate receipt.
- `evidence/capacity_receipt_consistency.json` — author receipt consistency extract.
- `reproducers/early_miss_gate.py` — reviewer-authored focused gate.
