#!/usr/bin/env python3
"""D4B authored strict overlay over the supplied R7 instrument.

This is a bounded private-package correction, NOT independent C, NOT H1,
NOT scientific/source/actor authority. It adds checks the active R7 path
lacks and exists only to demonstrate that named sabotage can be made RED.

Strict stages are: FRAME_STRICT, DECISION_STRICT, C_STRICT.
The original r7_integrated.check() runs first; its result is preserved.
"""
from __future__ import annotations
import hashlib, json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent / "PACKAGE"
sys.path.insert(0, str(PKG / "tools"))
import r7_integrated as base  # noqa: E402

MAN = json.loads((PKG / "03_FROZEN_SOURCE_CUTS.json").read_text())
BOUND = {x["id"]: x for x in json.loads((PKG / "02_BOUNDARY_CONTRACTS.json").read_text())["boundaries"]}
K3_PATH = MAN["k3_source_root"].rstrip("/") + "/"
HEX40 = re.compile(r"^[a-f0-9]{40}$")
HEX64 = re.compile(r"^[a-f0-9]{64}$")

BOILER = re.compile(
    r"(retained|preserved|see (above|record)|historical (meaning|record) kept|"
    r"no change|generic|placeholder|test-only)", re.I)
ACTOR_LEAK = re.compile(
    r"(survey|respondent|questionnaire|answer)[^.\n]{0,80}"
    r"(determines?|causes?|proves?|entitles?)[^.\n]{0,60}"
    r"(actor|person|motive|knowledge|perception|identity|ancestry|sect)", re.I)


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def k3_rows(repo_root: str) -> dict:
    """Exact raw row text + sha256 per K3 group/id, from the pinned protected blob."""
    out = {}
    snap = MAN["snapshot_sha"]
    for group, item in MAN["k3_files"].items():
        src = K3_PATH + item["file"]
        rev = subprocess.run(["git", "-C", repo_root, "rev-parse", f"{snap}:{src}"],
                             capture_output=True, text=True)
        if rev.returncode or rev.stdout.strip() != item["blob"]:
            raise RuntimeError(f"K3 blob mismatch {group}")
        cp = subprocess.run(["git", "-C", repo_root, "show", f"{snap}:{src}"],
                            capture_output=True, text=True)
        if cp.returncode:
            raise RuntimeError(f"K3 unreadable {group}")
        rows = {}
        for row in cp.stdout.splitlines()[1:]:
            if row.strip():
                rid = row.split("\t", 1)[0]
                rows[rid] = (row, _sha(row.encode()))
        out[group] = rows
    return out


def _load(root, ptr, code, errors):
    if not isinstance(ptr, dict):
        errors.append(code + ":NO_POINTER"); return None
    p = (pathlib.Path(root) / ptr.get("path", "")).resolve()
    rootp = pathlib.Path(root).resolve()
    if not str(p).startswith(str(rootp)) or not p.is_file():
        errors.append(code + ":ABSENT"); return None
    b = p.read_bytes()
    if _sha(b) != ptr.get("sha256"):
        errors.append(code + ":BYTES_CHANGED"); return None
    return json.loads(b)


def strict_history(frame, evidence_root, repo_root, errors):
    hist = _load(evidence_root, frame.get("historical_conservation"), "STRICT_HISTORY", errors)
    if hist is None:
        return
    actual = k3_rows(repo_root)
    for group in ("K1_CAP", "PYAT_PC", "P4R"):
        item = MAN["k3_files"][group]
        for rid in MAN["mandatory"][group]:
            rec = hist.get("coverage", {}).get(group, {}).get(rid)
            ctx = f"STRICT_K3:{group}:{rid}"
            if not isinstance(rec, dict):
                errors.append(ctx + ":MISSING"); continue
            if rec.get("original_source_blob") != item["blob"]:
                errors.append(ctx + ":BLOB_NOT_PINNED")
            row, rowsha = actual[group].get(rid, ("", ""))
            if rec.get("row_sha256") != rowsha:
                errors.append(ctx + ":ROW_HASH_NOT_SOURCE")
            ex = rec.get("source_row_excerpt")
            if not isinstance(ex, str) or len(ex) < 12 or ex not in row:
                errors.append(ctx + ":EXCERPT_NOT_IN_SOURCE_ROW")
            neg = rec.get("negative_meaning")
            STOP = {"preserved", "negative", "meaning", "record", "retained", "historical", "source", "generic"}
            negtok = set(re.findall(r"[a-z_]{6,}", (neg or "").lower())) - STOP
            rowtok = set(re.findall(r"[a-z_]{6,}", row.lower()))
            if not isinstance(neg, str) or len(neg.strip()) < 24 or len(negtok & rowtok) < 2:
                errors.append(ctx + ":NEGATIVE_NOT_BOUND_TO_SOURCE_VOCABULARY")
            if group == "PYAT_PC" and (rec.get("adopted") is not False or
                                       "NOT_ADOPTED" not in row.split("\t")[11]):
                errors.append(ctx + ":NOT_ADOPTED_NOT_CONSERVED")
            if group == "P4R" and (rec.get("closed") is not False or
                                   "HELD" not in row.split("\t")[8]):
                errors.append(ctx + ":P4R_HELD_NOT_CONSERVED")


def strict_design_coverage(decision, hist, errors):
    rows = decision.get("coverage_dispositions")
    if not isinstance(rows, list):
        errors.append("STRICT_DECISION:NO_118_COVERAGE_DISPOSITIONS"); return
    want = {(g, i) for g, ids in MAN["mandatory"].items() for i in ids}
    got = {(r.get("group"), r.get("id")) for r in rows if isinstance(r, dict)}
    if got != want or len(rows) != len(want):
        errors.append("STRICT_DECISION:118_COVERAGE_SET_DRIFT")
    seen = set()
    for r in rows:
        if not isinstance(r, dict):
            continue
        ctx = f"STRICT_118:{r.get('group')}:{r.get('id')}"
        if r.get("disposition") not in base.DISPOS:
            errors.append(ctx + ":BAD_DISPOSITION")
        if not isinstance(r.get("first_consumer"), str) or len(r["first_consumer"]) < 24:
            errors.append(ctx + ":NO_FIRST_CONSUMER")
        if not isinstance(r.get("owner"), str) or len(r["owner"]) < 6:
            errors.append(ctx + ":NO_OWNER")
        if r.get("evidence_grade") not in base.GRADES:
            errors.append(ctx + ":BAD_GRADE")
        arg = r.get("argument")
        if not isinstance(arg, str) or len(arg) < 30 or arg in seen or BOILER.fullmatch(arg.strip()):
            errors.append(ctx + ":BOILERPLATE_OR_NO_ARGUMENT")
        seen.add(arg)
        if r.get("negative_preserved") is not True:
            errors.append(ctx + ":NEGATIVE_NOT_ACCOUNTED")
    if len({r.get("first_consumer") for r in rows if isinstance(r, dict)}) < 3:
        errors.append("STRICT_DECISION:SINGLE_GENERIC_CONSUMER")


def strict_evidence_authority(frame, repo_root, expected_head, errors):
    """A content hash is not authority: require the exact Git blob at the protected head."""
    for row in frame.get("requirements", []):
        ev = row.get("evidence", {}) if isinstance(row, dict) else {}
        ctx = "STRICT_EVIDENCE:" + str(row.get("id"))
        blob = ev.get("git_blob")
        head = ev.get("protected_head")
        if not HEX40.fullmatch(str(blob)) or not HEX40.fullmatch(str(head)):
            errors.append(ctx + ":NOT_GIT_BLOB_ANCHORED"); continue
        if expected_head and head != expected_head:
            errors.append(ctx + ":BLOB_NOT_AT_LIVE_PROTECTED")
        cp = subprocess.run(["git", "-C", repo_root, "cat-file", "-p", blob],
                            capture_output=True)
        if cp.returncode:
            errors.append(ctx + ":BLOB_ABSENT"); continue
        if _sha(cp.stdout) != ev.get("sha256"):
            errors.append(ctx + ":FILE_HASH_IS_NOT_EXACT_BLOB_CONTENT")


def strict_boundaries(frame, errors):
    b = frame.get("boundary_contracts")
    if not isinstance(b, dict):
        errors.append("STRICT_FRAME:NO_BOUNDARY_CONTRACTS"); return
    if set(b) != set(BOUND):
        errors.append("STRICT_FRAME:BOUNDARY_SET_DRIFT")
    for tid, frozen in BOUND.items():
        x = b.get(tid, {})
        ctx = "STRICT_BOUNDARY:" + tid
        for f, fk in (("contract_name", "name"), ("producers", "producers"), ("receivers", "receivers"), ("must_preserve", "must_preserve"), ("veto", "veto"), ("time_class", "time_class"), ("owners", "owners")):
            if x.get(f) != frozen.get(fk):
                errors.append(ctx + ":REDEFINED_" + f)
        for f in ("positive", "negative", "restore", "first_consumer"):
            if not isinstance(x.get(f), str) or len(x[f]) < 30:
                errors.append(ctx + ":NO_" + f.upper())
        if x.get("status") not in {"ACTUAL_PROVED_AT_SCOPE", "SOURCE_STATIC_CONSERVED", "OWNER_HELD_FUTURE"}:
            errors.append(ctx + ":BAD_STATUS")
        if tid in base.FIRST3 if hasattr(base, "FIRST3") else tid in {"T1", "T2", "T3"}:
            if x.get("status") not in {"ACTUAL_PROVED_AT_SCOPE", "SOURCE_STATIC_CONSERVED"}:
                errors.append(ctx + ":P0_BOUNDARY_INOPERABLE")


def strict_grant_claims(packet, errors):
    """A textual assertion of a grant is not a grant; an owner receipt must exist."""
    txt = json.dumps(packet, ensure_ascii=False)
    if not re.search(r"(granted|authori[sz]ed in full|permission (is )?given|approved for all)", txt, re.I):
        return
    for row in packet.get("requirements", []) if isinstance(packet.get("requirements"), list) else []:
        blob = json.dumps(row, ensure_ascii=False)
        if not re.search(r"(granted|authori[sz]ed in full|permission (is )?given|approved for all)", blob, re.I):
            continue
        rec = row.get("grant_receipt")
        if not isinstance(rec, dict):
            errors.append("STRICT_GRANT:" + str(row.get("id")) + ":TEXTUAL_GRANT_WITHOUT_RECEIPT")
        else:
            if not all(isinstance(rec.get(k), str) and len(rec[k]) >= 8 for k in ("issuer", "artifact", "sha256")):
                errors.append("STRICT_GRANT:" + str(row.get("id")) + ":INCOMPLETE_RECEIPT")


def strict_actor_firewall(packet, stage, errors):
    if stage == "FRAME":
        txt = " ".join(str(r.get("substantive_requirement", "")) + " " + str(r.get("why_needed", ""))
                       for r in packet.get("requirements", []) if isinstance(r, dict))
    else:
        txt = " ".join(str(packet.get(k, "")) for k in
                       ("architecture_description", "entire_source_to_actor_dataflow",
                        "scientific_boundary_and_nonpreclusion"))
    for m in ACTOR_LEAK.finditer(txt):
        errors.append("STRICT_ACTOR:FORBIDDEN_SURVEY_TO_ACTOR_CAUSAL:" + m.group(0)[:90])
    fw = packet.get("actor_access_firewall")
    if isinstance(fw, dict):
        if fw.get("survey_to_actor_forbidden") is not True:
            errors.append("STRICT_ACTOR:FIREWALL_NOT_SET")
        for f in ("no_access_denial", "event_access", "owner"):
            if not isinstance(fw.get(f), str) or len(fw[f]) < 20:
                errors.append("STRICT_ACTOR:NO_" + f.upper())
    else:
        errors.append("STRICT_ACTOR:NO_FIREWALL")


def strict_release(decision, expected_head, errors):
    rel = decision.get("release")
    if not isinstance(rel, dict):
        errors.append("STRICT_RELEASE:NO_RELEASE_RECORD"); return
    if rel.get("status") not in {"CURRENT", "REVOKED", "SUSPENDED"}:
        errors.append("STRICT_RELEASE:BAD_STATUS")
    if not HEX40.fullmatch(str(rel.get("checked_against_protected_head", ""))):
        errors.append("STRICT_RELEASE:NO_PROTECTED_HEAD")
    elif expected_head and rel["checked_against_protected_head"] != expected_head:
        errors.append("STRICT_RELEASE:HEAD_NOT_LIVE_PROTECTED")
    vt = rel.get("revocation_test", {})
    if not isinstance(vt, dict) or any(not isinstance(vt.get(k), str) or len(vt[k]) < 20
                                       for k in ("positive", "negative", "restore")):
        errors.append("STRICT_RELEASE:NO_REVOCATION_TEST")
    if decision.get("grade") == "AUTHOR_PROPOSED_PENDING_C" and rel.get("status") != "CURRENT":
        errors.append("STRICT_RELEASE:READY_WITH_NONCURRENT_RELEASE")


def strict_builder(packet, source_root, errors):
    for card in packet.get("builder_cards", []):
        if not isinstance(card, dict) or card.get("grade") != "SPECIFICATION_CONSTRUCTION_READY":
            continue
        cmd = str(card.get("test_command", ""))
        rel = None
        for pref in ("python3 tools/", "python tools/"):
            if cmd.startswith(pref):
                rel = cmd[len(pref):].split()[0]
        if rel and not (pathlib.Path(source_root) / "tools" / rel).is_file():
            errors.append("STRICT_BUILDER:NONEXISTENT_TEST_COMMAND:" + rel)
        fc = card.get("first_consumer")
        if isinstance(fc, str) and ("/" not in fc and fc.endswith((".py", ".json"))):
            errors.append("STRICT_BUILDER:CONSUMER_IS_BARE_FILENAME")


def check(stage, packet, evidence_root, source_root, expected_head=None):
    errors = []
    if stage == "FRAME":
        r = base.check_frame(packet, evidence_root, source_root)
    elif stage == "DECISION":
        r = base.check_decision(packet, evidence_root, source_root)
    elif stage == "C_INTEGRATED":
        r = base.check_C(packet, evidence_root, source_root)
    else:
        return {"status": "RED", "errors": ["STRICT_STAGE_UNKNOWN"]}
    if r["status"] == "RED":
        return {"status": "RED", "errors": r["errors"], "base": r}
    try:
        repo = subprocess.run(["git", "-C", str(PKG), "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True).stdout.strip() or str(PKG)
        if stage == "FRAME":
            strict_history(packet, evidence_root, repo, errors)
            strict_evidence_authority(packet, repo, expected_head, errors)
            strict_boundaries(packet, errors)
            strict_actor_firewall(packet, "FRAME", errors)
            strict_grant_claims(packet, errors)
        if stage == "DECISION":
            frame = _load(evidence_root, packet.get("common_frame"), "STRICT_FRAME_LOAD", errors)
            if frame:
                hist = _load(evidence_root, frame.get("historical_conservation"), "STRICT_HISTORY", errors)
                if hist:
                    strict_design_coverage(packet, hist, errors)
                strict_actor_firewall(frame, "DECISION", errors)
                strict_grant_claims(frame, errors)
                strict_boundaries(frame, errors)
            strict_release(packet, expected_head, errors)
        if stage == "C_INTEGRATED":
            strict_builder(packet, source_root, errors)
    except Exception as e:  # noqa: BLE001
        errors.append("STRICT_OVERLAY_ERROR:" + type(e).__name__ + ":" + str(e)[:120])
    return {"status": "RED" if errors else "PASS_STRICT_LOCAL_ONLY", "errors": sorted(set(errors)), "base": r}
