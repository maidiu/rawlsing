"""Read exact Git text spans and record their provenance; executes no project code."""
import json
import pathlib
import subprocess
import sys

commit, path = sys.argv[1:3]
raw = subprocess.check_output(["git", "show", commit + ":" + path], text=True)
lines = raw.splitlines()
spans = [tuple(map(int, x.split(":"))) for x in sys.argv[3:]] or [(1, len(lines))]
blob = subprocess.check_output(["git", "rev-parse", commit + ":" + path], text=True).strip()
index_path = pathlib.Path(__file__).with_name("P1_SOURCE_INDEX.json")
index = json.loads(index_path.read_text()) if index_path.exists() else []
entry = {"commit": commit, "path": path, "blob": blob,
         "line_count": len(lines), "read_spans": spans, "executed": False}
if entry not in index:
    index.append(entry)
    index_path.write_text(json.dumps(index, indent=2) + "\n")
print(json.dumps(entry))
for start, end in spans:
    for n in range(start, min(end, len(lines)) + 1):
        print(f"{n}: {lines[n-1]}")
