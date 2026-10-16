"""Repository-native completion certification and notification for Rawlsing workers.

Operational infrastructure only. This module does not alter Rawlsing empirical,
semantic, authority, PRE-V3, V3, V2, campaign, adoption, or project-current law.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Sequence

MANIFEST_SCHEMA = "RABOCHII_RETURN_MANIFEST@1.0.0"
MANIFEST_PATH = ".rabochii/return_manifest.json"
DEFAULT_INBOX_ISSUE = 304

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_TERMINAL_RE = re.compile(r"^[A-Z0-9][A-Z0-9_]*__RETURN_TO_[A-Z0-9][A-Z0-9_]*$")
_RESULT_VALUES = frozenset({"PASS", "FAIL", "BLOCKED"})
_EVIDENCE_CONCLUSIONS = frozenset({"success", "failure"})
_REQUIRED_COMPLETION_FLAGS = (
    "commission_consumed",
    "all_required_outputs_durable",
    "no_required_work_remaining",
    "no_background_work_remaining",
    "return_packet_durable",
    "terminal_state_entered",
)
_REQUIRED_SEPARATION_FLAGS = (
    "performed_only_commissioned_role",
    "no_uncommissioned_repair",
    "no_uncommissioned_review",
)
_LEGACY_TERMINAL_RE = re.compile(
    r"\b([A-Z0-9][A-Z0-9_]*__RETURN_TO_[A-Z0-9][A-Z0-9_]*)\b"
)
_LEGACY_RUN_RE = re.compile(r"(?:run|Run)\s*:?\s*`?([0-9]{6,})`?")
_LEGACY_RESULT_RE = re.compile(
    r"\b(PASS|FAIL|BLOCKED)(?:__[A-Z0-9_]+)?\b", re.IGNORECASE
)


@dataclass(frozen=True)
class Certification:
    branch: str
    tip_sha: str
    task_id: str
    result: str
    terminal: str
    return_packet_path: str
    evidence_run_id: int | None
    mode: str


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA_RE.fullmatch(value))


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_manifest_shape(
    manifest: Mapping[str, Any],
    *,
    branch: str,
) -> tuple[str, ...]:
    """Validate self-contained completion claims before repository cross-checks."""
    errors: list[str] = []

    if manifest.get("schema_id") != MANIFEST_SCHEMA:
        errors.append(f"schema_id must be {MANIFEST_SCHEMA}")
    if manifest.get("branch") != branch:
        errors.append("branch must exactly match the branch being certified")
    if not _nonempty_string(manifest.get("task_id")):
        errors.append("task_id must be a nonempty string")

    commission = manifest.get("commission")
    if not isinstance(commission, Mapping):
        errors.append("commission must be an object")
        commission = {}
    if not _is_sha(commission.get("authority_ref")):
        errors.append("commission.authority_ref must be a lowercase 40-hex SHA")
    if not _is_sha(commission.get("exact_start_sha")):
        errors.append("commission.exact_start_sha must be a lowercase 40-hex SHA")

    returned = manifest.get("return")
    if not isinstance(returned, Mapping):
        errors.append("return must be an object")
        returned = {}
    result = returned.get("result")
    if result not in _RESULT_VALUES:
        errors.append("return.result must be PASS, FAIL, or BLOCKED")
    terminal = returned.get("terminal")
    if not isinstance(terminal, str) or not _TERMINAL_RE.fullmatch(terminal):
        errors.append("return.terminal must be an exact ...__RETURN_TO_... terminal")
    if returned.get("phase") != "CLOSURE_ONLY":
        errors.append("return.phase must be CLOSURE_ONLY")

    completion = returned.get("completion")
    if not isinstance(completion, Mapping):
        errors.append("return.completion must be an object")
        completion = {}
    for key in _REQUIRED_COMPLETION_FLAGS:
        if completion.get(key) is not True:
            errors.append(f"return.completion.{key} must be true")

    separation = manifest.get("separation")
    if not isinstance(separation, Mapping):
        errors.append("separation must be an object")
        separation = {}
    for key in _REQUIRED_SEPARATION_FLAGS:
        if separation.get(key) is not True:
            errors.append(f"separation.{key} must be true")

    packet = manifest.get("return_packet")
    if not isinstance(packet, Mapping):
        errors.append("return_packet must be an object")
        packet = {}
    if not _nonempty_string(packet.get("path")):
        errors.append("return_packet.path must be nonempty")
    if not _is_sha(packet.get("blob_sha")):
        errors.append("return_packet.blob_sha must be a lowercase 40-hex Git blob SHA")

    outputs = manifest.get("required_outputs")
    if not isinstance(outputs, list) or not outputs:
        errors.append("required_outputs must be a nonempty list")
        outputs = []
    names: set[str] = set()
    for index, output in enumerate(outputs):
        if not isinstance(output, Mapping):
            errors.append(f"required_outputs[{index}] must be an object")
            continue
        name = output.get("name")
        if not _nonempty_string(name):
            errors.append(f"required_outputs[{index}].name must be nonempty")
        elif name in names:
            errors.append(f"duplicate required output name {name}")
        else:
            names.add(name)
        kind = output.get("kind")
        if kind not in {"path", "commit"}:
            errors.append(f"required_outputs[{index}].kind must be path or commit")
        if kind == "path":
            if not _nonempty_string(output.get("path")):
                errors.append(f"required_outputs[{index}].path must be nonempty")
            if not _is_sha(output.get("blob_sha")):
                errors.append(f"required_outputs[{index}].blob_sha must be a 40-hex Git blob SHA")
        if kind == "commit" and not _is_sha(output.get("sha")):
            errors.append(f"required_outputs[{index}].sha must be a 40-hex commit SHA")
        if output.get("status") != "DURABLE":
            errors.append(f"required_outputs[{index}].status must be DURABLE")

    evidence = manifest.get("evidence")
    if not isinstance(evidence, Mapping):
        errors.append("evidence must be an object")
        evidence = {}
    required = evidence.get("required")
    if not isinstance(required, bool):
        errors.append("evidence.required must be boolean")
    elif required:
        run_id = evidence.get("workflow_run_id")
        if not isinstance(run_id, int) or run_id <= 0:
            errors.append("evidence.workflow_run_id must be a positive integer")
        if evidence.get("conclusion") not in _EVIDENCE_CONCLUSIONS:
            errors.append("evidence.conclusion must be success or failure")
        if not _is_sha(evidence.get("evidence_execution_sha")):
            errors.append("evidence.evidence_execution_sha must be a lowercase 40-hex SHA")
        if not _nonempty_string(evidence.get("workflow_name")):
            errors.append("evidence.workflow_name must be nonempty")

    return tuple(errors)


def certify_legacy_return_text(
    text: str,
    *,
    branch: str,
    tip_sha: str,
) -> Certification | None:
    """Strict compatibility mode for pre-manifest workers already in flight."""
    if not branch.startswith("agent/") or not _is_sha(tip_sha):
        return None
    upper = text.upper()
    if "CLOSURE_ONLY" not in upper:
        return None
    if "INCOMPLETE" in upper or "NOT COMPLETE" in upper:
        return None
    terminal_match = _LEGACY_TERMINAL_RE.search(upper)
    if terminal_match is None:
        return None
    if not any(
        token in upper
        for token in (
            "NO SELF-REVIEW",
            "SELF_REVIEW_PERFORMED = NO",
            "REPAIR_PERFORMED_BY_REVIEWER = NO",
            "INDEPENDENT_REVIEW_PERFORMED_BY",
            "NO REPAIR",
            "NO SECOND REVIEW",
        )
    ):
        return None
    result_match = _LEGACY_RESULT_RE.search(upper)
    if result_match is None:
        return None
    run_match = _LEGACY_RUN_RE.search(text)
    run_id = int(run_match.group(1)) if run_match else None
    return Certification(
        branch=branch,
        tip_sha=tip_sha,
        task_id="LEGACY_RETURN",
        result=result_match.group(1).upper(),
        terminal=terminal_match.group(1),
        return_packet_path="legacy-return-markdown",
        evidence_run_id=run_id,
        mode="LEGACY_STRICT",
    )


class GitHubClient:
    def __init__(self, repo: str, token: str) -> None:
        if "/" not in repo:
            raise ValueError("repo must be owner/name")
        self.repo = repo
        self.token = token

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: Mapping[str, Any] | None = None,
        accept: str = "application/vnd.github+json",
    ) -> Any:
        url = f"https://api.github.com{path}"
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Accept", accept)
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "rawlsing-return-beacon")
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise FileNotFoundError(path) from exc
            detail = exc.read().decode("utf-8", "replace")
            raise RuntimeError(f"GitHub API {method} {path} failed: {exc.code} {detail}") from exc
        if not raw:
            return None
        return json.loads(raw.decode("utf-8"))

    def get_branch_tip(self, branch: str) -> str:
        encoded = urllib.parse.quote(branch, safe="")
        obj = self._request("GET", f"/repos/{self.repo}/branches/{encoded}")
        return str(obj["commit"]["sha"])

    def get_commit(self, sha: str) -> Mapping[str, Any]:
        return self._request("GET", f"/repos/{self.repo}/commits/{sha}")

    def get_content(self, path: str, ref: str) -> tuple[str, str]:
        encoded_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
        encoded_ref = urllib.parse.quote(ref, safe="")
        obj = self._request("GET", f"/repos/{self.repo}/contents/{encoded_path}?ref={encoded_ref}")
        if obj.get("type") != "file":
            raise RuntimeError(f"{path} is not a file")
        content = base64.b64decode(obj["content"]).decode("utf-8")
        return content, str(obj["sha"])

    def get_workflow_run(self, run_id: int) -> Mapping[str, Any]:
        return self._request("GET", f"/repos/{self.repo}/actions/runs/{run_id}")

    def get_artifact(self, artifact_id: int) -> Mapping[str, Any]:
        return self._request("GET", f"/repos/{self.repo}/actions/artifacts/{artifact_id}")

    def resolve_commit(self, sha: str) -> None:
        self.get_commit(sha)

    def list_recent_return_branches(self, *, hours: int = 72) -> list[str]:
        """List recent agent branch tips whose commit headline is a return."""
        owner, name = self.repo.split("/", 1)
        query = """
        query($owner: String!, $name: String!, $after: String) {
          repository(owner: $owner, name: $name) {
            refs(refPrefix: "refs/heads/agent/", first: 100, after: $after) {
              nodes {
                name
                target {
                  ... on Commit { oid committedDate messageHeadline }
                }
              }
              pageInfo { hasNextPage endCursor }
            }
          }
        }
        """
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        result: list[str] = []
        after: str | None = None
        pages = 0
        while pages < 50:
            payload = self._request(
                "POST",
                "/graphql",
                body={
                    "query": query,
                    "variables": {"owner": owner, "name": name, "after": after},
                },
            )
            repo = payload.get("data", {}).get("repository") if isinstance(payload, Mapping) else None
            refs = repo.get("refs") if isinstance(repo, Mapping) else None
            if not isinstance(refs, Mapping):
                break
            for node in refs.get("nodes") or []:
                if not isinstance(node, Mapping):
                    continue
                branch = str(node.get("name", ""))
                target = node.get("target")
                if not branch.startswith("agent/") or not isinstance(target, Mapping):
                    continue
                committed = target.get("committedDate")
                headline = str(target.get("messageHeadline", ""))
                if not isinstance(committed, str) or "return" not in headline.lower():
                    continue
                try:
                    instant = datetime.fromisoformat(committed.replace("Z", "+00:00"))
                except ValueError:
                    continue
                if instant >= cutoff:
                    result.append(branch)
            page_info = refs.get("pageInfo")
            if not isinstance(page_info, Mapping) or page_info.get("hasNextPage") is not True:
                break
            after = page_info.get("endCursor")
            if not isinstance(after, str) or not after:
                break
            pages += 1
        return sorted(set(result))

    def issue_comments(self, issue_number: int) -> list[Mapping[str, Any]]:
        comments: list[Mapping[str, Any]] = []
        page = 1
        while page <= 20:
            rows = self._request(
                "GET",
                f"/repos/{self.repo}/issues/{issue_number}/comments?per_page=100&page={page}",
            )
            if not rows:
                break
            comments.extend(rows)
            if len(rows) < 100:
                break
            page += 1
        return comments

    def post_issue_comment(self, issue_number: int, body: str) -> None:
        self._request(
            "POST",
            f"/repos/{self.repo}/issues/{issue_number}/comments",
            body={"body": body},
        )


def _path_changed_in_tip(commit: Mapping[str, Any], path: str) -> bool:
    files = commit.get("files")
    return isinstance(files, list) and any(
        isinstance(item, Mapping) and item.get("filename") == path for item in files
    )


def _verify_required_outputs(
    client: GitHubClient,
    manifest: Mapping[str, Any],
    *,
    branch: str,
) -> tuple[str, ...]:
    errors: list[str] = []
    packet = manifest["return_packet"]
    try:
        _, actual_blob = client.get_content(str(packet["path"]), branch)
    except Exception as exc:
        errors.append(f"return packet cannot be read: {exc}")
    else:
        if actual_blob != packet["blob_sha"]:
            errors.append("return_packet.blob_sha does not match GitHub")

    for output in manifest["required_outputs"]:
        if output["kind"] == "path":
            try:
                _, actual_blob = client.get_content(str(output["path"]), branch)
            except Exception as exc:
                errors.append(f"required output {output['name']} cannot be read: {exc}")
            else:
                if actual_blob != output["blob_sha"]:
                    errors.append(f"required output {output['name']} blob SHA mismatch")
        else:
            try:
                client.resolve_commit(str(output["sha"]))
            except Exception as exc:
                errors.append(f"required commit {output['name']} cannot be resolved: {exc}")
    return tuple(errors)


def _verify_evidence(
    client: GitHubClient,
    manifest: Mapping[str, Any],
) -> tuple[str, ...]:
    evidence = manifest["evidence"]
    if evidence["required"] is not True:
        return ()
    errors: list[str] = []
    try:
        run = client.get_workflow_run(int(evidence["workflow_run_id"]))
    except Exception as exc:
        return (f"evidence workflow run cannot be read: {exc}",)
    if run.get("status") != "completed":
        errors.append("evidence workflow run is not completed")
    if run.get("conclusion") != evidence["conclusion"]:
        errors.append("evidence workflow conclusion does not match manifest")
    if run.get("name") != evidence["workflow_name"]:
        errors.append("evidence workflow name does not match manifest")
    if run.get("head_sha") != evidence["evidence_execution_sha"]:
        errors.append("evidence execution SHA does not match workflow run head SHA")

    artifact_id = evidence.get("artifact_id")
    if artifact_id is not None:
        if not isinstance(artifact_id, int) or artifact_id <= 0:
            errors.append("evidence.artifact_id must be a positive integer when present")
        else:
            try:
                artifact = client.get_artifact(artifact_id)
            except Exception as exc:
                errors.append(f"evidence artifact cannot be read: {exc}")
            else:
                if artifact.get("expired") is True:
                    errors.append("evidence artifact is expired")
    return tuple(errors)


def certify_manifest_at_tip(
    client: GitHubClient,
    *,
    branch: str,
) -> tuple[Certification | None, tuple[str, ...]]:
    try:
        tip_sha = client.get_branch_tip(branch)
        commit = client.get_commit(tip_sha)
        raw, _manifest_blob = client.get_content(MANIFEST_PATH, branch)
    except FileNotFoundError:
        return None, ("manifest not present",)
    except Exception as exc:
        return None, (f"unable to inspect branch: {exc}",)

    try:
        manifest = json.loads(raw)
    except Exception as exc:
        return None, (f"manifest is not valid JSON: {exc}",)
    if not isinstance(manifest, Mapping):
        return None, ("manifest root must be an object",)

    errors = list(validate_manifest_shape(manifest, branch=branch))
    if not _path_changed_in_tip(commit, MANIFEST_PATH):
        errors.append("manifest must be written/updated in the current branch-tip commit")
    if isinstance(manifest.get("return_packet"), Mapping):
        packet_path = manifest["return_packet"].get("path")
        if isinstance(packet_path, str) and not _path_changed_in_tip(commit, packet_path):
            errors.append("return packet must be written/updated in the same branch-tip commit as manifest")

    if not errors:
        errors.extend(_verify_required_outputs(client, manifest, branch=branch))
        errors.extend(_verify_evidence(client, manifest))

    if errors:
        return None, tuple(errors)

    returned = manifest["return"]
    evidence = manifest["evidence"]
    return (
        Certification(
            branch=branch,
            tip_sha=tip_sha,
            task_id=str(manifest["task_id"]),
            result=str(returned["result"]),
            terminal=str(returned["terminal"]),
            return_packet_path=str(manifest["return_packet"]["path"]),
            evidence_run_id=int(evidence["workflow_run_id"]) if evidence["required"] else None,
            mode="MANIFEST_V1",
        ),
        (),
    )


def _legacy_certify_tip(
    client: GitHubClient,
    *,
    branch: str,
) -> Certification | None:
    try:
        tip_sha = client.get_branch_tip(branch)
        commit = client.get_commit(tip_sha)
    except Exception:
        return None
    message = str(commit.get("commit", {}).get("message", ""))
    if "return" not in message.lower():
        return None
    files = commit.get("files")
    if not isinstance(files, list):
        return None
    texts: list[str] = []
    for item in files[:20]:
        if not isinstance(item, Mapping):
            continue
        path = item.get("filename")
        if not isinstance(path, str) or not path.endswith(".md"):
            continue
        if "RETURN" not in path.upper():
            continue
        try:
            text, _ = client.get_content(path, branch)
        except Exception:
            continue
        texts.append(text)
    if not texts:
        return None
    cert = certify_legacy_return_text("\n\n".join(texts), branch=branch, tip_sha=tip_sha)
    if cert is None:
        return None
    if cert.evidence_run_id is not None:
        try:
            run = client.get_workflow_run(cert.evidence_run_id)
        except Exception:
            return None
        if run.get("status") != "completed" or run.get("conclusion") not in _EVIDENCE_CONCLUSIONS:
            return None
    return cert


def _marker(cert: Certification) -> str:
    return f"<!-- rawlsing-return-beacon:{cert.branch}:{cert.tip_sha} -->"


def _already_notified(
    client: GitHubClient,
    issue_number: int,
    cert: Certification,
) -> bool:
    marker = _marker(cert)
    return any(marker in str(comment.get("body", "")) for comment in client.issue_comments(issue_number))


def _comment_body(cert: Certification) -> str:
    evidence = f"`{cert.evidence_run_id}`" if cert.evidence_run_id else "not required / not declared"
    return (
        f"{_marker(cert)}\n"
        f"## ✅ Certified worker return — {cert.result}\n\n"
        f"- **Task:** `{cert.task_id}`\n"
        f"- **Branch:** `{cert.branch}`\n"
        f"- **Certified branch tip:** `{cert.tip_sha}`\n"
        f"- **Terminal:** `{cert.terminal}`\n"
        f"- **Return packet:** `{cert.return_packet_path}`\n"
        f"- **Evidence run:** {evidence}\n"
        f"- **Certification mode:** `{cert.mode}`\n\n"
        "This notification means the repository completion contract is satisfied: "
        "the commissioned turn is durably returned and no required/background work remains. "
        "The result may be PASS, FAIL, or BLOCKED; completion is distinct from semantic success."
    )


def notify_if_certified(
    client: GitHubClient,
    *,
    branch: str,
    issue_number: int,
    allow_legacy: bool = True,
) -> bool:
    cert, _errors = certify_manifest_at_tip(client, branch=branch)
    if cert is None and allow_legacy:
        cert = _legacy_certify_tip(client, branch=branch)
    if cert is None:
        return False
    if _already_notified(client, issue_number, cert):
        return True
    client.post_issue_comment(issue_number, _comment_body(cert))
    return True


def _watch_branch(
    client: GitHubClient,
    *,
    branch: str,
    issue_number: int,
    timeout_seconds: int,
    interval_seconds: int,
) -> int:
    deadline = time.monotonic() + timeout_seconds
    while True:
        if notify_if_certified(client, branch=branch, issue_number=issue_number):
            return 0
        if time.monotonic() >= deadline:
            tip = "unknown"
            try:
                tip = client.get_branch_tip(branch)
            except Exception:
                pass
            marker = f"<!-- rawlsing-return-beacon-timeout:{branch}:{tip} -->"
            if not any(
                marker in str(comment.get("body", ""))
                for comment in client.issue_comments(issue_number)
            ):
                client.post_issue_comment(
                    issue_number,
                    (
                        f"{marker}\n"
                        "## ⏱️ Return watch timed out — not certified\n\n"
                        f"- **Branch:** `{branch}`\n"
                        f"- **Observed tip:** `{tip}`\n\n"
                        "No certified durable return appeared before the watcher timeout. "
                        "This is **not** a completion notification. The scheduled sweep will keep checking."
                    ),
                )
            return 2
        time.sleep(interval_seconds)


def _sweep(client: GitHubClient, *, issue_number: int) -> int:
    certified = 0
    for branch in client.list_recent_return_branches():
        try:
            if notify_if_certified(client, branch=branch, issue_number=issue_number):
                certified += 1
        except Exception as exc:
            print(f"warning: {branch}: {exc}", file=sys.stderr)
    print(f"return-beacon sweep complete; certified/known branches={certified}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--issue", type=int, default=DEFAULT_INBOX_ISSUE)
    sub = parser.add_subparsers(dest="command", required=True)
    watch = sub.add_parser("watch")
    watch.add_argument("--branch", required=True)
    watch.add_argument("--timeout-seconds", type=int, default=1500)
    watch.add_argument("--interval-seconds", type=int, default=15)
    sub.add_parser("sweep")
    validate = sub.add_parser("validate")
    validate.add_argument("manifest")
    validate.add_argument("--branch", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "validate":
        with open(args.manifest, "r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        errors = validate_manifest_shape(manifest, branch=args.branch)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 2
        print("PASS__RABOCHII_RETURN_MANIFEST_SHAPE")
        return 0

    if not args.repo or not args.token:
        print("GITHUB_REPOSITORY/--repo and GITHUB_TOKEN/--token are required", file=sys.stderr)
        return 2
    client = GitHubClient(args.repo, args.token)
    if args.command == "watch":
        return _watch_branch(
            client,
            branch=args.branch,
            issue_number=args.issue,
            timeout_seconds=args.timeout_seconds,
            interval_seconds=args.interval_seconds,
        )
    if args.command == "sweep":
        return _sweep(client, issue_number=args.issue)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
