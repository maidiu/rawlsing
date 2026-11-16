# SOROK #1038 — independent nonauthor C03/C04 custody G5

**Verdict:** `ACCEPT_SCOPED@C03_C04_SOURCEFREE_CUSTODY@ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9`

**Scope accepted:** child-facing C04 custody (C12 direct uptake, P6
`child_speech_experience`, D03/J1 consumer) and the C03 material-prospective
candidate readset, at `SOURCEFREE_S2_ONLY` grade.

**Not accepted, still HELD:** mother-owned event selection and generated
language (`language_generation_owner: NOT_IMPLEMENTED`), complete J1/Nadia
performed response, native Rule A/T, NO_CHANGE, durable acquisition, D04/D05,
scientific/human/source-rights receiving, protected merge, and #939 restart.
Parent self-read receipt-metadata exactness and D03 caller-receipt
root/branch/clock/operation binding remain exact residuals (below), not part of
this scoped acceptance.

## Custody of the review

- Reviewer session: `ses_e22146664ffeDffEDH4nsj8nsY`, fresh nonauthor reviewer;
  no authorship in Browser A, Browser B, A final, or #1030 code.
- Checkout: `/Users/matthewsmith/.codex/worktrees/sorok1038-custody-g5/Rawlsing`
- Branch: `codex/sorok1038-custody-g5-20261115-r1`
- Frozen candidate: `ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9`
- Ancestry verified in-object: `0ba01215936df0b28027afe6f1596e6e610dacf7`
  (A #1015) → `fa91ccc09fea4ef0b646f437c6d2b05aed04af2a` (B #1017) →
  `4e1cd301b994e4df58e89052642fde5c16fa3542` (A #1021) →
  `ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9` (#1030).
- Protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e` is an
  ancestor of the candidate and was not modified.
- Candidate delta from `4e1cd30`: 43 files, +2118/−1; the only product-code
  change is `parent_speech.py` (+15/−1). All other additions are the
  `EXECUTION_1008/` evidence and the new hostile test.
- Reviewer writes only `WORKER_REVIEWS/SOROK1038_C03_C04_CUSTODY_G5_R1/` and
  `.local-logs/sorok1038-custody-g5/`. Product files were read-only; no patch,
  no protected write, no push, no CI dispatch, no provider call, no browser
  contact, no other checkout touched.

## Exact source blobs

| Path | Git blob | SHA-256 |
|---|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_speech.py` | `71caad03c5bf4ed66fd0b903e55f0083f3368837` | `d6ffd5455748ffbc75efc64d1bb24ad4bdd31d7fa4a989e46de88fedf32ff5bc` |
| `WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_hostile_execution_r1.py` | `350d840efa21fa926f07817aad29d147a8b1c975` | `8165e641ff485212afd6aeb9fe0e19df777c16d09b97879c1206cf33999e502e` |
| `WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py` | `5fe96f524e8db5c2169328d5c124c916d56d1b8e` | — |
| `WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py` | `58bdfc451f06ea27becf91d7969f5835a4efc85b` | — |
| `WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c03_prospectives.py` | `f4d41a58e9f44cdb0bab57f351e32885e50397f5` | — |
| `WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py` | `ff40f49e3f2d14aa661729ff14644f55ddb2bd2e` | — |
| `WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py` | `8e3775ebb51547aefa4490227a95a7eeff0008a9` | — |
| `EXECUTION_1008/commands.sh` | `cad075a3548e327c10d6b5fff7bf0db2eee4e913` | — |
| `EXECUTION_1008/SUMMARY.md` | `73b4b3de35ea57bc28f3ec872af3644be71ef58f` | — |
| `EXECUTION_1008/probe_hostile.py` | `52857992f13886efc1303d92af375b2a010b7d97` | — |

Frozen packet law read at `227ce149fc7864c83c179a7d3ecaef2b92c5bdab`
(`03_TASK_PACKETS_R1.json`, C03/C04/E01/D03); MCR-lite read at
`CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md`; SOROK first-read
read at `SOROK_PRODUCT_CONTROL_ROOM/00_READ_ME_FIRST.md` and
`PROGRAMMA_SOROK/READ_FIRST.md`; PR custody read from `PR_1030.json` and
`PR_1027.json`. #1027 B04/B05 false-read defects were treated only as separate
owner risk (#1037), not as this reviewer's repair.

## Environment and command discipline

- macOS 13.7.8 x86_64; Python 3.11.3; pytest 9.1.1.
- Interpreter: `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`.
- Every command:
  `TMPDIR=$PWD/.local-logs/sorok1038-custody-g5/tmp`
  `PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`; world/log output
  stayed in assigned scratch or this return. `/usr/bin/time -l` used where
  noted. Host was under concurrent unrelated job load, so timings are not an
  isolated performance benchmark.

## Mandated suites independently rerun at the frozen candidate

| Suite | Pass | Exit | pytest s | Peak RSS bytes |
|---|---:|---:|---:|---:|
| `test_c04_first_consumer_identity.py` | 6 | 0 | 68.69 | 64,913,408 |
| `test_c04_custody.py` | 12 | 0 | 149.88 | 63,512,576 |
| `test_c03_prospectives.py` | 5 | 0 | 113.72 | 59,572,224 |
| `test_j1_three_head_join.py` | 10 | 0 | 493.10 | 70,471,680 |
| `test_c03_c04_consumer.py` | 3 | 0 | 103.38 | 68,128,768 |
| `test_c04_hostile_execution_r1.py` | 21 | 0 | 219.29 | 68,362,240 |
| `test_d03_immediate_uptake.py` | 7 | 0 | 144.45 | 67,891,200 |
| `test_d02_b_two_event_uptake.py` | 2 | 0 | 14.57 | 66,560,000 |
| `test_c02_c03_b_period_decision.py` | 11 | 0 | 329.30 | 75,689,984 |
| `test_b04_operations.py` | 4 | 0 | 99.85 | 64,491,520 |
| `test_b05_zero_and_held.py` | 2 | 0 | 22.36 | 65,564,672 |
| `test_house.py` | 8 | 0 | 264.26 | 71,606,272 |

All final-state exits were 0. No skips. The author's `EXECUTION_1008/logs`
counts were checked and are consistent with these reruns.

## RED → GREEN verification

The committed hostile test was run against the pre-repair code
`4e1cd301b994e4df58e89052642fde5c16fa3542` extracted by `git archive` under
review scratch, with only the current hostile test file copied in:

- Pre-repair: **6 failed, 15 passed**, exit 1, 205.69 s, max RSS 63,045,632 B.
  The six failures are exactly `text`, `event_kind`, `event_authored_by`,
  `decision_action`, `hidden_reason_hash`, `public_utterance` in the embedded
  admission receipt.
- Candidate: **21 passed**, exit 0.

The author's retained RED log shows 8 failed / 13 passed because it included two
test-harness errors that the committed corrected test no longer has; the
SUMMARY discloses that correction. The genuine RED is the six receipt fields
above.

## Independent hostile matrix

`g5_probe_matrix.py` (195 JSON records) used a real J1 ceiling. All Nadia-facing
consumers refused the following:

- Embedded receipt: `text`, `event_kind`, `event_authored_by`, `actor_id`,
  `alias`, `root`, `branch`, `clock`, `decision_id`, `operation_id`,
  `event_id`, `event_hash`, `child_actor_id`, `child_alias`,
  `child_perception_channel`, `hidden_reason`, `hidden_reason_hash`,
  `decision_action`, `public_utterance`, `status`, `schema`.
- Episode custody: wrong root/branch/actor/alias/text/decision/operation/
  event-hash/child identity/clock.
- Event custody: forged summary/location/sequence/clock/observable/body-text
  with stale hash; coherently recomputed event hash with stale event ID;
  event/receipt divergence.
- Perception history: severed child receipt, duplicate child receipt, wrong
  child channel, missing parent own-speech receipt.
- Selectors: both valid, event-only, operation-only accepted; forged, unknown,
  empty, or both-selector mismatches refused.
- False historical hearing: authentic `NOT_PERCEIVED`; forged later child
  perception refused; restoration returns `NOT_PERCEIVED`; later physical
  co-presence does not rewrite history.
- Privacy: hidden reason and hidden-reason hash absent from child uptake, P6,
  child experience, and D03; mutating the outer stored hidden reason does not
  leak; mutating the embedded receipt hidden reason is refused without echoing
  the marker.
- Event seal: complete BP4 content hash and event-ID content address enforced
  at parent replay/self-read and both child readers.

## C03 nonclaim and material readset

`read_parent_material_prospectives` returned
`CANDIDATES_ONLY_ACTOR_SELECTION_UNISSUED` with five options, `chosen_candidate:
None`, `performed_event: None`, and every option `chosen=False,
performed=False`. It created no world event, perception, episode, speech,
purchase, or rent. Changed debt (61) and changed care (8 h) made the junior
purchase `MATERIALLY_INELIGIBLE` while quiet nonpurchase remained
`ELIGIBLE_NOT_SELECTED`. The hidden motive, `CALLER_SUPPLIED_OBJECTIVE_REQUEST`,
and speech generation did not appear.

The C04 writer still labels the public text
`CALLER_SUPPLIED_NOT_GENERATED`, the hidden reason
`CALLER_SUPPLIED_NOT_GENERATED`, and `language_generation_owner:
NOT_IMPLEMENTED`. No successful reader in this review was presented as
autonomous mother volition, generated speech, or full J1 performance.

## Changed / restored / cold

- A second legitimate public utterance under a new operation ID was qualified
  by direct uptake and P6 with its own exact text and event; the first utterance
  remained exact. Changing the second embedded receipt text was refused;
  restoring it returned the exact second episode. Reusing the first operation
  with different text refused (`PARENT_UTTERANCE_REUSE_MISMATCH`) and did not
  alter the first event/hash.
- Purchase count remained 1 and rent count 0 across the legitimate second
  speech and refused mutations.
- Two truly fresh interpreter processes reopened the same on-disk J1 case via
  `reopen_owner`. Both returned the exact original event hash/text, direct
  uptake `PERCEIVED`, P6 `PERCEIVED`, J1 `UPSTREAM_CAUSAL_CHAIN_PROVEN_SUBSEQUENT_EVENT_HELD`,
  D03 `COMPUTED_TEST_ONLY_IMMEDIATE`, subsequent event not performed,
  `durable_formation: MISSING_RULE`, `language_generation_owner:
  NOT_IMPLEMENTED`, one speech episode, one purchase, zero rent, and no hidden
  reason/hash in child outputs. Session clock, episode/world/perception counts,
  and P3 store head were unchanged; the parent self-read still returned the
  hidden reason only to the parent.

## G1–G5

| Gate | Independent disposition |
|---|---|
| G1 parent/world/child identity | `PARTIAL_SOURCE_GROUNDED`: actual C01/C02 parent, B02/B03/B04/B05 material, C12, P6, D03/J1 exercised; plural native organization not proved. |
| G2 mother-owned act/expression | `HOLD_PARENT_SELECTOR_AND_LANGUAGE_OWNER`: C03 returns candidates only; C04 text/hidden reason are caller-supplied; `language_generation_owner: NOT_IMPLEMENTED`. |
| G3 hostile first consumer | `EXECUTED_SOURCEFREE_PASS` for the child-facing C04 custody and event/perception seal; exact residuals below. |
| G4 conservation/cold/economics | `EXECUTED_SOURCEFREE_PASS` for fresh-process cold, one speech, one purchase, zero rent, stable store head; branch-fork replay `UNOBSERVED`; provider cost `UNOBSERVED`. |
| G5 independent nonauthor receiving | This review: `ACCEPT_SCOPED` for child-facing C03/C04 sourcefree custody + material prospective readset. |

## Exact residuals and limits

1. **Parent self-read metadata is not exact.** `read_parent_utterance` /
   `_verify_utterance_custody` refuses forged `text`, `event_kind`,
   `event_authored_by`, `actor_id`, `root`, `branch`, `clock`, `decision_id`,
   `event_id`, `event_hash`, `child_perception_channel`, `hidden_reason`,
   `hidden_reason_hash`, `decision_action`, and `public_utterance`, but accepts
   and returns forged embedded-receipt `alias`, `operation_id`,
   `child_actor_id`, `child_alias`, `status`, `schema`, `grade`, `text_source`,
   `language_generation_owner`, `private_state`, `period_context`,
   `hidden_reason_source`, `custody`, `durable_acquisition`, and
   `native_science`. All corresponding child/P6/D03 readers refuse the required
   fields. No Nadia-facing effect or private-reason exposure was observed from
   this parent-only reader. This is recorded as a scoped residual, not accepted
   as exact parent self-read custody.
2. **D03 caller receipt binding.** D03 accepts a caller-supplied receipt with
   forged `root`, `branch`, `clock`, or `operation_id` with no observed output
   difference (author-disclosed). It refuses forged `decision_id`, `event_hash`,
   `actor_id`, `alias`, `text`, and `status`.
3. **Privileged coherent rewrite.** A writer able to rewrite the BP4 event, the
   C04 episode, and the C12 perceptions together can still satisfy local
   self-hashes; that is outside local read-side custody and remains source/
   append-owner authority.
4. **Branch-fork replay is UNOBSERVED**; no public C04 fork entry point exists
   at this cut.
5. **Provider/token cost, native psychology, human receiving, and protected
   integration were not observed**; tests are sourcefree and use no provider.
   Timings were taken under concurrent unrelated load and are not a benchmark.
6. **#1027 B04/B05 false-read defects** are separate owner risk under #1037;
   this review did not repair, accept, or generalize them as C04 failures.

## PROGRAMMA_DELTA

C03/C04 child-facing sourcefree custody and the material-prospective candidate
readset are independently received at the scoped grade. This receipt may release
separately authorized C05 custody work; it does not release G2, generated
language, complete J1, D04/D05, native/science/human/source rights, protected
merge, or a new fleet. No next job is launched.

**STOP.**
