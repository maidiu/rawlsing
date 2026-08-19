# 04 — INTERFACE, DAG & CHANGE CONTROL

## 1. Canonical interface registry

G4 maintains one machine-readable registry for every cross-worker/cross-domain interface.

Each interface record must include:

- interface ID/version/hash;
- producer authority;
- legal producer object family;
- consumer(s);
- edge class;
- object grain;
- required/optional/forbidden fields;
- identity tuple;
- cardinality/order/role law;
- positive/negative states;
- time semantics;
- reference/provenance obligations;
- authority bindings;
- compatibility rule;
- hostile fixture IDs;
- deprecation state.

## 2. DAG ownership law

Every canonical object has exactly one semantic owner, though it may have many legal consumers.

Every legal edge is explicitly registered. Unregistered transit is forbidden.

Stages/services may be co-executed physically without collapsing semantic ownership. Conversely, separate files/processes do not prove separate semantic jurisdiction.

## 3. Edge classes

Use only registered classes:

- `REQUIRED_SEMANTIC_TRANSFORM`
- `CONDITIONAL_SEMANTIC_TRANSFORM`
- `DIRECT_PUBLICATION_EDGE`
- `PRESERVE_BY_REFERENCE`
- `TRANSITIVE_REFERENCE`
- `GOVERNANCE_BOUNDARY`
- `REPOSITORY_RESOLUTION_BOUNDARY`
- `AUDIT_REPLAY_ONLY`
- `FORBIDDEN_EDGE`

## 4. Semantic reference versus provenance

A reference is semantic only if the consumer's lawful interpretation/result depends on the referenced producer meaning.

Provenance/audit reachability does not grant:

- source pooling;
- respondent linkage;
- structural admission;
- actor comparability;
- runtime permission;
- causal influence.

These require their own authority.

## 5. Change classes

### C0 — local implementation only

No shared contract, schema, identity, authority, negative state, DAG edge, or replay behavior changes.

Domain Vozhd may approve.

### C1 — compatible contract clarification

Makes an already-binding shared contract more explicit without changing legal object sets or consumer semantics.

Owning General Staff authority + G6 approves; impacted workers refresh.

### C2 — shared contract evolution

Changes schema/identity/state/interface behavior but preserves architecture.

Owning Staff authority, all impacted domain Vozhds, G6, Inspectorate, and Integration Command must sign off. Version increment required.

### C3 — architecture-affecting change

Adds/removes semantic owner, changes DAG jurisdiction, changes source/actor/structural ontology, or changes terminal capability.

Requires Campaign Vozhd and the appropriate higher architecture authority. Workers stop at the affected seam.

## 6. Change request contents

Every C1-C3 request must state:

- requesting worker/command;
- current contract and version;
- exact deficiency;
- proposed change;
- semantic reason;
- alternatives rejected;
- affected objects/fields/IDs/hashes;
- affected DAG edges;
- affected consumers;
- migration/replay consequences;
- negative-authority consequences;
- tests/fixtures affected;
- whether work can continue safely pending adjudication.

## 7. Stale-worker rule

When a shared contract changes, G6 marks all affected workers `STALE_CONTRACT`.

A stale worker may not cross the changed interface until it acknowledges the new version and either rebases or proves its current work is version-compatible.

## 8. No merge-by-convention

If two workers independently created semantically similar fields or types, Integration Command may not reconcile them by naming convention.

The shared owner must determine whether they are:

- same object;
- distinct objects;
- one implementation duplicate;
- one invalid unauthorized invention.

## 9. Compatibility-shim registry

Every shim record contains:

- shim ID;
- source contract/version;
- target contract/version;
- semantic claim;
- exact transform;
- owner;
- tests;
- consumers;
- retirement condition;
- latest permissible wave.

A shim with no retirement condition is rejected.

## 10. DAG linting requirements

Before every integration wave, automated/static checks should detect at least:

- orphan canonical objects;
- multiple semantic owners;
- forbidden edges;
- cycles where law requires acyclic flow;
- unregistered consumer inputs;
- missing authority hashes;
- missing reference targets;
- PSEPF in structural repository lane;
- direct empirical/structural -> V2 persona paths;
- unauthorized source-universe composition;
- stage-number-only transit with no unique transform/governance responsibility.
