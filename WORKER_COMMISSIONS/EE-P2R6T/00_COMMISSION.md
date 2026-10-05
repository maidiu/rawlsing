# EE-P2R6T — LITS AS2A PINNED AUTHORITY PATH-REF REPAIR

Repository:

`maidiu/rawlsing`

## Execution surface

**BROWSER**

## Library access

**NO**

Do not access Library files, LiTS/WVS carrier bytes, empirical outcomes, or performance measurements.

Exact branch:

`agent/rabochii-prev3-ee-p2r6t-lits-as2a-path-ref-repair-r1`

Exact base:

`d0187a01f21959f4834a7f774f92d06187f1efb3`

Before doing anything else, resolve live canonical HQ through:

`HQ_HANDOFF/LATEST.json`

and verify its immutable checkpoint packet.

At commission time the sealed checkpoint is:

`20260919T0130-0400`

with immutable handoff:

`54be9182ca73aa3ee969e6a6429d3fd426cc73ff`

Controlling decision:

`HQD-2026-09-19-077`

Read prospectively:

`HQ_HANDOFF/EE_P2X_LITS_AS2A_PATH_BLOCKER_ADOPTION_20260919.md`

## Mission

Repair exactly one pinned-authority path reference in the already-qualified production backend.

Do not change authority content.

Do not change the pinned authority commit.

Do not redesign the backend.

Do not execute the measured court.

The exact production blocker is:

`EE_P2X_LITS_I_A_S02_C11_REACHABILITY__COMMON_COURT_AUTHORITY_FAILURE`

at P2X return head:

`d0187a01f21959f4834a7f774f92d06187f1efb3`

## Exact backend

Path:

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

Current backend blob:

`ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

Pinned authority commit:

`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

Current wrong path component:

`AS2A_LITS1_SHARED_CERTIFICATION_20260827`

Exact path component at the pinned commit:

`banked_as2a`

Required exact repair:

Change only the backend constant/path construction needed so:

`LITS_LEDGER`

resolves to:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2a/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv`

and:

`LITS_PACKAGE`

resolves to:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2a/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json`

No alternate path is authorized.

No fallback lookup is authorized.

No latest/fuzzy/default path search is authorized.

## Exact authority identity that must remain unchanged

At pinned commit `3ce639e1...`:

Ledger Git blob:

`c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c`

Package Git blob:

`174b931e8aa89111086e3d46159b47154bed7f16`

These are byte-identical to the later canonical-name vendored copies under:

`WORKER_RETURNS/EE-P2R6K/SUPPORT/R5B/SUPPORT/FROZEN_BASE/AS2A_LITS1_SHARED_CERTIFICATION_20260827/`

The underlying banked builder remains:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2b/run_as2b_lits1_mechanical_certification.py`

Builder Git blob:

`c51b56779ab9d79126619b7733d41f5253c8150f`

The builder's internal expected semantic identities remain:

Part-A projection authority hash:

`9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06`

Slot ledger SHA-256:

`65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60`

Source SHA-256:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Do not alter any of these.

## Required proof

Browser qualification must prove:

1. backend still exports:
   `BACKEND_CONTRACT = "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"`;
2. pinned authority commit remains exactly `3ce639e1...`;
3. repaired `LITS_LEDGER` path resolves at that exact commit;
4. repaired `LITS_PACKAGE` path resolves at that exact commit;
5. resolved ledger Git blob is exactly `c24e0d6a...`;
6. resolved package Git blob is exactly `174b931e...`;
7. ledger SHA-256 recomputes exactly to `65bdb972...`;
8. package projection material recomputes exactly to `9dd1e6b7...`;
9. the exact banked builder's `read_banked_authority()` accepts these bytes when deployed under the backend's normal bounded deployment;
10. no path fallback exists;
11. missing exact `banked_as2a` path fails closed;
12. substituted ledger/package blob fails closed;
13. backend stage dispatch contract and existing R6S stage coverage remain unchanged;
14. no Library/carrier/outcome/performance access;
15. no P2X branch movement.

Prefer a static/fixture proof over executing source-dependent backend work.

Do not open LiTS.

## Diff law

Production diff must be minimal.

The only production source file permitted to change is:

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

The semantic effect must be only:

`PINNED_AUTHORITY_PATH_REF: canonical-name-missing -> banked_as2a-existing`

No other runtime behavior may change.

Qualification tests and governed return files may be added under their proper paths.

Any transient `.rabochii/court_spec.json` mutation must be restored byte-exact before final return.

## Required outputs

Production:

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

Qualification test:

`rawlsing_next/tests/test_ee_p2r6t_lits_as2a_path_ref_repair.py`

Governed return under:

`WORKER_RETURNS/EE-P2R6T/`

At minimum:

1. `00_RETURN.md`
2. `01_PINNED_TREE_AUTHORITY_RECEIPT.json`
3. `02_PATH_REF_REPAIR_RECEIPT.json`
4. `03_NEGATIVE_COURT.json`
5. `04_BROWSER_QUALIFICATION_RECEIPT.json`

## PASS terminal

`EE_P2R6T_PASS__LITS_AS2A_PINNED_AUTHORITY_PATH_REF_REPAIRED__EXACT_BANKED_AUTHORITY_BYTES_PRESERVED__READY_FOR_HQ_SELECTIVE_BACKEND_FANIN_AND_P2X_RESUME`

PASS wakes HQ adjudication only.

P2X remains held until HQ selectively fans the repaired backend blob into the same existing P2X branch and seals resume authority.

## BLOCK terminal

`EE_P2R6T_BLOCK__<EXACT_FIRST_PINNED_PATH_BLOB_OR_BACKEND_CONTRACT_MISMATCH>`

## Hard forbidden

- no Library access;
- no carrier/source bytes;
- no empirical outcomes;
- no performance measurements;
- no authority content mutation;
- no pinned commit change;
- no fallback/latest/fuzzy path lookup;
- no backend redesign;
- no owner/driver redesign;
- no workload/Lock mutation;
- no Candidate-C repair;
- no P2X branch movement;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase;
- no replacement branch.

Run governed Browser qualification.

Commit and push the exact branch.

Report PASS/BLOCK, final tip, repaired backend blob, exact resolved ledger/package blobs, Browser qualification run/job/artifact, and wake.

Return to HQ.
