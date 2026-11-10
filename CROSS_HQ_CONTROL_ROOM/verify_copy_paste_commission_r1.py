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
CONTRACT_FIELDS = [
 "COMMISSION_KIND", "CONTRACT_ID", "CONTRACT_SOURCE_CUT",
 "TERMINAL_CONSUMER_AND_EFFECT", "FROZEN_ORACLE_AND_COUNTEREXAMPLE",
 "PREBUILD_CONTRACT_CHALLENGE", "EXECUTION_AND_AUTHOR_PREFLIGHT",
 "CLOSURE_AND_OUT_OF_SCOPE",
]
REPAIR_FIELDS = [
 "FROZEN_FAILED_CLAIM", "REPRODUCER_AND_ROOT_CAUSE",
 "AFFECTED_DEPENDENCIES", "REGRESSION_AND_DELTA_REVIEW",
]
ALLOWED_KINDS = {"BUILD", "REPAIR", "REVIEW", "INVESTIGATION", "DOCUMENTARY"}
ALLOWED_INTELLIGENCE = {"I0", "I1", "I2", "I3", "I3+"}
FENCE = re.compile(r"(?m)^'''([a-zA-Z0-9_-]*)[ \t]*$".replace("'''", chr(96)*3))
SHA = re.compile(r"^[0-9a-f]{40}$")


def _named_parts(value: str):
    """Validate structural specificity, not the semantic truth of a source claim."""
    return {k: v.strip() for k, v in re.findall(r"(?:^|;)\\s*([A-Z_]+)\\s*=\\s*([^;]+)", value)}


def _require_parts(header, key, names, errors):
    parts = _named_parts(header.get(key, ""))
    for name in names:
        value = parts.get(name, "")
        if len(value) < 12 or value.upper() in {"TBD", "TODO", "PLACEHOLDER", "TO_BE_DECIDED", "NONE"}:
            errors.append("MISSING_SPECIFIC_" + key + "_" + name)


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
    lines = prompt.splitlines()[:100]
    header = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip() in FIELDS + CONTRACT_FIELDS + REPAIR_FIELDS:
                header[key.strip()] = value.strip()
    for key in FIELDS + CONTRACT_FIELDS:
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
    # Structural checks cannot establish that the source, exception, runner or consumer is real.
    kind = header.get("COMMISSION_KIND", "")
    if kind not in ALLOWED_KINDS:
        errors.append("INVALID_COMMISSION_KIND")
    if len(header.get("CONTRACT_ID", "")) < 8:
        errors.append("CONTRACT_ID_NOT_SPECIFIC")
    if not re.search(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])",
                     header.get("CONTRACT_SOURCE_CUT", "")):
        errors.append("CONTRACT_SOURCE_CUT_NOT_VERSION_PINNED")
    for key, names in [
        ("TERMINAL_CONSUMER_AND_EFFECT", ["CONSUMER", "EFFECT"]),
        ("FROZEN_ORACLE_AND_COUNTEREXAMPLE", ["POS", "NEG"]),
        ("PREBUILD_CONTRACT_CHALLENGE", ["CHALLENGE", "DISPOSITION"]),
        ("EXECUTION_AND_AUTHOR_PREFLIGHT", ["RUNNER", "PREFLIGHT"]),
        ("CLOSURE_AND_OUT_OF_SCOPE", ["ACCEPT_AT", "EXCLUDE"]),
    ]:
        _require_parts(header, key, names, errors)
    if kind == "REPAIR":
        for key in REPAIR_FIELDS:
            if not header.get(key) or header[key].upper() in {"TBD", "N/A", "NONE", "NULL", "?"}:
                errors.append("MISSING_OR_EMPTY_" + key)
        if not re.search(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])",
                         header.get("FROZEN_FAILED_CLAIM", "")):
            errors.append("REPAIR_FAILED_CLAIM_NOT_FROZEN")
        for key, names in [
            ("REPRODUCER_AND_ROOT_CAUSE", ["REPRO", "ROOT_CAUSE"]),
            ("AFFECTED_DEPENDENCIES", ["IMPACT", "PRESERVE"]),
            ("REGRESSION_AND_DELTA_REVIEW", ["REGRESSION", "REVIEW_SCOPE"]),
        ]:
            _require_parts(header, key, names, errors)
    return {"schema": "RAWLSING_COPY_PASTE_COMMISSION_R1",
            "status": "RED_INVALID_FOR_DISPATCH" if errors else "PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH",
            "errors": errors, "agent_type": header.get("AGENT_TYPE"),
            "intelligence_level": header.get("INTELLIGENCE_LEVEL"),
            "branch": header.get("BRANCH"), "commission_kind": kind,
            "contract_id": header.get("CONTRACT_ID"),
            "validation_scope": "STRUCTURE_ONLY__NO_SEMANTIC_OR_EXECUTION_CLAIM",
            "prompt_chars": len(prompt)}



def self_test():
    """Positive format fixtures and targeted faults; not original source execution."""
    base = {key: "SPECIFIC_QUALIFIED_FIELD_WITH_SOURCE_OR_SCOPE" for key in FIELDS}
    base.update({
        "AGENT_TYPE": "bounded implementation engineer",
        "INTELLIGENCE_LEVEL": "I3",
        "SINGLE_AGENT_FULL_DELIVERABLE": "YES",
        "BRANCH": "agent/contract-fixture-only",
        "STARTUP_SHA": "a" * 40,
        "EXECUTION_SURFACE": "S0_S1",
    })
    def fixture(kind):
        fields = dict(base)
        fields.update({
            "COMMISSION_KIND": kind,
            "CONTRACT_ID": "CASE-F03-AUTHORITY-CONSUMER",
            "CONTRACT_SOURCE_CUT": "src/legacy_v549b.py@" + "b" * 40,
            "TERMINAL_CONSUMER_AND_EFFECT":
                "CONSUMER=actual Pyat query reader; EFFECT=selected rule controls output",
            "FROZEN_ORACLE_AND_COUNTEREXAMPLE":
                "POS=selected rule changes observed result; NEG=severed selector must deny result",
            "PREBUILD_CONTRACT_CHALLENGE":
                "CHALLENGE=reporter-only branch is missed; DISPOSITION=inspect actual conditional exception",
            "EXECUTION_AND_AUTHOR_PREFLIGHT":
                "RUNNER=verified authorized Python checkout; PREFLIGHT=execute selected consumer and negative",
            "CLOSURE_AND_OUT_OF_SCOPE":
                "ACCEPT_AT=bounded S0 and S1 evidence; EXCLUDE=original native respondent authority",
        })
        if kind == "REPAIR":
            fields.update({
                "FROZEN_FAILED_CLAIM": "F03 claim@" + "c" * 40,
                "REPRODUCER_AND_ROOT_CAUSE":
                    "REPRO=reporter branch throws exception; ROOT_CAUSE=author missed 50th candidate branch",
                "AFFECTED_DEPENDENCIES":
                    "IMPACT=affected reporter output only; PRESERVE=unchanged question scoring",
                "REGRESSION_AND_DELTA_REVIEW":
                    "REGRESSION=add reporter counterexample to suite; REVIEW_SCOPE=source exception and related output",
            })
        body = "LAUNCH exact authorized agent\n" + "\n".join(
            k + ": " + v for k, v in fields.items()
        ) + "\nENGINEERING SCIENTIFIC AUTHORITY source review test return\n"
        fence = chr(96) * 3
        return ("AGENT TYPE: bounded implementation engineer\nINTELLIGENCE LEVEL: I3\n"
                + fence + "text\n" + body + fence + "\n")
    def change(markdown, key, value):
        return re.sub(r"(?m)^" + re.escape(key) + r":.*$", key + ": " + value, markdown, count=1)
    positives = {}
    for kind in ["BUILD", "REPAIR", "REVIEW", "INVESTIGATION", "DOCUMENTARY"]:
        out = validate(fixture(kind))
        if not out["status"].startswith("PASS"):
            raise AssertionError("VALID_FIXTURE_REJECTED " + kind + " " + repr(out["errors"]))
        positives[kind] = out["status"]
    build, repair = fixture("BUILD"), fixture("REPAIR")
    negatives = [
        ("missing source", change(build, "CONTRACT_SOURCE_CUT", "TBD")),
        ("unversioned source", change(build, "CONTRACT_SOURCE_CUT", "src/no-pin.py")),
        ("no consumer", change(build, "TERMINAL_CONSUMER_AND_EFFECT", "CONSUMER=TBD; EFFECT=rule changes output")),
        ("no negative", change(build, "FROZEN_ORACLE_AND_COUNTEREXAMPLE", "POS=expected output is observed; NEG=TBD")),
        ("no positive", change(build, "FROZEN_ORACLE_AND_COUNTEREXAMPLE", "POS=TBD; NEG=source rule must refuse")),
        ("no challenge", change(build, "PREBUILD_CONTRACT_CHALLENGE", "CHALLENGE=TBD; DISPOSITION=inspect source branch")),
        ("no preflight", change(build, "EXECUTION_AND_AUTHOR_PREFLIGHT", "RUNNER=verified checkout exists; PREFLIGHT=TBD")),
        ("no closure", change(build, "CLOSURE_AND_OUT_OF_SCOPE", "ACCEPT_AT=bounded evidence only; EXCLUDE=TBD")),
        ("invalid work kind", change(build, "COMMISSION_KIND", "UNKNOWN")),
        ("repair no frozen claim", change(repair, "FROZEN_FAILED_CLAIM", "unversioned reference")),
        ("repair no reproducer", change(repair, "REPRODUCER_AND_ROOT_CAUSE", "REPRO=TBD; ROOT_CAUSE=branch missing from analysis")),
        ("repair no cause", change(repair, "REPRODUCER_AND_ROOT_CAUSE", "REPRO=source exception observed; ROOT_CAUSE=TBD")),
        ("repair no impact", change(repair, "AFFECTED_DEPENDENCIES", "IMPACT=TBD; PRESERVE=all other case types")),
        ("repair no regression", change(repair, "REGRESSION_AND_DELTA_REVIEW", "REGRESSION=TBD; REVIEW_SCOPE=actual changed source")),
        ("repair no review scope", change(repair, "REGRESSION_AND_DELTA_REVIEW", "REGRESSION=add real reporter-case test; REVIEW_SCOPE=TBD")),
    ]
    for name, mutated in negatives:
        if validate(mutated)["status"] != "RED_INVALID_FOR_DISPATCH":
            raise AssertionError("NEGATIVE_FALSE_PASS " + name)
    return {"status": "PASS_SELF_TEST", "positive_kinds": positives,
            "negative_mutations_rejected": len(negatives),
            "scope": "format oracle only; not native source, science or runtime proof"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file", type=Path, nargs="?")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--json-issue", action="store_true")
    args = p.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2))
        return 0
    if args.file is None:
        p.error("a commission file is required unless --self-test is used")
    data = args.file.read_text(encoding="utf-8")
    if args.json_issue:
        data = json.loads(data).get("body") or ""
    result = validate(data)
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
