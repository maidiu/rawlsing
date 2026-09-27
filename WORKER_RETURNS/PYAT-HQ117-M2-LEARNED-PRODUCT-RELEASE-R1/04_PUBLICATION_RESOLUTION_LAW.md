# PYAT HQ117 — Publication and Resolution Law

## 1. Holding

Publication is the act of making one exact release resolvable.

It is not:
- semantic adjudication;
- current selection;
- consumer permission;
- structural admission;
- source retirement.

M2 separates immutable release identity from immutable publication-binding identity so that serving topology can change without rewriting semantic history.

## 2. Publication equation

A publication binding states:

THIS EXACT RELEASE_ID
IS RESOLVABLE THROUGH
THIS EXACT RESOLUTION MODE
USING
THIS EXACT RESOLVER/LOCATOR + INTEGRITY CONTRACT

A future conforming implementation may have many bindings for one release.

Examples:
- direct producer exact ref;
- content-addressed artifact/object;
- immutable repository object locator;
- virtual deterministic rebuilder;
- learned service resolver.

## 3. Exact-resolution law

Every resolution begins with an exact release id or exact publication-binding id.

Forbidden selector semantics inside M2:
- latest;
- default;
- nearest;
- fuzzy;
- semver range;
- filesystem-most-recent;
- database-last-row;
- highest version number;
- Git newest commit;
- absence of a newer row.

If a caller wants "current", it must first obtain an exact release id from M3's governed current-selection jurisdiction and then call M2 exact resolution.

Freeze:

M3_SELECTS_EXACT_RELEASE_ID
THEN
M2_RESOLVES_EXACT_RELEASE_ID

## 4. Direct producer resolution

DIRECT_PRODUCER_REF is a first-class publication mode.

This satisfies Authority31's producer-owned DAG law:
- producer identity remains visible;
- no copied wrapper becomes semantic owner;
- exact upstream object can remain canonical;
- M2 adds only release/publication metadata.

A release manifest may therefore contain no duplicate semantic payload.

The publication binding can resolve straight to the producer's exact ref.

## 5. Materialized publication

A materialized representation is lawful where operationally useful.

Requirements:
- exact release id attached;
- exact representation integrity hash/ref;
- exact producer subject ref remains recoverable;
- representation is verified semantically equivalent under the producer contract;
- materialization does not widen permissions;
- materialization does not become authority merely because persistent.

Changing serializer/compression/layout alone may create a new publication binding or representation hash while preserving release id.

## 6. Virtual/rebuilder publication

A virtual binding may point to a governed deterministic reconstruction procedure.

Requirements:
- exact release id;
- exact replay/rebuild contract;
- exact source/upstream roots;
- exact determinant closure;
- expected semantic identity;
- typed failure if reconstruction prerequisites are unavailable;
- no fallback to current authority.

A virtual binding may be slower than a cache. Slowness is not semantic invalidity.

## 7. Service publication

For LEARNED_SERVICE_CONTRACT:
- release subject is the exact logical service contract;
- publication binding locates a physical/runtime resolver for that service contract;
- endpoint address/process/container may change via new publication binding;
- service contract release id does not change solely because endpoint moved;
- a resolver must prove it implements the exact released service contract and authority closure;
- individual invocations produce execution receipts;
- invocation outputs become learned releases only if a semantic producer separately owns and publishes them.

A load balancer or mirror cannot silently choose a different service release.

## 8. Multiple bindings and mirrors

Multiple publication bindings may coexist for one release.

This is lawful redundancy, not currentness.

A resolver may choose among bindings only under non-semantic operational policy when every candidate binding is proven to resolve the exact same release id and subject.

If two bindings resolve different release ids, operational failover cannot choose between them. That would be lifecycle/current-selection.

## 9. Publication-binding change

Changes that normally produce a new publication_binding_id but NOT a new release_id:
- moved physical path;
- new repository location;
- new mirror;
- changed compression/serialization;
- materialized -> virtual;
- virtual -> materialized;
- cache/index redesign;
- new service endpoint;
- storage backend migration.

Changes that require a new release_id if constitutive:
- different release subject;
- different semantic producer contract;
- different authority closure;
- different semantic dependency closure;
- different determinant closure;
- different replay/reconstruction contract;
- different explanation lineage that reflects a genuinely different historical release basis.

## 10. Availability is not semantic state

A binding may be temporarily unavailable.

UNAVAILABLE_BINDING does not imply:
- withdrawn release;
- false product;
- superseded product;
- no-current product;
- permission denial.

It is an operational resolution state.

If all physical bindings are unavailable but deterministic reconstruction remains valid, M2 may still resolve via a governed rebuilder binding.

If no lawful binding/rebuild path is available, resolution fails closed while the historical release identity remains.

## 11. Typed nonpositive publication

M2 can publish:
- positive learned product;
- valid-empty disposition;
- observed-zero fact;
- zero-support disposition;
- exact candidate REJECT adjudication;
- BLOCKED/missing-authority disposition;
- noncomparable/no-transport disposition;
- out-of-scope/not-applicable disposition;
- coverage-limited/nonexhaustive disposition;
- integrity/replay failure record where that record is a producer-owned auditable disposition.

Publication success means only:
"this exact typed subject has been durably released."

It does not mean:
"the underlying proposition is positive."

## 12. REJECT and BLOCKED law

P1 governs:
- REJECT is an adjudication about a proposed relation proposition, not a negative truth-bearing semantic polarity;
- BLOCKED is unresolved authority state, not positive or negative truth.

Therefore M2 may publish exact REJECT/BLOCKED dispositions as typed subjects but MUST NOT:
- mint a negative semantic claim from REJECT;
- turn BLOCKED into REJECT;
- turn BLOCKED into empty positive;
- erase blocker/successor-obligation refs.

## 13. VALID_EMPTY law

VALID_EMPTY can be a successful release subject.

It means the competent producer's exact operation yielded a valid empty/nonpositive disposition under its contract.

It does not create:
- a positive relation with zero rows;
- an observed-zero claim unless producer semantics say so;
- a universal absence theorem;
- a permission to infer "false".

Freeze:

VALID_EMPTY__NO_POSITIVE_RELATION

## 14. Resolver permission firewall

M2 resolver answers:
- what exact release is this?
- can it be resolved exactly?
- what exact producer subject does it point to?
- what are its release/publication/replay/explanation refs?

M2 resolver does not answer:
- may V3 use it causally?
- may PRE-V3 consume it for this target?
- is it current?
- is this source pool comparable?
- is this relation structurally admitted?
- may this actor know it?

Those require their own authorities.

## 15. Repository/index law

A registry/index can accelerate lookup by exact release id.

Such a registry:
- may not define semantic identity;
- may not choose currentness;
- may not infer missing entries as withdrawal;
- may not widen scope;
- may not reinterpret historical releases.

Loss or rebuild of a pure index changes availability/performance, not release semantics.

A search catalog over release metadata is likewise nonauthoritative unless every displayed semantic field is verified as a projection of the exact producer subject.

## 16. Resolution receipt

Every exact resolution should be auditable with a receipt containing, at minimum:
- requested release_id;
- chosen publication_binding_id;
- exact release-core hash;
- exact resolved subject ref;
- representation integrity result;
- resolver contract identity;
- typed success/failure;
- no-selector-substitution assertion.

A resolution receipt is an audit object.

It is not M3 current-selection evidence unless separately referenced by an explicit lifecycle authority.

## 17. M3 publication relation

M2 publication may occur before, after, or without M3 current selection.

Lawful states include:
- published historical release, not current;
- published current release;
- directly referenced subject with no generic M2 release;
- published typed negative disposition;
- multiple historical releases all resolvable;
- no current release selected.

M3 may select only an exact release id.

M2 may never infer current from publication order.

## 18. Downstream service relation

A downstream consumer can choose one of two lawful paths:

A. exact direct producer dereference, if its own contract permits and no M2 release claim is required;

B. exact M2 release resolution, then consumer-specific permission/admission.

Neither path permits:
- semantic reownership;
- authority widening;
- currentness inference;
- actor-state leakage.

## 19. Physical architecture neutrality

M2 does not choose:
- centralized registry vs distributed manifests;
- SQL vs object store vs Git/content-addressed store;
- persistent payload vs virtual rebuild;
- one repository vs family-specific repositories;
- local vs remote resolver;
- cache/index strategy.

Any implementation must preserve the exact logical contracts above.

## 20. Publication terminal

The smallest generic release/publication jurisdiction is:
- immutable release core;
- immutable publication binding(s);
- exact resolution receipt;
- exact producer-preserving dereference;
- no currentness/permission semantics.

That jurisdiction is separable from M1 and M3 and therefore passes the M2 commission.
