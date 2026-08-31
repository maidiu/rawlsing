# Silent local completion attack

Protocol ruling: FAIL_CLOSED by text.

Machine ruling: `BYPASS_FOUND`.

The constitution correctly says local completion remains project-open until central reconciliation, and launch/return protocols require explicit obligation dispositions and a return destination.

The validator, however, does not compare a declared touched-obligation set with returned dispositions, does not require any touched disposition at all (`all([]) == True`), does not require central-state changed/unchanged declarations, and does not verify that any central ledger was actually updated. A packet can therefore represent local PASS while omitting the material central reconciliation and still receive validator PASS if the other shallow fields are populated.

This is a machine-level silent-completion bypass even though the prose constitution names the correct status `LOCAL_COMPLETE_UNRECONCILED`.
