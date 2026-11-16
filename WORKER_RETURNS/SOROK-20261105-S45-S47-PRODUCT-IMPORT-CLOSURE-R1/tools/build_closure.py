from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent
WORKSPACE = next(p for p in HERE.parents if (p / ".git").exists())
PRODUCT = TARGET / "product"
VENDOR = PRODUCT / "vendor"

S36 = ("8da78d8031a06a4bd7e1297fd713e573299c0860", "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1")
S37 = ("e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9", "SOROK-20261024-S37-INTEGRATED-CONSUMER-R1")
S39 = ("e41513fa65601a37e7b3b430d26c626ae0217d90", "SOROK-20261024-S39-GENERATED-RESPONSE-R1")
S40 = ("79b0357c7af9b66ad8a28f5b77b46b0348094a23", "SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1")
S41 = ("c72a10d284f8869b990db3e6849ed174a51bd784", "SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1")
S42 = ("2489f8cdfbb5c400c636f33c7cf8cdf0aa55dc91", "SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1")
S43 = ("3edd631fb6c31751dfd2143ba2faa9fc31561e54", "SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1")
S44 = ("923278fbe6b030e2ffdd10fe42d7a18266344611", "SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1")
S45 = ("f26a138e20d53c809d611cf8d834ec647b0804bf", "SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1")
S46 = ("f0ef39b92ce2e4add5c0a699389e12f1d7ae434e", "SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1")
S47 = ("765a441f87292aa4c17794745b65cb54e6aaa83f", "SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1")
JOIN_E = ("7bf2da302996491ddf34b9a039fea47ac982d135", "SOROK-20261022-SAME-PERSON-JOIN-R1")
LANGUAGE = ("8d2920da951f98cd8246d7c34cac777928e0c732", "LANGUAGE_MEDIATION_R1")
WP19 = ("3c4df43f813cd0727feff04f620aa0bbd9a63026", "SOROK-WP19-ENCOUNTER-PROTOTYPE-R1")
S11 = ("faec7ce909c54664e85320534bdf744b9bc47d37", "SOROK-S11-ENCOUNTER-EXIT-SPEC-R1")
LIVE = ("7bf2da302996491ddf34b9a039fea47ac982d135", "rawlsing_next")
CUMULATIVE = "765a441f87292aa4c17794745b65cb54e6aaa83f"

SKIP_SEGMENTS = {"evidence", "logs", "junit", "receipts", "tests", "tools", "__pycache__"}
LIVE_FILES = (
    "rawlsing_next/m1_temporal_v554_admission_dedup.py",
    "rawlsing_next/m2_v555_atomic_route.py",
    "rawlsing_next/m3_v556_higher_order_structural.py",
    "rawlsing_next/m4_v557_v558_publication_repository.py",
    "rawlsing_next/m5_runtime_rsc_peer_prior.py",
    "rawlsing_next/m6_actor_safe_expression.py",
)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=WORKSPACE, text=True)


def blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def paths_at(commit: str, prefix: str) -> list[str]:
    output = git("ls-tree", "-r", "--name-only", commit, "--", prefix)
    return [line for line in output.splitlines() if line]


def include(commit: str, path: str, kind: str) -> bool:
    if kind == "source":
        return path.endswith(".py")
    if kind == "tests":
        return path.endswith(".py")
    if kind == "join":
        if not (path.startswith("WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/joined/")
                or path.startswith("WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/")):
            return False
        if not path.endswith((".py", ".json")):
            return False
        segments = set(path.split("/"))
        return not (segments & SKIP_SEGMENTS)
    if kind == "language":
        return path.endswith(".py") and "/language_mediation/" in path
    if kind == "wp19":
        return path.endswith(".py") and "/wp19/" in path
    if kind == "s11":
        return path.endswith("/02_WP19_CONSUMABLE_INTERFACE.json")
    if kind == "live":
        return path in LIVE_FILES
    raise ValueError(kind)


def selected() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    rows += [(CUMULATIVE, p, S36[0]) for p in paths_at(S36[0], f"WORKER_RETURNS/{S36[1]}/candidate/") if include(S36[0], p, "source")]
    rows += [(CUMULATIVE, p, S37[0]) for p in paths_at(S37[0], f"WORKER_RETURNS/{S37[1]}/s37/") if include(S37[0], p, "source")]
    rows += [(CUMULATIVE, p, S37[0]) for p in paths_at(S37[0], f"WORKER_RETURNS/{S37[1]}/vendor/m35/") if include(S37[0], p, "source")]
    for commit, name in (S39, S40, S41, S42, S43, S44):
        rows += [(CUMULATIVE, p, commit) for p in paths_at(commit, f"WORKER_RETURNS/{name}/") if include(commit, p, "source")]
    for commit, name, package in ((S45[0], S45[1], "s45"), (S46[0], S46[1], "s46"), (S47[0], S47[1], "s47")):
        rows += [(CUMULATIVE, p, commit) for p in paths_at(commit, f"WORKER_RETURNS/{name}/{package}/") if include(commit, p, "source")]
        rows += [(CUMULATIVE, p, commit) for p in paths_at(commit, f"WORKER_RETURNS/{name}/tests/") if include(commit, p, "tests")]
        rows += [(CUMULATIVE, p, commit) for p in paths_at(commit, f"WORKER_RETURNS/{name}/") if p.endswith(f"/run_{package}.py")]
    rows += [(JOIN_E[0], p, JOIN_E[0]) for p in paths_at(JOIN_E[0], f"WORKER_RETURNS/{JOIN_E[1]}/") if include(JOIN_E[0], p, "join")]
    rows += [(LANGUAGE[0], p, LANGUAGE[0]) for p in paths_at(LANGUAGE[0], f"{LANGUAGE[1]}/") if include(LANGUAGE[0], p, "language")]
    rows += [(WP19[0], p, WP19[0]) for p in paths_at(WP19[0], f"WORKER_RETURNS/{WP19[1]}/") if include(WP19[0], p, "wp19")]
    rows += [(S11[0], p, S11[0]) for p in paths_at(S11[0], f"WORKER_RETURNS/{S11[1]}/") if include(S11[0], p, "s11")]
    rows += [(LIVE[0], p, LIVE[0]) for p in paths_at(LIVE[0], "rawlsing_next/") if include(LIVE[0], p, "live")]
    return sorted(set(rows))


def main() -> int:
    if (PRODUCT / "vendor").exists():
        shutil.rmtree(PRODUCT / "vendor")
    if (TARGET / "SOURCE_MANIFEST.json").exists():
        (TARGET / "SOURCE_MANIFEST.json").unlink()
    PRODUCT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for commit, path, semantic_root in selected():
        data = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=WORKSPACE)
        expected = git("rev-parse", f"{commit}:{path}").strip()
        actual = blob_sha1(data)
        if actual != expected:
            raise SystemExit(f"BLOB_MISMATCH:{commit}:{path}:{expected}:{actual}")
        logical = ""
        try:
            logical = git("rev-parse", f"{semantic_root}:{path}").strip()
        except subprocess.CalledProcessError:
            logical = ""
        source_commit = semantic_root if logical == expected else commit
        destination = PRODUCT / "vendor" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        manifest.append({
            "source_commit": source_commit,
            "semantic_root": semantic_root,
            "integration_cut": source_commit != semantic_root,
            "source_path": path,
            "installed_path": str(destination.relative_to(TARGET)),
            "git_blob": expected,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        })
    document = {
        "schema": "SOROK_S45_S47_PRODUCT_SOURCE_MANIFEST@1",
        "generated_by": "OC-A S45-S47 product import closure",
        "pinned_roots": {
            "s36": S36[0], "s37": S37[0], "s39": S39[0], "s40": S40[0],
            "s41": S41[0], "s42": S42[0], "s43": S43[0], "s44": S44[0],
            "s45": S45[0], "s46": S46[0], "s47": S47[0],
            "join_e": JOIN_E[0], "language": LANGUAGE[0],
            "wp19": WP19[0], "s11": S11[0],
            "live_rawlsing_next": LIVE[0],
        },
        "file_count": len(manifest),
        "total_bytes": sum(row["bytes"] for row in manifest),
        "files": manifest,
    }
    (TARGET / "SOURCE_MANIFEST.json").write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf8"
    )
    print(json.dumps({
        "target": str(TARGET),
        "files": len(manifest),
        "bytes": document["total_bytes"],
        "manifest": str(TARGET / "SOURCE_MANIFEST.json"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
