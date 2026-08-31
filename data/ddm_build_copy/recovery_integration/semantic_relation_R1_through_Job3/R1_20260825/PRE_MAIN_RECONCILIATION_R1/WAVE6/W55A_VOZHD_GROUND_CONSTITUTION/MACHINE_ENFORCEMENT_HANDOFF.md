# W55B machine-enforcement handoff

W55B is mechanical only. It must not alter constitutional meaning.

Implement one small fail-closed validator from:

- `GOVERNANCE_PROTOCOLS_R1/GROUNDING_RECEIPT_SCHEMA.json`;
- `GOVERNANCE_PROTOCOLS_R1/WORK_RETURN_SCHEMA.json`;
- `GOVERNANCE_PROTOCOLS_R1/CENTRAL_STATE_UPDATE_SCHEMA.json`;
- `GOVERNANCE_PROTOCOLS_R1/MACHINE_ENFORCEMENT_REQUIREMENTS.md`.

Minimum fixtures:

1. valid grounded project-decision packet → PASS;
2. valid bounded executor inheriting exact grounded parent → PASS;
3. deliberately ungrounded exploration presented for adoption → FAIL;
4. missing return destination → FAIL;
5. stale canonical head → FAIL;
6. unknown state/obligation ID → FAIL;
7. touched obligation without disposition → FAIL;
8. spawned successor without RETURN_TO → FAIL;
9. missing anti-resurrection acknowledgement → FAIL.

Validator output should be deterministic JSON and should not adjudicate substantive architecture or semantic closure. After tests, W55B may seal the W55A constitution into PRE-MAIN only if all checks and authority/runtime inertness pass.
