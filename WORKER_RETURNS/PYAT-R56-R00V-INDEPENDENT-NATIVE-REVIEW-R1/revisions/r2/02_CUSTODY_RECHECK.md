# Candidate custody recheck

## Gate behavior

PASS at scoped local policy grain. No gate defect from the original eight persists in the reviewer tests.

## Candidate manifest

`manifest.json` contains 27 file entries. Independent recomputation found two stale entries:

| File | Manifest recorded | Actual |
|---|---|---|
| `evidence/passport.json` | `e1663d7e4c23c32d5b995ce01bdb0cfb55928c875ca527646b2997eef85da076` | `fac1dc32f5d4e298494a83914391dc5271f21c2f0530ecf95f2da055055ddb8b` |
| `evidence/manifest_supersession.json` | `da2d80724048dcad9f4895930972235fd00f70f2430a01617c7bf2ab66bf87eb` | `70177f0fd11a3178c0bb9839d7f993a686924082dcea093b8b9ab502bfe99092` |

These files were written after the manifest scan. The candidate `00_RETURN.md` therefore overstates manifest exactness.

## Candidate SHA256SUMS

Two entries use `../../` paths that do not resolve from the candidate root, its `evidence/` directory, or the repository root:

- `../../CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py`
- `../../tests/universal_execution_oracle/test_r00e_r2_reviewer_regressions.py`

Their recorded hashes are correct for the files, but the paths are not independently resolvable as written. The candidate manifest contains correct root-relative code/test paths, so the evidence is recoverable via the manifest.

## General rule

Generate the manifest after all receipts/passport/supersession; generate sums with a declared base and self-exclusion; never claim exact hashes for files written after scanning.
