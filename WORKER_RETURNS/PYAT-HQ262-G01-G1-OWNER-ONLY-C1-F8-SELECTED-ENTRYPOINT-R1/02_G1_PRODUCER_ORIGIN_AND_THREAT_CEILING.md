# HQ262 G01 — G1 producer origin and threat ceiling

## What G1 was, and what changed

At HQ260 I returned `BLOCKED_REQUIRE_TRUST_ROOT` and banked the reproduction: F8 took
`evidence` from the caller, and `PossibilitySliceEvidence.authority_refs` /
`.provenance_refs` were validated in `__post_init__` but **never read** by the evaluation
path, so substitution left `result_hash` unchanged **and survived the replay verifier**.

That blocker was correct under a universal claim. HQ261 T01 affirmed the forgery but
**rejected** the universal claim, fixing the intended threat scope to an **external
data-only service client**. Under that scope the fix is not "a better hash" — it is to
remove the caller's ability to supply anything forgeable at all. This ingress does exactly
that.

## Why this is genuine origin and not a self-hash

This is **not** a caller-forgeable self-hash, which is what HQ260 refused:

- the evidence never comes from the client — it is `possibility_slice_evidence_or_null`
  produced by the C1 producer the owner itself invoked;
- the client cannot supply an authority, a provenance ref, a repository, a registry, a
  predicate, a witness, a model rule, an applicability receipt or an executable schema;
- the receipt binds the complete original C1 identity preimage, the C1 evidence projection
  hash, the C1 authority and provenance keys, the C1 risk set and denominator, the
  owner-held applicability scope hash **and** the F8 result hash.

A client that observes only the F8 number cannot reconstruct the receipt, because the
receipt also commits to C1 material the client never sees. Observed: C1 identity
`01c381d3…` vs F8 `47b51a3b…`, with genuine `C1-AT07-COMPARABILITY`, `C1-AT07-QUERY`,
`C1-AT07-ROUTING` and `C1-AT07-SOURCE` authorities.

## The ceiling — stated plainly

**Protected:** an external data-only service client. It cannot forge origin because it
cannot supply evidence or any producer object.

**NOT protected, and explicitly UNPROVED:** a malicious principal executing arbitrary
Python *inside the owner process*. That adversary can monkeypatch the owner, the C1
producer, `semantic_hash`, or the ingress itself. Nothing in this module defends against
that, and no test claims it does.

**NOT deployed security.** This is one process, no isolation was verified, and nothing here
is runtime remote proof. Claiming deployed security remains HOLD.

**NOT a trust root and NOT an EE14 grant.** The receipt is a *technical* origin receipt. It
is `authorizing=False`, carries no grant ref, no EE14 grant and no currentness, and it is
not an independently administered root. The applicability scope is `TEST_ONLY_UNISSUED`
with `issued=False`.

## Relationship to my HQ260 diagnostic

The HQ260 test asserts the provenance vulnerability and that no ingress module exists. It is
a **quarantine-branch diagnostic**. It is not imported, not reinterpreted, and must not be
cited as green owner-ingress acceptance. This HQ262 module is a separate, new artifact on a
separate branch under a different, explicitly narrowed threat model.

## What remains unbanked

The commission's specific four-respondent XOR figures (q1 = C|A=1 at 1/2,1/2 with joint
denominator 2; q2 = C|A=1,B=0 at 0/1 with denominator 1) are **not** reproduced. The court
uses the accepted source-free C1 AT07 fixture instead, which exercises genuine producer
origin but not those exact marginals. Typed negative grain (`VALID_EMPTY`, `NONCOMPARABLE`,
`UNDERPOWERED`, `UNKNOWN_OR_UNRESOLVED`), altered in-flight authority, and cross-source /
walkback-proxy refusal at this ingress are also **not** banked. All are recorded in
`01_…json` as non-coverage rather than glossed.

`G0b` EE14 model-use permission, FF02 LiTS positive relation, EE12/C7 pair authority and V3
are **UNISSUED**. Because the owner can run C1 over genuine source-free fixture material,
this lane did **not** need to return `G0B_OWNER_PERMISSION_REQUIRES_ADOPTION`; but it also
did not obtain any real permission, and none is claimed.
