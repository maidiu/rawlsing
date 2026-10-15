# Reproduction

Use an authorized local Python 3.11 environment with pytest and the repository's pinned Git objects available. No SAV/DTA or real-source access is needed. All files are created inside this return. The runtime and exact frozen predecessor material are intentionally untracked; `stage.py` rebuilds them from the pinned commits, checks original Git blob/NUL preimages and provisions the TEST_ONLY owner before requests. It refuses an existing runtime. The exact retained HQ282 worker is staged at the unchanged historical HQ280 test-selected path, with an explicit compatibility alias record.

From the repository root, let `R` be this return directory. Run `python3 "$R/repro/stage.py"` once in a fresh checkout. If a pinned object is unavailable, fetch its source branch/commit named by `source_selector.json` and the passport first. Staging changes no tracked predecessor source.

Execute `python3 "$R/repro/run.py" MODE` for these modes in order:

1. `pv2_33`, `v2k_24`, `pv_21`, `owners_111`: unchanged original suites; expect 33/24/21/111 passes. The owner mode records child import/callee telemetry.
2. `historical_cold`, `pv2i_historical`: actual predecessor cold/journal attacks, then all 48 unchanged independent guards; expect exit 1 and exactly 26 PASS / 22 FAIL.
3. `pv3_probe`, `cold`, `cold_receipt_attack`, `checkpoint_attack`, `audit_receipts`, `reconstruct`: actual repaired sources, two-process replay, journal/checkpoint attacks, accepted receipt verification and native-risk arithmetic reconstruction.
4. `pv3`: 28 additional repair guards, including persisted selective current authorization and offline HOLD; expect exit 0.
5. `pv2i_adapter`: same 48 frozen guards through the explicit interface adapter; expect exit 1 and 47 PASS / 1 FAIL. The remaining label assertion is preserved; a separate guard denies generic semantics instead of changing the owner.
6. `check_reproducibility`: bootstrap into a new nested owned directory without existing runtime/frozen inputs, then run the 28 new guards.
7. `finalize`: verify original staged sources, physical imports, all suite counts and observed per-case dispositions; rebuild the closure/passport evidence without touching the independent oracle.

Cold/probe/check-reproduction directories are single-use evidence roots. To repeat them, use a fresh checkout/runtime rather than reusing prior ledgers. Read source-integrity and clean-bootstrap outputs separately from scientific acceptance results. Raw nonzero historical/label exits are intentionally retained, not hidden by a wrapper success code.

The deployed request object is `deployment.api`. Its current decision store is fixed at trusted composition, outside caller ledger/register arguments. `FixtureOwnerControl` and `provision_owner.py` belong to trusted fixture administration. Test-profile selection and legacy revoked-snapshot translation are explicit harness controls and are absent from ordinary request signatures. Restoring an old request snapshot never invokes provisioning or regranting.
