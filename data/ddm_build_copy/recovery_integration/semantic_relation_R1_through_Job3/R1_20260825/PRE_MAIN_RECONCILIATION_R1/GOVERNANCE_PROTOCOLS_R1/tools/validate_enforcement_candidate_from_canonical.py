#!/usr/bin/env python3
"""Fail-closed canonical predecessor gate: W56N object/ref trust recovery."""
from __future__ import annotations
import sys
_FLAGS={k:bool(getattr(sys.flags,k,0)) for k in ('isolated','ignore_environment','no_user_site','no_site','safe_path')}
if not all(_FLAGS.values()):
    sys.stderr.write('FAIL_PYTHON_EXECUTION_NOT_ISOLATED: invoke with `python3 -I -S`; '+','.join(f'{k}={int(v)}' for k,v in _FLAGS.items())+'\n'); raise SystemExit(97)
import argparse,csv,hashlib,json,os,re,stat,subprocess
from pathlib import Path
from typing import Any
CANONICAL_REF='integration/pre-main-reconciliation-r1'
ROOT_REL='data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1'
GOV_REL=ROOT_REL+'/GOVERNANCE_PROTOCOLS_R1'
SELF_REL=GOV_REL+'/tools/validate_enforcement_candidate_from_canonical.py'
MANIFEST_REL=GOV_REL+'/GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv'
AUTH_SCHEMA_REL=GOV_REL+'/HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json'
RESULT_SCHEMA_REL=GOV_REL+'/HOSTILE_AUDIT_RESULT_SCHEMA_R1.json'
AUTH_PREFIX=ROOT_REL+'/AUDIT_AUTHORIZATIONS/'
OID_RE=re.compile(r'^(?:[0-9a-f]{40}|[0-9a-f]{64})$')
IMM_RE=re.compile(r'^(?P<sha>[0-9a-f]{40}|[0-9a-f]{64}):(?P<path>[^\n]+)$')
REF_RE=re.compile(r'^refs/(?:heads|remotes)/[A-Za-z0-9][A-Za-z0-9._/-]*$')
SCRIPT=Path(__file__).resolve(); MAX_META=8*1024*1024; MAX_TREES=200000; MAX_ENTRIES=2000000
class TrustFailure(RuntimeError): pass

def within(p:Path,r:Path)->bool:
    try: p=p.resolve(strict=False); r=r.resolve(strict=False); return p==r or r in p.parents
    except Exception: return True

def haslink(p:Path)->bool:
    try:
        if not p.is_absolute(): return True
        cur=Path(p.anchor)
        for x in p.parts[1:]:
            cur/=x
            if cur.is_symlink(): return True
        return False
    except Exception: return True

def roots(raw:str)->tuple[Path,Path]:
    p=Path(raw)
    if not p.is_absolute() or haslink(p): raise TrustFailure('repository-root-not-bounded')
    try:r=p.resolve(strict=True)
    except Exception as e: raise TrustFailure(f'repository-root-unresolvable:{e}') from e
    if r!=p or not r.is_dir() or not within(SCRIPT,r): raise TrustFailure('repository-root-invalid')
    g=r/'.git'
    if haslink(g): raise TrustFailure('repository-git-dir-symlink-component')
    try: gr=g.resolve(strict=True)
    except Exception as e: raise TrustFailure(f'repository-git-dir-unresolvable:{e}') from e
    if gr!=g or not gr.is_dir(): raise TrustFailure('repository-git-dir-invalid')
    o=gr/'objects'
    if haslink(o): raise TrustFailure('repository-object-dir-symlink-component')
    try: orr=o.resolve(strict=True)
    except Exception as e: raise TrustFailure(f'repository-object-dir-unresolvable:{e}') from e
    if orr!=o or not orr.is_dir(): raise TrustFailure('repository-object-dir-invalid')
    c=gr/'commondir'
    if c.exists() or c.is_symlink(): raise TrustFailure('repository-common-dir-indirection-rejected')
    return r,gr

def fingerprint(p:Path)->dict[str,Any]:
    try:
        s=p.stat()
        if not stat.S_ISREG(s.st_mode): raise TrustFailure('trusted-git-not-regular-file')
        h=hashlib.sha256()
        with p.open('rb') as f:
            for b in iter(lambda:f.read(1<<20),b''): h.update(b)
        return {'realpath':str(p),'sha256':h.hexdigest(),'device':int(s.st_dev),'inode':int(s.st_ino),'size':int(s.st_size),'mtime_ns':int(s.st_mtime_ns)}
    except TrustFailure: raise
    except Exception as e: raise TrustFailure(f'trusted-git-fingerprint-failed:{e}') from e

def gitexe(raw:str,repo:Path)->tuple[Path,dict[str,Any]]:
    p=Path(raw)
    if not p.is_absolute() or haslink(p): raise TrustFailure('trusted-git-path-not-bounded')
    try:r=p.resolve(strict=True)
    except Exception as e: raise TrustFailure(f'trusted-git-unresolvable:{e}') from e
    if r!=p or within(r,repo) or not r.is_file() or not os.access(r,os.X_OK): raise TrustFailure('trusted-git-invalid')
    return r,fingerprint(r)

def env()->dict[str,str]:
    e={'LC_ALL':'C','LANG':'C','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':os.devnull,'GIT_CONFIG_SYSTEM':os.devnull,'GIT_CONFIG_COUNT':'0','GIT_NO_REPLACE_OBJECTS':'1','GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0','GIT_PAGER':'','PAGER':'','GIT_OPTIONAL_LOCKS':'0'}
    if os.name=='nt':
        for k in ('SystemRoot','WINDIR'):
            if os.environ.get(k): e[k]=os.environ[k]
    return e

def alg(oid:str)->tuple[str,int]:
    if not OID_RE.fullmatch(oid or ''): raise TrustFailure('object-id-not-exact-pure-hex')
    return ('sha1',20) if len(oid)==40 else ('sha256',32)

def same_alg(oid:str,a:str)->None:
    if alg(oid)[0]!=a: raise TrustFailure('mixed-object-id-algorithms')

def oid_for(t:str,p:bytes,a:str)->str:
    if t not in {'commit','tree','blob','tag'}: raise TrustFailure('unsupported-git-object-type')
    h=hashlib.new(a); h.update(t.encode()+b' '+str(len(p)).encode()+b'\0'+p); return h.hexdigest()

def comps(rel:str)->list[str]:
    if not rel or rel.startswith('/') or '\0' in rel: raise TrustFailure('metadata-relative-path-invalid')
    ps=rel.split('/')
    if any(x in {'','.','..'} for x in ps): raise TrustFailure('metadata-relative-path-invalid-component')
    return ps

def meta(g:Path,rel:str,required:bool=False,max_bytes:int=MAX_META)->bytes|None:
    ps=comps(rel)
    if os.name!='posix' or not hasattr(os,'O_NOFOLLOW') or not hasattr(os,'O_DIRECTORY'): raise TrustFailure('bounded-metadata-reader-posix-openat-required')
    d=os.open(str(g),os.O_RDONLY|os.O_DIRECTORY)
    try:
        for x in ps[:-1]:
            try:n=os.open(x,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=d)
            except FileNotFoundError:
                if required: raise TrustFailure(f'metadata-required-path-missing:{rel}')
                return None
            except OSError as e: raise TrustFailure(f'metadata-path-component-not-bounded:{rel}:{e.errno}') from e
            os.close(d); d=n
        try:f=os.open(ps[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=d)
        except FileNotFoundError:
            if required: raise TrustFailure(f'metadata-required-path-missing:{rel}')
            return None
        except OSError as e: raise TrustFailure(f'metadata-file-not-bounded:{rel}:{e.errno}') from e
        try:
            s=os.fstat(f)
            if not stat.S_ISREG(s.st_mode) or s.st_size>max_bytes: raise TrustFailure(f'metadata-file-invalid:{rel}')
            out=b''
            while True:
                b=os.read(f,min(1<<20,max_bytes+1-len(out)))
                if not b: break
                out+=b
                if len(out)>max_bytes: raise TrustFailure(f'metadata-file-too-large:{rel}')
            return out
        finally: os.close(f)
    finally:
        try:os.close(d)
        except OSError:pass

def metakind(g:Path,rel:str)->str:
    ps=comps(rel)
    if os.name!='posix' or not hasattr(os,'O_NOFOLLOW') or not hasattr(os,'O_DIRECTORY'): raise TrustFailure('bounded-metadata-reader-posix-openat-required')
    d=os.open(str(g),os.O_RDONLY|os.O_DIRECTORY)
    try:
        for x in ps[:-1]:
            try:n=os.open(x,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=d)
            except FileNotFoundError:return 'missing'
            except OSError as e: raise TrustFailure(f'metadata-path-component-not-bounded:{rel}:{e.errno}') from e
            os.close(d); d=n
        try:s=os.stat(ps[-1],dir_fd=d,follow_symlinks=False)
        except FileNotFoundError:return 'missing'
        if stat.S_ISLNK(s.st_mode): raise TrustFailure(f'metadata-symlink-rejected:{rel}')
        if stat.S_ISREG(s.st_mode): return 'file'
        if stat.S_ISDIR(s.st_mode): return 'dir'
        raise TrustFailure(f'metadata-special-node-rejected:{rel}')
    finally:
        try:os.close(d)
        except OSError:pass

def controls(raw:bytes|None)->dict[str,str]:
    if raw is None:return {}
    try:text=raw.decode('utf-8','strict')
    except UnicodeDecodeError as e: raise TrustFailure('git-config-not-utf8') from e
    sec=''; out={}
    for z in text.splitlines():
        s=z.strip()
        if not s or s[0] in '#;':continue
        if s.startswith('[') and s.endswith(']'): sec=s[1:-1].split(None,1)[0].strip().lower(); continue
        if '=' not in s:continue
        k,v=[x.strip() for x in s.split('=',1)]; key=f'{sec}.{k.lower()}'
        if key in {'core.repositoryformatversion','extensions.objectformat','extensions.refstorage'}:
            if key in out: raise TrustFailure(f'duplicate-storage-control:{key}')
            out[key]=v.lower()
    rf=out.get('core.repositoryformatversion','0')
    if rf not in {'0','1'}: raise TrustFailure('unsupported-repository-format-version')
    of=out.get('extensions.objectformat','sha1')
    if of not in {'sha1','sha256'}: raise TrustFailure('unsupported-object-format')
    rs=out.get('extensions.refstorage','files')
    if rs!='files': raise TrustFailure('unsupported-ref-storage')
    return {'repositoryformatversion':rf,**({'objectformat':of} if of!='sha1' else {}),**({'refstorage':rs} if 'extensions.refstorage' in out else {})}

def packed(raw:bytes|None)->dict[str,str]:
    if raw is None:return {}
    try:text=raw.decode('ascii','strict')
    except UnicodeDecodeError as e: raise TrustFailure('packed-refs-not-ascii') from e
    out={}; last=False
    for line in text.splitlines():
        if not line:continue
        if line.startswith('#'):last=False;continue
        if line.startswith('^'):
            if not last or not OID_RE.fullmatch(line[1:]): raise TrustFailure('packed-refs-malformed-peeled-line')
            last=False;continue
        try:o,r=line.split(' ',1)
        except ValueError as e: raise TrustFailure('packed-refs-malformed-line') from e
        if not OID_RE.fullmatch(o) or not r.startswith('refs/') or any(c.isspace() for c in r) or r in out: raise TrustFailure('packed-refs-malformed-or-duplicate')
        out[r]=o; last=True
    return out

def loose(g:Path,ref:str)->str|None:
    b=meta(g,ref)
    if b is None:return None
    if b.startswith(b'ref:'): raise TrustFailure('symbolic-ref-indirection-rejected')
    if b.endswith(b'\n'): b=b[:-1]
    if b.endswith(b'\r') or b.find(b'\n')>=0 or b.find(b'\r')>=0: raise TrustFailure('loose-ref-multiline-rejected')
    try:s=b.decode('ascii','strict')
    except UnicodeDecodeError as e: raise TrustFailure('loose-ref-not-ascii') from e
    if not OID_RE.fullmatch(s): raise TrustFailure('loose-ref-not-exact-oid')
    return s

class GitTrust:
    def __init__(self,x:Path,r:Path,g:Path,fp:dict[str,Any]):self.executable=x;self.repo=r;self.git_dir=g;self.before=fp;self.env=env();self._packed=None
    def base(self):return [str(self.executable),'--no-pager','--no-replace-objects',f'--git-dir={self.git_dir}',f'--work-tree={self.repo}']
    def run(self,*a:str)->tuple[bool,bytes,bytes]:
        try:
            p=subprocess.run([*self.base(),*a],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=self.env,timeout=20,check=False);return p.returncode==0,p.stdout,p.stderr
        except Exception:return False,b'',b''
    def text(self,*a:str)->tuple[bool,str]:
        ok,b,_=self.run(*a)
        if not ok:return False,''
        try:return True,b.decode('utf-8','strict').strip()
        except UnicodeDecodeError:return False,''
    def read_object(self,o:str,t:str)->bytes:
        a,_=alg(o); ok,ty,_=self.run('cat-file','-t',o)
        if not ok:raise TrustFailure('git-object-type-read-failed')
        try:ts=ty.decode('ascii','strict').strip()
        except UnicodeDecodeError as e:raise TrustFailure('git-object-type-not-ascii') from e
        if ts!=t:raise TrustFailure(f'git-object-type-mismatch:{ts}:{t}')
        ok,p,_=self.run('cat-file',t,o)
        if not ok:raise TrustFailure('git-object-payload-read-failed')
        if oid_for(t,p,a)!=o:raise TrustFailure('git-object-id-rebind-mismatch')
        return p
    def _verify_payload(self,o:str,t:str,p:bytes)->None:
        a,_=alg(o)
        if oid_for(t,p,a)!=o:raise TrustFailure('git-object-id-rebind-mismatch')
    def read_verified_commit(self,o:str)->bytes:return self.read_object(o,'commit')
    def commit(self,o:str)->bytes:return self.read_verified_commit(o)
    def tree(self,o:str)->bytes:return self.read_object(o,'tree')
    def blob(self,o:str)->bytes:return self.read_object(o,'blob')
    def packed_refs(self)->dict[str,str]:
        if self._packed is None:self._packed=packed(meta(self.git_dir,'packed-refs'))
        return self._packed
    def resolve_ref(self,r:str)->tuple[bool,str]:
        try:
            if not REF_RE.fullmatch(r) or '..' in r or '@{' in r or r.endswith(('.', '/')) or '//' in r:return False,''
            l=loose(self.git_dir,r); p=self.packed_refs().get(r)
            if l and p and l!=p:raise TrustFailure('loose-packed-ref-conflict')
            o=l or p
            if not o:return False,''
            self.commit(o); return True,o
        except TrustFailure:return False,''
    def repository_hardening(self)->tuple[bool,dict[str,Any]]:
        d={}
        try:
            d['storage_controls']=controls(meta(self.git_dir,'config',required=True))
            d['reftable_kind']=metakind(self.git_dir,'reftable'); d['tables.list_kind']=metakind(self.git_dir,'tables.list')
            if d['reftable_kind']!='missing' or d['tables.list_kind']!='missing':return False,d
            pr=self.packed_refs();d['packed_ref_count']=len(pr)
            repl=sorted(r for r in pr if r.startswith('refs/replace/'))
            rk=metakind(self.git_dir,'refs/replace')
            if rk=='file':return False,d
            if rk=='dir' and any((self.git_dir/'refs/replace').iterdir()):repl.append('LOOSE_REPLACE_NAMESPACE_NONEMPTY')
            d['replace_refs_present']=repl
            if repl:return False,d
            for rel,key in [('info/grafts','grafts'),('objects/info/alternates','alternates'),('objects/info/http-alternates','http_alternates'),('shallow','shallow')]:
                b=meta(self.git_dir,rel); d[key]={'present':b is not None,'nonempty':bool(b and b.strip())}
                if b and b.strip():return False,d
            ok,top=self.text('rev-parse','--show-toplevel'); d['git_reported_worktree_root']=top if ok else 'UNRESOLVED'
            if not ok or Path(top).resolve(strict=True)!=self.repo:return False,d
            ok,gd=self.text('rev-parse','--absolute-git-dir'); d['absolute_git_dir']=gd if ok else 'UNRESOLVED'
            if not ok or Path(gd).resolve(strict=True)!=self.git_dir:return False,d
            ok,cd=self.text('rev-parse','--git-common-dir'); d['git_common_dir']=cd if ok else 'UNRESOLVED'
            cp=Path(cd) if ok else Path(); cp=cp if cp.is_absolute() else self.git_dir/cp
            if not ok or cp.resolve(strict=True)!=self.git_dir:return False,d
            return True,d
        except Exception as e:d['hardening_error']=str(e);return False,d
    hardening=repository_hardening
    def final_fingerprint_matches(self):
        a=fingerprint(self.executable);return a==self.before,a

def commit_info(g:GitTrust,o:str)->tuple[str,list[str]]:
    a,_=alg(o); raw=g.commit(o)
    try:h=raw.split(b'\n\n',1)[0].decode('ascii','strict').splitlines()
    except UnicodeDecodeError as e:raise TrustFailure('commit-headers-not-ascii') from e
    tree='';parents=[]
    for line in h:
        if line.startswith('tree '):
            x=line[5:]
            if tree:raise TrustFailure('commit-multiple-tree-headers')
            same_alg(x,a);tree=x
        elif line.startswith('parent '):x=line[7:];same_alg(x,a);parents.append(x)
    if not tree:raise TrustFailure('commit-tree-header-missing')
    return tree,parents

def tree_entries(g:GitTrust,o:str)->dict[str,tuple[str,str]]:
    a,n=alg(o); raw=g.tree(o); i=0;out={}
    while i<len(raw):
        sp=raw.find(b' ',i);nul=raw.find(b'\0',sp+1)
        if sp<0 or nul<0 or nul+1+n>len(raw):raise TrustFailure('tree-object-malformed')
        try:mode=raw[i:sp].decode('ascii','strict');name=raw[sp+1:nul].decode('utf-8','strict')
        except UnicodeDecodeError as e:raise TrustFailure('tree-entry-encoding-invalid') from e
        if not name or '/' in name or name in {'.','..'} or name in out:raise TrustFailure('tree-entry-name-invalid-or-duplicate')
        x=raw[nul+1:nul+1+n].hex();same_alg(x,a);out[name]=(mode,x);i=nul+1+n
    return out

def at_path(g:GitTrust,c:str,path:str)->tuple[str,bytes]:
    ps=path.split('/')
    if not path or path.startswith('/') or any(x in {'','.','..'} for x in ps):raise TrustFailure('repository-path-invalid')
    t,_=commit_info(g,c)
    for i,p in enumerate(ps):
        e=tree_entries(g,t)
        if p not in e:raise TrustFailure('repository-path-missing')
        mode,o=e[p];last=i==len(ps)-1
        if last:
            if mode not in {'100644','100755'}:raise TrustFailure('governance-path-not-regular-blob')
            return o,g.blob(o)
        if mode!='40000':raise TrustFailure('repository-path-component-not-tree')
        t=o
    raise TrustFailure('repository-path-unresolved')

def direct(g:GitTrust,c:str,p:str)->bool:
    try:return commit_info(g,c)[1]==[p]
    except TrustFailure:return False

def ancestor(g:GitTrust,a:str,d:str,limit:int=100000)->bool:
    try:alg(a);alg(d)
    except TrustFailure:return False
    st=[d];seen=set()
    try:
        while st:
            x=st.pop()
            if x in seen:continue
            seen.add(x)
            if len(seen)>limit:return False
            _,ps=commit_info(g,x)
            if x==a:return True
            st.extend(ps)
    except TrustFailure:return False
    return False

def leaves(g:GitTrust,t:str,prefix:str,out:set[str],budget:list[int])->None:
    budget[0]+=1
    if budget[0]>MAX_TREES:raise TrustFailure('changed-path-tree-budget-exceeded')
    for n,(m,o) in tree_entries(g,t).items():
        budget[1]+=1
        if budget[1]>MAX_ENTRIES:raise TrustFailure('changed-path-entry-budget-exceeded')
        p=f'{prefix}/{n}' if prefix else n
        if m=='40000':leaves(g,o,p,out,budget)
        else:out.add(p)

def tree_diff(g:GitTrust,a:str,b:str,prefix:str,out:set[str],budget:list[int])->None:
    if a==b:g.tree(a);return
    budget[0]+=2
    if budget[0]>MAX_TREES:raise TrustFailure('changed-path-tree-budget-exceeded')
    ea,eb=tree_entries(g,a),tree_entries(g,b)
    for n in sorted(set(ea)|set(eb)):
        p=f'{prefix}/{n}' if prefix else n;x=ea.get(n);y=eb.get(n)
        if x==y:
            if x and x[0]=='40000':g.tree(x[1])
            continue
        if x is None:
            if y[0]=='40000':leaves(g,y[1],p,out,budget)
            else:out.add(p)
        elif y is None:
            if x[0]=='40000':leaves(g,x[1],p,out,budget)
            else:out.add(p)
        elif x[0]=='40000' and y[0]=='40000':tree_diff(g,x[1],y[1],p,out,budget)
        else:
            out.add(p)
            if x[0]=='40000':leaves(g,x[1],p,out,budget)
            if y[0]=='40000':leaves(g,y[1],p,out,budget)

def changed(g:GitTrust,a:str,b:str)->tuple[bool,list[str]]:
    try:
        ta,_=commit_info(g,a);tb,_=commit_info(g,b);out=set();tree_diff(g,ta,tb,'',out,[0,0]);return True,sorted(out)
    except TrustFailure:return False,[]

def live(g:GitTrust)->tuple[bool,str,str]:
    lo,ls=g.resolve_ref('refs/heads/'+CANONICAL_REF);ro,rs=g.resolve_ref('refs/remotes/origin/'+CANONICAL_REF)
    if lo and ro and ls!=rs:return False,'','DIVERGED'
    if lo:return True,ls,'LOCAL'+('+REMOTE_MATCH' if ro else '')
    if ro:return True,rs,'REMOTE_ONLY'
    return False,'','UNRESOLVED'

def branch(g:GitTrust,n:str)->tuple[bool,str,str]:
    lo,ls=g.resolve_ref('refs/heads/'+n);ro,rs=g.resolve_ref('refs/remotes/origin/'+n)
    if lo and ro and ls!=rs:return False,'','DIVERGED'
    if lo:return True,ls,'LOCAL'+('+REMOTE_MATCH' if ro else '')
    if ro:return True,rs,'REMOTE_ONLY'
    return False,'','UNRESOLVED'

def cbytes(g:GitTrust,c:str,p:str)->tuple[bool,bytes]:
    try:return True,at_path(g,c,p)[1]
    except TrustFailure:return False,b''

def cjson(g:GitTrust,c:str,p:str)->Any:
    ok,b=cbytes(g,c,p)
    if not ok:return None
    try:return json.loads(b.decode('utf-8','strict'))
    except Exception:return None

def ijson(g:GitTrust,r:str)->Any:
    m=IMM_RE.fullmatch(r or '')
    if not m:return None
    try:return json.loads(at_path(g,m.group('sha'),m.group('path'))[1].decode('utf-8','strict'))
    except Exception:return None

def splitref(r:str)->tuple[str,str]:
    m=IMM_RE.fullmatch(r or '');return (m.group('sha'),m.group('path')) if m else ('','')

def typeok(v:Any,t:str)->bool:return {'object':isinstance(v,dict),'array':isinstance(v,list),'string':isinstance(v,str),'boolean':isinstance(v,bool),'integer':isinstance(v,int) and not isinstance(v,bool),'number':isinstance(v,(int,float)) and not isinstance(v,bool),'null':v is None}.get(t,False)
def serr(i:Any,s:dict,p:str='$')->list[str]:
    e=[]
    if 'type' in s:
        ts=s['type'] if isinstance(s['type'],list) else [s['type']]
        if not any(typeok(i,t) for t in ts):return [p+':type']
    if 'const' in s and i!=s['const']:e.append(p+':const')
    if 'enum' in s and i not in s['enum']:e.append(p+':enum')
    if isinstance(i,str):
        if len(i)<s.get('minLength',0):e.append(p+':minLength')
        if 'pattern' in s and not re.search(s['pattern'],i):e.append(p+':pattern')
    if isinstance(i,list):
        if len(i)<s.get('minItems',0):e.append(p+':minItems')
        if s.get('uniqueItems') is True:
            try:
                if len({json.dumps(x,sort_keys=True) for x in i})!=len(i):e.append(p+':uniqueItems')
            except Exception:e.append(p+':uniqueItems')
        if 'items' in s:
            for n,x in enumerate(i):e+=serr(x,s['items'],f'{p}[{n}]')
    if isinstance(i,dict):
        for k in s.get('required',[]):
            if k not in i:e.append(p+':missing:'+k)
        ps=s.get('properties',{})
        if s.get('additionalProperties') is False:
            for k in i:
                if k not in ps:e.append(p+':additional:'+k)
        for k,x in ps.items():
            if k in i:e+=serr(i[k],x,p+'.'+k)
    return e

def schemacheck(g:GitTrust,i:Any,c:str,p:str)->tuple[bool,list[str]]:
    s=cjson(g,c,p)
    if not isinstance(s,dict):return False,['canonical-schema-unavailable']
    e=serr(i,s);return not e,e

def fail(r:str,d:dict[str,Any]|None=None)->int:
    print(json.dumps({'checks':{'TRUST_ROOT_INITIALIZATION':False},'EXTERNAL_INTEGRATION_ELIGIBLE':False,'details':{'trust_failure':r,**(d or {})}},sort_keys=True));return 1

_REQUIRED_FLAGS=_FLAGS
_path_is_within=within
_validated_repository_root=roots
_validated_git_executable=gitexe
verified_blob_at_path=at_path
changed_paths_verified=changed

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--repository-root',required=True);ap.add_argument('--trusted-git-executable',required=True);ap.add_argument('candidate_sha');ap.add_argument('audit_evidence_ref');ap.add_argument('audit_authorization_ref');a=ap.parse_args()
    try:r,gd=roots(a.repository_root);gx,fp=gitexe(a.trusted_git_executable,r)
    except TrustFailure as e:return fail(str(e))
    bad=[]
    for x in sys.path:
        if not x or within(Path(x),r):bad.append(x)
    if bad:return fail('candidate-controlled-import-path-present',{'repo_import_paths':bad})
    g=GitTrust(gx,r,gd,fp);hok,hd=g.repository_hardening()
    if not hok:return fail('repository-object-or-ancestry-hardening-failed',{'repository_hardening':hd,'trusted_git':fp})
    ok,lc,src=live(g);C={'TRUST_ROOT_INITIALIZATION':True,'LIVE_CANONICAL_REF_RESOLVED':ok};D={'live_sha':lc,'live_source':src,'python_execution_flags':_FLAGS,'repo_import_paths':bad,'repository_root':str(r),'repository_git_dir':str(gd),'trusted_git_executable':str(gx),'trusted_git_fingerprint_before':fp,'git_subprocess_environment_keys':sorted(g.env),'git_path_in_child_environment':g.env.get('PATH'),'repository_hardening':hd,'object_identity_rule':'hash(type + SP + decimal_byte_length + NUL + exact_payload) == requested_oid','ref_provenance_rule':'exact full refs/heads or refs/remotes read only from nonredirected .git loose/packed storage; loose+packed must agree; symbolic/unsupported storage fails closed'}
    if not ok:print(json.dumps({'checks':C,'EXTERNAL_INTEGRATION_ELIGIBLE':False,'details':D},sort_keys=True));return 1
    C.update({'PYTHON_EXECUTION_ISOLATED':all(_FLAGS.values()),'NO_REPOSITORY_IMPORT_PATHS':not bad,'NO_PATH_AUTHORITY_FOR_GIT_EXECUTABLE':'PATH' not in g.env,'TRUSTED_GIT_OUTSIDE_REPOSITORY':not within(gx,r),'TRUSTED_GIT_PATH_ABSOLUTE':gx.is_absolute(),'REPOSITORY_METADATA_ROOT_PINNED':g.git_dir==r/'.git','TRUST_BEARING_GIT_OBJECT_BYTES_CRYPTOGRAPHICALLY_REBOUND':True,'TRUST_BEARING_REFS_DIRECT_BOUNDED_METADATA_ONLY':True})
    cok,cs=cbytes(g,lc,SELF_REL)
    try:cur=SCRIPT.read_bytes()
    except Exception:cur=b''
    C['EXECUTING_COPY_IS_CANONICAL_PREDECESSOR']=bool(cok and cs==cur);C['NO_RAWLSING_RUNTIME_IMPORTS']=True
    C['CANDIDATE_SHA_IS_EXACT_OID']=bool(OID_RE.fullmatch(a.candidate_sha or ''))
    try:g.commit(a.candidate_sha);ce=C['CANDIDATE_SHA_IS_EXACT_OID']
    except Exception:ce=False
    C['CANDIDATE_COMMIT_EXISTS']=ce;C['CANDIDATE_DESCENDS_FROM_LIVE_CANONICAL']=ce and ancestor(g,lc,a.candidate_sha)
    mok,mb=cbytes(g,lc,MANIFEST_REL);prot=set()
    if mok:
        try:prot={z.get('path','') for z in csv.DictReader(mb.decode('utf-8','strict').splitlines(),delimiter='\t') if z.get('path')}
        except Exception:prot=set()
    C['CANONICAL_PROTECTED_MANIFEST_LOADED']=bool(prot);deps={SELF_REL,MANIFEST_REL,AUTH_SCHEMA_REL,RESULT_SCHEMA_REL};C['CANONICAL_DEPENDENCY_CLOSURE_DECLARED']=deps<=prot;C['CANONICAL_AUTH_SCHEMA_AVAILABLE']=isinstance(cjson(g,lc,AUTH_SCHEMA_REL),dict);C['CANONICAL_RESULT_SCHEMA_AVAILABLE']=isinstance(cjson(g,lc,RESULT_SCHEMA_REL),dict);D['trusted_dependency_sources']={x:f'{lc}:{x}' for x in sorted(deps)}
    dok,df=changed(g,lc,a.candidate_sha);pch=sorted(set(df)&prot);C['PROTECTED_CHANGE_DETECTED']=bool(dok and pch);D['protected_changed_paths']=pch
    au=ijson(g,a.audit_authorization_ref);C['AUDIT_AUTHORIZATION_IMMUTABLE_JSON']=bool(au);aso,ase=schemacheck(g,au,lc,AUTH_SCHEMA_REL) if au else (False,['no-auth']);C['AUDIT_AUTHORIZATION_SCHEMA_VALID']=aso;D['authorization_schema_errors']=ase;ash,apath=splitref(a.audit_authorization_ref);C['AUTHORIZATION_PATH_IS_EXTERNAL_AUDIT_PREFIX']=apath.startswith(AUTH_PREFIX);C['AUTHORIZATION_DIRECT_CHILD_OF_LIVE_CANONICAL']=bool(ash and direct(g,ash,lc));C['AUTHORIZATION_OUTSIDE_CANDIDATE_LINEAGE']=bool(ash and not ancestor(g,a.candidate_sha,ash));arok,ard=changed(g,lc,ash) if ash else (False,[]);achs=set(ard);C['AUTHORIZATION_COMMIT_JURISDICTION_PURE']=bool(arok and achs and all(x.startswith(AUTH_PREFIX) for x in achs) and not(achs&prot));D['authorization_changed_paths']=sorted(achs);C['AUTHORIZATION_BINDS_CANONICAL_HEAD']=bool(au and au.get('canonical_head')==lc);C['AUTHORIZATION_BINDS_EXACT_CANDIDATE']=bool(au and au.get('candidate_sha')==a.candidate_sha)
    ad=ijson(g,a.audit_evidence_ref);C['AUDIT_EVIDENCE_IMMUTABLE_JSON']=bool(ad);rso,rse=schemacheck(g,ad,lc,RESULT_SCHEMA_REL) if ad else (False,['no-audit']);C['AUDIT_RESULT_SCHEMA_VALID']=rso;D['audit_schema_errors']=rse;dsh,dpath=splitref(a.audit_evidence_ref);br=str((ad or {}).get('audit_branch',''));ebr=str((au or {}).get('expected_audit_branch',''));pre=str((au or {}).get('audit_write_prefix',''));C['AUDIT_RESULT_PATH_WITHIN_AUTHORIZED_PREFIX']=bool(pre and dpath.startswith(pre));bok,bt,bs=branch(g,ebr) if ebr else (False,'','');D['audit_branch_source']=bs;C['AUTHORIZED_AUDIT_BRANCH_RESOLVES']=bok;C['AUDIT_EVIDENCE_COMMIT_IS_AUTHORIZED_BRANCH_TIP']=bool(bok and dsh and bt==dsh);C['AUDIT_RESULT_BRANCH_MATCHES_AUTHORIZATION']=bool(ad and br==ebr);C['AUDIT_DESCENDS_FROM_CANDIDATE']=bool(dsh and ancestor(g,a.candidate_sha,dsh));aok,add=changed(g,a.candidate_sha,dsh) if dsh else (False,[]);dchs=set(add);C['AUDIT_COMMIT_JURISDICTION_PURE']=bool(aok and dchs and pre and all(x.startswith(pre) for x in dchs) and not(dchs&prot));D['audit_changed_paths']=sorted(dchs);C['AUDIT_BINDS_EXACT_AUTHORIZATION_REF']=bool(ad and ad.get('authorization_ref')==a.audit_authorization_ref);C['AUDIT_CHALLENGE_MATCH']=bool(ad and au and ad.get('challenge_nonce')==au.get('challenge_nonce'));C['AUDIT_BINDS_EXACT_CANDIDATE']=bool(ad and ad.get('candidate_sha')==a.candidate_sha);C['AUDIT_MODE_HOSTILE_INDEPENDENT']=bool(ad and ad.get('audit_mode')=='HOSTILE_INDEPENDENT_AUDIT');ru=str((ad or {}).get('overall_ruling',''));to=str((ad or {}).get('terminal_token',''));allowed=set((au or {}).get('allowed_pass_rulings',[]));prefs=list((au or {}).get('allowed_terminal_token_prefixes',[]));C['AUDIT_RULING_EXACTLY_AUTHORIZED_PASS']=bool(ru and ru in allowed);C['AUDIT_TERMINAL_TOKEN_PREFIX_AUTHORIZED']=bool(to and any(to.startswith(x) for x in prefs))
    fok,fa=g.final_fingerprint_matches();C['TRUSTED_GIT_IDENTITY_STABLE_DURING_EXECUTION']=fok;D['trusted_git_fingerprint_after']=fa;eligible=all(C.values());print(json.dumps({'checks':C,'EXTERNAL_INTEGRATION_ELIGIBLE':eligible,'details':D},sort_keys=True));return 0 if eligible else 1
if __name__=='__main__':sys.exit(main())
