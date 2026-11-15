# VOZHD SWEEP PROTOCOL R1

The recurring central hammering loop:

1. Verify canonical project head and Ground version.
2. Read `00_RAWLSING_GROUND.md` when entering a new decision context.
3. Sweep `CENTRAL_PROJECT_STATE_R1/00_STATE_NOW.md`.
4. Sweep `PROJECT_STATE.tsv`, `OPEN_OBLIGATIONS.tsv` and `REINTEGRATION_LEDGER.tsv` for stranded/unbanked/blocked/return-required state.
5. Inspect `DEPENDENCY_RETURN_GRAPH.tsv` and `NEXT_ACTIONS.tsv` for dependency-ready fronts.
6. Descend into only the campaign/evidence routes materially relevant to the next decision.
7. Issue a grounding receipt.
8. Launch bounded workers with exact state/obligation IDs, authority ceilings and return destinations.
9. Consume returns; do not equate local success with project closure.
10. Update obligations, dependency/return edges and reintegration state.
11. Bank/adopt only through the adoption gate.
12. Re-anchor the cumulative canonical project ancestry.
13. Repeat.

The objective is continuous project attack without context-loss or periodic repository-wide rediscovery.
