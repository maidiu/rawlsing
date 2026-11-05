"""Exact S48-S52 pins, closure cuts and blob verification."""
from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = RETURN.parents[1]
COMMISSION_BASE = "078d9c57bc835a34e90b3671bdef6c28a0f43747"
G18_EXTERNAL = Path(
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/"
    "WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/"
    "candidate/vendor/bp2/vendor/g18"
)


@dataclass(frozen=True)
class Pin:
    key: str
    cut: str
    base: str
    package: str


PINS = {
    "s48": Pin("s48", "9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7",
               "WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1", "s48"),
    "s49": Pin("s49", "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43",
               "WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1", "s49"),
    "s50": Pin("s50", "515b9a8ee45672c97051df4efef679117a679525",
               "WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1", "s50"),
    "s51": Pin("s51", "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65",
               "WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1", "s51"),
    "s52": Pin("s52", "c821b488b3a9a3f0fa01b1981989cc17af637dc1",
               "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1", "s52"),
    "s47": Pin("s47", "765a441f87292aa4c17794745b65cb54e6aaa83f",
               "WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1", "s47"),
    "s46": Pin("s46", "f0ef39b92ce2e4add5c0a699389e12f1d7ae434e",
               "WORKER_RETURNS/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1", "s46"),
    "s45": Pin("s45", "f26a138e20d53c809d611cf8d834ec647b0804bf",
               "WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1", "s45"),
    "s44": Pin("s44", "923278fbe6b030e2ffdd10fe42d7a18266344611",
               "WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1", "s44"),
    "s43": Pin("s43", "3edd631fb6c31751dfd2143ba2faa9fc31561e54",
               "WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1", "s43"),
    "s41": Pin("s41", "c72a10d284f8869b990db3e6849ed174a51bd784",
               "WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1", "s41"),
    "s40": Pin("s40", "79b0357c7af9b66ad8a28f5b77b46b0348094a23",
               "WORKER_RETURNS/SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1", "s40"),
    "s36": Pin("s36", "8da78d8031a06a4bd7e1297fd713e573299c0860",
               "WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1", "candidate"),
    "r31j": Pin("r31j", "64fec28c374d8f77fb0b412d0c934d798ede03e8",
                "WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1", "candidate"),
    "join_e": Pin("join_e", "7bf2da302996491ddf34b9a039fea47ac982d135",
                  "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1", "joined"),
    "language": Pin("language", "8d2920da951f98cd8246d7c34cac777928e0c732",
                    "LANGUAGE_MEDIATION_R1", "language_mediation"),
    "s42": Pin("s42", "2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91",
               "WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1", "s42"),
    "s37": Pin("s37", "e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9",
               "WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1", "s37"),
    "s39": Pin("s39", "e41513fa65601a37e7b3b430d26c626ae0217d90",
               "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1", "s39"),
}

CLOSURES = {
    "s49": {
        "anchor": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43",
        "keys": {"s48": "9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7",
                 "s49": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43",
                 "s42": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43",
                 "s37": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43",
                 "s39": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43"},
    },
    "s50": {
        "anchor": "515b9a8ee45672c97051df4efef679117a679525",
        "keys": {"s50": "515b9a8ee45672c97051df4efef679117a679525",
                 "s49": "515b9a8ee45672c97051df4efef679117a679525",
                 "s48": "9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7",
                 "s42": "515b9a8ee45672c97051df4efef679117a679525",
                 "s37": "515b9a8ee45672c97051df4efef679117a679525",
                 "s39": "515b9a8ee45672c97051df4efef679117a679525"},
    },
    "s51": {
        "anchor": "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65",
        "keys": {"s51": "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65",
                 "s49": "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65",
                 "s48": "9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7",
                 "s42": "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65",
                 "s37": "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65",
                 "s39": "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65"},
    },
    "s52": {
        "anchor": "c821b488b3a9a3f0fa01b1981989cc17af637dc1",
        "keys": {"s52": "c821b488b3a9a3f0fa01b1981989cc17af637dc1",
                 "s51": "c821b488b3a9a3f0fa01b1981989cc17af637dc1",
                 "s49": "c821b488b3a9a3f0fa01b1981989cc17af637dc1",
                 "s48": "9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7",
                 "s42": "c821b488b3a9a3f0fa01b1981989cc17af637dc1",
                 "s37": "c821b488b3a9a3f0fa01b1981989cc17af637dc1",
                 "s39": "c821b488b3a9a3f0fa01b1981989cc17af637dc1"},
    },
}

FIXED_KEYS = ("s47", "s46", "s45", "s44", "s43", "s41", "s40", "s36", "r31j", "join_e", "language")
M35_CUT = "4170fbf19a9d5a64bc728f5b22156bbffcec51e5"
M35_BASE = "WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1"


def git(source_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(source_root),
                          capture_output=True, text=True, check=False)


def blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_map(source_root: Path, cut: str, base: str) -> dict[str, str]:
    proc = subprocess.run(["git", "ls-tree", "-r", "-z", cut, "--", base],
                          cwd=str(source_root), capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError("GIT_LS_TREE_FAILED:" + cut)
    rows = {}
    prefix = base.rstrip("/") + "/"
    for entry in proc.stdout.split(b"\0"):
        if not entry:
            continue
        meta, raw = entry.split(b"\t", 1)
        parts = meta.decode().split()
        path = raw.decode()
        if len(parts) == 3 and parts[1] == "blob" and path.startswith(prefix):
            rows[path[len(prefix):]] = parts[2]
    return rows


def verify_key(source_root: Path, stage: Path, key: str, cut: str) -> dict:
    pin = PINS[key]
    expected = tree_map(source_root, cut, pin.base)
    rows = []
    errors = []
    for rel in sorted(expected):
        if not rel.endswith(".py"):
            continue
        target = stage / pin.base / rel
        if not target.is_file():
            errors.append("MISSING:" + rel)
            continue
        actual = blob_sha1(target)
        exact = actual == expected[rel]
        rows.append({"path": rel, "pinned_git_blob_sha1": expected[rel],
                     "staged_git_blob_sha1": actual, "exact": exact,
                     "sha256": sha256_file(target)})
        if not exact:
            errors.append("BLOB_MISMATCH:" + rel)
    return {"key": key, "base": pin.base, "cut": cut,
            "files_checked": len(rows), "all_exact": not errors,
            "errors": errors, "rows": rows}


def manifest(source_root: Path, stages: dict[str, Path]) -> dict:
    closures = {}
    for name, stage in stages.items():
        keys = dict(CLOSURES[name]["keys"])
        for key in FIXED_KEYS:
            keys[key] = PINS[key].cut
        rows = {key: verify_key(source_root, stage, key, cut)
                for key, cut in keys.items()}
        seams = {}
        for key, cut in CLOSURES[name]["keys"].items():
            seam = []
            for rel, blob in tree_map(source_root, cut, PINS[key].base).items():
                if not rel.endswith(".py"):
                    continue
                base = tree_map(source_root, PINS[key].cut, PINS[key].base).get(rel)
                if base and base != blob:
                    seam.append({"path": rel, "base_pin_blob": base,
                                 "closure_blob": blob})
            if seam:
                seams[key] = {"base_pin_cut": PINS[key].cut,
                              "closure_cut": cut, "files": seam}
        closures[name] = {
            "anchor": CLOSURES[name]["anchor"],
            "keys": keys,
            "rows": rows,
            "all_exact": all(row["all_exact"] for row in rows.values()),
            "seams": seams,
        }
    m35_expected = tree_map(source_root, M35_CUT, M35_BASE)
    m35_root = stages["s49"] / PINS["s37"].base / "vendor" / "m35"
    m35_rows = []
    m35_errors = []
    for path in sorted(m35_root.rglob("*.py")):
        rel = str(path.relative_to(m35_root))
        expected = m35_expected.get(rel, "")
        actual = blob_sha1(path)
        exact = bool(expected) and expected == actual
        m35_rows.append({"path": rel, "pinned_git_blob_sha1": expected,
                         "staged_git_blob_sha1": actual, "exact": exact,
                         "sha256": sha256_file(path)})
        if not exact:
            m35_errors.append(rel)
    g18_expected = tree_map(
        source_root, PINS["r31j"].cut,
        PINS["r31j"].base + "/candidate/vendor/bp2/vendor/g18")
    g18_rows = []
    g18_errors = []
    if G18_EXTERNAL.is_dir():
        for path in sorted(G18_EXTERNAL.rglob("*.py")):
            rel = str(path.relative_to(G18_EXTERNAL))
            expected = g18_expected.get(rel, "")
            actual = blob_sha1(path)
            exact = bool(expected) and expected == actual
            g18_rows.append({"path": rel, "pinned_git_blob_sha1": expected,
                             "staged_git_blob_sha1": actual, "exact": exact,
                             "sha256": sha256_file(path)})
            if not exact:
                g18_errors.append(rel)
    return {
        "schema": "SOROK_CURRENT_B_SEAM_SOURCE_MANIFEST@1",
        "commission_base": COMMISSION_BASE,
        "primary_pins": {key: {"cut": PINS[key].cut, "base": PINS[key].base}
                         for key in ("s48", "s49", "s50", "s51", "s52")},
        "closures": closures,
        "m35_vendor": {"cut": M35_CUT, "files_checked": len(m35_rows),
                       "all_exact": not m35_errors, "errors": m35_errors,
                       "rows": m35_rows},
        "g18_external": {"path": str(G18_EXTERNAL), "cut": PINS["r31j"].cut,
                         "files_checked": len(g18_rows),
                         "all_exact": not g18_errors, "errors": g18_errors,
                         "rows": g18_rows},
        "all_exact": all(row["all_exact"] for row in closures.values())
        and not m35_errors and not g18_errors,
    }


__all__ = ["CLOSURES", "COMMISSION_BASE", "DEFAULT_SOURCE_ROOT", "G18_EXTERNAL",
           "PINS", "RETURN", "manifest", "tree_map", "verify_key"]
