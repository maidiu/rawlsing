from __future__ import annotations
import json, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_r157_projection_adapter import build_validated_c11_release_from_config, decode_fixture_config, build_governed_c11_projection
from rawlsing_next.pre553_source_i02_handoff import open_direct_native_i03
from rawlsing_next.tests.test_pyat960_s1e_support import build, source_fixture
from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _branch_predicate, _query, _run

def main():
    proof=Path(tempfile.mkdtemp(prefix='q2-native-query-'))
    fixture=source_fixture(proof)
    handoff=build(proof,fixture,name='q2.sqlite')
    incidence=decode_fixture_config(fixture['config'],fixture['path'])
    try: legacy=build_validated_c11_release_from_config(fixture['config'],incidence=incidence,batch_size=4)
    finally: incidence.close()
    repo=C11Repository((legacy,))
    projection=build_governed_c11_projection(fixture['config'])
    source={
      'universe': projection.universes[0],
      'respondents': {r.ref.key:r for r in projection.respondents},
      'qrefs': {'q101': projection.questions[0].native_question_ref},
      'risk_refs': {'R': projection.routing[0].risk_set_ref},
      'authorities': projection.authority_snapshots,
      'repo': repo,
      'release_ref': legacy.release_ref,
    }
    qa=_query_authority('q2-native')
    pred=_branch_predicate(source,qa,tag='q2-native')
    query=_query(source,qa,pred,('q101',),tag='q2-native',target_authority_refs=(projection.questions[0].semantic_authority_ref,))
    reader=open_direct_native_i03(handoff,repo,legacy.release_ref)
    try:
        result=_run(source,qa,pred,query)
        for fact in result.facts:
            print('STATE',fact.typed_state)
            print(json.dumps({k:str(v) for k,v in fact.target_topology.items()},indent=2)[:8000])
    finally:
        reader.close()
    return 0
raise SystemExit(main())
