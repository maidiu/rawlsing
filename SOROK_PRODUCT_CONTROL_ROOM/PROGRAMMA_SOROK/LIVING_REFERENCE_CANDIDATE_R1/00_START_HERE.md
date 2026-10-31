# SOROK PROGRAMMA — living reference candidate R2

**Status:** `WORKING_CANDIDATE_NOT_HQ_ADJUDICATED` — persistent sourcefree
Sorok-only operating map. It is not native person acceptance, science issuance,
owner adoption or a priority decree. Scope hold: this is a bounded R3-derived
substrate repair and O-SCIENCE candidate ingest, not a successor whole Sorok
Programma; full Programma must be source-grounded against the complete estate.

## Current cut

| Item | Exact value |
|---|---|
| Start | `67f667421fc90b22aad95cfc253a16feabc92348` |
| Seed build PRE-MAIN | `f40c26301d7d5b811c1bb92efa4934ad564ce5b3` |
| Observed PRE-MAIN | actual `origin/integration/pre-main-reconciliation-r1` read |
| R3 source/index | `e50d32eb6816578145d17dcd637a0b90b3a1ef40` |
| R3 review current | `06f40a3eabb4acfc57f433144224695c2427c25f` |
| R3 old negative (not acceptance) | `3f3d9ec2fddc36bd4047bc6c730382c65a5e692a` |
| O-SCIENCE return | `45efe65f73475e6a815e5fe93c3ee5179de27f67` |
| Program Map | `865b5b01e1a27e99020cf2bb389af8cd4c874b57:2a0a3a42d66f566f92d5c333fbbea4a5adb383b2` |

`refresh` reads the actual local Git refs when available and records the exact
read timestamp. A branch is not a running process; SEALED is never assumed live.

## Persisted reference

| Count | Value |
|---|---:|
| Nodes | 212 |
| Edges | 649 |
| Source rows | 144 Sorok + 3 references |
| Workstreams S0–S16 | 17 |
| Inherited C/A/M/N/O/E records | 102 / 102 source-grounded from R3 |
| Missing C12→A5 functions | 14 |
| O-SCIENCE candidate edges | 226 |
| Dynamic gaps | 38 |
| Derived work-now candidates | 38 |
| External boundary | 1 Pyat contract node only |

The baseline R1 graph is 198 nodes / 423 edges. The O-SCIENCE import is a
candidate-evidence merge into the same graph, not a second tracker.

## What runs

```sh
python3 living_reference.py refresh
python3 living_reference.py ingest-oscience
python3 living_reference.py overview
python3 living_reference.py zoom S5 --depth 2
python3 living_reference.py gaps --domain S15
python3 living_reference.py blocked-chain A5
python3 living_reference.py work-now
python3 living_reference.py coverage
python3 living_reference.py source S5
python3 living_reference.py consumer A5
python3 living_reference.py alternatives S5
python3 living_reference.py workers
python3 living_reference.py history H0001
python3 living_reference.py export
python3 living_reference.py intake-return FILE.json
python3 living_reference.py apply-authorized-transition FILE.json
python3 verify_source_manifest.py
python3 r2_live_transaction.py
```

`refresh` merges seeds and source-cut observations into the existing persisted
state. It never resets history, axes, imported evidence, discovered gaps or
candidate transitions. Duplicate O-SCIENCE imports are idempotent; changed input
cuts are recorded as visible deltas and staleness gaps, never auto-GREEN.

`blocked-chain` is a typed required-blocker/impact view. `critical-path` remains
only a legacy DAG illustration and says so.

## Authority limits

- O-SCIENCE evidence is `UNREVIEWED_CANDIDATE_EVIDENCE`; its 226 links are
  hypotheses, not issued original propositions. Original S questions/output are
  preserved exactly from the Program Map.
- The 102 inherited records have exact R3 source identity, but source exactness
  is not scientific issuance.
- No CAN008/CAN011/ADP/SCI05, native Pyat world/N11/N12/C11, native C4/C11/C12,
  human A5, production import, PRE-MAIN merge or owner adoption is issued.
- Owner grants remain `OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION`. Human
  participant evidence is simulated/candidate locally, never `PROVEN`.
- R6/R7 and the four sourcefree assets remain returned/unadopted. The external
  Pyat boundary is not locally mutable.
