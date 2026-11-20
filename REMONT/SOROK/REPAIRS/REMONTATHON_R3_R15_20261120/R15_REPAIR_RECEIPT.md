# REMONT R15 bounded first-fault repair receipt

## Source cut

Inherits original R14 PR #1214 `f8c0d8dc901116d5fd1bfa7ec992dffa90a9aef0`. Isolated fresh research candidate, no modifications to the R14 review head.

## P012 — defeated inhibitor propagation

**RED on frozen R14:** A/B/C simultaneously actor-accessible forms with A inhibits B and B inhibits C: the all-potential veto erroneously suppressed both B and C. C's action was lost even though its only inhibitor B was defeated by A. Two of four new P012 tests failed (including order permutation). Distinct positives demonstrate conservative mutual inhibition and a source dependent on blocked support must not acquire a fictional action.

**Repair:** Existing `constitution.compose` keeps the two-stage joint-link/motif potential fixed point, adds a **deterministic acyclic inhibition-court stratification** and demands that its actual *post-recruitment* inhibitory edges exactly justify the proposed veto. Where cyclic or source-dependent decisions are ambiguous, it retains the prior conservative policy. No additional actions, forms, bodies or world authority issued. This is a bounded correctness repair, not a theory of unconscious motivational resolution. P012 remains PARTIAL.

## P018 — auxiliary source and event identity

**RED on frozen R14:** generic commit could emit a hash-consistent `SOURCE_SEAL` audit event with no accompanying seal row; verify_chain accepted that ghost source event. A direct unanchored `constraints` row was invisible to verify_chain, and a source() read exposed a modified canonical source record before any explicit verify. Six of the initial nine tests failed total (four P018 cases plus two P012). Additional first-red stage: malformed sid/type inputs could mutate genesis or late-seal history, leaving malformed irreversible source metadata.

**Repair in existing `storage.ResearchLedger` owner:**
- Reserve INIT/SOURCE_SEAL kinds for their atomic issuer, refuse generic commit.
- Validate source IDs and categories before initial or late sealing. Invalid attempts leave no event/row.
- Check actual canonical source content and its SHA-256 digest against exact genesis/late-seal event anchors **before appending or reading**, rejecting orphan, duplicate, malformed or mutated seals.
- Independently verify every source-seal event has exactly one matching source ID/digest mapping. Non-source events cannot assert source-seal anchors.
- Explicitly refuse nonempty unanchored `constraints` table, rather than certify a ledger with auxiliary state outside its recorded world event ancestry.
- Existing valid late source seals, frozen genesis seals and SQLite cold reopen continue to work. Cryptographic hashes here are not keys, signatures or externally credentialed source authorization.

P018 remains PARTIAL: privacy/disclosure, native seal issuer, original source rights and adversarial database-writer tamper-proofing remain unissued.

## Execution and verdict

At current local Python 3.13.5: 276/276 unittest normal PASS, 276/276 unittest `-O` PASS, 276 pytest passes plus 22 subtests. Nine-event demo chain cold-verified. Requires fresh cold-archive execution on the exact committed Git source and independent hostile source/semantic review; not independently accepted. P009's native privacy side cannot be granted by a new sourcefree method; stays held.

Re-review especially: self-inhibitory/mutual cycles, source-dependent ungrounded alternatives, canonical source row mutation, unsupported auxiliary constraints, and `SOURCE_SEAL` events that look hash-consistent but lack a historical issuer. No new defect identities or status promotion; annotations under P012/P018 only.
