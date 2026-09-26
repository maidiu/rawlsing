# RAWLSING HQ CURRENT — MEASURED LAUNCH AUTHORIZED

Status: `MEASURED_LAUNCH_AUTHORIZED__LITS_I_ABC_AND_WVS7_ABC__NO_OTHER_EXECUTION_AUTHORIZED`

Checkpoint: `20260926T0149-0400`

Decision: `HQD-2026-09-26-107`

Semantic PRE-MAIN tip:
`b83905cc12415f975831982dd2f396150045d87f`

Protected execution:
`16f5e7d5f691e908d85dc1dd26b8a59a29f668f4`

Operative measurement control:
`agent/vozhd-fiabc-split-r2-fanin-r1`
checkout tip: `cee9e27d57dc72771d9c3ec5df26493321feeef5`
qualified implementation: `ed8dabf015d1fd4b4ade9b55816a420b0bc1811e`

Physical epoch:
`fc6afc9bc7b287f8fd0654e1da546faee7e6c85491e6735ebe4a161b0db3de35`

Canonical pair receipt identity:
`23b09690726319306e7e40c0d2af7106f1d7a44fef03e917f85002d8c3d99b12`

Pair terminal:
`PASS__PAIR_COMPATIBLE_BEFORE_MEASUREMENT`

## Explicit authorization

Exactly one fresh measured source-local run is authorized on each already-qualified host:

- `LITS_I/A -> B -> C`
- `WVS7/A -> B -> C`

The launches may run concurrently.

The canonical launcher is:
`HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh`

Each launch must consume its own exact qualified machine-readiness receipt and the exact canonical pair receipt above.

## Not authorized

No source-local S17.
No P2.
No architecture selection.
No adaptive repair after measured entry.
No code/package change.
No silent retry.
No cleanup/resume of a failed measured root.
No historical-root reuse.

If a measured run fails, preserve the work root exactly and return the terminal evidence.

After each terminal:
portable source evidence closure -> repo-live delta binding -> hardened merge -> HQ adjudication.

P2 remains blocked.
