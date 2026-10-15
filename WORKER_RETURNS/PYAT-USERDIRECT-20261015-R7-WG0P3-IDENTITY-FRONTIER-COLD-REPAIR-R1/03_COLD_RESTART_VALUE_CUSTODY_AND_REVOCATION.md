# Cold-Process Checkpoint/Resume, Value Custody and Revocation

## Cold Checkpoint Design

`ColdCheckpoint` stores:
- `plan_freeze_hash`: plan identity
- `completed_units`: unit → op_id mapping
- `fact_custody_snapshot`: immutable fact store with content hashes
- `source_editions`: release → source edition mapping
- `grant_state`: current permission state

`checkpoint_hash` = SHA-256 of all fields. `verify_checkpoint` validates:
1. Checkpoint hash matches computed hash
2. Plan freeze hash matches current plan
3. Source editions match current releases
4. Fact custody hashes match content

## Cold Restart Flow

1. Run 1 unit → durable checkpoint with fact custody snapshot
2. Exit process
3. Load checkpoint in fresh process
4. `restore_from_checkpoint` validates hashes and restores fact custody
5. Resume remaining units
6. Serve all results after full coverage

## Value Custody

`FactCustody` is an immutable content-addressed store:
- `store(key, data)`: computes SHA-256 of content, stores with hash
- `read(key)`: verifies hash matches before returning; raises `IdentityError` if tampered
- `snapshot()`: returns copy with hashes for checkpointing
- `restore(snapshot)`: restores facts and verifies all hashes

No mutable `fact_registry[ref]` posthoc denominator injection possible.

## Revocation

`consumer_effects` checks `plan.source_issuer_grant["grant"]`:
- `GRANTED_FIXTURE`: results served
- `WITHDRAWN`: `RevocationError` raised; previously issued results remain immutable historical records but cannot be newly served

## Forgery Detection

- Forged checkpoint: hash mismatch detected
- Stale checkpoint: plan freeze hash mismatch detected
- Altered fact payload: content hash mismatch detected
- Revoked grant: `RevocationError` at consumer read

## Tests

- `test_cold_checkpoint_resume_restores_facts`: 1 unit → checkpoint → fresh process → restore → resume → serve all
- `test_forged_checkpoint_rejected`: altered fact data rejected
- `test_stale_checkpoint_rejected`: different plan hash rejected
- `test_cold_payload_forgery_rejected`: forged payload hash rejected
- `test_late_revocation_blocks_current_read`: WITHDRAWN blocks current read
- `test_fact_payload_is_bound_at_read`: tampered fact detected at read
