# S06R security defects — direct frozen candidate code inspection

Frozen source `rawlsing_next/s06_trusted_release_replay.py` at `4fec074c7e40a8b233055ffd1d80dbede293c9c4`, Git blob `40b1009512aea909612a5fa01081ec3d0955860d`.

## Caller-controlled trusted=True is not a verifier

The setter operations `select_current` (193–225), `withdraw` (227–237), `invalidate` (239–249), `supersede` (251–261), `revoke` (263–273), and `invalidate_descendants` (275–288) all carry signature `*, trusted: bool=False`. Their sole "verifier requirement" is `if not trusted: return ...`. A caller can pass `trusted=True` and receive an `allowed=True` TrustVerdict, independent of identity, rights, token or signature. There is no trusted principal held out of caller reach. `select_current` tests only `current_epoch < self._epoch` and membership in `self._revoked` before appending SELECTED. It does not require the release to be REGISTERED/PUBLISHED or VALID; it does not read `_state["invalidations"]` or `_state["publications"]`. `withdraw` and `invalidate` do not propagate into its selection checks except independent `revoke`. Other methods are never invoked by the accepted owner.

The public `append_event(event)` (86–88) has **no trust argument at all**. It appends caller-chosen event dictionaries then applies state transitions for REGISTERED, PUBLISHED, SELECTED, WITHDRAWN, INVALIDATED, SUPERSEDED and REVOKED. Unrecognized `kind` values are appended without `else: raise`. This is an even shorter bypass than the truthy-flag mutation route.

## External authentication is an unparsed string

`from_checkpoint` lines 166–168 are literally:

    if require_independent_auth:
        if not external_auth_token:
            return None

There is no verification step after this. Arbitrary `"hello"`, `"valid-token"`, or the attacker's own claimed bearer token passes. The reviewer does **not** posit any missing magic issuer already existing elsewhere. No cryptographic signature, external keyring, trusted issuer record, issued grant, exact release subject, permitted operation, expiry, nonce, epoch or external root checked.

## Consistent history rewrite / self-consistent dual hashes

`_event_history_hash` (60–64) is SHA256(JSON(events, sort_keys=True, default=str)), `_state_projection_hash` (66–68) is likewise SHA256 of mutable state. `export` (111–125) outputs both hashes and event_count. `from_checkpoint` (128–187) trusts *all* those supplied values after rehashing and replaying supplied event corpus. An adversary can construct a new `[REGISTERED X, PUBLISHED X]` log, set `state.publications[X]=PUBLISHED`, `event_count=2`, recompute both hashes, and provide any nonempty token. The exact replay and hash comparisons succeed for that forged *self-consistent* corpus. Thus the implementation rejects stale/corrupted hashes, but cannot establish historical completeness or original issuance. Test case `S06R-H08` freezes this adversary. No new runtime execution is claimed.

The free-standing `epoch` and `revoked` are set in `export.checkpoint_payload` but omitted from hash functions. `from_checkpoint` sets `instance._epoch = epoch` and `instance._revoked = revoked` before applying events. It does not verify an external epoch signer or compare an independently bound revocation map. In particular, rewriting the epoch of a checkpoint with only REGISTERED and an irrelevant revocation list is invisible to both hashes and to state-rebuild checks. Event-driven REVOKED may add revoked refs on replay, but there is no check that supplied revoked set precisely equals the issued event-derived set or an external revocation ledger. A selected historical sequence spanning multiple epochs is also reconstructed with the **single saved final epoch** for all SELECTED event epochs, not each event's original epoch — risking false refusal of otherwise valid multi-epoch history.

`cold_replay` recreates the state from the event corpus already under the caller's control, starting with caller-present `_epoch`/`_revoked`; it proves neither the corpus existed before the checkpoint nor that B5/M2 accepted that event.

## Graph invalidation incomplete

`invalidate_descendants` lines 284–288:

    self.append_event({"kind": "INVALIDATED", "release_ref": release_ref})
    for old_ref, new_ref in self._state.get("supersessions", {}).items():
        if old_ref == release_ref:
            self.append_event({"kind": "INVALIDATED", "release_ref": new_ref})

Given A→B→C it invalidates only A and B, **not C**. Given branch/cycles, a single mapping `old_ref -> new_ref` cannot model multiple children per old release. The actual accepted `LearnedProductDeterminantGraph` is a richer descendant/determinant graph; there is no adapter. The logic preserves an unrelated sibling only because it never traverses its edge — this alone does not demonstrate complete selective invalidation.

## Exposed mutable internals and wrong interface

`events` line 190 returns `tuple(self._events)`, whose **dictionary elements are mutable aliases**, not immutable copies. `get_state` line 310 constructs only a top-level dict and returns nested `publications`, `selections`, `supersessions` dict references unchanged. The returned user-facing state can be mutated in place. `export` also copies only top-level state and event list, exposing mutable nested references. `_state_projection_hash` serializes sets via `default=str`, unsuitable for a canonical trust serialization (order/signature format is not defined).

`verify_trust_mode` lines 299–308 always refuses EXTERNAL_CUSTODY without a root, but it returns `TrustVerdict(allowed=True)` for all other modes **with no owner, source, release, attestation or scope**. That is not a valid B5 CURRENT or immutable snapshot authorization.

## Difference from author tests

Only after independent hostile commit `7e96914ed6c9a186d5de8a778e8396e46a741eb2` was pushed did reviewer read `rawlsing_next/tests/test_s06_trusted_release_replay.py`, blob `5e336e85e2b42fbd3a1808e74b58e97aa0486094`. Author's 26 PASS (not reviewer-executed) cover inconsistent tampering and an intentionally nonempty `"valid-token"` accepted, a `trusted=False` refusal plus `trusted=True` acceptance, one-hop invalidation, and own-format replay. These positive expectations **bake in the vulnerabilities** rather than testing a credential held by an independent principal. Their "wrong subject" mutates only a toy `state.publications` key, not an accepted typed M2 producer subject/release identity. Author test `test_valid_checkpoint_restore` restores its own S06 schema, not a B5 owner checkpoint.
