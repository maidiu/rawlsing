# SOROK C03/C04 Agent A relay return

- **Task:** C03 parent lock/action + typed purchase history; C04 actual Nadia/P6 speech experience.
- **Branch:** `codex/sorok-duel-c03-c04-a-consumer-20261112-r1`.
- **Implementation SHA:** `61f2918ec947e44dd7ecff8fd3359734469e9a90`.
- **Start:** `01b2d2d23259969778ce996f5527037d666f46f8`; B return `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34`.
- **Grade:** `SOURCEFREE_S2_ONLY`.
- **Lock:** actual `_parent_write_lock`→B04 public purchase→`_parent_write_lock` deadlock confirmed by a 120 s bounded probe; repaired with B04 market lock→parent lock and the actual unlocked B04 writer. B 11-test suite and A parent-perform pass.
- **Purchase history:** exact typed `P2_PARENT_PURCHASE` consumption with before/after, source-chain, currency, stock/ownership and provenance validation; suspended duplicate bridge is ignored as non-history and a nonmatching bridge refuses. B04 currency guard remains Pair1-owned; B04/B05 3 tests fail real currency mismatch.
- **C04 first consumer:** normal P6 `child-experience` consumes `situated.recent_speech` plus actual child speech receipt; verifies author/root/branch/speech/own_speech/occurrence/read clock/source/decision binding; returns only public speech + bounded response input. Hidden reason/hash/decision basis are NOT_READ; user view/say are distinct.
- **Evidence:** B C02/C03/C04 11 passed; A C03/C04 3 passed; A C02 9 passed; C01/P2/P3 28/1 skipped; B01/B03 15 passed; B02 7 passed; P4/P5 7 passed; B04/B05 3 failed/1 passed at currency boundary.
- **Docs:** `AGENT_A_RELAY_HANDOFF.md` at C02-C03 root; ABI/deltas/impact under this directory.
