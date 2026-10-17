# WG0Q — independent review wake (author handoff, not an acceptance)

This is an **author-side handoff**. It is not an independent verdict, not an HQ
accession, and not an issuer/semantic-source decision. WG0Q must reproduce,
falsify and judge independently; Pyat HQ accepts or rejects afterward.

## The exact claim to test

The repaired WG0P6 module
`candidate/court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py`
(sha256 `89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`,
blob `62895078908ff748771da9a9fbcec6b36d34a803`) now binds the **constructed**
`AuthoritySnapshot.content_hash` and full semantic body into the
owner-registered release material, so a same-`(authority_id, authority_version,
authority_content_hash)` body substitution is refused **before** native I03.

## Reproduce independently (do not trust this return)

1. Verify the branch head contains this commission and the repaired module;
   verify the module sha256 and blob above.
2. Run the exact frozen WG0O oracle and unchanged adapter against the repaired
   runtime:
   `WG0O_RUN=<your-run> python3 repro/run_frozen14.py`.
   A2 must be typed HELD; A3/A4 must be typed REFUSED; all with 0 supported
   cells and 0 new I03 calls; the eight other negatives typed; P1/P2/P3 42 cells.
3. Run the inherited core yourself: `wg0m33`, `original65`, `original3`,
   `j44_k11`, `owners80`, `author26`, `fresh`. Expect 236/236 on the mandatory
   decomposition and 42/42 on the WG0P6 source-view boundary.
4. Try to break it:
   - rehash the substituted body (construct a new `AuthoritySnapshot` whose
     claimed triple is unchanged but whose body differs) — must refuse;
   - copy a compiled plan and swap `plan.releases[...].qauth` — must refuse;
   - mutate `governed_operations` to a foreign singleton — must refuse;
   - set `effective_time_or_interval` to a date or add `supersession_refs` —
     must HELD, never silently serve;
   - remove `qauth` / empty `authorities` — must stay a typed refusal, not an
     untyped `KeyError`;
   - confirm P1/P2/P3 consumer bytes are identical to the WG0O pristine record.

## Residual owner decisions (explicitly NOT made here)

1. **Issuer-side temporal interpretation.** Whether
   `require_positive_authority` (the accepted native owner) should itself
   interpret `effective_time_or_interval` / `supersession_refs` and how a
   `SUPERSEDED_NOT_REPLAYABLE` state should be typed remains an owner-science
   decision. This repair only fails closed at the adapter seam.
2. **`authority_content_hash` semantics.** Whether the claimed hash is a label
   or a semantic content binding is an owner decision; this repair binds the
   constructed body independently of the claim and does not redefine the claim.
3. **Source-artifact revocation.** `FixtureOwner.revoke()` still accepts release
   tags only; `UNKNOWN_RELEASE_NO_REVOCATION` is the honest typed ceiling. No
   independent artifact-scoped revocation was invented.
4. **Broader issuer/adoption claims.** None are made.

## Non-grants

No original35, no real external authenticated issuer, no I05/Route B, no
OC05/N11/N12/V3, no production/canonical mutation, no accepted PRE553 native
owner rewrite, no frozen oracle edit, no method adoption, no HQ acceptance.

## Known honest gaps

- WG0N hostiles 20 were not re-executed (the separate WG0M return is not in this
  lineage); the parent/WG0O record stands and the WG0M 33 court itself was
  re-run 33/33.
- `cold_pointer` is not runnable from the committed evidence (literal
  `<WORKTREE>` placeholder, missing `owner/` tree); real cold recovery is
  covered by `original65` cold nodes, which pass.
- `author69` historical 29/36 and two older characterisation scripts were not
  re-claimed.

WG0Q should treat any divergence from these claims as a finding; nothing in this
return is banked as accepted.
