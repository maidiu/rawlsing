# CLOSED35-R2-GSS1984 — Realization Contract

Schema:

`CLOSED35_GSS1984_SEMANTIC_REALIZATION@1.0.0`

Semantic owner:

`GSS1984_SEMANTIC_OWNER_V1`

## 1. Purpose

This contract is the single candidate-neutral semantic owner for the exact canonical GSS1984 source.

It consumes governed physical incidence and accepted documentary authority. It does not decode the SAV, infer semantics from raw values, or manufacture unresolved routing/weight/longitudinal claims.

All A/B/C candidates must consume the same owner surface.

## 2. Immutable source binding

```text
family              = GSS
release             = 1984
canonical_filename  = GSS1984.sav
canonical_sha256    = 1da2df0c0e0692817081a46856deeaa6c78891101e53cf0139a971de16f7ac18
source_format       = SAV
reader_mode         = SAV_NATIVE_GOVERNED
authority72_class   = L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED
edge_classes        = [EC01, EC09, EC10, EC12, EC14]
```

Any filename, cumulative derivative, different release, or same-looking carrier is a different source until the generic parentage/equivalence court proves otherwise.

## 3. Authority ceiling

This owner may realize only facts already accepted by the GSS1984 packet:

- three-form topology;
- distinct main / MAS / SAQ instrument surfaces;
- ordered household-slot topology;
- source-local `FORM`, `FORMWT`, `VPSU`, and `VSTRAT` carrier preservation;
- replay identity from source SHA + row ordinal;
- bounded UNKNOWN for unmapped routing, analytical weight/design use, longitudinal equivalence, and stronger native-ID claims.

It may not turn a bounded UNKNOWN into a positive claim by analogy to another GSS year.

## 4. Replay and native identity

Canonical hard replay identity:

`source_sha256 + zero_based_source_row_ordinal`

Native `id`:

`SOURCE_LOCAL_ATTRIBUTE_CHECK_ONLY`

Allowed:

- preserve the exact physical `id` value when supplied by governed physical incidence;
- use it for source-local audit checks;
- retain the accepted fact that stronger cross-release identity authority is absent.

Forbidden:

- cross-release respondent joins;
- deduplication or row replacement using `id`;
- treating `id` as longitudinal person identity;
- using native `id` instead of the hard replay key.

Unknown state:

`BOUNDED_UNKNOWN__NATIVE_ID_SCOPE_BEYOND_EXACT_SNAPSHOT`

## 5. Form owner

The source-native form coordinate is `FORM`.

The accepted 1984 documentary surface establishes three distinct form identities:

- `FORM_X`
- `FORM_Y`
- `FORM_Z`

The owner must preserve the exact source form value and its governed documentary identity where available.

This contract does not manufacture a full numeric form map from browser-visible fixture fragments.

For each source variable, form membership is one of:

- `FORM_X_ONLY_DOCUMENTED`
- `FORM_Y_ONLY_DOCUMENTED`
- `FORM_Z_ONLY_DOCUMENTED`
- `MULTIFORM_DOCUMENTED`
- `BOUNDED_UNKNOWN__VARIABLE_FORM_MEMBERSHIP_UNMAPPED`

A missing cell cannot decide form membership.

A neighboring GSS release cannot decide form membership.

## 6. Module owner

Module identity is separate from form identity.

Allowed module identities:

- `MAIN_QUESTIONNAIRE`
- `MAS`
- `SAQ`
- `BOUNDED_UNKNOWN__MODULE_MEMBERSHIP_UNMAPPED`

The owner preserves MAS and SAQ as distinct source-native instrument surfaces.

Forbidden:

- `MAS == SAQ`;
- `MAS == MAIN`;
- `SAQ == MAIN`;
- deriving module membership from missingness;
- importing later ISSP, ballot, version, phase, or GSS Next structure into 1984.

Form and module may co-exist as coordinates; neither is silently substituted for the other.

## 7. Ordered household occurrence owner

The accepted 1984 source packet gives an exact hostile family:

`where1 .. where14`

Required semantic occurrence rank:

`1 .. 14`

Accepted physical column adjacency for this family is lexicographic:

`where1, where10, where11, where12, where13, where14, where2, ... where9`

Owner representation:

```text
HouseholdOccurrence
  family = where
  source_variable_identity
  occurrence_rank ∈ {1..14}
  source_physical_ordinal
  raw_physical_state
  raw_value_if_observed
  documentary_route_state
```

The occurrence rank comes from the exact governed slot identity, not from physical adjacency.

Candidates may store the occurrences differently. They may not reorder, deduplicate, flatten, or treat equal values as one occurrence.

This law is bounded to the accepted `where1..where14` GSS1984 family. It is not a generic rule for every numbered GSS variable.

## 8. Missing-state and routing separation

The owner keeps physical state and semantic applicability distinct.

Physical/source state may include:

- observed stored value;
- system missing;
- SPSS user-missing value/range;
- source value label such as IAP where physically/documentarily present.

Semantic routing/applicability may include:

- `ELIGIBLE_DOCUMENTED`
- `FORM_NOT_ADMINISTERED_DOCUMENTED`
- `MODULE_NOT_ADMINISTERED_DOCUMENTED`
- `ROUTED_SKIP_DOCUMENTED`
- `NOT_ASKED_DOCUMENTED`
- `BOUNDED_UNKNOWN__ROUTING_APPLICABILITY_UNMAPPED`

Rule:

`physical missingness -/-> routing/applicability`

A physical IAP/user-missing/system-missing state is preserved even when documentary route authority is unavailable. It is not promoted to a route state by label or incidence alone.

If documentary routing conflicts with an observed raw value, both survive and the later court must expose the contradiction rather than rewrite source truth.

## 9. Weight/design owner

The source-specific physical/source-authority surface includes:

- `FORMWT`
- `VPSU`
- `VSTRAT`

The owner preserves each carrier independently with its raw physical state and source identity.

Default analytical selector:

`NONE_AUTHORIZED_BY_THIS_REALIZATION`

Analytical weight/design state absent an exact governed use binding:

`BOUNDED_UNKNOWN__WEIGHT_DESIGN_USE_UNMAPPED`

Forbidden inferences from carrier names alone:

- `FORMWT` is the universal or default person weight;
- `FORMWT` defines an estimand;
- `VPSU` + `VSTRAT` automatically authorize a particular variance estimator;
- a carrier can be discarded because another looks more modern;
- a missing carrier implies simple random sampling;
- another GSS release supplies the missing analytical design law.

The later analytical caller must provide separately governed estimand/use authority or fail closed for weighted/design claims.

Raw or non-generalizing descriptive use may preserve all carriers without selecting one.

## 10. Longitudinal boundary

No cross-release equivalence is asserted for:

- native respondent identity;
- recurring variable names;
- value dictionaries;
- forms;
- modules;
- routing;
- weights;
- design variables.

Default state:

`BOUNDED_UNKNOWN__CROSS_RELEASE_EQUIVALENCE_UNMAPPED`

An exact future crosswalk may replace that state for a named relation only.

## 11. Candidate neutrality

The semantic preimage is exactly:

```text
canonical source identity
+ governed physical incidence
+ GSS1984_SEMANTIC_OWNER_V1
+ exact documentary bindings actually available
+ declared downstream analytical intent where required
```

Candidate identity is forbidden from the semantic preimage.

For equal governed inputs, A/B/C must emit the same:

- form identity;
- module identity;
- occurrence rank;
- route/applicability state;
- bounded UNKNOWN state;
- weight/design authority state;
- replay identity;
- cross-release support/rejection state.

## 12. S35/R35 composition

Applicable S35 classes:

- `EC01 FORMAT_FAMILY_SAV_DTA`
- `EC09 ORDERED_REPEATED_SLOT_TOPOLOGY`
- `EC10 FORM_MODULE_SKIP_ROUTING_CARRIERS`
- `EC12 WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN`
- `EC14 COMPOUND_EDGE_INTERACTION_COURT`

Required later R35 hooks:

- `R35_I01_PHYSICAL_METADATA_RECEIPT`
- `R35_I02_VERIFIED_DERIVATIVE_PARENTAGE_TO_CANONICAL_SHA` when a candidate is not direct from the canonical source
- `R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE` across all applicable edge dimensions

This owner adds no source-specific physical decoder or adapter.

## 13. Qualification boundary

Implementation of this contract does not prove:

- the canonical SAV was opened;
- row-level source processing occurred;
- the whole source is physically equivalent across A/B/C;
- A/B/C were executed;
- I05 passed;
- measured P2X occurred;
- unresolved L1 semantics were closed.

The later qualification court must prove the physical receipts first and then test all candidates against this immutable semantic owner.
