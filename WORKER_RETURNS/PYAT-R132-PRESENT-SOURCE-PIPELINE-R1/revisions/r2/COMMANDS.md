# R132 r2 — exact commands

## Actual composition smoke (executed; synthetic only)

```sh
env PYTHONPATH=. python3 - <<'PY'
from pathlib import Path
from rawlsing_next.tests.test_universal_source_projection import build_s3, s3_rows
from rawlsing_next.pre553_universal_workload import compile_universal_workload
from rawlsing_next.pre553_native_workload_binding import execute_test_only_workload
p=Path('.r61/r132-present-source-pipeline/r2-smoke/synthetic-small.sav')
b=build_s3(p, s3_rows(respondents=6, occasions=2))
c=compile_universal_workload(bundle=b, as_of='2026-10-26', host='local-r132-smoke', purpose='TEST_ONLY_SOURCEFREE')
for item in c.compiled:
    if item.issued is not None:
        r=execute_test_only_workload(issued=item.issued, source_factory=lambda _ref: b.physical_stream, host='local-r132-smoke', purpose='TEST_ONLY_SOURCEFREE')
        print(r.scope, r.decision_ref.as_dict(), r.manifest.manifest_hash, len(r.receipts), len(r.output_refs))
PY
```

Observed: 3 compiled / 3 issued / 3 executed; one native output/fact each.
This is synthetic TEST_ONLY evidence and is not source proof.

## Real admitted call (not run; no current source tuple)

```python
result = execute_issued_workload(
    workload,
    resolver,
    source_factory=source_factory,
    host=host,
    purpose=purpose,
    allow_test_only=False,
    prior_receipts=(),
    max_units=None,
)
```

`workload`, `resolver`, `source_factory`, `host`, and `purpose` are the current
source-specific admission tuple. The exact source custodian/owner decision is
in `SOURCE_AUTHORITY_DECISION.json`. Do not infer it from historical S44,
source possession, or TEST_ONLY data.

## Constraints

No raw source read, decoder, source hash, checkpoint replay, old retained
replay, new engine, CI/prod/actor grant, or FF/V553 source-grade run.
