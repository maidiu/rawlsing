#!/usr/bin/env python3
"""C0P — stage the ACCESSIBLE Pyat closure, blob-authenticated, into this return.

Resolution is not hand-curated: the closure is discovered by iteratively resolving
`ModuleNotFoundError`/`ImportError` against the pinned Pyat commit and pulling the
named module from that exact commit, then re-verifying Git blob SHA-1 (recomputed
from the true binary preimage) against `git rev-parse`.

Anything that cannot be resolved from the pinned commit is recorded as an
ABSENT interface and is NOT substituted, stubbed or reimplemented.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ["C0P_REPO"])
OUT = Path(os.environ["C0P_RUNTIME"])

# The Pyat commit whose tree actually carries the accessible machinery.
PYAT = "79cb8244a5291218bde17142b93fc2419eade396"      # E04T native current-grant repair
E04T = "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R15-E04T-NATIVE-CURRENT-GRANT-REPAIR-R1"

# E03 commit carries the N9/N10W progressive candidate that product.empirical
# imports. Discovered by reachability probe after an earlier probe silently
# failed (macOS has no `timeout`); recorded explicitly rather than by luck.
E03 = "0e0ed50dbce2dd1434d3a3c84b937b9a956adba9"

SEEDS = [
    ("rawlsing_next/pre553_n9_n10w_progressive_candidate.py",
     "rawlsing_next/pre553_n9_n10w_progressive_candidate.py"),
] + [
    (f"{E04T}/product/{m}.py", f"product/{m}.py")
    for m in ("__init__", "empirical", "world", "service", "nonparent", "scenario")
] + [
    (f"rawlsing_next/{m}.py", f"rawlsing_next/{m}.py")
    for m in (
        "m4_v557_v558_publication_repository", "m5_runtime_rsc_peer_prior",
        "pre553_empirical_objects", "pre553_empirical_authority",
        "pre553_empirical_possibility_provider", "pre553_empirical_query",
    )
] + [
    (f"rawlsing_next/tests/{m}.py", f"rawlsing_next/tests/{m}.py")
    for m in ("test_pre553_empirical_query", "c1_at08_at13_fixture")
]

# The probe must import EVERY entrypoint the court uses, including the two
# TEST_ONLY fixtures product.empirical builds its source from, otherwise the
# resolver stops before the closure is actually complete.
PROBE = "".join([
    "import sys;sys.path.insert(0,'.')\n",
    "import product.service, product.empirical\n",
    "from product.world import SelectedWorldCatalog\n",
    "from product.nonparent import consume\n",
    "from product.scenario import evaluate\n",
    "from rawlsing_next.pre553_empirical_possibility_provider import "
    "provide_empirical_possibility_slice\n",
    "import rawlsing_next.tests.test_pre553_empirical_query\n",
    "import rawlsing_next.tests.c1_at08_at13_fixture\n",
    "product.empirical.build_source()\n",
])


def git(*a, text=False):
    return subprocess.run(["git", "-C", str(REPO), *a], check=True,
                          capture_output=True, text=text).stdout


def blob_of(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def pull(src_commit, repo_path, dest_rel, ledger):
    data = git("cat-file", "blob", f"{src_commit}:{repo_path}")
    store = git("rev-parse", f"{src_commit}:{repo_path}", text=True).strip()
    b = blob_of(data)
    ok = b == store
    dest = OUT / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    ledger.append(dict(commit=src_commit, repo_path=repo_path, staged=dest_rel,
                       bytes=len(data), computed_blob_sha1=b,
                       git_store_blob_sha1=store,
                       sha256=hashlib.sha256(data).hexdigest(), all_match=ok))
    return ok


def missing_module():
    """Return the dotted name of the first unimportable module, or None."""
    env = dict(os.environ, PYTHONPATH=str(OUT))
    p = subprocess.run([sys.executable, "-c", PROBE], cwd=OUT,
                       capture_output=True, text=True, env=env)
    if p.returncode == 0:
        return None
    marker = "No module named '"
    idx = p.stderr.rfind(marker)
    if idx < 0:
        return f"UNPARSED::{p.stderr.strip().splitlines()[-1][:90]}"
    start = idx + len(marker)
    end = p.stderr.find("'", start)
    return p.stderr[start:end]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rawlsing_next").mkdir(parents=True, exist_ok=True)
    (OUT / "rawlsing_next/tests").mkdir(parents=True, exist_ok=True)
    (OUT / "rawlsing_next/tests/__init__.py").write_bytes(b"")
    (OUT / "rawlsing_next" / "__init__.py").write_bytes(b"")
    ledger, absent = [], []

    for repo_path, dest_rel in SEEDS:
        src_commit = E03 if dest_rel.endswith("pre553_n9_n10w_progressive_candidate.py") else PYAT
        if not pull(src_commit, repo_path, dest_rel, ledger):
            absent.append(f"{src_commit}:{repo_path}")

    # iteratively resolve the transitive closure
    for _ in range(40):
        mod = missing_module()
        if mod is None:
            break
        short = mod.split(".")[-1]
        for cand in (f"rawlsing_next/{short}.py", f"product/{short}.py"):
            if subprocess.run(["git", "-C", str(REPO), "cat-file", "-e",
                               f"{PYAT}:{cand}"],
                              capture_output=True).returncode == 0:
                pull(PYAT, cand, cand, ledger)
                break
        else:
            absent.append(f"{PYAT}:rawlsing_next/{short}.py")
            break

    ok = missing_module() is None
    if not ok:
        absent.append(f"UNRESOLVED::{missing_module()}")

    (OUT.parent / "_c0p_runtime_ledger.json").write_text(
        json.dumps(dict(pyat_commit=PYAT, ledger=ledger, absent=absent,
                        closure_resolves=ok), indent=2) + "\n")

    for row in ledger:
        print(f"{'OK  ' if row['all_match'] else 'FAIL'} {row['staged']:58s} "
              f"blob={row['computed_blob_sha1'][:14]}")
    print(f"\nstaged {len(ledger)} modules; closure resolves: {ok}")
    for a in absent:
        print(f"ABSENT INTERFACE: {a}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
