# GOVERNANCE ENFORCEMENT CHANGE PROTOCOL R1

Governance enforcement is constitutionally self-protected.

Protected paths are enumerated in `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`.

A candidate that changes any protected path is **not allowed to self-adopt**. The candidate validator must report `GOVERNANCE_SELF_INTEGRITY = false` while its protected blobs differ from live canonical PRE-MAIN, and `ADOPTION_ELIGIBLE = false` regardless of the packet's self-claims.

Audit separation is governed by `HOSTILE_AUDIT_INDEPENDENCE_PROTOCOL.md`.

## Lawful change sequence after bootstrap

1. begin from exact live canonical PRE-MAIN;
2. make the enforcement candidate on a separate branch;
3. record the candidate as `LOCAL_COMPLETE_UNRECONCILED`;
4. competent external VOZHD/HQ creates an immutable hostile-audit authorization commit rooted directly at the live canonical PRE-MAIN, outside the candidate lineage, naming the exact candidate, audit branch, challenge nonce, audit write scope, and exact allowed PASS rulings;
5. perform the hostile audit on the separately authorized audit branch;
6. validate the exact candidate + exact authorization + exact hostile-audit result using the **canonical predecessor copy** of `tools/validate_enforcement_candidate_from_canonical.py`;
7. if that predecessor gate passes, competent VOZHD/HQ may advance canonical PRE-MAIN to the exact audited candidate by an explicit reintegration act;
8. only after canonical movement does the new enforcement version become eligible to validate ordinary adoptive packets.

The meta-validator self-checks that its executing blob is exactly the blob at live canonical PRE-MAIN. A modified candidate copy therefore cannot stand in for the predecessor gate.

The meta-validator also requires exact authorization/result schemas, direct-canonical-root authorization ancestry, branch/write-scope separation, exact candidate binding, challenge matching, and exact authorized PASS enumeration. Substring heuristics such as `READY` or `_PASS` are forbidden.

## One-time bootstrap installation

The live PRE-MAIN preceding this repaired protocol does not yet contain the canonical-predecessor meta-validator or authorization schemas. Therefore the first installation cannot execute the future predecessor gate without circularly pretending the new script is already canonical.

Exactly one bootstrap is allowed for the exact post-W56D repair candidate. It must remain off PRE-MAIN, receive a separate external audit-authorization artifact rooted directly at the current canonical PRE-MAIN, receive an independent hostile audit of the exact candidate using that authorization/challenge, and then be integrated only by an explicit external VOZHD/HQ canonical-ref act after a clean hostile ruling. The candidate validator itself remains non-self-adoptive throughout.

Once that exact candidate is canonical, the bootstrap exception is exhausted permanently. All later enforcement changes require the canonical-predecessor meta-validator + external authorization + hostile-audit sequence above.

No candidate validator, schema, scope registry, anti-resurrection map, helper library, protected-path manifest, audit-authorization schema, hostile-audit-result schema, independence protocol, or meta-validator can be its own proof of adoption.

The canonical-predecessor / external-authorization / hostile-auditor / external-ref-movement separation is the enduring security boundary.
