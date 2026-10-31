# Exact remaining owner actions

## Engineering acceptance path

1. **PR #519 author**
   - Rebase/merge-forward from the current `59c9a7a4` review source onto PRE-MAIN `8e44ca9c`.
   - Preserve the exact 32-event/32-flight corpus and the F0R3 validator patch.
   - Re-lock the new head and report its exact SHA.
   - Do not silently roll the seed or edit historical events.

2. **Distinct independent reviewer**
   - Review the exact patched validator blob and the re-locked PR head.
   - Re-run the original 13 and candidate 20 witnesses against the exact current corpus.
   - Confirm N1–N7 are rejected and the legal `OWNER_ADOPTION_CANDIDATE` is accepted with `adoption=false`.
   - This review's author and the F0/F0R2/F0R3 authors cannot self-accept.

3. **Repository administrator**
   - Install/verify protection or a ruleset on `integration/pre-main-reconciliation-r1`.
   - Require the exact workflow `PRE-MAIN Branch Fan-in Receipt Integrity (sourcefree)`, job `receipt-contract`.
   - Require independent approval and no unauthorized bypass.
   - Read back `protected=true`, the exact check context, approval rule and bypass list.
   - A green optional workflow run is not sufficient.

4. **Authorized PRE-MAIN maintainer/owner**
   - Approve the exact initial 11-event seed provenance (currently `PENDING`).
   - Verify the PR head and current PRE-MAIN did not move after review.
   - Perform the protected merge/CAS only after all gates above.
   - Read back the merged target, paired Sorok/Pyat progress at the same commit/revision, and the actual importing first consumer.
   - Append `ADOPTED_CAS_VERIFIED` only after the real merge exists.

5. **Privileged verifier owner**
   - Authorize a separate verifier for signed/authorized source and science grants, merged target SHA, real first consumer, and current progress pair.
   - The offline validator cannot certify reviewer identity, source grants or adoption.

## Separate owner gates (not repaired here)

6. **Sorok incumbent:** reconcile MD revision 36 with JSON revision 35 in one truthful paired CAS publication.
7. **FIABC/Pyat owner:** classify the 144/3 governed failures against base and changed source; do not waive tests.
8. **HQ/F4 owner:** abandon or explicitly re-cut F4 (`9fb7caeb…`) from the reviewed current PR head; do not run a second control law.
9. **PR #514/#516 and source/actor owners:** no change or authority transfer is authorized by this review.

## Abort conditions

Abort the merge/CAS without adoption if any of these occur:

- PR #519 head, validator, seed, workflow or event/flight corpus moves after the reviewer locks it;
- current PRE-MAIN moves from the authorized base;
- the F0R3 patch does not apply or any witness regresses;
- the seed remains `PENDING`;
- the required check is still optional or its exact context is not read back;
- no independent review acceptance or privileged verifier exists;
- Sorok MD/JSON remains split or FIABC failures are unclassified;
- any attempt is made to treat a branch name, CI run, comment or filled field as authority.
