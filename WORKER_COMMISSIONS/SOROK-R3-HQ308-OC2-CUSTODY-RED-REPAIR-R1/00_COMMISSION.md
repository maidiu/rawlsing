# SOROK HQ308 OC2 — OC1 test-only repair

Repository: maidiu/rawlsing (private).
Role: source-free Python prototype implementer, not HQ or acceptance authority.
Branch: agent/rabochii-sorok-r3-hq308-oc2-custody-red-repair-r1
Parent: bea91e19ee77e2909bda700effb0ad358dff66e5
Startup: the new commit SHA after creating this commission, to be verified directly before work.
Allowed writes: WORKER_RETURNS/SOROK-R3-HQ308-OC2-CUSTODY-RED-REPAIR-R1/ only.
Model and environment: GPT-6 Medium, one Browser/GitHub agent with Python and pytest. Complete the entire task in one agent, without model, editor or harness switching.

Read Sorok 00_READ_ME_FIRST, 00B, 00C and 00D, and HQ308 intake. The original source-free prototype is at commit 19438890e43153e2bc4a1ad271b5e19bcef33e1e. The independent review is at aba637265bea2358790fea50d0e7abc98141e472. Read the full reports and test artifacts at those exact commits.

Repair the source-free candidate to satisfy its documented test-only lifecycle and data consistency requirements. Keep all 31 original cases unchanged and reproduce all 45 additional independent cases before and after changes. Add direct regression tests for the identified unsupported or inconsistent behavior, maintain complete and truthful test execution logs, and preserve deliberate NOT_REACHED owner boundaries. Never edit the reviewer or original tests to improve counts.

Return runnable candidate source, all original and additional test results, JUnit/stdout, review request, measured environment, changed paths and verified pushed remote SHA. This does not confer real independent scenario custody, live model-use permission, semantic issuance, production operation or V3 adoption.