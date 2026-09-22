# Runtime Package Admission Gaps

## 1. Generic admission gate

No audited source currently has a source-specific PRE553 runtime package comparable in function to the current exact runtime-package machinery.

That absence is not a defect. It means the following preimages must be frozen before any later source execution can claim runtime admission.

### A. Exact physical representation binding

The current generic facade computes a physical binding key from:

`R5_TYPED(raw_value) + physical_missing_state + source_missing_declaration`.

Future packages must therefore freeze:

1. canonical source SHA and source format;
2. exact reader/config identity;
3. decoder representation authority for every governed key lane;
4. R5 codec version;
5. the exact representation-preserving construction of response/coordinate/weight `physical_key` values.

Numeric magnitude equality is insufficient. `1` and `1.0` are distinct typed keys unless an independently authorized representation transform says otherwise.

A package that writes governed rules from convenient Python literals without proving they are the decoder's lawful representation is not admitted.

### B. Physical-state preservation

The runtime package must carry physical state independently from documentary semantics:

- system missing;
- source/format user-missing discrete values;
- user-missing ranges;
- extended missing where applicable;
- ordinary stored semantic-looking codes;
- source-cell absence/unrepresented state where applicable.

A label such as "missing", "not applicable", "not asked", or "refused" does not itself rewrite the physical class.

### C. Producer-to-C11 owner contract

For every projected slot, the package must freeze the exact producer-owned interpretation surface consumed by PRE553:

- response owner;
- coordinate owner;
- weight owner;
- occurrence/topology owner;
- routing/applicability owner;
- source-local coordinate owner;
- explicit negative/unsupported/UNKNOWN state.

No candidate may manufacture these during execution.

### D. Historical/current dependency closure

Every authority that comes from a later/current producer document and is applied to a historical file must be represented as an exact dependency with scope and effective provenance.

"Current guidance says X" is not enough to prove "the historical producer state was X".

The package must distinguish:

- historical source fact;
- later/current successor authority;
- exact scope in which that successor is allowed to govern;
- negative limits on retrojection.

### E. Risk-set membership preimage

Any `risk_set_ref` used by a predicate/query/discovery authority must have replayable membership authority.

A ref without a membership preimage is insufficient.

Membership must be reconstructible from:

- source replay identity;
- exact route/form/module/country predicates where applicable;
- the frozen producer authority owning those predicates;
- explicit UNKNOWN where membership cannot lawfully be decided.

### F. Exact question/value to response-value binding

A runtime response rule needs an exact `physical_key` and source-authorized response state.

Where the source package contains only a documentary statement, the runtime package must materialize the exact question/value binding into an exact runtime object/ref. It may not substitute:

- neighboring variable dictionaries;
- same numeric code in another question;
- current-wave aliases;
- label similarity;
- value-frequency patterns.

### G. Frozen runtime object catalog

The package must contain full exact preimages, not only hashes/refs, for the adopted runtime objects required before discovery:

- authorities;
- predicates;
- query templates;
- discovery authority/frontier;
- source universe;
- risk set;
- measure basis;
- replay/currentness binding.

The frozen catalog must also bind the source SHA and prohibit ambient "latest" resolution.

### H. Dynamic I05 preimage retention

Static pre-search catalogs are insufficient for dynamically generated I05 objects.

The downstream handoff must retain or deterministically reconstruct the exact preimages of:

- generated predicates;
- generated query specs / query roles;
- empirical facts;
- discovery receipts;
- evaluated frontier;
- replay/dependency closure.

A post-I05 ref that cannot be resolved to its exact object preimage is a terminal integration failure even when I05 itself produced the ref lawfully.

### I. Terminal consumer compatibility

A post-I05 consumer must accept the actual source-specific terminal/state domain without replacing it with a generic field or weaker state.

Required hostile handling includes:

- not-administered versus routed skip versus substantive nonresponse versus physical missing;
- unsupported versus not-applicable versus bounded UNKNOWN;
- opaque administrative carrier versus authorized route owner;
- all-user-missing physical variable versus nonexistent variable;
- source-local coordinate versus harmonized coordinate;
- source-local weight carrier versus selected analytical weight.

### J. Whole-source physical edge receipt

The runtime package may declare the required S35/R35 edge scope, but it cannot issue the physical PASS.

Later authorized source execution must prove whole-source preservation at the exact edge scope.

## 2. Source-specific admission gaps

| Source | Runtime-package admission state | Required before runtime admission |
|---|---|---|
| GSS 1972 | READY FOR PACKAGE | Bind exact decoder→R5 representation; materialize questionnaire routing/occurrence owners and exact runtime refs; preserve Q25 not-asked and route-unresolved states; pin later WTSSPS guidance as later/current provenance; represent modern variance as unsupported rather than missing. |
| GSS 1973 | READY FOR PACKAGE WITH BOUNDED UNKNOWN | Bind exact X/Y FORM representation, Appendix-P membership and CLASS/CLASSY dictionaries; retain FORM_NOT_ADMINISTERED precedence; keep Q105 card/form relation and exact birth-year route nonexecutable until authority exists; do not synthesize WTSSPS if absent. |
| GSS 1984 | READY FOR PACKAGE WITH BOUNDED UNKNOWN | Freeze X/Y/Z + MAIN/MAS/SAQ + where-slot topology; package only exact variable-form/module/routing bindings actually authorized; preserve unmapped membership and weight/design use as bounded UNKNOWN; no name-based design semantics. |
| Afrobarometer R1 | READY FOR PACKAGE WITH BOUNDED UNKNOWN | Preserve REFNUMB/CASENUMB/RESPNUMB separation, source-local COUNTRY, SUPDEM ordinary-storage/documentary-state split, all five weight roles and no default selector; package per-variable national variants only where exact authority exists. |
| EVS 1981 | READY FOR PACKAGE WITH BOUNDED UNKNOWN | Pin Windows-1252 reader condition; bind v308 declared user-missing range + positive code 3 physically without inventing its reason; preserve ranked slots/coordinates; keep native-ID, weight-estimand and cross-release coordinate relations unknown. |
| EVS 1990 | READY FOR PACKAGE WITH BOUNDED UNKNOWN | Pin Windows-1252 reader condition; preserve q745 as an all-user-missing existing column with raw -5 witness; preserve both ranked triplets and split coordinates; retain weight_g and weight_s independently with no default/estimand inference. |
| Afrobarometer R5 | AUTHORITY BLOCKED FOR UNRESTRICTED PACKAGE | Do not bind Q47C 997 to a semantic state without new exact producer authority; do not use unresolved EAST.AFR/SOUTHERN/NORTH.AF aliases or R1.ONLY..R4.ONLY as route owners. A bounded opaque package is possible only if workload semantics do not require those assertions. |
| Afrobarometer R9 | AUTHORITY BLOCKED FOR UNRESTRICTED PACKAGE | Do not assign a producer semantic binding to Q118_11 or exact producer aliases/roles to V397_A/V399_A without new authority. Q78F country applicability may be used at its already-closed grain. |
| Latinobarómetro 1995 | AUTHORITY BLOCKED FOR UNRESTRICTED WEIGHTED PACKAGE | Preserve all canonical rows, ENC as non-key, WT as a carrier, and Brazil discrepancy provenance. No external raw weighted default, WT estimand/domain/normalization/calibration, or Brazil row repair is authorized. An unweighted/bounded package may be separately scoped. |

## 3. Source-free gap versus source authority

The following are generic/source-free until proved otherwise:

- consumer honors representation form;
- dynamic generated query/fact objects survive static-catalog boundaries;
- post-I05 consumer can resolve every fact/query preimage;
- generic terminal machinery does not substitute a weaker state domain.

The following remain source-specific:

- exact route/form/module membership;
- exact response dictionary binding;
- historical successor scope;
- source-local weight/ID/coordinate authority;
- residual producer aliases/codes.

A source-free repair cannot close a documentary UNKNOWN, and a documentary packet cannot substitute for the missing generic runtime handoff.
