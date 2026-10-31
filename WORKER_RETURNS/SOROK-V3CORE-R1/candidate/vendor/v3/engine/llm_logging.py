# v3/engine/llm_logging.py
# Shared LLM call logging — request/response artifact writing for audit and causal trace.

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_llm_call(
    log_dir: Path,
    call_id: str,
    *,
    provider: str,
    model: str,
    system_prompt: str = "",
    user_prompt: str = "",
    raw_response: str = "",
    status: str = "ok",
    error: str | None = None,
    parse_status: str | None = None,
    extra: dict[str, Any] | None = None,
) -> Path:
    """Write a durable LLM call artifact and return the call directory path."""
    call_dir = log_dir / call_id
    call_dir.mkdir(parents=True, exist_ok=True)
    prompt_text = system_prompt + "\n\n---\n\n" + user_prompt if system_prompt else user_prompt
    input_hash = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    output_hash = hashlib.sha256((raw_response or "").encode("utf-8")).hexdigest()
    manifest = {
        "call_id": call_id,
        "provider": provider,
        "model": model,
        "status": status,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "input_chars": len(prompt_text),
        "output_chars": len(raw_response or ""),
        "generated_at": _now_iso(),
        "parse_status": parse_status,
        "error": error,
        "extra": extra or {},
    }
    (call_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    (call_dir / "system_prompt.txt").write_text(system_prompt or "", encoding="utf-8")
    (call_dir / "user_prompt.txt").write_text(user_prompt or "", encoding="utf-8")
    (call_dir / "raw_response.txt").write_text(raw_response or "", encoding="utf-8")
    return call_dir


def write_causal_trace_entry(
    trace_path: Path,
    *,
    session_id: str,
    age: int,
    year: int,
    stage: str,
    prompt_input_integrity: str,
    request_path: str,
    response_path: str,
    raw_candidate_ids: list[str] | None = None,
    parser_repairs: list[str] | None = None,
    sanitized_candidates: int = 0,
    scoring_inputs: dict[str, Any] | None = None,
    scoring_outputs: dict[str, Any] | None = None,
    selected_candidate_ids: list[str] | None = None,
    delta_templates: list[str] | None = None,
    merged_deltas: dict[str, Any] | None = None,
    applied_fields: list[str] | None = None,
    before_state_hash: str | None = None,
    after_state_hash: str | None = None,
    mutation_provenance: list[dict[str, Any]] | None = None,
    verdict: str = "clean",
) -> None:
    """Append one line to the causal trace JSONL."""
    entry = {
        "session_id": session_id,
        "age": age,
        "year": year,
        "stage": stage,
        "prompt_input_integrity": prompt_input_integrity,
        "request_path": request_path,
        "response_path": response_path,
        "raw_candidate_ids": raw_candidate_ids or [],
        "parser_repairs": parser_repairs or [],
        "sanitized_candidates": sanitized_candidates,
        "scoring_inputs": scoring_inputs or {},
        "scoring_outputs": scoring_outputs or {},
        "selected_candidate_ids": selected_candidate_ids or [],
        "delta_templates": delta_templates or [],
        "merged_deltas": merged_deltas or {},
        "applied_fields": applied_fields or [],
        "before_state_hash": before_state_hash or "",
        "after_state_hash": after_state_hash or "",
        "mutation_provenance": mutation_provenance or [],
        "verdict": verdict,
    }
    with open(trace_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")
