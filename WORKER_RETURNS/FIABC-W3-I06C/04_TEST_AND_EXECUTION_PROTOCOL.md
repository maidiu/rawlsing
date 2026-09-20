# FIABC-W3-I06C — Test and Execution Protocol

## Status in this worker

Implementation and hostile tests were authored with GitHub/browser repository tools only.

No local-machine Codex was used.

No measured P2X was run.

No source carrier was executed.

The tests in this branch are therefore **UNEXECUTED** at worker-return time. This is intentional and must not be rewritten as a PASS.

## 1. Browser/fan-in static review

Before execution, HQ should verify on the integrated fan-in tree:

1. I06A can normalize its exact process-isolation receipt into `ProcessIsolationReceipt` without dropping source/candidate/process/root identity.
2. I06B can normalize its metric records into `TelemetryMetric` with exact `action_id` and `binding_id`.
3. The P2X backend lifecycle handlers call `execute_lifecycle_action` only around actual candidate-state operations.
4. Old S09-S14 surrogates are not left as alternate PASS paths.
5. Candidate-specific N/A law is expressed with `typed_not_applicable_receipt`, not a zero-valued executed receipt.
6. Authorized stop logic uses `typed_unreached_receipt`.
7. P006 preserved LiTS-A credit passes through `adjudicate_preserved_work`; no historical number is copied directly into final metrics.
8. P007 LiTS-B telemetry remains null.
9. P008 calibration numbers never enter final P2 comparison.
10. Final lifecycle success remains bound to the integrated court terminal identity.

## 2. Unit test command

After fan-in onto a tree with the normal Python runtime available, run:

```bash
python -m unittest tests.test_fiabc_lifecycle_accounting -v
```

Expected hostile coverage:

- formula-derived invalidation work rejected;
- formula-like recomputation number differing from observed unit lineage rejected;
- law-hash stale/corrupt evidence rejected;
- generic temp-file interruption evidence rejected;
- rebuild without deletion/regeneration rejected;
- warm run without valid retained candidate state rejected;
- preserved incompatible state/binding barred from numeric credit;
- missing LiTS-B telemetry remains null;
- unreached stage cannot carry ordinary numeric metric;
- Candidate-A preservation cannot satisfy Candidate-B;
- fresh replay exact terminal identity accepted;
- wrong-terminal replay rejected.

The command above was **not run by FIABC-W3-I06C**.

## 3. Integration adapter qualification

After I06A/I06B fan-in, add or bind thin integration tests proving:

### I06A seam

Input:

- exact source/candidate cell;
- fresh process token;
- candidate-root identity;
- no reachable prior-candidate state.

Acceptance:

- `ProcessIsolationReceipt.validate()` passes for the same source/candidate;
- changing candidate/source causes fail-closed rejection;
- `fresh_process_for_cell=false` rejects;
- `cross_candidate_state_reachable=true` rejects.

### I06B seam

For one executed lifecycle action:

- I06B metric `action_id` must equal `ActionObservation.action_id`;
- I06B metric `binding_id` must equal exact `LifecycleBinding.binding_id`;
- a mismatched action/binding metric must fail before receipt emission;
- expected lifecycle metrics omitted by I06B must fail the executed-now contract rather than become zero.

## 4. Backend lifecycle qualification without measured P2X

This step may use deterministic fixtures/mocks or non-dispositive test state. It must **not** run measured P2X.

For each applicable action, exercise the backend adapter and inspect the I06C action observation:

### Cold first realization/open

- establish candidate-owned cold predicate;
- execute real candidate open/build;
- prove terminal identity.

### Warm retained-state use

- retain exact same-candidate state from the authorized cold action;
- execute governed warm repeat;
- prove retained state owner and object identity;
- prove terminal identity.

### Deletion/regeneration

- identify actual candidate-owned regenerable object(s);
- delete them;
- regenerate/rebind them through the candidate path;
- prove lineage;
- prove terminal identity.

### Source invalidation

- execute the governed source-release determinant change/invalidation fixture;
- record exact invalidated and recomputed unit IDs;
- verify metric count equals actual recomputed unit count;
- restore/finalize exact terminal identity.

### Authority/semantic invalidation

Use the same pattern at the semantic/authority determinant.

### Stale state

- alter/invalidate the governed determinant that makes retained state stale;
- observe detection;
- recover/rebuild/fail-closed according to candidate law;
- reproduce terminal identity.

### Corrupt state

- corrupt an actual candidate-owned regenerable state object;
- observe corruption detection;
- recover/fail closed;
- reproduce terminal identity.

### Interruption

- interrupt the real candidate build/session at an authorized checkpoint;
- prove the interrupted state belongs to that operation;
- recover/resume/rebuild the same operation;
- reproduce terminal identity.

A generic unrelated `*.partial` file is not an acceptable fixture.

### Fresh-process replay

- spawn/consume I06A fresh replay process proof;
- replay exact governed workload;
- prove replay process token differs;
- prove exact terminal identity.

### Audit/revalidation

- call the exact governed audit primitive;
- do not substitute a narrower law-string hash;
- prove final identity.

## 5. Preserved-work qualification

### P006 LiTS-A

Load the preserved receipt:

`WORKER_RETURNS/EE-P2X/01_LITS_I_A_FIRST_BUILD_STAGE.json`

Normalize only directly observed historical fields.

Construct `PreservedCompatibilityProof` only after final fan-in proves:

- source identity equality;
- candidate A equality;
- exact workload equality;
- exact runtime binding compatibility;
- exact cold/state binding compatibility;
- required process/isolation compatibility;
- operation equivalence;
- field-level metric-definition equivalence.

Then run `adjudicate_preserved_work`.

Acceptance:

- qualifying fields may be `MEASURED` under `LAWFULLY_PRESERVED_MEASURED_WORK`;
- every nonqualifying/missing field remains `MEASUREMENT_NOT_CAPTURED` with value `null`;
- no all-or-nothing synthetic vector is produced.

### P007 LiTS-B

Load:

`WORKER_RETURNS/EE-P2X/03_LITS_I_B_CACHELESS_C11_STAGE.json`

Acceptance:

- semantic evidence preserved;
- requested numeric fields remain `null`;
- disposition remains `PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY`;
- zero substitution fails review.

### P008 calibration

Any numeric calibration evidence remains excluded from dispositive P2 metrics.

### P009 stopped work

For each stopped stage:

- preserve reached evidence;
- emit `NOT_REACHED` for unreached lifecycle actions;
- ordinary numeric unreached metrics are forbidden.

## 6. Integrated pre-measurement acceptance

I06C is ready for measured-court use only after integrated qualification proves:

- all required I06A isolation receipts;
- all I06B metric binding semantics;
- all applicable lifecycle adapters execute candidate state rather than surrogates;
- all required terminal identities reproduce;
- preserved-work adjudication passes field-by-field;
- typed null/N/A/stop states survive final serialization.

This gate is qualification only. It does not itself authorize measured P2X; the wider Wave-3/HQ gates still control measured execution.

## 7. Forbidden substitutions

Do not accept any of the following as evidence that this protocol passed:

- a formula for recomputation work;
- a hash of lifecycle law text;
- a generic temp-file create/delete cycle;
- endpoint directory size standing in for observed I/O;
- candidate A preservation copied into candidate B;
- missing numeric telemetry coerced to zero;
- same-process replay labeled fresh;
- successful lifecycle state with a different terminal identity.

## 8. Required terminal after integrated qualification

The worker implementation terminal remains:

`FIABC_W3_I06C_LIFECYCLE_AND_PRESERVED_WORK_ACCOUNTING_IMPLEMENTED__READY_FOR_FANIN`

Integrated test PASS, when later executed, must be reported separately by HQ and must not be backfilled into this browser worker return.
