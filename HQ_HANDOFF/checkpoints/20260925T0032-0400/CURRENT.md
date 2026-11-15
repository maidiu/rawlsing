# RAWLSING HQ CURRENT — SOURCE-SPLIT PANDAS RUNTIME REPAIR PROMOTED

Status: `SOURCE_SPLIT_RUNTIME_REPAIRED__WAITING_FOR_FRESH_MACHINE_PREPARATION_RETURNS`

Checkpoint: `20260925T0032-0400`

Decision: `HQD-2026-09-25-097`

PRE-MAIN at seal:

`cc384462e3732f290de187453af38886d3b5cf6a`

Protected execution:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

Canonical source-split control:

`4f0ee6bbc7e3387fb1c71837c1ae8bea658f64a2`

Exact tested implementation:

`5c7aef690e4d04ebc1676d3448c0314a5c4c2d89`

## Qualified runtime

- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- pandas 2.3.1
- numpy 2.3.2
- Darwin x86_64

19/19 source-free qualification tests PASS.

## Preserved prior attempts

- prior WVS source-local measured root: immutable, never resume;
- blocked LiTS pre-candidate root: immutable, never reuse.

WVS A/B/C terminal labels from the prior attempt are void as candidate evidence because all three were masked by the same missing-pandas runtime defect.

## Next action

Prepare both machines for one fresh retry:

1. sync canonical source-split control to `4f0ee6...`;
2. exact expanded runtime on both machines;
3. fresh clean protected execution checkout at `3d8f2ad6...`;
4. brand-new empty persistent source-local work root;
5. retain existing session-safety controls;
6. report readiness to HQ.

Explicit measured launch remains blocked until both preparation returns are green.
