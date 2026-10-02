# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT AT07 SUCCESSOR SPINE — INDEPENDENT ORACLE REVIEW — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/reviewer-pyat-hq165-at07-successor-spine-independent-review-r1`

Exact oracle return:
`92ddee2241a78b46394665d325e5ebf0e75adf40`

Oracle artifact commit tested by producer:
`79a3b7e5a0de42ee49db2bc533daf19a7d2f3b74`

The only commit after that tested artifact commit adds:
`09_EXECUTION_RECEIPT.json`

Governing Astra ruling:
`a2e7767ecec9ecb6d241861628759f2e933920d5`

Do not modify implementation or oracle artifacts.

## Mission

Independently review the complete versioned AT07 successor-spine oracle package.

This is not a candidate-comparison or AT17-requalification lane.

Approval requires confidence that the successor oracle was derived independently from pinned law, not fit to candidate output, and that both forward and reverse expected identities are fully determined by the frozen inputs and adjudicated identity contract.

## 1. Provenance and terrain

Verify:

- branch final head is exactly `92ddee...`;
- commission base is `f23a3ac...`;
- all return movement is confined to:
  `WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/**`;
- no `rawlsing_next/**` file changed;
- original R8 historical artifacts were not modified;
- `79a3b7e5...` contains the final core oracle artifacts;
- `92ddee...` differs from it only by `09_EXECUTION_RECEIPT.json`.

Verify every copied `INPUTS/**` artifact against its stated original Git blob/commit. Do not trust only the worker's SHA-256 table.

## 2. Independence / contamination attack

Independently inspect `07_ORACLE_PROCEDURE.py` and the package.

Approval requires proving that expected truth is not obtained by:

- importing or executing production analytical composition;
- calling `AnalyticalCompositionResult.identity_material()`;
- calling the provider/consumer production path to obtain expected hashes;
- copying the known join forward digest into the result;
- reading a precomputed reverse successor digest from another accepted artifact;
- silently deriving expected truth from candidate output.

The known forward candidate observation
`01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd`
was disclosed in advance. Therefore do not treat mere agreement with it as evidence of independence.

Search the procedure/package for literal or indirect contamination paths.

## 3. Independently reconstruct the field-law delta

Do not trust the frozen manifest by assertion.

From the historical owner blob:
`26f3380cb83cbbcedc87c74aaf603b0492c8ce8f`

and adopted owner blob:
`604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`

independently enumerate the direct composed identity field sets.

Approval requires exactly:

- historical: 38 direct fields;
- current: 44 direct fields;
- removed: 0;
- added: exactly six:
  1. `discovery_receipt_refs`
  2. `discovery_frontier_ref`
  3. `recursive_handoff_refs`
  4. `recursive_lineage_refs`
  5. `joint_component_count`
  6. `joint_order_semantics`

Then independently establish the lawful direct AT07 values:

- `discovery_receipt_refs=[]`
- `discovery_frontier_ref=null`
- `recursive_handoff_refs=[]`
- `recursive_lineage_refs=[]`
- `joint_component_count=1`
- `joint_order_semantics="SEMANTIC_ORDERED"`

Do not conflate nested witness evolution with new top-level composed fields.

## 4. Independent hash reconstruction

This is the core review.

Using your own scratch/review derivation—not merely invoking the producer's `generate` mode—independently verify enough of the complete pinned preimages to establish both expected successor hashes.

At minimum independently verify:

- canonical source law:
  - forward 54/60 with cells 54/6;
  - reverse 54/62 with cells 54/8;
- frozen producer/query/predicate/fact/replay refs;
- consumer query identity;
- full 16-field witness identity and custody;
- source/release refs;
- risk/target/measure fields;
- evidence refs and consumer-result hashes where conserved;
- all 38 historical fields;
- all six direct additions;
- canonical ordering/null/empty/default semantics.

Then independently canonicalize/hash the complete forward and reverse successor preimages.

Expected only if independently obtained:

Forward:
`01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd`

Reverse:
`a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca`

Also independently reproduce the historical R8 digests:

Forward historical:
`03610f9d91b23cfb6f862dc91b5de92c7f4e4b8e44a53b9efdacb1cf73af6b9e`

Reverse historical:
`1202822cf98d802c04440328496dc64ee02e6d6030a3da6c9bf10ef1a6490a3c`

If the full expected preimage cannot be independently determined from frozen inputs and law, return:
`CHANGES_REQUIRED`
with the exact missing/ambiguous field. Do not bless a matching hash.

## 5. Procedure rerun

After the independent reconstruction above, run the producer's committed procedure:

- `generate`
- `verify`
- `hostiles`

Verify it reproduces the persisted artifacts exactly.

Check that generation does not mutate frozen inputs or historical evidence.

## 6. Hostile quality

Do not accept "44/44" based on count alone.

Verify the hostile set substantively covers:

- omission and wrong value for every one of the six direct additions in both directions;
- release mutation;
- source-universe mutation;
- witness mutation;
- authority mutation;
- serialization mutation;
- key ordering;
- array ordering;
- old-owner substitution;
- frozen-input mutation.

Verify mutations are rehashed/revalidated and are not rejected merely because a stale expected checksum was left unchanged.

Add independent review-only probes if needed.

## 7. Historical conservation

Verify:

- R8 bytes remain unchanged;
- old forward/reverse digests reproduce exactly;
- successor hashes are distinct versioned identities, never aliases;
- 38 existing fields are canonically equal in each direction;
- no existing field's value changed;
- source/authority/relation freezes remain unchanged;
- no claim is made that the successor was already current before this review/adoption.

## 8. Execution provenance

Reconcile the producer receipt:

- artifact commit tested: `79a3b7e5...`;
- clean tree before/after;
- Python 3.11.3;
- exact commands and exit 0;
- 44 rejected hostiles / 0 false accepts;
- final head `92ddee...` is one receipt-only commit later.

Independently rerun the oracle procedure in your reviewer environment and record your own runtime/commands/results.

Do not use the producer's environment as your only evidence.

## 9. Scope ceiling

Do not:

- compare against production candidate execution as acceptance evidence;
- modify AT17/N10E;
- rerun the C1-03 join;
- re-open C1-03A/R;
- access raw survey sources;
- broaden model/comparability authority.

The successor oracle is the only object under review.

## Return

Write only:

`WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-REVIEW-R1/**`

Required:

- `00_REVIEW.md`
- `01_PROVENANCE_AND_INDEPENDENCE_MATRIX.json`
- `02_FIELD_LAW_RECONSTRUCTION.json`
- `03_INDEPENDENT_HASH_RECONSTRUCTION.json`
- `04_HOSTILE_REVIEW.json`
- `05_EXECUTION_RECEIPT.json`
- `06_FINAL_DISPOSITION.json`

Allowed dispositions:

- `APPROVE_AT_DECLARED_GRAIN`
- `CHANGES_REQUIRED`
- `TYPED_RESIDUAL`
- `ESCALATE_WITH_COUNTEREXAMPLE`

Approval here is sufficient for HQ to adopt the exact successor spine. Do not create another review layer.

No implementation mutation. No self-adoption.

Terminal:
`AT07_SUCCESSOR_SPINE_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
