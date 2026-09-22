# Generic Failure-Class Applicability Matrix

## Applicability vocabulary

- `APPLICABLE_NOW` — the failure question already bears directly on the banked source/authority contract.
- `APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING` — the failure cannot occur until a source runtime package/catalog/consumer exists; absence of that package is not a defect.
- `NOT_APPLICABLE` — the source/domain does not invoke the failure class at the audited grain.
- `UNKNOWN_REQUIRED_AUTHORITY_ABSENT` — applicability/closure for the exact requested relation cannot be decided positively because the required source authority is absent.

## Matrix

| Source | DECODER_RUNTIME_TYPE__GOVERNED_KEY_NONINTERSECTION | LAWFUL_AUTHORITY_REPRESENTATION__CONSUMER_IGNORES_FORM | DYNAMIC_QUERY_REF__STATIC_CATALOG_ONLY_RESOLUTION | I05_FACT_EXISTS__POSTCONSUMER_PREIMAGE_MISSING | HISTORICAL_FILE__AMBIENT_CURRENT_DEPENDENCY | HISTORICAL_SUCCESSOR__RUNTIME_CATALOG_SCOPE_NOT_ENFORCED | SOURCE_SPECIFIC_TERMINAL_DOMAIN__GENERIC_FIELD_SUBSTITUTION | RISK_SET_DECLARED__MEMBERSHIP_PREIMAGE_UNAVAILABLE | QUESTION_VALUE_BINDING__EXACT_RESPONSE_REF_UNAVAILABLE | CURRENT_PRODUCT_SHAPE_MATCHES__SUBSTANTIVE_PRIOR_TRUTH_NOT_PROVED |
|---|---|---|---|---|---|---|---|---|---|---|
| GSS 1972 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW |
| GSS 1973 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW |
| GSS 1984 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | UNKNOWN_REQUIRED_AUTHORITY_ABSENT | UNKNOWN_REQUIRED_AUTHORITY_ABSENT | APPLICABLE_NOW |
| Afrobarometer R1 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW |
| Afrobarometer R5 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | UNKNOWN_REQUIRED_AUTHORITY_ABSENT | UNKNOWN_REQUIRED_AUTHORITY_ABSENT | APPLICABLE_NOW |
| Afrobarometer R9 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | UNKNOWN_REQUIRED_AUTHORITY_ABSENT | APPLICABLE_NOW |
| Latinobarometro 1995 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW |
| EVS 1981 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW |
| EVS 1990 | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_ONLY_AFTER_RUNTIME_PACKAGING | APPLICABLE_NOW |

## Failure-class holdings

### DECODER_RUNTIME_TYPE__GOVERNED_KEY_NONINTERSECTION

Every future package is exposed because PRE553 physical binding keys include the R5 type lane. A rule authored from a Python `int` cannot be assumed to intersect a decoder-returned `float64_finite` key merely because the displayed number is equal.

Required package law:

`decoder representation authority -> R5 typed physical key -> governed rule key`.

No magnitude-only repair.

### LAWFUL_AUTHORITY_REPRESENTATION__CONSUMER_IGNORES_FORM

Every package must prove not merely that an authority object exists, but that the consumer reads the exact representation-form field that makes the authority lawful.

The hostile mutation is:

- preserve the authority hash/ref;
- alter or omit the required representation form at the consumer seam;
- demand rejection.

This is representation-form law, not GSS questionnaire-form law.

### DYNAMIC_QUERY_REF__STATIC_CATALOG_ONLY_RESOLUTION

Exact I05 can generate derived predicates and query specs after the pre-search catalog is frozen.

A later consumer that resolves only the initial static catalog can therefore fail even though I05 itself executed lawfully.

Required closure:

- retain generated object preimages; or
- retain deterministic reconstruction material sufficient to reproduce the exact object/ref;
- prove the post-consumer resolves that dynamic object rather than searching only the static catalog.

### I05_FACT_EXISTS__POSTCONSUMER_PREIMAGE_MISSING

An exact fact ref is not enough.

The post-I05 handoff must retain the actual EmpiricalFact preimage, including its typed state, authority refs, dependency refs, source/release refs and replay root.

The hostile case is a valid I05 receipt whose fact ref survives while the fact object does not.

Required result: fail closed.

### HISTORICAL_FILE__AMBIENT_CURRENT_DEPENDENCY

All audited sources are historical products. Several accepted packets lawfully use later/current documentation only at a delimited scope.

A runtime must never resolve an unpinned "current" document or package at execution time and silently let it govern the historical source.

Concrete audit examples without importing any outside semantics:

- GSS 1972/1973 explicitly distinguish later current producer weight guidance from original historical source operation;
- Latinobarómetro 1995 explicitly separates later archive update notices/current ODA behavior from the missing 1995 WT/Brazil authority;
- all packets forbid importing neighboring-wave semantics merely because the present product looks similar.

### HISTORICAL_SUCCESSOR__RUNTIME_CATALOG_SCOPE_NOT_ENFORCED

A successor/current authority may be valid yet valid only for a named historical relation.

The runtime catalog must freeze:

- the exact successor object;
- the historical source/release it may govern;
- the specific operation/relation;
- negative limits.

A valid successor outside that frozen scope is not eligible merely because it is newer.

### SOURCE_SPECIFIC_TERMINAL_DOMAIN__GENERIC_FIELD_SUBSTITUTION

This is already applicable at the source-contract grain.

The audited estate contains noninterchangeable states such as:

- documented not-administered / routed-skip / substantive nonresponse / physical missing;
- unsupported / not applicable / bounded UNKNOWN;
- ordinary stored value with documentary "missing" meaning;
- opaque administrative field;
- all-user-missing but physically existing variable;
- source-local coordinate/weight carrier with no analytical default.

A generic terminal must carry these exact distinctions rather than substituting one generic missing/status field.

### RISK_SET_DECLARED__MEMBERSHIP_PREIMAGE_UNAVAILABLE

A future runtime `risk_set_ref` is lawful only if exact membership can be replayed.

Specific authority limits:

- GSS 1984 still lacks exhaustive variable×form/module routing membership;
- Afrobarometer R5 still lacks exact authority for several administrative route carriers.

Those cells are `UNKNOWN_REQUIRED_AUTHORITY_ABSENT`, not runtime defects.

For the other sources, membership preimages become a live failure question only after a package declares the risk set.

### QUESTION_VALUE_BINDING__EXACT_RESPONSE_REF_UNAVAILABLE

A source code/dictionary statement must be materialized into an exact runtime response binding before PRE553 can consume it.

Authority-blocked examples:

- Afrobarometer R5 `Q47C=997`;
- Afrobarometer R9 `Q118_11` producer binding;
- GSS 1984 exhaustive response/routing surfaces when the needed exact source mapping is not in the banked packet.

No neighbor-code, name, label, or distribution inference may manufacture the missing exact ref.

### CURRENT_PRODUCT_SHAPE_MATCHES__SUBSTANTIVE_PRIOR_TRUTH_NOT_PROVED

This class is applicable now to every historical source.

Matching current shape, field name, role, label, suffix, or downstream schema is corroborative at most. It does not prove the historical substantive relation.

Banked residuals already embody this law:

- Afrobarometer R9 role-compatible/current-like weight shapes do not close exact producer aliases;
- Latinobarómetro current ODA weighting behavior does not close 1995 WT semantics;
- GSS/EVS neighboring/current release conventions do not govern earlier releases absent exact authority.

## Cross-wave holding

No failure class above authorizes importing a WVS7 or LiTS-I substantive answer.

The transferable object is only the question:

> does the source/runtime path preserve the exact representation, provenance, membership, response binding, catalog scope, generated preimage and terminal domain required by its own authority?

If the answer depends on missing source authority, the result remains UNKNOWN/AUTHORITY_BLOCKED. If it depends on absent runtime plumbing, the result remains a runtime/source-free gate rather than a source defect.
