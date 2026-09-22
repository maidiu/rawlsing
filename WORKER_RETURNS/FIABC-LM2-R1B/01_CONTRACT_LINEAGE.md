# FIABC-LM2-R1B — Contract Lineage

## 1. Preflight before the authority-kind ontology

### 2026-08-20 07:10:37Z — C11 logical carrier preflight

Commit:

`1d7852b4edf0b97894e442aea1031cbfc5f3a248`

Title:

`PRE553 P10 complete C11 source contract preflight`

The preflight separated raw/native material from optional canonical material in the logical carrier:

- `QuestionVariableBinding.canonical_question_ref_or_typed_absence`;
- `RespondentEvent.canonical_value_or_typed_absence`;
- `RespondentEvent.value_transform_authority_ref_or_typed_absence`.

It required immutable authority closure and refused inferred semantic promotion, but it did not yet name the later authority-kind taxonomy.

This establishes that canonical material was optional from the carrier's conceptual birth.

## 2. Authority ontology splits source semantics from mapping

### 2026-08-20 09:41:36Z — I01 authority runtime

Commit:

`2faacc3f084cf65e61843f1692b947177a617013`

Title:

`Implement PRE553 immutable empirical authority validation`

Initial `AUTHORITY_KINDS` contains both:

`SOURCE_SEMANTICS_TOPOLOGY`

and:

`NATIVE_CANONICAL_MAPPING_HARMONIZATION`.

The original operation ceilings are already distinct:

### SOURCE_SEMANTICS_TOPOLOGY

- `INTERPRET_SOURCE_SEMANTICS`
- `INTERPRET_RESPONSE_TOPOLOGY`
- `INTERPRET_SPECIAL_STATES`

### NATIVE_CANONICAL_MAPPING_HARMONIZATION

- `MAP_NATIVE_CANONICAL_IDENTIFIER`
- `MAP_NATIVE_CANONICAL_VALUE`

Therefore the two authority kinds are siblings in the original ontology. One did not evolve out of the other.

Later cleanup at commit:

`b949280901b48f2ac6d4c711cd31f39b54889767`

removed invented relation-operation vocabulary but preserved this source-semantics versus native/canonical mapping distinction.

## 3. C11 binds canonical material to mapping authority

### 2026-08-20 11:14:04Z — I02 carrier integrity

Commit:

`e6cb975e1b2e401279c5580955464f6976929804`

Title:

`PRE553 I02 add C11 carrier integrity records`

Historical C11 file blob:

`bda39b1ccd22f27ae24476207a7f3f3e9025b698`.

Current LM2-base accepted C11 file blob:

`7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd`.

The `RespondentEvent` validator computes:

`has_canonical = canonical_question != None OR canonical_response != None`.

If true, it requires an exact transform authority and then exact-positive:

`authority_kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION"`.

That behavior is not a post-R6S patch. It precedes R6S.

I02 hostile tests also reject canonical material when exact mapping authority is absent.

## 4. Source-backed facade retains the distinction

### 2026-08-23 07:23:24Z — C05-R2A facade

Commit:

`91315bd3df9bd7f5e710d9791cc8be0bb96173fb`

Title:

`C05R2A: add explicit source-backed C11 facade`.

Facade contract:

`PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`.

The response rule has separate fields:

`canonical_value`

and:

`transform_authority_ref`.

The facade emits them directly as:

`canonical_response_value_if_authorized`

and:

`value_transform_authority_ref`.

It therefore delegates canonical authority validation to C11 rather than granting it.

### 2026-08-23 07:28:55Z — facade hostile/parity tests

Commit:

`018960039aa8cad19576e915e0358b5c05461ff7`.

The accepted source-backed fixture uses `SOURCE_SEMANTICS_TOPOLOGY` for source semantics while leaving `ResponseValueRule.canonical_value` and `transform_authority_ref` at their default absent values.

Thus the accepted generic bridge never demonstrated:

`SOURCE_SEMANTICS_TOPOLOGY -> populated canonical response value`.

## 5. WVS7 ownership bridge is source-local

### 2026-08-23 19:32:19Z — G-SR07-R2A

Commit:

`a06f2bced8677453cf77fec5e622cb334a9810a5`.

Key artifact:

`WVS7_C11_OWNERSHIP_BRIDGE.json`

blob:

`7213e0f7aa430b6faee609cdb26751101e15330f`.

The bridge closes C11 **ownership**, not canonical harmonization.

For questionnaire response slots it grants `RespondentEvent@1.0.0` source-semantic ownership while explicitly refusing unrelated downstream structural or identity authority.

Its respondent identity exceptions likewise refuse canonical respondent-key selection.

This is the first WVS7-specific historical bridge relevant here: it is intentionally native/source-local.

## 6. Accepted HB01 proves native-only WVS7 C11 is lawful

### 2026-09-11 21:00:15Z — Full GSR07 R2

Commit:

`a07e2a9a9c5299b80296aed323b7912192b31ddd`.

Return blob:

`172ff4bee2f66ee8ea8b086d7d226f778116bf64`.

Real-source certification passed and created a deterministic sealed WVS7 C11 release.

In its accepted test/construction surface, each WVS7 questionnaire binding uses:

`canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED")`.

Its response rules populate source response state/topology while leaving canonical response values absent.

No `NATIVE_CANONICAL_MAPPING_HARMONIZATION` authority is used to force source codes into canonical fields.

HQ accepted HB01 closure at:

`3468673673db2f3de804d6e825585f86ff98e870`.

This is the strongest historical precedent because it is WVS7-specific, real-source-backed, accepted, and C11/I03-qualified.

## 7. R6A closes source-native response semantics

### 2026-09-16 21:46:08Z — EE-R6A

Commit:

`4b141b8b5748175e34c9286eba36f53d8df1e9d5`.

R6A explicitly calls its object:

`SOURCE-NATIVE RESPONSE-SEMANTIC COURT`.

For Q291G5/Q291P5 it closes:

- exact current source qid binding;
- native raw response states;
- exact source-native response labels/special states;
- same-respondent matrix topology.

It explicitly states that source-native distinctions are preserved rather than harmonized away.

Nothing in the inspected R6A return grants Rawlsing canonical-value transformation authority.

## 8. P2F2 packages R6A as SOURCE_SEMANTICS_TOPOLOGY

### 2026-09-17 23:36:29Z — EE-P2F2

Tip:

`22667bd395e7293f99b285daddad36fe3a4377ef`.

Authority bundle blob:

`7147e76a1dfc62a4f8eb60df458baa9e41670f7a`.

Exact source authority:

- id: `EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY`;
- hash: `c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f`;
- kind: `SOURCE_SEMANTICS_TOPOLOGY`.

The WVS7 response-semantic object is hash:

`8aaa37c601f0dac74870c585567403520ce77287feae525832c59841dac1b710`.

No inspected P2F2 authority snapshot has kind:

`NATIVE_CANONICAL_MAPPING_HARMONIZATION`.

## 9. R6S introduces the composition error

### 2026-09-19 05:04:09Z — EE-P2R6S

Historical tip:

`48887a2b1523c9d20933e4d6c5e341e80d7a0ff6`.

Current LM2-base accepted materializer blob:

`11b28416aac5a4899706150721f2f8ac8bb6ee43`.

### Question lane

R6S remains source-local:

`canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED")`.

This is consistent with C11 and HB01.

### Response-value lane

For substantive codes 1..5, R6S does:

`canonical_value=str(code)`

and:

`transform_authority_ref=SOURCE_AUTH_REF`.

`SOURCE_AUTH_REF` resolves to the P2F2 authority whose kind is:

`SOURCE_SEMANTICS_TOPOLOGY`.

This is the first inspected WVS7 point where source-native response semantics are inserted into a field whose C11 contract explicitly denotes authorized canonical response material.

That is the contract divergence.

## 10. Why R6S qualification did not settle the issue

R6S's own return records browser/deterministic qualification with:

- no real WVS carrier access;
- no empirical outcomes;
- no measured performance;
- projection construction focused on metadata / B_COUNTRY.

Its generic source-backed facade statement therefore did not supersede the C11 authority rule.

There is no inspected R6S adjudication saying that `SOURCE_SEMANTICS_TOPOLOGY` is allowed to stand in for mapping authority.

The contradiction remained latent until LM2 attempted:

`CANDIDATE_NEUTRAL_COMMON_C11_BUILD`.

## 11. LM2 is the first exact collision court in this lineage

Base:

`bf0f4ebb00e7304e1cda29f7ca9b6595fff248dc`.

LM2 resolves the R6S transform authority and the accepted C11 validator together and obtains:

`Pre553AuthorityError: authority kind mismatch`

then:

`C11IntegrityError: canonical response/question material lacks exact positive mapping authority`.

No oracle was frozen and no Candidate A/B/C process began.

## 12. Archaeological conclusion

The history is internally coherent until R6S response-value construction:

1. canonical fields are optional;
2. source semantics and native/canonical mapping are distinct;
3. C11 enforces the distinction;
4. source-backed facade preserves the distinction;
5. WVS7 ownership/HB01 use native/source-local C11 successfully;
6. R6A/P2F2 grant source-native semantics/topology;
7. R6S populates canonical response values with that source-native authority;
8. LM2 correctly refuses the composition.

Therefore the C11 stop is an intentional guardrail, but the **R6S/C11 mismatch itself is a later composition contradiction**, not an intentional accepted authority gap.
