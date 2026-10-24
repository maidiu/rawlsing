# R91 R04_JOINED R3 contract — restored native output identity

Status: frozen before R3 code commit. Sole repair: cached completed outputs must
retain native identity. Prior partial restart/pin/manifest evidence preserved.

## Output custody

Checkpoint entries store full identity-bearing output material per completed
unit:

- unary/query: exact `query_ref`, fact preimages, `source_scope_mode`, exact
  `release_refs`;
- discovery: contract/authority/grammar/evaluated-frontier/replay refs,
  coverage/counts, receipt preimages, exact fact refs/facts, executed
  predicate/query refs and valid-empty.

Cold restore reconstructs actual native `QueryExecutionResult` objects for query
outputs and a frozen `RetainedDiscoveryResultView` for discovery output with
all identity fields and validated fact/receipt ordering/closure. Mutable
facts-only namespaces are removed. Partial prior outputs are restored through
the same checked constructors and fed to the existing Batch resume path.

## Preserved

Original external checkpoint pin, current-grant/source checks, original manifest
units, partial multi-unit prefix resume, completed-unit non-rerun, pending native
execution, exact output refs. No trust-boundary widening.

## Limits

No R05+, original science, CI/prod/N11/N12/Sorok/J52/W52; no new lineage or
exactly-once service. Local trusted-host TEST_ONLY only.
