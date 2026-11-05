"""Pinned S45-S47 source closure, exact staging and import provenance."""
from __future__ import annotations

import hashlib
import io
import shutil
import subprocess
import tarfile
from dataclasses import dataclass
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = RETURN.parents[1]
COMMISSION_BASE = "078d9c57bc835a34e90b3671bdef6c28a0f43747"


class HarnessError(RuntimeError):
    """A staging, pin or exactness failure."""


@dataclass(frozen=True)
class Pin:
    key: str
    role: str
    cut: str
    base: str
    package: str


PINS = {
    "s45": Pin(
        "s45",
        "S45 generated-root encounter (explicit requested pin)",
        "f26a138e20d53c809d611cf8d834ec647b0804bf",
        "WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1",
        "s45",
    ),
    "s46": Pin(
        "s46",
        "S46 interval participation consumer (explicit requested pin)",
        "f0ef39b92ce2e4add5c0a699389e12f1d7ae434e",
        "WORKER_RETURNS/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1",
        "s46",
    ),
    "s47": Pin(
        "s47",
        "S47 interval C9 conditioning (explicit requested pin)",
        "765a441f87292aa4c17794745b65cb54e6aaa83f",
        "WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1",
        "s47",
    ),
    "s44": Pin(
        "s44",
        "Accepted S44 sampled antecedent root dependency",
        "923278fbe6b030e2ffdd10fe42d7a18266344611",
        "WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1",
        "s44",
    ),
    "s43": Pin(
        "s43",
        "Accepted S43 historical language dependency",
        "3edd631fb6c31751dfd2143ba2faa9fc31561e54",
        "WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1",
        "s43",
    ),
    "s42": Pin(
        "s42",
        "Accepted S42 ongoing event consumer with S47 seam",
        "765a441f87292aa4c17794745b65cb54e6aaa83f",
        "WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1",
        "s42",
    ),
    "s41": Pin(
        "s41",
        "Accepted S41 continuing person events dependency",
        "c72a10d284f8869b990db3e6849ed174a51bd784",
        "WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1",
        "s41",
    ),
    "s40": Pin(
        "s40",
        "Accepted S40 generated native speech dependency",
        "79b0357c7af9b66ad8a28f5b77b46b0348094a23",
        "WORKER_RETURNS/SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1",
        "s40",
    ),
    "s39": Pin(
        "s39",
        "Accepted S39 generated response dependency",
        "e41513fa65601a37e7b3b430d26c626ae0217d90",
        "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1",
        "s39",
    ),
    "s37": Pin(
        "s37",
        "Accepted S37 integrated consumer with S47 C9 seam",
        "765a441f87292aa4c17794745b65cb54e6aaa83f",
        "WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1",
        "s37",
    ),
    "s36": Pin(
        "s36",
        "Accepted S36 actor-access response candidate",
        "8da78d8031a06a4bd7e1297fd713e573299c0860",
        "WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1",
        "candidate",
    ),
    "r31j": Pin(
        "r31j",
        "Pinned R31J vendor closure consumed by M35/BP2",
        "64fec28c374d8f77fb0b412d0c934d798ede03e8",
        "WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1",
        "candidate",
    ),
    "join_e": Pin(
        "join_e",
        "Pinned JOIN-E same-person closure",
        "7bf2da302996491ddf34b9a039fea47ac982d135",
        "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1",
        "joined",
    ),
    "language": Pin(
        "language",
        "Pinned language mediation closure",
        "8d2920da951f98cd8246d7c34cac777928e0c732",
        "LANGUAGE_MEDIATION_R1",
        "language_mediation",
    ),
}

STAGE_ORDER = (
    "s47",
    "s46",
    "s45",
    "s44",
    "s43",
    "s42",
    "s41",
    "s40",
    "s39",
    "s37",
    "s36",
    "r31j",
    "join_e",
    "language",
)

SEAM_FILES = {
    "s42": (
        "s42/event.py",
        "s42/session.py",
    ),
    "s37": ("s37/producer.py",),
}

M35_VENDOR_BASE = PINS["s37"].base + "/vendor/m35"
M35_CUT = "4170fbf19a9d5a64bc728f5b22156bbffcec51e5"
M35_PIN_BASE = (
    "WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1"
)

IGNORE_COPY = (
    ".git",
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    ".runtime",
    "logs",
    "junit",
    "evidence",
)


def run_git(source_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(source_root),
        capture_output=True,
        text=True,
        check=False,
    )


def require_git(source_root: Path) -> None:
    proc = run_git(source_root, "rev-parse", "--is-inside-work-tree")
    if proc.returncode != 0 or proc.stdout.strip() != "true":
        raise HarnessError(
            "SOURCE_ROOT_NOT_A_GIT_WORKTREE:" + str(source_root)
        )
    for pin in PINS.values():
        proc = run_git(source_root, "cat-file", "-e", pin.cut + "^{commit}")
        if proc.returncode != 0:
            raise HarnessError(
                "PINNED_COMMIT_MISSING:" + pin.key + ":" + pin.cut
            )


def git_tree_map(source_root: Path, cut: str, base: str) -> dict[str, str]:
    proc = subprocess.run(
        ["git", "ls-tree", "-r", "-z", cut, "--", base],
        cwd=str(source_root),
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise HarnessError(
            "GIT_LS_TREE_FAILED:"
            + cut
            + ":"
            + proc.stderr.decode(errors="replace")
        )
    rows: dict[str, str] = {}
    prefix = base.rstrip("/") + "/"
    for entry in proc.stdout.split(b"\0"):
        if not entry:
            continue
        meta, raw_path = entry.split(b"\t", 1)
        parts = meta.decode().split()
        if len(parts) != 3 or parts[1] != "blob":
            continue
        path = raw_path.decode()
        if not path.startswith(prefix):
            continue
        rows[path[len(prefix):]] = parts[2]
    return rows


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_pin(source_root: Path, pin: Pin, stage: Path) -> None:
    proc = subprocess.run(
        ["git", "archive", "--format=tar", pin.cut, pin.base],
        cwd=str(source_root),
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise HarnessError(
            "GIT_ARCHIVE_FAILED:"
            + pin.key
            + ":"
            + proc.stderr.decode(errors="replace")
        )
    with tarfile.open(fileobj=io.BytesIO(proc.stdout), mode="r:") as archive:
        archive.extractall(stage)


def copy_explicit(source: Path, dest: Path) -> None:
    if not source.is_dir():
        raise HarnessError("EXPLICIT_PIN_NOT_DIRECTORY:" + str(source))
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        source,
        dest,
        ignore=shutil.ignore_patterns(*IGNORE_COPY),
    )


def verify_pin(
    source_root: Path,
    pin: Pin,
    dest: Path,
    *,
    explicit: bool,
) -> dict:
    if not dest.is_dir():
        raise HarnessError("STAGED_PIN_MISSING:" + pin.key + ":" + str(dest))
    expected = git_tree_map(source_root, pin.cut, pin.base)
    rows = []
    errors = []
    for rel in sorted(expected):
        if not rel.endswith(".py"):
            continue
        target = dest / rel
        if not target.is_file():
            errors.append("MISSING:" + rel)
            continue
        actual_blob = git_blob_sha1(target)
        exact = actual_blob == expected[rel]
        rows.append({
            "path": rel,
            "pinned_git_blob_sha1": expected[rel],
            "staged_git_blob_sha1": actual_blob,
            "exact": exact,
            "sha256": sha256_file(target),
        })
        if not exact:
            errors.append("BLOB_MISMATCH:" + rel)
    staged_py = {
        str(path.relative_to(dest))
        for path in dest.rglob("*.py")
        if "__pycache__" not in path.parts
        and (path.is_relative_to(dest / pin.package) or "tests" in path.parts)
    }
    extra = sorted(staged_py - set(expected))
    for rel in extra:
        errors.append("EXTRA_PY:" + rel)
    return {
        "key": pin.key,
        "role": pin.role,
        "cut": pin.cut,
        "base": pin.base,
        "package": pin.package,
        "explicit_source": explicit,
        "files_checked": len(rows),
        "all_exact": not errors,
        "errors": errors,
        "rows": rows,
    }


def verify_m35_vendor(source_root: Path, stage: Path) -> dict:
    root = stage / M35_VENDOR_BASE
    expected = git_tree_map(source_root, M35_CUT, M35_PIN_BASE)
    rows = []
    errors = []
    for target in sorted(root.rglob("*")):
        if not target.is_file() or "__pycache__" in target.parts:
            continue
        rel = str(target.relative_to(root))
        if not rel.endswith(".py"):
            continue
        expected_blob = expected.get(rel, "")
        actual_blob = git_blob_sha1(target)
        exact = bool(expected_blob) and actual_blob == expected_blob
        rows.append({
            "path": rel,
            "pinned_git_blob_sha1": expected_blob,
            "staged_git_blob_sha1": actual_blob,
            "exact": exact,
            "sha256": sha256_file(target),
        })
        if not exact:
            errors.append("M35_VENDOR_MISMATCH:" + rel)
    return {
        "cut": M35_CUT,
        "base": M35_VENDOR_BASE,
        "files_checked": len(rows),
        "all_exact": not errors,
        "errors": errors,
        "rows": rows,
    }


def stage_sources(
    *,
    source_root: Path,
    stage: Path,
    explicit_paths: dict[str, Path],
    refresh: bool = True,
) -> dict:
    require_git(source_root)
    explicit_paths = {
        key: path.resolve() for key, path in explicit_paths.items() if path
    }
    unknown = sorted(set(explicit_paths) - set(PINS))
    if unknown:
        raise HarnessError("UNKNOWN_PIN_KEY:" + ",".join(unknown))
    if refresh and stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    for key in STAGE_ORDER:
        pin = PINS[key]
        dest = stage / pin.base
        explicit = explicit_paths.get(key)
        if explicit is not None:
            if explicit.is_relative_to(stage.resolve()):
                raise HarnessError(
                    "EXPLICIT_PIN_INSIDE_STAGE:" + key + ":" + str(explicit)
                )
            copy_explicit(explicit, dest)
        elif not dest.is_dir():
            extract_pin(source_root, pin, stage)
    rows = {}
    for key in STAGE_ORDER:
        pin = PINS[key]
        rows[key] = verify_pin(
            source_root,
            pin,
            stage / pin.base,
            explicit=key in explicit_paths,
        )
    m35 = verify_m35_vendor(source_root, stage)
    errors = []
    for key, row in rows.items():
        if not row["all_exact"]:
            errors.extend(key + ":" + item for item in row["errors"])
    if not m35["all_exact"]:
        errors.extend(m35["errors"])
    if errors:
        raise HarnessError("PIN_EXACTNESS_FAILED:" + "|".join(errors))
    return {
        "schema": "SOROK_S45_S47_HARNESS_STAGE@1",
        "commission_base": COMMISSION_BASE,
        "stage": str(stage),
        "source_root": str(source_root),
        "explicit_paths": {
            key: str(path) for key, path in sorted(explicit_paths.items())
        },
        "pins": {
            key: {
                "cut": pin.cut,
                "base": pin.base,
                "package": pin.package,
                "role": pin.role,
            }
            for key, pin in PINS.items()
        },
        "pin_rows": rows,
        "m35_vendor": m35,
        "all_exact": True,
    }


def module_origins(stage: Path, names: tuple[str, ...]) -> dict:
    import importlib

    rows = {}
    stage = stage.resolve()
    for name in names:
        try:
            module = importlib.import_module(name)
            path = Path(getattr(module, "__file__", "")).resolve()
            rows[name] = {
                "path": str(path),
                "under_stage": path.is_relative_to(stage),
                "status": "IMPORTED",
            }
        except Exception as exc:
            rows[name] = {
                "path": "",
                "under_stage": False,
                "status": "IMPORT_FAILED",
                "code": type(exc).__name__,
                "detail": str(exc),
            }
    return rows


__all__ = [
    "COMMISSION_BASE",
    "DEFAULT_SOURCE_ROOT",
    "HarnessError",
    "PINS",
    "RETURN",
    "SEAM_FILES",
    "STAGE_ORDER",
    "copy_explicit",
    "extract_pin",
    "git_blob_sha1",
    "git_tree_map",
    "module_origins",
    "require_git",
    "sha256_file",
    "stage_sources",
    "verify_m35_vendor",
    "verify_pin",
]
