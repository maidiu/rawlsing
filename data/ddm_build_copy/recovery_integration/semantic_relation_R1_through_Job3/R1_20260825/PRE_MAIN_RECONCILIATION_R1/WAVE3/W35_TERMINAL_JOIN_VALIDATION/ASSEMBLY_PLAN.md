# W35 ASSEMBLY PLAN

This records the exact deterministic plan used before advancing any canonical candidate ref.

1. Verify `integration/pre-main-reconciliation-r1 == daffee545fc60a8cd635aee9aafbe77a920f4c19`.
2. Create `agent/rabochii-premain-w3-terminal-join-r1` from that exact base.
3. Compare each frozen W31-W34 terminal ref directly against `daffee545...` and enumerate changed paths.
4. Refuse whole historical branch ancestry. Reuse only the adjudicated lane tree objects:
   - W31 canonical governance tree `ab93a01f...` and report tree `560549f8...`;
   - W32 report tree `227d0629...` and exact tested `rawlsing_next` tree `f5673a55...`;
   - W33 report tree `d58cb3f0...`;
   - W34 report tree `28a48fc2...`.
5. Build a synthetic Wave-3 tree from those four disjoint lane report trees.
6. Build PRE_MAIN with W31 governance + combined Wave-3 tree.
7. Attach PRE_MAIN and W32 `rawlsing_next` to the exact base root tree.
8. Create one assembly commit with sole parent `daffee545...`.
9. Validate exact tree identities, changed-file accounting, authority ceilings, denominators, anti-resurrection, open-state conservation, no-loss, and stronger-equivalent runtime proof.
10. Create `00_CANONICAL_ENTRYPOINT.md` and W35 reports only after the assembled payload exists.
11. Perform isolated cold-reader review using candidate repository surfaces and the entrypoint, not chat history.
12. Add terminal `RETURN_POINTER.json` as metadata-only finalization; rerun gates affected by documentation only.
13. Recheck candidate ref has not moved.
14. Only if PM-G1..PM-G8 are PASS and all zero-violation conditions hold, fast-forward `integration/pre-main-reconciliation-r1` to the terminal W35 pointer commit with `force=false`.
15. Verify ref equality and verify `main` remains unchanged.

No semantic collision is to be resolved by invention; W31 owns constitutional classification, W32 executable proof, W33 delegated-current carrier proof, and W34 preservation/exploration representation.
