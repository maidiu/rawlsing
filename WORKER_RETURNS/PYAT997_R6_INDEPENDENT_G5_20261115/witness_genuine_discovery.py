#!/usr/bin/env python3
"""Actual compiler-issued discovery through native I05/Batch and the R6 join."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i05,
)
from rawlsing_next.pre553_source_postconsumer_receipts import (
    join_saved_source_operation_fates,
)
from rawlsing_next.tests.test_pyat997_s1e_saved_native_first_consumer import (
    _NATIVE_HOST, _NATIVE_PURPOSE, _full, _issued_manifest, _native_i03,
)

root = Path(tempfile.mkdtemp(prefix="pyat997-r6-genuine-")).resolve()
handoff, estate, admission, compilation, resolver, sink = _full(root / "full")
workload = compilation.issued.workload
assert len(workload.requests) == 0
assert len(workload.discoveries) == 1
operation, fact_result, negatives = _native_i03(admission, compilation)
discovery = execute_saved_i05(
    admission, discovery_authority_ref=workload.discoveries[0])
manifest, predicates = _issued_manifest(workload, admission)
batch = execute_saved_batch(
    admission, manifest=manifest, predicate_ref_by_query=predicates)
joined = join_saved_source_operation_fates(
    handoff=handoff, estate_receipt=estate, admission=admission,
    compilation=compilation, workload=workload, resolver=resolver,
    host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=batch,
)
fact = fact_result.facts[0]
out = {
    "compiler_issued_query_requests": len(workload.requests),
    "compiler_issued_discoveries": len(workload.discoveries),
    "source_sha256": handoff.source_sha256,
    "i02_roots": estate.i02.__dict__,
    "family_counts": dict(estate.family_counts),
    "handoff_stats": dict(handoff.stats.__dict__),
    "i03_operation_id": operation,
    "i03_fact_ref": fact.ref.key,
    "i03_typed_state": fact.typed_state,
    "i03_raw": [fact.semantic_fields.get("raw_numerator_support"),
                 fact.semantic_fields.get("raw_denominator_support")],
    "i03_negatives": [x[1].typed_state for x in negatives],
    "i05_receipt_count": len(discovery.receipts),
    "batch_units": len(batch.receipts),
    "batch_states": [r.state for r in batch.receipts],
    "join_audit": dict(joined.audit),
    "join_rows": len(joined.rows),
    "source_opens_after_consumer": admission.binding_receipt().source_opens,
    "full_c11_builds": admission.binding_receipt().full_c11_repository_builds,
}
print(json.dumps(out, indent=2, sort_keys=True, default=str))
