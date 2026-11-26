"""Generated SAV -> country numeric -> real issued U43 Batch -> S04/FF01.

A bounded mixed-cardinality economics witness, not native original data,
a production benchmark or permission. Report actual width and governed width.
No synthetic oracle fact replaces I03; independently count the generated rows.
"""
import hashlib
import json
import resource
import tempfile
import time
import unittest
from collections import defaultdict
from contextlib import ExitStack
from functools import wraps
from statistics import median
from unittest.mock import patch
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

from rawlsing_next.pre553_country_numeric_carrier import build_country,CountryReader
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import (
    PhysicalSlot,RowRespondentBinding,ResponseSlotRule,ResponseValueRule,OccurrenceRule,
    CoordinateSlotRule,WeightSlotRule,physical_value_binding_key,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef,RoutingEligibilityFact,semantic_hash,
)
from rawlsing_next.pre553_c11_integrity import TypedAbsence,RespondentIdentity,QuestionVariableBinding
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_issued_workload import NativeWorkload,IssuedWorkloadRecord,canonical,operation_jobs
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_saved_durable_delivery import execute_publish_country,open_country_product
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
from rawlsing_next.tests.test_pre553_empirical_query import (
    _ref,_query_authority,_branch_predicate,_query,_predicate,_response_leaf,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,_d_auth,_discovery_authority,_grammar,_qt,_rule,
)

class CountryNativeEconomics(unittest.TestCase):
    def test_mixed_cardinality_sav_distinct_native_batch_and_cold_product(self):
        self._native_batch(wide=False)

    def test_wide_100_distinct_native_batch_and_cold_product(self):
        import os
        if os.environ.get("PYAT_WIDE_ECONOMICS")!="1":
            self.skipTest("separate wide economics CI job")
        self._native_batch(wide=True)

    def test_interrupted_country_campaign_resumes_only_pending_exact_units(self):
        self._native_batch(wide=False,resume_court=True)

    def test_distinct_issued_workloads_reuse_only_live_exact_country_preparation(self):
        self._native_batch(wide=False,session_court=True)

    def _native_batch(self,*,wide,resume_court=False,session_court=False,external_case=None):
        import os
        # Real operational wide path never owns an expanded routing tuple.
        # Keep the older full-object/hostile comparison executable on demand
        # (and default for the smaller test), without contaminating this
        # process's memory high-water with the historical representation.
        direct_pack=external_case is not None or resume_court or session_court or (wide and os.environ.get("PYAT_WIDE_LEGACY_COMPARE")!="1")
        from rawlsing_next.pre553_source_backed_c11_facade import _PackedRoutingFacts
        from rawlsing_next import pre553_issued_workload as issued
        tag=("country-native-resume" if resume_court else
             "country-native-wide" if wide else "country-native-economics")
        n,governed,extras=(64,16,23) if resume_court else (512,80,218) if wide else (800,16,23)
        rng=np.random.default_rng(312)
        values=rng.integers(0,2,(n,governed))
        if resume_court:
            # Exactly balanced pairwise marginals but a genuine three-way XOR.
            # A rare conjunction has one actual member, not a pruned branch.
            for i in range(n):
                values[i,0],values[i,1]=(i//2)%2,(i//4)%2
            values[:,2]=values[:,0]^values[:,1]
            values[:,3]=0
            values[6,3]=1
        names=tuple("q"+str(i) for i in range(governed))
        data={q:values[:,i].astype(str) for i,q in enumerate(names)}
        for i in range(extras):
            data["v"+str(i)]=np.arange(n,dtype=np.float64)*(1.000001+i*.00001)+i*.001
        data["G"]=np.where(np.arange(n)%2==0,"A","B")
        data["W"]=1.+(np.arange(n)%3)
        from contextlib import nullcontext
        if external_case is None:
            frame=pd.DataFrame(data)
            chosen=tuple(range(1,n+1,2))
            selected=values[::2,:]
            context=tempfile.TemporaryDirectory()
        else:
            # Reuse the SAME issuer/operation geometry for independently
            # retained countries from one already-built physical source.
            context=nullcontext(external_case["root"])
        with context as d:
            p=Path(d)
            country="A"
            if external_case is None:
                src=p/"generated.sav";db=p/"country.sqlite";products=p/"products";products.mkdir()
                pyreadstat.write_sav(frame,str(src))
                original_bytes=src.stat().st_size
                sha=hashlib.sha256(src.read_bytes()).hexdigest()
                t=time.monotonic()
                with decode_sav(src,expected_source_sha256=sha) as inc:
                    ordinals={v.name:v.ordinal for v in inc.variables}
                    receipt=build_country(inc,country_variable="G",country_value="A",output=db,
                                          require_current=lambda:True,block_rows=256)
                build_seconds=time.monotonic()-t
                src.unlink()
            else:
                db,receipt,ordinals,selected,chosen,country=(
                    external_case[k] for k in ("db","receipt","ordinals","selected","chosen","country"))
                tag="country-campaign-"+country
                sha=receipt.source_sha256
            self.assertEqual(receipt.country_rows,len(chosen))
            t=time.monotonic()
            fx=_fixture(tag);original=fx["projection"];universe=fx["universe"]
            if external_case is not None:
                material=universe.semantic_projection()
                fields=material.pop("semantic_fields")
                fields.update(country_geography=country,sampling_geography=country+"-NATIONAL")
                universe=type(universe)(**material,**fields)
                fx["universe"]=universe
            source_auth=fx["source_auth"];mapping_auth=fx["authorities"][1]
            respondents=tuple(RespondentIdentity(empirical_universe_ref=universe.ref,
                respondent_key=f"{tag}-{row}",source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT",f"{tag}-{row}"),
                identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE")) for row in chosen)
            qrefs={q:_ref("QUESTION_NATIVE",tag+"-"+q) for q in names}
            questions=tuple(QuestionVariableBinding(empirical_universe_ref=universe.ref,native_question_ref=qrefs[q],
                instrument_question_version="1",canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
                component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
                semantic_authority_ref=source_auth.authority_ref,topology_authority_ref=source_auth.authority_ref) for q in names)
            slots=tuple(ResponseSlotRule(PhysicalSlot(ordinals[q],q),binding,tuple(
                ResponseValueRule(physical_value_binding_key(v,"OBSERVED_STORAGE_VALUE"),"SUBSTANTIVE_RESPONSE",
                    (OccurrenceRule("0",_ref("TOPOLOGY",tag+"-"+q),{"kind":"SCALAR_SINGULAR","index":0}),),
                    v,mapping_auth.authority_ref) for v in ("0","1"))) for q,binding in zip(names,questions))
            risk=fx["risk_refs"]["R"];state="ELIGIBLE_APPLICABLE"
            def original_routes():
                return (RoutingEligibilityFact(typed_state=state,authority_snapshot_refs=(fx["routing_auth"].authority_ref,),
                dependency_refs=(),producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT",f"{tag}-{row}-{q}"),
                empirical_universe_ref=universe.ref,scoped_respondent_ref=person.ref,question_or_target_ref=qrefs[q],
                risk_set_ref=risk,routing_rule_ref=_ref("ROUTING_RULE",tag+"-"+q),applicability_state=state,routing_state=state,
                parent_predicate_refs=(),member_set_replay_ref=_ref("MEMBER_SET",tag+"-"+q))
                    for q in names for row,person in zip(chosen,respondents))
            routing=(_PackedRoutingFacts if direct_pack else tuple)(original_routes())
            projection=replace(original,expected_source_sha256=sha,
                source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT","urn:test:"+tag,sha),
                universes=(universe,),respondents=respondents,row_bindings=tuple(RowRespondentBinding(row,person.ref) for row,person in zip(chosen,respondents)),
                questions=questions,response_slots=slots,routing=routing,
                coordinate_slots=(replace(original.coordinate_slots[0],slot=PhysicalSlot(ordinals["G"],"G")),),
                weight_slots=(replace(original.weight_slots[0],slot=PhysicalSlot(ordinals["W"],"W")),))
            fx.update(qrefs=qrefs,respondents={p.respondent_key:p for p in respondents})
            qa=_query_authority(tag);da=_d_auth(tag+"-discovery")
            base=_branch_predicate(fx,qa,members=respondents,tag=tag+"-all")
            atom=_predicate(fx,qa,_response_leaf(fx,qa,"q0","1"),tag=tag+"-q0")
            joint=_query(fx,qa,base,("q0","q1","q2") if resume_court or external_case is not None else ("q0","q1"),tag=tag+"-joint")
            # Distinct actual predicates/targets, not repeated identical query.
            atom2=_predicate(fx,qa,_response_leaf(fx,qa,"q1","0"),tag=tag+"-q1-zero") if wide or resume_court else None
            conditional=tuple(_query(fx,qa,atom,(q,),tag=tag+"-"+q) for q in names[2:(52 if wide else 11)])
            alternate=tuple(_query(fx,qa,atom2,(q,),tag=tag+"-alt-"+q) for q in names[30:78]) if wide else ()
            unary=_query(fx,qa,base,("q1",),tag=tag+"-unary")
            grammar=_grammar(operation="I03-OP-"+tag+"-discovery",
                atoms=[_atom("ALL",base,"BRANCH"),_atom("X1",atom,"RESPONSE")],
                templates=[_qt("Y",unary)],rules=[_rule("pair","PAIR_RESPONSE_COTRAVEL","SINGLE_ATOM",
                    atom_ids=("X1",),baseline_atom_id="ALL",query_template_id="Y",
                    validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})])
            discovery=_discovery_authority(fx,grammar,da)
            queries=(joint,*conditional,*alternate,unary)
            preds=(base,atom,atom2) if wide else (base,atom)
            cat=RuntimeObjectCatalog((*fx["authorities"],qa,da),preds,queries,(discovery,))
            if resume_court:
                rare=_predicate(fx,qa,{"op":"AND","children":[
                    {"op":"AND","children":[_response_leaf(fx,qa,"q0","1"),
                                              _response_leaf(fx,qa,"q1","1")]},
                    _response_leaf(fx,qa,"q3","1")]},tag=tag+"-rare")
                forward=_query(fx,qa,atom,("q1",),tag=tag+"-forward")
                inverse=_query(fx,qa,atom2,("q0",),tag=tag+"-inverse")
                rare_query=_query(fx,qa,rare,("q4",),tag=tag+"-rare")
                queries=(*queries,forward,inverse,rare_query)
                preds=(base,atom,atom2,rare)
                cat=RuntimeObjectCatalog((*fx["authorities"],qa,da),preds,queries,(discovery,))
                from rawlsing_next.pre553_empirical_objects import exact_ref
                requests=tuple(I03ExecutionRequest(q.ref,exact_ref(q.condition_predicate_ref))
                               for q in queries)
            else:
                requests=tuple(I03ExecutionRequest(q.ref,base.ref if q in (joint,unary) else atom2.ref if q in alternate else atom.ref) for q in queries)
            if wide:
                self.assertEqual(len({q.ref.key for q in queries}),100)
                self.assertEqual(len(routing),len(chosen)*governed)
            ds=(discovery.ref,);jobs=operation_jobs(requests,ds)
            root=semantic_hash({"fixture":tag});frontier=semantic_hash({"jobs":jobs,"root":root})
            decision=_ref("TEST_ONLY_DECISION",tag);host,purpose="test-country","TEST_ONLY_COUNTRY_ECONOMICS"
            descriptor=dict(source_edition=sha,native_item_ids=list(names),release_tag=projection.instrument_release_id,
                routing_and_risk={"fixture":True},carrier={"kind":"COUNTRY_NUMERIC"},country_and_population={"fixture":country},
                weight_design_estimand={"measure":"RAW"},missing_and_occurrence_policy={"fixture":True},
                target_conditioner_roles={"joint":["q0","q1","q2"] if resume_court or external_case is not None else ["q0","q1"]})
            workload=NativeWorkload(decision_ref=decision,source_factory_ref=_ref("TEST_ONLY_FACTORY",tag),
                descriptor=canonical(descriptor),projection=projection,catalog=cat,requests=requests,discoveries=ds,
                original_u_root=root,expected_frontier_root=frontier)
            if direct_pack:
                # Independently issue the old canonical envelope using the
                # original producer stream, not the packed lane's own hash.
                # This is the same full wire, with no simultaneous object graph.
                digest=hashlib.sha256()
                for part in issued._routing_envelope_parts(workload):
                    if part is not None:
                        digest.update(part)
                    else:
                        digest.update(b"[")
                        count=0
                        for fact in original_routes():
                            if count:
                                digest.update(b",")
                            digest.update(issued.canonical_json(fact.as_dict()).encode("utf-8"))
                            count+=1
                        self.assertEqual(count,len(routing))
                        digest.update(b"]")
                issued_hash=digest.hexdigest()
                self.assertEqual(issued._stream_workload_digest(workload),issued_hash)
            else:
                issued_hash=semantic_hash(workload.envelope())
            record=IssuedWorkloadRecord(decision_ref=decision,source_permission_ref=_ref("TEST_ONLY_SOURCE_PERMISSION",tag),
                scientific_permission_refs=(_ref("TEST_ONLY_SCIENCE_PERMISSION",tag),),host=host,purpose=purpose,source_sha256=sha,
                envelope_sha256=issued_hash,original_u_root=root,expected_frontier_root=frontier,
                expected_jobs=jobs,currentness="CURRENT_GRANTED",scope="TEST_ONLY_SOURCEFREE",native_universe_refs=(universe.ref,))
            resolver=TestOnlyDecisionResolver(record)
            if external_case is not None:
                return workload,record,queries,host,purpose,qrefs
            if session_court:
                return self._distinct_country_workloads(p,db,receipt,workload,record,host,purpose)
            if resume_court:
                return self._country_continuity(p,db,receipt,products,workload,resolver,
                                                record,queries,host,purpose,selected,qrefs)
            from rawlsing_next.pre553_source_backed_c11_facade import _cache_projection_preimage,CONTRACT_ID
            if direct_pack:
                # Independent canonical projection hash, exact original
                # routing bodies streamed one at a time as above.
                from dataclasses import fields
                h=hashlib.sha256()
                def emit(value):
                    h.update(issued.canonical_json(value).encode("utf-8"))
                h.update(b'{"contract":')
                emit(CONTRACT_ID)
                h.update(b',"projection":{')
                for i,f in enumerate(sorted(fields(projection),key=lambda f:f.name)):
                    if i:
                        h.update(b",")
                    emit(f.name)
                    h.update(b":")
                    if f.name=="routing":
                        h.update(b"[")
                        for j,fact in enumerate(original_routes()):
                            if j:
                                h.update(b",")
                            emit(fact.as_dict())
                        h.update(b"]")
                    else:
                        emit(_cache_projection_preimage(getattr(projection,f.name)))
                h.update(b"}}")
                self.assertEqual(projection.cache_identity,h.hexdigest())
            else:
                self.assertEqual(projection.cache_identity,semantic_hash({
                    "contract":CONTRACT_ID,"projection":_cache_projection_preimage(projection)}))
            projection_seconds=time.monotonic()-t
            print("COUNTRY_NATIVE_SCALE_START",json.dumps({"rows":n,"country_rows":len(chosen),"physical_width":len(frame.columns),
                "governed_width":governed,"units":len(jobs),"country_bytes":receipt.bytes,
                "source_bytes":original_bytes,"build_seconds":build_seconds,"projection_seconds":projection_seconds,
                "direct_packed_producer":direct_pack}),flush=True)
            # Inclusive wall time/calls: nested counters deliberately NOT
            # summed. Retain actual incumbent query and publication owners.
            from rawlsing_next import pre553_issued_workload as issued
            from rawlsing_next import pre553_saved_durable_delivery as delivery
            from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
            if not direct_pack:
                # Matched admission microcomparison on the exact same governed
                # workload and runner, using the frozen pre-repair algorithms.
                old_times,new_times=[],[]
                for _ in range(3):
                    t0=time.monotonic()
                    with patch.object(issued,"material",_legacy_material):
                        old_hash=_legacy_semantic_hash(workload.envelope())
                    old_times.append(time.monotonic()-t0)
                    t0=time.monotonic()
                    new_hash=semantic_hash(workload.envelope())
                    new_times.append(time.monotonic()-t0)
                    self.assertEqual(old_hash,new_hash)
                    self.assertEqual(new_hash,record.envelope_sha256)
                self.assertEqual(issued._stream_workload_digest(workload),record.envelope_sha256)
                print("COUNTRY_ADMISSION_SERIALIZATION_MATCHED",json.dumps({
                    "old_median_s":median(old_times),"new_median_s":median(new_times),
                    "same_exact_hash":True,"repetitions":3}),flush=True)
                prepared=issued._PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256)
                self.assertIsNotNone(prepared)
                self.assertEqual(prepared.digest(),record.envelope_sha256)
                self.assertLess(prepared.retained_pin_bytes,prepared.encoded_routing_bytes//2)
                compact=issued._PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256,max_bytes=512*1024)
                self.assertIsNotNone(compact)
                self.assertIsNone(compact.fast_pins)
                self.assertEqual(compact.digest(),record.envelope_sha256)
                self.assertLess(compact.retained_pin_bytes,compact.encoded_routing_bytes//20)
                del compact
                # Envelope mechanics above the previous 16,384-record cap. This
                # deliberately repeated routing list is NOT a valid C11 release;
                # it tests only exact digest streaming and bounded retention.
                if not wide:
                    mechanical=replace(workload,projection=replace(workload.projection,
                        routing=workload.projection.routing*3))
                    wide_hash=semantic_hash(mechanical.envelope())
                    wide_prepared=issued._PreparedRoutingEnvelope.prepare(mechanical,wide_hash,max_bytes=1024*1024)
                    self.assertIsNotNone(wide_prepared)
                    self.assertEqual(wide_prepared.digest(),wide_hash)
                    self.assertGreater(wide_prepared.encoded_routing_bytes,32*1024*1024)
                    self.assertLess(wide_prepared.retained_pin_bytes,1024*1024)
                    print("COUNTRY_ROUTING_WIDE_ENVELOPE",json.dumps({
                        "records":len(wide_prepared.routing),
                        "encoded_bytes_avoided":wide_prepared.encoded_routing_bytes,
                        "retained_pin_bytes_estimate":wide_prepared.retained_pin_bytes,
                        "exact_hash_equal":True}),flush=True)
                    del wide_prepared,mechanical
                self.assertIsNone(issued._PreparedRoutingEnvelope.prepare(
                    workload,record.envelope_sha256,max_bytes=16))
                # A prepared fast path must not recreate canonical per-route
                # tuples. Mutating a *nested* reference must still be detected.
                # Explicitly require the fast layout at this fixture geometry.
                self.assertIsNotNone(prepared.fast_pins)
                self.assertIsNotNone(prepared.fast_ref_pins)
                with patch.object(issued,"_routing_pin",side_effect=AssertionError("repacked route")):
                    self.assertEqual(prepared.digest(),record.envelope_sha256)
                ref=workload.projection.routing[0].producer_replay_locator_or_reference_root
                old=ref.content_hash
                try:
                    object.__setattr__(ref,"content_hash","0"*64)
                    self.assertIsNone(prepared.digest())
                    with self.assertRaises(issued.WorkloadAdmissionError):
                        issued._admit(workload,resolver,host=host,purpose=purpose,
                            allow_test_only=True,prepared=prepared)
                finally:
                    object.__setattr__(ref,"content_hash",old)
                auth=workload.projection.routing[-1].authority_snapshot_refs[0]
                old=auth.authority_content_hash
                try:
                    object.__setattr__(auth,"authority_content_hash","0"*64)
                    self.assertIsNone(prepared.digest())
                finally:
                    object.__setattr__(auth,"authority_content_hash",old)
                # Reject substituted body/tuple and re-hash all nonrouting input.
                obj=workload.projection.routing[0]
                prior=obj.typed_state
                try:
                    object.__setattr__(obj,"typed_state","NOT_ASKED")
                    self.assertIsNone(prepared.digest())
                    with self.assertRaises(issued.WorkloadAdmissionError):
                        issued._admit(workload,resolver,host=host,purpose=purpose,
                            allow_test_only=True,prepared=prepared)
                finally:
                    object.__setattr__(obj,"typed_state",prior)
                prior_routing=workload.projection.routing
                try:
                    object.__setattr__(workload.projection,"routing",tuple(reversed(prior_routing)))
                    self.assertIsNone(prepared.digest())
                    with self.assertRaises(issued.WorkloadAdmissionError):
                        issued._admit(workload,resolver,host=host,purpose=purpose,
                            allow_test_only=True,prepared=prepared)
                finally:
                    object.__setattr__(workload.projection,"routing",prior_routing)
                prior_descriptor=workload.descriptor
                try:
                    changed=json.loads(prior_descriptor)
                    changed["routing_and_risk"]={"fixture":"different"}
                    object.__setattr__(workload,"descriptor",canonical(changed))
                    self.assertNotEqual(prepared.digest(),record.envelope_sha256)
                    with self.assertRaises(issued.WorkloadAdmissionError):
                        issued._admit(workload,resolver,host=host,purpose=purpose,
                            allow_test_only=True,prepared=prepared)
                finally:
                    object.__setattr__(workload,"descriptor",prior_descriptor)
                resolver._record=replace(record,currentness="REVOKED")
                try:
                    with self.assertRaises(issued.WorkloadAdmissionError):
                        issued._admit(workload,resolver,host=host,purpose=purpose,
                            allow_test_only=True,prepared=prepared)
                finally:
                    resolver._record=record
                prepared_times=[]
                for _ in range(3):
                    t0=time.monotonic()
                    self.assertEqual(prepared.digest(),record.envelope_sha256)
                    prepared_times.append(time.monotonic()-t0)
                print("COUNTRY_PREPARED_ENVELOPE_MATCHED",json.dumps({
                    "normal_median_s":median(new_times),"prepared_median_s":median(prepared_times),
                    "encoded_routing_bytes_avoided":prepared.encoded_routing_bytes,
                    "retained_pin_bytes_estimate":prepared.retained_pin_bytes,"routing_records":len(prepared.routing),
                    "fast_pin_tuples":prepared.fast_pins is not None,
                    "exact_hash_equal":True}),flush=True)
                del prepared
                # Move to the producer's detached field-grain representation
                # before actual country execution. Keep the old hostile court
                # above; the new input must preserve its independently issued
                # envelope and projection identities, not issue a new decision.
                from rawlsing_next.pre553_source_backed_c11_facade import _PackedRoutingFacts
                old_identity=projection.cache_identity
                packed=_PackedRoutingFacts(iter(routing))
                self.assertEqual(len(packed),len(routing))
                self.assertEqual(packed[0].as_dict(),routing[0].as_dict())
                self.assertEqual(packed[-1].as_dict(),routing[-1].as_dict())
                self.assertEqual(packed.row_ref(-1),routing[-1].ref)
                self.assertTrue(all(a==issued.canonical_json(b.as_dict()).encode("utf-8")
                                    for a,b in zip(packed.canonical_rows(),routing)))
                workload=replace(workload,projection=replace(projection,routing=packed))
                self.assertEqual(workload.projection.cache_identity,old_identity)
                self.assertEqual(issued._stream_workload_digest(workload),record.envelope_sha256)
            else:
                packed=routing
                self.assertIs(workload.projection.routing,packed)
            packed_prepared=issued._PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256)
            self.assertIsNotNone(packed_prepared)
            self.assertEqual(packed_prepared.digest(),record.envelope_sha256)
            self.assertLess(packed.payload_bytes,packed_prepared.encoded_routing_bytes//3)
            self.assertIsNotNone(packed_prepared.nonrouting_pin)
            with patch.object(_PackedRoutingFacts,"canonical_rows",side_effect=AssertionError("rescanned routing")), \
                 patch.object(issued,"_routing_envelope_parts",side_effect=AssertionError("reserialized nonrouting")):
                self.assertEqual(packed_prepared.digest(),record.envelope_sha256)
            # Every actual nested ref and semantic preimage remains pinned;
            # equal nominal object identities are not an authorization shortcut.
            for owner,field,changed in (
                (workload,"descriptor",canonical({**json.loads(workload.descriptor),"routing_and_risk":{"fixture":False}})),
                (workload.projection.respondents[0].empirical_universe_ref,"content_hash","0"*64),
                (workload.catalog.queries[0],"typed_state","INVALID_UNRESOLVED"),
                (workload.requests[0].query_ref,"content_hash","0"*64),
                (workload.projection.response_slots[0].values[0],"physical_key","changed"),
            ):
                prior=getattr(owner,field)
                try:
                    object.__setattr__(owner,field,changed)
                    self.assertIsNone(packed_prepared.digest(),field)
                finally:
                    object.__setattr__(owner,field,prior)
            self.assertEqual(packed_prepared.digest(),record.envelope_sha256)
            # An instance-level serializer override may not inherit a pin.
            target=workload.catalog.queries[0]
            try:
                object.__setattr__(target,"as_dict",lambda: {})
                self.assertIsNone(packed_prepared.digest())
            finally:
                object.__delattr__(target,"as_dict")
            self.assertEqual(packed_prepared.digest(),record.envelope_sha256)
            bounded=issued._PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256,max_bytes=1024)
            self.assertIsNone(bounded.nonrouting_pin)
            self.assertEqual(bounded.digest(),record.envelope_sha256)
            del bounded
            storage=packed._storage
            try:
                object.__setattr__(packed,"_storage",((),()))
                self.assertIsNone(packed_prepared.digest())
                with self.assertRaises(issued.WorkloadAdmissionError):
                    issued._admit(workload,resolver,host=host,purpose=purpose,
                                  allow_test_only=True,prepared=packed_prepared)
            finally:
                object.__setattr__(packed,"_storage",storage)
            # A malformed geometry may not hash one row stream and expose
            # another through random access; refuse before preparing it.
            from rawlsing_next.pre553_source_backed_c11_facade import SourceBackedC11FacadeError
            runs,ends=storage
            for bad in ((runs,(*ends[:-1],ends[-1]+1)),
                        (runs,()),(((*runs[0][:-1],runs[0][-1][:-1]),*runs[1:]),ends)):
                try:
                    object.__setattr__(packed,"_storage",bad)
                    with self.assertRaises(SourceBackedC11FacadeError):
                        issued._PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256)
                finally:
                    object.__setattr__(packed,"_storage",storage)
            print("COUNTRY_PACKED_ROUTING",json.dumps({
                "records":len(packed),"payload_bytes":packed.payload_bytes,
                "canonical_bytes":packed_prepared.encoded_routing_bytes,
                "additional_pin_bytes_estimate":packed_prepared.retained_pin_bytes,
                "nonrouting_pin_bytes_estimate":packed_prepared.nonrouting_pin.retained_bytes,
                "exact_envelope_and_projection":True}),flush=True)
            del packed_prepared,routing,projection
            if not direct_pack:
                del prior_routing,ref,auth,obj
            print("COUNTRY_NATIVE_PRE_EXECUTION_RSS",json.dumps({
                "peak_process_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "direct_packed_producer":direct_pack}),flush=True)
            from rawlsing_next import pre553_c11_ingest as c11_ingest
            timings=defaultdict(list)
            def time_call(owner,name,label):
                original=getattr(owner,name)
                @wraps(original)
                def wrapped(*args,**kwargs):
                    started=time.monotonic()
                    try:
                        return original(*args,**kwargs)
                    finally:
                        timings[label].append(time.monotonic()-started)
                return patch.object(owner,name,wrapped)
            with ExitStack() as stack:
                for owner,name,label in (
                    (issued,"_admit","issued_full_admission"),
                    (issued._PreparedRoutingEnvelope,"digest","prepared_routing_digest"),
                    (issued._PreparedRoutingEnvelope,"prepare","routing_preparation"),
                    (issued.NativeWorkload,"envelope","full_workload_envelope"),
                    (issued,"build_source_backed_c11_repository","cold_native_prepare"),
                    (c11_ingest,"_all_nonmanifest_refs","replay_closure_census"),
                    (c11_ingest,"_candidate_projection_semantic_hash","replay_projection_hash"),
                    (delivery,"_record","delivery_full_admission"),
                    (delivery,"_s04_manifest","prepublish_s04_manifest"),
                    (delivery,"_graph","durable_graph"),
                    (issued.NativeWorkloadResult,"exact_s2e_output_census","native_output_census"),
                    (CarrierNeutralResearchExecutor,"execute_i03","native_I03"),
                    (CarrierNeutralResearchExecutor,"execute_i05","native_I05"),
                    (CountryReader,"_column","authenticated_column_read_decode"),
                    (CountryReader,"verify_full","full_file_authentication"),
                    (delivery,"publish_empirical_closure","durable_publish"),
                ):
                    stack.enter_context(time_call(owner,name,label))
                pub=execute_publish_country(workload,resolver,host=host,purpose=purpose,country_path=db,
                    country_receipt=receipt,root_dir=products)
            print("COUNTRY_NATIVE_PHASES",json.dumps({k:{"calls":len(v),"total_s":sum(v),
                "median_s":median(v),"max_s":max(v)} for k,v in timings.items()}),flush=True)
            self.assertTrue(pub.complete)
            self.assertEqual(len(timings["routing_preparation"]),1)
            self.assertEqual(pub.batch_census["unit_count"],len(jobs))
            self.assertIsNotNone(pub.release_identity)
            db.unlink()
            # A real cold selected read before the complete archive open,
            # no original source or country file, no unrelated body hydration.
            selected_plan=((queries[0].ref,0),(queries[-1].ref,None))
            selected_kwargs=dict(expected_root=pub.receipt.root_identity,
                expected_release_ref=pub.release_identity.release_ref,country_receipt=receipt,
                workload=workload,resolver=resolver,host=host,purpose=purpose,requests=selected_plan)
            t_selected=time.monotonic()
            with patch.object(delivery,"open_empirical_closure",side_effect=AssertionError("full archive expansion")):
                selective=delivery.read_country_s04_selected(pub.receipt.root_path,**selected_kwargs)
            selective_s=time.monotonic()-t_selected
            self.assertEqual(len(selective.reads),2)
            self.assertEqual(len(selective.selected_unit_hashes),2)
            self.assertIn("NOT_FULL_ARCHIVE_AUDIT",selective.verification_scope)
            print("COUNTRY_COLD_SELECTED_READ",json.dumps({"units":2,"seconds":selective_s,
                "blobs_read":selective.blobs_read,"scope":selective.verification_scope}),flush=True)
            t=time.monotonic()
            timings.clear()
            with ExitStack() as stack:
                for owner,name,label in (
                    (issued.NativeWorkload,"envelope","cold_full_envelope"),
                    (issued._PreparedRoutingEnvelope,"digest","cold_prepared_routing_digest"),
                    (issued._PreparedRoutingEnvelope,"prepare","cold_routing_preparation"),
                    (delivery,"_record","cold_full_admission"),
                    (delivery,"open_empirical_closure","cold_closure_open"),
                    (delivery,"census_native_batch","cold_census"),
                    (delivery,"_graph","cold_graph"),
                    (delivery,"_read_s04","actual_cold_s04"),
                ):
                    stack.enter_context(time_call(owner,name,label))
                cold=open_country_product(pub.receipt.root_path,expected_root=pub.receipt.root_identity,
                    expected_release_ref=pub.release_identity.release_ref,country_receipt=receipt,workload=workload,
                    resolver=resolver,host=host,purpose=purpose)
                self.assertEqual(len(timings["cold_routing_preparation"]),1)
                plans=tuple((q.ref,0 if q==joint else None) for q in queries)
                t_bulk=time.monotonic()
                reads=cold.read_s04_many(plans)
                bulk_s=time.monotonic()-t_bulk
                self.assertEqual(len(reads),len(queries))
                print("COUNTRY_COLD_BULK_READ",json.dumps({"units":len(reads),"seconds":bulk_s}),flush=True)
                for i in (0,len(queries)-1):
                    single=cold.read_s04(plans[i][0],conditioner_index=plans[i][1])
                    self.assertEqual(delivery._s04_refs(single),delivery._s04_refs(reads[i]))
                self.assertEqual(tuple(delivery._s04_refs(x) for x in selective.reads),
                                 (delivery._s04_refs(reads[0]),delivery._s04_refs(reads[-1])))
                for q,read in zip(queries,reads):
                    fact=read.first_consumer.execution.facts[0]
                    mask=(np.ones(len(chosen),dtype=bool) if q in (joint,unary)
                          else selected[:,1]==0 if q in alternate else selected[:,0]==1)
                    self.assertEqual(fact.raw_denominator_support,int(mask.sum()))
                    from rawlsing_next.tests.test_pre553_empirical_query import _cell_map
                    reverse={ref.key:i for i,(name,ref) in enumerate(qrefs.items())}
                    from rawlsing_next.pre553_empirical_objects import exact_ref
                    target_indices=tuple(reverse[exact_ref(ref).key] for ref in q.target_refs)
                    cells=_cell_map(fact)
                    for cell,row in cells.items():
                        vals=(cell,) if isinstance(cell,str) else cell
                        expected_cell=mask.copy()
                        for col,val in zip(target_indices,vals):
                            expected_cell &= selected[:,col]==int(val)
                        self.assertEqual(row["raw_numerator_support"],int(expected_cell.sum()))
                    if q==joint:
                        self.assertEqual(read.first_consumer.ff01.semantic_projection()["raw_fully_resolved_joint_n"],len(chosen))
            # Measure actual unique retained files in the dedicated estate,
            # not merely the per-closure reference census. st_blocks counts
            # filesystem allocation, not logical bytes or process memory.
            physical_files=tuple(f for f in products.rglob("*") if f.is_file())
            unique_bytes=sum(f.stat().st_size for f in physical_files)
            allocated_bytes=sum(f.stat().st_blocks*512 for f in physical_files)
            self.assertEqual(unique_bytes,pub.receipt.cas_new_bytes+pub.receipt.manifest_bytes)
            print("COUNTRY_CLOSURE_FOOTPRINT",json.dumps({
                "unique_file_bytes":unique_bytes,"allocated_file_bytes":allocated_bytes,
                "file_count":len(physical_files),"manifest_bytes":pub.receipt.manifest_bytes,
                "logical_manifest_bytes":len(issued.canonical_json(cold._closure.manifest).encode("utf-8")),
                "cas_new_bytes":pub.receipt.cas_new_bytes,
                "referenced_bytes":pub.receipt.referenced_physical_bytes,
                "peak_publish_scratch_bytes":pub.receipt.peak_scratch_bytes}),flush=True)
            print("COUNTRY_COLD_PHASES",json.dumps({k:{"calls":len(v),"total_s":sum(v),
                "median_s":median(v),"max_s":max(v)} for k,v in timings.items()}),flush=True)
            # Selected read must not touch unrelated fact blobs. Full audit
            # must still refuse their absence, and selected corruption refuses.
            if not wide:
                from rawlsing_next import pre553_durable_empirical_closure as durable
                entries={issued.exact_ref(x["ref"]).key:x for x in cold._closure.manifest["core"]["objects"]}
                selected_fact=reads[0].first_consumer.execution.facts[0]
                unrelated_fact=reads[1].first_consumer.execution.facts[0]
                def blob_for(fact):
                    return products/durable.CAS_DIR/durable.BLOB_DIR/(entries[fact.ref.key]["document_hash"]+durable.BLOB_SUFFIX)
                self.assertLess(selective.blobs_read,len(tuple((products/durable.CAS_DIR/durable.BLOB_DIR).glob("*"))))
                unrelated=blob_for(unrelated_fact);backup=unrelated.read_bytes();unrelated.unlink()
                try:
                    again=delivery.read_country_s04_selected(pub.receipt.root_path,**selected_kwargs)
                    self.assertEqual(tuple(delivery._s04_refs(x) for x in again.reads),
                                     tuple(delivery._s04_refs(x) for x in selective.reads))
                    with self.assertRaises(durable.DurableEmpiricalClosureError):
                        durable.open_empirical_closure(pub.receipt.root_path,expected_root=pub.receipt.root_identity)
                finally:
                    unrelated.write_bytes(backup)
                selected_blob=blob_for(selected_fact);backup=selected_blob.read_bytes();selected_blob.unlink()
                try:
                    with self.assertRaises(durable.DurableEmpiricalClosureError):
                        delivery.read_country_s04_selected(pub.receipt.root_path,**selected_kwargs)
                finally:
                    selected_blob.write_bytes(backup)
                with self.assertRaises(durable.DurableEmpiricalClosureError):
                    delivery.read_country_s04_selected(pub.receipt.root_path,**{**selected_kwargs,"expected_root":"0"*64})
                resolver._record=replace(record,currentness="REVOKED")
                try:
                    with self.assertRaises(issued.WorkloadAdmissionError):
                        delivery.read_country_s04_selected(pub.receipt.root_path,**selected_kwargs)
                finally:
                    resolver._record=record
            result,=cold._closure.discovery_results
            self.assertEqual(result.candidate_count,result.covered_candidate_count)
            self.assertEqual(result.candidate_count,1)
            print("COUNTRY_NATIVE_SCALE_RESULT",json.dumps({"native_and_s04_seconds":pub.execution_seconds,
                "publication_seconds":pub.publication_seconds,"cold_s04_seconds":time.monotonic()-t,
                "closure_referenced_bytes":pub.receipt.referenced_physical_bytes,
                "peak_process_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "direct_packed_producer":direct_pack,
                "grade":"SOURCEFREE_256x300_80_GOVERNED_100_I03_NOT_ORIGINAL" if wide else "SOURCEFREE_400x41_16_GOVERNED_NOT_ORIGINAL"}),flush=True)


    def test_grouped_country_campaign_economics(self):
        """Real country/U43/Batch/S2F court; not #1001 terminal qualification."""
        import os
        location=os.environ.get("PYAT_R9_CAMPAIGN_ROOT")
        if not location:
            self.skipTest("run via tools.pyat_country_campaign_court")
        import gc
        from rawlsing_next import pre553_country_numeric_carrier as carrier
        from rawlsing_next import pre553_source_backed_c11_facade as facade
        from rawlsing_next import pre553_issued_workload as issued
        from rawlsing_next import pre553_saved_durable_delivery as delivery
        from rawlsing_next import pre553_durable_empirical_closure as durable
        from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
        from rawlsing_next.tests.test_pre553_empirical_query import _cell_map
        from rawlsing_next.pre553_empirical_objects import exact_ref
        from collections import Counter
        from dataclasses import asdict

        root=Path(location)
        self.assertTrue(root.is_dir())
        risk_mode=os.environ.get("PYAT_R10_REPLAY_RISK","factored")
        self.assertIn(risk_mode,("legacy","factored"))
        factor_risk=risk_mode=="factored"
        campaign_proofs=[]
        countries=root/"countries";countries.mkdir()
        products=root/"products";products.mkdir()
        sizes=tuple(int(x) for x in os.environ.get("PYAT_R9_COUNTRY_ROWS","128,192,256").split(","))
        self.assertEqual(len(sizes),3)
        self.assertTrue(all(n>=32 for n in sizes))
        labels=np.array([c for i in range(max(sizes)) for c,n in zip("ABC",sizes) if i<n])
        rng=np.random.default_rng(931)
        n=len(labels);governed=80;extra=218
        values=rng.integers(0,2,(n,governed))
        # Real heterogeneity across independently qualified universes.
        # Force all four X/Y configurations; A and B have opposing XORs.
        for country in "ABC":
            indices=np.flatnonzero(labels==country)
            values[indices,0]=np.arange(len(indices))%2
            values[indices,1]=(np.arange(len(indices))//2)%2
            if country in "AB":
                values[indices,2]=values[indices,0]^values[indices,1]^(country=="B")
        data={"q"+str(i):values[:,i].astype(str) for i in range(governed)}
        for i in range(extra):
            data["v"+str(i)]=(np.arange(n,dtype=np.float64)*(1.000001+i*.00001)+i*.001
                             if i%2 else (np.arange(n)+i)%7)
        data["G"]=labels;data["W"]=1.+(np.arange(n)%3)
        frame=pd.DataFrame(data)
        phase_file=root/"phase.json"
        def phase(name):
            tmp=phase_file.with_suffix(".tmp")
            tmp.write_text(json.dumps({"phase":name}),encoding="utf-8")
            tmp.replace(phase_file)
        def footprint(path):
            seen=set();size=allocated=files=0
            for f in path.rglob("*"):
                if not f.is_file():continue
                st=f.stat();key=(st.st_dev,st.st_ino)
                if key in seen:continue
                seen.add(key);size+=st.st_size
                allocated+=getattr(st,"st_blocks",0)*512;files+=1
            return {"logical_file_bytes":size,"allocated_bytes":allocated,"file_count":files}
        def elapsed(fn):
            wall=time.monotonic();cpu=time.process_time()
            result=fn()
            return result,{"wall_s":time.monotonic()-wall,"worker_cpu_s":time.process_time()-cpu}
        phase("source_generation")
        src=root/"survey.sav"
        shared=os.environ.get("PYAT_R10_SHARED_SOURCE")
        def create_source():
            import shutil
            if shared and Path(shared).is_file():
                shutil.copyfile(shared,src)
            else:
                pyreadstat.write_sav(frame,str(src))
                if shared:
                    shutil.copyfile(src,shared)
        _,source_time=elapsed(create_source)
        source_bytes=src.stat().st_size
        sha=hashlib.sha256(src.read_bytes()).hexdigest()
        del frame,data
        progress=[]
        def build():
            with decode_sav(src,expected_source_sha256=sha) as inc:
                ordinals={v.name:v.ordinal for v in inc.variables}
                built=list(carrier.build_country_set(inc,country_variable="G",root=countries,
                    require_current=lambda:True,max_open_countries=3,block_rows=256,
                    on_progress=lambda state:progress.append(dict(state))))
            return ordinals,built
        phase("grouped_country_build")
        (ordinals,built),build_time=elapsed(build)
        self.assertEqual(len(built),3)
        self.assertEqual(sum(r.country_rows for _,r in built),n)
        self.assertEqual(sum(p["phase"]=="SOURCE_SCAN" for p in progress),1)
        self.assertEqual(sum(p["phase"]=="CENSUS" for p in progress),1)
        receipts={}
        seen=set()
        phase("physical_census")
        for db,receipt in built:
            country=json.loads(receipt.country_key)["v"]
            self.assertIn(country,"ABC")
            indices=np.flatnonzero(labels==country)
            rows=tuple(int(i+1) for i in indices)
            with CountryReader(db,receipt,require_current=lambda:True) as reader:
                self.assertEqual(tuple(reader.row_ordinals()),rows)
                self.assertEqual(len(reader.variables),300)
                # Independent per-country high-cardinality physical scan.
                self.assertEqual(tuple(reader.matching_rows({"q0":"1"})),
                    tuple(int(i+1) for i in indices if values[i,0]==1))
            self.assertFalse(seen.intersection(rows));seen.update(rows)
            receipts[country]=(db,receipt)
        self.assertEqual(seen,set(range(1,n+1)))
        self.assertEqual(len({r.sha256 for _,r in built}),3)
        country_footprint=footprint(countries)
        # Original generated source not necessary to execute or serve.
        src.unlink()
        print("R9_COUNTRY_BUILD",json.dumps({"source_rows":n,"country_rows":sizes,
            "physical_width":300,"governed_width":80,"source_bytes":source_bytes,
            "source_generation":source_time,"grouped_build":build_time,
            "source_scan_groups":1,"census_passes":1,"country_files":country_footprint,
            "country_receipts":[asdict(r) for _,r in built]}),flush=True)

        def issue(workload,record,tag,requests,discoveries):
            decision=_ref("TEST_ONLY_DECISION",tag)
            jobs=operation_jobs(requests,discoveries)
            u=semantic_hash({"fixture":tag})
            frontier=semantic_hash({"jobs":jobs,"root":u})
            item=replace(workload,decision_ref=decision,requests=requests,
                         discoveries=discoveries,original_u_root=u,expected_frontier_root=frontier)
            grant=replace(record,decision_ref=decision,expected_jobs=jobs,
                original_u_root=u,expected_frontier_root=frontier,
                envelope_sha256=issued._stream_workload_digest(item))
            return item,TestOnlyDecisionResolver(grant)
        def fixture(country):
            db,receipt=receipts[country]
            indices=np.flatnonzero(labels==country)
            selected=values[indices,:]
            ext=dict(root=root,db=db,receipt=receipt,ordinals=ordinals,
                     selected=selected,chosen=tuple(int(i+1) for i in indices),country=country)
            return self._native_batch(wide=True,external_case=ext),selected
        def common(item,resolver,pub,receipt,host,purpose):
            return dict(expected_root=pub.receipt.root_identity,
                expected_release_ref=pub.release_identity.release_ref,country_receipt=receipt,
                workload=item,resolver=resolver,host=host,purpose=purpose)
        def check_counts(read,query,mask,selected,qrefs):
            fact=read.first_consumer.execution.facts[0]
            self.assertEqual(fact.raw_denominator_support,int(mask.sum()))
            axes=tuple({r.key:i for i,r in enumerate(qrefs.values())}[exact_ref(r).key]
                       for r in query.target_refs)
            cells=_cell_map(fact)
            self.assertEqual(len(cells),2**len(axes))
            for cell,row in cells.items():
                vals=(cell,) if isinstance(cell,str) else cell
                check=mask.copy()
                for axis,val in zip(axes,vals):
                    check &= selected[:,axis]==int(val)
                self.assertEqual(row["raw_numerator_support"],int(check.sum()))

        # These are inclusive call-boundary measurements, not additive
        # categories. No mock substitutes for native execution/publication.
        phase_stats=defaultdict(list)
        actual=[]
        def measured(owner,name,label):
            original=getattr(owner,name)
            @wraps(original)
            def invoke(*args,**kwargs):
                started=time.monotonic()
                try:
                    if label=="native_i03":actual.append(("QUERY",kwargs["query_ref"].key))
                    if label=="native_i05":actual.append(("DISCOVERY",kwargs["discovery_authority_ref"].key))
                    return original(*args,**kwargs)
                finally:
                    phase_stats[label].append(time.monotonic()-started)
            return patch.object(owner,name,invoke)
        def stats():
            return {k:{"calls":len(v),"inclusive_wall_s":sum(v),
                       "median_s":median(v),"max_s":max(v)} for k,v in phase_stats.items()}
        monitors=((facade,"_validate_country_produced_release","logical_i02"),
                  (issued,"_admit","issuer_admission"),
                  (carrier.CountryReader,"verify_full","full_file_authentication"),
                  (CarrierNeutralResearchExecutor,"execute_i03","native_i03"),
                  (CarrierNeutralResearchExecutor,"execute_i05","native_i05"),
                  (delivery,"_s04_manifest","s04_first_reads"),
                  (delivery,"publish_empirical_closure","s2f_publication"),
                  (issued.NativeWorkloadResult,"exact_s2e_output_census","s2e_census"))
        archived={}
        def pub_metrics(pub):
            r=pub.receipt
            return {"completed":pub.batch_census["completed_count"],
                    "root":r.root_identity,"publication_s":pub.publication_seconds,
                    "cas_new_bytes":r.cas_new_bytes,"manifest_bytes":r.manifest_bytes,
                    "referenced_bytes":r.referenced_physical_bytes,
                    "publisher_scratch_counter_bytes":r.peak_scratch_bytes,
                    "archive_footprint":footprint(products)}
        for country in "ABC":
            db,receipt=receipts[country]
            phase(country+"_issue")
            ((workload,record,queries,host,purpose,qrefs),selected),issuance=elapsed(lambda:fixture(country))
            phase_stats.clear();actual.clear()
            histories=[];pins=[];runs=[]
            phase(country+"_investigations")
            with ExitStack() as stack:
                for owner,name,label in monitors:stack.enter_context(measured(owner,name,label))
                session=stack.enter_context(carrier.CountryWorkloadSession(db,receipt,require_current=lambda:True))
                # Intentionally overlapping investigations: 1, 10, then
                # all 100 distinct I03 operations plus one I05. Different
                # issuer decisions, not artificially cached answers.
                for count in (1,10,100):
                    ds=workload.discoveries if count==100 else ()
                    item,resolver=issue(workload,record,country+"-"+str(count),workload.requests[:count],ds)
                    checkpoints=[]
                    def retain(pin,pub):
                        pins.append(pin)
                        checkpoints.append(pub_metrics(pub))
                    args=dict(checkpoint_every=34,checkpoint_observer=retain) if count==100 else {}
                    phase(country+"_investigation_"+str(count))
                    before=len(actual)
                    pub,timing=elapsed(lambda:session.publish(item,resolver,host=host,purpose=purpose,
                                                             root_dir=products,
                                                             factor_replay_risk_members=factor_risk,**args))
                    self.assertTrue(pub.complete)
                    self.assertEqual(pub.batch_census["completed_count"],count+len(ds))
                    campaign_proofs.append({"country":country,"count":count,
                        "census":semantic_hash(pub.batch_census),
                        "release":semantic_hash(pub.release_identity.as_dict())})
                    expected=Counter(("QUERY",r.query_ref.key) for r in item.requests)
                    expected.update(("DISCOVERY",r.key) for r in ds)
                    self.assertEqual(Counter(actual[before:]),expected)
                    histories.append({"i03":count,"i05":len(ds),"timing":timing,
                                      "final":pub_metrics(pub),"checkpoints":checkpoints})
                    runs.append((item,resolver,pub))
                self.assertEqual(len(phase_stats["logical_i02"]),1)
                self.assertEqual(len(actual),112)
            self.assertIsNone(session._reader);self.assertIsNone(session._entry)
            measured_stats=stats()
            self.assertEqual([x["completed"] for x in histories[-1]["checkpoints"]],[34,68,101])
            self.assertEqual(len(pins),3)
            # All three independent publications are served through the
            # selected cold reader; the final root also undergoes full open.
            phase(country+"_cold_retrieval")
            retrieval=[]
            for item,resolver,pub in runs:
                plan=((item.requests[0].query_ref,None),)
                result,timing=elapsed(lambda:delivery.read_country_s04_selected(
                    pub.receipt.root_path,**common(item,resolver,pub,receipt,host,purpose),requests=plan))
                check_counts(result.reads[0],queries[0],np.ones(len(selected),dtype=bool),selected,qrefs)
                retrieval.append({"units":1,"timing":timing,"blobs_read":result.blobs_read})
            item,resolver,pub=runs[-1]
            cold,full_open=elapsed(lambda:delivery.open_country_product(
                pub.receipt.root_path,**common(item,resolver,pub,receipt,host,purpose)))
            self.assertTrue(cold.complete)
            # Sample representative condition directions and joint support
            # against the original generated country rows, not another I03.
            sample=(0,1,50,51,98,99)
            plan=tuple((queries[i].ref,None) for i in sample)
            read,timing=elapsed(lambda:cold.read_s04_many(plan))
            for i,result in zip(sample,read):
                mask=(np.ones(len(selected),dtype=bool) if i in (0,99) else
                      selected[:,0]==1 if i<=50 else selected[:,1]==0)
                check_counts(result,queries[i],mask,selected,qrefs)
            direct,selected_time=elapsed(lambda:delivery.read_country_s04_selected(
                pub.receipt.root_path,**common(item,resolver,pub,receipt,host,purpose),requests=plan))
            self.assertEqual(tuple(delivery._s04_refs(r) for r in direct.reads),
                             tuple(delivery._s04_refs(r) for r in read))
            roles=0
            with patch.object(CarrierNeutralResearchExecutor,"execute_i03",
                              side_effect=AssertionError("retained consumer reran I03")):
                for discovery in cold._closure.discovery_results:
                    for candidate in discovery.receipts:
                        for role,refs in candidate.support_uncertainty_state.get("query_role_fact_refs",{}).items():
                            if len(refs)==1:
                                fact,role_receipt=cold.read_i05_role(candidate.ref,role)
                                self.assertTrue(fact.ref and role_receipt.ref);roles+=1
            self.assertGreater(roles,0)
            # Same source SHA is insufficient: another country's physical
            # receipt cannot be used to authorize this archive.
            wrong=receipts["B" if country=="A" else "A"][1]
            with self.assertRaisesRegex(delivery.SavedDeliveryError,"BINDING_DRIFT"):
                delivery.read_country_s04_selected(pub.receipt.root_path,
                    **common(item,resolver,pub,wrong,host,purpose),requests=plan)
            archived[country]=(pub.receipt.root_path,pub.receipt.root_identity,
                              pub.release_identity.release_ref)
            print("R9_COUNTRY_CAMPAIGN",json.dumps({"country":country,"rows":len(selected),
                "issuance":issuance,"investigations":histories,"inclusive_phases":measured_stats,
                "selected_small_reads":retrieval,"full_cold_open":full_open,
                "full_reader_selected_s04":timing,"selected_cold":selected_time,
                "selected_cold_blobs":direct.blobs_read,"retained_i05_roles":roles,
                "independent_source_counts_and_wrong_country_refusal":True}),flush=True)
            # Do not retain three logical graphs or full cold products.
            del cold,read,direct,result,runs,session,workload,record,queries,qrefs,item,resolver,pub,discovery,candidate,fact,role_receipt
            gc.collect()

        # A later return to A, after B and C, reissues a distinct workload.
        # This intentionally pays a new preparation; no cross-country cache.
        phase("return_to_A_issue")
        (workload,record,queries,host,purpose,qrefs),selected=fixture("A")
        db,receipt=receipts["A"]
        item,resolver=issue(workload,record,"A-return",workload.requests[51:61],())
        phase("return_to_A_execute")
        with patch.object(facade,"_validate_country_produced_release",
                          wraps=facade._validate_country_produced_release) as builds:
            pub,timing=elapsed(lambda:delivery.execute_publish_country(item,resolver,
                host=host,purpose=purpose,country_path=db,country_receipt=receipt,root_dir=products,
                factor_replay_risk_members=factor_risk))
            self.assertEqual(builds.call_count,1)
        self.assertEqual(pub.batch_census["completed_count"],10)
        self.assertEqual(pub.release_identity.release_ref,archived["A"][2])
        campaign_proofs.append({"country":"A-return","count":10,
            "census":semantic_hash(pub.batch_census),
            "release":semantic_hash(pub.release_identity.as_dict())})
        # Source and country deletion: old empirical publication survives.
        phase("return_to_A_retained_read")
        old,old_resolver=issue(workload,record,"A-100",workload.requests,workload.discoveries)
        path,root_pin,release=archived["A"]
        db.unlink()
        read,read_time=elapsed(lambda:delivery.read_country_s04_selected(path,
            expected_root=root_pin,expected_release_ref=release,country_receipt=receipt,
            workload=old,resolver=old_resolver,host=host,purpose=purpose,
            requests=((queries[0].ref,None),)))
        check_counts(read.reads[0],queries[0],np.ones(len(selected),dtype=bool),selected,qrefs)
        (root/"campaign-proof.json").write_text(json.dumps({"source_sha256":sha,
            "mode":risk_mode,"proofs":campaign_proofs,"country_files":country_footprint,
            "country_sha256":{key:rec.sha256 for key,(_,rec) in receipts.items()},
            "retained_products":footprint(products),
            "retained_cas":footprint(products/durable.CAS_DIR),
            "retained_manifests":footprint(products/durable.CLOSURES_DIR)},sort_keys=True),encoding="utf-8")
        print("R9_COUNTRY_CAMPAIGN_FINAL",json.dumps({"country_count":3,"distinct_source_rows":n,
            "replay_risk_mode":risk_mode,
            "actual_issued_units":346,"distinct_initial_i03_per_country":100,
            "return_to_A_10_units":timing,"return_to_A_after_country_deleted":read_time,
            "country_files_before_deletion":country_footprint,"retained_products":footprint(products),
            "full_workspace_after_deletion":footprint(root),
            "grade":"SOURCEFREE_THREE_COUNTRY_300_PHYSICAL_80_GOVERNED__NOT_ORIGINAL_OR_100K_FULL_VERTICAL"}),
            flush=True)

    def _distinct_country_workloads(self,root,db,receipt,workload,record,host,purpose):
        from rawlsing_next import pre553_country_numeric_carrier as carrier
        from rawlsing_next import pre553_source_backed_c11_facade as facade
        from rawlsing_next import pre553_issued_workload as issued
        from rawlsing_next import pre553_saved_durable_delivery as delivery
        from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
        from collections import Counter
        import gc

        # Two disjoint, separately issued workloads using one unchanged
        # governed projection and authority catalog. Not cached query results.
        def issue(tag,requests,discoveries):
            decision=_ref("TEST_ONLY_DECISION",tag)
            jobs=operation_jobs(requests,discoveries)
            u=semantic_hash({"fixture":tag})
            frontier=semantic_hash({"jobs":jobs,"root":u})
            item=replace(workload,decision_ref=decision,requests=requests,
                         discoveries=discoveries,original_u_root=u,expected_frontier_root=frontier)
            grant=replace(record,decision_ref=decision,expected_jobs=jobs,
                          original_u_root=u,expected_frontier_root=frontier,
                          envelope_sha256=issued._stream_workload_digest(item))
            return item,TestOnlyDecisionResolver(grant),grant

        half=len(workload.requests)//2
        cases=(issue("country-session-first",workload.requests[:half],()),
               issue("country-session-second",workload.requests[half:],workload.discoveries))
        self.assertFalse(set(q.query_ref for q in cases[0][0].requests)
                         &set(q.query_ref for q in cases[1][0].requests))
        original=db.read_bytes()
        outputs={}
        counts={}
        opens={}
        full_hashes={}
        times={}
        source_build=facade._validate_country_produced_release
        old_init=carrier.CountryReader.__init__
        old_verify=carrier.CountryReader.verify_full
        opened=[]
        authenticated=[]
        def count_open(self,*args,**kwargs):
            opened.append(1)
            return old_init(self,*args,**kwargs)
        def count_verify(self,*args,**kwargs):
            authenticated.append(1)
            return old_verify(self,*args,**kwargs)
        old_i03=CarrierNeutralResearchExecutor.execute_i03
        old_i05=CarrierNeutralResearchExecutor.execute_i05
        actual=[]
        def count_i03(self,**kw):
            actual.append(("QUERY",kw["query_ref"].key))
            return old_i03(self,**kw)
        def count_i05(self,**kw):
            actual.append(("DISCOVERY",kw["discovery_authority_ref"].key))
            return old_i05(self,**kw)
        expected=Counter(("QUERY",r.query_ref.key) for r in workload.requests)
        expected.update(("DISCOVERY",r.key) for r in workload.discoveries)
        # Two alternating matched series, same file, same issued inputs,
        # same publication owners; no cross-host speedup claim.
        for order in (("cold","live"),("live","cold")):
            for mode in order:
                run_id=len(times.get(mode,[]))
                destination=root/(mode+"-"+str(run_id));destination.mkdir()
                gc.collect()
                actual.clear()
                opened.clear()
                authenticated.clear()
                with patch.object(facade,"_validate_country_produced_release",wraps=source_build) as builds, patch.object(
                        CarrierNeutralResearchExecutor,"execute_i03",count_i03), patch.object(
                        CarrierNeutralResearchExecutor,"execute_i05",count_i05), patch.object(
                        carrier.CountryReader,"__init__",count_open), patch.object(
                        carrier.CountryReader,"verify_full",count_verify):
                    started=time.monotonic()
                    if mode=="cold":
                        pubs=[delivery.execute_publish_country(item,resolver,host=host,purpose=purpose,
                              country_path=db,country_receipt=receipt,root_dir=destination)
                              for item,resolver,_ in cases]
                    else:
                        with carrier.CountryWorkloadSession(db,receipt,require_current=lambda:True) as session:
                            pubs=[session.publish(item,resolver,host=host,purpose=purpose,root_dir=destination)
                                  for item,resolver,_ in cases]
                        self.assertIsNone(session._reader)
                        self.assertIsNone(session._entry)
                    elapsed=time.monotonic()-started
                    self.assertEqual(builds.call_count,2 if mode=="cold" else 1)
                    self.assertEqual(Counter(actual),expected)
                    counts[mode]=builds.call_count
                    self.assertEqual(len(opened),2 if mode=="cold" else 1)
                    self.assertEqual(len(authenticated),4)
                    opens[mode]=len(opened)
                    full_hashes[mode]=len(authenticated)
                times.setdefault(mode,[]).append(elapsed)
                semantic=[]
                for (item,resolver,_),pub in zip(cases,pubs):
                    product=delivery.open_country_product(pub.receipt.root_path,
                        expected_root=pub.receipt.root_identity,
                        expected_release_ref=pub.release_identity.release_ref,
                        country_receipt=receipt,workload=item,resolver=resolver,host=host,purpose=purpose)
                    semantic.append((pub.release_identity,pub.batch_census,
                        product._closure.i03_results,tuple(r.replay_ref for r in product._closure.discovery_results),
                        product._receipts))
                if mode in outputs:
                    self.assertEqual(semantic,outputs[mode])
                outputs[mode]=semantic
        self.assertEqual(outputs["cold"],outputs["live"])

        first,first_resolver,_=cases[0]
        second,second_resolver,second_grant=cases[1]
        with carrier.CountryWorkloadSession(db,receipt,require_current=lambda:True) as session:
            session.execute(first,first_resolver,host=host,purpose=purpose)
            # Equal content but a different owned projection instance is a
            # miss, not a detached old body resolver silently rebound.
            with patch.object(facade,"_validate_country_produced_release",wraps=source_build) as builds:
                session.execute(replace(second,projection=replace(second.projection)),
                                second_resolver,host=host,purpose=purpose)
                self.assertEqual(builds.call_count,1)
            second_resolver._record=replace(second_grant,currentness="REVOKED")
            try:
                with patch.object(facade,"_validate_country_produced_release",
                        side_effect=AssertionError("revoked workload prepared")), patch.object(
                        CarrierNeutralResearchExecutor,"execute_i03",
                        side_effect=AssertionError("revoked workload queried")):
                    with self.assertRaises(issued.WorkloadAdmissionError):
                        session.execute(second,second_resolver,host=host,purpose=purpose)
            finally:
                second_resolver._record=second_grant
            self.assertIsNone(session._reader)
        with self.assertRaises(carrier.CountryCarrierError):
            session.execute(first,first_resolver,host=host,purpose=purpose)
        # Even if the stat mutation alarm is defeated, a NEW workload must
        # authenticate the entire retained file before reusing preparation.
        with carrier.CountryWorkloadSession(db,receipt,require_current=lambda:True) as session:
            session.execute(first,first_resolver,host=host,purpose=purpose)
            signature=session._reader._signature
            with db.open("r+b") as stream:
                stream.seek(-1,2)
                stream.write(bytes([original[-1]^1]))
            try:
                with patch.object(carrier,"_stat_signature",return_value=signature), patch.object(
                        CarrierNeutralResearchExecutor,"execute_i03",
                        side_effect=AssertionError("changed file queried")):
                    with self.assertRaisesRegex(carrier.CountryCarrierError,"differs from held receipt"):
                        session.execute(second,second_resolver,host=host,purpose=purpose)
            finally:
                db.write_bytes(original)
            self.assertIsNone(session._reader)
        self.assertEqual(db.read_bytes(),original)
        print("COUNTRY_DISTINCT_WORKLOAD_REUSE",json.dumps({
            "country_rows":receipt.country_rows,"units":sum(len(x[0].requests)+len(x[0].discoveries) for x in cases),
            "actual_preparations":counts,"inventory_opens":opens,
            "full_file_authentications":full_hashes,"seconds":times,
            "median_seconds":{k:median(v) for k,v in times.items()},
            "exact_outputs_and_receipts":True,"independent_issue_revoke_and_full_file_negative":True,
            "grade":"SAME_HOST_SOURCEFREE_LIVE_REUSE_NOT_COLD_PERSISTENT_OR_ORIGINAL"
        }),flush=True)

    def _country_continuity(self,root,db,receipt,products,workload,resolver,record,
                            queries,host,purpose,selected,qrefs):
        from rawlsing_next import pre553_saved_durable_delivery as delivery
        from rawlsing_next import pre553_issued_workload as issued
        from rawlsing_next import pre553_durable_empirical_closure as durable
        from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
        import collections

        common=dict(workload=workload,resolver=resolver,host=host,purpose=purpose,
                    country_receipt=receipt)
        def run(destination,**kwargs):
            return delivery.execute_publish_country(**common,country_path=db,
                                                     root_dir=destination,**kwargs)
        def open_product(pub,**kwargs):
            return delivery.open_country_product(pub.receipt.root_path,
                expected_root=pub.receipt.root_identity,
                expected_release_ref=pub.release_identity.release_ref,**common,**kwargs)
        captured=[]
        original_publish=durable.publish_empirical_closure
        def capture(output,*args,**kwargs):
            captured.append(output)
            return original_publish(output,*args,**kwargs)
        with patch.object(delivery,"publish_empirical_closure",side_effect=capture), patch.object(
                issued.NativeWorkloadResult,"exact_s2e_output_census",autospec=True,
                side_effect=issued.NativeWorkloadResult.exact_s2e_output_census) as proofs:
            # Keep the R7/R8 exact-root publication oracle on the original
            # representation. New country publication defaults to factoring.
            baseline=run(products,factor_replay_risk_members=False)
            self.assertEqual(proofs.call_count,1,"final S2E proof rebuilt before publication")
        self.assertEqual(len(captured),1)
        baseline_reader=open_product(baseline)
        native_output=captured.pop()
        self._cas_publication_court(root,products,native_output,baseline)
        self._risk_replay_factoring_court(root,native_output,baseline,common,baseline_reader)
        self._fresh_proof_court(root,native_output,run,queries,baseline)
        del native_output
        # Actual process termination, not an exception which unwinds the
        # native session. Keep the original controlled interruption court.
        import os
        if os.environ.get("PYAT_R8_PROCESS_LOSS")=="1":
            self._process_loss_court(root,run,common,baseline,baseline_reader)
        bounded_dir=root/"bounded";bounded_dir.mkdir()
        bounded=run(bounded_dir,max_units=1)
        self.assertFalse(bounded.complete)
        self.assertEqual(bounded.batch_census["completed_count"],1)
        self.assertFalse(open_product(bounded,allow_partial=True).complete)
        self.assertTrue(baseline.complete)
        # R6 checkpoint publication must not weaken the original final
        # full-file authentication boundary. Change unused physical bytes
        # AFTER native calculation while defeating the stat mutation alarm.
        from rawlsing_next import pre553_country_numeric_carrier as carrier
        original_bytes=db.read_bytes()
        signature=carrier._stat_signature(db)
        manifest0=delivery._s04_manifest
        def changed_at_publication(*args,**kwargs):
            value=manifest0(*args,**kwargs)
            with db.open("r+b") as stream:
                stream.seek(-1,2)
                stream.write(bytes([original_bytes[-1]^1]))
            return value
        invalid=root/"invalid-publication";invalid.mkdir()
        external_pins=[]
        try:
            with patch.object(delivery,"_s04_manifest",changed_at_publication), patch.object(
                    carrier,"_stat_signature",return_value=signature):
                with self.assertRaisesRegex(carrier.CountryCarrierError,"differs from held receipt"):
                    run(invalid,max_units=1,checkpoint_every=1,
                        checkpoint_observer=lambda pin,pub:external_pins.append(pin))
            self.assertEqual(external_pins,[])
        finally:
            db.write_bytes(original_bytes)
        campaign=root/"campaign"
        campaign.mkdir()
        pins=[]
        class Interrupted(RuntimeError): pass
        def interrupt(pin,pub):
            pins.append((pin,pub))
            raise Interrupted("operator interrupted after retaining exact root")
        start=time.monotonic()
        with self.assertRaises(Interrupted):
            run(campaign,checkpoint_every=3,checkpoint_observer=interrupt)
        interruption_s=time.monotonic()-start
        pin,partial=pins[0]
        self.assertEqual(len(pins),1)
        self.assertFalse(partial.complete)
        self.assertEqual(partial.batch_census["completed_count"],3)
        with self.assertRaisesRegex(delivery.SavedDeliveryError,"PARTIAL"):
            open_product(partial)
        saved=open_product(partial,allow_partial=True)
        self.assertFalse(saved.complete)
        with self.assertRaisesRegex(delivery.SavedDeliveryError,"COMPLETE_PUBLICATION_REQUIRED"):
            delivery.read_country_s04_selected(partial.receipt.root_path,
                expected_root=partial.receipt.root_identity,
                expected_release_ref=partial.release_identity.release_ref,**common,
                requests=((queries[0].ref,None),))
        self.assertEqual(saved._closure.release_identities[0],baseline.release_identity)
        for receipt0 in saved._receipts:
            self.assertEqual(receipt0.state,"COMPLETED")
        manifest=delivery._manifest(workload,baseline.release_identity.release_ref)
        prior_by_ref={r.unit_ref.key:r for r in saved._receipts}
        pending=tuple(u for u in manifest.units if u.unit_ref.key not in prior_by_ref)
        # Wrong root and country pin fail before any native unit can be executed.
        for bad,exception in ((replace(pin,expected_root="0"*64),durable.DurableEmpiricalClosureError),
                              (replace(pin,expected_country_sha256="0"*64),delivery.SavedDeliveryError)):
            with patch.object(CarrierNeutralResearchExecutor,"execute_i03",
                    side_effect=AssertionError("bad resume executed I03")), patch.object(
                    CarrierNeutralResearchExecutor,"execute_i05",
                    side_effect=AssertionError("bad resume executed I05")):
                with self.assertRaises(exception):
                    run(campaign,resume_from=bad)
        resolver._record=replace(record,currentness="REVOKED")
        try:
            with self.assertRaises(issued.WorkloadAdmissionError):
                run(campaign,resume_from=pin)
        finally:
            resolver._record=record
        # A current semantic decision cannot excuse missing selected physical bytes.
        missing=db.with_suffix(".missing")
        db.rename(missing)
        try:
            with self.assertRaises((OSError,ValueError)):
                run(campaign,resume_from=pin)
        finally:
            missing.rename(db)

        actual=[]
        old_i03=CarrierNeutralResearchExecutor.execute_i03
        old_i05=CarrierNeutralResearchExecutor.execute_i05
        def count_i03(self,**kwargs):
            actual.append(("QUERY",kwargs["query_ref"].key))
            return old_i03(self,**kwargs)
        def count_i05(self,**kwargs):
            actual.append(("DISCOVERY",kwargs["discovery_authority_ref"].key))
            return old_i05(self,**kwargs)
        continued=[]
        def retain(pin,pub):
            continued.append((pin,pub))
        start=time.monotonic()
        with patch.object(CarrierNeutralResearchExecutor,"execute_i03",count_i03), patch.object(
                CarrierNeutralResearchExecutor,"execute_i05",count_i05):
            final=run(campaign,resume_from=pin,checkpoint_every=4,checkpoint_observer=retain)
        resume_s=time.monotonic()-start
        self.assertTrue(final.complete)
        self.assertEqual(final,continued[-1][1])
        self.assertEqual(collections.Counter(actual),
            collections.Counter((u.job_kind,u.job_ref.key) for u in pending))
        self.assertEqual(final.batch_census,baseline.batch_census)
        restored=open_product(final)
        self.assertEqual(restored._receipts,baseline_reader._receipts)
        self.assertEqual(restored._closure.release_identities,baseline_reader._closure.release_identities)
        self.assertEqual(restored._closure.i03_results,baseline_reader._closure.i03_results)
        self.assertEqual(tuple(r.replay_ref for r in restored._closure.discovery_results),
                         tuple(r.replay_ref for r in baseline_reader._closure.discovery_results))
        # Cold higher-order products and rare/inverse conditioning are
        # independently counted from source rows, not just compared to a
        # second run of the same evaluator.
        from rawlsing_next.tests.test_pre553_empirical_query import _cell_map
        from rawlsing_next.pre553_empirical_objects import exact_ref
        from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
        index_by_ref={r.key:i for i,r in enumerate(qrefs.values())}
        joint=queries[0];forward,inverse,rare=queries[-3:]
        for query,mask in ((joint,np.ones(len(selected),dtype=bool)),
                (forward,selected[:,0]==1),(inverse,selected[:,1]==0),
                (rare,(selected[:,0]==1)&(selected[:,1]==1)&(selected[:,3]==1))):
            read=restored.read_s04(query.ref)
            fact=read.first_consumer.execution.facts[0]
            self.assertEqual(fact.raw_denominator_support,int(mask.sum()))
            axes=tuple(index_by_ref[exact_ref(r).key] for r in query.target_refs)
            cells=_cell_map(fact)
            self.assertEqual(len(cells),2**len(axes))
            for cell,row in cells.items():
                vals=(cell,) if isinstance(cell,str) else cell
                actual_mask=mask.copy()
                for axis,val in zip(axes,vals):
                    actual_mask &= selected[:,axis]==int(val)
                self.assertEqual(row["raw_numerator_support"],int(actual_mask.sum()))
        self.assertEqual(restored.read_s04(rare.ref).first_consumer.execution.facts[0].raw_denominator_support,1)
        # FIELD FORGE's existing local joint algebra must use a stored fact
        # without calling the native evaluator again.
        with patch.object(CarrierNeutralResearchExecutor,"execute_i03",
                side_effect=AssertionError("retained joint replay executed I03")):
            workspace=restored.joint_workspace(joint.ref)
            for request in (S04Projection((1,),{0:"1"}),
                            S04Projection((0,),{1:"0"}),
                            S04Projection((2,),{0:"1",1:"1"}),
                            S04Projection((2,),{0:"1",1:"1"})):
                result=workspace.query(request).material()
                self.assertTrue(result["no_second_i03_or_source_query"])
                query_mask=np.ones(len(selected),dtype=bool)
                for axis,value in request.conditions.items():
                    query_mask &= selected[:,axis]==int(value)
                self.assertEqual(result["raw_selected_full_case_n"],int(query_mask.sum()))
                for cell in result["complete_output_cells"]:
                    mask=query_mask.copy()
                    for axis,value in zip(request.output_axes,cell["output_states"]):
                        mask &= selected[:,axis]==int(value)
                    self.assertEqual(cell["raw_count"],int(mask.sum()))
        plans=tuple((q.ref,None) for q in queries)
        self.assertEqual(tuple(delivery._s04_refs(r) for r in restored.read_s04_many(plans)),
                         tuple(delivery._s04_refs(r) for r in baseline_reader.read_s04_many(plans)))
        self.assertTrue(continued)
        final_pin=continued[-1][0]
        with self.assertRaisesRegex(delivery.SavedDeliveryError,"ALREADY_COMPLETE"):
            run(campaign,resume_from=final_pin)
        # Source and country may now disappear; complete retained product still
        # supplies actual consumer reads through the selected and full paths.
        db.unlink()
        select=delivery.read_country_s04_selected(final.receipt.root_path,
            expected_root=final.receipt.root_identity,
            expected_release_ref=final.release_identity.release_ref,**common,
            requests=plans)
        self.assertEqual(tuple(delivery._s04_refs(r) for r in select.reads),
                         tuple(delivery._s04_refs(r) for r in restored.read_s04_many(plans)))
        # Retained discovery roles (including valid empty fate) remain
        # available to the actual S04 recipient without source or a new I03.
        roles_read=0
        with patch.object(CarrierNeutralResearchExecutor,"execute_i03",
                side_effect=AssertionError("retained I05 reception executed I03")):
            for discovery in restored._closure.discovery_results:
                for candidate in discovery.receipts:
                    for role,refs in candidate.support_uncertainty_state.get("query_role_fact_refs",{}).items():
                        if len(refs)!=1:
                            continue
                        observed,role_receipt=restored.read_i05_role(candidate.ref,role)
                        old_observed,old_receipt=baseline_reader.read_i05_role(candidate.ref,role)
                        self.assertEqual((observed.ref,role_receipt.ref),(old_observed.ref,old_receipt.ref))
                        roles_read+=1
        self.assertGreater(roles_read,0)
        footprint=lambda path:sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        print("COUNTRY_CAMPAIGN_CONTINUITY",json.dumps({
            "country_rows":receipt.country_rows,"units":len(manifest.units),
            "completed_before_interrupt":3,"resumed_actual_executions":len(actual),
            "checkpoint_count":1+len(continued),"full_output_census_parity":True,
            "three_way_xor_rare_inverse_source_count_and_local_joint_reuse":True,
            "selected_after_source_and_country_deleted":len(select.reads),
            "retained_i05_roles_read":roles_read,
            "baseline_retained_bytes":footprint(products),"campaign_retained_bytes":footprint(campaign),
            "interruption_seconds":interruption_s,"resume_seconds":resume_s,
            "grade":"SOURCEFREE_CONTROLLED_INTERRUPTION_FRESH_READER_NOT_PROCESS_KILL_OR_ORIGINAL"
        }),flush=True)

    def _process_loss_court(self,root,run,common,baseline,baseline_reader):
        import os,signal,traceback
        from collections import Counter
        from rawlsing_next import pre553_saved_durable_delivery as delivery
        from rawlsing_next.pre553_empirical_objects import exact_ref
        from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
        destination=root/"killed-campaign"
        destination.mkdir()
        external=root/"operator-checkpoint-pin.json"
        from rawlsing_next import pre553_durable_empirical_closure as durable
        def retain_first(pin,pub):
            # The operator pin is independently retained outside the CAS.
            # The worker will die during the NEXT publication, not here.
            if external.exists():
                raise AssertionError("second checkpoint became visible")
            material=dict(closure_path=str(pin.closure_path),expected_root=pin.expected_root,
                expected_release_ref=pin.expected_release_ref.as_dict(),
                expected_country_sha256=pin.expected_country_sha256,
                completed=pub.batch_census["completed_count"])
            with external.open("w",encoding="utf-8") as handle:
                json.dump(material,handle,sort_keys=True)
                handle.flush()
                os.fsync(handle.fileno())
            fd=os.open(external.parent,os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        pid=os.fork()
        if pid==0:
            try:
                original=delivery.publish_empirical_closure
                def publish_then_die(output,*args,**kwargs):
                    if external.exists():
                        def failpoint(stage):
                            if stage=="before_manifest_replace":
                                os.kill(os.getpid(),signal.SIGKILL)
                        kwargs["failpoint"]=failpoint
                    return original(output,*args,**kwargs)
                with patch.object(delivery,"publish_empirical_closure",side_effect=publish_then_die):
                    run(destination,checkpoint_every=3,checkpoint_observer=retain_first)
            except BaseException:
                traceback.print_exc()
            os._exit(1)
        deadline=time.monotonic()+120
        while True:
            waited,status=os.waitpid(pid,os.WNOHANG)
            if waited:
                break
            if time.monotonic()>deadline:
                os.kill(pid,signal.SIGKILL)
                os.waitpid(pid,0)
                self.fail("checkpoint child timed out")
            time.sleep(.025)
        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(os.WTERMSIG(status),signal.SIGKILL)
        closures=destination/durable.CLOSURES_DIR
        self.assertEqual(len(list(closures.glob("closure-*"))),1)
        self.assertTrue(list(closures.glob(f"{durable.STAGING_PREFIX}{pid}-*")))
        material=json.loads(external.read_text())
        self.assertEqual(material.pop("completed"),3)
        material["expected_release_ref"]=exact_ref(material["expected_release_ref"])
        pin=delivery.CountryResumePin(**material)
        partial=delivery.open_country_product(pin.closure_path,
            expected_root=pin.expected_root,expected_release_ref=pin.expected_release_ref,
            **common,allow_partial=True)
        self.assertFalse(partial.complete)
        manifest=delivery._manifest(common["workload"],baseline.release_identity.release_ref)
        completed={r.unit_ref.key for r in partial._receipts}
        expected=Counter((u.job_kind,u.job_ref.key) for u in manifest.units
                         if u.unit_ref.key not in completed)
        actual=[]
        i03=CarrierNeutralResearchExecutor.execute_i03
        i05=CarrierNeutralResearchExecutor.execute_i05
        def record03(self,**kw):
            actual.append(("QUERY",kw["query_ref"].key))
            return i03(self,**kw)
        def record05(self,**kw):
            actual.append(("DISCOVERY",kw["discovery_authority_ref"].key))
            return i05(self,**kw)
        with patch.object(CarrierNeutralResearchExecutor,"execute_i03",record03), patch.object(
                CarrierNeutralResearchExecutor,"execute_i05",record05):
            final=run(destination,resume_from=pin)
        self.assertEqual(Counter(actual),expected)
        self.assertEqual(final.batch_census,baseline.batch_census)
        self.assertFalse(list(closures.glob(f"{durable.STAGING_PREFIX}{pid}-*")))
        restored=delivery.open_country_product(final.receipt.root_path,
            expected_root=final.receipt.root_identity,
            expected_release_ref=final.release_identity.release_ref,**common)
        self.assertEqual(restored._receipts,baseline_reader._receipts)
        self.assertEqual(restored._closure.i03_results,baseline_reader._closure.i03_results)
        self.assertEqual(tuple(x.replay_ref for x in restored._closure.discovery_results),
                         tuple(x.replay_ref for x in baseline_reader._closure.discovery_results))
        print("RELAY_R8_PROCESS_LOSS",json.dumps({"child_termination":"SIGKILL",
            "completed_before_death":len(completed),"resumed_native_units":len(actual),
            "exact_output_and_receipt_parity":True,
            "unpublished_staging_reclaimed":True,
            "grade":"SOURCEFREE_FORKED_WORKER_SIGKILL_BEFORE_SECOND_MANIFEST_REPLACE"
        }),flush=True)

    def _fresh_proof_court(self,root,output,run,queries,baseline):
        """Compare actual native replay reconstruction, not a simulated digest."""
        import os
        from rawlsing_next import pre553_durable_empirical_closure as durable
        from rawlsing_next import pre553_saved_durable_delivery as delivery
        from rawlsing_next import pre553_issued_workload as issued
        from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
        # An externally delivered checkpoint may not exempt the final native
        # snapshot from independent proof; simulate internal envelope drift
        # during the detached observer boundary without altering fact refs.
        from rawlsing_next._pre553_query_common import SOURCE_SCOPE_MODES
        seen=[]
        original_i03=CarrierNeutralResearchExecutor.execute_i03
        def capture03(executor,**kwargs):
            result=original_i03(executor,**kwargs)
            seen.append(result)
            return result
        changed=[]
        def corrupt_after_publish(pin,pub):
            result=seen[0]
            before=result.source_scope_mode
            alternative=next(x for x in sorted(SOURCE_SCOPE_MODES) if x!=before)
            object.__setattr__(result,"source_scope_mode",alternative)
            changed.append((result,before))
        # One partial operation; no additional native work can obscure the
        # discrepancy between its published and returned proof.
        try:
            with patch.object(CarrierNeutralResearchExecutor,"execute_i03",capture03):
                with self.assertRaisesRegex(delivery.SavedDeliveryError,"CHECKPOINT_FINAL_CENSUS_DRIFT"):
                    run(root/"r11-drift",max_units=1,checkpoint_every=1,
                        checkpoint_observer=corrupt_after_publish)
        finally:
            for item,before in changed:object.__setattr__(item,"source_scope_mode",before)
        self.assertEqual(len(changed),1)
        # Public cold reader remains an independent full proof, not a
        # consumer of the live result's census object.
        self.assertTrue(baseline.complete)
        facts=output.object_graph.empirical_facts
        releases=output.release_by_ref()
        for fact in facts:
            material,raw,digest=durable._fact_replay_preimage(fact,releases)
            self.assertEqual(raw,durable._canonical_bytes(material))
            self.assertEqual(digest,hashlib.sha256(raw).hexdigest())
        # Deliberately break the newly reconstructed native replay while
        # retaining the original fact and exact replay ref. Must refuse.
        original=durable._positive_fact_replay_material
        def bad_replay(fact,releases):
            material=original(fact,releases)
            if material is not None:material["risk_member_refs"]=[]
            return material
        with patch.object(durable,"_positive_fact_replay_material",bad_replay):
            with self.assertRaisesRegex(durable.DurableEmpiricalClosureError,"cannot be reconstructed"):
                durable._replay_documents(output,{},factor_replay_risk_members=True)
        if os.environ.get("PYAT_R11_MATCHED_PROOF")!="1":
            return
        from tools.pyat_country_storage_relay_benchmark import historical
        r10=historical("5a8f05f134e950277798e8eb8580453f32ca8fab",
                       "pre553_durable_empirical_closure")
        times={"R10":[],"R11":[]}
        proof=None
        for order in (("R10","R11"),("R11","R10"),("R10","R11"),("R11","R10")):
            for name in order:
                mod=r10 if name=="R10" else durable
                fragments={}
                started=time.monotonic()
                docs,_=mod._replay_documents(output,fragments,factor_replay_risk_members=True)
                times[name].append(time.monotonic()-started)
                material=(docs,fragments)
                if proof is None:proof=material
                self.assertEqual(material,proof)
        # Exact manifest root and every CAS byte, not just replay hash.
        pubs=[]
        for name,mod in (("R10",r10),("R11",durable)):
            dest=root/("r11-proof-"+name)
            pubs.append(mod.publish_empirical_closure(output,dest,compact_manifest=True,
                            factor_replay_risk_members=True))
        self.assertEqual(pubs[0].root_identity,pubs[1].root_identity)
        self.assertEqual(pubs[0].logical_evidence_bytes,pubs[1].logical_evidence_bytes)
        def inventory(name):
            base=root/("r11-proof-"+name)/durable.CAS_DIR
            return {str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in base.rglob("*") if p.is_file()}
        self.assertEqual(inventory("R10"),inventory("R11"))
        self.assertEqual(durable._manifest_file(Path(pubs[0].root_path)).read_bytes(),
                         durable._manifest_file(Path(pubs[1].root_path)).read_bytes())
        print("R11_FRESH_PROOF",json.dumps({"facts":len(facts),
            "replay_documents_seconds":times,"median_seconds":{k:median(v) for k,v in times.items()},
            "exact_root_manifest_cas":True,"one_final_census":True,
            "post_checkpoint_envelope_drift_refused":True,"replay_mutation_refused":True,
            "grade":"MATCHED_NATIVE_OUTPUT_REPLAY_CONSTRUCTION_NOT_FULL_CAMPAIGN"}),flush=True)

    def _risk_replay_factoring_court(self,root,output,baseline,common,baseline_reader):
        """Actual native output, exact legacy root plus factored replay root."""
        from rawlsing_next import pre553_durable_empirical_closure as durable
        from rawlsing_next import pre553_saved_durable_delivery as delivery
        from rawlsing_next.pre553_durable_empirical_fragments import FRAGMENT_MARKER
        destination=root/"r10-factored-risk"
        new=durable.publish_empirical_closure(output,destination,compact_manifest=True,
                                             factor_replay_risk_members=True)
        old=baseline.receipt
        self.assertNotEqual(new.root_identity,old.root_identity)
        self.assertEqual(new.cas_new_bytes,old.cas_new_bytes)
        self.assertEqual(new.logical_evidence_bytes,old.logical_evidence_bytes)
        old_core=baseline_reader._closure.manifest["core"]
        product=delivery.open_country_product(new.root_path,
            expected_root=new.root_identity,expected_release_ref=baseline.release_identity.release_ref,
            **common)
        self.assertEqual(product._receipts,baseline_reader._receipts)
        self.assertEqual(product.batch_census,baseline_reader.batch_census)
        self.assertEqual(product._closure.i03_results,baseline_reader._closure.i03_results)
        self.assertEqual(tuple(x.replay_ref for x in product._closure.discovery_results),
                         tuple(x.replay_ref for x in baseline_reader._closure.discovery_results))
        new_core=product._closure.manifest["core"]
        count=self._compare_risk_factored_cores(old_core,new_core)
        self.assertGreater(count,0)
        # Small fixtures can already compress repeated strings within a
        # deflate window; record actual physical bytes without requiring a
        # universal latency or compressed-size improvement.
        self.assertLess(len(durable._canonical_bytes(new_core)),len(durable._canonical_bytes(old_core)))
        plan=((common["workload"].requests[0].query_ref,None),)
        selected=delivery.read_country_s04_selected(new.root_path,
            expected_root=new.root_identity,expected_release_ref=baseline.release_identity.release_ref,
            **common,requests=plan)
        self.assertEqual(tuple(delivery._s04_refs(x) for x in selected.reads),
                         tuple(delivery._s04_refs(x) for x in baseline_reader.read_s04_many(plan)))
        with self.assertRaises(durable.DurableEmpiricalClosureError):
            durable.open_empirical_closure(new.root_path,expected_root=old.root_identity)
        # The added replay marker must still be backed by an authenticated
        # blob; no acceptance of a manifest-only risk-set assertion.
        risk=next(x["material"]["risk_member_refs"][FRAGMENT_MARKER]
                  for x in new_core["replays"]["facts"] if "risk_member_refs" in x["material"])
        path=destination/durable.CAS_DIR/durable.BLOB_DIR/(risk+durable.BLOB_SUFFIX)
        original=path.read_bytes()
        try:
            path.write_bytes(b"invalid risk fragment")
            with self.assertRaises(durable.DurableEmpiricalClosureError):
                durable.open_empirical_closure(new.root_path,expected_root=new.root_identity)
        finally:
            path.write_bytes(original)
        durable.open_empirical_closure(new.root_path,expected_root=new.root_identity).require_trusted()
        print("RELAY_R10_RISK_FACTORS",json.dumps({"factored_replays":count,
            "legacy_manifest_bytes":old.manifest_bytes,"factored_manifest_bytes":new.manifest_bytes,
            "legacy_cas_bytes":old.cas_new_bytes,"factored_cas_bytes":new.cas_new_bytes,
            "exact_native_and_selected_parity":True,"wrong_root_and_corrupt_fragment_refused":True}),flush=True)

    def _compare_risk_factored_cores(self,old,new):
        """Exact persisted core comparison, allowing only the risk transport
        representation to change; the incumbent evidence accounting stays."""

        from rawlsing_next.pre553_durable_empirical_fragments import FRAGMENT_MARKER
        from rawlsing_next.pre553_empirical_objects import semantic_hash
        self.assertEqual(set(old),set(new))
        for key in old:
            if key!="replays":
                self.assertEqual(old[key],new[key],key)
        self.assertEqual(set(old["replays"]),set(new["replays"]))
        for key in old["replays"]:
            if key!="facts":
                self.assertEqual(old["replays"][key],new["replays"][key])
        self.assertEqual(len(old["replays"]["facts"]),len(new["replays"]["facts"]))
        objects={x["ref"]["content_hash"]:x for x in new["objects"] if x["family"]=="EmpiricalFact@1.0.0"}
        count=0
        for a,b in zip(old["replays"]["facts"],new["replays"]["facts"]):
            material=dict(b["material"])
            if "risk_member_refs" in a["material"]:
                values=a["material"]["risk_member_refs"]
                digest=semantic_hash(values)
                self.assertEqual(material["risk_member_refs"],{FRAGMENT_MARKER:digest})
                self.assertIn(digest,objects[b["fact_ref"]["content_hash"]]["fragment_refs"])
                material["risk_member_refs"]=values
                count+=1
            self.assertEqual(a,{**b,"material":material})
        return count

    def _cas_publication_court(self,root,products,output,baseline):
        """Same actual native output; independent publication into a warm CAS.

        This is not a cache of scientific results. Each publication still
        constructs and validates the complete output graph. Only existing
        compressed bytes can discharge an exact-byte equality witness.
        """
        import shutil,zlib
        from rawlsing_next import pre553_durable_empirical_closure as durable
        from rawlsing_next.pre553_empirical_objects import canonical_json
        blobs=products/durable.CAS_DIR/durable.BLOB_DIR
        paths=sorted(blobs.glob("*"+durable.BLOB_SUFFIX))
        self.assertTrue(paths)
        expected_root=baseline.receipt.root_identity
        def warm(name):
            dest=root/name
            shutil.copytree(products/durable.CAS_DIR,dest/durable.CAS_DIR)
            return dest
        def publish(mod,dest):
            return mod.publish_empirical_closure(output,dest,
                        compact_manifest=True,expected_root=expected_root)
        same=warm("r8-cas-exact")
        with patch.object(durable,"_decode_verified_blob",
                          side_effect=AssertionError("identical CAS bytes decoded")):
            receipt=publish(durable,same)
        self.assertEqual(receipt.root_identity,expected_root)
        self.assertEqual(receipt.cas_new_bytes,0)
        durable.open_empirical_closure(receipt.root_path,expected_root=expected_root).require_trusted()
        # Recompress actual retained canonical material without changing its
        # content identity. The cold reader requires the original extent.
        blob=paths[0]
        raw=zlib.decompress(blob.read_bytes())
        alternative=zlib.compress(raw,0)
        self.assertNotEqual(len(alternative),blob.stat().st_size)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),blob.name[:-len(durable.BLOB_SUFFIX)])
        poisoned=warm("r8-cas-wrong-extent")
        changed=poisoned/durable.CAS_DIR/durable.BLOB_DIR/blob.name
        changed.write_bytes(alternative)
        with self.assertRaisesRegex(durable.DurableEmpiricalClosureError,"compressed size drift"):
            publish(durable,poisoned)
        self.assertFalse(list((poisoned/durable.CLOSURES_DIR).glob("closure-*")))
        # Same-size wrong bytes must not pass equality or the fallback.
        changed.write_bytes(b"\x00"*blob.stat().st_size)
        with self.assertRaises(durable.DurableEmpiricalClosureError):
            publish(durable,poisoned)
        self.assertFalse(list((poisoned/durable.CLOSURES_DIR).glob("closure-*")))
        changed.write_bytes(blob.read_bytes())
        # The cold reader historically permits alternate compression bytes
        # with the same content AND declared extents. Do not accidentally
        # turn exact-byte acceleration into a new physical format restriction.
        sample=canonical_json({"fixture":"a"*256}).encode("utf-8")
        generated=zlib.compress(sample,9)
        alternate=zlib.compress(sample,6)
        self.assertNotEqual(alternate,generated)
        self.assertEqual(len(alternate),len(generated))
        standalone=root/"same-extent-alternate.json.z"
        standalone.write_bytes(alternate)
        durable._verify_existing_blob(standalone,generated,
            hashlib.sha256(sample).hexdigest(),
            {"compressed_bytes":len(generated),"uncompressed_bytes":len(sample)})
        restored=publish(durable,poisoned)
        self.assertEqual(restored.root_identity,expected_root)
        durable.open_empirical_closure(restored.root_path,expected_root=expected_root).require_trusted()
        # Compare exact R7, not an emulation, where the immutable parent is
        # present. Local standalone tests need not fetch another Git object.
        import os
        if os.environ.get("PYAT_R8_MATCHED_PUBLICATION")=="1":
            from tools.pyat_country_storage_relay_benchmark import historical
            r7=historical("d8ae9a9324c4f923c2efe79e08ce8530bbf32cdc",
                          "pre553_durable_empirical_closure")
            old_bad=warm("r7-cas-wrong-extent")
            (old_bad/durable.CAS_DIR/durable.BLOB_DIR/blob.name).write_bytes(alternative)
            old_receipt=publish(r7,old_bad)
            # The inherited writer publishes success; its own cold reader refuses.
            with self.assertRaisesRegex(r7.DurableEmpiricalClosureError,"compressed size drift"):
                r7.open_empirical_closure(old_receipt.root_path,expected_root=expected_root)
            times={"R7":[],"R8":[]}
            for i,order in enumerate((("R7","R8"),("R8","R7"),("R7","R8"),("R8","R7"))):
                for version in order:
                    dest=warm(f"matched-publication-{i}-{version}")
                    started=time.monotonic()
                    value=publish(r7 if version=="R7" else durable,dest)
                    times[version].append(time.monotonic()-started)
                    self.assertEqual(value.cas_new_bytes,0)
                    self.assertEqual(value.root_identity,expected_root)
                    self.assertEqual(durable._manifest_file(Path(value.root_path)).read_bytes(),
                                     durable._manifest_file(Path(baseline.receipt.root_path)).read_bytes())
                    durable.open_empirical_closure(value.root_path,
                        expected_root=expected_root).require_trusted()
            print("RELAY_R8_WARM_PUBLICATION",json.dumps({
                "existing_blobs":len(paths),"exact_manifest_and_root":True,
                "old_accepts_reader_refused_extent":True,
                "R8_refuses_wrong_extent_and_bad_bytes":True,
                "seconds":times,"median_seconds":{k:median(v) for k,v in times.items()},
                "grade":"MATCHED_NATIVE_OUTPUT_WARM_CAS_PUBLICATION_NOT_FULL_WORKLOAD"
            }),flush=True)

    def test_physical_layout_query_tradeoffs_same_cells(self):
        """One selected carrier, bounded block-size comparison; not native-I03 proxy."""
        from rawlsing_next import pre553_country_numeric_carrier as carrier
        rng=np.random.default_rng(152)
        n=2400
        low=rng.integers(0,5,(n,12))
        high=rng.random((n,8))
        frame=pd.DataFrame({f"q{i}":low[:,i].astype(float) for i in range(12)})
        for i in range(8):
            frame[f"v{i}"]=high[:,i]
        frame["country"]=np.where(np.arange(n)%2==0,1.,2.)
        chosen=np.arange(0,n,2)
        # Same deterministic distinct predicates in each layout; warm
        # repeats reported separately from independent cold opening.
        workloads=[{f"q{i}":float(i%5)} for i in range(10)]
        workloads += [{f"q{i}":float(i%5),f"q{(i+1)%12}":float((i+2)%5)} for i in range(10)]
        workloads += [{f"v{i}":float(high[2*i,i])} for i in range(8)]
        oracle=[]
        for conditions in workloads:
            mask=np.ones(len(chosen),dtype=bool)
            for key,value in conditions.items():
                mask &= frame[key].to_numpy()[chosen]==value
            oracle.append(tuple(int(i+1) for i in chosen[mask]))
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);src=p/"mixed.sav"
            pyreadstat.write_sav(frame,str(src))
            with decode_sav(src) as inc:
                for block_rows in (128,1024,4096):
                    path=p/f"layout-{block_rows}.sqlite"
                    t=time.monotonic()
                    receipt=build_country(inc,country_variable="country",country_value=1.,
                        output=path,require_current=lambda:True,block_rows=block_rows)
                    build_s=time.monotonic()-t
                    t=time.monotonic()
                    with CountryReader(path,receipt,require_current=lambda:True) as reader:
                        cold_s=time.monotonic()-t
                        times=[]
                        for conditions,expected in zip(workloads,oracle):
                            t=time.monotonic()
                            actual=tuple(reader.matching_rows(conditions))
                            times.append(time.monotonic()-t)
                            self.assertEqual(actual,expected)
                        warm=[]
                        for _ in range(10):
                            t=time.monotonic()
                            self.assertEqual(tuple(reader.matching_rows(workloads[0])),oracle[0])
                            warm.append(time.monotonic()-t)
                        lanes=reader.db.execute("SELECT count(*) FROM lanes").fetchone()[0]
                    print("COUNTRY_PHYSICAL_QUERY_TRADEOFF",json.dumps({
                        "block_rows":block_rows,"bytes":receipt.bytes,"lanes":lanes,
                        "build_s":build_s,"cold_open_s":cold_s,
                        "distinct_low_unary_median_s":median(times[:10]),
                        "distinct_low_joint_median_s":median(times[10:20]),
                        "distinct_high_unary_median_s":median(times[20:]),
                        "distinct_total_s":sum(times),"identical_warm_median_s":median(warm),
                        "sourcefree":True}),flush=True)


from collections.abc import Mapping, Sequence
from typing import Any
from dataclasses import is_dataclass, fields
from decimal import Decimal
from fractions import Fraction
from enum import Enum
import hashlib
from rawlsing_next.pre553_empirical_objects import AuthorityRef,CanonicalSemanticObject,Pre553IntegrityError,_decimal_text

def _legacy_material(value: Any) -> Any:
    """Complete dataclass preimages, including fields omitted by count receipts."""
    if hasattr(value, "as_dict"):
        return _legacy_material(value.as_dict())
    if is_dataclass(value):
        return {f.name: _legacy_material(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Mapping):
        return {str(k): _legacy_material(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_legacy_material(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_legacy_material(v) for v in value), key=lambda x: json.dumps(x, sort_keys=True))
    return value



def _legacy_canonicalize(value: Any) -> Any:
    """Return deterministic JSON-safe semantic material.

    Binary floats (including NaN/Infinity) are forbidden. Exact numerics may be
    represented as integers, Decimal, Fraction, or exact strings.
    """
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise Pre553IntegrityError("float/NaN/Infinity forbidden in semantic identity")
    if isinstance(value, Decimal):
        return {"$exact_decimal": _decimal_text(value)}
    if isinstance(value, Fraction):
        return {"$exact_fraction": [value.numerator, value.denominator]}
    if isinstance(value, Enum):
        return _legacy_canonicalize(value.value)
    if isinstance(value, ExactRef):
        return value.as_dict()
    if isinstance(value, AuthorityRef):
        return value.as_dict()
    if isinstance(value, CanonicalSemanticObject):
        return value.ref.as_dict()
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise Pre553IntegrityError("semantic mapping keys must be strings")
        return {k: _legacy_canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value, (set, frozenset)):
        items = [_legacy_canonicalize(v) for v in value]
        return sorted(items, key=_legacy_canonical_json)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_legacy_canonicalize(v) for v in value]
    raise Pre553IntegrityError(f"unsupported semantic identity type: {type(value).__name__}")


def _legacy_canonical_json(value: Any) -> str:
    return json.dumps(_legacy_canonicalize(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def _legacy_semantic_hash(value: Any) -> str:
    return hashlib.sha256(_legacy_canonical_json(value).encode("utf-8")).hexdigest()



class MaterialFastPathParity(unittest.TestCase):
    def test_old_and_new_material_and_canonical_bytes_match(self):
        from rawlsing_next.pre553_issued_workload import material
        from rawlsing_next.pre553_empirical_objects import canonical_json,canonicalize
        from types import MappingProxyType
        fx=_fixture("material-parity")
        cases=[None,False,True,0,1,-100,2**100,"é🧠",{"z":[1,"a",None],"a":(False,3)},
               MappingProxyType({"x":Decimal("1.2300"),"y":Fraction(2,3)}),
               {3,1,2},fx["projection"],fx["authorities"],fx["universe"]]
        for value in cases:
            with self.subTest(kind=type(value).__name__):
                old=_legacy_material(value)
                new=material(value)
                self.assertEqual(new,old)
                self.assertEqual(canonical_json(new),_legacy_canonical_json(old))
        for bad in ({"x":1.0},[float("nan")],{1:"not semantic string key"}):
            with self.assertRaises(Pre553IntegrityError):
                canonicalize(bad)
            with self.assertRaises(Pre553IntegrityError):
                _legacy_canonicalize(bad)
        self.assertNotEqual(canonical_json(True),canonical_json(1))
        self.assertNotEqual(canonical_json("1"),canonical_json(1))
        # Full material is detached anew; mutation must not alias a past
        # envelope or evade the next full admission hash.
        mutable={"v":[1,2]}
        first=material(mutable)
        mutable["v"][0]=False
        self.assertEqual(first,{"v":[1,2]})
        self.assertNotEqual(canonical_json(first),canonical_json(material(mutable)))
