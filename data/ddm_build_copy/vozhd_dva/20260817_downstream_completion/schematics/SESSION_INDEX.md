# Schematic Session Index

The sessions are ordered by transformation chain, not by worker identity.

The sequencing law is **one seam at a time**. Multiple independent breakout workers may operate concurrently inside the active seam, but the next seam does not launch until Vozhd Dva has reconvened the active seam, adjudicated its competing models, and recorded the accepted upstream output contract that will bind the next session.

| ID | Seam | Current-stage responsibility under study | Status | Breakout pattern | Vozhd synthesis |
|---|---|---|---|---|---|
| S00 | V552J → V553 | temporalize governed upstream structural evidence without reconstructing its identity | `PACKETS_READY` | forward from V552J + backward from V554 | awaiting returns |
| S01 | V553 → V554 | convert historically situated structural pressure into bounded affordance while retaining temporal/structural authority | `BLOCKED_BY_S00_SYNTHESIS` | forward from accepted V553 output + backward from V555 | pending |
| S02 | V554 → V555 | create structural mediation route/condition semantics without instantiating biography | `BLOCKED_BY_S01_SYNTHESIS` | forward from accepted affordance output + backward from V556 + hostile inference critic | pending |
| S03 | V555 → V556 | create structural pressure-flow topology and attractor prerequisites from mediated routes | `BLOCKED_BY_S02_SYNTHESIS` | forward from accepted mediation output + backward from downstream runtime needs + critic as needed | pending |
| S04 | V556 → V557 | preserve runtime-authorized topology while adding renderer/source-generation separation | `BLOCKED_BY_S03_SYNTHESIS` | forward from accepted V556 output + renderer-boundary critic | pending |
| S05 | V557 → V558 | normalize preserved priors into governed runtime input without semantic starvation | `BLOCKED_BY_S04_SYNTHESIS` | forward from accepted V557 output + backward from V3 | pending |
| S06 | V558 → V3 | define lawful runtime-prior handoff and boundary between structural affordance and generated actor history | `BLOCKED_BY_S05_SYNTHESIS` | V558 forward + V3 backward | pending |
| S07 | V3 → V2 | expose generated state/history for phenomenological expression without granting V2 causal authority | `BLOCKED_BY_S06_SYNTHESIS` | V3 forward + V2 backward | pending |

## Active session

S00 only.

Canonical session workspace:
`schematics/sessions/S00_V552J_TO_V553/`

Breakout cells:
- `FORWARD_V552J/ASSIGNMENT.md`
- `BACKWARD_V554/ASSIGNMENT.md`

Common return schema:
- `REPORT_FORMAT.json`

Vozhd reconvening surface:
- `schematics/synthesis/S00_V552J_TO_V553_RULING.md`

## Launch discipline

- Only one seam is active at a time.
- Inside S00, the two independent perspectives launch from the same pinned base.
- They do not read one another's return before submission.
- Production code is read-only for both S00 workers.
- Each worker writes only `RESULT.md` and `RESULT.json` in its assigned S00 cell and opens a draft PR to the S00 integration branch.
- Vozhd Dva reviews both returns, merges accepted reports to the S00 integration branch, reconvenes them, and writes the S00 ruling.
- Only an adjudicated S00 ruling may promote S01 to `READY_TO_LAUNCH`.

## Progression

`S00 breakout → S00 synthesis → S01 breakout → S01 synthesis → ... → S07 synthesis`

A later seam may be inspected during backward reasoning as consumer context, but it cannot freeze architecture before its upstream input law exists.
