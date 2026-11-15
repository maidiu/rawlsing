# RAWLSING HQ CHECKPOINT — 20260919T1205-0400

Status: `R6U_R6V_R6W_R6X_ADOPTED__SELECTIVE_P2X_FANIN_READY__P2X_HELD_PENDING_LOCAL_RECONCILIATION`

Semantic PRE-MAIN:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

Controlling decisions:

- `HQD-2026-09-19-081`
- `HQD-2026-09-19-082`
- `HQD-2026-09-19-083`

Adoption record:

`HQ_HANDOFF/EE_P2R6U_R6V_R6W_R6X_PASS_ADOPTION_20260919.md`

## Adopted worker returns

- R6U final head: `85c1c00c4dfa0b63d029dc3d20ec865f4d3ed3e8`
- R6V final head: `75fcb21893919208423edadd24a2b43adf71c099`
- R6W final head: `c7cb149a11795d6b9651a4303258534058fd027f`
- R6X final head: `689995c798fece3c36d56905e4aaa67957ce8d79`

## Held P2X

Branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Held pre-fan-in head:

`ae8b1db9d8c3288e002950ac01123c70f3138320`

Stopped local ledger SHA-256:

`7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671`

## Selective fan-in set

R6U exact adopted R6A substrate:
13 exact runtime/query/fixture blobs.

R6V:
- WVS materializer `11b28416aac5a4899706150721f2f8ac8bb6ee43`

R6W:
- driver `02ca7cc9f5bf8665de712980a05fdcc059b93331`
- backend `b223d309b5f5fa45389badec719ce2882e672cca`
- strict driver binding `24311d54ca92a3255dcbbf05e7bc2b8d3ef19cb0`
- verifier remains unchanged at `da8f3434f791c9f6495238b28817de4b3e328ad3`

R6X:
- local reconciler `12836e591be9ed0aa4d46436deacebde038d9de0`

P2X remains held after fan-in until the exact stopped work root is reconciled locally and the receipt is returned to HQ.

Terminal:

`PARALLEL_REPAIRS_ADOPTED__SELECTIVE_FANIN_READY__LOCAL_RECONCILIATION_REQUIRED`
