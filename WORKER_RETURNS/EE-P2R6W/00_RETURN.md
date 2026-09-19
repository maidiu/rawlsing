# EE-P2R6W — governed return

## Disposition

PASS.

`EE_P2R6W_PASS__S17_PRETERMINAL_VERIFIER_ORDERING_AND_COURT_SCOPE_FAILURE_PATH_REPAIRED__READY_FOR_HQ_SELECTIVE_FANIN`

## HQ authority

Live HQ was resolved before implementation and rechecked before sealing.

- checkpoint: `20260919T0330-0400`
- immutable handoff: `9540aba11d40fc749ffa59827e871c1ba00e7ec6`
- semantic PRE-MAIN: `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`
- controlling decisions: `HQD-2026-09-19-081`, `HQD-2026-09-19-082`
- commissioned R6W tip: `c67f0a5c1461e90e72988286fba3dad4d521ecf8`
- held P2X head: `ae8b1db9d8c3288e002950ac01123c70f3138320`

P2X remained held and was not moved.

## Production repair

### Driver

`rawlsing_next/ee_p2x_darwin_court_driver.py`

- prior Git blob: `c3a368270f6f7a6f613efb78e31972e64a092c88`
- repaired Git blob: `02ca7cc9f5bf8665de712980a05fdcc059b93331`

The repaired S17 order is now exactly:

`all S00-S16 terminal -> _final_ready -> S17 absent -> backend S17/verifier -> backend result -> driver terminalizes S17`

The driver no longer writes a RUNNING S17 entry before invoking the backend. A legacy RUNNING S17 left by the pre-repair ordering is removable only when it is an empty preterminal placeholder: any receipt, receipt hash, output artifact, or terminal state makes deletion fail closed.

Non-S17 READY stages retain their previous BEGIN-before-backend lifecycle.

### Production backend

`rawlsing_next/ee_p2x_darwin_stage_backend.py`

- prior Git blob: `fb30167ebc060939e17eb15c71b93c000033eb4f`
- repaired Git blob: `b223d309b5f5fa45389badec719ce2882e672cca`

The S17 handler still targets the exact existing driver-bound verifier. The repair is confined to failure normalization/serialization:

- synthetic `COURT/ALL` common-court failure no longer calls the candidate-cell serializer;
- no `order.index("COURT/ALL")` path exists in that failure route;
- court failure evidence is candidate-neutral with `candidate: null`;
- exact kind remains `COMMON_COURT_AUTHORITY_FAILURE`;
- exact scope remains `COURT_UNTIL_RESUME`;
- the frozen verifier evidence-role contract remains `cell_receipt + failure_receipt`, with the former role carrying an explicitly typed court-scope receipt rather than a fake candidate cell;
- any ordinary `BackendStop` raised at COURT scope is normalized to the common-court path, never candidate-local S17 failure.

Ordinary source/candidate failure serialization is unchanged.

## Verifier integrity

The verifier itself was not changed:

`WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py`

Git blob remains exactly:

`da8f3434f791c9f6495238b28817de4b3e328ad3`

Its strict binding was updated only so the verifier checks the repaired driver bytes rather than the obsolete driver blob:

- binding prior blob: `50c9a53d0d77131df7c619114b476afce0b0bb0f`
- binding repaired blob: `24311d54ca92a3255dcbbf05e7bc2b8d3ef19cb0`
- bound repaired driver: `02ca7cc9f5bf8665de712980a05fdcc059b93331`

No verifier condition was removed or weakened.

## Governed Browser qualification

Transient PR `#418` was opened only to trigger the governed Browser court against held P2X base `ae8b1db9...`; it is closed unmerged.

Final qualified semantic candidate:

`a2013f8a7ff060700c63102b892db967f31bd242`

Final execution head:

`da52a5b4c54fe9785232c375e25613ec416d7979`

Governed run:

- run: `35430429640`
- job: `105863882747`
- bounded repair tests: **9 passed**
- protocol self-tests: **20 passed**
- artifact: `10580941421`
- artifact name: `rabochii-court-receipt-35430429640`
- artifact digest: `sha256:85acd4af110c1524d63757fb795a75b09612d2fc37ac88da2ca410737c23df0c`

The final court includes a direct bounded invocation of the actual production `_s17` handler, with only the subprocess result stubbed, and proves that the handler targets the exact unchanged verifier while S17 is absent; the driver then terminalizes S17 after PASS.

The first court attempt exposed only a qualification-fixture bug (`FakeLedger.data` absent): 7 tests passed / 1 fixture test failed. Production code was not changed in response. The corrected court passed 8/8, then the proof was deliberately strengthened with the real `_s17` handler test and the final court passed 9/9.

Transient `.rabochii/court_spec.json` was restored to absence at:

`a70ecba6119f460ed71ac72c295f6c3f33e1641e`

## Boundaries

No Library access. No LiTS/WVS carrier access. No source decode/open. No empirical outcome access. No measured P2X execution. No performance measurement. No ranking or selection. No Candidate-C repair. No MAIN or semantic PRE-MAIN movement. No P2X branch movement.

## Wake

HQ adjudication/selective fan-in only.

Fan in the repaired driver blob `02ca7cc9...`, repaired backend blob `b223d309...`, and strict binding blob `24311d54...` while preserving verifier blob `da8f3434...`; then seal the P2X resume authority under current HQ law.

Return to HQ.
