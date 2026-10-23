# R61-R01V R5 independent native qualification return — REVISE

**Verdict: `REVISE` for R01 A4 at the generic recurrence interface.** Candidate
`4b5fd7a240a6e2d007ba1df2424780e6b5612ea9` / code
`c9cd59536e9323e6f48f1818bd41204cc6ae6095` preserves R3 A1–A3 and executes a
real synthetic D=3 chain, and its issue-time resolver repairs several R4
attacks. It does not, however, revalidate the receipt-bound parent at
execution, does not bind ancestry or producer generation to an independent
artifact, and lets a replaced predecessor plan undercount issued work. A4
remains **not qualified**. This is not R03 issuance/adoption and not original
science.

## Exact identity and separation

- Correction: `3249eb333e1288362af649242d17f5ae9e689817`.
- Original commission: `9307abc2a9a4177fc8964496334e74694f8ba711`.
- Candidate/startup: `4b5fd7a240a6e2d007ba1df2424780e6b5612ea9`.
- Candidate code: `c9cd59536e9323e6f48f1818bd41204cc6ae6095`.
- Reviewer branch: `agent/opencode-pyat-r61-r01v-r5-independent-review-r1`.
- Mandatory tool preflight passed exactly at review start:
  `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r5`, same top level,
  expected branch, no tracked changes.
- EXPECTATIONS bytes recovered unchanged from
  `1738231a9ede56ada79861dac83130aa55285520`:
  SHA-256 `394238be34b98431f819020997061df7fd96817913d7ad696ed7be4e94cca39b`.
  The original wrong-worktree freeze is acknowledged in the separate
  `OPERATIONAL_CUSTODY_CORRECTION.md`; it is not authorized or adopted.
- Reviewer session is distinct from author
  `ses_e98c905cbffekusoHURfKyEUKG`; the failed prior reviewer session is not
  product evidence. Same account/provider remains disclosed and is not
  institutional independence or proven OS isolation.

## Independent replay and positive evidence

| Suite | Result | Evidence |
|---|---|---|
| Author R5 suite | 26 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Prior R3 A1–A3 controls | 10 passed, 0 failed/error/skip | `replay/r3_controls_junit.xml`, `.log` |
| Reviewer changed-data D=3 positive | 2 passed | `replay/positive_probe_junit.xml`, `.log` |
| Reviewer expected-refusal attacks H1–H7 | 7 failed (all are candidate defects) | `replay/hostile_probes_junit.xml`, `.log` |

The reviewer positive used changed rows and an independently constructed
operation set plus independently recomputed root/parent typed states. It showed
a neutral-aggregate exploratory parent with 75%/25% opposite-direction hidden
subgroups, real D=3 execution, and a fresh-process persisted-handoff restore.
The author report manifest's 7 SHA-256 entries and four code blobs were
independently reproduced; the manifest explicitly excludes itself.

## Blocking findings (minimal reproducible)

1. **Execution does not revalidate the embedded parent binding.** A plan whose
   parent handoff is replaced with a different valid handoff (receipt/replay
   refs left stale) executes and anti-joins `no_drop_ok: true`
   (`evidence/defect_demonstrations.json`, `H3_execution_binding`). This
   contradicts the return's claim of checking "again before execution".
2. **Receipt-bound ancestry is not bound.** Stripping a canonical parent's
   `ancestry_conditions`/`ancestry_predicates` leaves `parent_id` unchanged;
   generation-2 issue and execution accept and anti-join true (`H1`).
3. **Receipt-bound generation can be relabelled to skip a generation.** A
   generation-1 handoff relabelled `generation=2` (with recomputed canonical
   id) is accepted as the parent for generation 3 and executes (`H2`).
4. **Replaced predecessor plan undercounts issued work.** With a real 4-
   operation generation-1 plan, replacing it with 2 operations and cumulative
   count 2 is accepted; generation 2 then issues 3 operations instead of the
   honest 1 (`H4`).
5. **Root parent is not bound to the declared root.** A root parent whose
   predicate is not `root_predicate` is accepted and executes, mixing the
   root-relative and parent-relative anchors (`H6`).
6. Secondary: a zero per-generation cap raises
   `RECURRENCE_GENERATION_ISSUED_NO_OPERATIONS` instead of `STOPPED_BUDGET`
   with unissued entries (`H5`); activation accepts the wrong
   `next_generation` label (`H7`).

Full analysis and required minimal functions are in `defects_and_limits.md`.

## A4 / R03 status and trust boundary

- A4 is **not qualified** at the generic consumer grain. The declared trusted
  resolver authenticates issue-time receipt/predicate/source consistency, but
  not execution-time plan integrity, ancestry, producer generation, or the
  predecessor ledger.
- R03 remains **NOT_STARTED**. No R03 prerequisite is discharged here.
- The trust seam is a declared host/coordinator resolver, not a protected
  issuer, signing service, global durable uniqueness or R09 isolation.
  R04/R09 service-level fork prevention is NOT_REACHED.
- Reference caps/rows are TEST_ONLY synthetic engineering, not original
  35/1890 science. No global F6/F7/F8, N11/N12, Sorok, production/CI or
  J52/W52 claim follows. No self-adoption or reviewer repair.

## Artifacts and remote verification

`EXPECTATIONS.md`, `OPERATIONAL_CUSTODY_CORRECTION.md`, `00_RETURN.md`,
`defects_and_limits.md`, `independent_probes/`, `replay/` JUnit/logs,
`evidence/` (startup identity, defect demonstrations, oracle results),
`proof_witness.json`, `manifest.json`, `RESUME.md`. The reviewer branch is
pushed non-force; direct remote readback of the evidence commit and final tip
is recorded in `evidence/remote_readback.txt` and reported to the coordinator.
