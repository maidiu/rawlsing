# RA-D test source and logs

All logs are sanitized: user-home, worktree, scratch, G18, JOIN-E, language and V3 roots are placeholders. SHA-256 source identities and observed values are preserved.

## Scripts

| File | Purpose |
|---|---|
| `import_manifest.py` | Imports the S52 cut, records actual module `__file__`/SHA-256 and external roots. Run from the S52 package dir. |
| `probe_execution.py` | Main sourcefree probe: S51 object/hypothesis/offer/access/relevance, S52 candidate, S39 receipt, source cut, controlled material chain, later material consumer, S48 hold, S39 controls. |
| `probe_s48_hold.py` | S48 fake-runner source-owner HOLD and SCI05 HOLD probe. |
| `probe_s52_verifier_control.py` | S52 tamper control with and without a later unrelated episode. |
| `test_s52_postcondition_fault_ra_d.py` | Independent S52 hostile diagnostic; asserts the correct invariant and exits 0 only when the defect is reproduced. |

The scripts expect the extracted archive at `TEST_SOURCE_AND_LOGS/isolated_archive_s52c821`. That archive was removed after execution to avoid committing a copied source tree. The archive was verified byte-for-byte against the S52 and S50 commits before removal (`archive_vs_s52_commit.json`).

## Results

| File | Result |
|---|---|
| `import_manifest.json` | Module origins and hashes. |
| `causal_probe_result.json` | Main causal probe values. |
| `s48_probe_result.json` | Source-owner/SCI05 holds. |
| `s52_verifier_control.json` | `no note -> false`; `later note -> true`. |
| `s52_hostile_run.log` | S52 defect reproduced, tampered cash 999 accepted. |
| `s52_run_stdout.log` | S52 entrypoint output. |
| `s51_run_stdout.log` | S51 standalone entrypoint: `SOURCE_OWNER_HOLD` / `OPEN_CHOICE_SET`. |
| `s50_run_stdout.log` | V3/PFF fixture output; actual-root hold. |
| `SOROK-...-S44..._run.log` | S44 entrypoint. |
| `SOROK-...-S45..._run.log` | S45 entrypoint. |
| `S47_run.log` | S47 interval conditioning and source faults. |
| `*_pytest.log`, `s52_pytest_stdout.log` | Focused suite results. |
| `source_blob_comparison.json` | Accepted-cut vs S52-cut blob comparison (110 files, 5 deltas). |
| `archive_vs_s52_commit.json` | Extracted archive vs S52 commit (183 `.py`, 0 mismatches). |
| `environment_probe.txt` | Host/Python/pytest/Git versions. |

No provider call, raw data, accepted-source edit or native grant is present in this directory.
