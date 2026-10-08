import sys
sys.path.insert(0, "/tmp/hq245_asan")
import _p07_native_owner_stage_a as M
class Ref:
    def __init__(self): self.key = "K|O|" + "a"*64
class Rel:
    def __init__(self): self.ref = Ref(); self.content_hash = "a"*64
class EvilList(list):
    def __len__(self): return 5
obj = M.StageAOwner.__new__(M.StageAOwner)
obj.__init__(relations=EvilList([Rel()]), authority_registry=object(),
             trusted_semantic_hash=lambda x: "f"*64)
print("SURVIVED")
