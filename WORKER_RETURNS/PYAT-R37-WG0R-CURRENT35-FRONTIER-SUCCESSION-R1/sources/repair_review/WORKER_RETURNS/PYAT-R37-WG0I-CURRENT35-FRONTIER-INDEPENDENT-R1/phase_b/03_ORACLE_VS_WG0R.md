# WG0I — independent oracle vs WG0R comparison

WG0R return commit: `0310d94dfab57f811110027c1c801b725fdba5c1`.
This is an independent comparison of author evidence, not acceptance.

## Bounded author evidence

- Accounting rows: **18276**; unique IDs: **18276**; unique identity hashes: **18276**; waves: **35**; families: **9**.
- Author court: **82 passed / 0 failed / 0 error / 0 skip**; cold court: **82 passed / 0 failed**.
- WG0R itself: full current35 operation execution = **UNVERIFIED__NO_RAW_READS_OR_SOURCE_WARRANT_ISSUED**; pending edge = `EXACT_ACCEPTED_AUTHORITY_TO_OPERATION_CATALOG_BINDING_AND_FULL_FRONTIER_WITNESS`.

## Exact 18,276 vs 18,259 crosswalk

| Quantity | Value |
|---|---:|
| O35E rows | 18259 |
| WG0R accounting rows | 18276 |
| Common non-None identity hashes | 18250 |
| P2-only hashes | 26 |
| O35E None-identity (blocked) rows | 9 |
| O35E duplicate identity hashes (non-None) | 0 |
| Net count delta | +17 |

Arithmetic: 26 P2-only hashes - 9 O35E None-identity rows = 17 net count delta.

- P2-only carrier/admin variables (7): `numero`, `party`, `enc`, `pais`, `region`, `casenumb`, `wt`.
- P2-only measurement candidates (19): `Latinobarómetro 1995 p46f`, `Latinobarómetro 1995 p46e`, `Latinobarómetro 1995 p43a`, `Latinobarómetro 2024 Q8NCVA`, `Latinobarómetro 1995 p47b`, `Latinobarómetro 1995 p46a`, `Latinobarómetro 1995 p46h`, `Latinobarómetro 2024 Q47STC`, `Latinobarómetro 1995 p46c`, `Latinobarómetro 2024 Q8NCVC`, `Latinobarómetro 2024 Q45ST`, `Latinobarómetro 1995 p46b`, `Latinobarómetro 1995 p47c`, `Latinobarómetro 1995 p47a`, `Afrobarometer R1 xstronld`, `Latinobarómetro 1995 p33b`, `Latinobarómetro 1995 p46g`, `Latinobarómetro 1995 p46d`, `Latinobarómetro 2024 Q8NCVB`.

The 17-row net delta is **not** an automatic omission and **not** a WG0R defect: it is the difference between the P2 identity/accounting spine and the O35E eligible-item matrix, with 9 O35E blocked-identity rows carrying no P2 hash and 26 P2-only hashes. The 19 measurement candidates require exact owner crosswalk before the original item inventory can be called complete.

## Carrier RED

- Claimed: 18276 bytes / `64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98`.
- Observed: 18387 bytes / `3bee6f0ec5cae74c112f2896b517b23ab7e880c9400bf019d1df6d0b3157edee`; reserved-bit violations: 2114; state: `DISPOSITION_PAYLOAD_MISMATCH`.
- Fail-closed: **True**; local archive copy SHA-256: `c1d5a9a9b2905f7ed783a21f43eeef91bc173d6e5e077751a67f7025408ee7ad`.

## Independent decision

- Bounded native fixture + 18,276 identity accounting: **ACCEPT at own grain**.
- Retained disposition carrier: **REVISE / RED — exact republication required**.
- 17-row / 19-measurement-candidate crosswalk: **REVISE — owner typing required**.
- Full original35 eligible item/operation execution: **HOLD** (PERMITTED = 0 in the frozen oracle; WG0R also says UNVERIFIED).
