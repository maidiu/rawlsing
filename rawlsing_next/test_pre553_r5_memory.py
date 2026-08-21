import json, os, subprocess, sys, textwrap


def probe(n):
    code=r'''
import hashlib, json, os, resource, shutil, sys, tempfile
from rawlsing_next.pre553_r5_carrier import R5LongShardedBuilder,R5LongShardedReader
from rawlsing_next.pre553_r5_model import R5BuildConfig,R5CanonicalRow,R5ReleaseIdentity

def h(s): return hashlib.sha256(s.encode()).hexdigest()
n=int(sys.argv[1]); root=tempfile.mkdtemp(prefix='r5mem-')
rid=R5ReleaseIdentity('REL-MEM',h('semantic'),{'kind':'SOURCE_ARTIFACT','object_id':'src','content_hash':h('source')},h('manifest'),{f'M{i:02d}':('p',) for i in range(1,19)},{'decoder':'frozen'},h('compiler'),h('c11'))
cfg=R5BuildConfig(run_max_rows=128,run_max_bytes=32768,shard_max_rows=257,shard_max_bytes=65536,merge_fan_in=4,verified_spool_memory_bytes=8192)
def rows():
    for i in range(n):
        payload={'i':i,'unique':('u%08d-'%i)+('x'*96),'exception':{'rank':i%9,'state':'E'+str(i%13)} if i%10!=0 else None}
        yield R5CanonicalRow('rel-%04d'%(i%997),'RespondentEvent@1','e%012d'%i,h(json.dumps(payload,sort_keys=True)),payload)
target=os.path.join(root,'release')
t=R5LongShardedBuilder(cfg).build(rows(),release_identity=rid,target_directory=target)
a=R5LongShardedReader(target).full_audit()
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
if sys.platform!='darwin': rss*=1024
print(json.dumps({'n':n,'peak_rss_bytes':int(rss),'initial_runs':t['initial_runs'],'shards':t['final_shards'],'rows':a['canonical_rows']}))
shutil.rmtree(root)
'''
    out=subprocess.check_output([sys.executable,'-c',code,str(n)],cwd=os.path.dirname(os.path.dirname(__file__)),text=True)
    return json.loads(out)


def test_increasing_n_memory_plateaus_under_fixed_bounds():
    results=[probe(n) for n in (4000,16000,64000)]
    assert [r['rows'] for r in results]==[4000,16000,64000]
    assert results[-1]['initial_runs'] > results[0]['initial_runs']
    assert results[-1]['shards'] > results[0]['shards']
    baseline=results[0]['peak_rss_bytes']
    # Fixed run/shard/spool bounds mean N grows disk/time, not live structures.
    # Allow allocator/import noise of 16 MiB while forbidding N-proportional growth.
    assert results[-1]['peak_rss_bytes'] <= baseline + 16*1024*1024, results
