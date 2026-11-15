# Court 12 — Remaining Gate Classification

## Result

One new independent source-free blocker remains.

## NEW_PREORACLE_SOURCE_FREE_BLOCKER

### Name

`CROSS_SCHEMA_LOGICAL_CANDIDATE_IDENTITY_NORMALIZATION_MISSING`

### Exact defect

The current parity law uses direct candidate-hash equality where:

- historical identity = G02 `execution_candidate_hash`;
- current identity = PRE553 I05 `candidate_hash`;
- canonical hash constructions are different.

The same normalizer also drops the semantic material needed to replace that illegal equality with a lawful logical mapping:

- historical P2 parameter triple;
- current CONDITION predicate/query identity;
- current BASELINE predicate/query identity.

### Consequence

The source-free pre-oracle closure cannot be adopted.

The comparator has not established that the empirical witness on each side belongs to the same logical candidate.

### Minimum repair grain

Source-free only.

No source read or candidate execution is required to repair this law.

Required work:

1. define a deterministic cross-schema logical candidate key from immutable workload semantics;
2. derive expected keys from ASTRA/G02 immutable material;
3. derive observed keys from current compiled PRE553 candidate semantics;
4. for P2 bind exact parameter triple and CONDITION/BASELINE semantics;
5. compare empirical truth under that common logical key;
6. prohibit direct G02-hash↔PRE553-hash equality;
7. add hostile tests where witness/terminal/final envelope remain unchanged but:
   - parameter tuple changes;
   - CONDITION identity changes;
   - BASELINE identity changes;
   - historical/current native hash strings differ as expected;
8. rerun focused and broad source-free qualification.

## LOCAL_SOURCE_BACKED_EVIDENCE_REQUIRED

After the above source-free blocker is repaired and requalified, the next empirical gate remains the planned fresh local LiTS source-backed pass.

This audit does not perform it.

## PROMOTION_TRANSITION_WORK_ONLY

After a source-free repaired head is independently accepted, explicit adoption/transition to the governed execution line is still required by project governance before the local pre-candidate source pass.

This audit leaves the governed P2X branch frozen.

## POST_PREFLIGHT_WORK_ONLY

Candidate A/B/C execution, measured P2X and later promotion/candidate courts remain downstream.

They are not blockers to source-free pre-oracle law itself and were not run here.

## No additional speculative blocker

Beyond the logical candidate identity defect above, this audit found no second independent source-free pre-oracle blocker in:

- I03 jurisdiction;
- immutable ASTRA provenance;
- current full-fact retention;
- F02 selector substrate;
- freeze ordering;
- WVS7 successor conservation;
- packaging pins;
- qualification immutability;
- CI evidence.
