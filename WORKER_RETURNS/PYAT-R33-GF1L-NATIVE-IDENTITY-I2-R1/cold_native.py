import importlib.util,json,os,sys,hashlib
from pathlib import Path
s=importlib.util.spec_from_file_location('gf1l_fixture',os.environ['GF1J_GF1G_TEST'])
h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
r=h._template(); got=h.CONS(r)
assert h.GB.reattest()==74
assert got['separation_class']=='EXACT_PAIR_SEPARATION'
assert got['production_owner_commit'] is False
receipt=h.GB.import_custody()
for row in receipt['imports']:
    assert (h.COURT/row['file']).is_file()
print(json.dumps(dict(pid=os.getpid(),relation_hash=r.content_hash,result=got,custody=receipt,producer_file=h.G.__file__,consumer_file=sys.modules[h.CONS.__module__].__file__),sort_keys=True,indent=2))
