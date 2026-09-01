# Canonical dependency regression — FAIL

The exact live canonical commit is `8b13b67df8f055761b432191eca564c1840250ec`.

`git ls-tree -r` at that commit found **no** entries for:

- `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv`
- `HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json`
- `HOSTILE_AUDIT_RESULT_SCHEMA_R1.json`
- `tools/validate_enforcement_candidate_from_canonical.py`

Those files exist only in candidate `6e50b535c319d68472bfa78fadaeac6ab0ec595c`. Accordingly, authoritative execution reported `CANONICAL_PROTECTED_MANIFEST_LOADED=false`, both canonical schema availability checks false, canonical dependency closure false, and executing-copy-is-canonical-predecessor false. This is a blocking G11 failure; no assertion of candidate-loaded data safety is made.

