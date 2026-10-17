# GF1G Phase A — INDEPENDENT FREEZE (before any GF1E inspection)

**Status:** FROZEN AND PUSHED BEFORE GF1E CODE OR COMPUTED OUTPUTS WERE READ.
**Author:** fresh independent reviewer session, not GF1E author, not the GF1F prior reviewer, not HQ.

## Independence attestation

- This is a new, separate model session (fresh DeepSeek V4.1 Flash instance in the DSH harness).
- I have not read the GF1E author's conversation, the GF1F observed results/verdict, or any
  same-session history from those workers.
- I read only: the GF1G commission, governing Pyat 00D and Sorok 00C, the pre-GF1E R17 commission
  and precommitted contract, the R23 GF1C recovered consumer contract, the unchanged original 44
  specification, and the pre-GF1E generic producer owner at `9f4a23cef`.
- I verified the GF1E consumer blob identity (`git blob 75670c69…`, SHA-256 `06dd484b…`) without
  reading its content, then froze and pushed this oracle before Phase B.

## What was independently derived

1. A reference consumer `phase_a/reference_consumer/gf1_pair_support_consumer.py` written only from
   the frozen contract, not from GF1E code.
2. Genuine 2x2 native relations from the real pre-GF1E chain (74 blobs reattested):
   baseline `(00,01,10,11)=(1,0,0,1)`, intervention `R2_Y0→1` `(0,1,0,1)` in the B-slot orientation
   and `(0,0,1,1)` in the PAIR orientation, intervention `R1_Y1→0` `(1,0,1,0)` / `(1,1,0,0)`,
   and the distinct BOUNDED_DISCOVERY relations.
3. Reverse `X|Y` vs `Y|X` under its own `REVERSE_GRANTED` operation: roles swapped, different
   relation object identity, same counts; forward native order `FORWARD_NATIVE_ORDER`.
4. Four separation classes with an explicit, frozen definition:
   `EXACT_PAIR_SEPARATION`, `NO_PAIR_SEPARATION`, `UNDETERMINED_NO_ELIGIBLE_RISK`,
   `UNDETERMINED_ZERO_SUPPORT_RISK`.
5. Positive / zero / missing / suppressed risk:
   positive denominators and point-mass exact separation; zero eligible denominator;
   observed zero in supported risk set vs `ZERO_SUPPORT`; typed `MISSING_TARGET_STATE`,
   `UNRESOLVED_TARGET_STATE`, `NONRESPONSE` must HOLD.
6. Counts and denominators: per-condition denominator = sum of target counts; total joint support;
   eligible joint risk; excluded-ineligible count.
7. Nontrivial distributions: `(2,1,1,2)` → NO; `(2,0,0,2)` → EXACT; collapsed identical point
   mass → NO.
8. Exact relation identity hashes for every genuine/reverse/synthetic relation, and reference-relative
   consumer `result_hash` values with determinism and semantic-sensitivity checks.
9. An internally inconsistent but fully rehashed `condition_denominator_support` vs
   `sum(target_counts)` relation: typed rejection before any class is computed.
10. A support count exceeding eligible risk: typed rejection.
11. A fully rehashed, internally consistent relation with forged provenance/authority references:
    structurally indistinguishable; the consumer must retain `TEST_ONLY`/no-real-source privilege and
    must not claim issuer authentication. The relation schema has no external signature field.

## Reference evidence (pre-GF1E court, 9f4a23cef + reference consumer only)

| suite | result |
|---|---|
| unchanged original 44 (`test_gf1_generic_pair.py`) | 44 passed |
| GF1G precommitted independent suite (26) | 26 passed |

Logs/JUnit: `logs/`, `junit/`.

## Normative scope of `01_FROZEN_ORACLE.json`

- Relation identity hashes: **normative**. GF1E must reproduce the producer's `content_hash` /
  `object_id` bit-for-bit for the same inputs.
- Separation classes, counts, denominators, zero semantics, role identity: **normative**.
- Consumer `result_hash`: **reference-relative**. The frozen contract does not fix a
  cross-implementation canonical result payload; GF1E must be deterministic, self-consistent and
  semantically sensitive, but equality to the GF1G reference hash is not required.

## Prohibition observed

No GF1E implementation source, no GF1E executed evidence, and no GF1F expected results were read
before this freeze was committed and pushed.
