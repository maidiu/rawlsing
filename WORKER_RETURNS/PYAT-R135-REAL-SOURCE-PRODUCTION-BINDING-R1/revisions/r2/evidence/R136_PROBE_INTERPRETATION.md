# R136 frozen probe replay interpretation

Command: `.r61/r137-production-repair/probes/test_r136_production.py`.

Actual: `2 passed, 3 errors`.

- Passed: actual-value/restore probe; actual supported-fact probe.
- Error: foreign query authority source, foreign descriptor, foreign source authority.

The three frozen negative probe bodies call the old builder and assert a returned
non-positive result. The repaired builders now raise fail-closed refusal
exceptions before building/executing. The exact codes are recorded in
`PROOF_RECEIPT.json`; these are refusals, not accepted results. The frozen probe
file was not modified.
