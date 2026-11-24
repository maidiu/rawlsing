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
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

from rawlsing_next.pre553_country_numeric_carrier import build_country
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import (
    PhysicalSlot,RowRespondentBinding,ResponseSlotRule,ResponseValueRule,OccurrenceRule,
    CoordinateSlotRule,WeightSlotRule,physical_value_binding_key,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef,TypedAbsence,RespondentIdentity,QuestionVariableBinding,RoutingEligibilityFact,
    semantic_hash,
)
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
        tag="country-native-economics"
        n,governed,extras=800,16,23
        rng=np.random.default_rng(312)
        values=rng.integers(0,2,(n,governed))
        names=tuple("q"+str(i) for i in range(governed))
        frame=pd.DataFrame({q:values[:,i].astype(str) for i,q in enumerate(names)})
        for i in range(extras):
            frame["v"+str(i)]=np.arange(n,dtype=np.float64)*(1.000001+i*.00001)+i*.001
        frame["G"]=np.where(np.arange(n)%2==0,"A","B")
        frame["W"]=1.+(np.arange(n)%3)
        chosen=tuple(range(1,n+1,2))
        selected=values[::2,:]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);src=p/"generated.sav";db=p/"country.sqlite";products=p/"products";products.mkdir()
            pyreadstat.write_sav(frame,str(src))
            original_bytes=src.stat().st_size
            sha=hashlib.sha256(src.read_bytes()).hexdigest()
            t=time.monotonic()
            with decode_sav(src,expected_source_sha256=sha) as inc:
                ordinals={v.name:v.ordinal for v in inc.variables}
                receipt=build_country(inc,country_variable="G",country_value="A",output=db,
                                      require_current=lambda:True,block_rows=256)
            build_seconds=time.monotonic()-t
            self.assertEqual(receipt.country_rows,len(chosen))
            src.unlink()
            t=time.monotonic()
            fx=_fixture(tag);original=fx["projection"];universe=fx["universe"]
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
            routing=tuple(RoutingEligibilityFact(typed_state=state,authority_snapshot_refs=(fx["routing_auth"].authority_ref,),
                dependency_refs=(),producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT",f"{tag}-{row}-{q}"),
                empirical_universe_ref=universe.ref,scoped_respondent_ref=person.ref,question_or_target_ref=qrefs[q],
                risk_set_ref=risk,routing_rule_ref=_ref("ROUTING_RULE",tag+"-"+q),applicability_state=state,routing_state=state,
                parent_predicate_refs=(),member_set_replay_ref=_ref("MEMBER_SET",tag+"-"+q))
                for q in names for row,person in zip(chosen,respondents))
            projection=replace(original,expected_source_sha256=sha,
                source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT","urn:test:"+tag,sha),
                respondents=respondents,row_bindings=tuple(RowRespondentBinding(row,person.ref) for row,person in zip(chosen,respondents)),
                questions=questions,response_slots=slots,routing=routing,
                coordinate_slots=(replace(original.coordinate_slots[0],slot=PhysicalSlot(ordinals["G"],"G")),),
                weight_slots=(replace(original.weight_slots[0],slot=PhysicalSlot(ordinals["W"],"W")),))
            fx.update(qrefs=qrefs,respondents={p.respondent_key:p for p in respondents})
            qa=_query_authority(tag);da=_d_auth(tag+"-discovery")
            base=_branch_predicate(fx,qa,members=respondents,tag=tag+"-all")
            atom=_predicate(fx,qa,_response_leaf(fx,qa,"q0","1"),tag=tag+"-q0")
            joint=_query(fx,qa,base,("q0","q1"),tag=tag+"-joint")
            # Distinct actual predicates/targets, not repeated identical query.
            conditional=tuple(_query(fx,qa,atom,(q,),tag=tag+"-"+q) for q in names[2:11])
            unary=_query(fx,qa,base,("q1",),tag=tag+"-unary")
            grammar=_grammar(operation="I03-OP-"+tag+"-discovery",
                atoms=[_atom("ALL",base,"BRANCH"),_atom("X1",atom,"RESPONSE")],
                templates=[_qt("Y",unary)],rules=[_rule("pair","PAIR_RESPONSE_COTRAVEL","SINGLE_ATOM",
                    atom_ids=("X1",),baseline_atom_id="ALL",query_template_id="Y",
                    validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})])
            discovery=_discovery_authority(fx,grammar,da)
            queries=(joint,*conditional,unary)
            cat=RuntimeObjectCatalog((*fx["authorities"],qa,da),(base,atom),queries,(discovery,))
            requests=tuple(I03ExecutionRequest(q.ref,base.ref if q in (joint,unary) else atom.ref) for q in queries)
            ds=(discovery.ref,);jobs=operation_jobs(requests,ds)
            root=semantic_hash({"fixture":tag});frontier=semantic_hash({"jobs":jobs,"root":root})
            decision=_ref("TEST_ONLY_DECISION",tag);host,purpose="test-country","TEST_ONLY_COUNTRY_ECONOMICS"
            descriptor=dict(source_edition=sha,native_item_ids=list(names),release_tag=projection.instrument_release_id,
                routing_and_risk={"fixture":True},carrier={"kind":"COUNTRY_NUMERIC"},country_and_population={"fixture":"A"},
                weight_design_estimand={"measure":"RAW"},missing_and_occurrence_policy={"fixture":True},
                target_conditioner_roles={"joint":["q0","q1"]})
            workload=NativeWorkload(decision_ref=decision,source_factory_ref=_ref("TEST_ONLY_FACTORY",tag),
                descriptor=canonical(descriptor),projection=projection,catalog=cat,requests=requests,discoveries=ds,
                original_u_root=root,expected_frontier_root=frontier)
            record=IssuedWorkloadRecord(decision_ref=decision,source_permission_ref=_ref("TEST_ONLY_SOURCE_PERMISSION",tag),
                scientific_permission_refs=(_ref("TEST_ONLY_SCIENCE_PERMISSION",tag),),host=host,purpose=purpose,source_sha256=sha,
                envelope_sha256=semantic_hash(workload.envelope()),original_u_root=root,expected_frontier_root=frontier,
                expected_jobs=jobs,currentness="CURRENT_GRANTED",scope="TEST_ONLY_SOURCEFREE",native_universe_refs=(universe.ref,))
            resolver=TestOnlyDecisionResolver(record)
            projection_seconds=time.monotonic()-t
            print("COUNTRY_NATIVE_SCALE_START",json.dumps({"rows":n,"country_rows":len(chosen),"physical_width":len(frame.columns),
                "governed_width":governed,"units":len(jobs),"country_bytes":receipt.bytes,
                "source_bytes":original_bytes,"build_seconds":build_seconds,"projection_seconds":projection_seconds}),flush=True)
            pub=execute_publish_country(workload,resolver,host=host,purpose=purpose,country_path=db,
                country_receipt=receipt,root_dir=products)
            self.assertTrue(pub.complete)
            self.assertEqual(pub.batch_census["unit_count"],len(jobs))
            self.assertIsNotNone(pub.release_identity)
            db.unlink()
            t=time.monotonic()
            cold=open_country_product(pub.receipt.root_path,expected_root=pub.receipt.root_identity,
                expected_release_ref=pub.release_identity.release_ref,country_receipt=receipt,workload=workload,
                resolver=resolver,host=host,purpose=purpose)
            for q in queries:
                read=cold.read_s04(q.ref,conditioner_index=0 if q==joint else None)
                fact=read.first_consumer.execution.facts[0]
                expected=len(chosen) if q in (joint,unary) else int((selected[:,0]==1).sum())
                self.assertEqual(fact.raw_denominator_support,expected)
                if q==joint:
                    self.assertEqual(read.first_consumer.ff01.semantic_projection()["raw_fully_resolved_joint_n"],len(chosen))
            result,=cold._closure.discovery_results
            self.assertEqual(result.candidate_count,result.covered_candidate_count)
            self.assertEqual(result.candidate_count,1)
            print("COUNTRY_NATIVE_SCALE_RESULT",json.dumps({"native_and_s04_seconds":pub.execution_seconds,
                "publication_seconds":pub.publication_seconds,"cold_s04_seconds":time.monotonic()-t,
                "closure_referenced_bytes":pub.receipt.referenced_physical_bytes,
                "peak_process_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "grade":"SOURCEFREE_400x41_16_GOVERNED_NOT_ORIGINAL"}),flush=True)
