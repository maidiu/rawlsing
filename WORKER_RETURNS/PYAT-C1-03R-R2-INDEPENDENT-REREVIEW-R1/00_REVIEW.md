# PYAT C1-03R — OWNER FAIL-CLOSED R2 INDEPENDENT REREVIEW — R1

**Disposition:** `CHANGES_REQUIRED`

**Terminal:** `C1_03R_R2_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Reviewed implementation return:
`7f64493758f6b3b77d7e9ce1486c1324ff709edc`

R2 commission tip:
`88d94930179528ce37daac854a7f6a78f7f0f308`

Prior independent review:
`380a79cde63d9ee239e5812f89283e997e16da96`

Reviewer issue tip:
`f6e2b059883bee29b2dadfc1cc59df7a5a4c7735`

## Bottom line

All four prior fail-closed blockers are independently corrected:

- RVW-001 duplicate positive replacement rows: **PASS**
- RVW-002 negative serialization/schema boundary: **PASS**
- RVW-003 owner-unknown currentness: **PASS**
- RVW-004 checkpoint U replay: **PASS**

Both deliberately flagged readings are also correct at the accepted grain:

1. a **known, registered but never transitioned** dependent remains `CURRENT`;
2. a receipt declaring the **new noncurrent schema with zero noncurrent rows is refused**, not normalized.

However, the newly added three-state rollback witness is not lawful under the already-accepted consumed-determinant registration law. It obtains non-empty mixed A on v1→v2, v2→v3 and v3→v2 by pre-registering the same analytical product refs against **old_model, v2_ref and v3_ref simultaneously before those future revisions are consumed/current**.

That is future-authority pre-binding, the exact reachability manufacturing C1-03R previously removed.

The accepted one-step promotion fixture correctly binds the products only to `old_model`, the determinant they actually consumed. Under that lawful graph, v1→v2 is reachable; a later v2→v3 transition cannot affect those original refs because the owner graph is static and the replacement products are not dynamically re-registered into it. The R2 rollback fixture hides that continuation gap by installing future authority edges up front.

Therefore the four repairs themselves are accepted, but the R2 package cannot be approved because the commission explicitly requires a **genuinely mixed rollback witness under the same owner law** and preservation of the accepted architecture.

## RVW-001 — duplicate positive rows

**PASS.**

`AuthorityInvalidationReceipt.__post_init__` now checks `old.key in pairs` before the dict assignment.

Both attacks fail closed:
- duplicate source with same target;
- duplicate source with different targets.

The differing-target case can no longer last-write-win substitute a forged successor.

R/N disjointness and exact coverage of A remain enforced.

## RVW-002 — serialized negative fields and compatibility

**PASS.**

`NoncurrentDependentOutcome.from_dict` now:
- requires the `replacement_ref` key to exist;
- requires its value to be exactly `null`;
- rejects missing and non-null forms;
- does not synthesize null from absent serialized material.

`AuthorityInvalidationReceipt.from_dict` now treats the positive-only historical shape and the noncurrent schema as mutually exclusive forms.

When either new-schema marker is present, it requires:
- exact schema id `PRE553_AUTH40_SEMANTIC_AUTHORITY_INVALIDATION_NONCURRENT@1.0.0`;
- at least one noncurrent row.

Missing/forged schema on negative material fails. New-schema fields/schema on positive-only historical material fail. Clean positive-only legacy material retains the historical field set and identity.

### Flagged reading: new schema + zero rows

**APPROVED. Refusal is the correct law at this grain.**

The owner never emits the new schema for a positive-only receipt. Positive-only compatibility is specifically preserved by emitting the historical field set unchanged. Accepting:

`receipt_schema=<new schema>, noncurrent_dependents=[]`

would introduce a third representation the owner never emitted and would silently reinterpret positive-only material under the extension.

The R2 strict refusal directly implements the commission's requirement that incompatible new-schema presence on positive-only legacy material fail closed.

## RVW-003 — owner-unknown currentness

**PASS.**

A ref absent from `determinant_graph.known_dependent_refs` now yields:
- lifecycle state `NOT_GOVERNED`;
- reason code `OWNER_UNKNOWN_DEPENDENT`;
- no governing release.

The analytical resolver raises typed `OwnerUnknownDependent`.

Cache/resident object presence is not consulted.

This is distinct from an explicit noncurrent outcome, which remains `EXPLICIT_NONCURRENT` / `ExplicitNoncurrentDependent`.

### Flagged reading: known but never transitioned → CURRENT

**APPROVED at the declared registered-product grain.**

This is not the same inference that caused RVW-003.

In the C1-03R adapter, `known_dependent_refs` is populated by `AnalyticalDependencyRegistry` from exact `AnalyticalProductRegistration` objects. Such a registration requires at least one exact determinant authority the product actually consumed. The accepted fixtures then construct the lifecycle executor with the corresponding exact baseline authority as `initial_current_selection`.

So:
- owner-unknown + no transition = no authority to assert currentness → `NOT_GOVERNED`;
- owner-known registered baseline product + no lifecycle event invalidating it = baseline currentness remains unchanged → `CURRENT`.

This is also consistent with Astra's law that for known K, unaffected identities and current usability remain unchanged. It is not cache-presence inference.

This approval is bounded to the registered-product/current-baseline contract. It does not say that an arbitrary manually populated `known_dependent_refs` tuple can establish analytical truth outside that contract.

## RVW-004 — checkpoint U replay

**PASS.**

`AuthorityMaintenanceExecutor.from_checkpoint` now independently derives:

- `A = graph.affected(changed_authority_refs)`;
- `U = graph.unaffected(A)`;

and requires exact equality against both serialized sets before replaying the release.

The two required hostile shapes are materially correct:
- U omits a known sibling;
- U swaps/adds an owner-unknown sibling.

The hostile helper does not merely edit bytes. It rebuilds the invalidation, releases citing it, event-chain subject/parent refs, current-release pointers and checkpoint hash. Thus rejection is genuinely due to independent graph re-derivation, not a stale embedded hash.

## Shared owner law — promotion

**PASS.**

The existing mixed promotion witness remains lawful:

- product determinants are registered only against `old_model`, which they actually consumed;
- one replacement, two explicit noncurrent outcomes and one unaffected sibling are produced in one release;
- R ∩ N = ∅;
- R ∪ N = A;
- A ∩ U = ∅;
- A ∪ U = K;
- negative rows remain one generic disposition with exact grounds;
- sibling remains current/identity-stable.

## Shared owner law — rollback

**FAIL: C1-03R-R2-RVW-005 — FUTURE-DETERMINANT PREBINDING IN ROLLBACK WITNESS.**

The new `build_mixed_outcome_rollback_transition` constructs:

`model_revisions = (old_model, v2_ref, v3_ref)`

and then adds an authority edge from **every revision** to each of:
- replaced_product;
- noncurrent_product;
- downstream_product.

This graph is installed before the first promotion.

Therefore products that initially exist under v1 are declared dependent on v2 and v3 before either revision has been consumed/current.

That contradicts the accepted C1-03R registration law:
- registrations bind only determinants a product actually consumed;
- future/revised authority is never pre-registered;
- the revision enters only through the governed transition.

### Why this is load-bearing

The accepted one-step mixed fixture demonstrates the lawful shape: those products have authority edges only from `old_model`.

If the rollback fixture used that lawful graph:
- v1→v2 can have non-empty A;
- after the transition the lifecycle graph still contains only the original consumed determinant edges;
- v2→v3 changed refs do not match those old v1 authority edges;
- the replacement product returned by recomposition is not dynamically registered into the immutable `SemanticDeterminantGraph`.

So the second transition cannot obtain the claimed mixed A without either:
1. lawful post-transition determinant re-registration/rebinding of replacement products; or
2. future pre-binding.

R2 chose (2), which is forbidden.

The rollback court therefore proves that `promote_current` and `rollback_current` share mechanics on an artificially widened graph, but it does **not** prove a lawful three-state C1 analytical lifecycle under the accepted consumed-determinant owner contract.

### Required correction

Do not weaken the four R2 repairs.

Replace the rollback proof with a source-free three-state witness in which every graph edge is justified by an actually consumed determinant at the time that dependent exists.

If the present owner has no lawful mechanism to register/rebind the replacement product and its new consumed determinant for the next transition, return that exact bounded owner/registration gap to HQ instead of pre-binding future authorities.

## Preservation checks

No concrete regression found in:
- one generic noncurrent disposition;
- non-empty negative grounds;
- no DEFERRED/UNAVAILABLE/DELETED split;
- error→noncurrent prohibition;
- historical positive-only identity strategy;
- sealed-successor exact binding;
- decoy distinction;
- AuthorityCandidate identity;
- original mixed AT19 promotion witness;
- omitted-edge hostile;
- AT18 replay-grade separation.

`pre553_replay_audit.py` and `pre553_analytical_composition.py` are not modified by the R2 diff.

## Diff / provenance

`88d94930179528ce37daac854a7f6a78f7f0f308 -> 7f64493758f6b3b77d7e9ce1486c1324ff709edc`

is one commit ahead, zero behind.

The diff is confined to the commissioned terrain:
- `rawlsing_next/pre553_authority_maintenance.py`;
- `rawlsing_next/pre553_analytical_replay_dependency.py`;
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`;
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`;
- `rawlsing_next/tests/c1_at18_at19_fixture.py`;
- `WORKER_RETURNS/PYAT-C1-03R-OWNER-FAILCLOSED-R2/**`.

## Execution evidence

Worker execution records:

**160 passed, 0 failed, 0 errors, 0 skipped** over exactly:
- analytical replay dependency: 42;
- authority maintenance: 51;
- replay audit: 54;
- analytical composition: 13.

The counts reconcile against the committed test inventory:
- 39 functions + a four-case parametrized court = 42;
- 48 functions + a four-case parametrized court = 51;
- replay-audit remains the previously accepted unchanged 54-case court;
- 12 functions + the two-case AT07 parametrized court = 13.

No fresh runtime was available in this Browser/GitHub rereview lane. Proof grade is exact committed-source review plus reconciled worker execution evidence. The rollback blocker is source-level and does not depend on runtime behavior.

## Final

The owner fail-closed corrections RVW-001 through RVW-004 are accepted. Both flagged readings are accepted.

The package remains `CHANGES_REQUIRED` solely because the newly required rollback witness reintroduces future-determinant pre-binding and therefore does not satisfy the preserved owner-registration architecture.

**Terminal:** `C1_03R_R2_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
