# W55B fixture independence audit

Ruling: `PARTIAL_FIXTURES`.

The recorded 12/12 expectation match is genuine, but the suite does not substantively cover all constitutional attack paths.

Substantive examples:
- F03 does test explicit deliberately-ungrounded exploration and correctly fails adoption.
- F04 tests an actually empty return destination.
- F06/F07 test unknown state/obligation IDs.
- F09 tests an actually empty successor return list.

Material fixture gaps/mischaracterizations:
- F01 'valid grounded decision' omits several fields required by `GROUNDING_RECEIPT_SCHEMA.json` (`may_decide`, `may_not_decide`, `dependencies`) yet passes because the validator never invokes the schema. It also accepts `anti_resurrection_constraints: ["none"]`.
- F02 is named `VALID_BOUNDED_EXECUTION_WITH_EXACT_GROUNDED_PARENT`, but contains no exact grounded-parent receipt/ref at all. Passing it demonstrates the bypass.
- F05 tests internal disagreement between packet head and receipt head, not both fields carrying the same stale head against the actual current PRE-MAIN ref.
- F08 tests one present obligation with an empty disposition, not the vacuous `touched_obligation_dispositions: []` case.
- F12 tests literal `reintegration_status: PROJECT_CLOSED`, not a project-closed claim in ignored `local_status` paired with an open/unreconciled reintegration status.

These are not decorative fixtures: several paths are real. But critical adversarial cases are absent, and code inspection exposes bypasses the 12/12 matrix cannot close.
