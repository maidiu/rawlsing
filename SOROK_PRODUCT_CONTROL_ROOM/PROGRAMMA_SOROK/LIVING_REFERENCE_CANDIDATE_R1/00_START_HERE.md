# SOROK PROGRAMMA — living reference candidate R1

**Status:** `WORKING_CANDIDATE_NOT_HQ_ADJUDICATED` — sourcefree Sorok-only
operating map, not native person acceptance, science issuance or priority decree.

## Current cut

| Item | Exact value |
|---|---|
| Build/startup PRE-MAIN | `f40c26301d7d5b811c1bb92efa4934ad564ce5b3` |
| Refreshed PRE-MAIN | `8e44ca9c751049d65e6def47600b5c073ee04b29` |
| R3 source/index | `e50d32eb6816578145d17dcd637a0b90b3a1ef40` |
| R3 independent review | `3f3d9ec2fddc36bd4047bc6c730382c65a5e692a` |
| R6 source close | `28e38ebbf08bbfaeb152ae022046e1303d9a2e40` |
| R7 source closure | `7f25fb9bfc48679a47ccc61b36354f20fef54f1c` |
| Program Map | `865b5b01e1a27e99020cf2bb389af8cd4c874b57:2a0a3a42d66f566f92d5c333fbbea4a5adb383b2` |
| HQ product synthesis | `36ddfd8b787543751d4b350a315af31924d95d6e:1ba39a965d30e63c5b6183e4af1aa84d95b4021b` |

The build PRE-MAIN is preserved separately from the refreshed current head. The
R3 source manifest is reused; it is not re-adopted by this map.

## What runs

```sh
python3 living_reference.py refresh
python3 living_reference.py overview
python3 living_reference.py zoom S5 --depth 2
python3 living_reference.py gaps --domain S15
python3 living_reference.py critical-path L0_PERSON
python3 living_reference.py source S5
python3 living_reference.py consumer A5
python3 living_reference.py alternatives S5
python3 living_reference.py work-now
python3 living_reference.py workers
python3 living_reference.py history H0001
python3 living_reference.py export > /tmp/sorok-living-export.json
python3 living_reference.py intake-return FILE.json
python3 living_reference.py apply-authorized-transition FILE.json
python3 verify_source_manifest.py
```

`refresh` deterministically regenerates `state.json` and `SNAPSHOT.json` from
the frozen seeds. All query/update commands read the same state. `intake-return`
records a candidate return and any newly discovered requirement; it does not
promote. `apply-authorized-transition` requires owner and reviewer evidence,
changes only the selected candidate axis, appends immutable history, invalidates
downstream consumer claims, and never traverses the external Pyat boundary.

## Actual map

- 198 nodes, 423 edges.
- 144 Sorok source rows, 3 reference sources; no Pyat program rows are ingested.
- 22 coverage sectors: S0–S16, C/A19, M40, N12, O16, E15, material/independent
  B, relational constitution, needs/activity, practice/no-change, context,
  childhood/roles, user praxis, trust/injury/opacity, canon/history/clock,
  V2/UX, accessibility, safety/privacy, economics/retention, social
  possibilities, alpha/evaluation and recovery assets.
- 12 explicit gaps, including S5, S7, S11, S13, S14, S15, native C4/C11/C12,
  C9/C12 anchor, B-F1CR original bytes, native CAN/ADP, Pyat boundary and A5.
- 46 owner/source/science/HQ slots from R3, including six product-workstream
  owners.
- One external `PYAT_EXTERNAL_BOUNDARY` contract node only. No Pyat source,
  analysis, task ledger or program health is ingested.

## Authority limits

This is a sourcefree map/orchestration apparatus. No native C4/C9/C11/C12
person, native B, CAN008/CAN011/ADP/SCI05 rule, Pyat N11/N12/C11 grant, human
A5, production import, PRE-MAIN merge or priority decision is issued. The four
returned engineering assets remain author-tested, unadopted candidates. The
index and validator do not replace Sorok HQ's scientific/product judgment or
the original owners' authority.
