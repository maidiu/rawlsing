# SOROK P6 joined verification candidate

**STATUS:** `CANDIDATE_ONLY__RECOGNITION_PASS_SCOPED__JOINED_FOUR_PROOFS_PASS__JOINED_CLI_DEMO_PASS__NOT_MERGED`

- **Frozen runtime:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`
- **Assembled evidence:** `1c461ebc6d3ede1cdbeda244ab06c346ddbcc92e`
- **Recognition input:** `4f3f465923a61e9e3d76b9c0aa7f6ffd8ecad318`
- **Independent recognition review:** `a3ce6b4282c0c427ef11da71030d622aa908ee86` — `PASS_SCOPED`
- **Isolated branch:** `codex/sorok-p6-joined-verification-20261107-r1`
- **No PR/protected merge.** Original PR779 writer untouched.

## Composition

Recognition runtime files are exact from `4f3f4659…`:
`WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` and `run_p6.py`.
Recognition proof tree is exact from `4f3f4659…`:
`WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1`.
Independent review return is exact from `a3ce6b42…`:
`WORKER_RETURNS/SOROK-P6-COMMITTED-EVENT-REVIEW-20261107-R1`.
The assembled four-proof/cold-demo evidence from `1c461ebc…` is retained.
Unrelated runtime/protected material is unchanged.

## Joined tests

Collection across the four joined proofs:

```text
4 tests collected in 0.10s
```

```sh
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/test_gaze_proof.py \
  WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/test_history_order_proof.py \
  WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/test_p6_chronology_proof.py \
  WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/test_p6_actor_boundary_proof.py
```

```text
4 passed in 393.96s
exit status 0
```

No additional connected-house test was needed for interface difference; the
independent review already recorded its house test passing (`1 passed in 83.47s`)
and the four interface proofs pass against this runtime.

Independent recognition receipt: 5 recognition tests plus 1 house test passed
in `a3ce6b42…` (review return and evidence). Focused recognition tests remain
owned by that independent reviewer; this worker did not rerun them.

## Joined portable cold CLI demo

Command:

```sh
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/run_demo.py \
  --out WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo
```

Result: **13/13 command records exit 0**, fresh output directory, actual
cold-process CLI each time. Evidence: `joined_demo/TRANSCRIPT.md`,
`joined_demo/actual_run.jsonl`, `joined_demo/house_history.json`,
`joined_demo_run.log`, and `joined_demo_receipt.json`.

Captured joined facts:

- **Real recognition:** after `look sandals`, recognized identity
  `the repaired blue-thread sandals`, marking `blue-thread-left-strap`, event
  `TEST_ONLY_BP4_WORLD_EVT_dd7bc39df6549a9ec6aef43a7c8090410846c450a7d9b06262eaff44c5998179`,
  turn `4`; it remains in cold `view` after the later photo look.
- **Nadia material/time:** waiting SAY is REALIZED `248 -> 249`, material
  `2 -> 1`, free hours `11 -> 10`, actual action
  `TEST_ONLY_BP4_WORLD_EVT_c472b0e2…`.
- **History:** root
  `d747d2c208fb0fe3610c9f08d728d5f358758feee6be5164e07475e4431950c6`;
  `bench-installation` clock `234`, `strap-repair` clock `239`,
  `photo-exposure` clock `244`, dependency `["strap-repair"]`.
- **Leave-alone:** only coaster, sandals and photo are looked at; no mug look.
  `leave the mug alone` is admitted at clock `260 -> 261`; material stays `0 -> 0`
  (`MATERIAL_EXHAUSTED`), the earlier earned sandals recognition persists, and
  the final view does not force a new identity.

The previous frozen transcript in `SOROK-P6-COLD-DEMO-20261107-R1` is unchanged.
Its three recorded hashes still match:
`11da7a804aa3603997716794802ac4a65a90f490b3a6eea6a3151f0499496493`,
`7421fc2bd9dba4e08e3c00f39ec4943441d1eeb5e32101673e98b4f080924ae4`,
`87ca6dd35cdf29a5d97598f5bce855b27313ab12b0d45d95332795c7f4336e53`.
The joined demo is separate evidence and does not overwrite that transcript.

## Exact candidate paths

Runtime changes:
```text
WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py
WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py
```

Recognition evidence/review:
```text
WORKER_RETURNS/SOROK-P6-RECOGNITION-PROOF-20261107-R1/
WORKER_RETURNS/SOROK-P6-COMMITTED-EVENT-REVIEW-20261107-R1/
```

Retained assembled evidence:
```text
WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/
WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/
WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/
WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/
WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/
WORKER_RETURNS/SOROK-P6-PROOF-ASSEMBLY-20261107-R1/
```

Joined evidence:
```text
WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/00_RETURN.md
WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo/
WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo_run.log
WORKER_RETURNS/SOROK-P6-JOINED-VERIFICATION-20261107-R1/joined_demo_receipt.json
SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md
SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json
```

## Boundary

Sourcefree only. P5 #775/P6 #779 remain unreceived candidates; recognition
review is scoped, not merge/native/human/science acceptance. No protected or
shared-progress write, no PR779 branch write, no new PR. FIABC 144 PASS / 3 FAIL
and all prior scope/native/human holds remain. Recognition fix and actual demo
were separate active lanes; this is their candidate joined verification only.
