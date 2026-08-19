# M4 hostile test oracle

Authority: `M4_SCR5578_MIXED_PRODUCER_FINAL_SEAM@1.0.0`

All tests are fail-closed. A test marked PASS means the final seam contract has an exact deterministic disposition for the hostile case; it does not authorize production implementation.

## M4-H01 — wrong producer head or contract seal

**Attack:** substitute a different SCR553/SCR554 head, a different SCR555 local contract, a different M2 package, a different SCR556 local contract, a different M3 result blob, or a different frozen SCR5578 contract hash.

**Expected:** reject binding as producer/final-seam integrity failure. No latest/current-branch repair.

**Disposition:** PASS.

## M4-H02 — V555 B1 smuggled into route identity

**Attack:** append B1 ID as an eighth semantic route field.

**Expected:** reject. B1 is the V554->V555 permission/replay envelope and is not a V555 route participant or route-identity member.

**Disposition:** PASS.

## M4-H03 — V555 F1 collapse

**Attack:** two routes share channel/receiver fields but have different canonical SCR554 F1 IDs; collapse them into one route.

**Expected:** reject. `EXACT_V554_F1_REF` is field 1 of the canonical seven-field tuple; different canonical F1 means different route.

**Disposition:** PASS.

## M4-H04 — V555 locator replaces tuple equality

**Attack:** accept a route because locator/hash matches while the seven-field tuple differs or cannot be recovered.

**Expected:** integrity failure. Locator is nonsemantic and must reverse to exact producer identity.

**Disposition:** PASS.

## M4-H05 — inherited F2 re-owned by V555/V557/V558

**Attack:** copy/rename/re-evaluate an inherited V554 F2 as V555 or repository semantics.

**Expected:** reject. F2 remains V554-owned exact-reference-only.

**Disposition:** PASS.

## M4-H06 — V556 participant route re-ID

**Attack:** replace exact V555 participant route identity with a new V556/M4 locator identity, run ID, slot ID, label, or normalized route key.

**Expected:** reject. Exact accepted V555 route identity is the sole base participant identity.

**Disposition:** PASS.

## M4-H07 — V556 n-ary truncation

**Attack:** a rule requires three participant occurrences; package or resolve only two and emit a positive two-party relation.

**Expected:** `INTEGRITY_FAILURE` or producer-governed invalid/unresolvable participant outcome as applicable; never a smaller positive relation.

**Disposition:** PASS.

## M4-H08 — V556 order/multiplicity corruption

**Attack:** reorder an ordered rule, deduplicate repeated authorized occurrences, or rewrite multiplicity indices.

**Expected:** reject. Exact V556 rule owns role/order/cardinality/multiplicity.

**Disposition:** PASS.

## M4-H09 — co-resolution invents V556

**Attack:** two V555 routes resolve in the same query/context; infer interaction/topology.

**Expected:** no new V556 object. Co-resolution is not V556 authority.

**Disposition:** PASS.

## M4-H10 — source composition from provenance

**Attack:** use a common provenance ancestor, time, geography, endpoint, or stratum to pool/compose distinct source universes.

**Expected:** reject positive composition absent exact operation-specific composition authority. Default remains `NONE_BY_DEFAULT`.

**Disposition:** PASS.

## M4-H11 — V557 permission widening

**Attack:** producer allows `{REVIEW}`; V557 records `{REVIEW, CONTEXT}`.

**Expected:** `INTEGRITY_FAILURE__FORBIDDEN_PERMISSION_WIDENING`.

**Disposition:** PASS.

## M4-H12 — resolver permission widening

**Attack:** V557 allows `{REVIEW, CONTEXT}`; resolver emits `{REVIEW, CONTEXT, ACTIVE_CAUSAL}`.

**Expected:** fail closed. Resolver may only narrow.

**Disposition:** PASS.

## M4-H13 — dependency permission inheritance

**Attack:** root is allowed active causal use; an interpretation-critical dependency is review-only; inherit root permission into dependency.

**Expected:** reject. Permission is item-wise for every root and dependency.

**Disposition:** PASS.

## M4-H14 — repository presence as permission

**Attack:** publish/use an item merely because it exists in StructuralPriorRepository or a collection is globally ready.

**Expected:** reject. Presence/readiness grants no permission.

**Disposition:** PASS.

## M4-H15 — missing positive closure

**Attack:** remove one required positive authority/content dependency while raw producer directories are absent.

**Expected:** `INTEGRITY_FAILURE`; no raw-stage, network, fuzzy, latest, or label repair.

**Disposition:** PASS.

## M4-H16 — missing negative closure

**Attack:** omit an interpretation-critical denial/limit/noncomparability/unknown-authority reference while keeping the positive object.

**Expected:** `INTEGRITY_FAILURE`; positive publication/resolution cannot silently survive loss of negative authority.

**Disposition:** PASS.

## M4-H17 — bare hash or mutable locator

**Attack:** closure leaf has a content hash but no exact immutable deterministic resolution contract, or locator points to mutable latest/current content.

**Expected:** unsatisfied closure -> integrity failure.

**Disposition:** PASS.

## M4-H18 — role/order/cardinality normalized by repository

**Attack:** V558 serializes edges and then treats serialization order or simplified binary shape as semantic structure.

**Expected:** reject. Producer/reference-contract roles, semantic order, cardinality, and multiplicity must be preserved exactly.

**Disposition:** PASS.

## M4-H19 — PSEPF/reverse-lane smuggling

**Attack:** insert PSEPF / PositionedSubjectEmpiricalPossibilityField, V3EmpiricalPossibilityInput, ActorComparatorReceipt, or rendered persona as StructuralPriorRepository root/semantic edge.

**Expected:** forbidden reference class; reject package/resolution.

**Disposition:** PASS.

## M4-H20 — audit receipt becomes semantic prior

**Attack:** use DiscoveryResultReceipt or ReplayReceipt as a structural semantic root or authority substitute.

**Expected:** reject semantic use; audit-only status preserved.

**Disposition:** PASS.

## M4-H21 — valid-empty / missing / integrity collapse

**Attack:** rewrite physical missing dependency or broken index as producer `VALID_EMPTY`, or rewrite producer missing/noncomparability as repository integrity failure without preserving producer state.

**Expected:** reject. Packaging integrity and producer semantic state are separate typed dimensions.

**Disposition:** PASS.

## M4-H22 — observed zero becomes missing

**Attack:** rewrite authorized observed numeric zero as missing/denied/empty.

**Expected:** reject. Producer measurement semantics survive packaging/resolution.

**Disposition:** PASS.

## M4-H23 — latest/fuzzy/raw/network/LLM repair

**Attack:** exact reference fails; resolver chooses latest version, nearest time, similar label, network result, LLM inference, embedding match, random/default candidate, or filesystem-first row.

**Expected:** deterministic failure/typed unresolved result; no repair.

**Disposition:** PASS.

## M4-H24 — nondeterministic equal-rank tie

**Attack:** singular resolution has equally ranked exact candidates and no exact precedence authority; choose first row or lexicographic winner semantically.

**Expected:** `AMBIGUOUS_EQUAL_RANK_AUTHORITY` / corresponding resolution ambiguity. Lexicographic order may serialize only.

**Disposition:** PASS.

## M4-H25 — raw producer directories removed

**Attack:** delete/withhold raw V553/V554/V555/V556 stage directories from the runtime environment after building a complete immutable package.

**Expected:** same semantic resolution, identity, state, permission, role/order/cardinality/multiplicity, receipt, and replay result. Any attempted raw-stage fallback is failure.

**Disposition:** PASS.

## M4-H26 — partial atomic publication/repository bundle

**Attack:** expose roots before required manifests/locators/reference graph/index/policy/closure are atomically available.

**Expected:** fail closed as incomplete bundle; no partial semantic visibility.

**Disposition:** PASS.

## M4-H27 — deterministic replay mutation

**Attack:** same exact immutable repository/index/query/policy/generated bindings produce different SelectionRecords, selected set, typed state, receipt, fidelity, refresh metadata, or RSC.

**Expected:** replay integrity failure.

**Disposition:** PASS.

## M4-H28 — M5 receives invented RSC instance

**Attack:** M4 supplies a fabricated `context_id`/`context_content_hash` without an actual resolver-produced RSC instance.

**Expected:** reject. `M5_RSC_HANDOFF.json` defines the machine-verification signature only; M5 must receive a real exact RSC instance satisfying it.

**Disposition:** PASS.

## Final oracle

All hostile cases are closed without semantic amendment to SCR553/SCR554/SCR555/SCR556/SCR5578.

Final M4 token: `M4_ACCEPTED__SCR5578_EXACT_CONTRACT_CLOSED`.
