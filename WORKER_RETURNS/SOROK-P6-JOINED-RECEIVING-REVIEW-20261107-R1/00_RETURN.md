# SOROK P6 joined receiving review

**Candidate:** `2533e764e8a6494c326f8db5630d8132178bf1f8`
**Frozen prior draft:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
**Protected observed:** `7a5429ffbc48efd25e28c912da80c822e66bc182`
**Joined return:** `WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/00_RETURN.md`
**Recognition input:** `4f3f465923a61e9e3d76b9c0aa7f6ffd8ecad318`
**Recognition closure:** `a3ce6b4282c0c427ef11da71030d622aa908ee86` — `PASS_SCOPED`
**VERDICT: PASS_SCOPED** — the assembled P6 candidate is selectively composed, sourcefree, preserves the frozen runtime and paired PROGRAMMA holds, and the actual cold consumer plus reused proofs support the claimed scoped result.

This is a receiving review of the assembled product by other authors. It is not a
self-review of the prior recognition return; that return is used only as the exact
recognition input.

## Composition and scope — PASS

Verified by exact tree diffs:

- `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` and `run_p6.py` are
  byte-identical to `4f3f4659…`.
- `WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1` is byte-identical to
  `4f3f4659…`.
- `WORKER_RETURNS/SOROK-P6-COMMITTED-EVENT-REVIEW-20261107-R1` is byte-identical
  to `a3ce6b42…`.
- The four combined proof directories and `SOROK-P6-COLD-DEMO-20261107-R1` are
  byte-identical to assembly `1c461ebc…`.
- `git diff 41b21bab…2533e764` contains only P6 runtime/evidence and paired
  `SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.{md,json}`. No P3/P4/P5,
  `rawlsing_next`, unrelated protected, or PR779 writer file changed.
- `CURRENT_PROGRESS.json` is semantically identical to `41b21bab…` except for
  the new `p6_joined_verification_candidate` key. The large byte diff is
  formatting/key-order churn, not unrelated semantic material.
- `CURRENT_PROGRESS.md` adds only the P6 joined candidate entry.

Sourcefree scope is preserved: no source bytes, native issuance, science, human
acceptance, or protected merge is claimed.

## Paired PROGRAMMA grades — PASS

Both paired files carry the same status:

`CANDIDATE_ONLY__RECOGNITION_PASS_SCOPED__JOINED_PROOFS_PASS__JOINED_DEMO_PASS__NOT_MERGED`

- JSON: `p6_joined_verification_candidate.recognition_verdict = PASS_SCOPED`
- MD: same status and recognition verdict
- Inherited `p6_candidate_20261107.grade = SOURCEFREE_TEST_ONLY`
- Preserved holds: `FIABC/LiTS 144 PASS / 3 FAIL`, all prior scope/native/human
  holds, P5 #775 and P6 #779 unreceived.

The joined return uses a slightly longer status label
(`JOINED_FOUR_PROOFS_PASS__JOINED_CLI_DEMO_PASS`); this is a wording variance,
not a contradictory grade.

## Actual cold first consumer — PASS

Reused the joined 13-command receipt and transcript. Verified independently:

- `joined_demo_receipt.json`: `command_count=13`, `all_exit_zero=true`
- `actual_run.jsonl`: 13 records, all `exit=0`
- Total cold CLI latency: **187.826s**; per-command min **3.521s**, max **27.897s**
- Evidence hashes:
  - `TRANSCRIPT.md` `88f703c76edc5b5d0da0560390b6f755f5017651c6b9fc92747c58a79fa25885`
  - `actual_run.jsonl` `a8ce2e3e4cc2ccda393f062635bc6be077e0fd1d58145659c13bfdc094689756`
  - `house_history.json` `03cf9da0bcf2396ba362b67aa2f10dff2d0f673a0619a0c861b515d9b54fee3f`

The demo ran in the sibling worktree at the same candidate SHA `2533e764`; its
runtime files diff-empty against `4f3f4659…`.

Covered facts:

- **Pre-existing history:** epoch `248`, root
  `d747d2c208fb0fe3610c9f08d728d5f358758feee6be5164e07475e4431950c6`;
  `bench-installation` clock `234`, `strap-repair` clock `239`,
  `photo-exposure` clock `244` depending on `strap-repair`.
- **Material/time:** Nadia SAY `REALIZED 248 -> 249`, material `2 -> 1`,
  free hours `11 -> 10`, actual action
  `TEST_ONLY_BP4_WORLD_EVT_c472b0e2…`.
- **User choice:** explicit `leave the mug alone` SAY; no mug look; material
  remains `0 -> 0` with `MATERIAL_EXHAUSTED`; final view does not force a new
  identity.
- **Committed-event recognition:** `look sandals` emits identity
  `the repaired blue-thread sandals`, marking `blue-thread-left-strap`, event
  `TEST_ONLY_BP4_WORLD_EVT_dd7bc39df6549a9ec6aef43a7c8090410846c450a7d9b06262eaff44c5998179`,
  turn `4`; it persists through later cold views after the photo look.
- **Cold restore:** every command is a separate OS process against the cold
  checkpoint; history and recognition persist. The chronology proof separately
  covers tamper rejection and exact restore.
- **Gaze/actor isolation:** covered by the reused four proofs and independently
  checked by the actor-boundary test below; no actor input was changed.

## Reused and discriminating tests — PASS

Reused joined evidence (no full-suite rerun):

- Four combined proofs: `4 passed in 393.96s`
- Independent recognition: `5 passed in 238.71s`; house `1 passed in 83.47s`
- Joined cold demo: 13/13 exit 0

One independent discriminating boundary rerun against this candidate:

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/test_p6_actor_boundary_proof.py
```

```text
1 passed in 27.13s
```

This confirms the assembled runtime keeps the P4/Nadia speech, uptake,
expression, material/time interval, turn material, clock, room and invitation
identical when only private `p6_gaze.json` changes.

## Material limits

- Candidate only; not merged. P5 #775 and P6 #779 remain unreceived upstream.
- Recognition closure is scoped, not native/science/human acceptance.
- No PR779 writer, protected operation, or unrelated program was touched.
- Latency: cold CLI total `187.826s`, max single command `27.897s`; four-proof
  suite `393.96s`. This is not production latency evidence.
- `CURRENT_PROGRESS.json` has large formatting/key-order churn even though the
  semantic change is only the new P6 joined key; review consumers should use
  semantic diff, not byte count.
- The joined return’s boundary sentence says “No protected or shared-progress
  write” while the candidate intentionally updates paired `CURRENT_PROGRESS`.
  Read this as no protected/other shared-progress write; the paired PROGRAMMA
  entry itself is present and additive. This is a wording caveat, not a runtime
  or composition defect.
- No native science, actor authority, human acceptance, or FIABC change is
  claimed; inherited `144 PASS / 3 FAIL` remains.

## PROGRAMMA_DELTA

- **Identity:** P6 joined candidate `2533e764…`; frozen `41b21bab…`; protected observed `7a5429ff…`.
- **Function:** independent receiving review of assembled P6 cold first consumer and joined proofs.
- **Verdict:** `PASS_SCOPED`.
- **Evidence:** selective composition exact; 13/13 cold commands; recognition turn 4; reused 4 joined proofs and recognition 5+1; independent actor-boundary `1 passed in 27.13s`.
- **Limits:** candidate only, sourcefree, P5 #775/P6 #779 unreceived, no native/science/human/protected merge; latency `187.826s` cold total, `27.897s` max command.
