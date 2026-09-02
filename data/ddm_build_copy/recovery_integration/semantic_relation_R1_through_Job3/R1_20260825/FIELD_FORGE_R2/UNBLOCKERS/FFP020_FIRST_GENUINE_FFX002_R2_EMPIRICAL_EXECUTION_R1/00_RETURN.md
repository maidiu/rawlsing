# FFP020 — FIRST GENUINE FFX002-R2 EMPIRICAL EXECUTION + MAXIMAL-UTILITY ABLATION — RETURN R1

Status:

`PARTIAL__Q03_REFERENCE_TARGET_AND_FROZEN_SUBSTRATE_EVIDENCE_BANKED__MANDATORY_CORE_B_GENUINE_SCALE_IMPLEMENTATION_BLOCKS_COMPLETE_FFX002_R2_EXECUTION`

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-field-forge-r2-ffp020-first-genuine-ffx002r2-empirical-execution-r1`

Exact starting HEAD: `433104a5bb1e7ada710c6243413e6061a4ca41cf`

Jurisdiction: FFP020 empirical calibration only. No CIM mutation, CITC mutation, comparison-identity mutation, TTAR minting, PRA mutation, actor/V3 interpretation, production-architecture generalization, second canary, or final CVCR/COCR disposition was performed.

## 1. Exact frozen evidence recovered and verified

FFP017 Library-backed empirical artifacts were materialized from:

`/Rawlsing/FIELD_FORGE_R2/FFP017_FIRST_GENUINE_CANARY_COEXPOSURE_RISKSET_R1`

Their bytes were independently SHA-256 verified against the governed FFP017 pointer manifest. The exact common risk set contains `19,210` governed respondents. Filtering the frozen selected-response facts to that exact risk set yields exactly:

`19,210 respondents × 13 selected measurements = 249,730 respondent-measurement rows`

with zero missing risk-set measurement cells. No exposure fact was inferred from response missingness.

Exact Q73A native state counts inside the frozen risk set are:

- `Q73A=-1`: `5`
- `Q73A=0`: `7,466`
- `Q73A=1`: `10,161`
- `Q73A=9`: `1,578`

Thus the exact frozen Q03 baseline/comparison denominators reproduce FFP019 exactly: `7,466` and `10,161`.

The FFP017 native `Q86A×Q86B×Q86C` J3 inventory contains `38` exact observed configurations whose support sums to the full `19,210` respondents. This survives as higher-order substrate information. It is not promoted into a Core-A result and is not constitutive of Q03.

See:

- `01_Q03_EXACT_REALIZED_SAMPLE_TARGET_VECTOR.json`
- `03_SURVIVING_EMPIRICAL_EVIDENCE_RECEIPT.json`

## 2. Exact Q03 realized-sample reference target banked

From the frozen FFP017 substrate and the dispositive FFP016 role assignments, FFP020 computed and banked the exact representation-independent Q03 reference target:

`Delta_D(s) = P_sample(D=s | Q73A=1) - P_sample(D=s | Q73A=0)`

for every exact native state `s` of every FFP016 `ACTIVE_DISPOSITION` measurement:

`Q76A, Q76B, Q86A, Q86B, Q86C, Q86D, Q86E, Q86F`.

The banked target contains `34` exact disposition-state components. It uses raw realized-sample counts only: no weighting, pooling, rebinning, harmonization, imputation, special-state collapse, Q84 cross-country equivalence, response-missingness exposure inference, or TTAR operation.

Artifact:

`01_Q03_EXACT_REALIZED_SAMPLE_TARGET_VECTOR.json`

SHA-256:

`8c5e69b2f1aeb86a5988b4ef587016bab10ef214a955e96d357db08dae49781b`

This is a **reference target from the frozen common substrate**, not an A/B/C representation output and not a self-certification of any view. It exists so a later lawful view output can be mechanically compared componentwise under FFP019 `CITC016 = EXACT_ZERO`.

## 3. Mandatory Core-B implementation blocker

The exact FFP013 Core-B implementation at the required starting HEAD is not executable at the frozen `R*` scale without a different implementation.

`data/ddm_build_copy/ffx002_r2_local_geometry.py` performs all of the following on the respondent grain:

1. `_distance_matrix` allocates a dense `n × n` Python list-of-lists and evaluates every respondent pair.
2. `_classical_mds` allocates dense `n × n` squared-distance and Gram matrices.
3. `_jacobi_eigh` copies the full Gram matrix and allocates a dense `n × n` identity/eigenvector matrix.
4. Each Jacobi rotation scans the complete upper triangle to find the next largest off-diagonal value.
5. `_build_component` then constructs another dense embedded-distance matrix and reruns `_classical_mds` for dimensionality-sensitivity variants.

For `n = 19,210`:

- `n² = 369,024,100` cells;
- unique respondent pairs = `184,502,445`;
- a single dense `float64` `n²` matrix has a packed lower bound of about `2.749 GiB`;
- five such packed matrices already imply about `13.747 GiB` before Python-object overhead;
- under the actual CPython list-plus-float representation, one fully populated matrix is approximately `10.999 GiB`, and five matrix-scale structures are approximately `54.995 GiB`, before the repeated eigensolver work and other outputs.

These memory figures are engineering arithmetic, **not** new empirical materiality thresholds.

More importantly, the deterministic Jacobi contract is computationally incompatible with this scale even apart from memory: each rotation searches `184,502,445` off-diagonal pairs, and the implementation permits a rotation count proportional to `100 × n²` before failure.

This is therefore typed as:

`BLOCKED__MANDATORY_CORE_B_IMPLEMENTATION_NOT_EXECUTABLE_AT_FROZEN_RSTAR_SCALE`

It is **not** a common-semantic-input failure, risk-set failure, PRA failure, ancestry failure, CITC failure, or empirical invalidity finding.

See:

`02_CORE_B_GENUINE_SCALE_BLOCKER.json`

## 4. Exact integrated-entrypoint disposition

The commanded full-scale entrypoint was **not launched into the known dense Core-B path** after the exact implementation-capacity gate above was established.

The FFP013 integrated stack invokes producers in order `A -> B -> C` and writes the integrated evidence surfaces only after all mandatory producers return. Launching the full `19,210`-respondent bundle would therefore enter a deterministic mandatory-arm implementation path that cannot lawfully produce the complete A/B/C result under the frozen code; forcing an OOM/nonconvergent resource burn would not create empirical evidence and would risk losing the already-established valid substrate evidence.

No claim is made that a genuine A, B, or C representation result was produced by FFP020. No synthetic result is relabeled as empirical.

## 5. Required result surfaces

### 5.1 `EXPERIMENT_VALIDITY`

`BLOCKED_BEFORE_COMPLETE_MULTIVIEW_EXECUTION__NO_COMMON_INPUT_INVALIDITY_ESTABLISHED`

The frozen empirical substrate, respondent identity, risk set, exact Q73A membership, FFP016 roles, and position/disposition ancestry remain valid evidence. Complete FFX002-R2 experiment validity cannot be certified because mandatory Core B cannot complete at the exact empirical scale under the frozen implementation.

### 5.2 `Q03_CLAIM_SUFFICIENCY_EVIDENCE`

`EXACT_REFERENCE_TARGET_AVAILABLE__PER_ARM_SUFFICIENCY_NOT_YET_ADJUDICABLE`

The exact 34-component realized-sample Q03 target is banked. No A/B/C arm output exists from this worker to compare against `CITC016 = EXACT_ZERO`; therefore no arm is labeled Q03-sufficient or Q03-insufficient here.

### 5.3 `REPRESENTATION_INFORMATION_AND_LOSS_VECTOR`

`NO_GENUINE_ARM_VECTOR_PRODUCED`

FFP009–FFP013 declared representation/loss contracts remain design/software evidence only. FFP020 does not misstate those preexisting contracts as genuine empirical loss measurements.

### 5.4 `SUPPLEMENTARY_UTILITY_AND_UNIQUE_CAPABILITY_EVIDENCE`

`VALID_SUBSTRATE_INFORMATION_RETAINED__REPRESENTATION_SPECIFIC_UTILITY_NOT_YET_EMPIRICALLY_ADJUDICABLE`

The exact J3 inventory, native-state variation, and frozen respondent facts survive and remain lawful inputs for later utility measurement. Their existence is not evidence that A or B empirically adds unique utility over C until the corresponding view actually executes.

### 5.5 `P0_P1_P2_P3_DOWNSTREAM_ABLATION`

`NOT_EXECUTED__MANDATORY_VIEW_OUTPUTS_UNAVAILABLE`

No synthetic or design-only package is substituted for genuine empirical P0/P1/P2/P3 evidence.

### 5.6 `HOSTILE_NULL_AND_REPLAY_RESULTS`

`FFP017_SUBSTRATE_REPLAY_EVIDENCE_RETAINED__NO_COMPLETE_FFP020_MULTIVIEW_HOSTILE_RUN`

The preexisting FFP017 deterministic replay and exposure/risk-set hostile evidence remains valid substrate evidence. FFP013 synthetic hostile tests remain software evidence. Neither is relabeled as a genuine FFP020 A/B/C hostile experiment.

### 5.7 `RAW_LEGACY_DESIGN_DIAGNOSTICS__NONAUTHORITATIVE`

`NOT_EMITTED_AS_EMPIRICAL_VIEW_DIAGNOSTICS__NO_GENUINE_ARM_OUTPUTS`

FFX002 historical thresholds remain nonauthoritative design capital. FFP020 mints no new utility threshold and does not apply legacy thresholds to nonexistent genuine arm outputs.

## 6. Q03 and supplementary interpretability after the blocker

Q03 target identity remains fully adjudicable at the frozen substrate grain. **Per-view Q03 sufficiency does not.** It requires genuine A/B/C output interfaces to exist.

Supplementary substrate information remains lawfully interpretable as exact empirical facts. **Representation-specific supplementary utility does not.** It requires an actually executed representation and lawful downstream comparison.

This distinction preserves the FFP020 anti-sterilization law without laundering unexecuted software into evidence.

## 7. Smallest blocker to completion

The single smallest blocker is:

`CORE_B_GENUINE_SCALE_EXECUTION_IMPLEMENTATION`

A subsequent bounded repair must provide a Core-B execution implementation that can operate on the exact `19,210`-member frozen respondent substrate while preserving the already-governed Core-B semantic/method contract, common-input identity, risk set, role identities, state universe, and representation-local ceiling. It must not solve scalability by changing the estimand, sampling away the frozen Q03 risk set, pooling states, changing roles, inventing semantic transforms, or weakening CITC.

Once that implementation exists, the exact FROZEN_EMPIRICAL_CANARY bundle can be executed and the full seven FFP020 empirical result surfaces can be generated.

## 8. Authority / mutation ceiling

FFP020 performed none of the following:

- CIM mutation;
- CITC mutation;
- comparison-identity mutation;
- new materiality tolerance or threshold;
- TTAR issuance;
- PRA re-role;
- Q84 harmonization;
- special-state pooling;
- preferred/master representation selection;
- class/field/capital/hegemony/homology/mechanism promotion;
- actor/V3 interpretation;
- final CVCR/COCR disposition.

## Terminal return

`PARTIAL__VALID_FROZEN_EMPIRICAL_EVIDENCE_PRESERVED__EXACT_Q03_REFERENCE_TARGET_BANKED__COMPLETE_A_B_C_AND_MAXIMAL_UTILITY_EXECUTION_BLOCKED_BY_CORE_B_GENUINE_SCALE_IMPLEMENTATION__READY_FOR_BOUNDED_CORE_B_EXECUTABILITY_REPAIR`
