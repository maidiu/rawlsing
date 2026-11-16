# Canonical retained-object inventory

This is the source-free-qualified inventory contract. Counts that are fixed by the current frontier are asserted here; other public-object-family counts are recorded exactly by the fresh checkpoint's own `inventory` map rather than guessed before source-backed materialization.

| Object / material | Required retention | Source-free-fixed count/status |
|---|---|---:|
| `EmpiricalFact@1.0.0` | complete canonical preimage | **60** |
| `DiscoveryResultReceipt@1.0.0` | complete canonical preimage | **50** |
| `EmpiricalQuerySpec@1.0.0` | every exact role-referenced current query | exact count recorded by checkpoint |
| `EmpiricalPredicate@1.0.0` | every exact role/query-referenced current predicate | exact count recorded by checkpoint |
| `DiscoveryAuthority@1.0.0` | current exact bounded discovery authority | retained |
| `AuthoritySnapshot@1.0.0` | all runtime/retained-object authority snapshots plus representation authority snapshot | exact count recorded by checkpoint |
| `EmpiricalUniverse@1.0.0` | current sealed-release universe support object(s) | retained |
| `SourceUniverseRelation@1.0.0` | current sealed-release relation support objects where present | exact count recorded by checkpoint |
| `StructuralEmpiricalAdmission@1.0.0` | forbidden in this closure | **0** |
| C11 logical release identity | exact release/source/release-manifest hashes | retained |
| C11 `ReplayManifest` | complete internal replay preimage + exact ref | retained |
| representation authority material | exact bounded q301 DTA representation authority | retained |
| candidate frontier | exact current candidates | **50** |
| role bindings | exact candidate role→predicate/query bindings | **77** |
| compact constituent-I03 fact manifest | exact fact refs + typed states for standard oracle comparison | **60 facts** |
| canonical fact fragments | lossless hash-verified deduplicated identity material | exact count recorded by checkpoint |

## Fact fields conserved

Because the complete canonical fact preimage is rehydrated, conservation includes all identity-bearing fields, including as applicable:

- complete cell semantic projection;
- raw numerator support;
- raw denominator support;
- raw resolved target support;
- weighted support fields;
- uncertainty state;
- target topology;
- target-domain identity;
- response-state semantics;
- risk-set identity and exact member refs;
- denominator member refs;
- empirical universe/source provenance refs;
- authority snapshot refs;
- dependency refs;
- producer replay root;
- I03 replay ref;
- execution contract/detail fields.

## Query/predicate conservation

Complete query preimages preserve target refs/order, target topology, condition predicate, risk set, source/universe scope, measure basis, requested output grain, authorities, dependencies and replay root.

Complete predicate preimages preserve canonical predicate AST/hash, exact coordinate/question/value refs, risk/scope refs, same-respondent semantics, operator semantics, authority/dependency closure and replay root.

The 77 compact role bindings are checked against the retained canonical `DiscoveryResultReceipt` identities, preventing predicate/query substitution.
