"""Independent source-identity checks for the RA-D review."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys
from pathlib import Path

REPO = Path(os.environ["RAD_REVIEW_REPO"])
ARCHIVE = Path(os.environ["RAD_REVIEW_ARCHIVE"])
S52_COMMIT = "c821b488b3a9a3f0fa01b1981989cc17af637dc1"
S50_COMMIT = "515b9a8ee45672c97051df4efef679117a679525"

def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True)

report = {"schema": "RA_D_INDEPENDENT_REVIEW_SOURCE_IDENTITY@1"}

# 1. Every .py archived from the S52 commit must equal the committed blob.
tree = git("ls-tree", "-r", "-z", "--name-only", S52_COMMIT, "WORKER_RETURNS/")
paths = [p for p in tree.split("\0") if p and p.endswith(".py")]
rows = []
for rel in paths:
    frag = rel.split("WORKER_RETURNS/", 1)[1]
    # only S36-S52 returns belong to the RA-D extraction
    if not any(frag.startswith(x) for x in (
        "SOROK-20261024-S36", "SOROK-20261024-S37", "SOROK-20261024-S39",
        "SOROK-20261024-S40", "SOROK-20261024-S41", "SOROK-20261024-S42",
        "SOROK-20261024-S43", "SOROK-20261024-S44", "SOROK-20261025-S45",
        "SOROK-20261025-S46", "SOROK-20261025-S47", "SOROK-20261025-S48",
        "SOROK-20261025-S49", "SOROK-20261025-S51", "SOROK-20261025-S52")):
        continue
    expected = git("rev-parse", f"{S52_COMMIT}:{rel}").strip()
    file = ARCHIVE / rel
    actual = blob_sha1(file.read_bytes()) if file.is_file() else ""
    rows.append({"file": rel, "expected_blob": expected, "actual_blob": actual, "same": expected == actual, "exists": file.is_file()})
report["s52_python_archive"] = {
    "count": len(rows),
    "all_same": bool(rows) and all(r["same"] for r in rows),
    "mismatches": [r for r in rows if not r["same"]],
    "files": rows,
}

# 2. Five ancestor divergences, verified from accepted cut commits vs archived bytes.
cut_files = [
    ("SOROK-20261024-S37-INTEGRATED-CONSUMER-R1", "e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9", "s37/producer.py"),
    ("SOROK-20261024-S39-GENERATED-RESPONSE-R1", "e41513fa65601a37e7b3b430d26c626ae0217d90", "s39/model.py"),
    ("SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1", "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43", "s49/actor.py"),
    ("SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1", "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43", "s49/session.py"),
    ("SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1", "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65", "s51/session.py"),
]
cut_rows = []
for ret, cut, sub in cut_files:
    rel = f"WORKER_RETURNS/{ret}/{sub}"
    expected = git("rev-parse", f"{cut}:{rel}").strip()
    file = ARCHIVE / rel
    actual = blob_sha1(file.read_bytes()) if file.is_file() else ""
    cut_rows.append({"return": ret, "cut": cut, "file": rel, "accepted_blob": expected,
                     "s52_archive_blob": actual, "differs": expected != actual})
report["ancestor_divergences"] = {"count": len(cut_rows), "rows": cut_rows,
                                  "all_five_differ": all(r["differs"] for r in cut_rows)}

# 3. Imported modules: exact path and hashes from the reviewer's extraction.
s52 = ARCHIVE / "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
s48 = ARCHIVE / "WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1"
s39 = ARCHIVE / "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1"
for p in (s52, s48, s39):
    sys.path.insert(0, str(p))
from s52.bootstrap import install
install()
import s52.session as ss, s52.performer as sp, s51.session as s51, s49.actor as s49a, s49.session as s49s, s39.model as s39m
import lab_sgi1.history as g18h, lab_sgi1.joint as g18j
import joined.session as js
import language_mediation.session as lang
mods = {"s52.session": ss, "s52.performer": sp, "s51.session": s51,
        "s49.actor": s49a, "s49.session": s49s, "s39.model": s39m,
        "lab_sgi1.history": g18h, "lab_sgi1.joint": g18j,
        "joined.session": js, "language_mediation.session": lang}
mod_rows = []
for name, mod in mods.items():
    p = Path(mod.__file__).resolve()
    mod_rows.append({"module": name, "path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                     "in_review_archive": str(ARCHIVE) in str(p)})
report["imported_modules"] = {"rows": mod_rows,
    "all_s52_chain_from_archive": all(r["in_review_archive"] for r in mod_rows[:6]),
    "external_roots": {k: v for k, v in mod_rows if k in ("lab_sgi1.history", "joined.session", "language_mediation.session")} if False else
        [r for r in mod_rows if r["module"] in ("lab_sgi1.history", "joined.session", "language_mediation.session")]}

# 4. S50 31 source identities and fixture hash.
s50 = ARCHIVE / "WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1"
sys.path.insert(0, str(s50))
from s50.recovery import verify_source
v = verify_source()
report["s50_source_identity"] = {"count": v["count"], "all_exact": v["all_exact"],
    "fixture_sha256": v["fixture_sha256"], "source_root": v["source_root"],
    "mismatches": [r for r in v["rows"] if not r["exact"]]}

# 5. S50 commit archive bytes match 515b9a8e.
s50_rows = []
for rel in [x for x in git("ls-tree", "-r", "-z", "--name-only", S50_COMMIT,
             "WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1/").split("\0") if x]:
    expected = git("rev-parse", f"{S50_COMMIT}:{rel}").strip()
    file = ARCHIVE / rel
    actual = blob_sha1(file.read_bytes()) if file.is_file() else ""
    s50_rows.append({"file": rel, "expected_blob": expected, "actual_blob": actual, "same": expected == actual})
report["s50_commit_archive"] = {"count": len(s50_rows), "all_same": all(r["same"] for r in s50_rows),
                                "mismatches": [r for r in s50_rows if not r["same"]]}

print(json.dumps(report, indent=2, sort_keys=True))
