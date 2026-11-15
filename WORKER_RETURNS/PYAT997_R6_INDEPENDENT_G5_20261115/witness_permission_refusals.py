#!/usr/bin/env python3
"""Independent wrong source/science permission refusal through the R6 join."""
from __future__ import annotations

import json
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyDecisionResolver, _ref,
)
from rawlsing_next.pre553_source_postconsumer_receipts import (
    SourceReceiptJoinError, join_saved_source_operation_fates,
)
from rawlsing_next.tests.test_pyat997_s1e_saved_native_first_consumer import (
    _NATIVE_HOST, _NATIVE_PURPOSE, _full, _issued_manifest,
)

root = Path(tempfile.mkdtemp(prefix="pyat997-r6-permission-")).resolve()
out = {}
for attack in ("source_permission", "scientific_permission"):
    base = root / attack
    handoff, estate, admission, compilation, resolver, sink = _full(base)
    original = compilation.issued
    forged_record = replace(
        original.record,
        **(
            {"source_permission_ref": _ref(
                "TEST_ONLY_SOURCE_PERMISSION", "pyat997-forged-source")}
             if attack == "source_permission" else
             {"scientific_permission_refs": (_ref(
                 "TEST_ONLY_SCIENTIFIC_PERMISSION", "pyat997-forged-science"),)})
    )
    forged_issued = replace(original, record=forged_record)
    forged_compilation = replace(compilation, issued=forged_issued)
    forged_resolver = TestOnlyDecisionResolver(forged_record)
    manifest, _ = _issued_manifest(original.workload, admission)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True)
    try:
        joined = join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=admission,
            compilation=forged_compilation, workload=original.workload,
            resolver=forged_resolver, host=_NATIVE_HOST,
            purpose=_NATIVE_PURPOSE, runner=runner,
        )
        out[attack] = {
            "refused": False,
            "positive": joined.audit.get("positive_native_linked_operations"),
        }
    except SourceReceiptJoinError as exc:
        out[attack] = {
            "refused": True,
            "error": str(exc),
            "positive_attribution": 0,
            "runner_receipts": len(runner.receipts),
        }
print(json.dumps(out, indent=2, sort_keys=True))
raise SystemExit(0 if all(v.get("refused") and v.get("positive_attribution") == 0
                          for v in out.values()) else 2)
