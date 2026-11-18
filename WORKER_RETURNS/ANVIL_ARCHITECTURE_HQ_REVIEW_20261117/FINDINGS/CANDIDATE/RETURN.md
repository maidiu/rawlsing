# RETURN — final conditional integrated candidate

**Status:** `FINAL_CANDIDATE_CORRECTED_PENDING_SAME_DISTINCT_C_RECHECK`.
**Predecessor:** `98b8d261accfcc7834c86d3f0d52f23e4524f666` (tag `anvil-architecture-candidate-20261117-r1`, untouched).
**Branch:** `agent/anvil-integrated-architecture-20261117-r1`.
**Corrected candidate tag:** `anvil-architecture-candidate-20261117-r2` (applied at this correction commit).
**Final selection frozen:** yes, as a **conditional candidate**; **not accepted**.
**Independent C / protected H1:** not performed, not claimed.

## Exact refs

| Purpose | Ref |
|---|---|
| S1 common frame (immutable) | commit `5a619ff9fa79be9183eb4d4378d42f040ef2bd9b`; `7e7bfb96…` |
| S1 v2 addendum | `S1/FRAME_V2_ADDENDUM.json`; `aa170d89…` |
| Final decision | `S2_S3/FINAL_DECISION.json`; local guard PASS 16/16, 118/118 |
| Product cut | `cea2d4d3009e9087d2267e9d1f53bec28b730dc7` |
| Protected currentness read | `31291d08179890852246c8742700e055168e9933` |
| Register snapshot | `b830458c3ebfe0a3f0e2d18e516e68b90324c88a` |
| Construction specialist | `f8c98027599b62069c03a269989075b4442f5138` (7 hashes/12 pins) |
| Query specialist | `a5ea7fd9c6d8fdb4ba43d839bff900df4b60d89a` (7 hashes/10 pins) |

## Selected conditional design

**Prepared-session-first**, with **conditional construction/recovery repair**;
the **durable locator index is held**, not selected.

1. **Query first step:** one `PreparedSavedC11Admission.open` + one
   `prepared_i03` per exact release/universe/workload; forward-wire the existing
   `PreparedI03Session` into the real I03/I05 first consumer and saved Batch
   units. Keep `check_current` before/after every operation and per-operation
   fact/replay.
2. **Construction conditional:** one 13-family journal and one Q2 certificate
   only if full physical body/lane/selector proof against Q2 survives; otherwise
   keep the second certificate. Remove the duplicate 3-family journal and the
   target-before-manifest orphan window; private stage, no-clobber claim/lease,
   typed orphan. No false atomic-rename guarantee.
3. **Durable index held:** 1.30 GB cited SQLite index (4.19× the 310.16 MB
   estate), invalidation/rebuild and `S` share unmeasured. Qualify only if
   `H/S/Q/O` measurement shows `S` material and a compact exact encoding earns
   its retained cost.
4. **Evidence:** exact fact/replay identity; content-addressed set refs only
   under identical population/condition/routing/measure/wave; forward/reverse,
   weighted/unweighted, missing/routing and cross-wave remain separate; replay
   re-executes; cached facts never authoritative.
5. **Recovery:** private stage, no-clobber claim/lease, manifest-linked
   completion, typed orphan; completed/other-writer releases never overwritten
   or deleted; GC only proven-dead scratch.

## Why this over the specialists

Construction favored a durable index; Query favored prepared-session-first and
showed the durable index’s retained/invalidation cost. The adjudication is not a
majority vote: prepared-session-first is the smallest actual-code change with no
retained artifact; the construction one-certificate is conditional on full Q2
proof with a second-certificate fallback; the durable index is the only
fresh-open `S` remover but must earn its retained cost. See
`S2_S3/SPECIALIST_ADJUDICATION.md`.

## Corrected cost facts

- 2×100,000 refs at 150–250 bytes = **30–50 MB per fact**, not 15–25 MB;
  100 facts = **3–5 GB** before provenance; actual serialization unmeasured.
- One admission reused: `H + N(S+Q+O)`; truly fresh: `N(H+S+Q+O)`; prepared
  same-process: `H + S + N(Q+O)`; durable index: `H + I + N(Q+O)`.
- The 1.69–1.70× four-op report is **not** a measured 100-op asymptote; any
  `S/Q` inference is hypothetical.
- 3033.723 s / 310.16 MB / 5.26 GB / 4.39 GB / 1.30 GB / 562.362 s are cited
  sourcefree, cut-specific; 5.26/4.39/1.30 GB are disk, not RSS; 3.245
  events/respondent is sparse, not dense 100k.

## Executed witnesses (sourcefree existing code)

| Command | Result | Log |
|---|---|---|
| `pytest -q rawlsing_next/tests/test_pre553_prepared_saved_i03.py` | 3 passed in 4.69 s | `RUNS/prepared_saved_i03.txt` |
| `pytest -q rawlsing_next/tests/test_pre553_direct_estate_i03.py` | 7 passed in 2.08 s | `RUNS/direct_estate_i03.txt` |
| `pytest -q rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py` | 24 passed in 12.78 s | `RUNS/saved_native_first_consumer.txt` |

These are not native/source proof; they show the native evaluator executes on
sourcefree fixtures. No 100k/6 GiB/1-10-100 claim.

## New frame requirements adjudicated

`REQ-COST-LAYER-DECOMPOSITION`, `REQ-DERIVED-INDEX-BINDING`,
`REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY`, `REQ-CONSTRUCTION-ATOMIC-RECOVERY` are in
`S1/FRAME_V2_ADDENDUM.json`. The immutable base 16/118 frame is preserved. The
52/24/21 #1097 estate remains navigation/negative, not additive.

## Holds unchanged

26 PYAT-PC `NOT_ADOPTED`; 14 P4R `HELD`; F26 exact hold; native original35/
source/science/actor; 100k/6 GiB/1-10-100; F5–F8/N9/N10W/SEAM/SOROK actual
readers; Batch/NORMAL/resume owner ACKs; durable index conditional; independent
C; protected H1.

## Manifest

`PACKAGE_MANIFEST.json` is regenerated at final freeze over all owned payloads
except itself; `S2_S3/FINAL_DECISION_GUARD.txt` is included with its actual
hash. The prior provisional manifest mismatch is corrected here. The local guard
PASS is structural, not independent architecture/science acceptance.

## Stop

Stop for distinct independent C on the tagged candidate. No author acceptance,
no protected adoption, no implementation or benchmark campaign.


## D1–D5 correction (same distinct C)

See `S2_S3/D1_D5_CORRECTION_MAP.md`. D1 specialist state received/adjudicated; D2 machine architecture/sequence/per-requirement effects/crosswalk regenerated for prepared-session-first + conditional construction/recovery + held index; D3 v2 supplementary guard calls accepted guard and checks 20/20 + 118/118 with omission/unconditional/stale negatives REFUSE; D4 wrapper/Batch grade `PROPOSED_NOT_WIRED`, direct prepared path separate, exact ABI boundaries and owner protocol recorded; D5 provisional files marked `SUPERSEDED_BY_FINAL` and manifest roles split. N3 Q2 must be source-derived, not journal-originated. No product edit, native run or engineering launch. Stop for the same reviewer recheck.
