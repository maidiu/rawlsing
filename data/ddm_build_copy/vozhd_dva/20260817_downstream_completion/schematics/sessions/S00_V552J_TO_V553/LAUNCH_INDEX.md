# S00 Launch Index

**Session:** S00 — V552J → V553  
**Execution:** two independent read-only schematic breakouts, then Vozhd reconvening  
**Later seams:** blocked

## Integration branch

`agent/vozhd-dva-s00-integration`

The integration branch is pinned from the finalized S00 packet snapshot. Worker branches are created from the same snapshot and open draft PRs back to this branch.

## S00-F — forward from V552J

- Branch: `agent/vozhd-dva-s00-forward-v552j`
- Assignment: `schematics/sessions/S00_V552J_TO_V553/FORWARD_V552J/ASSIGNMENT.md`
- Return:
  - `schematics/sessions/S00_V552J_TO_V553/FORWARD_V552J/RESULT.md`
  - `schematics/sessions/S00_V552J_TO_V553/FORWARD_V552J/RESULT.json`
- Production edits: prohibited.

## S00-B — backward from V554

- Branch: `agent/vozhd-dva-s00-backward-v554`
- Assignment: `schematics/sessions/S00_V552J_TO_V553/BACKWARD_V554/ASSIGNMENT.md`
- Return:
  - `schematics/sessions/S00_V552J_TO_V553/BACKWARD_V554/RESULT.md`
  - `schematics/sessions/S00_V552J_TO_V553/BACKWARD_V554/RESULT.json`
- Production edits: prohibited.

## Isolation law

The two breakout workers may share canonical source/context files but must not read one another's result files before submission. Their disagreement is evidence for reconvening, not something they should negotiate away independently.

## Vozhd reconvening

After both accepted reports are present on the S00 integration branch, Vozhd writes:

`schematics/synthesis/S00_V552J_TO_V553_RULING.md`

S01 remains blocked until that ruling reaches `VOZHD_ADJUDICATED` and explicitly states the V553 output contract that becomes S01 upstream law.
