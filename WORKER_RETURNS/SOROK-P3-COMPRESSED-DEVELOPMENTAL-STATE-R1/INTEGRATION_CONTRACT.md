# P3 integration contract — candidate sourcefree engineering

Protected start c852d7516e23fcb6cf2215e9be7c5fa268503516. Governing user launch is pinned in CHECKPOINT.json. STANDING_DISCIPLINES.md governs HQ and every commission. E1/S1 remain candidates until independent input review; no native science is selected. These interfaces freeze mechanical dependencies so independent implementation need not wait on source review.

## Actual seam and retained owners

Keep #704 contracts/BatchEngine/RecursionCycle/P2Owner and #697 S39–S47 unchanged. New `p3.P3Owner` implements the same DevelopmentOwner protocol by composing an actual P2Owner and a normalized psychological sidecar under that P2 session's state_root. There is exactly one P2 actor/root/branch/clock; no independent B1 actor root. The wrapper's snapshot hashes the actual P2 snapshot plus the sidecar's committed state head. Its input proposals remain the accepted P2 grammar. No compression/rule/context field is injected into P2 circumstances.

A frozen, source-hashed owner configuration maps proposal IDs to exact proposal hashes and supplemental test-only context/evidence/rule selectors. This configuration is not model-writable. Native P2 admission/perception and actual material availability remain independently read. Scope-specific response computation cannot create tools/resources/permissions or claim a changed native action merely because a candidate response exists.

Initial positive semantics selectively adapt B1's executed `mode_for`/scoped mediator predicates: actual P2 experience + explicitly sourcefree historical participation can create an actor-bound mediator under a separate frozen TEST_ONLY registry. A later actual P2 event's response evaluator reads the committed record and commits a computed sourcefree response transaction. Distinguish that response from an enacted native P2 action; retain actual performed/access/C9 evidence. Contradictory streams coexist and context may select eligible streams at read time without a scalar winner or lifecycle mutation. No psychological effect is emitted in production mode.

## Files and write ownership

All new implementation lives in this return's `p3/`, with tests in `tests/`. HQ owns __init__.py, p3_owner.py, test_rules.py, projections.py and integrated/cold/resource tests/CLI. Storage worker owns only p3/state_store.py, tests/test_state_store.py and evidence/storage/. Compression worker owns only p3/compression.py, tests/test_compression.py and evidence/compression/. The two input reviewers own separate return roots. No worker edits #704/#697, sourcepack, production registry, protected tree, other workers' files or PROGRAMMA.

## Normalized storage API (mechanical worker)

Use plain JSON mappings, shared canonical/digest conventions and `RecursionRefusal` (or a ValueError subclass convertible by HQ). No psychological rule content belongs in this store. API:

- `PsycheStore(path, *, binding, registry_hash, source_hash)`; binding has exact nonempty root/actor/branch. Reopen requires identical binding/schema/registry/source. Normalized indexed tables; no whole life/checkpoint rewrites.
- `head() -> dict`: O(1) committed record-state hash/count. Initial head derives binding/registry/source. Chain each newly inserted immutable record's canonical content/hash; zero-record response leaves record head unchanged.
- `query(*, project, counterpart, as_of) -> list[dict]`: indexed actor-local exact-scope records effective at as_of, deterministic order, verify row content hashes. Preserve multiple contradictory records. No automatic lifecycle changes.
- `get_operation(operation_id) -> dict | None`; durable body includes proposal_hash, expected snapshot, plan_hash, base_before, psyche_before, phase, base_result, effects_receipt, result as available.
- `pending() -> list[dict]`: unresolved operations only, excluding COMPLETE; owner blocks unrelated work until exact pending operation reconciles.
- `reserve(operation_id, *, proposal_hash, expected, plan_hash, base_before, psyche_before, plan) -> dict`: BEGIN IMMEDIATE, stale-head check, immutable request binding; phase PREPARED. Exact repeated request returns same row; mismatch refuses.
- `save_world(operation_id, base_result) -> dict`: PREPARED -> WORLD_COMMITTED, immutable exact result; repeated same result idempotent.
- `commit_effects(operation_id, *, records, response, event_binding, compression=None, projection=None) -> dict`: requires WORLD_COMMITTED, exact bound root/actor/branch/source/registry/rule/causal parents/time, immutable record IDs/hashes and expected head. Atomically append all valid records, response, receipt and phase PSYCH_COMMITTED. Any invalid target rolls back all. Replay exact input returns same receipt; mismatch refuses. `event_binding` includes actual P2 event ID/hash/clock and owner identity, checked against stored base_result. Optional `compression` and `projection` evidence are bound into the request hash and stored in the receipt (with content hashes) before the receipt hash, so they survive recovery. No free-standing actor-state mutation API. Records use explicit TEST_ONLY provenance; CREATE only, CAN-011-shaped MEDIATOR/TENSION/PRACTICE; no automatic updates or native claims. Every record includes root, actor, branch, project, counterpart, record_id, kind, payload, rule_id/version/hash, registry_hash, source_hash, effective_from, causal_parents, grade and hash (digest excluding hash). Nonempty parent refs include the actual admitted event hash.
- `finish(operation_id, result) -> dict`: PSYCH_COMMITTED -> COMPLETE with immutable serialized RealizedEvent. Exact replay returns same; mismatch refuses. Validate result identity and linkage to durable receipts: require an effects-receipt hash link, require `receipt_ref` to equal `P3_PSYCH:` plus the receipt response hash, and when the receipt carries projection/compression evidence require the result's accessible/actor surface and compression evidence to match it exactly.
- `close()`. Expose measured row-read/write counters or SQLite trace-based evidence for targeted vs full reads; no artificial timing promises.

Store schema must bind complete rule descriptors via frozen registry identity, and reject a record's rule ID/version/hash not in the owner-supplied plan's permitted rules. Owner evaluates rule-specific semantics separately. Implement recoverable phases, not an always-refuse pending operation that cannot be reconciled.

## Recoverable cross-store protocol (HQ owner)

Under a P3 root lock, validate expected combined state and all proposal/config/source/registry/authority fields BEFORE any effects; call unchanged P2 preflight for all proposal fields. Reserve P3 PREPARED with deterministic base operation ID. Call unchanged P2.realize using saved base_before. Persist actual base result, then commit the source-bound psychology response/effects, then complete the P3 RealizedEvent. On restart:

- PREPARED with no base operation: exact original base operation may start once if original material snapshot still matches.
- PREPARED with a completed base operation: read its exact immutable receipt and material after-state; save_world without repeating P2 effects.
- Base reservation without result: explicit ambiguous HOLD; never blindly reissue.
- WORLD_COMMITTED: recompute/revalidate exact deterministic sourcefree plan against stored actual event/access and prior head, then commit once.
- PSYCH_COMMITTED: reconstruct/finish result from durable base/effect receipts without new effects; compression/projection evidence is read from the receipt, never recomputed.
- COMPLETE: return exact prior result subject to #704 replay identity semantics.

Fail closed for wrong root/actor/branch/time/source/rule, changed plan, changed material/psychological state or unreconciled foreign operation. Test crash boundaries in real subprocesses. Forks require separately bound roots; no inherited record from another root is silently admitted.

## Compression API (independent mechanical worker)

- `preflight(spec, *, identity, proposal, catalog) -> dict` returns detached validated spec; no effects.
- `bind(spec, *, identity, proposal, catalog, realized) -> dict` returns content-addressed metadata after validating actual P2 event/access/interval receipts. Never writes world/psychology.

All arguments are plain JSON documents. `identity` is StateIdentity.document(); `proposal` EventProposal.document(); `realized` RealizedEvent.document() from unchanged P2. `catalog` maps exact source refs to canonical source documents with `hash=digest(document excluding hash)`, grade SOURCEFREE_TEST_ONLY, root/actor/branch, kind, from_clock/to_clock and data. Lookup verifies exact source bytes/hash and owner identity/time. Source documents are explicitly sourcefree authority, never generated proof of original witnessed acts.

`spec` fields: envelope_id, proposal_hash, representation_form, represented_window {from_clock,to_clock,coverage_basis}, recurrence_basis_refs, participation_refs, material_relation_refs, observed, unobserved, selection_basis. Supported forms: SINGULAR_OCCURRENCE, REPRESENTATIVE_EPISODE, ACCUMULATED_INTERVAL, RETROSPECTIVE_CRYSTALLIZATION. Required refs differ by form: representative needs separately sourced recurring relation; interval needs bounded interval source; retrospective needs fixed historical source. All need actual present event binding and actor participation/access for any claim that this actor experienced it. Reject unsupported fields/global multiplier/fabricated witness counts/automatic effects. Allowed temporal coverage cannot manufacture event IDs. Owner binding verifies actual P2 event actor/branch/hash, interval receipt where claimed, and accessible actor perception; absent access yields explicit HELD evidence, never a positive participation assertion. Envelope preserves precise observed/unobserved scope and actual vs represented history separately. Return includes hashes of source refs, actual native event ref/hash, actual interval/perception refs, identity, representation_form and no psychological effects. Representativeness describes selection, not repeated acted event admission. This layer never authorizes ADP016/017 memory or claims.

## Integrated acceptance retained in full

At least two actual 3–5-event batches through RecursionCycle -> BatchEngine -> P3Owner -> unchanged P2Owner. Primary persisted mediator -> later computed response on same actual P2 root, matched no-mediator control. Additionally all user A–H contrasts: history, material, interlocutor, coexistence, stable no-new-record event, sourced condensed episode/interval, actor/user/objective opacity, identity/version/source/authority failures + cold/idempotency/crash/sever/restore. Keep #704 regressions. Measure bytes/actor/event/record, targeted/full reads, context bytes, event/batch/cold latency, calls/batch and provenance overhead. Test-only response selection is explicitly separate from material feasibility and native performed action. Final new-runtime independent exact-SHA S2 review remains mandatory. No receiving or native claim from input review alone.

## Optional D02 read-only situated context (candidate)

`p3.situated_context.build_situated_context(owner, *, expected=None, event_id=None, expected_source_closure=None, plan=None) -> dict` is an additive, read-only consumer over the existing `P3Owner`/`PsycheStore` and actual world/actor readers. It is not a second owner, store, scheduler, rule or world writer.

- With `plan`, it validates the plan root/actor/branch/source/registry/grade/hash and permitted rules, then reads `PsycheStore.query(project, counterpart, as_of=owner clock)` and runs the existing `projections.activate` with a context whose `actor_observed` is derived only from actual focal `read_actor_access`, never a caller boolean. The result exposes bounded eligible modes/hashes, withheld records, active vs latent contradictions, exact source/registry hashes and an unchanged store head. It never writes a target, memory, immediate response, performed action or native claim. `native_rule`/`memory_formation` remain `MISSING_RULE`.
- Without `plan`, acquired state is `NO_PLAN_SCOPE`; the selector still reads only the P3 head, not records.
- B02 current-period ingress is optional and exact: when an actual B02 plan is established, the current logical clock is mapped through its declared anchor/ticks, `read_material_period` must return the same logical tick, and the bounded current period/employment/typed `p3_interval_span` plus exact B02 source hash are included. Historical dates are not treated as current state; absent/outside/non-aligned/holder-mismatch cases return an explicit hold. The B02 materializer/interleaving remains outside this contract.
- The selector returns a detached context suitable for the existing `RecursionCycle` provider `context`; the provider is transport, not actor cognition.
- Refusals include stale/foreign state, pending P3 operation, plan override keys, source-closure change, source/module identity, and tampered store records. A changed selected reader or plan scope changes the context hash/readset.
- Limits: objective material availability is not actor perception; options are sourcefree input labels, not choices; contradictions are not resolved by a native rule; file-level D02 source closure is not an authenticated root; old-code/pin roots require fresh fixtures; no native CAN/ADP/Pyat, rights, human or protected merge is issued.

## Optional D03 sourcefree immediate speech uptake (candidate, B addendum)

`p3.immediate_uptake.build_immediate_uptake(owner, *, speech_event_id, child_id, utterance_receipt, plan, expected=None, expected_source_closure=None, expected_speaker_actor_id=None) -> dict` is a read-only adapter over the actual C04 `parent_speech.read_child_uptake`/writer receipt, the actual C01 speaker registration and the existing P3 `PsycheStore.query` + `projections.activate` + `test_rules` response-rule machinery. It is not a new owner, store, scheduler, rule, world writer or target writer.

- It requires the actual child `speech` receipt and public uptake; co-presence alone, a caller boolean, a handmade utterance dictionary, a self-only parent receipt or an unperceived/severed event does not produce an immediate response. A child-unperceived speech yields `HELD_NOT_PERCEIVED` with no speech text, no prior modes and no store write; the parent's prior decision remains.
- The prior organization is the sealed P3 plan/record scope (`vertical:project`/`vertical:counterpart` in the current sourcefree fixture), explicitly **not** the registered parent identity. The actual parent speaker/role/event is a separate `speech_scope`; the two scopes are never silently renamed into one maternal record.
- The immediate response uses the existing P3 response rule descriptor and `projections.activate`; it returns bounded allowed modes/streams and active contradictions, with `material_feasibility = NOT_EVALUATED_WORLD_PROPOSAL_SEPARATE`. Physical material feasibility does not suppress a legitimate attempt or false-belief candidate.
- It never writes a durable target/memory/acquired state: `durable_formation.status = MISSING_RULE`, `written = false`, `target_candidate = null`; store head before/after must match. `native_rule`/`native_action`/`memory_formation` remain held.
- It returns an exact D03 reader source closure and expected-closure refusal, and a detached input suitable for the existing `RecursionCycle` provider context. The provider remains transport; a later P3 response on the same prior organization is a separate actual computation.
- Limits: C04 is consumed at its standalone writer/child-uptake seam, not the normal P4/P6 C04 consumer under Pair3 repair; D03 does not establish a live P6 join, parent-authored act, native CAN-008 rule, human/actor/source rights or protected acceptance. Full D04 remains dependency-held.

### B D02 current-period addendum

The optional D02 current-period ingress uses the actual incremental B02 `read_period_plan` + `period_progress` + `read_material_period` + `p3_interval_span` path. `period_progress.current_date` is the current date; no private anchor-date arithmetic is substituted. The declared S46 tick-day basis is read from the plan; a non-day-aligned current clock holds, and no elapsed workshop tick is silently relabeled as a year. The B02 materializer/interleaving and historical as-of remain outside this contract.
