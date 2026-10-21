"""Repeated-topology query against the S3 C11 release."""
from __future__ import annotations

from itertools import product

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.tests.pre553_query_frontier_fixtures import _custom_query
from rawlsing_next.tests.test_pre553_empirical_query import _branch_predicate, _query_authority


def run(fx):
    source = fx["source"]
    qa = _query_authority("ur-b-s3-repeated-query")
    pred = _branch_predicate(source, qa, tag="s3-repeated-all")
    sequences = []
    for seq in product(("0", "1", "2"), repeat=2):
        sequences.append([
            {"event_id": f"S3-{i}-{value}", "multiplicity_order_rank_fields": {
                "kind": "REPEATED_EVENT", "multiplicity_index": i}, "value": value}
            for i, value in enumerate(seq)])
    spec = _custom_query(source, qa, pred, "SCORE", topology="REPEATED_EVENT",
                         domain=sequences, included_states=("SUBSTANTIVE_RESPONSE",),
                         tag="s3-repeated")
    registry = AuthorityRegistry(tuple((*fx["authorities"], qa)))
    repo, rel = build_source_backed_c11_repository(fx["incidence"], fx["projection"])
    result = execute_empirical_query(
        repository=repo, query=spec, predicate=pred,
        authority_registry=registry, release_refs=(rel.release_ref,))
    return {"release": rel, "spec": spec, "result": result}
