# CANDIDATE PROTECTED-MANIFEST MUTATION ATTACK

The trusted protected set is built only from `canonical_text(live, MANIFEST_REL)`.

Accordingly a future candidate copy of `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv` that removes the meta-validator, authorization schema, result schema, or other protected files does not directly alter the predecessor's intended trusted protected set.

The dependency-closure check additionally requires `{SELF_REL, MANIFEST_REL, AUTH_SCHEMA_REL, RESULT_SCHEMA_REL} <= protected` from the canonical-loaded manifest.

Direct candidate-manifest weakening classification: `FAILS_CLOSED / SAFE`.

Separate blocker: a candidate-created Python module such as `tools/argparse.py` is executable through interpreter import resolution even though it is not a trusted manifest input.