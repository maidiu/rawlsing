#!/usr/bin/env python3
"""Read-only ChatGPT-to-O-LIVE query port. Does not run a person or issue authority.

Only the pre-existing Sorok living_reference.py is queried; no separate graph,
scientific state, source-of-truth or mutable chatbot memory is created.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

HERE = Path(__file__).resolve().parent
SCHEMA = "PROGRAMMA_SOROK_CHAT_QUERY@0.1"
SOURCE_CUT = "54013d1907e5ea55b0d1f54ea9afe07ef6388b11"
REQUIRED_ID = frozenset({
    "focus", "zoom", "maturity", "lateral", "code", "evidence",
    "consumer", "source", "alternatives", "history", "blocked-chain",
})
NO_ID = frozenset({
    "home", "overview", "work-now", "workers", "owners", "coverage",
    "whole-gaps", "gaps", "verify-sources", "verify-journal", "journal",
})
ALLOWED = REQUIRED_ID | NO_ID
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/+-]{0,255}$")
READ_SCOPE = "AUTHOR_TESTED_O_LIVE_CANDIDATE__NOT_CANONICAL__NOT_NATIVE"


class ChatQueryError(ValueError):
    """Reject unqualified requests without converting into a write operation."""


def validate(request: Mapping[str, Any]) -> list[str]:
    if not isinstance(request, Mapping):
        raise ChatQueryError("REQUEST_MUST_BE_OBJECT")
    if set(request) - {"verb", "id", "depth", "domain", "stage"}:
        raise ChatQueryError("UNRECOGNIZED_FIELDS")
    verb = request.get("verb")
    if verb not in ALLOWED:
        raise ChatQueryError("READ_ONLY_VERB_NOT_ALLOWED")
    result = [verb]
    if verb in REQUIRED_ID:
        ident = request.get("id")
        if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
            raise ChatQueryError("VALID_EXACT_ID_REQUIRED")
        result.append(ident)
        if verb in {"focus", "zoom"}:
            depth = request.get("depth", 1)
            if not isinstance(depth, int) or isinstance(depth, bool) or not (0 <= depth <= 4):
                raise ChatQueryError("DEPTH_OUT_OF_BOUNDS")
            result.extend(["--depth", str(depth)])
        elif "depth" in request:
            raise ChatQueryError("DEPTH_NOT_SUPPORTED")
        if "stage" in request or "domain" in request:
            raise ChatQueryError("FILTER_NOT_SUPPORTED")
    else:
        if "id" in request or "depth" in request:
            raise ChatQueryError("ID_OR_DEPTH_NOT_SUPPORTED")
        if verb not in {"whole-gaps", "gaps"} and ("domain" in request or "stage" in request):
            raise ChatQueryError("FILTER_NOT_SUPPORTED")
        if verb == "gaps" and "stage" in request:
            raise ChatQueryError("STAGE_NOT_SUPPORTED")
        for name in ("stage", "domain"):
            if name in request:
                val = request[name]
                if not isinstance(val, str) or not ID_RE.fullmatch(val):
                    raise ChatQueryError("FILTER_MUST_BE_EXACT_ID")
                result.extend(["--" + name, val])
    return result


def query(
    request: Mapping[str, Any],
    *,
    root: Path = HERE,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    argv = validate(request)
    root = Path(root).resolve()
    script = root / "living_reference.py"
    state = root / "state.json"
    if not script.is_file() or not state.is_file():
        raise ChatQueryError("O_LIVE_SOURCE_OR_STATE_MISSING")
    command = [sys.executable, str(script), "--state", str(state), *argv]
    try:
        result = runner(command, cwd=root, text=True, capture_output=True, timeout=120, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ChatQueryError("O_LIVE_READ_TIMED_OUT") from exc
    if result.returncode != 0:
        raise ChatQueryError(f"O_LIVE_READ_FAILED_{result.returncode}: {result.stderr[-800:]}")
    if len(result.stdout) > 1000000:
        raise ChatQueryError("O_LIVE_RESPONSE_TOO_LARGE__USE_FOCUS")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ChatQueryError("O_LIVE_RETURNED_NON_JSON") from exc
    return {
        "schema": SCHEMA,
        "request": dict(request),
        "status": READ_SCOPE,
        "source": {
            "repository": "maidiu/rawlsing",
            "candidate_branch": "codex/programma-sorok-p0-p1-engineering-20261101",
            "pinned_source_sha": SOURCE_CUT,
            "execution": "LOCAL_SOURCEFREE_QUERY_ONLY__NOT_EXECUTED_BY_CHATGPT_BROWSER",
        },
        "authority": {
            "review": "AUTHOR_RETURNED__INDEPENDENT_ADOPTION_NOT_ESTABLISHED",
            "native_science": "HELD",
            "actor": "HELD",
            "programme_person_production": "NOT_RUN",
        },
        "result": data,
    }


def main() -> int:
    raw = sys.stdin.read()
    try:
        result = query(json.loads(raw))
    except (ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"schema": SCHEMA, "error": str(exc), "status": "NO_PROMOTION"}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
