#!/usr/bin/env python3
"""Portable evidence/control binding helpers for FIABC source-local split execution.

This module is control-plane only. It never opens a raw survey source, imports a
candidate owner, launches a candidate process, or performs measured P2X work.

The source-local launcher is expected to call:
  * ``baseline`` before measured source-block entry;
  * ``failure`` if the measured driver exits nonzero; and
  * ``closure`` only after a source-local terminal exists.

A post-qualification immutable control binding is deliberately external to the
implementation commit. It binds a qualified implementation head and exact
launcher/driver/merge/helper bytes without self-referential commit hashing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Mapping, Sequence

EXPECTED_EXECUTION_HEAD = "3d8f2ad62600b6777dcb23a28404a067502e77a0"
EXPECTED_EXECUTION_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXPECTED_SOURCES = ("LITS_I", "WVS7")
EXPECTED_CANDIDATES = ("A", "B", "C")
EXPECTED_SOURCE_SHA256 = {
    "LITS_I": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
    "WVS7": "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",
}
EXPECTED_MANIFEST_GIT_BLOB_SHA1 = "49692c1c8527680c97af073039b36125edd7e56d"
LEGACY_WVS_RUN5_CONTROL_HEAD = "4f0ee6bbc7e3387fb1c71837c1ae8bea658f64a2"

CONTROL_BINDING_SCHEMA = "RAWLSING_FIABC_SPLIT_CONTROL_BINDING@1.0.0"
REPO_BASELINE_SCHEMA = "RAWLSING_FIABC_SOURCE_LOCAL_REPO_LIVE_BASELINE@1.0.0"
PORTABLE_CLOSURE_SCHEMA = "RAWLSING_FIABC_SOURCE_LOCAL_PORTABLE_EVIDENCE@1.0.0"
ORCHESTRATION_FAILURE_SCHEMA = "RAWLSING_FIABC_SOURCE_LOCAL_ORCHESTRATION_FAILURE@1.0.0"
CONTROL_COMPATIBILITY_SCHEMA = "RAWLSING_FIABC_SPLIT_CONTROL_COMPATIBILITY@1.0.0"

TERMINAL_SCHEMA = "RAWLSING_FIABC_SOURCE_LOCAL_TERMINAL@1.0.0"
LEDGER_SCHEMA = "RAWLSING_EE_P2X_DARWIN_STAGE_LEDGER@1.0.0"
COMPLETE_LEDGER_DISPOSITIONS = frozenset({
    "PASS",
    "PRESERVED",
    "SKIPPED_BY_FROZEN_LAW",
    "CANDIDATE_LOCAL_FAILURE",
    "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
    "BLOCKED_BY_COMMON_COURT_AUTHORITY",
})
STAGE_CATALOG = (
    "S00_SOURCE_PREFLIGHT_IDENTITY",
    "S01_CANDIDATE_PREPARATION_BUILD",
    "S02_C11_REACHABILITY",
    "S03_PARITY_ORACLE_GATE",
    "S04_I03_EXECUTION",
    "S05_I05_LEARNED_PRODUCTION",
    "S06_PROVENANCE_AUDIT",
    "S07_COLD_RESEARCH",
    "S08_WARM_REPEATED_RESEARCH",
    "S09_DELETION_REGEN_OR_A_PERSISTENCE",
    "S10_SOURCE_RELEASE_INVALIDATION",
    "S11_SEMANTIC_AUTHORITY_INVALIDATION",
    "S12_STALE_CACHE_OR_PERSISTENT_STATE",
    "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE",
    "S14_INTERRUPTION_RECOVERY",
    "S15_FRESH_PROCESS_REPLAY",
    "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
)

LIVE_EVIDENCE_REL = Path("WORKER_RETURNS/EE-P2X/LOCAL_COURT")
CONTROL_PATHS = (
    "HQ_HANDOFF/launchers/RUN_FIABC_SOURCE_LOCAL_SPLIT.sh",
    "HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py",
    "HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_MERGE.py",
    "HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py",
)


class EvidenceClosureError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _git(root: Path, *args: str, check: bool = True, text: bool = True):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )


def _load_json(path: Path, *, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise EvidenceClosureError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(value, Mapping):
        raise EvidenceClosureError(f"{label} must be a mapping: {path}")
    return value


def _identity_checked(
    path: Path,
    *,
    label: str,
    identity_field: str = "receipt_identity",
) -> Mapping[str, Any]:
    doc = _load_json(path, label=label)
    material = {k: v for k, v in doc.items() if k != identity_field}
    observed = _sha256_bytes(_canon(material))
    if doc.get(identity_field) != observed:
        raise EvidenceClosureError(f"{label} identity drift: {path}")
    return doc


def _write_identified_json(
    path: Path,
    payload: Mapping[str, Any],
    *,
    identity_field: str = "receipt_identity",
) -> Mapping[str, Any]:
    out = dict(payload)
    out[identity_field] = _sha256_bytes(_canon(out))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return out


def _resolve_inside(root: Path, relative: str | Path, *, label: str) -> Path:
    root = root.resolve()
    raw = Path(relative)
    if raw.is_absolute():
        raise EvidenceClosureError(f"{label} must be relative: {raw}")
    path = (root / raw).resolve()
    if path != root and root not in path.parents:
        raise EvidenceClosureError(f"{label} escapes bound root: {relative}")
    return path


def _expected_stage_addresses(source: str) -> tuple[str, ...]:
    if source not in EXPECTED_SOURCES:
        raise EvidenceClosureError(f"unknown source: {source}")
    return tuple(
        f"{source}/{candidate}/{stage_id}"
        for candidate in EXPECTED_CANDIDATES
        for stage_id in STAGE_CATALOG
    )


def _manifest_identity_ok(identity: Any) -> bool:
    return (
        isinstance(identity, Mapping)
        and identity.get("schema") == "RAWLSING_FIABC_CURRENT_SIX_CELL_EXECUTION_MANIFEST@1.0.0"
        and identity.get("git_blob_sha1") == EXPECTED_MANIFEST_GIT_BLOB_SHA1
        and isinstance(identity.get("sha256"), str)
        and len(str(identity.get("sha256"))) == 64
    )


def _validate_terminal(doc: Mapping[str, Any], source: str) -> None:
    if doc.get("schema") != TERMINAL_SCHEMA:
        raise EvidenceClosureError(f"{source}: source-local terminal schema drift")
    if doc.get("source") != source:
        raise EvidenceClosureError(f"{source}: terminal source mismatch")
    if doc.get("source_sha256") != EXPECTED_SOURCE_SHA256[source]:
        raise EvidenceClosureError(f"{source}: canonical source SHA mismatch")
    if doc.get("execution_head") != EXPECTED_EXECUTION_HEAD:
        raise EvidenceClosureError(f"{source}: protected execution head drift")
    if tuple(doc.get("candidate_order", ())) != EXPECTED_CANDIDATES:
        raise EvidenceClosureError(f"{source}: candidate inventory/order drift")
    if not _manifest_identity_ok(doc.get("current_execution_manifest")):
        raise EvidenceClosureError(f"{source}: execution-manifest identity drift")
    for key, expected in (
        ("source_local_only", True),
        ("six_cell_s17_executed", False),
        ("six_cell_completion_claimed", False),
        ("measured_synthesis_performed", False),
        ("p2_synthesis_authorized", False),
    ):
        if doc.get(key) is not expected:
            raise EvidenceClosureError(f"{source}: terminal invariant drift: {key}")
    terminals = doc.get("candidate_terminals")
    if not isinstance(terminals, Mapping) or tuple(terminals.keys()) != EXPECTED_CANDIDATES:
        raise EvidenceClosureError(f"{source}: candidate terminal inventory drift")
    if not isinstance(doc.get("common_blockers"), list):
        raise EvidenceClosureError(f"{source}: common blocker inventory malformed")
    if not isinstance(doc.get("incomplete_stages"), list):
        raise EvidenceClosureError(f"{source}: incomplete-stage inventory malformed")


def _load_ledger(work_root: Path) -> tuple[Mapping[str, Any], Path]:
    path = work_root / "ee_p2x_stage_ledger.json"
    if not path.is_file():
        raise EvidenceClosureError(f"stage ledger missing: {path}")
    doc = _load_json(path, label="stage ledger")
    if doc.get("schema") != LEDGER_SCHEMA:
        raise EvidenceClosureError("stage ledger schema drift")
    if not _manifest_identity_ok(doc.get("continuation_map")):
        raise EvidenceClosureError("stage ledger manifest identity drift")
    if tuple(doc.get("source_order", ())) != EXPECTED_SOURCES:
        raise EvidenceClosureError("stage ledger source order drift")
    if tuple(doc.get("candidate_order", ())) != EXPECTED_CANDIDATES:
        raise EvidenceClosureError("stage ledger candidate order drift")
    if doc.get("p2x_branch") != EXPECTED_EXECUTION_BRANCH:
        raise EvidenceClosureError("stage ledger protected branch drift")
    return doc, path


def _stage_receipt_index(
    work_root: Path,
    source: str,
    ledger: Mapping[str, Any],
    terminal: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    stages = ledger.get("stages")
    if not isinstance(stages, Mapping):
        raise EvidenceClosureError("stage ledger stages mapping missing")
    expected = set(_expected_stage_addresses(source))
    observed = set(stages)
    foreign = sorted(observed - expected)
    if foreign:
        raise EvidenceClosureError(
            f"{source}: ledger contains non-selected-source/foreign stages: {foreign[:5]}"
        )

    missing = sorted(expected - observed)
    declared_incomplete = sorted(str(x) for x in terminal.get("incomplete_stages", ()))
    allow_missing = terminal.get("status") == "BLOCKED__COMMON_COURT_AUTHORITY"
    if missing and (not allow_missing or missing != declared_incomplete):
        raise EvidenceClosureError(
            f"{source}: incomplete ledger stages incoherent with terminal: "
            f"missing={missing} declared={declared_incomplete}"
        )
    if not missing and declared_incomplete:
        raise EvidenceClosureError(
            f"{source}: terminal declares incomplete stages but ledger is complete"
        )

    receipt_index: list[dict[str, Any]] = []
    repo_artifacts: dict[str, dict[str, Any]] = {}
    blocker_addresses: list[str] = []
    failure_cells: set[str] = set()

    for address in sorted(observed):
        entry = stages[address]
        if not isinstance(entry, Mapping):
            raise EvidenceClosureError(f"{source}: malformed ledger entry: {address}")
        if entry.get("state") == "RUNNING":
            raise EvidenceClosureError(f"{source}: RUNNING stage remains: {address}")
        disposition = entry.get("terminal_disposition")
        if disposition not in COMPLETE_LEDGER_DISPOSITIONS:
            raise EvidenceClosureError(f"{source}: nonterminal ledger entry: {address}")
        if entry.get("state") != "TERMINAL" or entry.get("verifier_completion") is not True:
            raise EvidenceClosureError(
                f"{source}: terminal ledger mechanics invalid: {address}"
            )
        receipt_rel = entry.get("receipt_path")
        receipt_hash = entry.get("receipt_hash")
        if not isinstance(receipt_rel, str) or not isinstance(receipt_hash, str):
            raise EvidenceClosureError(f"{source}: stage receipt binding missing: {address}")
        receipt_path = _resolve_inside(work_root, receipt_rel, label=f"{address} receipt")
        if not receipt_path.is_file() or _sha256_file(receipt_path) != receipt_hash:
            raise EvidenceClosureError(f"{source}: stage receipt hash drift: {address}")
        receipt_index.append({
            "address": address,
            "terminal_disposition": disposition,
            "receipt_path": receipt_rel,
            "receipt_sha256": receipt_hash,
        })
        if disposition in {
            "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
            "BLOCKED_BY_COMMON_COURT_AUTHORITY",
        }:
            blocker_addresses.append(address)
        if disposition == "CANDIDATE_LOCAL_FAILURE":
            failure_cells.add("/".join(address.split("/")[:2]))

        artifacts = entry.get("output_artifact_hashes", {})
        if not isinstance(artifacts, Mapping):
            raise EvidenceClosureError(
                f"{source}: output artifact mapping malformed: {address}"
            )
        for locator, expected_hash in artifacts.items():
            if not isinstance(locator, str) or not isinstance(expected_hash, str):
                raise EvidenceClosureError(
                    f"{source}: malformed artifact binding: {address}"
                )
            if locator.startswith("work:"):
                rel = locator[5:]
                p = _resolve_inside(work_root, rel, label=f"{address} work artifact")
                if not p.is_file() or _sha256_file(p) != expected_hash:
                    raise EvidenceClosureError(
                        f"{source}: work artifact hash drift: {locator}"
                    )
            elif locator.startswith("repo:"):
                rel = locator[5:]
                path = Path(rel)
                try:
                    path.relative_to(LIVE_EVIDENCE_REL)
                except ValueError as exc:
                    raise EvidenceClosureError(
                        f"{source}: repo artifact escapes admitted live-evidence "
                        f"namespace: {locator}"
                    ) from exc
                prior = repo_artifacts.get(rel)
                current = {
                    "repo_relative_path": rel,
                    "sha256": expected_hash,
                    "stages": [],
                }
                if prior is not None and prior["sha256"] != expected_hash:
                    raise EvidenceClosureError(
                        f"{source}: same repo artifact bound to conflicting hashes: {rel}"
                    )
                if prior is None:
                    repo_artifacts[rel] = current
                    prior = current
                prior["stages"].append(address)
            else:
                raise EvidenceClosureError(
                    f"{source}: unbound artifact locator: {locator}"
                )

    terminal_blockers = sorted(str(x) for x in terminal.get("common_blockers", ()))
    if sorted(blocker_addresses) != terminal_blockers:
        raise EvidenceClosureError(
            f"{source}: blocker inventory disagrees with ledger"
        )
    terminal_failures = sorted(
        str(x) for x in terminal.get("candidate_failure_cells", ())
    )
    if sorted(failure_cells) != terminal_failures:
        raise EvidenceClosureError(
            f"{source}: candidate failure inventory disagrees with ledger"
        )

    candidate_terminals = terminal["candidate_terminals"]
    stages_map = ledger["stages"]
    for candidate in EXPECTED_CANDIDATES:
        terminal_address = f"{source}/{candidate}/{STAGE_CATALOG[-1]}"
        stated = candidate_terminals[candidate]
        if not isinstance(stated, Mapping) or stated.get("address") != terminal_address:
            raise EvidenceClosureError(
                f"{source}/{candidate}: terminal address drift"
            )
        entry = stages_map.get(terminal_address)
        if entry is None:
            if (
                terminal.get("status") != "BLOCKED__COMMON_COURT_AUTHORITY"
                or stated.get("terminal_disposition")
                != "INCOMPLETE_DUE_COMMON_COURT_BLOCKER"
                or terminal_address not in missing
            ):
                raise EvidenceClosureError(
                    f"{source}/{candidate}: absent terminal not explained by "
                    "common-court blocker"
                )
        else:
            if stated.get("terminal_disposition") != entry.get("terminal_disposition"):
                raise EvidenceClosureError(
                    f"{source}/{candidate}: terminal disposition disagrees with ledger"
                )
            if stated.get("receipt_hash") != entry.get("receipt_hash"):
                raise EvidenceClosureError(
                    f"{source}/{candidate}: terminal receipt hash disagrees with ledger"
                )

    return receipt_index, [repo_artifacts[k] for k in sorted(repo_artifacts)]


def _tracked_head_inventory(repo_root: Path) -> dict[str, str]:
    proc = _git(
        repo_root,
        "ls-files",
        "-z",
        "--",
        LIVE_EVIDENCE_REL.as_posix(),
        text=False,
    )
    raw = proc.stdout
    if not isinstance(raw, (bytes, bytearray)):
        raw = bytes(raw)
    out: dict[str, str] = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        rel = item.decode("utf-8")
        show = _git(repo_root, "show", f"HEAD:{rel}", text=False)
        body = show.stdout
        if not isinstance(body, (bytes, bytearray)):
            body = bytes(body)
        out[rel] = _sha256_bytes(bytes(body))
    return out


def _worktree_live_inventory(repo_root: Path) -> dict[str, str]:
    root = repo_root / LIVE_EVIDENCE_REL
    if not root.exists():
        return {}
    if root.is_symlink():
        raise EvidenceClosureError(
            "repo-live evidence namespace may not be a symlink"
        )
    out: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise EvidenceClosureError(
                f"repo-live evidence contains symlink: {path}"
            )
        if path.is_file():
            rel = path.relative_to(repo_root).as_posix()
            out[rel] = _sha256_file(path)
    return out


def capture_repo_live_baseline(
    *,
    repo_root: Path,
    source: str,
    output_path: Path,
) -> Mapping[str, Any]:
    repo_root = repo_root.resolve()
    if source not in EXPECTED_SOURCES:
        raise EvidenceClosureError(f"unknown source: {source}")
    head = _git(
        repo_root, "rev-parse", "--verify", "HEAD^{commit}"
    ).stdout.strip()
    branch = _git(repo_root, "branch", "--show-current").stdout.strip()
    if head != EXPECTED_EXECUTION_HEAD or branch != EXPECTED_EXECUTION_BRANCH:
        raise EvidenceClosureError(
            "repo-live baseline must bind exact protected execution checkout"
        )

    tracked = _tracked_head_inventory(repo_root)
    worktree = _worktree_live_inventory(repo_root)
    drift = sorted(
        rel for rel, expected in tracked.items()
        if worktree.get(rel) != expected
    )
    untracked = sorted(set(worktree) - set(tracked))
    if drift or untracked:
        raise EvidenceClosureError(
            "pre-run repo-live evidence namespace is not at exact HEAD baseline: "
            f"tracked_drift={drift} untracked={untracked}"
        )
    payload = {
        "schema": REPO_BASELINE_SCHEMA,
        "status": "PASS__EXACT_HEAD_LIVE_EVIDENCE_BASELINE",
        "source": source,
        "execution_branch": branch,
        "execution_head": head,
        "live_evidence_root": LIVE_EVIDENCE_REL.as_posix(),
        "tracked_head_inventory": dict(sorted(tracked.items())),
        "worktree_inventory": dict(sorted(worktree.items())),
        "nonselected_source_mutations_present": False,
        "raw_source_access_performed": False,
        "candidate_processes_started": 0,
        "measured_execution_performed": False,
    }
    return _write_identified_json(output_path, payload)


def _verify_baseline(path: Path, source: str) -> Mapping[str, Any]:
    doc = _identity_checked(path, label="repo-live evidence baseline")
    if doc.get("schema") != REPO_BASELINE_SCHEMA or doc.get("source") != source:
        raise EvidenceClosureError("repo-live baseline schema/source drift")
    if doc.get("execution_head") != EXPECTED_EXECUTION_HEAD:
        raise EvidenceClosureError("repo-live baseline protected head drift")
    if doc.get("live_evidence_root") != LIVE_EVIDENCE_REL.as_posix():
        raise EvidenceClosureError("repo-live baseline root drift")
    if not isinstance(doc.get("worktree_inventory"), Mapping):
        raise EvidenceClosureError("repo-live baseline inventory malformed")
    return doc


def create_control_binding(
    *,
    control_root: Path,
    qualified_implementation_head: str,
    output_path: Path,
    qualification_return_ref: str,
) -> Mapping[str, Any]:
    control_root = control_root.resolve()
    if len(qualified_implementation_head) != 40:
        raise EvidenceClosureError(
            "qualified implementation head must be a full 40-hex commit"
        )
    if _git(
        control_root,
        "cat-file",
        "-e",
        f"{qualified_implementation_head}^{{commit}}",
        check=False,
    ).returncode:
        raise EvidenceClosureError(
            "qualified implementation commit is unavailable"
        )

    files: dict[str, str] = {}
    for rel in CONTROL_PATHS:
        proc = _git(
            control_root,
            "show",
            f"{qualified_implementation_head}:{rel}",
            text=False,
            check=False,
        )
        if proc.returncode:
            raise EvidenceClosureError(
                f"qualified implementation lacks required control file: {rel}"
            )
        body = proc.stdout
        if not isinstance(body, (bytes, bytearray)):
            body = bytes(body)
        files[rel] = _sha256_bytes(bytes(body))

    qualified_branch = _git(
        control_root, "branch", "--show-current"
    ).stdout.strip()
    if not qualified_branch:
        raise EvidenceClosureError(
            "qualified control checkout must be on a named branch"
        )
    payload = {
        "schema": CONTROL_BINDING_SCHEMA,
        "status": "QUALIFIED_SOURCE_FREE_CONTROL_IMPLEMENTATION",
        "qualified_control_branch": qualified_branch,
        "qualified_implementation_head": qualified_implementation_head,
        "protected_execution_head": EXPECTED_EXECUTION_HEAD,
        "qualification_return_ref": qualification_return_ref,
        "bound_files": files,
        "binding_design": (
            "POST_QUALIFICATION_EXTERNAL_RECEIPT__QUALIFIED_HEAD_PLUS_EXACT_FILE_HASHES"
        ),
        "self_referential_commit_hash_required": False,
    }
    return _write_identified_json(output_path, payload)


def verify_control_binding(
    *,
    binding_path: Path,
    control_root: Path,
    require_clean: bool = True,
) -> Mapping[str, Any]:
    control_root = control_root.resolve()
    doc = _identity_checked(binding_path, label="control binding")
    if doc.get("schema") != CONTROL_BINDING_SCHEMA:
        raise EvidenceClosureError("control binding schema drift")
    if doc.get("status") != "QUALIFIED_SOURCE_FREE_CONTROL_IMPLEMENTATION":
        raise EvidenceClosureError("control binding is not qualified")
    if doc.get("protected_execution_head") != EXPECTED_EXECUTION_HEAD:
        raise EvidenceClosureError(
            "control binding protected execution drift"
        )
    qualified = doc.get("qualified_implementation_head")
    if not isinstance(qualified, str) or len(qualified) != 40:
        raise EvidenceClosureError(
            "control binding qualified head malformed"
        )
    if _git(
        control_root,
        "cat-file",
        "-e",
        f"{qualified}^{{commit}}",
        check=False,
    ).returncode:
        raise EvidenceClosureError(
            "qualified control implementation commit unavailable"
        )
    expected_branch = doc.get("qualified_control_branch")
    observed_branch = _git(
        control_root, "branch", "--show-current"
    ).stdout.strip()
    if not isinstance(expected_branch, str) or not expected_branch:
        raise EvidenceClosureError(
            "control binding qualified branch malformed"
        )
    if observed_branch != expected_branch:
        raise EvidenceClosureError(
            f"wrong control branch: expected {expected_branch}, got {observed_branch}"
        )

    bound = doc.get("bound_files")
    if not isinstance(bound, Mapping):
        raise EvidenceClosureError(
            "control binding file inventory malformed"
        )
    if set(CONTROL_PATHS) - set(bound):
        raise EvidenceClosureError(
            "control binding omits required launcher/driver/merge/helper"
        )
    observed: dict[str, str] = {}
    for rel in CONTROL_PATHS:
        path = _resolve_inside(
            control_root, rel, label="bound control file"
        )
        if not path.is_file():
            raise EvidenceClosureError(
                f"bound control file missing: {rel}"
            )
        observed[rel] = _sha256_file(path)
        if observed[rel] != bound.get(rel):
            raise EvidenceClosureError(
                f"bound control file hash drift: {rel}"
            )

    if require_clean:
        dirty = _git(
            control_root,
            "status",
            "--porcelain",
            "--untracked-files=all",
        ).stdout.strip()
        if dirty:
            raise EvidenceClosureError("control checkout is dirty")

    current_head = _git(
        control_root, "rev-parse", "--verify", "HEAD^{commit}"
    ).stdout.strip()
    return {
        "binding_receipt_sha256": _sha256_file(binding_path),
        "binding_receipt_identity": doc.get("receipt_identity"),
        "qualified_control_branch": expected_branch,
        "qualified_implementation_head": qualified,
        "observed_control_checkout_head": current_head,
        "protected_execution_head": EXPECTED_EXECUTION_HEAD,
        "bound_files": dict(sorted(observed.items())),
        "control_checkout_clean": True if require_clean else None,
    }


def _portable_repo_copy_path(
    portable_root: Path, repo_rel: str
) -> Path:
    return _resolve_inside(
        portable_root,
        Path("repo_live_evidence") / repo_rel,
        label="portable repo-live copy",
    )


def build_portable_evidence_closure(
    *,
    work_root: Path,
    repo_root: Path,
    source: str,
    baseline_path: Path,
    control_root: Path,
    control_binding_path: Path,
    output_path: Path | None = None,
    allow_legacy_terminal_control: bool = False,
) -> Mapping[str, Any]:
    work_root = work_root.resolve()
    repo_root = repo_root.resolve()
    if source not in EXPECTED_SOURCES:
        raise EvidenceClosureError(f"unknown source: {source}")

    terminal_path = work_root / "court" / "source_local_terminal.json"
    terminal = _identity_checked(
        terminal_path, label="source-local terminal"
    )
    _validate_terminal(terminal, source)

    ledger, ledger_path = _load_ledger(work_root)
    ledger_sha = _sha256_file(ledger_path)
    if terminal.get("stage_ledger_sha256") != ledger_sha:
        raise EvidenceClosureError(
            f"{source}: terminal stage-ledger hash drift"
        )
    if terminal.get("current_execution_manifest") != ledger.get(
        "continuation_map"
    ):
        raise EvidenceClosureError(
            f"{source}: terminal/ledger manifest identity mismatch"
        )

    source_identities = ledger.get("source_identities")
    if not isinstance(source_identities, Mapping):
        raise EvidenceClosureError(
            "stage ledger source identities malformed"
        )
    if set(source_identities) != {source}:
        raise EvidenceClosureError(
            f"{source}: ledger source identities are not source-local: "
            f"{sorted(source_identities)}"
        )
    source_identity = source_identities[source]
    if (
        not isinstance(source_identity, Mapping)
        or source_identity.get("sha256") != EXPECTED_SOURCE_SHA256[source]
    ):
        raise EvidenceClosureError(
            f"{source}: ledger canonical source identity drift"
        )

    stage_receipts, repo_artifacts = _stage_receipt_index(
        work_root, source, ledger, terminal
    )
    baseline = _verify_baseline(baseline_path, source)
    baseline_inventory = dict(baseline["worktree_inventory"])
    current_inventory = _worktree_live_inventory(repo_root)

    changed = sorted(
        rel
        for rel in set(baseline_inventory) | set(current_inventory)
        if baseline_inventory.get(rel) != current_inventory.get(rel)
    )
    deleted = [rel for rel in changed if rel not in current_inventory]
    if deleted:
        raise EvidenceClosureError(
            f"{source}: repo-live evidence was deleted and cannot be "
            f"packaged: {deleted}"
        )

    ledger_repo_paths = {
        item["repo_relative_path"] for item in repo_artifacts
    }
    unbound_mutations = sorted(set(changed) - ledger_repo_paths)
    if unbound_mutations:
        raise EvidenceClosureError(
            f"{source}: repo-live mutation is not attributable to "
            f"selected-source ledger: {unbound_mutations}"
        )

    portable_root = work_root / "court" / "portable_evidence"
    portable_root.mkdir(parents=True, exist_ok=True)
    repo_copies: list[dict[str, Any]] = []
    for item in repo_artifacts:
        rel = item["repo_relative_path"]
        source_path = _resolve_inside(
            repo_root, rel, label="repo-live evidence artifact"
        )
        if not source_path.is_file():
            raise EvidenceClosureError(
                f"{source}: repo-live evidence missing: {rel}"
            )
        observed = _sha256_file(source_path)
        if observed != item["sha256"]:
            raise EvidenceClosureError(
                f"{source}: repo-live evidence hash drift: {rel}"
            )
        copy_path = _portable_repo_copy_path(portable_root, rel)
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, copy_path)
        copied_hash = _sha256_file(copy_path)
        if copied_hash != observed:
            raise EvidenceClosureError(
                f"{source}: portable repo-live copy hash drift: {rel}"
            )
        repo_copies.append({
            **item,
            "baseline_sha256": baseline_inventory.get(rel),
            "change_type": (
                "CREATED"
                if rel not in baseline_inventory
                else "MODIFIED"
                if baseline_inventory[rel] != observed
                else "UNCHANGED_LEDGER_REFERENCED"
            ),
            "portable_path": str(copy_path.relative_to(work_root)),
            "portable_sha256": copied_hash,
        })

    binding = verify_control_binding(
        binding_path=control_binding_path,
        control_root=control_root,
        require_clean=True,
    )
    terminal_control = terminal.get("control_runner")
    if not isinstance(terminal_control, Mapping):
        raise EvidenceClosureError(
            f"{source}: terminal control-runner identity missing"
        )
    terminal_control_head = terminal_control.get("control_head")
    if not allow_legacy_terminal_control:
        if (
            terminal_control_head
            != binding["qualified_implementation_head"]
        ):
            raise EvidenceClosureError(
                f"{source}: terminal control head is not the qualified "
                "implementation head"
            )
        if (
            terminal_control.get("launcher_sha256")
            != binding["bound_files"][CONTROL_PATHS[0]]
        ):
            raise EvidenceClosureError(
                f"{source}: launcher hash not qualified"
            )
        if (
            terminal_control.get("source_local_driver_sha256")
            != binding["bound_files"][CONTROL_PATHS[1]]
        ):
            raise EvidenceClosureError(
                f"{source}: source-local driver hash not qualified"
            )

    binding_copy = portable_root / "control_binding.json"
    shutil.copyfile(control_binding_path, binding_copy)
    if (
        _sha256_file(binding_copy)
        != binding["binding_receipt_sha256"]
    ):
        raise EvidenceClosureError(
            "portable control-binding copy hash drift"
        )

    baseline_copy = portable_root / "repo_live_baseline.json"
    shutil.copyfile(baseline_path, baseline_copy)
    if _sha256_file(baseline_copy) != _sha256_file(baseline_path):
        raise EvidenceClosureError(
            "portable baseline copy hash drift"
        )

    changed_set = set(changed)
    included_changed = {
        item["repo_relative_path"]
        for item in repo_copies
        if item["repo_relative_path"] in changed_set
    }
    if included_changed != changed_set:
        raise EvidenceClosureError(
            f"{source}: portable repo-live delta is incomplete"
        )

    payload = {
        "schema": PORTABLE_CLOSURE_SCHEMA,
        "status": "PASS__PORTABLE_SOURCE_LOCAL_EVIDENCE_CLOSED",
        "source": source,
        "source_sha256": EXPECTED_SOURCE_SHA256[source],
        "execution_branch": EXPECTED_EXECUTION_BRANCH,
        "execution_head": EXPECTED_EXECUTION_HEAD,
        "current_execution_manifest": terminal[
            "current_execution_manifest"
        ],
        "candidate_order": list(EXPECTED_CANDIDATES),
        "source_terminal": {
            "path": str(terminal_path.relative_to(work_root)),
            "sha256": _sha256_file(terminal_path),
            "receipt_identity": terminal["receipt_identity"],
            "status": terminal["status"],
        },
        "stage_ledger": {
            "path": str(ledger_path.relative_to(work_root)),
            "sha256": ledger_sha,
            "stage_count": len(ledger["stages"]),
        },
        "stage_receipts": stage_receipts,
        "repo_live_baseline": {
            "path": str(baseline_copy.relative_to(work_root)),
            "sha256": _sha256_file(baseline_copy),
            "receipt_identity": baseline["receipt_identity"],
        },
        "repo_live_evidence": repo_copies,
        "repo_live_delta_paths": changed,
        "all_repo_live_mutations_attributable_to_selected_source_ledger": True,
        "nonselected_source_evidence_included": False,
        "control_binding": {
            **binding,
            "portable_path": str(binding_copy.relative_to(work_root)),
            "portable_sha256": _sha256_file(binding_copy),
        },
        "terminal_control_head": terminal_control_head,
        "terminal_control_legacy_allowed_for_packaging": bool(
            allow_legacy_terminal_control
        ),
        "host": terminal.get("host"),
        "source_local_only": True,
        "six_cell_s17_executed": False,
        "six_cell_completion_claimed": False,
        "measured_synthesis_performed": False,
        "p2_synthesis_authorized": False,
        "portable_packaging_performed_after_source_terminal": True,
        "portable_packaging_is_measured_candidate_work": False,
        "raw_source_bytes_copied": False,
    }
    if output_path is None:
        output_path = (
            work_root
            / "court"
            / "portable_source_evidence_closure.json"
        )
    return _write_identified_json(output_path, payload)


def write_orchestration_failure_receipt(
    *,
    work_root: Path,
    source: str,
    measured_driver_exit_code: int,
    control_root: Path,
    control_binding_path: Path,
    output_path: Path | None = None,
) -> Mapping[str, Any]:
    work_root = work_root.resolve()
    if source not in EXPECTED_SOURCES:
        raise EvidenceClosureError(f"unknown source: {source}")
    if measured_driver_exit_code == 0:
        raise EvidenceClosureError(
            "orchestration-failure receipt requires nonzero driver exit"
        )

    ledger_path = work_root / "ee_p2x_stage_ledger.json"
    ledger_hash: str | None = None
    candidate_entries: list[str] = []
    last_address: str | None = None
    if ledger_path.is_file():
        ledger_doc = _load_json(
            ledger_path, label="partial stage ledger"
        )
        stages = ledger_doc.get("stages")
        if isinstance(stages, Mapping):
            candidate_entries = [
                str(address)
                for address in stages
                if str(address).startswith(f"{source}/")
            ]
            if candidate_entries:
                last_address = candidate_entries[-1]
        ledger_hash = _sha256_file(ledger_path)

    progress_path = work_root / "fiabc_driver_progress.jsonl"
    terminal_path = (
        work_root / "court" / "source_local_terminal.json"
    )
    preflight_path = (
        work_root / "court" / "source_local_preflight.json"
    )
    runtime = None
    if preflight_path.is_file():
        preflight = _load_json(
            preflight_path, label="source-local preflight"
        )
        runtime = preflight.get("host")

    binding = verify_control_binding(
        binding_path=control_binding_path,
        control_root=control_root,
        require_clean=True,
    )
    payload = {
        "schema": ORCHESTRATION_FAILURE_SCHEMA,
        "status": (
            "STOPPED__NONZERO_MEASURED_DRIVER_EXIT__NO_AUTOMATIC_RETRY"
        ),
        "classification": (
            "CONTROL_OR_ORCHESTRATION_FAILURE__NOT_CANDIDATE_LOCAL_FAILURE"
        ),
        "source": source,
        "selected_source_sha256": EXPECTED_SOURCE_SHA256[source],
        "execution_branch": EXPECTED_EXECUTION_BRANCH,
        "execution_head": EXPECTED_EXECUTION_HEAD,
        "qualified_control_identity": binding,
        "runtime": runtime,
        "measured_driver_exit_code": int(measured_driver_exit_code),
        "candidate_stage_ledger_entry_exists": bool(candidate_entries),
        "candidate_stage_ledger_entries": candidate_entries,
        "last_terminal_or_partial_stage_address": last_address,
        "stage_ledger_present": ledger_path.is_file(),
        "stage_ledger_sha256": ledger_hash,
        "progress_jsonl_present": progress_path.is_file(),
        "progress_jsonl_sha256": (
            _sha256_file(progress_path)
            if progress_path.is_file()
            else None
        ),
        "source_local_terminal_present": terminal_path.is_file(),
        "source_local_terminal_sha256": (
            _sha256_file(terminal_path)
            if terminal_path.is_file()
            else None
        ),
        "PRESERVE_WORK_ROOT": str(work_root),
        "automatic_retry_authorized": False,
        "retry_requires_hq_adjudication": True,
        "candidate_failure_inferred_from_process_exit": False,
        "six_cell_s17_executed": False,
        "p2_synthesis_authorized": False,
    }
    if output_path is None:
        output_path = (
            work_root
            / "court"
            / "source_local_orchestration_failure.json"
        )
    return _write_identified_json(output_path, payload)


def validate_control_compatibility_receipt(
    *,
    path: Path,
    lits_qualified_head: str,
    wvs_qualified_head: str,
    wvs_terminal_control_head: str | None,
) -> Mapping[str, Any]:
    doc = _identity_checked(
        path, label="control compatibility receipt"
    )
    if doc.get("schema") != CONTROL_COMPATIBILITY_SCHEMA:
        raise EvidenceClosureError(
            "control compatibility receipt schema drift"
        )
    if (
        doc.get("status")
        != "PASS__EXPLICIT_CONTROL_COMPATIBILITY_ADJUDICATED"
    ):
        raise EvidenceClosureError(
            "control compatibility receipt is not PASS"
        )
    if (
        doc.get("LITS_I_qualified_control_head")
        != lits_qualified_head
    ):
        raise EvidenceClosureError(
            "compatibility receipt LiTS qualified head drift"
        )
    if doc.get("WVS7_qualified_control_head") != wvs_qualified_head:
        raise EvidenceClosureError(
            "compatibility receipt WVS qualified head drift"
        )
    if (
        doc.get("WVS7_terminal_control_head")
        != wvs_terminal_control_head
    ):
        raise EvidenceClosureError(
            "compatibility receipt WVS terminal control head drift"
        )
    if doc.get("candidate_execution_semantics_unchanged") is not True:
        raise EvidenceClosureError(
            "compatibility receipt lacks candidate-semantic equivalence"
        )
    if doc.get("portable_evidence_reverified") is not True:
        raise EvidenceClosureError(
            "compatibility receipt lacks portable evidence reverification"
        )
    if (
        doc.get("physical_metric_admissibility_explicitly_adjudicated")
        is not True
    ):
        raise EvidenceClosureError(
            "compatibility receipt omits physical-metric adjudication"
        )
    if doc.get("silent_grandfathering") is not False:
        raise EvidenceClosureError(
            "compatibility receipt permits silent grandfathering"
        )
    return doc


def legacy_wvs_run5_framework(
    *,
    wvs_root: Path,
    current_binding_path: Path,
    output_path: Path,
) -> Mapping[str, Any]:
    """Produce a non-adjudicative framework for WVS RUN5 conservation."""
    wvs_root = wvs_root.resolve()
    terminal_path = (
        wvs_root / "court" / "source_local_terminal.json"
    )
    terminal_present = terminal_path.is_file()
    terminal_control_head = None
    terminal_sha = None
    if terminal_present:
        terminal = _identity_checked(
            terminal_path, label="legacy WVS terminal"
        )
        if terminal.get("source") != "WVS7":
            raise EvidenceClosureError(
                "legacy WVS framework root is not WVS7"
            )
        terminal_control = terminal.get("control_runner")
        if isinstance(terminal_control, Mapping):
            terminal_control_head = terminal_control.get(
                "control_head"
            )
        terminal_sha = _sha256_file(terminal_path)

    binding = _identity_checked(
        current_binding_path, label="current control binding"
    )
    payload = {
        "schema": (
            "RAWLSING_FIABC_WVS_RUN5_COMPATIBILITY_FRAMEWORK@1.0.0"
        ),
        "status": (
            "HOLD__EXPLICIT_COMPATIBILITY_ADJUDICATION_REQUIRED"
        ),
        "source": "WVS7",
        "legacy_expected_control_head": LEGACY_WVS_RUN5_CONTROL_HEAD,
        "observed_terminal_control_head": terminal_control_head,
        "terminal_present": terminal_present,
        "terminal_sha256": terminal_sha,
        "current_qualified_control_head": binding.get(
            "qualified_implementation_head"
        ),
        "required_findings": [
            "NO_REPAIRED_DEFECT_ENCOUNTERED_BY_LEGACY_WVS_EXECUTION",
            "NO_SPLIT_ONLY_PRESTATE_COST_CONTAMINATED_GOVERNED_PHYSICAL_VECTOR",
            "WVS_C_S00_PLACEMENT_LAWFULLY_ADJUDICATED",
            "ALL_REPO_LOCAL_ARTIFACTS_AVAILABLE_AND_HASH_BINDABLE",
            "PORTABLE_EVIDENCE_REVERIFIED_WITHOUT_MEASURED_MUTATION",
            "CANDIDATE_EXECUTION_SEMANTICS_UNCHANGED_ACROSS_CONTROL_HEADS",
            "PHYSICAL_METRIC_ADMISSIBILITY_EXPLICITLY_ADJUDICATED",
        ],
        "automatic_grandfathering_allowed": False,
        "rerun_automatically_required": False,
        "next_action": (
            "HQ_ISSUE_EXPLICIT_CONTROL_COMPATIBILITY_RECEIPT_OR_VOID_LEGACY_METRICS"
        ),
    }
    return _write_identified_json(output_path, payload)


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    baseline = sub.add_parser("baseline")
    baseline.add_argument(
        "--source", choices=EXPECTED_SOURCES, required=True
    )
    baseline.add_argument("--repo-root", type=Path, required=True)
    baseline.add_argument("--output", type=Path, required=True)

    bind = sub.add_parser("seal-control-binding")
    bind.add_argument("--control-root", type=Path, required=True)
    bind.add_argument(
        "--qualified-implementation-head", required=True
    )
    bind.add_argument(
        "--qualification-return-ref", required=True
    )
    bind.add_argument("--output", type=Path, required=True)

    closure = sub.add_parser("closure")
    closure.add_argument(
        "--source", choices=EXPECTED_SOURCES, required=True
    )
    closure.add_argument("--work-root", type=Path, required=True)
    closure.add_argument("--repo-root", type=Path, required=True)
    closure.add_argument("--baseline", type=Path, required=True)
    closure.add_argument("--control-root", type=Path, required=True)
    closure.add_argument(
        "--control-binding", type=Path, required=True
    )
    closure.add_argument("--output", type=Path)
    closure.add_argument(
        "--allow-legacy-terminal-control", action="store_true"
    )

    failure = sub.add_parser("failure")
    failure.add_argument(
        "--source", choices=EXPECTED_SOURCES, required=True
    )
    failure.add_argument("--work-root", type=Path, required=True)
    failure.add_argument("--exit-code", type=int, required=True)
    failure.add_argument("--control-root", type=Path, required=True)
    failure.add_argument(
        "--control-binding", type=Path, required=True
    )
    failure.add_argument("--output", type=Path)

    legacy = sub.add_parser("wvs-run5-framework")
    legacy.add_argument("--wvs-root", type=Path, required=True)
    legacy.add_argument(
        "--current-control-binding", type=Path, required=True
    )
    legacy.add_argument("--output", type=Path, required=True)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "baseline":
        result = capture_repo_live_baseline(
            repo_root=args.repo_root,
            source=args.source,
            output_path=args.output,
        )
    elif args.command == "seal-control-binding":
        result = create_control_binding(
            control_root=args.control_root,
            qualified_implementation_head=(
                args.qualified_implementation_head
            ),
            output_path=args.output,
            qualification_return_ref=args.qualification_return_ref,
        )
    elif args.command == "closure":
        result = build_portable_evidence_closure(
            work_root=args.work_root,
            repo_root=args.repo_root,
            source=args.source,
            baseline_path=args.baseline,
            control_root=args.control_root,
            control_binding_path=args.control_binding,
            output_path=args.output,
            allow_legacy_terminal_control=(
                args.allow_legacy_terminal_control
            ),
        )
    elif args.command == "failure":
        result = write_orchestration_failure_receipt(
            work_root=args.work_root,
            source=args.source,
            measured_driver_exit_code=args.exit_code,
            control_root=args.control_root,
            control_binding_path=args.control_binding,
            output_path=args.output,
        )
    elif args.command == "wvs-run5-framework":
        result = legacy_wvs_run5_framework(
            wvs_root=args.wvs_root,
            current_binding_path=args.current_control_binding,
            output_path=args.output,
        )
    else:
        raise AssertionError(args.command)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
