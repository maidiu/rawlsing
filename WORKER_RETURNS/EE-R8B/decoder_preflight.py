import datetime,hashlib,json,os,pathlib,platform,sys
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'runtime_code'))
from rawlsing_next.pre553_physical_decoder import decode_sav,decode_dta
import pyreadstat,pyarrow
universe=sys.argv[2]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
source=root/'sources'/('WVS Wave 7.sav' if universe=='WVS7' else 'LITS-2006-data.dta')
inc=decode_sav(source) if universe=='WVS7' else decode_dta(source,encoding='latin1')
expected=(97220,613) if universe=='WVS7' else (29002,1198)
assert (inc.row_count,len(inc.variables))==expected
required=['Q138','Q291G5','Q291P5'] if universe=='WVS7' else ['q301_2','q301_7']
names=[v.name for v in inc.variables]
assert all(v in names for v in required)
print(json.dumps({'status':'PASS_REAL_EXACT_DECODER_PREFLIGHT','universe':universe,'pid':os.getpid(),'started_at_utc':start,'ended_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'executable':sys.executable,'python':sys.version,'sys_platform':sys.platform,'source_sha256':inc.source_sha256,'source_bytes':source.stat().st_size,'rows':inc.row_count,'variables':len(inc.variables),'required_source_coordinates':required,'reader_configuration':dict(inc.reader_configuration),'runtime_versions':{'pyreadstat':pyreadstat.__version__,'pyarrow':pyarrow.__version__},'runtime_freeze_sha256':hashlib.sha256((root/'runtime_freeze.json').read_bytes()).hexdigest(),'scope':'decoder/import/execution-surface preflight only; no candidate invocation or reference-oracle materialization'}))
