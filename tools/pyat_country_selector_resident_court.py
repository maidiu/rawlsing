"""Matched selector-view economics using the real country-wide fixture.
No source or authority grant. Python reachable object-size accounting only:
SQLite/native heap, allocator fragmentation, process tree and interpreter
shared roots are deliberately not claimed as measured.
"""
import gc
import hashlib
import json
import statistics
import sys
import time
from collections.abc import Mapping
from unittest.mock import patch
from rawlsing_next import _pre553_c11_execution_view as view
from rawlsing_next.tests.test_pre553_country_numeric_economics import CountryNativeEconomics


def reachable(*roots, exclude=()):
    seen={id(x) for x in exclude}
    stack=list(roots)
    total=0
    while stack:
        obj=stack.pop()
        if id(obj) in seen or isinstance(obj,type) or callable(obj):
            continue
        seen.add(id(obj))
        total+=sys.getsizeof(obj)
        if isinstance(obj,memoryview):
            stack.append(obj.obj)
        elif isinstance(obj,(tuple,list,set,frozenset,dict,Mapping)):
            stack.extend(gc.get_referents(obj))
        elif type(obj).__module__.startswith("rawlsing_next"):
            stack.extend(gc.get_referents(obj))
    return total


def main():
    original=view._compact_country_headers
    seen=False

    def compare(release_ref,replay_ref,non_events,headers,bodies,routing=None):
        nonlocal seen
        if seen:
            return original(release_ref,replay_ref,non_events,headers,bodies,routing)
        seen=True
        args=(release_ref,replay_ref,non_events,headers,bodies,routing)
        def build(packed):
            if packed:
                return original(*args)
            with patch.object(view._PackedCountrySelectors,"build",
                              side_effect=lambda headers,bodies:tuple(h.selector for h in headers)):
                return original(*args)
        times={False:[],True:[]}
        versions={}
        for order in ((False,True),(True,False),(False,True),(True,False)):
            for packed in order:
                gc.collect()
                t=time.perf_counter()
                versions[packed]=build(packed)
                times[packed].append(time.perf_counter()-t)
        old,new=versions[False],versions[True]
        assert isinstance(new.lane.selectors,view._PackedCountrySelectors)
        assert tuple(old.lane.selectors)==tuple(new.lane.selectors)
        assert len(old)==len(new)
        # Real respondent postings, actual exact targets, all three access
        # lanes and state filter; no full-event wire reconstruction needed.
        targets=tuple(dict.fromkeys(s.native_question_ref for s in old.lane.selectors))[:8]
        def select(public):
            h=hashlib.sha256()
            n=0
            for group in public.by_respondent.values():
                for q in targets:
                    for s in group.select(q,include_component=True):
                        h.update(s.ref.key.encode())
                        h.update(s.response_event_id_or_deterministic_index.encode())
                        n+=1
            return n,h.hexdigest()
        times2={False:[],True:[]};out={}
        for order in ((False,True),(True,False),(False,True),(True,False)):
            for packed in order:
                t=time.perf_counter()
                out[packed]=select(versions[packed])
                times2[packed].append(time.perf_counter()-t)
        assert out[False]==out[True]
        exclude=(bodies.reader,)
        report={"events":len(headers),"selected":out[True][0],
            "header_graph_bytes":reachable(headers),
            "body_and_projection_graph_bytes":reachable(bodies,exclude=exclude),
            "routing_graph_bytes":reachable(routing),
            "R3_tuple_view": {"selector_graph_bytes":reachable(old.lane.selectors),
                "public_view_graph_bytes":reachable(old,exclude=exclude),
                "view_plus_live_headers_graph_bytes":reachable(old,headers,exclude=exclude),
                "view_build_median_s":statistics.median(times[False]),
                "selection_median_s":statistics.median(times2[False])},
            "R4_packed_view": {"selector_graph_bytes":reachable(new.lane.selectors),
                "public_view_graph_bytes":reachable(new,exclude=exclude),
                "view_plus_live_headers_graph_bytes":reachable(new,headers,exclude=exclude),
                "view_build_median_s":statistics.median(times[True]),
                "selection_median_s":statistics.median(times2[True]),
                "payload_count":len(new.lane.selectors.payloads)},
            "grade":"ACTUAL_WIDE_COUNTRY_VIEW_GRAPH_ESTIMATE__NOT_RSS_OR_FULL_NATIVE_CAUSAL_SPEEDUP"}
        print("RELAY_SELECTOR_GRAPH",json.dumps(report),flush=True)
        return new
    import unittest
    with patch.object(view,"_compact_country_headers",side_effect=compare):
        suite=unittest.TestSuite([CountryNativeEconomics("test_wide_100_distinct_native_batch_and_cold_product")])
        result=unittest.TextTestRunner(verbosity=2).run(suite)
    assert result.wasSuccessful() and seen


if __name__=="__main__":
    main()
