# PYAT #1006 runbook and regeneration commands

## Environment

The accepted global Python lacked pyarrow.  A task-local environment was
created inside this return directory; no global environment was modified.

```bash
cd /Users/matthewsmith/.codex/worktrees/sorok-duel-b01/Rawlsing
python3 -m venv WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/.venv
WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/.venv/bin/python -m pip install \
  pyarrow pytest psutil pandas pyreadstat
```

Recorded versions: Python 3.11.3, pyarrow 26.0.1, pandas 3.1.1, pyreadstat
1.3.7, pytest 9.2.0, psutil 7.2.2, numpy 2.4.6.  The venv is ignored by the
return-directory `.gitignore` and is not committed.

## Representative same-fixture estate

`evidence/representative-estate/` is a real small sourcefree release: 64
respondents, 13 complete family members, locator, manifest, weights, typed
missing B, routed D/MR and repeated MR.  Its exact roots and query/fact refs
are in `evidence/representative_receipt.json`.

```bash
PYTHONPATH=.:WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1 \
WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/.venv/bin/python - <<'PY'
import json
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle
base = Path("WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1")
receipt = json.loads((base / "evidence/representative_receipt.json").read_text())
ctx = build_context(ShapeSpec(
    "representative", 64, include_weights=True,
    tag="PYAT1006-REPRESENTATIVE",
))
bundle = build_query_bundle(ctx)
admission = SavedC11Admission.open(
    root=base / receipt["root"],
    exact_path=base / receipt["root"] / receipt["exact_path"],
    independently_held_manifest_sha256=receipt["manifest_sha256"],
    independently_held_i02=ExternalI02Roots(**receipt["i02"]),
    release_ref=exact_ref(receipt["reconstructed_v1_release_ref"]),
    runtime_catalog=bundle.catalog,
    current_authorizer=lambda _roots: True,
)
result = admission.execute_i03(
    query_ref=bundle.selected.ref,
    predicate_ref=bundle.selected_predicate.ref,
)
print([fact.ref.as_dict() for fact in result.facts])
PY
```

The executable, self-contained version is `make_representative.py`; it
regenerates the fixture, the release and the receipt and checks exact native
oracle equality:

```bash
PYTHONPATH=.:WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1 \
WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/.venv/bin/python \
WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/make_representative.py
```

For a direct query-oriented replay, `fresh_probe.py` accepts a capsule with
`root`, `exact_path`, `manifest_sha256`, `i02`, `release`, `query`,
`predicate` and `catalog`.  The full capsule is emitted by `shape_worker.py`.

## Baseline shapes

Run sequentially; each subprocess is monitored at 20 ms against the 6 GiB
process-tree cap and the 3 GiB disk reserve.  Large generated estates remain
under `.local-data/` (ignored, removable scratch); compact receipts are in
`evidence/`.

```bash
R=WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1
PY=$R/.venv/bin/python

# 1k diagnostic, all native readers, n=10 repeat + 10 fresh
$PY $R/run_suite.py --outdir $R/.local-data/suite-1k --shapes diag-1k

# 10k diagnostic, all native readers, n=5 repeat + 5 fresh in the preset
$PY $R/run_suite.py --outdir $R/.local-data/suite-10k --shapes diag-10k-fast
# five additional same-process repeats and ten fresh-process probes:
$PY $R/query_probe.py --capsule $R/.local-data/suite-10k/capsule.json \
  --out $R/.local-data/suite-10k/repeat_probe_5.json --queries "" --repeat 5
for i in $(seq 1 10); do
  $PY $R/fresh_probe.py $R/.local-data/suite-10k/fresh-capsule.json
done

# skew shape: 1k respondents, 600 extra one-respondent MR events
$PY $R/run_suite.py --outdir $R/.local-data/suite-skew-1k --shapes skew-1k

# 50k writer-only split run
$PY $R/run_suite.py --outdir $R/.local-data/suite-50k-write --shapes scale-50k
# measured query probe on the same estate
$PY $R/query_probe.py --capsule $R/.local-data/suite-50k-write/capsule.json \
  --out $R/.local-data/suite-50k-write/query_probe.json \
  --queries selected,f2_reverse,f4_three --repeat 0
$PY $R/session_probe.py $R/.local-data/suite-50k-write/capsule.json

# 100k closest executable shape, writer-only split run
$PY $R/run_suite.py --outdir $R/.local-data/suite-100k-write --shapes scale-100k
$PY $R/query_probe.py --capsule $R/.local-data/suite-100k-write/capsule.json \
  --out $R/.local-data/suite-100k-write/query_probe.json \
  --queries selected,f2_reverse,f4_three --repeat 0
$PY $R/session_probe.py $R/.local-data/suite-100k-write/capsule.json
```

The earlier unsplit 50k attempt (`suite-50k`) timed out at 2400 s before its
worker wrote final metrics; the process tree was 1,654,665,216 B and did not
hit the 6 GiB cap.  That failed shape is recorded in
`evidence/failed_50k_timeout.json`; the completed split writer receipt above is
the authoritative 50k writer measurement.

## Tests

```bash
R=WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1
PY=$R/.venv/bin/python
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1

$PY -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py

$PY -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat991_s2d_saved_admission.py \
  rawlsing_next/tests/test_pyat991_s2d_b_adversarial.py \
  rawlsing_next/tests/test_pyat991_s2d_a_counter.py \
  rawlsing_next/tests/test_pyat991_s2d_five_readers.py \
  rawlsing_next/tests/test_pyat991_s2d_g5_source_scope.py

$PY -m pytest -q -o addopts='' -p no:cacheprovider \
  $R/test_1006_baseline.py --basetemp=$R/.local-data/pytest-tmp
```

Observed: 31 passed (S2-C/S2-D focused); 29 passed for the RUNBOOK five-file
S2-D group; 2 passed for the separate partial-binding suite; 6 passed for the
own fixture/oracle/restore/hostile tests.  The old "36 passed" claim is
withdrawn.  Follow-through locality tests add 2 passed.

This worker did not perform independent G5 review; those are accepted test
reuses and own nonauthor test receipts, not self-acceptance.  Independent G5
`0169fac9...` returned `REVISE_EXACT_DEFECT`; its 29-test and writer-only-RSS
corrections are reflected above.

## Follow-through r2 — locality candidate and writer profile

Reviewer-retained sourcefree releases are read-only at
`/Users/matthewsmith/.codex/worktrees/pyat1007-dual-series-prep/Rawlsing/WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R1/data/`.
The exact capsule hashes are in `followthrough_r2/evidence/locality_candidate_matrix.json`.
Production remains unchanged; the candidate is `EXPERIMENT_NOT_IMPLEMENTED`.

```bash
R=WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1
PY=$R/.venv/bin/python
export PYTHONPATH=.:$R PYTHONDONTWRITEBYTECODE=1

# matched before/after locality pairs on the same reviewer-retained estates
$PY $R/followthrough_r2/run_locality_matrix.py   --outdir $R/followthrough_r2/.local-data/matrix-1k10k   --cases diag-1k,diag-10k --timeout 1800
$PY $R/followthrough_r2/run_locality_matrix.py   --outdir $R/followthrough_r2/.local-data/matrix-100k   --cases hist-100k --timeout 1800
$PY $R/followthrough_r2/summarize_locality.py

# semantic oracle/change/restore/hostile test for the runtime candidate
$PY -m pytest -q -o addopts='' -p no:cacheprovider   $R/followthrough_r2/test_locality_candidate.py   --basetemp=$R/followthrough_r2/.local-data/pytest

# writer call-boundary profile (2k absolute and cProfile)
$PY $R/followthrough_r2/writer_profile.py   --outdir $R/followthrough_r2/.local-data/writer-profile-2k-absolute   --respondents 2000 --no-cprofile
$PY $R/followthrough_r2/writer_profile.py   --outdir $R/followthrough_r2/.local-data/writer-profile-2k   --respondents 2000
```
