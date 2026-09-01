# New-obligation transaction

Classification: `OVERSTRICT_BUT_SAFE` / terminal shorthand `overstrict-safe`.

A packet cannot introduce an ID absent from canonical OPEN_OBLIGATIONS; both work-return and update new-obligation lists must agree and be subsets of the existing ledger. This prevents silent unregistered creation. It effectively requires pre-registration / prior central-state update rather than an atomic packet-plus-ledger insertion. The model is operationally overstrict but is not a fail-open bypass and does not by itself prove an impossible cycle.