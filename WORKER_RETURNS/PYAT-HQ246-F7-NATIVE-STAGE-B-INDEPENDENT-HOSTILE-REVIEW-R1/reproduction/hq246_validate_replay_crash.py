import sys, hashlib
sys.path.insert(0,".")
from rawlsing_next import _p07_native_owner_stage_b as M
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
SEM=lambda v: hashlib.sha256(repr(v).encode()).hexdigest()
CANON=lambda v: v
REQ=lambda a,b: True
o=M.StageBOwner.__new__(M.StageBOwner)
o.__init__(relations=[FR()], authority_snapshots=[FS()], trusted_semantic_hash=SEM,
           trusted_canonicalize=CANON, trusted_require_positive_authority=REQ,
           relation_class=FR, authority_snapshot_class=FS)
d=o.decide(relation_kind="SOURCE_SEMANTIC_EQUIVALENCE", source_universe_refs=[Ref("U-A"),Ref("U-B")],
           operation_scope={"s":1}, target_use="USE-1", effective_scope={"s":1})
print("DECIDE_STATE", d["state"])
d["relation_kind"]=123
o.validate_decision_replay(d)   # non-str field -> build_replay_preimage -> PyUnicode_FromString(NULL)
print("SURVIVED")
