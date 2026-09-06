# GT3/GT4 O3 — V558 DEPENDENCY-ROLE RECONSTRUCTION BOUNDARY AUDIT R1

## Terminal

`FAIL__GT34_O3_ASTRA006_DEPENDENCY_ROLE_RECONSTRUCTION_DEFECT_PROVED`

## Execution boundary

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-gt34-o3-v558-dependency-role-boundary-audit-r1`
- exact working-ancestry start: `3aaf6759f270c9b730db5d09bb6a87f92ec34345`
- immutable instruction ref: `15f1a470843ffe322c054a115c0685cb8a4e26e8`
- instruction blob: `9fbafb5fbae85bda28c1c577a9fd0bf85e868dd5`
- worker: `O3 — V558 DEPENDENCY-ROLE RECONSTRUCTION BOUNDARY AUDIT R1`
- profile: `HOSTILE_AUDIT`
- production implementation: NONE
- repository redesign: NONE
- positive V3 execution: NONE
- actor mutation: NONE

ASTRA-006 was treated as an OPEN QUESTION.

This audit promotes it to a bounded current defect only after proving an ordinary public reconstruction path that can lose dependency-role declarations while retaining the same producer object identity and then pass the accepted V558 builder/resolver and first downstream M5 trust boundary.

---

# 1. Astra source question

Astra finding source:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/ASTRA_DEEP_SYSTEM_AUDIT_R1/02_FINDINGS_LEDGER.jsonl`

blob:

`0ea6bb23be3c17f009c705dec74fdd622da4668a`

ASTRA-006 correctly held only an open question.

Its exact prior concern was:

- builder-enforced dependency completeness exists;
- itemwise transitive permission checks exist;
- `StructuralObject` identity omits `required_dependency_refs` and `negative_dependency_refs`;
- repository checksum material includes exact edge hashes but does not independently authenticate the object's dependency-declaration metadata;
- opaque M1 lineage may lawfully remain opaque provenance.

Astra did not prove a valid constructor-to-consumer bypass.

O3 does.

---

# 2. Exact current accepted implementation boundary

Primary V557/V558 executable boundary:

`rawlsing_next/m4_v557_v558_publication_repository.py`

blob:

`9005308fb06686b593783666e77d06619645b2bb`

The current module history includes the accepted sideline runtime and subsequent hardening commits:

- `f090d625fee3ca715559a7d13817e6d3d82183ed` — Implement M4 V557/V558 sideline runtime
- `74532ca58a601ce17c677643ae7cb1c8030df1a4` — Harden M4 producer and checksum validation
- `de817104ff10dd6be6d1c65af25c1d9d02b4319a` — Preserve V556 producer bytes during M4 validation
- `e51730e461a15b0ad20f02f2efb4bccd751c2c81` — M4 repair validation order for V556 participant closure

The actual first downstream consumer in the current executable tree is:

`rawlsing_next/m5_runtime_rsc_peer_prior.py`

blob:

`18735bdb31a220aed032aa722574d685e2bdddf5`

introduced at:

`93cc3e7381b9abb07c0642d6549a754711432b52`

message:

`Implement M5 runtime RSC structural peer seam`

M5 explicitly states that M4 remains sole owner of V558 exact resolution.

M5 does not accept an already-materialized free-form RSC as authority. It takes exact in-memory:

- `V558RepositoryBundle`
- `ContextQuery`
- `ResolutionResult`

and `_exact_m4_resolution(...)` reruns:

`resolve_v558(repository, query, ...)`

then requires the supplied `ResolutionResult` to equal that deterministic re-resolution exactly.

This is the current first downstream V558 trust boundary.

---

# 3. Codec / loader answer

## Accepted external serialization codec

O3 found **no accepted external V558 codec/loader/reconstructor** in the current M4 or M5 runtime modules.

The M4 implementation exposes no:

- `from_dict`;
- `to_dict` bundle codec;
- `serialize`;
- `deserialize`;
- JSON/YAML/pickle loader;
- decode/encode reconstruction API;
- file `open(...)` persistence loader.

The operative current path is in-memory typed construction.

That fact does **not** close ASTRA-006, because the ordinary public typed reconstruction surface itself is sufficient to demonstrate role loss.

Therefore outcome C is unavailable.

---

# 4. What the current builder gets right

The builder itself is strong **relative to the dependency declarations it receives**.

## 4.1 Required + negative completeness

`build_v558_repository_bundle(...)` iterates:

`tuple(entry.obj.required_dependency_refs) + tuple(entry.obj.negative_dependency_refs)`

For every declared dependency it requires:

1. exact dependency object present in the standalone repository;
2. at least one exact source->target repository edge;
3. edge `requiredness == "REQUIRED"`.

Missing declared positive or negative dependency fails:

`required positive/negative dependency absent from standalone repository`

or:

`required positive/negative dependency lacks exact role-preserving edge`.

Existing current tests prove that an ordinary correctly-declared root cannot omit its negative dependency edge:

`test_standalone_closure_requires_positive_and_negative_dependencies_and_exact_edges`

in:

`rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`

blob:

`f29a06ba2d3e43786a5562cae86a356721c6b922`

This control is valid.

## 4.2 V556 role/order/cardinality

The same builder independently validates V556 participant edge role, semantic ordinal, multiplicity and declared cardinality against the producer payload.

Partial n-ary closure is rejected.

This is not the ASTRA-006 defect.

## 4.3 Exact edge identity

`ReferenceEdge` content-addresses:

- source locator;
- target locator;
- reference-contract authority;
- edge role;
- requiredness;
- participant role;
- cardinality;
- multiplicity key;
- order significance;
- semantic ordinal.

Repository material includes exact `edge_hash` values.

Changing or omitting an edge changes the repository identity.

The defect is not an edge-hash collision or stale repository checksum.

---

# 5. What is not content-addressed

`StructuralObject` has:

- `required_dependency_refs`;
- `negative_dependency_refs`.

But its `content_hash` is validated only against:

`semantic_hash(payload)`.

Exact current code:

- freezes `payload`;
- requires `semantic_hash(frozen_payload) == content_hash`;
- canonicalizes/sorts required and negative dependency refs;
- does **not** include either dependency-ref tuple in the producer object digest.

`make_structural_object(...)` likewise computes:

`content_hash = semantic_hash(payload)`

independently of:

- `required_dependency_refs`;
- `negative_dependency_refs`.

Therefore the following two `StructuralObject` values can have the **same**:

- producer family;
- semantic class;
- object ID;
- payload;
- content hash;
- schema;
- typed state;
- producer use ceiling;
- source stage;
- `obj.ref`;

while differing in whether an exact dependency is declared required or negative.

That is the authenticated-role gap.

---

# 6. Governance, publication and locator do not repair the gap

## V557 governance

`V557GovernanceRecord` binds:

- `obj.ref`;
- producer allowed uses;
- V557 allowed uses;
- decision state;
- exception state;
- authority ref.

It does not bind dependency declaration tuples independently.

If reconstructed object A' has the same `obj.ref` and use ceiling as A but weakened dependency declarations, the same governance identity remains compatible.

## V557 publication identity

`_publication_material(...)` binds each entry as:

- `object_ref`;
- producer family;
- typed state;
- governance ref.

It does not include required/negative dependency declaration metadata.

Therefore A and dependency-weakened A' can produce the same publication-root identity material.

## Producer locator

`ProducerLocator` reversibly binds:

- producer family;
- object ID/hash;
- schema;
- governance ref;
- producer contract/rule bindings;
- storage/provenance locators.

Again, it does not independently bind the dependency-declaration tuples.

`RepositoryEntry.__post_init__` therefore cannot distinguish A from A' when the producer ref/hash and all locator-bound fields are unchanged.

---

# 7. Exact public reconstruction bypass

This is the dispositive proof.

No private repository mutation, monkeypatch, raw dataclass bundle forgery, or future external codec is necessary.

All necessary steps exist on the ordinary public M4 construction surface.

Start from the exact shape already exercised by the accepted test:

- root structural object A;
- required positive dependency P;
- required negative dependency N;
- A declares:
  - `required_dependency_refs = (P.ref,)`;
  - `negative_dependency_refs = (N.ref,)`;
- exact P and N repository edges.

The lawful builder rejects omission of N's edge while A still declares N.

Now reconstruct A through ordinary public:

`make_structural_object(...)`

using the exact same:

- producer family;
- semantic class;
- object ID;
- schema/version;
- typed state;
- producer allowed uses;
- payload;
- source stage;

and retain:

`required_dependency_refs = (P.ref,)`

but supply:

`negative_dependency_refs = ()`.

Call this A'.

Because `content_hash = semantic_hash(payload)` and the payload is unchanged:

`A'.content_hash == A.content_hash`

and therefore:

`A'.ref == A.ref`.

This is not hash collision behavior. It is the specified current identity projection.

Because the producer ref and use ceiling are unchanged:

- the V557 governance binding remains valid at its authenticated fields;
- the publication root sees the same producer object ref;
- the locator can bind the same producer ID/hash/schema/governance tuple.

Now call ordinary public:

`build_v558_repository_bundle(...)`

with A', P and a repository edge only for P.

The builder's dependency-completeness loop sees only A' current declarations.

N is no longer in:

`required_dependency_refs + negative_dependency_refs`.

Therefore the missing N edge is not an error.

The builder seals a new checksum-valid repository whose exact edge set omits N.

That repository is not corrupt according to:

`_validate_repository_checksum(...)`

because the checksum faithfully authenticates the weakened edge set it was given.

This proves:

> a dependency role can be deleted before repository construction while the producer object retains the same exact semantic ref/hash.

ASTRA-006 is therefore not merely a future-codec risk.

---

# 8. Resolver cannot recover the omitted role

`resolve_v558(...)` validates:

- repository checksum;
- query hash;
- exact index key;
- exact repository locator;
- transitive closure over repository edges whose `requiredness == "REQUIRED"`;
- exact object bodies;
- itemwise producer + V557 permission subsets.

Its transitive closure is edge-derived.

Once the reconstructed A' omitted the negative declaration and the repository omitted N's edge, the resolver has no authenticated producer-role fact from which to infer that N should have existed.

It must not invent one.

Therefore:

- checksum validation passes for the weakened repository;
- closure traversal sees only remaining required edges;
- itemwise permission checks apply only to remaining closure entries.

The resolver's current behavior is locally correct.

The input identity is insufficient.

---

# 9. First downstream M5 consumer cannot detect the role loss

M5 is unusually strong about replay:

`_exact_m4_resolution(...)`

reruns `resolve_v558` and rejects any supplied M4 evidence that differs from deterministic re-resolution.

That protects against:

- stale supplied `ResolutionResult`;
- altered selection records;
- altered resolved entries;
- altered resolution receipt.

It cannot protect against a semantically weakened but checksum-valid repository whose lost dependency role is no longer authenticated anywhere M4 can inspect.

M5 derives:

- `permission_subset_proof_digest`;
- `reference_closure_digest`;
- `preserved_negative_entry_set_digest`;
- provenance and producer-binding digests;

from the exact M4 resolution **of the supplied repository**.

Those digests accurately describe the weakened repository.

They do not prove that the original producer object once required a now-omitted negative dependency.

Consequently M5's deterministic re-resolution does not close this defect.

---

# 10. Itemwise permissions remain sound

O3 does **not** find permission widening in the ordinary intact repository path.

M4 computes transitive required entries from repository edges and, for each selected root, requires the requested use to be a subset of both:

- each dependency object's producer allowed uses;
- each dependency's V557 allowed uses.

Existing test:

`test_dependency_permission_is_checked_itemwise_and_root_permission_does_not_inherit`

proves a root cannot lend its permission to a dependency.

M5 separately reconstructs and validates a permission subset proof and later `bind_structural_peer_use(...)` refuses a use absent from an RSC entry's `resolver_allowed_uses`.

So:

`ROOT_PERMISSION_DOES_NOT_INHERIT_TO_DEPENDENCY`

remains proved.

The defect is earlier: a dependency role can disappear from the authenticated closure before those itemwise checks execute.

---

# 11. Opaque lineage / provenance is not the defect

O3 separately inspected:

`rawlsing_next/m4_m1_evaluation_binding.py`

blob:

`491233f9d21e4c851bd3075aef65b5d3022d4127`

The relation-M1 wrapper verifies exact V554 publication refs against exact payload hashes and then creates structural objects without automatically reclassifying every lineage/provenance ref as a required repository dependency.

That is not by itself wrong.

The accepted invariant remains:

> opaque lineage/provenance is evidence unless a producer/dependency contract explicitly promotes it to a required or negative dependency role.

M5 likewise proves that provenance strings cannot create permission.

Existing test:

`test_repository_index_and_provenance_never_widen_permission_or_create_actor_effect`

uses a provenance locator containing strings such as:

`ACTIVE_CAUSAL/POOLING/AUTHORIZED`

and still obtains permission denial.

Therefore O3 does **not** recommend turning opaque M1 lineage into executable edges.

Any repair must preserve this distinction.

---

# 12. Negative dependencies are semantically distinct and currently vulnerable

ASTRA-006 specifically asked whether a roundtrip/reconstruction could omit or reclassify a negative dependency while retaining a valid-looking identity.

O3 answer:

**YES.**

The producer object ref can remain identical because dependency declaration tuples are outside its content hash.

The V557 governance/publication/locator identity layers do not add those tuples.

The V558 repository hash authenticates the edge set that exists, but has no independent authenticated statement of the dependency role set that should have existed.

Therefore a reconstructed role-weakened object can produce a valid-looking, checksum-valid repository.

This is exact dependency-role loss, not merely loss of explanatory metadata.

---

# 13. No current external codec does not create a safe trust boundary

Outcome C required proof that:

1. no accepted codec exists;
2. the actual first consumer receives only a trusted in-memory bundle built by the validated builder;
3. no alternate public constructor/loader can bypass dependency-role validation.

O3 proves (1).

O3 cannot prove (2)-(3).

The ordinary public typed reconstruction path:

`make_structural_object -> V557PublicationEntry/build_v557_publication_bundle -> RepositoryEntry -> build_v558_repository_bundle`

is already an alternate reconstruction path relative to the original producer dependency-role declaration.

The builder validates the declaration it receives, not an authenticated prior declaration identity.

M5 accepts the resulting exact typed repository and reruns its resolver; there is no non-forgeable builder-origin seal binding original dependency-role declarations.

Therefore the current first-canary trust boundary is not executable strongly enough to bank outcome C.

---

# 14. Required-question adjudication

1. **What accepted codec/loader exists?**  
   No external serialization codec/loader found. Current executable boundary is typed in-memory M4 construction plus M5 exact re-resolution.

2. **Does construction validate required + negative completeness?**  
   Yes, relative to the dependency declarations present on the supplied `StructuralObject`.

3. **What dependency-role material is content-addressed?**  
   Exact repository edges are content-addressed with role/requiredness/cardinality/participant metadata. Producer dependency-declaration tuples are not part of `StructuralObject.content_hash`.

4. **What role material is reconstructed from trusted builder law?**  
   Builder closure obligations come from the current object's `required_dependency_refs` and `negative_dependency_refs`, plus special producer-payload validation such as V556 participant roles.

5. **Are opaque M1 lineage refs intentionally non-executable provenance?**  
   Yes. Presence alone grants neither dependency role nor permission.

6. **Can roundtrip/reconstruction omit/reclassify a negative dependency under valid-looking identity?**  
   Yes. Exact defect proved as above.

7. **Does first consumer infer permission/causal readiness from lineage presence?**  
   No. M4 and M5 permission checks are explicit and itemwise.

8. **Does resolver permission remain itemwise?**  
   Yes.

9. **Is there an executable trusted boundary making current design sound?**  
   No. M5 re-resolution authenticates the supplied repository, but original dependency-role declarations can already have been weakened under the same producer ref.

10. **Does no external codec make first canary safe in-memory?**  
    No. The public typed reconstruction path itself is sufficient to lose the role.

---

# 15. Exact defect

`V558_DEPENDENCY_ROLE_DECLARATIONS_NOT_BOUND_TO_PRODUCER_IDENTITY__PUBLIC_RECONSTRUCTION_CAN_DROP_REQUIRED_OR_NEGATIVE_ROLE_BEFORE_CHECKSUMMED_REPOSITORY_BUILD`

The narrow failure is:

`dependency declaration -> producer exact ref`

is not authenticated.

The builder and resolver correctly enforce:

`current declaration -> exact edges -> transitive itemwise permission`.

But they cannot establish:

`this current declaration is the same dependency-role declaration owned by the exact producer object identity`.

That missing binding is dispositive.

---

# 16. Repair ceiling

O3 does not redesign the repository.

The minimum future repair must establish an authenticated dependency-role source before or at reconstruction.

Lawful classes include, without selecting one here:

- bind required/negative dependency declarations into an identity-bearing producer-side projection;
- or bind an independently content-addressed dependency-role declaration/closure contract to the producer object ref;
- or rederive exact roles from an independently authenticated producer contract/payload where that derivation is complete and deterministic, then reject supplied declarations that differ.

A repair must **not**:

- turn every opaque lineage/provenance ref into a dependency;
- infer dependency role from mere reference presence;
- grant permission from provenance;
- redesign V558 semantics;
- change itemwise permission law;
- make negative dependencies positive causal facts.

After repair, hostile proof must include:

1. same producer object identity cannot carry two different required/negative role sets;
2. deleting/reclassifying a negative dependency before V558 build fails;
3. stale reconstructed declaration fails before ordinary M5 peer use;
4. intact role-complete bundle still resolves identically;
5. opaque lineage remains non-executable.

---

## Final disposition

ASTRA-006 is no longer merely an open codec question.

The accepted builder and first consumer are locally strong, but the reconstruction boundary does not authenticate dependency-role declarations to the producer identity.

A public role-stripped reconstruction can therefore pass ordinary V558 build/checksum/resolution and M5 exact re-resolution.

`FAIL__GT34_O3_ASTRA006_DEPENDENCY_ROLE_RECONSTRUCTION_DEFECT_PROVED`
