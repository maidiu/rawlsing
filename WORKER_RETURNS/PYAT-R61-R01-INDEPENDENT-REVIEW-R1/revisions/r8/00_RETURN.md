# R61-R01V R8 independent native qualification return — ACCEPT_SCOPED_LOCAL

**Verdict: `ACCEPT_SCOPED_LOCAL`** for the exact R8 candidate under the declared
local trusted coordinator / TEST_ONLY profile. Candidate
`813775c07f0831605b6484a1d82afada30d85968` / code
`b57e6cf7544c9a66d5dc1c9c7b0ba9d5ba810369` fixes the four remaining R7
validation defects through the shared create/live/restore validator, and the
retained R7 native/cold/hostile positives still pass. A4 is qualified only at
this scoped generic campaign-owner grain; R03 remains NOT_STARTED and no
original/world/full-machine/science claim follows.

## Exact identity and separation

- Commission: `d5e9d097966401eee88005bba87084d6339e2685`.
- Previous R7 review: `bfebaeefa452eac90e4b2153c05d17b018347551`.
- R61AF adjudication: `e349da0d886d8e365648afccf40a2e6b8e105ff7`.
- R61V owner decision: `8c03f95ca77a4c874449fff67a4032f83d9d0a02`.
- Candidate/startup: `813775c07f0831605b6484a1d82afada30d85968`.
- Candidate code: `b57e6cf7544c9a66d5dc1c9c7b0ba9d5ba810369`.
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r8-independent-review-r1`.
- Mandatory first-tool preflight passed exactly in
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`, expected branch,
  no tracked changes.
- Reviewer EXPECTATIONS were frozen and committed (`74f8f1891`) before reading
  R8 candidate code, R8 author tests, the R8 return or the R8 contract.
- Reviewer is the existing distinct session, never author
  `ses_e98c905cbffekusoHURfKyEUKG`; same account/provider is disclosed and is
  not institutional independence or proven OS isolation.

## Independent replay and targeted R8 proof

| Suite | Result | Evidence |
|---|---|---|
| Author R8 suite | 32 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Previous R7 changed-data D=3 owner positive | 2 passed | `replay/positive_probe_junit.xml`, `.log` |
| Previous R7 owner controls | 15 passed | `replay/controls_junit.xml`, `.log` |
| Previous R7 hostile/closure suite | 9 passed | `replay/hostile_probes_junit.xml`, `.log` |
| R3 A1–A3 controls | 10 passed | `replay/r3_controls_junit.xml`, `.log` |
| R8 targeted defect proof | 4/4 former defects now typed-refuse | `evidence/targeted_results.json`, `targeted_proof.log` |

The previous R7 probes were copied unchanged as versioned adapters below the R8
own root; no archived probe was edited. Their former five failures now pass as
expected refusals, and their positive/control/cold cases remain green.

## Targeted R7 defects fixed

1. Wrong `target_label` with the original query and a query-target/label
   mismatch both raise `CAMPAIGN_TARGET_LABEL_QUERY_MISMATCH`; the correct label
   still creates/issues/executes.
2. Catalog `(s1,0)` bound to the `s1=1` predicate raises
   `CAMPAIGN_CONDITION_VALUE_PREDICATE_MISMATCH`; the correct predicate still
   works, and restore reuses the same validator.
3. Malformed public condition key raises
   `RecurrenceRefusal: CAMPAIGN_TYPED_OCCURRENCE_KEY_REQUIRED`, not
   AttributeError.
4. Duplicate condition refs raise `RecurrenceRefusal: DUPLICATE_CONDITION_REF`,
   not bare ValueError.

## Retained R7 native/cold/hostile evidence

The reviewer positive independently reconstructs expected operation sets and
multiplicity, recomputes root/parent typed states from changed rows, preserves
the neutral hidden 75/25 minority and nonwinning exploration, and runs real D=3
execution. Controls independently confirm multiple generation-1 batches
(cumulative 4 then 8), stopped/no-work predecessor advancement, pre-activation
restore/activation without rerunning discovery, post-activation existing
activation, native-call conservation, run-local concurrency, fixed original-pin
refusal, wrong query/catalog refusal, duplicate catalog/missing release refusal,
typed receipt states and inflight typed HOLD. The author manifest's seven report
hashes and four code blobs were independently reproduced; the manifest
self-excludes.

## Scope, limits and NOT_REACHED

- A4 is qualified only as the declared local trusted campaign-owner facade under
  TEST_ONLY synthetic inputs. No protected issuer, signing service, global
  durable uniqueness, R04 joined custody or R09 capture is claimed; R04/R09 fork
  prevention is NOT_REACHED.
- Fixed original pin refuses altered/rehashed snapshots and missing pins;
  forged snapshot plus forged trusted pin is the declared R61AF host-trust
  boundary, not an in-scope refusal gate. No new pin service is required.
- Canonical-authorized question-ref inventory variants outside the native
  TEST_ONLY fixture were not independently constructed; no universal inventory
  claim is made.
- R03 remains NOT_STARTED. No original 35/1890, global F6/F7/F8, N11/N12,
  Sorok, production/CI or J52/W52 claim follows. No self-adoption or reviewer
  repair. R08/R61Q is a separate lane and was not reviewed, repaired or
  certified here.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/` (startup identity,
targeted proof, oracle results), `proof_witness.json`, `manifest.json`,
`RESUME.md`. The reviewer branch is pushed non-force. Evidence commit
`36a4e3593609aa348514c5a75562398930dc645f` was directly read back at the
remote, as recorded in `evidence/remote_readback.txt`; the final branch tip is
also verified by direct remote readback and reported to the coordinator. The
candidate branch remained at `813775c07f0831605b6484a1d82afada30d85968`.
