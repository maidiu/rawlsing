# SOROK #1008 — C03/C04 final A→B→A execution and repair return

Mode: MCR-lite EXECUTE / FALSIFY / REPAIR / RETEST / STOP
Repository: maidiu/rawlsing
Starting HEAD: `4e1cd301b994e4df58e89052642fde5c16fa3542`
Worktree: `/Users/matthewsmith/s2b-work/pyat1008-c03c04-exec`
Execution branch: `sorok-c03-c04-exec-1008`
Parent lineage verified: `4e1cd301b` ← `e42b12aa8` ← `d95ab945b`; protected PRE-MAIN
`6a5c12f04323d74001f9632063ec907f4fc4468e` is an ancestor.
Environment: Darwin, Python 3.11.3, pytest 9.0.2.
No rebase, no integration substitution, no protected merge, no #939 restart.

## 1. Changed files

- `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_speech.py`
  (15 added / 1 removed): exact binding of the embedded C04 admission receipt in
  `read_child_uptake` and `_verify_utterance_custody`.
- `WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_hostile_execution_r1.py`
  (new): 21 executed hostile/cold/material controls.
- `EXECUTION_1008/` (new): `SUMMARY.md`, `commands.sh`, `probe_hostile.py`,
  and raw logs under `logs/` with per-command exit codes and `/usr/bin/time -l`
  peak RSS.

No B02/B04/B05, D02/D03/P3, J1, P6, C03 prospective, BP4 writer, PRE-MAIN, or
protected authority was modified.

## 2. Defect found, repaired, RED→GREEN

Failing SHA while RED: `4e1cd301b994e4df58e89052642fde5c16fa3542` plus the new
test file only. Command:
`python3 -m pytest -q WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_hostile_execution_r1.py`

RED (`logs/21_hostile_execution_RED.log`, first run before harness correction):
8 failed, 13 passed, exit 1. Six failures were the genuine defect: tampering
one field inside the episode's embedded `receipt` was accepted by
`read_child_uptake` and by P6 `child_speech_experience`:

- `receipt.text` = "I agree to everything." accepted
- `receipt.event_kind` = "MOVE" accepted
- `receipt.event_authored_by` = "IMPERSONATED_PARENT" accepted
- `receipt.decision_action` = "PURCHASE" accepted at the time (test initially
  reused the authentic value; corrected to `DECLINE`; the defect remained)
- `receipt.hidden_reason_hash` forged accepted
- `receipt.public_utterance` = False accepted

Two further RED failures were test-harness errors (keyword argument name in a
perception monkeypatch; a constant read from `j1_join`). They were corrected
without weakening any assertion. A second run (`22_hostile_execution_GREEN.log`)
left only the `decision_action` authentic-value fixture error (1 failed, 20
passed). Final run (`23_hostile_execution_GREEN2.log`): **21 passed, 0 failed,
exit 0**.

Repair: require the embedded admission receipt to be exactly the admitted
record: event kind, event author, public text, `hidden_reason == "NOT_READ"`,
decision action, hidden-reason hash, and `public_utterance is True`, in both
direct child uptake and parent replay/self-read. Authentic records created by
the existing writer satisfy all checks; no writer, ledger, schema, or authority
was added. B's BP4 content seal and both A rounds' event/receipt checks remain
in place and are still exercised by the inherited tests.

Post-repair affected reruns (all green): A final identity 6, A custody 12,
J1 10, D03 7, C03/C04 consumer 3, C02/C03 period decision 11, D02 uptake 2,
C03 prospectives 5.

## 3. Mandated suites (post-repair final state)

| Suite | PASS | FAIL | SKIP | exit | real s | peak RSS MiB |
|---|---:|---:|---:|---:|---:|---:|
| `test_c04_first_consumer_identity.py` | 6 | 0 | 0 | 0 | 52.27 | 67.5 |
| `test_c04_custody.py` | 12 | 0 | 0 | 0 | 129.45 | 64.5 |
| `test_c03_prospectives.py` | 5 | 0 | 0 | 0 | 37.84 | 67.1 |
| `test_j1_three_head_join.py` | 10 | 0 | 0 | 0 | 304.30 | 79.4 |
| `test_c03_c04_consumer.py` | 3 | 0 | 0 | 0 | 111.32 | 73.5 |

Starting-SHA pre-repair runs are also in `logs/01`–`05` (same pass counts,
exit 0); they establish that the inherited candidate itself was green before
the repair.

## 4. Regression suites executed at the starting SHA

| Source-owned entry point | PASS | exit |
|---|---:|---:|
| `SOROK-DUEL-C01-R1/test_c01_supporting_actor.py` | 6 | 0 |
| `SOROK-DUEL-C01-R1/B_RETURN_R1/test_c01_b_supporting_actor.py` | 8 | 0 |
| `SOROK-DUEL-C01-R1/C02/test_c02_parent_activity.py` | 4 | 0 |
| `SOROK-DUEL-C02-R1/test_c02_b_parent_activity.py` | 7 | 0 |
| `SOROK-DUEL-C02-R1/A_RETURN_R2/test_c02_live_root_b02.py` | 5 | 0 |
| `SOROK-DUEL-C02-C03-R2/test_c02_c03_b_period_decision.py` | 11 | 0 (rerun post-repair 11, exit 0) |
| `SOROK-DUEL-B04-R1/test_b04_composition.py` | 3 | 0 |
| `SOROK-DUEL-B04-R1/test_b04_operations.py` | 4 | 0 |
| `SOROK-DUEL-B05-R1/test_b05_batch_cycle.py` | 1 | 0 |
| `SOROK-DUEL-B05-R1/test_b05_cross_batch.py` | 1 | 0 |
| `SOROK-DUEL-B05-R1/test_b05_interleave_retry.py` | 1 | 0 |
| `SOROK-DUEL-B05-R1/test_b05_rollback.py` | 1 | 0 |
| `SOROK-DUEL-B05-R1/test_b05_rolling.py` | 1 | 0 |
| `SOROK-DUEL-B05-R1/test_b05_zero_and_held.py` | 2 | 0 |
| `SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_initiative.py` | 5 | 0 |
| `SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_initiative_hostile.py` | 20 | 0 |
| `SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_scene_context.py` | 2 | 0 |
| `SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py` | 8 | 0 |
| `SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py` | 18 | 0 |
| `SOROK-DUEL-D03-R1/tests/test_d03_immediate_uptake.py` | 7 | 0 |
| `SOROK-DUEL-D02-R1/tests/test_d02_b_two_event_uptake.py` | 2 | 0 |

No skips were reported. Unrelated historical FIABC failures were not used:
this execution ran the selected C01/C02/B04/B05/P6/D02/D03/C03/C04/E01/J1
entry points only.

## 5. Hostile first-consumer results (executed)

1. Correct and conflicting `event_id`/`operation_id`: matching and both-selector
   reads pass; unknown, empty and cross-spliced selectors refuse
   (`CHILD_EXPERIENCE_UTTERANCE_NOT_FOUND`, `CHILD_EXPERIENCE_SELECTOR_SCHEMA`).
2. Original BP4 content hash and content-derived event ID: altered event with
   stale hash/ID refuses at parent replay/self-read, P6 and direct child uptake
   (`*_WORLD_EVENT_UNSEALED`); authentic event passes.
3. Forged summary, location, observable, sequence, speaker, text and clock:
   refused. The new run adds clock and a second public-field control; B's
   inherited four-field control remains green.
4. Historically heard speech with original C12 receipt: `PERCEIVED` from direct
   uptake, P6 and J1; D03 `joint_check`.
5. Historically heard speech with severed child receipt:
   `CHILD_UPTAKE_PERCEPTION_SEVERED` / `CHILD_EXPERIENCE_PERCEPTION_SEVERED`.
6. Originally unheard speech with forged later child perception:
   `CHILD_UPTAKE_FALSE_PERCEPTION`; restoration returns authentic
   `NOT_PERCEIVED`.
7. Missing/duplicated parent or child receipts: missing parent receipt refuses;
   duplicate child receipt refuses; duplicate parent receipt refuses
   (`CHILD_UPTAKE_PARENT_RECEIPT_SEVERED`); duplicate utterance episode refuses.
8. Mismatched episode root, branch, actor, alias, clock, child identity, and
   embedded admission receipt: refused. The embedded receipt fields listed in
   §2 were the new repair.
9. Hidden parental reasoning: absent from child experience, P6 output and D03
   output in the heard J1 test and the unheard late-co-presence control.
10. Intact historical speech after genuine cold reopen and restored mutation:
    both cold reopens `PERCEIVED`; event hash, utterance-episode count and
    purchase count unchanged; no duplicate speech, purchase, rent or actor
    activity. Branch-fork replay is UNOBSERVED: this source cut exposes no
    public branch-fork entry point for C04 (store has branch identity/ancestry
    checks but no fork writer). It is not asserted as passed.

Additional controls: later physical co-presence does not rewrite a historically
unheard arrival (`NOT_PERCEIVED`, J1 held, hidden reason absent); changed debt
and care obligations make the purchase candidate materially ineligible while
quiet nonpurchase remains eligible; the prospective reader remains read-only
and issues no chosen/performed candidate.

## 6. Materials, purchase, rent, conservation

J1 executed actual PURCHASE at 40 units with parent cash 100→60, household cash
unchanged, one purchase episode, D03 store head unchanged, and cold reopen with
exactly one purchase and one utterance episode. B04 composition/operations and
B05 batch/cross-batch/rollback/rolling/zero-held suites pass with their existing
writers. Insufficient parent cash, currency mismatch, tight space, noise and
unknown acoustics bind the parent act and speech as inherited. The legacy
caller-directed request/proposal remains explicitly `CALLER_SUPPLIED_OBJECTIVE_REQUEST`
and is not represented as independent maternal volition.

## 7. Execution economics

- Per-suite elapsed and peak RSS are in §3, §4 and raw logs. Peak RSS observed
  in the new hostile suite: 67.5 MiB; highest observed in this execution:
  79.4 MiB (J1 rerun).
- Wall clock from first to last raw log: 17:38:03–18:30:35 local (about 52m32s),
  plus checkout, test authoring and this return.
- Provider tokens/cost, native psychology, external human receiving: UNOBSERVED
  or NOT_IMPLEMENTED. Tests are sourcefree and use no provider.
- Exit statuses: all final-state suites exit 0. RED receipts are retained with
  exit 1.

## 8. G1–G5

| Gate | Disposition | Evidence |
|---|---|---|
| G1 parent/world/child identity | PARTIAL_SOURCE_GROUNDED | actual C01/C02 parent, B02/B03/B04/B05 material, C12 store and J1/P6/D03 consumers exercised; independent plural native organization not proved |
| G2 mother-owned act/expression/perception | HOLD_PARENT_SELECTOR_AND_LANGUAGE_OWNER | decision request/proposal and speech text/hidden reason remain caller-supplied; `language_generation_owner: NOT_IMPLEMENTED`; C03 reader returns `CANDIDATES_ONLY_ACTOR_SELECTION_UNISSUED` |
| G3 hostile first consumer | EXECUTED_SOURCEFREE_PASS | 21 new hostile controls plus inherited A/B controls, actual J1/P6/D03 stores; RED→GREEN receipt §2 |
| G4 conservation/cold/economics | EXECUTED_SOURCEFREE_PASS (branch fork UNOBSERVED) | cold reopen and restored-mutation cold replay preserve event hash, one utterance and one purchase; per-process time/RSS measured; provider UNOBSERVED |
| G5 independent nonauthor receiving | NOT_STARTED / cannot self-issue | no nonauthor receiver in this execution |

## 9. Remaining holds and strongest unrepaired weakness

- G2: no source-owned mother selector, no independently generated maternal
  language. `perform_parent_utterance` still accepts caller-supplied text and
  hidden reason; `as_actor=parent_id` is a self-reader label, not an
  authenticated principal.
- G5 remains separate and unissued.
- Native Rule A/T, NO_CHANGE, memory/durable acquisition, and D04/D05 child
  performer remain MISSING_RULE / held.
- D03's caller-supplied utterance receipt binds event/hash/speaker/alias/text/
  child/action, but does not independently bind receipt `root`, `branch`,
  `clock` or `operation_id`; forging those four fields was accepted with no
  observable output difference. This is a D03/P3 owner boundary, not modified.
- Strongest unrepaired first-consumer weakness: a privileged writer able to
  coherently rewrite the BP4 event, the C04 episode and the C12 perceptions
  together remains outside self-hash custody; only the append/store owner and
  source rights can address that. The event-ID prefix is also pinned to the
  current BP4 `TEST_ONLY_BP4_WORLD_EVT_` format and fails closed on an
  unversioned legitimate migration.

No protected merge, native scientific promotion, actor authorization, human
rights grant, or #939 fleet restart is issued. STOP.
