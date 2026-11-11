# RAWLSING HQ CURRENT — SOURCE-SPLIT RUNNER ADMITTED

Status: `SOURCE_SPLIT_RUNNER_QUALIFIED__WAITING_FOR_BOTH_MACHINE_READINESS_RETURNS`

Checkpoint: `20260924T2247-0400`

Decision: `HQD-2026-09-24-095`

Canonical PRE-MAIN at seal:

`b6ca245549a1afb52d029f7700b067a4169d45f5`

Protected execution remains:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

Qualified source-split control:

`agent/vozhd-fiabc-source-split-alternate-runner-r1`

Exact qualified control head:

`1e701f10258831b6f453db8ad9d7ddbcba0bf247`

## Qualification

- 18/18 source-free tests PASS;
- zero source opens;
- zero source hash passes during qualification;
- zero decoder calls;
- zero candidate-process attempts;
- zero candidate outputs;
- no measured execution.

Exact qualified measured-orchestration blobs:

- source-local driver: `c6549d62db847699e5dd177eafa18c87cae7cbf2`;
- merge verifier: `51c254a3b254e84b71a6304a99eaef05ac49e919`;
- source-local launcher: `5ff364bef2ec9e315e9603877594a19834a8e39e`.

These blobs are unchanged at the published control head, so the dirty control worktree used while assembling the qualification packet does not create an exact-byte ambiguity.

## Measured-use law

The alternate runner is admitted in principle only as:

- LiTS-I A->B->C on the LiTS host;
- WVS7 A->B->C on the WVS host.

Host is nested within source.

Absolute LiTS-vs-WVS physical metrics are never treated as host-neutral.

The alternate runner does not execute or claim full six-cell S17 and does not authorize P2 synthesis.

## Remaining gate

Actual launch is blocked until BOTH machine bootstrap reports prove:

- protected execution head exactly `3d8f2ad6...`;
- source-split control head exactly `1e701f1...`;
- clean worktrees;
- pinned CPython 3.11.3 / pyreadstat 1.3.6 / pyarrow 25.0.1 / Darwin x86_64;
- canonical selected-source SHA;
- fresh persistent work root;
- automatic logout disabled;
- session/sleep persistence safe for multi-hour execution.

Once both returns are green, final dual-machine launch authorization can be issued without another runner code-qualification cycle.

P2 synthesis remains blocked.
