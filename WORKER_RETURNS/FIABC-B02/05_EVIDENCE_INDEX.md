# FIABC-B02 — EVIDENCE INDEX

Audit target unless otherwise noted:

- Repository: `maidiu/rawlsing`
- P2X branch: `agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`
- Current audited P2X tip: `617c9c9426db12a3c0f7fea6b68a582c10759553`
- FIABC base: `d474f8e3c9630c4bcbb10d6e8359b71ba5b3060d`

## P2X constitution and measured-return state

1. `WORKER_COMMISSIONS/EE-P2X/00_COMMISSION.md`
   - Defines the two-source A/B/C court, source/candidate order, candidate meanings, parity/oracle law, LiTS 50/77 workload, WVS 46-candidate workload, persistence/deletion/replay requirements, and no-ranking boundary.

2. `WORKER_RETURNS/EE-P2X/00_RETURN.md`
   - Primary governed record of the last live continuation.
   - Proves LiTS A/B runtime-authority import failure, LiTS-C frozen nonqualification, WVS A/B recursion failure, WVS-C preserved failure, and failed/nonterminal S17.
   - Explicitly says no candidate output, learned product, performance vector, ranking, or successful P2X terminal was admitted.

3. `WORKER_RETURNS/EE-P2X/14_LOCAL_ATTEMPT_20260919_RUNTIME_DEPENDENCY_BLOCKER.json`
   - Records exact local driver/backend command, exact source SHA verification, and earlier infrastructure-attempt context.

## Driver / reducer / evidence law

4. `rawlsing_next/ee_p2x_darwin_court_driver.py`
   - Hard-binds continuation-map identity, P2R1 seam identity, A/B/C owner blobs, source order, runtime gate, and ledger schemas.
   - `DriverServices.compose_p2r1_binding` is the convergence path for projection + runtime catalog + accepted candidate repository.
   - `load_exact_owner_module` proves immutable Git-object deployment rather than simple current-tree import.
   - `_preserve`, `_preserved_wvs_c`, `_backend_terminal`, and `StageLedger` prove how historical and fresh evidence become live.

5. `WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json`
   - Exact stage-by-stage execute/preserve/skip law.
   - Direct references to historical P2X and P2R1 worker-return evidence.
   - Documents source/candidate prerequisites and WVS-C no-executable-path law.

6. `WORKER_RETURNS/EE-P2X/LOCAL_EXECUTOR_README.md`
   - States driver ledger is primary execution evidence.
   - States normalized receipt existence alone is not fresh execution evidence unless bound by the actual driver stage.
   - States LiTS-A first build / LiTS-B cacheless C11 are repetition-forbidden preserved evidence and WVS-C is not executed.

7. `WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json`
   - Machine-readable driver-to-ledger-to-normalized-receipt binding law and required evidence-artifact roles.

## Current backend and PRE553 execution seam

8. `rawlsing_next/ee_p2x_darwin_stage_backend.py`
   - Concrete current stage backend.
   - `_decode` uses `pre553_physical_decoder`.
   - `_lits_projection` consumes historical AS2A/AS2B paths.
   - `_support_module` consumes P2R6S LiTS worker-return support.
   - `_wvs_docs` and `_wvs_materializer` consume P2R6S WVS worker-return packaging.
   - `_compose_lits`, `_compose_wvs`, `_bind`, `_i03`, `_i05` establish the call graph toward common execution.
   - `_s17` invokes the driver-bound final verifier.

9. `rawlsing_next/pre553_carrier_execution.py`
   - Accepted P2R1 carrier-neutral C11 -> I03/I05 seam.
   - Materializes canonical PRE553 objects from full exact preimages, resolves exact refs, binds governed projection/repository, and performs no semantic inference/defaulting.

10. `rawlsing_next/pre553_runtime_authority.py` at tip `617c9c9426db12a3c0f7fea6b68a582c10759553`
    - Current successor runtime-authority contract module.
    - Compared against the earlier live-run `ModuleNotFoundError` to distinguish repository survival from live court consumption.

11. Commit `617c9c9426db12a3c0f7fea6b68a582c10759553` — `EE-P2X: fan in adopted R6U R6V R6W runtime and reconciliation repairs`
    - Adds the runtime-authority module and post-run WVS recursion/reconciliation changes.
    - Establishes chronology: these successor resources are later than the live failures recorded in `00_RETURN.md`.

## Worker-return runtime packages / historical fan-in

12. `WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py`
    - Imports current `Pre553RuntimeAuthoritySet` / runtime context.
    - Materializes the exact LiTS 50/77 runtime package.
    - Hard-binds historical D02 frontier authority, F02 selector closure, B6 query input, Node4A support, AS3R3 runtime producer/contract, R6N proof, P2R1 identities, accepted owner identities, and HQ binding registry.

13. `WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json`
    - Backend's direct WVS runtime catalog/Lock2 package input.

14. `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`
    - Backend's direct WVS projection materializer.

15. Historical LiTS paths named in the backend:
    - `.../banked_as2b/run_as2b_lits1_mechanical_certification.py`
    - `.../banked_as2a/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv`
    - `.../banked_as2a/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json`
    - exact historical commit `3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`.

16. Candidate owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
    - A: `rawlsing_next/pre553_r5_source_backed_adapter.py`
    - B: `rawlsing_next/pre553_source_backed_c11_facade.py`
    - C: `rawlsing_next/pre553_route_c_accelerators.py`
    - Driver extracts exact blobs from this commit into a private work-root module path.

17. P2R1 accepted evidence commit `9511f44728a8469d685463ec0fc880864c9187de`
    - `WORKER_RETURNS/EE-P2R1/08_EXACT_RUNTIME_OBJECT_CATALOG_PREIMAGE_RECEIPT.json`
    - `WORKER_RETURNS/EE-P2R1/09_CARRIER_NEUTRAL_I03_I05_RUNNER_QUALIFICATION_RECEIPT.json`
    - `WORKER_RETURNS/EE-P2R1/10_ABC_ADAPTER_QUALIFICATION_MATRIX.json`
    - `WORKER_RETURNS/EE-P2R1/11_LITS_C_REAL_DETERMINANT_19_ATOM_BINDING_RECEIPT.json`
    - `WORKER_RETURNS/EE-P2R1/12_WVS_C_ZERO_ACCELERATOR_ADJUDICATION.json`
    - Qualification alone is not counted as fresh P2X execution.

## Evidence interpretation law used by FIABC-B02

- `accepted authority` is not collapsed into `current runtime package`;
- `current runtime package` is not collapsed into `live court consumption`;
- `historical receipt intentionally rebound by the driver` **is** live consumption of historical evidence;
- `current code present after the recorded run` is **not** live consumption until a governed post-fan-in execution receipt proves it;
- `candidate-local governed nonqualification` is preserved as a negative state and is not rewritten as generic missing functionality.
