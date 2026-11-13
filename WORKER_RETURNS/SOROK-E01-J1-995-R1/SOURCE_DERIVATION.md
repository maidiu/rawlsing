# E01/J1 source derivation — B + C + D on the shared ancestor

**Grade:** `SOURCEFREE_S2_ONLY`.
**Status:** `J1_PARTIAL_EXACT_BLOCKER` (upstream causal chain executable; terminal child performed event has no competent owner).
**Machine record:** `SOURCE_DERIVATION.json`.

## Heads and ancestry

| Role | Exact commit |
|---|---|
| Common ancestor | `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34` |
| B (CG-B material) | `1161e5f74081888bd813825b3df4afab3e2f5ca7` |
| C (CG-C parent/speech) | `fa80f7a88533dabf70eda7a108e71dc377cbd910` |
| D (CG-D Nadia/P3) | `85793cb74a9c2deb66570059a65b3f84b776c72e` |
| Composition B into D | `7e9b3f7e2` |
| Composition C into D+B | `58361bf20` |
| Code/test cut | `c724d1a89626f3e177acd004c0be20029dc7ade4` |

Verified merge bases:

```text
D-B: 7663067647c945126d183c59cec6c6bfc8a09ab3
D-C: 1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34
B-C: 1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34
```

`1510d835...` is an ancestor of B, C and D. B and C do not contain one another; D does not contain either latest head. The two merge commits preserve the exact B and C heads as parents; no rebase, no squash and no synthetic replacement of their histories.

## Composition rule

1. Start at assigned D head `85793cb74a9c2deb66570059a65b3f84b776c72e`.
2. Merge exact B head `1161e5f74081888bd813825b3df4afab3e2f5ca7` with `--no-ff`. Git produced a clean merge. The result matches B's B01–B05 files byte-for-byte; D's D02/D03 files remain present.
3. Merge exact C head `fa80f7a88533dabf70eda7a108e71dc377cbd910` with `--no-ff`. Git produced a clean merge. The result matches C's parent/decision/speech/P6 files byte-for-byte; B's newer typed/currency files and D's P3 files remain present.
4. No conflict resolution weakened or deleted a test. C's older B04/B05 fork is superseded by B's exact newer typed/currency head, not by a local rewrite.
5. One bounded truthfulness correction was applied to C's inherited `parent_decision.py`: a `HOLD` action now reports `physical_admission = "HELD"` instead of `"VALID_EMPTY"`. This matches C's own C03/C04 ABI (`PERFORMED | VALID_EMPTY | HELD`) and is the only production edit after the B/C merges.

## Key file hashes

The complete table is in `SOURCE_DERIVATION.json`. Selected values:

| File | B head | C head | D head | Composed code cut |
|---|---|---|---|---|
| `B04/material_operations.py` | `e3b428df...c513d0b` | — | — | same as B |
| `B05/rolling_reproduction.py` | `efce28ef...334293e` | — | — | same as B |
| `C parent_activity.py` | — | `775552b9...8b5e27` | — | same as C |
| `C parent_decision.py` | — | `64208c11...e06a810` | — | `0fa40ee8...c034d4` (HOLD label fix) |
| `C parent_speech.py` | — | `b86f0c18...2002f33` | — | same as C |
| `C run_p6.py` | — | `d7211a4c...f7594f` | — | same as C |
| `D p3/immediate_uptake.py` | — | — | `0329e85d...108982` | same as D |
| `D p3/situated_context.py` | — | — | `38bc8816...d34dee` | same as D |
| `D p3/p3_owner.py` | — | — | `81be18da...31b44b` | same as D |
| `D p3/state_store.py` | — | — | `fc878ce9...02589a` | same as D |

## Source-pin position

- D03 retains its exact selected reader closure. It pins P3 owner/store/rules/projections/compression, parent speech, supporting actor and S45 projection.
- The J1 adapter adds its own outer closure for the files it actually reads: D03's closure plus `run_p6.py`, `situated.py`, `house.py`, B02 `historical_period.py`, B04 `material_operations.py`, `parent_decision.py` and `parent_activity.py`.
- The J1 test verifies the closure hash and refuses a changed expected hash.
- P3 prior roots from older cuts remain incompatible. This composition uses fresh actual-P2/P3 roots; no migration or pin weakening was attempted.
- No CG-A `#982`/`#992` source or branch was imported, modified or treated as green. No protected PRE-MAIN write or merge occurred.
