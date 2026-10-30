"""Recreate exact sourcefree inputs inside this return; no original source edits."""
import ast
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
F1C = "bcea367e7dc0f2e069de71b0fe5e481de094dad5"
F1C_DIR = "WORKER_RETURNS/SOROK-F1C-NONRETROACTIVE-WORLD-B-SOURCEFREE-RECEIVER-R1"
ARCHIVES = {
    "runtime": ("64fec28c374d8f77fb0b412d0c934d798ede03e8", "WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1"),
    "join_runtime": ("7bf2da302996491ddf34b9a039fea47ac982d135", "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1"),
}


def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", *args])


def identity(data):
    return {"git_blob": hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest()}


def write_exact(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == data, "EXISTING_SOURCE_DRIFT:" + str(path)
    else:
        path.write_bytes(data)


def main():
    original = {}
    for path in git("ls-tree", "-r", "--name-only", F1C, F1C_DIR).decode().splitlines():
        data = git("show", F1C + ":" + path)
        original[Path(path).name] = data
        write_exact(HERE / Path(path).name, data)
    doc = original["02_EXECUTABLE_CAUSAL_RIVALS_AND_VERIFIED_SOURCES.md"].decode()
    program = doc.split("<!-- F1C_PROGRAM_START -->\n```python\n", 1)[1].split("\n```", 1)[0] + "\n"
    assert identity(program.encode())["sha256"] == "7e3492a267acbc0fa11d8792158bdaa2acc9dfb6053f16141ed637dc1cd2881b"
    write_exact(HERE / "f1c.py", program.encode())
    for directory, (commit, prefix) in ARCHIVES.items():
        target = HERE / directory
        if not target.exists():
            target.mkdir()
            with tarfile.open(fileobj=io.BytesIO(git("archive", commit + ":" + prefix))) as archive:
                assert all(not p.name.startswith("/") and ".." not in Path(p.name).parts for p in archive)
                archive.extractall(target)
    handoff = json.loads(original["04_OWNER_SOURCE_REVIEW_AND_CONSUMER_HANDOFF.json"])
    manifest = []
    for index, row in enumerate(handoff["sources"]):
        data = git("show", row["commit"] + ":" + row["path"])
        assert identity(data) == {key: row[key] for key in ("git_blob", "sha256")}
        path = HERE / "sources" / f'{index:02d}_{row["label"]}_{Path(row["path"]).name}'
        write_exact(path, data)
        manifest.append(dict(row, local_path=str(path.relative_to(HERE.parent.parent.parent))))
    (HERE / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    queue = ["rawlsing_next.m6_actor_safe_expression", "rawlsing_next.v3_psepf_zero_positive_guard"]
    seen = {}
    while queue:
        name = queue.pop(0)
        if name in seen:
            continue
        path = name.replace(".", "/") + ".py"
        data = git("show", F1C + ":" + path)
        write_exact(HERE / path, data)
        seen[name] = dict(commit=F1C, path=path, **identity(data))
        for node in ast.walk(ast.parse(data)):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("rawlsing_next."):
                queue.append(node.module)
            if isinstance(node, ast.Import):
                queue.extend(x.name for x in node.names if x.name.startswith("rawlsing_next."))
    (HERE / "live_namespace_manifest.json").write_text(json.dumps(list(seen.values()), indent=2) + "\n")
    print("Exact F1C program, 27 source pins, R31J/JOIN archives, seven-module namespace closure ready.")


if __name__ == "__main__":
    main()
