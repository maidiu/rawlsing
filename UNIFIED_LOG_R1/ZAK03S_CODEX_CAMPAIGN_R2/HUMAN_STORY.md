# HUMAN_STORY.md — Who writes the structural rule, and what is it bound to?

**Boundary:** all statements are about protected `6a5c12f04323d74001f9632063ec907f4fc4468e` and the explicitly named candidates. They are not claims about the active PYAT machine globally.

## The short answer

The old F03 world is clear: a selected QSM row answers whether a specific source question may be used as directional relation evidence, context, administrative exclusion, or a certified exception. It copies six structural coordinates (`driver_id`, `driver_facet_id`, `question_block_id`, `structural_domain_id`, `relation_axis_id`, `target_entity_id`), polarity/reversal, coverage and pressure eligibility. That is a source-rule decision.

The modern I04 world is different. I04 has a `StructuralAdmissionRule` with a serious field set: structural target identity, structural semantic identity, directionality/role semantics, target-use permission refs, required authority bindings, estimand/measure/time scope and negatives. It can produce an `ADMITTED` receipt. But in the protected tree:

- **No non-test code constructs that rule.**
- The only concrete constructor is a test fixture.
- The test creates an `AUTH-admit` authority snapshot whose hash is computed from the fixture rule’s own semantic material. That is internally consistent, but it is not an external issuer and it is not a selected QSM row.
- The real non-test receiver, `RouteObligation.from_structural_admission`, consumes the receipt and derives route facts. It does not invoke I04, and its own callers are tests.

So the answer is not “the engine is missing.” It is “the rule producer and the selected-source binding are missing at this cut.”

## Three different things that look like permission

1. **`target_use_permission_refs` on the I04 rule** — a required tuple of `ExactRef`s carried into the receipt. It is not itself the checked authority.
2. **`RequiredAuthorityBinding` with `authority_kind="TARGET_USE_PERMISSION"`** — the actual gate. I04 resolves this `AuthorityRef`, checks operation/source/target-use, and only then can admit.
3. **`target_use_ref` / `target_use_authority_ref` / `target_use_operation` on an I03 query** — the optional target-use triple. PR1042/1043’s selected-QSM reader requires this triple and checks that it is in the query closure. This is **not** an I04 rule.

The test fixture uses a permission `ExactRef` (`PERM`) and a separate permission `AuthorityRef` (`AUTH-perm`). I04 carries `PERM` into the receipt but gates on the binding to `AUTH-perm`. No code checks that `PERM` equals the granting authority. That is a field-level gap worth naming, not a claim that the test is invalid.

## What binds to a selected QSM?

The clearest candidate is PR1042/PR1043’s `SelectedQsmRequest`:

- exact QSM path and file SHA;
- exact `row_payload_hash`;
- exact `authority_version` and `authority_rule_id`;
- source family, canonical wave, country, variable;
- native question ref;
- separate current target-use ref/authority/operation.

That candidate checks the selected QSM row’s positive status/disposition, source/wave/country, and a unique same-code native C11 response slot. Then it calls `execute_route_b_production` (I03/I05). It does **not** build `StructuralAdmissionRule` and does **not** call I04. Its receipt even records `i05_historical_qsm_authority_established=False`.

B49’s `select_source_rules` is a different selected-rule producer: it selects original35 source rules with implementation id, source variable, disposition, semantic direction, routing/response status and exact identity hash, and feeds the source-native C11 adapter. R157’s factory builds the C11 projection from a validated config and uses a typed structural replay absence. Neither produces an I04 rule.

## A worked field example

**Old F03 input:** `source_family`, `canonical_wave`, `country_code`, `question_id`, `var_code`; optional QUC fields `semantic_role_authority_status`, `semantic_role`, `current_directional_atom_eligible`, `allowed_as_v551_relation_evidence`, `structural_mapping_status`.

**Old F03 output:** six structural coordinates, `source_response_polarity`, `relation_projection_polarity`, `item_reversal`, `current_directional_atom_eligible`, `allowed_as_v551_relation_evidence`, `question_relation_coverage_eligible`, `question_relation_pressure_eligible`, `structural_mapping_status`, `mapping_status`, `semantic_role`, `semantic_role_authority_status`, `v551_visible`, `manual_review_flag`, `manual_review_reason`, plus authority-resolution metadata (`question_relation_authority_joined`, resolution status, lookup key, match count, country code, artifact path/SHA, row payload hash, review status/notes).

**Modern test fixture input/output:** a `StructuralAdmissionRule` with `admission_authority_ref`, `admission_operation`, `target_use`, structural target/semantic refs, `target_use_permission_refs`, required authority bindings, negative refs and compatibility fields; output is a `StructuralEmpiricalAdmission` receipt.

There is no bridge from the first field set to the second in protected code.

## What is reusable

- I04’s rule schema and decision precedence are useful structural-admission capital.
- The test fixture is a precise, readable example of a complete lawful rule shape.
- `RouteObligation.from_structural_admission` is a real receiver that can be tested once a producer exists.
- `pre553_carrier_execution.materialize_public_object` can re-materialize a receipt from a canonical preimage; it is a deserializer, not a producer.
- Candidate PR1042/1043 is the closest selected-QSM binding, but to I03, not I04.
- B49/R157 are real source/C11 producers, but not rule producers.

## What is not proved

No protected non-test rule constructor. No protected QSM→I04 binding. No protected non-test I04 invocation. No non-test caller of the receiver. No `PRESENT` M15 binding proved to come from `ADMITTED`. No selected QSM runtime execution or adoption. No original35/native claim.

## Case index

- [Producer/binding case](CASES/ZAK03S_CASE_R2_RULE_PRODUCER_MAP.md)
- R1 I04 seam case: `../ZAK03S_CODEX_CAMPAIGN_R1/CASES/ZAK03S_CASE_I04_STRUCTURAL_SEAM.md`
- R3 F03 case: `../ZAK03_SOURCE_AUTHORITY_RECON_R3/CASES/ZAK03_T_0004.md`
