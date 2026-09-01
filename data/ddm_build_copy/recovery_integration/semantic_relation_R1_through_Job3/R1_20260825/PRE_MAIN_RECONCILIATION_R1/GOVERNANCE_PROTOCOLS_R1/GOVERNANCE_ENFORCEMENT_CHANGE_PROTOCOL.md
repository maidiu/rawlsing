# GOVERNANCE ENFORCEMENT CHANGE PROTOCOL R1

Governance enforcement is constitutionally self-protected.

Protected paths are enumerated in `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`.

A candidate that changes any protected path is **not allowed to self-adopt**. The candidate validator must report `GOVERNANCE_SELF_INTEGRITY = false` while its protected blobs differ from live canonical PRE-MAIN, and `ADOPTION_ELIGIBLE = false` regardless of the packet's self-claims.

Lawful change sequence:

1. begin from exact live canonical PRE-MAIN;
2. make the enforcement candidate on a separate branch;
3. record the candidate as `LOCAL_COMPLETE_UNRECONCILED`;
4. perform an independent hostile audit from outside the candidate authorship context;
5. if the audit passes, competent VOZHD/HQ may advance canonical PRE-MAIN to the exact audited candidate by an explicit reintegration act;
6. only after that canonical movement does the new enforcement version become eligible to validate ordinary adoptive packets.

No candidate validator, schema, scope registry, anti-resurrection map, or helper library can be its own proof of adoption.

This protocol deliberately leaves the final canonical-ref movement outside the self-modifying validator. That separation is the security boundary.
