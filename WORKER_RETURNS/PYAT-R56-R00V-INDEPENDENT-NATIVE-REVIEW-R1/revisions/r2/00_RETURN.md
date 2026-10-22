# PYAT R56 R00V-R2 — independent requalification of repaired R00E

**VERDICT:** `REVISE__GATE_BEHAVIOR_REQUALIFIED__CUSTODY_MANIFEST_AND_SUMS_STALE`.
**ROLE:** same independent R00V reviewer as `140c41d6…`; not R00E implementer, R00P owner or native/original issuer.
**MODEL / HARNESS:** DeepSeek V4.1-Flash, reasoning MAX, I2-I3, OpenCode local, mainMac. One agent; no subagents; external model calls 0; usage/cost UNKNOWN.
**CANDIDATE / STARTUP:** `3d4d77e9b667a1cddac07c3bfdda7d8795de458d`.
**SUCCESSOR BRANCH:** `agent/rabochii-pyat-r56-r00v-r2-gate-requalification-r1`.
**EVIDENCE COMMIT:** `d768c675661f0d3026a468aa92ab4bcd65b25837`.
**REMOTE SHA:** branch HEAD read back after the final non-force push; exact value in the handoff/git readback (not embedded, to avoid a self-referential commit).

## Four-column return

| FINDING | INTERPRETATION / RIVALS | HQ ACTION | OWNER |
|---|---|---|---|
| **F1. The repaired gate passes the targeted behavior requalification.** All 8 original R00V defects now produce secure HOLD/REFUSE outcomes; all 36 frozen cases pass with independently recomputed policy blobs; valid local subsets, reverse order, typed identity, and lawful occurrence transport survive. | Gate logic is materially repaired at TEST_ONLY policy scope. This is not native/R09/original acceptance. | `ACCEPT_SCOPED_LOCAL` for gate behavior, subject to custody fix. | R00V / R00E |
| **F2. The candidate successor custody manifest is stale.** `manifest.json` records wrong hashes for `evidence/passport.json` and `evidence/manifest_supersession.json`; the candidate return says the manifest is exact. | This is a packaging defect, not a gate-transition defect. The manifest was generated before two later receipt files were written. | **REVISE**; same implementer must regenerate manifest after all receipts. No gate architecture change. | R00E |
| **F3. Candidate `SHA256SUMS.txt` has two unresolvable code/test paths** (`../../CROSS_HQ…`, `../../tests/…`). | The manifest has correct root-relative code/test paths, so evidence remains recoverable; the sums file is not independently resolvable as written. | **REVISE**; use declared root-relative paths or correct sums-relative paths. | R00E |
| **F4. All same-assertion fault/restore and shared-contract obligations pass.** Fresh-process baseline ALLOW → policy-operation fault REFUSE_FRONTIER → restore ALLOW. External shared refs were read; candidate changed-test gate passes; reviewer tests are independent. | Real local execution receipts, not policy identity lists alone. | Retain as requalification evidence. | R00V |
| **F5. Native/original/R09 remain unheld.** Gate-only local Python does not qualify a survey, C11, native events, original35 or N11/N12. | Preserve all holds. | No native promotion. | R09/native/original owners |

## Defect requalification

| Original defect | Repaired decision | Reviewer assertion |
|---|---|---|
| D1 executed native without evidence | `HOLD_TRUSTED_NATIVE` | PASS |
| D2 supported completion without evidence | `HOLD_TRUSTED_NATIVE` | PASS |
| D3 prohibited → completed observed-zero | `REFUSE_STATUS` | PASS |
| D4 semantic mutation masked by status edit | `REFUSE_FRONTIER` | PASS |
| D5 unknown grade/kind | `REFUSE_AUTHORITY` | PASS |
| D6 duplicate/unknown occurrence objects | `REFUSE_FRONTIER` | PASS |
| D7 handle contract mismatch | `REFUSE_PIN` | PASS |
| D8 ELIGIBLE → HELD disposition | `REFUSE_STATUS` | PASS |

Additional independent checks: valid full occurrence transport ALLOW; semantic occurrence mismatch/unsupported transport REFUSE; unknown submitted kind/native claim REFUSE; semantic mutation masked by disposition edit REFUSE; handle version mismatch REFUSE; invalid status values/unknown edit IDs REFUSE; simultaneous faults cannot return local ALLOW.

## Executed receipts

- `evidence/reviewer_replay.json` — **36/36** frozen cases, independent pin.
- `evidence/defect_requalification.json` — **8/8** defects repaired.
- `evidence/junit/r00v_r2.xml` — **41 tests, 0 failures/errors/skips** (24 candidate + 17 reviewer).
- `evidence/dependency_fault.json` — ALLOW → REFUSE_FRONTIER → ALLOW in separate processes.
- `evidence/candidate_changed_test_gate.json` — candidate tests pass mechanical proof gate.
- `evidence/reviewer_changed_test_gate.json` — reviewer tests pass mechanical proof gate.
- `evidence/candidate_custody_recheck.json` — **2 manifest stale entries, 2 sums path failures**.
- `evidence/proof_witness.json` — reviewer test/replay/defect/JUnit/dependency hashes.
- `evidence/session.json`, `evidence/passport.json` — actual reviewer session/host/model/usage.
- `evidence/shared_contract_requalification.json` — exact external shared-contract reads and obligations.

## Smallest custody repro

```bash
cd <candidate worktree>
R=WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/revisions/r2
shasum -a 256 $R/evidence/passport.json $R/evidence/manifest_supersession.json
python3 - <<'PY'
import json, hashlib
from pathlib import Path
R = Path("WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/revisions/r2")
m = json.loads((R/"manifest.json").read_text())
for row in m["files"]:
    p = Path(row["path"])
    if p.name in {"passport.json", "manifest_supersession.json"}:
        print(p.name, row["sha256"], hashlib.sha256(p.read_bytes()).hexdigest())
PY
```

Observed:
- `manifest.json` records `passport.json` as `e1663d7e…`; actual `fac1dc32…`.
- `manifest.json` records `manifest_supersession.json` as `da2d8072…`; actual `70177f0f…`.
- `SHA256SUMS.txt` entries `../../CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py` and `../../tests/universal_execution_oracle/test_r00e_r2_reviewer_regressions.py` resolve to nonexistent paths from the candidate root/evidence/root.

General rule: generate the manifest in a second pass after all receipts, then generate sums with a declared root and self-exclusion; never claim exact hashes for files written after scanning.

## Three courts

| Court | Verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `ACCEPT_SCOPED_LOCAL__GATE_BEHAVIOR`; `REVISE` return custody | No native execution. |
| **SCIENTIFIC** | `NO_SCIENTIFIC_CLAIM` | Policy fixtures only. |
| **AUTHORITY** | `HOLD` | R09, native/original, N11/N12, production unissued. |

## Limits

- No R09, native event, actual consumer, survey/decoder, original35, N11/N12 or A5 evidence.
- Same-process `PinnedPolicyHandle` supervisor trust remains explicit; no arbitrary supervisor-process resistance claimed.
- Candidate custody defect is the only persisting defect found; gate behavior passes.
- Original R00V evidence at `140c41d6…` remains untouched; this successor does not rewrite historical xfail evidence.
- No policy/foreign return edits, source access, protected CI, production promotion or other R-node work. J52/W52 remain stopped.

Stop for the same R00E implementer to fix the manifest/sums custody and then return for finite acceptance. No new architecture or policy oracle change.
