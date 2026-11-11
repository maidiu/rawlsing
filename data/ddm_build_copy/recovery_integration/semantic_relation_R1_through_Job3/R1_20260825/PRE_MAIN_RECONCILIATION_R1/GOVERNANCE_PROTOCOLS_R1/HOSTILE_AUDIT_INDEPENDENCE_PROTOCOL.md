# HOSTILE AUDIT INDEPENDENCE PROTOCOL R1

A governance-enforcement candidate may not manufacture its own audit proof.

Machine-enforceable independence is procedural rather than psychological: the repository cannot cryptographically prove that two AI conversations were cognitively independent, but it can prove that audit authority was issued outside the candidate lineage and that the audit result remained confined to an authorized hostile-audit branch and write scope.

For any future enforcement candidate, the canonical predecessor must require all of the following:

1. an immutable `HOSTILE_AUDIT_AUTHORIZATION_R1` JSON artifact;
2. the authorization commit is an exact direct child of the live canonical PRE-MAIN head, not a descendant of the candidate;
3. the authorization names the exact candidate SHA, expected audit branch, audit-only write prefix, challenge nonce, exact allowed PASS rulings, and allowed terminal-token prefixes;
4. the authorization commit changes only an audit-authorization path and no governance-enforcement protected path;
5. the hostile audit runs on the separately named authorized branch whose base includes the exact candidate;
6. the immutable `commit:path` audit-result reference must use the exact current tip commit of the authorized audit branch;
7. the candidate is an ancestor of that audit-result/tip commit;
8. every candidate→audit changed path lies beneath the authorized audit-only prefix;
9. no governance-enforcement protected file changes in the audit branch;
10. the immutable audit-result JSON validates against `HOSTILE_AUDIT_RESULT_SCHEMA_R1.json`;
11. audit result candidate SHA, authorization ref, challenge nonce and audit branch all exactly match the authorization/Git state;
12. `overall_ruling` must be an exact member of the authorization's `allowed_pass_rulings`; substring matching such as `READY` or `_PASS` is forbidden;
13. `terminal_token` must begin with an explicitly authorized token prefix.

The audit-result JSON does not declare its own containing commit SHA. Git identity is supplied by the immutable `commit:path` reference passed to the canonical-predecessor meta-validator, eliminating any impossible self-referential commit requirement.

The external authorization artifact is the project-level attestation predicate. A candidate branch cannot satisfy this gate using evidence stored only in its own lineage.

## Trust boundary

This protocol does not pretend Git can establish the inner cognitive independence of an AI worker. That remains an external delegation fact. What the machine proves is that a competent external authorization act existed outside the candidate lineage before the hostile result was accepted, and that the authorized audit was branch-separated, candidate-bound, jurisdiction-pure and exact-ruling-bound.

## Bootstrap

The first installation of this protocol occurs while the live PRE-MAIN predecessor does not yet contain the meta-validator. That one installation may proceed only through:

- exact W56E successor candidate;
- a separate external authorization artifact rooted directly at the current canonical PRE-MAIN;
- an independent hostile audit of the exact candidate using the authorization challenge;
- an explicit external Vozhd/HQ PRE-MAIN movement after hostile PASS.

After that installation, there is no bootstrap exception. Future enforcement changes must be evaluated by the canonical predecessor copy of the meta-validator plus this authorization protocol.
