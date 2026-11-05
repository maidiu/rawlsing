# PROGRAMMA_DELTA — SOROK P2 explicit interval continuation R1

**Delta ID:** `SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1`
**Base:** `41bf45813fd0adeffd9b54e1306c2022abe96514`
**Result:** `PASS` focused additive continuation.

## Delta

Added an additive callable/CLI layer over the accepted S45-S47 product:

- Explicit caller-supplied S46 interval continuation (`ACTUAL`,
  `SCHEDULED_ONLY`, `DECLINED`, `CONSTRAINED`, `BLOCKED`, `UNKNOWN`).
- WAIT/ABSENCE without interval input remain typed holds; no activity is
  inferred and no ACTUAL mode is forced.
- Uses existing `run_s45_s47.py interval`/`admit` commands and the public
  `S45Projection` view/DO_HELP surface.
- First consumer consequence: public continued encounter view and DO_HELP.
- Focused evidence: ACTUAL material `0` and DO_HELP refused; SCHEDULED_ONLY
  material `1` and DO_HELP accepted; cut/restore; cold continuity; missing
  input hold.

## Not changed

- No inherited product, vendor, projection, causal harness or PROGRAMMA working
  file was edited.
- No protected PRE-MAIN write, PR697 merge or product semantic change.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human authority.
- No actor choice/motive/B state/paid counterpart fabrication.
- Not general autonomous absence life.

## Next owner action

Existing independent review of this additive commit is required before HQ
fan-in or any PRE-MAIN receiving action.
