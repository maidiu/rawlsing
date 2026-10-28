# P05 mandatory existing-code check

Before implementing P05 B02–B07, inspect `agent/rabochii-pyat-hq282-p01-v2-durable-consumer-integration-r1@3f91dc22d2eb`, reviewed at `73d45f3ac6a50fbee6666ad3a5023840f01ef196`.

Existing sourcefree `rawlsing_next` files: `pre553_batch_durable_checkpoint_candidate.py`, `pre553_governed_batch_checkpoint_integration_candidate.py`, `pre553_original_workload_binder_candidate.py`, `pre553_original_workload_contract_v2_candidate.py`, `pre553_original_workload_v2_verifier_candidate.py`, `pre553_v2_durable_consumer_integration_candidate.py`.

The return `WORKER_RETURNS/PYAT-HQ282-P01-V2-DURABLE-CONSUMER-INTEGRATION-R1/00_RETURN.md` reports 3 sourcefree I03/I05 operations, 3 real fixture Field Forge consumer outputs, 25 integrated passes, and 169 ordinary tests with 6 explicit historical skips. Independent review reports 22 semantic checks and no sourcefree blocker at the tested SHA; the read-only reviewer could not independently repeat filesystem recovery.

**Required:** compare existing `open_session`, `run_to_completion`, `recover`, `admit_saved_receipts` and `run_integrated` against selected SRC04 `native_streaming`, including source/authority/run identity, complete cells, torn JSONL, duplicate/conflict and replay. Port compatible operational receipt code instead of rebuilding. A separate P01 I02-certified physical C11 journal is still needed.

**Not proved:** an original SRC04 source-qualified Lane D consumer, repair of the four original adapter resume defects, or production adoption. No automatic merge, source grant or new worker.
