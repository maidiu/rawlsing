"""Reproduce source-only C4C2 provenance; never import production or read data.

Run with a working stdlib Python from the worker checkout. Git reads are limited
to named implementation/test/workflow/return blobs. This is not a runtime court.
"""
import ast
import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

BASE = "8f7efe690a161902e79358eb31650c238a4c0be8"
COMMISSION = "1d1676f4b0d8a1963acad5f2dbaa7ae8ffb91e6e"
MERGE = "9a5752a8ce4a119efd24cbbeedd8cbcda8abbadb"
C3 = "30686b185d4ceb2c94f61815ef70d8c8e76255d6"
ROOT = Path(__file__).resolve().parents[2]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def source(path, ref=BASE):
    assert path.startswith(("rawlsing_next/", "WORKER_RETURNS/", ".github/", ".rabochii/"))
    return git("show", ref + ":" + path)


def blob(path, ref=BASE):
    return git("rev-parse", ref + ":" + path)


def main():
    execution_head = git("rev-parse", "HEAD")
    assert execution_head == BASE, "Perform qualification provenance at the exact base HEAD"
    git("merge-base", "--is-ancestor", MERGE, BASE)
    matrix = json.loads(source("WORKER_RETURNS/PYAT-C4A-C1-C3-INTEGRATION-R1/02_FINAL_BLOB_MATRIX.json"))
    pins = []
    for item in matrix["pinned_blobs"]:
        actual = blob(item["path"])
        assert actual == item["expected_blob"]
        pins.append({"path": item["path"], "side": item["side"], "expected_blob": item["expected_blob"],
                     "actual_blob": actual, "status": "EXACT"})
    facade = "rawlsing_next/pre553_source_backed_c11_facade.py"
    assert blob(facade) == "8a761119e4a8d68eb291fc4edfadb52e027f8284"
    tests = [
        ("test_closed35_g01_sav_numeric_representation_authority.py", 9),
        ("test_closed35_d01_declared_encoding_admission.py", 8),
        ("test_closed35_d02_opaque_datetime_carrier.py", 13),
        ("test_fiabc_lm2_r1j_sav_representation_authority.py", 9),
        ("test_r35_i01_physical_metadata.py", 6),
        ("test_pre553_source_backed_c11_facade.py", 10),
    ]
    court = []
    for name, count in tests:
        path = "rawlsing_next/tests/" + name
        assert (ROOT / path).is_file()
        assert blob(path) == blob(path, C3)
        court.append({"path": path, "blob": blob(path), "accepted_C3_blob": blob(path, C3),
                      "expected_count_from_commission": count, "exists": True, "status": "EXACT"})
    assert sum(x["expected_count_from_commission"] for x in court) == 55
    roots = ["rawlsing_next.pre553_physical_decoder", "rawlsing_next.pre553_source_backed_c11_facade",
             "rawlsing_next.pre553_empirical_possibility_provider", "rawlsing_next.pre553_analytical_composition",
             "rawlsing_next.source_backed_positioned_subject_possibility"]
    queue, modules, external, dynamic = list(roots), {}, set(), []
    while queue:
        module = queue.pop()
        if module in modules:
            continue
        path = module.replace(".", "/") + ".py"
        text = source(path)
        tree = ast.parse(text)
        edges = []
        for node in ast.walk(tree):
            names = ([x.name for x in node.names] if isinstance(node, ast.Import)
                     else [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
            if isinstance(node, ast.ImportFrom):
                assert node.level == 0, "Resolve relative import before making closure claim"
            for name in names:
                if name.startswith("rawlsing_next."):
                    edges.append({"module": name, "line": node.lineno})
                    queue.append(name)
                else:
                    external.add(name.split(".")[0])
            if isinstance(node, ast.Call):
                call = ast.unparse(node.func)
                final = (node.func.id if isinstance(node.func, ast.Name)
                         else node.func.attr if isinstance(node.func, ast.Attribute) else None)
                if final in {"import_module", "exec_module", "spec_from_file_location", "__import__", "eval", "exec", "run_module", "run_path"}:
                    dynamic.append({"module": module, "line": node.lineno, "call": ast.unparse(node)})
        forbidden = [x for x in ("ee_p2x_darwin_court_driver", "ee_p2x_darwin_stage_backend", "EXPECTED_RUNTIME", "FROZEN_PYREADSTAT_VERSION", "duckdb") if x in text]
        assert not forbidden, (module, forbidden)
        modules[module] = {"path": path, "blob": blob(path), "imports": edges}
    assert len(dynamic) == 1 and dynamic[0]["call"] == "__import__('json')"
    # rawlsing_next is a namespace package here: no package initializer executes.
    assert not (ROOT / "rawlsing_next/__init__.py").exists()
    local_packages = {}
    for name in ("pyreadstat", "pyarrow", "pandas", "numpy", "pytest", "duckdb"):
        try:
            local_packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            local_packages[name] = None
    tools = {n: shutil.which(n) for n in ("docker", "podman", "colima", "lima", "limactl", "nerdctl", "orb", "qemu-system-x86_64", "multipass", "vagrant", "gh", "ssh")}
    surface_paths = [Path.home() / ".colima", Path.home() / ".lima", Path.home() / ".docker",
                     Path("/var/run/docker.sock"), Path("/Applications/Docker.app"), Path("/Applications/OrbStack.app"),
                     Path("/opt/homebrew/bin/docker"), Path("/usr/local/bin/docker"), Path.home() / ".ssh/config"]
    workflows = []
    for path in git("ls-tree", "-r", "--name-only", BASE, ".github/workflows").splitlines():
        workflows.append({"path": path, "blob": blob(path)})
    return {
        "schema": "PYAT_C4C2_STATIC_AUDIT@1", "execution_head": execution_head,
        "combined_base": BASE, "commission_tip": COMMISSION, "merge_ancestor_verified": MERGE,
        "commission_delta": git("diff", "--name-only", BASE, COMMISSION).splitlines(),
        "pinned_blobs": pins, "facade_blob": blob(facade), "authoritative_court": court,
        "call_path_roots": roots, "transitive_local_modules": modules,
        "external_import_roots": sorted(external), "dynamic_loaders": dynamic,
        "namespace_package_without_initializer": True,
        "P2X_DARWIN_GATES_NOT_ON_C4_PATH": True, "duckdb_required_on_inspected_path": False,
        "local_audit_host": {"system": platform.system(), "release": platform.release(), "platform": platform.platform(),
                             "machine": platform.machine(), "implementation": platform.python_implementation(),
                             "python": platform.python_version(), "executable": sys.executable, "byteorder": sys.byteorder,
                             "package_metadata_for_this_interpreter_only": local_packages},
        "runtime_commands": tools, "surface_paths": {str(p): p.exists() for p in surface_paths},
        "workflow_blobs": workflows, "existing_court_spec": json.loads(source(".rabochii/court_spec.json")),
        "non_mac_qualification_run": False, "production_imports": 0,
        "raw_source_content_reads": 0, "reader_probes_run": 0, "court_tests_run": 0,
        "audit_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
