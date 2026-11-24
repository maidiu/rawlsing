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

    def _native_batch(self,*,wide):
        tag="country-native-wide" if wide else "country-native-economics"
        n,governed,extras=(512,80,218) if wide else (800,16,23)
        rng=np.random.default_rng(312)
        values=rng.integers(0,2,(n,governed))
        names=tuple("q"+str(i) for i in range(governed))
        data={q:values[:,i].astype(str) for i,q in enumerate(names)}
        for i in range(extras):
            data["v"+str(i)]=np.arange(n,dtype=np.float64)*(1.000001+i*.00001)+i*.001
        data["G"]=np.where(np.arange(n)%2==0,"A","B")
        data["W"]=1.+(np.arange(n)%3)
        frame=pd.DataFrame(data)
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
            atom2=_predicate(fx,qa,_response_leaf(fx,qa,"q1","0"),tag=tag+"-q1-zero") if wide else None
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
            requests=tuple(I03ExecutionRequest(q.ref,base.ref if q in (joint,unary) else atom2.ref if q in alternate else atom.ref) for q in queries)
            if wide:
                self.assertEqual(len({q.ref.key for q in queries}),100)
                self.assertEqual(len(routing),20480)
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
            # Inclusive wall time/calls: nested counters deliberately NOT
            # summed. Retain actual incumbent query and publication owners.
            from rawlsing_next import pre553_issued_workload as issued
            from rawlsing_next import pre553_saved_durable_delivery as delivery
            from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
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
                    (issued.NativeWorkload,"envelope","full_workload_envelope"),
                    (issued,"build_source_backed_c11_repository","cold_native_prepare"),
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
            self.assertEqual(pub.batch_census["unit_count"],len(jobs))
            self.assertIsNotNone(pub.release_identity)
            db.unlink()
            t=time.monotonic()
            timings.clear()
            with ExitStack() as stack:
                for owner,name,label in (
                    (issued.NativeWorkload,"envelope","cold_full_envelope"),
                    (issued._PreparedRoutingEnvelope,"digest","cold_prepared_routing_digest"),
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
                for q in queries:
                    read=cold.read_s04(q.ref,conditioner_index=0 if q==joint else None)
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
            print("COUNTRY_COLD_PHASES",json.dumps({k:{"calls":len(v),"total_s":sum(v),
                "median_s":median(v),"max_s":max(v)} for k,v in timings.items()}),flush=True)
            result,=cold._closure.discovery_results
            self.assertEqual(result.candidate_count,result.covered_candidate_count)
            self.assertEqual(result.candidate_count,1)
            print("COUNTRY_NATIVE_SCALE_RESULT",json.dumps({"native_and_s04_seconds":pub.execution_seconds,
                "publication_seconds":pub.publication_seconds,"cold_s04_seconds":time.monotonic()-t,
                "closure_referenced_bytes":pub.receipt.referenced_physical_bytes,
                "peak_process_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                "grade":"SOURCEFREE_256x300_80_GOVERNED_100_I03_NOT_ORIGINAL" if wide else "SOURCEFREE_400x41_16_GOVERNED_NOT_ORIGINAL"}),flush=True)


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
