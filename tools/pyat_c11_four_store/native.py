"""TEST-ONLY wiring to the *existing*, unmodified native I03 evaluator.

This controlled adapter constructs an exact DirectEstateI03Session-shaped
research reader from an independently verified source and a separately
audited persistent store. No production reader or scientific issuer is
modified, installed or accredited.  It does not implement a second
statistical evaluator.

IMPORTANT: runtime type guards in the original evaluator require the exact
DirectEstateI03Session class. This adapter uses __new__ and instance-bound
physical methods. It is an experiment, not a substitute for protected S2-D
reader receiving; its construction is intentionally visible in reports.
"""
from __future__ import annotations

import json
from types import MethodType
from typing import Any, Iterator

from .stores import Store, StoreFailure


def _native_object(ref: str, body: str):
    from rawlsing_next.pre553_parquet_carrier import _object_from_row
    obj = _object_from_row(json.loads(body))
    if obj.ref.key != ref:
        raise StoreFailure("native object ExactRef diverged from persisted canonical body")
    return obj


def open_native_session(store: Store, verified: Any, recorded_plan: Any = None):
    from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
    from rawlsing_next.pre553_anvil_stream_native_i03 import (
        VerifiedAnvilStreamEstate, RecordedRoutingPlan,
    )
    from rawlsing_next.pre553_c11_integrity import RespondentIdentity
    from rawlsing_next.pre553_empirical_objects import (
        EmpiricalUniverse, SourceUniverseRelation,
        RespondentEvent, RoutingEligibilityFact, WeightMeasureFact,
        EmpiricalCoordinateFact, exact_ref,
    )
    if type(verified) is not VerifiedAnvilStreamEstate:
        raise StoreFailure("native test requires actual independently verified ANVIL stream")
    verified._live()
    if recorded_plan is not None:
        if type(recorded_plan) is not RecordedRoutingPlan:
            raise StoreFailure("unqualified recorded routing plan")
        recorded_plan.require_for(verified)
    if store.get_meta("state") != "COMMITTED":
        raise StoreFailure("native test refuses incomplete SQLite source")
    from pathlib import Path
    if store.name == "H" and not store.estate_path.samefile(verified.directory):
        raise StoreFailure("hybrid source Parquet differs from verified original")
    # All four stores have been audited against same saved source before
    # entering this exact-type native evaluator.
    reader = DirectEstateI03Session.__new__(DirectEstateI03Session)
    reader.estate = verified
    reader._recorded_plan = recorded_plan
    reader._temporary = None
    reader._db = store.db
    reader._files = {}
    reader._row_group_cache = {}
    reader.respondents = {}
    reader._universe = None
    reader._relations = ()
    reader._test_only_four_store = store.name
    universe_key = verified.i02.universe
    for ref, body in store.iter_family("EmpiricalUniverse"):
        obj = _native_object(ref, body)
        if type(obj) is EmpiricalUniverse and obj.ref.key == universe_key:
            if reader._universe is not None:
                raise StoreFailure("duplicate empirical universe in SQLite")
            reader._universe = obj
    if reader._universe is None:
        raise StoreFailure("native empirical universe missing")
    for ref, body in store.iter_family("RespondentIdentity"):
        obj = _native_object(ref, body)
        if type(obj) is not RespondentIdentity:
            raise StoreFailure("wrong respondent body type")
        if exact_ref(obj.empirical_universe_ref).key == universe_key:
            if ref in reader.respondents:
                raise StoreFailure("duplicate native respondent")
            reader.respondents[ref] = obj
    relations = []
    for ref,body in store.iter_family("SourceUniverseRelation"):
        obj = _native_object(ref,body)
        if type(obj) is not SourceUniverseRelation:
            raise StoreFailure("wrong universe relation body type")
        if reader._universe.ref.as_dict() in obj.source_universe_refs:
            relations.append(obj)
    reader._relations = tuple(sorted(relations, key=lambda x:x.ref.key))

    def selected(self, respondent_ref, target, *,
                 native_only=False, include_component=False, states=None):
        for ref,body in store.select_events(
            respondent=respondent_ref.key, target=exact_ref(target).key,
            native_only=native_only, include_component=include_component, states=states,
        ):
            verified._live()
            obj = _native_object(ref, body)
            if type(obj) is not RespondentEvent:
                raise StoreFailure("saved event body has wrong exact type")
            if (exact_ref(obj.scoped_respondent_ref).key != respondent_ref.key
                    or obj.empirical_universe_ref.key != universe_key):
                raise StoreFailure("wrong-universe or respondent event")
            if self._recorded_plan is not None:
                obj = self._recorded_plan.event_transforms.get(ref, obj)
            verified._live()
            yield obj

    def side_family(self, family, respondent_key):
        accepted = {
            "EmpiricalCoordinateFact": EmpiricalCoordinateFact,
            "RoutingEligibilityFact": RoutingEligibilityFact,
            "WeightMeasureFact": WeightMeasureFact,
        }
        if family not in accepted:
            raise StoreFailure("wrong physical native side family")
        material = []
        for ref,body in store.side_family(family=family,respondent=respondent_key):
            verified._live()
            obj = _native_object(ref,body)
            if type(obj) is not accepted[family]:
                raise StoreFailure("bad native side-family type")
            if (obj.scoped_respondent_ref.key != respondent_key
                    or obj.empirical_universe_ref.key != universe_key):
                raise StoreFailure("native side-family exact-scope mismatch")
            material.append(obj)
        for obj in sorted(material, key=lambda x:x.ref.key):
            verified._live()
            yield obj

    def routing(self, *, respondent, target, risk_set):
        if self._recorded_plan is not None:
            verified._live()
            for obj in self._recorded_plan.facts_by_key.get(
                (respondent,target,risk_set), ()
            ):
                verified._live()
                yield obj
            return
        for ref,body in store.routing_facts(
            respondent=respondent,target=target,risk_set=risk_set,
        ):
            verified._live()
            obj = _native_object(ref,body)
            if (type(obj) is not RoutingEligibilityFact
                    or obj.scoped_respondent_ref.key != respondent
                    or obj.empirical_universe_ref.key != universe_key
                    or exact_ref(obj.question_or_target_ref).key != target
                    or exact_ref(obj.risk_set_ref).key != risk_set):
                raise StoreFailure("stored native routing identity mismatch")
            verified._live()
            yield obj

    reader._selected_events = MethodType(selected, reader)
    reader._respondent_family = MethodType(side_family, reader)
    reader._routing_facts = MethodType(routing, reader)
    return reader


def execute_issued(store: Store, verified: Any, operation: dict):
    """The only numeric producer is existing rawlsing_next.execute_empirical_query."""
    from rawlsing_next.pre553_empirical_query import execute_empirical_query
    query = operation["query"]
    predicate = operation["predicate"]
    registry = operation["authority_registry"]
    recorded_plan = operation.get("recorded_plan")
    name = operation.get("name", query.ref.key)
    if not name:
        raise StoreFailure("issued operation lacks exact identifier")
    reader = open_native_session(store, verified, recorded_plan)
    # Existing I03 checks query/predicate/source/issuer and builds original
    # EmpiricalFact; adapter changes only how the saved objects are retrieved.
    verified._live()
    result = execute_empirical_query(
        repository=reader, query=query, predicate=predicate,
        authority_registry=registry,
        release_refs=(verified.native_release_ref,),
    )
    verified._live()
    from rawlsing_next.pre553_s04_observed_research import (
        receive_s04_i03_research, S04KnowledgeError,
    )
    knowledge=None
    try:
        knowledge=receive_s04_i03_research(query=query,execution=result)
        s04={"status":"PRODUCED_TESTONLY_S04",
             "ref":knowledge.ref.key,
             "content_hash":knowledge.content_hash}
    except S04KnowledgeError as exc:
        s04={"status":"METHOD_SPECIFIC_S04_REFUSAL",
             "reason_type":type(exc).__name__,
             "reason":str(exc)}
    ff01={"status":"NOT_REQUESTED"}
    details=operation.get("ff01")
    if details is not None:
        if knowledge is None:
            ff01={"status":"NOT_APPLICABLE_S04_UNAVAILABLE"}
        else:
            from rawlsing_next.pre553_s04_ff01_consumer import (
                receive_ff01_from_s04, S04FF01SeamError,
            )
            if not isinstance(details,dict) or "conditioner_index" not in details or "producer_permission_ceiling" not in details:
                raise StoreFailure("FF01 requires exact existing consumer conditions/permission ceilings")
            try:
                output=receive_ff01_from_s04(
                    knowledge=knowledge,query=query,execution=result,
                    conditioner_index=details["conditioner_index"],
                    producer_permission_ceiling=details["producer_permission_ceiling"],
                    relation_permission_ceiling=details.get("relation_permission_ceiling"),
                )
                ff01={"status":"PRODUCED_TESTONLY_EXISTING_FF01",
                      "ref":output.ref.key,"content_hash":output.content_hash}
            except S04FF01SeamError as exc:
                ff01={"status":"EXISTING_FF01_TYPED_REFUSAL",
                      "reason_type":type(exc).__name__,"reason":str(exc)}
    verified._live()
    return {
        "name": str(name),
        "query_ref": result.query_ref.key,
        "source_scope_mode": result.source_scope_mode,
        "release_refs": [r.key for r in result.release_refs],
        "facts": [
            {"ref":f.ref.key, "state":f.typed_state,
             "semantic_hash":f.content_hash}
            for f in result.facts
        ],
        "s04":s04,
        "ff01":ff01,
        "grade": "EXISTING_I03_AND_S04_FF01_CONSUMERS_WITH_TEST_ONLY_PHYSICAL_ADAPTER",
    }
