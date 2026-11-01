# CONDITIONAL REPAIR OR REJECTION

## Four separate verdicts

### (a) Sourcefree defect repair worth adapting — **YES, MERIT_RECOMMENDED_WITH_CONDITIONS**

S06G genuinely repairs the twelve S06FR defect-presence cases at the tested local grain. The current B5/M2 code is the pre-hardening base; independent E2 tests confirm 0/10 current behavior versus 10/10 candidate behavior, and the S06G candidate does not break the accepted B5 court or the 45/45 adjacent integration suites.

**Merit:** recursive payload immutability, owner mutation transaction/rollback, serialized selection, serialized M2 writers, guarded saved helpers, and native checkpoint semantic replay are the right structural repairs. This is not a cosmetic patch.

### (b) Compatibility regression — **YES, BOUNDED TO TWO ACCEPTED M2 FIXTURES + ONE TEST-HELPER DEPENDENCY**

- `test_17_binding_cannot_resolve_different_release` and
  `test_18_endpoint_failover_only_among_same_release` fail under S06G at
  `RELEASE_UNAVAILABLE` because they insert a foreign representation/binding
  into a repository without lawfully registering the foreign release. Current
  accepts the fixture and reaches the later oracle; S06G refuses earlier.
- The new reconciled S06G cases first assert the early refusal, then lawfully
  register the foreign release/representation and preserve the original
  `PUBLICATION_BINDING_MISMATCH` oracle. They are new tests, not edits to the
  accepted tests.
- The S06G test module also imports
  `rawlsing_next.tests.test_pre553_s06f_native_owner_security`, which is absent
  from current. A separate engineer must add/rewrite the helper or provide a
  standalone S06G test module.
- No other production-level regression was observed: accepted B5 39/39,
  adjacent integration 45/45, S06G new court 42/42.

**Owner action:** decide whether the two accepted M2 fixtures are invalid
setups (early refusal is correct) and authorize a new fixture-update review.
Do not weaken `release_exact` or edit the accepted tests in place.

### (c) Unsuitable code — **NOT SUITABLE FOR EXTERNAL/PROTECTED/PRODUCTION USE**

S06G is local in-memory exception atomicity and serialization only. It does
not provide durable commit storage, OS-kill recovery, multiprocess
coordination, fork/pickle portability of locks, authenticated issuer/epoch,
revocation/as-of source, protected CURRENT or external custody. A same-process
Python caller can still set private attributes, open transactions, replace
callables or mutate private dictionaries. The honest mode remains
`LOCAL_UNAUTHENTICATED`; `require_external_issuer` correctly holds.

**Reject** any claim that S06G establishes external custody, native source
rights, N11/N12, C11/C12, production readiness or authenticated completeness.

### (d) Unqualified claim — **THE UNFILTERED 187/14 IS NOT GREEN; A GREEN SELECTION IS NOT ADOPTION**

The correct factual claim is:

- **187 passed / 14 failed, exit 1, no skips/errors** in the unfiltered suite.
- 12 failures are obsolete S06FR defect-presence assertions (defect repaired).
- 2 failures are accepted-M2 fixture incompatibilities (early refusal).
- A separate 187/14-deselected selection is a selection, not a green court and
  not an acceptance.
- The S06G author’s own return is honest about this; the **unqualified** claim
  would be “187 green” or “security accepted.” Both are rejected.

## Precise MERIT/patch recommendation for a separate engineer

**Do not self-integrate.** A separate owner/engineer should:

1. **Base:** current PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`;
   current lifecycle `a11c9eb73abab9be118ef4f0b6e325e676059f27`, release
   `f76c390665f06ef126968ccf1a6b2d816f43ae92`.
2. **Apply the S06G semantic diff**, not a wholesale branch cherry-pick:
   - lifecycle `dadf2362f3195c28ebaf97655e28cdba72c04fb3`
   - release `1cb7692399aad8fb272c8c9ce956719527829007`
   The candidate is based on S06F `6187d0a2`, whose merge base with current is
   `7f29aec3`, not current; the production diff is +545/−4 lifecycle and
   +155/−10 release.
3. **Preserve public signatures** used by
   `pre553_learned_world_composition.py`: `stage_release`, `register_product`,
   `publish_product`, `selection_key`, `select_current`, `events`,
   `audit_replay`, and M2 register/publish/resolve entrypoints.
4. **Keep both accepted M2 tests unchanged.** Add only new reconciled tests
   that assert early `RELEASE_UNAVAILABLE`, then lawfully register the foreign
   release/representation, then test `PUBLICATION_BINDING_MISMATCH`.
5. **Port/own the test helper:** add or rewrite
   `test_pre553_s06f_native_owner_security` helpers, or provide standalone
   S06G fixtures. Do not assume the S06G test module collects on current.
6. **Retain all 12 old S06FR defect assertions** as historical defect-presence
   evidence. Do not delete, weaken or relabel them.
7. **Run and bank:**
   - S06G full suite: 187/14 unfiltered, exact 12 obsolete + 2 fixture
     failures; no skips/errors.
   - S06G 42-case repair court.
   - Accepted B5 39/39; accepted M2 26/2 or an owner-approved fixture update.
   - Adjacent integration 45/45.
   - Independent E2 10/10 on candidate and 10/10 failure on current as the
     differential witness.
   - Cold restore, concurrency, saved-helper misuse, changed projection and
     honest `LOCAL_UNAUTHENTICATED` downgrade.
8. **Owner review:** distinct reviewer after exact returned SHA; original
   author and D4 reviewer must not self-review. No adoption, merge, external
   issuer or protected-current claim.

## What to reject outright

- Wholesale replacement of current B5/M2 with the S06G branch or any change that
  edits accepted tests to make 187/14 look green.
- Any “external custody”, “protected current”, “native issuer”, “N11/N12”,
  “C11/C12”, “production ready” or “authenticated completeness” claim.
- Any use of S06G to rehabilitate D3’s standalone caller-trusted S06 wrapper.
- Any merge into PRE-MAIN/main without a separate owner, exact-SHA review and
  proportional receiving decision.
