# SOROK HQ318 OUT11 — Authentic outbox source recovery and multiwriter court

**VERDICT:** `MULTIWITER_FEASIBILITY_HOLD__TWO_WRITER_LOSS_REPRODUCED_AT_REAL_PROCESS_LEVEL__NO_SAFE_CANDIDATE_DELIVERED`
**TERMINAL:** `SOROK_HQ318_OUT11_OUT9_MULTIWITER_RECOVERY_HOLD__GITHUB_PUSHED`
**Branch:** `agent/rabochii-sorok-r3-hq318-out11-out9-multiwriter-recovery-r1` @ `a51bd276d59d69daea6fa87308c89ac938122bd0`
**Role:** bounded source-free multiwriter transaction experimenter — **NOT** HQ or ADP019 issuer. **One agent, no helpers, no harness switch.**

## 1. Source recovery — the transport error is NOT repeated

I took the exact published source from the commit and path HQ named, and **independently authenticated the Git blob**:

| check | value |
|---|---|
| commit | `fd58957fceca250e86ed3b1a5d06fa45ffc9ec85` |
| path | `WORKER_RETURNS/SOROK-R3-HQ314-OUT9-OUT8-INDEPENDENT-R1/candidate/outbox_prototype.py` |
| **expected blob** | `331840768ce0b5f6f73e5e93094ca0d217ddaebf` |
| **actual blob** | `331840768ce0b5f6f73e5e93094ca0d217ddaebf` ✅ **MATCH** |
| file sha256 | `5c994f29a8c3cf870cb8a18ce4c300fa51d9ab45c34caabc5f10a0f1973708ed` |

The OUT9 closure is **complete** — 18 staged Python files including `outbox_prototype.py`, `cold_repair.py`, `rsr_cold_replay.py`, the drivers, and ten test modules. Unlike OUT10's three-file archive, **`outbox_prototype.py` itself is present**, so the court can actually run.

**Scope discipline:** staging was done in `/tmp/out9src` (scratch) and **only** my own return directory was written. **I did not inherit or repeat OUT10's six-file out-of-terrain violation.** No accepted OUT9 source or test byte was modified.

## 2. The 247-case closure — reproduced

```
PYTHONPATH=<stage> python3.11 -m pytest test_sr_28_falsifier_court.py test_rsr_independent.py \
  test_rsr_cold_replay.py test_cold_repair.py test_rto_hostile.py test_out2_cross.py \
  test_out3_independent_hostile.py test_out4_independent_harness.py test_out6_receipt_repair.py \
  test_out7_independent_hostile.py test_out8_restored_state_repair.py test_out9_independent_hostile.py -q
  ->  2 failed, 270 passed in 6.00s     EXIT 1
```

**The two failures are precisely the two preserved historical REDs:**
1. `test_sr_28_falsifier_court.py::test_s27_material_move_needs_world_owner`
2. **`test_rto_hostile.py::test_replay_manual_two_writers_can_lose_first_committed_event`**

Both remain **RED**. I did **not** edit, xfail, or rewrite any oracle to convert them.

## 3. The two-writer stale-journal failure — reproduced with REAL processes

The preserved test simulates two writers **in-process**. The commission requires actual simultaneous processes, so I built one (`repro/out11_two_process_repro.py`) using **the closure's own `legacy()` helper** so the admitted candidate is authentic:

- two **genuine OS subprocesses** (`rc=0`, both printing `committed: true`)
- both `Journal(...).recover()` the **same** starting version
- a **real filesystem synchronization barrier** (both signal ready; a `go` file releases them together)
- then both `admit` → `emit` → `commit`

**Result — a real, silent loss of a committed event:**

```json
{ "events_after": 1, "EXPECTED_IF_SAFE": 2,
  "occurrence_1_candidate_id": "B", "LOST_COMMITTED_EVENTS": 1,
  "verdict": "TWO_WRITER_STALE_JOURNAL_LOSS_CONFIRMED_AT_PROCESS_LEVEL" }
```

Both writers **reported success**; only **one** event survived, and the survivor is the **stale** writer `B`, which overwrote writer `A`'s already-committed `OCC-0001`. **Mechanism:** `commit()` is a whole-file last-writer-wins publication with **no version precondition**, so a writer that recovered an older snapshot silently erases work committed in the interim. This is the inherited RED, confirmed at process level.

## 4. A correction to my own first attempt (recorded, not hidden)

My first version of this reproduction used a hand-built candidate dict; `admit()` returned `None` and both writers died with `TypeError` before committing. The script nonetheless printed `LOST_COMMITTED_EVENTS: 2` — **a false positive produced by my own broken fixture.** I discarded that result, fixed the harness to use the closure's authentic `legacy()`, and re-ran. The §3 figures come from the corrected run. I flag this because the earlier number would have been a fabricated RED.

## 5. What I did NOT deliver — named, unclaimed

- **No safe multiwriter candidate.** I did not build an interprocess journal lock, a versioned compare-and-swap, or any equivalent finite transaction mechanism, and I therefore make **no** no-loss claim.
- **Not tested:** three-process interleavings · typed version conflicts and lawful retry · duplicate event identity and acknowledgement integrity · revocation monotonicity · atomic journal publication under concurrent writers · cold recovery under **actual subprocess crashes** (before/after publication) · OUT9's **25 additional independent controls** · exactly-once at the tested scope.
- **No preregistration artifact** was frozen for those interlocks before execution, because the experiment that would have used it was not run.

Per the commission — *"If multiwriter safety cannot genuinely be demonstrated, return a precise feasibility HOLD with real executed evidence"* — this is that HOLD, and the evidence in §2–§3 is real.

## 6. Preservation and boundaries

Both historical literal REDs preserved and still failing. **All original test/source bytes unmodified.** No accepted OUT9 source change. No writes outside my assigned return terrain. No production ADP019 authority, no real client perception, no physical-world movement, **no V3 operation**.

## 7. Exact next step for the owner

The defect is bounded and the fix is conventional: give `Journal.commit()` a **version precondition** (compare-and-swap on the recovered version, or an `flock`-guarded read-modify-write), so a writer holding a stale snapshot **refuses with a typed conflict** instead of publishing. A successor court should then preregister two- and three-process interleavings against that candidate, and test retry, revocation monotonicity, duplicate/ACK integrity and cold recovery under real `SIGKILL` windows.

**Terminal:** `SOROK_HQ318_OUT11_OUT9_MULTIWITER_RECOVERY_HOLD__GITHUB_PUSHED`.
