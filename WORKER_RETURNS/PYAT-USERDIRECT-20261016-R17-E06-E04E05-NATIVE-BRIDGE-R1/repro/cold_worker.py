from bootstrap import ROOT,RT
from support import *
from observe import Observer
import sys,os,hashlib
ledger_path=ROOT/sys.argv[1];dest=ROOT/sys.argv[2]
assert ledger_path.resolve().is_relative_to(ROOT) and dest.resolve().is_relative_to(ROOT)
ledger=json.loads(ledger_path.read_text());obs=Observer();obs.start()
b=bridge();b.provider.world['registry']=AuthorityRegistry(hydrate(x) for x in ledger['grants'])
p=b.prepare(request());output=b.read(p)
# A prior-process projection is never a trusted E04T owner entry or grant.
f=bridge();f.provider.world['registry']=AuthorityRegistry(hydrate(x) for x in ledger['grants']);f.provider.cache[('Y',(('A',1),))]=ledger['projection']
try:f.prepare(request())
except ValueError as exc:foreign=dict(type=type(exc).__name__,reason=str(exc))
else:raise AssertionError('FOREIGN_PROCESS_PROJECTION_ACCEPTED')
assert foreign['reason']=='UNATTESTED_NATIVE_CACHE_ENTRY'
obs.stop();trace=obs.result()
dest.write_text(json.dumps(dict(pid=os.getpid(),ledger_sha256=hashlib.sha256(ledger_path.read_bytes()).hexdigest(),grant_ledger_attached_before_first_query=True,result=output,foreign_projection=foreign,trace=trace),separators=(',',':'))+'\n')
print('E06 COLD',ledger['state'],output['state'],'native imports',len(trace['imports']))
