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
from tools.pyat_country_storage_relay_benchmark import historical, R4


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
    r4_view=historical(R4,"_pre553_c11_execution_view")
    original_add=view._CountryHeaderBuilder.add
    r4_builder=r4_view._CountryHeaderBuilder()
    r4_headers=[]
    emission={"R4":0.0,"R5":0.0}
    seen=False

    def compare_add(builder,event,*,source_coordinates):
        if seen:
            return original_add(builder,event,source_coordinates=source_coordinates)
        result={}
        for version in (("R4","R5") if len(r4_headers)%2==0 else ("R5","R4")):
            start=time.perf_counter()
            result[version]=(r4_builder.add(event,source_coordinates=source_coordinates)
                if version=="R4" else original_add(builder,event,source_coordinates=source_coordinates))
            emission[version]+=time.perf_counter()-start
        r4_headers.append(result["R4"])
        return result["R5"]

    def compare(release_ref,replay_ref,non_events,headers,bodies,routing=None):
        nonlocal seen,r4_builder
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
        # Compare the actual old emission representation as well as the
        # retained view. Both builders saw the identical validated events.
        previous_headers=tuple(sorted(r4_headers,key=lambda h:h.ref.key))
        assert len(previous_headers)==len(headers)
        fields=("ref","typed_state","native_question_ref",
            "canonical_question_ref_if_authorized","component_or_subitem_ref",
            "authority_snapshot_refs","raw_response_value",
            "canonical_response_value_if_authorized","multiplicity_order_rank_fields",
            "response_event_id_or_deterministic_index")
        for previous,current in zip(previous_headers,headers):
            assert previous.ref==current.ref and previous.content_hash==current.content_hash
            for field in ("empirical_universe_ref","scoped_respondent_ref","dependency_refs",
                          "event_group_id","source_coordinates"):
                assert getattr(previous,field)==getattr(current,field),field
            ps,cs=previous.selector,current.selector
            assert all(getattr(ps,field)==getattr(cs,field) for field in fields)
        r4=r4_view._compact_country_headers(release_ref,replay_ref,non_events,
                                            previous_headers,bodies,routing)
        assert isinstance(new.lane.selectors,view._PackedCountrySelectors)
        assert tuple(old.lane.selectors)==tuple(new.lane.selectors)
        assert len(old)==len(new)
        # Real respondent postings, actual exact targets, all three access
        # lanes and state filter; no full-event wire reconstruction needed.
        targets=tuple(dict.fromkeys(s.native_question_ref for s in old.lane.selectors))[:8]
        def select(public,states=None):
            h=hashlib.sha256()
            n=0
            for group in public.by_respondent.values():
                for q in targets:
                    for s in group.select(q,include_component=True,states=states):
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
        # Match the actual immutable R4 implementation against R5, not an
        # emulated baseline. Separate admitted and zero-match state filters.
        r5_times={"R4":{},"R5":{}}
        for label,states in (("all",None),("none",frozenset())):
            timings={"R4":[],"R5":[]}
            parity={}
            for order in (("R4","R5"),("R5","R4"),("R4","R5"),("R5","R4")):
                for version in order:
                    start=time.perf_counter()
                    result=select(r4 if version=="R4" else new,states)
                    timings[version].append(time.perf_counter()-start)
                    if version in parity:
                        assert result==parity[version]
                    parity[version]=result
            assert parity["R4"]==parity["R5"]
            for version in timings:
                r5_times[version][label]={"median_s":statistics.median(timings[version]),
                    "samples_s":timings[version],"selected":parity[version][0]}
        print("RELAY_R5_SELECTOR_FILTER",json.dumps(r5_times),flush=True)
        exclude=(bodies.reader,)
        print("RELAY_R5_EMISSION",json.dumps({
            "events":len(headers),"exact_header_field_parity":True,
            "R4":{"header_graph_bytes":reachable(previous_headers),
                  "view_plus_headers_graph_bytes":reachable(r4,previous_headers,exclude=exclude),
                  "builder_add_seconds":emission["R4"]},
            "R5":{"header_graph_bytes":reachable(headers),
                  "view_plus_headers_graph_bytes":reachable(new,headers,exclude=exclude),
                  "builder_add_seconds":emission["R5"]},
            "grade":"ACTUAL_MATCHED_HEADER_GRAPH_AND_SUM_OF_ADD_TIMES__NOT_PROCESS_RSS_OR_FULL_INGEST_TIME"
        }),flush=True)
        r4_headers.clear()
        r4_builder=None
        report={"events":len(headers),"selected":out[True][0],
            "header_graph_bytes":reachable(headers),
            "body_and_projection_graph_bytes":reachable(bodies,exclude=exclude),
            "routing_graph_bytes":reachable(routing),
            "tuple_view_from_R5_headers": {"selector_graph_bytes":reachable(old.lane.selectors),
                "public_view_graph_bytes":reachable(old,exclude=exclude),
                "view_plus_live_headers_graph_bytes":reachable(old,headers,exclude=exclude),
                "view_build_median_s":statistics.median(times[False]),
                "selection_median_s":statistics.median(times2[False])},
            "R5_packed_view": {"selector_graph_bytes":reachable(new.lane.selectors),
                "public_view_graph_bytes":reachable(new,exclude=exclude),
                "view_plus_live_headers_graph_bytes":reachable(new,headers,exclude=exclude),
                "view_build_median_s":statistics.median(times[True]),
                "selection_median_s":statistics.median(times2[True]),
                "payload_count":len(new.lane.selectors.payloads)},
            "grade":"ACTUAL_WIDE_COUNTRY_VIEW_GRAPH_ESTIMATE__NOT_RSS_OR_FULL_NATIVE_CAUSAL_SPEEDUP"}
        print("RELAY_SELECTOR_GRAPH",json.dumps(report),flush=True)
        return new
    import unittest
    with patch.object(view,"_compact_country_headers",side_effect=compare), patch.object(
            view._CountryHeaderBuilder,"add",new=compare_add):
        suite=unittest.TestSuite([CountryNativeEconomics("test_wide_100_distinct_native_batch_and_cold_product")])
        result=unittest.TextTestRunner(verbosity=2).run(suite)
    assert result.wasSuccessful() and seen


if __name__=="__main__":
    main()
