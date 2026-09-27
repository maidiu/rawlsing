# M1 RULE BINDING AND AUTHORITY LAW R1

## 1. Central rule

M1 never asks:

> Which validator seems appropriate?

M1 asks:

> Which exact competent authority, under an explicit governed binding, says that this exact validator governs this exact claim family and scope?

Freeze:

`RULE_NAME_MATCH != RULE_AUTHORITY`

`I05_RULE_ID != M1_VALIDATION_AUTHORITY`

`NEWEST_RULE != CURRENT_RULE`

`PROTOTYPE_SUCCESS != ADOPTION`

`EVIDENCE_PROVENANCE != ACCEPTANCE_AUTHORITY`

## 2. Exact selection procedure

For every call M1 SHALL:

1. resolve the declared `claim_family_id` and `claim_rule_id`;
2. consume exactly one `M1FamilyRuleBinding` applicable to the requested jurisdiction;
3. verify the binding's exact authority id/version/hash;
4. verify the binding's selection purpose;
5. for `CURRENT_GOVERNED_USE`, require explicit P2-compliant current-selection authority;
6. for `EXACT_PINNED_REPLAY`, require the caller to name the historical exact binding and prohibit any currentness claim;
7. verify family, source/universe, risk, topology, measure, time/geography and target scope applicability;
8. resolve every premise channel the rule declares required;
9. fail closed on missing, denied, conflicting or scope-mismatched required premises;
10. dispatch only to the exact validator named in the binding.

There is no fallback resolver.

## 3. Forbidden selection mechanisms

The following have zero semantic authority:
- latest timestamp;
- newest commit;
- highest semantic-version string;
- filesystem order;
- first/last registry row;
- source name similarity;
- family name similarity;
- candidate `rule_id` string coincidence;
- previous successful execution;
- most complete provenance;
- most support;
- a default validator;
- historical precedent absent current binding.

## 4. Discovery authority boundary

I05 `DiscoveryAuthority` already binds discovery-time `support_rules` and `validation_rules`. Those rules authorize the discovery procedure and terminal receipt semantics at I05 grain.

They do not become universal M1 learned-validation authority merely because:
- they are in a current I05 authority object;
- a receipt is `EVALUATED_SUPPORTED`;
- `validation_fact_refs` are present;
- all candidate coverage is terminal;
- replay is exact.

A family may deliberately adopt the same substantive rule for M1, but that requires an explicit competent M1 family-rule binding. Reuse is lawful; inference is not.

## 5. P1 identity boundary

P1 separates:
- relation proposition identity;
- semantic claim identity;
- governing authority instance;
- lifecycle/current-selection;
- consumer permission.

M1 conforms by making its output an adjudication receipt whose identity can change with authority while separately carrying any P1 semantic claim identity emitted by the family validator.

A generic hash of arbitrary JSON cannot establish typed claim correctness.

## 6. P2 currentness boundary

P2 freezes `CURRENTNESS_IS_EXPLICIT`.

M1 therefore does not maintain or infer currentness. It may consume a P2-compliant current-selection fact as a premise for choosing an applicable current family rule.

`RECERTIFIES != CURRENT_SELECT`

A recertified validator is not current solely because it is newer.

## 7. Operation-scoped premise law

Comparability, source-universe composition, pooling/backfill, weight/design/estimand, measurement portability and prerequisite-universe completeness remain separate operation-scoped authorities.

If a family validator requires one:
- it must name the exact required authority kind;
- M1 must bind the exact positive authority/load;
- absence or conflict blocks the affected adjudication.

No neighboring authority widens another. In particular, shared labels/scales or source-semantic equivalence do not manufacture measurement portability.

## 8. Historical/candidate/prototype owners that must not self-promote

### I05
Current exact discovery owner. Reusable evidence/replay machinery. Not generic learned-acceptance owner.

### C07
Architecture precedent that explicitly identified missing empirical validation/comparability/composition authorities. Its learned-world DAG does not fill those missing rules.

### PRE553 I04
Structural-admission owner for one exact structural-use jurisdiction. It cannot become M1 empirical validation and M1 cannot become I04.

### FF02 / D04 candidate court
Demonstrates lane-specific relation/admission reasoning and the rule that valid-empty/support cannot be laundered into structure. Candidate/pending-HQ artifacts remain noncurrent unless explicitly adopted.

### Field Forge R2
Actor-independent structural relation architecture and negative-ceiling law. It does not authorize M1 substantive learned-validation rules by generic inheritance.

### P1/P2 semantic constitution
Binding constitutional precedent for identity and lifecycle. They do not themselves decide arbitrary empirical claim families.

### Source-specific comparators/validators
Callable only within exact adopted family/scope. No generic promotion.

## 9. Authority conflict law

If multiple candidate bindings appear applicable and no exact authority resolves precedence/currentness:
- M1 returns `BLOCKED` or `UNRESOLVED` with `AMBIGUOUS_OR_CONFLICTING_RULE_AUTHORITY`;
- it must not pick one by chronology or specificity heuristic.

If an authority hash or semantic projection mismatches:
- M1 returns `INTEGRITY_FAILURE`.

## 10. Provenance/support hostile theorem

The decisive hostile case is:

- all input objects have valid hashes;
- replay closes;
- provenance is complete;
- empirical support is nonzero/high;
- I05 says `EVALUATED_SUPPORTED`;
- but no exact competent M1 family-rule binding exists.

Required M1 output:

`BLOCKED__MISSING_FAMILY_VALIDATION_RULE_AUTHORITY`

Any `RULE_SATISFIED` result in this fixture is unconstitutional.

This proves:

`PROVENANCE + SUPPORT + REPLAY != SUBSTANTIVE_ACCEPTANCE_AUTHORITY`
