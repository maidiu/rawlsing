"""Static, import-free closure + edge audit over the freeze worktree.
Parses with ast only. Executes nothing. Writes nothing."""
import ast, json, os, sys
ROOT = "/tmp/hq191freeze"
SRC = os.path.join(ROOT, "rawlsing_next")

def mods_in(path):
    return sorted(f for f in os.listdir(path) if f.endswith(".py"))

def internal_imports(fname):
    """Top-level rawlsing_next imports this module performs."""
    p = os.path.join(SRC, fname)
    try:
        tree = ast.parse(open(p, encoding="utf-8").read())
    except Exception as e:
        return set()
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.startswith("rawlsing_next"):
                    out.add(a.name.split(".")[1])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("rawlsing_next"):
                parts = node.module.split(".")
                if len(parts) > 1:
                    out.add(parts[1])
                for a in node.names:
                    out.add(a.name)
    return {m for m in out if os.path.exists(os.path.join(SRC, m + ".py"))}

# Forward closure from the analytic roots declared by the lane.
ROOTS = ["pre553_analytical_composition", "pre553_source_backed_c11_facade",
         "source_backed_positioned_subject_possibility", "pre553_recursive_handoff"]
def closure(roots):
    seen, stack = set(), list(roots)
    while stack:
        m = stack.pop()
        if m in seen: continue
        seen.add(m)
        stack.extend(internal_imports(m + ".py"))
    return seen

five = closure(["pre553_analytical_composition"])
routeb = closure(["pre553_route_b_production"])
union = closure(ROOTS)
print("five_layer_closure =", len(five))
print("route_b_closure    =", len(routeb))
print("union_closure      =", len(union))
print("union modules      =", sorted(union))
print()
# Compare with the declared union list.
declared = set(json.load(open("/Users/matthewsmith/Desktop/Rawlsing/review-hq191/PYAT_CONTROL_ROOM/"
  "SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/R7-DARWIN-ENVIRONMENT-CLOSURE-R1/evidence/static_closure.json"))["modules"])
declared_mods = {os.path.basename(p)[:-3] for p in declared}
print("declared union size =", len(declared_mods))
print("measured == declared:", union == declared_mods)
print("declared - measured :", sorted(declared_mods - union))
print("measured - declared :", sorted(union - declared_mods))
print()
# Edge audit: dynamic-loader / subprocess / source patterns.
PATTERNS = ["importlib", "exec_module", "spec_from_file_location", "module_from_spec",
            "sys.modules", "subprocess", "os.system", "os.popen", "exec(", "eval(",
            "os.environ", "os.getenv", "duckdb", "__import__", "ee_p2x", "fiabc_"]
edges = {p: [] for p in PATTERNS}
for f in mods_in(SRC):
    txt = open(os.path.join(SRC, f), encoding="utf-8").read()
    for p in PATTERNS:
        if p in txt:
            edges[p].append("rawlsing_next/" + f)
mine = {k: v for k, v in edges.items() if v}
print("EDGE AUDIT (modules containing each pattern):")
print(json.dumps(mine, indent=1))
