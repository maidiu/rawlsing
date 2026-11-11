#!/usr/bin/env python3
"""Read-only pre-dispatch validator; format PASS is not execution, science, or authority."""
import argparse
import json
import re
import hashlib
import csv
import subprocess
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
 "MCR", "COMMISSION_KIND", "CONTRACT_ID", "CONTRACT_SOURCE_CUT",
 "WORK_SCOPE_AND_FLIGHT",
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
    return {k: v.strip() for k, v in re.findall(r"(?:^|;)\s*([A-Z_]+)\s*=\s*([^;]+)", value)}


def _require_parts(header, key, names, errors):
    parts = _named_parts(header.get(key, ""))
    for name in names:
        value = parts.get(name, "")
        if len(value) < 12 or value.upper() in {"TBD", "TODO", "PLACEHOLDER", "TO_BE_DECIDED", "NONE"}:
            errors.append("MISSING_SPECIFIC_" + key + "_" + name)



# MCR-C: this lives in the existing launch checker. Never use the candidate's
# own format PASS as substantive or independent acceptance.
MCR_BEGIN = "MCR_COMPLETION_CONTRACT_BEGIN"
MCR_END = "MCR_COMPLETION_CONTRACT_END"
EVIDENCE_BEGIN = "MCR_COMPLETION_EVIDENCE_BEGIN"
EVIDENCE_END = "MCR_COMPLETION_EVIDENCE_END"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ID = re.compile(r"^[A-Z][A-Z0-9_-]{2,79}$")
BAD_UNICODE = re.compile(r"[\u00ad\u200b\u200c\u200d\u2060\ufeff]")
VAGUE = {"", "TBD", "TODO", "UNKNOWN", "N/A", "NONE", "PLACEHOLDER", "LATER",
         "TO BE DECIDED", "AS NEEDED", "SEE ABOVE"}
GRADES = {"S0": 0, "S1": 1, "S2": 2, "S3": 3}


def _specific(value, label, errors, minimum=16):
    if not isinstance(value, str) or len(value.strip()) < minimum or value.strip().upper() in VAGUE:
        errors.append("MCR_C_UNSPECIFIED_" + label)
        return False
    return True


def _safe_path(value):
    if not isinstance(value, str) or BAD_UNICODE.search(value) or "\\" in value:
        return False
    if not value or value.strip().upper() in VAGUE or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        return False
    return not any(c in {"", ".", ".."} for c in value.split("/"))


def _source_tuple(value, errors, label, check_git=False):
    if not isinstance(value, dict) or set(value) != {"path", "commit", "blob"}:
        errors.append("MCR_C_SOURCE_TUPLE_REQUIRED_" + label)
        return
    if not _safe_path(value["path"]):
        errors.append("MCR_C_UNSAFE_SOURCE_PATH_" + label)
    for k in ("commit", "blob"):
        if not isinstance(value[k], str) or not HEX40.fullmatch(value[k]):
            errors.append("MCR_C_INVALID_40HEX_" + k.upper() + "_" + label)
    if check_git and _safe_path(value["path"]) and all(
            isinstance(value[k], str) and HEX40.fullmatch(value[k])
            for k in ("commit", "blob")):
        try:
            actual = subprocess.run(
                ["git", "rev-parse", value["commit"] + ":" + value["path"]],
                capture_output=True, text=True, timeout=12, check=False,
            )
            if actual.returncode or actual.stdout.strip() != value["blob"]:
                errors.append("MCR_C_SOURCE_BLOB_MISMATCH_" + label)
        except (OSError, subprocess.TimeoutExpired):
            errors.append("MCR_C_SOURCE_BLOB_UNVERIFIED_" + label)


def _extract_block(text, begin, end, errors):
    if text.count(begin) != 1 or text.count(end) != 1:
        errors.append("MCR_C_MISSING_OR_DUPLICATE_BLOCK_" + begin)
        return ""
    first = text.index(begin) + len(begin)
    last = text.index(end)
    if first >= last:
        errors.append("MCR_C_REVERSED_BLOCK_" + begin)
        return ""
    return text[first:last].strip()


def _json_record(raw, prefix, errors):
    def reject_duplicates(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError("duplicate JSON key " + k)
            result[k] = v
        return result
    try:
        return json.loads(raw, object_pairs_hook=reject_duplicates)
    except (ValueError, TypeError) as e:
        errors.append("MCR_C_INVALID_JSON_" + prefix + ":" + str(e)[:75])
        return None


def completion_contract(prompt, errors, check_git=False):
    block = _extract_block(prompt, MCR_BEGIN, MCR_END, errors)
    if not block:
        return None
    records = {"MCR_SCOPE": [], "MCR_OBLIGATION": [], "MCR_RECEIVING": []}
    for line in block.splitlines():
        if not line.strip():
            continue
        key, sep, payload = line.strip().partition(":")
        if sep != ":" or key not in records:
            errors.append("MCR_C_UNKNOWN_CONTRACT_RECORD_" + key[:42])
            continue
        rec = _json_record(payload.strip(), key, errors)
        if isinstance(rec, dict):
            records[key].append(rec)
        else:
            errors.append("MCR_C_NONOBJECT_" + key)
    if len(records["MCR_SCOPE"]) != 1 or len(records["MCR_RECEIVING"]) != 1:
        errors.append("MCR_C_ONE_SCOPE_AND_RECEIVING_REQUIRED")
    if not records["MCR_OBLIGATION"]:
        errors.append("MCR_C_NO_OBLIGATIONS")
    if errors and (len(records["MCR_SCOPE"]) != 1 or len(records["MCR_RECEIVING"]) != 1):
        return None
    scope = records["MCR_SCOPE"][0]
    for k in ("parent", "enumerator", "no_drop_check"):
        _specific(scope.get(k), "SCOPE_" + k.upper(), errors, 20)
    if not isinstance(scope.get("expected_count"), int) or isinstance(scope.get("expected_count"), bool) or scope["expected_count"] < 1:
        errors.append("MCR_C_EXPECTED_COUNT_REQUIRED")
    _source_tuple(scope.get("source"), errors, "SCOPE", check_git)
    if scope.get("enumerator") == scope.get("no_drop_check"):
        errors.append("MCR_C_ENUMERATOR_NOT_NO_DROP_TEST")
    receiving = records["MCR_RECEIVING"][0]
    for k in ("gate", "independent_owner"):
        _specific(receiving.get(k), "RECEIVING_" + k.upper(), errors, 16)
    for k, expected in (
        ("all_obligations", "PASS_REQUIRED"),
        ("author_ceiling", "DELIVERED_PENDING_RECEIVING"),
        ("on_any_failure", "INCOMPLETE"),
    ):
        if receiving.get(k) != expected:
            errors.append("MCR_C_RECEIVING_FAIL_CLOSED_" + k.upper())
    ids = set()
    for i, ob in enumerate(records["MCR_OBLIGATION"]):
        label = "OBLIGATION_" + str(i + 1)
        oid = ob.get("id")
        if not isinstance(oid, str) or not ID.fullmatch(oid):
            errors.append("MCR_C_BAD_ID_" + label)
        elif oid in ids:
            errors.append("MCR_C_DUPLICATE_ID_" + oid)
        else:
            ids.add(oid)
        for k in ("result", "check", "positive", "negative", "consumer", "owner"):
            _specific(ob.get(k), label + "_" + k.upper(), errors, 16)
        if ob.get("positive") == ob.get("negative"):
            errors.append("MCR_C_NONDISCRIMINATING_ORACLE_" + label)
        if not isinstance(ob.get("positive"), str) or not ob["positive"].startswith("PASS="):
            errors.append("MCR_C_NO_EXPLICIT_PASS_EXPECTATION_" + label)
        if not isinstance(ob.get("negative"), str) or not ob["negative"].startswith("RED="):
            errors.append("MCR_C_NO_EXPLICIT_RED_EXPECTATION_" + label)
        for k in ("output", "evidence"):
            if not _safe_path(ob.get(k)):
                errors.append("MCR_C_UNSAFE_EXACT_PATH_" + label + "_" + k.upper())
        if ob.get("check_kind") not in ("EXEC", "SOURCE", "INDEPENDENT"):
            errors.append("MCR_C_INVALID_CHECK_KIND_" + label)
        if not isinstance(ob.get("check"), str) or not ob["check"].startswith(("RUN:", "SOURCE:", "COURT:")):
            errors.append("MCR_C_CHECK_NOT_EXPLICIT_" + label)
        elif ob["check_kind"] == "EXEC" and not ob["check"].startswith("RUN:"):
            errors.append("MCR_C_EXEC_WITHOUT_RUN_" + label)
        elif ob["check_kind"] == "SOURCE" and not ob["check"].startswith("SOURCE:"):
            errors.append("MCR_C_SOURCE_WITHOUT_TRACE_" + label)
        elif ob["check_kind"] == "INDEPENDENT" and not ob["check"].startswith("COURT:"):
            errors.append("MCR_C_INDEPENDENT_WITHOUT_COURT_" + label)
        if ob.get("minimum_grade") not in (*GRADES, "AUTHORITY"):
            errors.append("MCR_C_INVALID_GRADE_" + label)
        if ob.get("failure") != "INCOMPLETE":
            errors.append("MCR_C_MUST_FAIL_INCOMPLETE_" + label)
        _source_tuple(ob.get("source"), errors, label, check_git)
    # Catch an abbreviated SHA that a correctly shaped scope pin otherwise hides.
    # 30-39 hex candidates in authority text must be complete; 7-char casual labels
    # are not falsely presented as exact source identities.
    if re.search(r"(?<![0-9a-f])[0-9a-f]{30,39}(?![0-9a-f])", prompt, re.I):
        errors.append("MCR_C_ABBREVIATED_MATERIAL_HASH")
    if BAD_UNICODE.search(prompt):
        errors.append("MCR_C_INVISIBLE_CHARACTER_IN_LAUNCH")
    if isinstance(scope.get("expected_count"), int) and scope["expected_count"] > len(records["MCR_OBLIGATION"]):
        cols = scope.get("identity_columns")
        if not isinstance(cols, list) or not cols or any(
                not isinstance(c, str) or not c.strip() for c in cols):
            errors.append("MCR_C_FROZEN_IDENTITY_COLUMNS_REQUIRED")
        if not isinstance(scope.get("source"), dict) or not str(scope["source"].get("path", "")).endswith((".tsv", ".csv")):
            errors.append("MCR_C_FROZEN_IDENTITY_REGISTRY_REQUIRED")
    return {"scope": scope, "obligations": records["MCR_OBLIGATION"],
            "receiving": receiving, "sha256": hashlib.sha256(block.encode("utf-8")).hexdigest()}


def _git(root, *args):
    try:
        p = subprocess.run(["git", "-C", str(root), *args],
                           capture_output=True, timeout=25, check=False)
        return p.stdout if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def _committed_file(root, sha, path, errors, label):
    """Verify exact checkout blob, not an untracked or post-commit replacement."""
    if not _safe_path(path):
        errors.append("MCR_C_INVALID_COMMITTED_PATH_" + label)
        return None
    tracked = _git(root, "rev-parse", sha + ":" + path)
    current = _git(root, "hash-object", str(root / path))
    if not tracked or not current or tracked.strip() != current.strip():
        errors.append("MCR_C_OUTPUT_NOT_COMMITTED_AT_CANDIDATE_" + label)
        return None
    try:
        actual = root / path
        resolved = actual.resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
        return resolved.read_bytes()
    except (OSError, ValueError, RuntimeError):
        errors.append("MCR_C_MISSING_OR_ESCAPED_FILE_" + label)
        return None


def _verified_source_bytes(root, source, errors, label):
    if not isinstance(source, dict) or not all(k in source for k in ("path", "commit", "blob")):
        errors.append("MCR_C_SOURCE_MISSING_" + label)
        return None
    path, commit, blob = source["path"], source["commit"], source["blob"]
    if not (_safe_path(path) and isinstance(commit, str) and HEX40.fullmatch(commit)
            and isinstance(blob, str) and HEX40.fullmatch(blob)):
        errors.append("MCR_C_SOURCE_INVALID_" + label)
        return None
    actual = _git(root, "rev-parse", commit + ":" + path)
    if not actual or actual.strip().decode("ascii", "replace") != blob:
        errors.append("MCR_C_SOURCE_BLOB_UNVERIFIED_" + label)
        return None
    content = _git(root, "show", commit + ":" + path)
    if content is None:
        errors.append("MCR_C_SOURCE_CONTENT_UNAVAILABLE_" + label)
    return content


def _expected_id_set(root, contract, errors):
    scope = contract["scope"]
    count = scope["expected_count"]
    obligations = contract["obligations"]
    content = _verified_source_bytes(root, scope["source"], errors, "SCOPE")
    if content is None:
        return set()
    cols = scope.get("identity_columns")
    if not cols:
        ids = [ob["id"] for ob in obligations]
    else:
        try:
            data = content.decode("utf-8-sig")
            rdr = csv.DictReader(data.splitlines(), delimiter="\t" if scope["source"]["path"].endswith(".tsv") else ",")
            if not set(cols).issubset(set(rdr.fieldnames or [])):
                errors.append("MCR_C_EXPECTED_ID_COLUMNS_NOT_IN_SOURCE")
                return set()
            ids = [json.dumps([row[c] for c in cols], ensure_ascii=False, separators=(",", ":"))
                   for row in rdr]
        except (UnicodeError, csv.Error, KeyError, TypeError):
            errors.append("MCR_C_EXPECTED_IDS_UNREADABLE")
            return set()
    if len(ids) != count or len(set(ids)) != len(ids):
        errors.append("MCR_C_FROZEN_UNIVERSE_COUNT_OR_DUPLICATE_MISMATCH")
    return set(ids)


def verify_return(commission, returned, candidate_sha, root):
    """Only documentary author-evidence readiness. NEVER authoritative completion."""
    root = Path(root).resolve()
    errors = []
    initial = validate(commission)
    if initial["status"] != "PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH":
        return {"status": "RED_INCOMPLETE", "errors": initial["errors"]}
    if not isinstance(candidate_sha, str) or not HEX40.fullmatch(candidate_sha):
        return {"status": "RED_INCOMPLETE", "errors": ["EXACT_CANDIDATE_SHA_REQUIRED"]}
    actual_head = _git(root, "rev-parse", "HEAD")
    if not actual_head or actual_head.decode("ascii", "replace").strip() != candidate_sha:
        errors.append("MCR_C_CHECKOUT_NOT_EXACT_CANDIDATE")
    fences = list(FENCE.finditer(commission))
    contract = completion_contract(
        commission[fences[0].end():fences[1].start()].strip(), errors
    )
    if contract is None:
        return {"status": "RED_INCOMPLETE", "errors": errors}
    expected_ids = _expected_id_set(root, contract, errors)
    # Each per-obligation frozen source must resolve too; scope source alone
    # does not authenticate the potentially distinct scientific/code inputs.
    for obligation in contract["obligations"]:
        _verified_source_bytes(root, obligation["source"], errors, "OBLIGATION_" + obligation["id"])
    block = _extract_block(returned, EVIDENCE_BEGIN, EVIDENCE_END, errors)
    proof = {}
    coverage = []
    for line in block.splitlines():
        if not line.strip():
            continue
        key, sep, payload = line.strip().partition(":")
        if sep != ":" or key not in {"MCR_EVIDENCE", "MCR_COVERAGE"}:
            errors.append("MCR_C_INVALID_EVIDENCE_RECORD")
            continue
        obj = _json_record(payload.strip(), key, errors)
        if not isinstance(obj, dict):
            errors.append("MCR_C_BAD_EVIDENCE_OBJECT")
            continue
        if key == "MCR_COVERAGE":
            coverage.append(obj)
            continue
        if not isinstance(obj.get("id"), str):
            errors.append("MCR_C_EVIDENCE_ID_REQUIRED")
            continue
        if obj["id"] in proof:
            errors.append("MCR_C_DUPLICATE_EVIDENCE_" + obj["id"])
        proof[obj["id"]] = obj
    if len(coverage) != 1:
        errors.append("MCR_C_EXACT_ONE_SCOPE_COVERAGE_REQUIRED")
    else:
        cov = coverage[0]
        if cov.get("candidate_sha") != candidate_sha or cov.get("contract_sha256") != contract["sha256"]:
            errors.append("MCR_C_COVERAGE_WRONG_CANDIDATE_OR_CONTRACT")
        covered_path = cov.get("delivered_ids_file")
        payload = _committed_file(root, candidate_sha, covered_path, errors, "COVERAGE")
        if payload is not None:
            if hashlib.sha256(payload).hexdigest() != cov.get("delivered_ids_sha256"):
                errors.append("MCR_C_COVERAGE_DIGEST_MISMATCH")
            try:
                delivered_ids = [line for line in payload.decode("utf-8-sig").splitlines() if line]
            except UnicodeError:
                delivered_ids = []
                errors.append("MCR_C_COVERAGE_NOT_UTF8")
            if len(delivered_ids) != len(set(delivered_ids)):
                errors.append("MCR_C_COVERAGE_DUPLICATE_IDS")
            if len(delivered_ids) != contract["scope"]["expected_count"]:
                errors.append("MCR_C_COVERAGE_COUNT_MISMATCH")
            if set(delivered_ids) != expected_ids:
                errors.append("MCR_C_NO_DROP_SET_MISMATCH")
    required = {o["id"]: o for o in contract["obligations"]}
    if set(proof) != set(required):
        errors.extend("MCR_C_MISSING_PROOF_" + oid for oid in set(required) - set(proof))
        errors.extend("MCR_C_UNCONTRACTED_PROOF_" + oid for oid in set(proof) - set(required))
    for oid in set(required) & set(proof):
        ob, p = required[oid], proof[oid]
        if p.get("candidate_sha") != candidate_sha or p.get("contract_sha256") != contract["sha256"]:
            errors.append("MCR_C_PROOF_WRONG_CANDIDATE_OR_CONTRACT_" + oid)
        if p.get("status") != "PASS":
            errors.append("MCR_C_PROOF_NOT_PASS_" + oid)
        grade, minimum = p.get("grade"), ob["minimum_grade"]
        if (minimum == "AUTHORITY" and grade != "AUTHORITY") or (
            minimum in GRADES and (grade not in GRADES or GRADES[grade] < GRADES[minimum])
        ):
            errors.append("MCR_C_INSUFFICIENT_EVIDENCE_GRADE_" + oid)
        for label, key, hashkey, required_path in (
            ("EVIDENCE", "evidence_file", "evidence_sha256", ob["evidence"]),
            ("OUTPUT", "output_file", "output_sha256", ob["output"]),
        ):
            if p.get(key) != required_path:
                errors.append("MCR_C_" + label + "_PATH_MISMATCH_" + oid)
                continue
            payload = _committed_file(root, candidate_sha, required_path, errors, label + "_" + oid)
            if payload is not None and hashlib.sha256(payload).hexdigest() != p.get(hashkey):
                errors.append("MCR_C_" + label + "_DIGEST_MISMATCH_" + oid)
    return {
        "status": "RED_INCOMPLETE" if errors else "READY_FOR_INDEPENDENT_RECEIVING",
        "errors": sorted(set(errors)), "candidate_sha": candidate_sha,
        "contract_sha256": contract["sha256"],
        "verified_obligation_count": len(required) - len(set(required) - set(proof)),
        "expected_identity_count": contract["scope"]["expected_count"],
        "authority": "AUTHOR_EVIDENCE_COVERAGE_ONLY__NEVER_SELF_CERTIFIES_COMPLETE",
    }


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
    # MCR-C obligation-to-proof contract is a pre-dispatch requirement.
    contract = completion_contract(prompt, errors)
    # Structural checks cannot establish that the source, exception, runner or consumer is real.
    if header.get("MCR") != "REQUIRED":
        errors.append("MCR_REQUIRED_NOT_ATTESTED")
    kind = header.get("COMMISSION_KIND", "")
    if kind not in ALLOWED_KINDS:
        errors.append("INVALID_COMMISSION_KIND")
    if len(header.get("CONTRACT_ID", "")) < 8:
        errors.append("CONTRACT_ID_NOT_SPECIFIC")
    if not re.search(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])",
                     header.get("CONTRACT_SOURCE_CUT", "")):
        errors.append("CONTRACT_SOURCE_CUT_NOT_VERSION_PINNED")
    for key, names in [
        ("WORK_SCOPE_AND_FLIGHT", ["PARENT", "TRANCHE", "PILOT", "PARALLEL"]),
        ("TERMINAL_CONSUMER_AND_EFFECT", ["CONSUMER", "EFFECT"]),
        ("FROZEN_ORACLE_AND_COUNTEREXAMPLE", ["POS", "NEG"]),
        ("PREBUILD_CONTRACT_CHALLENGE", ["CHALLENGE", "DISPOSITION"]),
        ("EXECUTION_AND_AUTHOR_PREFLIGHT", ["RUNNER", "PREFLIGHT"]),
        ("CLOSURE_AND_OUT_OF_SCOPE", ["ACCEPT_AT", "EXCLUDE"]),
    ]:
        _require_parts(header, key, names, errors)
    # MCR-AF: the first case is a method check, never a terminal substitute
    # or universal serial barrier. This only recognizes explicit bad forms;
    # substantive mission conservation remains an HQ/reviewer obligation.
    scope = _named_parts(header.get("WORK_SCOPE_AND_FLIGHT", ""))
    pilot = scope.get("PILOT", "").upper()
    parallel = scope.get("PARALLEL", "").upper()
    if pilot and not (pilot.startswith("CALIBRATION_NONTERMINAL") or pilot.startswith("NOT_APPLICABLE")):
        errors.append("MCR_AF_PILOT_MUST_BE_NONTERMINAL")
    if parallel.startswith(("BLOCK_ALL", "SERIAL_FIRST_CASE", "NONE_UNTIL_PILOT_PASSES")):
        errors.append("MCR_AF_ARTIFICIAL_SERIAL_BARRIER")
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
            "branch": header.get("BRANCH"), "mcr": header.get("MCR"), "commission_kind": kind,
            "contract_id": header.get("CONTRACT_ID"),
            "mcr_completion_contract_sha256": contract["sha256"] if contract else None,
            "mcr_required_obligation_count": len(contract["obligations"]) if contract else 0,
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
            "MCR": "REQUIRED",
            "COMMISSION_KIND": kind,
            "CONTRACT_ID": "CASE-F03-AUTHORITY-CONSUMER",
            "CONTRACT_SOURCE_CUT": "src/legacy_v549b.py@" + "b" * 40,
            "WORK_SCOPE_AND_FLIGHT":
                "PARENT=complete governed Pyat world output; TRANCHE=selected consumer and all linked obligations; "
                "PILOT=CALIBRATION_NONTERMINAL selected F03 diagnostic; PARALLEL=READY independent source and consumer investigations",
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
        source = {"path": "CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py",
                  "commit": "b" * 40, "blob": "c" * 40}
        scope = {
            "parent": "Complete inherited commissioning contract at actual first consumer",
            "source": source, "expected_count": 2,
            "enumerator": "RUN: python3 tools/list_frozen_ids.py --exact-source",
            "no_drop_check": "RUN: python3 tools/compare_all_ids.py --reject-missing-and-extra",
        }
        obligations = [
            {"id": "EXACT-SOURCE-CUSTODY",
             "result": "Resolve all assigned source tuples against the frozen registry",
             "output": "WORKER_RETURNS/commission/source-custody.tsv",
             "check_kind": "SOURCE",
             "check": "SOURCE: git show pinned source commit:path and compare exact blob",
             "positive": "PASS=the exact source blob matches the frozen provenance tuple",
             "negative": "RED=an otherwise plausible 38-digit commit pin is rejected",
             "evidence": "WORKER_RETURNS/commission/custody-evidence.txt",
             "minimum_grade": "S1",
             "consumer": "Qualified ZAK-00 actual source custody receiver",
             "owner": "Separate qualified source engineering reviewer",
             "failure": "INCOMPLETE", "source": source},
            {"id": "CURRENT-CONSUMER-EFFECT",
             "result": "Demonstrate selected rule effect in the actual first consumer",
             "output": "WORKER_RETURNS/commission/consumer-effect.tsv",
             "check_kind": "EXEC",
             "check": "RUN: python3 tools/actual_first_reader_test.py --negative",
             "positive": "PASS=selected rule changes the chosen first reader output",
             "negative": "RED=removing selected-rule grant refuses the same output",
             "evidence": "WORKER_RETURNS/commission/consumer-evidence.txt",
             "minimum_grade": "S1",
             "consumer": "Qualified actual first reader of selected result",
             "owner": "Separate execution reviewer at exact frozen cut",
             "failure": "INCOMPLETE", "source": source},
        ]
        receiving = {
            "gate": "python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --verify-return",
            "independent_owner": "separate exact-head engineering receiver with owner rights",
            "all_obligations": "PASS_REQUIRED",
            "author_ceiling": "DELIVERED_PENDING_RECEIVING",
            "on_any_failure": "INCOMPLETE",
        }
        body = "LAUNCH exact authorized agent\n" + "\n".join(
            k + ": " + v for k, v in fields.items()
        ) + "\nENGINEERING SCIENTIFIC AUTHORITY source review test return\n"
        body += "MCR_COMPLETION_CONTRACT_BEGIN\n"
        body += "MCR_SCOPE: " + json.dumps(scope, sort_keys=True) + "\n"
        for obligation in obligations:
            body += "MCR_OBLIGATION: " + json.dumps(obligation, sort_keys=True) + "\n"
        body += "MCR_RECEIVING: " + json.dumps(receiving, sort_keys=True) + "\n"
        body += "MCR_COMPLETION_CONTRACT_END\n"
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
        ("no parent mission", change(build, "WORK_SCOPE_AND_FLIGHT",
          "PARENT=TBD; TRANCHE=complete source and consumer reconstruction; PILOT=CALIBRATION_NONTERMINAL diagnostic; PARALLEL=READY independent lanes")),
        ("no owned tranche", change(build, "WORK_SCOPE_AND_FLIGHT",
          "PARENT=whole world mandate; TRANCHE=TBD; PILOT=CALIBRATION_NONTERMINAL diagnostic; PARALLEL=READY independent lanes")),
        ("pilot falsely terminal", change(build, "WORK_SCOPE_AND_FLIGHT",
          "PARENT=whole world mandate; TRANCHE=all signed outputs; PILOT=TERMINAL first F03 case; PARALLEL=READY separate investigations")),
        ("first-case serial blockade", change(build, "WORK_SCOPE_AND_FLIGHT",
          "PARENT=whole world mandate; TRANCHE=all signed outputs; PILOT=CALIBRATION_NONTERMINAL diagnostic; PARALLEL=SERIAL_FIRST_CASE all other agents blocked")),
        ("missing parallel route", change(build, "WORK_SCOPE_AND_FLIGHT",
          "PARENT=whole world mandate; TRANCHE=all signed outputs; PILOT=CALIBRATION_NONTERMINAL diagnostic; PARALLEL=TBD")),
        ("MCR-C missing contract", build.replace("MCR_COMPLETION_CONTRACT_BEGIN", "MCR_WRONG_BEGIN")),
        ("MCR-C missing no-drop", build.replace('"no_drop_check": "RUN: python3 tools/compare_all_ids.py --reject-missing-and-extra"', '"no_drop_check": "TBD"')),
        ("MCR-C no obligations", re.sub(r"(?m)^MCR_OBLIGATION: .*\n", "", build)),
        ("MCR-C duplicate obligations", build.replace("MCR_RECEIVING:", 'MCR_OBLIGATION: ' +
          re.search(r"(?m)^MCR_OBLIGATION: (.*)$", build).group(1) + "\nMCR_RECEIVING:")),
        ("MCR-C truncated commit", build.replace('"commit": "' + "b" * 40 + '"', '"commit": "' + "b" * 38 + '"')),
        ("MCR-C bad output Unicode", build.replace("WORKER_RETURNS/commission/source-custody.tsv", "WORKER_RETURNS/commission/source\u00adcustody.tsv")),
        ("MCR-C nondiscriminating oracle", build.replace(
          "RED=an otherwise plausible 38-digit commit pin is rejected",
          "PASS=the exact source blob matches the frozen provenance tuple")),
        ("MCR-C self-certified completion", build.replace(
          '"author_ceiling": "DELIVERED_PENDING_RECEIVING"', '"author_ceiling": "COMPLETE_AT_CONTRACTED_SCOPE"')),
        ("MCR-C falsely downgraded failure", build.replace('"failure": "INCOMPLETE"', '"failure": "HOLD"', 1)),
        ("MCR-C missing receipt", build.replace('"evidence": "WORKER_RETURNS/commission/custody-evidence.txt"',
                                                  '"evidence": "TBD"')),
        ("missing MCR", change(build, "MCR", "TBD")),
        ("MCR advisory only", change(build, "MCR", "ADVISORY")),
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
    p.add_argument("--verify-return", type=Path)
    p.add_argument("--candidate-sha")
    p.add_argument("--evidence-root", type=Path, default=Path("."))
    p.add_argument("--source-check", action="store_true")
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
    if args.verify_return:
        if not args.candidate_sha:
            p.error("--candidate-sha is required with --verify-return")
        result = verify_return(data, args.verify_return.read_text(encoding="utf-8"),
                               args.candidate_sha, args.evidence_root)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "READY_FOR_INDEPENDENT_RECEIVING" else 2
    result = validate(data)
    # A structural-only PASS is never an actual dispatch credential.
    # The official CLI ALWAYS verifies real Git source blob paths/commits
    # when its format requirements pass. --source-check is retained as an
    # explicit backwards-compatible spelling of the same strict behavior.
    if result["status"].startswith("PASS"):
        checks = []
        fences = list(FENCE.finditer(data))
        completion_contract(data[fences[0].end():fences[1].start()].strip(), checks, check_git=True)
        if checks:
            result["status"] = "RED_INVALID_FOR_DISPATCH"
            result["errors"].extend(checks)
        else:
            result["validation_scope"] = "STRUCTURE_AND_GIT_SOURCE_BLOBS_ONLY__NOT_CONSUMER_PROOF"
    print(json.dumps(result, indent=2))
    return 0 if result["status"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
