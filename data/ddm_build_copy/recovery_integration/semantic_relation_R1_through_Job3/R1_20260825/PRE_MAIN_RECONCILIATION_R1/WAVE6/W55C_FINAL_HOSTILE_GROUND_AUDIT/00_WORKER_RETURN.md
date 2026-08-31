# W55C FINAL HOSTILE GROUND / NO-STRANDING / CONSTITUTIONAL ENFORCEMENT AUDIT — RETURN

Worker branch: `agent/rabochii-premain-w6c-final-hostile-ground-audit-r1`

Audited candidate: `integration/pre-main-reconciliation-r1 @ 8b13b67df8f055761b432191eca564c1840250ec`

Overall ruling: `BLOCKED__VALIDATOR_FAIL_OPEN`

The Ground itself is sufficient and the central state is sweepable. The blocker is the W55B machine-enforcement layer: `GOVERNANCE_PROTOCOLS_R1/tools/validate_governance_packet.py` accepts multiple packets that the constitution says must fail closed.

Ground cold questions: 22 `PASS_DIRECT`; 0 `PASS_AFTER_DECLARED_ROUTE`; 0 `AMBIGUOUS`; 0 `FAIL`.

Ground compression: `COMPACT_SUFFICIENT`.

Central hidden-state defects: 0.

Hostile bypass counts:
- ungrounded-decision bypasses: 0 for a truly missing receipt;
- shallow-grounding bypasses: 5;
- bounded-execution privilege escalations: 6;
- ungrounded-exploration direct-adoption bypasses: 0;
- stale-head bypasses: 1;
- silent-completion bypasses: 1;
- successor-parent bypasses: 1;
- blocked-work disappearance bypasses: 3 representative known cases;
- fake-project-closure bypasses: 6;
- authority-resurrection bypasses: 10;
- unknown-normalization bypasses: 5.

Validator audit: 3 `CODE_PROVES_FAIL_CLOSED`; 0 `TEST_RECEIPT_ONLY`; 0 `AMBIGUOUS`; 9 `BYPASS_FOUND`.

Fixture ruling: `PARTIAL_FIXTURES`.

Word-count variance: `LAWFUL_NONBLOCKING_VARIANCE`.

Fresh Vozhd ruling: `VOZHD_CONTINUITY_PASS`.

Material discrepancy versus W55 intent: W55A requires exact parent-inherited bounded execution, live canonical-head validation, scope-relevant grounding, complete touched-obligation disposition, typed reintegration, and meaningful anti-resurrection acknowledgement. W55B's validator does not enforce those requirements, while its 12 fixtures do not exercise the decisive bypasses.

Ref-safety proof after the audit commit:
- `integration/pre-main-reconciliation-r1` remained `8b13b67df8f055761b432191eca564c1840250ec`;
- `main` remained `0777a34e50221bde6801dbaca26c058a7350c9e8`.

Terminal SHA is returned externally because embedding a commit's own SHA in content determining that commit is self-referential.

Terminal token:

`W55C_FINAL_HOSTILE_GROUND_AUDIT_BLOCKED__GC-G11_VALIDATOR_FAIL_OPEN__NO_GLOBAL_ADOPTION`
