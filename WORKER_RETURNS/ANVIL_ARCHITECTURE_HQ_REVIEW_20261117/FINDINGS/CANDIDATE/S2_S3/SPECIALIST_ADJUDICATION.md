# SPECIALIST ADJUDICATION — both returns consumed

**Status:** both returns received and adjudicated; no outstanding specialist
dependency. HQ receiving records are qualifications, not architecture acceptance.

## Exact pins

| Lane | Commit | Root | HQ verification |
|---|---|---|---|
| Construction | `f8c98027599b62069c03a269989075b4442f5138` | `WORKER_RETURNS/ANVIL_ARCHITECTURE_SPECIALISTS_20261117/CONSTRUCTION/` | 7 payload hashes, 12 source pins; `evidence/CONSTRUCTION_SPECIALIST_RECEIVING.json` |
| Query | `a5ea7fd9c6d8fdb4ba43d839bff900df4b60d89a` | `WORKER_RETURNS/ANVIL_ARCHITECTURE_SPECIALISTS_20261117/QUERY/` | 7 hashes, 10 source pins; `evidence/QUERY_SPECIALIST_RECEIVING.json` |

Both used the same frame commit `5a619ff9…` and product cut `cea2d4d…`; neither
edited product code, ran a heavy/native benchmark, or claimed final acceptance.

## Findings that survived independent agreement

- Cold `H` hashes all 14 members and checks manifest/I02/root/census; it is per
  fresh admission, not per operation.
- `DirectEstateI03Session._build` scans all event and side-family row groups and
  builds a temporary SQLite index `S`; `PreparedI03Session` reuses it only within
  one process.
- `execute_empirical_query` loops all universe respondents `Q`; there is no
  selective pushdown in the cold path.
- `SavedC11Admission.execute_i03/i05` and saved Batch units open fresh sessions;
  the prepared session is not forward-wired. NORMAL/resume remain typed owner
  holds.
- Facts carry full risk/denominator member refs; evidence output `O` can
  dominate and is not reduced by prepared-session reuse.
- The writer builds a second I02 and re-reads every Parquet row; the Q2/13-family
  journal is duplicated; the target is created before the manifest, leaving a
  real orphan window.
- The 100k witness is sparse (3.245 events/respondent), sourcefree/cut-specific;
  5.26/4.39/1.30 GB are disk/staging, not RSS.

## The disagreement and adjudication

**Construction:** recommends A1+A2+A5+A10 — one Q2 certificate, one journal, one
full physical proof, durable index, atomic recovery — with fallback to the
second certificate.

**Query:** recommends prepared-session-first; the durable index is conditional
on measured `S`, and the cited SQLite index is 1.30 GB (4.19× the 310.16 MB
estate) with unproven invalidation/rebuild economics.

**Adjudication (whole-system cost, not majority):**

1. **Prepared-session-first is selected** for the first consumer because it is
   the smallest change from actual code, adds no retained artifact, preserves
   exact facts/replay, and removes repeated `S` within a process.
2. **Durable index is held**, not rejected forever. It is the only route that
   removes `S` on a one-operation fresh open, but it must earn its 1.30 GB
   retained cost and invalidation/rebuild burden after `H/S/Q/O` measurement and
   a compact exact encoding. It is not a first selection.
3. **Construction one-certificate/one-journal is conditional**, not automatic.
   Duplicate certification may carry independent proof value; full physical
   body/lane/selector proof against Q2 is the gate. If it fails, keep the second
   certificate and take only one-journal + recovery + prepared session.
4. **Recovery repair is selected independently** because the current
   target-before-manifest window is a real interrupted-build defect. Use a
   private stage, no-clobber claim/lease, typed orphan and manifest-linked
   completion; do not claim a portable atomic-rename no-clobber guarantee.
5. **Evidence/output contract is adopted** as exact identity only: share
   content-addressed sets only under identical population/condition/routing/
   measure/wave; forward/reverse, weighted/unweighted and cross-wave remain
   separate; replay re-executes; cached facts never authoritative.

## Corrections applied

- 2×100,000 refs at 150–250 bytes = **30–50 MB per fact**, not 15–25 MB;
  100 facts = **3–5 GB** before provenance. Actual cardinality/serialization
  unknown.
- One-admission reused vs truly fresh formulas separated:
  `H+N(S+Q+O)` vs `N(H+S+Q+O)`; prepared same-process `H+S+N(Q+O)`; durable
  index `H+I+N(Q+O)`.
- The 1.69–1.70× four-op author report is **not** a measured 100-op asymptote;
  the `S/Q≈1.2` inference is hypothetical.
- No blanket no-cache/full-hash/replay algorithm is adopted as permanent law;
  the contract is exact identity + per-operation current/replay.
- Atomic rename may clobber; no false crash guarantee.
- The final package manifest and `FINAL_DECISION_GUARD.txt` hashes are
  independently recomputed at freeze.

## New frame requirements adjudicated

Adopted into `S1/FRAME_V2_ADDENDUM.json`:

- `REQ-COST-LAYER-DECOMPOSITION` — H/S/Q/O separation, present-hard.
- `REQ-DERIVED-INDEX-BINDING` — future nonpreclusion / conditional owner gate.
- `REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY` — present-hard exactness, no blanket
  cache law.
- `REQ-CONSTRUCTION-ATOMIC-RECOVERY` — present-hard interrupted-build recovery.

The immutable base 16/118 frame is preserved; the addendum is the v2 shared
frame for final selection. No new science, K3/K4, F26 caller or native right is
invented.

## No acceptance

Both returns are specialist documentary analyses. Their local pins and HQ
receiving are not independent architecture C, native/source/science/actor
qualification, 100k/6 GiB/1-10-100 measurement, or protected adoption.
