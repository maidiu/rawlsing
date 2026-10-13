# PYAT R3 S06 -- Trusted Release, Checkpoint, and Replay Return

**Commission:** PYAT-R3-S06-B5-RELEASE-REPLAY-TRUST-R1
**Branch:** `agent/rabochii-pyat-r3-s06-b5-release-replay-trust-r1`
**Implementation base:** `7f29aec36d24f16da52d84f17c00f08db3a55434`
**Astra R3:** `88d3c40def26d34ff202258171c256dfa9d17dbb`
**Prior evidence:** N04 `b5a6b6409c765d2aecb8c2f9c9ef9bd8fc6473c2`, N04R `fde95ee9275f9fe14b6868db363035757cffab48`, P02R `b3523bed5d751b24f0bf1fd111af4161727fe9b5`

## Defect inventory (from N04R independent review)

| Defect | N04R finding | S06 fix |
|---|---|---|
| Altered-state restoration | Raw executor accepts altered publication state | Event-history hash + state rebuild verification rejects |
| History truncation | Truncated events accepted | Event count + hash validation rejects |
| Unwrapped withdraw | `withdraw_product` succeeds without verifier | `trusted` flag required |
| Unwrapped invalidate | `declare_invalidation` succeeds without verifier | `trusted` flag required |
| Unwrapped supersede | `supersede_current` succeeds without verifier | `trusted` flag required |
| Self-consistent hash only | Hash treated as independent auth | Dual hash (event history + state projection) separated; `require_independent_auth` gate |
| Stale epoch | No epoch check on selection | `current_epoch < checkpoint_epoch` rejection |
| External root | Local replay claimed as external custody | `TrustMode.EXTERNAL_CUSTODY` rejected without root |

## What was built

`rawlsing_next/s06_trusted_release_replay.py` -- `TrustedCheckpoint` class with:
- Full event-history preservation (no truncation)
- Dual hash: event history hash (independent) + state projection hash (self-consistent)
- State rebuilt from events on restore; mismatch = rejection
- Verifier-required state-changing methods (withdraw/invalidate/supersede/revoke)
- Stale-epoch selection rejection
- Revocation propagation to descendants; siblings preserved
- Cold replay verification
- Trust mode separation: LOCAL_REPLAY, IMMUTABLE_SNAPSHOT, PROTECTED_CURRENT, EXTERNAL_CUSTODY

## Test evidence

`python3 -m pytest rawlsing_next/tests/test_s06_trusted_release_replay.py -v` -- exit 0, 26/26 pass

## Required acceptance cases

- Valid positive restore: `test_valid_checkpoint_restore`, `test_cold_replay_from_events`
- Hostile negative restore: `test_altered_publication_state_rejected`, `test_truncated_event_history_rejected`
- Mutation after checkpoint: `test_mutation_after_checkpoint_detected`
- Wrong subject: `test_wrong_subject_not_restored`
- Stale epoch: `test_stale_epoch_selection_rejected`
- Unauthorized method route: `test_unwrapped_withdraw_rejected_without_trust`, `test_unwrapped_invalidate_rejected_without_trust`, `test_unwrapped_supersede_rejected_without_trust`
- Invalidated descendants: `test_invalidate_descendants_propagates`
- Preserved unrelated siblings: `test_unrelated_siblings_preserved`
- Independent auth separation: `test_self_consistent_hash_not_independent_auth`, `test_independent_auth_token_accepted`
- External root requirement: `test_external_custody_claim_rejected_without_root`

## Trust modes separated

- `LOCAL_REPLAY`: local event replay, not external custody
- `IMMUTABLE_SNAPSHOT`: authorized immutable development snapshot
- `PROTECTED_CURRENT`: epoch-validated current selection
- `EXTERNAL_CUSTODY`: requires independent external authority (not proved)

## Residual external authority dependencies

- External custody for production claims: requires independent external root
- Real-source F7 qualification: requires source/design/operation authority
- B5 CURRENT publication: requires separate HQ authorization
- Independent reviewer verification: separate commission required

## Not done

- No edits to Worker 1's adapter
- No unrelated semantic or statistical changes
- No G0b, B5 CURRENT, or production publication
- No external authority, permission, or publication issued

## Terminal

`PYAT_R3_S06_B5_TRUSTED_RELEASE_REPLAY_IMPLEMENTED_LOCAL_TESTS_PASS__AWAITING_INDEPENDENT_REVIEW__NO_PRODUCTION_PUBLICATION`
