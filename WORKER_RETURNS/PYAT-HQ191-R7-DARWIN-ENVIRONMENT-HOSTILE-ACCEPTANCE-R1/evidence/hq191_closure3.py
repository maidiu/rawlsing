import ast,json,os
SRC="/tmp/hq191freeze/rawlsing_next"
def internal(f):
    p=os.path.join(SRC,f)
    try: t=ast.parse(open(p,encoding="utf-8").read())
    except Exception: return set()
    o=set()
    for n in ast.walk(t):
        if isinstance(n,ast.Import):
            for a in n.names:
                if a.name.startswith("rawlsing_next"): o.add(a.name.split(".")[1])
        elif isinstance(n,ast.ImportFrom) and n.module and n.module.startswith("rawlsing_next"):
            ps=n.module.split(".")
            if len(ps)>1: o.add(ps[1])
            for a in n.names: o.add(a.name)
    return {m for m in o if os.path.exists(os.path.join(SRC,m+".py"))}
def khop(roots,k):
    cur=set(roots); seen=set(roots)
    for _ in range(k):
        nxt=set()
        for m in cur: nxt|=internal(m+".py")
        nxt-=seen; seen|=nxt; cur=nxt
    return seen
print("k-hop reachability from pre553_analytical_composition:")
for k in (1,2,3,4,6):
    print(f"  k={k}: {len(khop(['pre553_analytical_composition'],k))}")
print("full transitive:", len(khop(['pre553_analytical_composition'],50)))
print()
print("Does the union have a root set covering all 23? Try common entries:")
declared=json.load(open("/Users/matthewsmith/Desktop/Rawlsing/review-hq191/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/R7-DARWIN-ENVIRONMENT-CLOSURE-R1/evidence/static_closure.json"))["modules"]
dm={os.path.basename(p)[:-3] for p in declared}
# Which declared members are NOT reachable from the union roots I used?
mine=khop(["pre553_analytical_composition","pre553_source_backed_c11_facade","source_backed_positioned_subject_possibility","pre553_recursive_handoff"],50)
missing=sorted(dm-mine)
print("declared members not reachable from my roots:", missing)
for m in missing:
    print(f"  {m}: exists={os.path.exists(os.path.join(SRC,m+'.py'))}, imports={sorted(internal(m+'.py'))}")
