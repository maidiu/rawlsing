# SCRV3 M6 Currentness / Invalidation Contract

**Predicate:** `SCRV3_M6_AARE_CURRENTNESS_V1`  
**Envelope:** `ActorAccessibleRenderEnvelope@1.0.0`

At `as_of_causal_time`, one exact actor is bound to one co-valid quartet: generated-person hash, actor-state hash, ADP-016 memory-state hash, and ADP-017 epistemic/accessibility/permission-state hash. ADP-017 is additionally bound to `1.0.0` / `git-blob-sha1:eece4f3f2f3f9288ab9bbc645dc81e20a99e1280`. `as_of_causal_time` is V3 causal time, never wall clock.

An envelope is current iff `integrity_state == VERIFIED`, actor IDs match, receiver causal time is not earlier than `as_of_causal_time`, all four current source hashes equal the bound hashes, and the accepted ADP-017 version/hash equal the envelope binding.

A later causal cursor with the same four hashes remains current. No wall-clock TTL exists.

`STALE_RENDER_ENVELOPE` applies only when a previously verified historical envelope is checked at a later causal time and at least one bound semantic source hash changed.

`INTEGRITY_FAILURE` applies for actor mismatch, receiver time before `as_of_causal_time`, missing/unverifiable hashes, same-time/earlier competing hashes, authority mismatch, entry/decision/envelope hash failure, or replay-closure failure.

A stale envelope may remain historical replay/audit material; it cannot supply current V2 behavior.

Every relevant generated-person, actor-state, ADP-016 memory/accessibility, ADP-017 stance/accessibility/permission, or actor-perceived-view change must alter at least one bound source hash. If it does not, producer content-addressed state integrity failed.

Stale or integrity-failed input yields zero actor-safe claim semantics. Transcript/session content, full GeneratedPersonRecord, upstream priors, opaque provenance, and guessed schemas are not fallback sources.
