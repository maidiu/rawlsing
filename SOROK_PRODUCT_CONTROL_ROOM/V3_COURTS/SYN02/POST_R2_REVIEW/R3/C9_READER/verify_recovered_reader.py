"""C9-R3 reader byte-exact rescue verification, not native adoption.

Run from any cwd:
  python3 verify_recovered_reader.py
  python3 verify_recovered_reader.py --actor-tests
  C12_READER_SOURCE=<exact supported C12 return root> python3 verify_recovered_reader.py --full-tests

Full reader acceptance requires C12 and origin-source closure; this runner cannot
issue Rule A/T, confer a source grant, or prove later E2 behavior.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
C9 = ROOT.parent / "C9_SQL"
MANIFEST = ROOT / "RECOVERY_READER_SOURCE_MANIFEST_R1.json"


def blob_hash(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def source_proof() -> dict:
    spec = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = spec["source_files"]
    for relative, expected in files.items():
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError("MISSING_READER_FILE:" + relative)
        actual = blob_hash(path.read_bytes())
        if actual != expected:
            raise RuntimeError("READER_BLOB_MISMATCH:" + relative)
    from check_reader_precondition import HASHES
    for relative, expected in HASHES.items():
        path = C9 / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError("EXACT_C9_B_SOURCE_HASH_MISMATCH:" + relative)
    return {
        "status": "EXACT_READER_AND_WRITER_SOURCE_BLOBS",
        "reader_files": len(files),
        "selected_writer": spec["expected_writer_orig_ref"],
        "native_or_original_science": "NOT_GRANTED",
    }


def tests(full: bool) -> dict:
    if full:
        c12 = os.environ.get("C12_READER_SOURCE")
        if not c12 or not Path(c12).is_dir():
            raise RuntimeError("FULL_FORK_COURT_HELD__C12_READER_SOURCE_ABSENT")
    candidates = ["test_actor_reader.py", "test_dry_sequence.py", "test_legacy_migration.py"]
    if full:
        candidates.append("test_actor_fork_reader.py")
    env = os.environ.copy()
    env["C9_READER_SOURCE"] = str(C9)
    with tempfile.TemporaryDirectory(prefix="sorok-r3-reader-") as temp:
        junit = Path(temp) / "reader.xml"
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--junitxml", str(junit)]
            + [str(ROOT / x) for x in candidates],
            cwd=ROOT, env=env, capture_output=True, text=True, check=False,
        )
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        if not junit.is_file():
            raise RuntimeError("READER_JUNIT_ABSENT")
        tree = ET.parse(junit).getroot()
        suites = [tree] if tree.tag == "testsuite" else list(tree.findall(".//testsuite"))
        totals = {k: sum(int(x.get(k, "0")) for x in suites)
                  for k in ("tests", "failures", "errors", "skipped")}
        receipt = {"mode": "FULL_SOURCEFREE_WITH_C12" if full else "PORTABLE_SOURCEFREE_ACTOR_DRY_MIGRATION",
                   "return_code": result.returncode, "totals": totals,
                   "provenance": "NOT_AN_ORIGINAL_SOURCE_OR_NATIVE_ACTOR_ACCEPTANCE"}
        if result.returncode != 0 or totals["tests"] == 0 or any(
            totals[x] for x in ("failures", "errors", "skipped")
        ):
            raise RuntimeError("READ_CONSUMER_COURT_NOT_FULL_PASS:" + str(receipt))
        return receipt


def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("--actor-tests", action="store_true")
    cli.add_argument("--full-tests", action="store_true")
    args = cli.parse_args()
    print(json.dumps(source_proof(), sort_keys=True))
    if args.actor_tests or args.full_tests:
        print(json.dumps(tests(args.full_tests), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError) as exc:
        print("HOLD:", exc, file=sys.stderr)
        raise SystemExit(2)
