# SRC04 runtime-overlay blocker

R2 used the base repaired v2 config and stopped at:

`UNBOUND_RESPONSE_CELL: {"row": 1, "slot": (176, "q716withoutmorocco")}`

The required input is the accepted intermediate runtime config:

- canonical SHA-256 `ba886d87763fdeb4d91df784b9672d6604081c9eaf81fd9ef6b3d334d4a387e0`
- added rule counts `q715withoutmorocco=303`, `q716withoutmorocco=327`, `q715incomedeciles=4`, `q716incomedeciles=2`

Known local historical evidence contains the hash/counts, not the exact bytes. The base v2 and initial campaign-a local release are insufficient. Rebuilding from the original source is forbidden in this repair; guessing numeric domains is prohibited. Therefore the exact blocker is **missing retained ba886d runtime-config bytes**, not a writer or selection defect.

The base selected slice is complete for all 177 response fields and 3 coordinates; q217 remains held at 38 unbound cells. The corrected runner requires the ba886d overlay and refuses before source if it is absent.

No original source was opened, stat'ed, hashed or decoded in this repair. No writer build was run.
