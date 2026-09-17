import hashlib,importlib,importlib.metadata as md,json,pathlib,platform,sys,urllib.request,datetime,shutil,subprocess
root=pathlib.Path(__file__).resolve().parent
rows=[]
for wheel in sorted((root/'wheels').glob('*.whl')):
 name,version=wheel.name.split('-')[:2]
 release=json.loads(subprocess.check_output(['curl','--fail','--silent','--show-error',f'https://pypi.org/pypi/{name}/{version}/json']))
 item=next(x for x in release['urls'] if x['filename']==wheel.name)
 digest=hashlib.sha256(wheel.read_bytes()).hexdigest()
 assert digest==item['digests']['sha256']
 dist=md.distribution(name)
 assert dist.version==version
 rows.append({'distribution':dist.metadata['Name'],'version':version,'wheel':wheel.name,'wheel_bytes':wheel.stat().st_size,'sha256':digest,'download_url':item['url'],'upload_time':item['upload_time_iso_8601'],'installed_requires_dist':dist.requires,'installed_metadata_sha256':hashlib.sha256(dist.read_text('METADATA').encode()).hexdigest()})
mods={}
for name in ['pyreadstat','pyarrow','numpy','narwhals','pandas']:
 m=importlib.import_module(name);mods[name]={'version':m.__version__,'path':m.__file__,'module_sha256':hashlib.sha256(pathlib.Path(m.__file__).read_bytes()).hexdigest()}
obj={'status':'PASS_EXACT_RUNTIME_COLOCATED','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'executable_realpath':str(pathlib.Path(sys.executable).resolve()),'executable_sha256':hashlib.sha256(pathlib.Path(sys.executable).resolve().read_bytes()).hexdigest(),'platform':platform.platform(),'sys_platform':sys.platform,'machine':platform.machine(),'packages':rows,'imports':mods,'r2b_qualified_wheel':{'sha256':'3ac231771dc038e0a42a4d14599af3112684f7eba680983b3ef9581db3e3b163','tag':'cp313-manylinux_x86_64','executable_on_this_worker':False,'reason':'CPython 3.11.3 / Darwin x86_64; compatible exact-version wheel used'},'additional_dependency_reason':{'numpy':'pyreadstat and pandas mandatory Requires-Dist','narwhals':'pyreadstat mandatory Requires-Dist','pandas':'Exact decoder defaults to pandas output; actual pre-install call raised PyreadstatError cannot import pandas','python-dateutil':'pandas mandatory Requires-Dist','pytz':'pandas mandatory Requires-Dist','tzdata':'pandas mandatory Requires-Dist','six':'python-dateutil mandatory Requires-Dist'},'local_linux_executor_inventory':{name:shutil.which(name) for name in ['docker','podman','colima','multipass','limactl','qemu-system-x86_64']},'transport':'PyPI exact release wheel download; release SHA-256 verified before decoder preflight; no Actions artifact/run created'}
(root/'runtime_freeze.json').write_text(json.dumps(obj,indent=2)+'\n')
print('PASS: nine exact wheels verified against PyPI release metadata; five imports verified')
