import sys, os
MODE = os.environ.get("HQ246_MOD", "worktree")
if MODE == "asan":
    sys.path.insert(0, "/tmp/hq246_asan")
    import _p07_native_owner_stage_b as M
else:
    sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq246-stageb-review")
    from rawlsing_next import _p07_native_owner_stage_b as M
print("MODULE", M.__file__)
class Ref:
    def __init__(s,oid): s.kind="SourceUniverse"; s.object_id=oid; s.content_hash="a"*64
    @property
    def key(s): return f"{s.kind}|{s.object_id}|{s.content_hash}"
    def as_dict(s): return {"kind":s.kind,"object_id":s.object_id,"content_hash":s.content_hash}
class ARef:
    authority_id="EQ1"; authority_version="1.0.0"; authority_content_hash="b"*64
    @property
    def key(s): return f"{s.authority_id}|{s.authority_version}|{s.authority_content_hash}"
    def as_dict(s): return {"authority_id":s.authority_id,"authority_version":s.authority_version,"authority_content_hash":s.authority_content_hash}
class FR:
    ref=Ref("U-A"); content_hash="c"*64; relation_kind="SOURCE_SEMANTIC_EQUIVALENCE"
    authority_operation="SEMANTIC_EQUIVALENCE_ADMISSION"; target_use="USE-1"
    relation_authority_ref=ARef(); operation_scope={"s":1}
    source_universe_refs=(Ref("U-A"),Ref("U-B"))
    semantic_fields={"decision":"AUTHORIZED","replay_identity":"r"*64}
    def semantic_projection(s): return {"p":1}
class FS:
    authority_ref=ARef(); content_hash="b"*64
    def semantic_projection(s): return {"s":1}
SEM=lambda v:"d"*64; CANON=lambda v:v; REQ=lambda a,b:True
def build(rels,snaps):
    o=M.StageBOwner.__new__(M.StageBOwner)
    o.__init__(relations=rels, authority_snapshots=snaps, trusted_semantic_hash=SEM,
               trusted_canonicalize=CANON, trusted_require_positive_authority=REQ,
               relation_class=FR, authority_snapshot_class=FS)
    return o
real=int(sys.argv[1]); rep=int(sys.argv[2]); which=sys.argv[3]
class Evil(list):
    def __len__(self): return rep
base=[FR() for _ in range(real)]
snaps=[FS()]
try:
    if which=="rel": o=build(Evil(base), snaps)
    else: o=build(base, Evil(snaps*real))
    print("SURVIVED counts=", o.counts)
except Exception as e:
    print("EXC", type(e).__name__, str(e)[:90])
