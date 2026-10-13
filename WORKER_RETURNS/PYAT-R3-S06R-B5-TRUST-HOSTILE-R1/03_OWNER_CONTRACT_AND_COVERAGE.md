# Real B5/M2 owner contract — security coverage matrix

**Accepted canonical ref:** \`7f29aec36d24f16da52d84f17c00f08db3a55434\`.

Canonical owner:
- \`rawlsing_next/pre553_learned_product_lifecycle.py\`, blob \`a11c9eb73abab9be118ef4f0b6e325e676059f27\`; \`LearnedProductLifecycleExecutor\`.
- \`rawlsing_next/pre553_learned_product_release.py\`, blob \`f76c390665f06ef126968ccf1a6b2d816f43ae92\`; \`M2Repository\`, \`register_producer_subject\`, \`constitute_release\`, \`resolve_subject_exact\`, \`resolve_release_exact\`.

Prior actual independent coverage:
- N04 \`b5a6b6409c765d2aecb8c2f9c9ef9bd8fc6473c2\` — \`WORKER_RETURNS/PYAT-HQ282-N04-B5-OWNER-INTERFACE-CORRECTION-R1/02_METHOD_COVERAGE_AND_OWNER_GAPS.md\`.
- N04R \`fde95ee9275f9fe14b6868db363035757cffab48\` — \`WORKER_RETURNS/PYAT-HQ282-N04R-INDEPENDENT-CHECKPOINT-REVIEW-R1/02_OWNER_METHOD_AND_REPLAY.md\`, and \`04_RECOMMENDED_NEXT_CHANGE.md\`.
- P02R \`b3523bed5d751b24f0bf1fd111af4161727fe9b5\` — \`WORKER_RETURNS/PYAT-HQ282-P02R-C02J-INDEPENDENT-INTERFACE-VERIFICATION-R1/02_INTERFACE_FINDINGS.md\`.
- C02J overlay prior \`b5a6b6409c765d2aecb8c2f9c9ef9bd8fc6473c2\`, source-backed into that historical branch, but not adopted as canonical authority merely because it exists.

**Critical identity fact:** S06 \`TrustedCheckpoint\` constructs its own \`_events\`, \`_state\`, \`_epoch\`, \`_revoked\`. It imports no \`pre553_learned_product_lifecycle\`, \`pre553_learned_product_release\`, \`LearnedProductLifecycleExecutor\`, \`M2Repository\`, \`ExactRef\`, \`LearnedProductLifecycleEvent\`, \`CurrentSelectionReceipt\`, event-authority ref, producer subject, exact release, or M2 permission ceiling. No code in S06 hooks \`LearnedProductLifecycleExecutor\` or \`M2Repository\`. This is **not** owner enforcement.

## Previously identified entrypoint inventory, not covered by S06

| Accepted B5 route | N04/P02R coverage | S06 actual integration |
|---|---|---|
| \`stage_release\`, \`stage_protocol\`, \`register_product\`, \`publish_product\`, \`select_current\`, \`from_checkpoint\` | C02J overlay covered candidate subset; N04 repaired a checkpoint subject-ref mismatch | **NONE**: S06 own checkpoint, no B5 wrapper |
| \`record_recertification\`, \`declare_no_current\` | PARTIAL prior overlay checks | **NONE** |
| \`supersede_current\`, \`withdraw_product\`, \`declare_invalidation\`, \`record_rebuild_eligibility\`, \`link_rebuild\`, \`record_cache_materialized\`, \`record_cache_dropped\`, \`attest_gc_eligibility\`, \`record_payload_gc\` | UNWRAPPED prior overlay; first three independently reachable without verifier per N04R | **NONE**: similarly named S06 mutators only change S06's own state |
| \`M2Repository.register_subject\`, \`register_closure\`, \`register_release\`, \`register_representation\`, \`register_binding\` | UNWRAPPED prior overlay | **NONE** |
| \`constitute_closure\`, \`register_representation\`, \`publish_binding\` | UNWRAPPED prior overlay | **NONE** |
| \`register_producer_subject\`, \`constitute_release\` | C02J candidate overlay for two module-level functions | **NONE** |

N04R had already demonstrated representative raw B5 direct mutations reachable without its overlay; S06 does not invoke, intercept or change those functions. Do not infer "same method name" means real B5 protection.

## Native B5/M2 schema mismatch

At accepted B5 lines 2630–2697, \`LearnedProductLifecycleExecutor._checkpoint_payload()\` emits \`schema\`, \`contract_id\`, \`runtime_schema\`, \`repository_subjects\`, \`registered_release_refs\`, typed \`events\`, \`selection_keys\`, \`selection_receipts\`, \`no_current_receipts\`, \`selection_index\`, publication/validity/replay/rebuild/materialization/payload maps, typed invalidations/rebuild/GC, and determinant graph. \`export_checkpoint\` wraps it in \`{"checkpoint_payload": payload, "checkpoint_hash": semantic_hash(payload)}\`. \`from_checkpoint\` validates schema and contract identities, stages typed releases and validates exact registered-set coverage and selection state (lines 2699+); N04R finds residual history/state completeness issues.

S06 checkpoint instead \`{"checkpoint_payload":{"events":[arbitrary dict], "state":{plain maps}, "epoch":int, "revoked":[strings]}, "event_history_hash": sha, "state_projection_hash": sha, "event_count":int}\`. S06 \`from_checkpoint\` looks for \`event_history_hash\`, which accepted B5 checkpoint does not contain, and returns None; it does not deserialize native typed lifecycle events or M2 exact references. \`verify_trust_mode\` does not resolve source release permission, current selection receipt, event ordinal or M2 subject binding. Local \`select_current(selection_key:str, release_ref:str, current_epoch:int, trusted:bool)\` is not compatible with B5 \`select_current(selection_key_ref:ExactRef, release_ref:ExactRef, expected_previous_receipt_ref:..., event_authority_ref:..., event_rule_ref:..., selection_attestation_ref:...)\`. B5 enforces PUBLISHED+VALID, product-family and selection-scope equality at \`_selection_subject_ok\` (lines 1742–1755), and attaches typed event and receipt identities (lines 1760–1809). S06 does neither.

M2 \`resolve_release_exact\` is content-bound to accepted typed subject/closure/replay identity; S06 hashes and stores user-authored strings and a separate event table. There is no compatible S06 owner replay contract. Source-free author tests cannot close this.

## Native descendant semantics

Canonical \`LearnedProductDeterminantGraph.affected\` and \`unaffected\` (owner lines 1275–1304) and B5 invalidation receipts define dependency-aware propagation. S06 \`supersessions: dict[old,new]\` is neither that graph nor guaranteed transitive. A→B→C is enough to reject "multi-generation complete". Independent hostiles H11/H24 specify correct graph closure, protected sibling controls and cycles.

## Prior-source disposition

The N04R bounded checkpoint correction was independently accepted for the corrected subject resolution only, NOT full B5 trust. P02R/N04R flagged independent event issuer, permission source, revocation/as-of, concurrency and proof of accepted-owner event replay as outstanding. S06 does not establish any of them. Preservation of those scientific holds is mandatory.
