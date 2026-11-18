"""Bounded matched routing-locator qualification; no new engine or raw source."""
from __future__ import annotations

from dataclasses import replace
import json
import resource
import tempfile
import time
from pathlib import Path

import pytest

from rawlsing_next._pre553_query_common import _parse_target_plan, _profile
from rawlsing_next._pre553_query_eval import _build_fact, _evaluate_index_group
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def _eval(index, query, predicate, registry):
    plan = _parse_target_plan(query, registry)
    profile = _profile(query)
    evaluation = _evaluate_index_group(
        (index,), query=query, predicate=predicate, plan=plan,
        profile=profile, registry=registry, group_scope=None,
    )
    fact = _build_fact(
        (index,), query=query, predicate=predicate, plan=plan,
        profile=profile, evaluation=evaluation, registry=registry,
    )
    return evaluation, fact


def main() -> int:
    root = Path(tempfile.mkdtemp(
        prefix="qualification-",
        dir="WORKER_RETURNS/ANVIL_ROUTING_ACCESS_IMPLEMENTATION_20261118/tmp",
    ))
    monkey = pytest.MonkeyPatch()
    try:
        source, _qa, predicate, _other, queries, admission = _fixture(
            monkey, root, "QUAL",
        )
        import pyarrow.parquet as pq
        reads = []
        original_read = pq.ParquetFile.read_row_group

        def counted_read(self, *args, **kwargs):
            reads.append(1)
            return original_read(self, *args, **kwargs)

        monkey.setattr(pq.ParquetFile, "read_row_group", counted_read)
        result = {"schema": "ANVIL_ROUTING_ACCESS_QUALIFICATION@1", "fixture": "existing tiny 8R controlled prepared fixture", "operations": [], "h_note": "estate/fixture admission outside timed prepared session; not isolated", "reads_note": "all Parquet row-group reads during prepared build + qualification ops"}
        session_started = time.perf_counter()
        context = admission.prepared_i03()
        prepared = context.__enter__()
        session_elapsed = time.perf_counter() - session_started
        try:
            index = prepared._session.indices_for(
                query=queries["f4"], release_refs=(admission.release_ref,),
            )[0][1]
            baseline_index = replace(index, routing_lookup=None)
            calls = []
            objects = []
            original_lookup = prepared._session._routing_lookup.lookup

            def counted_lookup(*, respondent, target, risk_set):
                calls.append((respondent, target, risk_set))
                for fact in original_lookup(respondent=respondent, target=target, risk_set=risk_set):
                    objects.append(fact.ref.key)
                    yield fact

            monkey.setattr(prepared._session._routing_lookup, "lookup", counted_lookup)
            registry = admission._runtime_catalog.authority_registry
            for name in ("f4", "f2"):
                q = queries[name]
                c0 = time.perf_counter()
                ce, cf = _eval(index, q, predicate, registry)
                qms = (time.perf_counter() - c0) * 1000
                b0 = time.perf_counter()
                be, bf = _eval(baseline_index, q, predicate, registry)
                bms = (time.perf_counter() - b0) * 1000
                o0 = time.perf_counter()
                export = canonical_json(cf)
                oms = (time.perf_counter() - o0) * 1000
                result["operations"].append({
                    "name": name,
                    "candidate_q_ms": round(qms, 3),
                    "baseline_q_ms": round(bms, 3),
                    "export_o_ms": round(oms, 3),
                    "export_bytes": len(export.encode()),
                    "fact_ref_equal": cf.ref == bf.ref,
                    "fact_json_equal": canonical_json(cf) == canonical_json(bf),
                    "risk_members_equal": ce.risk_members == be.risk_members,
                    "denominator_members_equal": ce.denominator_members == be.denominator_members,
                    "cells_equal": ce.raw_cells == be.raw_cells,
                    "observed_zero_cells": sum(1 for v in ce.raw_cells.values() if v == 0),
                    "used_object_refs_equal": [o.ref.key for o in ce.used_objects] == [o.ref.key for o in be.used_objects],
                    "used_authority_refs_equal": ce.used_authority_refs == be.used_authority_refs,
                })
            locator_count = prepared._session._db.execute("SELECT COUNT(*) FROM routing_locator").fetchone()[0]
            session_reads = len(reads)
            result.update({
                "routing_locator_rows": locator_count,
                "lookup_calls": len(calls),
                "lookup_objects_yielded": len(objects),
                "prepared_session_build_ms": round(session_elapsed * 1000, 3),
                "parquet_row_group_reads_total": session_reads,
                "parent_maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "scratch_retained": "session SQLite temp only; no persistent artifact",
                "coordinate_case": "ABSENT_FROM_TINY_FIXTURE; existing native suites cover coordinate/observed-zero cases",
            })
        finally:
            context.__exit__(None, None, None)
        result["all_parity"] = all(
            all(x[k] for k in (
                "fact_ref_equal", "fact_json_equal", "risk_members_equal",
                "denominator_members_equal", "cells_equal",
                "used_object_refs_equal", "used_authority_refs_equal",
            ))
            for x in result["operations"]
        )
        Path("WORKER_RETURNS/ANVIL_ROUTING_ACCESS_IMPLEMENTATION_20261118/evidence/qualification.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return 0 if result["all_parity"] else 1
    finally:
        monkey.undo()


if __name__ == "__main__":
    raise SystemExit(main())
