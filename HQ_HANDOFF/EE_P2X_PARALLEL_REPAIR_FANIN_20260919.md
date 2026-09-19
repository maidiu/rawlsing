# EE-P2X PARALLEL REPAIR SELECTIVE FAN-IN — 2026-09-19

Status: `R6U_R6V_R6W_R6X_FANNED_IN__P2X_HELD_PENDING_EXACT_LOCAL_RECONCILIATION`

Decision:

`HQD-2026-09-19-084`

Semantic PRE-MAIN remains:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

## P2X integration

Branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

Prior held head:

`ae8b1db9d8c3288e002950ac01123c70f3138320`

Selective fan-in commit:

`617c9c9426db12a3c0f7fea6b68a582c10759553`

Parent:

`ae8b1db9d8c3288e002950ac01123c70f3138320`

Exact diff count:

`18 files`

No worker branch merge was performed.

No worker tests, PR scaffolding, transient court specs, or worker-return evidence were fanned in except the exact R6X reconciler executable required for local recovery.

## R6U exact adopted substrate fanned in

- `rawlsing_next/_pre553_query_common.py` → `938a6b03a63dd34ef4f0f63655ed8f11f65c5d92`
- `rawlsing_next/_pre553_query_eval.py` → `128b31fa60c2650d8c7af30f1f4b1d1470acd2b6`
- `rawlsing_next/_pre553_query_predicate.py` → `edc943ca6690ac73f24492f3d01ad9ee17f70f21`
- `rawlsing_next/pre553_discovery_exact.py` → `c7380774e8a1959da5ed8c6f23c2fc3cf99ad18d`
- `rawlsing_next/pre553_empirical_query.py` → `482778348d6b450f46985c2161af32f2961d8384`
- `rawlsing_next/pre553_runtime_authority.py` → `2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`
- `rawlsing_next/pre553_runtime_composition.py` → `3753c183ddb25b1b0eb0ce84db1868f39f50d3fa`
- `rawlsing_next/pre553_runtime_context.py` → `3c26c77892395a4825b377b740e37df7ea1148d4`
- five exact adopted R4A fixtures:
  `e49b33417ea1f57e5eacb557c173507a118e11de`,
  `490434c1fc87decb97d187e6185e1848045dd9c5`,
  `a18fd79609f080062b93dfe0e2bab8e9bf865af3`,
  `5000020fa6554be9c2ad2ab418b6f5269b59d69a`,
  `e19d076e2d2b0ecbf7ccacba5e23dd185ce43cfc`.

## R6V repaired WVS materializer fanned in

`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`

blob:

`11b28416aac5a4899706150721f2f8ac8bb6ee43`

## R6W S17 repair fanned in

Driver:

`rawlsing_next/ee_p2x_darwin_court_driver.py`

blob:

`02ca7cc9f5bf8665de712980a05fdcc059b93331`

Backend:

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

blob:

`b223d309b5f5fa45389badec719ce2882e672cca`

Strict driver-binding packet:

`WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json`

blob:

`24311d54ca92a3255dcbbf05e7bc2b8d3ef19cb0`

Driver-bound verifier remains unchanged at:

`da8f3434f791c9f6495238b28817de4b3e328ad3`

## R6X local reconciler fanned in

`WORKER_RETURNS/EE-P2R6X/03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py`

blob:

`12836e591be9ed0aa4d46436deacebde038d9de0`

## Hold / next lawful action

P2X measured execution remains **HELD**.

The local stopped work root must still contain exact stopped ledger SHA-256:

`7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671`

The only next authorized local action is:

`EXACT_R6X_STOPPED_LEDGER_RECONCILIATION_ONLY`

Execution surface:

`LOCAL-MACHINE CODEX`

Maximum intelligence:

`LUNA`

Library access:

`NO`

No source carrier path is needed or authorized for reconciliation.

The reconciler must be run from exact P2X head `617c9c9426db12a3c0f7fea6b68a582c10759553` against the exact existing stopped work root.

Required command shape:

`python WORKER_RETURNS/EE-P2R6X/03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py --work-root <EXACT_EXISTING_P2X_WORK_ROOT> --repo-root <EXACT_REPOSITORY_ROOT>`

The resulting:

`<work-root>/ee_p2r6x_reconciliation_receipt.json`

must be returned to HQ before measured P2X may resume.

Do not run the P2X driver yet.

Terminal:

`P2X_REPAIRS_FANNED_IN__LOCAL_RECONCILIATION_ONLY_AUTHORIZED__MEASURED_P2X_HELD`
