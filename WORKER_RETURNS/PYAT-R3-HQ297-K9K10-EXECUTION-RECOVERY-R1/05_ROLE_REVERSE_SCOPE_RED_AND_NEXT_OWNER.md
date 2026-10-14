# Reverse-role forged-scope authority — source witness, not a staged PE RED

Frozen independent fixture `test_strict_reverse_scoped_issuer_forgery_must_refuse` constructs `authority_id=urn:test:unissued:reversal:WRONG_TOPOLOGY`, `authority_version=999.0.0`, and a 64-hex fabricated content hash; expects `TYPED_REFUSAL` with no geometry.

**Pinned PE source** `58484f4c3d9aae148d4116dcf00420c432aefcbd`:

- Lines 354–358: `_auth` coercion/shape for the caller's optional reversal reference.
- Lines 660–673: if role is reverse, only `reversal is None` activates refusal. A non-null forged `AuthorityRef` passes this gate.
- Lines 685–695: `producer_risk_ref == request.denominator_basis_ref` tests an ordinary denominator ref, without independent reverse-role issuer/target/risk-set authorization.
- Lines 697 onward: accepted C1 composition is called without an observed independent reverse-scope warrant resolver.

**Qualification:** STATIC NEGATIVE WITNESS, **NOT EXECUTED AGAINST PE**. The separately executed isolated helper demonstrates why non-null presence is insufficient but does not itself prove actual PE result-state behavior. The unchanged frozen PE test remains a predicted semantic RED until pinned qualified execution.

**Smallest owner repair:** define and require an issuer-issued exact reverse-role warrant keyed to source release, native sampling unit, subject/target coordinate order, conditioner set, authorized reverse operation, target-specific risk set and denominator basis, scope/time/use/issuer validity, and immutable read receipt. Resolve against a permitted authority registry—not only the request reference shape—and refuse a forged or merely declarative reference before C1 composition. Keep forward legal fraction unaffected.

**Who may act:** PE/C1 authorized owner plus independent scientific/authority reviewer for adoption; K9E has no authority to edit owner code or mint a warrant. Full K9_06 and K10_12 require separate SC0 adapter and N9 world-owner evidence.
