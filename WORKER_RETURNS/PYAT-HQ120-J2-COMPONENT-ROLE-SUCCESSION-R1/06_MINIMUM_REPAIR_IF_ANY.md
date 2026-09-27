# PYAT HQ120-J2 — MINIMUM REPAIR IF ANY

J2 makes no production change.

This is the smallest repair shape supported by the evidence if HQ elects to close the two role-succession gaps.

## 1. Do not add a new giant carrier

The common component-vector receipt already supplies:

- exact subject/dimension identity;
- complete governed component set;
- exact component refs;
- authority state/value binding;
- negative refs;
- replay/proof hashes.

Reuse it.

## 2. Add one exact role-succession binding/producer

Create a narrow current contract whose job is only:

```text
EXACT CURRENT COMPONENT SET
+ EXACT FAMILY-ROLE AUTHORITY
+ EXACT HISTORICAL/CURRENT ROLE MAPPING
-> EXACT FAMILY_ITEM_ROLE COMPONENT VECTOR
```

Required invariants:

- role value cannot be inferred from ordinal, filename, variable name, target label or historical proximity;
- every governed component has either one exact role value or an exact typed negative/unresolved state;
- role value is bound through `authoritative_value_digest`;
- role authority is bound through `value_authority_ref`;
- the exact historical authority/mapping ref is in replay/dependency closure;
- unknown role stays unresolved.

The existing `ComponentAuthorityBinding.role` field may carry a stable participant descriptor, but should not be treated as the role authority itself.

## 3. Bind the certification act to M1

Install one exact M1 family-rule binding and validator for the relevant current learned joint-evidence family.

The rule must state whether the current semantics:

A. preserve the historical contribution vocabulary exactly; or
B. replace it with an explicit successor vocabulary and a total authority-bound mapping.

The validator must consume exact component/evidence prerequisites and make no role inference by adjacency or string resemblance.

At minimum hostile cases must cover:

- relation-bearing matched component;
- matched context component;
- special/missing component;
- governed nonrelation/context component;
- ambiguous match;
- unresolved match;
- one relation component only;
- two relation components;
- relation + context;
- negative/blocked authority;
- changed family-role authority.

## 4. Preserve contribution determinant exactly

Two minimal lawful representations are possible.

### Option A — second component-vector receipt

Emit a second `ComponentAuthorityVectorReceipt` whose authority dimension is:

`COMPONENT_CERTIFICATION_CONTRIBUTION`.

This is preferable if later consumers need independent exact dereference of the per-component contribution vector.

### Option B — M1 determinant-only preservation

If contribution is used only internally to the family certification decision, the M1 validator may freeze the exact ordered per-component classification inside its determinant/explanation material, with exact component refs and authority inputs.

This option is lawful only if:

- the contribution vector is fully reconstructable from the frozen determinant;
- no later consumer contract requires an independently resolvable contribution object;
- replay proves the same decision and same vector;
- the field retirement is explicitly banked.

## 5. M1 prerequisite transport

The current M1 bundle's generic `additional_dependency_refs` is insufficient by itself because it preserves reachability but not semantic interpretation.

Prefer a named `M1PrerequisiteChannel` for the role-vector premise, carrying:

- exact channel kind;
- SATISFIED/BLOCKED/UNRESOLVED state;
- exact role authority refs;
- exact component-vector dependency ref;
- exact contract/version identity in detail;
- no fuzzy/current-by-chronology selection.

The family validator must validate the exact premise rather than merely checking a dependency exists.

If this cannot be done unambiguously with the current channel contract, then and only then add the smallest typed role-vector input field/catalog to M1.

## 6. Consumer proof

The closing court must identify the actual consumer.

For certification contribution, the natural current consumer is the exact M1 family validator.

For family-item role, acceptable consumers are:

- that same M1 validator; or
- an earlier exact current semantic projection/target-resolution owner if HQ proves the family-role function is fully consumed there.

No PASS from a dormant receipt with no consumer.

## 7. No B5 change

Do not put component certification contribution into B5 lifecycle merely because the historical word is “certification.”

The historical function is evidence-role adjudication.

## 8. Required closure receipt

A repair court should return a table with, per historical role function:

```text
historical function
historical authority ref
current role dimension/rule ref
mapping authority ref
producer ref
consumer ref
negative-state mapping
replay ref
same-grain disposition
```

PASS only if all role functions are exact-current or explicitly retired at the same semantic grain.
