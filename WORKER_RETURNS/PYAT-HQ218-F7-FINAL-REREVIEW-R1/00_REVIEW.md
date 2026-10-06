# PYAT HQ218 — F7 FINAL HOSTILE REREVIEW — R1

**Lane:** `PYAT-HQ218-F7-FINAL-REREVIEW-R1`  
**Role:** Browser/GitHub independent hostile reviewer — READ-ONLY / NO REPAIR  
**Commission tip:** `7867a777b1b26024ec620b0e82ea9ffdb9fb6ddc`  
**Exact candidate:** `agent/rabochii-pyat-hq217-f7-final-bounded-repair-r1 @ 136223506eaaf8d7c031a2822f2bfb6ac5bd420e`  
**Prior hostile rereview:** `be0ae0f1e3dfea27b1520e81b30c781412e30c92`  
**Accepted contract:** `c57a96897788108db7b194e4e51691d1ca8ab729`  
**Forward law read from exact control object:** HQD-216 @ `e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2`

## Disposition

`F7_FINAL_BOUNDED_REPAIR_PARTIAL__NAMED_DEFECT`

HQ217 closes substantial portions of the HQ215 defect set, but it does **not** close F7's authority chain. Three reachable fail-open/bypass defects remain:

1. **RR-02B / permission scope:** `resolve_required_authority(... require_use_scope=True)` treats an absent `target_use_refs` scope entry as success. The complete ExactRef comparison is correct **when a scope entry exists**, but no scope entry silently becomes unrestricted. This affects both TEMPORAL_COMPARABILITY and TARGET_USE_PERMISSION resolution.
2. **RR-03:** `temporal_identity_contract_ref` is hash-bound only to caller-supplied material. The separate TEMPORAL_EVIDENCE snapshot is never linked to that ref/material. A caller can mint arbitrary `{"identity_surface_jointly_satisfied": true}` material, hash it, mint the matching ref, and pass the identity gate. The caller boolean was removed as authority; caller-authored material replaced it.
3. **RR-04:** the source-relation owner path is not actually adjudicated. Production accepts `source_relation_resolver: Any`, calls only `resolver.resolve_exact(ref)`, and checks only that the returned object's `ref` matches. It never requires a real `SourceRelationResolver`, never calls the owner's positive `decide(...)` path, and never checks the resolved relation's decision, relation kind, exact source pair, operation scope, target use, or relation authority. A stub resolver, a DENIED exact relation, a wrong-kind relation, or a relation for the wrong pair can satisfy this half of the gate while an independent positive SOURCE_EQUIVALENCE snapshot satisfies the other half.

These are implementation defects, not evidence gaps and not a reason to reopen F7 architecture.

## Mandatory attack results

### RR-01 — requirements material

**SUSTAINED at the exact commissioned defect grain.**

`comparability_requirements_ref` is required, the supplied material's canonical semantic hash must equal its content hash, the consumed requirement-result tuple is derived from the bound material, and a contradictory caller duplicate is refused. The old “decorative ref + independent result tuple” route is closed.

This review does not invent a new owner for `comparability_requirements_ref`; the accepted contract names it as an ExactRef but does not separately name an authority owner in the way it explicitly does for temporal identity and source equivalence.

### RR-02 — complete governed-use identity

**PARTIAL / BLOCKING DEFECT.**

The new `_scope_covers_governed_use` compares the complete `kind + object_id + content_hash` identity. Same object_id/different hash does not match. A bare object_id string does not match.

But `resolve_required_authority` lines 491-494 execute the exact comparison only if `scope.get("target_use_refs") is not None`. If the scope entry is absent, `require_use_scope=True` succeeds without proving any governed-use coverage. `require_positive_authority` is called earlier without `target_use_ref`, so no owner-level fallback check closes the hole.

Thus:
- wrong exact scoped use → refused;
- bare scope token → refused;
- **missing use scope entirely → accepted**.

That is not fail-closed governed-use identity.

### RR-03 — temporal identity authority

**FAIL / BLOCKING.**

The accepted authority contract names `temporal_identity_contract_ref` as an ExactRef owned by TEMPORAL_EVIDENCE. HQ217 adds `temporal_identity_contract_material`, but the only binding is:

`semantic_hash(caller_material) == caller_ref.content_hash`.

Separately, F7 resolves a TEMPORAL_EVIDENCE authority snapshot, but it does not scope or bind that snapshot to the identity ref/material. The material is also not validated as an owner-produced identity object or as the required composition of identity surfaces. Production merely reads:

`bool(identity_material.get("identity_surface_jointly_satisfied"))`.

Therefore the following source-level counterexample remains reachable:

- caller chooses arbitrary mapping with `identity_surface_jointly_satisfied: true`;
- caller computes its hash and supplies a matching arbitrary ExactRef;
- unrelated positive TEMPORAL_EVIDENCE authority remains present;
- hash binding passes;
- identity gate passes.

The value is no longer taken from the top-level boolean, but it is still caller-authored and unverified.

This also means HQ217 has not lawfully retired the accepted residual `IDENTITY_CONTRACT_INSTANCE_MISSING`; it has substituted request-local material for an owner-resolved instance.

### RR-04 — source-equivalence owner path

**FAIL / BLOCKING.**

The accepted contract's two-path law says the existing source-relation owner resolves an exact positive SOURCE_EQUIVALENCE result and the temporal owner consumes that already-resolved result.

The actual owner API distinguishes:

- `SourceRelationResolver.resolve_exact(ref)`: exact object lookup only;
- `SourceRelationResolver.decide(...)`: relation kind / exact pair / scope / target use selection plus positive relation-authority adjudication;
- `_validate_positive(...)`: checks `decision == AUTHORIZED`, replay identity, expected authority operation, exact relation authority kind/scope.

F7 uses only `resolve_exact`. Worse, the request field is `Any`, so a duck-typed stub with `resolve_exact` can return an object carrying the requested ref. F7 then appends a POSITIVE source-relation resolution record without checking the relation's decision/kind/pair/scope/use/authority.

The lawful court fixture does build one genuine content-addressed `SourceUniverseRelation` through the accepted factory. That proves a good relation **can** be supplied; it does not prove production **requires** one. There is no court witness for a stub resolver, a DENIED relation, a wrong relation kind, or a wrong exact source pair, and the fail-capability audit does not mutate RR-04.

### RR-05 — measure binding

**SUSTAINED by exact source inspection.**

`quantity_surface.measure_ref` is mandatory whenever a quantity surface is present, both ExactRef/AuthorityRef-shaped exact forms are parsed, its key is compared with the resolved measure authority set before the delta is computed, wrong/absent measure refuses, and the supplied exact measure identity is serialized in the receipt.

### RR-06 — missing order-basis ref

**SUSTAINED.**

For an authorized order disposition with no `temporal_order_basis_ref`, the producer records the accepted `TEMPORAL_ORDER_BASIS_AUTHORITY_REF_ABSENT` reason. Precedence selects `TEMPORAL_INSUFFICIENT_AUTHORITY`, and the cross-field validator narrowly accepts null basis only for exactly that state/reason pair.

### RR-07 — total precedence

**SUSTAINED at the named partial-order defect.**

The partial-order guard now runs only when the selected state is itself comparable. A higher-priority identity/authority/etc. terminal is emitted rather than converted into an exception. No comparable overlap/no-direction state is manufactured over a higher-priority negative.

### Permission refs

**PARTIAL / BLOCKING through the same RR-02B root cause.**

Every supplied `target_use_permission_refs` element is iterated and resolved; no extra element is silently ignored. However each resolution uses the fail-open `require_use_scope` behavior above. A positive TARGET_USE_PERMISSION snapshot with no `target_use_refs` entry can therefore pass without proving permission for the governed use.

## Productive adequacy under HQD-216

The arithmetic/receipt machinery remains productive in shape: exact positive delta, exact zero, decrease, partial-order no-direction, and cross-universe receipt construction are not collapsed away. The repairs did not make F7 a refusal-only machine.

But **lawful positive productive adequacy is not yet proved**, because the positive fixture still depends on unverified request-local temporal identity material, and the cross-universe path does not require a positive owner decision. HQD-216 permits synthetic fixtures; it does not permit synthetic material to impersonate missing owner authority.

This is a local F7 implementation defect, not an upstream estate-occupancy defect.

## Noncollapse invariants

The exact candidate still preserves:

- 12 relation states, no thirteenth state;
- 19 authority kinds, including the single TEMPORAL_COMPARABILITY kind and matching ceiling;
- exact-zero direction law: int/Decimal/Fraction only, exact sign comparison, floats refused, no deadband/tolerance/epsilon arithmetic;
- 3+ anchors refuse pre-receipt;
- prior-F7 mapping remains live;
- negative/refusal states serialize NOT_COMPARABLE;
- the live frozen backfill surface is consulted;
- no F8 consumer power, source selection, interpolation, trajectory, causation/currentness, scalar temporal pressure, pooling/equivalence creation, or actor/person power is introduced.

## Court authenticity and environment

The worker is correct not to call the 82-ID base-vs-new slice “82 semantic defects.” I sustain that caveat.

However the exact committed court does **not** match the per-file counts in HQ217's environment report:

- repaired F7 court: 79 test functions; six parametrizations expand by 17 extra cases → **96 collected items**, not 98;
- M1 court: 24 test functions; one four-case parametrization → **27 collected items**, not 25;
- total remains **123**, so the aggregate can coincide while the per-file provenance is wrong.

The base F7 court reconstructs to 83, matching the base report. The repaired court adds 13 ordinary test functions, therefore 83 → 96.

The claimed fail-capability block also says “all verified,” but its listed mutations cover RR-01/RR-03 material hash binding, RR-02 bare-token scope, RR-05 measure comparison, RR-07 partial-order guard, and RR-01 surface derivation. It does **not** independently break RR-04 owner adjudication, RR-06 basis handling, or permission-ref resolution.

HQ217's own interpreter record is otherwise internally consistent: CPython 3.11.3 / pytest 9.1.1, non-governed throwaway environment, no full-suite claim. The historical HQ214 3.11.3-versus-3.12.14 conflict remains correctly recorded rather than fabricated away. No GitHub workflow run exists for the candidate commit.

The exact-zero result is independently source-grounded beyond substring theatre: executable numeric flow accepts only int/Decimal/Fraction, computes an exact difference, and defines canonical zero as exact sign == 0. This review did not execute a local AST tool because the commissioned lane is Browser/GitHub-only.

## Bounded repair set

1. Make `require_use_scope=True` require a non-null governed-use scope entry and exact complete-ref coverage; absence must be SCOPE_MISMATCH / insufficient authority.
2. Bind `temporal_identity_contract_ref` to actual TEMPORAL_EVIDENCE-owned identity material. If no owner-resolvable identity instance exists, retain the accepted missing-instance blocker; do not authorize caller-minted identity material.
3. Consume an actual positive source-relation owner decision for SOURCE_SEMANTIC_EQUIVALENCE. A plain exact-object lookup is insufficient. The owner decision must bind relation kind, exact source pair, operation scope/use/effective scope, exact relation ref, and positive authority.
4. Add discriminating court witnesses for missing governed-use scope, self-minted identity material, stub resolver, DENIED relation, wrong relation kind, and wrong source pair; fix per-file collection accounting and the overbroad fail-capability claim.

No new authority kind, relation state, reason code, public object family, or architecture reopen is required by these findings.

`HQ218_F7_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
