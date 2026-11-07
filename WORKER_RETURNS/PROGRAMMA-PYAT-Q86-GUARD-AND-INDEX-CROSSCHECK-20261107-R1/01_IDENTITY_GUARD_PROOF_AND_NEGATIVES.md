# R8 IDENTITY GUARD PROOF AND NEGATIVES

## Repair
File: `rawlsing_next/field_forge_conditional_support.py`.

The producer now resolves the exact frozen source-native identities through the existing source owner `wave1_r5_q86_c11_projection.question_ref` and compares both caller-supplied refs before any relation profile is minted:

- expected conditioner: `question_ref("Q86B")` = `QUESTION_IMPLEMENTATION` `question_impl.phase0.2fb3a62609dad4c1306d` with hash `2fb3a62609dad4c1306d8cfa14f997eab4d6e65ada56083279386a202544a506`.
- expected target: `question_ref("Q86A")` = `QUESTION_IMPLEMENTATION` `question_impl.phase0.67f036c0efb7fb98ff4a` with hash `67f036c0efb7fb98ff4a93dc811bf59cfc095608eda374f6534b006a62241bd3`.

The check is exact-ref equality. It never parses an object_id substring, label, or caller-supplied `source_native_variable`. The frozen labels remain literal; relation family/version, permission ceilings, and bridge ABI are unchanged.

## Positive frozen path
Synthetic closure-B fixture and the real retained GT2 transport were both executed.

- Real retained frozen relation: `SUPPORTED`, 6 condition rows, conditioner Q86B, target Q86A, relation ref `urn:rawlsing:field-forge:conditional-support:sha256:1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`, count-profile hash `49bf14eb4a2b7fbf8e79ea4c72d10f4027819381564f582242ef6e24fc14fb59`.
- The same real retained relation hash was computed on the untouched R7 base and after this guard: byte/semantic identity preserved.
- C to D admission: `ADMITTED`, `STRUCTURAL_MEDIATION_INPUT`; participant labels Q86B/Q86A; no actor or REVIEW promotion.

## Required negatives
Proof runner: `06_R8_PROOF_RUNNER.py`, exit `0`, trace `R8_PROOF_TRACE.json`.

| Negative | Result |
|---|---|
| unlike Q99B to Q99A pair | refused with `FieldForgeConditionalSupportError` before profile minting |
| forged object_id with Q86 text but wrong exact kind | refused with `FieldForgeConditionalSupportError` |
| wrong Q86A identity hash | refused with `FieldForgeConditionalSupportError` |
| swapped Q86 roles | refused with `FieldForgeConditionalSupportError` role/order |
| wrong risk set | relation can be built only after exact Q86 refs; C to D bridge refuses `frozen risk-set exact identity mismatch` |
| wrong relation permission | C to D admission `DENIED`, no target-use permission |
| wrong source family/wave | admission `OUT_OF_SCOPE`, `SOURCE_FAMILY_OR_WAVE_MISMATCH`, no target-use permission |
| wrong source artifact | admission `INTEGRITY_FAILURE`, `SOURCE_ARTIFACT_IDENTITY_MISMATCH`, no target-use permission |
| nonpositive upstream `OBSERVED_ZERO` | relation remains `OBSERVED_ZERO`; admission `UNRESOLVED`; no positive relation or target-use permission |
| cold restore | rebuilt frozen relation ref matches baseline exactly; admission `ADMITTED` |

The wrong-risk result is deliberately an admission-level refusal: exact Q86 identity is established first, and the later frozen bridge remains the owner for risk/source/permission closure. The guard does not widen or duplicate that authority.

## Tests
- `140 passed in 117.78s`, exit `0`: FF producer, closure-B bridge, E2B harness, D to M4 bridge, retained structural court, and GT12 I03 positive facts.
- `58 passed in 2.25s`, exit `0`: C11 ingest, source-backed facade, and empirical query.
- Inherited failures: one failure and three errors in the GT34/A2 group are identical on the untouched R7 base and are recorded in `07_R7_GATE_AND_INHERITED_FAILURES.md`; they are not attributed to this guard.

## Residual boundary
The C to D bridge remains a frozen, narrow adapter and was not widened. A directly forged `ExactConditionalSupportProfile` object with recomputed hash is an out-of-contract object, not a permitted producer output; no normal producer can mint it after this guard. The only production source of the relation is the guarded producer.
