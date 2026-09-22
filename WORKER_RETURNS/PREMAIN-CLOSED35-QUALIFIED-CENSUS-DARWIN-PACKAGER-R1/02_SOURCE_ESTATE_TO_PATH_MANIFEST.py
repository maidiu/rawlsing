#!/usr/bin/env python3
"""Source-free estate-to-harness bridge for the authoritative CLOSED35 census.

No survey decoding happens here. This program verifies byte identity, stages the
35 canonical carriers, emits the exact harness path manifest, and validates the
authoritative receipt tree after the frozen census harness has run.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile
from typing import Any, Mapping, Sequence
import zipfile

PATH_SCHEMA = "CLOSED35_SOURCE_PATH_MANIFEST@1.0.0"
ESTATE_SCHEMA = "PREMAIN_CLOSED35_SOURCE_ACQUISITION_MANIFEST@1.0.0"
HARNESS_SCHEMA = "PREMAIN_CLOSED35_CENSUS_INPUT_REGISTRY@1.0.0"
RECEIPT_SCHEMA = "CLOSED35_SOURCE_REPRESENTATION_RECEIPT@1.0.0"
OBS_SCHEMA = "CLOSED35_REPRESENTATION_OBSERVATIONS@1.0.0"
EDGE_SCHEMA = "CLOSED35_EDGE_PRESERVATION_RECEIPT@1.0.0"
DEP_SCHEMA = "CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE@1.0.0"
RUNTIME_SCHEMA = "CLOSED35_RUNTIME_RECEIPT@1.0.0"
SUMMARY_SCHEMA = "CLOSED35_CENSUS_SUMMARY@1.0.0"
BINDING_SCHEMA = "PREMAIN_CLOSED35_DARWIN_PACKAGER_BINDING@1.0.0"

HARNESS_BRANCH = "agent/rabochii-premain-closed35-qualified-representation-census-harness-r1"
HARNESS_HEAD = "efe8de2b032c93d1820fd3f8c82fe2f1acabbf87"
QUALIFIED_HEAD = "11704fbfa16797fbdd55dadc7929aaad729c9454"
ESTATE_HEAD = "4e230628ae31b6b4de581f3a797e1d1bcb0047a0"
ESTATE_PATH = "WORKER_RETURNS/PREMAIN-CLOSED35-SOURCE-ESTATE-CLOSURE-R1/02_CLOSED35_SOURCE_ACQUISITION_MANIFEST.json"
ESTATE_BLOB = "331de4fb28871b9b18f3da44ea2ac17aa94a5c00"
HARNESS_REGISTRY_PATH = "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1/01_CLOSED35_CENSUS_INPUT_REGISTRY.json"
HARNESS_REGISTRY_BLOB = "1b15ce03e337d156c9b9da6d3d60a7a8d1b23591"
HARNESS_RUNNER_PATH = "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1/02_RUN_CLOSED35_QUALIFIED_REPRESENTATION_CENSUS.sh"
HARNESS_RUNNER_BLOB = "9008ab5cecc46ea01127ff61f4646b17a82826f2"
SURFACE_PATH = "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1/03_GOVERNED_TYPED_SURFACE_REGISTRY.csv"
SURFACE_BLOB = "f3c2c1915c4f3bf379e5233ce9dc4137a841f9e8"

EXPECTED_RUNTIME = {
    "platform": "Darwin",
    "machine": "x86_64",
    "cpython": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
}

AGGREGATES = (
    "CLOSED35_REPRESENTATION_OBSERVATIONS.json",
    "CLOSED35_TYPED_JOIN_MATRIX.csv",
    "CLOSED35_EDGE_PRESERVATION_RECEIPT.json",
    "CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json",
    "CLOSED35_RUNTIME_RECEIPT.json",
    "CLOSED35_CENSUS_SUMMARY.json",
)
RAW_SUFFIXES = {".sav", ".dta", ".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"}


class PackagerError(RuntimeError):
    pass


def fail(msg: str) -> None:
    raise PackagerError(msg)


def cjson(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git(repo: Path, *args: str, check: bool = True) -> str:
    p = subprocess.run(["git", "-C", str(repo), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode:
        fail("git " + " ".join(args) + " failed: " + p.stderr.strip())
    return p.stdout.strip()


def object_exists(repo: Path, spec: str) -> bool:
    return subprocess.run(["git", "-C", str(repo), "cat-file", "-e", spec],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def runtime_facts() -> dict[str, str]:
    def pkg(name: str) -> str:
        try:
            return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            return "UNAVAILABLE"
    return {
        "platform": platform.system(),
        "machine": platform.machine(),
        "cpython": platform.python_version(),
        "pyreadstat": pkg("pyreadstat"),
        "pyarrow": pkg("pyarrow"),
    }


def validate_runtime(facts: Mapping[str, str]) -> None:
    if dict(facts) != EXPECTED_RUNTIME:
        fail("runtime mismatch: expected " + json.dumps(EXPECTED_RUNTIME, sort_keys=True)
             + " got " + json.dumps(dict(facts), sort_keys=True))


def validate_repo_facts(branch: str, head: str, clean: bool, qualified_ancestor: bool) -> None:
    if branch != HARNESS_BRANCH:
        fail(f"wrong branch: {branch!r}")
    if head != HARNESS_HEAD:
        fail(f"wrong harness head: {head!r}")
    if not clean:
        fail("checkout is not clean")
    if not qualified_ancestor:
        fail("qualified implementation head is not an ancestor")


def preflight_repo(repo: Path) -> dict[str, Any]:
    branch = git(repo, "branch", "--show-current")
    head = git(repo, "rev-parse", "HEAD")
    clean = git(repo, "status", "--porcelain", "--untracked-files=all") == ""
    anc = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", QUALIFIED_HEAD, head],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    validate_repo_facts(branch, head, clean, anc)
    pins = (
        (f"{ESTATE_HEAD}:{ESTATE_PATH}", ESTATE_BLOB, "source-estate manifest"),
        (f"HEAD:{HARNESS_REGISTRY_PATH}", HARNESS_REGISTRY_BLOB, "harness registry"),
        (f"HEAD:{HARNESS_RUNNER_PATH}", HARNESS_RUNNER_BLOB, "harness runner"),
        (f"HEAD:{SURFACE_PATH}", SURFACE_BLOB, "surface registry"),
    )
    for spec, expected, label in pins:
        if not object_exists(repo, spec):
            fail(f"missing pinned Git object for {label}: {spec}")
        actual = git(repo, "rev-parse", spec)
        if actual != expected:
            fail(f"{label} blob drift: {actual} != {expected}")
    facts = runtime_facts()
    validate_runtime(facts)
    return {"branch": branch, "head": head, "runtime": facts}


def validate_estate(v: Mapping[str, Any]) -> None:
    if v.get("schema") != ESTATE_SCHEMA:
        fail("estate manifest schema mismatch")
    c = v.get("counts") or {}
    if c.get("canonical_sources") != 35 or c.get("exact_identity_pass") != 35 or c.get("CANONICAL_BYTES_NOT_LOCATED") != 0:
        fail("estate is not 35 PASS / 0 unresolved")
    src = v.get("sources")
    if not isinstance(src, list) or len(src) != 35:
        fail("estate must contain exactly 35 sources")
    if [x.get("canonical_source_id") for x in src] != [f"CLOSED35-{i:02d}" for i in range(1, 36)]:
        fail("estate source IDs drift")
    states = [x.get("acquisition_state") for x in src]
    if states.count("EXACT_ARCHIVE_MEMBER_AVAILABLE") != 34 or states.count("EXACT_ALIAS_AVAILABLE") != 1:
        fail("estate acquisition-state cardinality drift")
    if set((v.get("carrier_roots") or {}).keys()) != {"surveys", "lits1", "wvs7"}:
        fail("estate must bind exactly three carrier roots")


def validate_harness(v: Mapping[str, Any]) -> None:
    if v.get("schema") != HARNESS_SCHEMA:
        fail("harness registry schema mismatch")
    src = v.get("sources")
    if not isinstance(src, list) or len(src) != 35:
        fail("harness registry must contain exactly 35 sources")
    if [x.get("source_id") for x in src] != [f"{i:02d}" for i in range(1, 36)]:
        fail("harness source IDs drift")


def load_estate(repo: Path) -> Mapping[str, Any]:
    v = json.loads(git(repo, "show", f"{ESTATE_HEAD}:{ESTATE_PATH}"))
    validate_estate(v)
    return v


def load_harness(repo: Path) -> Mapping[str, Any]:
    v = json.loads((repo / HARNESS_REGISTRY_PATH).read_text())
    validate_harness(v)
    return v


def bind(estate: Mapping[str, Any], harness: Mapping[str, Any]) -> list[dict[str, Any]]:
    validate_estate(estate); validate_harness(harness)
    out = []
    for i, (e, h) in enumerate(zip(estate["sources"], harness["sources"]), 1):
        sid = f"{i:02d}"
        if e["canonical_source_id"] != f"CLOSED35-{sid}" or h["source_id"] != sid:
            fail(f"ID mismatch at {sid}")
        if e["canonical_filename"] != h["canonical_filename"]:
            fail(f"filename mismatch at {sid}")
        if e["canonical_sha256"] != h["canonical_sha256"]:
            fail(f"SHA mismatch at {sid}")
        if int(e["canonical_expected_size"]) != int(h["size_bytes"]):
            fail(f"size mismatch at {sid}")
        out.append({
            "source_id": sid,
            "filename": e["canonical_filename"],
            "sha256": e["canonical_sha256"],
            "size": int(e["canonical_expected_size"]),
            "state": e["acquisition_state"],
            "member": e.get("archive_member_path"),
        })
    return out


def verify_identity(path: Path, size: int, sha: str, label: str) -> None:
    if not path.is_file():
        fail(f"{label} missing: {path}")
    if path.stat().st_size != size:
        fail(f"{label} size mismatch")
    actual = sha256_file(path)
    if actual != sha:
        fail(f"{label} SHA-256 mismatch: {actual} != {sha}")


def immutable_json(path: Path, value: Mapping[str, Any]) -> None:
    data = cjson(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            fail(f"immutable conflict: {path}")
        return
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    tmp = Path(name)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError:
            if path.read_bytes() != data:
                fail(f"immutable race/conflict: {path}")
    finally:
        tmp.unlink(missing_ok=True)


def write_stream(handle, target: Path, size: int, sha: str) -> None:
    if target.exists():
        verify_identity(target, size, sha, "existing staged " + target.name)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + target.name + ".", dir=target.parent)
    os.close(fd)
    tmp = Path(name)
    h = hashlib.sha256(); n = 0
    try:
        with tmp.open("wb") as out:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                out.write(block); h.update(block); n += len(block)
            out.flush(); os.fsync(out.fileno())
        if n != size or h.hexdigest() != sha:
            fail(f"extracted member identity mismatch for {target.name}")
        try:
            os.link(tmp, target)
        except FileExistsError:
            verify_identity(target, size, sha, "raced staged " + target.name)
    finally:
        tmp.unlink(missing_ok=True)


def zip_map(zf: zipfile.ZipFile, names: Sequence[str]) -> dict[str, zipfile.ZipInfo]:
    all_names: dict[str, list[zipfile.ZipInfo]] = {}
    for info in zf.infolist():
        all_names.setdefault(info.filename, []).append(info)
    out = {}
    for name in names:
        if name.startswith("__MACOSX/") or "/__MACOSX/" in name:
            fail("canonical target may not be an __MACOSX sidecar")
        infos = all_names.get(name, [])
        if len(infos) != 1:
            fail(f"archive member {name!r} count {len(infos)} != 1")
        out[name] = infos[0]
    return out


def allowed_output(rel: str) -> bool:
    if rel in AGGREGATES:
        return True
    return bool(re.fullmatch(r"source_receipts/SOURCE_(0[1-9]|[12][0-9]|3[0-5])_REPRESENTATION_RECEIPT\.json", rel))


def validate_output_reuse(root: Path) -> None:
    if not root.exists():
        return
    if not root.is_dir():
        fail("output root is not a directory")
    bad = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and not allowed_output(p.relative_to(root).as_posix())]
    if bad:
        fail("output root contains non-census files: " + ", ".join(sorted(bad)))


def build_manifest(stage: Path, bound: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    sources = {x["source_id"]: str((stage / x["filename"]).resolve()) for x in bound}
    v = {"schema": PATH_SCHEMA, "sources": sources}
    if sorted(sources) != [f"{i:02d}" for i in range(1, 36)]:
        fail("generated manifest is not exact 01..35")
    for x in bound:
        p = Path(sources[x["source_id"]])
        if not p.is_absolute() or p.name != x["filename"]:
            fail(f"generated path drift at {x['source_id']}")
    return v


def stage(estate: Mapping[str, Any], harness: Mapping[str, Any], surveys: Path, lits1: Path, wvs7: Path,
          stage_root: Path, manifest_out: Path, binding_out: Path, output_root: Path) -> Mapping[str, Any]:
    bound = bind(estate, harness)
    roots = estate["carrier_roots"]
    expected = {
        "surveys": (int(roots["surveys"]["archive_size"]), roots["surveys"]["archive_sha256"]),
        "lits1": (int(roots["lits1"]["raw_size"]), roots["lits1"]["raw_sha256"]),
        "wvs7": (int(roots["wvs7"]["archive_size"]), roots["wvs7"]["archive_sha256"]),
    }
    verify_identity(surveys, *expected["surveys"], "surveys.zip carrier")
    verify_identity(lits1, *expected["lits1"], "LiTS-I carrier")
    verify_identity(wvs7, *expected["wvs7"], "WVS7 archive carrier")

    stage_root.mkdir(parents=True, exist_ok=True)
    wanted = {x["filename"] for x in bound}
    extras = sorted(p.name for p in stage_root.iterdir() if p.name not in wanted)
    if extras:
        fail("unexpected stage-root entries: " + ", ".join(extras))

    sitems = [x for x in bound if x["state"] == "EXACT_ARCHIVE_MEMBER_AVAILABLE" and str(x["member"]).startswith("surveys/")]
    witems = [x for x in bound if x["state"] == "EXACT_ARCHIVE_MEMBER_AVAILABLE" and not str(x["member"]).startswith("surveys/")]
    aitems = [x for x in bound if x["state"] == "EXACT_ALIAS_AVAILABLE"]
    if (len(sitems), len(aitems), len(witems)) != (33, 1, 1):
        fail("expected 33 surveys members + 1 LiTS-I alias + 1 WVS7 member")

    with zipfile.ZipFile(surveys, "r") as zf:
        m = zip_map(zf, [x["member"] for x in sitems])
        for x in sitems:
            with zf.open(m[x["member"]], "r") as src:
                write_stream(src, stage_root / x["filename"], x["size"], x["sha256"])

    alias = aitems[0]
    with lits1.open("rb") as src:
        write_stream(src, stage_root / alias["filename"], alias["size"], alias["sha256"])

    w = witems[0]
    with zipfile.ZipFile(wvs7, "r") as zf:
        m = zip_map(zf, [w["member"]])
        with zf.open(m[w["member"]], "r") as src:
            write_stream(src, stage_root / w["filename"], w["size"], w["sha256"])

    actual = {p.name for p in stage_root.iterdir() if p.is_file()}
    if actual != wanted or len(actual) != 35:
        fail("staging is not exactly 35 canonical files")
    for x in bound:
        verify_identity(stage_root / x["filename"], x["size"], x["sha256"], "staged " + x["source_id"])

    manifest = build_manifest(stage_root, bound)
    immutable_json(manifest_out, manifest)
    binding = {
        "schema": BINDING_SCHEMA,
        "estate_head": ESTATE_HEAD,
        "harness_head": HARNESS_HEAD,
        "qualified_head": QUALIFIED_HEAD,
        "carrier_identities": {k: {"size": v[0], "sha256": v[1]} for k, v in expected.items()},
        "source_identities": [{"source_id": x["source_id"], "size": x["size"], "sha256": x["sha256"]} for x in bound],
        "path_manifest_sha256": hashlib.sha256(cjson(manifest)).hexdigest(),
        "staged_source_count": 35,
        "unresolved_source_count": 0,
    }
    immutable_json(binding_out, binding)
    validate_output_reuse(output_root)
    return binding


def reject_raw(root: Path) -> None:
    bad = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.suffix.lower() in RAW_SUFFIXES]
    if bad:
        fail("raw survey/archive file in receipt tree: " + ", ".join(sorted(bad)))


def verify_results(output: Path, harness: Mapping[str, Any]) -> Mapping[str, int]:
    validate_harness(harness)
    if not output.is_dir():
        fail("census output root missing")
    reject_raw(output); validate_output_reuse(output)
    rr = output / "source_receipts"
    expected = {f"SOURCE_{i:02d}_REPRESENTATION_RECEIPT.json" for i in range(1, 36)}
    if not rr.is_dir() or {p.name for p in rr.iterdir() if p.is_file()} != expected:
        fail("authoritative result must contain exactly 35 receipt files")
    by_id = {x["source_id"]: x for x in harness["sources"]}
    receipts = {}; passed = blocked = 0
    for sid in [f"{i:02d}" for i in range(1, 36)]:
        v = json.loads((rr / f"SOURCE_{sid}_REPRESENTATION_RECEIPT.json").read_text())
        if v.get("schema") != RECEIPT_SCHEMA or v.get("source_id") != sid or v.get("canonical_sha256") != by_id[sid]["canonical_sha256"]:
            fail(f"receipt {sid} identity/schema mismatch")
        if v.get("status") == "PASS": passed += 1
        elif v.get("status") == "BLOCKED": blocked += 1
        else: fail(f"receipt {sid} status invalid")
        receipts[sid] = v
    for name in AGGREGATES:
        if not (output / name).is_file():
            fail("missing aggregate: " + name)

    obs = json.loads((output / AGGREGATES[0]).read_text())
    if obs.get("schema") != OBS_SCHEMA or obs.get("source_receipt_count") != 35 or len(obs.get("sources") or []) != 35:
        fail("observation aggregate mismatch")
    for v in obs["sources"]:
        if receipts.get(str(v.get("source_id"))) != v:
            fail("aggregate/source receipt drift")

    edge = json.loads((output / AGGREGATES[2]).read_text())
    if edge.get("schema") != EDGE_SCHEMA or len(edge.get("sources") or []) != 35:
        fail("edge aggregate mismatch")
    dep = json.loads((output / AGGREGATES[3]).read_text())
    if dep.get("schema") != DEP_SCHEMA or dep.get("pass") is not True or dep.get("ambient_current_dependency_leaks") not in ([], None):
        fail("historical dependency aggregate mismatch")
    run = json.loads((output / AGGREGATES[4]).read_text())
    if run.get("schema") != RUNTIME_SCHEMA or run.get("pass") is not True:
        fail("runtime receipt mismatch")
    validate_runtime(run.get("observed") or {})
    summary = json.loads((output / AGGREGATES[5]).read_text())
    if summary.get("schema") != SUMMARY_SCHEMA or summary.get("source_count") != 35:
        fail("summary schema/count mismatch")
    if int(summary.get("source_pass_count", -1)) + int(summary.get("source_blocked_count", -1)) != 35:
        fail("summary PASS/BLOCKED count mismatch")
    if summary.get("terminal") != "CLOSED35_REPRESENTATION_CENSUS_COMPLETE":
        fail("summary terminal mismatch")

    with (output / AGGREGATES[1]).open(newline="") as f:
        r = csv.DictReader(f)
        headers = ["source_id","source_file","surface_id","variable_name","classification","owner_key_status","exact_join","numeric_coercion_used_for_join"]
        if r.fieldnames != headers:
            fail("typed join matrix header mismatch")
        for row in r:
            if row["source_id"] not in by_id:
                fail("typed join matrix unknown source")
            if row["numeric_coercion_used_for_join"].lower() not in {"false", "0"}:
                fail("typed join matrix reports numeric coercion")
    return {"receipts": 35, "pass": passed, "blocked": blocked, "aggregates": 6}


def cmd_preflight(a: argparse.Namespace) -> int:
    repo = Path(a.repo_root).resolve()
    result = preflight_repo(repo)
    for raw, label in ((a.surveys_zip, "surveys.zip"), (a.lits1, "LiTS-I"), (a.wvs7_zip, "WVS7 archive")):
        if not Path(raw).expanduser().resolve().is_file():
            fail(f"{label} input missing")
    print("CLOSED35_PACKAGER PREFLIGHT PASS " + json.dumps(result, sort_keys=True))
    return 0


def cmd_stage(a: argparse.Namespace) -> int:
    repo = Path(a.repo_root).resolve()
    result = stage(load_estate(repo), load_harness(repo),
                   Path(a.surveys_zip).expanduser().resolve(),
                   Path(a.lits1).expanduser().resolve(),
                   Path(a.wvs7_zip).expanduser().resolve(),
                   Path(a.stage_root).expanduser().resolve(),
                   Path(a.manifest_out).expanduser().resolve(),
                   Path(a.binding_out).expanduser().resolve(),
                   Path(a.output_root).expanduser().resolve())
    print("CLOSED35_STAGE COMPLETE 35 PASS / 0 unresolved")
    print(json.dumps(result, sort_keys=True))
    return 0


def cmd_verify(a: argparse.Namespace) -> int:
    repo = Path(a.repo_root).resolve()
    result = verify_results(Path(a.output_root).expanduser().resolve(), load_harness(repo))
    print("CLOSED35_RESULT_VERIFY PASS " + json.dumps(result, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    q = s.add_parser("preflight")
    q.add_argument("--repo-root", required=True); q.add_argument("--surveys-zip", required=True)
    q.add_argument("--lits1", required=True); q.add_argument("--wvs7-zip", required=True); q.set_defaults(fn=cmd_preflight)
    q = s.add_parser("stage")
    for name in ("repo-root","surveys-zip","lits1","wvs7-zip","stage-root","manifest-out","binding-out","output-root"):
        q.add_argument("--" + name, required=True)
    q.set_defaults(fn=cmd_stage)
    q = s.add_parser("verify-results")
    q.add_argument("--repo-root", required=True); q.add_argument("--output-root", required=True); q.set_defaults(fn=cmd_verify)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    a = parser().parse_args(argv)
    try:
        return int(a.fn(a))
    except PackagerError as e:
        print("CLOSED35_PACKAGER BLOCKED: " + str(e), file=os.sys.stderr)
        return 86


if __name__ == "__main__":
    raise SystemExit(main())
