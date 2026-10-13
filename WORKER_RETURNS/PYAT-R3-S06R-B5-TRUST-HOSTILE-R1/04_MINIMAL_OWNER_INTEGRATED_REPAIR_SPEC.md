# S06R — minimal owner-integrated security repair specification

This is a **patch specification only**. The review must not modify frozen author code or production owners. A future worker must implement on a distinct candidate branch with test-first hostiles retained from \`01_FROZEN_INDEPENDENT_SECURITY_HOSTILES.json\`; independent reviewer must examine execution results from a qualified local isolated worktree.

## Gate 0 — Do not permit S06 as a trust authority

1. Rename/classify the present \`TrustedCheckpoint\` as an **in-memory SOURCE_FREE_TOY_CHECKPOINT**, not B5/M2 trusted enforcement. Do not accept its \`trusted=True\` or strings as an authority. Maintain internal hash/replay development checks as **LOCAL_REPLAY integrity**, and refuse protected modes.
2. Reject any production consumption or CURRENT selection through this module. Preserve existing B5/M2 accepted behavior until a complete owner-issued guard exists.

## Gate 1 — actual verifier-held principal and issuer

Replace \`trusted: bool\` and \`external_auth_token: str\` at the security boundary with a **verifier-owned capability** that untrusted callers cannot construct or supply as raw booleans. A competent external authority must define:
- signed/enveloped \`issuer_id\`, signature algorithm/key identity and trusted verifying key (and key revocation);
- exact operation/audience, B5/M2 owner identity, released \`release_ref\`/producer subject and product family, selection scope and target-use permission ceiling;
- exact checkpoint digest, append-only event ordinal/previous-root and immutable external ledger root/custody identity;
- monotonic epoch/as-of, validity interval, expiry and effective revocation state, evidence authority/rule and nonce/replay protection.
Check cryptographic signature and entitlement against **independently acquired** trust store; fail closed on missing, expired, wrong scope, wrong subject or revocation. A nonempty token is not a capability. A verifier initialized from material *authored by the same untrusted caller* is not an independent root.

No source-science/G0b/issuer contract is implicitly supplied by this specification. Without accepted competent issuers, return \`EXTERNAL_ISSUER_HOLD\`.

## Gate 2 — enforce at the accepted owner mutation boundary

Provide one **mandatory, non-bypassable entrypoint** for each B5/M2 mutator, using an owner-held authority and immutable evidence snapshots. Prefer owner-integrated transaction guards over process-local monkey patches; if process/local wrappers are used for development, state candidly that saved callable aliases/direct repository access cannot be prevented and require a trusted host's access control.

B5 \`stage_release\`, \`stage_protocol\`, \`register_product\`, \`publish_product\`, \`record_recertification\`, \`select_current\`, \`declare_no_current\`, \`from_checkpoint\`, plus the **nine N04R unwrapped**: \`supersede_current\`, \`withdraw_product\`, \`declare_invalidation\`, \`record_rebuild_eligibility\`, \`link_rebuild\`, \`record_cache_materialized\`, \`record_cache_dropped\`, \`attest_gc_eligibility\`, \`record_payload_gc\`. Close two partial overlay paths: no explicit subject on NO_CURRENT, recertification missing event verification.

M2 \`register_producer_subject\`, \`constitute_release\`, and the **eight unwrapped**: \`M2Repository.register_subject/register_closure/register_release/register_representation/register_binding\` and module \`constitute_closure/register_representation/publish_binding\`. Separate source-authentication vs issuer/revocation checks according to operation. Verify no direct or saved alias path can change accepted shared state outside policy; account for race/atomicity.

Only where event/permission is actually qualified may B5 operations authorize state transitions. Authorization belongs to the state mutation site, not the caller's boolean.

## Gate 3 — native release/checkpoint/replay, not parallel model

Verify/checkpoint the accepted \`LearnedProductLifecycleExecutor.export_checkpoint\` schema, typed \`LearnedProductLifecycleEvent\`, \`CurrentSelectionReceipt\`, \`NoCurrentReceipt\`, \`LearnedProductLifecycleSubject\`, and M2 \`ReleaseCore\` exactly. Do not introduce a second authoritative \`{"events","state","epoch","revoked"}\` store. Use corrected N04 release→producer-subject resolution: \`M2.resolve_subject_exact(repository, release_ref)\`, not \`subject_exact(release_ref)\`.

Rebuild lifecycle state from the **complete previously witnessed event sequence** at source-exact ordinal/parent-ref chain and compare all accepted owner publication/validity/replay/selection/invalidation, determinant and materialization projections. Bind checkpoint hash/event count to independent **append-only** issuer/custody root; reject consistent rewrites to both hash and history. Persist native observed owner operation/receipt identities; verify exact prior selection receipt, event rule/authority ref, product family and scope. Distinguish as-of historical replay from issuance of new CURRENT. Ensure \`read/verification\` and \`mutate/publication\` are atomic or use compare-and-swap against verified root.

## Gate 4 — epochs, currentness and revocation

Epoch/revocation are **independently issued inputs**, never caller-adjustable numbers or mutable unrooted lists. Bind to same source/release/subject/action/custodian. Apply effective-time/as-of policy, monotonic constraints, and selection checks at every operative call including NO_CURRENT, recertification and rebuild. A release MUST be registered, published, valid, not withdrawn/invalidated/revoked, with exact native producer permissions, and its selection key/ref must match product family and scope. Prevent future epoch bypass and rollback/fork. External custody must remain HOLD until an independent custodian signs receipt.

## Gate 5 — transitive dependent invalidation and sibling safety

Walk the accepted \`LearnedProductDeterminantGraph\` or authoritative directed dependency graph, not \`supersessions\` map. Compute full reachable transitive set (A→B→C and branching A→B/A→C→D), de-duplicate, detect cycles or apply explicit cycle policy, preserve unrelated siblings, issue individually typed owner invalidation receipts, and ensure CURRENT cannot select any invalidated/revoked dependent. Verify separate historical as-of resolutions remain truthful without reauthorizing CURRENT. Qualify downstream reference closure across generations and overlays.

## Gate 6 — independently executable acceptance evidence

Use a **qualified isolated DeepSeek Harness / Python worktree** with known base/branch/commit hashes, reproducible source-free environment. Copy review hostiles from their frozen SHA, do not rewrite or adopt candidate assertions. Run in this order:
- independent \`repro/test_s06r_independent_hostiles.py\` against frozen S06 candidate (expected scientific/security rejections of vulnerable behavior; currently likely failing);
- same against proposed repair; expect all declared hostiles PASS;
- real B5/M2 mutation entrypoint courts and N04R/P02R regression suites; require owner-native replay and checkpoint closure;
- stress/fork/concurrent mutation and external signature/missing-root refusals; signed inputs only with authorized externally issued fixture keys (TEST ONLY, not live grants).

Retain full commands, environment, test results, exits, fixture origin and input SHA, and independently verified remote candidate SHA. **Do not claim current reviewer executed tests**. A fail of *existing candidate* hostiles is evidence of defects, not proof that accepted owners are compromised in all deployments.

**Exit:** only a future independent security reviewer may recommend promotion of an owner-integrated, signed, reproducible, correctly scoped B5/M2 development security interface. Separate HQ/current/G0b scientific grant still required for production; PRE-V3 completion remains distinct from V3.
