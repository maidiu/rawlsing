# PYAT C1-01 — R7 CLOSED-WITNESS OWNER + PACKET + HOSTILE COURT CLOSURE — R1

Disposition: `PATCH_READY__REVIEW_AND_EXECUTION_REQUIRED`

Commission tip: `7ea809f3b4433d24c027eb0ad3e98b0a6d3fb607`  
Exact base: `458f839845fc149874e5a64af5eda41bbd52c4e1`  
Implementation tip before this return: `f7d72915fe6ac6b7dc2dc583fff462f748c3556d`

## Returned closure

The three R6 review defects were repaired within the exact commission boundary.

1. **CLOSED 16-key owner law**
   - `rawlsing_next/pre553_analytical_composition.py`
   - before blob: `5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`
   - after blob: `26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`
   - `required.issubset(identity)` was removed.
   - `_verify_witness(...)` now fails closed unless `set(identity) == required`, with typed `ConditionValueRelationMismatch` detail for both missing and extra keys.
   - No other production-owner semantic law was changed.

2. **Literal witness preimage + dependency freeze**
   - `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R6/02_NORMATIVE_WITNESS_MATERIALS.json`
   - before blob: `52ec60046787269691b31bbd1be875052de5d733`
   - after blob: `57f4caf5a5c148d60fcfe8322ff2016de5b4f4a1`
   - the existing packet schema tag remains `PYAT_C1_00_R6_NORMATIVE_WITNESS_MATERIALS@1`.
   - both directions now literally serialize the complete CLOSED 16-key `identity_material` and all commissioned audit fields.
   - immutable path+blob selectors are frozen for the accepted R2 relation oracle, R2 synthetic authority freeze, R3 evidence identity preimage, R6 query materials, and R6 evidence recomputation.
   - the accepted query, witness, and evidence hashes remain unchanged.

3. **Hostile / reidentification court restoration**
   - `rawlsing_next/tests/test_pre553_analytical_composition.py`
   - before blob: `aaeab2c8841c1a160346b78140c0bb2a001db0c8`
   - after blob: `db6b876f15d145cfc48cc6d944e48da4460842d3`
   - H1 matching-hash 17th-field rejection restored.
   - H2 valid AT19 determinant reidentification restored.
   - H3 exact denominator-member identity hostile restored while visible 54/60 is held fixed.
   - H4 geometry-cell identity hostile restored.
   - H5 fixture-only pairing/comparability-authority reidentification restored.
   - existing R6 positive and fail-closed courts remain present.

## Identity preservation

The governing packet still freezes:

- forward query: `8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`
- reverse query: `2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`
- forward witness: `f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`
- reverse witness: `a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`
- forward evidence: `c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`
- reverse evidence: `0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

Static post-write audit confirms each literal direction contains exactly the frozen 16 key names, `effective_time_or_interval = null`, and `binding_mode = EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE`.

## Execution status

The exact commissioned pytest command was **not executed**. This worker's isolated shell/container surface failed before any command could start, and GitHub reports no workflow run or commit status for the implementation tip. No execution PASS is claimed.

Required execution remains:

`python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

## Boundary receipt

Raw survey files accessed/materialized: **0**.  
Candidate A/B/C: **not run**.  
Measured P2X: **not run**.  
Real-source C11: **not run**.  
C1-02: **not begun**.  
New real-source semantic/comparability/model/actor authority: **none**.

`C1_01_R7_OWNER_CLOSURE_RETURNED__HQ_ADJUDICATION_REQUIRED`
