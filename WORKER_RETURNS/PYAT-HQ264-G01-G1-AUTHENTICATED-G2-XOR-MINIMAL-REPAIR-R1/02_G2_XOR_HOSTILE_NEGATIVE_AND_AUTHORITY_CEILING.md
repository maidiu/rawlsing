# HQ264 G01 — G2, XOR, hostile, negative and authority ceiling

## F1 status: feasible, and the G0b blocker is ruled out

The adopted G2 path requires **no operative G0b permission**. Two independent reasons,
both read directly from the adopted source at the verified blobs:

1. `AUTHORISED_AUTHORITY = "ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED"` —
   applicability emits an admissible SET only and explicitly does not authorise ranking or
   selection. That is not a model-use grant, so it does not require G0b.
2. `ApplicabilityAuthorityRecord` accepts a plain `admission_authority_ref`, constructible
   source-free as TEST_ONLY_UNISSUED.

And the binder is **not** a self-hash substitute. Its docstring says a self-consistent
hash or shape check "proves nothing, because a caller can fabricate a self-consistent
binding", and `_authenticate_binding_against_authority` re-derives the binding from the
exact request, receipt and rule and returns the re-derived object. That is exactly the
substitute property F1 asks for, and exactly what my HQ262 candidate's local scope hash
lacked.

**Correction to the prior blocker.** My HQ260 return said `BLOCKED_REQUIRE_TRUST_ROOT`
under a universal claim. HQ261 narrowed the claim, and HQ264 asks whether genuine G2 is
reachable. It is. **`G0B_OWNER_PERMISSION_REQUIRES_ADOPTION` is therefore NOT the correct
disposition for F1**, and no existing-owner edit is needed for it.

## F2 status: blocked on a genuinely missing artifact

The approved HQ253 T01 four-respondent source-free XOR fixture is **not in the
repository**. Confirmed by search, not assumed.

F2 demands exact figures: q1 = q(C|A=1) at **1/2 and 1/2** with **native joint denominator
2**, and q2 = q(C|A=1,B=0) at **0 and 1** with **native joint denominator 1**, over the
same four original respondents in one exact release, with two distinct C1 producer
identities and preserved same-respondent lineage.

Producing those numbers would require me to invent the four respondent identities, the
release, the risk-set and denominator membership, and the two C1 producer/predicate/witness
sets. The commission forbids exactly this: "If the fixture's exact identity/authority is
unavailable, identify the missing artifact and STOP rather than silently substitute", and
names the prohibited moves — multiply marginals, swap in new F8-only evidence, differentiate
only by `cell` in a hash, invent a second statistical engine.

Invented identities would yield numbers that *look* like the commissioned figures while
being my own construction. That would be worse than a HOLD, because the figures would be
indistinguishable from the real ones to any later reader.

## F3–F6: not attempted, and why that is the honest choice

F3, F5 and F6 are individually repairable. All three are repairs **to** the candidate. Doing
them while F1 and F2 remain open would produce a candidate that still substitutes a local
scope hash for real G2 and still lacks the commissioned XOR grain — a **half-corrected**
candidate whose green tests would imply a repair that had not happened.

That is the specific failure mode this review series exists to prevent, so I declined.

F4 additionally cannot be exercised honestly without an authenticated G2 receipt to
distinguish applicability non-admission from an admitted source with missing internal
evidence.

## Hostile and negative coverage: none added this lane

No hostile court was written, because every commissioned hostile (G2 wrong permission
refs/release/source, evidence/provenance in-flight mutation, forged origin/hash, low-level F8
minting an owner receipt, typed negative with no F8 invocation, cross-source and walkback
proxy refusal) depends on the F1/F2 candidate that is blocked. The only executed assertion
is that the unmodified HQ262 candidate court still passes 22.

The HQ263 independent review's F1–F6 slots were read as instruction. Per the commission I
distinguish it carefully: it returned `FAIL_REQUIRED_CORRECTION` with source-static certainty
and **no qualified clean-SHA runtime**. Its probes were never executed. Nothing in this
return treats them as executed tests, and nothing in this return claims to have
independently reproduced them.

## Authority ceiling

Unchanged and unexceeded: no raw survey, no Library search, no external source fetch, no
invented trust root, no self-issued EE14 grant, no deployed-security claim, no T1
declaration, no self-adoption. No accepted owner (C1, F8, applicability, G2, B5, G3) and no
inherited return artifact was edited. No source-file, HQ-handoff, authority-issuer, grant,
world or V3 edit. The two permitted candidate files are byte-unchanged.
