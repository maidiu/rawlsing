# Fixed semantic-pair tranche protocol

Global P2 semantic adjudication proceeds in fixed work units of exactly 3,000 pending queue rows whenever at least 3,000 remain.

1. Record the governing queue count before selection.
2. Select exactly 3,000 rows deterministically, using coherent semantic neighborhoods where possible and a stable ordered boundary slice where necessary.
3. Freeze and deliver the selected candidate surface.
4. Adjudicate all 3,000 rows under the embedded acceptance standard.
5. Record the exact authority partition and two-sided evidence surface.
6. Prove that selected and remaining IDs form an exact disjoint partition of the incoming queue.
7. Deterministically rebuild and hash-compare all governing outputs.
8. Package the tranche into the cumulative handoff before starting another work unit.
9. Report start count, exactly 3,000 adjudicated, end count, and observed wall-clock span.

Do not drift above the 3,000-row cap to finish a neighborhood. Carry a deterministic remainder into the next tranche.
