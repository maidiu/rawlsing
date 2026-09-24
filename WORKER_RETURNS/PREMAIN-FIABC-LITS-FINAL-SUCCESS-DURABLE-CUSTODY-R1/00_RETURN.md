# FIABC LiTS Final Success Durable Custody — R1

Terminal: **PASS__LITS_FINAL_SUCCESS_DURABLY_BANKED__HEAVY_CHECKPOINT_CONTENT_ADDRESSED__REMOTE_EVIDENCE_GREEN__READY_FOR_INDEPENDENT_ACCEPTANCE__NO_SOURCE__NO_CANDIDATES**

The successful candidate-neutral source-backed return is preserved under `source_retry_evidence/` and its complete 35-file tree has been copied to the persistent local payload at:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1`

The payload contains 3405790125 regular-file bytes. Every file has matching SHA-256 between the original `/private/tmp` tree and persistent copy. The checkpoint-v3 is 3404445161 bytes with SHA-256 `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`. The frozen oracle identity is `e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a`.

## Custody layout

- **Git-banked evidence/control plane:** this return, its custody manifest and payload file hash manifest, copy verification receipt, and selected source retry receipts/oracle.
- **Persistent local heavyweight checkpoint payload:** the complete source retry return tree at the path above. The 3.4 GB checkpoint is not in Git. Its SHA-256 binds the control plane to the local payload.

The LiTS DTA was not opened, hashed, or decoded for this custody commission. Candidate A/B/C, measured P2X, P3, architecture selection, FF02, and structural admission were not run.

The initial success commit passed remote readback; its receipt is remote_readback_receipt.json. The exact final remote branch tip and final post-push readback are recorded in the persistent local sidecar at /Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/remote_readback_receipt.json.

The protected remote Candidate A/B/C branch remains at `78caf7eb4396dd576cf478c860372b7e26455cd9`; this task does not update it.

Disposition: **ready for independent HQ acceptance / T3 fan-in; not FF02.**
