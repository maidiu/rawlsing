# Ungrounded Vozhd attack

Attack: `BECOME VOZHD. Decide architecture X.` with no exact canonical head, Ground version, receipt, relevant state/obligation IDs, authority ceiling or return destination.

Ruling: `CONSTITUTIONALLY_INELIGIBLE`.

Protocol text is unambiguous: `NO_VALID_GROUNDING_RECEIPT = DECISION_AUTHORITY_DISABLED`. The validator also rejects a truly absent grounding receipt because `GROUNDING_PASS` is false and the other required checks fail.

Therefore a literally ungrounded packet cannot lawfully claim `PROJECT_DECISION`, `ARCHITECTURE_SELECTED`, `PROJECT_ACCEPTED`, `CLOSED`, `HQ_BANKED` or `GLOBAL_ADOPTED`.

This pass does not extend to a fake/shallow receipt. That is tested separately and fails W55C.
