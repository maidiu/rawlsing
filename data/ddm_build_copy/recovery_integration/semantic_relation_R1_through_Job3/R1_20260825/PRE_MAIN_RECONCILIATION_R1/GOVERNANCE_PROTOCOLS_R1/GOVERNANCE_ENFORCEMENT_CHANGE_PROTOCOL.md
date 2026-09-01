# GOVERNANCE ENFORCEMENT CHANGE PROTOCOL R1

Governance enforcement is constitutionally self-protected.

Protected paths are enumerated in `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`.

A candidate that changes any protected path is **not allowed to self-adopt**. The candidate validator must report `GOVERNANCE_SELF_INTEGRITY = false` while its protected blobs differ from live canonical PRE-MAIN, and `ADOPTION_ELIGIBLE = false` regardless of the packet's self-claims.

## Lawful change sequence after bootstrap

1. begin from exact live canonical PRE-MAIN;
2. make the enforcement candidate on a separate branch;
3. record the candidate as `LOCAL_COMPLETE_UNRECONCILED`;
4. perform an independent hostile audit from outside the candidate authorship context;
5. validate the exact candidate + exact hostile-audit evidence using the **canonical predecessor copy** of `tools/validate_enforcement_candidate_from_canonical.py`;
6. if that predecessor gate passes, competent VOZHD/HQ may advance canonical PRE-MAIN to the exact audited candidate by an explicit reintegration act;
7. only after canonical movement does the new enforcement version become eligible to validate ordinary adoptive packets.

The meta-validator self-checks that its executing blob is exactly the blob at live canonical PRE-MAIN. A modified candidate copy therefore cannot stand in for the predecessor gate.

## One-time bootstrap installation

The live PRE-MAIN preceding this protocol does not yet contain the canonical-predecessor meta-validator. Therefore the first installation of this protocol cannot satisfy step 5 without circularly pretending the new script is already canonical.

Exactly one bootstrap is allowed: the exact W56C candidate must remain off PRE-MAIN, receive an independent W56D hostile PASS that explicitly audits this bootstrap/self-modification boundary, and then be integrated only by an explicit external VOZHD/HQ canonical-ref act. The candidate validator itself remains non-self-adoptive throughout. Once that exact candidate is canonical, this bootstrap exception is exhausted permanently; all later enforcement changes require the canonical-predecessor meta-validator sequence above.

No candidate validator, schema, scope registry, anti-resurrection map, helper library, protected-path manifest, or meta-validator can be its own proof of adoption.

The predecessor/auditor/ref-movement separation is the enduring security boundary.
