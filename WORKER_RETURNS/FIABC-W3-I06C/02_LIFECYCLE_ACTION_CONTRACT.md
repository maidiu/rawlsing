# FIABC-W3-I06C — Lifecycle Action Contract

## 1. Governing boundary

This contract implements the lifecycle/preserved-work portion of FIABC Wave-3 IMP11 under the FIABC-W2-B03 accounting constitution.

It does not redefine candidate semantics, source meaning, process isolation or telemetry semantics.

The atomic accounting key remains source-local:

`(source_id, source_sha256, candidate_id, candidate_owner_identity, workload_id, authority_set_identity, runtime_binding_identity, state_scope_identity)`

A successful lifecycle receipt also binds the expected governed terminal identity.

## 2. Integration order

The only lawful executed-now sequence is:

1. I06A supplies a valid process-isolation receipt for the exact source x candidate cell.
2. I06C constructs an exact `LifecycleBinding`.
3. I06C issues one `LifecycleActionRequest` naming the governed lifecycle operation.
4. The candidate/backend lifecycle port performs the actual candidate-state action.
5. The returned `ActionObservation` passes action-specific I06C validation.
6. Only then may I06B supply numeric telemetry.
7. Every I06B metric must bind both the validated `action_id` and exact `binding_id`.
8. I06C emits one immutable accounting receipt.

Telemetry presented before, instead of, or without an executed action is inadmissible.

## 3. I06A process-isolation input

`ProcessIsolationReceipt` requires:

- exact source ID;
- exact candidate ID;
- unique process token;
- candidate-root identity;
- `fresh_process_for_cell = true`;
- `cross_candidate_state_reachable = false`.

I06C does not spawn the process. It rejects lifecycle work if this proof does not match the lifecycle binding.

For fan-in, `ProcessIsolationReceipt.from_mapping()` is the normalization seam.

## 4. Lifecycle binding

`LifecycleBinding` fixes:

- source ID;
- source SHA-256;
- candidate ID;
- candidate-owner identity;
- frozen workload ID;
- frozen authority-set identity;
- runtime binding identity;
- candidate state-scope identity;
- expected final governed terminal identity;
- I06A isolation receipt.

The canonical `binding_id` hashes all these determinants plus the candidate process token/root. A lifecycle receipt from one candidate/process/state scope therefore cannot be silently reused by another.

## 5. Evidence kinds

Only:

`EXECUTED_CANDIDATE_ACTION`

can satisfy an executed lifecycle obligation.

The following are explicitly non-executed surrogate classes and are rejected:

- `FORMULA_DERIVED`
- `LAW_HASH_ONLY`
- `GENERIC_TEMP_FILE`
- `DECLARATIVE_ONLY`

These tags do not create truth by labeling alone; they make the interface fail closed when a sibling/backend tries to pass the known Wave-2 surrogate patterns through the lifecycle recorder.

## 6. Action-specific law

### 6.1 Cold first realization/open

Requires:

- exact lifecycle binding;
- candidate-owned accelerating cold state proved absent before action;
- actual action ID;
- pre/post state identities;
- governed terminal identity reproduced after the action.

A mere declaration that a run is "cold" is insufficient.

### 6.2 Warm retained-state use

Requires:

- retained-state object identity;
- retained-state owner equals current candidate;
- retained state is present in the candidate-owned pre-action state;
- final governed terminal identity reproduced.

State owned by A cannot warm B or C. State absent from the pre-action object set cannot create a warm metric.

### 6.3 Deletion / regeneration

Requires all of:

- non-empty deleted candidate-state object set;
- every deleted object was present before the action;
- non-empty regenerated candidate-state object set;
- every regenerated object is present after the action;
- deleted-to-regenerated lineage;
- governed terminal identity reproduced.

Receipt-writing time, cache-class prose, or a claimed rebuild without state deletion/regeneration cannot populate rebuild telemetry.

### 6.4 Source-release invalidation

Requires:

- exact invalidation trigger identity;
- actual invalidated governed unit IDs;
- actual recomputed unit IDs;
- terminal identity parity after recomputation.

`source_release_invalidation_recomputation_units` is accepted only when its value equals `len(recomputed_unit_ids)`.

No formula may assign this count.

### 6.5 Authority / semantic invalidation

Requires the same executed invalidation/recomputation structure at the authority determinant.

`semantic_authority_invalidation_recomputation_units` must equal the actual recomputed-unit lineage.

### 6.6 Stale-state detection and recovery

Requires:

- governed determinant identity before;
- different governed determinant identity after invalidation/change;
- stale state actually detected;
- recovery actually performed;
- terminal identity reproduced.

Hashing a stale-state law string is not candidate-state behavior.

### 6.7 Corrupt-state detection and recovery

Requires:

- corruption target is an actual candidate-owned object present before the exercise;
- corruption actually injected;
- corruption actually detected;
- recovery actually performed;
- terminal identity reproduced.

A digest of the intended corruption law is not a corrupt-state exercise.

### 6.8 Interruption recovery

Requires:

- interrupted operation exactly equals the governed candidate build/session operation;
- interrupted candidate-state object is part of the real candidate pre-action state;
- interruption actually injected;
- recovery resumes/rebuilds the same governed operation;
- recovery completes;
- terminal identity reproduced.

Creating and deleting an unrelated `*.partial` file cannot satisfy this contract.

### 6.9 Fresh-process replay

Requires:

- parent process token;
- replay process token;
- tokens differ;
- final governed terminal identity exactly matches the integrated court expectation.

Fresh replay is not satisfied by a second call inside the same process.

### 6.10 Audit/revalidation

Requires the action to name the exact governed audit primitive. Hashing already-held law/input strings under a narrower surrogate is inadmissible.

## 7. I06B telemetry input

I06C expects I06B to provide normalized `TelemetryMetric` records or a mechanically equivalent wrapper through `CallableTelemetryAdapter`.

Every measured lifecycle metric must include:

- metric name;
- metric unit;
- numeric nonnegative value;
- `state = MEASURED`;
- exact lifecycle `action_id`;
- exact lifecycle `binding_id`.

Reserved lifecycle metric names are action-class bound. For example, `delete_rebuild_wall_ns` is valid only for `DELETION_REGENERATION`, invalidation recomputation-unit fields are valid only for their corresponding invalidation action, and `fresh_process_replay_wall_ns` is valid only for `FRESH_PROCESS_REPLAY`. Generic resource fields such as CPU/RSS/I/O may accompany any executed action when I06B records them.

I06C does not measure CPU, RSS, wall time, I/O or scratch itself.

I06C only decides whether a lifecycle number is causally attached to the correct validated lifecycle action.

## 8. Accounting dispositions

Every final lifecycle/accounting record has exactly one HQ-facing disposition:

### `EXECUTED_NOW`

The lifecycle action actually executed under the current binding and admitted I06B metrics are action-bound.

### `LAWFULLY_PRESERVED_MEASURED_WORK`

At least one historical numeric field passed the final preserved-work compatibility court field-by-field.

This does not imply every requested metric was historically captured. Missing fields remain null.

### `PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY`

The preserved receipt remains semantically relevant, but no requested numeric metric qualifies for final comparison.

This includes LiTS-B and incompatible/missing LiTS-A telemetry fields.

### `NOT_REACHED`

The lifecycle stage was not reached under an authorized stop. Numeric values are forbidden.

### `NOT_APPLICABLE`

The frozen court says the operation/cost is not a candidate obligation at that grain. Numeric values are forbidden.

Common upstream capital uses this candidate-cost disposition; candidate-local access to that capital remains an independently executable C1 action when it occurs.

## 9. Preserved LiTS-A field-by-field admission

P006 LiTS-A does not receive automatic numeric credit.

`PreservedCompatibilityProof` must bind:

- exact preserved receipt ref;
- current lifecycle binding ID;
- workload compatibility;
- runtime-binding compatibility;
- state-binding/cold-state compatibility;
- process/isolation compatibility;
- operation equivalence;
- metric-definition equivalence for each numeric field admitted.

Only directly observed fields listed in `metric_definition_matches` become `MEASURED`.

A single failed operation-binding condition bars numeric credit for the preserved operation. Individual missing fields stay `MEASUREMENT_NOT_CAPTURED`.

## 10. Preserved LiTS-B

P007 proves semantic/identity work but its runner captured no numeric telemetry.

I06C therefore always produces:

`PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY`

for numeric lifecycle fields derived solely from that receipt.

The values are `null`, never `0`.

## 11. Calibration-only evidence

P008 pre-P2 Candidate-A evidence may carry historical numbers for planning. I06C never promotes those numbers into dispositive P2 comparison metrics.

## 12. Authorized stops

P009 stop evidence remains historical evidence.

Any unreached lifecycle metric is:

- disposition: `NOT_REACHED`
- metric state: `NOT_REACHED_AUTHORIZED_STOP`
- value: `null`

If an alleged unreached preserved stage also carries an ordinary numeric lifecycle metric, I06C rejects the receipt as an accounting-contract breach.

## 13. Terminal identity invariant

Every successful executed lifecycle action must reproduce the same expected governed terminal identity bound into the request.

This protects the court from "measuring" a lifecycle action that changed the meaning or output being compared.

The accounting layer therefore measures physical lifecycle work only while preserving semantic/output identity.

## 14. Fan-in rule

I06A and I06B may use different concrete class/function names.

HQ should adapt them at the narrow seams:

- I06A -> `ProcessIsolationReceipt`
- backend lifecycle implementation -> `LifecycleActionPort`
- I06B -> `TelemetryPort`

Do not move process logic or metric collection into I06C during fan-in.

Do not weaken I06C validation to match sibling convenience.
