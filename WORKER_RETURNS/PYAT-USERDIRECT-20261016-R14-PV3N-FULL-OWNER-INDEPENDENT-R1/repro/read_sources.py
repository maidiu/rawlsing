from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1]
PACKETS={'pv3':('5c70c7d347998907c1c8a865f833dad581777a0e','PYAT-USERDIRECT-20261015-R12-PV3-INDEPENDENT-ROOT-CUSTODY-REPAIR-R1'),'pv3i':('44a82d764f6cb58fb56af6b20d32313affe68962','PYAT-USERDIRECT-20261015-R13-PV3I-INDEPENDENT-CUSTODY-COURT-R1'),'pv2i':('1de1c9c57bffa8bb663edd44af744379b028f698','PYAT-USERDIRECT-20261015-R11-PV2I-INDEPENDENT-ORIGINAL-SCOPE-R1')}
rows=[]
for name,(rev,folder) in PACKETS.items():
 prefix='WORKER_RETURNS/'+folder+'/'
 for p in subprocess.check_output(['git','ls-tree','-r','--name-only',rev,prefix],text=True).splitlines():
  b=subprocess.check_output(['git','show',rev+':'+p]);blob=subprocess.check_output(['git','rev-parse',rev+':'+p],text=True).strip()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
  d=R/'runtime'/name/p[len(prefix):];d.parent.mkdir(parents=True,exist_ok=True)
  if d.exists():assert d.read_bytes()==b
  else:d.write_bytes(b)
  rows.append(dict(commit=rev,path=p,blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),local=str(d.relative_to(R))))
(R/'source_packet_receipts.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Pinned packets verified',len(rows),'files; no candidate imported or executed')
