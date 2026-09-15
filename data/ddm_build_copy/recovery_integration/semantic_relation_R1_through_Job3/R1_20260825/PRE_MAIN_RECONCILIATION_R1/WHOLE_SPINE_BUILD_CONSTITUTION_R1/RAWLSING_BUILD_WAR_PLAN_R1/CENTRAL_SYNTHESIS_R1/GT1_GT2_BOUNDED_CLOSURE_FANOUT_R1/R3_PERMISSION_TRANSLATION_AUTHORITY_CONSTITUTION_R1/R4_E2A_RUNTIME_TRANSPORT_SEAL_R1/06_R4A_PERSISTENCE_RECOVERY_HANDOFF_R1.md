# R4A PERSISTENCE-ONLY RECOVERY HANDOFF R1

Repository:

`maidiu/rawlsing`

Worker branch:

`agent/rabochii-gt12-r4a-current-genuine-gt2-execution-r2`

Expected current branch HEAD before recovery:

`a6e587e2a99bc949155eb677611d78f5649510b6`

This handoff is instruction evidence only. Do not make the instruction commit working ancestry.

Profile:

`CLOSURE_ONLY`

Submode:

`PERSISTENCE_RECOVERY`

## Frozen recovered facts

The immediately preceding R4A execution reported genuine completion of:

`MATERIALIZE -> HASH_VERIFY -> PROJECT -> VALIDATE -> INDEX -> EXECUTE -> EXTRACT -> SEAL_INPUT`

with exact current identities:

- predicate:
  `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- query:
  `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- fact:
  `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`
- replay:
  `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`
- state:
  `SUPPORTED`
- denominator:
  `19210`
- order:
  `Q86B -> Q86A`

Frozen A1:
- release:
  `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- replay manifest:
  `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`

Reported prepared transport:
- manifest SHA-256:
  `8eba455707a78c71bc846e8b91e528c3ed336a0d09ced8e69eec5b01a6ecaacd`
- combined opaque event payload SHA-256:
  `2fa09161ad457750dc3c80865811731908bdeb1c82dfdd36e958f178ede041b1`
- opaque event material:
  38,420 RespondentEvent hashes / 1,229,440 bytes / ten shards
- reconstructed provenance closure:
  76,843 refs

Authorized exact repair blobs:
- `rawlsing_next/_pre553_query_eval.py` Git blob:
  `e2d91984541df7c692a1b2f32370500838a2a000`
- `rawlsing_next/tests/test_pre553_i03_scale_equivalence_repair.py` Git blob:
  `14e53b01305d3b91535608845de9fe4941237de2`

Intended evidence path:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/`

Expected prepared files:
- `00_RETURN.md`
- `01_EXECUTION_EVIDENCE.json`
- `02_CONSTRUCTOR_COMPLETE_MANIFEST.json`
- `03_LIVENESS.jsonl`
- `04_SEAL_INPUT.json`
- `payload/event_ref_hashes.0000.bin`
  through
  `payload/event_ref_hashes.0009.bin`

## Mission

This turn is NOT authorized to rerun R4A.

### First legal action

Inspect the already-prepared local workspace from the preceding execution.

Look first for the exact prepared evidence directory/files and the reported local execution workspace under `/mnt/data`.

If the prepared payload exists:

1. verify the manifest SHA-256 is exactly
   `8eba455707a78c71bc846e8b91e528c3ed336a0d09ced8e69eec5b01a6ecaacd`;
2. verify the combined opaque event payload SHA-256 is exactly
   `2fa09161ad457750dc3c80865811731908bdeb1c82dfdd36e958f178ede041b1`;
3. verify the ten expected shards are complete;
4. verify the evidence files record the exact current identities above;
5. verify the worker branch still has expected HEAD
   `a6e587e2a99bc949155eb677611d78f5649510b6`.

Then PERSIST BEFORE DOING ANYTHING ELSE.

### Atomic persistence law

Do not upload/commit fifteen files serially one by one if the low-level Git object API is available.

Prefer:

1. reuse the exact existing repair/test Git blobs named above;
2. create blobs for the prepared evidence/manifest/shards;
3. create one tree based on the current branch tree;
4. create one commit with parent
   `a6e587e2a99bc949155eb677611d78f5649510b6`;
5. atomically fast-forward
   `agent/rabochii-gt12-r4a-current-genuine-gt2-execution-r2`
   to that commit;
6. immediately re-read branch HEAD and verify every intended path/blob exists.

The persistence commit may contain only:
- the exact bounded PRE553 repair;
- its exact focused hostile test;
- the bounded R4A execution/evidence/payload path above.

No old temporary workflow, PR, audit, or forensic artifacts.

### Absolutely forbidden in this recovery turn

Do NOT:
- rematerialize FFP014/FFP017;
- rerun PROJECT;
- rerun C11 validation;
- rebuild the release index;
- rerun I03 empirical evaluation;
- reconstruct the ordinary EmpiricalFact again;
- profile the constructor;
- re-extract the payload;
- execute E2B;
- redesign the transport format;
- create another workflow/PR merely to persist files.

```
PREPARED_PAYLOAD_AVAILABLE => PERSIST_BEFORE_REEXECUTE
```

If the prepared local payload is genuinely absent or hash-incompatible, STOP.

Return:

`BLOCKED_MATERIAL_UNAVAILABLE__R4A_PREPARED_EXECUTION_PAYLOAD_NOT_RECOVERABLE__NEW_REAL_EXECUTION_AUTHORITY_REQUIRED`

Do not silently authorize another expensive R4A run in this persistence-recovery turn.

## Terminal

After successful atomic persistence, verify the committed return/evidence supports all original Worker A terminal claims.

Only then issue:

`PASS__GT12_R4A_CURRENT_GT2_EXECUTED__ACTUAL_QUERY_FACT_OBTAINED__CONSTRUCTOR_COMPLETE_PAYLOAD_EXTRACTED`

Return:
- exact new terminal SHA;
- exact committed evidence root;
- exact manifest hash;
- exact event payload hash;
- confirmation that no expensive execution stage was rerun in this persistence-only recovery.
