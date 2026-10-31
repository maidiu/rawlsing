#!/usr/bin/env python3
"""
v3/tools/distill_memory.py

Hierarchical memory distillation for persona_sheet.json files.

Takes an existing persona_sheet.json (which may have repetitive backstory
from pre-dedup pipeline runs and structural stubs) and runs an LLM pass
to produce a condensed, layered memory where:

  - Oldest memories (pre-adolescence) are compressed into resonance
    fragments: brief, sensory traces that "linger beneath" the surface.
    Format: "Beneath that, from age N, lingers: ..."
  - Adolescent and early-adult memories are kept at medium density —
    the key ruptures and gifts in prose, not enumerated.
  - Recent memories (roughly the last 10 years) are preserved vivid
    and specific, scene-level detail intact.

The result reads like a character's internalized sense of their own life —
not a ledger, but a palimpsest: old things faintly visible under new ones.

Usage (standalone):
    python -m v3.tools.distill_memory path/to/persona_sheet.json

    Optional flags:
      --out PATH       Write result to PATH instead of overwriting in-place.
      --dry-run        Print the distilled backstory without writing.
      --model MODEL    Override model (default: $SIM_MODEL or gpt-4o).
      --max-chars N    Target character count for distilled backstory (default: 6000).

Can also be imported and called programmatically:
    from v3.tools.distill_memory import distill_persona_sheet_backstory
    new_sheet = distill_persona_sheet_backstory(sheet_dict, openai_key="...")
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import hashlib
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pre-processing: strip repetitions and stubs from a raw backstory string
# before sending to the LLM. The LLM prompt is strong enough to handle
# the raw text, but cleaning it first reduces token waste and prevents the
# LLM from inheriting the repetition structure.
# ---------------------------------------------------------------------------

_STUB_LINE_RE = re.compile(
    r"^\s*Age \d+:\s*\n"
    r"Age \d+:.*\[Structural year[^\n]*\]\s*$",
    re.MULTILINE,
)
_STUB_SINGLE_RE = re.compile(
    r"^Age \d+:.*\[Structural year[^\n]*\]\n?",
    re.MULTILINE,
)
_STATS_LINE_RE = re.compile(
    r"^\s*Age \d+:\s*health \d+/100.*\[Structural year[^\n]*\]\s*\n?",
    re.MULTILINE,
)


def _preprocess_backstory(raw: str) -> str:
    """
    Remove structural stubs and deduplicate repeated rupture/metabolization
    lines from a raw backstory string. Does not alter real scenes.
    """
    # Strip structural year stubs (both single-line and block forms)
    cleaned = _STATS_LINE_RE.sub("", raw)
    cleaned = _STUB_LINE_RE.sub("", cleaned)
    cleaned = _STUB_SINGLE_RE.sub("", cleaned)

    # Remove "Age N:\n" headers that now have no content after stub removal
    cleaned = re.sub(r"\nAge \d+:\n(?=\nAge \d+:|\Z)", "\n", cleaned)

    # Deduplicate repeated rupture sentences across bands.
    # The repeated content pattern: "At N something gave way: «...»." appearing
    # multiple times with identical text → keep first occurrence only.
    seen_rupture_sents: set[str] = set()
    output_lines: list[str] = []
    for line in cleaned.split("\n"):
        stripped = line.strip()
        # Detect repeated "gave way" / "been carrying" / "they received a gift" lines
        if re.match(r"^(At \d+ something gave way|They've been carrying|At \d+ they received a gift|At \d+ a disruption)", stripped):
            key = re.sub(r"\s+", " ", stripped)[:120]
            if key in seen_rupture_sents:
                continue
            seen_rupture_sents.add(key)
        output_lines.append(line)

    cleaned = "\n".join(output_lines)

    # Collapse runs of 3+ blank lines to 2
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


# ---------------------------------------------------------------------------
# Distillation prompt
# ---------------------------------------------------------------------------

_DISTILLATION_SYSTEM = """You are a literary memory editor. Your job is to rewrite a character's backstory as internalized, lived memory — not a ledger, not allegory, not a mood poem. The output should read like a real person's specific past: the names of people, the names of places, the actual things that happened.

Rules:
1. OLDEST MEMORIES (before adolescence, roughly before age 13): compress to 1–2 sentences per major event. Keep it SPECIFIC: keep any named person (friend, parent, teacher), keep the specific setting (classroom, home, neighborhood), keep what actually happened. Do NOT convert real events into abstract metaphors or atmospheric language. WRONG: "the belief that home is a fortress and adults are its unwavering sentinels." RIGHT: "At 3 his father left for two months — no explanation given — and something in how he understood adults shifted permanently."
2. ADOLESCENT MEMORIES (age 13–18): one paragraph per major rupture or gift. Keep names, keep the place, keep what was said or done. Compress length, not specificity.
3. EARLY ADULT (age 18–25): one paragraph per watershed. If the scene names specific people and places, keep those names. Let the scenes breathe.
4. RECENT (age 25 to present): preserve scene-level detail as fully as possible. Real scenes with specific people, places, and what happened — use them close to verbatim, cutting only repetition or structural artifacts.
5. NEVER invent new facts. Only compress, reorder, and clarify what is already given.
6. DROP: structural stubs, stat lines (health 50/100 etc.), repeated sentences, "[no recorded scene]" and "[Structural year]" artifacts, anything purely mechanical.
7. KEEP: every named person (even minor ones). Every named place. Every specific incident. The actual words someone said if quoted. The person's own name. The specific ages.
8. OUTPUT FORMAT: Plain prose. No markdown headers. No band labels. No numbered lists. Paragraphs separated by blank lines. End with the most recent memory.
9. TARGET LENGTH: approximately {max_chars} characters (give or take 20%).
10. TONE: This must feel like someone's actual memory — grounded and specific, not literary or symbolic. Concrete over atmospheric. Named and placed over abstract and ambient.
"""

_DISTILLATION_USER = """Here is the raw backstory for {name}, age {age}, from {country}. Please edit it into compressed, specific lived memory following the rules above. Keep named people, named places, and specific events. Do not convert concrete facts into atmospheric metaphors.

RAW BACKSTORY:
---
{backstory}
---

Edited backstory (specific, concrete, named — not allegorical):"""


def _build_distillation_prompt(
    name: str,
    age: int,
    country: str,
    backstory: str,
    max_chars: int = 6000,
) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for the distillation call."""
    system = _DISTILLATION_SYSTEM.format(max_chars=max_chars)
    user = _DISTILLATION_USER.format(
        name=name,
        age=age,
        country=country,
        backstory=backstory,
    )
    return system, user


def _distillation_manifest(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    preprocessed: str,
    distilled: str,
    status: str,
    dropped_stub_count: int = 0,
    source_defects: list[str] | None = None,
) -> dict[str, Any]:
    prompt_bytes = (system_prompt + "\n\n---\n\n" + user_prompt).encode("utf-8")
    input_hash = hashlib.sha256(preprocessed.encode("utf-8")).hexdigest()
    prompt_hash = hashlib.sha256(prompt_bytes).hexdigest()
    output_hash = hashlib.sha256((distilled or "").encode("utf-8")).hexdigest()
    return {
        "model": model,
        "prompt_hash": prompt_hash,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "input_chars": len(preprocessed),
        "output_chars": len(distilled or ""),
        "dropped_stub_count": dropped_stub_count,
        "status": status,
        "source_defects": list(source_defects or []),
    }


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def _call_llm(
    system_prompt: str,
    user_prompt: str,
    openai_key: str,
    model: str = "gpt-4o",
) -> str:
    """Call OpenAI/DeepSeek and return the assistant text. Raises on failure."""
    from openai import OpenAI  # noqa: PLC0415

    if model.startswith("deepseek"):
        client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY") or openai_key,
            base_url="https://api.deepseek.com",
        )
    else:
        client = OpenAI(api_key=openai_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=4000,
        temperature=0.7,
    )
    return (resp.choices[0].message.content or "").strip()


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

def distill_persona_sheet_backstory(
    sheet: dict[str, Any],
    openai_key: str | None = None,
    model: str | None = None,
    max_chars: int = 6000,
    dry_run: bool = False,
    log_dir: Path | None = None,
) -> dict[str, Any]:
    """
    Distill the backstory in `sheet` in-place (returns modified copy).

    Args:
        sheet: A persona_sheet dict with at least an "identity" and "backstory" key.
        openai_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: Model to use. Falls back to SIM_MODEL env var, then gpt-4o.
        max_chars: Target character count for distilled backstory.
        dry_run: If True, do the LLM call but don't modify the sheet — return
                 a copy with a "distilled_backstory_preview" key instead.
        log_dir: If set, writes LLM call artifacts (request/response) to this directory.

    Returns:
        Modified (or preview) sheet dict.
    """
    import copy
    sheet = copy.deepcopy(sheet)

    key = openai_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("No OpenAI API key: set OPENAI_API_KEY or pass openai_key=")

    resolved_model = model or os.environ.get("SIM_MODEL", "gpt-4o")

    identity = sheet.get("identity") or {}
    given = identity.get("given_name", "the persona")
    family = identity.get("family_name", "")
    name = f"{given} {family}".strip()
    age = int(identity.get("age", 0))
    country = identity.get("country", "unknown")

    raw_backstory = sheet.get("backstory", "")
    if not raw_backstory or not raw_backstory.strip():
        logger.warning("distill_persona_sheet_backstory: empty backstory — nothing to distill")
        sheet["distillation_manifest"] = {
            "model": resolved_model,
            "prompt_hash": "",
            "input_hash": "",
            "output_hash": "",
            "input_chars": 0,
            "output_chars": 0,
            "dropped_stub_count": 0,
            "status": "skipped_empty",
            "source_defects": ["empty_backstory"],
        }
        sheet["distillation_metadata"] = sheet["distillation_manifest"]
        return sheet

    # Pre-process to remove stubs and deduplicate
    preprocessed = _preprocess_backstory(raw_backstory)
    dropped_stub_count = max(0, len(raw_backstory.splitlines()) - len(preprocessed.splitlines()))
    if raw_backstory and not sheet.get("backstory_raw"):
        sheet["backstory_raw"] = raw_backstory

    if len(preprocessed) < 500:
        logger.warning(
            "distill_persona_sheet_backstory: backstory after preprocessing is very short "
            "(%d chars) — skipping LLM call and returning preprocessed version",
            len(preprocessed),
        )
        system_prompt, user_prompt = _build_distillation_prompt(
            name=name,
            age=age,
            country=country,
            backstory=preprocessed,
            max_chars=max_chars,
        )
        manifest = _distillation_manifest(
            model=resolved_model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            preprocessed=preprocessed,
            distilled=preprocessed,
            status="preprocessed_fallback",
            dropped_stub_count=dropped_stub_count,
            source_defects=["stubs_removed"] if dropped_stub_count else [],
        )
        if not dry_run:
            sheet["backstory"] = preprocessed
            sheet["distillation_manifest"] = manifest
            sheet["distillation_metadata"] = manifest
        else:
            sheet["distilled_backstory_preview"] = preprocessed
            sheet["distillation_manifest"] = manifest
            sheet["distillation_metadata"] = manifest
        return sheet

    system_prompt, user_prompt = _build_distillation_prompt(
        name=name,
        age=age,
        country=country,
        backstory=preprocessed,
        max_chars=max_chars,
    )

    logger.info(
        "distill_persona_sheet_backstory: calling %s for %s age %d (preprocessed %d chars → target %d chars)",
        resolved_model, name, age, len(preprocessed), max_chars,
    )

    distilled = _call_llm(system_prompt, user_prompt, key, resolved_model)
    manifest_status = "clean"

    # Write durable LLM call artifacts when log_dir is provided
    if log_dir is not None and distilled:
        try:
            from v3.engine.llm_logging import log_llm_call
            provider = "deepseek" if resolved_model.startswith("deepseek") else "openai"
            log_llm_call(
                log_dir=log_dir,
                call_id=f"distill_memory_{name.replace(' ', '_').lower()[:20]}",
                provider=provider,
                model=resolved_model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                raw_response=distilled,
                status="ok",
                parse_status=manifest_status,
            )
        except Exception:
            pass

    if not distilled:
        logger.error("distill_persona_sheet_backstory: LLM returned empty string — keeping preprocessed")
        distilled = preprocessed
        manifest_status = "llm_empty_fallback"

    logger.info(
        "distill_persona_sheet_backstory: done. %d chars → %d chars",
        len(raw_backstory), len(distilled),
    )

    manifest = _distillation_manifest(
        model=resolved_model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        preprocessed=preprocessed,
        distilled=distilled,
        status=manifest_status,
        dropped_stub_count=dropped_stub_count,
        source_defects=([
            defect
            for defect in (
                "stubs_removed" if dropped_stub_count else "",
                "llm_empty_fallback" if manifest_status == "llm_empty_fallback" else "",
            )
            if defect
        ]),
    )

    if dry_run:
        sheet["distilled_backstory_preview"] = distilled
        sheet["_distill_preprocessed_chars"] = len(preprocessed)
        sheet["_distill_output_chars"] = len(distilled)
        sheet["distillation_manifest"] = manifest
        sheet["distillation_metadata"] = manifest
    else:
        sheet["backstory"] = distilled
        sheet["distillation_manifest"] = manifest
        sheet["distillation_metadata"] = manifest

    return sheet


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli_main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Distill a persona_sheet.json backstory into a layered literary palimpsest."
    )
    parser.add_argument("sheet_path", help="Path to persona_sheet.json")
    parser.add_argument(
        "--out", default=None,
        help="Output path (default: overwrite input file)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print distilled backstory without writing"
    )
    parser.add_argument(
        "--model", default=None,
        help="Override model (default: $SIM_MODEL or gpt-4o)"
    )
    parser.add_argument(
        "--max-chars", type=int, default=6000,
        help="Target character count for distilled backstory (default: 6000)"
    )
    parser.add_argument(
        "--preprocess-only", action="store_true",
        help="Only run the pre-processing step (strip stubs, dedup) — no LLM call"
    )
    args = parser.parse_args(argv)

    sheet_path = Path(args.sheet_path)
    if not sheet_path.exists():
        print(f"Error: {sheet_path} does not exist", file=sys.stderr)
        sys.exit(1)

    with sheet_path.open("r", encoding="utf-8") as f:
        sheet = json.load(f)

    if args.preprocess_only:
        raw = sheet.get("backstory", "")
        cleaned = _preprocess_backstory(raw)
        print(f"Raw: {len(raw)} chars → Preprocessed: {len(cleaned)} chars\n")
        print(cleaned)
        return

    # .env fallback
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parents[3] / ".env")
    except ImportError:
        pass

    result = distill_persona_sheet_backstory(
        sheet,
        model=args.model,
        max_chars=args.max_chars,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        preview = result.get("distilled_backstory_preview", "")
        pre_chars = result.get("_distill_preprocessed_chars", "?")
        out_chars = result.get("_distill_output_chars", "?")
        print(f"[dry-run] preprocessed: {pre_chars} chars → distilled: {out_chars} chars\n")
        print("=" * 60)
        print(preview)
        return

    out_path = Path(args.out) if args.out else sheet_path
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    identity = result.get("identity") or {}
    name = f"{identity.get('given_name', '')} {identity.get('family_name', '')}".strip()
    original_chars = len(sheet.get("backstory", ""))
    new_chars = len(result.get("backstory", ""))
    print(f"Distilled {name}: {original_chars} chars → {new_chars} chars → {out_path}")


if __name__ == "__main__":
    _cli_main()
