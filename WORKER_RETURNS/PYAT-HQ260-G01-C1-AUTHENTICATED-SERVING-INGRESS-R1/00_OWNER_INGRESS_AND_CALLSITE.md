# HQ260 G01 — C1 owner-authenticated G1 selected-serving ingress — 00 OWNER INGRESS AND CALLSITE

**TERMINAL: `HQ260_G01_RETURNED__NOT_ADOPTED`**
**Disposition: `BLOCKED_REQUIRE_TRUST_ROOT`**

No ingress module was written. That is a deliberate outcome, not an omission — see section 4.

## 1. Control resolution (live origin, not worker-local LATEST)

- live canonical `origin/integration/pre-main-reconciliation-r1` = `788b2bf7e53c35e25d3f83b638e989169f3d990c`
- this commission tip `f38a2363a4bb6de394bfcdad99692564dab1b4aa`, startup base `cb5f363b26c886c6ef855f81aa133fe194460c67`
- **The tip is NOT an ancestor of live control — they have DIVERGED.** Live control carries five
  commits past the tip (HQ260 CURRENT.json/MD prep, checkpoint manifest binding, EE14
  governance issuance, HQ pointer advance), including the HQ260 sealed EE14 competence
  instrument.
- I worked on the commissioned tip, the branch's own base. **Divergence is reported, not
  silently reconciled**, and no live-control branch was modified.

Commission-pinned blob verified at the tip:
- `rawlsing_next/pre553_analytical_composition.py` = `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` — **matches exactly**

## 2. Actual existing callsite and accepted owner flow (inspected, not assumed)

C1 producer: `compose_positioned_subject_possibility` (line 1008) of
`pre553_analytical_composition.py`, returning frozen `AnalyticalCompositionResult`
(line 335), whose `composed_result_identity_hash` carries full ancestry, authority and
provenance.

F8 ingress: `evaluate_positioned_subject_possibility(*, query, rule, evidence)` at
`rawlsing_next/source_backed_positioned_subject_possibility.py:417`, with
`verify_positioned_subject_possibility_replay` at line 458.

Evidence record: `PossibilitySliceEvidence` at line 153, with `provenance_refs` (line 163)
and `authority_refs` (line 164).

## 3. The first missing edge — banked at runtime

**`evidence` is a CALLER-SUPPLIED argument to the F8 ingress.** In that module,
`provenance_refs` and `authority_refs` appear at exactly four places: the two field
declarations (lines 163, 164) and the two `__post_init__` normalisations (lines 181, 182).
**The F8 evaluation path never reads either field.**

Runtime evidence on this commit, governed interpreter 3.11.3:

```
honest   authority_refs: ['HQ260-evidence-e']   forged   authority_refs: ['HQ260-FORGED']
honest   provenance    : provenance:e            forged   provenance    : provenance:FORGED
result_state honest=EXACT_SUPPORTED forged=EXACT_SUPPORTED  IDENTICAL=True
result_hash  identical=True
material()   identical=True
replay verifier ACCEPTED forged evidence: True
```

G1 is confirmed exactly as the commission describes: substituting
`PossibilitySliceEvidence.authority_refs` or `.provenance_refs` leaves the F8 numerical
result **and** its identity hash unchanged, **and** survives the replay verifier.

## 4. Why no code was written

The commission permits a new ingress module **only if verified necessary**, and instructs:
if code cannot authenticate producer custody under the current mutable Python trust
boundary, document the exact stronger needed owner boundary and STOP rather than declaring an
in-process self-hash secure.

There is no way to close G1 in-process that is not a caller-forgeable self-hash:

- `evidence` arrives from the caller, so any binding computed in the same process is
  recomputable by that same caller — banked directly in
  `test_caller_recomputed_hash_is_forgeable_and_therefore_not_a_trust_root`;
- the accepted owners are ordinary mutable Python modules, with no immutable owner boundary,
  no sealed producer identity and no independently administered principal at runtime;
- a new adapter would only re-wrap caller-supplied evidence behind a digest the caller can
  regenerate, which is precisely the forgery the commission forbids.

Writing one would have produced a green test and false assurance. Avoiding that is the point
of this stage.

## 5. Exact minimal precondition to unblock

1. **An immutable producer-origin binding for evidence material.** `PossibilitySliceEvidence`
   must be minted inside an owner that holds the evidence authority/provenance custody and is
   not reachable by, or recomputable from, the caller — a sealed owner boundary, not an
   in-process self-hash.
2. **The F8 ingress must accept only owner-minted evidence**, with the owner identity carried
   into the result identity so that substitution changes `result_hash`.
3. **A trusted reference for that owner identity** independent of the caller. Absent this, no
   digest over caller-held material is evidence of origin.

Until (1)–(3) exist, the correct behaviour is exactly what is banked here: substitution is
observable to tests and invisible to F8.
