# MACHINE ENFORCEMENT REQUIREMENTS R1

W55B should implement a small deterministic fail-closed validator, not an orchestration platform.

Given a grounding/adoption packet plus central-state files, the validator must be able to emit at least:

- `GROUNDING_PASS`;
- `CANONICAL_PROJECT_HEAD_MATCH`;
- `GROUND_VERSION_MATCH`;
- `KNOWN_STATE_IDS`;
- `KNOWN_OBLIGATION_IDS`;
- `AUTHORITY_CEILING_DECLARED`;
- `RETURN_DESTINATION_DECLARED`;
- `TOUCHED_OBLIGATIONS_DISPOSITIONED`;
- `NEW_OBLIGATIONS_REGISTERED`;
- `SUCCESSOR_RETURN_PATH_DECLARED`;
- `REINTEGRATION_STATUS_VALID`;
- `ANTI_RESURRECTION_ACKNOWLEDGED`.

For project-level adoption, missing/unknown required fields must produce FAIL, not warning-success.

The validator should not decide whether an architecture is good, whether an obligation is substantively closed, or whether historical evidence should be promoted. Those remain competent grounded authority decisions.

A bounded execution packet may point to an exact valid grounded parent receipt instead of repeating full decision grounding. The validator must confirm the inheritance relation and authority ceiling.

Keep the implementation reviewable: schemas + one validator + fixtures representing valid grounded decision, valid bounded execution, deliberately ungrounded exploration rejected for adoption, missing-return-path rejection, stale-head rejection and unresolved-touched-obligation rejection.
