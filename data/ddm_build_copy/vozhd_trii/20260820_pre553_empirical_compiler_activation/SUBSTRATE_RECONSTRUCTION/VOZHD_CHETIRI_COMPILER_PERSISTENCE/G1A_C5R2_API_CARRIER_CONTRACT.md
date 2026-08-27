# G1A C5R2 — Semantic-Maintenance API / Carrier Contract

**Repository:** `maidiu/rawlsing`

**Exact HQ launch HEAD:** `4fedf24084a317806141f4799aa8359ad40c8f7c`

**Owner:** `PRE553_SEMANTIC_MAINTENANCE_OWNER_C5R2_REF_V1`

**Executor:** `PRE553_SEMANTIC_RELEASE_EXECUTOR_C5R2_REF_V1`

**Authority ceiling:** `C5R2_ISOLATED_REFERENCE_EXECUTION_ONLY__NOT_LIVE_PROMOTION`

## 1. Reference implementation

`C5R2/reference_semantic_maintenance.py`

The implementation is intentionally branch-local and additive. Its `ExactRef` wire shape is the same exact identity pattern already used by PRE553 (`kind`, `object_id`, content hash). It does not change or widen the live PRE553 authority-kind vocabulary.

## 2. Owner API

### Governing inputs

- `register_governance_authority(ref)` — registers the exact court/governance authority permitted to make semantic decisions.
- `register_family_rule(family, ref)` — binds an exact governed family rule; missing/unregistered family rules fail closed.
- `bind_evidence(bundle)` — persists a `COMPLETE` exact evidence bundle and its binding authority.

### Semantic production

- `nominate(candidate)` — emits only `SEMANTIC_CANDIDATE`; nomination creates zero semantic authority.
- `adjudicate(decision)` — records explicit governed `ACCEPT`, `REJECT`, or `BLOCKED` at exact candidate scope.
- `create_authority(...)` — may create an immutable positive semantic authority only from an exact governed `ACCEPT`.
- `resolve_authority_exact(ref)` — exact id/hash resolution only; no latest/default/fuzzy/nearest fallback.

### Lifecycle/currentness

- `record_lifecycle(event)` — persists typed `SURVIVES_SAME_ID`, `RECERTIFIES`, `CORRECTS`, `WITHDRAWS`, `CURRENT_SELECT`, `REOPENS_BLOCKED`, `APPENDS_SUCCESSOR_OBLIGATION`, or `CHANGES_SCOPE_EXPLICITLY` events.
- `select_current(...)` — explicit current-selection operation under exact jurisdiction key.
- `withdraw(...)` — explicit withdrawal; immutable authority history remains.
- `current_exact(jurisdiction_key)` — returns only the explicitly selected authority; no recency inference.

For `REOPENS_BLOCKED`, the event subject must be an exact prior `BLOCKED` adjudication. The event does not create positive authority or currentness.

### Genealogy

- `adjudicate_genealogy(decision)` — explicit governed `SPLIT`, `MERGE`, `VARIANT`, `EXCLUSION`, or `SUCCESSOR` decision; ambiguous/blocked genealogy fails closed.
- `append_genealogy(edge)` — append-only edge creation and exact-ref validation.

Split law:

`UNION(EXACT_CHILD_MEMBER_SETS) == EXACT_PARENT_MEMBER_SET`

and every declared child set must equal its exact child authority member set. Loss, addition, overlap, mismatched child declarations, or ambiguity fails closed.

Merge law:

`UNION(EXACT_PARENT_MEMBER_SETS) == EXACT_CHILD_MEMBER_SET`

Variant/exclusion law:

an exact registered governed genealogy decision is mandatory. A label, similarity, or arbitrary ref cannot create either relation.

### Dependency/revalidation

- `bind_descendants(binding)` — persists immutable forward semantic-authority → I04/structural-descendant bindings.
- `revalidate_descendants(..., triggering_event=...)` — regenerates reverse reachability from forward bindings and emits a receipt only when a typed lifecycle event is supplied.

`DEPENDENCY_TRAVERSAL_WITHOUT_TYPED_EVENT -> FAIL_CLOSED`

This preserves P7: reachability can execute consequences but cannot infer semantic/lifecycle meaning.

## 3. Release executor API

- `assemble_release(...)` — creates immutable semantic release from exact authority/lifecycle/genealogy/revalidation refs and optional exact predecessor release.
- `resolve_release_exact(ref)` — exact replay only.
- `promote(release_ref, decision_authority_ref=...)` — explicit governed promotion; all release authorities must already be explicitly current.
- `rollback(predecessor_release_ref, decision_authority_ref=...)` — explicit governed rollback of release-current pointer only.

No release API can rewrite prior authority, lifecycle, genealogy, dependency, revalidation, or release records.

## 4. Carrier classes

The reference carrier is an append-only logical journal divided into two authority-bearing streams.

### Semantic-maintenance stream

Record kinds:

- `GOVERNANCE_AUTHORITY_BINDING`
- `FAMILY_RULE_BINDING`
- `COMPLETE_EVIDENCE_BINDING`
- `CANDIDATE_NOMINATION`
- `GOVERNED_ADJUDICATION`
- `IMMUTABLE_SEMANTIC_AUTHORITY`
- `TYPED_LIFECYCLE_EVENT`
- `GOVERNED_GENEALOGY_ADJUDICATION`
- `APPEND_ONLY_GENEALOGY`
- `IMMUTABLE_FORWARD_DEPENDENCY_BINDING`
- `DESCENDANT_REVALIDATION`

### Release stream

Record kinds:

- `IMMUTABLE_SEMANTIC_RELEASE`
- `EXPLICIT_RELEASE_PROMOTION`
- `EXPLICIT_RELEASE_ROLLBACK`

Every journal record receives a deterministic content hash. The reference execution emits both append-only journals. The persisted witness records their deterministic roots, record counts/kinds, exact predecessor/successor refs, and replay results; the executable implementation is the reproducer for the full journal payloads.

The carrier classification is:

- semantic authority/lifecycle/genealogy/release objects: P2-class governed products;
- replay/journal/change receipts: P3-class replay/provenance products;
- regenerated reverse indexes: cache/derived only, never semantic authority.

## 5. Identity contract

Semantic claim identity is computed only from proposition identity plus truth-bearing assertion state.

Evidence/authority-instance changes that leave all constitutive family semantics equal preserve semantic claim identity and may create a new governing authority instance under `RECERTIFIES`.

Constitutive changes create a different proposition/claim identity and require `CORRECTS` (or another explicitly governed P2 event appropriate to the actual change).

Reaffirmation/no-replacement is represented by `SURVIVES_SAME_ID`; it does not require a new authority instance.

## 6. Fail-closed contract

The implementation rejects:

- authority creation from nomination alone;
- authority creation from REJECT/BLOCKED;
- incomplete evidence bundles;
- missing/unregistered family rules;
- unregistered governance authority;
- ambiguous genealogy;
- split member loss/addition/overlap/mismatch;
- ungoverned split/merge/variant/exclusion;
- current selection by version/chronology;
- release promotion without explicit current authority selection;
- release promotion/rollback without explicit governance authority;
- dependency traversal that attempts to infer lifecycle type;
- exact replay requests for absent refs.

## 7. Executed proof

`C5R2/G1A_C5R2_AUTHORITATIVE_EXECUTION_WITNESS.json`

Executed owner journal root:

`2a570d698810727ef1143492065aa1edfa67f7bfc5222b1f22f2397c99dce080`

Executed release journal root:

`850a5fa8430d2a86837bf50d56dd32eda9ae0f644a6d012b20d3fb7a349fa4c3`

The proof fixture is authoritative only inside the C5R2 reference jurisdiction named above. The carrier/API contract is therefore executable and governed without constituting live semantic promotion.

`C5R2_API_CARRIER_CONTRACT_COMPLETE__EXACT_APPEND_ONLY_OWNER_EXECUTOR_PATH_PROVED__NO_LIVE_PROMOTION`
