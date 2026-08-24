# REC-01 V2 adjudication return

Court state: `EXECUTION_BLOCKED__NO_SUBSTANTIVE_TIR014_VERDICT`

P0: exact branch and launch head passed.

P1: passed using the immutable R06 sibling access patch. The R06 commit and all three exact sibling paths were verified/read without merge, rebase, or cherry-pick.

P2: passed. Expected and observed WVS7 SHA-256 are both `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`.

P3: `STOP__FIELD_BINDING_AMBIGUOUS`. The required exact WVS7-specific governed C11 projection and the exact PD01/R14 probe/crosswalk inputs cited by R06 are unavailable. The generic C05R2A implementation is expressly not a WVS7-specific projection authority.

Source rows tested: `0`

Physical cells tested: `0`

Populated occurrences tested: `0`

Special/absence cells tested: `0`

FD collisions: `0__NOT_EVALUATED`

Missing projections: `0__NOT_EVALUATED`

Ambiguous projections: `0__NOT_EVALUATED`

Carrier-only determinants: `0__NOT_EVALUATED`

Typed-absence collisions: `0__NOT_EVALUATED`

Slot/rank preservation failures: `0__NOT_EVALUATED`

Exceptions: `0__NOT_EVALUATED`

No substantive TIR-014 verdict is issued.
