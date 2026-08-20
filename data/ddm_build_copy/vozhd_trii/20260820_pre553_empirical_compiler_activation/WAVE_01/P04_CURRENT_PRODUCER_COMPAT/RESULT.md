# PRE553 P04 — Current Producer Compatibility Return

## Result

`PRE553_P04_CURRENT_PRODUCER_COMPAT_CLOSED`

Task: `PRE553-W01-P04-R1-002`  
Agent: `PRE553_P04_CURRENT_PRODUCER_COMPAT_R1`  
Branch: `agent/vozhd-trii-pre553-w04-current-producer-compat`  
Exact accepted downstream base: `e51730e461a15b0ad20f02f2efb4bccd751c2c81`

The bounded P04 normalization return is closed as a governance/spec/evidence result. It does **not** authorize a producer adapter implementation and it does **not** restore any retired runtime carrier.

## Holding

Current V550–V552/R1 material is compatible with PRE553 only through an explicit admission rule that proves semantic parity for the concrete producer object under consideration. Artifact-family resemblance, historical naming, path availability, repository presence, or a successful parse is never sufficient.

The controlling migration law is:

1. preserve exact producer/source identity and provenance when those properties are semantic;
2. preserve query scope, partition/universe, variable/measure and observation semantics;
3. preserve negative semantics as states, never as numeric or Boolean defaults;
4. preserve valid generated `0` and `false` as values distinct from unknown, missing, invalid, unauthorized or not-observed states;
5. admit artifact-family differences only when they are demonstrated to be nonsemantic;
6. reject ambiguous J/non-J, V55x/R1 or other carrier substitutions unless an exact parity proof resolves the distinction;
7. never invoke V550/V551/V552/V558 or other retired carriers as hidden current-runtime fallback;
8. never treat active V558 metadata or repository context as current empirical runtime truth;
9. fail closed whenever parity, source authority or state preservation cannot be proved.

## Exact evidence bound by this return

### V550/V551 response-semantics seam

Authority: `data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.manifest.json`

- contract: `V550_V551_RESPONSE_SEMANTICS_INFRASTRUCTURE_SEAM_R1`
- version: `v1`
- contract SHA-256: `3a04a9e689b5d027e501a1cc165093773407338313feb25e86c2356ea752b704`
- retrieval scope is semantically gated as `all` or `filtered`;
- generated empirical meaning requires producer generation success (`searches2_n >= 1`);
- the metric-source seam preserves the state distinctions `ok`, `query_failed`, `missing`, `variable_present`, `not_observed`;
- failure states must never be downgraded to value `0`.

### R1 finite-universe authority

Authority root: `data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/00_README_FIRST.md`

- exact released study: `ATP W135`
- `study_key=ATP_W135`
- DOI: `10.17605/OSF.IO/R6QPS`
- source file: `ATP W135.sav`
- source file SHA-256: `6cec90ec72df360341236f7634d5d76c9a0604168d4174a03e8b8efd388bbbae`
- authoritative manifest: `22_shared_respondent_relation_manifest.R1.json`
- manifest SHA-256: `84009652424d200ced06933173eb8b2f8fb89d51f7909d3da40f6f59ad5da9d9`
- exact study universe, respondent-key set, authority tuple and source-manifest identity must survive before derived predicates are admitted;
- source-level exclusions remain fail-closed and respondent linkage is source-backed rather than inferred from row order.

## Deliverables

- `CURRENT_PRODUCER_COMPATIBILITY_MATRIX.json` — normative producer-family admission matrix.
- `MIGRATION_RULES.md` — migration/admission decision procedure for I04.
- `HOSTILE_COMPATIBILITY_ORACLE.md` — negative tests that prevent silent retired-carrier reentry or semantic collapse.
- `RESULT.json` — machine-readable closure record.

## No-drift declaration

This return was prepared only against exact accepted downstream base `e51730e461a15b0ad20f02f2efb4bccd751c2c81`. It changes governance/spec/evidence files only beneath the assigned P04 return directory. It changes no production code, launcher, IO policy, runtime path, producer implementation, V553 implementation, V558 implementation or POST553 interface.

## Gate effect

P04 now supplies the compatibility-matrix prerequisite for I04 migration review. I04 remains responsible for any authorized current-producer adapter implementation and must consume this matrix fail-closed; P04 itself grants no runtime fallback authority.
