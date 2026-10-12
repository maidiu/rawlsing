# C02J — Issuer holds and principal petition

## Holds (exact, demonstrated, not solved)

1. **CEILING HOLD.** The permission ceiling is self-declared in custody.
   Demonstrated: `PATCHED_fake_permission` refuses substitution (must equal
   the frozen expectation), and the legitimate positive publishes the HELD
   ceiling. But the declared value itself is unproved — no issuer exists to
   validate it against. A caller who controls custody construction controls
   the ceiling.
2. **TAUTOLOGY HOLD.** The frozen expectation is derived from the construction
   it authenticates. Demonstrated both directions: post-authoring mutation is
   detected and refused (`PATCHED_mutated_repo_publish`), but re-derivation
   after mutation still admits (`PATCHED_self_made_expectation_publish`
   refuses only because the swapped map mismatches the held repo — a fully
   re-derived map over a fully substituted repo would admit). Only an
   issuer-held expectation source would close this.
3. **REPLAY HOLD.** `REPLAY_COMPLETE` is an owner-held claim gated by the M2
   closure's own grade. Stale grades are refused (`PATCHED_stale_replay_grade`);
   replay is never re-executed here.
4. **AUTHORITY HOLD.** Semantic AuthoritySnapshot refs are owner-held.
5. **EVENT-ATTRIBUTION HOLD.** Forged event authority/rule refs on direct calls
   are not authenticated (demonstrated: subject still held-authenticated,
   attribution unproved). No issuer binds event refs.
6. **No issuer / trust root / signature scheme / G0b / G1 / CURRENT / V3.**

## Principal petition (competent acts required before operative use)

1. **Owner act:** adopt verifier-held mediation as the sole operative ingress
   per `03_PROPOSED_MANDATORY_PATCH.md` (cutover procedure included).
2. **Issuer act (or recorded out-of-scope):** either stand up a competent
   producer issuer that signs ceilings and holds expectations independently,
   or record that self-declared ceilings and derived expectations are accepted
   residual risk with the demonstrated refusal surface as the boundary.
3. **Revocation act:** move the revocation ledger from harness-held to an
   operated revocation source with as-of semantics.
4. **No self-adoption:** none of the above is taken by this return. The
   overlay is test-only; the candidate is development-grade; the holds are
   open.
