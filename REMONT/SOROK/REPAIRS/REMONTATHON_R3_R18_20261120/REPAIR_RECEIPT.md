# REMONTATHON R18 — P004 activity course authority, test-first sourcefree repair

- **Frozen parent**: R17 PR #1230, `6f2e98433822a4fb1246ff72c388b2e901c6ab7f`.
- **Owner**: `SEAM/ORACLE/UM_SOROK_ORGANISM_R3/um_sorok_organism/activity.py::record_activity_afterlife`.
- **First source**: `activity.py` identical SHA-1 Git blob `646ac2ba7a6d32ccb7325e0ff7694f72b71a142d` in frozen R17 and R16. Its `project_ids == selected IDs` check did not establish that all selected projects actually existed or contained the performed operation among their means. The recorder silently ignored incompatible selections; mixed selections caused an incomplete/false recorded purpose set.
- **Red court**: 8 new methods run against frozen R17 as reconstructed from exact R16 parent + Git-verified R17 patch; 3 FAIL (selected project means incompatible, unknown project ID, mixed valid+incompatible); 5 PASS. Red reproduced normal and `-O` before changing `activity.py`.
- **Repair**: check every actor-policy selected project exists exactly once and admits `own_action` in `means`, before mutating `operational_history` / `activity_history`; reject with `ACTIVITY_SELECTED_MEANS_CONTRADICTION`. Continue to accept valid single/multi-project courses, projectless actor policy, blocked attempts, and explicitly declared legacy direct-helper history.
- **Normal, `-O`, pytest**: 296/296 PASS each; pytest includes 32 subtests; cold archive and deterministic demo independently checked. Regression is a bounded sourcefree authorization check, not a theory of motive genesis.
- **Scope**: P004 remains PARTIAL. P012/P018 current engineering and P009 native privacy unpromoted. No duplicate R17 P018 repair or reassignment of SORACLE's construction. R17 author P018 fix awaiting independent receiving; R18 similarly requires independent review and Python 3.11 exact-head run.
- **Custody**: 73 P identities, 53 previously reviewed at bounded first-fault scope, 8 OPEN, 8 PARTIAL, 4 author-repaired review-pending P070–P073, T=0, E=6. No protected PRE-MAIN, native science/issuer, PROGRAMMA or paired CURRENT_PROGRESS receiving.

## Actual joined R17 full court and cold proof

- Reconstructed R17 exact Git source updates: `storage.py` `a89be36d3fe74b46f94a572be4db77941d7d9083`, `tests/test_remontathon_r4.py` `47d2d88b85ee573d313fd18a2346c2931b639664`, `tests/test_r17_source_preflight.py` `792a2546b12723e7e190fa32f50aab28b1703878`. All other inherited R16 Python files unchanged. R17 manifest agrees; 48 Python files become 49 with new R18 test file.
- 296/296 normal, 296/296 optimized and pytest 296 +32 subtests in fresh extracted archive.
- Two fresh demo processes `PYTHONHASHSEED=1` and `173` produced byte-identical output. Independent SQLite opens of both report `integrity_check=ok`, nine locally hash-chained events (not external cryptographic signatures), full last hash `bc47d6102f9cf402193131bd196cb697aa47930e53ff53cc6329ef3efed5b363`, and two source seals verified.
- Executed under Python 3.13.5; remote Python 3.11.3 at inherited R17 belongs to R17 only, not this candidate. Distinct engineering and scientific receiving still required.
