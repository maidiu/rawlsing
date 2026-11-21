#!/usr/bin/env python3
"""Sourcefree full native proof for operation-scoped historical DEFER universe use."""
from __future__ import annotations
import dataclasses, json, tempfile, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
import pytest
from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate, execute_anvil_stream_i03
from rawlsing_next.pre553_anvil_stream_recorded import RecordedUniverseUse
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, EmpiricalQuerySpec, EmpiricalUniverse, ExactRef,
    make_empirical_predicate, semantic_hash,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.tests.test_pre553_anvil_stream_native_i03 import _stream

def main():
    scratch=Path(tempfile.mkdtemp(prefix='universe-use-',dir='/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode'))
    mp=pytest.MonkeyPatch()
    try:
        source,auth,pred,query,catalog,root,release,manifest,held,grant=_stream(scratch,mp,'UNIVERSE-USE',source_id='SRC04')
        estate=VerifiedAnvilStreamEstate(root,exact_path=release,independently_held=held,current_authorizer=grant)
        universe=next(estate.iter_family('EmpiricalUniverse'))
        hist=AuthorityRef('SOURCE_SEMANTICS_TOPOLOGY','Q006-HIST-DEFER',semantic_hash({'state':'DEFER','source':estate.i02.source,'release':estate.i02.release}))
        defer=EmpiricalUniverse(typed_state=universe.typed_state,authority_snapshot_refs=(hist,),dependency_refs=universe.dependency_refs,producer_replay_locator_or_reference_root=universe.producer_replay_locator_or_reference_root,**dict(universe.semantic_fields))
        # Build query/predicate with defer universe; retain original authorities.
        predicate=make_empirical_predicate(predicate_ast=dict(pred.predicate_ast),typed_state=pred.typed_state,authority_snapshot_refs=pred.authority_snapshot_refs,dependency_refs=pred.dependency_refs,producer_replay_locator_or_reference_root=pred.producer_replay_locator_or_reference_root,grammar_authority_ref=pred.grammar_authority_ref,coordinate_question_value_refs=pred.coordinate_question_value_refs,risk_set_refs=pred.risk_set_refs,scope_refs=(defer.ref,),same_respondent_binding_semantics=pred.same_respondent_binding_semantics,operator_semantics_refs=pred.operator_semantics_refs)
        qf=dict(query.semantic_fields); qf['empirical_universe_refs']=(defer.ref,); qf['scope_refs']=(defer.ref,); qf['condition_predicate_ref']=predicate.ref
        q=EmpiricalQuerySpec(typed_state=query.typed_state,authority_snapshot_refs=query.authority_snapshot_refs,dependency_refs=(predicate.ref,),producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,**qf)
        positive=AuthorityRef('Q006_RECORDED_UNIVERSE_USE','Q006-POSITIVE-USE',semantic_hash({'hist':hist.key,'source':estate.i02.source,'release':estate.i02.release}))
        use=RecordedUniverseUse(historical_ref=hist,positive_ref=positive,owner_decision_sha256='sourcefree',operation_document_sha256='sourcefree',source_root=estate.i02.source,release_root=estate.i02.release,universe_root=defer.ref.key,replay_root=estate.i02.replay,question_ref=source['qrefs']['Y'],query_ref=q.ref,predicate_ref=predicate.ref,scope='Q103_RAW_UNWEIGHTED_RECORDED_RESPONSE_ONLY',current_verifier=lambda: True)
        # Replace index universe and attach the scoped use handle.
        original=DirectEstateI03Session.indices_for
        original_query = query
        def indices_for(self,*,query,release_refs):
            ((uni,idx),)=original(self,query=original_query,release_refs=release_refs)
            idx=dataclasses.replace(idx,universe=defer,universe_use=use)
            return ((uni,idx),)
        mp.setattr(DirectEstateI03Session,'indices_for',indices_for)
        with DirectEstateI03Session(estate) as session:
            result=execute_empirical_query(repository=session,query=q,predicate=predicate,authority_registry=catalog.authority_registry,release_refs=(estate.native_release_ref,))
            result2=execute_empirical_query(repository=session,query=q,predicate=predicate,authority_registry=catalog.authority_registry,release_refs=(estate.native_release_ref,))
        def refused(fn):
            try:
                fn(); return False
            except Exception:
                return True
        negatives={
            'missing_current': refused(lambda: dataclasses.replace(use,current_verifier=lambda: False).authorize(defer,q,predicate)),
            'wrong_history': refused(lambda: dataclasses.replace(use,historical_ref=AuthorityRef('SOURCE_SEMANTICS_TOPOLOGY','WRONG','0'*64)).authorize(defer,q,predicate)),
            'wrong_query': refused(lambda: dataclasses.replace(use,query_ref=ExactRef('EmpiricalQuerySpec@1.0.0','wrong','0'*64)).authorize(defer,q,predicate)),
        }
        print(json.dumps({'schema':'ANVIL_Q006_UNIVERSE_USE_SOURCEFREE@1','status':'NATIVE_GREEN' if result.facts and result.facts[0].typed_state=='SUPPORTED' else 'NATIVE_RED','typed_state':result.facts[0].typed_state if result.facts else None,'denominator':result.facts[0].raw_denominator_support if result.facts else None,'detail':result.facts[0].semantic_fields.get('execution_detail') if result.facts else None,'cells':len(result.facts[0].target_topology.get('complete_cell_semantic_projection',())) if result.facts else 0,'historical_state':'DEFER','both_authority_refs_in_result':hist.key in [r.key for r in result.facts[0].authority_snapshot_refs] and positive.key in [r.key for r in result.facts[0].authority_snapshot_refs] if result.facts else False,'replay':result.facts[0].semantic_fields.get('replay_ref') if result.facts else None,'repeat_replay_equal':bool(result.facts and result2.facts and result.facts[0].semantic_fields.get('replay_ref')==result2.facts[0].semantic_fields.get('replay_ref')),'negatives':negatives},indent=2,default=str))
        return 0
    finally: mp.undo()
if __name__=='__main__': raise SystemExit(main())
