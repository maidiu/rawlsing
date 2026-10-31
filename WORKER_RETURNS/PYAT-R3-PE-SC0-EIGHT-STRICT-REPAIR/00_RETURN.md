# PYAT R3 — PE-SC0 eight strict failures: sourcefree value-bearing overlay

**Role:** independent bounded sourcefree repair engineer. Not PRE-MAIN
integrator, N9/source issuer, original PE reviewer, or own hostile reviewer.

**Repository:** `maidiu/rawlsing` (private).

**Branch:** `agent/pyat-r3-pe-sc0-eight-strict-failure-repair-20261031-r1`.

**Startup:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`.

**PRE-MAIN intake at return start:** `87755f02ec5c37499b09e80db6fbdcc9316a6b15` (no PRE-MAIN write).

**Executor:** OpenCode / `opencode-go/deepseek-v4.1-flash`. Isolated worktree;
no production source or PRE-MAIN write; no external paid call.

**Write scope:** only `WORKER_RETURNS/PYAT-R3-PE-SC0-EIGHT-STRICT-REPAIR/`.

## FINDING

The eight remaining strict failures are genuine missing PE receipt semantics:
the pinned PE candidate carries N9 dependency identity but no value-bearing
world fields, no four clocks, no negative-status algebra, no H2 refresh
receipts, no values-read receipts and no generic consumers.

The prior scoped return `9647d851a2d9b6e93e6711eec7a65325fb83aaa1` closed the
reversed-issuer defect but still left eight strict gaps (5 strict passed / 8
failed). This return starts from that finding and closes all eight at
**sourcefree fixture-overlay scope**:

- The pinned PE module `58484f4c3d9aae148d4116dcf00420c432aefcbd` is unchanged.
- An overlay runs only after the original PE service returns `EXACT_SUPPORTED`.
  It attaches values from the executed HQ298 SC0 fixture provider and from the
  original PE/C1/N10E receipt.
- The 13 strict assertions are unchanged. The strict court blob remains
  `d2fe653dadf94893b0fdfd268f36683f8dfed9af`.
- One disclosed test-only fixture support patch registers a
  `TARGET_USE_PERMISSION` snapshot so the repaired positive reverse path can be
  exercised. It changes no assertion and grants no production authority.
- `n10e_values_read_receipt` uses the actual PE geometry, not the SC0 54/60
  baseline: reverse `P1` is 48/64; the Law A conception target `yes` is 21/30.
- Reversed-issuer forgery is refused at the overlay boundary with
  `REVERSED_UNAUTHORIZED_ROLE` and no geometry or value enrichment.

The result is **not** a production PE repair. The pinned PE contract used
without the overlay remains red on the same strict court.

## ACTUAL TESTS

Exact PE tree `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65`, extracted fresh by
the repro scripts.

| Court | Actual result |
|---|---|
| Original author 21 | **21 passed** |
| Original independent strict 13 | **4 passed / 9 failed** (preserved) |
| Overlay author 21 | **21 passed** |
| Overlay independent strict 13 | **13 passed** |
| Overlay positive + fault negatives | **9 passed** |

Commands:

```bash
./repro/run_original_red.sh
./repro/run_overlay_courts.sh
```

JUnit/log receipts are under `repro/`; `repro/test_summary.json` records the
same counts. The overlay fault court covers wrong issuer, invalidated snapshot,
missing producer, severed consumer, generated-binding source promotion and
missing publication clock. All fail closed.

## WHAT WAS DONE

- Reproduced the original PE red: author 21/21, strict 4/13.
- Reproduced the prior repaired `_auth` behavior; the overlay restores the
  exact-issuer dereference at its boundary without editing the pinned module.
- Reused the HQ298 SC0 fixture port (`b15dbbc4...`) for world values and two
  generic consumers; 13/13 port/oracle files are blob-identical to that commit.
- Added `candidate/sc0_pe_overlay.py` with fail-closed validation of producer,
  consumer, clocks, status algebra, refresh channels and binding echo.
- Added `candidate/PE_TEST_FIXTURE_AUTHORITY.patch` for the test-only positive
  reverse snapshot.
- Added the 9-test overlay court and reproducible original/overlay scripts.
- Wrote the eight-line adjudication and the five supporting return documents.

## WHAT DID NOT CHANGE

- No PE module edit, no strict assertion edit, no production fixture edit.
- No `rawlsing_next/` production change, no PRE-MAIN change, no merge.
- No original survey/response bytes, source release, operative N9, N10W joint
  model use, actor/person state, N11/N12, V3 wake or scientific adoption.
- No production consumer or refresh integration.

## SCIENCE / AUTHORITY

Engineering: **CLOSED AT SOURCEFREE OVERLAY SCOPE** for the eight strict
assertions and the reversed-issuer fault.

Science: **HOLD** — all values are synthetic fixture values; fractions are
exact synthetic-source arithmetic, not real-population probability or causal
effect.

Authority: **HOLD** — no source/actor/model-use/adoption grant; the test
fixture reversal snapshot is not a real issuer; integration and independent I3
review remain required.

## OWNER ACTION

1. Preserve this return as sourcefree overlay evidence only.
2. Route the eight field semantics and the test-only fixture registration to
   the original PE/SC0 owner for a decision on a real successor contract.
3. Do not satisfy production integration by installing `sitecustomize.py` or
   applying the fixture patch.
4. Require independent I3 hostile review at the exact pushed SHA before any
   canonical integration.
5. Do not claim pinned PE READY, operative N9, N10W model use or adoption.

## RETURN ARTIFACTS

- `00_RETURN.md`
- `EIGHT_STRICT_ASSERTION_ADJUDICATION.jsonl`
- `ORIGINAL_VS_CURRENT_SOURCE_CONSUMER.md`
- `POSITIVE_AND_FAULT_NEGATIVE_RECEIPTS.md`
- `SCIENCE_AND_AUTHORITY_HOLDS.md`
- `INTEGRATION_AND_ROLLBACK.md`
- `candidate/sc0_pe_overlay.py`
- `candidate/sitecustomize.py`
- `candidate/PE_TEST_FIXTURE_AUTHORITY.patch`
- `candidate/port/`, `candidate/oracles/` (HQ298 `b15dbbc4...`)
- `tests/test_pe_sc0_overlay_court.py`
- `repro/run_original_red.sh`, `repro/run_overlay_courts.sh`
- `repro/*.log`, `repro/*.junit.xml`, `repro/test_summary.json`,
  `repro/port_source_manifest.json`

Exact pushed remote SHA is reported in the completion message and is not
self-referenced inside its own commit.

TERMINAL: `PE_SC0_EIGHT_STRICT_CLOSED_AT_SOURCEFREE_OVERLAY__21_AUTHOR_PASS__13_STRICT_PASS__9_OVERLAY_FAULTS_PASS__PINNED_PE_UNCHANGED__NO_ADOPTION__NO_MERGE`.
