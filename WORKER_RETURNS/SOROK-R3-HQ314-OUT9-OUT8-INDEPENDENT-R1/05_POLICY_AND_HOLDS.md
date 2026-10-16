# HQ314 OUT9 — policy HOLDs, unpublished-source HOLD, model/privacy HOLDs

This engineering court decides **none** of the following. They are preserved
verbatim as competent-owner HOLDs.

## OUTP normative HOLDs (unchanged, preserved)

| ID | Question | Status |
|---|---|---|
| OUTP L1 | implicit minimal legacy fixture grammar (no-authority compatibility fixtures may satisfy aggregate scalars) | **HOLD** — competent owner must decide prospectively |
| OUTP L2 | explicit fixture tag requirement (legacy fixtures must carry an explicit tag) | **HOLD** — same |

The candidate source under review explicitly comments that no-viewer legacy
fixture scalar ACK "remains legacy-only pending OUTP L1/L2 and A1/A2
competent-owner decisions; this condition does NOT require projection
opportunity or assert perception" (OUT8-patched `validate_state`). My tests
exercise both strict grade (`SOURCEFREE_BOUND_DECIDER_NOT_OWNER`) and the
inherited legacy fixture behavior **without selecting** either policy.

| ID | Question | Status |
|---|---|---|
| OUTP A1 | transport ACK = client-observed transport acknowledgment | **HOLD** |
| OUTP A2 | prior projection-opportunity ACK | **HOLD** — same |

The aggregate-ACK/congruance checks this court verifies are the *seam
invariants* the repair implemented regardless of which policy is later chosen
(forged aggregate ACK without a genuine client receipt must fail under either
reading). My tests never assert a transport or projection ACK as real
acknowledgment.

## OUT5 — unpublished-original-source HOLD (preserved)

- OUT5's exact original 14 tests were never published as executable source.
- This court does **not** invent, reconstruct, substitute or claim execution of
  them. Status: **`OUT5_EXACT_14_NOT_RUN_UNPUBLISHED`**.
- The 18 OUT6 repair tests and my 25 OUT9 tests are NOT retroactive OUT5
  certification.

## S27 and two-writer REDs (preserved, not laundered)

- `test_s27_material_move_needs_world_owner` — a physical/material movement
  requires a real world owner that a source-free prototype cannot issue. RED
  preserved. Any primitive `COUNT_SHIELD`-style fixture-owned physical mutation
  cannot be done by this prototype.
- `test_replay_manual_two_writers_can_lose_first_committed_event` — a stale
  hidden-state concurrent write can lose the first committed event. RED
  preserved as the explicit non-goal for this single-writer trial.

## Model / privacy / usage HOLDs

- **Model calls issued by this reviewer: 0.** No paid/external model call, no
  actor-model run, no harness escalation, no helper agent.
- **Cash observed: UNKNOWN** (nothing billed). Authoring environment is Step 5
  Preview through the owner's existing OpenCode setup; free status is
  user-reported and is not represented as ongoing unlimited capacity.
- **Privacy:** no private repository content, source byte or credential was
  exported outside the authorized local host; no original survey data,
  respondent material or external private-source export. Only synthetic
  source-free fixtures and the pinned prototype/test closure were used.
- No `CURRENT`/PRE-MAIN/production changes, no semantic adoption, no V3 wake.

## Explicitly NOT established by this court

- real client ACKs (all client receipts are fixture state),
- human perception (no test asserts it; `projection.perceive` stays unauthorized),
- multiwriter safety,
- ADP-019 event authority or an external admission anchor,
- any population, psychological or behavioral calibration,
- OUTP policy choices (L1/L2, A1/A2),
- OUT5 acceptance.
