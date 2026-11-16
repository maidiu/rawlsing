#!/usr/bin/env python3
"""SOROK live operational-currentness intake (R1).

The frozen 27-packet projection and its exact-pin validator remain the static
snapshot.  This module adds the missing live layer: it observes declared GitHub
refs, consumes only explicitly committed receipts, and writes a visible
CURRENTNESS_HOLD with exact missing evidence when a relevant ref moved without
reconciliation.  Issue comments, review comments, owner decisions and local
runner tables are not observable through git; the projection says so and needs
an explicit receipt for each.

Authentication model: receipt and evidence content hashes are frozen in the
paired JSON.  This proves exact content integrity, not reviewer cryptography.
No sourcefree event is promoted to native/protected by this module.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol

ROOT = Path(__file__).resolve().parents[3]
SOROK = ROOT / "SOROK_PRODUCT_CONTROL_ROOM"
PROGRESS = SOROK / "CURRENT_PROGRESS.json"
MARKDOWN = SOROK / "CURRENT_PROGRESS.md"
STATIC_VALIDATOR = SOROK / "PROGRAMMA_SOROK" / "verify_operational_currentness_r1.py"
BASE = SOROK / "PROGRAMMA_SOROK" / "CURRENTNESS_LIVE_R1"
RECEIPTS = BASE / "receipts"
BOOTSTRAP = BASE / "bootstrap.json"
STATIC_KEY = "operational_currentness_r1"
LIVE_KEY = "operational_currentness_live_r1"
SCHEMA = "SOROK_OPERATIONAL_CURRENTNESS_LIVE@1"
RECEIPT_SCHEMA = "SOROK_CURRENTNESS_RECEIPT@1"
START = "<!-- SOROK_CURRENTNESS_LIVE_START -->"
END = "<!-- SOROK_CURRENTNESS_LIVE_END -->"
SCOPED_GRADES = {
    "ACCEPT_SCOPED_SOURCEFREE",
    "ACCEPT_SCOPED_SOURCEFREE_ENGINEERING",
    "ACCEPT_SCOPED_EXPERIMENT",
    "ACCEPT_SCOPED_DOC_BENCHMARK",
}
PROTECTED_GRADES = {"PROTECTED_SOURCEFREE_MERGE"}
EVENT_KINDS = {
    "ACCEPTED_CODE", "PROTECTED_MERGE", "INDEPENDENT_REVIEW",
    "OWNER_DECISION", "ACCEPTED_RETURN",
}


class CurrentnessError(ValueError):
    pass


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_sha40(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(ch in "0123456789abcdef" for ch in value)
    )


def is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CurrentnessError(f"cannot read exact JSON {path}: {exc}") from exc


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        try:
            os.unlink(name)
        except FileNotFoundError:
            pass


def load_static_validator():
    spec = importlib.util.spec_from_file_location(
        "sorok_frozen_currentness_validator", STATIC_VALIDATOR,
    )
    if spec is None or spec.loader is None:
        raise CurrentnessError("cannot load frozen SOROK validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Observer(Protocol):
    def heads(self) -> Mapping[str, str]: ...
    def ref(self, refname: str) -> str | None: ...
    def is_ancestor(self, ancestor: str, descendant: str) -> bool: ...
    def merge_parents(self, sha: str) -> tuple[str, ...]: ...


class GitRefObserver:
    def __init__(self, root: Path = ROOT) -> None:
        self.root = root

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                ["git", *args], cwd=self.root, text=True,
                capture_output=True, timeout=60, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise CurrentnessError(f"git unavailable: {exc}") from exc

    def heads(self) -> Mapping[str, str]:
        proc = self._git("ls-remote", "--heads", "origin")
        if proc.returncode != 0:
            raise CurrentnessError("live discovery failed: " + proc.stderr.strip())
        result: dict[str, str] = {}
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) != 2:
                raise CurrentnessError("malformed git ls-remote output")
            sha, ref = parts
            if not is_sha40(sha) or not ref.startswith("refs/heads/"):
                raise CurrentnessError("malformed git ls-remote identity")
            result[ref] = sha
        return result

    def ref(self, refname: str) -> str | None:
        proc = self._git("ls-remote", "--exit-code", "origin", refname)
        if proc.returncode == 2:
            return None
        if proc.returncode != 0:
            raise CurrentnessError(
                f"live discovery failed for {refname}: {proc.stderr.strip()}"
            )
        matches = []
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1] == refname:
                matches.append(parts[0])
        if len(matches) != 1 or not is_sha40(matches[0]):
            raise CurrentnessError(f"cannot uniquely resolve {refname}")
        return matches[0]

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        proc = self._git("merge-base", "--is-ancestor", ancestor, descendant)
        if proc.returncode not in (0, 1):
            raise CurrentnessError("cannot verify ancestry: " + proc.stderr.strip())
        return proc.returncode == 0

    def merge_parents(self, sha: str) -> tuple[str, ...]:
        proc = self._git("show", "-s", "--format=%P", sha)
        if proc.returncode != 0:
            raise CurrentnessError(
                f"cannot read merge parents for {sha}: {proc.stderr.strip()}"
            )
        return tuple(proc.stdout.strip().split())


@dataclass(frozen=True)
class CheckResult:
    live: Mapping[str, Any]
    observed: Mapping[str, str]
    holds: tuple[str, ...]
    mode: str
    status: str

    @property
    def ok(self) -> bool:
        return not self.holds


def load_receipt(path: Path) -> dict[str, Any]:
    data = _read_json(path)
    if not isinstance(data, dict):
        raise CurrentnessError(f"receipt is not an object: {path}")
    required = (
        "schema", "receipt_id", "event_kind", "event_ref", "event_sha",
        "grade", "scope", "owner", "accepted_at", "reviewer", "evidence",
        "attestation",
    )
    missing = [key for key in required if key not in data]
    if missing:
        raise CurrentnessError(
            f"receipt {path.name} lacks exact fields: {', '.join(missing)}"
        )
    if data["schema"] != RECEIPT_SCHEMA:
        raise CurrentnessError(f"receipt {path.name} has wrong schema")
    if data["event_kind"] not in EVENT_KINDS:
        raise CurrentnessError(f"receipt {path.name} has unknown event kind")
    if not is_sha40(data["event_sha"]):
        raise CurrentnessError(f"receipt {path.name} has invalid event SHA")
    if not isinstance(data["event_ref"], str) or not data["event_ref"].startswith("refs/"):
        raise CurrentnessError(f"receipt {path.name} has invalid event ref")
    if not isinstance(data["scope"], str) or not data["scope"].startswith("SOURCEFREE"):
        raise CurrentnessError(f"receipt {path.name} exceeds sourcefree scope ceiling")
    if not isinstance(data["evidence"], list) or not data["evidence"]:
        raise CurrentnessError(f"receipt {path.name} has no evidence")
    for entry in data["evidence"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise CurrentnessError(f"receipt {path.name} has malformed evidence")
        if not is_sha256(entry.get("sha256")):
            raise CurrentnessError(f"receipt {path.name} has malformed evidence hash")
    return data


def receipt_sha256(receipt: Mapping[str, Any]) -> str:
    return sha256_text(canonical(receipt))


def validate_evidence(receipt: Mapping[str, Any], evidence_root: Path) -> None:
    root = evidence_root.resolve()
    for entry in receipt["evidence"]:
        path = (root / entry["path"]).resolve()
        if not path.is_relative_to(root):
            raise CurrentnessError(
                f"receipt {receipt['receipt_id']} evidence escapes root"
            )
        if not path.is_file():
            raise CurrentnessError(
                f"receipt {receipt['receipt_id']} missing evidence {entry['path']}"
            )
        if sha256_file(path) != entry["sha256"]:
            raise CurrentnessError(
                f"receipt {receipt['receipt_id']} evidence drift {entry['path']}"
            )


class CurrentnessEngine:
    def __init__(
        self,
        *,
        progress_path: Path = PROGRESS,
        markdown_path: Path = MARKDOWN,
        receipts_dir: Path = RECEIPTS,
        evidence_root: Path = ROOT,
        observer: Observer | None = None,
        clock: Callable[[], str] = now_utc,
        static_module: Any | None = None,
    ) -> None:
        self.progress_path = progress_path
        self.markdown_path = markdown_path
        self.receipts_dir = receipts_dir
        self.evidence_root = evidence_root
        self.observer = observer or GitRefObserver()
        self.clock = clock
        self.static = static_module or load_static_validator()

    # ---------------------------------------------------------------- storage
    def load_root(self) -> dict[str, Any]:
        root = _read_json(self.progress_path)
        if not isinstance(root, dict):
            raise CurrentnessError("CURRENT_PROGRESS.json is not an object")
        return root

    def load_static(self, root: Mapping[str, Any] | None = None) -> dict[str, Any]:
        root = root if root is not None else self.load_root()
        state = root.get(STATIC_KEY)
        if not isinstance(state, dict):
            raise CurrentnessError("frozen SOROK currentness state is absent")
        return state

    def load_live(self, root: Mapping[str, Any] | None = None) -> dict[str, Any]:
        root = root if root is not None else self.load_root()
        state = root.get(LIVE_KEY)
        if not isinstance(state, dict):
            raise CurrentnessError("live SOROK currentness state is absent")
        return state

    def historical_root_hash(self, root: Mapping[str, Any]) -> str:
        historical = {key: value for key, value in root.items() if key != LIVE_KEY}
        return sha256_text(canonical(historical))

    @staticmethod
    def split_markdown(markdown: str) -> tuple[str, str]:
        if markdown.count(START) == 0 and markdown.count(END) == 0:
            return "", markdown
        if markdown.count(START) != 1 or markdown.count(END) != 1:
            raise CurrentnessError("paired Markdown live markers are duplicated")
        start = markdown.index(START)
        end = markdown.index(END) + len(END)
        if start != 0:
            raise CurrentnessError("paired Markdown live block is not first")
        suffix = markdown[end:]
        if not suffix.startswith("\n\n"):
            raise CurrentnessError("paired Markdown live separator drifted")
        return markdown[start:end], suffix[2:]

    @staticmethod
    def render_live_block(live: Mapping[str, Any]) -> str:
        last = live.get("last_check") or {}
        accepted = live.get("accepted_events") or []
        lines = [
            START,
            "## SOROK operational currentness — live intake (R1)",
            (
                f"**Checked:** {last.get('at')} | **Mode:** {last.get('mode')} | "
                f"**Status:** {last.get('status')}"
            ),
            (
                "**Static frozen snapshot:** validated below; exact static "
                f"state SHA-256 `{live.get('static_snapshot_sha256')}`. "
                "Static history is not a live event feed."
            ),
            (
                "**Protected baseline:** "
                f"`{live['protected']['branch']}` @ "
                f"`{live['protected']['head_at_read']}`; protected rev "
                f"{live['protected']['progress_revision']}."
            ),
            "**Static scoped accepted, unmerged:** B05 (#1089), C04 (#1062), C05 (#1091).",
            (
                "**Freshness:** PASS is current only within "
                f"{live.get('freshness_max_age_hours', 24)}h of Checked; "
                "run --check to refresh."
            ),
        ]
        if accepted:
            for event in accepted:
                lines.append(
                    f"**Live accepted event `{event['id']}`:** "
                    f"`{event['event_sha']}` — {event['grade']}; "
                    f"{event['integration']}; scope `{event['scope']}`."
                )
        else:
            lines.append("**Live accepted events:** none reconciled.")
        holds = last.get("holds") or []
        if holds:
            lines.append("**CURRENTNESS_HOLD:**")
            lines.extend(f"- {hold}" for hold in holds)
        else:
            lines.append("**CURRENTNESS_HOLD:** none.")
        streams = live.get("unverified_streams") or []
        lines.append(
            "**Unverified live streams:** " + "; ".join(streams)
            if streams else "**Unverified live streams:** none declared."
        )
        lines.append(
            "**Next owner action:** "
            + (live.get("next_owner_action") or "reconcile exact missing receipt")
        )
        lines.append(END)
        return "\n".join(lines)

    def write_state(self, root: dict[str, Any], live: dict[str, Any]) -> None:
        markdown = self.markdown_path.read_text(encoding="utf-8")
        _block, original = self.split_markdown(markdown)
        if sha256_text(original) != live["historical_md_sha256"]:
            raise CurrentnessError("refusing to overwrite drifted historical Markdown")
        if len(original) != live["historical_md_length"]:
            raise CurrentnessError("refusing to overwrite drifted historical Markdown")
        if self.historical_root_hash(root) != live["historical_root_sha256"]:
            raise CurrentnessError("refusing to overwrite drifted historical JSON")
        new_root = {LIVE_KEY: live}
        new_root.update({key: value for key, value in root.items() if key != LIVE_KEY})
        _atomic_write(
            self.progress_path,
            json.dumps(new_root, indent=2, ensure_ascii=False) + "\n",
        )
        _atomic_write(
            self.markdown_path,
            self.render_live_block(live) + "\n\n" + original,
        )

    # ------------------------------------------------------------------ static
    def static_holds(
        self, root: Mapping[str, Any], live: Mapping[str, Any], *, offline: bool = False,
    ) -> list[str]:
        holds: list[str] = []
        if live.get("schema") != SCHEMA:
            holds.append("STATIC_LIVE_SCHEMA_DRIFT")
        if live.get("static_key") != STATIC_KEY:
            holds.append("STATIC_KEY_DRIFT")
        try:
            static_state = self.load_static(root)
        except CurrentnessError as exc:
            holds.append(f"STATIC_STATE_MISSING: {exc}")
            return holds
        errors = self.static.validate(static_state, git=not offline)
        holds.extend("STATIC_FROZEN: " + error for error in errors)
        if sha256_text(canonical(static_state)) != live.get("static_snapshot_sha256"):
            holds.append("STATIC_SNAPSHOT_DRIFT")
        if self.historical_root_hash(root) != live.get("historical_root_sha256"):
            holds.append("HISTORICAL_JSON_DRIFT")
        try:
            markdown = self.markdown_path.read_text(encoding="utf-8")
            _live_block, original = self.split_markdown(markdown)
            if sha256_text(original) != live.get("historical_md_sha256"):
                holds.append("HISTORICAL_MD_DRIFT")
            if len(original) != live.get("historical_md_length"):
                holds.append("HISTORICAL_MD_DRIFT")
            if START in markdown and END in markdown:
                start = markdown.index(START)
                end = markdown.index(END) + len(END)
                if markdown[start:end] != self.render_live_block(live):
                    holds.append("PAIRED_LIVE_MD_DRIFT")
            starts = markdown.count("<!-- SOROK_OPERATIONAL_CURRENT_START -->")
            ends = markdown.count("<!-- SOROK_OPERATIONAL_CURRENT_END -->")
            if starts != 1 or ends != 1:
                holds.append("STATIC_PAIRED_MD_MARKERS_MISSING")
            else:
                sm = "<!-- SOROK_OPERATIONAL_CURRENT_START -->"
                em = "<!-- SOROK_OPERATIONAL_CURRENT_END -->"
                if markdown[markdown.index(sm):markdown.index(em) + len(em)] != self.static.render(static_state):
                    holds.append("STATIC_PAIRED_MD_DRIFT")
        except (OSError, CurrentnessError, KeyError, TypeError) as exc:
            holds.append(f"STATIC_MD_ERROR: {exc}")
        for event in live.get("accepted_events", []):
            try:
                self._validate_event_receipt(event)
            except CurrentnessError as exc:
                holds.append(f"RECEIPT_INVALID {event.get('id')}: {exc}")
        return holds

    def _validate_event_receipt(self, event: Mapping[str, Any]) -> None:
        path = self.receipts_dir / event["receipt"]
        receipt = load_receipt(path)
        validate_evidence(receipt, self.evidence_root)
        digest = receipt_sha256(receipt)
        if digest != event.get("receipt_sha256"):
            raise CurrentnessError(f"receipt hash drift for {event['id']}")
        for key in ("event_kind", "event_ref", "event_sha", "grade", "scope"):
            if receipt.get(key) != event.get(key):
                raise CurrentnessError(
                    f"receipt/event field drift for {event['id']}: {key}"
                )

    # -------------------------------------------------------------------- live
    def relevant_observed(
        self, live: Mapping[str, Any], heads: Mapping[str, str],
    ) -> dict[str, str]:
        prefixes = tuple(live["watch"]["branch_prefixes"])
        protected_ref = "refs/heads/" + live["watch"]["protected_branch"]
        observed: dict[str, str] = {}
        for ref, sha in heads.items():
            name = ref.removeprefix("refs/heads/")
            if ref == protected_ref or any(name.startswith(p) for p in prefixes):
                observed[ref] = sha
        for ref in live.get("baseline_refs", {}):
            if ref in heads:
                observed.setdefault(ref, heads[ref])
        for ref in live["watch"].get("pr_refs", []):
            value = self.observer.ref(ref)
            if value is None:
                continue
            observed[ref] = value
        return observed

    def live_holds(
        self, live: Mapping[str, Any], observed: Mapping[str, str],
    ) -> list[str]:
        holds: set[str] = set()
        protected_ref = "refs/heads/" + live["watch"]["protected_branch"]
        protected_head = live["protected"]["head_at_read"]
        if protected_ref not in observed:
            holds.add(f"PROTECTED_REF_MISSING {protected_ref}")
        elif observed[protected_ref] != protected_head:
            merge = next(
                (
                    event for event in live.get("accepted_events", [])
                    if event.get("event_kind") == "PROTECTED_MERGE"
                    and (
                        event.get("event_sha") == observed[protected_ref]
                        or self.observer.is_ancestor(
                            event.get("event_sha"), observed[protected_ref]
                        )
                    )
                ),
                None,
            )
            if merge is None:
                holds.add(
                    "PROTECTED_HEAD_DRIFT "
                    f"{protected_head} -> {observed[protected_ref]}; "
                    "required: explicit PROTECTED_MERGE receipt"
                )
        accepted_by_ref = {
            event.get("event_ref"): event
            for event in live.get("accepted_events", [])
            if event.get("event_kind") == "ACCEPTED_CODE"
        }
        baseline = live.get("baseline_refs", {})
        for ref, sha in observed.items():
            if ref == protected_ref:
                continue
            event = accepted_by_ref.get(ref)
            if event is not None and event.get("event_sha") == sha:
                continue
            if baseline.get(ref, {}).get("sha") == sha:
                continue
            holds.add(
                "MISSING_RECEIPT "
                f"{ref}@{sha}; required: explicit receipt with exact "
                "event_ref/event_sha, sourcefree scoped grade, scope and evidence"
            )
        for event in live.get("accepted_events", []):
            if event.get("event_kind") != "ACCEPTED_CODE":
                continue
            ref = event.get("event_ref")
            current = observed.get(ref)
            if current is None:
                holds.add(
                    f"MISSING_ACCEPTED_REF {ref}; required: restore or "
                    "supersede with an explicit receipt"
                )
            elif current != event.get("event_sha"):
                holds.add(
                    "REF_DRIFT "
                    f"{ref} {event.get('event_sha')} -> {current}; "
                    "required: new explicit receipt"
                )
        for ref in baseline:
            if ref not in observed:
                holds.add(
                    f"BASELINE_REF_MISSING {ref}; required: deletion/supersession receipt"
                )
        return sorted(holds)

    def check(
        self, *, write: bool = False, offline: bool = False,
    ) -> CheckResult:
        root = self.load_root()
        live = copy.deepcopy(self.load_live(root))
        holds = self.static_holds(root, live, offline=offline)
        observed: dict[str, str] = {}
        mode = "OFFLINE" if offline else "LIVE"
        if offline:
            status = "OFFLINE_NOT_CURRENT" if not holds else "STATIC_HOLD"
        else:
            try:
                heads = dict(self.observer.heads())
                observed = self.relevant_observed(live, heads)
                holds.extend(self.live_holds(live, observed))
            except CurrentnessError as exc:
                holds.append(f"LIVE_DISCOVERY_FAILED: {exc}")
            status = "PASS" if not holds else "CURRENTNESS_HOLD"
        live["last_check"] = {
            "mode": mode, "status": status, "at": self.clock(),
            "observed": dict(sorted(observed.items())),
            "holds": sorted(holds),
        }
        if write and not offline:
            try:
                self.write_state(root, live)
            except CurrentnessError as exc:
                holds.append(f"PAIRED_WRITE_REFUSED: {exc}")
                live["last_check"]["holds"] = sorted(holds)
                live["last_check"]["status"] = "CURRENTNESS_HOLD"
                status = "CURRENTNESS_HOLD"
        return CheckResult(
            live=live, observed=dict(sorted(observed.items())),
            holds=tuple(sorted(holds)), mode=mode, status=status,
        )

    def _freshness_holds(self, live: Mapping[str, Any]) -> list[str]:
        last = live.get("last_check") or {}
        at = last.get("at")
        if not at:
            return ["CHECK_NOT_RUN"]
        try:
            then = datetime.fromisoformat(at)
        except ValueError:
            return ["CHECK_TIMESTAMP_INVALID"]
        max_age = float(live.get("freshness_max_age_hours", 24))
        age = (datetime.now(timezone.utc) - then).total_seconds() / 3600.0
        if age > max_age:
            return [
                "CHECK_STALE "
                f"last check {at} is {age:.1f}h old; max {max_age:g}h; run --check"
            ]
        return []

    def status(self) -> CheckResult:
        root = self.load_root()
        live = self.load_live(root)
        last = live.get("last_check") or {}
        holds = tuple(sorted(
            set(last.get("holds", ())) | set(self._freshness_holds(live))
        ))
        return CheckResult(
            live=live, observed=last.get("observed", {}),
            holds=holds,
            mode=last.get("mode", "NOT_CHECKED"),
            status=last.get("status", "NOT_CHECKED"),
        )

    def discover(self) -> CheckResult:
        root = self.load_root()
        live = self.load_live(root)
        holds = self.static_holds(root, live)
        try:
            heads = dict(self.observer.heads())
            observed = self.relevant_observed(live, heads)
            holds.extend(self.live_holds(live, observed))
        except CurrentnessError as exc:
            observed = {}
            holds.append(f"LIVE_DISCOVERY_FAILED: {exc}")
        return CheckResult(
            live=live, observed=observed, holds=tuple(sorted(holds)),
            mode="DISCOVER", status="PASS" if not holds else "CURRENTNESS_HOLD",
        )

    # --------------------------------------------------------------- bootstrap
    def init(self, bootstrap_path: Path = BOOTSTRAP, *, force: bool = False) -> dict[str, Any]:
        root = self.load_root()
        if LIVE_KEY in root and not force:
            raise CurrentnessError("live currentness state already exists")
        static_state = self.load_static(root)
        errors = self.static.validate(static_state, git=True)
        if errors:
            raise CurrentnessError(
                "cannot initialize over invalid frozen snapshot: " + "; ".join(errors)
            )
        bootstrap = _read_json(bootstrap_path)
        markdown = self.markdown_path.read_text(encoding="utf-8")
        _block, original = self.split_markdown(markdown)
        live: dict[str, Any] = {
            "schema": SCHEMA,
            "as_of": bootstrap["as_of"],
            "adoption": "PENDING_INDEPENDENT_RECEIVING",
            "static_key": STATIC_KEY,
            "static_snapshot_sha256": sha256_text(canonical(static_state)),
            "protected": copy.deepcopy(bootstrap["protected"]),
            "watch": copy.deepcopy(bootstrap["watch"]),
            "baseline_refs": copy.deepcopy(bootstrap["baseline_refs"]),
            "accepted_events": [],
            "history": [],
            "freshness_max_age_hours": bootstrap.get("freshness_max_age_hours", 24),
            "unverified_streams": list(bootstrap["unverified_streams"]),
            "next_owner_action": bootstrap["next_owner_action"],
            "historical_root_sha256": self.historical_root_hash(root),
            "historical_md_sha256": sha256_text(original),
            "historical_md_length": len(original),
            "last_check": {
                "mode": "NOT_CHECKED", "status": "NOT_CHECKED",
                "at": None, "observed": {}, "holds": [],
            },
        }
        for ref, fact in live["baseline_refs"].items():
            if not ref.startswith("refs/") or not is_sha40(fact.get("sha")):
                raise CurrentnessError(f"invalid baseline ref {ref}")
        self.write_state(root, live)
        return live

    # --------------------------------------------------------------- reconcile
    def reconcile(self, receipt_path: Path, *, write: bool = True) -> CheckResult:
        root = self.load_root()
        live = copy.deepcopy(self.load_live(root))
        receipt = load_receipt(receipt_path)
        validate_evidence(receipt, self.evidence_root)
        try:
            receipt_name = receipt_path.resolve().relative_to(
                self.receipts_dir.resolve()
            ).as_posix()
        except ValueError as exc:
            raise CurrentnessError(
                "RECEIPT_OUTSIDE_INBOX: submit the receipt into "
                f"{self.receipts_dir}"
            ) from exc
        kind = receipt["event_kind"]
        if kind == "ACCEPTED_CODE":
            observed = self.observer.ref(receipt["event_ref"])
            if observed != receipt["event_sha"]:
                raise CurrentnessError(
                    "RECEIPT_EVENT_MISMATCH "
                    f"{receipt['event_ref']} observed {observed} != "
                    f"receipt {receipt['event_sha']}"
                )
            if receipt["grade"] not in SCOPED_GRADES:
                raise CurrentnessError(
                    f"GRADE_CEILING_VIOLATION {receipt['grade']}"
                )
            event = {
                "id": receipt.get("event_id", receipt["receipt_id"]),
                "event_kind": kind,
                "event_ref": receipt["event_ref"],
                "event_sha": receipt["event_sha"],
                "grade": receipt["grade"],
                "scope": receipt["scope"],
                "integration": "UNMERGED_SCOPED_ACCEPTED",
                "owner": receipt["owner"],
                "need": receipt.get("need", "PROTECTED_RECEIVING_DECISION"),
                "receipt": receipt_name,
                "receipt_sha256": receipt_sha256(receipt),
                "reviewer": receipt["reviewer"],
                "accepted_at": receipt["accepted_at"],
            }
        elif kind == "PROTECTED_MERGE":
            protected_ref = "refs/heads/" + live["watch"]["protected_branch"]
            observed = self.observer.ref(protected_ref)
            if observed != receipt["event_sha"]:
                raise CurrentnessError(
                    "PROTECTED_MERGE_NOT_CURRENT_HEAD "
                    f"{observed} != {receipt['event_sha']}"
                )
            pr_head = receipt.get("pr_head_sha")
            if not is_sha40(pr_head) or pr_head not in self.observer.merge_parents(observed):
                raise CurrentnessError("PROTECTED_MERGE_PARENT_DRIFT")
            if receipt["grade"] not in PROTECTED_GRADES:
                raise CurrentnessError(
                    f"GRADE_CEILING_VIOLATION {receipt['grade']}"
                )
            event = {
                "id": receipt.get("event_id", receipt["receipt_id"]),
                "event_kind": kind,
                "event_ref": protected_ref,
                "event_sha": observed,
                "grade": receipt["grade"],
                "scope": receipt["scope"],
                "integration": "PROTECTED_HISTORICAL",
                "owner": receipt["owner"],
                "need": "NONE",
                "receipt": receipt_name,
                "receipt_sha256": receipt_sha256(receipt),
                "reviewer": receipt["reviewer"],
                "accepted_at": receipt["accepted_at"],
            }
            live["protected"]["head_at_read"] = observed
            live["protected"]["progress_revision"] = receipt["progress_revision"]
        else:
            raise CurrentnessError(
                f"receipt kind {kind} requires a typed target event; not auto-promoted"
            )
        for old in list(live.get("accepted_events", [])):
            if old.get("id") == event["id"]:
                live["accepted_events"].remove(old)
                live["history"].append({
                    "at": self.clock(), "action": "REPLACED",
                    "event_id": old["id"], "event_ref": old.get("event_ref"),
                    "event_sha": old.get("event_sha"), "by": event["id"],
                })
            elif (
                kind == "ACCEPTED_CODE"
                and old.get("event_kind") == "ACCEPTED_CODE"
                and old.get("event_ref") == event["event_ref"]
            ):
                live["accepted_events"].remove(old)
                live["history"].append({
                    "at": self.clock(), "action": "SUPERSEDED",
                    "event_id": old["id"], "event_ref": old.get("event_ref"),
                    "event_sha": old.get("event_sha"), "by": event["id"],
                })
        live.setdefault("accepted_events", []).append(event)
        live["accepted_events"].sort(key=lambda item: item["id"])
        live["history"].append({
            "at": self.clock(), "action": "RECONCILED",
            "event_id": event["id"], "event_ref": event["event_ref"],
            "event_sha": event["event_sha"],
            "receipt_sha256": event["receipt_sha256"],
        })
        live["last_reconciled_at"] = self.clock()
        if write:
            self.write_state(root, live)
        return self.check(write=write)


def _print_result(result: CheckResult) -> None:
    print(CurrentnessEngine.render_live_block(result.live))
    if result.holds:
        for hold in result.holds:
            print("CURRENTNESS_HOLD: " + hold, file=sys.stderr)
    else:
        print("SOROK_LIVE_CURRENTNESS_PASS: no unreconciled relevant event")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--reconcile", type=Path)
    parser.add_argument("--init", nargs="?", const=BOOTSTRAP, type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    engine = CurrentnessEngine()
    try:
        if args.init is not None:
            live = engine.init(args.init, force=args.force)
            print(f"INITIALIZED {len(live['baseline_refs'])} live baseline refs")
            return 0
        if args.reconcile is not None:
            result = engine.reconcile(args.reconcile, write=not args.no_write)
            _print_result(result)
            return 0 if result.ok else 1
        if args.discover:
            result = engine.discover()
            for ref, sha in result.observed.items():
                print(f"OBSERVED {ref} {sha}")
            _print_result(result)
            return 0 if result.ok else 1
        if args.status:
            result = engine.status()
            print(CurrentnessEngine.render_live_block(result.live))
            for hold in result.holds:
                print("CURRENTNESS_HOLD: " + hold, file=sys.stderr)
            return 0 if not result.holds else 1
        result = engine.check(write=not args.no_write, offline=args.offline)
        print(CurrentnessEngine.render_live_block(result.live))
        if result.holds:
            for hold in result.holds:
                print("CURRENTNESS_HOLD: " + hold, file=sys.stderr)
            return 1
        print("SOROK_LIVE_CURRENTNESS_PASS: no unreconciled relevant event")
        return 0
    except CurrentnessError as exc:
        print("CURRENTNESS_HOLD: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
