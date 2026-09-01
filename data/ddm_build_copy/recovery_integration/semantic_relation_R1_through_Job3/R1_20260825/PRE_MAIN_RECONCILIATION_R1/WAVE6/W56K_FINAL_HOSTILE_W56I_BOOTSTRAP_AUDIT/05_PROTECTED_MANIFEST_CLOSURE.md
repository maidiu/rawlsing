# Protected manifest closure

## G5 — PASS at repository-file payload level

The candidate tree contains the predecessor validator, protected manifest, authorization schema, result schema, audit-independence protocol, enforcement-change protocol, ordinary governance validator and ordinary support surfaces.

## G6 — PASS at declared protected-path level

Candidate `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv` explicitly protects:
- itself;
- `tools/validate_enforcement_candidate_from_canonical.py`;
- `HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json`;
- `HOSTILE_AUDIT_RESULT_SCHEMA_R1.json`;
- `GOVERNANCE_ENFORCEMENT_CHANGE_PROTOCOL.md`;
- `HOSTILE_AUDIT_INDEPENDENCE_PROTOCOL.md`;
- `tools/governance_r2_support.py`;
- `tools/validate_governance_packet.py`;
- the ordinary packet/closure schemas and enforcement maps named by the post-bootstrap governance contract.

Thus W56J's missing-canonical-file observation does not establish candidate payload incompleteness.

This PASS is deliberately limited to repository artifact declaration. Executable dependency closure fails separately because the predecessor validator invokes an unpinned `git` executable via process PATH.