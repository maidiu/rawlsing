# PYAT C2-02 — NEXT C4 PROVING-WORKLOAD WITNESS SELECTION — R1

Disposition:

`INPUT_OR_CUSTODY_BLOCKER`

Terminal:

`C2_02_C4_PROVING_WORKLOAD_RETURNED__HQ_ADJUDICATION_REQUIRED`

Branch:

`agent/rabochii-pyat-hq131-c2-02-proving-workload-r1`

Commission tip:

`440e0a600f66103aad6076979cb23209f0a0ae4a`

Exact base:

`c5cb9ea33192dfc438b9559691832e1a6aaf96fc`

This is source-free documentary workload selection only.

C4 was not executed. Raw survey data was not opened, materialized, decoded, or inferred from. Production code was not mutated. No semantic, comparability, pooling, survey, model, or epistemic-origin authority was created.

## 1. Selected proving set

The smallest competent set I can justify at the commissioned edge-class grain is **8 exact source identities**:

| source | exact role |
|---|---|
| SRC02 — Afro Barometer Round 5 | G01 user-missing native-int→float64 representation edge |
| SRC06 — Arab Barometer Wave 5 | G01 observed native-int→float64 representation edge |
| SRC08 — Asian Barometer Wave 1 | D01 exact-SHA BIG5 admission |
| SRC12 — EVS 1990 | D01 exact-SHA WINDOWS-1252 admission + EVS multi-wave member 1 |
| SRC14 — EVS 2008 | D02 opaque decoder-native date/time edge + EVS multi-wave member 2 |
| SRC26 — Latinobarometro 2024 | unique R05 raw-header / decoded-dictionary-width divergence |
| SRC27 — LiTS I | fresh-current full Route-B anchor + B01 bounded DTA bridge |
| SRC35 — WVS Wave 7 | retained full-route comparator + B02 Q291 bounded SAV bridge |

The exact identities, SHAs and operations are frozen in
`02_PROPOSED_PROVING_SET.json`.

## 2. Why three sources are not sufficient

Three identities are only the logical lower bound for:

- at least two source families; and
- at least two waves in one family.

That lower bound is not a competent physical/authority proving set.

The source ledger contains independent edge classes that cannot be merged merely because one can fit two families and two waves into three files:

- G01 user-missing representation;
- G01 observed representation;
- D01 BIG5;
- D01 WINDOWS-1252;
- D02 opaque decoder-native date/time;
- R05 raw-header/dictionary-stream divergence;
- LiTS-I B01 + retained canonical empirical closure;
- WVS7 B02 + retained admitted release/replay/oracle.

The selected EVS 1990 + EVS 2008 pair satisfies the same-family/multi-wave requirement **without adding two extra generic waves**: both were already independently required by D01/D02.

Removing any of the eight selected identities loses at least one commissioned edge class or the LiTS/WVS retained-vs-fresh proof shape.

## 3. Full-route versus physical-edge roles

The set is intentionally tiered.

### Full empirical Route-B anchors

**SRC27 LiTS I**

This is the proposed one-fresh-pass current production witness after all execution prerequisites are met.

Exact retained independent evidence already exists:

- source SHA:
  `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- canonical empirical closure:
  `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`;
- checkpoint SHA-256:
  `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`;
- oracle identity:
  `e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a`;
- 50 candidates;
- 77 exact query roles;
- 60 empirical facts;
- 50 discovery receipts.

C4 should perform **exactly one governed fresh LiTS-I source-backed pass**, then compare the current identities/preimages against this retained independent material.

**SRC35 WVS7**

WVS7 supplies the deliberately different half of AT21: competent retained evidence that should **not** be gratuitously reread merely so it can be called fresh.

Retained accepted identities include:

- source SHA:
  `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- admitted logical release:
  `e6881e9a08a48f8871790e781c28bddbc44ee35db894d6ad7b1105a6a8fd262f`;
- replay:
  `996ba218fc5da5e0ad1ddf0cdc7f91ce8fb8a7363ce62076dc3f4073b85c383f`;
- independent oracle:
  `3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800`.

### Physical-edge witnesses

SRC02, SRC06, SRC08, SRC12, SRC14 and SRC26 are selected to prove current physical/representation/decoder boundaries, **not** to manufacture survey-semantic Route-B authority.

If HQ broadens C4 to require full semantic Route-B composition on those six sources, that becomes a separate:

`TYPED_AUTHORITY_RESIDUAL`

until competent source-specific semantic authority is frozen.

## 4. Fresh-source read plan

The workload distinguishes what truly needs current source contact from what can lawfully use retained proof.

Fresh full-route read:

- SRC27 LiTS I — exactly one governed source-backed pass.

Fresh bounded physical reads, if the final C4 freeze includes current real-source edge revalidation:

- SRC02;
- SRC06;
- SRC08;
- SRC12;
- SRC26.

Conditional fresh read:

- SRC14 EVS 2008 — **not yet lawful** for the D02 proof until the blocker below is closed.

No fresh raw-source read required:

- SRC35 WVS7 — retained exact release/replay/oracle comparator.

Excluded sources:

- **0 fresh reads** in the minimal proving workload.

Every fresh source must independently record source SHA/config, full-file hash passes, path opens, metadata/header reads, decoder invocations, selected/full reads, retry counts and the accounting basis.

## 5. Exact blocker

One source-input custody gap prevents me from honestly returning `READY_FOR_HQ_C4_FREEZE`.

The accepted CLOSED35/C2-01 evidence proves:

- D02 is an exact generic nonsemantic implementation debt;
- the affected exact source is SRC14 EVS 2008;
- C3 now supplies the accepted generic opaque decoder-native date/time carrier law.

But the inspected source-free evidence does **not** freeze an exact real-source EVS 2008 date/time-bearing physical column/cell locator, nor an independently frozen whole-source traversal oracle identifying the expected D02 occurrence.

That matters because AT20 requires an independent oracle. C4 cannot:

1. open EVS 2008;
2. discover which field produces the native date/time object;
3. then use that C4 discovery as its own expected witness.

Blocker:

`C2-02-BLOCK-D02-LOCATOR-001`

Wake condition:

- recover/freeze an exact immutable physical locator + expected native-type/carrier witness from competent retained evidence; **or**
- independently freeze a deterministic whole-source D02 traversal oracle before C4 source execution.

This is an input/custody problem, not permission to inspect the raw source in C2-02.

## 6. Other mandatory pre-execution dependencies

Two additional dependencies must be true at the final C4 execution head.

### C1-01

C1-00 R4 contract/oracle has independent approval, but inspected evidence still states C1-01 is unimplemented/unexecuted.

C4 full Route-B composition must therefore wait for a separately frozen and independently accepted C1-01 implementation/court.

C1-00 approval is not silently treated as C1-01 execution approval.

### C3 integration ancestry

Accepted C3 integration head:

`30686b185d4ceb2c94f61815ef70d8c8e76255d6`

Independent C3 integration review:

`462e6bf1ed514056f9316dad761054e690a7755d`

The exact C2-02 base does not itself contain those integrated G01/D01/D02 implementation blobs.

The eventual C4 execution head must therefore either:

- descend from the accepted C3 integration; or
- independently prove exact blob equivalence for the accepted six-file C3 implementation/test surface.

These are execution-ancestry prerequisites, not authority to rewrite C2-02.

## 7. All-35 conservation

All 35 exact source identities are accounted for in
`05_ALL35_HORIZONTAL_ACCOUNTING_PLAN.json`.

The plan contains:

- 8 selected identities;
- 27 explicitly excluded identities;
- exact source file/SHA/format/family/wave;
- historical representation state;
- selection/exclusion reason;
- explicit proof ceiling.

No excluded source disappears.

In particular:

- SRC03 X01 remains unresolved;
- SRC05 X02 remains unresolved;
- excluded authority-blocked surfaces remain blocked/unproved;
- SRC21's exact G01 scope remains distinct even though SRC06 is the smaller observed-value proving witness;
- WVS1 blocked surfaces remain blocked;
- WVS4 is not promoted into F7 comparability merely because WVS7 is selected.

C4 success on eight sources may not become an `ALL35_PASS`.

The 280 source×F1-F8 cells remain individually accountable.

## 8. AT01 / AT02 / AT20 / AT21 / AT27 result

- **AT01** — exact identity workload selected; execution pending.
- **AT02** — exact authority boundaries selected with explicit no-inference ceilings.
- **AT20** — independent oracle/source accounting shape selected; D02 locator blocker prevents complete freeze.
- **AT21** — LiTS fresh-current versus WVS retained proof shape selected.
- **AT27** — all 35 identities retained in the horizontal accounting plan; no global green claim.

## 9. Epistemic-origin residual

Carried unchanged:

`C2-EPCLASS-PAYLOAD-001 = UNRESOLVED__NOT_MISSING_PROVED`

No row-level epistemic-origin classification was inferred or invented.

## 10. Return artifacts

- `01_OBLIGATION_TO_SPECIMEN_MATRIX.json`
  blob `e3ff869a3901584b4b9bcb57ef90e30b2496b1b2`
- `02_PROPOSED_PROVING_SET.json`
  blob `e54a0cd79c97538584226d07ab6d64bf07b88d4a`
- `03_REDUNDANCY_AND_EXCLUSION_AUDIT.json`
  blob `b77cf9f9bdde357963bb265845f6c087eee9b034`
- `04_AUTHORITY_ORACLE_RETENTION_REQUIREMENTS.json`
  blob `f73be03ff2d93d04c1bb74d2d0f920f64f351423`
- `05_ALL35_HORIZONTAL_ACCOUNTING_PLAN.json`
  blob `6db0c4d3e648d54ca87ef036fd5fbe4844397778`
- `06_FINAL_DISPOSITION.json`
  blob `9ad3fb14d9f344d213258556b30ddc0cd2be447a`

## 11. Final

The source-selection problem itself is closed at the commissioned documentary grain:

**eight exact sources are necessary and sufficient for the declared heterogeneous edge workload.**

The workload is **not yet executable as a fully frozen C4 court** because the unique SRC14 D02 real-source witness lacks a predeclared exact locator/oracle.

Disposition:

`INPUT_OR_CUSTODY_BLOCKER`

HQ can close that narrow blocker, require accepted C1-01 and C3 ancestry, and then issue the governed C4 execution freeze without reopening the eight-source selection.

`C2_02_C4_PROVING_WORKLOAD_RETURNED__HQ_ADJUDICATION_REQUIRED`
