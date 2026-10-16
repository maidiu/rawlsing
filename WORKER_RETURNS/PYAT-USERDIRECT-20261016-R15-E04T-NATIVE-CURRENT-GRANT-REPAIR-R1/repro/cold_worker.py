"""Fresh process; hydrate explicit fixture permission state before any query."""
from common import *
import sys,os
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
fixture=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[2])
def hydrate(d):return AuthoritySnapshot(typed_state=d['typed_state'],authority_snapshot_refs=d['authority_snapshot_refs'],dependency_refs=d['dependency_refs'],producer_replay_locator_or_reference_root=d['producer_replay_locator_or_reference_root'],**d['semantic_fields'])
s=GenericSelectedWorldService();s.provider.world['registry']=AuthorityRegistry(hydrate(x) for x in fixture['grants']);ss=s.select()
a=consume(s,ss);b=evaluate(s,ss,PROPOSALS)
if fixture['state']=='restored':assert a==fixture['nonparent'] and b==fixture['scenario']
else:
 for result in (a,b):
  empirical=result['material']['empirical'];assert empirical['state']=='PARTIAL_TYPED_EMPIRICAL_SUPPORT'
  assert all(x['state']!='EXACT_SUPPORTED' and x['cells']==[] and x['denominator']==0 and x['geometry'] is None for x in empirical['steps'])
 assert not s.provider.cache and not s.provider._accepted
fresh=GenericSelectedWorldService();fresh.provider.world['registry']=AuthorityRegistry(hydrate(x) for x in fixture['grants']);fs=fresh.select();fresh.provider.cache[('Y',(('A',1),))]=fixture['projection']
try:fresh.possibilities(fs)
except ValueError as e:injection_error=str(e)
else:raise AssertionError('FOREIGN_PROCESS_PROJECTION_ACCEPTED')
assert injection_error=='UNATTESTED_NATIVE_CACHE_ENTRY'
fresh.provider.cache.clear();assert consume(fresh,fs)==a
out.write_text(json.dumps(dict(pid=os.getpid(),results=dict(state=fixture['state'],nonparent=a,scenario=b,foreign_projection_refused=injection_error,permission_fixture_attached_before_query=True)),indent=2)+'\n')
