# FIABC-W3-I03 — Implementation / Diff Inventory

## Production code

### rawlsing_next/pre553_candidate_c_production_binding.py

New current production binding. Its bounded responsibilities are:

- freeze Candidate-C owner/policy identity without copying or replacing the immutable owner blob;
- freeze current LiTS-I and WVS7 source/projection identities;
- expose source-specific repository-builder-compatible Candidate-C entrypoints;
- route lawful current zero-accelerator realization through the existing source-backed C11 facade;
- bind a replayable Candidate-C physical/provenance receipt;
- reject source/projection drift and accelerator-scope creep.

It does not mint EmpiricalFact, DiscoveryAuthority, semantic authority, routing authority, question meaning, or source meaning. It does not alter I03 or I05 engines.

## Tests

### rawlsing_next/tests/test_pre553_candidate_c_production_binding.py

New focused hostile/identity tests. No existing test was changed.

## Return package

- WORKER_RETURNS/FIABC-W3-I03/00_RETURN.md
- WORKER_RETURNS/FIABC-W3-I03/01_IMPLEMENTATION_DIFF_INVENTORY.md
- WORKER_RETURNS/FIABC-W3-I03/02_TEST_AND_EXECUTION_PROTOCOL.md
- WORKER_RETURNS/FIABC-W3-I03/03_FANIN_BINDING_CONTRACT.md
- WORKER_RETURNS/FIABC-W3-I03/RETURN.json

## Explicit non-diffs

Not modified:

- HQ_HANDOFF/*
- Wave-2 decision ledgers
- historical EE-P2X continuation reducer
- frozen Candidate-A/B/C owner blobs
- rawlsing_next/pre553_source_backed_c11_facade.py
- I03 semantic executor
- I05 discovery executor
- CACC1/CACC2 owner implementation
- source/projection semantic authorities
