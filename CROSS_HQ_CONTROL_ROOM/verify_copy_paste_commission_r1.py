#!/usr/bin/env python3
"""Read-only pre-dispatch validator; format PASS is not execution, science, or authority."""
import argparse
import json
import re
from pathlib import Path

FIELDS = [
 "REPOSITORY", "AGENT_TYPE", "INTELLIGENCE_LEVEL", "SINGLE_AGENT_FULL_DELIVERABLE",
 "EXECUTION_SURFACE", "USER_SELECTED_EDITOR_MODEL_PAIR", "MODEL", "REASONING",
 "PROVIDER/EDITOR_HARNESS", "MODEL_MAX_AVAILABILITY", "HOST_ACCOUNT_QUOTA_COST",
 "BRANCH", "STARTUP_SHA", "ACTIVE_WORKER_NO_DISTURBANCE",
 "BROWSER?", "DEEPSEEK?", "CODEX_6_1_HIGH_NECESSARY?", "OTHERWISE_MIDDLE?",
 "WHY_NOT_BROWSER", "WHY_NOT_FLASH", "WHY_NOT_CODEX_HIGH", "WHY_NOT_MIDDLE",
 "SCIENCE_SOURCE_ACTOR_AUTHORITY", "POST_RETURN_INDEPENDENT_REVIEW",
]
ALLOWED_INTELLIGENCE = {"I0", "I1", "I2", "I3", "I3+"}
FENCE = re.compile(r"(?m)^'''([a-zA-Z0-9_-]*)[ \t]*$".replace("'''", chr(96)*3))
SHA = re.compile(r"^[0-9a-f]{40}$")


def validate(markdown: str):
    errors = []
    fences = list(FENCE.finditer(markdown))
    if len(fences) != 2:
        return {"schema": "RAWLSING_COPY_PASTE_COMMISSION_R1",
                "status": "RED_INVALID_FOR_DISPATCH",
                "errors": ["REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK"]}
    if fences[0].group(1).lower() != "text" or fences[1].group(1):
        errors.append("MUST_USE_TEXT_FENCE")
    prompt = markdown[fences[0].end():fences[1].start()].strip()
    if not prompt.startswith("LAUNCH"):
        errors.append("PROMPT_MUST_START_WITH_LAUNCH")
    if len(prompt) < 650:
        errors.append("PROMPT_INCOMPLETE")
    heading = markdown[:fences[0].start()]
    for label in ["AGENT TYPE", "INTELLIGENCE LEVEL"]:
        if not re.search(r"\b" + re.escape(label) + r"\b", heading, re.I):
            errors.append("NOT_VISIBLE_ABOVE_FENCE_" + label.replace(" ", "_"))
    lines = prompt.splitlines()[:55]
    header = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip() in FIELDS:
                header[key.strip()] = value.strip()
    for key in FIELDS:
        if not header.get(key) or header[key].upper() in {"TBD", "N/A", "NONE", "NULL", "?"}:
            errors.append("MISSING_OR_EMPTY_" + key)
    if header.get("INTELLIGENCE_LEVEL") not in ALLOWED_INTELLIGENCE:
        errors.append("INVALID_INTELLIGENCE_CLASS")
    if len(header.get("AGENT_TYPE", "")) < 15:
        errors.append("AGENT_TYPE_NOT_SPECIFIC")
    if not SHA.fullmatch(header.get("STARTUP_SHA", "")):
        errors.append("EXACT_40_HEX_STARTUP_REQUIRED")
    if not header.get("BRANCH", "").startswith(("agent/", "review/", "integration/", "proposal/")):
        errors.append("EXACT_BRANCH_REQUIRED")
    if header.get("SINGLE_AGENT_FULL_DELIVERABLE") != "YES":
        errors.append("SINGLE_AGENT_OWNERSHIP_REQUIRED")
    if not re.search(r"S[0-3](?:_|\b)", header.get("EXECUTION_SURFACE", "")):
        errors.append("S0_S3_EXECUTION_REQUIRED")
    for term in ["ENGINEERING", "SCIENTIFIC", "AUTHORITY"]:
        if term not in prompt.upper():
            errors.append("MISSING_THREE_COURT_" + term)
    for term in ["source", "review", "test", "return"]:
        if not re.search(r"\b" + term + r"\w*\b", prompt, re.I):
            errors.append("MISSING_COMPLETE_TASK_" + term.upper())
    return {"schema": "RAWLSING_COPY_PASTE_COMMISSION_R1",
            "status": "RED_INVALID_FOR_DISPATCH" if errors else "PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH",
            "errors": errors, "agent_type": header.get("AGENT_TYPE"),
            "intelligence_level": header.get("INTELLIGENCE_LEVEL"),
            "branch": header.get("BRANCH"), "prompt_chars": len(prompt)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file", type=Path)
    p.add_argument("--json-issue", action="store_true")
    args = p.parse_args()
    data = args.file.read_text(encoding="utf-8")
    if args.json_issue:
        data = json.loads(data).get("body") or ""
    result = validate(data)
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
