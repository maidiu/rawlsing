# BP3 owner handback — D1/D2/D3

## D1 — accepted original writer cutover / legacy API retirement

**Decision required:** the accepted C8 Journal owner must authorize installing the exclusive writer at every legally callable writer process and retiring/renaming the accepted `Journal.commit`/`admit_and_queue` routes.

**Tangible candidate:** `c8_exclusive_writer.py::install_exclusive_gate()` closes both class methods; `ExclusiveJournal` is the sole new append path. Exact old blob `331840768ce0b5f6f73e5e93094ca0d217ddaebf`; exact gate test `test_old_journal_commit_route_closed_preserves_acknowledged_bytes`; old writer counterexample in C8OI `evidence/legacy_writer_bypass_counterexample.json`.

**Not issued:** production cutover, old API deletion, sitecustomize/deployment, file permissions, migration of existing journals, process supervision, direct-filesystem prevention.

**Residual:** a process that does not load the candidate, raw OS writes, or a privileged actor can still erase bytes. D1 must close that with deployment and OS policy; code alone does not.

## D2 — independent key and monotonic anti-rollback authority

**Decision required:** a distinct key/anchor custodian must issue a production writer key, protected key store/HSM/KMS, monotonic anchor service and protected watermark, with rotation, revocation and offline policy.

**Tangible candidate:** `WriterKeyStore`, `KeyedCapability`, `KeyedMonotonicAnchor`, `ExclusiveJournal.verify_journal`; tests `test_forged_capability_refused`, `test_byte_valid_rollback_detected_by_external_anchor`, `test_anchor_offline_refused`, `test_anchor_rotated_key_refuses_old_watermark`, `test_key_leak_means_external_key_custody_boundary`, `test_key_store_inside_journal_directory_refused`.

**Not issued:** real key, HSM/KMS, external service, certificate, production anchor, revocation list, true independent custodian. The test key is `TEST_ONLY`, held apart from the journal only for the test fixture.

**Residual:** a leaked writer key can mint valid capabilities/proofs; an anchor log and its watermark rolled back together defeat detection; no power-failure guarantee. D2 must protect both stores and define compromise/rotation response.

## D3 — ADP019 real occurrence and performed E2

**Decision required:** the V3 External Admission Court must issue a real ADP019 admission receipt for an actual eligible occurrence, and the actual action owner must produce later performed E2. C9R may change its consumer contract independently.

**Tangible candidate:** `c9_event_ingress.receive_event` consumes the actual C8 receipt only with a proof verifier; it returns `ADP019_ADMISSION_RECEIPT_ABSENT`, `e2_performed=False`, no native actor. Tests `test_c9_ingress_reads_actual_c8_receipt_without_native_claim`, `test_c9_ingress_refuses_wrong_expected_digest`.

**Not issued:** ADP019 receipt, native event, actor, C9R binding, performed E2, C10/C12 continuation, C11 weld, Pyat authority. No fixture is called a native occurrence.

## Deployment/repair sequencing

1. D1 owner reviews gate/old-writer counterexample and authorizes a sourcefree staging cutover test.
2. D2 custodian provisions external key/anchor; replace the test key; exercise rotation/offline/revocation and rollback of both journal and anchor snapshots.
3. D3 owner supplies actual admission/action occurrence; bind C9 ingress to it; keep native E2 claim separate.
4. Only then can a production security claim be considered; this return is a sourcefree candidate, not production proof.
