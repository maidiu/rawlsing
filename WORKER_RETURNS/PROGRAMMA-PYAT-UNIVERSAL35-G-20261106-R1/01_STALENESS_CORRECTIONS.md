# 01 — Precise currentness correction patch recommendations for #705

These are recommendations only. G did not edit shared guides/status. Apply them
as additive correction banners or replacement sentences on a fresh branch from
protected `d119045f4169439b4ba02d0870bc328f8beb3aaa`, preserving historical text
and source cuts. Do not rewrite old history into “always current.”

## A. Dossier `PRE553_UNIVERSAL35_RECOVERY_20261106_R1/00_MASTER_RECOVERY_AND_CURRENT_STATE.md`

Replace the status sentences claiming #696 pending, #702/#703 unmerged, L03
unmerged, compression unreviewed with a currentness banner:

> **Current protected update (2026-11-06, post-#705 base):** #696/B00 merged at
> `a02cd4e164eabed978bc577ed68f1c424b0ab187` with an exact C8 acceptance receipt
> for `915b17ab7c7aeddf17e886086c3f4b574da1fcd4`; #702/L01 merged at
> `aaf098b877ccf825e09966ae5e74347f8829c3d3`; #703 PR remains open at
> `31c59b6d1c0d452b34b3e133e4a2b01317d00925`, but its L02 code/test blobs are
> already byte-identical in protected `d119045f` via `1cbf3c63e`; its control-room
> docs remain unreconciled. L03 grouped P2 `409be32f…` and capacity guard
> `9a5cfd2…` are received at `d119045f`; compressed-body `02c1200…` is
> independently accepted by `9999c0af…` but is **not** in `d119045f`; W04 explicit
> caller-configured persistent cache equivalence was owner-accepted; final L03
> return `8af04c817f008ba4be5640bf776d09ed530a6cf2`. #705 remains a candidate
> documentary dossier and inherits no protected adoption from its #696 base.

Add source-custody overlay:

> **Source presence currentness:** all 35 original source files are present and
> hash/size/mtime-matched against R157 under caller-configured
> `USER_ORIGINAL35_DATA_ROOT` (`b90708f7d79624faae3da2408932829e569e5ae2`, 35
> exact matches, 1,319,161,326 bytes). This is byte custody, not respondent
> decode/native fact/source-science issuance. `SOURCE_NOT_PRESENT_HERE` is not the
> current blocker for any of the 35; operation/source/permission qualifications
> remain exact.

## B. Dossier `01_SOURCE_ROSTER_AND_STATUS.md`

Keep the 35-table rows, R157 counts, HELD/fixture grades and exception links
unchanged. Add above the table:

> **Byte-presence vs declared-support distinction:** the original declaration
> grades (HELD/supported/fixture) remain as stated; separately, all 35 physical
> source files are currently present and exact-hash verified under the root alias
> per `b90708f7…`. Do not turn byte presence into original35 native execution,
> source-science issuance, or a change to each original declaration grade.

## C. Dossier `02_FUNCTION_EVIDENCE_AND_PRIORITIES.md`

Update only the currentness cells:

- W01: #702 merged `aaf098b87`; world-source binder received sourcefree.
- W03: compressed-body `02c1200` reviewed/accepted `9999c0afa`; not received in
  `d119045f`; current-base fan-in C pending.
- W04: explicit caller-configured persistent cache accepted by owner as W04
  equivalence; default remains owner policy; no blanket default.
- W05: grouped P2 + capacity guard received at `d119045f`.
- W08: #702 merged `aaf098b87`.
- P03: P2/guard received; compressed accepted but unreceived.
- P08: #702 merged; N9/native remains separate.
- P09/P11/P12: preserve HELD/architecture-pending; no new native grant.

## D. Dossier `04_RECOVERY_AUDIT_AND_ACCEPTANCE.md`

Replace “#702/#703 unmerged; compressed author-only; #696 pending” with the
currentness banner from A. Preserve:
- FIABC **144 PASS / 3 FAIL**; no all-green.
- C8 expected sets: 51 child / 82 seam / 88 direct / 13 IF; prior C8 `REVISE` at
  `01948f71e81c3d9e04075b533429d7b0bb609594` against `8333e6`; corrected
  `915b17` matches 23/23 transitive and 13/13 conditional.
- The exact `915b17` independent C8 review artifact was not found in local refs;
  the protected merge receipt `a02cd4` states exact C8 acceptance. Do not invent a
  separate artifact.
- #703 code already received; #703 docs still open.

## E. Overlay files

Recommended replacement/append banners:

1. `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md`
   - Replace “P2 grouped now exists as independently reviewed branch-only …
     compressed-body candidate remains unreviewed” with:
     “P2 grouped and capacity guard are received at protected `d119045f`;
     compressed bodies are reviewed/accepted `9999c0afa` but not yet received;
     #696/#702 merged; #703 code received, PR/docs open; #705 candidate only.”
   - Keep the OCT28-CAS2 paragraph as historical at its stated cut.

2. `05_ROADMAP/README.md`
   - Replace “L03 reviewed grouped P2 and capacity guard unmerged, compressed-body
     unreviewed; L01/#702 and L02/#703 accepted scoped sourcefree unmerged;
     current #696 exact-head receiving pending” with current merge/receipt state
     from A. Keep 62/82/49 and historical text.

3. `05_ROADMAP/REMAINING_REAL_PYAT_WORK.md`
   - In the P0 table: update P0.2/P0.3/P0.4/P0.5/P0.6 status cells: #702 merged;
     #703 code received/PR open; P2/guard received; compressed accepted but
     unreceived; #696 merged with C8 receipt; source bytes present under root
     alias; W04 owner equivalence.
   - Preserve original A01–A16 and 49 GAP rows; no new IDs.

4. `05_ROADMAP/NEXT_R_GAP49_NEXT_DECISIONS.md`
   - Update GAP-008 annotation: accepted L01/#702 merged; L02/#703 code received
     but PR/docs open; compressed accepted; P2/guard received; #696 merged/C8
     receipt. Keep original GAP-001–049 unchanged.

5. `05_ROADMAP/PREREQUISITES_AND_UNLOCKS.md`
   - Update “L03 P2/guard unmerged, compressed unreviewed” to current state; keep
     all 82 original predicates and 51 child IDs unchanged.

6. `05_ROADMAP/SECTIONS/01_SOURCE_GOVERNANCE.md`
   - Add source-custody overlay from A/B; keep HELD/fixture and R157 grades.

7. `05_ROADMAP/SECTIONS/03_ROUTE_B_C11.md`
   - Update currentness: P2/guard received; compressed accepted but unreceived;
     #702 merged; #703 code received/docs open; W03/W04 default/cold limits remain.

8. `05_ROADMAP/SECTIONS/04_F1_F4_EMPIRICAL.md`
   - Update #703 code received (not “unmerged”); L03 P2/guard received; compressed
     accepted; no native/all35 promotion.

9. `05_ROADMAP/SECTIONS/05_LEARNED_LIFECYCLE.md`,
   `06_FIELD_FORGE_F5.md`, `09_N9_WORLD.md`, `10_N10_POSSIBILITY_F8.md`,
   `11_N11_N12_GATE.md`
   - Update #702 to merged; L02 code to received; keep FF/N9/N10W/N11/N12
     authority and native holds separate.

## F. #703 control-doc collision

- L02 code/test blobs at `31c59b6d1` are already identical in `d119045f`; do not
  re-receive code.
- #703 branch control docs overlap `COMPONENT_STATUS.jsonl`,
  `CURRENT_SEAM_STATES.jsonl`, `README.md`, `REMAINING_REAL_PYAT_WORK.md`,
  `NEXT_R_GAP49_NEXT_DECISIONS.md` and S02–S11. One reconciler must select current
  rows, not merge the stale branch wholesale.
- Current #703 code consumer belongs E; physical fan-in belongs C; no overlap with
  #705 documentary receiving.

## G. No-change zones

Do not modify: 35 source manifest rows/counts, 25 W/P IDs, 62 component IDs, 82
seam IDs/kinds/predicates, 49 GAP IDs, 51 graph child IDs, 88 direct arcs, 13 IF
edges, C8 expected sets, FIABC 144/3, native/source/actor/FF holds, or protected
CAS without the qualified owner and independent review.
