> **Superseded execution order (2026-08-03):** Do not run the live respondent canaries yet. Section 86 now governs the next step: first implement the V550 shared respondent substrate and V550J no-database co-execution contract, then prove the structure with synthetic data. The live-canary instructions below remain the later empirical gate after Section 86 is complete.

# Exact continuation

1. Restore/checkout the Section 85 cumulative checkpoint.
2. Unpack the included nine-source canary archive.
3. Connect to the live respondent-level DDM database/view described in `LIVE_HOST_DATABASE_CONTRACT.md`.
4. Run `code/check_live_respondent_database.py`; do not continue unless all nine scopes and all configured variables pass.
5. Regenerate the bounded authority and confirm exact hashes.
6. Run the host-specific plan-only gate.
7. Run GSS 2010/US first.
8. If GSS passes, run Afrobarometer, Arab Barometer, Asian Barometer, EVS, Latinobarómetro, LiTS, South Asia, and WVS.
9. Preserve the first genuine V550J/V551J/V552J failure without broadening scope.
10. Repair only the concrete failed contract.
11. Freeze the completed nine-source empirical canary before considering a 35-wave J run.

Do not generate full canonical production files yet.
