#!/usr/bin/env python3
"""Reader-only recovery for a validated resumed run layout.

The running producer may have published under <run>/releases; the legacy reader
expects <run>/private. This entry accepts ONLY the expected digest-named release
directly under an exact owner-private 0700 run root, and uses the existing native
reader. It never moves, rewrites, or rebuilds anything.
"""
from __future__ import annotations
import argparse,json,os,stat,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;A=HERE.parents[2]
sys.path[:0]=[str(HERE),str(A/'MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_OPERATOR_INTEGRATION_20261118')]
from streaming_estate import StreamRoots,open_stream_native_estate

def mode_ok(p):
 return p.is_dir() and not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o700

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run-root',type=Path,required=True);ap.add_argument('--layout',choices=('private','resumed'),required=True);ap.add_argument('--release-digest',required=True);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--roots-json',required=True);ap.add_argument('--binding-dir',type=Path,required=True);ap.add_argument('--test-current',action='store_true',help='TEST_ONLY sourcefree roots equality');ap.add_argument('--out',type=Path)
 args=ap.parse_args();run=args.run_root.absolute();digest=args.release_digest
 if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise SystemExit('BAD_RELEASE_DIGEST')
 if not mode_ok(run):raise SystemExit('RUN_ROOT_NOT_EXACT_0700')
 base=run if args.layout=='resumed' else run/'private'
 expected=base/'releases'/digest
 if not expected.is_dir() or expected.is_symlink():raise SystemExit('NONEXACT_ESTATE_PATH')
 if not mode_ok(expected):raise SystemExit('RELEASE_NOT_EXACT_0700')
 roots=StreamRoots(**json.loads(args.roots_json))
 if args.test_current:
  current=lambda r:r==roots
 else:
  from sqlite_free_witness import _grant
  _,bound,resolver,_,_=_grant(args.binding_dir);req=bound.request
  def current(r):
   return resolver.resolve_current(req) is not None and r==roots
 estate=open_stream_native_estate(base,exact_path=expected,manifest_sha256=args.manifest_sha256,roots=roots,current_authorizer=current)
 count=sum(1 for _ in estate.iter_family('RespondentEvent'))
 out={'schema':'ANVIL_SRC04_RESUMED_READER@1','status':'READER_OPENED','run_root':str(run),'layout':args.layout,'release_path':str(expected),'manifest_sha256':args.manifest_sha256,'stream_release':roots.release,'event_count':count,'sqlite_files':[]}
 if args.out:args.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
