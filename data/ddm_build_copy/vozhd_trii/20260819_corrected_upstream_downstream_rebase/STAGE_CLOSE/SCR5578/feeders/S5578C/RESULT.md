# S5578C — HOSTILE STANDALONE CLOSURE / LOCATOR / NEGATIVE-REFERENCE FEEDER

**Campaign:** `VOZHD_TRII_CORRECTED_UPSTREAM_DOWNSTREAM_REBASE`  
**Parent:** `SCR5578_PUBLICATION_REPOSITORY_RESOLUTION`  
**Later barriers:** M4 / M5  
**Repository:** `maidiu/rawlsing`  
**Exact launch base:** `baa257cb901ad8e5dc4d89faf2d81ea6f442ff8d`  
**Branch:** `agent/vozhd-trii-dr-r03-spec-v5578-standalone`  
**Write scope:** `data/ddm_build_copy/vozhd_trii/20260819_corrected_upstream_downstream_rebase/STAGE_CLOSE/SCR5578/feeders/S5578C/`  
**Authority:** `NON_DISPOSITIVE_FEEDER`  
**Production code modified:** `NO`  
**Broad DAG reopened:** `NO`  
**SCR5578/M4/M5 final authority claimed:** `NO`

## 1. Result

S5578C returns:

`S5578C_FEEDER_COMPLETE`

No parent-authority conflict and no broad-topology contradiction were found.

The hostile premise is confirmed:

> A reference-minimized V557/V558 bundle is semantically safe only if minimization removes **copies**, not **interpretation-critical dependency closure**. Every required positive, negative, permission, authority and relation dependency must either be packaged as immutable content or resolve through an exact immutable content-addressed/hash-bound locator contract. If an indispensable dependency is missing, mutable, ambiguous, hash/version-conflicting, role-corrupt, cardinality/order-corrupt, or forbidden by class/permission, the root/repository/query fails closed. V558 may verify, link and index; it may not repair meaning.

The exact closure proposal is in `REQUIRED_CLOSURE_MATRIX.csv`. Concrete breakage cases are in `BROKEN_REFERENCE_COUNTEREXAMPLES.csv`. Executable-style fixture specifications are in `HOSTILE_FIXTURES.md`.

## 2. Binding authority read

S5578C read and treated as binding/non-dispositive according to their status:

### Parent authorities

- `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/24_DR_R03_SYNTHESIS_RETURN_ADJUDICATION_AND_STAGE_CLOSE_GATE.md`
- `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/25_STAGE_CLOSE_READ_PARALLEL_COMMAND_AND_LAUNCH_AUTHORITY.md`

Parent 24 freezes the relevant broad law:

- S06: V557 runtime-use governance and V558 repository/resolution are logically distinct; repository presence does not grant permission.
- S07: reference minimization is lawful only under strict standalone dependency closure; missing/mutable/ambiguous/hash/version failures fail closed; provenance never grants composition authority.
- S08: source plurality and source-specific positive/negative/conflicting/noncomparable states remain first-class.
- S11: upstream structural/empirical prior references may not become downstream behavioral/persona authority.

### Accepted R03 synthesis

Read from accepted branch `agent/vozhd-trii-dr-r03-synthesis`:

- `R03/SYNTHESIS/RESULT.md` including S06-S08/S11;
- `R03/SYNTHESIS/FINAL_BROAD_DAG.md`;
- `R03/SYNTHESIS/WHOLE_MACHINE_CLOSURE_GATE.md`;
- `R03/SYNTHESIS/STAGE_CLOSE_READ_BURDEN_MATRIX.csv`;
- `R03/SYNTHESIS/STAGE_CLOSE_READ_CAMPAIGN.md`.

SCR5578's binding merge barrier is explicit: with raw producer directories absent, every interpretation-critical positive/negative dependency resolves exactly or fails closed; producer IDs/hashes remain canonical; permission monotonicity holds item-wise; PSEPF is rejected; resolver is deterministic and repository inclusion grants no permission.

### EP5578 exact evidence head

Read from exact head:

`f95f01f8112c646897058de809c98f5b3e8b429b`

including:

- `EVIDENCE_PACK.md`;
- `EVIDENCE_INDEX.csv`;
- `REFERENCE_CLASS_MATRIX.csv`;
- `IMPLEMENTATION_AUTHORITY_GAP_MATRIX.csv`.

EP5578 establishes that accepted architecture already requires standalone closure, producer-preserving locators, typed reference closure and deterministic resolution, while current legacy V557/V558 executable terrain does not demonstrate those contracts. It specifically records the current standalone closure as an implementation gap and role/order preservation as a live risk.

### Accepted hostile feeders

Read accepted heads from `R03/PARALLEL_RETURN_INDEX.json`:

- R03B `26a1710548385339bdcb4cbf32244550867c5e10`;
- R03C `fe6a33cf529039cca4fb6837a3e5d5feb1ab7fc3`;
- R03D `1a1898b8338733641731c95719e840c3707bcf99`;
- R03F `9f661931d51e03f137601b27eeaecf77ab11ad2f`.

Relevant adopted evidence:

- R03B: V557/V558 logical authorities survive even if physically co-packaged; V555 routes and mixed producer roots may publish directly without no-op filler stages.
- R03C: weak ID-chain provenance is insufficient; standalone closure must be role-preserving and materialized or hash-bound; historical authority/source-universe/query/measure/negative dependencies must remain exactly resolvable; ReplayReceipt stays audit-only.
- R03D: PSEPF structural publication, producer re-ID/reownership and permission/negative-authority leakage must fail closed.
- R03F: negative authority can be starved by positive-only packaging; provenance is not composition authority; source plurality and source-sensitive identity must survive.

### CAN-003 / CAN-004 / CAN-005

Read exact accepted authority:

- `CAN_003_V557_RUNTIME_USE/AUTHORITY.json`;
- `CAN_004_IMMUTABLE_PUBLICATION_REPOSITORY_BUNDLE/AUTHORITY.json`;
- `CAN_005_CONTEXT_RESOLVER_POLICY_BINDING/AUTHORITY.json`.

These authorities already supply the exact non-inventive ceiling needed for this feeder. S5578C proposes closure requirements and fixtures within that ceiling; it does not create a new semantic owner.

## 3. Core hostile ruling — copied field removal versus dependency removal

The safe optimization is:

```text
REMOVE repeated payload copies from V555/V556/V557/V558 rows
KEEP exact immutable semantic dependency graph
```

The unsafe optimization is:

```text
REMOVE copied payload
AND
replace exact dependency with only:
  an ID string,
  a display label,
  a mutable path,
  a current/latest registry lookup,
  an untyped provenance link,
  or an index row
```

The latter silently changes semantics because downstream can no longer prove what exact producer object, governing authority, role, scope, negative state or permission decision the root depended on.

S5578C therefore distinguishes four storage/reference classes:

1. `MUST_PACKAGE_ADMINISTRATIVE_INTEGRITY_OBJECT` — publication/repository manifests, locator registry, reference/closure graph, index manifests, CAN-003 governance records/collection manifests and their hashes.
2. `PACKAGE_OR_EXACT_IMMUTABLE_HASH_BOUND_RESOLVE` — producer semantic objects and interpretation-critical authorities/dependencies.
3. `AUDIT_ONLY_NONSEMANTIC` — replay/audit provenance that is retained for a governed audit claim but does not participate as semantic input, ranking, composition or permission.
4. `MUST_NOT_APPEAR_IN_STRUCTURAL_REPOSITORY_SEMANTIC_GRAPH` — PSEPF, ActorComparatorReceipt and V3EmpiricalPossibilityInput.

A hash string alone is not necessarily a satisfied closure leaf. If the consumer must dereference the object to interpret/replay it, the bundle must contain the bytes/material or an exact immutable resolution contract proving how that exact hash is resolved without latest/fuzzy/network/raw-stage substitution.

## 4. Required closure classes

### 4.1 Positive producer meaning

Every published root must preserve the canonical producer tuple:

```text
producer_family
producer_object_id
producer_object_hash
producer_build_id/hash
producer_schema_id/version
producer_rule/predicate/reference-contract ids/versions/hashes where applicable
producer semantic/epistemic state
producer permission ceiling
```

A V558 locator is administrative. It cannot replace this tuple.

### 4.2 Negative and limit meaning

Positive roots are not interpretable in isolation when their lawful use depends on negative/limit objects.

Required typed distinctions include, as applicable:

- producer `NEGATIVE_AUTHORITY` / exact subtype;
- `MISSING_AUTHORITY`;
- `NONCOMPARABLE`;
- governed `VALID_EMPTY` and exact subtype;
- V553 `TEMPORAL_LIMIT` / temporal noncomparability;
- V554 applicability denial/block/defer state;
- V555/V556 typed deny/valid-empty states;
- V557 `DENY_CAUSAL_USE` / `NOT_APPLICABLE`;
- packaging `INTEGRITY_FAILURE`.

These are noninterchangeable. Omitting a producer negative is not equivalent to no restriction. A broken locator is not producer missing authority. Empty index result is not producer valid-empty.

### 4.3 Authority dependencies

Historical meaning requires exact authority identity:

```text
authority_id + version + content_hash
```

plus packaged content or immutable resolution contract when interpretation requires dereference.

`latest/current/default` is never historical authority. Same logical rule name is insufficient. Unknown future versions are not compatible by family resemblance.

### 4.4 Role / order / cardinality / multiplicity

CAN-004 makes the semantic edge itself part of closure identity.

For every declared interpretation-critical reference the closure must bind:

```text
source_locator_ref
target_locator_ref
reference_contract_id/version/hash
edge_role
requiredness
participant_role
declared_cardinality
multiplicity_key
order_significant
semantic_ordinal
```

This is mandatory because identical target node sets can encode different semantics.

A V555 route must retain source/mediator/receiver identity/order. A V556 n-ary interaction must remain n-ary and role-qualified. Sorting locators is permitted for deterministic bytes only when producer authority says semantic order is irrelevant.

### 4.5 Source-universe / query / risk-set / measure dependencies

When corrected structural meaning descends from empirical admission, exact closure must preserve the interpretation-critical chain declared by the producer/reference contracts, which may include:

```text
StructuralEmpiricalAdmission
-> EmpiricalFact
-> EmpiricalQuerySpec
-> EmpiricalUniverse
-> exact risk-set/routing membership or deterministic rule
-> exact measure/weight/design/estimand authority
-> support/uncertainty/negative state
-> historical AuthoritySnapshot
-> exact C11 content/replay identity
```

These objects need not be copied onto every V555/V556 row. They may not disappear from closure when the root's meaning depends on them.

Source labels, identical respondent display IDs, equal scalar denominators, identical percentages or common query labels do not establish universe equivalence, respondent linkage, sample pooling or composition authority.

### 4.6 Source composition authority

When a producer/root actually claims a cross-source operation, closure must contain the exact operation-specific authority and participating universe identities.

S5578C preserves the distinction:

```text
SOURCE_SEMANTIC_EQUIVALENCE
!= RESPONDENT_IDENTITY_LINKAGE
!= SAMPLE_POOLING_AUTHORITY
!= CROSS_SOURCE_COMPOSITION_AUTHORITY
```

If no such positive authority exists, co-resolution/provenance reachability does not create one.

### 4.7 Permissions

Three permission layers remain separately bound:

```text
producer permission ceiling
-> V557 item/collection publication/use decision
-> resolver query-relative narrowing
```

Required invariant:

`resolver_allowed_uses ⊆ V557_allowed_uses ⊆ producer_allowed_uses`.

Repository membership, collection readiness, successful closure, an index hit or an active root never widens another object's permission.

Reference accessibility is not independent runtime-use permission.

## 5. Locator law

A lawful producer-preserving locator must bind enough material to reverse exactly to one authoritative producer tuple without text/fuzzy rematching.

The CAN-004 minimum includes:

- locator ID;
- logical collection kind;
- authoritative object ID/hash;
- authoritative producer family;
- authoritative build ID/hash;
- producer schema ID/version;
- producer rule/predicate/reference-contract bindings;
- V557 governance record ID/hash;
- content blob hash;
- storage locator;
- provenance locator.

S5578C adds no new locator semantics. It applies the accepted law hostilely:

- path-only locator fails standalone closure;
- mutable stage path fails replay;
- nonreversible locator fails producer ownership;
- multiple incompatible targets fail strong-reference law;
- locator ID never becomes structural semantic identity;
- index rows must dereference/reverify locator and producer object before selection.

## 6. Negative-reference theorem

A reference-minimized bundle is incorrect if it preserves every positive root but drops a negative object that can change interpretation or permission.

For each root, closure construction must therefore walk both positive and negative schema/reference-contract edges. The closure proof must answer:

> If this negative/limit/noncomparability/denial object were absent, could the root become eligible, selectable, composable, temporally supported, or causally usable when it should not?

If yes, the negative is interpretation-critical and must be packaged or exactly immutably resolvable.

This includes V553 temporal limits and producer noncomparability even when the final positive descendant is stored elsewhere.

## 7. Provenance is not composition

S5578C attacks a particularly dangerous reference-minimal implementation pattern:

```text
resolver can dereference A provenance
resolver can dereference B provenance
therefore resolver may combine A and B
```

The implication is invalid.

Transitive provenance answers **where meaning came from and under what authority**. Composition authority answers **whether multiple meanings may be jointly interpreted under a named operation**.

The closure graph must preserve both if both exist. It must never infer the latter from the former.

Likewise, ContextResolver may co-resolve separately authorized objects but may not create a V556 F1/F2 because participants share endpoint/time/geography/stratum/provenance or appear in one query.

## 8. PSEPF smuggling ruling

The corrected reference-class registry must reject structural registration of:

- `PositionedSubjectEmpiricalPossibilityField`;
- `ActorComparatorReceipt` as a structural prior;
- `V3EmpiricalPossibilityInput`.

A syntactically valid V557 governance record, generic-prior wrapper, V558 locator, opaque name or runtime permission cannot convert object ontology.

Structural repository admission must validate the authoritative producer class/owner, not the wrapper's display class.

Incidental audit/prose mentions must not become closure edges. A semantic closure walker follows only producer/reference-contract-declared interpretation-critical references. This both prevents PSEPF smuggling and prevents arbitrary provenance bloat.

## 9. Latest / fuzzy / repair ruling

When closure breaks, lawful behavior is not graceful semantic degradation.

Forbidden repair includes:

- raw producer-directory lookup;
- network/API lookup;
- mutable `latest` / `current` / `default`;
- nearest time or geography;
- source-label rematch;
- prefix/substring semantic match;
- score/confidence rank;
- majority/most-common;
- first-row/file-order selection;
- embedding/LLM similarity;
- current authority substitution;
- dropping a missing participant/negative and continuing.

The broken exact locator/hash remains part of failure evidence. Repair requires a new valid immutable publication/repository bundle, not mutation in place.

## 10. Standalone structural resolution versus full offline empirical replay

S5578C adopts R03C's distinction because it prevents both unnecessary bloat and false replay claims.

### Claim A — standalone V558 structural resolution

Raw V553–V556 directories are absent. Exact producer structural semantics and their interpretation-critical authority/provenance dependencies resolve from the immutable repository closure. This does **not** require physically embedding all respondent-event C11 incidence if no structural interpretation operation reads those rows.

### Claim B — full offline empirical replay

If the system claims it can recompute the admitted empirical fact from historical raw incidence, then the exact C11 content and all risk-set/measure/authority inputs must be packaged or exactly immutable-resolvable. A C11 hash with no available immutable material/resolution contract is insufficient.

Failure of Claim B does not authorize rewriting Claim A's structural object. It means full empirical replay is unavailable/fails closed.

## 11. Required parent fixtures

S5578C proposes that SCR5578 and M4/M5 adopt at least the fixture classes in `HOSTILE_FIXTURES.md`:

- raw producer directories absent standalone success;
- mutable/broken locator rejection;
- object/authority hash/version mismatch;
- missing negative/temporal-limit rejection;
- valid-empty versus broken-empty separation;
- n-ary role/cardinality/order corruption;
- producer re-ID rejection;
- item-wise permission monotonicity;
- dependency permission noninheritance;
- provenance-as-composition rejection;
- source-universe collision rejection;
- query/risk-set/measure closure after copy removal;
- PSEPF smuggling rejection;
- latest/fuzzy repair rejection;
- ambiguous strong-reference rejection;
- index-hit re-verification;
- co-resolution noncomposition;
- full-replay-claim distinction;
- arbitrary audit/prose mention non-following;
- atomic bundle/policy identity tests.

## 12. What this feeder does not decide

S5578C does not decide:

- SCR5578's final runtime-use governance schema;
- SCR5578's final corrected producer-family registry after SCR553/554/555/556 signoff;
- exact physical storage engine/file layout;
- whether V557/V558 are physically co-packaged;
- final M4 producer seam acceptance;
- final M5 V3 peer-prior integration;
- production implementation or migration sequence.

Those remain parent/sibling authority.

## 13. Final handoff

The parent can safely minimize repeated payload only after it proves, per root and bundle:

```text
1. exact producer identity/hash survives;
2. every required semantic edge is typed and hash-bound;
3. positive AND negative dependencies close;
4. source/query/risk-set/measure/authority identity closes where interpretation-critical;
5. role/cardinality/multiplicity/order survives;
6. CAN-003 permission bindings survive item-wise;
7. locators are immutable/reversible and indexes are nonsemantic;
8. no repair/latest/fuzzy/raw-stage/network fallback exists;
9. PSEPF/reverse-lane classes are rejected;
10. provenance does not become composition permission;
11. raw producer directories can be absent;
12. same exact repository/query/policy/bindings replay identically.
```

No evidence requires reopening the frozen broad DAG. The result is a bounded SCR5578 closure requirement and hostile fixture package.

**Token:** `S5578C_FEEDER_COMPLETE`
