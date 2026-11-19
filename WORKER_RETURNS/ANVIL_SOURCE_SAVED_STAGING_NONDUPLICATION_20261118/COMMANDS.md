# Commands

```bash
# Exact accepted baseline + frozen construction-only patch
git -C /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER \
  archive aee95429609c372564e996c2d3d3eb30e9253cbf rawlsing_next \
  | tar -x -C /tmp/anvil_staging_nondup
cd /tmp/anvil_staging_nondup
git init -q
git add rawlsing_next
git -c user.email=a@b -c user.name=scratch commit -qm baseline
git apply /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER/WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_ONLY_CANDIDATE_20261118/candidate.patch
git add rawlsing_next
git -c user.email=a@b -c user.name=scratch commit -qm construction-only

# Harness
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  python3 -B rawlsing_next/tests/staging_nonduplication_harness.py /tmp/anvil_staging_proof
```

The harness output is `proof.json`; `harness.out` is the PASS line and
`harness.err` is empty.
