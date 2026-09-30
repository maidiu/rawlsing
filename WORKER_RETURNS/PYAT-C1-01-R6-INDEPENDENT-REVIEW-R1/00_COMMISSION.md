# PYAT C1-01 — R6 NORMATIVE IDENTITY INDEPENDENT REVIEW — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Independent Browser/GitHub documentary + code reviewer, GPT-5.6 Sol High

Branch:
`agent/reviewer-pyat-hq133-c1-01-r6-r1`

Exact base / returned patch:
`663379caa7c9b8a80bca889d8d5b59d0486ff901`

Original R6 commission:
`8a038b99d432cc13e9342f9073382ec10076b04d`

Do not mutate production code. Review only.

## Mission

Independently determine whether the returned R6 patch correctly implements HQ's fixture-only normative identity supersession without smuggling in real-source semantics or weakening the accepted C1 relation/evidence law.

The worker disposition is:
`PATCH_READY__EXECUTION_CAPABILITY_BLOCKED`.

Execution is being qualified separately. This review is primarily semantic-contract, scope, identity and test adequacy review.

## Required checks

### A. Exact scope

Compare commission→return and require that all changed files are inside the exact R6 allowlist.

Verify:
- `rawlsing_next/pre553_analytical_composition.py` remains exact blob
  `5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`;
- no public producer/consumer owner changed;
- no raw-source authority/control file changed.

### B. R6 query identity

Recompute independently from committed material:

Forward query expected:
`8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`

Reverse query expected:
`2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`

Verify the exact HQ normative caller-defined fields:
- query_id;
- synthetic subject material/ref;
- requested_projection;
- null effective_time_or_interval.

Ensure the remaining query material comes from exact already-accepted AT07 source/release/target/binding objects rather than inference.

### C. R6 witness identity

Independently verify the witness material is an exact CLOSED 16-field mapping and no additional field can influence identity.

Expected witness hashes:

Forward:
`f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`

Reverse:
`a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`

Pay special attention to whether the committed R6 packet contains enough exact material and exact references to reconstruct the full 16-field witness preimage later without repeating the R5 underdetermination problem.

If the packet only records resulting hashes/summaries but leaves any identity-bearing field underdetermined, return CHANGES_REQUIRED and name the missing material.

### D. Evidence supersession

Independently recompute the new noncircular evidence identity from the accepted evidence-preimage law with R6 witness refs.

Expected:

Forward:
`c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`

Reverse:
`0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

Verify old R2/R3/R5 opaque hashes remain preserved as historical superseded fixture evidence and are not reverse-engineered.

### E. Test adequacy

Inspect the exact modified:
`rawlsing_next/tests/test_pre553_analytical_composition.py`

Require that it actually constructs:
public producer → frozen analytical adapter → public positioned-subject consumer

and verifies:
- 54/60 forward;
- 54/62 reverse;
- new R6 query/witness/evidence identities;
- actual producer identity;
- denominator-derived raw_support;
- stale/mutated witness failure;
- mismatched relation failure before evidence construction and consumer invocation;
- no preconstructed final slice;
- old historical hashes not treated as current.

Check all commissioned mandatory hostile dimensions from C1-01; if any are missing from the R6 test after the large rewrite, name them exactly.

### F. Authority ceiling

R6 must remain source-free fixture identity authority only.

It creates no:
- real-source comparability;
- survey semantics;
- model authority;
- structural truth;
- actor inference.

## Return terrain

Write only:
`WORKER_RETURNS/PYAT-C1-01-R6-INDEPENDENT-REVIEW-R1/**`

Required:
- `00_REVIEW.md`
- `01_SCOPE_AND_IDENTITY_AUDIT.json`
- `02_PREIMAGE_COMPLETENESS_AUDIT.json`
- `03_TEST_AND_HOSTILE_AUDIT.json`
- `04_FINAL_DISPOSITION.json`

Allowed:
- `APPROVE_AT_DECLARED_GRAIN`
- `CHANGES_REQUIRED`
- `ESCALATE_WITH_COUNTEREXAMPLE`

Do not claim execution PASS. Execution is a separate lane.

Terminal:
`C1_01_R6_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
