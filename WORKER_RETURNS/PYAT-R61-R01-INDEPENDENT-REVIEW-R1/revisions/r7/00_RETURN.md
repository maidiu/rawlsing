# R61-R01V R7 independent native qualification return — REVISE

**Verdict: `REVISE` for R01 A4 at the exact generic campaign-owner interface.**
Candidate `9c0f81ecb76ffe35d0190e31492ea1e9b568f01b` / code
`0271a7e37a3ccccce5ff69db99f56f7745a62875` is a substantial whole-function
repair: create resolves native context, chronology is independent of
generation, multiple generation-1 batches and stopped/no-work prefixes count
correctly, pre-activation restore activates without rerunning discovery, fixed
original-pin restore and full record closure work, and the native
changed-data/minority/cold positives pass. Four remaining facade-validation
defects prevent `ACCEPT_SCOPED_LOCAL`. This is not R03 issuance/adoption and not
original science.

## Exact identity and separation

- Commission: `fbb162a0717bb067b7f2e244d738c33cd13f49af`.
- R61AF adjudication: `e349da0d886d8e365648afccf40a2e6b8e105ff7`.
- R61V owner decision: `8c03f95ca77a4c874449fff67a4032f83d9d0a02`.
- Candidate/startup: `9c0f81ecb76ffe35d0190e31492ea1e9b568f01b`.
- Candidate code: `0271a7e37a3ccccce5ff69db99f56f7745a62875`.
- Prior R6 review: `568ff717662ac1ee63d29bad3080deaf10bd17f9` (unchanged).
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r7-independent-review-r1`.
- Mandatory first-tool preflight passed exactly in
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`, expected branch,
  no tracked changes.
- Reviewer EXPECTATIONS were frozen and committed (`615a79058`) before reading
  R7 candidate code, R7 author tests, the R7 author return or the R7 contract.
- Reviewer is the existing distinct session, never author
  `ses_e98c905cbffekusoHURfKyEUKG`; same account/provider is disclosed and is
  not institutional independence or proven OS isolation.

## Independent replay and positive evidence

| Suite | Result | Evidence |
|---|---|---|
| Author R7 suite | 31 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Prior R3 A1–A3 controls | 10 passed, 0 failed/error/skip | `replay/r3_controls_junit.xml`, `.log` |
| Reviewer changed-data D=3 owner positive | 2 passed | `replay/positive_probe_junit.xml`, `.log` |
| Reviewer owner controls | 15 passed | `replay/controls_junit.xml`, `.log` |
| Reviewer hostile/closure suite | 5 failed, 4 passed | `replay/hostile_probes_junit.xml`, `.log` |

The positive used changed rows, independently constructed expected operation
sets and independently recomputed root/parent states. It showed a neutral 50/50
exploratory parent with 75/25 opposite hidden subgroups, real D=3 execution,
nonwinning exploration, and in-process plus fresh-process post-activation cold
restore followed by actual next-batch execution. Controls independently
confirmed multiple generation-1 batches (4 then 8), stopped/no-work predecessor
advancement, pre-activation restore/activation without rerun, post-activation
existing activation, native-call conservation, run-local concurrency, fixed-pin
refusal, wrong query/catalog refusal, typed receipt states and inflight HOLD.
The author manifest's 8 report hashes and four code blobs were independently
reproduced.

## Blocking findings (minimal reproducible)

1. **Target label is not tied to the query target.** `target_label="wrong-label"`
   with the unchanged `t` query is accepted and executed
   (`evidence/defect_demonstrations.json`, `H1_target_label_mismatch`); a query
   targeting `s3` with `target_label="t"` is also accepted and executed
   (`H2`). R61AF requires target/query compatibility.
2. **Condition catalog key/value is not tied to predicate semantics.** Catalog
   entry `(s1,0)` can be bound to the `s1=1` predicate; creation, issue and
   execution succeed, and the plan labels the condition `s1=0` while executing
   the `s1=1` predicate (`H3`). This violates the complete typed condition
   inventory and the label/fact distinction.
3. **Malformed public condition key raises raw `AttributeError`.** `issue`
   with a string key instead of `OccurrenceKey` crashes rather than typed-refuse
   (`H4`).
4. Secondary: duplicate condition refs raise bare `ValueError` with
   `RECURRENCE_DUPLICATE_CONDITION_PREDICATE` rather than `RecurrenceRefusal`
   (`H5`).

Full analysis and minimal missing functions are in `defects_and_limits.md`.

## R61AF fixed-pin correction

R61AF reclassifies forged-snapshot-plus-forged-pin as host-trust replacement,
not an in-scope refusal gate. We did not use it as a defect. The fixed original
pin correctly refuses altered/rehashed snapshots and missing pins; genuine
snapshots restore. R7's internal closure additionally refused the forged-lineage
mutation even with both inputs forged (`RESTORE_FULL_RECORD_CLOSURE_MISMATCH`),
which is stronger than required and recorded only as a host-trust demonstration.

## A4 / R03 status and trust boundary

- A4 is **not qualified** at the generic campaign-owner grain because the whole
  facade still accepts target/query and catalog-key/predicate misbindings and
  has a public typed-refusal gap.
- R03 remains **NOT_STARTED**. No R03 prerequisite is discharged here.
- Trust seam remains a declared trusted local coordinator campaign; no
  protected issuer, signing service, global durable uniqueness, R04 joined
  custody or R09 capture. R04/R09 fork prevention is NOT_REACHED.
- Reference caps/rows are TEST_ONLY synthetic engineering, not original
  35/1890 science. No global F6/F7/F8, N11/N12, Sorok, production/CI or
  J52/W52 claim follows. No self-adoption or reviewer repair.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/` (startup identity,
exploration, closure, defect demonstrations, oracle results),
`proof_witness.json`, `manifest.json`, `RESUME.md`. The reviewer branch is
pushed non-force. Evidence commit
`257a0af9ea2bf76805862b7e0ee8e8451837b6b3` was directly read back at the
remote, as recorded in `evidence/remote_readback.txt`; the final branch tip is
also verified by direct remote readback and reported to the coordinator. The
candidate branch remained at `9c0f81ecb76ffe35d0190e31492ea1e9b568f01b`.
