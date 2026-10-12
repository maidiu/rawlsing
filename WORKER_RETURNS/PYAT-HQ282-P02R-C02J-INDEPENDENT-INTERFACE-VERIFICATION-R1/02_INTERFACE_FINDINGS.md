# Interface findings

## Eight documented B5 wrappers

| Method | Actual overlay check | Review evidence / limit |
|---|---|---|
| stage_release | Resolve registered release, repository identity/replay/revocation checks and presented-field comparison | Normal and five independently altered fields; unknown release baseline |
| stage_protocol | Converts protocol, same subject check | Unknown registry rejected; conversion uses accepted owner |
| register_product | Registry, then full subject check if staged subject exists | Normal registration; unknown registry rejected |
| publish_product | Registry, then full subject check if staged subject exists | Normal publication; unknown registry rejected; event kwargs unchecked |
| record_recertification | Registry lookup only | Unknown registry refused; registered revoked release recertifies; substituted event refs accepted |
| select_current | Registry and full subject check when present | Normal saved-current setup; unknown registry refused; withdrawn selection refused by accepted owner |
| declare_no_current | Registry lookup only if explicit subject_release_ref supplied | Omitted subject argument permits event and selection-state change without a registered verifier |
| from_checkpoint | Accepted restore (which calls patched stage_release), then verify_checkpoint_subject | Valid published/current restore fails; subject_exact receives release_ref instead of release.release_subject_ref |

The checkpoint implementation first verifies structural self-hash, registered-state coverage and deterministic re-export. It restores saved state mappings rather than replaying event transitions to derive and compare state. A truncated history still reporting PUBLISHED, and a publication state changed to REGISTERED while retaining its publish event, both restore without the overlay. Those local self-hashes do not authenticate provenance. Under the overlay, the same bad records are refused at the same incorrect producer-subject lookup that refuses valid records; this is not evidence of a working completeness check. Incomplete publication state coverage and an unchanged payload with a bad hash are specifically rejected by the accepted owner.

## Other state-changing entrypoints

Source inspection of the pinned executor shows these public mutators are unwrapped: supersede_current, withdraw_product, declare_invalidation, record_rebuild_eligibility, link_rebuild, record_cache_materialized, record_cache_dropped, attest_gc_eligibility, record_payload_gc. They use owner checks and internal event/selection helpers, not the proposed release-verifier routing. Withdrawal without any registered verifier was executed and succeeded. The other eight mutators were inspected, not individually tested; no claim that all invalid inputs pass is made. selection_key also mutates the local key table despite the overlay documentation calling it read-only. It does not itself publish or select a release.

M2 wrappers cover only module functions register_producer_subject and constitute_release. Both check repository object identity, not whether new material has independently authorized identity. A new producer subject in a held repository was accepted. M2Repository.register_subject/register_closure/register_release/register_representation/register_binding and module constitute_closure/register_representation/publish_binding remain unwrapped. Direct foreign-repository register_subject was executed successfully. Other M2 routes were inspected, not individually exercised. Imports saved before monkey-patching can also retain original Python callables (inspection only). This is a process-local test layer, not a Python principal isolation boundary.

## Identity and authority limits

Prior expected material prepared before replacement rejects a new repository. The prior expectation here is separately retained synthetic fixture data, not an external issuer. Replacing the complete material and deriving a matching expectation before verifier construction succeeds. Likewise substituting both custody ceiling and expected ceiling succeeds. The verifier demonstrates internal consistency against a chosen constructor-time reference; an independently controlled expectation issuer and permission decision are still needed.

The overlay checks presented subject authority IDs and permission keys but not independent permission entitlement. Frozen expected mappings resist ordinary map changes; repository aliases preserve object identity and can still mutate held contents. A determinant changed through an alias after the expectation was frozen is rejected. Release core resolution verifies its semantic projection hash. M2 closure_exact and subject_exact return stored objects without a general re-hash of their current contents; do not generalize release-core content addressing to all retained records.

Event references are exact and included in event identities. Exact syntax, parent linkage and append order do not establish issuer authorization. Direct recertification accepted substituted authority and rule references both before and after overlay activation. The facade supplies constructor-held event references, whose issuance is also unproved.

Revocation is constructor-supplied sets of release, authority and replay-closure keys. All four publication refusals were observed. No expiry timestamp, live revocation source, effective interval or as-of policy exists. After selection and withdrawal, event-based historical resolution reports the old CURRENT_SELECTED and current state reports NO_CURRENT. With current revocation in the overlay, the historical checkpoint path is refused at staging while the event path continues to return historical selection. These are saved historical claims, not newly authorized current publication. Revocation also does not cover recertification of a registered release.

The obsolete replay grade is refused relative to the fixture's required deterministic-rebuild grade. HISTORICAL_EXPLANATION_ONLY remains in the accepted vocabulary, so this does not prove a universal prohibition of historical grade in every possible custody configuration. Incomplete replay after custody is refused through exact M2 resolution. No independent rebuild or replay execution was performed.

## Concrete follow-up requirements

1. Correct checkpoint release-to-producer-subject lookup, then test valid restore alongside tampered history/state; derive lifecycle state from events and compare with saved claims.
2. Route every operative owner mutation through the intended checks, including recertification and implicit NO_CURRENT subjects. Define which methods need product verification versus a separate event authority decision.
3. Require independently controlled expected identity and allowable permission scope, and check direct event authority/rule provenance.
4. Supply a current revocation authority and define expiry and historical as-of semantics consistently across event and checkpoint resolution.
5. Establish replay completeness independently of its stored label, and test concurrent mutation/verification if supported. Stable concurrent facade publication here creates separate fresh executors; identical event hashes do not prove durable exactly-once publication.

No proposed implementation fixes were applied. These are reviewer requirements for a future candidate and independent review.
