# DR-R02 — REFERENCE CLOSURE MINIMALITY

## 1. Governing rule

Downstream semantic objects must retain enough exact reference closure to recover their governing evidence and authority without copying upstream semantic payloads into every stage.

R02 distinguishes five roles:

- `DIRECT_SEMANTIC_INPUT`
- `PRESERVE_BY_REFERENCE`
- `TRANSITIVELY_DEREFERENCEABLE`
- `AUDIT_ONLY`
- `MUST_NOT_APPEAR`

The default is the least repetitive role that still preserves deterministic interpretation and replay.

## 2. Core theorem

A downstream object does not need a physical copy of every upstream identity if its immutable reference graph can recover them exactly.

Therefore, for example:

```text
V556 F1/F2
-> V555 route
-> V554 affordance
-> StructuralEmpiricalAdmission or V553 temporal basis
-> StructuralEmpiricalAdmission
-> EmpiricalFact
-> EmpiricalQuerySpec / EmpiricalUniverse / measure / authority / replay
```

is sufficient exact provenance closure **provided** every locator is immutable/content-addressed and the standalone V558 repository can resolve the chain with raw producer directories absent.

Consequently a V556 row does not need to physically copy `EmpiricalQuerySpec` fields, weight fields, source labels and admission text merely for debugging convenience.

## 3. V553

### DIRECT_SEMANTIC_INPUT

V553 needs:

- the `StructuralEmpiricalAdmission` identity;
- structural target/relation/direction/use refs required by its temporal operation;
- source/time/native-scope identity required for comparability;
- V553 temporal/comparability authority.

### PRESERVE_BY_REFERENCE

- admission authority identity;
- exact upstream structural reference set where semantically relevant.

### TRANSITIVELY_DEREFERENCEABLE

By default:

- `EmpiricalFact` payload;
- `EmpiricalQuerySpec` AST;
- `EmpiricalUniverse` full manifest;
- weight/measure design details;
- source-normalization authority;
- discovery receipt;
- replay receipt payload.

V553 may dereference any of these when validation requires them. It need not duplicate them into every temporal object.

## 4. V554

V554 direct semantic input is one exact basis object selected by the rule:

- direct `StructuralEmpiricalAdmission`; or
- V553 temporal object.

V554 must preserve the producer basis ID and exact V554 rule/condition identities.

Upstream empirical query/universe/measure/replay identity is normally `TRANSITIVELY_DEREFERENCEABLE` through the basis object. A V554 rule may require a particular support, uncertainty or source property; even then V554 may dereference the authoritative upstream object rather than copy a second authority value.

## 5. V555

Direct semantic input:

- exactly one V554 F1 affordance per route;
- exact V555 route rule;
- mediator/channel structural role;
- receiver constraint.

Preserve by reference:

- inherited V554 F2 IDs;
- any exact V554/V553 producer IDs needed by the route rule.

Transitive reference is sufficient by default for:

- StructuralEmpiricalAdmission;
- EmpiricalFact;
- EmpiricalQuerySpec;
- EmpiricalUniverse;
- weight/measure basis;
- DiscoveryResultReceipt;
- ReplayReceipt.

V555 must not copy an inherited V554 applicability condition and rename it as a route-born condition.

## 6. V556

Direct semantic input:

- V555 route IDs as base-edge identities;
- exact participant roles/order/cardinality;
- governed V556 rule;
- V555 route-condition/effect refs when the V556 rule explicitly uses them.

By default the entire empirical provenance stack is transitively reachable through route -> affordance -> basis.

Thus:

`V556 does not need a physically copied EmpiricalQuerySpec ID merely because that query ultimately supports one participant route.`

A direct locator may be indexed operationally for performance, but it remains a nonsemantic alias and cannot become a second provenance authority.

## 7. V557

V557's unique obligation is runtime publication/use governance plus referential-closure proof.

It therefore must register or be able to traverse every producer locator needed to interpret a runtime-published object.

It does **not** need to mint new V557 semantic objects for:

- StructuralEmpiricalAdmission;
- EmpiricalFact;
- EmpiricalQuerySpec;
- EmpiricalUniverse;
- DiscoveryResultReceipt;
- ReplayReceipt;
- admission/query authority snapshots.

V557 may create runtime-authorized locator/manifest records pointing to those producer-owned identities. Those records govern publication/use, not the meaning of the referenced object.

## 8. V558

A standalone `StructuralPriorRepository` must contain immutable producer material or content-addressed closure sufficient to dereference all required semantics after raw stage directories are absent.

This can require physically packaging referenced producer objects or content-addressed blobs. Physical inclusion does not imply semantic reownership.

V558 may build indexes over:

- producer object IDs;
- structural position/stratum/geography/time locators;
- negative-authority locators;
- provenance/authority locators.

Indexes are lookup structures, not new semantic copies.

`PositionedSubjectEmpiricalPossibilityField` remains `MUST_NOT_APPEAR` as a structural repository prior.

## 9. Reference-class rulings

### Source/universe identity

Structural stages need exact source/universe identity reachable. Direct physical repetition at every stage is unnecessary unless a stage rule uses it as part of its own semantic key.

Default: `TRANSITIVELY_DEREFERENCEABLE` after the first producer basis.

### Query identity

Exact query identity must be recoverable for admitted empirical structural evidence.

Default after admission: `TRANSITIVELY_DEREFERENCEABLE`.

### Admission authority

Direct at the admission object; later structural stages preserve basis/admission locator and may dereference authority.

Default later: `PRESERVE_BY_REFERENCE` or transitive closure, not copied rule text.

### ReplayReceipt

`AUDIT_ONLY` / replay locator. It is not a runtime structural prior.

### Weight/measure basis

Empirical query/admission authority must preserve it. Later stages receive support/uncertainty semantics relevant to their own rules and can dereference exact measure provenance.

Default later: `TRANSITIVELY_DEREFERENCEABLE`.

### DiscoveryResultReceipt

No generic runtime role. When a structurally admitted fact originated in autonomous discovery, the receipt may remain provenance behind the admission/fact.

Default: `AUDIT_ONLY` / authoring provenance.

### ActorComparatorReceipt

No structural-lane role. In the reverse lane it is consumed by possibility production and then remains transitively reachable behind PSEPF.

Default in V3: `TRANSITIVELY_DEREFERENCEABLE`, not direct runtime prior.

## 10. Provenance starvation test

Transitive closure is insufficient if any of the following occurs:

- an intermediate locator is mutable or nonunique;
- a required historical authority version cannot be dereferenced;
- source/universe identity is lost or reconstructed from labels;
- the standalone repository omits referenced producer material;
- a consumer must parse descriptive text to recover identity;
- a later stage silently substitutes a new authority version;
- negative/noncomparability state is not preserved.

Any such case must be hardened at stage close-read.

## 11. No-debugging-duplication law

Human convenience is not semantic authority.

A field may be duplicated into an operational index or diagnostic view, but:

1. the canonical producer reference remains authoritative;
2. the copy is nonsemantic;
3. mismatch fails closed;
4. the copy may be regenerated or removed without information loss.

## 12. Final ruling

The minimal downstream provenance topology is a **content-addressed transitive reference graph**, not a flat repeated provenance record on every object.

Each stage directly owns only its new semantic identity and the exact refs needed to bind that identity. Everything else remains reachable through immutable producer closure.
