# SOROK automatic currentness R1 — author return

**Engineering:** `AUTHOR_CANDIDATE_FOR_INDEPENDENT_NONAUTHOR_REVIEW`
**Scientific:** `HELD` | **Authority:** `HELD`
**Issue:** SOROK automatic PROGRAMMA currentness (new explicit user commission)
**Author session:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Base:** `75581fa9e2c8576d1ca9a7a9a18759ea840d82e8` (PR #1095 frozen cut)
**Branch:** `codex/sorok-automatic-currentness-engine-20261115-r1`
**Terminal:** frozen implementation for one independent nonauthor review; no automatic R2.

## What is actually wired

`SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py`
adds a real intake/reconciliation path over the existing paired
`CURRENT_PROGRESS.json` / `CURRENT_PROGRESS.md`:

- **Material-result intake** binds a real controller run to its exact
  `job.json` / `binding.json` / `launch.json` / `process.json` /
  `completion.json` hashes, PID/session/grant/argv/worktree/recipient, committed
  return artifact hash and competent role. Exit `0` becomes
  `RETURNED_REVIEW_PENDING`, never acceptance.
- **Independent review intake** requires a distinct reviewer/author session,
  exact implementation source, scoped verdict, `full_original_claim =
  NOT_ESTABLISHED`, and immutable review commit/document git-blob pins. Historical
  #1089/#1091/#1062 receipts are replayed explicitly with
  `replay_is_not_new_review=true`; they are not represented as new review work.
- **Atomic paired reconciliation** uses an exclusive lock, generation markers,
  a recoverable PREPARED/COMMITTED journal transaction and a reader boundary that
  refuses mixed MD/JSON generations with
  `PAIRED_MD_JSON_MIXED_GENERATION`. The JSON pair is the only truth; the MD is
  derived; the journal is recovery custody only.
- **Dependency reevaluation** recomputes all 27 original B01–G04 tasks from the
  frozen packet/GMT sources, preserves exact original edges/classes/source and
  separates scoped engineering, independent receiving, protected integration,
  original-task completion, scientific authority and execution state. STOP,
  revocation and source-authority HOLD propagate transitively to dependents.
- **Cold start / authenticated intake** compares the authenticated GitHub
  baseline and local controller receipts since the last checkpoint. New/unseen
  or unavailable evidence emits specific `RECONCILIATION_REQUIRED`; a matched
  baseline is recorded as custody, not acceptance. There is no universal
  chat-start callback: cold start is the explicit existing-HQ/controller
  invocation below plus the installed SOROK-only completion hook.
- **One operational readout** (`status` / `startup`) returns generation,
  checkpoint, verified receiving/scoped READY, HOLDs with owner/reason, exact
  unmet scoped/full-original prerequisites, source/review pins, evidence
  freshness, adoption and protected-CI state, and one non-dispatch next action.

## Real execution evidence

- **Real finite existing-controller child worker:** job
  `sorok-automatic-currentness-real-return-20261115T224953`, supervised child
  exit `0`, real `completion.json` and observer `finished.json`, return artifact
  sha256 `8dcab490673c31b998793dff52eed8c9fa555a8700a45fc2e2199a846f64a2c0`.
  The installed controller's additive SOROK-only hook automatically called the
  runtime and recorded `SOROK_CURRENTNESS_INTAKE_OK`; the runtime state records
  `RETURNED_REVIEW_PENDING`, not acceptance. `notify=False` prevented an
  unattended cascade.
- **Two earlier finite attempts are retained as fail-visible history:** the first
  failed on hook argument order; the second failed with `RETURN_ARTIFACT_MISSING`
  because the fixture child wrote the wrong argv path. Both were explicitly
  inspected and resolved with evidence after the successful third run. A zero
  child exit was never promoted to acceptance.
- **Historical review replay:** B05 #1089, C04 #1062 and C05 #1091 exact
  immutable nonauthor receipts were intaken as explicit replays; their scoped
  task states are preserved and `replay_is_not_new_review=true`.
- **Cold start:** `startup` and `status` were run in fresh processes from the
  durable pair, with generation/checkpoint readback and no chat memory.

## Current readout (frozen cut)

- Generation `20`; final runtime state has no unresolved reconciliation items.
- `RECEIVE B01` is the recommended next non-dispatch action, owner
  `S47/P2 objective world; P6 house.py`; full original completion is
  `NOT_ESTABLISHED`.
- Scoped received/unmerged: B05 (#1089), C04 (#1062), C05 (#1091), all
  `PENDING_PROTECTED_CI_AND_ADOPTION`.
- Seven protected P3/P4/P5/P6/MI/MII/MIII foundations preserved.
- #939 old-fleet STOP preserved; Browser #1008/#1010 terminal scoped/held and
  #1012 not launched wait J1; no Browser session was touched.
- Native science/actor/human authority and protected integration remain HELD.

## Frozen #1095 preservation (four minor observations retained, not silently fixed)

1. The frozen `operational_currentness_r1` JSON key remains prepended exactly as
   received; the new runtime key is appended last.
2. #1095 changed six files, including the two frozen task/GMT sources; exact
   blobs are preserved: task `17cfae53...`, GMT `474befcb...`, verifier
   `d971b6ea...`, workflow `f76c0d90...`.
3. `last_reported_oldmac_five_receipts=PR1063_TW0_JOB_RECEIVING_20261115` is a
   label; the actual artifact is
   `WORKER_RETURNS/SOROK_HQ_CLASSIFIED_QUEUE_20261115_R1/01_TWO_JOB_RECEIVING.md`
   at `74f3fbbace77c6700381a5b95edcc8f1524d0670`.
4. #1008/#1010 strings remain unpinned historical strings and the lower historic
   MI #791 copy remains historical.
   The immutable `75581fa9` cut was not mutated to clean these; the runtime
   block carries dated documentary currentness instead.

## Exact files

- New product: `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py`
  (`blob 6164e595efcd176bb2ec9b75aa99074472a4c9b4`).
- New test: `.../test_operational_currentness_runtime_r1.py`
  (`blob 38465315646d3a4deec68ddff87651ca47f5f89b`; 15 passed).
- Paired progress: `CURRENT_PROGRESS.json` / `.md`, runtime key/block only;
  frozen projection and history preserved.
- Minimal frontdoor/work-now invocation notes: `00_PROGRAMMA_SOROK.md`,
  `10_RECONCILIATION_QUEUE_SOURCE_GAPS_AND_CLOSEOUT_CHECK_R1.md`.
- Own evidence/controller backup/diff/installer/recovery and fixtures:
  `WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R1/`.

Installed controller hook: `launch.py` sha256 `4c5004ef...`,
`completion_events.py` sha256 `503f7b41...`. Original files are backed up under
`controller/original/`; `controller/manage_hook.py restore` restores them.
Bindings without `sorok_currentness` are unchanged; PYAT has no new behavior.

## Exact commands / pins

See `evidence/COMMANDS.txt`, `evidence/BLOB_PINS.json`,
`evidence/runtime_journal.jsonl`, `evidence/controller_runs/`,
`evidence/final_status.json`, `evidence/final_startup.json` and
`evidence/final_runtime_tests.out`.

## Holds / limits

- This is not independent acceptance. The separate nonauthor must review the
  frozen commit and feed their own real review receipt; `mechanism_review.state`
  is `PENDING_EXTERNAL_NONAUTHOR_REVIEW`.
- Hosted CI remains unavailable due to account billing; no required CI was
  bypassed or claimed PASS. Protected adoption remains
  `PENDING_PROTECTED_CI_AND_ADOPTION`.
- No new ledger, world store, scheduler, agent fleet, controller replacement,
  provider/account/model/global-permission change or protected merge.
- No native science, actor knowledge, human authority or psychological fact is
  claimed. Fully privileged local checkpoint fabrication remains outside the
  observed controller/public-store threat model.

## STOP

Frozen implementation for the same separate nonauthor review. No automatic R2,
no job dispatch from READY, no protected adoption.
