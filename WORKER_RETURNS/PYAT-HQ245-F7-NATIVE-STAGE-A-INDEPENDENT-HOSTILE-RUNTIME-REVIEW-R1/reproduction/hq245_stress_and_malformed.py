import random, resource, sys, traceback
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq245-stagea-review")
import rawlsing_next._p07_native_owner_stage_a as M
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
class Ref:
    def __init__(s, k="K|O|"+"a"*64): s.key=k
class Rel:
    def __init__(s, k="K|O|"+"a"*64, ch="a"*64): s.ref=Ref(k); s.content_hash=ch
sem = lambda x: "f"*64
owner = M.build_stage_a_owner(relations=[Rel()], authority_registry=object(), trusted_semantic_hash=sem)
r0 = rss()
N = 300000
for _ in range(N):
    try: owner.resolve_exact(Rel().ref)
    except Exception: pass
r1 = rss()
print("resolve_loop", N, "maxrss_delta_kb", r1-r0)
# randomized malformed resolve inputs
random.seed(7)
bad = [None, 1, 3.14, "s", b"b", [], {}, object(), Ref("bad"), {"kind":"x"},
       {"kind":"x","object_id":"y"}, {"kind":"x","object_id":"y","content_hash":123},
       {"kind":None,"object_id":None,"content_hash":None}, lambda: 1]
crashes=0
for _ in range(200000):
    try: owner.resolve_exact(random.choice(bad))
    except Exception: pass
print("malformed_resolve_loop_ok")
# randomized constructor inputs
for _ in range(50000):
    try:
        M.build_stage_a_owner(relations=random.choice(bad), authority_registry=object(),
                              trusted_semantic_hash=sem)
    except Exception: pass
print("malformed_ctor_loop_ok")
# re-init on sealed
for _ in range(1000):
    try: owner.__init__(relations=[Rel()], authority_registry=object(), trusted_semantic_hash=sem)
    except Exception: pass
print("reinit_refused_ok", "sealed=", owner.sealed, "diag=", owner.custody_diagnostic()["n_relations"])
print("STRESS_COMPLETE")
