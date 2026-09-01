# FFP011 — CORE-B LOCAL GEOMETRY PRODUCER R1 — WORKER RETURN

Status: `PASS__EXE003_CLOSED__CORE_B_LOCAL_GEOMETRY_PRODUCER_IMPLEMENTED`

Repository: `maidiu/rawlsing`  
Worker branch: `agent/rabochii-field-forge-r2-ffp011-core-b-local-geometry-r1`  
Exact starting HEAD: `9611a9067ab28e17eb45b565398c7e604a24e77b`  
Consumed FFX002-R2 design authority by exact ref only: `5343862783959a1455735c0a5eb7b330c76f42d5`

No production data was used. Synthetic tests only.

## 1. EXE003 closure

FFP006 identified:

`EXE003__CORE_B_LOCAL_GEOMETRY_PRODUCER_ABSENT`

This worker closes that implementation-existence blocker with:

- `data/ddm_build_copy/ffx002_r2_local_geometry.py`
- `data/ddm_build_copy/compile_ffx002_r2_local_geometry.py`
- `data/ddm_build_copy/test_ffx002_r2_local_geometry.py`

Executable entrypoint:

```bash
python data/ddm_build_copy/compile_ffx002_r2_local_geometry.py \\
  --input-json <frozen-core-b-input.json> \\
  --output-json <local-geometric-output.json>
```

The producer does not claim that FFX002-R2 as a whole is executable. EXE001/EXE002/EXE004/EXE005 remain outside this worker.

## 2. Contract implemented

The producer is bounded to `arm_id=B`, `view_family=LOCAL_GEOMETRIC`.

It implements:

1. **separate position/disposition geometries**
   - `ACTIVE_POSITION` and `ACTIVE_DISPOSITION` are validated independently;
   - position and disposition active ancestry must be disjoint;
   - respondent sets must be identical;
   - no cross-space re-optimization or homology-like objective is implemented.

2. **frozen common-manifest attestation**
   - all FFX002-R2 required common-manifest fields are required;
   - SHA-256 is independently recomputed from canonical UTF-8 sorted-key JSON;
   - optional declared set-array paths are canonicalized as sets;
   - hash mismatch fails closed as `COMMON_INPUT_ARM_HASH_DIVERGENCE`.

3. **explicit method manifest**
   - schema: `FFX002_R2_LOCAL_GEOMETRIC_METHOD_R1`;
   - metric: exact frozen-state Hamming or explicitly weighted Hamming;
   - decomposition: deterministic classical MDS using bounded Jacobi eigendecomposition;
   - dimensionality: preregistered fixed `d` or full positive rank, bounded to 10;
   - numeric axes are `D1..Dn` only.

4. **local outputs**
   - component-local distance matrix;
   - k-neighborhoods;
   - complete metric distance order;
   - farthest/opposition peers typed as metric opposition only;
   - low-dimensional coordinates and normalized stress;
   - explicit `DOES_NOT_REPRESENT` for cross-component metric when components are disconnected.

5. **stability diagnostics**
   - deterministic leave-one-respondent-out neighborhood Jaccard diagnostics;
   - dimension `d-1/d/d+1` compression sensitivity;
   - metric-to-embedding Spearman and normalized stress;
   - no universal sociological stability constants are minted.

6. **invariant/loss receipt**
   - exact semantic mutation count = 0;
   - state-universe, role, respondent-set, and ancestry-disjointness attestations;
   - FFX002-R2 invariant dispositions I01-I18 where applicable;
   - known geometric loss is explicit rather than silently repaired.

7. **deterministic/versioned numeric replay**
   - replay schema: `FFX002_R2_LOCAL_GEOMETRIC_NUMERIC_REPLAY_R1`;
   - canonical eigenvector sign;
   - respondent-ID tie breaking;
   - fixed serialized float precision from the method manifest;
   - explicit absolute/relative numeric tolerances;
   - degenerate eigenspaces are compared by distance/Gram invariants rather than narrative axis identity.

## 3. Semantic firewall

Post-fork geometry may not:

- merge or collapse states;
- rebin/recode/reorder categories;
- pool special states;
- change eligibility or risk set;
- change estimand;
- re-role active/supplementary/conditioning/excluded semantics.

The producer rejects forbidden semantic-transform keys recursively in the method manifest, rejects state IDs outside each frozen measurement state set, requires exact row measurement coverage, and requires exact frozen analytic roles.

Human-readable measurement labels are ignored by computation. The synthetic label-scramble test proves that replacing labels with `CLASS`, `RELIGIOSITY`, or `CAPITAL` leaves the complete output byte-equivalent at canonical JSON level.

## 4. Geometry is a view

The output hard-codes the claim ceiling:

`LOCAL_GEOMETRIC_RELATIONS_ONLY__NO_EMPIRICAL_WORLD_OR_SOCIAL_ONTOLOGY`

Forbidden claims include:

- `GLOBAL_WORLD_SPACE`
- `SOCIAL_ONTOLOGY`
- `CLASS_FIELD_CAPITAL_HEGEMONY`
- `HOMOLOGY`
- `CAUSAL_MECHANISM`
- `ACTOR_PSYCHOLOGY`
- `REALIZED_V3_PERSONALITY`
- `CROSS_CONTEXT_RECURRENCE`

No semantic label is used to derive metric, coordinates, neighborhoods, order, opposition, dimensionality, or compression.

## 5. Synthetic validation

The branch's executable code, normalized only by removing comments/blank lines, was checksum-matched to the isolated test copy and exercised in Python.

Result:

`17 passed`

Covered hostile cases include:

- frozen common-manifest tamper;
- post-fork rare-state merge request;
- ordinal rebin request;
- category reorder request;
- analytic-role override;
- risk-set filter request;
- special-state pooling request;
- unknown/merged state injection;
- active-position re-role;
- cross-side ancestry contamination;
- respondent risk-set divergence;
- semantic-label scramble;
- disconnected component no-bridge rule;
- deterministic replay;
- weighted metric as explicit method sensitivity while frozen semantic hashes remain identical.

## 6. Non-claims

This worker does not:

- mint PRA, TTAR, respondent, exposure, estimand, or source authority;
- infer exposure from missingness;
- acquire or use production data;
- create a latent ontology;
- create a distance-based semantic equivalence;
- merge/rebin/re-role frozen semantic states;
- interpret numeric axes socially;
- implement Core A or Core C;
- run the full FFX002-R2 comparison.

Terminal return:

`EXE003_CLOSED__BOUNDED_LOCAL_GEOMETRIC_PRODUCER_AND_SYNTHETIC_HOSTILE_TESTS_PRESENT`
