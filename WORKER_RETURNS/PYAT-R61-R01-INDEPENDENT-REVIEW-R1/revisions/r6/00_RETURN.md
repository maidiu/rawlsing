# R61-R01V R6 independent native qualification return — REVISE

**Verdict: `REVISE` for R01 A4 at the exact generic campaign-owner interface.**
Candidate `fea3ca17d94183efbd526dc1687ae06b7bbbf0f7` / code
`3d60f9cb6f43830244fbd79699d1cf4041622d05` implements a real retained local
campaign owner and defeats the old live plan/parent injection attacks. It does
not validate source/release compatibility at creation, does not validate the
supplied query/condition context at restore, admits a self-consistent forged
snapshot with a forged pin, and refuses generation-1 multiple batches. A4 is
not qualified. This is not R03 issuance/adoption and not original science.

## Exact identity and separation

- Commission: `d737562873558ce01116f079815b00bdb06416fe`.
- R61V owner decision: `8c03f95ca77a4c874449fff67a4032f83d9d0a02`.
- Candidate/startup: `fea3ca17d94183efbd526dc1687ae06b7bbbf0f7`.
- Candidate code: `3d60f9cb6f43830244fbd79699d1cf4041622d05`.
- Author API freeze: `e2b87e6c33364e5361ed3c0b10ba5c13e34efbba`.
- Prior R5 review: `537bd3985d8a3825186e41cab9308d8150cac848` (unchanged).
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r6-independent-review-r1`.
- Mandatory first-tool preflight passed exactly in
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`, expected branch,
  no tracked changes.
- Reviewer EXPECTATIONS were frozen and committed (`bd0e662e6`) before reading
  R6 candidate code, R6 author tests, the R6 return or the author API contract.
- Reviewer is the existing distinct session, never author
  `ses_e98c905cbffekusoHURfKyEUKG`; same account/provider is disclosed and is
  not institutional independence or proven OS isolation.

## Independent replay and positive evidence

| Suite | Result | Evidence |
|---|---|---|
| Author R6 suite | 28 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Prior R3 A1–A3 controls | 10 passed, 0 failed/error/skip | `replay/r3_controls_junit.xml`, `.log` |
| Reviewer changed-data D=3 owner positive | 2 passed | `replay/positive_probe_junit.xml`, `.log` |
| Reviewer owner controls | 8 passed | `replay/controls_junit.xml`, `.log` |
| Reviewer expected-refusal/positive attacks H1–H8 | 8 failed (all candidate defects) | `replay/hostile_probes_junit.xml`, `.log` |

The reviewer positive used changed rows, independently constructed expected
operation sets and independently recomputed root/parent states. It showed a
neutral 50/50 exploratory parent with 75/25 opposite hidden subgroups, real
D=3 native execution, nonwinning exploration, and both in-process and
fresh-process post-activation snapshot restore followed by actual next-batch
execution. Controls independently confirmed retry idempotency/no second native
call, zero-cap no-native-call, forged lineage/label/predecessor refusals,
cross-campaign lineage refusal, deep-detached inspect, altered snapshot with
the original pin refusal, multiple generation-2 batches, and run-local
concurrent execute serialization. The author manifest's 7 report hashes and
four code blobs were independently reproduced.

## Blocking findings (minimal reproducible)

1. **Create does not validate source/release compatibility.** A fabricated
   release ref absent from the repository is accepted; issue and execute
   succeed with `no_drop_ok: true`, and receipts claim the nonexistent release
   (`evidence/defect_demonstrations.json`, `H2_bogus_release`).
2. **Restore accepts a wrong query context.** Restoring with a different query
   object succeeds; the next issue/execute uses a plan `query_ref` that differs
   from the retained `root.query_ref` (`H3_wrong_restore_query`). An incomplete
   frozen condition catalog is also accepted (`H8`).
3. **Self-consistent forged snapshot with a forged pin is admitted.** The
   restored campaign keeps the original `campaign_ref` and exposes forged
   lineage (`H4`). The original pin correctly rejects the same snapshot, so the
   missing function is an independently retained pin anchor, not the self-hash.
4. **Generation-1 multiple batches are refused** with
   `ROOT_GENERATION_MUST_NOT_HAVE_PREDECESSOR` (`H1`), contrary to C.2/E/F4,
   while generation-2 multiple batches work and count correctly.
5. Secondary: a pre-activation restored execution cannot activate
   (`RESTORED_EXECUTION_NATIVE_RESULT_NOT_REPLAYED`, `H5`); stopped-budget
   issuances do not advance the predecessor ref (`H6`); duplicate condition
   catalog entries silently collapse (`H7`); Execute revalidates only part of
   the retained parent identity (`defects_and_limits.md`, D8, no live public
   injection found).

Full analysis and minimal missing functions are in `defects_and_limits.md`.

## A4 / R03 status and trust boundary

- A4 is **not qualified** at the generic campaign-owner grain. The retained
  owner is a real advance over R5 but does not yet satisfy R61V sections A,
  C.1, C.3, D and F1/F4/F5.
- R03 remains **NOT_STARTED**. No R03 prerequisite is discharged here.
- Trust seam remains a declared trusted local coordinator campaign; no
  protected issuer, signing service, global durable uniqueness, R04 joined
  custody or R09 capture. R04/R09 fork prevention is NOT_REACHED.
- Reference caps/rows are TEST_ONLY synthetic engineering, not original
  35/1890 science. No global F6/F7/F8, N11/N12, Sorok, production/CI or
  J52/W52 claim follows. No self-adoption or reviewer repair.
- R08/R61Q projection/export is a separate author lane and was not inspected,
  repaired or certified by this R01V reviewer.

## Artifacts and remote verification

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/` JUnit/logs, `evidence/` (startup identity,
exploration, defect demonstrations, oracle results), `proof_witness.json`,
`manifest.json`, `RESUME.md`. The reviewer branch is pushed non-force; direct
remote readback of the evidence commit and final tip is recorded in
`evidence/remote_readback.txt` and reported to the coordinator. The candidate
branch is expected to remain at `fea3ca17d94183efbd526dc1687ae06b7bbbf0f7`.
