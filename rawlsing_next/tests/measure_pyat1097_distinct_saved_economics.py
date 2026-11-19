"""Sourcefree P0 economics: exact same DISTINCT native I03 questions, two routes.

Run separately per mode so ru_maxrss measures each complete worker process:
    python3 -B rawlsing_next/tests/measure_pyat1097_distinct_saved_economics.py \
        --mode legacy --size 10 --out /tmp/sourcefree-legacy-10.json

    python3 -B rawlsing_next/tests/measure_pyat1097_distinct_saved_economics.py \
        --mode shared --size 10 --out /tmp/sourcefree-shared-10.json

The sourcefree C11 fixture is constructed BEFORE the execution timer and
is not reused across process runs. Both routes preserve original I03 + S04
facts. This measures a small 4-respondent/size-target *sourcefree canary*,
not original-source economics or a 100k/6GiB acceptance test.
"""
from __future__ import annotations

import argparse
import json
import resource
import sys
import tempfile
from pathlib import Path
from time import perf_counter_ns

import pytest

from rawlsing_next.pre553_distinct_cold_s04_batch import (
    SOURCEFREE_ONLY_ASSERTION, S04DistinctOperation, execute_distinct_native_s04_research,
)
from rawlsing_next.pre553_s04_first_consumer import receive_s04_first_consumer
from rawlsing_next.tests.test_pre553_distinct_cold_i03_batch import _case

CONTRACT = "PYAT1097_DISTINCT_SOURCEFREE_EXECUTION_ECONOMICS@1"
DATA_GRADE = "FOUR_RESPONDENT_SOURCEFREE_1_10_100_DISTINCT_I03_NOT_NATIVE_SCALE"


def measure(*, mode: str, size: int) -> dict:
    if mode not in {"legacy", "shared"} or size not in {1, 10, 100}:
        raise ValueError("fixed sourcefree 1/10/100 and legacy/shared modes only")
    with tempfile.TemporaryDirectory(prefix="pyat1097-econ-") as temporary:
        with pytest.MonkeyPatch.context() as monkeypatch:
            (
                source, qa, predicate, queries, executor, requests, root
            ) = _case(
                Path(temporary), monkeypatch, size,
                name=f"PYAT1097-ECON-SOURCEFREE-{size}",
            )
            start = perf_counter_ns()
            if mode == "legacy":
                from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
                opened = {"n": 0}
                original_enter = DirectEstateI03Session.__enter__

                def counted_enter(self):
                    opened["n"] += 1
                    return original_enter(self)

                monkeypatch.setattr(
                    DirectEstateI03Session, "__enter__", counted_enter,
                )
                products = []
                for query in queries:
                    execution = executor.execute_i03(
                        query_ref=query.ref, predicate_ref=predicate.ref,
                    )
                    products.append(
                        receive_s04_first_consumer(
                            query=query, execution=execution,
                        )
                    )
                index_preparations = opened["n"]
            else:
                native = execute_distinct_native_s04_research(
                    sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
                    executor=executor,
                    operations=tuple(
                        S04DistinctOperation(query.ref, predicate.ref)
                        for query in queries
                    ),
                )
                products = native.first_consumers
                index_preparations = native.original_i03_batch.prepared_session_count
            elapsed_ns = perf_counter_ns() - start
            rss_native = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            # getrusage(ru_maxrss) is bytes on Darwin and KiB on Linux.
            rss_bytes = int(rss_native if sys.platform == "darwin" else rss_native * 1024)
            per_query = [
                {
                    "query_ref": query.ref.as_dict(),
                    "source_fact_ref": product.execution.facts[0].ref.as_dict(),
                    "s04_knowledge_ref": product.knowledge.ref.as_dict(),
                    "typed_state": product.knowledge.material()["producer_typed_state"],
                    "consumer_status": product.receipt.material()["consumer_status"],
                    "risk_set_ref": product.knowledge.material()["risk_set_ref"],
                }
                for query, product in zip(queries, products)
            ]
            if len(per_query) != size or index_preparations != (
                size if mode == "legacy" else 1
            ):
                raise AssertionError("native engine index count/query count violated")
            return {
                "contract": CONTRACT,
                "grade": DATA_GRADE,
                "mode": mode,
                "distinct_queries": size,
                "source_release_ref": source["release_ref"].as_dict(),
                "native_index_preparations": index_preparations,
                "elapsed_ns_excluding_fixture_construction": elapsed_ns,
                "peak_whole_process_rss_bytes": rss_bytes,
                "rss_note": "Whole process ru_maxrss, includes fixture construction, not isolated query RSS",
                "all_original_queries": per_query,
                "native_source_admission": "SOURCEFREE_ONLY__ORIGINAL_RIGHTS_NOT_ISSUED",
            }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("legacy", "shared"), required=True)
    parser.add_argument("--size", choices=(1, 10, 100), type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = measure(mode=args.mode, size=args.size)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise SystemExit("REFUSE_OVERWRITE_FROZEN_ECON_PROOF")
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        f"{args.mode} {args.size}: elapsed_ns="
        f"{result['elapsed_ns_excluding_fixture_construction']} "
        f"index_preparations={result['native_index_preparations']} "
        f"peak_process_rss_bytes={result['peak_whole_process_rss_bytes']}"
    )


if __name__ == "__main__":
    main()
