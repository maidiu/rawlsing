import ast, json, os
ROOT="/tmp/hq191freeze"; SRC=os.path.join(ROOT,"rawlsing_next")
def internal(f):
    p=os.path.join(SRC,f)
    try: tree=ast.parse(open(p,encoding="utf-8").read())
    except Exception: return set()
    out=set()
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            for a in n.names:
                if a.name.startswith("rawlsing_next"): out.add(a.name.split(".")[1])
        elif isinstance(n,ast.ImportFrom) and n.module and n.module.startswith("rawlsing_next"):
            ps=n.module.split(".")
            if len(ps)>1: out.add(ps[1])
            for a in n.names: out.add(a.name)
    return {m for m in out if os.path.exists(os.path.join(SRC,m+".py"))}
def closure(roots):
    seen,st=set(),list(roots)
    while st:
        m=st.pop()
        if m in seen: continue
        seen.add(m); st.extend(internal(m+".py"))
    return seen
five=closure(["pre553_analytical_composition"]); routeb=closure(["pre553_route_b_production"])
union=closure(["pre553_analytical_composition","pre553_source_backed_c11_facade","source_backed_positioned_subject_possibility","pre553_recursive_handoff"])
print(f"five_layer_closure = {len(five)}")
print(f"route_b_closure    = {len(routeb)}")
print(f"union_closure      = {len(union)}")
declared=set(json.load(open("/Users/matthewsmith/Desktop/Rawlsing/review-hq191/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/R7-DARWIN-ENVIRONMENT-CLOSURE-R1/evidence/static_closure.json"))["modules"])
dm={os.path.basename(p)[:-3] for p in declared}
print(f"declared union     = {len(dm)}   measured==declared: {union==dm}")
print(f"  declared-measured: {sorted(dm-union)}")
print(f"  measured-declared: {sorted(union-dm)}")
print()
PATS=["importlib","exec_module","spec_from_file_location","module_from_spec","sys.modules","subprocess","os.system","os.popen","exec(","eval(","os.environ","os.getenv","duckdb","__import__","ee_p2x","fiabc_"]
print("EDGE AUDIT AT THE DECLARED EVIDENCE GRAIN (the closure modules only):")
hits={}
for m in sorted(union):
    txt=open(os.path.join(SRC,m+".py"),encoding="utf-8").read()
    found=[p for p in PATS if p in txt]
    if found: hits[m]=found
for m,f in hits.items(): print(f"  {m}: {f}")
if not hits: print("  (no pattern present in any closure module)")
print()
print("expected sole nonzero class __import__ present:", "__import__" in [p for fs in hits.values() for p in fs])
