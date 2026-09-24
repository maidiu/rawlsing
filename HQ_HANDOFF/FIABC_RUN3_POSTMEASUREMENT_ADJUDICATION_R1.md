# FIABC RUN3 — POST-MEASUREMENT HQ ADJUDICATION — R1

Status: `RUN3_VOID_FOR_P2_COMPARATIVE_SELECTION__REPAIR_AND_FRESH_RERUN_REQUIRED`

Measured execution head:

`bc832181b4284ac110d2be44fc83504e04de081e`

## Adopted forensic returns

### LiTS/A

Worker branch:
`agent/rabochii-fiabc-run3-litsa-r5-provenance-forensics-r1`

Worker head:
`18def02a4eac771eeaf1e2680d79955e30f64faa`

Terminal:
`RUN3_LITSA_VOID_AS_CANDIDATE_EVIDENCE__COURT_PROVENANCE_GLUE_DEFECT_PROVED`

Holding:
The measured backend constructed Candidate A's R5 `source_artifact_ref` with the wrong `kind` and without the governed `object_id`. The frozen A owner correctly failed closed. This is not an architectural failure of persistent R5.

Required repair surface:
`rawlsing_next/ee_p2x_darwin_stage_backend.py::_r5_release_identity`
and the matching canonical-root assertion.

The canonical source ref is already governed by the projection:
- kind: `SOURCE_ARTIFACT`
- object_id: `projection.source_artifact_id`
- content_hash: `projection.expected_source_sha256`

Candidate A owner bytes remain frozen.

### LiTS/B

Worker branch:
`agent/rabochii-fiabc-run3-litsb-frozen-owner-type-universe-forensics-r1`

Worker head:
`e92ce1dc4e0bb1c86d8f8da47e54e6c841061134`

Terminal:
`RUN3_LITSB_VOID_AS_CANDIDATE_EVIDENCE__FROZEN_OWNER_TYPE_UNIVERSE_DEFECT_PROVED`

Holding:
The exact frozen B owner was loaded under a synthetic module identity. That frozen file defines its own `GovernedC11Projection` class. The common P2R1 binder constructed the supplied projection from the canonical current class. Python therefore deterministically rejected the current projection at frozen B's nominal `isinstance` boundary before Candidate B's architecture was lawfully exercised.

Required repair:
a semantically transparent isolated exact-owner B execution universe in which frozen B's exact bytes occupy a coherent canonical facade/type universe before projection construction and repository execution.

Forbidden:
weakening `isinstance`, monkeypatching, duck typing without authority, field dropping, or globally replacing the parent's canonical facade.

### LiTS/C and common LiTS representation seam

Worker branch:
`agent/rabochii-fiabc-run3-litsc-projection-coverage-forensics-r1`

Worker head:
`fc2fd29a192e6f58c827ab1f527550af3c549fee`

Terminal:
`RUN3_LITSC_VOID_AS_CANDIDATE_EVIDENCE__COMMON_PROJECTION_OR_REPRESENTATION_DEFECT_PROVED`

Holding:
RUN3's measured backend bypassed the already-qualified LiTS representation-authority / projection-owner adaptation required to reconcile decoder-native float64 physical response cells with the governed response-rule key domain.

Accepted representation authority:
`9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d`

Accepted representation source-free qualification head:
`d1833f9ebe363258575c6bd95737eb8f1b0f4154`

Accepted legacy projection-owner rebind head:
`ea0baa4d87244a548ba9a6a46a883d307c65e3e4`

Accepted legacy projection-owner qualification:
`4c1641d1f1ec51a4116d0664dbf149e915465bdb`

The candidate-neutral oracle path already consumes this bounded authority. The measured A/B/C path did not.

This is common court/source-projection integration law, not Candidate C semantics.

## Cross-lane synthesis

The three defects are ordered, not independent candidate verdicts.

1. LiTS/A encounters malformed R5 provenance before it can reach the common C11 representation seam.
2. LiTS/B encounters split Python class identity before it can reach the common C11 representation seam.
3. LiTS/C reaches the common physical->C11 seam directly and exposes the already-known decoder-native float64 versus governed response-key domain mismatch.
4. Therefore fixing only A provenance or only B class identity would merely expose the same downstream common representation defect.

RUN3's generic `CANDIDATE_LOCAL_FAILURE` labels are overbroad for all three LiTS events and are not admissible for P2 architecture comparison.

## WVS7/A

WVS7/A entered measured S01 but no terminal receipt was written. Local OS forensics supplied by the operator strongly attributes the interruption to macOS automatic logout at the configured 3600-second idle threshold, with launcher exit 137 occurring during the logout sequence.

Classification:
`INFRASTRUCTURE_INTERRUPTION__MACOS_AUTO_LOGOUT__HIGH_CONFIDENCE`

Limitation:
the exact worker-PID signal path was not directly observed.

WVS7/A is not candidate-failure evidence. WVS7/B and WVS7/C were not reached.

## RUN3 admissibility

RUN3 remains immutable historical measured evidence.

It is useful for:
- forensic failure diagnosis;
- failed-run physical telemetry explicitly marked non-comparative;
- proof that the current court integration was not yet fit for dispositive A/B/C comparison.

It is not admissible for:
- P2 architecture comparison;
- candidate ranking;
- architecture selection;
- carrying forward terminal candidate correctness judgments.

No RUN3 work root may be repaired, resumed, rewritten, or converted into a successful run.

## Required repair order

### R1 — Candidate A provenance glue

Repair the current measured backend so all R5 release source references use the already-governed full canonical `SOURCE_ARTIFACT` ExactRef.

Align the backend canonical-root check to the same law.

Do not modify Candidate A owner bytes or semantics.

### R2 — Candidate B frozen-owner execution universe

Create a source-free qualified isolated execution/import boundary for exact frozen B bytes such that:
- B's builder;
- B's `GovernedC11Projection`;
- B's nested physical rule classes;
- B's `physical_value_binding_key`

inhabit one coherent frozen-owner facade universe.

The parent A/C runtime universe must remain unchanged.

### R3 — Common LiTS representation bridge

Integrate the already-accepted bounded LiTS representation authority and projection-owner adaptation into the measured common LiTS physical->C11 path.

All A/B/C routes must reach one common governed semantic C11 truth surface.

No generic int/float/Decimal coercion is permitted.

No label/frequency/missingness inference is permitted.

No Candidate-C-only semantic patch is permitted.

### R4 — Cross-candidate source-free qualification

Before any fresh measured run, prove source-free that:

- A's lawful R5 provenance is accepted by frozen A;
- A reaches the authorized common LiTS representation seam;
- B's frozen owner receives a projection from the same exact class/key universe it uses;
- B consumes the authorized bounded representation adaptation;
- C consumes the same common representation authority;
- all three reproduce the required governed C11/oracle truth surface;
- hostile neighboring type/token/state/declaration cases fail closed;
- frozen candidate definitions, T2, T3, T5, source hashes, oracle identities, metric definitions, and cell order remain unchanged.

No real-source candidate execution is permitted during repair qualification.

## Fresh-run law

Only after R1-R4 are source-free qualified and canonically adopted may a successor protected execution head be advanced.

The next measured court must start:
- from a fresh checkout;
- from a fresh work root;
- from zero candidate state;
- with macOS automatic logout disabled for the duration of the run;
- without reusing RUN3 candidate artifacts or numeric results.

RUN3 may never be resumed.

## P2 status

`BLOCKED_PENDING_REPAIR_AND_FRESH_SIX_CELL_MEASURED_COURT`

No architecture ranking or selection is authorized.
