# 02 — Actual receiving state, collisions, and finite actions

## Protected/PR state table

| Candidate | Exact head/merge | Actual state | Qualification |
|---|---|---|---|
| #696 B00 graph | head `915b17ab7`; merge `a02cd4e164`; C8 expected-set review `01948f71e81c3d9e04075b533429d7b0bb609594` | **MERGED** protected 2026-11-06 05:17 | Merge receipt: exact C8 independently accepted at `915b17ab`; 62/82/49 and 51/82 preserved. C8 artifact at `01948f` is REVISE of prior `8333e6`; corrected graph matches expected sets 23/23 transitive and 13/13 conditional |
| #702 L01 | head `0252e028e`; merge `aaf098b87` | **MERGED** protected | R01 S2 acceptance at `0252e02`; 171 tests + hermetic cold replay per receipt; sourcefree; FIABC 144/3 retained |
| #703 L02 | head `31c59b6d1`; merge ref `9061399593` | **PR OPEN**; L02 code/test blobs already received at `d119045f` via `1cbf3c63e`; control docs not received | Code lane E; physical fan-in C; no overlap. Do not re-receive code; reconcile docs |
| L03 P2 | `409be32f7`; review `e2f6c164` | **RECEIVED** at `d119045f` | Sourcefree scoped P2 |
| L03 capacity guard | `9a5cfd2ab`; review `0d3191b3` | **RECEIVED** at `d119045f` | Focused guard acceptance preserved |
| L03 compressed body | `02c1200b8`; review `9999c0afa`; final return `8af04c817` | **ACCEPTED SCOPE, NOT IN `d119045f`** | Current base execution view is pre-compression `de5613301`; current-base fan-in C pending, not reviewed here |
| #705 dossier | head `62329a720`; merge ref `041b6ea834` | **OPEN / UNMERGED candidate** | Content integrity PASS_SCOPED; currentness REVISE; no protected adoption from #696 base |
| #691 GF1 | TEST_ONLY optional | not universal prerequisite | Preserve optional scope |
| FIABC/R09 | historical 144 PASS / 3 FAIL | retained | No all-green conversion |

## Qualified owner / CI

- Protected CAS owner/integrator: existing Pyat HQ/B00 receiving owner (GitHub
  protected merge actor `Maidiu` / `GitHub` per local receipts). G is not owner,
  merger, or reviewer of its own return.
- Live CI: **NOT_REFRESHED_LIVE** in this lane; no `gh`/browser access. Local
  merge/commit receipts:
  - #696 C8 exact-head receipt in `a02cd4` message;
  - #702 R01 S2/test receipt in `aaf098` message;
  - L03 P2/guard CI receipt in `d119045f` message, with FIABC 144/3 retained.
- Do not label full CI green from these local receipts.

## #703 collision table

| Path family | Collision | Handling |
|---|---|---|
| `rawlsing_next/pre553_analytical_composition.py` + L02 test/proof | Code already identical at `d119045f` | Leave received code; do not re-merge #703 code |
| `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/COMPONENT_STATUS.jsonl`, `CURRENT_SEAM_STATES.jsonl` | #703 branch and #705 overlays both touch control docs; current d119 has later L01 receipt | One reconciler selects current rows; preserve 62/82 IDs/status/predicates |
| `README.md`, `REMAINING_REAL_PYAT_WORK.md`, `NEXT_R_GAP49_NEXT_DECISIONS.md`, S02–S11 | #703 branch docs overlap #705 overlays and current protected agenda | Reconcile by currentness, not wholesale merge |
| #705 dossier `PRE553_UNIVERSAL35_RECOVERY.../00–04` | Candidate only, based on pre-merge `915b17` | Fresh branch from `d119045f`; add currentness/source-custody overlays |

## Finite remaining receiving actions

1. Fresh branch from protected `d119045f` by designated HQ writer.
2. Apply selected #705 dossier `00–04` and overlays, with corrections in
   `01_STALENESS_CORRECTIONS.md`.
3. Add source-custody currentness overlay: 35/35 present/hash-matched under
   `USER_ORIGINAL35_DATA_ROOT`; byte custody only.
4. Reconcile #703 control docs only; leave L02 code received.
5. Run static exact-head checks: 35 manifest rows, 25 W/P, 62/82/49, 51/82/88/13,
   C8 expected sets, FIABC 144/3.
6. Distinct nonauthor exact-head review; record C8 receipt/expected-set evidence.
7. Qualified protected CAS merge/readback + paired `CURRENT_PROGRESS.md/.json`.
8. Keep A/B/C/E code lanes unblocked; D may receive read-only source root when
   ABI ready.

## Non-blockade statement

The #705 documentary corrections are **not** a prerequisite for A/B/C/E code
work. Do not use this receiving review as a generic administrative blockade.
#703 code consumer remains E; physical fan-in remains C.
