# BP4 dependency and source-grade diagram

```text
A0-A3 CLI/API  (bp4/cli.py, bp4/product.py)
   |
   +-- C12Store (bp4/store.py, SQLite append-only)
   |      episodes / world_event / perception / checkpoint / fork
   |
   +-- C10 receiver (bp4/c10.py)
   |      |
   |      +-- BP1 sourcefree two-actor life (vendor/bp1, pinned b4e07ef5)
   |      |      per-actor ledgers, G18 material/action receipts, snapshots
   |      |
   |      +-- BP3 keyed C8 writer (vendor/bp3, pinned 7faaa072)
   |      |      ExclusiveJournal + keyed proof + external monotonic anchor
   |      |      c9_event_ingress.receive_event -> TEST_ONLY C8 readset
   |      |
   |      +-- C9R TEST_ONLY target (vendor/c9r, pinned 6fa29399)
   |      |      candidate.CandidateStore target_state record + later E2
   |      |      (produced through bp1.c9_bridge.run_bp1_c9)
   |      |
   |      +-- objective world (bp4/world.py)
   |             owner receipts, events, clock, positions/resources
   |
   +-- V2/M6 actor-safe ingress (bp4/perception.py -> rawlsing_next.m6_actor_safe_expression)
   |      READY_FULL_CLAIM_SCOPE only for lawfully perceived claims
   |
   +-- BP2 compatibility contract (bp4/bp2_compat.py)
          typed receiving requirement only; BP2 is a separate campaign and has
          NOT emitted a joined envelope in this return.
```

## Pinned inputs

| Input | Ref | Use |
|---|---|---|
| BP4 sealed startup | `e699fed59925a3d7b3f02805f85771ae2df32be8` | branch base |
| BP1 source | `b4e07ef515e9464c7bc8177e394ac29f4a4af72a` | two-actor ledgers, C9 bridge |
| BP1 documentation | `be9f3a9e1bb4c61a8c3ec89a9a5d18b4a10762a2` | return/custody |
| BP3 source | `7faaa0722336231335d974bebc70c1282c79ce3e` | keyed C8 writer/ingress |
| C9R source | `6fa2939972ce5a2c0cc4f2b033946b276f1c2934` | TEST_ONLY C9 target/E2 |
| C9RI acceptance | `5753d9b4f8fad9f2175b1e285733f95bb8387888` | scoped independent acceptance |
| PA0 atlas | `3b39c86b376efff8c11833b8451c1791adddb9bc` | V2/M6 and V3 existence map |
| BP2 commission | `19503a3ea09bdf840a5ce98a9697650c387787fa` | future joined producer |

## Source grades (preserved, never promoted)

- BP1: `SOURCEFREE_FIXTURE_ACTOR_NOT_NATIVE`, `native_grant=NOT_GRANTED`.
- BP3: `TEST_ONLY_EXTERNAL_KEY_AND_ANCHOR_NOT_NATIVE`.
- C9R: `TEST_ONLY_SOURCEFREE_TECHNICAL`, native rule/E2 held.
- M6: current adopted actor-safe expression code, but no generated person record exists.
- World/C12/product: `TEST_ONLY_SOURCEFREE_*`, `native=False`.

## BP2 join (future, not fabricated)

BP2 must emit `BP2_JOINED_EVENT_HISTORY_TARGET_E2_ENVELOPE@1` with two distinct
actors, objective event refs, actor history hashes, C8 occurrence refs, C9 target
refs, E2 receipt refs, world refs, effective clocks, authority grades and native
grants. `bp2_compat.validate_envelope` enforces the shape; a self-granted native
flag is refused. Until then, `from_c10` is a typed adapter, not a BP2 emission.
