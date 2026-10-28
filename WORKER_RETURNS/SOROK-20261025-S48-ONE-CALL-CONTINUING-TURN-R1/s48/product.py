"""Sourcefree one-call product envelope transport and validation."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import RETURN, install

install()

from .errors import ProductCallError, S48Refusal
from .sources import candidate_specs, eligible_candidate_ids

PRODUCT_SCHEMA = "S48_PRODUCT_ENVELOPE@1"
PRODUCT_INPUT_SCHEMA = "S48_ACTOR_PRODUCT_INPUT@1"
CANDIDATES = {
    "OTHER_REFUSES_TOOL": {
        "source_operation": "REFUSE_TOOL",
        "source_kind": "REQUIRES_INDEPENDENT_CURRENT_B_SOURCE",
    },
    "OTHER_SHARES_TOOL": {
        "source_operation": "SHARE_TOOL",
        "source_kind": "REQUIRES_INDEPENDENT_CURRENT_B_SOURCE",
    },
}

# Compatibility names only.  There are deliberately no CLI/model/provider
# defaults: every paid transport selection must be explicit in the environment.
PRODUCT_CLI = ""
PRODUCT_MODEL = ""
PRODUCT_VARIANT = ""
PRODUCT_CONFIG: dict[str, Any] = {}
PRODUCT_PERMISSIONS = {
    "edit": "deny",
    "bash": "deny",
    "webfetch": "deny",
    "question": "deny",
    "task": "deny",
    "external_directory": "deny",
}


@dataclass(frozen=True)
class ProductSelection:
    cli: str
    provider: str
    model: str
    variant: str
    account: str


def _required_env(name: str, missing_code: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ProductCallError(
            missing_code,
            f"{name} must be explicitly selected; no PATH or model default is used",
        )
    return value


def select_product() -> ProductSelection:
    """Return the complete explicit paid-transport selection or fail closed."""
    cli = _required_env("S48_PRODUCT_CLI", "S48_PRODUCT_CLI_MISSING")
    provider = _required_env("S48_PRODUCT_PROVIDER", "S48_PRODUCT_PROVIDER_MISSING")
    model = _required_env("S48_PRODUCT_MODEL", "S48_PRODUCT_MODEL_MISSING")
    variant = _required_env("S48_PRODUCT_VARIANT", "S48_PRODUCT_VARIANT_MISSING")
    account = _required_env("S48_PRODUCT_ACCOUNT", "S48_PRODUCT_ACCOUNT_MISSING")

    cli_path = Path(cli).expanduser()
    if not cli_path.is_absolute():
        raise ProductCallError(
            "S48_PRODUCT_CLI_NOT_ABSOLUTE",
            f"S48_PRODUCT_CLI must be an absolute executable path: {cli_path}",
        )
    if not cli_path.is_file() or not os.access(cli_path, os.X_OK):
        raise ProductCallError(
            "S48_PRODUCT_CLI_INVALID",
            f"S48_PRODUCT_CLI is not an executable file: {cli_path}",
        )
    if not provider or "/" in provider:
        raise ProductCallError("S48_PRODUCT_PROVIDER_INVALID", provider)
    model_provider, separator, model_name = model.partition("/")
    if not separator or not model_name or model_provider != provider:
        raise ProductCallError(
            "S48_PRODUCT_PROVIDER_MODEL_MISMATCH",
            f"provider={provider!r} model={model!r}",
        )
    return ProductSelection(
        cli=str(cli_path),
        provider=provider,
        model=model,
        variant=variant,
        account=account,
    )


def product_config(selection: ProductSelection | None = None) -> dict[str, Any]:
    """Build OpenCode config from the explicit selection, never from defaults."""
    selected = selection or select_product()
    return {
        "model": selected.model,
        "small_model": selected.model,
        "enabled_providers": [selected.provider],
        "autoupdate": False,
        "permission": dict(PRODUCT_PERMISSIONS),
    }


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_hash(value: Any) -> str:
    return _sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def build_payload(session, *, event: Mapping[str, Any] | None = None) -> dict:
    events = session.read_events()
    if event is None:
        if not events:
            raise S48Refusal("S48_OCCURRED_EVENT_MISSING")
        event = events[-1]
    c9 = event.get("c9")
    if not isinstance(c9, Mapping):
        raise S48Refusal("S48_C9_RESULT_MISSING")
    world = session.world()
    state = dict((world.actor_state or {}).get("A") or {})
    prerequisites = session.world_prerequisites()
    language = event.get("language")
    public_language = None
    if isinstance(language, Mapping) and language.get("status") in {
        "ACCEPTED", "NONVERBAL",
    }:
        public_language = {
            "status": language.get("status"),
            "native_text": language.get("native_text", ""),
            "translation_text": language.get("translation_text", ""),
        }
    return {
        "schema": PRODUCT_INPUT_SCHEMA,
        "event_ref": event.get("e1_event_id"),
        "event_hash": event.get("e1_event_hash"),
        "event_ordinal": event.get("event_ordinal"),
        "event_time": event.get("event_time"),
        "actor_id": event.get("actor_id"),
        "occurred_event": {
            "source_operation": event.get("source_operation"),
            "selected_option": event.get("selected_option"),
            "action_event_kind": event.get("action_event_kind"),
            "performed": bool(event.get("performed")),
            "language": public_language,
        },
        "c9_result": {
            "outcome": c9.get("outcome"),
            "response_kind": c9.get("response_kind"),
            "target_branch": c9.get("target_branch"),
            "target_reason": c9.get("target_reason"),
            "target_proposals": list(c9.get("target_proposals") or []),
        },
        "accessible_world": {
            "scene": (world.positions or {}).get("A"),
            "clock": session.clock(),
            "material_remaining": state.get("material_remaining"),
            "tools_remaining": state.get("tools_remaining"),
            "free_hours": state.get("free_hours"),
            "material_available": prerequisites.get("material_available"),
            "tool_available": prerequisites.get("tool_available"),
        },
        "allowed_prospective_candidates": candidate_specs(session),
    }


def build_prompt(payload: Mapping[str, Any]) -> str:
    return (
        "You are a bounded sourcefree product voice for one continuing-person turn. "
        "Use only the JSON payload below. Do not use tools, files, the web, private "
        "context, hidden reasons, or other-person motives. Do not choose or describe "
        "the actor's response, help, refusal, or other action. Do not appoint a rule, "
        "owner, target, or authority. Return exactly one JSON object and no prose.\n\n"
        "Required object schema:\n"
        '{"narrative": "retrospective reader narrative", '
        '"self_account": null or "a short optional proposed actor self-account", '
        '"prospective": [{"candidate_id": "allowed ID", "rationale": "why this world proposal"}]}\n\n'
        "self_account may be null when no distinct new self-account is proposed; "
        "do not add one merely to satisfy the schema. prospective must use only "
        "allowed_prospective_candidates IDs. The allowed list is the complete "
        "turn-local set of lawful world proposals. If exactly one allowed proposal "
        "is lawful from the supplied facts, include it; return an empty list only "
        "if no allowed proposal is lawful. Do not choose a proposal merely to avoid "
        "an empty list. The payload contains the actual occurred event, its C9 "
        "result, and accessible world facts.\n\nPAYLOAD:\n"
        + json.dumps(payload, sort_keys=True, separators=(",", ":"))
    )


def _strip_fence(text: str) -> str:
    value = text.strip()
    if value.startswith("```"):
        lines = value.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            first = lines[0].strip().lower()
            if first in {"```", "```json"}:
                return "\n".join(lines[1:-1]).strip()
    return value


def parse_envelope(text: str) -> dict:
    try:
        value = json.loads(_strip_fence(text))
    except (TypeError, ValueError) as exc:
        raise S48Refusal("S48_PRODUCT_MALFORMED_JSON", str(exc)) from exc
    if not isinstance(value, dict) or set(value) != {
        "narrative", "self_account", "prospective"
    }:
        raise S48Refusal("S48_PRODUCT_ENVELOPE_SHAPE")
    if not isinstance(value["narrative"], str):
        raise S48Refusal("S48_PRODUCT_NARRATIVE_INVALID")
    self_account = value["self_account"]
    if self_account is not None and not isinstance(self_account, str):
        raise S48Refusal("S48_PRODUCT_SELF_ACCOUNT_INVALID")
    if isinstance(self_account, str) and not self_account.strip():
        self_account = None
    if not isinstance(value["prospective"], list):
        raise S48Refusal("S48_PRODUCT_PROSPECTIVE_INVALID")
    seen = set()
    prospective = []
    for item in value["prospective"]:
        if not isinstance(item, dict) or set(item) != {"candidate_id", "rationale"}:
            raise S48Refusal("S48_PRODUCT_CANDIDATE_SHAPE")
        candidate_id = item.get("candidate_id")
        rationale = item.get("rationale")
        if candidate_id not in CANDIDATES:
            raise S48Refusal("S48_PRODUCT_CANDIDATE_UNAUTHORIZED")
        if not isinstance(rationale, str):
            raise S48Refusal("S48_PRODUCT_CANDIDATE_RATIONALE_INVALID")
        if candidate_id in seen:
            raise S48Refusal("S48_PRODUCT_CANDIDATE_DUPLICATE")
        seen.add(candidate_id)
        prospective.append({
            "candidate_id": candidate_id,
            "rationale": rationale,
        })
    return {
        "schema": PRODUCT_SCHEMA,
        "narrative": value["narrative"],
        "self_account": self_account,
        "self_account_present": bool(self_account),
        "prospective": prospective,
    }


def _parse_events(stdout: str) -> list[dict]:
    events = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def run_product_cli(
    prompt: str,
    *,
    workdir: str | Path,
    log_dir: str | Path,
    timeout: int = 300,
) -> dict:
    selection = select_product()
    work = Path(workdir)
    logs = Path(log_dir)
    return_root = Path(RETURN).resolve()
    logs_resolved = logs.resolve()
    if logs_resolved != return_root and not logs_resolved.is_relative_to(return_root):
        raise ProductCallError(
            "S48_PRODUCT_LOG_DIR_OUTSIDE",
            f"log_dir must remain inside the S48 return root: {logs_resolved}",
        )
    work.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    stamp = hashlib.sha256(prompt.encode()).hexdigest()[:16]
    stdout_path = logs / f"product_{stamp}.stdout.jsonl"
    stderr_path = logs / f"product_{stamp}.stderr.log"
    env = dict(os.environ)
    env["OPENCODE_CONFIG_CONTENT"] = json.dumps(product_config(selection))
    env["TMPDIR"] = str(logs)
    env["XDG_CACHE_HOME"] = str(RETURN / "runtime" / "product-cache")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("OPENCODE_PID", None)
    started = time.time()
    cmd = [
        selection.cli,
        "run",
        "--model", selection.model,
        "--variant", selection.variant,
        "--format", "json",
        "--pure",
        "--dir", str(work),
        "--title", "S48_PRODUCT_TURN",
        prompt,
    ]
    proc = subprocess.run(
        cmd, cwd=str(work), env=env, capture_output=True, text=True,
        timeout=timeout,
    )
    duration_ms = int((time.time() - started) * 1000)
    stdout_path.write_text(proc.stdout)
    stderr_path.write_text(proc.stderr)
    events = _parse_events(proc.stdout)
    step_starts = [row for row in events if row.get("type") == "step_start"]
    step_finishes = [row for row in events if row.get("type") == "step_finish"]
    text_parts = [
        str((row.get("part") or {}).get("text", ""))
        for row in events if row.get("type") == "text"
    ]
    session_ids = sorted({
        str(row.get("sessionID")) for row in events if row.get("sessionID")
    })
    receipt = {
        "schema": "S48_PRODUCT_CALL_RECEIPT@1",
        "actual_provider_call": False,
        "subprocess_completed": True,
        "account_transport": "ALIAS_ONLY",
        "provider_step_observed": bool(step_starts and step_finishes and text_parts),
        "provider_call_evidence": "SOURCEFREE_SUBPROCESS_EVENTS_NOT_PROVIDER_PROOF",
        "provider": selection.provider,
        "model": selection.model,
        "variant": selection.variant,
        "cli": selection.cli,
        "account_sha256": _sha(selection.account.encode()),
        "cli_exit": proc.returncode,
        "duration_ms": duration_ms,
        "step_count": len(step_starts),
        "step_finish_count": len(step_finishes),
        "provider_call_count": len(step_starts),
        "event_count": len(events),
        "text_part_count": len(text_parts),
        "session_ids": session_ids,
        "stdout_path": str(stdout_path.relative_to(RETURN)),
        "stderr_path": str(stderr_path.relative_to(RETURN)),
        "stdout_sha256": _sha(proc.stdout.encode()),
        "stderr_sha256": _sha(proc.stderr.encode()),
        "prompt_sha256": _sha(prompt.encode()),
        "output_sha256": _sha("".join(text_parts).encode()),
    }
    if proc.returncode != 0:
        raise ProductCallError("S48_PRODUCT_CALL_FAILED", str(proc.returncode), receipt)
    if not step_starts or not step_finishes:
        raise ProductCallError("S48_PRODUCT_CALL_MISSING_STEP", "", receipt)
    if len(step_starts) != 1 or len(step_finishes) != 1:
        raise ProductCallError("S48_PRODUCT_CALL_COUNT_INVALID", "", receipt)
    if not text_parts:
        raise ProductCallError("S48_PRODUCT_OUTPUT_MISSING", "", receipt)
    text = "".join(text_parts)
    receipt["response_sha256"] = _sha(text.encode())
    try:
        envelope = parse_envelope(text)
    except S48Refusal as exc:
        receipt["parse_refusal"] = exc.code
        raise ProductCallError("S48_PRODUCT_OUTPUT_INVALID", exc.code, receipt) from exc
    return {"status": "OK", "envelope": envelope, "call_receipt": receipt, "prompt_hash": receipt["prompt_sha256"]}


__all__ = [
    "CANDIDATES", "PRODUCT_CONFIG", "PRODUCT_INPUT_SCHEMA", "PRODUCT_MODEL",
    "PRODUCT_SCHEMA", "PRODUCT_VARIANT", "ProductSelection", "build_payload",
    "build_prompt", "eligible_candidate_ids", "parse_envelope", "product_config",
    "run_product_cli", "select_product",
]
