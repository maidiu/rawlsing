import sys
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq245-stagea-review")
import rawlsing_next._p07_native_owner_stage_a as M
class Ref:
    def __init__(self): self.key = "K|O|" + "a"*64
class Rel:
    def __init__(self): self.ref = Ref(); self.content_hash = "a"*64
mode = sys.argv[1]
if mode == "under":
    class L(list):
        def __len__(self): return 1
    obj = M.StageAOwner.__new__(M.StageAOwner)
    obj.__init__(relations=L([Rel(), Rel(), Rel()]), authority_registry=object(),
                 trusted_semantic_hash=lambda x: "f"*64)
    print("UNDER_CLAIM n_relations=", obj.custody_diagnostic()["n_relations"])
elif mode == "tuple":
    class T(tuple):
        def __len__(self): return 4
    obj = M.StageAOwner.__new__(M.StageAOwner)
    obj.__init__(relations=T((Rel(),)), authority_registry=object(),
                 trusted_semantic_hash=lambda x: "f"*64)
    print("TUPLE_SURVIVED")
elif mode == "exact_len_ok":
    obj = M.StageAOwner.__new__(M.StageAOwner)
    obj.__init__(relations=[Rel()], authority_registry=object(),
                 trusted_semantic_hash=lambda x: "f"*64)
    print("EXACT_OK n_relations=", obj.custody_diagnostic()["n_relations"])
elif mode == "factory_subclass":
    class L(list):
        def __len__(self): return 5
    try:
        M.build_stage_a_owner(relations=L([Rel()]), authority_registry=object(),
                              trusted_semantic_hash=lambda x: "f"*64)
        print("FACTORY_ACCEPTED")
    except TypeError as e:
        print("FACTORY_REFUSED", e)
