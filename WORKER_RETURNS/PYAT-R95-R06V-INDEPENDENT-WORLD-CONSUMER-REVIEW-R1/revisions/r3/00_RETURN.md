# R95-R06V R3 independent exact-boundary successor review — REVISE

**Verdict: `REVISE`.** The four named repairs are not all complete. The author
R3 suite passes 14/14, the five prior independent probes pass, the equal-payload
temporal control refuses, and the actual R05->P41 positive/restore is preserved.
But a caller-supplied forged P41 runtime returning canned receipts is accepted
as actual execution, an arbitrary subject-selected coordinator original is
emitted as authenticated output, and the joined wrapper accepts an arbitrary
real-type `StructuralEmpiricalAdmission` as CONTEXT-to-STRUCTURAL authority.
The exact R3 boundary obligations are therefore not satisfied.

## Exact identity and separation

- R3 commission: `0fcf61136bbd05a184034c05990a87a6a8a9b6a7`.
- Exact candidate/startup: `02800fcfd77abde178851031f877838bedb5e242`.
- Author R3 contract/code: `033efe2b4a636d909fe4def2056aa5c68762e182` /
  `d0690af0c85fca962a4ac1e08012e869e94cb404`.
- Prior full review commission/oracle:
  `e2776897af673f14237178daf7ae35c2331d48af` /
  `0153d1f9b88ede3f76e5b1658a7441cb2e9a1713`.
- R95 grant: `1315aff53c3eb063a65088fcb5bd8398852668fa`.
- Reviewer branch: `agent/opencode-pyat-r95-r06v-r3-world-consumer-review-r1`.
- Root/branch/HEAD gate passed at the stable worktree; only generated untracked
  pycache/temp runtime material was present. Existing distinct R06V reviewer,
  not author/HQ; no candidate edit.
- Reviewer EXPECTATIONS were frozen and committed at `535a936b2` before R3
  code/probe inspection.
- Only the two authorized R06 paths differ from startup in `rawlsing_next/`:
  `pre553_universal_world_binding.py`,
  `tests/test_universal_world_binding.py`. Actual code blobs:
  `f695d8974c1b5cf617213a9976620defc91fb270`,
  `a0cdee8d481382a4fd1e6065206badd99398192f`.

## Independent replay

| Suite | Result | Evidence |
|---|---|---|
| Author R3 suite | 14 passed, 0 failed/error/skip | `replay/author_suite_junit.xml`, `.log` |
| Prior R06V five probes | 5 passed | `replay/prior_probes_junit.xml`, `.log` |
| R3 successor controls | 3 passed, 3 failed | `replay/successor_probes_junit.xml`, `.log` |

Successor passes:

- `S2`: R05 forged real-type FF admission refusal (but see FF defect; the
  refusal is from `ExactRef` vs canonical MappingProxy source comparison, not
  actual issuance/authority validation).
- `S4`: equal actual payload with distinct clocks refuses
  `R05_TEMPORAL_PAIR_NOT_CONSUMED`.
- `S5`: genuine actual positive, hostile caller callback refusal, restore.

Successor failures:

1. **`S1` forged runtime accepted.** A fake `p41_service.P41Service` under a
   caller-supplied `R05ActualExecution.p41_runtime` returned canned,
   self-consistent T0/T1 receipts; `select_r05_world_view` returned
   `R05_WORLD_SELECTED_VIEW` without invoking the actual pinned P41 owner.
2. **`S3` subject-selected coordinator original accepted.** Replacing
   `R05ActualExecution.coordinator_original_ref` with an arbitrary forged
   `ExactRef` still produced an accepted view and emitted the forged original.
3. **`S6` joined FF forged real-type accepted.** A fabricated
   `StructuralEmpiricalAdmission` with arbitrary content but the required
   type/state/target satisfied `select_joined_world_view` and produced
   `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` for a CONTEXT field. The R05 and
   simple wrappers do not accept the same forged object only because their
   canonical-source comparison is also broken (see defect 3).

## Four-repair qualification

1. **Actual P41/E04 invocation — NOT complete.** Host-retained construction and
   callback refusal exist, but the runtime/service is imported from an
   unpinned caller path and the actual execution/original is not independently
   authenticated. `S1` and `S3`.
2. **Actual temporal dependence — complete for this synthetic pair.** `S4`,
   prior `H1` and the author no-change test refuse equal actual payloads;
   positive actual route/N10W change, cold replay, current/as-of, revocation
   and restore remain. `S5` and author 14/14.
3. **Cross-unit linkage — complete at the public wrappers.** Prior `H2`,
   author transport controls, and all three wrappers return
   `CROSS_UNIT_LINKED_QUERY_UNAVAILABLE` for label-only pooling; genuine linked
   indexed query is not invented.
4. **FF admission — NOT complete.** The joined wrapper accepts an arbitrary
   real-type admission; the source/field comparison used by R05/simple wrappers
   compares an `ExactRef` to canonical `MappingProxy` refs and therefore cannot
   accept a genuine canonical admission either. No actual issuance/authority
   closure is validated. `S6`.

## Exact missing functions

- In `_execute_p41_world`, pin/verify the actual P41 runtime/service identity
  and content (or construct the accepted actual owner internally from a
  host-retained invariant) instead of importing `bootstrap`/`p41_service`/
  `product.world` from an arbitrary `p41_runtime` string. Reject forged runtime
  modules/service returning canned receipts.
- Bind `R05ActualExecution.coordinator_original_ref` to an independently
  retained actual R05/R03 coordinator original and verify its exact content/ref;
  do not copy a subject-selected ref into `r05_binding`/the view. Refuse mismatch.
  The same independent-original check should cover the actual learned/step
  inputs, not only equality between two caller-supplied copies.
- Use one canonical ref comparison for `StructuralEmpiricalAdmission`
  source/field refs (canonical MappingProxy vs `ExactRef`), and validate actual
  competent admission issuance/authority closure, not merely real type/state/
  target. Apply to `select_joined_world_view` as well as `select_world_view` and
  `select_r05_world_view`; otherwise return typed unavailable/refusal. Preserve
  the genuine direct STRUCTURAL positive and do not invent F5/F6/F7 science.
- No candidate repair, new worker/provider, or new R09 trust service is added.

## Retained positive evidence

- Author R3 14/14; prior R06V 5/5; actual R05 learned
  `LEARNED_CONSUMER_EXACT_SUPPORTED` -> actual P41 N9/N10W/E04 receipt with
  routes `ELIGIBLE/WITHIN_MODELED_BUDGET` ->
  `BLOCKED_BY_MODELED_RULE/RESOURCE_CONSTRAINED`, N10E bound to the R05
  consumer hash and coordinator original present.
- Two real fields affect the same actual routes/assertion; `S5` positive and
  restore are preserved.
- Cold fresh-process replay, current/as-of, revocation, severance/restore and
  R1 J42/N10E genuine positives remain; cross-unit label positives are now
  typed UNAVAILABLE.
- U43/R03/R04/R05/R08/native/FF/temporal/J42/P41/E04 bodies unchanged; only the
  two authorized R06 paths differ from startup.

## Limits and NOT_REACHED

Sourcefree TEST_ONLY local trusted host only; no source respondent access. No
cryptographic/R09 isolation; the reviewer does not accept the author's
convention that `R05ActualExecution` is host-retained as authentication because
the public request accepts a forged runtime/original and mints output.
Original F7 measured waves, original 35/1890/F6/F8, source/science, F5/F6/F7
issuance, CI/prod, N11/N12, Sorok and J52/W52 remain held/NOT_REACHED. The
temporal pair is declared synthetic modeled-rule software evidence, not
original F7 issuance. No self-adoption, production merge or R05 wake.

## Artifacts and remote verification

`EXPECTATIONS.md`, this return, `defects_and_limits.md`, `RESUME.md`,
`independent_probes/` (`test_r06v_world.py`, `test_r06v_r3_successor.py`),
`replay/` JUnit/logs, `evidence/commands.txt`, `proof_witness.json`,
`manifest.json` (self-excluding), and `evidence/remote_readback.txt`. The
reviewer branch is pushed non-force; direct remote SHA readback is recorded
after the evidence push and reported to the coordinator. The candidate branch
remains at `02800fcfd77abde178851031f877838bedb5e242` throughout this review.
