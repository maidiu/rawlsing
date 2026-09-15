# GT3/GT4 N3 — REPAIRED METABOLISM AUTHORITY HOSTILE RE-AUDIT R1

## Terminal

`PASS__GT34_N3_REPAIRED_METABOLISM_AUTHORITY_HOSTILE_AUDIT__LAWFUL_FOR_VALID_EMPTY_ADOPTION`

## Execution boundary

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt34-n3-metabolism-repaired-candidate-hostile-audit-r1`
- exact working-ancestry start: `bca519e3d39b7c3886210958800a4b47ecb50440`
- immutable instruction ref: `58919890d0d502c4dd65b962dc8436cb4758710a`
- instruction blob: `aad246110f5f451f30a31c5df5246f25859943f4`
- worker: `N3 — REPAIRED METABOLISM AUTHORITY HOSTILE RE-AUDIT R1`
- profile: `HOSTILE_AUDIT`
- adoption: NONE
- implementation: NONE
- operation registration: NONE
- PSEPF execution: NONE
- actor mutation: NONE

Audit target is only the corrected M2 package.

M2 return:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT3_GT4_Q69B_METABOLISM_TARGET_EFFECT_WAVE_R1/M2_METABOLISM_CONTENT_ADDRESS_REPAIR_R1/00_RETURN.md`

M2 return blob:

`486cd220b3e1123f95a5107b94f21ce3097b0636`

Corrected authority:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0`

Corrected authority hash:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

Valid-empty registry:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY@1.0.0`

state:

`VALID_EMPTY_NO_ACCEPTED_OPERATIONS`

registry hash:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

Operation-entry projection:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_ENTRY_SEMANTIC_PROJECTION@1.0.0`

projection-law hash:

`ab0866cf59676a097cb49d5c77cdd3898b92c9abab7dc223eaa7e9151177587f`

Decision-receipt projection:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT_SEMANTIC_PROJECTION@1.0.0`

projection-law hash:

`e0b6a723aaa31f07c0bf9d156961c9fdcd424e3b6705acbfc04d2612278b2e80`

Superseded K2 authority hash:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

Disposition of superseded hash:

`HISTORICAL_EVIDENCE_ONLY__MUST_NOT_BE_ADOPTED`

---

# 1. Central holding

The exact two defects proved by L2 are closed by M2 without semantic widening.

The repaired package is lawful for **valid-empty adoption only**.

The valid-empty registry carries:

`ZERO_POSITIVE_AUTHORITY`.

N3 found no remaining defect in:

- corrected content addressing;
- operation-entry replay identity;
- decision-receipt replay identity;
- collection canonicalization;
- valid-empty behavior;
- target-owner selection;
- ownership boundaries;
- direct-assignment firewall;
- measurement portability;
- stochastic authority;
- negative-state preservation.

No positive operation becomes lawful by this PASS.

A future positive operation still requires a separately accepted-current registry entry and its own hostile review/adoption.

---

# 2. Independent recomputation of all four corrected hashes — PASS

Current repository canonical law was checked at:

`rawlsing_next/pre553_empirical_objects.py`

blob:

`91974c52ce8c0acafa939be0d7d83f4a5c8085b7`

Relevant current law:

`canonical_json(value) = json.dumps(canonicalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)`

`semantic_hash(value) = SHA256(UTF8(canonical_json(value))).hexdigest()`

Set-like current law canonicalizes each member, keys by canonical JSON, collapses identical canonical members, and emits members in canonical-JSON sort order.

N3 independently parsed the exact corrected JSON material from the M2 return and recomputed:

### Corrected authority

expected:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

recomputed:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

result:

`EXACT_MATCH`

### Valid-empty registry

expected:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

recomputed:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

result:

`EXACT_MATCH`

### Operation-entry semantic projection

expected:

`ab0866cf59676a097cb49d5c77cdd3898b92c9abab7dc223eaa7e9151177587f`

recomputed:

`ab0866cf59676a097cb49d5c77cdd3898b92c9abab7dc223eaa7e9151177587f`

result:

`EXACT_MATCH`

### Decision-receipt semantic projection

expected:

`e0b6a723aaa31f07c0bf9d156961c9fdcd424e3b6705acbfc04d2612278b2e80`

recomputed:

`e0b6a723aaa31f07c0bf9d156961c9fdcd424e3b6705acbfc04d2612278b2e80`

result:

`EXACT_MATCH`

For control, N3 also recomputed the superseded K2 authority material:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

That exact old hash is valid only for the old defective candidate material. It is not the corrected candidate identity and must not be adopted.

---

# 3. Structural-diff court — no semantic widening — PASS

N3 structurally compared the old K2 authority JSON with the corrected M2 authority JSON.

The only changed paths are exactly:

1. `operation_registry_contract.operation_entry_semantic_projection`
2. `operation_registry_contract.operation_ref_contract.hash`
3. `operation_registry_contract.operation_ref_contract.projection_ref`
4. `operation_registry_contract.operation_ref_contract.validation`
5. `replay_contract.decision_receipt_hash_contract`
6. `replay_contract.decision_receipt_semantic_projection`

No other authority material changed.

The valid-empty registry material is byte-for-byte semantically identical before and after repair.

Therefore M2 did not alter:

- jurisdiction;
- owner;
- input family;
- decision space;
- decision precedence;
- decision meanings;
- operation kinds;
- positive transition requirements;
- READ_ONLY requirements;
- source cardinality;
- measurement-transfer prohibition;
- target-owner separation;
- causal-parent requirements;
- stochastic/ADP-020 law;
- non-ownership list;
- direct-assignment firewall;
- current-selection law.

The corrected authority hash changes only because exact identity/replay law was added to authority material.

---

# 4. Operation-entry self-hash court — PASS

L2's first defect was:

`UNDERDEFINED_SELF_HASHING_OPERATION_ENTRY`.

M2 closes it exactly.

The operation semantic projection includes 21 semantic fields:

1. `operation_ref.operation_id`
2. `operation_ref.operation_version`
3. `status`
4. `operation_kind`
5. `accepted_input_class_ref`
6. `accepted_upstream_input_states`
7. `requested_use_classes`
8. `temporal_applicability_rule_ref`
9. `source_scope_cardinality`
10. `measurement_transfer_allowed`
11. `metabolism_effect_ceiling`
12. `downstream_consumer_authority_ref`
13. `downstream_mutation_owner_authority_ref_or_read_only_none`
14. `downstream_transition_rule_ref_or_read_only_none`
15. `downstream_mutation_ceiling_ref_or_read_only_none`
16. `causal_parent_contract_ref`
17. `causal_parent_requirements`
18. `execution_mode`
19. `adp020_contract_or_deterministic_none`
20. `replay_rule_ref`
21. `negative_limit_refs`

The only excluded field is:

`operation_ref.operation_content_hash`

because it is the derived digest.

Exact law:

`operation_content_hash = lowercase_hex(SHA256(UTF8(canonical_json(operation_entry_semantic_projection))))`

Then and only then is the final:

`{operation_id, operation_version, operation_content_hash}`

materialized or validated.

There is no recursive digest fixed point.

N3 synthetic hostile check changed every one of the 21 semantic fields independently. Every change altered the digest.

N3 separately changed only the supplied derived `operation_content_hash`. Projection identity remained unchanged, and the supplied hash then failed exact validation.

Therefore a caller cannot create a second compliant operation identity by choosing a different derived hash.

---

# 5. Operation ID/version remain semantic — PASS

`operation_ref.operation_id`

and:

`operation_ref.operation_version`

are both inside the semantic projection.

They are not excluded with the derived content hash.

Independent perturbation of either changed the synthetic projection digest.

The repair therefore did not turn ID/version into decorative or caller-controlled metadata.

---

# 6. Operation collection law — PASS

Operation-entry set-like fields are explicitly:

- `accepted_upstream_input_states`
- `requested_use_classes`
- `causal_parent_requirements`
- `negative_limit_refs`

They use repository canonical-set normalization.

N3 reversed every set-like field simultaneously and obtained the same digest.

N3 inserted duplicate canonical members and obtained the same digest, matching current repository canonical-set law.

Top-level semantically ordered sequence fields are explicitly:

`NONE`

for this v1 entry schema.

The repaired authority further freezes:

- undeclared sequence -> schema mismatch;
- unlisted entry field -> schema mismatch;
- only operation ID/version/content hash are allowed in `operation_ref`;
- alternate projection -> forbidden;
- caller-selected projection -> forbidden.

No implementation-local collection interpretation remains.

---

# 7. Decision-receipt projection completeness — PASS

L2's second defect was:

`UNDEFINED_DECISION_RECEIPT_HASH_PROJECTION`.

M2 closes it by defining one exact projection over all 28 replay-material fields named by K2's `every_decision_binds` contract:

1. `actor_ref`
2. `actor_identity_authority_ref`
3. `v3_empirical_possibility_input_ref`
4. `psepf_ref`
5. `psepf_replay_ref`
6. `comparator_receipt_refs`
7. `conditioner_ancestry_refs`
8. `source_universe_ref`
9. `release_ref`
10. `empirical_reference_time_ref`
11. `measure_basis_ref`
12. `estimand_refs`
13. `uncertainty_ref_or_typed_state_ref`
14. `v3_decision_time_ref`
15. `v3_effective_use_time_ref`
16. `requested_use_class`
17. `requested_operation_ref`
18. `operation_registry_ref`
19. `resolved_operation_entry_ref_or_typed_absence`
20. `requested_downstream_owner_ref_or_read_only_marker`
21. `resolved_downstream_owner_ref_or_typed_absence`
22. `causal_parent_contract_ref_or_typed_absence`
23. `causal_parent_refs`
24. `pre_state_checkpoint_ref`
25. `runtime_rule_registry_ref`
26. `rng_decision_receipt_refs_or_empty`
27. `decision_state`
28. `decision_reason_code`

The only excluded receipt field is:

`decision_receipt_hash`.

N3 independently perturbed every one of the 28 included fields. Every perturbation changed the receipt digest.

No K2 replay-material receipt field is silently outside identity.

---

# 8. Decision-receipt hash law and independent verification — PASS

Exact law:

`decision_receipt_hash = lowercase_hex(SHA256(UTF8(canonical_json(decision_receipt_semantic_projection))))`

The receipt is materialized/validated only after this digest is recomputed.

The authority explicitly freezes:

- self reference = forbidden;
- alternate projection = forbidden;
- caller-selected projection = forbidden;
- unlisted receipt field = schema mismatch;
- projection/hash mismatch = `INTEGRITY_FAILURE`;
- caller-supplied hash authority = false.

A downstream owner with the immutable receipt material and the corrected adopted authority can therefore:

1. reconstruct the exact projection;
2. canonicalize its set-like fields;
3. canonicalize the resulting projection;
4. recompute SHA-256;
5. require exact equality with `decision_receipt_hash`.

No implementation-specific hash projection is needed.

---

# 9. Receipt collection law — PASS

Receipt set-like fields are explicitly:

- `comparator_receipt_refs`
- `conditioner_ancestry_refs`
- `estimand_refs`
- `causal_parent_refs`
- `rng_decision_receipt_refs_or_empty`

Reversing all of those collections leaves receipt identity unchanged under repository canonical-set law.

Top-level semantically ordered receipt sequences are explicitly:

`NONE`.

Semantic order inside exact referenced replay, ancestry, or RNG objects remains governed by those referenced content identities rather than by incidental order in this receipt.

This is compatible with accepted ADP-020, whose stochastic replay identity binds exact draw coordinates, semantic rule identity, candidate-set identity and decision/draw receipts rather than relying on incidental iteration order.

Accepted ADP-020 artifact:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/ADP_020_V3_CAUSAL_RNG/AUTHORITY.json`

blob:

`1f13dc7ccc69bda562613d6215acc996a9c092e4`

No RNG semantic owner was imported into the metabolism authority.

---

# 10. Positive / negative / valid-empty receipts share one identity law — PASS

The same decision-receipt projection applies to every K2 decision state:

- `ALLOW_READ_ONLY`
- `ELIGIBLE_FOR_NAMED_TRANSITION_RULE`
- `DENY`
- `VALID_EMPTY`
- `NONCOMPARABLE`
- `STALE`
- `UNRESOLVED_INPUT`
- `UNRESOLVED_AUTHORITY`
- `INTEGRITY_FAILURE`

N3 instantiated every state under the same projection schema and independently produced a valid 64-hex SHA-256 digest for each.

There is no special weaker hash law for negative, unresolved, stale, noncomparable, or valid-empty receipts.

Therefore negative authority cannot evade replay identity.

---

# 11. Valid-empty registry remains zero positive authority — PASS

The corrected package's registry material remains exactly:

- state = `VALID_EMPTY_NO_ACCEPTED_OPERATIONS`;
- `entries = []`;
- `positive_read_operations = 0`;
- `positive_transition_operations = 0`;
- `accepted_current_only = true`;
- `caller_selectable = false`;
- `fuzzy_latest_default_forbidden = true`.

Its hash is unchanged because its material is unchanged:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

The corrected authority continues to say:

`VALID_EMPTY_REGISTRY__NO_POSITIVE_READ_OR_TRANSITION_OPERATION_AUTHORIZED`.

Therefore adoption of this exact valid-empty package permits:

- zero `ALLOW_READ_ONLY` operation;
- zero `ELIGIBLE_FOR_NAMED_TRANSITION_RULE` operation;
- zero target mutation owner selection;
- zero RNG consumption under a metabolism operation;
- zero actor mutation.

This PASS must not be read as authority for any concrete metabolism operation.

---

# 12. Target-owner selection without registered operation — REJECTED / PASS

The invocation may request an operation and requested target owner, but caller request is not resolution authority.

A positive transition still requires an accepted-current exact operation entry binding:

- exact operation identity/hash;
- exact input class;
- exact use;
- exact downstream mutation owner;
- exact downstream transition rule;
- exact mutation ceiling;
- exact temporal applicability;
- exact causal-parent contract/parents;
- exact pre-state checkpoint;
- exact replay rule;
- exact ADP-020 material if stochastic.

The current registry has no entry.

Therefore no CAN-008 or other owner is selected by this package.

The repaired hash law does not alter this.

---

# 13. Ownership and no-direct-assignment court — PASS

Controlling N007 artifact:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N007_TRII_DEVELOPMENTAL_ROUTE/CORPUS/ORIGINAL/ebb5733d3160__RESULT.md`

blob:

`ebb5733d3160c2d1c54475780f2a6512f88f9eea`

N007 freezes:

`PSEPF -> V3EmpiricalPossibilityInput -> V3`

with actor mutation solely under named V3 transition authorities.

It forbids direct assignments including:

- field mass -> actor belief probability;
- modal population cell -> actor response/persona;
- survey configuration -> memory/knowledge;
- population possibility -> generated structural position.

The corrected M2 authority's non-ownership and direct-assignment firewall are byte-for-byte semantically unchanged from K2.

It still does not own:

- PSEPF geometry;
- comparator/query/source/measure semantics;
- portability/equivalence;
- V557/V558 context;
- downstream actor-state semantics;
- actor mutation;
- randomness semantics;
- V2 rendering/persona/voice.

No raw PSEPF -> actor-state promotion was introduced by M2.

---

# 14. Portability leakage court — REJECTED / PASS

The corrected candidate retains:

`measurement_transfer_or_portability = FORBIDDEN_NOT_CONSUMED`

and first-operation source scope:

`EXACTLY_ONE_SOURCE_UNIVERSE_AND_RELEASE`.

Every positive operation entry must still bind:

`measurement_transfer_allowed`

and the first-wave law remains false.

The hash repair did not add any source-equivalence, measure-equivalence, pooling, transfer, or portability operation.

N007 separately freezes source plurality and composition as none-by-default absent operation-specific positive authority.

No portability leakage exists in the corrected package.

---

# 15. Negative-state preservation — PASS

The corrected authority preserves the same distinct decision states as K2:

- `DENY`
- `VALID_EMPTY`
- `NONCOMPARABLE`
- `STALE`
- `UNRESOLVED_INPUT`
- `UNRESOLVED_AUTHORITY`
- `INTEGRITY_FAILURE`

The decision-precedence law is unchanged.

The receipt projection now makes those exact outcomes replay-addressable under one common hash law.

M2 therefore repaired replay determinacy without collapsing negative semantics.

---

# 16. Stochastic bypass court — REJECTED / PASS

The corrected authority preserves K2's exact stochastic ceiling.

A stochastic positive operation requires exact ADP-020 authority, named stream, authorized RNG operation and receipts.

Accepted ADP-020 law independently freezes:

- RNG may not create candidates;
- randomness is not semantic authority;
- empty candidate set consumes zero draws and gets no fabricated fallback;
- deterministic path consumes no dummy draw;
- replay metadata failure blocks rather than silently reseeding or repairing;
- candidate ordering cannot be promoted into semantic priority.

M2 did not modify any stochastic field except making exact operation/replay identity independently content-addressable.

No stochastic bypass exists.

---

# 17. Superseded K2 identity court — PASS

The old K2 authority hash:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

correctly identifies only the pre-repair candidate.

The repaired authority material hashes to:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

The old candidate was never adopted.

Therefore retaining authority ID/version `1.0.0` during pre-adoption repair does not create two adopted-current authorities.

Any HQ adoption must content-bind the corrected authority hash.

The valid-empty registry hash remains unchanged, so lawful adoption must bind the exact pair:

- authority hash `e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`;
- registry hash `b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`.

The superseded authority hash is not an alternative current candidate.

---

# 18. Required N3 audit adjudication

1. exact recomputation of all four corrected hashes — **PASS**
2. operation-entry projection has no self-hash cycle — **PASS**
3. operation ID/version remain semantic — **PASS**
4. only derived operation content hash is excluded — **PASS**
5. receipt projection binds every K2 replay-material receipt field — **PASS**
6. only derived receipt hash is excluded — **PASS**
7. set-like vs ordered collection law is unambiguous — **PASS**
8. unknown fields fail schema rather than evade identity — **PASS**
9. positive/negative/valid-empty receipts share one hash law — **PASS**
10. downstream owner can independently recompute receipt — **PASS**
11. valid-empty registry remains zero positive authority — **PASS**
12. no target owner can be selected absent exact registered operation — **PASS**
13. no raw PSEPF -> actor-state promotion — **PASS**
14. no portability authority leakage — **PASS**
15. no semantic/jurisdiction widening introduced by hash repair — **PASS**

L2's original non-hash hostile holdings also survive because M2 did not alter their controlling semantic material.

---

# 19. Adoption ceiling

N3 authorizes no adoption itself.

Its holding is only that HQ may lawfully adopt the exact corrected authority together with the exact valid-empty registry if HQ chooses.

Such adoption would create:

- a metabolism authority membrane;
- deterministic exact content-addressing/replay law;
- **zero positive metabolism operations**.

It would not authorize:

- READ_ONLY use;
- transition eligibility;
- CAN-008 selection;
- any target effect;
- any PSEPF execution;
- any actor mutation.

Any future positive registry entry must receive a new content identity and separate semantic review/adoption.

## Final disposition

The repaired package survives hostile re-audit.

The two L2 content-addressing defects are closed without widening K2's authority model.

`PASS__GT34_N3_REPAIRED_METABOLISM_AUTHORITY_HOSTILE_AUDIT__LAWFUL_FOR_VALID_EMPTY_ADOPTION`
