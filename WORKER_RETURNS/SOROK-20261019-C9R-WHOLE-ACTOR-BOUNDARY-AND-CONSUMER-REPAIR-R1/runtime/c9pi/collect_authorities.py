from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;REPO=R.parents[1]
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO)
rows=[]
def save(blob,dst,path='',commit=''):
 b=git('cat-file','blob',blob);out=R/'frozen/authorities'/dst;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
 rows.append(dict(blob=blob,sha256=hashlib.sha256(b).hexdigest(),path=path,commit=commit,staged=str(out.relative_to(R))))
known={'CAN008_R2_adoption.md':'a6bc1555489271e1adb2271ed02d46bb7f888170','CAN008_R2_body.md':'b80dd6925066510ecbbfec7b427bf9f688475663','CAN008_v1.md':'976c59086b938992114f68621f149687670e306d','CAN011.md':'1ed04e62a363493bc7032a99139454a3126e6ea0','ADP007.md':'28813c575c681abf3c6235ff23c6f01f7123acc7','ADP008.md':'6428e26f4e85ede66a10ea2761362ff0cd84fc5e','ADP019.md':'5c38772ea193e5a3f20da23c16df086a153ab2f2','ADP016.md':'0b7bbe29f6509e31ac7d842962a2bf3d636daa2c','ADP017.md':'6b4162df27003bec413074178c46fea6360d71a0','ADP020.md':'1911352f4bd5b04dfeaa0f26930e6702998bb76d','proof_law.md':'a83d054a656ff9d7bf32b18495bd0a1843c02da9'}
for dst,blob in known.items():save(blob,dst)
for commit,prefix in [('4a806ab74e1c348805a546658c8b2c71fbdd53d8','SOROK_PRODUCT_CONTROL_ROOM/'),('b09a624e637c85ada6563b91ec12ab5213e9c169','CROSS_HQ_CONTROL_ROOM/'),('1a25b19dd01e8e7954e38c59ffc7e52c50739c9f','WORKER_RETURNS/')]:
 for line in git('ls-tree','-r',commit,prefix).decode().splitlines():
  meta,path=line.split('\t');blob=meta.split()[-1];name=Path(path).name
  take=(prefix.startswith('SOROK') and (name.startswith(('00','07_FRESH','SOROK_ONLY_PARALLEL')))) or (prefix.startswith('CROSS') and any(s in name for s in ('TERMINAL_PRODUCT','PARALLEL_FLIGHT'))) or ('B3AS' in path and name in ('00_RETURN.md','00_REVIEW.md','00_RETURN_REVIEW.md'))
  if take:save(blob,name,path,commit)
for line in git('ls-tree','-r','HEAD','data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/').decode().splitlines():
 meta,path=line.split('\t')
 if any(x in path for x in ('ADP_010_','ADP_021_')) and path.endswith('AUTHORITY.md'):save(meta.split()[-1],path.split('/')[-2]+'.md',path,'4a806ab74e1c348805a546658c8b2c71fbdd53d8')
for commit,path,dst in [
 ('7ffc20ddb30f71034abf8d02c224d13d6952e11f','WORKER_RETURNS/SOROK-R3-HQ319-LIFE1-WORLD-RELATION-EPOCHAL-COURT-R1/00_RETURN.md','LIFE1.md'),
 ('1a25b19dd01e8e7954e38c59ffc7e52c50739c9f','WORKER_RETURNS/SOROK-20261018-B3A-SCHEMA-READSET-REPAIR-INDEPENDENT-I2-R1/00_RETURN.md','B3AS.md'),
 ('1a25b19dd01e8e7954e38c59ffc7e52c50739c9f','WORKER_RETURNS/SOROK-20261018-B3A-SCHEMA-READSET-REPAIR-INDEPENDENT-I2-R1/02_REQUIREMENTS_AND_LIMITATIONS.md','B3AS_limitations.md'),
 ('b09a624e637c85ada6563b91ec12ab5213e9c169','CROSS_HQ_CONTROL_ROOM/HQ_TERMINAL_DELIVERABLE_CONTINUITY_AND_ANTI_MICROFOCUS_LAW_R1.md','terminal_law.md')]:
 save(git('rev-parse',commit+':'+path).decode().strip(),dst,path,commit)
(R/'custody/authority_preimages.json').write_text(json.dumps(rows,indent=2)+'\n')
print('authorities',len(rows))
