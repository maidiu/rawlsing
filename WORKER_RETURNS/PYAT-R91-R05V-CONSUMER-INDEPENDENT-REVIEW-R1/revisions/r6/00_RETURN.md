# R91 R05V R6 independent review — return

Verdict: **REVISE.** R6 repairs the R5 slot/coordinator gap for actual AT10
discovery and AT11 recursive routes and exercises E41 route reconciliation. But
three actual-function gaps remain: the coordinator still mints a trusted original
through an unadmitted executor-only path; the trusted consumer does not bind the
submitted learned M1/M2/B5 to the retained original; and the actual joint route
still runs only through the raw compatibility API, not the trusted coordinator.
The actual source/evidence change also remains raw-only with no restore.

## Custody

- Stable root `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r91-r05v-r6-consumer-review-r1`; startup/HEAD
  `6a46e9e93ba148e4685aec585db70acf4cf84494`; clean at gate.
- R05V R6 commission `53488ef4...`; High decision `c618dc28...`; R6 contract
  `f069e1a80970d8b1601ec6de4156107d77bf48a5`; R6 code
  `4f2b097e433c2a6dfa986cccdcf85d637ba69c5e`; module blob `a486eddf...`, test
  blob `f3a90a53...`.
- Frozen EXPECTATIONS `bf3f7e983e1b191ed2ed43c7d977a5789e42a511`,
  committed before R6 code.
- R4 custody `0b60f26d...`; R5 `70d1d874...`; prior R5 review `73f6f1f...`.
  Accepted R08/provider/evaluator bodies unchanged; analytical R4 custody
  `ed2b1680...` remains within the five-path grant.
- R6 author manifest 7/7 independently matched; only authorized two code/test
  paths plus author r6 return changed.

## What R6 establishes

- Author 40/40; prior R1/R2/R3/R5 probes 19/19; provider 43/43; analytical
  composition 13/13.
- `NativeGraphSlot` now carries actual discovery result/receipt/frontier,
  recursive handoff/lineage/root-parent, condition witness, target arity/order,
  M1/M2/B5/currentness and E41 input fields.
- Coordinator executes actual AT10 discovery and AT11 recursive inputs through
  `compose_positioned_subject_possibility` and actual E41 extension from admitted
  slots; actual discovery/recursive positives use `trusted_graph_reader`; E41
  route/receipt and retained-original view checks pass.
- Actual joint arity 2 and R4 direct coordinator/typed axes remain.

## Remaining defects

### R6-P1 — Unadmitted executor-only coordinator still mints a trusted original

`TrustedNativeGraphCoordinator(executors={...})` with no `admitted_slots` still
runs the legacy fallback: a request slot selects an executor, which returns a
prebuilt actual composition; the coordinator validates fields and retains the
original. Independent probe `::test_unadmitted_executor_cannot_mint_trusted_original`
builds a single direct slot and executor from the actual M01 composition, calls
`execute`, and the trusted consumer returns `LEARNED_CONSUMER_EXACT_SUPPORTED`.
This is not an admitted operation and violates the High decision's
coordinator-owned admitted-input boundary and R6's contract claim "uses
independently admitted slots, never request-selected replacements."

### R6-P2 — Trusted consumer does not bind learned M1/M2/B5 to the retained original

The retained slot records M1 disposition/M2 release/B5 presence, but the
trusted consumer path does not compare the submitted `learned` object to them.
Independent probe `::test_trusted_consumer_binds_learned_m1_m2_b5_to_original`
captures the actual AT10 discovery trusted call and substitutes a second
productive learned product built from the same discovery with a different M1
disposition (`83220c...` vs `049214...`). The same retained graph/reader returns
`LEARNED_CONSUMER_EXACT_SUPPORTED`; the original M1/M2/B5 association is not
enforced.

### R6-P3 — Actual joint route still bypasses the coordinator; actual evidence change remains raw-only

The actual AT10 discovery test builds the joint composition and calls the raw
`evaluate_learned_world_consumer`; dynamic capture records
`raw_joint_calls=1, trusted_joint_calls=0`. The added `target_arity`/order slot
fields are not exercised through coordinator for the joint route. The actual
evidence-change composition is likewise raw and has no trusted-restore path.
The R6 return's claim that actual joint positives run through the coordinator is
not true.

## Exact missing function

1. Require `admitted_slots`/actual admitted inputs for `execute`; deny the
   executor-only fallback from minting a trusted original, or demote it to a
   non-exact compatibility view with no verified original.
2. Compare the submitted learned M1/M2/B5/currentness refs against the retained
   original slot before serving exact support; a different productive learned
   product must refuse/change.
3. Run the actual joint route through admitted coordinator slots and prove actual
   source/native evidence change and severed required dependency through the
   trusted reader with exact restore, not wrong-predicate-only/raw assertions.

No new authority, engine, provider or scientific aggregation is required. The
actual discovery/recursive/E41 coordinator capability is genuine partial work.

## Limits

Full live J42/P41/E04 remains NOT_REACHED; R04 independent. No original source/
science, F6/F7/FieldForge, CI/prod, N11/N12, Sorok, J52/W52 or adoption. Local
trusted-coordinator assumption; no OS/R09 protection. No candidate edit,
self-adoption or author wake.

Artifacts: `EXPECTATIONS.md`, `defects.md`, `limits.md`, `RESUME.md`,
`proof_witness.json`, `SHA256manifest.json`, `outcomes/r05v_r6_observations.json`,
`probes/test_r05v_r6_actual_gap.py`, prior probe copies, `junit/*.xml`,
`logs/stdout.jsonl`.
