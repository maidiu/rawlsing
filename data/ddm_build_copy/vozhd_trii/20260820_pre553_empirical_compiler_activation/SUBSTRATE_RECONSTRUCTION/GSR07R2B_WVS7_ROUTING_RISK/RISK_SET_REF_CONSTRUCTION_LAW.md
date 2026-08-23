# G-SR07-R2B — deterministic `risk_set_ref` / `member_set_replay_ref` construction law

Status: `FROZEN_LANE_B_CONSTRUCTION_LAW__NON_CERTIFYING`

This law defines identity construction only. It does not manufacture missing documentary inputs and it does not consume Lane C provisional work.

## 1. Inputs must already be accepted

For one target/rule instance, construction requires:

1. exact WVS7 source snapshot SHA-256 (`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`);
2. exact accepted `EmpiricalUniverse` ref;
3. exact target/question ref from the accepted Lane-A/C11 ownership join;
4. one Lane-B rule-family row plus target-specific parameters;
5. exact authority refs for every documentary predicate used by that rule;
6. exact scoped respondent refs bound to source snapshot + source row ordinal;
7. exact positive determinant facts required by the rule (country, form, person-position presence, parent response, subgroup coordinate, etc.).

Observed child missingness, response incidence, frequencies, or complement-of-populated-rows are never determinant inputs.

## 2. Canonical rule material

Use the existing PRE553 `canonicalize` / `semantic_hash` law. Build:

```text
routing_rule_material = {
  contract: "PRE553_WVS7_GSR07R2B_ROUTING_RULE@1.0.0",
  source_sha256,
  empirical_universe_ref,
  target_ref,
  rule_family_id,
  rule_parameters,
  positive_determinant_ast,
  parent_routing_rule_refs,
  documentary_authority_refs,
  unknown_policy: "PRESERVE_ROUTING_UNKNOWN",
  anti_inference_policy: "NO_MISSINGNESS_FREQUENCY_OR_COMPLEMENT_INFERENCE"
}
```

Sort all set-like reference lists by exact ref key before hashing. The semantic hash `H_rule = semantic_hash(routing_rule_material)` defines:

```text
routing_rule_ref = ExactRef(
  kind="ROUTING_RULE",
  object_id="urn:rawlsing:pre553:gsr07r2b:wvs7:routing-rule:sha256:" + H_rule,
  content_hash=H_rule
)
```

## 3. `risk_set_ref`

`risk_set_ref` identifies the governed risk-set *definition*, not a guessed observed row complement.

```text
risk_set_material = {
  contract: "PRE553_WVS7_GSR07R2B_RISK_SET@1.0.0",
  source_sha256,
  empirical_universe_ref,
  target_ref,
  routing_rule_ref,
  parent_risk_set_refs,
  determinant_input_schema_refs,
  documentary_authority_refs,
  respondent_identity_protocol: "EXACT_SOURCE_SNAPSHOT_PLUS_ROW_ORDINAL_TO_SCOPED_RESPONDENT_REF",
  membership_semantics: "POSITIVE_ELIGIBILITY_ONLY__UNKNOWN_IS_NOT_NEGATIVE"
}
```

`H_risk = semantic_hash(risk_set_material)` and:

```text
risk_set_ref = ExactRef(
  kind="RISK_SET",
  object_id="urn:rawlsing:pre553:gsr07r2b:wvs7:risk-set:sha256:" + H_risk,
  content_hash=H_risk
)
```

## 4. Tri-state deterministic evaluation

Evaluate every scoped respondent in source row-ordinal order from accepted determinant inputs only. Each row must resolve to exactly one of:

- `ELIGIBLE_APPLICABLE` — positive rule satisfied;
- an explicit negative state (`NOT_ELIGIBLE` or `INAPPLICABLE`) only when the accepted rule contains a positive, deterministic negative branch (for example exact country outside a closed module scope, exact form=B for target Q294A, or MENA_25=No for the borrower follow-up);
- `ROUTING_UNKNOWN` — determinant absent, conflicting, unaccepted, or not representable.

Do not turn UNKNOWN into a nonmember by complement. Do not turn a child response/missing code into the parent route.

## 5. `member_set_replay_ref`

The member-set replay object binds all three partitions, not merely the positive denominator:

```text
member_set_replay_material = {
  contract: "PRE553_WVS7_GSR07R2B_MEMBER_SET_REPLAY@1.0.0",
  source_sha256,
  risk_set_ref,
  routing_rule_ref,
  ordered_evaluations: [
    {
      source_row_ordinal,
      scoped_respondent_ref,
      routing_state,
      determinant_fact_refs,
      authority_refs_used
    }, ...
  ],
  eligible_member_refs_sorted,
  explicit_nonmember_refs_sorted,
  routing_unknown_refs_sorted,
  evaluation_order: "SOURCE_ROW_ORDINAL_ASC",
  no_complement_inference: true
}
```

The ordered evaluations are canonicalized; the three set-like ref arrays are key-sorted. `H_members = semantic_hash(member_set_replay_material)` defines:

```text
member_set_replay_ref = ExactRef(
  kind="MEMBER_SET_REPLAY",
  object_id="urn:rawlsing:pre553:gsr07r2b:wvs7:member-set-replay:sha256:" + H_members,
  content_hash=H_members
)
```

Every `RoutingEligibilityFact@1.0.0` for this target/rule instance must carry this exact `risk_set_ref`, `routing_rule_ref`, and `member_set_replay_ref`. `parent_predicate_refs` must name only accepted positive predicate refs.

## 6. Nested rules

Nested targets are conjunctions of positive parents, never row complements. Examples:

- Q294A = Political-Trust-module membership AND exact form assignment A;
- MENA_26*/27* = MENA-module membership AND exact MENA_25=Yes;
- H310 = accepted Gender-version/target administration AND exact H309=Yes;
- NG_13 = Nigeria country-specific item administration AND accepted respondent sex=female.

If any required parent is `ROUTING_UNKNOWN`, the child is `ROUTING_UNKNOWN` unless a separate accepted authority independently resolves it.

## 7. Replay stability

Changing any source snapshot, authority snapshot, target binding, rule parameter, parent rule, respondent binding, determinant fact, or tri-state evaluation changes the corresponding semantic hash. A ref is therefore reusable only for the exact frozen closure from which it was constructed.
