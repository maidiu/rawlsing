# GT12 E2B R3 — MINIMAL PUBLICATION BUNDLE CONTRACT R1

## Terminal

`PASS__GT12_E2B_R3_MINIMAL_PUBLICATION_AUTHORITY_BUNDLE_CONTRACT_DEFINED__NO_ADOPTION`

## Scope

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt12-e2b-r3-publication-bundle-contract-r1`
- exact working-ancestry start: `a9633c86734b68d04805efa2c8524f57708bd3f7`
- immutable instruction ref: `802c376c218f579fb28977c59590e43c2cef5957`
- worker: `H2 — MINIMAL PUBLICATION BUNDLE CONTRACT R1`
- production surface: READ ONLY
- provider-existence proposition: NOT DECIDED; H1 owns it
- authority adoption: NONE
- production implementation: NONE

The current APIs can represent the smallest lawful contract without semantic distortion. The correct production representation is one immutable, content-addressed **binding envelope** that preserves two distinct authority components while deriving the two redundant API identifiers mechanically.

It is **not** four caller-selected values and it is **not** one fused authority.

## 1. Exact four-input semantic/type contract

### A. `governed_use_id`

**Runtime type:** exact non-empty string.

**Semantic owner:** the accepted-current V554 governed-use namespace/provider competent for the relation-specific M1/V554 operation. The runtime owner is V554; this string is not itself an authority grant.

**Exact jurisdiction:** one frozen use of:
- `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`;
- basis kind `ADMITTED_FIELD_FORGE_RELATION`;
- signature `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`;
- target use `STRUCTURAL_MEDIATION_INPUT`;
- focal proposition `GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_COUNT_PROFILE_WITHIN_SCOPE`;
- direct route `V554_TO_V557_DIRECT`.

**Identity/currentness:** exact frozen identifier only; no `latest`, `default`, wildcard, environment selection, or caller override. It need not itself be hash-shaped because its semantics are content-bound by the publication authority and outer bundle.

**Cross-field binding:** it MUST equal:
1. `publication_authority.governed_use_id`;
2. the `governed_use_id` supplied to `evaluate_m1_admitted_field_forge_relation_v554`;
3. the resulting `M1Evaluation.governed_use_id`;
4. the direct V554→V557 handoff material's `governed_use_id`.

**Authority status:** identifier of an already-governed operation; no independent semantic authority.

Evidence:
- `rawlsing_next/gt12_d_to_m4_typed_bridge.py::evaluate_typed_d_to_e_at_v554`
- `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py::_parse_invocation`
- `rawlsing_next/m1_temporal_v554_admission_dedup.py::_handoff`

### B. `v554_rule_ref`

**Runtime type:** mapping exactly normalized as:
`{"id": <nonempty>, "version": <nonempty>, "hash": <lowercase sha256>}`.

**Semantic owner:** accepted-current SCR554/V554 rule authority competent for the relation-specific SIG-004 admitted-relation ingress.

**Exact jurisdiction:** the referenced rule must explicitly be competent for the same frozen relation M1 contract, `ADMITTED_FIELD_FORGE_RELATION`, `SIG_004`, `STRUCTURAL_MEDIATION_INPUT`, focal proposition, and direct V554→V557 publication path. It cannot be inferred from a generic V554-looking name or shape.

**Identity/currentness:** exact id/version/content hash resolving to accepted-current rule material. No fuzzy/current-by-convention selection.

**Cross-field binding:** exact id/version/hash MUST equal:
1. `publication_authority.rule_ref`;
2. the rule embedded in the relation equivalence key;
3. F1 `rule_id/rule_version/rule_hash`;
4. the direct handoff `v554_rule_ref`.

**Authority status:** the ref identifies an already-governed V554 rule. The referenced rule is authority-bearing; the ref is not a second publication grant.

**Generic-rule competence:** an already-accepted general V554 rule can be competent only if its adopted semantic jurisdiction explicitly includes this exact SIG-004 relation path. Broadness cannot be used to infer missing relation competence. If a new rule must be constituted, the smallest lawful rule is relation/use-specific.

Evidence:
- `rawlsing_next/m1_temporal_v554_admission_dedup.py::_rule`
- `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py::evaluate_m1_admitted_field_forge_relation_v554`

### C. `publication_authority`

**Runtime type / exact consumed schema:**
- `authority_id`
- `authority_version`
- `authority_hash`
- `producer`
- `publisher`
- `governed_use_id`
- `rule_ref`
- `decision`
- `allowed_object_families`

**Semantic owner:** accepted-current V554→V557 publication-authority owner for this exact governed use/rule.

**Positive authority carried:** this is the component that authorizes the direct publication handoff. Required consumed values/constraints:
- authority id/version/hash: exact accepted-current authority identity;
- `producer == "V554"`;
- `publisher == "V557"`;
- `governed_use_id`: exact bound governed use;
- `rule_ref`: exact bound V554 rule;
- `decision == "AUTHORIZED"`;
- `allowed_object_families == ("F1",)` exactly.

**Minimal family proof:** the relation-specific production call fixes `conditions=()`. Therefore:
- F2 count is exactly zero;
- an eligible evaluation produces F1 and B1;
- downstream current M4 requires the eligible F1 lineage and a nonempty direct handoff, not B1;
- `structural_objects_from_accepted_m1` can lawfully materialize the exact F1-only handoff;
- publishing B1 would authorize an additional V554 object not required by the positive relation-to-context path.

Therefore the smallest lawful positive publication set is **F1 only**. `("F1","F2","B1")` is fixture-style overbreadth for this path.

If the production call ever stops fixing `conditions=()`, this contract becomes stale and MUST fail closed rather than widening families.

**Authority hash:** must be the exact accepted/adopted content hash of the authority object under its governing canonicalization. H2 does not mint a final authority identity or assume a hash law for an unknown H1 provider.

Evidence:
- `rawlsing_next/m1_temporal_v554_admission_dedup.py::_publication/_handoff`
- `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py` positive F1 construction
- `rawlsing_next/m4_m1_evaluation_binding.py::structural_objects_from_accepted_m1`

### D. `v557_authority_ref`

**Runtime type:** exact `m4_v557_v558_publication_repository.AuthorityRef`:
- constructor fields: `authority_id, authority_version, authority_hash`;
- serialized form: `{"id": ..., "version": ..., "content_hash": ...}`.

**Semantic owner:** accepted-current V557 governance authority.

**Smallest jurisdiction:** authorize `govern_v557` to issue governance records only for the exact V554/F1 structural objects emitted by this bound relation-specific direct handoff, with:
- decision state exactly `ALLOW_CONTEXT_ONLY`;
- V557 allowed uses exactly `("CONTEXT",)`;
- no exception state;
- producer family V554;
- source stage `M1_RELATION_V554_TO_V557`.

**Authority status:** genuine V557 governance authority, but it does **not** create the producer's CONTEXT permission. Producer `("CONTEXT",)` is already derived by the separately adopted PRE-V3→M4 translation authority.

**Required distinction:** the adopted translator
`GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY`
(hash `d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`)
is not thereby a V557 governance authority. Its ref/adoption receipt may remain rule/provenance bindings, but cannot substitute for `v557_authority_ref` without separately adopted V557 competence.

**General-V557 competence:** an existing general V557 authority may be used if its accepted semantics explicitly cover these V554/F1 objects and CONTEXT-only governance. If new authority is required, the smallest lawful jurisdiction is relation/use-specific.

Evidence:
- `rawlsing_next/m4_v557_v558_publication_repository.py::AuthorityRef/govern_v557`
- `rawlsing_next/gt12_d_to_m4_typed_bridge.py::publish_and_resolve_relation_v554_at_current_m4`
- `rawlsing_next/gt12_permission_translation_authority.py`

## 2. Candidate bundle schema

Best representation: **one immutable bound envelope containing two distinct authority components; derive the other two API inputs.**

Conceptual candidate schema:

`GT12_E2B_R3_MINIMAL_V554_V557_PUBLICATION_GOVERNANCE_BINDING@1.0.0`

```
{
  "schema": "...@1.0.0",
  "status": "CONTRACT_ONLY__NO_ADOPTION",
  "jurisdiction": {
    "program": "GT1_GT2_WAVE1_FROZEN_CANARY",
    "relation_m1_contract": "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0",
    "basis_kind": "ADMITTED_FIELD_FORGE_RELATION",
    "signature_id": "V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT",
    "target_use": "STRUCTURAL_MEDIATION_INPUT",
    "focal_structural_proposition_ref":
      "GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_COUNT_PROFILE_WITHIN_SCOPE",
    "producer_family": "V554",
    "publication_target": "V557",
    "conditions_exact": [],
    "publication_object_families_exact": ["F1"],
    "required_v557_state": "ALLOW_CONTEXT_ONLY",
    "required_v557_uses_exact": ["CONTEXT"]
  },
  "publication_authority": {
    "authority_id": "...",
    "authority_version": "...",
    "authority_hash": "...",
    "producer": "V554",
    "publisher": "V557",
    "governed_use_id": "...",
    "rule_ref": {"id":"...","version":"...","hash":"..."},
    "decision": "AUTHORIZED",
    "allowed_object_families": ["F1"]
  },
  "v557_authority_ref": {
    "authority_id": "...",
    "authority_version": "...",
    "authority_hash": "..."
  },
  "derived_api_projection": {
    "governed_use_id": "publication_authority.governed_use_id",
    "v554_rule_ref": "publication_authority.rule_ref",
    "publication_authority": "publication_authority",
    "v557_authority_ref": "v557_authority_ref"
  }
}
```

The accepted/adopted binding envelope should itself be content-addressed over canonical bundle material. That bundle hash binds the two authority components and prevents a caller from mixing a use from provider A, a rule from B, publication authority from C, and V557 authority from D.

The four runtime arguments remain API-compatible, but the production binder must project them from this one fixed current bundle rather than accept them independently from a caller.

## 3. Required cross-field invariants

1. `publication_authority.producer == "V554"`.
2. `publication_authority.publisher == "V557"`.
3. `publication_authority.decision == "AUTHORIZED"`.
4. `publication_authority.allowed_object_families == ("F1",)` exactly.
5. runtime `governed_use_id == publication_authority.governed_use_id`.
6. runtime `v554_rule_ref == publication_authority.rule_ref` exactly by id/version/hash.
7. V554 rule jurisdiction must cover `RELATION_M1_CONTRACT_ID + ADMITTED_FIELD_FORGE_RELATION + SIG_004 + STRUCTURAL_MEDIATION_INPUT`.
8. the actual M1 candidate equivalence key and F1 rule fields must equal the same rule ref.
9. `conditions == ()`; any nonempty condition set invalidates the F1-only publication contract.
10. direct handoff route must equal `V554_TO_V557_DIRECT`.
11. direct handoff object refs must be exactly the eligible F1 publication roots authorized by the bundle; no F2/B1 root may be introduced.
12. materialized M4 objects must all have `producer_family == "V554"`, `semantic_class == "F1"`, source stage `M1_RELATION_V554_TO_V557`.
13. producer allowed uses must already equal inherited `("CONTEXT",)`; the bundle must not derive a permission atom.
14. V557 governance must be exactly `ALLOW_CONTEXT_ONLY`, allowed uses `("CONTEXT",)`, no REVIEW/ACTIVE_CAUSAL.
15. V557 authority ref must be exact/current and semantically competent for this governance operation.
16. the V557 authority component must not acquire competence merely by equality/association with the PRE-V3→M4 translator.
17. all id/version/hash components must be exact; no latest/default/fuzzy selection.
18. the bound-bundle current selection itself must be caller-nonselectable.

## 4. Currentness / adoption requirements

H2 makes no provider-existence finding.

A competent later binding must prove one of:

**Existing-provider path:** H1 identifies exact accepted-current publication authority/rule/use and exact accepted-current V557 authority satisfying this contract. HQ records/selects one immutable bundle hash as current. No semantic authority may be inferred from test fixtures or historical candidates.

**New-authority path:** if H1 proves absence, HQ must explicitly constitute/adopt only the missing publication and/or V557 competence under this contract, then adopt/select the exact bundle hash. H2's schema is not itself an adoption.

For either path:
- exact rule and authority id/version/hash are mandatory;
- exact accepted/current-selection evidence is mandatory;
- no clock, branch naming convention, "latest", default, or caller choice may determine currentness;
- synthetic preflight identities are forbidden production values;
- the already-adopted PRE-V3→M4 translator and its adoption remain external prerequisites, not bundled replacement authority.

## 5. Minimal hostile court for a later binding

A later implementation must at minimum prove:

1. exact bundle schema/hash/current-selection identity;
2. real production entry exposes no independent caller overrides for any of the four values;
3. governed-use mismatch between bundle/publication/M1/handoff fails closed;
4. V554 rule id/version/hash drift fails closed;
5. V554 rule lacking explicit SIG-004 relation competence fails closed;
6. publication producer/publisher/decision mismatch fails closed;
7. publication family set empty fails and any set broader than exactly `("F1",)` fails this contract;
8. nonempty M1 conditions fail this contract rather than silently adding F2;
9. B1/F2 publication-root injection fails;
10. publication authority id/version/hash stale/wrong/unaccepted fails;
11. V557 authority id/version/hash stale/wrong/unaccepted fails;
12. PRE-V3→M4 translator ref used as V557 authority without separate V557 competence fails;
13. V557 REVIEW, ACTIVE_CAUSAL, larger use set, or non-`ALLOW_CONTEXT_ONLY` state fails;
14. V553/V555/V556 producer-family substitution fails;
15. actor/V3/V2/persona/render semantic-class contamination fails;
16. the exact F1 handoff materializes as V554, reaches exact V557 governance, V558 packaging/resolution, and does not alter inherited permission semantics.

## 6. Exact positive authority granted

The minimal bound authority permits only this:

> After an already-current, already-admitted FIELD FORGE relation has passed the exact relation-specific SIG-004 M1/V554 court, authorize publication of its exact eligible **F1** V554 structural object to V557 under the bound governed use and V554 rule, and authorize V557 to govern that exact object as **CONTEXT-only** for subsequent exact V558 resolution.

The bundle does not create empirical truth, relation meaning, admission, or permission. It licenses the missing publication/governance operation only.

## 7. Exact negative authority exclusions

The bundle MUST NOT authorize or imply:

- new empirical meaning or empirical execution;
- FIELD FORGE production or semantic ownership;
- PRE-V3 admission;
- a new permission atom or permission translation;
- REVIEW;
- ACTIVE_CAUSAL;
- F2 or B1 publication on this no-condition positive path;
- V553, V555, or V556 substitution/production;
- comparator/PSEPF authority;
- actor inference or actor-state mutation;
- positive V3 transition;
- V2 authority/expression;
- generalized V554→V557 publication outside the exact governed use/rule;
- generalized V557 competence outside the exact accepted authority jurisdiction;
- fuzzy/latest/default current selection.

## 8. Mechanical-bindability

**YES.** Once H1/HQ identifies or adopts competent exact authority components, later binding can be purely mechanical:

1. load one fixed accepted-current bundle;
2. verify its content hash/current-selection receipt and both authority identities;
3. derive `governed_use_id` from `publication_authority.governed_use_id`;
4. derive `v554_rule_ref` from `publication_authority.rule_ref`;
5. pass the exact publication-authority projection to the existing relation M1 API;
6. construct/pass the exact bound `AuthorityRef` to V557;
7. retain the already-adopted CONTEXT-only permission translator unchanged.

No new semantic inference is required at runtime. If an H1 near-match fails any competence requirement above, it cannot be mechanically coerced; HQ must adopt the missing narrow authority instead.

## Disposition

The current publication/M4 APIs are sufficient for this minimal contract. No production API redesign is required.

`PASS__GT12_E2B_R3_MINIMAL_PUBLICATION_AUTHORITY_BUNDLE_CONTRACT_DEFINED__NO_ADOPTION`
