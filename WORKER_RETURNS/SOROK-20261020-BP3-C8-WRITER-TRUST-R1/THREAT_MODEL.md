# BP3 threat model

## Assets

- Acknowledged C8 journal state and occurrence IDs.
- Writer version/acknowledged prefix.
- Append proof and external monotonic watermark.
- The accepted read-only consumer's actual readset and C9 ingress receipt.

## Adversaries / tests

| Adversary | Candidate response | Residual |
|---|---|---|
| Old `Journal.commit` caller | `LegacyWriterRouteClosed` | process not importing gate / raw OS |
| Old `Journal.admit_and_queue` caller | `LegacyWriterRouteClosed` | same |
| Stale writer | version CAS `StaleJournalConflict` | retry policy external |
| Forged capability | HMAC `CapabilityRefused` | leaked key |
| Unkeyed digest/bearer token | never accepted as auth; `KeyedProofInvalid` | none in candidate |
| Byte-valid rollback of journal+proof | anchor watermark `AnchorRollbackDetected` | anchor+watermark both rolled back |
| Anchor offline/invalid MAC/rotated key | `AnchorUnavailable` | custodian availability |
| Duplicate append | `DUPLICATE_NO_CHANGE` | none |
| Crash before rename | prior bytes preserved | FS/power assumptions |
| Crash after commit before proof | `verify_journal` refuses; unacknowledged | reconciliation not implemented |
| Raw filesystem write / OS delete | **not prevented** | D1 OS permissions |
| 2/3/5 concurrent writers | lock + CAS; no acknowledged loss in test | scheduler/FS beyond test |
| C9 ingress without proof verifier | `PROOF_VERIFIER_REQUIRED` | deployment must inject verifier |
| C9 ingress wrong state digest | `C8_STATE_DIGEST_MISMATCH` | none in candidate |

## Security claim

`TEST_ONLY_SOURCEFREE_CANDIDATE`: when the candidate is loaded and the test key/anchor are external, the old callable class writer is refused, and append/rollback proofs are keyed and anchored. This is not a production security proof. D1/D2/D3 are unissued.
