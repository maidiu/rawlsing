# M04I2 — unjournaled and terminal counterexamples

**Candidate reviewed:** M04 target `2309a73bcea1572f6545d5b26027ddc608bee271`, patched helper blob `5ba929f51870b111ca54ca87fdf97338e4295625`.
**Original helper:** blob `2434bda6f4b00e6ea5881291f5422227e8045e74`.
**Frozen test:** blob `8add06c66b347e324443c1263771755f6898c7e2`.
**Original reviewer:** `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`.
**M03 author source:** `e1f7a74e51201b9614bcc578348b4e9db7be7bd3`.

## 1. The three journaled classes are closed at the tested grain

The 51-case frozen reviewer suite was executed from two independently staged cold runtimes. The baseline original helper produced **41 PASS / 10 FAIL**; the patched helper produced **51 PASS / 0 FAIL** in both roots. The ten baseline failures are exactly:

- four `test_cross_cell_none_owner_cannot_erase_first_committed_belief` cases (`NONE`, `CERTAIN`, `UNCERTAIN`, `UNAVAILABLE`);
- four `test_revoked_or_withdrawn_state_cannot_be_resurrected_by_partial_rollback` cases (`False/True` × `SUPERSEDE_EXACT_RECORD/WITHDRAW`);
- two `test_fully_rehashed_transition_requires_actual_prestate_ancestry` cases (`False/True`).

The same frozen bytes pass after the patch. The inherited 413, 100 and 74 suites remain **587/587 PASS** before and after. The separate historical CAN3 nine remain **9 FAIL** and are not part of the 51 or 587.

## 2. Material residual: unjournaled ADP017 terminal route

The patch adds `validate_journaled_transition_ancestry(c)` and calls it from `validate_binding(c)`. That function iterates `c.journal.read_effects("ADP017_COMMIT")` and requires each journaled transition to remain present with its recorded pre-state and post-state. It does **not** iterate `c.ctx.epistemic_transitions` to require that every current transition is journaled, and `validate_consumption(c, at)` binds the terminal snapshot to `transitions[-1]` without requiring a matching journal entry. The author's own Limits section states direct unjournaled ADP017 calls are covered only to the extent exercised by the frozen tests; the frozen 51 do not exercise it.

### 2.1 Direct owner-API variant (primary)

Executed by `WORKER_RETURNS/M04I2-R3/candidate/m04i2_unjournaled_probe.py --variant direct`:

1. `Cell().prepare('CERTAIN','BELIEF')` produces one journaled ADP017 transition.
2. A **journaled** `SUPERSEDE_EXACT_RECORD` to `CLAIM_INACCESSIBLE` revokes first-person access.
3. A direct `owner.adp017_apply_epistemic_effect` call with `SUPERSEDE_EXACT_RECORD` back to `CLAIM_ACCESSIBLE`, targeting the revoked effect, is made **without** a journal commit.
4. `read_owner(..., '1998-11-20T09:00:00Z')` is called.

Observed on both original `2434` and patched `5ba929`:

```json
{
  "variant": "direct",
  "before_direct": {
    "state_transitions": 2,
    "journaled_adp017": 2,
    "active_stances": 1,
    "accessibility": "CLAIM_INACCESSIBLE"
  },
  "after_direct": {
    "decision_state": "APPLIED_EPISTEMIC_TRANSITION",
    "state_transitions": 3,
    "journaled_adp017": 2,
    "active_stances": 1,
    "accessibility": "CLAIM_ACCESSIBLE"
  },
  "result": {
    "read": "ACCEPTED",
    "streams": {"memory": "BUFFER", "epistemic": "REROUTE"},
    "disposition": "BOUND_CANONICAL_CLAIM_WITH_NATIVE_STATE",
    "rollback_unchanged": false
  },
  "exit": 2
}
```

The journal still contains only the original ADD and the real revocation. The unjournaled restore is the terminal transition, and the read returns `REROUTE` as if the revocation had never occurred. This is a direct terminal-rollback bypass plus an unjournaled ADP017 route.

### 2.2 Unjournaled forged-pre-state variant

Executed by `.../m04i2_unjournaled_probe.py --variant forged`:

1. `Cell().prepare('CERTAIN','BELIEF')` produces one journaled transition.
2. A new transition is appended whose `pre_state_hash` is a fabricated digest, with its effect ID, transition ID, stance set, snapshot and permission recomputed coherently.
3. The original journal entry is left intact; no journal entry is added for the new transition.
4. `restore(packet)` succeeds and `read_owner` succeeds.

Observed on both original `2434` and patched `5ba929`:

```json
{
  "variant": "forged",
  "before_direct": {"state_transitions": 1, "journaled_adp017": 1, "active_stances": 1, "accessibility": "CLAIM_ACCESSIBLE"},
  "after_direct": {"state_transitions": 2, "journaled_adp017": 1, "active_stances": 1},
  "result": {
    "read": "ACCEPTED",
    "streams": {"memory": "BUFFER", "epistemic": "REROUTE"},
    "disposition": "BOUND_CANONICAL_CLAIM_WITH_NATIVE_STATE",
    "rollback_unchanged": false
  },
  "exit": 2
}
```

This is the same pre-state-ancestry attack the patch is intended to stop, but routed through an unjournaled transition instead of modifying the journaled transition. The frozen `test_fully_rehashed_transition_requires_actual_prestate_ancestry` modifies the journaled transition and is caught; an appended unjournaled transition is not.

### 2.3 Why the current patch does not close it

The patch proves that each **journaled** transition is still present and matches its journal entry's `before` and recorded post-state. It does not prove the converse: that the terminal transition used for consumption is itself in the journal. The terminal checks are:

```python
transitions = [t for t in c.ctx.epistemic_transitions if t["effect"]["claim_ref"] == selected]
...
require(transitions and snapshot["last_transition_ref"] == transitions[-1]["transition_id"],
        "CLAIM_LAST_TRANSITION_TERMINAL")
require(snapshot["current_state_hash"] == transitions[-1]["post_state_set_hash"],
        "CLAIM_LAST_TRANSITION_STATE")
```

There is no `journal entry -> terminal transition` or `terminal transition -> journal entry` equality. The journal check and the terminal check are not joined.

### 2.4 Required correction direction (not implemented by this reviewer)

The original author must add a positive journal-coverage check, for example:

- every transition used as the terminal transition for a selected claim has exactly one `ADP017_COMMIT` journal entry;
- the journal entry's recorded transition ID, pre-state, post-state set hash and owner-state `after` match the terminal transition and current owner state;
- any `ctx.epistemic_transitions` entry without a matching journal entry is rejected before consumption;
- new tests cover the direct unjournaled `SUPERSEDE_EXACT_RECORD` and unjournaled forged-pre-state variants above.

A check that only iterates journal entries and never verifies that every transition is journaled is insufficient. A test that only modifies the journaled transition is also insufficient.

## 3. Terminal-rollback and pre-state lineage

The journaled terminal-rollback and pre-state classes are closed by the patch at the frozen-test grain:

- `test_revoked_or_withdrawn_state_cannot_be_resurrected_by_partial_rollback[False/True × SUPERSEDE_EXACT_RECORD/WITHDRAW]` passes after patch.
- `test_fully_rehashed_transition_requires_actual_prestate_ancestry[False/True]` passes after patch.

The residual is specifically the **unjournaled** route, not a failure of those journaled tests. The historical CAN3 nine remain separate and unchanged.

## 4. Replay commands

```bash
# Cold reconstruction (reviewer harness; use a scratch root, not the original return tree)
python3 repro/stage_independent.py
python3 repro/install_candidate.py

# Baseline original helper 2434
python3 review/run_fresh.py            # 41 passed, 10 failed, exit 1
python3 repro/run.py after original_413  # 413 passed
python3 repro/run.py after independent_100  # 100 passed
python3 repro/run_author.py            # 74 passed
python3 repro/run_historical.py        # 9 failed, expected

# Install patched helper 5ba929 at runtime/m02/runtime/m01/repro/claim_provenance.py
python3 review/run_fresh.py            # 51 passed, exit 0
python3 repro/run.py after original_413  # 413 passed
python3 repro/run.py after independent_100  # 100 passed
python3 repro/run_author.py            # 74 passed
python3 repro/run_historical.py        # 9 failed, expected

# Independent counterexamples
python3 candidate/m04i2_unjournaled_probe.py --runtime <runtime>/m02/runtime/m01/repro --variant direct
python3 candidate/m04i2_unjournaled_probe.py --runtime <runtime>/m02/runtime/m01/repro --variant forged
```

Expected counterexample result is `read: ACCEPTED`, `epistemic: REROUTE`, `exit: 2` on both original and patched helpers. That is the RED finding of this review.

## 5. Evidence

- `evidence/fresh_baseline_junit.xml` — 51 tests, 10 failures.
- `evidence/fresh_patched_junit.xml` — 51 tests, 0 failures.
- `evidence/cold2_fresh_baseline_junit.xml` — 51 tests, 10 failures.
- `evidence/cold2_fresh_patched_junit.xml` — 51 tests, 0 failures.
- `evidence/historical_nine_junit.xml` — 9 tests, 9 failures (retained-JUnit replay).
- `evidence/unjournaled_probe_original.json`, `..._patched.json`, `..._patched_cold2.json` — direct route.
- `evidence/forged_prestate_probe_*.json` — forged-pre-state unjournaled route.
- `evidence/01_INPUT_SOURCE_IDENTITIES.json` — 457-file pinned source reconstruction manifest.
- `01_REPLAY_JUNIT_AND_SOURCE_HASHES.json` — exact counts, exits and hashes.

No test was edited or skipped. No native CAN3/ADP/Pyat science is claimed. The nine historical failures remain original-owner RED.
