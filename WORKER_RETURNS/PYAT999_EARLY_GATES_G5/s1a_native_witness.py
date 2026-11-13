"""Independent S1-A native cache admission/recompute witness.

Run from the S1-A tested worktree at 6286.  Uses the actual source-backed
producer and execute_empirical_query, with a cell-open counter and RSS.
"""
from __future__ import annotations

import json
from pathlib import Path
import resource
import sys

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream, SourceBackedC11SessionCache,
    build_source_backed_c11_repository,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _cell_map, _query, _query_authority,
)


def _rss():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: s1a_native_witness.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("private proofroot required")
    tmp = proofroot / "s1a-native"
    tmp.mkdir(parents=True, exist_ok=True)
    fx = _fixture("s1a-g5-native")
    opens = {"cell_iter_calls": 0}

    def stream():
        def cells():
            opens["cell_iter_calls"] += 1
            return iter(fx["cells"])
        return ExactPhysicalCellStream(
            source_sha256=fx["source_sha"], row_count=3,
            cell_iter_factory=cells,
        )

    cache = SourceBackedC11SessionCache()
    source = stream()
    repo, release = build_source_backed_c11_repository(
        source, fx["projection"], cache=cache,
    )
    qa = _query_authority("s1a-g5-native")
    pred = _branch_predicate(
        fx, qa, members=(fx["respondents"]["R1"],), tag="s1a-g5-native",
    )
    query = _query(fx, qa, pred, ("Y",), tag="s1a-g5-native")
    registry = AuthorityRegistry((*fx["authorities"], qa))

    def fact(repository, rel):
        return execute_empirical_query(
            repository=repository, query=query, predicate=pred,
            authority_registry=registry, release_refs=(rel.release_ref,),
        ).facts[0]

    cold_fact = fact(repo, release)
    cold_opens = opens["cell_iter_calls"]
    warm_repo, warm_release = build_source_backed_c11_repository(
        source, fx["projection"], cache=cache,
    )
    warm_fact = fact(warm_repo, warm_release)
    warm_opens = opens["cell_iter_calls"]
    cache.clear()
    rebuilt_repo, rebuilt_release = build_source_backed_c11_repository(
        source, fx["projection"], cache=cache,
    )
    rebuilt_fact = fact(rebuilt_repo, rebuilt_release)
    rebuilt_opens = opens["cell_iter_calls"]
    out = {
        "schema": "PYAT999_S1A_NATIVE_CACHE_WITNESS@1",
        "tested_worktree": str(Path.cwd()),
        "fixture_rows": 3,
        "cold_cell_iter_calls": cold_opens,
        "warm_cell_iter_calls": warm_opens,
        "clear_recompute_cell_iter_calls": rebuilt_opens,
        "cold_fact_ref": cold_fact.ref.as_dict(),
        "warm_fact_ref": warm_fact.ref.as_dict(),
        "rebuilt_fact_ref": rebuilt_fact.ref.as_dict(),
        "warm_fact_equal_cold": warm_fact.ref == cold_fact.ref,
        "rebuilt_fact_equal_cold": rebuilt_fact.ref == cold_fact.ref,
        "cold_cell_map": _cell_map(cold_fact),
        "warm_cell_map": _cell_map(warm_fact),
        "rebuilt_cell_map": _cell_map(rebuilt_fact),
        "cache_entries_after_rebuild": cache.entry_count,
        "parent_max_rss_bytes": _rss(),
        "note": "tiny sourcefree fixture; not 100k or production safety",
    }
    (proofroot / "s1a_native_witness.json").write_text(
        json.dumps(out, indent=2, sort_keys=True, default=str), encoding="utf-8",
    )
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    return 0 if (
        cold_fact.ref == warm_fact.ref == rebuilt_fact.ref
        and cold_opens == 1 and warm_opens == 1 and rebuilt_opens == 2
        and cache.entry_count == 1
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
