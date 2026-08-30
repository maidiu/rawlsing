# RABOCHII 5 — PRE-MAIN WAVE 1 PRE553 / SUBSTRATE / RUNTIME LINEAGE R1

Status: `FORENSIC_RETURN_COMPLETE__NO_INTEGRATION_PERFORMED`

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-premain-w1-substrate-runtime-r1`

Exact starting HEAD: `0777a34e50221bde6801dbaca26c058a7350c9e8`

Write jurisdiction: `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WAVE1/W05_SUBSTRATE_RUNTIME/`

Sibling discipline: `WAVE1 sibling outputs were not inspected or consumed.`

## 1. EXECUTIVE DISPOSITION

The empirical substrate/runtime lineage after `main@0777a34e50221bde6801dbaca26c058a7350c9e8` is **not represented by one complete descendant tree**.

There is a strong integrated authority/control lineage:

`main@0777a34`
→ repaired V550-V552J lineage
→ frozen PRE553 whole-machine runtime `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
→ PRE553 substrate reconstruction control `04a0109aa170c6041b199e5c6130a39a8e0f6029`.

That control head is the strongest verified integrated substrate/runtime authority anchor. It is 444 commits ahead of the commanded `main` base with no reverse divergence and contains the frozen PRE553 machine, source/database disposition law, selected `PARQUET_DUCKDB_DIRECT` baseline, accepted SR06 decoder/carrier/direct-DuckDB implementation, and accepted C05R2A source-backed C11 facade.

But it is **not a complete accepted-implementation superset**.

Two material accepted physical implementation lineages are stranded off the control tree:

1. **SR06 R4 functional-dependency compaction** — accepted at `20cfc676bdcebbf9aa5ef129bb7b94451f3af175`, but `rawlsing_next/pre553_r4_compaction.py` is absent from `04a0109`; the R4 branch and the control branch diverge.
2. **R5 Compact-V2 Serial Turbo V4 + Audit69** — selected/validated implementation at `55d4bae445b5eb837aec6f3c67083e131d8e3b0c` + `d6206cd0e351100b64cdf3ace997733153c18eb7`, but the selected R5 line and control diverge from the R5 authorization point. Comparing `d6206cd` against `04a0109` exposes 22 R5-side commits absent from control.

Therefore **pre-main cannot be reconstructed losslessly by rebasing or merging only the reconstruction-control head**. It needs the control head as the authority anchor **plus explicit adjudication/carry-forward of the accepted R4 and selected R5 physical deltas**.

## 2. CURRENT AUTHORITY STACK

The current authority stack is layered. Newer physical code does not automatically own higher semantic authority.

### A. Structural question authority

`main@0777a34` remains a valid R1 question-relation authority migration. Its QSM R1 structural authority is not revoked by later PRE553 work.

The later conflict is narrower and material: the **PostgreSQL empirical-runtime role** carried by that era is no longer authoritative as canonical empirical truth.

### B. Frozen semantic empirical runtime

The frozen PRE553 whole-machine implementation is pinned at:

`9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`.

It adds the C11 repository/integrity/ingest surfaces, empirical objects and authority, exact query/discovery/replay/source-equivalence machinery, structural admission, batch runner, and downstream V554-V558/V3/V2 runtime seams. It is an ancestor of the reconstruction control.

This is the semantic/runtime substrate that later physical storage work is obligated to preserve.

### C. Database and physical carrier authority

The substrate reconstruction law explicitly demotes legacy PostgreSQL to historical/compatibility evidence. The legacy facet-ready view is a historical V550 ingress/convenience surface, **not** source-equivalence or canonical C11 truth.

The selected primary empirical carrier/runtime is:

`PARQUET_DUCKDB_DIRECT`

with immutable/content-addressed Parquet as persistent empirical carrier and embedded DuckDB direct sessions as the analytical/query execution mechanism.

No persistent `.duckdb` database, PostgreSQL database, SQLite database, or `DATABASE_URL` is granted canonical empirical-truth authority.

### D. Accepted SR06 baseline

The accepted SR06 implementation lineage runs through:

- `c5e2c5c820c9b3917a4814bd7031074090763cb6`
- `250f43bfdf1432d60ea5c53b95a22a67a0160ae3`
- `fc74879bdc3a1d987e3f19022116ac551da582e6`
- `606813b01021eb2555017e028d5742b1e6f12e94`
- integrated into control at `def253c7f62b74d07c7297e6ca279642b7d13904`.

It implements exact-SHA source decoding, source-physical incidence, C11 bridging, relational Parquet persistence, typed queryable relations, direct in-memory DuckDB, and semantic-root/replay closure. This baseline is physically present in the reconstruction control.

### E. Accepted R4 scalable representation — stranded

Authority 49 accepts R4 as the scalable physical execution representation for frozen C11 semantics.

Accepted implementation head:

`agent/vozhd-trii-sr06-relational-scale-correction@20cfc676bdcebbf9aa5ef129bb7b94451f3af175`.

The accepted R4 code is **not** in the reconstruction control. The control records the adjudication but does not carry the implementation tree.

R5 does not silently retire R4. R4 remains accepted reference/fallback terrain unless a later explicit authority says otherwise.

### F. R5 physical candidate lineage — accepted/selected but non-serving

The R5 lineage must be read by authority state, not by branch recency.

- Original bounded LONG_SHARDED shadow: final accepted implementation `36bf351dda12f0aa93c9ff426ae54d80143d0bf9`; receipt closure `46a9d35d0edecc7dc9182038baeb0d0748c50fdc`. G0-G8 acceptance does **not** grant serving adoption and does **not** retire R4.
- Compact-V2 serial correctness oracle: `11877f5a043418100773b8a476ee425ec63305cd`.
- Parallel-12: `7049660a574456b4a4333c97a277f6b3d8a2c1b3`; exact-equivalent but explicitly `DO_NOT_SELECT`.
- Serial Turbo V4: `55d4bae445b5eb837aec6f3c67083e131d8e3b0c`; 77/77 closure, exact carrier equivalence, materially faster build; selected for full-source HQ court.
- Single-pass Audit69: `d6206cd0e351100b64cdf3ace997733153c18eb7`; 96-pass R5 suite, 19-pass hostile court, exact equality, selected for full-WVS7 certification.
- Authority67/68 overlap paths are correctness evidence only and explicitly not selected.

The current selected R5 physical stack is therefore **V4 + Audit69**, but its authority remains `inactive / non-serving physical implementation`. Physical acceptance does not make R5 the semantic owner of C11 and does not constitute full-source certification.

### G. Authority70 block and C05R2A closure

The full-WVS7 Authority70 court at:

`agent/vozhd-trii-r5-v4-single-pass-full-wvs70@daeaaf1d6ba0364aab7fda4643aae1da52ec54d2`

stopped at preflight with `BLOCKED_POTENTIAL_FROZEN_CONTRACT_CONTRADICTION`. No full source build, serving selector change, or certified R5 publication followed from that court.

The generic implementation-contract gap was subsequently closed by the accepted carrier-neutral source-backed C11 facade:

`agent/vozhd-chetiri-c05r2a-source-backed-c11-facade@0336eb60fce9fbc17a36cadcd36a5720eabd706b`.

Its lawful path is:

`exact physical/native source truth`
→ `explicit governed semantic/replay projection`
→ `validated C11 source release`
→ `C11LogicalRelease`
→ `C11Repository`
→ `frozen I03`.

That facade is an ancestor of `04a0109` and is physically integrated in the reconstruction control. It closes the **generic bridge implementation gap**, not WVS7-specific source certification, and it does not grant R5 semantic or serving authority.

## 3. MAIN CONFLICT THAT PRE-MAIN MUST RESOLVE

The commanded base `main@0777a34` visibly represents a V550-era PostgreSQL facet-ready empirical runtime.

Later accepted substrate authority says:

- raw source bytes remain external source authority;
- canonical empirical truth must preserve source-native distinctions and validated C11 semantics;
- primary persistence is immutable/content-addressed Parquet;
- DuckDB is embedded/direct execution, not a persistent authority database;
- PostgreSQL is historical/compatibility evidence unless a named equivalence scope proves otherwise;
- absence from the legacy DB is not evidence that a source state did not exist.

Therefore pre-main must preserve the valid R1 question-relation authority from `0777a34` **while refusing the obsolete implication that the legacy PostgreSQL runtime is canonical empirical truth**.

This is a role rebinding problem, not a blanket deletion problem.

## 4. STRANDING MAP

### Stranded from `main` but contained in the control lineage

- repaired V550-V552J implementation;
- frozen PRE553 semantic/runtime implementation;
- SR04 carrier selection and database provenance law;
- SR06 baseline decoder/Parquet/DuckDB implementation;
- C05R2A source-backed C11 facade;
- later substrate/source authority documentation.

These are recoverable by representing `04a0109` as the integrated control anchor.

### Stranded even from the reconstruction control

- accepted R4 implementation `20cfc676…`;
- selected R5 V4 build implementation `55d4bae…`;
- selected R5 Audit69 implementation `d6206cd…`.

These require explicit pre-main reconciliation against the control anchor. Authority documents on control are insufficient because the actual accepted code is on divergent implementation lines.

## 5. SUPERSESSION / DO-NOT-IMPORT RULES

Do not equate `newer branch` with `current authority`.

Explicitly noncurrent physical choices include:

- persistent DuckDB/Postgres/SQLite as primary C11 carrier: not selected;
- SR06 R3 physical representation: superseded for scale representation by accepted R4;
- R5 LONG_SHARDED V1 layout: superseded physically by Compact-V2;
- R5 Parallel-12: correct but rejected for selection;
- Authority67/68 trailing-audit overlap implementations: correct but not selected;
- Authority70 blocked full-WVS7 court: blocker evidence, not a serving or certified runtime head.

The current R5 implementation selection is V4 + Audit69, but it remains non-serving.

## 6. PRE-MAIN REQUIRED REPRESENTATION

A lossless pre-main substrate/runtime reconstruction should represent, at minimum:

1. **Primary integrated authority/runtime anchor**
   - `agent/vozhd-trii-pre553-substrate-reconstruction-control`
   - `04a0109aa170c6041b199e5c6130a39a8e0f6029`

2. **Accepted R4 stranded implementation**
   - `agent/vozhd-trii-sr06-relational-scale-correction`
   - accepted range ending `20cfc676bdcebbf9aa5ef129bb7b94451f3af175`

3. **Selected R5 physical build stack, preserved as inactive/non-serving**
   - bounded accepted R5 root `36bf351dda12f0aa93c9ff426ae54d80143d0bf9`
   - Compact-V2 serial reference `11877f5a043418100773b8a476ee425ec63305cd`
   - Serial Turbo V4 `55d4bae445b5eb837aec6f3c67083e131d8e3b0c`

4. **Selected R5 audit stack, preserved as inactive/non-serving**
   - Audit69 `d6206cd0e351100b64cdf3ace997733153c18eb7`

5. **Authority70 blocker provenance**
   - `daeaaf1d6ba0364aab7fda4643aae1da52ec54d2`
   - evidence only; not runtime adoption.

6. **C05R2A generic source-backed C11 bridge**
   - `0336eb60fce9fbc17a36cadcd36a5720eabd706b`
   - already inherited by the control anchor; must remain semantically binding.

7. **Role correction for legacy PostgreSQL**
   - preserve historical/compatibility evidence and R1 QSM authority;
   - do not preserve PostgreSQL as canonical empirical-truth owner.

This report does **not** prescribe a merge order or perform any integration. It identifies the authority-bearing heads/ranges and the places where a future pre-main integration court must adjudicate tree combination.

## 7. FORENSIC PROOFS USED

- `0777a34 -> 9188dc9`: strict ahead relation; frozen PRE553 runtime is downstream of main.
- `9188dc9 -> 04a0109`: strict ahead relation; reconstruction control contains frozen PRE553 runtime.
- `0777a34 -> 04a0109`: control is 444 commits ahead with no reverse divergence.
- `946705d -> 9188dc9`: V550-V552J G5 integration is an ancestor of frozen PRE553.
- `0336eb60 -> 04a0109`: accepted C05R2A facade is an ancestor of control.
- `20cfc676 <-> 04a0109`: divergent; accepted R4 implementation is not carried by control.
- `d6206cd <-> 04a0109`: divergent from R5 authorization point; 22 R5-side commits are absent from control.
- Direct tree check: `rawlsing_next/pre553_r4_compaction.py` is absent from `04a0109`.
- Direct control-tree check: baseline `pre553_parquet_carrier.py`, direct DuckDB/source bridge/facade surfaces are present.

## 8. LIMITS

This worker is forensic and did not execute runtime tests, mutate existing branches, merge, rebase, cherry-pick, delete, or force-push.

No WAVE1 sibling return was inspected or consumed.

The strongest-downstream-container claims are limited to containers actually verified by branch ancestry/tree evidence in this court. A branch being chronologically newer was never treated as acceptance evidence.

## 9. OUTPUT INDEX

- `SUBSTRATE_RUNTIME_LINEAGE.tsv` — material lineage map.
- `CURRENT_IMPLEMENTATION_AUTHORITY.tsv` — current accepted authority by subsystem.
- `STRANDED_IMPLEMENTATION.tsv` — implementation absent from main and/or the authority control tree.
- `SUPERSEDED_IMPLEMENTATION.tsv` — rejected, nonselected, or superseded implementation states.
- `PREMAIN_REQUIRED_DELTAS.tsv` — exact heads/ranges and role corrections pre-main must represent.

Return disposition:

`PREMAIN_SUBSTRATE_RUNTIME_LINEAGE_RECONSTRUCTED__CONTROL_HEAD_INCOMPLETE_WITHOUT_STRANDED_R4_R5_DELTAS`
