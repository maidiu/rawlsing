import resource, sys
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq245-stagea-review")
import rawlsing_next._p07_native_owner_stage_a as M
class Ref:
    def __init__(s): s.key="K|O|"+"a"*64
class Rel:
    def __init__(s): s.ref=Ref(); s.content_hash="a"*64
owner = M.build_stage_a_owner(relations=[Rel()], authority_registry=object(),
                              trusted_semantic_hash=lambda x: "f"*64)
r = Rel()
n = int(sys.argv[1])
for _ in range(n): owner.resolve_exact(r.ref)
print(n, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
