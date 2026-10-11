# HQ280 PV3 A01 — All-35 original administered-item inventory anti-join and identity succession

**Commission:** PYAT-HQ280-PV3-A01-SOURCE35-ORIGINAL-ITEM-CROSSWALK-R1
**Branch:** `agent/rabochii-pyat-hq280-pv3-a01-source35-original-item-crosswalk-r1`
**Terminal:** `HQ280_PV3_A01_ALL35_ORIGINAL_ITEM_IDENTITY_CONSERVED_OR_EXACT_INSTRUMENT_HOLDS__GITHUB_PUSHED`
**Result: PASS — original-item identity CONSERVED; exact-instrument witness holds; GitHub pushed.**

## Authority, scope and limits

Governed by `HQD-2026-10-10-280` under parallel seal `908ee4e7…`, canonical baseline
`a70a069fa948e0f3c041b389edcc732c6b948a4f` (`integration/pre-main-reconciliation-r1`),
semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390`.

This return is **development/documentary only**. It grants no original source-read,
no semantic/model/use adoption, no G0b/EE12/operative-publication permission.
No raw SAV/DTA executed, no respondent microdata re-read, no respondent lineage exported,
no canonical or semantic PRE-MAIN mutation, no self-adoption. Only return-scoped scripts
and results were created, in an isolated worker worktree. All 35 original wave identities
and typed scientific holds are kept visible.

## Primary evidence verified

- LR-A archive `RAWLSING_HQ280_LR_A_SOURCE_SCIENCE_FORENSIC_RETURN_R1.zip`
  sha256 `e201e7923e1d34520dec7134a51e338b5204d55e39c3caa6a51b65888663600b` — **verified exact**.
- Crosswalk `02_ORIGINAL_ITEM_IDENTITY_CARRIER_CROSSWALK.json`, 423,620,953 bytes,
  schema `RAWLSING_HQ280_LR_A_CROSSWALK@1.0.0` — **streamed (ijson), never fully loaded**.
- LR-A independent summaries (`evidence/scientific_summary.json`, `mechanical_summary.json`)
  used only as independent witnesses for validation, not copied as findings.

## Method

Streaming/chunked deterministic derivation over the 423 MB crosswalk (memory-bounded via
`ijson`), stable sort keys, no wall-clock in derived content, input hash + schema recorded in
every report. Large data-only per-implementation output kept outside Git and hash-pinned;
manifest plus small per-wave counts and gap samples committed.

## What was built (all 35 waves / 9 families, 18,276 implementations)

- **`01_ALL35_SOURCE_AND_ORIGINAL_ITEM_SUMMARY.json`** — full source + original-item summary,
  per-wave counts, typed measure-role classes, grain/adoption tallies, duplicate detection.
- **`02_INSTRUMENT_PHYSICAL_IMPLEMENTATION_ANTIJOINS.json`** — full two-sided anti-join:
  implementation→absent carriers, carrier→asserted-vs-population coverage, and the retained
  non-P2/excluded complement (7,882 rows: 4,316 `EXACT_SCIENTIFIC_OR_PERMISSION_HOLD`,
  3,566 `IDENTITY_OR_PRECEDENCE_CONFLICT`) that must not be silently dropped.
- **`03_NATIVE_TOPOLOGY_IDENTITY_GAPS.md`** — native gaps (G1–G6).
- **`04_EXACT_SOURCE_COMPETENCE_EDGES.json`** — 544 documentary source→carrier competence edges.
- **`05_HOSTILE_COUNT_AND_IDENTITY_TESTS.json`** — the three A01 hostile cases, executed.
- **`06_MANIFEST.json`** — input/report/repro hashes + external large-dataset pointer.
- **`repro/`** — derivation scripts and exact test log; large per-implementation JSONL external.

## Findings (identity conserved; no original item silently dropped)

1. **Population conserved exactly.** 18,276 implementations streamed. Typed measure roles, never
   zero-filled: `MEASUREMENT_CANDIDATE` 13,270, `CONTEXT_NONMEASURE` 4,272,
   `ADMINISTRATIVE_NONMEASURE` 490, `DERIVED_NONMEASURE_OR_CONTEXT` 29,
   `NONMEASURE_OR_ADMIN_HINT` 15. Zero duplicate implementation IDs and zero duplicate
   `exact_identity_sha256` — identity is unique per implementation.
2. **Independent witnesses reproduced.** All 7 checks PASS: total 18,276; deep response
   bindings 16,308 bound + 1,968 blocked (= 18,276); catalog-only 26; register-only 9;
   case-collision groups 7; non-P2/excluded rows retained 7,882; register-only items retained
   as typed complement (not dropped). Gaps are preserved as holds, **not** treated as missing
   categorical labels.
3. **Inner-join omission is structurally available (hostile T1).** Only 4 of 46 carriers cover
   100% of the population (`QSM_PROVENANCE`, `QSM_RAW`, `R10K_IMPLEMENTATION_SOURCE_CONTEXT_R1.csv`,
   `R10K_O06_IMPLEMENTATION_ROUTING_CENTRAL.jsonl`); the other 42 are partial, so any single-carrier
   inner join silently drops administered items. Only a union-of-carriers outer join is omission-safe.
4. **Battery-parent/child present (hostile T2).** 129 implementations carry parent/child/battery
   driver bindings retained as a distinct identity class.
5. **Alias collision confirmed (hostile T3).** 7 case-variant namespace collisions, e.g. LiTS III
   `DURATION1`/`Duration1` — the same `question_id` maps to two distinct implementation IDs. Real
   ambiguity for source owners, retained, not resolved here.
6. **Alternative conflicts are mass-present.** 10,457 of 18,276 (57.2%) carry ≥1 carrier conflict,
   retained verbatim for owner adjudication.
7. **Governed grain is "historical implementation," not "original measured item."** The crosswalk
   itself marks every row `HISTORICAL_IMPLEMENTATION__NOT_AUTOMATICALLY_ORIGINAL_MEASURED_ITEM`;
   no original-item count is inferred from `implementation_count`. Where an exact instrument witness
   exists it is honoured; where it does not, the count is labeled UNKNOWN, never zero.

## Acceptance

`02`/`04`/`05` + `repro/` are exact, re-runnable (`repro/TEST_LOG.txt`), and every witness check
PASSes. Identity is conserved across all 35 waves. Canonical and semantic PRE-MAIN untouched.
Large/sensitive dataset (`external/crosswalk_per_implementation.jsonl`, 18,276 records,
sha256 `4bcfe8e8…bfa1476c`) is external and hash-pinned in `06_MANIFEST.json`, not committed.

**HOLD (by design, for owner scope):** semantic adjudication of the 10,457 carrier conflicts, the
129 battery-parent/child identities, and the 7 alias collisions — these are source-identity-owner
(A01/A02) decisions, not documentary findings, and are left visible rather than silently resolved.