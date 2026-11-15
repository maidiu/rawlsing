# Correction map — independent G5 handoff defects

**Review:** `c5a71fcc59a45aa470720159a334ae57f365de11` (`WORKER_REVIEWS/PYAT_COUNTRY_REUSE_G5_20261115/00_REVIEW.md`)
**Measurement:** `ACCEPT_SCOPED@SOURCEFREE_REUSE_COURT_REPRODUCED`
**Handoff:** `REVISE_EXACT_DEFECT@G4_OPTIONS_AND_HANDOFF_CLAIMS`
**Frozen raw measurement:** author commit `f7a7652258907129988504e53fae286da1dbf45d`; `evidence/`, `logs/`, `probe/` unchanged by this correction.
**Correction base:** `6cb7866d6ccfcade7a7aaa92cbbd6398a5a672bb`; this correction is narrative + manifest only.

The frozen raw evidence remains authoritative for the measured facts/counters. Where the old narrative conflicts with the independent review, the corrected text below is the current canonical interpretation; historical quotations in the review remain historical.

## Material defects

| ID | Reviewer finding | Exact old cell(s) | Corrected cell(s) | Status |
|---|---|---|---|---|
| C1 | **B was labeled a measured candidate/implementation**, but no B code, patch or A/B run exists. | `G4_OPTIONS.md` title §B “(the only measured candidate…)”; §B “**Why B**… only option”; Recommendation item 3 “B is the smallest measured candidate”; `00_RETURN.md` G4 row “B … is the only measured candidate”; `PROGRAMMA_DELTA.md` open obligation 2 “B (bounded prepared-session/iterator repair)”; `SELF_CRITIQUE.md` had no B-hypothesis hold. | `G4_OPTIONS.md` §B title/status “source-grounded hypothesis, NOT measured”; §B “hypothesis only / no B implementation/run”; Recommendation item 3 “B is a hypothesis… authorize bounded measurement”; `00_RETURN.md` G4 row “source-grounded unmeasured hypothesis”; `PROGRAMMA_DELTA.md` obligation 2 “B is not measured”; `SELF_CRITIQUE.md` item 13; `G3_GROUPED_OR_BARRIER.md` conclusion “B is not measured”. | Corrected |
| C2 | **#999 context stale**: accepted successor exists but was not adopted in `9d96a9c…`. | `G1_SOURCE_CONTRACT.md` §7 “#999 successor still pending”; `00_RETURN.md` §4 “#999 bodytruth G5 is still pending… requires accepted successor”; `PROGRAMMA_DELTA.md` obligation 3 “#999 accepted immutable successor…”; `SELF_CRITIQUE.md` item 12; `G4_OPTIONS.md` Prerequisites. | `G1_SOURCE_CONTRACT.md` §1 table/§7 “accepted `ce770425…` / `c18b7e08…`, created after start, not adopted”; `00_RETURN.md` §4 “accepted successor exists, not adopted; adopt/qualify + exact grant”; `PROGRAMMA_DELTA.md` obligation 3; `SELF_CRITIQUE.md` item 14; `G4_OPTIONS.md` Prerequisites “adopt/qualify, do not wait for new acceptance”. | Corrected |
| C3 | **Unfrozen wall-stability / three-pass claim**: one frozen author pass, independent 65.661 s. | `SELF_CRITIQUE.md` item 5 “three same-command… 1.02×–1.26×… cold wall stable at ~51.9–52.2 s”; `G3_GROUPED_OR_BARRIER.md` §1 “three same-command passes… 1.02×–1.26×”; `00_RETURN.md` header one-pass; `G2_COLD_COST.md` 100-op headline; `PROGRAMMA_DELTA.md` Added. | `SELF_CRITIQUE.md` item 5 “author one pass 51.929; review 65.661; earlier sentence withdrawn; no stable throughput”; `G3` table/§1 “author one pass 1.021×; review 1.199×; identical receipts”; `00_RETURN.md` header/table “author 51.929 / review 65.661; ambient”; `G2` table/§5/§7 “author/review columns; no stable constant”; `PROGRAMMA_DELTA.md` Added “author + review, ambient”. | Corrected |
| C4 | **Source-open mislabeled as tripwire**; it is INAPPLICABLE. | `00_RETURN.md` table “Full `C11Repository` / whole-table / source opens 0/0/0 tripwires”; `SELF_CRITIQUE.md` item 14 (implied zero); `G4_OPTIONS.md` test falsifiers “zero source opens”. | `00_RETURN.md` “C11Repository 0 / read_table 0 real tripwires; source-open INAPPLICABLE”; `G2_COLD_COST.md` table source-open row; `SELF_CRITIQUE.md` item 10; `G4_OPTIONS.md` falsifier “source-open INAPPLICABLE; C11Repository/read_table zero”. | Corrected |
| C5 | **Process-tree RSS mislabeled as sampled high-water / false equality.** | `00_RETURN.md` table “Cold process-tree RSS peak 137.2 MB”; `G2_COLD_COST.md` table “Process-tree RSS peak”; `SELF_CRITIQUE.md` item 8 “peak equals self max RSS”. | `00_RETURN.md` “RSS inference `max(before, after, self ru_maxrss)`; 137.2 MB author (self 136.503 MB; 733,184 B difference); 127.6 MB review”; `G2` table “RSS inference” + self/diff; `SELF_CRITIQUE.md` item 8 corrected. | Corrected |
| C6 | **Proxy counters over-promoted**: row-group/bytes not physical I/O/decompression; `_build` instrumentation-inclusive; object counts not tripwires. | `00_RETURN.md` headline “row-group reads / compressed-uncompressed / `_build` share”; `G2_COLD_COST.md` table/§4; `SELF_CRITIQUE.md` items 6–7/14. | `00_RETURN.md` labels “metadata-call proxy / metadata-sum proxy / instrumentation-inclusive”; `G2` header qualifiers + table; `SELF_CRITIQUE.md` items 6, 7, 9; `G4_OPTIONS.md` B target “metadata-sum proxy”. | Corrected |
| C7 | **Measurement acceptance conflated with production/security/science/new QUERY issuer qualification.** | `00_RETURN.md` header/§4; `G5_REVIEW_PENDING.md` was “PENDING_DISTINCT_REVIEW”; `PROGRAMMA_DELTA.md`; `SELF_CRITIQUE.md` item 10. | `00_RETURN.md` header “measurement ACCEPT_SCOPED; corrected handoff; no production/security/science/new QUERY acceptance”; `G5_REVIEW_PENDING.md` received-review status; `PROGRAMMA_DELTA.md` receiving; `SELF_CRITIQUE.md` item 12. | Corrected |

## Qualifier corrections

| ID | Reviewer qualifier | Corrected treatment |
|---|---|---|
| Q1 | Row-group reads/bytes are metadata-call/sum proxies. | Carried in `00_RETURN.md`, `G2_COLD_COST.md`, `SELF_CRITIQUE.md` item 7. |
| Q2 | `_build` share is instrumentation-inclusive, not a full time decomposition. | Carried in `00_RETURN.md`, `G2_COLD_COST.md` §4, `SELF_CRITIQUE.md` item 6. |
| Q3 | Family/event materialization counts are native work, not negative tripwires. | Carried in `G2_COLD_COST.md` table, `SELF_CRITIQUE.md` item 9. |
| Q4 | Grouped in-memory wall is contended (author 1.021×, review 1.199×). | Carried in `G3_GROUPED_OR_BARRIER.md`, `00_RETURN.md`, `SELF_CRITIQUE.md` item 5. |
| Q5 | 1,000-distinct projection is author 519.29 s / review 656.61 s, both over budget. | Carried in `00_RETURN.md`, `G2_COLD_COST.md`, `G3_GROUPED_OR_BARRIER.md`, `SELF_CRITIQUE.md` item 1. |
| Q6 | 1,000-repeat probe is repeat-only, not distinct. | Retained and labeled in G3/00_RETURN/SELF_CRITIQUE. |
| Q7 | Existing cold guards kept; no chosen layout/new engine/production patch. | Retained in G4, G1, 00_RETURN, G5, PROGRAMMA_DELTA. |

## Frozen evidence / supersession statement

- The raw author measurement, logs, probes and evidence at `f7a765…` are **preserved unchanged**. This correction does not rerun or rewrite them.
- The independent review's exact facts/counters are the accepted measurement basis. Its 65.661 s cold wall and 1.199× grouped observation are recorded alongside the author's 51.929 s / 1.021× pass; neither is a stable performance constant.
- The corrected narrative above **supersedes** the earlier headline/handoff sentences listed in C1–C7. Any historical quotation of those sentences is historical only and must not be used as the current handoff.
- The 100-operation measurement is accepted at `SOURCEFREE_TEST_ONLY`; B remains unmeasured; #999 successor is not adopted in the measured cut; no production/security/science/new QUERY issuer qualification follows.

## Verification performed

- Manifest: `MANIFEST.json` lists 47 payloads; each byte count and SHA-256 was rechecked after this correction. Result: **47/47 exact, 0 bad**.
- Frozen raw payloads: `git diff --name-only f7a7652258907129988504e53fae286da1dbf45d -- .../evidence .../logs .../probe` returned **0 files**. The original measurement/logs/probes/evidence are untouched.
- Production: `git diff --name-only 9d96a9cac7d10f59f2c30d8045dd1696fa3ab969 -- rawlsing_next` returned **0 files**.
- Canonical-current grep: the only occurrence of the withdrawn phrases “only measured candidate” / “three same-command” / “stable at ~51.9–52.2 s” is the explicit withdrawal/negative statement in `SELF_CRITIQUE.md` item 5/13; all other occurrences are historical quotations in this correction map. No stale overclaim remains in the current canonical narrative.
- No benchmark rerun, no new fixture, no new A/B, no production edit, no guard removal.
